#### Install Ubuntu 24.04
```bash
wsl --install -d Ubuntu-24.04
# Create default account and password
```
#### Setup PX4 Autopilot
```bash
cd ~
mkdir sd1_ws
cd sd1_ws
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
cd PX4-Autopilot 
bash ./Tools/setup/ubuntu.sh
exit # (Go to powershell)
wsl --shutdown
wsl.exe -d Ubuntu-24.04 # Go to bash
```


#### Jazzy Debian Install
I'm just going to put the instructions from here below https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F\" '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo $VERSION_CODENAME)_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update && sudo apt install ros-dev-tools
sudo apt upgrade
sudo apt install ros-jazzy-desktop
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc && source ~/.bashrc
# Test ros2 install
ros2 run demo_nodes_cpp talker 
```
You should see [INFO] [1757130632.075320083] [talker]: Publishing: 'Hello World: 1'


#### drone_ai_sim repo setup
```bash
cd ~/sd1_ws/
git clone https://github.com/LIONS-Automated-Drones/drone_ai_sim
cd drone_ai_sim/
git checkout dev
```

#### UPDATE SDF
```bash
cd ~/sd1_ws/PX4-Autopilot/Tools/simulation/gz/models/x500
> model.sdf  # Empties the file
nano model.sdf
# PASTE THE CODE FROM drone_modified.sdf then ctrl + x
cd ~/sd1_ws/PX4-Autopilot/Tools/simulation/gz/worlds
> default.sdf
nano default.sdf
# PASTE THE CODE FROM world_modified.sdf then ctrl + x
```

#### Install ROS-Gazebo Packages
```bash
sudo apt update
sudo apt install \
  ros-jazzy-ros-gz-bridge \
  ros-jazzy-ros-gz-image \
  ros-jazzy-ros-gz-sim \
  ros-jazzy-ros-gz-interfaces \
  ros-jazzy-rtabmap-ros
sudo apt install ros-jazzy-web-video-server
```


#### Setup venv & repo
```bash
cd ~/sd1_ws/
sudo apt install python3.12-venv
python3 -m venv drone_venv
source drone_venv/bin/activate
pip install dotenv setuptools langchain langchain-openai langgraph mavsdk
pip install websockets asyncio
cd ~/sd1_ws/drone_ai_sim/test/langgraph
touch .env
nano .env
# Paste IN .env config & save **
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434
USE_REACT=true
```


#### Stereo Image Proc Setup
```bash
cd ~/.ros
mkdir -p ~/.ros/camera_info
nano ~/.ros/camera_info/stereo_left.yaml
# Paste from git
nano ~/.ros/camera_info/stereo_right.yaml
# Paste from git
sudo apt update
sudo apt install ros-jazzy-image-pipeline
```




#### Running
Follow instructions in README.md to build the package and run