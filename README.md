# lions-automated-drones
Senior Design 1 Project: LIONS Automated Drone System (Agentic AI)

#### Setting up WSL environment
Follow directions in `wsl.md` to setup wsl2 environment on windows. If you aren't on windows ¯\_(ツ)_/¯

#### Seting up depot world
Go to the link below and download the world and unzip
`https://app.gazebosim.org/OpenRobotics/fuel/models/Depot`
```bash
mkdir -p ~/.gz/models
# Copy to models folder
cp -r /mnt/c/Users/YOUR_USERNAME/Downloads/Depot ~/.gz/models/
touch depot.sdf
nano depot.sdf
# Paste code from /world/depot.sdf and then save
# DO NOT FORGET TO UPDATE /homo/connor/ to your
# username before pasting
```

#### Building package
```bash
cd ~/sd1_ws/ # One level up from github repo
colcon build --packages-select drone_ai_sim_ros
source install/setup.bash
```

#### Running the project
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

#### Updates bashrc
You will likely want to add most of these to you bashrc. 

```bash
nano ~/.bashrc
# Paste the code below and save
source ~/.bashrc
```
READ THE COMMENTS BECAUSE YOU NEED TO UPDATE SOME SECTIONS
```bash
source /opt/ros/jazzy/setup.bash

export PATH=/usr/local/cuda-13.0/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-13.0/lib64:$LD_LIBRARY_PATH
# Change /connor/ to your username
source /home/connor/sd1_ws/install/setup.bash
# --- Forcing NVIDIA OpenGL Driver in WSL ---
# Only add these if you are using a NVIDIA GPU
export __GLX_VENDOR_LIBRARY_NAME=nvidia
export MESA_D3D12_DEFAULT_ADAPTER_NAME=NVIDIA
export GALLIUM_DRIVER=d3d12
```
#### GPU Acceleration in WSL
If you have a NVIDIA gpu and update your bashrc with what I provided,
WSL should use GPU acceleration which will make gazebo simulation run much faster. You can confirm this by running
`glxinfo | grep "OpenGL renderer"`. For me, this outputs: 
"OpenGL renderer string: D3D12 (NVIDIA GeForce RTX 4050 Laptop GPU)". If you have a different type of gpu, you will need to do
research on how to get it to work.

#### Useful ROS2 Commands
Node name and topic name
```bash
ros2 topic list # View all ros topics
ros2 topic echo /topic_name --once # See data coming from topic
ros2 topic hz /topic_name # See how many times a topic is publishing per second
ros2 topic info /topic_name # See type and num subs and pubs
ros2 node list # View active nodes
ros2 param list /node_name # See parameters of node
ros2 param describe /node_name param_name # See parameter info
```