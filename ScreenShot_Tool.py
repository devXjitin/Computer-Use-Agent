import mss
from datetime import datetime
from autourgos.core import Tool


def capture_screenshot(save_path: str = "screenshot.png", monitor: int = 1) -> str:
    """
    This tool helps to capture screenshot.

    Args:
        save_path (str): Path where the screenshot will be saved.
                         Default is "screenshot.png".
        monitor (int): Monitor index to capture.
                       1 = primary monitor. Default is 1.

    Returns:
        str: The file path of the saved screenshot.
    """
    try:
        with mss.mss() as sct:
            monitor_info = sct.monitors[monitor]
            screenshot = sct.grab(monitor_info)

            mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)

        return save_path

    except Exception as e:
        raise RuntimeError(f"Screenshot capture failed: {e}")

capture_screenshot()