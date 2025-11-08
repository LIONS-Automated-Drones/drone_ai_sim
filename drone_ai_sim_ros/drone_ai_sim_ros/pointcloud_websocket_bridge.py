#!/usr/bin/env python3
"""
ROS2 PointCloud2 to WebSocket Bridge (Verbose Debug Version)

Adds detailed logging to help debug network binding and connection issues.
"""

import asyncio
import json
import struct
import argparse
import socket
import threading
from typing import Optional, Dict, Any
import websockets
from aiohttp import web

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Path


class PointCloudWebSocketBridge(Node):
    """Bridge that converts ROS2 PointCloud2 messages to WebSocket JSON."""

    def __init__(self):
        super().__init__('pointcloud_websocket_bridge')

        # Declare parameters
        self.declare_parameter('topic', '/stereo/points2')
        self.declare_parameter('port', 8765)
        self.declare_parameter('host', 'localhost')

        self.topic_name = self.get_parameter('topic').get_parameter_value().string_value
        self.port = self.get_parameter('port').get_parameter_value().integer_value
        self.host = self.get_parameter('host').get_parameter_value().string_value

        self.latest_pointcloud_data: Optional[Dict[str, Any]] = None
        self.latest_pose_data: Optional[Dict[str, Any]] = None
        self.latest_path_data: Optional[Dict[str, Any]] = None
        self.world_memory: Dict[str, Any] = {}
        self.connected_clients: set = set()
        self.data_lock = asyncio.Lock()

        # Subscribe to the PointCloud2 topic
        self.subscription = self.create_subscription(
            PointCloud2,
            self.topic_name,
            self.pointcloud_callback,
            10
        )

        # Subscribe to localization pose
        self.pose_subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/localization_pose',
            self.pose_callback,
            10
        )

        # Subscribe to path
        self.path_subscription = self.create_subscription(
            Path,
            '/mapPath',
            self.path_callback,
            10
        )

        # HTTP Server setup
        self.http_port = 5445
        self.app = None
        self.runner = None
        self.http_thread = None
        
        # Start HTTP server in a separate thread
        self.start_http_server()

        self.get_logger().info("✅ PointCloudWebSocketBridge node initialized.")
        self.get_logger().info(f"🛰️  Subscribed to topic: {self.topic_name}")
        self.get_logger().info(f"📍 Subscribed to pose: /localization_pose")
        self.get_logger().info(f"🛤️  Subscribed to path: /mapPath")
        self.get_logger().info(f"🌐 WebSocket configured for ws://{self.host}:{self.port}")
        self.get_logger().info(f"🔌 HTTP server running on port: {self.http_port}")
        self.get_logger().info("⏳ Waiting for messages...")

    def pointcloud_callback(self, msg: PointCloud2):
        """Callback for PointCloud2 messages. Converts to Three.js format."""
        try:
            vertices = []
            colors = []

            for point in point_cloud2.read_points(msg, field_names=['x', 'y', 'z', 'rgb'], skip_nans=True):
                x, y, z, rgb = point
                vertices.extend([float(x), float(z), float(-y)])

                rgb_bytes = struct.pack('f', rgb)
                rgb_int = struct.unpack('I', rgb_bytes)[0]
                r = ((rgb_int >> 16) & 0xFF) / 255.0
                g = ((rgb_int >> 8) & 0xFF) / 255.0
                b = (rgb_int & 0xFF) / 255.0
                if r == 0 and g == 0 and b == 0:
                    r = g = b = 0.5

                colors.extend([r, g, b])

            if not vertices:
                self.get_logger().warning('⚠️ Received empty point cloud')
                return

            pointcloud_data = {
                'vertices': vertices,
                'colors': colors,
                'timestamp': self.get_clock().now().nanoseconds / 1e9,
                'num_points': len(vertices) // 3,
                'frame_id': msg.header.frame_id
            }

            asyncio.create_task(self.update_pointcloud_data(pointcloud_data))
            self.get_logger().info(f'💾 Processed point cloud with {len(vertices) // 3} points')

        except Exception as e:
            self.get_logger().error(f'💥 Error processing point cloud: {str(e)}')

    def pose_callback(self, msg: PoseWithCovarianceStamped):
        """Callback for localization pose messages."""
        try:
            # Extract position
            position = {
                'x': float(msg.pose.pose.position.x),
                'y': float(msg.pose.pose.position.y),
                'z': float(msg.pose.pose.position.z)
            }

            # Extract orientation (quaternion)
            orientation = {
                'x': float(msg.pose.pose.orientation.x),
                'y': float(msg.pose.pose.orientation.y),
                'z': float(msg.pose.pose.orientation.z),
                'w': float(msg.pose.pose.orientation.w)
            }

            # Extract covariance (6x6 matrix, we'll use the first 3 diagonal elements for position uncertainty)
            covariance = list(msg.pose.covariance)
            
            pose_data = {
                'position': position,
                'orientation': orientation,
                'covariance': covariance,
                'timestamp': self.get_clock().now().nanoseconds / 1e9,
                'frame_id': msg.header.frame_id
            }

            asyncio.create_task(self.update_pose_data(pose_data))
            self.get_logger().debug(f'📍 Updated pose: ({position["x"]:.2f}, {position["y"]:.2f}, {position["z"]:.2f})')

        except Exception as e:
            self.get_logger().error(f'💥 Error processing pose: {str(e)}')

    def path_callback(self, msg: Path):
        """Callback for path messages."""
        try:
            # Extract all poses in the path
            poses = []
            for pose_stamped in msg.poses:
                poses.append({
                    'position': {
                        'x': float(pose_stamped.pose.position.x),
                        'y': float(pose_stamped.pose.position.y),
                        'z': float(pose_stamped.pose.position.z)
                    },
                    'orientation': {
                        'x': float(pose_stamped.pose.orientation.x),
                        'y': float(pose_stamped.pose.orientation.y),
                        'z': float(pose_stamped.pose.orientation.z),
                        'w': float(pose_stamped.pose.orientation.w)
                    }
                })

            path_data = {
                'poses': poses,
                'timestamp': self.get_clock().now().nanoseconds / 1e9,
                'frame_id': msg.header.frame_id,
                'num_poses': len(poses)
            }

            asyncio.create_task(self.update_path_data(path_data))
            self.get_logger().debug(f'🛤️  Updated path with {len(poses)} poses')

        except Exception as e:
            self.get_logger().error(f'💥 Error processing path: {str(e)}')

    async def update_pointcloud_data(self, data: Dict[str, Any]):
        async with self.data_lock:
            self.latest_pointcloud_data = data
            await self.broadcast_to_clients()

    async def update_pose_data(self, data: Dict[str, Any]):
        async with self.data_lock:
            self.latest_pose_data = data
            await self.broadcast_to_clients()

    async def update_path_data(self, data: Dict[str, Any]):
        async with self.data_lock:
            self.latest_path_data = data
            await self.broadcast_to_clients()

    async def broadcast_to_clients(self):
        if not self.connected_clients:
            self.get_logger().debug("No connected WebSocket clients to broadcast to.")
            return

        # Combine all data into a single message
        combined_data = {
            'pointcloud': self.latest_pointcloud_data,
            'pose': self.latest_pose_data,
            'path': self.latest_path_data,
            'world_memory': self.world_memory
        }

        json_data = json.dumps(combined_data)
        disconnected = set()

        for client in self.connected_clients:
            try:
                await client.send(json_data)
            except websockets.exceptions.ConnectionClosed:
                self.get_logger().warning("Client disconnected unexpectedly.")
                disconnected.add(client)
            except Exception as e:
                self.get_logger().error(f'Error sending to client: {str(e)}')
                disconnected.add(client)

        self.connected_clients -= disconnected
        self.get_logger().debug(f'📤 Broadcasted data to {len(self.connected_clients)} active clients.')

    async def handle_client(self, websocket):
        """Handle WebSocket client connections."""
        self.get_logger().info(f'🔌 New client connected from {websocket.remote_address}')
        self.connected_clients.add(websocket)
        self.get_logger().info(f'👥 Total connected clients: {len(self.connected_clients)}')

        try:
            async with self.data_lock:
                # Send all available data to new client
                combined_data = {
                    'pointcloud': self.latest_pointcloud_data,
                    'pose': self.latest_pose_data,
                    'path': self.latest_path_data,
                    'world_memory': self.world_memory
                }
                await websocket.send(json.dumps(combined_data))

            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'ping':
                        await websocket.send(json.dumps({'type': 'pong'}))
                    elif data.get('type') == 'request_data':
                        async with self.data_lock:
                            combined_data = {
                                'pointcloud': self.latest_pointcloud_data,
                                'pose': self.latest_pose_data,
                                'path': self.latest_path_data,
                                'world_memory': self.world_memory
                            }
                            await websocket.send(json.dumps(combined_data))
                except json.JSONDecodeError:
                    self.get_logger().warning(f'Invalid JSON received: {message}')
        except websockets.exceptions.ConnectionClosed:
            self.get_logger().info('🔌 Client disconnected.')
        finally:
            self.connected_clients.discard(websocket)
            self.get_logger().info(f'👥 Clients remaining: {len(self.connected_clients)}')

    def start_http_server(self):
        """Start the aiohttp server in a separate thread."""
        def run_server():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.app = web.Application()
            self.app.router.add_get('/health', self.handle_health)
            self.app.router.add_post('/world_memory', self.handle_world_memory_update)
            
            self.runner = web.AppRunner(self.app)
            loop.run_until_complete(self.runner.setup())
            site = web.TCPSite(self.runner, '0.0.0.0', self.http_port)
            loop.run_until_complete(site.start())
            
            self.get_logger().info(f"✅ HTTP server started on 0.0.0.0:{self.http_port}")
            loop.run_forever()
        
        self.http_thread = threading.Thread(target=run_server, daemon=True)
        self.http_thread.start()
    
    async def handle_health(self, request):
        """Health check endpoint."""
        return web.json_response({
            'status': 'healthy',
            'node': 'pointcloud_websocket_bridge',
            'http_port': self.http_port,
            'websocket_port': self.port,
            'connected_clients': len(self.connected_clients),
            'has_pointcloud': self.latest_pointcloud_data is not None,
            'has_pose': self.latest_pose_data is not None,
            'has_path': self.latest_path_data is not None,
            'world_memory_size': len(self.world_memory)
        })
    
    async def handle_world_memory_update(self, request):
        """HTTP POST endpoint to update world_memory."""
        try:
            data = await request.json()
            self.get_logger().info(f"📥 Received world_memory update: {len(data)} objects")
            
            async with self.data_lock:
                self.world_memory = data
                # Broadcast to all connected clients
                await self.broadcast_to_clients()
            
            return web.json_response({
                'success': True,
                'message': f'Updated world_memory with {len(data)} objects'
            })
        except Exception as e:
            self.get_logger().error(f"💥 Error updating world_memory: {str(e)}")
            return web.json_response({
                'success': False,
                'error': str(e)
            }, status=500)


