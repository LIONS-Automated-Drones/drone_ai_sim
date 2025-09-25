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
        Node(
            package="drone_ai_sim_ros",
            executable="odom_tf_broadcaster",
            name="odom_tf_broadcaster",
            output="screen",
        ),
        # Static TFs
        # Node(
        #     package="tf2_ros",
        #     executable="static_transform_publisher",
        #     name="odom_to_baselink",
        #     arguments=["0", "0", "0", "0", "0", "0", "x500_0/odom", "base_link"],
        # ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="baselink_to_left",
            arguments=["0.1", "0", "0.05", "0", "0", "0", "base_link", "stereo_left_link"],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="baselink_to_right",
            arguments=["0.1", "0.12", "0.05", "0", "0", "0", "base_link", "stereo_right_link"],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="rightlink_to_sim_right",
            arguments=["0", "0", "0", "0", "0", "0", "stereo_right_link", "x500_0/stereo_right_link/stereo_right"],
        ),

        # Republisher
        Node(
            package="drone_ai_sim_ros",
            executable="republish",
            name="camera_republisher",
            output="screen",
        ),

        # Image rectification
        Node(
            package="image_proc",
            executable="rectify_node",
            name="rectify_right",
            remappings=[
                ("image", "/stereo/right"),
                ("camera_info", "/stereo/right/camera_info"),
                ("image_rect", "/right/image_rect"),
            ],
        ),
        Node(
            package="image_proc",
            executable="rectify_node",
            name="rectify_left_color",
            remappings=[
                ("image", "/stereo/left"),
                ("camera_info", "/stereo/left/camera_info"),
                ("image_rect", "/left/image_rect_color"),
            ],
        ),
        Node(
            package="image_proc",
            executable="rectify_node",
            name="rectify_left",
            remappings=[
                ("image", "/stereo/left"),
                ("camera_info", "/stereo/left/camera_info"),
                ("image_rect", "/left/image_rect"),
            ],
        ),

        # Stereo disparity
        Node(
            package="stereo_image_proc",
            executable="disparity_node",
            name="stereo_disparity",
            remappings=[
                ("left/image_rect", "/left/image_rect"),
                ("right/image_rect", "/right/image_rect"),
                ("left/camera_info", "/stereo/left/camera_info"),
                ("right/camera_info", "/stereo/right/camera_info"),
            ],
            parameters=[{
                "approx_sync": True,
                "queue_size": 20,
            }],
        ),

        # Stereo point cloud
        Node(
            package="stereo_image_proc",
            executable="point_cloud_node",
            name="stereo_pointcloud",
            remappings=[
                ("left/image_rect_color", "/left/image_rect_color"),
                ("right/image_rect", "/right/image_rect"),
                ("left/camera_info", "/stereo/left/camera_info"),
                ("right/camera_info", "/stereo/right/camera_info"),
                ("disparity", "/disparity"),
            ],
            parameters=[{
                "approx_sync": True,
                "queue_size": 20,
            }],
        ),

        # Web video server
        Node(
            package="web_video_server",
            executable="web_video_server",
            name="web_video_server",
            output="screen",
            parameters=[{
                "address": "0.0.0.0",
                "port": 8080,
            }],
        ),
    ])
