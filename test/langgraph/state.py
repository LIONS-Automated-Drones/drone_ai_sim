from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Represents the state of our agent, which is just the conversation history."""
    messages: Annotated[List[BaseMessage], operator.add]
