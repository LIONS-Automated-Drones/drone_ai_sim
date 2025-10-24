#!/usr/bin/env python3
import asyncio
import threading
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import aiohttp


class CmdVelMavsdkBridge(Node):
    """
    ROS 2 node that subscribes to /cmd_vel and forwards linear/angular velocities to the API endpoint.
    """
    def __init__(self):
        super().__init__("cmd_vel_mavsdk_bridge")
        self.ros_messages = 0
        self.api_messages = 0
        # Parameters
        self.declare_parameter("api_url", "http://localhost:3223/api/velocity")
        self.declare_parameter("yaw_rate_scale", 4.0)  # Scale factor for yaw rate (default 25x)
        self.api_url = self.get_parameter("api_url").get_parameter_value().string_value
        self.yaw_rate_scale = self.get_parameter("yaw_rate_scale").get_parameter_value().double_value

        # Create a new event loop for async operations
        self.loop = asyncio.new_event_loop()
        
        # HTTP session for making requests
        self.session = None
        
        # Start event loop in separate thread
        self.loop_thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self.loop_thread.start()
        
        # Wait for session to be created
        future = asyncio.run_coroutine_threadsafe(self.setup_http_session(), self.loop)
        future.result(timeout=5.0)

        # ROS 2 subscriber
        self.subscription = self.create_subscription(
            Twist, "/cmd_vel", self.cmd_vel_callback, 10
        )

        # Last received Twist
        self.last_twist = Twist()

        # Start the periodic velocity sender (10 Hz)
        self.timer = self.create_timer(0.10, self.send_velocity_command)
        self.get_logger().info(f"cmd_vel → API bridge initialized. Sending to {self.api_url}")
        self.get_logger().info(f"Yaw rate scaling factor: {self.yaw_rate_scale}x")

    def _run_event_loop(self):
        """
        Run the event loop in a separate thread.
        """
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
    
    async def setup_http_session(self):
        """
        Setup aiohttp session for API requests.
        """
        self.session = aiohttp.ClientSession()
        self.get_logger().info("HTTP session created for API communication.")

    def cmd_vel_callback(self, msg: Twist):
        """
        Store the latest /cmd_vel message for periodic sending.
        """
        self.last_twist = msg
        self.ros_messages += 1
        if self.ros_messages % 100 == 0:
            self.get_logger().info(f"Received cmd_vel: {msg}")

    def send_velocity_command(self):
        """
        Periodic timer callback that sends latest Twist via HTTP API.
        """
        if not self.session:
            return

        # ROS 2 Twist uses m/s in robot body frame:
        # linear.x → forward, linear.y → left, linear.z → up, angular.z → yaw rate (rad/s)
        vx = self.last_twist.linear.x
        vy = -self.last_twist.linear.y  # PX4 body frame: right = positive Y
        vz = -self.last_twist.linear.z  # PX4 NED frame: down = positive Z
        # Convert rad/s → deg/s and apply scaling factor for more responsive rotation
        yaw_rate = self.last_twist.angular.z * 180.0 / 3.1415926 * self.yaw_rate_scale
        self.api_messages += 1
        if self.api_messages % 100 == 0:
            self.get_logger().info(f"Sending velocity command: {vx}, {vy}, {vz}, {yaw_rate}")
        if vx == 0 and vy == 0 and vz == 0 and yaw_rate == 0:
            return
            
        # Send asynchronously without blocking the ROS 2 thread
        asyncio.run_coroutine_threadsafe(self._async_send_velocity(vx, vy, vz, yaw_rate), self.loop)

    async def _async_send_velocity(self, vx, vy, vz, yaw_rate):
        """
        Sends velocity command via HTTP API.
        """
        try:
            payload = {
                'vx': vx,
                'vy': vy,
                'vz': vz,
                'yaw_rate': yaw_rate
            }
            async with self.session.post(self.api_url, json=payload, timeout=aiohttp.ClientTimeout(total=0.5)) as response:
                if response.status != 200:
                    self.get_logger().warn(f"API request failed with status {response.status}")
        except asyncio.TimeoutError:
            self.get_logger().warn("API request timed out")
        except Exception as e:
            self.get_logger().warn(f"Velocity send failed: {e}")

    def destroy_node(self):
        """
        Clean shutdown.
        """
        self.get_logger().info("Shutting down bridge...")
        if self.session:
            # Close session in the event loop thread
            future = asyncio.run_coroutine_threadsafe(self.session.close(), self.loop)
            try:
                future.result(timeout=2.0)
            except Exception as e:
                self.get_logger().warn(f"Error closing session: {e}")
        
        # Stop the event loop
        self.loop.call_soon_threadsafe(self.loop.stop)
        if self.loop_thread.is_alive():
            self.loop_thread.join(timeout=2.0)
        
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelMavsdkBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
