# agent_pilot.py
# The main script that runs the agent and its tools to control the simulated drone.

#ON LINE 142 CHANGE THE IP ADDRESS TO YOU HOST MACHINE TO CONNECT TO OLLAMA SERVER (will make a ENV file to fix this in the future)

import asyncio
import threading
import time
from smolagents import CodeAgent
from smolagents.models import OpenAIServerModel
from smolagents.tools import tool

from drone_interface import DroneInterface

# Create a single instance of our drone interface
drone_ctrl = DroneInterface()

# Dedicated asyncio thread setup
def run_async_loop(loop):
    """Function to run the asyncio event loop in a background thread."""
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.new_event_loop()
async_thread = threading.Thread(target=run_async_loop, args=(loop,), daemon=True)
async_thread.start()


MISSION_PROMPT = """
You are an autonomous drone pilot AI. Your goal is to write a complete Python script to execute a multi-step mission based on the user's request.
You have access to a set of Python tools.
You MUST write a complete, multi-line Python script.
You MUST NOT write any comments in your code.
All lines of code MUST have zero indentation unless they are inside a control structure.
You MUST wrap your entire script in `<code>...</code>` tags.
When the entire mission is complete, you MUST call the `final_answer()` tool with a summary of the mission.

Here is a perfect example of how to structure your code for a mission:
---
Mission: "connect, take off, fly a 5 meter circle, then return and land"
Thought: I will write a script that calls the tools in sequence to complete the mission.
<code>
print(connect_to_drone())
print(arm_and_takeoff())
print(fly_in_a_circle(radius=5.0, velocity=2.0))
print(return_to_home_and_land())
final_answer("Mission complete: connected, took off, flew a 5m circle, and returned to land.")
</code>
---

Now, generate a similar script for the following mission.

Your Mission: {user_request}
"""


# --- Tool Definitions ---
# These are SYNCHRONOUS, but submit their async logic to the background thread.
def run_async_tool(coro):
    """Helper function to run a coroutine on the background loop and get the result."""
    future = asyncio.run_coroutine_threadsafe(coro, loop)
    return future.result()

@tool
def connect_to_drone() -> str:
    """Connects to the drone simulator. Call this first."""
    return run_async_tool(drone_ctrl.connect())

@tool
def arm_and_takeoff() -> str:
    """Arms the drone and then immediately commands it to take off. This is the standard procedure."""
    print("--- Arming and Taking Off ---")
    # We now run the two async functions sequentially inside the tool
    is_armed = run_async_tool(drone_ctrl.arm())
    if not is_armed:
        return "Arming failed. Cannot take off."
    
    is_airborne = run_async_tool(drone_ctrl.takeoff())
    return "Takeoff sequence initiated successfully." if is_airborne else "Takeoff failed after arming."

@tool
def fly_to_gps_location(latitude: float, longitude: float, altitude: float, yaw: float) -> str:
    """
    Flies the drone to a specific GPS coordinate.


    Args:
        latitude (float): The target latitude in degrees.
        longitude (float): The target longitude in degrees.
        altitude (float): The target altitude in meters (absolute).
        yaw (float): The target yaw angle in degrees.
    """
    success = run_async_tool(drone_ctrl.goto_location(latitude, longitude, altitude, yaw))
    return "Successfully flew to location." if success else "Failed to fly to location."

@tool
def fly_in_a_circle(radius: float, velocity: float) -> str:
    """
    Commands the drone to fly in a circle at its current location.

    Args:
        radius (float): The radius of the circle in meters.
        velocity (float): The flight speed in meters per second.
    """
    success = run_async_tool(drone_ctrl.do_orbit(radius, velocity))
    return "Orbit complete." if success else "Orbit failed."

@tool
def return_to_home_and_land() -> str:
    """Commands the drone to fly back to its launch point and land."""
    success = run_async_tool(drone_ctrl.return_to_launch())
    return "Return to launch initiated." if success else "RTL command failed."

@tool
def get_drone_telemetry() -> str:
    """Gets the current position, altitude, and heading of the drone."""
    data = run_async_tool(drone_ctrl.get_telemetry())
    return str(data) if data else "Could not retrieve telemetry."

tool
def is_drone_armed() -> bool:
    """
    Checks if the drone's motors are armed. Returns True if armed, False otherwise.
    """
    return run_async_tool(drone_ctrl.is_armed())

@tool
def wait_for_seconds(seconds: float) -> str:
    """
    Pauses the mission for a specified number of seconds. Use this to hover.

    Args:
        seconds (float): The number of seconds to wait.
    """
    print(f"--- Waiting for {seconds} seconds... ---")
    time.sleep(seconds)
    return f"Waited for {seconds} seconds."

class DronePilotAgent:
    def __init__(self):
        print("--- Initializing Drone Pilot Agent...")
        ollama_model = OpenAIServerModel(
            model_id="codellama:13b",
            api_base="http://192.168.64.1:11434/v1",
            api_key="ollama"
        )
        # --- UPDATED TOOL LIST ---
        self.agent = CodeAgent(
            tools=[
                connect_to_drone,
                arm_and_takeoff,
                fly_to_gps_location,
                fly_in_a_circle,
                return_to_home_and_land,
                get_drone_telemetry,
                wait_for_seconds
            ],
            model=ollama_model,
            add_base_tools=True
        )

    def run_mission(self, prompt: str):
        full_prompt = MISSION_PROMPT.format(user_request=prompt)
        print(f"--- Sending prompt to agent ---")
        self.agent.run(full_prompt)
        print("--- Agent has completed the mission. ---")

def main():
    pilot = DronePilotAgent()
    print("\n--- Drone Pilot Agent is Ready! ---")
    print("Ensure the Gazebo simulation is running in a separate terminal.")
    print("Give the agent a complete mission in one sentence.")
    print("Type 'quit' or 'exit' to close.\n")

    try:
        while True:
            prompt = input("Enter your mission: ")
            if prompt.lower() in ["quit", "exit"]:
                break
            pilot.run_mission(prompt)
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        print("\n--- Shutting down agent and closing event loop. ---")
        loop.call_soon_threadsafe(loop.stop)
        async_thread.join()

if __name__ == "__main__":
    main()
