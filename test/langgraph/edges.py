from state import AgentState

# The conditional edge that decides where to go next
def should_continue(state: AgentState):
    if not state["messages"][-1].tool_calls:
        # If the agent didn't call a tool, the loop is done.
        return "end"
    else:
        # Otherwise, call the tool.
        return "continue"
