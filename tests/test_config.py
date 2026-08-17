import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from core.config import load_config


class TestLoadConfig(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.workspace = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_defaults_when_no_toml_present(self):
        with patch.dict("os.environ", {}, clear=True):
            config = load_config(self.workspace)
        self.assertEqual(config.llm.provider, "deepseek")
        self.assertEqual(config.llm.model, "deepseek-chat")
        self.assertIsNone(config.llm.api_key)
        self.assertFalse(config.jira.enabled)

    def test_api_key_precedence(self):
        with patch.dict(
            "os.environ",
            {"DEEPSEEK_API_KEY": "deepseek-key", "OPENAI_API_KEY": "openai-key"},
            clear=True,
        ):
            config = load_config(self.workspace)
        self.assertEqual(config.llm.api_key, "deepseek-key")

    def test_toml_overrides_defaults(self):
        (self.workspace / ".pr_reviewer.toml").write_text(
            """
            [llm]
            provider = "openai"
            model = "gpt-4o-mini"
            language = "portuguese"

            [jira]
            enabled = true
            url = "https://example.atlassian.net"
            """,
            encoding="utf-8",
        )
        with patch.dict("os.environ", {}, clear=True):
            config = load_config(self.workspace)
        self.assertEqual(config.llm.provider, "openai")
        self.assertEqual(config.llm.model, "gpt-4o-mini")
        self.assertEqual(config.llm.language, "portuguese")
        self.assertTrue(config.jira.enabled)
        self.assertEqual(config.jira.url, "https://example.atlassian.net")

    def test_malformed_toml_falls_back_to_defaults_with_warning(self):
        (self.workspace / ".pr_reviewer.toml").write_text("this is not [valid toml", encoding="utf-8")
        stderr = io.StringIO()
        with patch.dict("os.environ", {}, clear=True), redirect_stderr(stderr):
            config = load_config(self.workspace)
        self.assertEqual(config.llm.provider, "deepseek")
        self.assertIn("Warning", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
