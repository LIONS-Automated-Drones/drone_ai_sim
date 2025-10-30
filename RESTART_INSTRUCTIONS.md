# How to Restart the System

## The Problem
The `orchestrate.launch.py` was started when NumPy 2.3.4 was installed, causing `yolo_perception_node` to crash. Now that NumPy 1.26.4 is installed, the launch file needs to be restarted.

## Solution

### Terminal 1 (Orchestrate Launch):

1. **Stop the current launch** (Ctrl+C)
   
2. **Restart it:**
   ```bash
   cd ~/repos/drone_ai_sim
   source install/setup.bash
   ros2 launch drone_ai_sim_ros orchestrate.launch.py
   ```

3. **Verify the yolo_perception_node starts:**
   Look for these lines in the output:
   ```
   [yolo_perception_node]: 🔄 Loading YOLO model: yolov8n.pt
   [yolo_perception_node]: ✅ YOLO model loaded successfully
   [yolo_perception_node]: ✅ YOLO Perception Node initialized
   [yolo_perception_node]: 🛎️  Service available: trigger_detection
   ```

4. **Check nodes are running:**
   In another terminal:
   ```bash
   ros2 node list | grep yolo
   ```
   Should show: `/yolo_perception_node`

### Terminal 2 (Test.py - LangGraph Agent):

1. **Restart test.py** (if running, Ctrl+C first)
   ```bash
   cd ~/repos/drone_ai_sim/test/langgraph
   source ~/repos/drone_ai_sim/venv/bin/activate
   python test.py
   ```

2. **Try the vision command:**
   ```
   Mission: what do you see
   ```

### Expected Success Output:

From Terminal 2 (test.py):
```
[INFO] --- Starting ROS2 client thread...
[INFO] --- Preloaded ROS core: librosidl_typesupport_c.so
[INFO] --- Preloaded ROS core: librosidl_typesupport_fastrtps_c.so
[INFO] --- Preloaded ROS core: librosidl_typesupport_introspection_c.so
[INFO] --- Preloaded: libares_interfaces__rosidl_generator_c.so
[INFO] --- Preloaded: libares_interfaces__rosidl_typesupport_c.so
[INFO] --- Preloaded: libares_interfaces__rosidl_typesupport_fastrtps_c.so
[INFO] --- Preloaded: libares_interfaces__rosidl_typesupport_introspection_c.so
[INFO] --- Preloaded: libares_interfaces__rosidl_generator_py.so
[INFO] --- Preloaded: libares_interfaces__rosidl_typesupport_cpp.so
[INFO] --- Preloaded: libares_interfaces__rosidl_typesupport_fastrtps_cpp.so
[INFO] --- Preloaded: libares_interfaces__rosidl_typesupport_introspection_cpp.so
[INFO] --- Creating service client for object detection...
[INFO] --- Waiting for object detection service to be available...
[INFO] --- Service available! Calling object detection...  ← Success!
[INFO] --- Object detection response: [...]
```

## Quick Verification Commands

```bash
# Terminal 3 - Check system status:

# 1. Verify NumPy version (should be 1.26.4):
python3 -c "import numpy; print(numpy.__version__)"

# 2. Check if orchestrate is running:
ps aux | grep orchestrate

# 3. Check all ROS nodes:
ros2 node list

# 4. Test the service manually:
ros2 service call /trigger_detection ares_interfaces/srv/DetectObjects "{trigger: true}"
```

## If Still Fails

1. **Check Gazebo is running** (Terminal 0)
2. **Check NumPy version** (must be 1.26.4, not 2.x)
3. **Rebuild ROS packages if needed:**
   ```bash
   cd ~/repos/drone_ai_sim
   colcon build --packages-select drone_ai_sim_ros
   source install/setup.bash
   ```

