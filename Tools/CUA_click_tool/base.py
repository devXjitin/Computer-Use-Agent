"""
Computer Use Agent - Click Tool
Implements mouse clicking functionality using PyAutoGUI and LangChain
"""

import pyautogui
from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class ClickInput(BaseModel):
    """Input schema for Click tool"""
    x: int = Field(description="X coordinate on screen where to click")
    y: int = Field(description="Y coordinate on screen where to click")
    button: str = Field(
        default="left",
        description="Mouse button to click: 'left', 'right', or 'middle'"
    )
    clicks: int = Field(
        default=1,
        description="Number of clicks (1 for single click, 2 for double click)"
    )
    interval: float = Field(
        default=0.0,
        description="Interval in seconds between clicks (for multiple clicks)"
    )


class ClickTool(BaseTool):
    """Tool for performing mouse clicks at specified coordinates"""
    
    name: str = "click"
    description: str = """
    Click at a specific location on the screen.
    Use this to interact with UI elements like buttons, links, text fields.
    Requires X and Y coordinates of the target element.
    Supports left, right, and middle mouse buttons.
    Can perform single or double clicks.
    
    Examples:
    - Click button at coordinates (500, 300)
    - Right-click context menu at (800, 400)
    - Double-click file at (200, 150)
    """
    args_schema: Type[BaseModel] = ClickInput
    
    def _run(
        self,
        x: int,
        y: int,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.0
    ) -> str:
        """Execute the click action"""
        try:
            # Validate button type
            if button not in ["left", "right", "middle"]:
                return f"Error: Invalid button '{button}'. Use 'left', 'right', or 'middle'."
            
            # Get screen size for validation
            screen_width, screen_height = pyautogui.size()
            
            # Validate coordinates
            if not (0 <= x <= screen_width):
                return f"Error: X coordinate {x} is out of screen bounds (0-{screen_width})"
            
            if not (0 <= y <= screen_height):
                return f"Error: Y coordinate {y} is out of screen bounds (0-{screen_height})"
            
            # Perform the click
            pyautogui.click(
                x=x,
                y=y,
                clicks=clicks,
                interval=interval,
                button=button
            )
            
            click_type = "double-click" if clicks == 2 else "click"
            return f"Successfully performed {button} {click_type} at coordinates ({x}, {y})"
            
        except Exception as e:
            return f"Error performing click: {str(e)}"
    
    async def _arun(
        self,
        x: int,
        y: int,
        button: str = "left",
        clicks: int = 1,
        interval: float = 0.0
    ) -> str:
        """Async version of the click action"""
        return self._run(x, y, button, clicks, interval)
