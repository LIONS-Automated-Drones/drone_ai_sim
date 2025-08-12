import asyncio
from mavsdk import System

class DroneService:
    """A wrapper class for MAVSDK to simplify drone control."""
    def __init__(self):
        self.drone = System()
        self.is_connected = False

    async def connect(self):
        """
        Connects to the simulated drone.
        """
        if self.is_connected:
            return True
            
        print("--- Connecting to drone...")
        await self.drone.connect(system_address="udp://:14540")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("--- Drone connected!")
                self.is_connected = True
                return True
        return False

    async def arm(self):
        """
        Arms the drone.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot arm.")
            return False
        print("--- Arming drone...")
        await self.drone.action.arm()
        return True

    async def takeoff(self):
        """
        Takes off to a default altitude.
        """
        if not self.is_connected:
            print("--- Drone not connected. Cannot take off.")
            return False
        print("--- Taking off...")
        await self.drone.action.takeoff()
        await asyncio.sleep(5) # Wait for takeoff to complete
        return True
