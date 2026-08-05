"""
Jira integration.
"""
from typing import Optional, Dict, Any
from .config import JiraConfig
import urllib.request
import json
import base64

class JiraClient:
    def __init__(self, config: JiraConfig):
        self.config = config

    def get_issue(self, issue_key: str) -> Optional[Dict[str, Any]]:
        if not self.config.enabled or not self.config.url or not self.config.email or not self.config.api_token:
            return None
            
        try:
            url = f"{self.config.url.rstrip('/')}/rest/api/2/issue/{issue_key}"
            auth_str = f"{self.config.email}:{self.config.api_token}"
            auth_bytes = auth_str.encode("ascii")
            base64_auth = base64.b64encode(auth_bytes).decode("ascii")
            
            req = urllib.request.Request(url)
            req.add_header("Authorization", f"Basic {base64_auth}")
            req.add_header("Accept", "application/json")
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    return data
        except Exception:
            return None
        return None
