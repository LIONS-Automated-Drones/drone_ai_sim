import re
import json
from langchain_core.messages import HumanMessage, ToolMessage
from state import AgentState
from tools import get_tools, drone_service
from utils import parse_tool_call_from_text

# Get the list of tools
tools = get_tools()

async def call_model(state: AgentState, agent):
    """
    The agent node, which reasons about the next action.
    Injects world memory and drone telemetry context into the conversation.
    """
    context_messages = []
    
    # Get and format drone telemetry
    try:
        if drone_service.is_connected:
            telemetry = await drone_service.get_comprehensive_telemetry()
            if telemetry:
                # Add "connected" field to telemetry
                telemetry["connected"] = True
                drone_state = telemetry
            else:
                # Telemetry fetch failed but drone is connected
                drone_state = {"connected": True, "error": "Failed to fetch telemetry"}
        else:
            # Drone not connected - provide default state
            drone_state = {
                "connected": False,
                "armed": False,
                "flight_mode": "UNKNOWN",
                "battery_percent": 0.0,
                "gps_fix_type": "NO_FIX",
                "gps_satellites": 0,
                "health_all_ok": False,
                "position_relative": {"x_m": 0.0, "y_m": 0.0, "z_m": 0.0},
                "altitude_m": 0.0,
                "velocity_ms": 0.0,
                "heading_deg": 0.0,
                "is_in_air": False
            }
    except Exception as e:
        # Error getting telemetry
        drone_state = {"connected": False, "error": str(e)}
    
    # Determine tool availability based on connection status
    is_connected = drone_state.get("connected", False)
    
    # Define which tools are always available (even when not connected)
    always_available = {"arm_and_takeoff", "sense_objects", "clear_world_memory"}
    
    # Get all tool names
    all_tool_names = [tool.name for tool in tools]
    
    # Create tool availability message
    tool_availability_lines = ["=== Tool Call Availability ==="]
    for tool_name in all_tool_names:
        if is_connected or tool_name in always_available:
            tool_availability_lines.append(f"{tool_name}: AVAILABLE")
        else:
            tool_availability_lines.append(f"{tool_name}: UNAVAILABLE")
    
    # Add tool availability as a HumanMessage
    tool_availability_msg = HumanMessage(content="\n".join(tool_availability_lines))
    context_messages.append(tool_availability_msg)
    
    # Format drone state for prompt as a ToolMessage
    if drone_state.get("connected"):
        drone_lines = ["CURRENT DRONE STATE:"]
        drone_lines.append(f"  - Connected: {drone_state['connected']}")
        drone_lines.append(f"  - Armed: {drone_state.get('armed', 'Unknown')}")
        drone_lines.append(f"  - Flight Mode: {drone_state.get('flight_mode', 'Unknown')}")
        drone_lines.append(f"  - In Air: {drone_state.get('is_in_air', 'Unknown')}")
        drone_lines.append(f"  - Battery: {drone_state.get('battery_percent', 0):.1f}%")
        drone_lines.append(f"  - Altitude: {drone_state.get('altitude_m', 0):.2f}m")
        drone_lines.append(f"  - Heading: {drone_state.get('heading_deg', 0):.1f}°")
        drone_lines.append(f"  - Velocity: {drone_state.get('velocity_ms', 0):.2f}m/s")
        pos = drone_state.get('position_relative', {})
        drone_lines.append(f"  - Position (relative): x={pos.get('x_m', 0):.2f}m, y={pos.get('y_m', 0):.2f}m, z={pos.get('z_m', 0):.2f}m")
        drone_lines.append(f"  - GPS: {drone_state.get('gps_fix_type', 'Unknown')} ({drone_state.get('gps_satellites', 0)} satellites)")
        drone_lines.append(f"  - Health: {'OK' if drone_state.get('health_all_ok', False) else 'NOT OK'}")
    else:
        drone_lines = ["CURRENT DRONE STATE:"]
        drone_lines.append(f"  - Connected: False")
        if "error" in drone_state:
            drone_lines.append(f"  - Error: {drone_state['error']}")
        else:
            drone_lines.append(f"  - To connect, call 'arm_and_takeoff' tool. No other tools will work until you take off (which connects you to the drone service)")
    
    # Add drone state as a ToolMessage
    drone_state_msg = ToolMessage(
        content="\n".join(drone_lines),
        tool_call_id="get_drone_state",
        name="get_drone_state"
    )
    context_messages.append(drone_state_msg)
    
    # Format world memory for the prompt
    world_memory = state.get("world_memory", {})
    if world_memory:
        memory_lines = ["CURRENT WORLD MODEL (objects you have sensed):"]
        for obj_id, obj_data in world_memory.items():
            coords = obj_data["map_coords"]
            memory_lines.append(
                f"  - {obj_id}: {obj_data['class_name']} at ({coords['x']:.2f}, {coords['y']:.2f}, {coords['z']:.2f})"
            )
        # Add world memory as a ToolMessage
        memory_msg = ToolMessage(
            content="\n".join(memory_lines),
            tool_call_id="get_world_memory",
            name="get_world_memory"
        )
        context_messages.append(memory_msg)
    
    # Add context messages to state
    modified_state = dict(state)
    modified_state["messages"] = list(state["messages"]) + context_messages
    response = agent.invoke(modified_state)
    
    # Return response with updated drone_state
    return {"messages": [response], "drone_state": drone_state}

