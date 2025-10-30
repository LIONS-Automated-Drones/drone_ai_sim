# Sense Objects Tool - Developer Reference

## Quick Overview

The `sense_objects` tool enables the LangGraph agent to detect objects in the drone's camera view and remember their 3D locations.

## Tool Specification

**Name**: `sense_objects`

**Description**: Uses the drone's camera and YOLO object detection to identify objects in view and store their 3D locations in memory.

**Parameters**: None (automatically uses current camera view)

**Returns**: String describing detected objects with their map coordinates

## Usage in Agent

### Natural Language Triggers
- "What do you see?"
- "Look around"
- "Tell me what objects are nearby"
- "Scan the area"

### Example Mission Flow

```python
# User: "Take off and tell me what you see"

# Agent reasoning:
# 1. Call arm_and_takeoff tool
# 2. Wait for completion
# 3. Call sense_objects tool
# 4. Receive: "Detected 2 object(s):
#       - chair_1: chair at map coordinates (2.34, -1.23, 0.45) meters
#       - person_1: person at map coordinates (5.67, 2.11, 0.98) meters"
# 5. Objects now in world_memory
# 6. Can reason about object locations
```

## State Management

### AgentState Structure

```python
class AgentState(TypedDict):
    messages: List[BaseMessage]  # Conversation history
    world_memory: Dict[str, dict]  # Detected objects
    # {
    #   "chair_1": {
    #     "class_name": "chair",
    #     "map_coords": {"x": 2.34, "y": -1.23, "z": 0.45}
    #   },
    #   "person_1": {
    #     "class_name": "person", 
    #     "map_coords": {"x": 5.67, "y": 2.11, "z": 0.98}
    #   }
    # }
```

### Memory Lifecycle

1. **Initialization**: Empty dict `{}` at mission start
2. **Update**: When `sense_objects` is called, new objects are added
3. **Persistence**: Stays in state throughout the mission
4. **Access**: Automatically injected into agent context on each reasoning step
5. **Reset**: Cleared when new mission starts

## Implementation Details

### Tool Execution Flow

```
1. Agent calls sense_objects
   ↓
2. SenseObjectsTool._arun() executes
   ↓
3. Gets ROS node (starts thread if needed)
   ↓
4. Creates DetectObjects service client
   ↓
5. Waits for yolo_perception_node service
   ↓
6. Calls service with trigger=True
   ↓
7. Waits for response (max 15 seconds)
   ↓
8. Formats detected objects as string
   ↓
9. Returns to agent
   ↓
10. sequential_tool_node parses response
   ↓
11. Updates state["world_memory"]
   ↓
12. call_model injects memory into next reasoning step
```

### ROS2 Service Interface

```python
# Service: /trigger_detection
# Type: ares_interfaces/srv/DetectObjects

# Request
bool trigger  # Set to True to trigger detection

# Response
ares_interfaces/SensedObject[] sensed_objects
  # Each SensedObject contains:
  #   string class_name
  #   geometry_msgs/Point map_coords
```

### Object ID Generation

Objects are assigned unique IDs in the format: `{class_name}_{count}`

Examples:
- First chair detected: `chair_1`
- Second chair: `chair_2`
- First person: `person_1`

IDs are generated within each tool call based on class name counts.

## Error Handling

### Common Errors and Responses

| Error | Tool Response | Cause |
|-------|--------------|-------|
| ROS not available | "Error: ROS client not available" | ros_client import failed |
| Service timeout | "Error: Object detection service not available after 10s" | yolo_perception_node not running |
| Detection timeout | "Error: Object detection service timed out after 15 seconds" | YOLO inference too slow |
| No objects | "I looked around but didn't detect any recognizable objects" | Nothing in view or low confidence |

### Debugging

```python
# Enable detailed logging in tools.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Check mission_log output
# All tool execution is logged with "--- EXECUTING TOOL: ..." prefix

# Manually test the ROS service
ros2 service call /trigger_detection ares_interfaces/srv/DetectObjects "{trigger: true}"
```

## Memory Context Injection

The `call_model` function in `nodes.py` automatically injects world memory:

