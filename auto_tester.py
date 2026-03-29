import sys
from unittest.mock import patch, MagicMock

# Create mock objects for optional dependencies so tests don't fail if they aren't installed on the tester's machine
sys.modules['face_recognition'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['pytesseract'] = MagicMock()
sys.modules['pyautogui'] = MagicMock(
    screenshot=MagicMock(return_value=MagicMock()),
    size=MagicMock(return_value=(1920, 1080)),
    position=MagicMock(return_value=(960, 540))
)

import automation_engine as ae
import screen_control as sc
import browsing_engine as be
from command_parser import split_into_tasks
from task_engine import execute_task, COMMANDS_MAP

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'

test_cases = [
    "open chrome",
    "open youtube and search music",
    "take screenshot",
    "increase volume",
    "read screen",
    "remember my name is Jarvis",
    "shutdown", # Verify destructive commands are caught safely
    "open google and search python then take screenshot",
    "open youtube and play ACDC",
    "turn off wifi",
    "turn on light"
]

def run_automated_tests():
    print("Starting Automated Command Tester...")
    print("=" * 50)
    
    # Append all static triggers from COMMANDS_MAP to get ~100% test coverage
    for trigger in COMMANDS_MAP.keys():
        if trigger not in test_cases:
            test_cases.append(trigger)
            
    passed = 0
    failed = 0
    
    # Patch all major side-effect sources across the codebase
    with patch('webbrowser.open') as p_web, \
         patch('os.system') as p_os, \
         patch('subprocess.run') as p_sub, \
         patch('os.startfile') as p_os_start, \
         patch('sys.exit') as p_exit, \
         patch('task_engine.get_ai_response', return_value="Mock AI Response"), \
         patch('pyperclip.paste', return_value="http://mocked-url.com"):
         
         for case in test_cases:
             print(f"Testing Command: {Color.YELLOW}'{case}'{Color.END}")
             try:
                 # 1. Parse into individual tasks
                 tasks = split_into_tasks(case)
                 for i, task in enumerate(tasks):
                     # 2. Execute directly
                     res = execute_task(task)
                     res_text = str(res)[:100] + "..." if res and len(str(res)) > 100 else res
                     print(f"  -> Task {i+1}: '{task}' | Response: {res_text}")
                 print(f"[{Color.GREEN}SUCCESS{Color.END}]\n")
                 passed += 1
             except Exception as e:
                 print(f"[{Color.RED}FAILED{Color.END}] Error: {e}\n")
                 failed += 1

    print("=" * 50)
    print("TEST REPORT")
    print(f"  Total Tested: {passed + failed}")
    print(f"  {Color.GREEN}Passed{Color.END}:     {passed}")
    print(f"  {Color.RED}Failed{Color.END}:     {failed}")
    print("=" * 50)

if __name__ == '__main__':
    run_automated_tests()
