#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import yaml
from pathlib import Path


def load_camera_info(yaml_path: str, frame_id: str) -> CameraInfo:
    """
    Load calibration parameters from a YAML file into a CameraInfo message.
    """
    if not Path(yaml_path).exists():
        raise FileNotFoundError(f"Camera calibration file not found: {yaml_path}")

    with open(yaml_path, 'r') as f:
        calib_data = yaml.safe_load(f)

    msg = CameraInfo()
    msg.width = calib_data['image_width']
    msg.height = calib_data['image_height']
    msg.distortion_model = calib_data['distortion_model']
    msg.d = calib_data['distortion_coefficients']['data']
    msg.k = calib_data['camera_matrix']['data']
    msg.r = calib_data['rectification_matrix']['data']
    msg.p = calib_data['projection_matrix']['data']
    msg.header.frame_id = frame_id   # force correct TF frame
    return msg


class CameraInfoRepublisher(Node):
    def __init__(self):
        super().__init__('stereo_camera_info_republisher')


        self.declare_parameter('use_sim_time', True)
        use_sim_time = self.get_parameter('use_sim_time').get_parameter_value().bool_value
        if use_sim_time:
            self.get_logger().info("Using simulated time (/clock)")
        # Paths to calibration files (place them in ~/.ros/camera_info/)
        left_yaml = str(Path.home() / '.ros/camera_info/stereo_left.yaml')
        right_yaml = str(Path.home() / '.ros/camera_info/stereo_right.yaml')

        # Load calibration
        try:
            self.left_info = load_camera_info(left_yaml, "stereo_left_optical_frame")
            self.right_info = load_camera_info(right_yaml, "stereo_right_optical_frame")
        except FileNotFoundError as e:
            self.get_logger().error(str(e))
            rclpy.shutdown()
            return

        # Publishers for CameraInfo
        self.left_info_pub = self.create_publisher(CameraInfo, '/stereo/left/camera_info', 10)
        self.right_info_pub = self.create_publisher(CameraInfo, '/stereo/right/camera_info', 10)

        # Publishers for rectified Images (what rtabmap subscribes to)
        self.left_img_pub = self.create_publisher(Image, '/stereo/left/image_rect', 10)
        self.right_img_pub = self.create_publisher(Image, '/stereo/right/image_rect', 10)

        # Subscriptions to raw Gazebo image topics
        self.create_subscription(Image, '/stereo/left', self.left_callback, 10)
        self.create_subscription(Image, '/stereo/right', self.right_callback, 10)

        self.get_logger().info("Stereo CameraInfo Republisher started. optical frames")

    def left_callback(self, msg: Image):
        # Fix frame_id for image
        msg.header.frame_id = "stereo_left_optical_frame"
        self.left_img_pub.publish(msg)

        # Sync camera_info timestamp and publish
        self.left_info.header.stamp = msg.header.stamp
        self.left_info_pub.publish(self.left_info)

    def right_callback(self, msg: Image):
        msg.header.frame_id = "stereo_right_optical_frame"
        self.right_img_pub.publish(msg)

        self.right_info.header.stamp = msg.header.stamp
        self.right_info_pub.publish(self.right_info)



def main(args=None):
    rclpy.init(args=args)
    node = CameraInfoRepublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
