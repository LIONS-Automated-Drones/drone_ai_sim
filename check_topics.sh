#!/bin/bash

echo "=== Checking ROS 2 Topics ==="
echo ""

echo "1. Raw stereo images from Gazebo:"
timeout 2 ros2 topic hz /stereo/left 2>&1 | head -3
timeout 2 ros2 topic hz /stereo/right 2>&1 | head -3

echo ""
echo "2. Rectified images:"
timeout 2 ros2 topic hz /left/image_rect 2>&1 | head -3
timeout 2 ros2 topic hz /right/image_rect 2>&1 | head -3

echo ""
echo "3. Disparity:"
timeout 2 ros2 topic hz /disparity 2>&1 | head -3

echo ""
echo "4. Camera info:"
timeout 2 ros2 topic hz /stereo/left/camera_info 2>&1 | head -3

echo ""
echo "=== Topic List ==="
ros2 topic list | grep -E "(stereo|disparity|image_rect)"

