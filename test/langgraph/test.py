import asyncio
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from tools import get_tools
from graph import build_graph

# Load environment variables from .env file
load_dotenv()

# --- 1. Setup the Agent ---
tools = get_tools()
llm = ChatOpenAI(
    model=os.getenv("OLLAMA_MODEL"),
    openai_api_base=os.getenv("OLLAMA_BASE_URL") + "/v1",
    openai_api_key="ollama",
    temperature=0,
)

# The agent's "brain" that decides which tool to call
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a drone pilot AI. Your job is to call the correct tools to execute the user's mission. Respond with a final summary when the mission is complete."),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- 2. Build and Compile the Graph ---
app = build_graph(agent_executor)

# --- 3. Run the Test ---
async def main():
    print("--- Starting LangGraph Test ---")
    prompt_count = 1
    while True:
        mission_prompt = input(f"Enter Prompt {prompt_count}: ")
        if mission_prompt.lower() in ["quit", "exit"]:
            break

        # astream() lets us see the output of each node as it runs
        async for event in app.astream({"messages": [HumanMessage(content=mission_prompt)]}):
            # Print the final result from the agent node
            if "agent" in event:
                print("\n--- FINAL AGENT RESPONSE ---")
                print(event["agent"]["messages"])
        
        print(f"\nPrompt {prompt_count} Completed Successfully!")
        prompt_count += 1


if __name__ == "__main__":
    asyncio.run(main())