import os
import asyncio
from typing import Optional, Callable, Awaitable
from dotenv import load_dotenv
from environment_settings import ENVIRONMENT_SETTINGS

class MissionLogger:
    """
    Mission logger that adapts to CLI or WebSocket environments.
    """
    
    def __init__(self):
        self.websocket_send_callback: Optional[Callable[[str], Awaitable[None]]] = None
        self.telemetry_callback: Optional[Callable[[str], Awaitable[None]]] = None
    
    def set_websocket_callback(self, callback: Callable[[str], Awaitable[None]]):
        """Set the WebSocket send callback for React mode."""
        self.websocket_send_callback = callback
        # Use the same callback for telemetry for now
        self.telemetry_callback = callback
    
    def set_telemetry_callback(self, callback: Callable[[str], Awaitable[None]]):
        """Set the telemetry send callback for React mode."""
        self.telemetry_callback = callback
    
    async def _async_log(self, message: str, log_type: str = "INFO"):
        """
        Internal async log method.
        
        Args:
            message (str): The message to log
            log_type (str): Type of log message (INFO, ERROR, WARNING, etc.)
        """
        # Format the message with log type
        formatted_message = f"[{log_type}] {message}"
        
        # Always log to CLI/console
        print(formatted_message)
        
        # If in React mode and WebSocket callback is available, also send to WebSocket
        if ENVIRONMENT_SETTINGS.use_react and self.websocket_send_callback:
            try:
                await self.websocket_send_callback(formatted_message)
            except Exception as e:
                print(f"[ERROR] Failed to send log to WebSocket: {e}")
    
    def log(self, message: str, log_type: str = "INFO"):
        """
        Synchronous log method that uses fire-and-forget for WebSocket sending.
        
        Args:
            message (str): The message to log
            log_type (str): Type of log message (INFO, ERROR, WARNING, etc.)
        """
        # Format the message with log type
        formatted_message = f"[{log_type}] {message}"
        
        # Always log to CLI/console immediately
        print(formatted_message)
        
        # If in React mode and WebSocket callback is available, fire-and-forget the WebSocket send
        if ENVIRONMENT_SETTINGS.use_react and self.websocket_send_callback:
            try:
                # Try to get the current event loop, if any
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Create a task in the current loop (fire and forget)
                    asyncio.create_task(self._send_to_websocket(formatted_message))
                else:
                    # No running loop, just skip WebSocket (shouldn't happen in normal usage)
                    raise RuntimeError("No running event loop")
            except RuntimeError:
                # No event loop, just skip WebSocket (CLI mode or no async context)
                raise RuntimeError("No running event loop")
    
    async def _send_to_websocket(self, formatted_message: str):
        """Helper method to send message to WebSocket with error handling."""
        try:
            await self.websocket_send_callback(formatted_message)
        except Exception as e:
            print(f"[ERROR] Failed to send log to WebSocket: {e}")

# Global logger instance
_logger = MissionLogger()

def mission_log(message: str, log_type: str = "INFO"):
    """
    Log a mission-related message (synchronous).
    
    Args:
        message (str): The message to log
        log_type (str): Type of log message (INFO, ERROR, WARNING, etc.)
    """
    _logger.log(message, log_type)

def set_websocket_callback(callback: Callable[[str], Awaitable[None]]):
    """
    Set the WebSocket send callback for the global logger.
    
    Args:
        callback: Async function that takes a string message and sends it via WebSocket
    """
    _logger.set_websocket_callback(callback)

def set_telemetry_callback(callback: Callable[[str], Awaitable[None]]):
    """
    Set the telemetry send callback for the global logger.
    
    Args:
        callback: Async function that takes a string telemetry data and sends it via WebSocket
    """
    _logger.set_telemetry_callback(callback)

async def send_telemetry(telemetry_json: str):
    """
    Send telemetry data via WebSocket (async).
    
    Args:
        telemetry_json (str): JSON string containing telemetry data
    """
    if ENVIRONMENT_SETTINGS.use_react and _logger.telemetry_callback:
        try:
            await _logger.telemetry_callback(telemetry_json)
        except Exception as e:
            print(f"[ERROR] Failed to send telemetry to WebSocket: {e}")

def is_react_mode() -> bool:
    """
    Check if the logger is running in React/WebSocket mode.
    
    Returns:
        bool: True if in React mode, False if in CLI mode
    """
    return ENVIRONMENT_SETTINGS.use_react
