#!/bin/bash
# Pre-flight Checklist for Vision System
# Run this before starting the full simulation

echo "============================================"
echo "🚁 ARES Vision System Pre-flight Check"
echo "============================================"
echo ""

cd /home/raytech/repos/drone_ai_sim
source install/setup.bash 2>/dev/null

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

CHECKS_PASSED=0
CHECKS_FAILED=0

# Function to print status
check_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((CHECKS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((CHECKS_FAILED++))
    fi
}

echo "📦 Checking Dependencies..."
echo "----------------------------------------"

# Check NumPy version
NUMPY_VERSION=$(python3 -c "import numpy; print(numpy.__version__)" 2>/dev/null)
if [[ "$NUMPY_VERSION" == "1.26.4" ]]; then
    check_status 0 "NumPy version: $NUMPY_VERSION"
else
    check_status 1 "NumPy version: $NUMPY_VERSION (expected 1.26.4)"
fi

# Check OpenCV
OPENCV_VERSION=$(python3 -c "import cv2; print(cv2.__version__)" 2>/dev/null)
if [[ ! -z "$OPENCV_VERSION" ]]; then
    check_status 0 "OpenCV installed: $OPENCV_VERSION"
else
    check_status 1 "OpenCV not found"
fi

# Check Ultralytics (YOLO)
YOLO_CHECK=$(python3 -c "from ultralytics import YOLO; print('OK')" 2>/dev/null)
if [[ "$YOLO_CHECK" == "OK" ]]; then
    check_status 0 "Ultralytics (YOLO) installed"
else
    check_status 1 "Ultralytics not found"
fi

echo ""
echo "🔧 Checking ROS Packages..."
echo "----------------------------------------"

# Check ares_interfaces build
if [ -d "install/ares_interfaces" ]; then
    check_status 0 "ares_interfaces package built"
else
    check_status 1 "ares_interfaces not built"
fi

# Check drone_ai_sim_ros build
if [ -d "install/drone_ai_sim_ros" ]; then
    check_status 0 "drone_ai_sim_ros package built"
else
    check_status 1 "drone_ai_sim_ros not built"
fi

# Check YOLO node executable
if [ -f "install/drone_ai_sim_ros/lib/drone_ai_sim_ros/yolo_perception_node" ]; then
    check_status 0 "yolo_perception_node executable exists"
else
    check_status 1 "yolo_perception_node executable missing"
fi

# Check shared libraries
if [ -f "install/ares_interfaces/lib/libares_interfaces__rosidl_generator_py.so" ]; then
    check_status 0 "ares_interfaces shared libraries built"
else
    check_status 1 "ares_interfaces shared libraries missing"
fi

echo ""
echo "🚀 Testing YOLO Node Startup..."
echo "----------------------------------------"

# Try to start the node briefly
timeout 3 ros2 run drone_ai_sim_ros yolo_perception_node 2>&1 | grep -q "YOLO model loaded successfully"
if [ $? -eq 0 ]; then
    check_status 0 "YOLO node can start and load model"
else
    check_status 1 "YOLO node failed to start"
fi

echo ""
echo "📝 Checking Python Environment..."
echo "----------------------------------------"

# Check if running in venv for agent
if [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
    echo -e "${YELLOW}⚠️  INFO${NC}: Running in venv (for agent)"
else
    echo -e "${YELLOW}⚠️  INFO${NC}: Not in venv (for ROS nodes)"
fi

# Check critical paths
if [ -d "/opt/ros/jazzy" ]; then
    check_status 0 "ROS 2 Jazzy installed"
else
    check_status 1 "ROS 2 Jazzy not found"
fi

echo ""
echo "============================================"
echo "📊 RESULTS"
echo "============================================"
echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"
echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
echo ""

if [ $CHECKS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CHECKS PASSED - READY FOR LAUNCH!${NC}"
    echo ""
    echo "🚀 To start the simulation:"
    echo "   Terminal 1: ros2 launch drone_ai_sim_ros orchestrate.launch.py"
    echo "   Terminal 2: cd test/langgraph && python test.py"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  SOME CHECKS FAILED - REVIEW ISSUES ABOVE${NC}"
    echo ""
    echo "🔧 Common fixes:"
    echo "   - NumPy: pip install --break-system-packages 'numpy==1.26.4' --force-reinstall --no-deps"
    echo "   - OpenCV: pip install --break-system-packages 'opencv-python-headless<4.9.0'"
    echo "   - Rebuild: colcon build --packages-select ares_interfaces drone_ai_sim_ros"
    echo ""
    exit 1
fi

