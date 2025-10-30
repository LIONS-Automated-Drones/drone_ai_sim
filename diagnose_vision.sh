#!/bin/bash

echo "===== YOLO PERCEPTION NODE DIAGNOSTICS ====="
echo ""

# Check if orchestrate is running
echo "1. Checking if orchestrate.launch.py is running..."
if ps aux | grep -q "[o]rchestrate.launch.py"; then
    echo "   ✅ orchestrate.launch.py is running"
else
    echo "   ❌ orchestrate.launch.py is NOT running"
    exit 1
fi

# Check if yolo_perception_node is running
echo ""
echo "2. Checking if yolo_perception_node is running..."
if ros2 node list | grep -q "yolo_perception_node"; then
    echo "   ✅ yolo_perception_node is running"
else
    echo "   ❌ yolo_perception_node is NOT running!"
    echo "   Check Terminal 1 for crash logs"
    exit 1
fi

# Check if required topics are publishing
echo ""
echo "3. Checking required topics..."

echo "   3a. /left/image_rect_color:"
if ros2 topic hz /left/image_rect_color --once 2>&1 | grep -q "average rate"; then
    echo "      ✅ Publishing"
else
    echo "      ❌ Not publishing or no data"
fi

echo "   3b. /disparity:"
if ros2 topic hz /disparity --once 2>&1 | grep -q "average rate"; then
    echo "      ✅ Publishing"
else
    echo "      ❌ Not publishing or no data"
fi

echo "   3c. /stereo/left/camera_info:"
if ros2 topic hz /stereo/left/camera_info --once 2>&1 | grep -q "average rate"; then
    echo "      ✅ Publishing"
else
    echo "      ❌ Not publishing or no data"
fi

# Check if service is available
echo ""
echo "4. Checking if /trigger_detection service is available..."
if ros2 service list | grep -q "trigger_detection"; then
    echo "   ✅ Service is available"
else
    echo "   ❌ Service NOT available"
    exit 1
fi

# Check TF frames
echo ""
echo "5. Checking TF frames..."
echo "   Available frames:"
timeout 2 ros2 run tf2_ros tf2_echo map stereo_left_optical_frame 2>&1 | head -5 || echo "      ❌ Transform map -> stereo_left_optical_frame not available"

echo ""
echo "6. Testing service call..."
echo "   Calling /trigger_detection..."
echo "   (Check Terminal 1 for detailed ROS node logs)"
echo ""

ros2 service call /trigger_detection ares_interfaces/srv/DetectObjects "{trigger: true}"

echo ""
echo "===== DIAGNOSTICS COMPLETE ====="
echo ""
echo "NEXT STEPS:"
echo "1. Look at Terminal 1 (orchestrate.launch.py) for these logs:"
echo "   - '🔔 Detection service called'"
echo "   - '🔍 Running YOLO detection...'"
echo "   - 'Detected: <object> (conf: X.XX)'"
echo "   - Either '→ Map coords' or '⚠️ Could not compute 3D position'"
echo ""
echo "2. If you see '⚠️ Could not compute 3D position', common causes:"
echo "   - Invalid disparity (NaN or ≤0)"
echo "   - Unreasonable depth (<0.1m or >50m)"
echo "   - TF transform failure (map frame not available)"

