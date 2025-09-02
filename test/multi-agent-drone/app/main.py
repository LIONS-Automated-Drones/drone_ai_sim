# app/main.py
import asyncio
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from graph import build_graph

# Load environment variables
load_dotenv(dotenv_path='../.env')

async def main():
    app = build_graph()
    print("--- Multi-Agent Drone System Initialized ---")
    print("--- Gazebo simulation should be running via Docker Compose ---")
    
    while True:
        mission = input("Enter your mission: ")
        if mission.lower() in ["quit", "exit"]:
            break

        events = app.astream(
            {"messages": [HumanMessage(content=mission)]}
        )

        async for event in events:
            for key, value in event.items():
                if key != "__end__":
                    print(f"--- Event: {key} ---")
                    if "messages" in value:
                        last_message = value['messages'][-1]
                        if last_message.tool_calls:
                             print(f"Tool Call: {last_message.tool_calls[0]['name']} with args {last_message.tool_calls[0]['args']}")
                        else:
                             print(f"Message: {last_message.content}")

if __name__ == "__main__":
    asyncio.run(main())