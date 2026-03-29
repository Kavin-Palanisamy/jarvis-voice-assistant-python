from memory_engine import memory
from command_parser import split_into_tasks, clean_task
from task_engine import execute_task
import os

def test_memory():
    print("--- Testing Memory Engine ---")
    memory.clear_history()
    resp = memory.store_preference("favorite music", "lo-fi")
    print(resp)
    val = memory.get_preference("favorite music")
    print(f"Retrieved: {val}")
    assert val == "lo-fi"
    print("Memory Test Passed\n")

def test_parser():
    print("--- Testing Command Parser ---")
    cmd = "Jarvis please open youtube and then search iron man also take a screenshot"
    tasks = split_into_tasks(cmd)
    cleaned = [clean_task(t) for t in tasks]
    print(f"Tasks: {cleaned}")
    assert len(cleaned) == 3
    assert "open youtube" in cleaned[0]
    assert "search iron man" in cleaned[1]
    assert "take a screenshot" in cleaned[2]
    print("Parser Test Passed\n")

def test_task_logic():
    print("--- Testing Task Engine Logic ---")
    # Mocking execution by checking routing
    print("Testing routing for 'remember'...")
    resp = execute_task("remember my favorite car is Audi R8")
    print(resp)
    assert "Audi R8" in resp
    
    print("Testing routing for 'what is'...")
    resp = execute_task("what is my favorite car")
    print(resp)
    assert "Audi R8" in resp
    
    print("Task Engine Logic Test Passed\n")

if __name__ == "__main__":
    try:
        test_memory()
        test_parser()
        test_task_logic()
        print("ALL TESTS PASSED SUCCESSFULLY!")
    except Exception as e:
        print(f"TEST FAILED: {str(e)}")
