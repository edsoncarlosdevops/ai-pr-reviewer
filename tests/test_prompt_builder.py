import unittest

from core.diff_analyzer import DiffScope
from core.prompt_builder import PromptBuilder


class TestPromptBuilder(unittest.TestCase):
    def test_includes_language_mandate(self):
        scope = DiffScope(files_changed=["app.py"])
        prompt = PromptBuilder(scope, context_data={}, language="portuguese").build()
        self.assertIn("TARGET FEEDBACK LANGUAGE MANDATE", prompt)
        self.assertIn("'portuguese'", prompt)

    def test_injects_language_specific_domain_rules(self):
        scope = DiffScope(files_changed=["core/app.py"])
        prompt = PromptBuilder(scope, context_data={}).build()
        self.assertIn("Python Rules", prompt)
        self.assertIn("PEP 8 styling", prompt)

    def test_no_domain_rules_for_unmatched_extensions(self):
        scope = DiffScope(files_changed=["README.txt"])
        prompt = PromptBuilder(scope, context_data={}).build()
        self.assertNotIn("## Domain Rules to Enforce", prompt)

    def test_fallback_instruction_when_no_context_available(self):
        scope = DiffScope(files_changed=["README.txt"])
        prompt = PromptBuilder(scope, context_data={}).build()
        self.assertIn("FALLBACK AGENT INSTRUCTION", prompt)

    def test_context_consulted_lists_loaded_files(self):
        scope = DiffScope(files_changed=["app.py"])
        prompt = PromptBuilder(scope, context_data={"AGENTS.md": "some rules"}).build()
        self.assertIn("AGENTS.md", prompt)
        self.assertNotIn("FALLBACK AGENT INSTRUCTION", prompt)

    def test_jira_summary_included_when_present(self):
        scope = DiffScope(files_changed=["app.py"])
        jira_data = {"fields": {"summary": "Fix the login bug"}}
        prompt = PromptBuilder(scope, context_data={}, jira_data=jira_data).build()
        self.assertIn("Fix the login bug", prompt)

    def test_raw_diff_included_in_prompt(self):
        scope = DiffScope(files_changed=["app.py"], raw_diff="diff --git a/app.py b/app.py")
        prompt = PromptBuilder(scope, context_data={}).build()
        self.assertIn("diff --git a/app.py b/app.py", prompt)


if __name__ == "__main__":
    unittest.main()
