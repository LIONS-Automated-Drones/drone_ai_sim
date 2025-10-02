#!/usr/bin/env python3
"""
Test script for RTSP vision integration.
This script tests the RTSP frame capture functionality.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.append(os.path.dirname(__file__))

from agents.vision import capture_rtsp_frame, frame_to_base64, AnalyzeImageTool

async def test_rtsp_capture():
    """Test RTSP frame capture functionality."""
    print("=== Testing RTSP Vision Integration ===")
    
    # Load environment variables
    load_dotenv()
    
    # Get RTSP URL from environment or use default
    rtsp_url = os.getenv("RTSP_URL", "rtsp://192.168.64.1:8554/live")
    print(f"Testing RTSP stream: {rtsp_url}")
    
    # Test frame capture
    print("\n1. Testing frame capture...")
    success, frame = capture_rtsp_frame(rtsp_url)
    
    if not success:
        print("Frame capture failed")
        print("Make sure the RTSP stream is running and accessible")
        return False
    
    print("Frame capture successful")
    print(f"   Frame shape: {frame.shape}")
    print(f"   Frame dtype: {frame.dtype}")
    
    # Test base64 conversion
    print("\n2. Testing base64 conversion...")
    image_data = frame_to_base64(frame)
    
    if not image_data:
        print("Base64 conversion failed")
        return False
    
    print("Base64 conversion successful")
    print(f"   Base64 length: {len(image_data)} characters")
    
    # Test AnalyzeImageTool
    print("\n3. Testing AnalyzeImageTool...")
    try:
        tool = AnalyzeImageTool()
        result = await tool._arun("dummy_path", "what do you see in the image")
        print("AnalyzeImageTool executed successfully")
        print(f"   Result preview: {result[:100]}...")
        return True
    except Exception as e:
        print(f"AnalyzeImageTool failed: {e}")
        return False

async def main():
    """Main test function."""
    print("RTSP Vision Integration Test")
    print("=" * 40)
    
    success = await test_rtsp_capture()
    
    if success:
        print("\nAll tests passed! RTSP vision integration is working.")
        print("\nYou can now use the multi-agent system with live video streams.")
        print("Example commands:")
        print("  - 'if you see a car then land'")
        print("  - 'if you see a human then takeoff'")
    else:
        print("\nTests failed. Please check:")
        print("  - RTSP stream is running")
        print("  - Network connectivity")
        print("  - Environment variables (RTSP_URL, OLLAMA_BASE_URL)")

if __name__ == "__main__":
    asyncio.run(main())
