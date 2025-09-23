import cv2
import requests
import base64
import time
import os
from dotenv import load_dotenv  # <-- ADD THIS LINE

load_dotenv()  # <-- ADD THIS LINE to load variables from .env

# --- Agent Configuration ---

# NVIDIA API Configuration
NVIDIA_API_URL = "https://ai.api.nvidia.com/v1/vlm/nvidia/vila"
VLM_MODEL = "nvidia/vila-40b"

# Securely get your variables from the loaded .env file
RTSP_URL = os.getenv("RTSP_URL") # <-- CHANGE THIS LINE
NVIDIA_API_KEY = os.getenv("NVAPI_KEY")

# Check that the variables were loaded correctly
if not NVIDIA_API_KEY:
    print("Error: NVAPI_KEY not found in .env file or environment.")
    exit()
if not RTSP_URL:
    print("Error: RTSP_URL not found in .env file or environment.")
    exit()

# --- Tool: VLM Object Detection (NVIDIA API Version) ---
def detect_object_in_stream(prompt: str, rtsp_url: str) -> bool:
    """
    Captures a frame from the RTSP stream and sends it to the NVIDIA VLM for detection.
    """
    try:
        # 1. Capture a single frame from the RTSP stream
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print(f"Error: Could not open RTSP stream at {rtsp_url}.")
            return False

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Failed to read frame from stream.")
            return False

        # 2. Encode the image frame to a base64 string
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        
        image_data_url = f"data:image/jpeg;base64,{image_base64}"

        # 3. Set up headers and payload for the NVIDIA API call
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        payload = {
            "model": VLM_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Does the image contain the following object: {prompt}? Respond with only 'yes' or 'no'."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_data_url}
                        }
                    ]
                }
            ],
            "max_tokens": 10,
            "temperature": 0.20,
            "top_p": 0.70,
            "stream": False
        }

        # 4. Make the API request
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        # 5. Process the response
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        
        return "yes" in content.lower()

    except requests.exceptions.RequestException as e:
        print(f"Error calling NVIDIA API: {e}")
        if e.response is not None:
            print(f"API Response: {e.response.text}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

# --- Agentic Logic ---
# (The rest of your code remains exactly the same)
if __name__ == "__main__":
    print("Starting NVIDIA VLM agent. Press Ctrl+C to stop.")
    while True:
        object_to_find = "hand"
        print(f"Scanning for a '{object_to_find}'...")
        is_detected = detect_object_in_stream(object_to_find, RTSP_URL)
        if is_detected:
            print(f"SUCCESS: A '{object_to_find}' was detected!")
        else:
            print(f"FAILED: No '{object_to_find}' was found.")
        time.sleep(10)