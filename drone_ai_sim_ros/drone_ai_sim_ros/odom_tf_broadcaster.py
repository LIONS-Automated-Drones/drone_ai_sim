import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class OdomTFPublisher(Node):
    def __init__(self):
        super().__init__('odom_tf_broadcaster')

        # ✅ Declare and respect use_sim_time param
        self.declare_parameter('use_sim_time', True)
        use_sim_time = self.get_parameter('use_sim_time').get_parameter_value().bool_value
        if use_sim_time:
            self.get_logger().info("Using simulated time (/clock)")

        # TF broadcaster automatically respects the node's clock
        self.tf_broadcaster = TransformBroadcaster(self)

        self.sub = self.create_subscription(Odometry, '/odom', self.callback, 10)
        self.get_logger().info("odom_tf_broadcaster node started. Listening to /odom")

    def callback(self, msg: Odometry):
        t = TransformStamped()
        t.header = msg.header
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
