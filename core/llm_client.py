"""
LLM Client wrapper around OpenAI SDK.
"""
from typing import Optional
from openai import OpenAI
from .config import LLMConfig

class LLMClient:
    def __init__(self, config: LLMConfig):
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key or "dummy-key",
            base_url=config.base_url
        )

    def generate_review(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are an expert AI PR Reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"Error generating review: {str(e)}"
