"""
task_engine.py
Queues and executes parsed Task chaining sequences asynchronously.
"""

import asyncio
from typing import List, Any
from logger import get_logger
from command_parser import Task, ActionType

from automation_engine import AutomationEngine
from system_control import SystemControl
from file_manager import FileManager
from internet_engine import InternetEngine
from memory_engine import MemoryEngine

logger = get_logger()

class TaskEngine:
    def __init__(self, memory: MemoryEngine):
        self.memory = memory
        self.automation = AutomationEngine()
        self.system = SystemControl()
        self.files = FileManager()
        self.internet = InternetEngine()
        logger.info("Task engine and sub-engines loaded.")

    async def execute_task(self, task: Task) -> Any:
        """Executes a single task based on its ActionType."""
        action = task.action_type
        params = task.parameters
        logger.info(f"Executing: {task}")
        
        try:
            if action == ActionType.OPEN_APP:
                app = params.get("app_name", "")
                success = self.system.launch_app(app)
                return f"Successfully opened {app}" if success else f"Failed to open {app}"
                
            elif action == ActionType.WEB_SEARCH:
                query = params.get("query", "")
                result = await self.internet.perform_search(query)
                return result
                
            elif action == ActionType.SYSTEM_CMD:
                cmd = params.get("command", "")
                if cmd == "volume":
                    self.system.set_volume(int(params.get("level", 50)))
                elif cmd == "brightness":
                    self.system.set_brightness(int(params.get("level", 50)))
                return f"Executed system command: {cmd}"
                
            elif action == ActionType.MEMORY_QUERY:
                pass

            elif action == ActionType.FILE_OP:
                op = params.get("operation")
                if op == "create":
                    self.files.create_file(params.get("filename", "temp.txt"), params.get("content", ""))
                return f"File operation {op} completed."

            elif action == ActionType.AUTOMATION:
                if params.get("action") == "type":
                    self.automation.type_text(params.get("text", ""))
                return "Automation completed."
                
            elif action == ActionType.CHAT:
                return "Chat routed."
                
            else:
                return f"Action fallback / Not Implemented Fully: {action}"
                
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return f"Error executing task: {e}"

    async def execute_chain(self, tasks: List[Task]) -> List[Any]:
        """Sequentially executes a list of tasks."""
        results = []
        for index, task in enumerate(tasks):
            logger.info(f"--- Chain Step {index+1}/{len(tasks)} ---")
            result = await self.execute_task(task)
            results.append(result)
            if "Error" in str(result) or "Failed" in str(result):
                logger.warning(f"Chain step {index+1} encountered an issue.")
        return results

if __name__ == "__main__":
    pass
