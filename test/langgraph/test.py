import asyncio
import os
from dotenv import load_dotenv
import websockets
import socket
import json

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
        ("system", "You are a drone pilot AI with computer vision capabilities. Your job is to execute the user's mission by calling tools one at a time. Think step-by-step. "
         "\n\nVISION CAPABILITIES:"
         "\n- You have a 'sense_objects' tool that uses YOLO object detection to see what's around you"
         "\n- Use this tool whenever asked 'what do you see?', 'look around', 'detect objects', etc."
         "\n- Detected objects are stored in your world memory with their 3D map coordinates"
         "\n- Your world model will be shown to you automatically when objects are detected"
         "\n\nIMPORTANT RULES:"
         "\n- Call tools ONE AT A TIME using the proper tool-calling feature"
         "\n- NEVER write JSON in your text responses - use tool calls instead"
         "\n- When the mission is complete, call 'mission_complete' with a summary"
         "\n\nNow execute the user's request."),
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
        # Initialize state with empty world memory
        initial_state = {
            "messages": [HumanMessage(content=mission_prompt)],
            "world_memory": {}
        }
        mission_log(f"--- Starting mission with prompt: {mission_prompt}")
        async for event in app.astream(initial_state):
            mission_log(f"--- Graph event: {list(event.keys())}")
            if not cancel_flag.is_set():
                for v in event.values():
                    if not cancel_flag.is_set():
                        if "messages" in v:
                            last_msg = v["messages"][-1]
                            mission_log(f"--- Message type: {type(last_msg).__name__}")
                            message_content = last_msg.content
                            if message_content:
                                mission_log(f"--- Sending message: {message_content[:100]}...")
                                await send_message_callback(message_content)
                            # Log tool calls if present
                            if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                                mission_log(f"--- Tool calls detected: {[tc['name'] for tc in last_msg.tool_calls]}")
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
    except Exception as e:
        error_msg = f"Error during mission execution: {str(e)}"
        mission_log(f"--- {error_msg}")
        import traceback
        mission_log(traceback.format_exc())
        await send_message_callback(f"Mission failed: {str(e)}")
    finally:
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
                if current_mission_task:
                    current_mission_task.cancel()

            # Handle start_nav command
            elif msg == "start_nav":
                print("Received START_NAV signal from dashboard.")
                success = await drone_service.start_nav_control()
                if success:
                    await websocket.send("Nav2 control started. Drone will follow /cmd_vel commands.")
                else:
                    await websocket.send("Failed to start Nav2 control. Is the drone connected?")
            # Handle stop_nav command
            elif msg == "stop_nav":
                print("Received STOP_NAV signal from dashboard.")
                success = await drone_service.stop_nav_control()
                if success:
                    await websocket.send("Nav2 control stopped. Drone is holding position.")
                else:
                    await websocket.send("Failed to stop Nav2 control.")
            # If there's a mission already running, reject new mission
            elif mission_running.is_set():
                # Optionally cancel the previous mission or inform the client
                print("Mission already running, cannot process command...")
                await websocket.send("Please cancel the previous mission or wait for it to complete before sending additional mission commands.")
            else:
                # Start new mission as background task
                print(f"Starting mission: {message}")
                mission_running.set()
                current_mission_task = asyncio.create_task(handle_mission(message, websocket.send))
    except websockets.exceptions.ConnectionClosed:
        print("React dashboard disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")
        try:
            await websocket.send(f"Error: {e}")
        except:
            pass  # Connection might be closed

async def velocity_listener():
    """
    UDP listener that receives velocity commands from cmd_vel_bridge ROS node.
    Runs as a background task and updates drone_service velocity.
    """
    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 6000))
    sock.setblocking(False)  # Non-blocking for asyncio
    
    print("--- Velocity listener started on UDP port 6000 ---")
    
    loop = asyncio.get_event_loop()
    
    try:
        while True:
            try:
                # Receive data (non-blocking)
                data, addr = await loop.sock_recvfrom(sock, 1024)
                
                # Parse JSON
                velocity_data = json.loads(data.decode())
                
                # Update drone_service
                drone_service.update_nav_velocity(
                    linear_x=velocity_data.get("linear_x", 0.0),
                    linear_y=velocity_data.get("linear_y", 0.0),
                    linear_z=velocity_data.get("linear_z", 0.0),
                    angular_x=velocity_data.get("angular_x", 0.0),
                    angular_y=velocity_data.get("angular_y", 0.0),
                    angular_z=velocity_data.get("angular_z", 0.0)
                )
                
            except json.JSONDecodeError as e:
                print(f"Error decoding velocity data: {e}")
            except Exception as e:
                print(f"Error in velocity listener: {e}")
                await asyncio.sleep(0.01)  # Brief pause on error
    except asyncio.CancelledError:
        print("--- Velocity listener stopped ---")
    finally:
        sock.close()

async def run_websocket_server():
    """Starts the WebSocket server and velocity listener."""
    # Start the velocity listener as a background task
    velocity_task = asyncio.create_task(velocity_listener())
    
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