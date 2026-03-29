import pyautogui
import time

# Screen dimensions for corner calculations
_W, _H = pyautogui.size()


def move_mouse_to(x, y):
    """Moves the mouse to a specific (x, y) coordinate."""
    pyautogui.moveTo(x, y, duration=0.5)
    return f"Moved mouse to {x}, {y}."


def move_to_corner(corner: str):
    """
    Moves the mouse to a named corner of the screen.
    corner: 'top-right', 'top-left', 'bottom-right', 'bottom-left', 'center'
    """
    corner = corner.lower().replace(" ", "-")
    positions = {
        "top-right":    (_W - 10, 10),
        "top-left":     (10, 10),
        "bottom-right": (_W - 10, _H - 10),
        "bottom-left":  (10, _H - 10),
        "center":       (_W // 2, _H // 2),
        "top":          (_W // 2, 10),
        "bottom":       (_W // 2, _H - 10),
    }
    pos = positions.get(corner, (_W - 10, 10))  # default: top-right
    pyautogui.moveTo(pos[0], pos[1], duration=0.6)
    return f"Mouse moved to the {corner}, Sir."


def click_at(x=None, y=None, clicks=1):
    """Clicks at the current position or specified (x, y) coordinates."""
    if x is not None and y is not None:
        pyautogui.click(x, y, clicks=clicks, interval=0.1)
    else:
        pyautogui.click(clicks=clicks, interval=0.1)
    return "Clicking now, Sir."


def right_click_at(x=None, y=None):
    """Right-clicks at the current position or specified coordinates."""
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
    else:
        pyautogui.rightClick()
    return "Right-click executed, Sir."


def double_click_at(x=None, y=None):
    """Double-clicks at a position."""
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
    else:
        pyautogui.doubleClick()
    return "Double-click executed, Sir."


def type_text(text):
    """Types the given text with a slight delay between characters."""
    pyautogui.write(text, interval=0.05)
    return f"Typed: {text}"


def press_key(key):
    """Presses a specific key (e.g., 'enter', 'esc', 'space')."""
    pyautogui.press(key)
    return f"Pressed the {key} key, Sir."


def hotkey(*keys):
    """Presses a keyboard shortcut (e.g., hotkey('ctrl', 'c'))."""
    pyautogui.hotkey(*keys)
    return f"Shortcut {'+'.join(keys)} executed."


def scroll(amount):
    """Scrolls the screen up (positive) or down (negative)."""
    pyautogui.scroll(amount)
    direction = "up" if amount > 0 else "down"
    return f"Scrolling {direction}, Sir."


def get_mouse_position():
    """Returns the current mouse position."""
    x, y = pyautogui.position()
    return f"The cursor is at {x}, {y}."


def drag_to(x, y):
    """Drags the mouse to a specific (x, y) coordinate."""
    pyautogui.dragTo(x, y, duration=1)
    return f"Dragged mouse to {x}, {y}."
