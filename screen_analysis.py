import pyautogui
import os
from PIL import Image
from ai_brain import get_ai_response

# Auto-configure Tesseract path for Windows
try:
    import pytesseract
    _tess_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Users\Kavin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
    ]
    for _p in _tess_paths:
        if os.path.exists(_p):
            pytesseract.pytesseract.tesseract_cmd = _p
            break
    TESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    TESSERACT_AVAILABLE = False


def _take_screen_snapshot():
    """Helper: takes a screenshot and saves it temporarily."""
    screenshot = pyautogui.screenshot()
    folder = "temp"
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = os.path.join(folder, "current_screen.png")
    screenshot.save(path)
    return path


def read_screen():
    """Captures the screen, performs OCR, and returns the raw text."""
    if not TESSERACT_AVAILABLE:
        return "Sir, Tesseract OCR is not installed. Please install it from https://github.com/UB-Mannheim/tesseract/wiki"
    path = _take_screen_snapshot()
    try:
        text = pytesseract.image_to_string(Image.open(path))
        return text.strip() if text.strip() else "The screen appears blank or non-textual, Sir."
    except Exception as e:
        return f"Error reading screen: {str(e)}"


def extract_text_from_screen():
    """Reads the screen via OCR and returns the raw extracted text."""
    text = read_screen()
    if not text or len(text) < 10:
        return "I could not extract meaningful text from your screen, Sir."
    # Trim for speech
    snippet = text[:500]
    return f"Here is the text I extracted from your screen, Sir:\n{snippet}"


def summarize_screen():
    """Reads the screen and uses AI to summarize what is being displayed."""
    text = read_screen()
    if not text or len(text) < 10:
        return "The screen appears to be blank or non-textual, Sir."
    
    prompt = (
        "I am looking at the user's screen. Here is the text I extracted via OCR. "
        "Please summarize what the user is currently looking at or working on:\n\n"
        + text[:2000]
    )
    summary = get_ai_response(prompt)
    return f"Based on my optical analysis, you are looking at:\n{summary}"


def explain_document():
    """Reads the screen OCR text and uses AI to explain the document in detail."""
    text = read_screen()
    if not text or len(text) < 20:
        return "There is no readable document on the screen, Sir."
    
    prompt = (
        "The user has a document open on their screen. The OCR-extracted text is below. "
        "Please explain what this document is about, its key points, and any important information:\n\n"
        + text[:3000]
    )
    explanation = get_ai_response(prompt)
    return f"Document analysis complete, Sir:\n{explanation}"


if __name__ == "__main__":
    pass
