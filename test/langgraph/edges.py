import re
from state import AgentState

def route_agent_response(state: AgentState, tool_names):
    """
    The conditional edge that routes the agent's response to the correct node.
    """
    last_message = state["messages"][-1]

    if last_message.tool_calls:
        return "continue"

    # A more general pattern to catch any plausible-looking tool call.
    tool_pattern = r'\{\s*"name"\s*:\s*".+?".*?\}'
    match = re.search(tool_pattern, last_message.content, re.DOTALL)
    
    if match:
        return "clarify"
    
    return "end"