```python
if world_memory:
    memory_string = """
    CURRENT WORLD MODEL (objects you have sensed):
      - chair_1: chair at (2.34, -1.23, 0.45)
      - person_1: person at (5.67, 2.11, 0.98)
    """
    # Injected as HumanMessage before agent invocation
```

This allows the agent to reason about objects without explicitly querying state.

## Agent Prompt Integration

System prompt includes:

> "You have a 'sense_objects' tool that uses computer vision to detect objects in your camera view and remember their 3D locations. Use this when asked 'what do you see?' or when you need to locate objects. Your world model (detected objects and their locations) will be shown to you automatically when available."

This guides the agent to:
- Use the tool when appropriate
- Understand that memory is automatically provided
- Reason about object locations in 3D space

## Example Agent Reasoning

### Example 1: Simple Detection

**User**: "What do you see?"

**Agent Internal Process**:
```
1. User wants to know about visible objects
2. I should use sense_objects tool
3. [calls sense_objects]
4. Tool returns: "Detected 2 objects: chair_1 at (2.34, -1.23, 0.45), person_1 at (5.67, 2.11, 0.98)"
5. Memory updated with these objects
6. I should report to user
```

**Agent Response**: "I can see 2 objects: a chair at coordinates (2.34, -1.23, 0.45) meters and a person at (5.67, 2.11, 0.98) meters in the map frame."

### Example 2: Navigation to Object

**User**: "Fly to the chair"

**Agent Internal Process**:
```
1. User wants me to navigate to a chair
2. Check my world memory...
3. Memory shows: chair_1 at (2.34, -1.23, 0.45)
4. I need to fly to those coordinates
5. Get current telemetry to calculate relative movement
6. [calls get_telemetry]
7. Calculate direction and distance
8. [calls move_relative_cardinal or goto_location]
```

**Agent Response**: "I have a chair in my memory at map coordinates (2.34, -1.23, 0.45). Flying there now..."

## Performance Considerations

- **Service Call Time**: 2-5 seconds (includes YOLO inference + depth calculation + transforms)
- **Memory Size**: Each object ~100 bytes, negligible for typical missions
- **Threading**: ROS node runs in separate daemon thread, doesn't block asyncio
- **Concurrent Calls**: Service calls are sequential (only one at a time)

## Testing

### Unit Test Example

```python
# test_sense_objects.py
import pytest
from tools import SenseObjectsTool

@pytest.mark.asyncio
async def test_sense_objects_no_ros():
    tool = SenseObjectsTool()
    result = await tool._arun()
    assert "Error: ROS client not available" in result or "Detected" in result

# Integration test (requires ROS2 running)
@pytest.mark.asyncio
async def test_sense_objects_integration():
    tool = SenseObjectsTool()
    result = await tool._arun()
    # Should either detect objects or report none detected
    assert "Detected" in result or "didn't detect" in result
```

### Manual Testing

```bash
# Terminal 1: Start ROS pipeline
ros2 launch drone_ai_sim_ros orchestrate.launch.py

# Terminal 2: Run agent
cd test/langgraph
python3 test.py

# In agent CLI:
> "what do you see?"
# Should trigger sense_objects tool and return detected objects
```

## Future Enhancements

Possible improvements to the tool:

1. **Confidence Filtering**: Add parameter to filter by confidence
2. **Class Filtering**: Only detect specific object classes
3. **Region of Interest**: Detect only in specific image regions
4. **Multi-Frame Aggregation**: Combine detections over multiple frames
5. **Object Tracking**: Track objects over time with unique persistent IDs
6. **Semantic Relationships**: Detect spatial relationships (left of, behind, etc.)

## Code Locations

- **Tool Definition**: `test/langgraph/tools.py` (SenseObjectsTool class)
- **ROS Client**: `test/langgraph/ros_client.py`
- **State Definition**: `test/langgraph/state.py` (AgentState)
- **Memory Parsing**: `test/langgraph/nodes.py` (parse_sense_objects_response)
- **Memory Injection**: `test/langgraph/nodes.py` (call_model)
- **ROS Service**: `drone_ai_sim_ros/drone_ai_sim_ros/yolo_perception_node.py`
- **Message Definitions**: `ares_interfaces/msg/SensedObject.msg`
- **Service Definitions**: `ares_interfaces/srv/DetectObjects.srv`

