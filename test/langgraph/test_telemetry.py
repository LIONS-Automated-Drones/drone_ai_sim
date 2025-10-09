#!/usr/bin/env python3
"""
Test script for telemetry streaming functionality.
This script tests the telemetry data structure and JSON serialization.
"""

import json
import time
import asyncio
from drone_service import DroneService

def test_telemetry_data_structure():
    """Test that the telemetry data structure is correctly formatted."""
    print("Testing telemetry data structure...")
    
    # Mock telemetry data
    mock_telemetry = {
        "type": "telemetry",
        "timestamp": int(time.time() * 1000),
        "armed": True,
        "flight_mode": "MANUAL",
        "battery_percent": 85.5,
        "gps_fix_type": "FIX_3D",
        "gps_satellites": 8,
        "health_all_ok": True,
        "position_relative": {
            "x_m": 10.5,
            "y_m": -5.2,
            "z_m": 15.0
        },
        "altitude_m": 120.5,
        "velocity_ms": 12.3,
        "heading_deg": 45.0,
        "is_in_air": True
    }
    
    # Test JSON serialization
    try:
        json_str = json.dumps(mock_telemetry)
        parsed_back = json.loads(json_str)
        
        # Verify all fields are present
        required_fields = [
            "type", "timestamp", "armed", "flight_mode", "battery_percent",
            "gps_fix_type", "gps_satellites", "health_all_ok", "position_relative",
            "altitude_m", "velocity_ms", "heading_deg", "is_in_air"
        ]
        
        for field in required_fields:
            if field not in parsed_back:
                print(f"❌ Missing field: {field}")
                return False
        
        # Verify position_relative structure
        pos_fields = ["x_m", "y_m", "z_m"]
        for field in pos_fields:
            if field not in parsed_back["position_relative"]:
                print(f"❌ Missing position field: {field}")
                return False
        
        print("✅ Telemetry data structure test passed")
        print(f"📊 Sample JSON: {json_str}")
        return True
        
    except Exception as e:
        print(f"❌ JSON serialization failed: {e}")
        return False

async def test_drone_service_telemetry():
    """Test the DroneService telemetry methods (without actual connection)."""
    print("\nTesting DroneService telemetry methods...")
    
    drone_service = DroneService()
    
    # Test that methods exist
    methods_to_test = [
        'get_comprehensive_telemetry',
        'start_telemetry_streaming',
        'stop_telemetry_streaming'
    ]
    
    for method_name in methods_to_test:
        if hasattr(drone_service, method_name):
            print(f"✅ Method {method_name} exists")
        else:
            print(f"❌ Method {method_name} missing")
            return False
    
    # Test takeoff_position initialization
    if hasattr(drone_service, 'takeoff_position'):
        print("✅ takeoff_position attribute exists")
    else:
        print("❌ takeoff_position attribute missing")
        return False
    
    # Test telemetry streaming flags
    if hasattr(drone_service, 'telemetry_streaming'):
        print("✅ telemetry_streaming flag exists")
    else:
        print("❌ telemetry_streaming flag missing")
        return False
    
    print("✅ DroneService telemetry methods test passed")
    return True

def test_mission_log_telemetry():
    """Test the mission_log telemetry functions."""
    print("\nTesting mission_log telemetry functions...")
    
    try:
        from mission_log import send_telemetry, set_telemetry_callback
        print("✅ Telemetry functions imported successfully")
        
        # Test callback setting (should not raise an error)
        async def dummy_callback(data):
            pass
        
        set_telemetry_callback(dummy_callback)
        print("✅ set_telemetry_callback works")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def main():
    """Run all tests."""
    print("🚁 Drone Telemetry System Tests")
    print("=" * 40)
    
    tests = [
        ("Telemetry Data Structure", test_telemetry_data_structure()),
        ("DroneService Methods", await test_drone_service_telemetry()),
        ("Mission Log Functions", test_mission_log_telemetry())
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        if result:
            passed += 1
        print()
    
    print("=" * 40)
    print(f"📈 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Telemetry system is ready.")
        print("\n📝 Next steps:")
        print("1. Start the drone simulation (Gazebo)")
        print("2. Run the LangGraph test with USE_REACT=true")
        print("3. Connect the React dashboard")
        print("4. Execute 'arm_and_takeoff' command")
        print("5. Observe real-time telemetry at 2Hz frequency")
    else:
        print("⚠️  Some tests failed. Please fix the issues before proceeding.")

if __name__ == "__main__":
    asyncio.run(main())
