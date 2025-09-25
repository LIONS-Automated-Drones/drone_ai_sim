import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from rtabmap_msgs.msg import MapGraph

class TrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('trajectory_publisher')
        self.sub = self.create_subscription(MapGraph, '/mapGraph', self.callback, 10)
        self.pub = self.create_publisher(Path, '/trajectory', 10)

    def callback(self, msg: MapGraph):
        path = Path()
        path.header.stamp = self.get_clock().now().to_msg()
        path.header.frame_id = msg.header.frame_id if msg.header.frame_id else "map"

        for i, pose in enumerate(msg.poses):
            pose_stamped = PoseStamped()
            pose_stamped.header = path.header
            pose_stamped.pose = pose
            path.poses.append(pose_stamped)

        self.pub.publish(path)
        self.get_logger().info(f"Published trajectory with {len(path.poses)} poses")

def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryPublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
