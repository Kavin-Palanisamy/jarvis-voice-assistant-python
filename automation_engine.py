"""
automation_engine.py
Handles keyboard/mouse automation and OCR using PyAutoGUI and pytesseract.
"""

import pyautogui
import pytesseract
from PIL import Image
import time
from logger import get_logger

logger = get_logger()

# Optional: set pytesseract path if not in env
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class AutomationEngine:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        logger.info("Automation engine loaded.")

    def type_text(self, text: str, interval: float = 0.05):
        """Types out text simulating human speed."""
        logger.info(f"Typing text: '{text}'")
        pyautogui.write(text, interval=interval)

    def hotkey(self, *keys):
        """Executes a hotkey combination securely."""
        logger.info(f"Executing hotkeys: {keys}")
        pyautogui.hotkey(*keys)

    def click_coordinates(self, x: int, y: int):
        """Clicks specific screen coordinates."""
        logger.info(f"Clicking at ({x}, {y})")
        pyautogui.click(x, y)

    def screenshot_and_ocr(self) -> str:
        """Takes a screenshot and attempts OCR to find text."""
        logger.info("Capturing screenshot for OCR...")
        try:
            img = pyautogui.screenshot()
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
            
    def scroll(self, amount: int):
        """Scrolls the screen logically. Negative means down."""
        logger.info(f"Scrolling: {amount} units")
        pyautogui.scroll(amount)

if __name__ == "__main__":
    auto = AutomationEngine()
    print("Automation engine is responsive.")
