from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Gazebo <-> ROS bridge
        Node(
            package="ros_gz_bridge",
            executable="parameter_bridge",
            name="gz_bridge",
            output="screen",
            arguments=[
                "/stereo/left@sensor_msgs/msg/Image@gz.msgs.Image",
                "/stereo/right@sensor_msgs/msg/Image@gz.msgs.Image",
                "/stereo/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
                "/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry",
            ],
        ),

        # Static TFs
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="odom_to_baselink",
            arguments=["0", "0", "0", "0", "0", "0", "x500_0/odom", "base_link"],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="baselink_to_left",
            arguments=["0.1", "0", "0.05", "0", "0", "0", "base_link", "stereo_left"],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="baselink_to_right",
            arguments=["0.1", "0.12", "0.05", "0", "0", "0", "base_link", "stereo_right"],
        ),

        # Your republisher node
        Node(
            package="drone_ai_sim_ros",
            executable="republish",
            name="camera_republisher",
            output="screen",
        ),
    ])
