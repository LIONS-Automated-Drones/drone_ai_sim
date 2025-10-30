from typing import TypedDict, Annotated, List, Dict
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Represents the state of our agent, including conversation history and world memory."""
    messages: Annotated[List[BaseMessage], operator.add]
    world_memory: Dict[str, dict]  # Dictionary of detected objects: {object_id: {class_name, coords}}
