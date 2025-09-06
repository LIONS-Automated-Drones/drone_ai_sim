#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class OdomToTF(Node):
    def __init__(self):
        super().__init__('odom_to_tf')
        self.sub = self.create_subscription(
            Odometry,
            '/model/x500_0/odometry_with_covariance',
            self.callback,
            10)
        self.br = TransformBroadcaster(self)

    def callback(self, msg: Odometry):
        t = TransformStamped()
        t.header = msg.header
        t.child_frame_id = msg.child_frame_id or "base_link"
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        t.transform.rotation = msg.pose.pose.orientation
        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = OdomToTF()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
