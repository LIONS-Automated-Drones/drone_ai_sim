import asyncio
import os
from dotenv import load_dotenv
import websockets

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from tools import get_tools, drone_service
from graph import build_graph
from mission_log import set_websocket_callback, mission_log
from environment_settings import ENVIRONMENT_SETTINGS
# --- 1. Setup the Agent ---
tools = get_tools()
tool_names = [tool.name for tool in tools]
llm = ChatOpenAI(
    model=ENVIRONMENT_SETTINGS.openrouter_model,
    openai_api_base=ENVIRONMENT_SETTINGS.openrouter_base_url,
    openai_api_key=ENVIRONMENT_SETTINGS.openrouter_api_key,
    temperature=0,
)

agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a drone pilot AI. Your job is to execute the user's mission by calling tools one at a time. Think step-by-step. When the entire mission is complete, and only then, call the 'mission_complete' tool with a summary of what you did. You MUST NOT include JSON in your text responses. To execute an action, you MUST use the tool-calling feature exclusively."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

agent = agent_prompt | llm.bind_tools(tools)

# --- 2. Build and Run the Graph ---
app = build_graph(agent, tool_names)

# --- 3. Set up global variables ---
cancel_flag = asyncio.Event()
mission_running = asyncio.Event()
manual_override_engaged = asyncio.Event()

async def handle_mission(mission_prompt, send_message_callback):
    """Handles a single mission prompt, streaming back results."""
    try:
        async for event in app.astream({"messages": [HumanMessage(content=mission_prompt)]}):
            if not cancel_flag.is_set():
                for v in event.values():
                    if not cancel_flag.is_set():
                        if "messages" in v:
                            message_content = v["messages"][-1].content
                            if message_content:
                                await send_message_callback(message_content)
                    else:
                        await send_message_callback("Canceling the current mission")
                        mission_log("Cancel flag is set, terminating")
                        await drone_service.cancel()
                        break
            else:
                await send_message_callback("Canceling the current mission")
                mission_log("Cancel flag is set, terminating")
                await drone_service.cancel()
                break
    except asyncio.CancelledError:
        await drone_service.cancel()
        await send_message_callback("Canceling the current mission")
        mission_log("Mission forcibly cancelled")
    mission_running.clear()
    cancel_flag.clear()
    mission_log("Mission completed")


async def websocket_handler(websocket):
    """Handles WebSocket connections and messages."""
    global cancel_flag
    global mission_running
    global manual_override_engaged
    global drone_service

    cancel_flag.clear()
    mission_running.clear()
    manual_override_engaged.clear()

    current_mission_task = None

    print("React dashboard connected.")
    set_websocket_callback(websocket.send)
    try:
        async for message in websocket:
            msg = message.strip().lower()
            # Reset the manual override flag if the dashboard sends "restart"
            if msg == "restart":
                print("Received RESTART signal from dashboard.")
                manual_override_engaged.clear()
                await websocket.send("Manual override disengaged.")
            # Check if manual override is engaged
            elif manual_override_engaged.is_set():
                print("Manual override still engaged. Ignoring message...")
                await websocket.send("Manual override is still engaged. Please deactivate before continuing.")
            # Set cancel_flag if the dashboard sends "cancel", either by the manual override button or through the chatbox
            elif msg == "cancel":
                print("Received CANCEL signal from dashboard.")
                cancel_flag.set()
                manual_override_engaged.set()
                await websocket.send("Mission cancellation requested. Entering manual override...")
                await drone_service.cancel()
                try:
                    current_mission_task.cancel()
                finally:
                    continue
            # If there's a mission already running, reject new mission
            elif mission_running.is_set():
                # Optionally cancel the previous mission or inform the client
                print("Mission already running, cannot process command...")
                await websocket.send("Please cancel the previous mission or wait for it to complete before sending additional mission commands.")
            else:
                # Start new mission as background task
                print(f"Starting mission: {message}")
                current_mission_task = asyncio.create_task(handle_mission(message, websocket.send))
            print(f"Received mission from dashboard: {message}")
            await handle_mission(message, websocket.send)
    except websockets.exceptions.ConnectionClosed:
        print("React dashboard disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            await websocket.send(f"Error: {e}")
        except:
            pass  # Connection might be closed

async def run_websocket_server():
    """Starts the WebSocket server."""
    async with websockets.serve(websocket_handler, ENVIRONMENT_SETTINGS.server_address, ENVIRONMENT_SETTINGS.server_port):
        print(f"--- WebSocket server started at ws://{ENVIRONMENT_SETTINGS.server_address}:{ENVIRONMENT_SETTINGS.server_port} ---")
        await asyncio.Future()  # Run forever

async def run_cli():
    """Runs the command-line interface."""
    print("--- Starting LangGraph Test (CLI Mode) ---")
    prompt_count = 1
    while True:
        mission_prompt = input(f"Enter Prompt {prompt_count}: ")
        if mission_prompt.lower() in ["quit", "exit"]:
            break

        async def cli_send(message):
            print(message)

        await handle_mission(mission_prompt, cli_send)
        
        print(f"\nPrompt {prompt_count} Completed Successfully!")
        prompt_count += 1

async def main():
    if ENVIRONMENT_SETTINGS.use_react:
        await run_websocket_server()
    else:
        await run_cli()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- Exiting ---")