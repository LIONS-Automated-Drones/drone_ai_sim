from langchain_core.messages import AIMessage, ToolMessage
from state import AgentState

# Node that calls the agent to decide the next action
async def call_agent_node(state: AgentState, agent_executor):
    print("--- AGENT: Thinking... ---")
    response = await agent_executor.ainvoke(state)
    # Wrap the string output in an AIMessage inside a list
    return {"messages": [AIMessage(content=response["output"])]}

# Node that executes the chosen tool
async def call_tool_node(state: AgentState, agent_executor):
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    # This calls our TakeoffTool._arun() method
    tool_result = await agent_executor.tools[tool_call["name"]].ainvoke(tool_call["args"])
    return {"messages": [ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])]}
