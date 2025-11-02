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
                "/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU",
                "/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock"
            ],
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
            parameters=[{
                "use_sim_time": True
            }]
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="baselink_to_right",
            arguments=["0.1", "0.12", "0.05", "0", "0", "0", "base_link", "stereo_right_link"],
            parameters=[{
                "use_sim_time": True
            }]
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="rightlink_to_sim_right",
            arguments=["0", "0", "0", "0", "0", "0", "stereo_right_link", "x500_0/stereo_right_link/stereo_right"],
            parameters=[{
                "use_sim_time": True
            }]
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="baselink_to_imu",
            arguments=["0", "0", "0", "0", "0", "0", "base_link", "x500_0/imu_link/imu_sensor"],
            parameters=[{
                "use_sim_time": True
            }]
        ),

        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="stereo_left_optical_tf",
            arguments=["0", "0", "0", "-1.5708", "0", "-1.5708", "stereo_left_link", "stereo_left_optical_frame"],
            parameters=[{
                "use_sim_time": True
            }]
        ),

        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            name="stereo_right_optical_tf",
            arguments=["0", "0", "0", "-1.5708", "0", "-1.5708", "stereo_right_link", "stereo_right_optical_frame"],
            parameters=[{
                "use_sim_time": True
            }]
        ),

        # Republisher
        Node(
            package="drone_ai_sim_ros",
            executable="republish",
            name="camera_republisher",
            output="screen",
            parameters=[{
                "use_sim_time": True
            }]
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
            parameters=[{
                "use_sim_time": True  # Critical for simulation timing
            }]
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
            parameters=[{
                "use_sim_time": True
            }]
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
            parameters=[{
                "use_sim_time": True
            }]
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
                "use_sim_time": True
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
                # Tell it to publish in left optical frame
                "frame_id": "stereo_left_optical_frame",
                "use_sim_time": True
            }],
        ),
        # RTAB-Map SLAM
        Node(
            package="rtabmap_odom",
            executable="stereo_odometry",
            name="stereo_odometry",
            output="screen",
            parameters=[{
                "frame_id": "base_link",
                "odom_frame_id": "odom_stereo",
                "approx_sync": True,
                "approx_sync_max_interval": 0.01,
                "subscribe_imu": True,
                "Vis/UseIMU": True,
                "Vis/IMUGravity": True,
                "queue_size": 30,
                "use_sim_time": True,
                "publish_tf": True
            }],
            remappings=[
                ("left/image_rect", "/stereo/left/image_rect"),  
                ("right/image_rect", "/stereo/right/image_rect"),
                ("left/camera_info", "/stereo/left/camera_info"),
                ("right/camera_info", "/stereo/right/camera_info"),
                ("imu", "/imu/data"),
                ("odom", "/stereo_odometry/odom"),
            ],
        ),

        # -------------------- RTAB-Map SLAM --------------------
        Node(
            package="rtabmap_slam",
            executable="rtabmap",
            name="rtabmap",
            output="screen",
            parameters=[{
                "frame_id": "base_link",
                "subscribe_stereo": True,
                "approx_sync": True,
                "subscribe_odom": True,
                "subscribe_imu": True,
                "delete_db_on_start": True,
                "publish_tf": True,
                "publish_odom_tf": False,
                "publish_trajectory": True,
                "Vis/UseIMU": True,
                "Vis/IMUGravity": True,
                "Optimizer/GravitySigma": "0.1",
                "stereo_optical_frame_id": "stereo_left_optical_frame",
                "stereo_optical_frame_id_right": "stereo_right_optical_frame",
                "use_sim_time": True
            }],
            remappings=[
                ("odom", "/stereo_odometry/odom"),
                ("imu", "/imu/data"),
                ("left/image_rect", "/stereo/left/image_rect"),
                ("right/image_rect", "/stereo/right/image_rect"),
                ("left/camera_info", "/stereo/left/camera_info"),
                ("right/camera_info", "/stereo/right/camera_info"),
            ],
        ),
        # YOLO Perception Node
        Node(
            package="drone_ai_sim_ros",
            executable="yolo_perception_node",
            name="yolo_perception_node",
            output="screen",
            parameters=[{
                "use_sim_time": True,
                "model_name": "yolov8n.pt",
                "confidence_threshold": 0.5,
                "target_frame": "base_link"  # Use base_link - always available from static TF
            }]
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
        Node(
            package="drone_ai_sim_ros",
            executable="pointcloud_websocket_bridge",
            name="pointcloud_websocket_bridge",
            output="screen",
            parameters=[{
                "use_sim_time": True,
                "topic": "/cloud_map",
                "port": 9000,
                "host": "0.0.0.0"
            }]
        ),
    ])
