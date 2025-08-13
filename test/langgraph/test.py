import asyncio
import os
import operator
import re
import json
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from tools import get_tools

# Load environment variables from .env file
load_dotenv()

# --- 1. Define the Agent State ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. Setup the Agent ---
tools = get_tools()
tool_names = [tool.name for tool in tools]
llm = ChatOpenAI(
    model=os.getenv("OLLAMA_MODEL"),
    openai_api_base=os.getenv("OLLAMA_BASE_URL") + "/v1",
    openai_api_key="ollama",
    temperature=0,
)

# The agent's "brain" that decides which tool to call.
# This includes the "soft fix" from Solution 1.
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a drone pilot AI. Your job is to execute the user's mission by calling tools one at a time. Think step-by-step. When the entire mission is complete, and only then, call the 'mission_complete' tool with a summary of what you did. You MUST NOT include JSON in your text responses. To execute an action, you MUST use the tool-calling feature exclusively."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

agent = agent_prompt | llm.bind_tools(tools)

# --- 3. Build the Graph ---

# This is our custom node. It will only execute the FIRST tool call
# that the agent suggests, forcing sequential execution.
async def sequential_tool_node(state: AgentState) -> dict:
    """
    A custom tool node that executes only the first tool call found and provides
    feedback to the agent if multiple tools were suggested.
    """
    last_message = state["messages"][-1]
    
    # --- Part 1: Execute only the first tool call ---
    tool_call = last_message.tool_calls[0]
    
    tool_to_call = None
    for tool in tools:
        if tool.name == tool_call["name"]:
            tool_to_call = tool
            break

    if tool_to_call is None:
        raise ValueError(f"Tool '{tool_call['name']}' not found.")
        
    response = await tool_to_call.ainvoke(tool_call["args"])
    
    # --- Part 2: Create the feedback messages ---
    messages_to_add = []
    
    # Add the result of the tool we just ran
    messages_to_add.append(ToolMessage(content=str(response), tool_call_id=tool_call["id"]))
    
    # If the agent suggested more than one tool, add a feedback message
    if len(last_message.tool_calls) > 1:
        feedback_message = (
            "SYSTEM NOTE: You suggested multiple tools, but I am configured to only "
            "execute one tool at a time. I have executed the first one, "
            f"'{tool_call['name']}'. Please review the result and decide on the next step."
        )
        # Using HumanMessage is a common way to inject system-level feedback
        messages_to_add.append(HumanMessage(content=feedback_message))
    
    return {"messages": messages_to_add}

# This is the new node that asks the agent for clarification.
def ask_for_clarification_node(state: AgentState) -> dict:
    feedback_message = (
        "SYSTEM NOTE: I detected what looks like a tool call in your text response. "
        "This is not the correct way to call a tool. "
        "If you intended to execute an action, please call the tool again using the proper tool-calling feature. "
        "If you intended to just display the JSON as part of your thought process, please rephrase your response without the JSON formatting."
    )
    return {"messages": [HumanMessage(content=feedback_message)]}
    
# This is the new conditional edge that implements the clarification loop.
def route_agent_response(state: AgentState):
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "continue"

    # A more general pattern to catch any plausible-looking tool call.
    tool_pattern = r'\{\s*"name"\s*:\s*".+?".*?\}'
    match = re.search(tool_pattern, last_message.content, re.DOTALL)
    
    if match:
        return "clarify"
    
    return "end"

workflow = StateGraph(AgentState)

# The agent node, which reasons about the next action
def call_model(state):
    response = agent.invoke(state)
    return {"messages": [response]}

workflow.add_node("agent", call_model)
workflow.add_node("tools", sequential_tool_node)
workflow.add_node("clarify", ask_for_clarification_node)

workflow.set_entry_point("agent")

# Use the new conditional edge to route the agent's response
workflow.add_conditional_edges(
    "agent",
    route_agent_response,
    {
        "continue": "tools",
        "clarify": "clarify",
        "end": END,
    },
)

# Connect the other nodes back to the agent
workflow.add_edge("tools", "agent")
workflow.add_edge("clarify", "agent")

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