# app/agents/pilot.py
import os
from langchain.tools import BaseTool, tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Import the service, which will be a shared instance
from services.drone_service import DroneService

# Create a single, shared instance of our drone service
drone_service = DroneService()

# --- PILOT AGENT TOOLS ---
# Note: These tools are now async and directly use the async drone_service methods.

@tool
async def arm_and_takeoff() -> str:
    """Connects to the drone, arms it, and commands it to take off. This must be the first action."""
    print("--- PILOT: Connecting and taking off... ---")
    if not await drone_service.connect(): return "Failed to connect to drone."
    if not await drone_service.arm(): return "Failed to arm drone."
    if not await drone_service.takeoff(): return "Failed to take off."
    return "Takeoff successful. Drone is airborne."

@tool
async def move_forward(distance_m: float) -> str:
    """Moves the drone forward a specified distance in meters relative to its current heading."""
    print(f"--- PILOT: Moving forward {distance_m}m... ---")
    telemetry = await drone_service.get_telemetry()
    if not telemetry: return "Failed to get telemetry."
    # Simplified for the example, using a placeholder for calculation
    # In a real scenario, you'd use your get_bearing_and_move function here
    success = await drone_service.goto_location(
        telemetry["latitude_deg"] + 0.0001 * distance_m, # Simplified movement
        telemetry["longitude_deg"],
        telemetry["absolute_altitude_m"],
        telemetry["heading_deg"]
    )
    return f"Move forward {distance_m}m complete." if success else "Move failed."

@tool
async def land_drone() -> str:
    """Lands the drone at its current position."""
    print("--- PILOT: Landing... ---")
    if not await drone_service.land(): return "Landing failed."
    return "Drone has landed."

@tool
async def capture_image() -> str:
    """Captures an image from the drone's camera and returns a file path."""
    print("--- PILOT: Capturing image... ---")
    # In a real system, this would trigger a camera and save a file.
    # For now, we return a mock path.
    mock_path = "/tmp/drone_capture.jpg"
    return f"Image captured successfully. Available at: {mock_path}"


# --- PILOT AGENT DEFINITION ---

def create_pilot_agent():
    """Creates the pilot agent executor."""
    pilot_tools = [arm_and_takeoff, move_forward, land_drone, capture_image]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a drone pilot. Your job is to execute flight commands precisely as requested. You only have access to flight-related tools. Do not ask for clarification, just execute the command."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    llm = ChatOpenAI(
        model=os.getenv("OLLAMA_MODEL"),
        base_url=os.getenv("OLLAMA_BASE_URL") + "/v1",
        api_key="ollama",
        temperature=0,
    )
    
    return prompt | llm.bind_tools(pilot_tools)