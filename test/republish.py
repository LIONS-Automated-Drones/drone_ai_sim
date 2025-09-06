#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CameraInfo

class CameraInfoRelay(Node):
    def __init__(self):
        super().__init__('camera_info_relay')
        self.sub = self.create_subscription(CameraInfo, '/stereo/camera_info', self.callback, 10)
        self.pub_left = self.create_publisher(CameraInfo, '/left/camera_info', 10)
        self.pub_right = self.create_publisher(CameraInfo, '/right/camera_info', 10)
        self.get_logger().info("Relaying /stereo/camera_info -> /left/camera_info and /right/camera_info")

    def callback(self, msg):
        self.pub_left.publish(msg)
        self.pub_right.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = CameraInfoRelay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
