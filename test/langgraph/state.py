from typing import TypedDict, Annotated, List, Dict, Optional
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Represents the state of our agent, including conversation history, world memory, and drone telemetry."""
    messages: Annotated[List[BaseMessage], operator.add]
    world_memory: Dict[str, dict]  # Dictionary of detected objects: {object_id: {class_name, coords}}
    drone_state: Optional[Dict]  # Current drone telemetry data including connection status
