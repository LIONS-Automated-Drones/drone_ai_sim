#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=[
                "ros2", "run", "ros_gz_bridge", "parameter_bridge",
                "/stereo/left@sensor_msgs/msg/Image@gz.msgs.Image",
                "/stereo/right@sensor_msgs/msg/Image@gz.msgs.Image",
                "/stereo/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
                "/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry",
            ],
            output="screen"
        ),

        ExecuteProcess(
            cmd=["ros2", "run", "tf2_ros", "static_transform_publisher",
                 "0", "0", "0", "0", "0", "0", "x500_0/odom", "base_link"],
            output="screen"
        ),
        ExecuteProcess(
            cmd=["ros2", "run", "tf2_ros", "static_transform_publisher",
                 "0.1", "0", "0.05", "0", "0", "0", "base_link", "stereo_left"],
            output="screen"
        ),
        ExecuteProcess(
            cmd=["ros2", "run", "tf2_ros", "static_transform_publisher",
                 "0.1", "0.12", "0.05", "0", "0", "0", "base_link", "stereo_right"],
            output="screen"
        ),

        # Call your raw python script
        ExecuteProcess(
            cmd=["python3", "/home/connor/sd1_ws/drone_ai_sim/test/republish.py"],
            output="screen"
        ),
    ])
