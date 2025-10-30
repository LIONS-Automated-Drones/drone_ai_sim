# Debug: YOLO Detects Objects But Perception Node Returns Nothing

## Problem Summary

Your standalone YOLO script detects a chair at 0.75 confidence, but the `yolo_perception_node` returns "no objects detected" when called via the ROS service.

## Root Cause Analysis

The ROS service **IS working** (all 11 libraries loaded ✅), but the perception node is returning an empty list. This happens when:

1. ✅ **YOLO runs successfully**
2. ✅ **YOLO detects objects** (e.g., chair at 0.75 confidence)
3. ❌ **BUT `pixel_to_map_coords()` returns `None`** for ALL detections

When `pixel_to_map_coords()` fails, the detection is logged but **NOT included in the response**.

### Why `pixel_to_map_coords()` Might Fail

The function can return `None` for several reasons:

| Failure Point | Cause | Log Message |
|---------------|-------|-------------|
| **Invalid Disparity** | Disparity at pixel is NaN or ≤0 | `❌ Invalid disparity at (x, y): ...` |
| **Unreasonable Depth** | Calculated depth <0.1m or >50m | `❌ Unreasonable depth calculated: Xm` |
| **TF Transform Failure** | No transform from camera frame to map frame | `❌ TF2 transform failed (... → ...): ...` |

## Changes Made (Enhanced Logging)

I've added **detailed diagnostic logging** to `yolo_perception_node.py`:

### 1. Detection Count
```python
📊 YOLO found X detections above confidence threshold 0.5
```
This shows how many objects YOLO detected BEFORE filtering.

### 2. Disparity Validation
```python
❌ Invalid disparity at (x, y): NaN (NaN=True, ≤0=N/A)
```
Shows if the disparity image has no depth data at the object's location.

### 3. Depth Calculation
```python
📏 Depth calculation: f=XXXpx, baseline=0.XXXm, disparity=XXpx → depth=Xm
```
Shows the stereo depth calculation step-by-step.

### 4. TF Transform
```python
🔄 Looking up transform: stereo_left_optical_frame → map
✅ Transformed to map frame: (X, Y, Z)
```
or
```python
❌ TF2 transform failed (stereo_left_optical_frame → map): ...
```
Shows if coordinate transformation succeeds.

## How to Debug

### Step 1: Restart the ROS System

**Terminal 1** (must restart to load new code):
```bash
# Stop current launch (Ctrl+C)
cd ~/repos/drone_ai_sim
source install/setup.bash
ros2 launch drone_ai_sim_ros orchestrate.launch.py
```

Watch for startup messages, especially:
```
[yolo_perception_node]: ✅ YOLO Perception Node initialized
[yolo_perception_node]: 🛎️  Service available: trigger_detection
```

### Step 2: Run Diagnostic Script

**Terminal 3**:
```bash
cd ~/repos/drone_ai_sim
source install/setup.bash
./diagnose_vision.sh
```

This will:
- ✅ Check if all required nodes are running
- ✅ Check if topics are publishing
- ✅ Check if TF frames are available
- 🔔 Call the detection service

### Step 3: Try Vision Command

**Terminal 2**:
```bash
cd ~/repos/drone_ai_sim/test/langgraph
source ~/repos/drone_ai_sim/venv/bin/activate
python test.py
```

Then in the web interface:
```
Mission: what do you see
```

### Step 4: Analyze Logs in Terminal 1

While the vision command runs, **watch Terminal 1** for these logs:

#### Expected Success Flow:
```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found 1 detections above confidence threshold 0.5
[yolo_perception_node]: Detected: chair (conf: 0.75) at pixel (320, 240)
[yolo_perception_node]: 📏 Depth calculation: f=387.50px, baseline=0.120m, disparity=15.50px → depth=3.00m
[yolo_perception_node]: 🔄 Looking up transform: stereo_left_optical_frame → map
[yolo_perception_node]: ✅ Transformed to map frame: (1.50, 0.20, 0.80)
[yolo_perception_node]: → Map coords: (1.50, 0.20, 0.80)
[yolo_perception_node]: ✅ Detection complete: 1 objects with valid 3D positions
```

