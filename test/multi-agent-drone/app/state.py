# app/state.py
from typing import TypedDict, Annotated, List, Optional
import operator
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Represents the shared state of our multi-agent system."""
    messages: Annotated[List[BaseMessage], operator.add]
    # The agent that should act next.
    next_agent: Optional[str]