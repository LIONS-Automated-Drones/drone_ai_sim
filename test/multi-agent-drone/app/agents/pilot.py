# app/agents/pilot.py
import os
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Import the service, which will be a shared instance
from services.drone_service import DroneService
from utils import get_bearing_and_move

# Create a single, shared instance of our drone service
drone_service = DroneService()

# --- PILOT AGENT TOOLS ---
# Using BaseTool classes like the working langgraph setup

class ArmAndTakeoffTool(BaseTool):
    name: str = "arm_and_takeoff"
    description: str = "Connects to the drone, arms it, and commands it to take off. This must be the first action."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Connects, arms, and takes off the drone."""
        print("--- PILOT: Connecting and taking off... ---")
        if not await drone_service.connect(): return "Failed to connect to drone."
        if not await drone_service.arm(): return "Failed to arm drone."
        if not await drone_service.takeoff(): return "Failed to take off."
        return "Takeoff successful. Drone is airborne."

class MoveForwardTool(BaseTool):
    name: str = "move_forward"
    description: str = "Moves the drone forward a specified distance in meters relative to its current heading."

    def _run(self, distance_m: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, distance_m: float, *args, **kwargs) -> str:
        """Moves the drone forward a specified distance."""
        print(f"--- PILOT: Moving forward {distance_m}m... ---")
        telemetry = await drone_service.get_telemetry()
        if not telemetry: return "Failed to get telemetry."
        
        # Calculate new position using proper bearing calculation
        new_lat, new_lon = get_bearing_and_move(
            telemetry["latitude_deg"],
            telemetry["longitude_deg"], 
            telemetry["heading_deg"],
            "forward",
            distance_m
        )
        
        success = await drone_service.goto_location(
            new_lat,
            new_lon,
            telemetry["absolute_altitude_m"],
            telemetry["heading_deg"]
        )
        return f"Move forward {distance_m}m complete." if success else "Move failed."

class MoveDirectionTool(BaseTool):
    name: str = "move_direction"
    description: str = "Moves the drone in a specified direction (forward, back, left, right, forward_left, etc.) a specified distance."

    def _run(self, direction: str, distance_m: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, direction: str, distance_m: float, *args, **kwargs) -> str:
        """Moves the drone in a specified direction."""
        print(f"--- PILOT: Moving {direction} {distance_m}m... ---")
        telemetry = await drone_service.get_telemetry()
        if not telemetry: return "Failed to get telemetry."
        
        new_lat, new_lon = get_bearing_and_move(
            telemetry["latitude_deg"],
            telemetry["longitude_deg"], 
            telemetry["heading_deg"],
            direction,
            distance_m
        )
        
        success = await drone_service.goto_location(
            new_lat,
            new_lon,
            telemetry["absolute_altitude_m"],
            telemetry["heading_deg"]
        )
        return f"Move {direction} {distance_m}m complete." if success else "Move failed."

class OrbitLocationTool(BaseTool):
    name: str = "orbit_location"
    description: str = "Makes the drone orbit at its current location with specified radius and velocity."

    def _run(self, radius_m: float, velocity_ms: float = 2.0, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, radius_m: float, velocity_ms: float = 2.0, *args, **kwargs) -> str:
        """Makes the drone orbit at its current location."""
        print(f"--- PILOT: Starting orbit with radius {radius_m}m... ---")
        success = await drone_service.do_orbit(radius_m, velocity_ms)
        return f"Orbit complete with radius {radius_m}m." if success else "Orbit failed."

class ReturnToLaunchTool(BaseTool):
    name: str = "return_to_launch"
    description: str = "Returns the drone to its takeoff location and lands."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Returns the drone to its takeoff location and lands."""
        print("--- PILOT: Returning to launch... ---")
        success = await drone_service.return_to_launch()
        return "Return to launch complete." if success else "Return to launch failed."

class LandDroneTool(BaseTool):
    name: str = "land_drone"
    description: str = "Lands the drone at its current position."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Lands the drone."""
        print("--- PILOT: Landing... ---")
        if not await drone_service.land(): return "Landing failed."
        return "Drone has landed."

class CaptureImageTool(BaseTool):
    name: str = "capture_image"
    description: str = "Captures an image from the drone's camera and returns a file path."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Captures an image from the drone's camera."""
        print("--- PILOT: Capturing image... ---")
        # In a real system, this would trigger a camera and save a file.
        # For now, we return a mock path.
        mock_path = "/tmp/drone_capture.jpg"
        return f"Image captured successfully. Available at: {mock_path}"


# --- PILOT AGENT DEFINITION ---

def create_pilot_agent():
    """Creates the pilot agent executor."""
    pilot_tools = [
        ArmAndTakeoffTool(),
        MoveForwardTool(),
        MoveDirectionTool(),
        OrbitLocationTool(),
        ReturnToLaunchTool(),
        LandDroneTool(),
        CaptureImageTool()
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a drone pilot. Your job is to execute flight commands precisely as requested. You only have access to flight-related tools. Do not ask for clarification, just execute the command."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    llm = ChatOpenAI(
        model=os.getenv("OLLAMA_MODEL"),
        openai_api_base=os.getenv("OLLAMA_BASE_URL") + "/v1",
        openai_api_key="ollama",
        temperature=0,
    )
    
    return prompt | llm.bind_tools(pilot_tools)