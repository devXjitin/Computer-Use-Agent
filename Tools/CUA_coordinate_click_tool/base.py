"""
Computer Use Agent - Coordinates Click Tool
Tool clicking at screen coordinates using PyAutoGUI and LangChain
"""

import pyautogui
from langchain.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field


class CoordinatesClickInput(BaseModel):
    """Input schema for Coordinates Click tool"""
    x: int = Field(description="X coordinate on screen where to click")
    y: int = Field(description="Y coordinate on screen where to click")
    button: str = Field(
        default="left",
        description="Mouse button: 'left', 'right', or 'middle'"
    )
    clicks: int = Field(
        default=1,
        description="Number of clicks (1=single, 2=double)"
    )
    interval: float = Field(
        default=0.0,
        description="Interval between clicks in seconds"
    )
    duration: float = Field(
        default=0.0,
        description="Duration to move mouse to coordinates (0=instant)"
    )


class CoordinatesClickTool(BaseTool):
    """Tool for clicking at specific screen coordinates"""
    
    name: str = "coordinates_click"
    description: str = """
    Click at exact screen coordinates with advanced options.
    Features:
    - Precise coordinate targeting
    - Left/right/middle button support
    - Single or double-click
    - Optional smooth mouse movement
    - Screen bounds validation
    """
    args_schema: Type[BaseModel] = CoordinatesClickInput
    
    # Cache screen size for optimization
    _screen_size: Optional[tuple] = None
    
    def _get_screen_size(self) -> tuple:
        """Get screen size with caching for performance"""
        if self._screen_size is None:
            self._screen_size = pyautogui.size()
        return self._screen_size
    
    def _validate_inputs(self, x: int, y: int, button: str) -> Optional[str]:
        """Validate input parameters"""
        # Validate button type
        if button not in ["left", "right", "middle"]:
            return f"Invalid button '{button}'. Must be 'left', 'right', or 'middle'."
        
        # Validate coordinates
        screen_width, screen_height = self._get_screen_size()
        if not (0 <= x <= screen_width):
            return f"X coordinate {x} out of bounds (0-{screen_width})"
        if not (0 <= y <= screen_height):
            return f"Y coordinate {y} out of bounds (0-{screen_height})"
        
        return None
    
    def _run(
        self,
        x: int,
        y: int,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.0,
        duration: float = 0.0
    ) -> str:
        """Execute the click action"""
        try:
            # Validate inputs
            error = self._validate_inputs(x, y, button)
            if error:
                return f"Error: {error}"
            
            # Move to position if duration specified
            if duration > 0:
                pyautogui.moveTo(x, y, duration=duration)
            
            # Perform the click
            pyautogui.click(
                x=x,
                y=y,
                clicks=clicks,
                interval=interval,
                button=button
            )
            
            # Format response
            click_type = "double-click" if clicks == 2 else "click"
            movement = f" (moved in {duration}s)" if duration > 0 else ""
            return f"✓ {button.capitalize()} {click_type} at ({x}, {y}){movement}"
            
        except pyautogui.FailSafeException:
            return "Error: PyAutoGUI fail-safe triggered (mouse moved to corner)"
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _arun(
        self,
        x: int,
        y: int,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.0,
        duration: float = 0.0
    ) -> str:
        """Async version of the click action"""
        return self._run(x, y, button, clicks, interval, duration)