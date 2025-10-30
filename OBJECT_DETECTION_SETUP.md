# Object Detection and Memory System Setup Guide

This guide explains how to build and use the new object detection and memory capabilities integrated into the ARES drone AI system.

## Overview

The system now includes:
1. **YOLOv8 object detection** running on the drone's stereo camera feed
2. **3D position estimation** using stereo disparity and RTAB-Map SLAM
3. **Persistent memory** that stores detected objects and their locations
4. **Natural language queries** like "What do you see?"

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   LangGraph Agent                            │
│  - New "sense_objects" tool                                  │
│  - World memory (detected objects)                           │
└──────────────┬──────────────────────────────────────────────┘
               │ ROS2 Service Call
               ▼
┌─────────────────────────────────────────────────────────────┐
│            YOLO Perception Node (ROS2)                       │
│  - YOLOv8 object detection                                   │
│  - Stereo depth estimation                                   │
│  - TF2 coordinate transformation                             │
└──────────────┬──────────────────────────────────────────────┘
               │ Subscribes to
               ▼
┌─────────────────────────────────────────────────────────────┐
│              RTAB-Map SLAM Pipeline                          │
│  - /left/image_rect_color                                    │
│  - /disparity                                                │
│  - /stereo/left/camera_info                                  │
└──────────────────────────────────────────────────────────────┘
```

## Installation Steps

### 1. Build the Custom ROS2 Interfaces

```bash
cd /home/raytech/repos/drone_ai_sim

# Build the ares_interfaces package
colcon build --packages-select ares_interfaces
source install/setup.bash
```

### 2. Install Python Dependencies

```bash
# Install YOLOv8 (ultralytics package)
pip install ultralytics

# The first time you run, YOLOv8 will automatically download the model weights
```

### 3. Build the Updated drone_ai_sim_ros Package

```bash
cd /home/raytech/repos/drone_ai_sim

# Build the updated package
colcon build --packages-select drone_ai_sim_ros
source install/setup.bash
```

### 4. Install Python Dependencies for LangGraph Agent

```bash
cd /home/raytech/repos/drone_ai_sim/test/langgraph

# The ros_client module uses rclpy (should already be installed with ROS2)
# Verify it's available:
python3 -c "import rclpy; print('rclpy available')"
```

## Usage

### 1. Start the Simulation and ROS2 Pipeline

```bash
# Terminal 1: Start Gazebo simulation (if not already running)
# [Your usual Gazebo launch command]

# Terminal 2: Launch the ROS2 pipeline including the new perception node
cd /home/raytech/repos/drone_ai_sim
source install/setup.bash
ros2 launch drone_ai_sim_ros orchestrate.launch.py
```

This will now launch:
- All the existing nodes (RTAB-Map, stereo processing, etc.)
- **NEW**: The `yolo_perception_node` for object detection

### 2. Start the LangGraph Agent

```bash
# Terminal 3: Start the agent
cd /home/raytech/repos/drone_ai_sim/test/langgraph
python3 test.py
```

### 3. Test Object Detection

Connect from your React dashboard (or CLI mode) and try these commands:

```
"Take off and what do you see?"

"Fly forward 5 meters, then tell me what objects are visible"

"What do you see? Remember the locations."

"Fly to the chair"  # After detecting a chair
```

## How It Works

### Service-Based Detection

The `yolo_perception_node` provides a ROS2 service called `trigger_detection`:

```bash
# You can manually test the service:
ros2 service call /trigger_detection ares_interfaces/srv/DetectObjects "{trigger: true}"
```

### World Memory

When the agent calls `sense_objects`:
1. The tool makes a ROS2 service call to `trigger_detection`
2. The YOLO node detects objects in the current camera view
3. For each detection:
   - Gets the pixel coordinates (bounding box center)
   - Looks up the disparity value at that pixel
   - Calculates depth: `Z = focal_length * baseline / disparity`
   - Projects to 3D in camera frame
   - Transforms to the `map` frame using TF2
4. Returns a list of `SensedObject` messages
5. The tool formats the response and the `sequential_tool_node` parses it
6. Updates the agent's `world_memory` state with the object IDs and 3D coordinates

### Memory Persistence

The world memory persists throughout a mission:
- Each detected object gets a unique ID (e.g., `chair_1`, `person_2`)
- The 3D coordinates are stored in the `map` frame
- The agent sees the memory on every reasoning step
- Memory resets when a new mission starts

## Configuration

### YOLO Model Selection

You can change the YOLO model in `orchestrate.launch.py`:

```python
parameters=[{
    "model_name": "yolov8n.pt",  # Options: yolov8n, yolov8s, yolov8m, yolov8l, yolov8x
    "confidence_threshold": 0.5,  # Adjust detection confidence
    "target_frame": "map"
}]
```

Models:
- `yolov8n.pt` - Nano (fastest, least accurate)
- `yolov8s.pt` - Small
- `yolov8m.pt` - Medium
- `yolov8l.pt` - Large
- `yolov8x.pt` - Extra large (most accurate, slowest)

### Troubleshooting

#### Service Not Available
```bash
# Check if the perception node is running:
ros2 node list | grep yolo_perception

