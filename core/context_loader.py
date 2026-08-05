"""
Loads workspace context.
"""
from pathlib import Path
from typing import List, Dict

class ContextLoader:
    def __init__(self, workspace: Path, extra_files: List[str]):
        self.workspace = workspace
        self.extra_files = extra_files

    def load_context(self) -> Dict[str, str]:
        context_data = {}
        target_files = ["AGENTS.md", "README.md"] + self.extra_files
        
        for file_name in target_files:
            file_path = self.workspace / file_name
            if file_path.exists() and file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        context_data[file_name] = f.read()
                except Exception:
                    pass
                    
        return context_data
