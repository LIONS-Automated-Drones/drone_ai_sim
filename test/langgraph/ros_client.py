"""
ROS Client Module for LangGraph Agent

This module provides a bridge between the LangGraph agent and ROS2.
It runs an rclpy node in a separate thread to allow the agent to call ROS2 services
without blocking the main asyncio event loop.
"""

import threading
import time
import rclpy
from rclpy.node import Node

# Global variables for the ROS node and thread
g_ros_node = None
g_ros_thread = None
g_ros_lock = threading.Lock()
g_ros_initialized = False


class MinimalROSClient(Node):
    """
    A minimal ROS2 node that can be used to create service clients.
    This node runs in a separate thread and is shared by all tools that need ROS2 access.
    """
    
    def __init__(self):
        super().__init__('langgraph_ros_client')
        self.get_logger().info('LangGraph ROS Client Node initialized')


def spin_ros_node():
    """
    Spin the ROS node in a separate thread.
    This function runs in the background and keeps the ROS node alive.
    """
    global g_ros_node, g_ros_initialized
    
    try:
        import os
        import sys
        
        # Use print instead of mission_log since we're in a separate thread without event loop
        print("[INFO] --- Starting ROS2 client thread...")
        
        # Set up environment for ROS libraries before initializing
        ros_lib_paths = [
            "/opt/ros/jazzy/lib",
            "/home/raytech/repos/drone_ai_sim/install/ares_interfaces/lib"
        ]
        
        # Add to LD_LIBRARY_PATH (though this won't help the current process)
        current_ld = os.environ.get('LD_LIBRARY_PATH', '')
        new_ld_paths = [p for p in ros_lib_paths if os.path.exists(p) and p not in current_ld]
        if new_ld_paths:
            os.environ['LD_LIBRARY_PATH'] = ':'.join(new_ld_paths + ([current_ld] if current_ld else []))
        
        # Preload shared libraries using ctypes
        import ctypes
        
        # First, preload core ROS typesupport libraries (dependencies)
        ros_core_libs = [
            "/opt/ros/jazzy/lib/librosidl_typesupport_c.so",
            "/opt/ros/jazzy/lib/librosidl_typesupport_fastrtps_c.so",
            "/opt/ros/jazzy/lib/librosidl_typesupport_introspection_c.so",
        ]
        
        for lib_path in ros_core_libs:
            try:
                if os.path.exists(lib_path):
                    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
                    print(f"[INFO] --- Preloaded ROS core: {os.path.basename(lib_path)}")
            except Exception as e:
                print(f"[WARN] --- Could not preload {os.path.basename(lib_path)}: {e}")
        
        # Then preload ALL ares_interfaces libraries (in dependency order)
        ares_libs = [
            "libares_interfaces__rosidl_generator_c.so",
            "libares_interfaces__rosidl_typesupport_c.so",
            "libares_interfaces__rosidl_typesupport_fastrtps_c.so",
            "libares_interfaces__rosidl_typesupport_introspection_c.so",
            "libares_interfaces__rosidl_generator_py.so",
            "libares_interfaces__rosidl_typesupport_cpp.so",
            "libares_interfaces__rosidl_typesupport_fastrtps_cpp.so",
            "libares_interfaces__rosidl_typesupport_introspection_cpp.so",
        ]
        
        for lib_name in ares_libs:
            try:
                lib_path = f"/home/raytech/repos/drone_ai_sim/install/ares_interfaces/lib/{lib_name}"
                if os.path.exists(lib_path):
                    ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
                    print(f"[INFO] --- Preloaded: {lib_name}")
            except Exception as e:
                print(f"[WARN] --- Could not preload {lib_name}: {e}")
        
        # Add Python paths
        ros_python_paths = [
            "/opt/ros/jazzy/lib/python3.12/site-packages",
            "/home/raytech/repos/drone_ai_sim/install/ares_interfaces/lib/python3.12/site-packages"
        ]
        for path in ros_python_paths:
            if os.path.exists(path) and path not in sys.path:
                sys.path.insert(0, path)
        
        # Initialize ROS if not already initialized
        if not rclpy.ok():
            rclpy.init()
        
        g_ros_node = MinimalROSClient()
        g_ros_initialized = True
        print("[INFO] --- ROS2 client node created and spinning...")
        
        # Spin the node (this blocks until shutdown)
        rclpy.spin(g_ros_node)
        
    except Exception as e:
        print(f"[ERROR] --- Error in ROS thread: {e}")
        import traceback
        print(traceback.format_exc())
    finally:
        if g_ros_node:
            g_ros_node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        print("[INFO] --- ROS2 client thread terminated")


def start_ros_client_thread():
    """
    Start the ROS client thread if it hasn't been started yet.
    This function is idempotent - it's safe to call multiple times.
    """
    global g_ros_thread, g_ros_initialized
    
    with g_ros_lock:
        if g_ros_thread is None or not g_ros_thread.is_alive():
            g_ros_initialized = False
            g_ros_thread = threading.Thread(target=spin_ros_node, daemon=True)
            g_ros_thread.start()
            
            # Wait for initialization
            timeout = 10.0  # 10 second timeout
            start_time = time.time()
            while not g_ros_initialized and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            if not g_ros_initialized:
                raise RuntimeError("Failed to initialize ROS client within timeout")
            
            print("[INFO] --- ROS2 client thread started successfully")


def get_ros_node() -> MinimalROSClient:
    """
    Get the global ROS node instance, starting the thread if necessary.
    
    Returns:
        The global ROS node instance
        
    Raises:
        RuntimeError: If the ROS node cannot be initialized
    """
    global g_ros_node
    
    # Start the thread if needed
    if g_ros_node is None or not g_ros_initialized:
        start_ros_client_thread()
    
    if g_ros_node is None:
        raise RuntimeError("Failed to get ROS node - initialization failed")
    
    return g_ros_node


def shutdown_ros_client():
    """
    Shutdown the ROS client thread.
    This should be called when the application is exiting.
    """
    global g_ros_node, g_ros_thread
    
    with g_ros_lock:
        if g_ros_node:
            print("[INFO] --- Shutting down ROS client...")
            rclpy.shutdown()
            if g_ros_thread and g_ros_thread.is_alive():
                g_ros_thread.join(timeout=5.0)
            g_ros_node = None
            g_ros_thread = None

