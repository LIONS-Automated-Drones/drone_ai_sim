import re
from state import AgentState
from utils import parse_tool_call_from_text

def route_agent_response(state: AgentState, tool_names):
    """
    The conditional edge that routes the agent's response to the correct node.
    """
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "continue"

    if getattr(last_message, "invalid_tool_calls", None):
        return "invalid"

    if parse_tool_call_from_text(last_message.content):
        return "clarify"
    
    return "end"
