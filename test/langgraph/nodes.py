from langchain_core.messages import HumanMessage, ToolMessage
from state import AgentState
from tools import get_tools

# Get the list of tools
tools = get_tools()

def call_model(state: AgentState, agent):
    """
    The agent node, which reasons about the next action.
    """
    response = agent.invoke(state)
    return {"messages": [response]}

async def sequential_tool_node(state: AgentState) -> dict:
    """
    A custom tool node that executes only the first tool call found and provides
    feedback to the agent if multiple tools were suggested.
    """
    last_message = state["messages"][-1]
    
    tool_call = last_message.tool_calls[0]
    
    tool_to_call = None
    for tool in tools:
        if tool.name == tool_call["name"]:
            tool_to_call = tool
            break

    if tool_to_call is None:
        raise ValueError(f"Tool '{tool_call['name']}' not found.")
        
    response = await tool_to_call.ainvoke(tool_call["args"])
    
    messages_to_add = []
    messages_to_add.append(ToolMessage(content=str(response), tool_call_id=tool_call["id"]))
    
    if len(last_message.tool_calls) > 1:
        feedback_message = (
            "SYSTEM NOTE: You suggested multiple tools, but I am configured to only "
            "execute one tool at a time. I have executed the first one, "
            f"'{tool_call['name']}'. Please review the result and decide on the next step."
        )
        messages_to_add.append(HumanMessage(content=feedback_message))
    
    return {"messages": messages_to_add}

def ask_for_clarification_node(state: AgentState) -> dict:
    """
    The node that asks the agent for clarification if it detects a text-based tool call.
    """
    feedback_message = (
        "SYSTEM NOTE: I detected what looks like a tool call in your text response. "
        "This is not the correct way to call a tool. "
        "If you intended to execute an action, please call the tool again using the proper tool-calling feature. "
        "If you intended to just display the JSON as part of your thought process, please rephrase your response without the JSON formatting."
    )
    return {"messages": [HumanMessage(content=feedback_message)]}
