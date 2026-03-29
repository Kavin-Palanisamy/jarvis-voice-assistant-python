"""
memory_engine.py
Handles persistent storage for context, conversations, and learned facts via SQLite.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from logger import get_logger
logger = get_logger()

class MemoryEngine:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = Path(db_path)
        self._init_db()

    def _init_db(self):
        """Initializes the SQLite database and schema if it does not exist."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        user_input TEXT,
                        jarvis_response TEXT,
                        intent TEXT
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS preferences (
                        key TEXT PRIMARY KEY,
                        value TEXT,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS facts (
                        entity TEXT PRIMARY KEY,
                        value TEXT,
                        confidence REAL,
                        source_conversation_id INTEGER
                    )
                ''')
                conn.commit()
            logger.info(f"Database initialized at {self.db_path.absolute()}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def remember_conversation(self, user_input: str, response: str, intent: str = "UNKNOWN") -> Optional[int]:
        """Stores an interaction in the memory."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO conversations (user_input, jarvis_response, intent) VALUES (?, ?, ?)",
                    (user_input, response, intent)
                )
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            logger.error(f"Failed to record conversation: {e}")
            return None

    def get_context_window(self, limit: int = 10) -> List[Dict[str, str]]:
        """Retrieves the last N interactions for LLM context."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT user_input, jarvis_response FROM conversations ORDER BY timestamp DESC LIMIT ?",
                    (limit,)
                )
                rows = cursor.fetchall()
                
                context = []
                for row in reversed(rows):
                    context.append({"role": "user", "parts": [row["user_input"]]})
                    context.append({"role": "model", "parts": [row["jarvis_response"]]})
                return context
        except Exception as e:
            logger.error(f"Failed to retrieve context window: {e}")
            return []

    def update_preference(self, key: str, value: Any):
        """Stores or updates a user preference mapping."""
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                str_val = json.dumps(value) if not isinstance(value, str) else value
                cursor.execute(
                    "INSERT OR REPLACE INTO preferences (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                    (key, str_val)
                )
                conn.commit()
                logger.debug(f"Preference updated: {key} = {value}")
        except Exception as e:
            logger.error(f"Failed to update preference '{key}': {e}")

    def get_preference(self, key: str, default: Any = None) -> Any:
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM preferences WHERE key = ?", (key,))
                row = cursor.fetchone()
                if row:
                    try:
                        return json.loads(row[0])
                    except json.JSONDecodeError:
                        return row[0]
                return default
        except Exception as e:
            logger.error(f"Failed to get preference '{key}': {e}")
            return default

    def store_fact(self, entity: str, value: str, confidence: float = 1.0, source_id: int = None):
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO facts (entity, value, confidence, source_conversation_id) VALUES (?, ?, ?, ?)",
                    (entity, value, confidence, source_id)
                )
                conn.commit()
                logger.debug(f"Fact stored: {entity} -> {value}")
        except Exception as e:
            logger.error(f"Failed to store fact '{entity}': {e}")

    def recall_fact(self, entity: str) -> Optional[str]:
        try:
            with sqlite3.connect(str(self.db_path)) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT value FROM facts WHERE entity = ?", (entity,))
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            logger.error(f"Failed to recall fact '{entity}': {e}")
            return None

if __name__ == "__main__":
    mem = MemoryEngine(":memory:")
    mem.update_preference("preferred_browser", "Chrome")
    logger.info(f"Test Browser: {mem.get_preference('preferred_browser')}")
