# Multi-Agent Drone System with VLM Context

A proof-of-concept multi-agent drone system that combines a **Pilot Agent** and **Vision Agent** to enable autonomous drone operations based on visual context. The system uses a Vision Language Model (VLM) to analyze images and provide context for pilot decision-making.

## Quick Start

### Prerequisites

1. **Python Environment**

   ```bash
   pip install -r requirements.txt
   ```

2. **Ollama Models**
   Ensure you have these models running on your Ollama server:

   - `llama3.2-vision:11b` (for image analysis)
   - `llama3.1:8b` (for vision agent tool calling)

3. **Gazebo Simulation**
   - Start Gazebo simulation environment
   - Ensure drone simulation is running and accessible

## Configuration

### Environment Variables

Create a `.env` file in the `app/` directory:

```
VIRTUAL=true (make this false if you are connecting to the real drone via serial)

OLLAMA_BASE_URL=http://<ollama_machine_ip>:11434

OLLAMA_MODEL=llama3.1:8b

OLLAMA_VLM_MODEL=llama3.2-vision:11b
```

- **NOTE** you need to pull these models from ollama beforehand

### Running the System

```bash
cd app
python main.py
```

### Example Commands

- **Takeoff**: `pilot takeoff`
- **Vision Analysis**: `what do you see in the image`
- **Conditional Landing**: `if see car in image pilot land`

## How It Works

1. **User Input**: Natural language commands are processed by the router
2. **Agent Selection**: Router determines whether to use pilot or vision agent
3. **Vision Analysis**:
   - Vision agent calls `analyze_image` tool
   - Tool reads `image.jpeg` from app directory
   - Makes VLM request to Ollama with base64-encoded image
   - Returns detailed visual analysis
4. **Action Triggering**: If specific objects detected (car, bicycle), pilot agent executes landing
5. **Drone Control**: Pilot agent uses shared drone service for seamless operations

## Architecture

### Agents

- **Pilot Agent**: Controls drone operations (takeoff, landing, movement) using MAVSDK
- **Vision Agent**: Analyzes images using Ollama VLM and triggers pilot actions based on visual content

### Key Features

- **Real VLM Integration**: Uses Ollama's `llama3.2-vision` for actual image analysis
- **Shared Drone Service**: Both agents use the same connected drone instance
- **Context-Driven Actions**: Vision analysis triggers specific pilot behaviors
- **Single Request Optimization**: Each vision query makes only one VLM request

### Image Analysis

- Place your test image as `image.jpeg` in the `app/` directory
- The system will analyze this image when vision commands are issued

## Current Capabilities

- Real-time image analysis with VLM
- Context-driven drone landing
- Shared drone connection management
- Single VLM request per analysis
- Clean response formatting

## Example Output

```
--- Multi-Agent Drone System Initialized ---
Enter your mission: pilot takeoff
--- PILOT: Connecting and taking off... ---
--- Drone connected!
--- Taking off...
--- Takeoff altitude: 2.5m
--- Drone has reached takeoff altitude.
Tool Result: Takeoff successful. Drone is airborne.

Enter your mission: if see car in image pilot land
--- VLM: Analyzing image.jpeg for 'if see car in image pilot land'... (Request #1) ---
--- VLM: Making request to http://localhost:11434/api/chat with model llama3.2-vision:11b... ---
--- VLM: Raw response: The image depicts a black car, specifically a Hyundai Tucson...
--- VLM: Detected car, calling pilot to land... ---
--- Landing...
--- Drone has landed.
Tool Result: The image depicts a black car, specifically a Hyundai Tucson...
Drone has been commanded to land.
```

## Troubleshooting

- **Connection Issues**: Ensure Gazebo simulation is running
- **VLM Errors**: Verify Ollama models are installed and running
- **Image Not Found**: Place `image.jpeg` in the `app/` directory
- **Timeout Issues**: Check Ollama server connectivity and model availability

This proof-of-concept demonstrates how VLM context can drive autonomous drone behavior, providing a foundation for more complex vision-guided navigation systems.