# Check if the service exists:
ros2 service list | grep trigger_detection

# View node logs:
ros2 node info /yolo_perception_node
```

#### No Objects Detected
- Make sure there are objects visible in the camera view
- Check the confidence threshold (lower it if needed)
- Verify the camera topics are publishing:
  ```bash
  ros2 topic echo /left/image_rect_color --no-arr
  ros2 topic echo /disparity --no-arr
  ```

#### TF2 Transform Errors
- Ensure RTAB-Map is running and publishing transforms
- Check available frames:
  ```bash
  ros2 run tf2_ros tf2_echo map stereo_left_optical_frame
  ```

#### Invalid Disparity Values
- This can happen if objects are too close or too far
- Check the stereo camera calibration
- Verify disparity is being computed:
  ```bash
  ros2 topic echo /disparity --no-arr
  ```

## File Structure

```
drone_ai_sim/
├── ares_interfaces/              # NEW: Custom ROS2 messages/services
│   ├── msg/
│   │   └── SensedObject.msg
│   ├── srv/
│   │   └── DetectObjects.srv
│   ├── CMakeLists.txt
│   └── package.xml
│
├── drone_ai_sim_ros/
│   ├── drone_ai_sim_ros/
│   │   └── yolo_perception_node.py  # NEW: YOLO detection node
│   ├── launch/
│   │   └── orchestrate.launch.py    # UPDATED: Added perception node
│   ├── package.xml                   # UPDATED: Added dependencies
│   └── setup.py                      # UPDATED: Added entry point
│
└── test/langgraph/
    ├── ros_client.py                 # NEW: ROS2 bridge for agent
    ├── state.py                      # UPDATED: Added world_memory
    ├── tools.py                      # UPDATED: Added SenseObjectsTool
    ├── nodes.py                      # UPDATED: Memory parsing & injection
    └── test.py                       # UPDATED: Enhanced prompt
```

## Example Missions

### Mission 1: Object Survey
```
"Take off to 5 meters, tell me what you see, then land"
```

Expected behavior:
1. Drone takes off
2. Calls `sense_objects` tool
3. Reports detected objects with 3D coordinates
4. Objects are stored in memory
5. Lands

### Mission 2: Object-Based Navigation
```
"Take off, look around, then fly towards any chairs you detect"
```

Expected behavior:
1. Drone takes off
2. Calls `sense_objects`
3. Agent reasons about chair locations in memory
4. Navigates towards the chair's map coordinates
5. Reports completion

### Mission 3: Multi-Point Survey
```
"Take off, fly north 10 meters and tell me what you see, 
then fly east 10 meters and tell me what you see again"
```

Expected behavior:
1. Takes off
2. Moves north, senses objects (memory updated)
3. Moves east, senses objects again (memory grows)
4. Agent has memory of all detected objects from both locations

## Performance Tips

1. **Model Selection**: Use `yolov8n.pt` for real-time performance
2. **Confidence Threshold**: Set to 0.5-0.7 for good balance
3. **Service Timeout**: YOLO inference can take 1-3 seconds on CPU
4. **Disparity Quality**: Ensure good lighting and texture for accurate depth

## Next Steps

Possible enhancements:
- [ ] Add object tracking across multiple frames
- [ ] Implement object re-identification
- [ ] Add spatial reasoning (e.g., "fly to the left of the chair")
- [ ] Visualize detected objects in the React dashboard
- [ ] Store object detections to a database for long-term memory
- [ ] Add semantic segmentation for more detailed scene understanding

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review ROS2 logs: `ros2 topic echo /rosout`
3. Check YOLO node output for detection information
4. Verify all transforms are available: `ros2 run tf2_tools view_frames`

