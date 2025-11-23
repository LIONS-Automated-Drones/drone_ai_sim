import cv2
import ollama
import base64
import time
import requests
import numpy as np
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()
# --- Agent Configuration ---
OLLAMA_URL = os.getenv("OLLAMA_URL")
ROS_VIDEO_URL = os.getenv("ROS_VIDEO_URL")
VLM_MODEL = os.getenv("VLM_MODEL")

# --- Tool: VLM Object Detection ---
def detect_object_in_stream(prompt: str, ros_video_url: str, show_visualization: bool = True) -> tuple[bool, Optional[np.ndarray]]:
    """
    Captures a frame from the ROS web video server HTTP multipart stream and sends it to the VLM for detection.
    
    Args:
        prompt: The object to detect
        ros_video_url: The ROS web video server URL
        show_visualization: Whether to return the frame for visualization
        
    Returns:
        tuple: (detection_result, frame) - detection result and the captured frame
    """
    try:
        # Get a single frame from the HTTP multipart stream
        frame = capture_frame_from_multipart_stream(ros_video_url)
        
        if frame is None:
            print("Failed to capture frame from ROS video stream.")
            return False, None

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
        detection_result = "yes" in response['response'].lower()
        
        return detection_result, frame if show_visualization else None

    except Exception as e:
        print(f"Error during VLM inference: {e}")
        return False, None

def capture_frame_from_multipart_stream(url: str, timeout: int = 10) -> Optional[np.ndarray]:
    """
    Captures a single frame from an HTTP multipart stream (like ROS web video server).
    
    Args:
        url: The HTTP multipart stream URL
        timeout: Timeout in seconds for the request
        
    Returns:
        numpy.ndarray: The captured frame, or None if failed
    """
    try:
        # Start a session to get the multipart stream
        session = requests.Session()
        response = session.get(url, stream=True, timeout=timeout)
        
        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code} when accessing {url}")
            return None
        
        # Define the boundary string (common for MJPEG streams)
        boundary = b"--boundarydonotcross"
        
        # Initialize buffer to hold stream data
        buffer = b""
        
        # Read chunks until we get a complete frame
        for chunk in response.iter_content(chunk_size=1024):
            buffer += chunk
            
            # Look for the start of a frame
            start = buffer.find(boundary)
            if start == -1:
                continue
                
            # Find the end of headers (double CRLF)
            headers_end = buffer.find(b"\r\n\r\n", start)
            if headers_end == -1:
                continue
                
            # Extract frame data after headers
            frame_start = headers_end + 4
            frame_data = buffer[frame_start:]
            
            # Find the end of the frame (next boundary)
            frame_end = frame_data.find(boundary)
            if frame_end == -1:
                continue
                
            # Extract the complete frame data
            jpeg_data = frame_data[:frame_end]
            
            # Convert to numpy array and decode
            frame_array = np.frombuffer(jpeg_data, dtype=np.uint8)
            frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
            
            if frame is not None:
                session.close()
                return frame
        
        session.close()
        return None
        
    except Exception as e:
        print(f"Error capturing frame from multipart stream: {e}")
        return None

def display_frame_with_result(frame: np.ndarray, object_name: str, detected: bool, window_name: str = "VLM Vision") -> bool:
    """
    Display the captured frame with detection result overlay.
    
    Args:
        frame: The captured frame to display
        object_name: The name of the object being detected
        detected: Whether the object was detected
        window_name: Name of the display window
        
    Returns:
        bool: True if should continue, False if user pressed 'q' to quit
    """
    if frame is None:
        return True
        
    # Create a copy of the frame to draw on
    display_frame = frame.copy()
    
    # Add text overlay with detection result
    status_text = f"Looking for: {object_name}"
    result_text = f"Detected: {'YES' if detected else 'NO'}"
    
    # Set colors based on detection result
    status_color = (255, 255, 255)  # White
    result_color = (0, 255, 0) if detected else (0, 0, 255)  # Green if detected, Red if not
    
    # Add text to frame
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    
    # Status text (top)
    cv2.putText(display_frame, status_text, (10, 30), font, font_scale, status_color, thickness)
    
    # Result text (below status)
    cv2.putText(display_frame, result_text, (10, 60), font, font_scale, result_color, thickness)
    
    # Add timestamp
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    cv2.putText(display_frame, f"Time: {timestamp}", (10, display_frame.shape[0] - 10), 
                font, 0.5, status_color, 1)
    
    # Display the frame
    cv2.imshow(window_name, display_frame)
    
    # Check for 'q' key press to quit (wait 1ms)
    key = cv2.waitKey(1) & 0xFF
    return key != ord('q')

# --- Agentic Logic ---
if __name__ == "__main__":
    print("=== Interactive VLM Object Detection ===")
    print("This tool will search for objects in your ROS camera feed using AI vision.")
    print("Instructions:")
    print("- Enter the object you want to find when prompted")
    print("- Press 'q' in the video window to quit")
    print("- Press Ctrl+C in console for emergency stop")
    print("- Type 'quit' or 'exit' when asked for an object to stop")
    print("=" * 50)

    try:
        while True:
            # Ask user what object to look for
            print("\n" + "=" * 30)
            object_to_find = input("What object would you like to detect? (or 'quit'/'exit' to stop): ").strip()
            
            # Check if user wants to quit
            if object_to_find.lower() in ['quit', 'exit', 'q', '']:
                print("Exiting...")
                break
                
            if not object_to_find:
                print("Please enter a valid object name.")
                continue

            print(f"\n🔍 Scanning for '{object_to_find}'...")
            print("📷 Capturing frame from ROS camera...")
            
            # Perform detection
            is_detected, frame = detect_object_in_stream(object_to_find, ROS_VIDEO_URL, show_visualization=True)

            # Show results in console
            print("\n" + "=" * 40)
            if is_detected:
                print(f"✅ SUCCESS: '{object_to_find}' was detected!")
            else:
                print(f"❌ NOT FOUND: '{object_to_find}' was not detected.")
            print("=" * 40)

            # Display the frame with detection result
            if frame is not None:
                print("📺 Displaying result in video window...")
                print("   (Close the window or press 'q' to continue to next search)")
                
                # Show the frame and wait for user to close window or press 'q'
                display_frame_with_result(frame, object_to_find, is_detected)
                cv2.waitKey(0)  # Wait indefinitely until any key is pressed
                cv2.destroyAllWindows()  # Close the window
            else:
                print("⚠️  Failed to capture frame from camera.")
                
            print("\nReady for next search...")
                    
    except KeyboardInterrupt:
        print("\n\nReceived Ctrl+C - shutting down...")
    except EOFError:
        print("\n\nInput stream closed - shutting down...")
    finally:
        # Clean up OpenCV windows
        cv2.destroyAllWindows()
        print("🛑 VLM agent stopped. Goodbye!")