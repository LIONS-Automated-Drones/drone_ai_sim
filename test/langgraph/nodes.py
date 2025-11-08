import re
import json
import os
import aiohttp
from langchain_core.messages import HumanMessage, ToolMessage
from state import AgentState
from tools import get_tools
from utils import parse_tool_call_from_text

# Get the list of tools
tools = get_tools()

def call_model(state: AgentState, agent):
    """
    The agent node, which reasons about the next action.
    Injects world memory context into the conversation.
    """
    # Format world memory for the prompt
    world_memory = state.get("world_memory", {})
    if world_memory:
        memory_lines = ["CURRENT WORLD MODEL (objects you have sensed):"]
        for obj_id, obj_data in world_memory.items():
            coords = obj_data["map_coords"]
            memory_lines.append(
                f"  - {obj_id}: {obj_data['class_name']} at ({coords['x']:.2f}, {coords['y']:.2f}, {coords['z']:.2f})"
            )
        memory_string = "\n".join(memory_lines)
        
        # Add memory context as a system-style message if not already present
        # We'll inject it by temporarily adding it to messages
        from langchain_core.messages import HumanMessage
        memory_msg = HumanMessage(content=f"\n\n{memory_string}\n")
        
        # Create modified state with memory context
        modified_state = dict(state)
        modified_state["messages"] = list(state["messages"]) + [memory_msg]
        response = agent.invoke(modified_state)
        
        # Remove the memory message from the actual conversation
        return {"messages": [response]}
    else:
        response = agent.invoke(state)
        return {"messages": [response]}

async def sequential_tool_node(state: AgentState) -> dict:
    """
    A custom tool node that executes only the first tool call found and provides
    feedback to the agent if multiple tools were suggested.
    Also updates world_memory when sense_objects tool is called.
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
    
    # Update world_memory if sense_objects was called
    result = {"messages": messages_to_add}
    if tool_name == "sense_objects":
        updated_memory = parse_sense_objects_response(str(response), state.get("world_memory", {}))
        result["world_memory"] = updated_memory
        
        # Send the updated world_memory to the pointcloud bridge
        await send_world_memory_to_bridge(updated_memory)
    
    return result


async def send_world_memory_to_bridge(world_memory: dict):
    """
    Send the updated world_memory to the pointcloud websocket bridge.
    
    Args:
        world_memory: The world_memory dictionary to send
    """
    # Get the Linux IP from environment variable
    linux_ip = os.environ.get('YOLO_SERVER_IP', 'localhost')
    bridge_url = f'http://{linux_ip}:5445/world_memory'
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(bridge_url, json=world_memory) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ Successfully sent world_memory to bridge: {result.get('message', 'OK')}")
                else:
                    print(f"⚠️ Failed to send world_memory to bridge: HTTP {response.status}")
    except Exception as e:
        print(f"⚠️ Error sending world_memory to bridge: {str(e)}")


def parse_sense_objects_response(response: str, current_memory: dict) -> dict:
    """
    Parse the sense_objects tool response and update world memory.
    
    Args:
        response: The tool response string
        current_memory: The current world_memory dictionary
        
    Returns:
        Updated world_memory dictionary
    """
    # Create a copy of current memory
    memory = dict(current_memory)
    
    # Parse the response to extract object information
    # Format: "  - object_id: class_name at map coordinates (x, y, z) meters"
    import re
    pattern = r'- ([a-zA-Z0-9_]+): ([a-zA-Z0-9_]+) at map coordinates \(([0-9.-]+), ([0-9.-]+), ([0-9.-]+)\) meters'
    
    matches = re.findall(pattern, response)
    for match in matches:
        object_id, class_name, x, y, z = match
        memory[object_id] = {
            "class_name": class_name,
            "map_coords": {
                "x": float(x),
                "y": float(y),
                "z": float(z)
            }
        }
    
    return memory

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
