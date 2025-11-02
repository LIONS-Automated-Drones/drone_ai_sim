from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    """
    Configurable launch file that supports both Gazebo simulation and ZED 2i hardware.
    
    Usage:
        # Simulation mode (default)
        ros2 launch drone_ai_sim_ros orchestrate.launch.py mode:=sim
        
        # Hardware mode with ZED 2i
        ros2 launch drone_ai_sim_ros orchestrate.launch.py mode:=hardware
    """
    
    # Declare launch arguments
    mode_arg = DeclareLaunchArgument(
        'mode',
        default_value='hardware',
        description='Operating mode: "sim" for Gazebo simulation or "hardware" for ZED 2i camera'
    )
    
    def launch_setup(context, *args, **kwargs):
        mode = LaunchConfiguration('mode').perform(context)
        use_sim_time = (mode == 'sim')
        
        nodes = []
        
        # ==================== SIMULATION-ONLY NODES ====================
        if mode == 'sim':
            # Gazebo <-> ROS bridge (SIM ONLY)
            nodes.append(Node(
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
            ))
            
            # Gazebo-specific TF publishers
            nodes.append(Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="rightlink_to_sim_right",
                arguments=["0", "0", "0", "0", "0", "0", "stereo_right_link", "x500_0/stereo_right_link/stereo_right"],
                parameters=[{"use_sim_time": True}]
            ))
            
            nodes.append(Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="baselink_to_imu",
                arguments=["0", "0", "0", "0", "0", "0", "base_link", "x500_0/imu_link/imu_sensor"],
                parameters=[{"use_sim_time": True}]
            ))
            
            # Camera republisher (SIM ONLY - republishes from Gazebo topics)
            nodes.append(Node(
                package="drone_ai_sim_ros",
                executable="republish",
                name="camera_republisher",
                output="screen",
                parameters=[{"use_sim_time": True}]
            ))
            
            # Image rectification (SIM ONLY - Gazebo images need rectification)
            nodes.extend([
                Node(
                    package="image_proc",
                    executable="rectify_node",
                    name="rectify_right",
                    remappings=[
                        ("image", "/stereo/right"),
                        ("camera_info", "/stereo/right/camera_info"),
                        ("image_rect", "/right/image_rect"),
                    ],
                    parameters=[{"use_sim_time": True}]
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
                    parameters=[{"use_sim_time": True}]
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
                    parameters=[{"use_sim_time": True}]
                ),
            ])
            
            # Stereo disparity (SIM ONLY)
            nodes.append(Node(
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
            ))
            
            # Stereo point cloud (SIM ONLY)
            nodes.append(Node(
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
                    "frame_id": "stereo_left_optical_frame",
                    "use_sim_time": True
                }],
            ))
        
        # ==================== HARDWARE-ONLY NODES ====================
        elif mode == 'hardware':
            # ZED 2i Camera Wrapper (HARDWARE ONLY)
            # Use the official ZED launch file as an IncludeLaunchDescription
            zed_wrapper_dir = get_package_share_directory('zed_wrapper')
            zed_launch_path = os.path.join(zed_wrapper_dir, 'launch', 'zed_camera.launch.py')
            
            nodes.append(IncludeLaunchDescription(
                PythonLaunchDescriptionSource(zed_launch_path),
                launch_arguments={
                    'camera_model': 'zed2i',
                    'camera_name': 'zed2i',
                    'node_name': 'zed_node',
                    'publish_urdf': 'true',
                    'publish_tf': 'true',
                    'publish_map_tf': 'false',  # Let rtabmap handle mapping
                    'publish_imu_tf': 'false',
                    'use_sim_time': 'false',
                    'camera_flip' : 'true'
                }.items()
            ))
            
            # TF from base_link to ZED camera (adjust based on physical mounting)
            nodes.append(Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="base_to_zed",
                arguments=[
                    "0.1", "0", "0.05",  # X, Y, Z offset from base_link (ADJUST FOR YOUR DRONE)
                    "0", "0", "0",        # Roll, Pitch, Yaw
                    "base_link", "zed2i_camera_center"
                ],
                parameters=[{"use_sim_time": False}]
            ))
        
        # ==================== COMMON NODES (BOTH MODES) ====================
        
        # Base camera link TFs (common structure)
        if mode == 'sim':
            # Simulation uses manual stereo setup
            nodes.extend([
                Node(
                    package="tf2_ros",
                    executable="static_transform_publisher",
                    name="baselink_to_left",
                    arguments=["0.1", "0", "0.05", "0", "0", "0", "base_link", "stereo_left_link"],
                    parameters=[{"use_sim_time": use_sim_time}]
                ),
                Node(
                    package="tf2_ros",
                    executable="static_transform_publisher",
                    name="baselink_to_right",
                    arguments=["0.1", "0.12", "0.05", "0", "0", "0", "base_link", "stereo_right_link"],
                    parameters=[{"use_sim_time": use_sim_time}]
                ),
                Node(
                    package="tf2_ros",
                    executable="static_transform_publisher",
                    name="stereo_left_optical_tf",
                    arguments=["0", "0", "0", "-1.5708", "0", "-1.5708", "stereo_left_link", "stereo_left_optical_frame"],
                    parameters=[{"use_sim_time": use_sim_time}]
                ),
                Node(
                    package="tf2_ros",
                    executable="static_transform_publisher",
                    name="stereo_right_optical_tf",
                    arguments=["0", "0", "0", "-1.5708", "0", "-1.5708", "stereo_right_link", "stereo_right_optical_frame"],
                    parameters=[{"use_sim_time": use_sim_time}]
                ),
            ])
        
        # RTAB-Map Stereo Odometry (BOTH MODES)
        rtabmap_image_topics = {
            'sim': {
                'left': '/stereo/left/image_rect',
                'right': '/stereo/right/image_rect',
                'left_info': '/stereo/left/camera_info',
                'right_info': '/stereo/right/camera_info',
                'imu': '/imu/data',
            },
            'hardware': {
                'left': '/zed2i/zed_node/left/image_rect_color',
                'right': '/zed2i/zed_node/right/image_rect_color',
                'left_info': '/zed2i/zed_node/left/camera_info',
                'right_info': '/zed2i/zed_node/right/camera_info',
                'imu': '/zed2i/zed_node/imu/data',
            }
        }
        
        topics = rtabmap_image_topics[mode]
        
        # Stereo point cloud OLD FOR GAZEBO
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
        # RTAB-Map SLAM OLD FOR GAZEBO
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

        # -------------------- RTAB-Map SLAM  OLD FOR GAZEBO --------------------
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
        
        # YOLO Perception Node (BOTH MODES - configured via parameters)
        nodes.append(Node(
            package="drone_ai_sim_ros",
            executable="yolo_perception_node",
            name="yolo_perception_node",
            output="screen",
            parameters=[{
                "use_sim_time": use_sim_time,
                "mode": mode,  # Pass mode to the node
                "model_name": "yolov8n.pt",
                "confidence_threshold": 0.5,
                "target_frame": "base_link"
            }]
        ))
        
        # Web video server (BOTH MODES)
        nodes.append(Node(
            package="web_video_server",
            executable="web_video_server",
            name="web_video_server",
            output="screen",
            parameters=[{
                "address": "0.0.0.0",
                "port": 8080,
            }],
        ))
        
        # PointCloud WebSocket Bridge (BOTH MODES)
        # nodes.append(Node(
        #     package="drone_ai_sim_ros",
        #     executable="pointcloud_websocket_bridge",
        #     name="pointcloud_websocket_bridge",
        #     output="screen",
        #     parameters=[{
        #         "use_sim_time": use_sim_time,
        #         "topic": "/cloud_map",
        #         "port": 9000,
        #         "host": "0.0.0.0"
        #     }]
        # ))
        
        return nodes
    
    return LaunchDescription([
        mode_arg,
        OpaqueFunction(function=launch_setup)
    ])
