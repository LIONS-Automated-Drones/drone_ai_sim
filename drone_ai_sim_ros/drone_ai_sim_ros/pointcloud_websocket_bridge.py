#!/usr/bin/env python3
"""
ROS2 PointCloud2 to WebSocket Bridge

This script subscribes to a ROS2 PointCloud2 topic and publishes the data
over a WebSocket in a format suitable for Three.js rendering.

Usage:
    python pointcloud_websocket_bridge.py --topic /stereo/points2 --port 8765
"""

import asyncio
import json
import struct
import argparse
from typing import Optional, Dict, Any
import websockets

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from sensor_msgs_py import point_cloud2


class PointCloudWebSocketBridge(Node):
    """Bridge that converts ROS2 PointCloud2 messages to WebSocket JSON."""

    def __init__(self, topic_name: str):
        super().__init__('pointcloud_websocket_bridge')
        
        self.topic_name = topic_name
        self.latest_pointcloud_data: Optional[Dict[str, Any]] = None
        self.connected_clients: set = set()
        self.data_lock = asyncio.Lock()
        
        # Subscribe to the PointCloud2 topic
        self.subscription = self.create_subscription(
            PointCloud2,
            topic_name,
            self.pointcloud_callback,
            10
        )
        
        self.get_logger().info(f'Subscribed to topic: {topic_name}')
        self.get_logger().info('Waiting for PointCloud2 messages...')

    def pointcloud_callback(self, msg: PointCloud2):
        """Callback for PointCloud2 messages. Converts to Three.js format."""
        try:
            vertices = []
            colors = []
            
            # Extract points with XYZ and RGB
            for point in point_cloud2.read_points(msg, field_names=['x', 'y', 'z', 'rgb'], skip_nans=True):
                x, y, z, rgb = point
                
                # Add vertex position (negate Z to fix coordinate system)
                vertices.extend([float(x), float(z), float(-y)])
                
                # Extract RGB from packed float/int
                rgb_bytes = struct.pack('f', rgb)
                rgb_int = struct.unpack('I', rgb_bytes)[0]
                
                # Extract color components (0xRRGGBB format)
                r = ((rgb_int >> 16) & 0xFF) / 255.0
                g = ((rgb_int >> 8) & 0xFF) / 255.0
                b = (rgb_int & 0xFF) / 255.0
                
                # Use gray fallback if RGB is all zeros
                if r == 0 and g == 0 and b == 0:
                    r = g = b = 0.5
                
                colors.extend([r, g, b])
            
            if not vertices:
                self.get_logger().warning('Received empty point cloud')
                return
            
            # Create data structure for Three.js
            pointcloud_data = {
                'vertices': vertices,
                'colors': colors,
                'timestamp': self.get_clock().now().nanoseconds / 1e9,
                'num_points': len(vertices) // 3,
                'frame_id': msg.header.frame_id
            }
            
            # Store and broadcast the latest data
            asyncio.create_task(self.update_pointcloud_data(pointcloud_data))
            
            self.get_logger().info(f'Processed point cloud with {len(vertices) // 3} points')
            
        except Exception as e:
            self.get_logger().error(f'Error processing point cloud: {str(e)}')

    async def update_pointcloud_data(self, data: Dict[str, Any]):
        """Update the latest point cloud data thread-safely."""
        async with self.data_lock:
            self.latest_pointcloud_data = data
            await self.broadcast_to_clients(data)

    async def broadcast_to_clients(self, data: Dict[str, Any]):
        """Broadcast point cloud data to all connected WebSocket clients."""
        if not self.connected_clients:
            return
        
        json_data = json.dumps(data)
        
        # Send to all connected clients
        disconnected_clients = set()
        for client in self.connected_clients:
            try:
                await client.send(json_data)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                self.get_logger().error(f'Error sending to client: {str(e)}')
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        self.connected_clients -= disconnected_clients

    async def handle_client(self, websocket):
        """Handle a new WebSocket client connection."""
        self.get_logger().info(f'New client connected from {websocket.remote_address}')
        self.connected_clients.add(websocket)
        
        try:
            # Send the latest data immediately if available
            async with self.data_lock:
                if self.latest_pointcloud_data:
                    await websocket.send(json.dumps(self.latest_pointcloud_data))
            
            # Keep the connection alive and handle incoming messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get('type') == 'ping':
                        await websocket.send(json.dumps({'type': 'pong'}))
                    elif data.get('type') == 'request_data':
                        async with self.data_lock:
                            if self.latest_pointcloud_data:
                                await websocket.send(json.dumps(self.latest_pointcloud_data))
                except json.JSONDecodeError:
                    self.get_logger().warning(f'Received invalid JSON: {message}')
                    
        except websockets.exceptions.ConnectionClosed:
            self.get_logger().info('Client disconnected')
        finally:
            self.connected_clients.discard(websocket)


async def main():
    """Main entry point for the bridge."""
    parser = argparse.ArgumentParser(
        description='Bridge ROS2 PointCloud2 topics to WebSocket'
    )
    parser.add_argument(
        '--topic',
        type=str,
        default='/stereo/points2',
        help='ROS2 PointCloud2 topic name (default: /stereo/points2)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=8765,
        help='WebSocket server port (default: 8765)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='WebSocket server host (default: localhost)'
    )
    
    args = parser.parse_args()
    
    # Initialize ROS2
    rclpy.init()
    
    # Create the bridge node
    bridge = PointCloudWebSocketBridge(args.topic)
    
    # Create WebSocket server
    print(f'Starting WebSocket server on ws://{args.host}:{args.port}')
    print(f'Subscribing to ROS2 topic: {args.topic}')
    print('Press Ctrl+C to stop')
    
    async def spin_ros():
        """Spin ROS2 in the async event loop."""
        while rclpy.ok():
            rclpy.spin_once(bridge, timeout_sec=0.01)
            await asyncio.sleep(0.01)
    
    # Start WebSocket server and ROS2 spinning concurrently
    async with websockets.serve(bridge.handle_client, args.host, args.port):
        try:
            await spin_ros()
        except KeyboardInterrupt:
            print('\nShutting down...')
        finally:
            bridge.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    asyncio.run(main())
