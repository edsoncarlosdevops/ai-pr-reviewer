"""
Jira integration.
"""
import sys
from typing import Any, Dict, Optional

import requests

from .config import JiraConfig


class JiraClient:
    def __init__(self, config: JiraConfig):
        self.config = config

    def get_issue(self, issue_key: str) -> Optional[Dict[str, Any]]:
        if not self.config.enabled or not self.config.url or not self.config.email or not self.config.api_token:
            return None

        url = f"{self.config.url.rstrip('/')}/rest/api/2/issue/{issue_key}"
        try:
            response = requests.get(
                url,
                auth=(self.config.email, self.config.api_token),
                headers={"Accept": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            print(f"Warning: failed to fetch Jira issue '{issue_key}' ({exc}).", file=sys.stderr)
            return None
