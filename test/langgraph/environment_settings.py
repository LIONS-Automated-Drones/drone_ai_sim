import os
import json
from dotenv import load_dotenv

class EnvironmentSettings:
    def __init__(self):
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://192.168.1.117:11434")
        self.use_react = os.getenv("USE_REACT", "false").lower() == "true"
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "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")
        self.openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash-lite")
        self.is_gazebo = os.getenv("IS_GAZEBO", "true").lower() == "true"
        self.serial_port = os.getenv("SERIAL_PORT", "/dev/tty.usbserial-0001")
        self.baud_rate = os.getenv("BAUD_RATE", "57600")
        self.udp_address = os.getenv("UDP_ADDRESS", "udp://:14540")
        self.server_address = os.getenv("SERVER_ADDRESS", "0.0.0.0")
        self.server_port = os.getenv("SERVER_PORT", "8000")
        # print ALL settings
        json_settings = self.__dict__
        print(json.dumps(json_settings, indent=4))
      
load_dotenv()
ENVIRONMENT_SETTINGS = EnvironmentSettings()