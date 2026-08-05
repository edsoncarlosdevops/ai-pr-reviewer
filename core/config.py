"""
Configuration module for the AI PR Reviewer.
"""
import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List

@dataclass
class JiraConfig:
    enabled: bool = False
    url: str = ""
    email: str = ""
    api_token: str = ""

@dataclass
class LLMConfig:
    provider: str = "deepseek"
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com"
    api_key: Optional[str] = None

@dataclass
class AppConfig:
    llm: LLMConfig = field(default_factory=LLMConfig)
    jira: JiraConfig = field(default_factory=JiraConfig)
    extra_context_files: List[str] = field(default_factory=list)

def load_config(workspace_path: Path) -> AppConfig:
    config_path = workspace_path / ".pr_reviewer.toml"
    
    app_config = AppConfig()
    app_config.llm.api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
    
    if config_path.is_file():
        try:
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
                
            if "llm" in data:
                llm_data = data["llm"]
                app_config.llm.provider = llm_data.get("provider", app_config.llm.provider)
                app_config.llm.model = llm_data.get("model", app_config.llm.model)
                app_config.llm.base_url = llm_data.get("base_url", app_config.llm.base_url)
                
            if "jira" in data:
                jira_data = data["jira"]
                app_config.jira.enabled = jira_data.get("enabled", app_config.jira.enabled)
                app_config.jira.url = jira_data.get("url", app_config.jira.url)
                app_config.jira.email = jira_data.get("email", app_config.jira.email)
                app_config.jira.api_token = jira_data.get("api_token", app_config.jira.api_token)
                
            if "context" in data:
                app_config.extra_context_files = data["context"].get("extra_files", [])
        except Exception:
            pass
            
    return app_config
