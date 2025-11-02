import asyncio
import time
import os
import aiohttp
from langchain.tools import BaseTool
from drone_service import DroneService
from utils import get_bearing_and_move, get_cardinal_and_move
from mission_log import mission_log

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
    name: str = "land"
    description: str = "Lands the drone at its current position."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Lands the drone."""
        print("--- EXECUTING TOOL: Landing drone... ---")
        landed = await drone_service.land()
        return "Landed successfully." if landed else "Landing failed."

class MoveRelativeBodyTool(BaseTool):
    name: str = "move_relative_self"
    description: str = "Moves the drone a specified distance in a direction relative to its current heading (e.g., 'forward', 'left', 'back_right')."

    def _run(self, direction: str, distance_m: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, direction: str, distance_m: float, *args, **kwargs) -> str:
        """Moves the drone relative to its body."""
        print(f"--- EXECUTING TOOL: Moving {distance_m}m {direction}... ---")
        telemetry = await drone_service.get_telemetry()
        if not telemetry:
            return "Failed to get current telemetry. Cannot move."

        new_lat, new_lon = get_bearing_and_move(
            telemetry["latitude_deg"],
            telemetry["longitude_deg"],
            telemetry["heading_deg"],
            direction,
            distance_m
        )
        
        success = await drone_service.goto_location(
            new_lat, new_lon, telemetry["absolute_altitude_m"], telemetry["heading_deg"]
        )
        return f"Successfully moved {distance_m}m {direction}." if success else "Failed to move."

class MoveRelativeNorthTool(BaseTool):
    name: str = "move_relative_cardinal"
    description: str = "Moves the drone a specified distance in a cardinal direction (e.g., 'N', 'E', 'SW')."

    def _run(self, direction: str, distance_m: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, direction: str, distance_m: float, *args, **kwargs) -> str:
        """Moves the drone in a cardinal direction."""
        print(f"--- EXECUTING TOOL: Moving {distance_m}m {direction}... ---")
        telemetry = await drone_service.get_telemetry()
        if not telemetry:
            return "Failed to get current telemetry. Cannot move."

        new_lat, new_lon = get_cardinal_and_move(
            telemetry["latitude_deg"],
            telemetry["longitude_deg"],
            direction,
            distance_m
        )

        success = await drone_service.goto_location(
            new_lat, new_lon, telemetry["absolute_altitude_m"], telemetry["heading_deg"]
        )
        return f"Successfully moved {distance_m}m {direction}." if success else "Failed to move."

class OrbitTool(BaseTool):
    name: str = "fly_in_a_circle"
    description: str = "Commands the drone to fly in a circle at its current location."

    def _run(self, radius_m: float, velocity_ms: float, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, radius_m: float, velocity_ms: float, *args, **kwargs) -> str:
        """Orbits the drone."""
        print(f"--- EXECUTING TOOL: Orbiting with radius {radius_m}m... ---")
        success = await drone_service.do_orbit(float(radius_m), float(velocity_ms))
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

class RotateTool(BaseTool):
    name: str = "rotate"
    description: str = "Rotates the drone by a specified number of degrees (0-360) in the given direction ('cw' for clockwise, 'ccw' for counterclockwise)."

    def _run(self, degrees: float, direction: str, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, degrees: float, direction: str, *args, **kwargs) -> str:
        """Rotates the drone."""
        print(f"--- EXECUTING TOOL: Rotating {degrees}° {direction.upper()}... ---")
        success = await drone_service.rotate(degrees, direction)
        return f"Successfully rotated {degrees}° {direction.upper()}." if success else f"Failed to rotate {degrees}° {direction.upper()}."

class MissionCompleteTool(BaseTool):
    name: str = "mission_complete"
    description: str = "Call this tool when the entire mission is successfully completed. Provide a final summary of the mission as an argument."

    def _run(self, summary: str) -> str:
        """Marks the mission as complete."""
        return f"Mission complete: {summary}"

    async def _arun(self, *args, **kwargs) -> str:
        """Marks the mission as complete."""
        summary = kwargs.get("summary") or kwargs.get("message") or (args[0] if args else "")
        return f"Mission complete: {summary}"

class CancelTool(BaseTool):
    name: str = "cancel_mission"
    description: str = "Cancels any currently running commands then hovers in place."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Cancels current mission and hovers in place"""
        print("--- EXECUTING TOOL: Canceling and holding... ---")
        success = await drone_service.cancel()
        return "Cancel complete." if success else "Cancel failed."

