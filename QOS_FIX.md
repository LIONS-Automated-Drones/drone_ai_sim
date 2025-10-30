# Critical Fix: QoS Profile Mismatch

## The Problem

The `yolo_perception_node` was **never receiving camera_info messages**, causing the camera model to never initialize. This was because of a **QoS (Quality of Service) profile mismatch**.

### What is QoS?

In ROS 2, publishers and subscribers must have **compatible QoS profiles** to communicate. If they don't match, messages are silently dropped.

Camera topics typically use the `sensor_data` QoS profile:
- **Reliability:** `BEST_EFFORT` (allows some packet loss for speed)
- **Durability:** `VOLATILE` (don't store old messages)
- **History:** `KEEP_LAST` with depth 10

### The Bug

**Before:**
```python
self.camera_info_sub = self.create_subscription(
    CameraInfo,
    '/stereo/left/camera_info',
    self.camera_info_callback,
    10  # ❌ This uses DEFAULT QoS (RELIABLE)
)
```

**After:**
```python
sensor_qos = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=10
)

self.camera_info_sub = self.create_subscription(
    CameraInfo,
    '/stereo/left/camera_info',
    self.camera_info_callback,
    sensor_qos  # ✅ Now uses sensor_data QoS
)
```

## Why This Matters

1. **Default QoS uses `RELIABLE` reliability** - guarantees delivery but slower
2. **Camera topics use `BEST_EFFORT`** - allows packet loss for real-time performance
3. **`RELIABLE` subscribers can't connect to `BEST_EFFORT` publishers** in ROS 2

Result: The subscription was created but **never received any messages**.

## The Fix

I updated all three subscriptions in `yolo_perception_node.py`:
- ✅ `/left/image_rect_color` → sensor_data QoS
- ✅ `/disparity` → sensor_data QoS  
- ✅ `/stereo/left/camera_info` → sensor_data QoS

## Expected Behavior After Fix

**On startup:**
```
[yolo_perception_node]: ✅ YOLO Perception Node initialized
[yolo_perception_node]: 📡 Subscribed with sensor_data QoS profile
[yolo_perception_node]: 📷 Camera frame detected: x500_0/stereo_left_link/stereo_left
[yolo_perception_node]: ✅ Camera model initialized: fx=762.72, fy=762.72, cx=640.00, cy=360.00  ← NEW!
```

**On detection:**
```
[yolo_perception_node]: 🔔 Detection service called
[yolo_perception_node]: 🔍 Running YOLO detection...
[yolo_perception_node]: 📊 YOLO found 1 detections above confidence threshold 0.5
[yolo_perception_node]: Detected: chair (conf: 0.68) at pixel (673, 188)
[yolo_perception_node]: 📏 Depth calculation: f=762.72px, baseline=0.120m, disparity=60.12px → depth=1.52m
[yolo_perception_node]: 🎯 Projecting pixel (673, 188) to 3D ray...
[yolo_perception_node]: Camera params: fx=762.72, fy=762.72, cx=640.00, cy=360.00  ← Should work!
[yolo_perception_node]: 📐 Ray vector: (0.043, -0.226, 1.000)
[yolo_perception_node]: 🔄 Looking up transform: x500_0/stereo_left_link/stereo_left → map
[yolo_perception_node]: ✅ Transformed to map frame: (1.50, 0.20, 0.80)
[yolo_perception_node]: ✅ Detection complete: 1 objects with valid 3D positions
```

## How to Test

### 1. Restart Terminal 1
```bash
# Ctrl+C to stop
cd ~/repos/drone_ai_sim
source install/setup.bash
ros2 launch drone_ai_sim_ros orchestrate.launch.py
```

**Look for:** `✅ Camera model initialized: fx=...` within a few seconds of startup.

### 2. Verify Subscriptions
```bash
ros2 topic info /stereo/left/camera_info
```

Should show `yolo_perception_node` in the Subscription list.

### 3. Test Vision Command
In Terminal 2:
```bash
python test.py
# Then: "what do you see"
```

Should return detected objects!

## Debugging QoS Issues

If you ever have subscription issues in ROS 2:

```bash
# Check publisher QoS:
ros2 topic info /stereo/left/camera_info --verbose

# Look for:
# QoS profile:
#   Reliability: BEST_EFFORT  ← Must match subscriber!
#   Durability: VOLATILE
#   History: KEEP_LAST
```

If your subscriber uses different QoS, messages won't be received.

## Files Changed

- ✅ `drone_ai_sim_ros/drone_ai_sim_ros/yolo_perception_node.py`
  - Lines 80-111: Added sensor_data QoS profile
  - Lines 137-153: Simplified camera_info_callback with flag
  - Line 171: Use flag instead of checking P matrix

## Status

**Confidence Level:** 🟢 **VERY HIGH**

This is a well-known ROS 2 issue. The QoS profile mismatch prevents any communication, and the fix is straightforward and battle-tested.

**Ready for Testing:** ✅ YES

