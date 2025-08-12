import asyncio
from langchain.tools import BaseTool
from drone_service import DroneService

# Create a single instance of our drone interface
drone_service = DroneService()

class TakeoffTool(BaseTool):
    name: str = "arm_and_takeoff"
    description: str = "Connects to the drone, arms it, and commands it to take off. This should be the first action in any mission."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")


    async def _arun(self, *args, **kwargs) -> str:
        """Connects, arms, and takes off the drone."""
        print("--- EXECUTING TOOL: Connecting and taking off... ---")
        connected = await drone_service.connect()
        if not connected:
            return "Failed to connect to the drone."
        
        armed = await drone_service.arm()
        if not armed:
            return "Failed to arm the drone."

        took_off = await drone_service.takeoff()
        if not took_off:
            return "Failed to take off."

        return "Takeoff sequence initiated successfully. The drone is now airborne."

class LandTool(BaseTool):
    name: str = "land_drone"
    description: str = "Lands the drone at its current position."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Lands the drone."""
        print("--- EXECUTING TOOL: Landing drone... ---")
        landed = await drone_service.land()
        return "Landed successfully." if landed else "Landing failed."

class GoToTool(BaseTool):
    name: str = "go_to_location"
    description: str = "Flies the drone to a specific GPS coordinate."

    def _run(self, latitude_deg: float, longitude_deg: float, altitude_m: float, yaw_deg: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, latitude_deg: float, longitude_deg: float, altitude_m: float, yaw_deg: float, *args, **kwargs) -> str:
        """Flies to a specific location."""
        print(f"--- EXECUTING TOOL: Flying to {latitude_deg}, {longitude_deg}... ---")
        success = await drone_service.goto_location(latitude_deg, longitude_deg, altitude_m, yaw_deg)
        return "Successfully flew to location." if success else "Failed to fly to location."

class OrbitTool(BaseTool):
    name: str = "fly_in_a_circle"
    description: str = "Commands the drone to fly in a circle at its current location."

    def _run(self, radius_m: float, velocity_ms: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, radius_m: float, velocity_ms: float, *args, **kwargs) -> str:
        """Orbits the drone."""
        print(f"--- EXECUTING TOOL: Orbiting with radius {radius_m}m... ---")
        success = await drone_service.do_orbit(radius_m, velocity_ms)
        return "Orbit complete." if success else "Orbit failed."

class RTLTool(BaseTool):
    name: str = "return_to_launch"
    description: str = "Commands the drone to fly back to its launch point and land."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Returns to launch."""
        print("--- EXECUTING TOOL: Returning to launch... ---")
        success = await drone_service.return_to_launch()
        return "Return to launch initiated." if success else "RTL command failed."

class TelemetryTool(BaseTool):
    name: str = "get_telemetry"
    description: str = "Gets the current position, altitude, and heading of the drone."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Gets telemetry data."""
        print("--- EXECUTING TOOL: Fetching telemetry... ---")
        data = await drone_service.get_telemetry()
        return str(data) if data else "Could not retrieve telemetry."
    
tools = [TakeoffTool(), LandTool(), GoToTool(), OrbitTool(), RTLTool(), TelemetryTool()]

def get_tools():
    return tools

