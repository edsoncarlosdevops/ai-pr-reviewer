"""
Builds the LLM prompt.
"""
from typing import Dict, Any, Optional
from .diff_analyzer import DiffScope

class PromptBuilder:
    def __init__(self, diff_scope: DiffScope, context_data: Dict[str, str], jira_data: Optional[Dict[str, Any]] = None):
        self.diff_scope = diff_scope
        self.context_data = context_data
        self.jira_data = jira_data

    def build(self) -> str:
        prompt = "Please review the following PR diff and provide a code review in the style of Clark VanScoder.\\n\\n"
        
        prompt += "### Context\\n"
        for file_name, content in self.context_data.items():
            prompt += f"#### {file_name}\\n```\\n{content}\\n```\\n\\n"
            
        if self.jira_data:
            summary = self.jira_data.get("fields", {}).get("summary", "No summary")
            prompt += f"### Jira Issue\\nSummary: {summary}\\n\\n"
            
        prompt += f"### Scope\\nFiles changed: {len(self.diff_scope.files_changed)}\\n"
        prompt += f"Commit count: {self.diff_scope.commit_count}\\n\\n"
        
        prompt += "### Diff\\n```diff\\n"
        prompt += self.diff_scope.raw_diff
        prompt += "\\n```\\n"
        
        prompt += "\\nPlease format your output directly as markdown.\\n"
        return prompt
