"""
Loads workspace context dynamically scanning for all AGENTS.md, *.prompt.md, .cursorrules, and architectural files.
"""
import sys
from pathlib import Path
from typing import Dict, List


class ContextLoader:
    def __init__(self, workspace: Path, extra_files: List[str]):
        self.workspace = workspace
        self.extra_files = extra_files

    def _read_file(self, context_data: Dict[str, str], path: Path, rel_path: str) -> None:
        try:
            context_data[rel_path] = path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Warning: could not read context file {rel_path} ({exc}).", file=sys.stderr)

    def load_context(self) -> Dict[str, str]:
        context_data = {}

        # 1. Dynamically scan all AGENTS.md files throughout the entire repository tree
        try:
            for agents_file in self.workspace.rglob("AGENTS.md"):
                if any(part.startswith('.') for part in agents_file.parts if part != '.'):
                    continue
                self._read_file(context_data, agents_file, str(agents_file.relative_to(self.workspace)))
        except Exception as exc:
            print(f"Warning: failed to scan for AGENTS.md files ({exc}).", file=sys.stderr)

        # 2. Dynamically scan for project-specific custom prompt/rules files (*.prompt.md, .cursorrules, CLAUDE.md)
        custom_rule_patterns = ["*.prompt.md", ".cursorrules", "CLAUDE.md", "REVIEW_GUIDELINES.md"]
        for pattern in custom_rule_patterns:
            try:
                for rule_file in self.workspace.rglob(pattern):
                    if any(part.startswith('.') for part in rule_file.parts if part not in ['.', '.cursorrules']):
                        continue
                    self._read_file(context_data, rule_file, str(rule_file.relative_to(self.workspace)))
            except Exception as exc:
                print(f"Warning: failed to scan for '{pattern}' files ({exc}).", file=sys.stderr)

        # 3. Search root README.md
        readme_file = self.workspace / "README.md"
        if readme_file.exists() and readme_file.is_file():
            self._read_file(context_data, readme_file, "README.md")

        # 4. Search extra files requested in .pr_reviewer.toml
        for extra_name in self.extra_files:
            extra_path = self.workspace / extra_name
            if extra_path.exists() and extra_path.is_file():
                self._read_file(context_data, extra_path, extra_name)
            else:
                print(f"Warning: extra_context_files entry '{extra_name}' not found in workspace.", file=sys.stderr)

        return context_data
