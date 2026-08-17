import unittest

from core.config import LLMConfig
from core.llm_client import LLMClient


class TestLLMClient(unittest.TestCase):
    def test_raises_clear_error_when_api_key_missing(self):
        config = LLMConfig(api_key=None)
        with self.assertRaises(ValueError) as ctx:
            LLMClient(config)
        self.assertIn("No LLM API key configured", str(ctx.exception))

    def test_constructs_when_api_key_present(self):
        config = LLMConfig(api_key="sk-test")
        client = LLMClient(config)
        self.assertEqual(client.config.api_key, "sk-test")


if __name__ == "__main__":
    unittest.main()
