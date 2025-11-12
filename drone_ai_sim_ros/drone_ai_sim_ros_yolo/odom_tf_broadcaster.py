import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class OdomTFPublisher(Node):
    def __init__(self):
        super().__init__('odom_tf_broadcaster')

        # TF broadcaster automatically respects the node's clock
        self.tf_broadcaster = TransformBroadcaster(self)

        self.sub = self.create_subscription(Odometry, '/odom', self.callback, 10)
        self.get_logger().info("odom_tf_broadcaster node started. Listening to /odom")

    def callback(self, msg: Odometry):
        t = TransformStamped()
        t.header = msg.header
        t.header.frame_id = "odom_stereo"     # <—— instead of msg.header.frame_id
        t.child_frame_id = "base_link"
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = msg.pose.pose.position.z
        t.transform.rotation = msg.pose.pose.orientation
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = OdomTFPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
