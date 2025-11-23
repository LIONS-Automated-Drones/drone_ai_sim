# app/agents/vision.py
import os
import json
import base64
import requests
import re
import cv2
import numpy as np
from langchain.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- VLM AGENT TOOLS ---

def extract_target_object(mission: str) -> str:
    """Extract the target object from the user's mission."""
    mission_lower = mission.lower()
    
    # Common objects to detect
    objects = [
        "car", "vehicle", "automobile", "truck", "van", "suv",
        "human", "person", "people", "man", "woman", "child", "pedestrian",
        "bike", "bicycle", "motorcycle", "scooter",
        "dog", "cat", "animal", "pet",
        "building", "house", "structure",
        "tree", "plant", "vegetation"
    ]
    
    for obj in objects:
        if obj in mission_lower:
            return obj
    
    # If no specific object found, return the first noun-like word
    words = mission_lower.split()
    for word in words:
        if len(word) > 3 and word not in ["if", "you", "see", "then", "land", "takeoff", "pilot", "vision", "image", "in"]:
            return word
    
    return "object"  # fallback

def extract_requested_action(mission: str) -> str:
    """Extract the requested action from the user's mission."""
    mission_lower = mission.lower()
    
    # Look for action keywords
    if "takeoff" in mission_lower or "take off" in mission_lower:
        return "takeoff"
    elif "land" in mission_lower:
        return "land"
    elif "move" in mission_lower:
        return "move"
    elif "fly" in mission_lower:
        return "fly"
    
    return "land"  # default to land for safety

def capture_rtsp_frame(rtsp_url: str) -> tuple[bool, np.ndarray]:
    """
    Capture a single frame from the RTSP stream.
    Returns (success, frame) tuple.
    """
    cap = None
    try:
        print(f"Attempting to connect to RTSP stream: {rtsp_url}")
        
        # Open the RTSP stream with timeout settings
        cap = cv2.VideoCapture(rtsp_url)
        
        # Set buffer size to reduce latency
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not cap.isOpened():
            print(f"Error: Could not open RTSP stream at {rtsp_url}")
            print("Possible causes:")
            print("- RTSP server is not running")
            print("- Network connectivity issues")
            print("- Incorrect RTSP URL")
            print("- Firewall blocking the connection")
            return False, None
        
        # Read a single frame with timeout
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to read frame from RTSP stream")
            print("Possible causes:")
            print("- Stream is not active")
            print("- Network timeout")
            print("- Stream format not supported")
            return False, None
        
        if frame is None or frame.size == 0:
            print("Received empty frame from RTSP stream")
            return False, None
        
        print(f"Successfully captured frame from RTSP stream: {frame.shape}")
        return True, frame
        
    except Exception as e:
        print(f"Error capturing RTSP frame: {e}")
        return False, None
    finally:
        # Always release the capture
        if cap is not None:
            cap.release()

def frame_to_base64(frame: np.ndarray) -> str:
    """
    Convert OpenCV frame to base64 encoded string for VLM.
    """
    try:
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        image_bytes = buffer.tobytes()
        
        # Convert to base64
        image_data = base64.b64encode(image_bytes).decode('utf-8')
        print(f"Converted frame to base64: {len(image_data)} characters")
        return image_data
        
    except Exception as e:
        print(f"Error converting frame to base64: {e}")
        return None

class AnalyzeImageTool(BaseTool):
    name: str = "analyze_image"
    description: str = "Analyzes the live video stream and answers a question about it. Captures a frame from the RTSP stream for analysis."
    
    def __init__(self):
        super().__init__()
        self._request_count = 0

    def _run(self, image_path: str, question: str, *args, **kwargs) -> str:
        raise NotImplementedError("This tool does not support synchronous execution.")

    async def _arun(self, image_path: str, question: str, *args, **kwargs) -> str:
        """Analyzes a live video frame from the RTSP stream and answers a question about it."""
        self._request_count += 1
        
        # Extract target object and requested action from the mission
        target_object = extract_target_object(question)
        requested_action = extract_requested_action(question)
        
        print(f"--- VLM: Extracted target object: '{target_object}' and action: '{requested_action}' from mission: '{question}' ---")
        
        try:
            # Get RTSP URL from environment or use default
            rtsp_url = os.getenv("RTSP_URL", "rtsp://192.168.64.1:8554/live")
            print(f"--- VLM: Capturing frame from RTSP stream: {rtsp_url} ---")
            
            # Capture frame from RTSP stream
            success, frame = capture_rtsp_frame(rtsp_url)
            if not success:
                return f"Error: Could not capture frame from RTSP stream at {rtsp_url}"
            
            # Convert frame to base64 for VLM
            image_data = frame_to_base64(frame)
            if not image_data:
                return "Error: Could not convert frame to base64 for VLM analysis"
            
            # Make VLM request to Ollama
            ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_VLM_MODEL", "llama3.2-vision")
            
            if not model:
                return "Error: OLLAMA_VLM_MODEL environment variable not set"
            
            # Always use simple "what's in the image" prompt
            vlm_prompt = "What's in this image? Be specific about what you see."
            print(f"--- VLM: Using simple prompt: '{vlm_prompt}' (Request #{self._request_count}) ---")
            
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": vlm_prompt,
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
            
            # Check if target object is detected in the response
            vlm_result_lower = vlm_result.lower()
            target_object_lower = target_object.lower()
            
            print(f"--- VLM: Checking if '{target_object_lower}' appears in response ---")
            
            # Check for exact match or related terms
            detected = False
            if target_object_lower in vlm_result_lower:
                detected = True
            else:
                # Check for related terms
                related_terms = {
                    "car": ["vehicle", "automobile", "truck", "van", "suv", "sedan"],
                    "human": ["person", "people", "man", "woman", "child", "pedestrian", "individual"],
                    "bike": ["bicycle", "motorcycle", "scooter", "cycle"],
                    "dog": ["animal", "pet", "canine"],
                    "cat": ["animal", "pet", "feline"]
                }
                
                if target_object_lower in related_terms:
                    for term in related_terms[target_object_lower]:
                        if term in vlm_result_lower:
                            detected = True
                            break
            
            if detected:
                print(f"--- VLM: Detected {target_object}, executing requested action: {requested_action} ---")
                from agents.pilot import drone_service
                
                # Execute the requested action
                if requested_action == "takeoff":
                    # Connect, arm, and takeoff
                    if not await drone_service.connect():
                        return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Failed to connect to drone for takeoff."
                    if not await drone_service.arm():
                        return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Failed to arm drone for takeoff."
                    success = await drone_service.takeoff()
                    if success:
                        return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Drone has been commanded to takeoff."
                    else:
                        return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Takeoff command failed."
                        
                elif requested_action == "land":
                    success = await drone_service.land()
                    if success:
                        return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Drone has been commanded to land."
                    else:
                        return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Landing command failed."
                else:
                    return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' detected. Action '{requested_action}' not implemented."
            else:
                print(f"--- VLM: Target object '{target_object}' not detected in image ---")
                return f"Image analysis: {vlm_result}\n\nTarget object '{target_object}' not detected in image. No action taken."
                
        except Exception as e:
            print(f"--- VLM: Error during analysis: {e} ---")
            return f"Error analyzing image: {str(e)}"

# --- VLM AGENT DEFINITION ---

def create_vlm_agent():
    """Creates the VLM agent executor."""
    vlm_tools = [AnalyzeImageTool()]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a visual analysis expert. Your job is to analyze live video frames and answer questions based on their content. When asked to analyze the video stream, always use the analyze_image tool to capture and analyze the current frame from the RTSP stream."),
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