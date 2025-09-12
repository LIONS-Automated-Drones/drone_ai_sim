# lions-automated-drones
Senior Design 1 Project: LIONS Automated Drone System (Agentic AI)

Building package
```bash
cd ~/sd1_ws/ # One level up from github repo
colcon build --packages-select drone_ai_sim_ros
source install/setup.bash
```

Running the project
```bash
# Terminal 1
PX4_GZ_WORLD=depot HEADLESS=1 make px4_sitl gz_x500
# Terminal 2 
ros2 launch drone_ai_sim_ros orchestrate.launch.py
# Terminal 3 
source ~/sd1_ws/drone_venv/bin/activate
# Change /mnt/c/SD1/drone_ai_sim to wherever you have the
# repo on your computer. /mnt/c is your C:/ drive on windows
cd /mnt/c/SD1/drone_ai_sim/test/langgraph
python test.py
```