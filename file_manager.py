"""
file_manager.py
Handles CRUD operations on the local file system.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from logger import get_logger

logger = get_logger()

class FileManager:
    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir).resolve()
        logger.info(f"File manager operating from {self.root}")

    def create_file(self, filename: str, content: str = "") -> bool:
        """Creates a file with the specified content."""
        target = self.root / filename
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Created file: {target}")
            return True
        except Exception as e:
            logger.error(f"Failed to create file {filename}: {e}")
            return False

    def read_file(self, filename: str) -> Optional[str]:
        """Reads content from a file."""
        target = self.root / filename
        try:
            if target.exists() and target.is_file():
                with open(target, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {e}")
            return None

    def search_files(self, query: str) -> List[str]:
        """Searches for files matching a query recursively."""
        results = []
        try:
            for path in self.root.rglob(f"*{query}*"):
                if path.is_file():
                    results.append(str(path.relative_to(self.root)))
            return results
        except Exception as e:
            logger.error(f"Error searching files for {query}: {e}")
            return []

if __name__ == "__main__":
    fm = FileManager()
    print(f"Working directory: {fm.root}")