#### If Invalid Disparity:
```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found 1 detections above confidence threshold 0.5
[yolo_perception_node]: Detected: chair (conf: 0.75) at pixel (320, 240)
[yolo_perception_node]: ❌ Invalid disparity at (320, 240): nan (NaN=True, ≤0=N/A)
[yolo_perception_node]: ⚠️ Could not compute 3D position for chair
[yolo_perception_node]: ✅ Detection complete: 0 objects with valid 3D positions
```
**Cause:** Stereo camera not generating disparity data at that pixel (no texture/depth).

#### If Unreasonable Depth:
```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found 1 detections above confidence threshold 0.5
[yolo_perception_node]: Detected: chair (conf: 0.75) at pixel (320, 240)
[yolo_perception_node]: 📏 Depth calculation: f=387.50px, baseline=0.120m, disparity=0.50px → depth=93.00m
[yolo_perception_node]: ❌ Unreasonable depth calculated: 93.00m (must be 0.1-50m)
[yolo_perception_node]: ⚠️ Could not compute 3D position for chair
[yolo_perception_node]: ✅ Detection complete: 0 objects with valid 3D positions
```
**Cause:** Low disparity (poor stereo match) results in calculated depth >50m.

#### If TF Transform Fails:
```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found 1 detections above confidence threshold 0.5
[yolo_perception_node]: Detected: chair (conf: 0.75) at pixel (320, 240)
[yolo_perception_node]: 📏 Depth calculation: f=387.50px, baseline=0.120m, disparity=15.50px → depth=3.00m
[yolo_perception_node]: 🔄 Looking up transform: stereo_left_optical_frame → map
[yolo_perception_node]: ❌ TF2 transform failed (stereo_left_optical_frame → map): Lookup would require extrapolation into the future
[yolo_perception_node]: ⚠️ Could not compute 3D position for chair
[yolo_perception_node]: ✅ Detection complete: 0 objects with valid 3D positions
```
**Cause:** RTAB-Map hasn't published a map frame yet, or TF tree is incomplete.

## Likely Culprits

Based on your setup, the most likely issues are:

### 1. **Invalid Disparity (Most Likely)**
- The stereo camera might not be generating good disparity data
- Objects too close/far for stereo matching
- Poor lighting or low texture on the object

**Fix:** Check disparity image quality:
```bash
# In a browser, go to:
http://localhost:8080/stream?topic=/disparity&type=ros_compressed
```
The chair should appear as a bright blob (close = bright, far = dark).

### 2. **TF Transform to Map Frame**
- RTAB-Map needs time to initialize and create the map frame
- The drone might not have moved enough for RTAB-Map to build a map

**Fix:** Wait longer after startup, or change target frame from `map` to `odom_stereo`:
```python
# In orchestrate.launch.py, line 241:
"target_frame": "odom_stereo"  # Instead of "map"
```

### 3. **Low Disparity Resolution**
- Disparity calculation might be too coarse
- Small disparity values get filtered out

**Check:** Look at the disparity value in logs. If <1.0, it's too low.

## Quick Fixes

### Fix 1: Change Target Frame (Easiest)

Edit `orchestrate.launch.py` line 241:
```python
"target_frame": "odom_stereo"  # or "base_link" instead of "map"
```

Then rebuild and restart:
```bash
cd ~/repos/drone_ai_sim
colcon build --packages-select drone_ai_sim_ros
source install/setup.bash
# Restart Terminal 1 (orchestrate)
```

### Fix 2: Increase Depth Range

Edit `yolo_perception_node.py` line 273:
```python
if depth < 0.1 or depth > 100.0:  # Increased from 50m to 100m
```

### Fix 3: Add Disparity Debug Output

Check what the disparity image looks like:
```bash
ros2 topic echo /disparity --once
```

## Summary

The issue is NOT with the ROS service itself (that's working perfectly now), but with the **3D position calculation** for detected objects. The enhanced logging will show you exactly where it's failing:

- **Disparity issue** → Stereo camera problem
- **Depth issue** → Stereo calibration or range problem  
- **TF issue** → RTAB-Map or frame configuration problem

**Next step:** Run the diagnostic script and check Terminal 1 logs while running "what do you see".

