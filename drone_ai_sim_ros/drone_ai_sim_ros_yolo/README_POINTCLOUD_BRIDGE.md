# ROS2 PointCloud2 to WebSocket Bridge

This script bridges ROS2 PointCloud2 messages to a WebSocket server, allowing real-time 3D point cloud visualization in web browsers using Three.js.

## Overview

The `pointcloud_websocket_bridge.py` script:
- Subscribes to a ROS2 PointCloud2 topic
- Extracts point positions (XYZ) and colors (RGB)
- Converts the data to a Three.js-compatible format
- Broadcasts the data over WebSocket to connected clients
- Supports multiple simultaneous web client connections

## Prerequisites

### ROS2 Installation
You need ROS2 installed with the following packages:
```bash
# Replace <distro> with your ROS2 distribution (e.g., humble, iron, jazzy)
sudo apt install ros-<distro>-rclpy
sudo apt install ros-<distro>-sensor-msgs
sudo apt install ros-<distro>-sensor-msgs-py
```

### Python Dependencies
```bash
pip install websockets numpy
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
Run the script with default settings (subscribes to `/stereo/points2` on port 8765):
```bash
# Source your ROS2 workspace first
source /opt/ros/<distro>/setup.bash
source ~/your_workspace/install/setup.bash  # If using a custom workspace

# Run the bridge
python3 pointcloud_websocket_bridge.py
```

### Custom Topic
Specify a different PointCloud2 topic:
```bash
python3 pointcloud_websocket_bridge.py --topic /camera/depth/points
```

### Custom Port
Change the WebSocket server port:
```bash
python3 pointcloud_websocket_bridge.py --port 9000
```

### Custom Host
Bind to a specific network interface:
```bash
python3 pointcloud_websocket_bridge.py --host 0.0.0.0  # Listen on all interfaces
```

### Full Example
```bash
python3 pointcloud_websocket_bridge.py \
  --topic /stereo/points2 \
  --port 8765 \
  --host localhost
```

## Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--topic` | `/stereo/points2` | ROS2 PointCloud2 topic name |
| `--port` | `8765` | WebSocket server port |
| `--host` | `localhost` | WebSocket server host/IP |

## Point Cloud Data Format

The script sends JSON messages over WebSocket with the following structure:

```json
{
  "vertices": [x1, y1, z1, x2, y2, z2, ...],
  "colors": [r1, g1, b1, r2, g2, b2, ...],
  "timestamp": 1234567890.123,
  "num_points": 1000,
  "frame_id": "stereo_camera"
}
```

- **vertices**: Flat array of XYZ coordinates (Float32Array compatible)
- **colors**: Flat array of RGB values normalized to [0.0, 1.0] (Float32Array compatible)
- **timestamp**: Unix timestamp in seconds
- **num_points**: Number of points in the cloud
- **frame_id**: ROS2 frame ID from the message header

## Color Handling

The script supports two coloring modes:

1. **RGB from PointCloud2**: If the point cloud contains RGB/RGBA fields, those colors are used
2. **Height-based fallback**: If no color data is available, colors are generated based on the Z coordinate (height)

## Web Client Integration

### React/TypeScript Example

The script is designed to work with the Digital Twin component in the react-dashboard:

```typescript
const ws = new WebSocket("ws://localhost:8765")

ws.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  // Convert to Float32Arrays for Three.js
  const vertices = new Float32Array(data.vertices)
  const colors = new Float32Array(data.colors)
  
  // Use with Three.js BufferGeometry
  const geometry = new THREE.BufferGeometry()
  geometry.setAttribute("position", new THREE.BufferAttribute(vertices, 3))
  geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3))
}
```

### Client Commands

Clients can send JSON messages to the server:

```json
// Request latest data
{"type": "request_data"}

// Ping/pong for connection testing
{"type": "ping"}
```

## Testing the Bridge

### 1. Start the Bridge
```bash
python3 pointcloud_websocket_bridge.py --topic /stereo/points2
```

Expected output:
```
Starting WebSocket server on ws://localhost:8765
Subscribing to ROS2 topic: /stereo/points2
Press Ctrl+C to stop
Subscribed to topic: /stereo/points2
Waiting for PointCloud2 messages...
```

### 2. Verify ROS2 Topic
In another terminal, verify your PointCloud2 topic is publishing:
```bash
ros2 topic list | grep points
ros2 topic hz /stereo/points2
ros2 topic echo /stereo/points2 --once
```

### 3. Connect Web Client
Start your React dashboard:
```bash
cd react-dashboard
npm run dev
```

Then click "Start Scan" in the Digital Twin component.

## Troubleshooting

### "No module named 'rclpy'"
Solution: Make sure you've sourced your ROS2 setup file:
```bash
source /opt/ros/<distro>/setup.bash
```

### "No module named 'websockets'"
Solution: Install the websockets package:
```bash
pip install websockets
```

### "Received empty point cloud"
Possible causes:
- The topic is publishing empty messages
- All points contain NaN values (filtered out)
- Check your point cloud source

### WebSocket Connection Refused
Possible causes:
- Bridge script is not running
- Wrong port number
- Firewall blocking the connection
- Host/IP mismatch

### No Data Received
Check:
```bash
# Is the topic publishing?
ros2 topic hz /stereo/points2

# Are there any errors in the bridge script output?
# Look for error messages in the terminal running the bridge

# Is the web client connected?
# Check browser console for WebSocket errors
```

## Performance Considerations

- **Point Cloud Size**: Large point clouds (>100K points) may cause lag. Consider downsampling.
- **Update Rate**: The bridge processes every message. High frequency topics may impact performance.
- **Network**: Local connections (localhost) are much faster than remote connections.

## Converting to ROS2 Node (Future)

To convert this script into a proper ROS2 node:

1. Move it to a ROS2 package
2. Add node declaration to `setup.py`
3. Use `ros2 run` instead of `python3`
4. Add launch file support

Example `setup.py` entry:
```python
entry_points={
    'console_scripts': [
        'pointcloud_bridge = drone_ai_sim_ros.pointcloud_websocket_bridge:main',
    ],
},
```

## License

Same license as the parent project.

## Support

For issues or questions, refer to the main project documentation or create an issue in the project repository.

