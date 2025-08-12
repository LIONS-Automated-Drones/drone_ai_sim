from functools import partial
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import call_agent_node, call_tool_node
from edges import should_continue

def build_graph(agent_executor):
    """
    Builds and compiles the LangGraph workflow.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", partial(call_agent_node, agent_executor=agent_executor))
    workflow.add_node("tool", partial(call_tool_node, agent_executor=agent_executor))

    workflow.set_entry_point("agent")
    workflow.add_conditional_edges("agent", should_continue, {"continue": "tool", "end": END})
    workflow.add_edge("tool", "agent")

    app = workflow.compile()
    return app
