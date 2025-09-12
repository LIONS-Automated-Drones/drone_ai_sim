import asyncio
from mavsdk import System
from mavsdk.action import OrbitYawBehavior
from utils import calculate_distance
from mission_log import mission_log

class DroneService:
    """A wrapper class for MAVSDK to simplify drone control."""
    def __init__(self):
        self.drone = System()
        self.is_connected = False

    async def connect(self):
        """
        Connects to the simulated drone.
        """
        if self.is_connected:
            return True
            
        mission_log("--- Connecting to drone...")
        await self.drone.connect(system_address="udp://:14540")

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
        mission_log("--- Taking off...")
        takeoff_altitude = await self.drone.action.get_takeoff_altitude()
        current_altitude =  await anext(self.drone.telemetry.position())
        current_altitude = current_altitude.absolute_altitude_m
        target_altitude = current_altitude + takeoff_altitude
        mission_log(f"--- Current altitude: {current_altitude}m, Target altitude: {target_altitude}m")
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

# Helper to fix a common issue with anext in some environments
async def anext(ait):
    return await ait.__anext__()
