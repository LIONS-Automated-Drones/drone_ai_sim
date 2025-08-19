import cv2
import ollama
import base64
import time

# --- Agent Configuration ---
JETSON_IP = "<your_jetson_ip>"
MACBOOK_IP = "<your_macbook_ip>"
OLLAMA_URL = f"http://192.168.1.227:11434"
RTSP_URL = f"rtsp://192.168.1.138:8554/live"
VLM_MODEL = "gemma3:4b"

# --- Tool: VLM Object Detection ---
def detect_object_in_stream(prompt: str, rtsp_url: str) -> bool:
    """
    Captures a frame from the RTSP stream and sends it to the VLM for detection.
    """
    try:
        # Capture a single frame from the RTSP stream
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            print("Error: Could not open RTSP stream.")
            return False

        ret, frame = cap.read()
        cap.release()

        if not ret:
            print("Failed to read frame from stream.")
            return False

        # Encode the image frame to a base64 string
        _, buffer = cv2.imencode('.jpg', frame)
        image_base64 = base64.b64encode(buffer).decode('utf-8')

        # Initialize the Ollama client and send the request
        client = ollama.Client(host=OLLAMA_URL)
        response = client.generate(
            model=VLM_MODEL,
            prompt=f"Does the image contain the following object: {prompt}? Respond with only 'yes' or 'no'.",
            images=[image_base64]
        )

        # Check the response for "yes" or "no"
        return "yes" in response['response'].lower()

    except Exception as e:
        print(f"Error during VLM inference: {e}")
        return False

# --- Agentic Logic ---
if __name__ == "__main__":
    print("Starting VLM agent. Press Ctrl+C to stop.")

    while True:
        # The object you want to look for
        object_to_find = "hand"

        print(f"Scanning for a '{object_to_find}'...")
        is_detected = detect_object_in_stream(object_to_find, RTSP_URL)

        if is_detected:
            print(f"SUCCESS: A '{object_to_find}' was detected!")
        else:
            print(f"FAILED: No '{object_to_find}' was found.")

        # Wait 5 seconds before the next check to avoid overwhelming the Jetson
        time.sleep(50)