from functools import partial
from langgraph.graph import StateGraph, END
from state import AgentState
from nodes import call_model, sequential_tool_node, ask_for_clarification_node
from edges import route_agent_response

def build_graph(agent, tool_names):
    """
    Builds and compiles the LangGraph workflow.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", partial(call_model, agent=agent))
    workflow.add_node("tools", sequential_tool_node)
    workflow.add_node("clarify", ask_for_clarification_node)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        partial(route_agent_response, tool_names=tool_names),
        {
            "continue": "tools",
            "clarify": "clarify",
            "end": END,
        },
    )

    workflow.add_edge("tools", "agent")
    workflow.add_edge("clarify", "agent")

    app = workflow.compile()
    return app
