#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovariance, TwistWithCovariance
import gz.msgs.odometry_with_covariance_pb2 as gz_odom_cov
import gz.transport13 as gz_transport   # version may differ (13 for Fortress/Harmonic)


class OdomCovBridge(Node):
    def __init__(self):
        super().__init__('odom_cov_bridge')

        # ROS2 publisher
        self.odom_pub = self.create_publisher(Odometry, '/model/x500_0/odometry_with_covariance', 10)

        # Gazebo subscriber
        self.sub = gz_transport.Subscriber(
            '/model/x500_0/odometry_with_covariance',
            gz_odom_cov.OdometryWithCovariance,
            self.gazebo_callback
        )

        self.get_logger().info("Bridging Gazebo OdometryWithCovariance -> ROS2 Odometry")

    def gazebo_callback(self, msg: gz_odom_cov.OdometryWithCovariance):
        ros_msg = Odometry()
        ros_msg.header.stamp = self.get_clock().now().to_msg()
        ros_msg.header.frame_id = "odom"
        ros_msg.child_frame_id = "base_link"

        # Pose
        ros_msg.pose.pose.position.x = msg.pose.pose.position.x
        ros_msg.pose.pose.position.y = msg.pose.pose.position.y
        ros_msg.pose.pose.position.z = msg.pose.pose.position.z
        ros_msg.pose.pose.orientation.x = msg.pose.pose.orientation.x
        ros_msg.pose.pose.orientation.y = msg.pose.pose.orientation.y
        ros_msg.pose.pose.orientation.z = msg.pose.pose.orientation.z
        ros_msg.pose.pose.orientation.w = msg.pose.pose.orientation.w

        # Copy covariance if present
        if msg.pose.HasField("covariance"):
            ros_msg.pose.covariance[:] = msg.pose.covariance

        # Twist
        ros_msg.twist.twist.linear.x = msg.twist.twist.linear.x
        ros_msg.twist.twist.linear.y = msg.twist.twist.linear.y
        ros_msg.twist.twist.linear.z = msg.twist.twist.linear.z
        ros_msg.twist.twist.angular.x = msg.twist.twist.angular.x
        ros_msg.twist.twist.angular.y = msg.twist.twist.angular.y
        ros_msg.twist.twist.angular.z = msg.twist.twist.angular.z

        if msg.twist.HasField("covariance"):
            ros_msg.twist.covariance[:] = msg.twist.covariance

        # Publish to ROS
        self.odom_pub.publish(ros_msg)


def main(args=None):
    rclpy.init(args=args)
    node = OdomCovBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
