"""
Loads workspace context dynamically scanning for all AGENTS.md, *.prompt.md, .cursorrules, and architectural files.
"""
from pathlib import Path
from typing import List, Dict

class ContextLoader:
    def __init__(self, workspace: Path, extra_files: List[str]):
        self.workspace = workspace
        self.extra_files = extra_files

    def load_context(self) -> Dict[str, str]:
        context_data = {}
        
        # 1. Dynamically scan all AGENTS.md files throughout the entire repository tree
        try:
            for agents_file in self.workspace.rglob("AGENTS.md"):
                if any(part.startswith('.') for part in agents_file.parts if part != '.'):
                    continue
                try:
                    rel_path = str(agents_file.relative_to(self.workspace))
                    context_data[rel_path] = agents_file.read_text(encoding="utf-8")
                except Exception:
                    pass
        except Exception:
            pass

        # 2. Dynamically scan for project-specific custom prompt/rules files (*.prompt.md, .cursorrules, CLAUDE.md)
        custom_rule_patterns = ["*.prompt.md", ".cursorrules", "CLAUDE.md", "REVIEW_GUIDELINES.md"]
        for pattern in custom_rule_patterns:
            try:
                for rule_file in self.workspace.rglob(pattern):
                    if any(part.startswith('.') for part in rule_file.parts if part not in ['.', '.cursorrules']):
                        continue
                    try:
                        rel_path = str(rule_file.relative_to(self.workspace))
                        context_data[rel_path] = rule_file.read_text(encoding="utf-8")
                    except Exception:
                        pass
            except Exception:
                pass

        # 3. Search root README.md
        readme_file = self.workspace / "README.md"
        if readme_file.exists() and readme_file.is_file():
            try:
                context_data["README.md"] = readme_file.read_text(encoding="utf-8")
            except Exception:
                pass

        # 4. Search extra files requested in .pr_reviewer.toml
        for extra_name in self.extra_files:
            extra_path = self.workspace / extra_name
            if extra_path.exists() and extra_path.is_file():
                try:
                    context_data[extra_name] = extra_path.read_text(encoding="utf-8")
                except Exception:
                    pass

        return context_data
