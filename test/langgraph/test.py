import asyncio
import os
from typing import TypedDict, Annotated, List
import operator
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage
from langchain.tools import BaseTool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import StateGraph, END

from drone_service import DroneService

# Load environment variables from .env file
load_dotenv()


# --- 1. Define a Single, Simplified Tool ---
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

# --- 2. Setup the Agent ---
tools = [TakeoffTool()]
llm = ChatOpenAI(
    model=os.getenv("OLLAMA_MODEL"),
    openai_api_base=os.getenv("OLLAMA_BASE_URL") + "/v1", # Make sure your URL has /v1
    openai_api_key="ollama", # Required but not used by Ollama
    temperature=0,
)

# The agent's "brain" that decides which tool to call
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a drone pilot AI. Your job is to call the correct tools to execute the user's mission. Respond with a final summary when the mission is complete."),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)
agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- 3. Define the Graph's State and Nodes ---

class AgentState(TypedDict):
    """Represents the state of our agent, which is just the conversation history."""
    messages: Annotated[List[BaseMessage], operator.add]

# Node that calls the agent to decide the next action
# Node that calls the agent to decide the next action
async def call_agent_node(state: AgentState):
    print("--- AGENT: Thinking... ---")
    response = await agent_executor.ainvoke(state)
    # Wrap the string output in an AIMessage inside a list
    return {"messages": [AIMessage(content=response["output"])]}

# Node that executes the chosen tool
async def call_tool_node(state: AgentState):
    last_message = state["messages"][-1]
    tool_call = last_message.tool_calls[0]
    # This calls our TakeoffTool._arun() method
    tool_result = await agent_executor.tools[tool_call["name"]].ainvoke(tool_call["args"])
    return {"messages": [ToolMessage(content=str(tool_result), tool_call_id=tool_call["id"])]}

# The conditional edge that decides where to go next
def should_continue(state: AgentState):
    if not state["messages"][-1].tool_calls:
        # If the agent didn't call a tool, the loop is done.
        return "end"
    else:
        # Otherwise, call the tool.
        return "continue"

# --- 4. Build and Compile the Graph ---
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_agent_node)
workflow.add_node("tool", call_tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"continue": "tool", "end": END})
workflow.add_edge("tool", "agent") # Loop back to the agent after the tool runs

app = workflow.compile()

# --- 5. Run the Test ---
async def main():
    print("--- Starting LangGraph Test ---")
    mission_prompt = "Please take off the drone."
    
    # astream() lets us see the output of each node as it runs
    async for event in app.astream({"messages": [HumanMessage(content=mission_prompt)]}):
        # Print the final result from the agent node
        if "agent" in event:
            print("\n--- FINAL AGENT RESPONSE ---")
            print(event["agent"]["messages"])

if __name__ == "__main__":
    asyncio.run(main())