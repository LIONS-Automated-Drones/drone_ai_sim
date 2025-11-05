# Nav2 Integration with MAVSDK

This document describes how Nav2 velocity commands are integrated with the MAVSDK-controlled drone.

## Architecture

The system uses a velocity passthrough architecture with UDP socket communication:

1. **Nav2** publishes velocity commands to `/cmd_vel` (standard ROS topic)
2. **cmd_vel_bridge.py** (ROS 2 node) subscribes to `/cmd_vel` and forwards velocity data via UDP socket
3. **test.py** runs a UDP listener that receives velocity data and updates `drone_service.most_recent_velocity`
4. **drone_service** maintains a background task that continuously sends the most recent velocity to MAVSDK at 20Hz
5. **test.py** (websocket server) handles `start_nav` and `stop_nav` commands from the dashboard
6. **React dashboard** provides UI controls to start/stop Nav2 integration

### Why UDP Sockets?

The cmd_vel_bridge is a ROS 2 node running in a separate process from the Python asyncio-based langgraph system. They cannot share memory or directly import each other. UDP provides:
- **Fast, lightweight communication** for high-frequency velocity updates
- **No connection overhead** - fire and forget
- **Process isolation** - ROS and asyncio remain independent

## Data Flow

```
Nav2 → /cmd_vel → cmd_vel_bridge (ROS node)
                        ↓
                   UDP Socket (port 6000)
                        ↓
                  velocity_listener (test.py) → drone_service.most_recent_velocity
                                                         ↓
                                                 20Hz velocity loop → MAVSDK → Drone
```

## Key Features

- **Non-blocking**: The velocity update is instantaneous - no queue buildup
- **Latest velocity**: Only the most recent `/cmd_vel` is used, older commands are discarded
- **Continuous sending**: The drone receives velocity updates at 20Hz regardless of Nav2 publish rate
- **Safe shutdown**: Stopping Nav2 control commands the drone to hold position

## Components

### 1. drone_service.py

Added methods:
- `update_nav_velocity()`: Updates the stored velocity (called by cmd_vel_bridge)
- `start_nav_control()`: Starts the velocity sending loop
- `stop_nav_control()`: Stops the loop and commands drone to hold
- `_nav_velocity_loop()`: Background task that sends velocity at 20Hz

### 2. cmd_vel_bridge.py

ROS 2 node that:
- Subscribes to `/cmd_vel` topic
- Packages velocity data as JSON
- Sends velocity data via UDP socket to `127.0.0.1:6000`
- Runs independently as a separate ROS process

### 3. test.py

Added features:
- **UDP velocity listener**: Background task that receives velocity data on port 6000 and updates `drone_service.most_recent_velocity`
- **Websocket message handlers**:
  - `start_nav`: Starts Nav2 control mode
  - `stop_nav`: Stops Nav2 control mode and holds position

### 4. React Dashboard (status-box.tsx)

Added UI controls:
- "Start Nav" / "Stop Nav" button in the telemetry panel
- Status indicator showing if Nav2 is active or inactive

## Usage

### Starting the System

1. **Start the ROS bridge (in WSL/Linux terminal)**:
```bash
cd ~/drone_ai_sim/test/langgraph
python3 cmd_vel_bridge.py
```

2. **Start the langgraph websocket server (in WSL/Linux terminal)**:
```bash
cd ~/drone_ai_sim/test/langgraph
python test.py
```

3. **Start Nav2** (if not already running):
```bash
ros2 launch nav2_bringup ...
```

4. **Open the React Dashboard** and connect

### Enabling Nav2 Control

1. In the React dashboard, click the **"Start Nav"** button
2. The drone will start following `/cmd_vel` commands from Nav2
3. The status will show "Nav2: ACTIVE"

### Disabling Nav2 Control

1. Click the **"Stop Nav"** button
2. The drone will immediately hold its current position
3. The velocity sending loop stops
4. The status will show "Nav2: INACTIVE"

## Frame Conversions

The system handles frame conversions between ROS and MAVSDK:

**ROS cmd_vel (body frame, FLU - Forward-Left-Up)**:
- `linear.x`: Forward velocity (positive = forward)
- `linear.y`: Left velocity (positive = left)
- `linear.z`: Up velocity (positive = up)
- `angular.z`: Yaw rate (positive = counterclockwise)

**MAVSDK (body frame, FRD - Forward-Right-Down)**:
- `forward_m_s`: Forward velocity (positive = forward)
- `right_m_s`: Right velocity (positive = right) ← **negated from ROS**
- `down_m_s`: Down velocity (positive = down) ← **negated from ROS**
- `yawspeed_deg_s`: Yaw rate in degrees/s ← **converted from rad/s**

## Important Notes

1. **Drone must be connected and armed** before starting Nav2 control
2. **Manual override takes precedence**: If manual override is enabled, Nav2 control will be automatically stopped
3. **Offboard mode**: The drone must be in a mode that accepts velocity commands (typically OFFBOARD mode in PX4)
4. **Safety**: Always test in simulation first before using on a physical drone
5. **Update rate**: The cmd_vel_bridge runs synchronously with ROS callbacks, while the velocity loop runs at 20Hz asynchronously
6. **UDP Port**: Ensure port 6000 is available on localhost for velocity communication

## Troubleshooting

**Nav2 control not starting?**
- Check that the drone is connected (websocket messages will indicate)
- Ensure the drone is armed
- Verify cmd_vel_bridge.py is running

**Drone not moving?**
- Check that `/cmd_vel` is being published: `ros2 topic echo /cmd_vel`
- Verify Nav2 is active in the dashboard status
- Check drone flight mode (must support velocity commands)

**cmd_vel_bridge not receiving messages?**
- Verify the topic name: `ros2 topic list | grep cmd_vel`
- Check ROS domain ID matches
- Ensure the node is running: `ros2 node list | grep cmd_vel_bridge`

## Future Enhancements

Potential improvements:
- Add velocity limiting for safety
- Support for NED frame velocity commands
- Velocity feedback visualization in dashboard
- Automatic Nav2 start/stop based on mission state
- Integration with the LangGraph mission system

