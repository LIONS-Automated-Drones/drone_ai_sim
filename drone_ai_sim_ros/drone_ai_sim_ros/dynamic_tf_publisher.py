#!/usr/bin/env python3
import math, sys, rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class DynamicTFPublisher(Node):
    def __init__(self):
        super().__init__('dynamic_tf_publisher')
        if len(sys.argv) < 9:
            self.get_logger().error(
                "Usage: dynamic_tf_publisher parent child x y z roll pitch yaw [rate]"
            )
            sys.exit(1)

        self.parent = sys.argv[1]
        self.child = sys.argv[2]
        self.xyz = [float(v) for v in sys.argv[3:6]]
        self.rpy = [float(v) for v in sys.argv[6:9]]
        self.rate = float(sys.argv[9]) if len(sys.argv) > 9 else 10.0

        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(1.0 / self.rate, self.publish_tf)
        self.get_logger().info(f"Publishing {self.parent}->{self.child} at {self.rate} Hz")

    def publish_tf(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = self.parent
        t.child_frame_id = self.child
        t.transform.translation.x, t.transform.translation.y, t.transform.translation.z = self.xyz

        # RPY → quaternion
        cr = math.cos(self.rpy[0] / 2)
        sr = math.sin(self.rpy[0] / 2)
        cp = math.cos(self.rpy[1] / 2)
        sp = math.sin(self.rpy[1] / 2)
        cy = math.cos(self.rpy[2] / 2)
        sy = math.sin(self.rpy[2] / 2)
        t.transform.rotation.w = cr * cp * cy + sr * sp * sy
        t.transform.rotation.x = sr * cp * cy - cr * sp * sy
        t.transform.rotation.y = cr * sp * cy + sr * cp * sy
        t.transform.rotation.z = cr * cp * sy - sr * sp * cy

        self.br.sendTransform(t)

def main():
    rclpy.init()
    node = DynamicTFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
