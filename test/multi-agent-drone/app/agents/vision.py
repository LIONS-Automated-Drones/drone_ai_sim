# app/agents/vision.py
import os
import json
import base64
import requests
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- VLM AGENT TOOLS (MOCK) ---

class AnalyzeImageTool(BaseTool):
    name: str = "analyze_image"
    description: str = "Analyzes the image at 'image.jpeg' and answers a question about it. Always use 'image.jpeg' as the image_path parameter."
    
    def __init__(self):
        super().__init__()
        self._request_count = 0

    def _run(self, image_path: str, question: str, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, image_path: str, question: str, *args, **kwargs) -> str:
        """Analyzes an image from the given path and answers a question about it."""
        self._request_count += 1
        print(f"--- VLM: Analyzing {image_path} for '{question}'... (Request #{self._request_count}) ---")
        
        try:
            # Handle relative paths - look in the app directory
            if not os.path.isabs(image_path):
                # Get the directory where this script is located (app directory)
                app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                image_path = os.path.join(app_dir, image_path)
            
            print(f"--- VLM: Looking for image at: {image_path} ---")
            
            # Check if file exists
            if not os.path.exists(image_path):
                return f"Error: Image file not found at {image_path}"
            
            # Read and encode the image
            with open(image_path, "rb") as image_file:
                image_bytes = image_file.read()
                print(f"--- VLM: Read {len(image_bytes)} bytes from image file ---")
                image_data = base64.b64encode(image_bytes).decode('utf-8')
                print(f"--- VLM: Encoded to {len(image_data)} base64 characters ---")
            
            # Make VLM request to Ollama
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_VLM_MODEL", "llama3.2-vision")
            
            if not model:
                return "Error: OLLAMA_VLM_MODEL environment variable not set"
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Look at this image and answer this question: {question}. Be specific about what you see in the image.",
                        "images": [image_data]
                    }
                ],
                "stream": False
            }
            
            print(f"--- VLM: Making request to {ollama_url}/api/chat with model {model}... ---")
            print(f"--- VLM: Image size: {len(image_data)} characters (base64) ---")
            
            try:
                response = requests.post(f"{ollama_url}/api/chat", json=payload, timeout=120)
                response.raise_for_status()
                
                # Handle potential streaming response by taking only the first JSON object
                response_text = response.text.strip()
                print(f"--- VLM: Raw response text: {response_text[:200]}... ---")
                
                # Try to parse as single JSON first
                try:
                    response_data = response.json()
                except ValueError:
                    # If that fails, try to extract first JSON object from streaming response
                    lines = response_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line:
                            try:
                                response_data = json.loads(line)
                                break
                            except ValueError:
                                continue
                    else:
                        return f"Error: Could not parse JSON response from VLM"
                
                print(f"--- VLM: Response keys: {list(response_data.keys())} ---")
                
                if "message" in response_data and "content" in response_data["message"]:
                    vlm_result = response_data["message"]["content"]
                else:
                    print(f"--- VLM: Unexpected response format: {response_data} ---")
                    return f"Unexpected response format from VLM: {response_data}"
                
                print(f"--- VLM: Raw response: {vlm_result} ---")
                
            except requests.exceptions.Timeout:
                return "Error: VLM request timed out after 120 seconds"
            except requests.exceptions.ConnectionError as e:
                return f"Error: Cannot connect to Ollama server at {ollama_url}: {e}"
            except requests.exceptions.HTTPError as e:
                return f"Error: HTTP error from Ollama server: {e}"
            except Exception as e:
                return f"Error: Unexpected error during VLM request: {e}"
            
            # Check if bicycle is detected and handle landing
            if "car" in vlm_result.lower() or "bike" in vlm_result.lower():
                from agents.pilot import drone_service
                print("--- VLM: Detected car, calling pilot to land... ---")
                success = await drone_service.land()
                if success:
                    return f"{vlm_result}\n\nDrone has been commanded to land."
                else:
                    return f"{vlm_result}\n\nLanding command failed."
            else:
                return vlm_result
                
        except Exception as e:
            print(f"--- VLM: Error during analysis: {e} ---")
            return f"Error analyzing image: {str(e)}"

# --- VLM AGENT DEFINITION ---

def create_vlm_agent():
    """Creates the VLM agent executor."""
    vlm_tools = [AnalyzeImageTool()]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a visual analysis expert. Your job is to analyze images and answer questions based on their content. When asked to analyze an image, always use the analyze_image tool with the image path 'image.jpeg'."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    # Use a regular LLM that supports tools for the vision agent
    # The actual VLM call happens inside the AnalyzeImageTool
    llm = ChatOpenAI(
        model=os.getenv("OLLAMA_MODEL", "llama3.2"),
        openai_api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/v1",
        openai_api_key="ollama",
        temperature=0,
    )
    
    return prompt | llm.bind_tools(vlm_tools)