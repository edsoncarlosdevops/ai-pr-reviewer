"""
Loads workspace context recursively scanning for guideline & architectural files.
"""
from pathlib import Path
from typing import List, Dict

class ContextLoader:
    def __init__(self, workspace: Path, extra_files: List[str]):
        self.workspace = workspace
        self.extra_files = extra_files

    def load_context(self) -> Dict[str, str]:
        context_data = {}
        
        # 1. Search root and nested subdirectories for AGENTS.md
        try:
            for agents_file in self.workspace.rglob("AGENTS.md"):
                # Ignore hidden directories like .git or .github
                if any(part.startswith('.') for part in agents_file.parts):
                    continue
                try:
                    rel_path = str(agents_file.relative_to(self.workspace))
                    context_data[rel_path] = agents_file.read_text(encoding="utf-8")
                except Exception:
                    pass
        except Exception:
            pass

        # 2. Search root README.md
        readme_file = self.workspace / "README.md"
        if readme_file.exists() and readme_file.is_file():
            try:
                context_data["README.md"] = readme_file.read_text(encoding="utf-8")
            except Exception:
                pass

        # 3. Search extra files requested in .pr_reviewer.toml
        for extra_name in self.extra_files:
            extra_path = self.workspace / extra_name
            if extra_path.exists() and extra_path.is_file():
                try:
                    context_data[extra_name] = extra_path.read_text(encoding="utf-8")
                except Exception:
                    pass

        return context_data
