import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from core.context_loader import ContextLoader


class TestContextLoader(unittest.TestCase):
    def setUp(self):
        self._tmp = TemporaryDirectory()
        self.workspace = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_loads_root_and_nested_agents_md(self):
        (self.workspace / "AGENTS.md").write_text("root rules", encoding="utf-8")
        nested = self.workspace / "terraform"
        nested.mkdir()
        (nested / "AGENTS.md").write_text("terraform rules", encoding="utf-8")

        loader = ContextLoader(self.workspace, extra_files=[])
        context = loader.load_context()

        self.assertEqual(context["AGENTS.md"], "root rules")
        self.assertEqual(context[str(Path("terraform") / "AGENTS.md")], "terraform rules")

    def test_skips_hidden_directories(self):
        hidden = self.workspace / ".git"
        hidden.mkdir()
        (hidden / "AGENTS.md").write_text("should not load", encoding="utf-8")

        loader = ContextLoader(self.workspace, extra_files=[])
        context = loader.load_context()

        self.assertNotIn(str(Path(".git") / "AGENTS.md"), context)

    def test_loads_readme_and_custom_rule_files(self):
        (self.workspace / "README.md").write_text("readme content", encoding="utf-8")
        (self.workspace / "CLAUDE.md").write_text("claude rules", encoding="utf-8")

        loader = ContextLoader(self.workspace, extra_files=[])
        context = loader.load_context()

        self.assertEqual(context["README.md"], "readme content")
        self.assertEqual(context["CLAUDE.md"], "claude rules")

    def test_loads_extra_context_files_and_warns_on_missing(self):
        (self.workspace / "docs").mkdir()
        (self.workspace / "docs" / "architecture.md").write_text("arch doc", encoding="utf-8")

        loader = ContextLoader(
            self.workspace,
            extra_files=["docs/architecture.md", "does/not/exist.md"],
        )
        context = loader.load_context()

        self.assertEqual(context["docs/architecture.md"], "arch doc")
        self.assertNotIn("does/not/exist.md", context)


if __name__ == "__main__":
    unittest.main()
