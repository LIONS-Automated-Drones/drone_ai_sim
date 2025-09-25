import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseStamped
from tf2_ros import Buffer, TransformListener
import tf2_geometry_msgs  # for do_transform_pose

class OdomTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('odom_trajectory_publisher')

        # TF listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Subscribers & publishers
        self.sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.pub = self.create_publisher(Path, '/trajectory', 10)

        # Path message
        self.path = Path()
        self.path.header.frame_id = "map"  # always in map frame

    def odom_callback(self, msg: Odometry):
        pose_stamped = PoseStamped()
        pose_stamped.header = msg.header
        pose_stamped.pose = msg.pose.pose

        try:
            # Transform from odom → map
            transform = self.tf_buffer.lookup_transform(
                "map",                  # target frame
                msg.header.frame_id,    # source frame (x500_0/odom)
                rclpy.time.Time())
            
            pose_in_map = tf2_geometry_msgs.do_transform_pose(pose_stamped, transform)

            # Append to path
            self.path.poses.append(pose_in_map)
            self.path.header.stamp = self.get_clock().now().to_msg()

            self.pub.publish(self.path)
            self.get_logger().info(f"Trajectory length: {len(self.path.poses)} poses")

        except Exception as e:
            self.get_logger().warn(f"TF transform failed: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = OdomTrajectoryPublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
