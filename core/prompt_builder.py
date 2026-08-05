"""
Builds the LLM prompt by loading prompt templates, context files, language preference, and scope.
"""
from pathlib import Path
from typing import Dict, Any, Optional
from .diff_analyzer import DiffScope

class PromptBuilder:
    def __init__(
        self,
        diff_scope: DiffScope,
        context_data: Dict[str, str],
        jira_data: Optional[Dict[str, Any]] = None,
        model_name: str = "deepseek-chat",
        language: str = "english"
    ):
        self.diff_scope = diff_scope
        self.context_data = context_data
        self.jira_data = jira_data
        self.model_name = model_name
        self.language = language

    def build(self) -> str:
        base_prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "base_review.md"
        base_instruction = ""
        if base_prompt_path.exists():
            base_instruction = base_prompt_path.read_text(encoding="utf-8")
        else:
            base_instruction = "You are Clark VanScoder, lead DevOps architect. Perform a strict code review."

        # Detect language specific extra prompts
        extra_prompts = []
        prompts_dir = Path(__file__).resolve().parent.parent / "prompts"
        for file_path in self.diff_scope.files_changed:
            ext = Path(file_path).suffix.lower()
            if ext in [".tf", ".tfvars"] and (prompts_dir / "terraform.md").exists():
                extra_prompts.append(("Terraform Rules", (prompts_dir / "terraform.md").read_text(encoding="utf-8")))
            elif "Dockerfile" in file_path and (prompts_dir / "docker.md").exists():
                extra_prompts.append(("Docker Rules", (prompts_dir / "docker.md").read_text(encoding="utf-8")))
            elif ext in [".py"] and (prompts_dir / "python.md").exists():
                extra_prompts.append(("Python Rules", (prompts_dir / "python.md").read_text(encoding="utf-8")))
            elif "ros2" in file_path.lower() or "telemetry" in file_path.lower():
                if (prompts_dir / "ros2.md").exists():
                    extra_prompts.append(("ROS 2 Rules", (prompts_dir / "ros2.md").read_text(encoding="utf-8")))

        prompt = f"{base_instruction}\n\n"
        prompt += f"Evaluator Model Name to output in the template: {self.model_name}\n"
        prompt += f"TARGET FEEDBACK LANGUAGE MANDATE: You MUST write your entire review response (comments, findings, rationale) in '{self.language}'. Maintain all exact markdown structure and headers.\n\n"

        if extra_prompts:
            prompt += "## Specialized Rules to Enforce\n"
            for title, rules in extra_prompts:
                prompt += f"### {title}\n{rules}\n\n"

        prompt += "## Repository Context Files Loaded\n"
        if self.context_data:
            for file_name, content in self.context_data.items():
                prompt += f"### File `{file_name}`\n```\n{content[:2000]}\n```\n\n"
        else:
            prompt += "_No AGENTS.md or extra context files found._\n\n"

        if self.jira_data:
            summary = self.jira_data.get("fields", {}).get("summary", "No summary")
            prompt += f"## Jira Ticket Context\nSummary: {summary}\n\n"

        prompt += "## Pull Request Diff Scope\n"
        prompt += f"- Files Changed: {', '.join(self.diff_scope.files_changed) if self.diff_scope.files_changed else 'None'}\n"
        prompt += f"- Directories Touched: {', '.join(self.diff_scope.directories_touched) if self.diff_scope.directories_touched else 'Root'}\n"
        prompt += f"- Commit Count: {self.diff_scope.commit_count}\n"
        prompt += f"- DDL/Schema Touched: {self.diff_scope.has_ddl}\n"
        prompt += f"- Runtime/FE/UX Code: {self.diff_scope.has_runtime or self.diff_scope.has_fe_ux}\n\n"

        prompt += "## Raw Git Patch Diff\n```diff\n"
        prompt += self.diff_scope.raw_diff
        prompt += "\n```\n\n"

        prompt += f"Output the markdown review strictly adhering to the requested format and in the target language '{self.language}'."
        return prompt