async def main_async(topic=None, port=None, host=None):
    rclpy.init()
    bridge = PointCloudWebSocketBridge()

    # Allow manual CLI overrides if provided
    if topic:
        bridge.topic_name = topic
    if port:
        bridge.port = port
    if host:
        bridge.host = host

    bridge.get_logger().info(
        f"⚙️  Final config: ws://{bridge.host}:{bridge.port} (topic={bridge.topic_name})"
    )

    async def spin_ros():
        while rclpy.ok():
            rclpy.spin_once(bridge, timeout_sec=0.01)
            await asyncio.sleep(0.01)

    try:
        async with websockets.serve(
            bridge.handle_client,
            bridge.host,
            bridge.port,
            family=socket.AF_INET
        ):
            bridge.get_logger().info(f"✅ WebSocket server started on ws://{bridge.host}:{bridge.port}")
            await spin_ros()
    except Exception as e:
        bridge.get_logger().error(f"💥 Failed to start WebSocket server: {e}")
    finally:
        bridge.get_logger().info("🛑 Shutting down bridge node...")
        bridge.destroy_node()
        rclpy.shutdown()


def main():
    asyncio.run(main_async())



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Bridge ROS2 PointCloud2 topics to WebSocket')
    parser.add_argument('--topic', type=str, default=None)
    parser.add_argument('--port', type=int, default=None)
    parser.add_argument('--host', type=str, default=None)
    args = parser.parse_args()

    asyncio.run(main_async(topic=args.topic, port=args.port, host=args.host))