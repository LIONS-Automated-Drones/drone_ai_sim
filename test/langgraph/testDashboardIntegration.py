import asyncio
import os
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

from tools import get_tools
from graph import build_graph

import io
from contextlib import redirect_stdout
from websockets.asyncio.client import connect

#

# Load environment variables from .env file
load_dotenv()

# --- 1. Setup the Agent ---
tools = get_tools()
tool_names = [tool.name for tool in tools]
llm = ChatOpenAI(
    model=os.getenv("OLLAMA_MODEL"),
    openai_api_base=os.getenv("OLLAMA_BASE_URL") + "/v1",
    openai_api_key="ollama",
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

# --- Main with connecting to the React Dashboard ---
async def main():
    print("--- Starting LangGraph Test ---")
    prompt_count = 1

    async with connect("ws://192.168.56.1:12691") as websocket: # Use your localhost IP address within VirtualBox here
        buffer = io.StringIO()
        while True:
            mission_prompt = await websocket.recv()
            if mission_prompt.lower() in ["quit", "exit"]:
                break
            with redirect_stdout(buffer):
                async for event in app.astream({"messages": [HumanMessage(content=mission_prompt)]}):
                    for v in event.values():
                        if "messages" in v:
                            print(v["messages"][-1].content)
            captured = buffer.getvalue()
            print(captured)
            await websocket.send(captured)
            buffer.seek(0)
            buffer.truncate(0)
            print(f"\nPrompt {prompt_count} Completed Successfully!")
            prompt_count += 1

if __name__ == "__main__":
    asyncio.run(main())