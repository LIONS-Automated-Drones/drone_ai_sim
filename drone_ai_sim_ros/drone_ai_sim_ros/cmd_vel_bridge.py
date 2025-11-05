#!/usr/bin/env python3
"""
ROS 2 node that subscribes to /cmd_vel and forwards velocity commands via UDP.
This bridges Nav2's velocity commands to the MAVSDK interface via socket communication.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import json

# UDP address for the velocity receiver in test.py
VELOCITY_RECEIVER_ADDR = ("127.0.0.1", 6000)


class CmdVelBridge(Node):
    """
    ROS 2 node that subscribes to /cmd_vel and forwards velocity via UDP socket.
    """

    def __init__(self):
        super().__init__('cmd_vel_bridge')
        
        # Create UDP socket for sending velocity data
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Subscribe to /cmd_vel topic
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10  # QoS depth
        )
        
        self.get_logger().info(f'cmd_vel_bridge started, forwarding /cmd_vel to {VELOCITY_RECEIVER_ADDR}')

    def cmd_vel_callback(self, msg: Twist):
        """
        Callback for /cmd_vel messages.
        Sends the velocity data via UDP to the test.py velocity listener.
        """
        # Package velocity data as JSON
        data = {
            "linear_x": msg.linear.x,
            "linear_y": msg.linear.y,
            "linear_z": msg.linear.z,
            "angular_x": msg.angular.x,
            "angular_y": msg.angular.y,
            "angular_z": msg.angular.z
        }
        
        try:
            # Send via UDP
            self.sock.sendto(json.dumps(data).encode(), VELOCITY_RECEIVER_ADDR)
        except Exception as e:
            self.get_logger().error(f'Failed to send velocity data: {e}')

    def destroy_node(self):
        """Clean up socket on shutdown."""
        self.sock.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    
    node = CmdVelBridge()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

