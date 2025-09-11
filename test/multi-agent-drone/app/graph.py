from functools import partial
import re
from typing import List

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, ToolMessage

from state import AgentState
from agents.pilot import create_pilot_agent, ArmAndTakeoffTool, MoveForwardTool, MoveDirectionTool, OrbitLocationTool, ReturnToLaunchTool, LandDroneTool, CaptureImageTool
from agents.vision import create_vlm_agent, AnalyzeImageTool


def _route_agent(state: AgentState) -> str:
    """
    Simple intent router. Chooses which agent should act next based on the
    latest user message content. Defaults to pilot for safety-critical actions.
    """
    last = state["messages"][-1]
    content = last.content.lower() if isinstance(last, HumanMessage) else ""

    vision_keywords: List[str] = [
        "see", "look", "detect", "recognize", "identify", "image", "photo", "picture",
        "vlm", "yolo", "vision"
    ]
    pilot_keywords: List[str] = [
        "take off", "takeoff", "arm", "land", "rtl", "return", "move", "fly",
        "go to", "goto", "orbit", "yaw", "altitude", "heading"
    ]

    if any(k in content for k in vision_keywords):
        return "vision"
    if any(k in content for k in pilot_keywords):
        return "pilot"

    # Fallback: if tools were called earlier, continue with that agent
    next_agent = state.get("next_agent")
    return next_agent or "pilot"


def _call_model(state: AgentState, agent_executor):
    """
    Call the provided agent (pilot or vision) with the current state.
    """
    response = agent_executor.invoke(state)
    return {"messages": [response]}


async def _tool_node(state: AgentState):
    """
    Execute only the first tool call emitted by the agent, then return its
    ToolMessage and optionally a HumanMessage feedback if multiple tools were proposed.
    """
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]

    # Build the tool registry once
    tools = [
        # Pilot tools
        ArmAndTakeoffTool(),
        MoveForwardTool(),
        MoveDirectionTool(),
        OrbitLocationTool(),
        ReturnToLaunchTool(),
        LandDroneTool(),
        CaptureImageTool(),
        # Vision tools
        AnalyzeImageTool(),
    ]

    tool_to_call = None
    for t in tools:
        if t.name == tool_call["name"]:
            tool_to_call = t
            break

    if tool_to_call is None:
        raise ValueError(f"Tool '{tool_call['name']}' not found.")

    # Debug: print the tool call details
    print(f"Tool call details: {tool_call}")
    
    # Execute the tool - handle tools that don't need arguments
    if tool_call["name"] in ["arm_and_takeoff", "land_drone", "return_to_launch", "capture_image"]:
        # These tools don't need arguments, so pass empty dict
        response = await tool_to_call.ainvoke({})
    else:
        # These tools need arguments, so pass them
        response = await tool_to_call.ainvoke(tool_call["args"])

    messages_to_add = [
        ToolMessage(content=str(response), tool_call_id=tool_call["id"])
    ]

    if len(last_message.tool_calls) > 1:
        messages_to_add.append(
            HumanMessage(
                content=(
                    "SYSTEM NOTE: You suggested multiple tools, but I am configured to only "
                    "execute one tool at a time. I have executed the first one, "
                    f"'{tool_call['name']}'. Please review the result and decide on the next step."
                )
            )
        )

    return {"messages": messages_to_add}


def _route_after_agent(state: AgentState, tool_names):
    """Route based on whether the agent made a structured tool call or wrote JSON-like text."""
    last = state["messages"][-1]
    if last.tool_calls:
        return "tools"

    # Detect attempted JSON/text tool call to nudge the model
    content = getattr(last, "content", "") or ""
    if re.search(r"\{\s*\"name\"\s*:\s*\".+?\"", content):
        return "clarify"

    return END


def build_graph():
    """
    Build and compile the multi-agent workflow with a simple router that chooses
    between the pilot and vision agents. Returns a runnable app.
    """
    pilot = create_pilot_agent()
    vision = create_vlm_agent()

    workflow = StateGraph(AgentState)

    # Nodes
    workflow.add_node("router", lambda s: {"next_agent": _route_agent(s)})
    workflow.add_node("pilot", partial(_call_model, agent_executor=pilot))
    workflow.add_node("vision", partial(_call_model, agent_executor=vision))
    workflow.add_node("tools", _tool_node)
    workflow.add_node(
        "clarify",
        lambda s: {
            "messages": [
                HumanMessage(
                    content=(
                        "SYSTEM NOTE: I detected what looks like a tool call in your text response. "
                        "NO TOOLS WERE EXECUTED. Please call tools using the tool-calling feature, "
                        "not by writing JSON in the content."
                    )
                )
            ]
        },
    )

    # Entry and routing
    workflow.set_entry_point("router")
    workflow.add_conditional_edges(
        "router",
        lambda s: s.get("next_agent", "pilot"),
        {
            "pilot": "pilot",
            "vision": "vision",
        },
    )

    # After an agent acts, decide next step
    tool_names = [
        "arm_and_takeoff",
        "move_forward", 
        "move_direction",
        "orbit_location",
        "return_to_launch",
        "land_drone",
        "capture_image",
        "analyze_image",
    ]

    workflow.add_conditional_edges(
        "pilot",
        partial(_route_after_agent, tool_names=tool_names),
        {"tools": "tools", "clarify": "clarify", END: END},
    )
    workflow.add_conditional_edges(
        "vision",
        partial(_route_after_agent, tool_names=tool_names),
        {"tools": "tools", "clarify": "clarify", END: END},
    )

    # Loop back after tool execution
    workflow.add_edge("tools", "router")
    workflow.add_edge("clarify", "router")

    return workflow.compile()


