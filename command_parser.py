"""
command_parser.py
Maps natural language intents to ActionTypes and builds Task chains.
"""

from enum import Enum, auto
from typing import List, Dict, Any
from logger import get_logger

logger = get_logger()

class ActionType(Enum):
    OPEN_APP = auto()
    WEB_SEARCH = auto()
    FILE_OP = auto()
    SYSTEM_CMD = auto()
    AUTOMATION = auto()
    MEMORY_QUERY = auto()
    CHAIN = auto()
    CHAT = auto()
    UNKNOWN = auto()
    ERROR = auto()

class Task:
    def __init__(self, action_type: ActionType, parameters: Dict[str, Any]):
        self.action_type = action_type
        self.parameters = parameters
        
    def __repr__(self):
        return f"Task({self.action_type.name}, {self.parameters})"

class CommandParser:
    def __init__(self):
        self.intent_map = {
            "OPEN_APP": ActionType.OPEN_APP,
            "WEB_SEARCH": ActionType.WEB_SEARCH,
            "FILE_OP": ActionType.FILE_OP,
            "SYSTEM_CMD": ActionType.SYSTEM_CMD,
            "AUTOMATION": ActionType.AUTOMATION,
            "MEMORY_QUERY": ActionType.MEMORY_QUERY,
            "CHAIN": ActionType.CHAIN,
            "CHAT": ActionType.CHAT,
            "ERROR": ActionType.ERROR
        }
    
    def parse_llm_output(self, llm_output: Dict[str, Any]) -> List[Task]:
        """Converts LLM JSON intent payload into actionable Task objects."""
        tasks = []
        intent_str = llm_output.get("intent", "UNKNOWN")
        entities = llm_output.get("entities", {})
        
        action_type = self.intent_map.get(intent_str, ActionType.UNKNOWN)
        
        if action_type == ActionType.CHAIN and "steps" in entities:
            # Handle chained multi-step commands
            for step in entities["steps"]:
                step_intent = step.get("intent", "UNKNOWN")
                step_action = self.intent_map.get(step_intent, ActionType.UNKNOWN)
                tasks.append(Task(step_action, step.get("entities", {})))
        else:
            tasks.append(Task(action_type, entities))
            
        logger.debug(f"Parsed {len(tasks)} tasks from intent {intent_str}")
        return tasks

if __name__ == "__main__":
    parser = CommandParser()
    sample_llm = {
        "intent": "OPEN_APP",
        "entities": {"app_name": "Spotify"}
    }
    tasks = parser.parse_llm_output(sample_llm)
    print(tasks)
