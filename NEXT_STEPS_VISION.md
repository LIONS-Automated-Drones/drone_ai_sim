# NEXT STEPS: Debug "No Objects Detected"

## TL;DR

✅ **ROS service is working** (all 11 libraries loaded successfully)  
❌ **YOLO detects objects but `pixel_to_map_coords()` filters them out**

## Quick Action Plan

### 1. Restart ROS System (REQUIRED)
```bash
# Terminal 1 - Stop with Ctrl+C, then:
cd ~/repos/drone_ai_sim
source install/setup.bash
ros2 launch drone_ai_sim_ros orchestrate.launch.py
```
**Why:** New logging code needs to be loaded.

### 2. Run Diagnostics
```bash
# Terminal 3:
cd ~/repos/drone_ai_sim
source install/setup.bash
./diagnose_vision.sh
```

### 3. Test Vision Command
```bash
# Terminal 2:
cd ~/repos/drone_ai_sim/test/langgraph
source ~/repos/drone_ai_sim/venv/bin/activate
python test.py

# In web interface:
Mission: what do you see
```

### 4. **CHECK TERMINAL 1** for These Logs

Look for this sequence:
```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found X detections    ← How many?
[yolo_perception_node]: Detected: chair (conf: 0.75)  ← Did YOLO see it?
[yolo_perception_node]: 📏 Depth calculation: ...     ← What depth?
[yolo_perception_node]: ❌ [ERROR MESSAGE]            ← Why did it fail?
```

## Common Issues & Fixes

| Log Message | Problem | Quick Fix |
|-------------|---------|-----------|
| `❌ Invalid disparity` | No stereo depth at that pixel | Check disparity image quality |
| `❌ Unreasonable depth: 93m` | Stereo matching poor | Change to `target_frame: "odom_stereo"` |
| `❌ TF2 transform failed` | Map frame not available | Wait longer or use `"odom_stereo"` |

## Most Likely Fix: Change Target Frame

**Edit:** `drone_ai_sim_ros/launch/orchestrate.launch.py` line 241:

**Change FROM:**
```python
"target_frame": "map"
```

**Change TO:**
```python
"target_frame": "odom_stereo"
```

**Rebuild:**
```bash
cd ~/repos/drone_ai_sim
colcon build --packages-select drone_ai_sim_ros
source install/setup.bash
# Restart Terminal 1
```

**Why:** The `map` frame requires RTAB-Map to have built a map, which takes time. The `odom_stereo` frame is available immediately.

## Files to Check

- ✅ **Enhanced Logging:** `drone_ai_sim_ros/drone_ai_sim_ros/yolo_perception_node.py`
- 🔧 **Config:** `drone_ai_sim_ros/launch/orchestrate.launch.py` (line 241)
- 📋 **Details:** `DEBUG_NO_DETECTIONS.md`

## Expected Success Output (Terminal 1)

```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found 1 detections above confidence threshold 0.5
[yolo_perception_node]: Detected: chair (conf: 0.75) at pixel (320, 240)
[yolo_perception_node]: 📏 Depth calculation: f=387.50px, baseline=0.120m, disparity=15.50px → depth=3.00m
[yolo_perception_node]: 🔄 Looking up transform: stereo_left_optical_frame → odom_stereo
[yolo_perception_node]: ✅ Transformed to map frame: (1.50, 0.20, 0.80)
[yolo_perception_node]: → Map coords: (1.50, 0.20, 0.80)
[yolo_perception_node]: ✅ Detection complete: 1 objects with valid 3D positions
```

## If Still Fails

Share the Terminal 1 logs (especially the `❌` lines) so we can see exactly which step is failing.

