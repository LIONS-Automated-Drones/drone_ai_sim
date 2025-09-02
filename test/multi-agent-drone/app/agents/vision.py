# app/agents/vision.py
import os
import random
from langchain.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# --- VLM AGENT TOOLS (MOCK) ---

@tool
def analyze_image(image_path: str, question: str) -> str:
    """Analyzes an image from the given path and answers a question about it."""
    print(f"--- VLM: Analyzing {image_path} for '{question}'... ---")
    # This is a MOCK response. In a real system, you would call your VLM here.
    if "chair" in question.lower():
        responses = [
            "A chair is visible in the center of the image.",
            "No chair detected in the current view.",
            "I can see something that looks like a chair on the right side.",
        ]
        return random.choice(responses)
    return "I am unable to answer that question. I can only detect chairs right now."

# --- VLM AGENT DEFINITION ---

def create_vlm_agent():
    """Creates the VLM agent executor."""
    vlm_tools = [analyze_image]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a visual analysis expert. Your job is to analyze images and answer questions based on their content."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    llm = ChatOpenAI(
        model=os.getenv("OLLAMA_MODEL"),
        base_url=os.getenv("OLLAMA_BASE_URL") + "/v1",
        api_key="ollama",
        temperature=0,
    )
    
    return prompt | llm.bind_tools(vlm_tools)