class TakePictureTool(BaseTool):
    name: str = "take_picture"
    description: str = "Takes a picture with the drone's camera."

    def _run(self, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, *args, **kwargs) -> str:
        """Takes a picture"""
        print("--- EXECUTING TOOL: Taking picture... ---")
        mission_log("TAKE_PICTURE", log_type="COMMAND")
        return "Picture taken successfully."

class SenseObjectsTool(BaseTool):
    name: str = "sense_objects"
    description: str = "Uses the drone's camera and YOLO object detection to identify objects in view and store their 3D locations in memory. Call this when you want to know 'what do you see?'"

    def _run(self, yolo_ip: str = None, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, yolo_ip: str = None, *args, **kwargs) -> str:
        """Triggers object detection and returns detected objects with their 3D positions via HTTP"""
        print("--- EXECUTING TOOL: Sensing objects... ---")
        
        # Get YOLO server IP from parameter or environment variable
        if yolo_ip is None:
            yolo_ip = os.environ.get('YOLO_SERVER_IP', 'localhost')
        
        yolo_url = f"http://{yolo_ip}:5444/detect"
        mission_log(f"--- Connecting to YOLO server at {yolo_url}")
        
        try:
            # Make HTTP POST request to the YOLO detection endpoint
            timeout = aiohttp.ClientTimeout(total=20.0)  # YOLO can take a few seconds
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                mission_log("--- Sending detection request...")
                
                try:
                    async with session.post(yolo_url) as response:
                        if response.status != 200:
                            error_text = await response.text()
                            return f"Error: YOLO server returned status {response.status}: {error_text}"
                        
                        data = await response.json()
                        
                except aiohttp.ClientConnectorError:
                    return f"Error: Could not connect to YOLO server at {yolo_url}. Is the yolo_perception_node running?"
                except asyncio.TimeoutError:
                    return "Error: Request to YOLO server timed out after 20 seconds."
            
            # Check response
            if not data.get('success', False):
                error = data.get('error', 'Unknown error')
                return f"Error: Object detection failed: {error}"
            
            objects = data.get('objects', [])
            
            if not objects:
                mission_log("--- No objects detected")
                return "I looked around but didn't detect any recognizable objects in the current view."
            
            # Format the detected objects
            mission_log(f"--- Detected {len(objects)} objects")
            result_lines = [f"Detected {len(objects)} object(s):"]
            
            # Track objects by class for unique IDs
            class_counts = {}
            
            for obj in objects:
                class_name = obj['class_name']
                map_coords = obj['map_coords']
                
                # Generate unique ID
                if class_name not in class_counts:
                    class_counts[class_name] = 0
                class_counts[class_name] += 1
                object_id = f"{class_name}_{class_counts[class_name]}"
                
                # Format coordinates
                x, y, z = map_coords['x'], map_coords['y'], map_coords['z']
                
                result_lines.append(
                    f"  - {object_id}: {class_name} at map coordinates ({x:.2f}, {y:.2f}, {z:.2f}) meters"
                )
                
                mission_log(f"--- Sensed: {object_id} at ({x:.2f}, {y:.2f}, {z:.2f})")
            
            result = "\n".join(result_lines)
            result += "\n\nNote: These objects have been stored in my memory with their precise 3D locations."
            
            return result
            
        except Exception as e:
            error_msg = f"Error during object detection: {str(e)}"
            mission_log(f"--- {error_msg}")
            import traceback
            mission_log(traceback.format_exc())
            return error_msg

tools = [
    TakeoffTool(),
    LandTool(),
    MoveRelativeBodyTool(),
    MoveRelativeNorthTool(),
    OrbitTool(),
    RTLTool(),
    TelemetryTool(),
    RotateTool(),
    MissionCompleteTool(),
    CancelTool(),
    TakePictureTool(),
    SenseObjectsTool(),
    ]

def get_tools():
    return tools

