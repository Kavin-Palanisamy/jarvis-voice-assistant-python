"""
test_runner.py
Automated command simulation to validate pipeline connectivity.
"""

import asyncio
import time
from main import JarvisApp
from logger import get_logger

logger = get_logger()

TEST_CASES = [
    "what is my name",
    "set volume to 50",
    "open notepad",
    "what is the weather in London"
]

async def run_tests():
    print("\n┌─────────────────────────────────────────────────┐")
    print("│           JARVIS AUTO TEST REPORT               │")
    print("├──────────────────────────┬───────────┬──────────┤")
    print("│ Command                  │ Result    │ Time     │")
    print("├──────────────────────────┼───────────┼──────────┤")
    
    # Init without blocking tests
    app = JarvisApp()
    
    passed = 0
    failed = 0
    
    for cmd in TEST_CASES:
        start_time = time.time()
        try:
            # Bypass manual input
            await app.process_user_input(cmd)
            duration = time.time() - start_time
            print(f"│ {cmd[:24]:<24} │ ✓ SUCCESS │ {duration:.1f}s     │")
            passed += 1
        except Exception as e:
            duration = time.time() - start_time
            print(f"│ {cmd[:24]:<24} │ ✗ FAILED  │ {duration:.1f}s     │")
            logger.error(f"Test '{cmd}' failed: {e}")
            failed += 1
            
    print("└──────────────────────────┴───────────┴──────────┘")
    print(f"Tests: {len(TEST_CASES)} | Passed: {passed} | Failed: {failed}")

if __name__ == "__main__":
    asyncio.run(run_tests())
