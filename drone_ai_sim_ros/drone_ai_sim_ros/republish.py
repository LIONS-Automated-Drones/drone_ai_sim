#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
import yaml
from pathlib import Path
from typing import List


def load_camera_info(yaml_path: str, frame_id: str, logger) -> CameraInfo:
    """
    Load calibration parameters from a YAML file into a CameraInfo message.
    Ensures all matrix arrays are flattened to lists of floats.
    """
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Camera calibration file not found: {yaml_path}")

    with open(path, 'r') as f:
        calib = yaml.safe_load(f)

    def flatten(data) -> List[float]:
        # Some YAML parsers can return nested lists; flatten them safely
        if isinstance(data, list):
            return [float(x) for sub in data for x in (sub if isinstance(sub, list) else [sub])]
        return [float(x) for x in data.values()] if isinstance(data, dict) else [float(data)]

    msg = CameraInfo()
    msg.width = int(calib['image_width'])
    msg.height = int(calib['image_height'])
    msg.distortion_model = calib['distortion_model']
    msg.d = flatten(calib['distortion_coefficients']['data'])
    msg.k = flatten(calib['camera_matrix']['data'])
    msg.r = flatten(calib['rectification_matrix']['data'])
    msg.p = flatten(calib['projection_matrix']['data'])
    msg.header.frame_id = frame_id

    if len(msg.p) != 12:
        logger.warn(f"⚠️ Camera {frame_id}: projection matrix has {len(msg.p)} elements (expected 12)")

    logger.info(f"Loaded calibration for {frame_id}: "
                f"fx={msg.k[0]:.2f}, fy={msg.k[4]:.2f}, "
                f"cx={msg.k[2]:.2f}, cy={msg.k[5]:.2f}, "
                f"P[3]={msg.p[3]:.3f}")

    return msg


class CameraInfoRepublisher(Node):
    def __init__(self):
        super().__init__('stereo_camera_info_republisher')

        left_yaml = Path.home() / '.ros/camera_info/stereo_left.yaml'
        right_yaml = Path.home() / '.ros/camera_info/stereo_right.yaml'

        # Load both cameras
        try:
            self.left_info = load_camera_info(str(left_yaml), "stereo_left_optical_frame", self.get_logger())
            self.right_info = load_camera_info(str(right_yaml), "stereo_right_optical_frame", self.get_logger())
        except FileNotFoundError as e:
            self.get_logger().error(str(e))
            rclpy.shutdown()
            return

        # Publishers
        self.left_info_pub = self.create_publisher(CameraInfo, '/stereo/left/camera_info', 10)
        self.right_info_pub = self.create_publisher(CameraInfo, '/stereo/right/camera_info', 10)
        self.left_img_pub = self.create_publisher(Image, '/stereo/left/image_rect', 10)
        self.right_img_pub = self.create_publisher(Image, '/stereo/right/image_rect', 10)

        # Subscribers
        self.create_subscription(Image, '/stereo/left', self.left_callback, 10)
        self.create_subscription(Image, '/stereo/right', self.right_callback, 10)

        self.frame_count = 0
        self.get_logger().info("✅ Stereo CameraInfo Republisher initialized and running")

        # Extra sanity check: warn if no baseline
        if abs(self.right_info.p[3]) < 1e-3:
            self.get_logger().warn("⚠️ Right camera P[3] is zero — stereo baseline not applied!")

    def left_callback(self, msg: Image):
        msg.header.frame_id = "stereo_left_optical_frame"
        self.left_img_pub.publish(msg)

        self.left_info.header.stamp = msg.header.stamp
        self.left_info_pub.publish(self.left_info)

        self.frame_count += 1
        if self.frame_count % 60 == 0:  # every ~2 seconds at 30Hz
            self.get_logger().info_throttle(5.0, f"Publishing left frame {self.frame_count}")

    def right_callback(self, msg: Image):
        msg.header.frame_id = "stereo_right_optical_frame"
        self.right_img_pub.publish(msg)

        self.right_info.header.stamp = msg.header.stamp
        self.right_info_pub.publish(self.right_info)

        if self.frame_count % 60 == 0:
            self.get_logger().info_throttle(5.0, f"Publishing right frame {self.frame_count}")


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
