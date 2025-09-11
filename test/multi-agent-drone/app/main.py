# app/main.py
import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from graph import build_graph

# Load environment variables
#load_dotenv(dotenv_path='../.env')
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

async def main():
    app = build_graph()
    print("--- Multi-Agent Drone System Initialized ---")
    print("--- Gazebo simulation should be running via Docker Compose ---")
    
    while True:
        mission = input("Enter your mission: ")
        if mission.lower() in ["quit", "exit"]:
            break

        events = app.astream({"messages": [HumanMessage(content=mission)]})

        async for event in events:
            for key, value in event.items():
                if key != "__end__":
                    print(f"--- Event: {key} ---")
                    if "messages" in value and value["messages"]:
                        last_message = value["messages"][-1]
                        if isinstance(last_message, AIMessage):
                            if getattr(last_message, "tool_calls", None):
                                tc = last_message.tool_calls[0]
                                print(f"Tool Call: {tc['name']} with args {tc['args']}")
                            else:
                                print(f"Message: {last_message.content}")
                        elif isinstance(last_message, ToolMessage):
                            print(f"Tool Result: {last_message.content}")
                        else:
                            print(getattr(last_message, "content", ""))

if __name__ == "__main__":
    asyncio.run(main())