async def sequential_tool_node(state: AgentState) -> dict:
    """
    A custom tool node that executes only the first tool call found and provides
    feedback to the agent if multiple tools were suggested.
    """
    last_message = state["messages"][-1]
    
    tool_call = last_message.tool_calls[0]
    
    # Extract the actual tool name (handle prefixes like "default_api." or "default_api_")
    tool_name = tool_call["name"]
    original_name = tool_name
    
    # Handle dot-separated prefix (e.g., "default_api.sense_objects")
    if "." in tool_name:
        tool_name = tool_name.split(".")[-1]
        print(f"[DEBUG] Tool name had dot prefix: '{original_name}' -> '{tool_name}'")
    # Handle underscore prefix without dot (e.g., "default_api_sense_objects")
    elif tool_name.startswith("default_api_"):
        tool_name = tool_name.replace("default_api_", "", 1)
        print(f"[DEBUG] Tool name had underscore prefix: '{original_name}' -> '{tool_name}'")
    
    tool_to_call = None
    for tool in tools:
        if tool.name == tool_name:
            tool_to_call = tool
            break

    if tool_to_call is None:
        available_tools = [t.name for t in tools]
        raise ValueError(f"Tool '{tool_call['name']}' not found. Parsed name: '{tool_name}'. Available tools: {available_tools}")
        
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
    It parses the attempted tool call to provide more specific feedback.
    """
    last_message = state["messages"][-1]
    
    # Default feedback message
    feedback_message = (
        "SYSTEM NOTE: I detected what looks like a tool call in your text response. "
        "NO TOOLS WERE EXECUTED. This is not the correct way to call a tool. "
        "If you intended to execute an action, please call the tool again using the proper tool-calling feature. "
        "If you intended to just display the JSON as part of your thought process, please rephrase your response without the JSON formatting."
    )

    # Try to parse the specific tool name for better feedback
    tool_name = parse_tool_call_from_text(last_message.content)
    if tool_name:
        feedback_message = (
            f"SYSTEM NOTE: The '{tool_name}' tool WAS NOT CALLED. "
            "I detected that you tried to call a tool in your text response. This is not the correct way to call a tool. "
            f"To call the '{tool_name}' tool, you MUST use the tool-calling feature instead of writing it in the content."
        )

    return {"messages": [HumanMessage(content=feedback_message)]}

async def invalid_tool_node(state: AgentState):
    last = state["messages"][-1]
    bad = last.invalid_tool_calls[0]
    
    # Get list of valid tool names
    valid_tool_names = [tool.name for tool in tools]
    valid_tools_str = ", ".join(valid_tool_names)
    
    contentStr = (
        f"The tool call you attempted was invalid: {bad['name']}. "
        "Please reformat your tool call according to the schema.\n\n"
        f"Valid tool names are: {valid_tools_str}"
    )
    # Construct a repair message
    repair_msg = HumanMessage(
        content=contentStr
    )
    return {"messages": [repair_msg]}