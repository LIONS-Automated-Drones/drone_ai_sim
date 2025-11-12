#!/home/connor/rosvenv/bin/python
"""
YOLO Perception Node for ARES Drone AI System

This node subscribes to the stereo vision pipeline outputs (color image, disparity map, camera info)
and provides an HTTP API for object detection that:
1. Runs YOLOv8 on the color image to detect objects
2. Uses the disparity map to calculate 3D positions
3. Transforms detected objects to the map frame
4. Returns a list of detected objects with their 3D locations via HTTP
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from stereo_msgs.msg import DisparityImage
from geometry_msgs.msg import Point, PointStamped
from ares_interfaces.srv import DetectObjects
from ares_interfaces.msg import SensedObject

import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
import tf2_ros
import tf2_geometry_msgs
from image_geometry import PinholeCameraModel
import asyncio
import threading
from aiohttp import web

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False


class YOLOPerceptionNode(Node):
    """
    ROS2 node that performs object detection using YOLOv8 and converts 2D detections to 3D positions.
    """

    def __init__(self):
        super().__init__('yolo_perception_node')

        # Check if YOLO is available
        if not YOLO_AVAILABLE:
            self.get_logger().error(
                "ERROR: ultralytics package not found! Please install: pip install ultralytics"
            )
            raise ImportError("ultralytics package required for YOLO detection")

        # Parameters
        self.declare_parameter('model_name', 'yolov8n.pt')  # Nano model for speed
        self.declare_parameter('confidence_threshold', 0.5)
        self.declare_parameter('target_frame', 'map')  # Frame to transform detections to
        self.declare_parameter('mode', 'sim')  # 'sim' for Gazebo or 'hardware' for ZED 2i
        self.declare_parameter('use_sim_time', True)
        self.set_parameters([rclpy.parameter.Parameter('use_sim_time', rclpy.Parameter.Type.BOOL, True)])
        self.get_logger().info("Simulation time (use_sim_time) enabled by default")
        model_name = self.get_parameter('model_name').get_parameter_value().string_value
        self.confidence_threshold = self.get_parameter('confidence_threshold').get_parameter_value().double_value
        self.target_frame = self.get_parameter('target_frame').get_parameter_value().string_value
        self.mode = self.get_parameter('mode').get_parameter_value().string_value

        # Initialize YOLO model
        self.get_logger().info(f"Loading YOLO model: {model_name}")
        self.yolo_model = YOLO(model_name)
        self.get_logger().info("YOLO model loaded successfully")

        # Initialize CV bridge
        self.bridge = CvBridge()

        # Initialize camera model
        self.cam_model = PinholeCameraModel()

        # Initialize TF2 buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # Storage for latest messages
        self.latest_color_image = None
        self.latest_disparity_image = None  # Used in sim mode
        self.latest_depth_image = None      # Used in hardware mode
        self.latest_camera_info = None
        self.camera_model_initialized = False
        
        # Configure topic names and camera frame based on mode
        if self.mode == 'sim':
            color_topic = '/left/image_rect_color'
            depth_topic = '/disparity'
            camera_info_topic = '/stereo/left/camera_info'
            self.camera_frame = "stereo_left_optical_frame"
            self.use_disparity = True  # Sim uses disparity images
        else:  # hardware mode
            color_topic = '/zed2i/zed_node/left/color/rect/image'
            depth_topic = '/zed2i/zed_node/depth/depth_registered'
            camera_info_topic = '/zed2i/zed_node/left/color/rect/camera_info'
            self.camera_frame = "zed2i_left_camera_optical_frame"
            self.use_disparity = False  # ZED uses direct depth images

        # QoS profile for sensor data
        from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Color image subscriber (common)
        self.color_sub = self.create_subscription(
            Image,
            color_topic,
            self.color_callback,
            sensor_qos
        )
        
        # Depth/Disparity subscriber (mode-specific)
        if self.use_disparity:
            self.disparity_sub = self.create_subscription(
                DisparityImage,
                depth_topic,
                self.disparity_callback,
                sensor_qos
            )
        else:
            self.depth_sub = self.create_subscription(
                Image,
                depth_topic,
                self.depth_callback,
                sensor_qos
            )
        
        # Camera info subscriber
        self.camera_info_sub = self.create_subscription(
            CameraInfo,
            camera_info_topic,
            self.camera_info_callback,
            sensor_qos
        )
        
        self.get_logger().info(f"Operating in {self.mode.upper()} mode")
        self.get_logger().info("Subscribed with sensor_data QoS profile")

        # HTTP Server setup
        self.http_port = 5444
        self.app = None
        self.runner = None
        self.http_thread = None
        
        # Start HTTP server in a separate thread
        self.start_http_server()

        self.get_logger().info("YOLO Perception Node initialized")
        self.get_logger().info(f"Color topic: {color_topic}")
        self.get_logger().info(f"Depth topic: {depth_topic}")
        self.get_logger().info(f"Camera info topic: {camera_info_topic}")
        self.get_logger().info(f"HTTP server running on port: {self.http_port}")
        self.get_logger().info(f"Camera frame: {self.camera_frame}")
        self.get_logger().info(f"Target frame: {self.target_frame}")

    def color_callback(self, msg: Image):
        """Store the latest color image."""
        self.latest_color_image = msg

    def disparity_callback(self, msg: DisparityImage):
        """Store the latest disparity image (SIM mode only)."""
        self.latest_disparity_image = msg
    
    def depth_callback(self, msg: Image):
        """Store the latest depth image (HARDWARE mode only)."""
        self.latest_depth_image = msg

    def camera_info_callback(self, msg: CameraInfo):
        """Store the latest camera info and update camera model."""
        self.latest_camera_info = msg
        
        # Only initialize once
        if not self.camera_model_initialized:
            try:
                self.cam_model.fromCameraInfo(msg)
                self.camera_model_initialized = True
                self.get_logger().info(
                    f"Camera model initialized: fx={self.cam_model.fx():.2f}, "
                    f"fy={self.cam_model.fy():.2f}, cx={self.cam_model.cx():.2f}, cy={self.cam_model.cy():.2f}"
                )
            except Exception as e:
                self.get_logger().error(f"Failed to initialize camera model: {str(e)}")
                import traceback
                self.get_logger().error(traceback.format_exc())

    def start_http_server(self):
        """Start the aiohttp server in a separate thread."""
        def run_server():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.app = web.Application()
            self.app.router.add_get('/detect', self.handle_detect)
            self.app.router.add_get('/health', self.handle_health)
            
            self.runner = web.AppRunner(self.app)
            loop.run_until_complete(self.runner.setup())
            site = web.TCPSite(self.runner, '0.0.0.0', self.http_port)
            loop.run_until_complete(site.start())
            
            self.get_logger().info(f"HTTP server started on 0.0.0.0:{self.http_port}")
            loop.run_forever()
        
        self.http_thread = threading.Thread(target=run_server, daemon=True)
        self.http_thread.start()
    
    async def handle_health(self, request):
        """Health check endpoint."""
        return web.json_response({
            'status': 'healthy',
            'node': 'yolo_perception_node',
            'port': self.http_port,
            'mode': self.mode,
            'camera_initialized': self.camera_model_initialized,
            'has_color_image': self.latest_color_image is not None,
            'has_depth_data': (self.latest_disparity_image is not None if self.use_disparity else self.latest_depth_image is not None)
        })
    
    async def handle_detect(self, request):
        """HTTP endpoint for object detection."""
        self.get_logger().info("Detection HTTP endpoint called")
        
        # Perform detection (same logic as old service callback)
        detected_objects = self.perform_detection()
        
        if detected_objects is None:
            return web.json_response({
                'success': False,
                'error': 'Detection failed - missing required data',
                'objects': []
            }, status=500)
        
        return web.json_response({
            'success': True,
            'objects': detected_objects
        })

    def perform_detection(self):
        """
        Performs object detection and returns detected objects as a list of dicts.
        Returns None if required data is missing.
        """
        self.get_logger().info("Performing detection...")

        # Check if we have all required data
        if self.latest_color_image is None:
            self.get_logger().warning("No color image available yet")
            return None
        
        # Check for depth data based on mode
        if self.use_disparity and self.latest_disparity_image is None:
            self.get_logger().warning("No disparity image available yet (SIM mode)")
            return None
        elif not self.use_disparity and self.latest_depth_image is None:
            self.get_logger().warning("No depth image available yet (HARDWARE mode)")
            return None
        
        # Check if camera model is initialized
        if self.latest_camera_info is None or not self.camera_model_initialized:
            self.get_logger().warning("Camera info not available or camera model not initialized")
            return None

        try:
            # Convert ROS Image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(self.latest_color_image, desired_encoding='bgr8')
            
            # Run YOLO detection
            self.get_logger().info("Running YOLO detection...")
            results = self.yolo_model(cv_image, conf=self.confidence_threshold, verbose=False)
            
            # Process detections
            detected_objects = []
            detection_count = 0
            total_detections = 0
            
            for result in results:
                total_detections += len(result.boxes)
            
            self.get_logger().info(f"YOLO found {total_detections} detections above confidence threshold {self.confidence_threshold}")
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get detection info
                    cls_id = int(box.cls[0])
                    class_name = self.yolo_model.names[cls_id]
                    confidence = float(box.conf[0])
                    
                    # Get bounding box center
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    
                    self.get_logger().info(
                        f"  Detected: {class_name} (conf: {confidence:.2f}) at pixel ({cx}, {cy})"
                    )
                    
                    # Get 3D position
                    map_point = self.pixel_to_map_coords(cx, cy)
                    
                    if map_point is not None:
                        # Create dict representation of detected object
                        obj_dict = {
                            'class_name': class_name,
                            'confidence': confidence,
                            'map_coords': {
                                'x': float(map_point.x),
                                'y': float(map_point.y),
                                'z': float(map_point.z)
                            }
                        }
                        detected_objects.append(obj_dict)
                        detection_count += 1
                        
                        self.get_logger().info(
                            f"    → Map coords: ({map_point.x:.2f}, {map_point.y:.2f}, {map_point.z:.2f})"
                        )
                    else:
                        self.get_logger().warning(f"Could not compute 3D position for {class_name}")
            
            self.get_logger().info(f"Detection complete: {detection_count} objects with valid 3D positions")
            return detected_objects
            
        except CvBridgeError as e:
            self.get_logger().error(f"CV Bridge error: {str(e)}")
            return None
        except Exception as e:
            self.get_logger().error(f"Error during detection: {str(e)}")
            import traceback
            self.get_logger().error(traceback.format_exc())
            return None

    def pixel_to_map_coords(self, pixel_x: int, pixel_y: int) -> Point:
        """
        Convert a 2D pixel coordinate to 3D map coordinates using depth/disparity and TF2.
        Handles both simulation (disparity) and hardware (depth) modes.
        
        Args:
            pixel_x: X coordinate in the image
            pixel_y: Y coordinate in the image
            
        Returns:
            Point in the map frame, or None if conversion fails
        """
        try:
            # Get depth based on mode
            if self.use_disparity:
                # SIM MODE: Calculate depth from disparity
                disparity_cv = self.bridge.imgmsg_to_cv2(
                    self.latest_disparity_image.image,
                    desired_encoding='32FC1'
                )
                
                # Ensure pixel coordinates are within image bounds
                height, width = disparity_cv.shape
                pixel_x = max(0, min(pixel_x, width - 1))
                pixel_y = max(0, min(pixel_y, height - 1))
                
                # Get disparity value at pixel
                disparity = disparity_cv[pixel_y, pixel_x]
                
                # Check for invalid disparity
                if np.isnan(disparity) or disparity <= 0:
                    self.get_logger().warning(
                        f"Invalid disparity at ({pixel_x}, {pixel_y}): {disparity} "
                        f"(NaN={np.isnan(disparity)}, <=0={disparity <= 0 if not np.isnan(disparity) else 'N/A'})"
                    )
                    return None
                
                # Calculate depth from disparity
                # Disparity formula: d = f * T / Z  =>  Z = f * T / d
                focal_length = self.latest_disparity_image.f  # Focal length in pixels
                baseline = self.latest_disparity_image.t  # Baseline in meters
                depth = (focal_length * baseline) / disparity
                
                self.get_logger().info(
                    f"[SIM] Depth from disparity: f={focal_length:.2f}px, baseline={baseline:.3f}m, "
                    f"disparity={disparity:.2f}px -> depth={depth:.2f}m"
                )
            else:
                # HARDWARE MODE: Use direct depth from ZED
                depth_cv = self.bridge.imgmsg_to_cv2(
                    self.latest_depth_image,
                    desired_encoding='32FC1'
                )
                
                # Ensure pixel coordinates are within image bounds
                height, width = depth_cv.shape
                pixel_x = max(0, min(pixel_x, width - 1))
                pixel_y = max(0, min(pixel_y, height - 1))
                
                # Get depth value at pixel (ZED depth is already in meters)
                depth = depth_cv[pixel_y, pixel_x]
                
                # Check for invalid depth
                if np.isnan(depth) or depth <= 0:
                    self.get_logger().warning(
                        f"Invalid depth at ({pixel_x}, {pixel_y}): {depth} "
                        f"(NaN={np.isnan(depth)}, <=0={depth <= 0 if not np.isnan(depth) else 'N/A'})"
                    )
                    return None
                
                self.get_logger().info(f"[HARDWARE] Depth from ZED: {depth:.2f}m at pixel ({pixel_x}, {pixel_y})")
            
            # Check for reasonable depth (e.g., between 0.1m and 50m)
            if depth < 0.1 or depth > 50.0:
                self.get_logger().warning(f"Unreasonable depth: {depth:.2f}m (must be 0.1-50m)")
                return None
            
            # Project pixel to 3D ray in camera frame
            try:
                self.get_logger().info(f"Projecting pixel ({pixel_x}, {pixel_y}) to 3D ray...")
                self.get_logger().info(
                    f"   Camera params: fx={self.cam_model.fx():.2f}, fy={self.cam_model.fy():.2f}, "
                    f"cx={self.cam_model.cx():.2f}, cy={self.cam_model.cy():.2f}"
                )
                
                ray = self.cam_model.projectPixelTo3dRay((pixel_x, pixel_y))
                
                self.get_logger().info(f"   Ray type: {type(ray)}, Ray value: {ray}")
                
                if ray is None:
                    self.get_logger().error(
                        f"projectPixelTo3dRay returned None for pixel ({pixel_x}, {pixel_y}). "
                        f"Camera model may not be fully initialized."
                    )
                    return None
                
                self.get_logger().info(f"Ray vector: ({ray[0]:.3f}, {ray[1]:.3f}, {ray[2]:.3f})")
                
            except Exception as e:
                self.get_logger().error(f"Failed to project pixel to 3D ray: {str(e)}")
                import traceback
                self.get_logger().error(traceback.format_exc())
                return None
            
            # Scale ray by depth to get 3D point in camera optical frame
            point_camera = PointStamped()
            point_camera.header.frame_id = self.camera_frame
            point_camera.header.stamp = self.latest_color_image.header.stamp
            point_camera.point.x = ray[0] * depth
            point_camera.point.y = ray[1] * depth
            point_camera.point.z = ray[2] * depth
            
            # Transform to map frame
            try:
                # Wait for transform (with timeout)
                self.get_logger().info(f"Looking up transform: {self.camera_frame} -> {self.target_frame}")
                transform = self.tf_buffer.lookup_transform(
                    self.target_frame,
                    self.camera_frame,
                    rclpy.time.Time(),
                    timeout=rclpy.duration.Duration(seconds=1.0)
                )
                
                point_map = tf2_geometry_msgs.do_transform_point(point_camera, transform)
                self.get_logger().info(f"Transformed to map frame: ({point_map.point.x:.2f}, {point_map.point.y:.2f}, {point_map.point.z:.2f})")
                return point_map.point
                
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, 
                    tf2_ros.ExtrapolationException) as e:
                self.get_logger().warning(f"TF2 transform failed ({self.camera_frame} -> {self.target_frame}): {str(e)}")
                return None
                
        except Exception as e:
            self.get_logger().error(f"Error in pixel_to_map_coords: {str(e)}")
            return None


def main(args=None):
    rclpy.init(args=args)
    node = YOLOPerceptionNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

