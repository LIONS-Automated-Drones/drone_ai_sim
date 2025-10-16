import asyncio
import os
import json
import time
from mavsdk import System
from mavsdk.action import OrbitYawBehavior
from utils import calculate_distance
from mission_log import mission_log, set_telemetry_callback, send_telemetry
from environment_settings import ENVIRONMENT_SETTINGS

class DroneService:
    """A wrapper class for MAVSDK to simplify drone control."""
    def __init__(self):
        self.drone = System()
        self.is_connected = False
        
        # Load connection settings from environment variables
        self.virtual = ENVIRONMENT_SETTINGS.is_gazebo
        if not self.virtual:
            self.serial_port = ENVIRONMENT_SETTINGS.serial_port
            self.baud_rate = ENVIRONMENT_SETTINGS.baud_rate
            self.udp_address = ENVIRONMENT_SETTINGS.udp_address
        else:
            self.udp_address = ENVIRONMENT_SETTINGS.udp_address
        
        # Telemetry streaming
        self.telemetry_streaming = False
        self.telemetry_task = None
        self.takeoff_position = None  # Store initial position for relative calculations

    async def connect(self):
        """
        Connects to the drone - either virtual (Gazebo UDP) or physical (Serial SiK radio).
        """
        if self.is_connected:
            return True
        
        if self.virtual:
            mission_log("--- Connecting to virtual drone (Gazebo)...")
            connection_string = self.udp_address
        else:
            mission_log(f"--- Connecting to physical drone via SiK radio...")
            mission_log(f"--- Serial port: {self.serial_port}, Baud rate: {self.baud_rate}")
            connection_string = f"serial://{self.serial_port}:{self.baud_rate}"
            
        mission_log(f"--- Connection string: {connection_string}")
        await self.drone.connect(system_address=connection_string)

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                mission_log("--- Drone connected!")
                self.is_connected = True
                async for health in self.drone.telemetry.health():
                    mission_log("--- Health status ---")
                    mission_log(health)
                    break
                return True
        return False

    async def arm(self):
        """
        Arms the drone.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot arm.")
            return False
        mission_log("--- Arming drone...")
        await self.drone.action.arm()
        return True

    async def takeoff(self):
        """
        Takes off to a default altitude.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot take off.")
            return False
        
        # Store takeoff position for relative calculations
        position = await anext(self.drone.telemetry.position())
        self.takeoff_position = {
            "latitude_deg": position.latitude_deg,
            "longitude_deg": position.longitude_deg,
            "absolute_altitude_m": position.absolute_altitude_m
        }
        mission_log(f"--- Stored takeoff position: {self.takeoff_position}")
        
        mission_log("--- Taking off...")
        takeoff_altitude = await self.drone.action.get_takeoff_altitude()
        current_altitude = position.absolute_altitude_m
        target_altitude = current_altitude + takeoff_altitude
        mission_log(f"--- Current altitude: {current_altitude}m, Target altitude: {target_altitude}m")
        
        # Start telemetry streaming after storing takeoff position
        await self.start_telemetry_streaming()
        
        await self.drone.action.takeoff()
        i = 0
        while True:
            position = await anext(self.drone.telemetry.position())
            if abs(position.absolute_altitude_m - target_altitude) < 0.25:
                mission_log("--- Drone has reached takeoff altitude.")
                break
            await asyncio.sleep(1)
            if i % 10 == 0:
                mission_log(f"--- Drone has not reached takeoff altitude. Current altitude: {position.absolute_altitude_m}m, target altitude: {target_altitude}m")
            i += 1
        return True

    async def land(self):
        """
        Lands the drone.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot land.")
            return False
        mission_log("--- Landing...")
        await self.drone.action.land()
        async for in_air in self.drone.telemetry.in_air():
            if not in_air:
                mission_log("--- Drone has landed.")
                # Stop telemetry streaming when landed
                await self.stop_telemetry_streaming()
                break
        return True

    async def goto_location(self, latitude_deg, longitude_deg, altitude_m, yaw_deg):
        """
        Commands the drone to fly to a specific GPS location.
        Args:
            latitude_deg (float): Target latitude.
            longitude_deg (float): Target longitude.
            altitude_m (float): Target altitude in meters.
            yaw_deg (float): Target yaw angle in degrees.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot go to location.")
            return False
        mission_log(f"--- Flying to {latitude_deg}, {longitude_deg} at {altitude_m}m...")
        await self.drone.action.goto_location(latitude_deg, longitude_deg, altitude_m, yaw_deg)
        
        while True:
            position = await anext(self.drone.telemetry.position())
            distance = calculate_distance(
                position.latitude_deg,
                position.longitude_deg,
                latitude_deg,
                longitude_deg
            )
            if distance < 1:  # 1-meter tolerance
                mission_log("--- Arrived at target location.")
                break
            await asyncio.sleep(1)
            
        return True

    async def do_orbit(self, radius_m: float, velocity_ms: float):
        """
        Commands the drone to fly in a circle around its current position.
        """
        if not self.is_connected:
            mission_log("--- Drone note connected. Cannot orbit.")
            return False
        
        position = await anext(self.drone.telemetry.position())
        altitude = position.absolute_altitude_m

        mission_log(f"--- Orbiting at current location with radius {radius_m}m...")
        await self.drone.action.do_orbit(
            radius_m=radius_m,
            velocity_ms=velocity_ms,
            yaw_behavior=OrbitYawBehavior.HOLD_FRONT_TANGENT_TO_CIRCLE,
            latitude_deg=position.latitude_deg,
            longitude_deg=position.longitude_deg,
            absolute_altitude_m=altitude
        )
        await asyncio.sleep(15)
        return True
    
    async def return_to_launch(self):
        """
        Commands the drone to return to its takeoff location and land.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot return to launch.")
            return False
        mission_log("--- Returning to launch location...")
        await self.drone.action.return_to_launch()
        async for in_air in self.drone.telemetry.in_air():
            if not in_air:
                mission_log("--- Drone has landed at launch point.")
                break
        return True
    
    async def rotate(self, degrees: float, direction: str):
        """
        Rotates the drone by a specified number of degrees in the given direction.
        Args:
            degrees (float): Number of degrees to rotate (0-360).
            direction (str): Direction to rotate - 'cw' for clockwise, 'ccw' for counterclockwise.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot rotate.")
            return False
        
        # Validate inputs
        if not 0 <= degrees <= 360:
            mission_log(f"--- Invalid rotation angle: {degrees}. Must be between 0 and 360 degrees.")
            return False
        
        if direction not in ['cw', 'ccw']:
            mission_log(f"--- Invalid direction: {direction}. Must be 'cw' or 'ccw'.")
            return False
        
        # Get current telemetry
        telemetry = await self.get_telemetry()
        if not telemetry:
            mission_log("--- Failed to get current telemetry. Cannot rotate.")
            return False
        
        current_heading = telemetry["heading_deg"]
        
        # Calculate new heading
        if direction == 'cw':
            new_heading = (current_heading + degrees) % 360
        else:  # ccw
            new_heading = (current_heading - degrees) % 360
        
        mission_log(f"--- Rotating {degrees}° {direction.upper()} from {current_heading:.1f}° to {new_heading:.1f}°...")
        
        # Rotate in place by going to current position with new heading
        success = await self.goto_location(
            telemetry["latitude_deg"],
            telemetry["longitude_deg"],
            telemetry["absolute_altitude_m"],
            new_heading
        )
        
        if success:
            mission_log(f"--- Rotation complete. New heading: {new_heading:.1f}°")
        else:
            mission_log("--- Rotation failed.")
        
        return success
    
    async def get_telemetry(self):
        """
        Gets the current telemetry data from the drone.
        Returns:
            A dictionary with telemetry data or None if not available.
        """
        if not self.is_connected:
            mission_log("--- Drone not connected. Cannot get telemetry.")
            return None
            
        try:
            # Get the first available telemetry data
            position = await anext(self.drone.telemetry.position())
            heading = await anext(self.drone.telemetry.heading())
            is_in_air = await anext(self.drone.telemetry.in_air())

            telemetry_data = {
                "latitude_deg": position.latitude_deg,
                "longitude_deg": position.longitude_deg,
                "absolute_altitude_m": position.absolute_altitude_m,
                "relative_altitude_m": position.relative_altitude_m,
                "heading_deg": heading.heading_deg,
                "is_in_air": is_in_air
            }
            return telemetry_data
        except Exception as e:
            mission_log(f"--- Error getting telemetry: {e}")
            return None

    async def get_comprehensive_telemetry(self):
        """
        Gets comprehensive telemetry data for streaming to dashboard.
        Returns:
            A dictionary with all required telemetry data or None if not available.
        """
        if not self.is_connected:
            return None
            
        try:
            # Get all required telemetry data
            position = await anext(self.drone.telemetry.position())
            heading = await anext(self.drone.telemetry.heading())
            is_in_air = await anext(self.drone.telemetry.in_air())
            armed = await anext(self.drone.telemetry.armed())
            battery = await anext(self.drone.telemetry.battery())
            gps_info = await anext(self.drone.telemetry.gps_info())
            health_all_ok = await anext(self.drone.telemetry.health_all_ok())
            velocity_ned = await anext(self.drone.telemetry.velocity_ned())
            
            # Get flight mode
            try:
                flight_mode = await anext(self.drone.telemetry.flight_mode())
                flight_mode_str = str(flight_mode).split('.')[-1]  # Extract enum name
            except:
                flight_mode_str = "UNKNOWN"
            
            # Calculate position relative to takeoff
            relative_position = {"x_m": 0.0, "y_m": 0.0, "z_m": 0.0}
            if self.takeoff_position:
                # Calculate distance from takeoff position
                distance_horizontal = calculate_distance(
                    self.takeoff_position["latitude_deg"],
                    self.takeoff_position["longitude_deg"],
                    position.latitude_deg,
                    position.longitude_deg
                )
                
                # Calculate bearing to determine x,y components
                import math
                lat1_rad = math.radians(self.takeoff_position["latitude_deg"])
                lat2_rad = math.radians(position.latitude_deg)
                dlon_rad = math.radians(position.longitude_deg - self.takeoff_position["longitude_deg"])
                
                y = math.sin(dlon_rad) * math.cos(lat2_rad)
                x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad)
                
                bearing_rad = math.atan2(y, x)
                
                relative_position = {
                    "x_m": distance_horizontal * math.cos(bearing_rad),  # North-South (positive = North)
                    "y_m": distance_horizontal * math.sin(bearing_rad),  # East-West (positive = East)
                    "z_m": position.absolute_altitude_m - self.takeoff_position["absolute_altitude_m"]  # Up-Down (positive = Up)
                }
            
            # Calculate total velocity
            velocity_total = math.sqrt(velocity_ned.north_m_s**2 + velocity_ned.east_m_s**2 + velocity_ned.down_m_s**2)
            
            telemetry_data = {
                "type": "telemetry",
                "timestamp": int(time.time() * 1000),  # milliseconds
                "armed": armed,
                "flight_mode": flight_mode_str,
                "battery_percent": battery.remaining_percent,
                "gps_fix_type": str(gps_info.fix_type).split('.')[-1],
                "gps_satellites": gps_info.num_satellites,
                "health_all_ok": health_all_ok,
                "position_relative": relative_position,
                "altitude_m": position.absolute_altitude_m,
                "velocity_ms": velocity_total,
                "heading_deg": heading.heading_deg,
                "is_in_air": is_in_air
            }
            return telemetry_data
        except Exception as e:
            mission_log(f"--- Error getting comprehensive telemetry: {e}")
            return None

    async def start_telemetry_streaming(self):
        """Start streaming telemetry data at 10Hz frequency."""
        if self.telemetry_streaming:
            return  # Already streaming
        
        self.telemetry_streaming = True
        self.telemetry_task = asyncio.create_task(self._telemetry_stream_loop())
        mission_log("--- Telemetry streaming started at 10Hz")

    async def stop_telemetry_streaming(self):
        """Stop streaming telemetry data."""
        self.telemetry_streaming = False
        if self.telemetry_task:
            self.telemetry_task.cancel()
            try:
                await self.telemetry_task
            except asyncio.CancelledError:
                pass
            self.telemetry_task = None
        mission_log("--- Telemetry streaming stopped")

    async def _telemetry_stream_loop(self):
        """Internal loop for streaming telemetry data."""
        try:
            while self.telemetry_streaming and self.is_connected:
                telemetry_data = await self.get_comprehensive_telemetry()
                if telemetry_data:
                    # Send telemetry via the callback (similar to mission_log)
                    await send_telemetry(json.dumps(telemetry_data))
                
                # Wait for 0.5 seconds (2Hz frequency)
                await asyncio.sleep(1/10)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            mission_log(f"--- Error in telemetry streaming: {e}")
            self.telemetry_streaming = False

# Helper to fix a common issue with anext in some environments
async def anext(ait):
    return await ait.__anext__()
