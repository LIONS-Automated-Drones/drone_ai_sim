import asyncio
import os
import operator
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition

from tools import get_tools

# Load environment variables from .env file
load_dotenv()

# --- 1. Define the Agent State ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. Setup the Agent ---
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
        ("system", "You are a drone pilot AI. Your job is to execute the user's mission by calling tools one at a time. Think step-by-step. When the entire mission is complete, and only then, call the 'mission_complete' tool with a summary of what you did."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

agent = agent_prompt | llm.bind_tools(tools)

# --- 3. Build the Graph ---
workflow = StateGraph(AgentState)

# The agent node, which reasons about the next action
def call_model(state):
    response = agent.invoke(state)
    return {"messages": [response]}

workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

# The conditional edge that decides where to go next
workflow.add_conditional_edges("agent", tools_condition)

# Connect the tool node back to the agent
workflow.add_edge("tools", "agent")

app = workflow.compile()

# --- 4. Run the Test ---
async def main():
    print("--- Starting LangGraph Test ---")
    prompt_count = 1
    while True:
        mission_prompt = input(f"Enter Prompt {prompt_count}: ")
        if mission_prompt.lower() in ["quit", "exit"]:
            break

        async for event in app.astream({"messages": [HumanMessage(content=mission_prompt)]}):
            for v in event.values():
                if "messages" in v:
                    print(v["messages"][-1].content)
        
        print(f"\nPrompt {prompt_count} Completed Successfully!")
        prompt_count += 1

if __name__ == "__main__":
    asyncio.run(main())