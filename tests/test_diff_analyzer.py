import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from core.diff_analyzer import DiffAnalyzer

SAMPLE_DIFF = """diff --git a/src/app.py b/src/app.py
index 0000000..1111111 100644
--- a/src/app.py
+++ b/src/app.py
@@ -1,2 +1,3 @@
 def main():
+    print("hello")
     pass
diff --git a/tests/test_app.py b/tests/test_app.py
index 0000000..2222222 100644
--- a/tests/test_app.py
+++ b/tests/test_app.py
@@ -1,1 +1,2 @@
 import unittest
+import os
diff --git a/infra/schema.sql b/infra/schema.sql
index 0000000..3333333 100644
--- a/infra/schema.sql
+++ b/infra/schema.sql
@@ -1,1 +1,2 @@
 CREATE TABLE foo (id INT);
+CREATE TABLE bar (id INT);
"""


def write_diff(content: str) -> Path:
    f = NamedTemporaryFile(mode="w", suffix=".patch", delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return Path(f.name)


class TestDiffAnalyzer(unittest.TestCase):
    def test_missing_file_returns_empty_scope(self):
        analyzer = DiffAnalyzer(Path("/nonexistent/path.patch"))
        scope = analyzer.analyze()
        self.assertEqual(scope.files_changed, [])
        self.assertEqual(scope.raw_diff, "")

    def test_analyze_extracts_files_and_flags(self):
        diff_path = write_diff(SAMPLE_DIFF)
        try:
            scope = DiffAnalyzer(diff_path).analyze()
            self.assertEqual(
                scope.files_changed,
                ["src/app.py", "tests/test_app.py", "infra/schema.sql"],
            )
            self.assertIn("src", scope.directories_touched)
            self.assertIn("tests", scope.directories_touched)
            self.assertIn("infra", scope.directories_touched)
            self.assertTrue(scope.has_ddl)
            self.assertTrue(scope.has_runtime)
            self.assertFalse(scope.has_fe_ux)
            self.assertEqual(scope.commit_count, 1)
        finally:
            diff_path.unlink()

    def test_exclude_patterns_strip_matching_files(self):
        diff_path = write_diff(SAMPLE_DIFF)
        try:
            scope = DiffAnalyzer(diff_path, exclude_patterns=["tests/*"]).analyze()
            self.assertEqual(scope.files_changed, ["src/app.py", "infra/schema.sql"])
            self.assertNotIn("tests/test_app.py", scope.raw_diff)
            self.assertIn("src/app.py", scope.raw_diff)
        finally:
            diff_path.unlink()

    def test_exclude_patterns_can_drop_all_files(self):
        diff_path = write_diff(SAMPLE_DIFF)
        try:
            scope = DiffAnalyzer(diff_path, exclude_patterns=["*"]).analyze()
            self.assertEqual(scope.files_changed, [])
            self.assertEqual(scope.raw_diff.strip(), "")
        finally:
            diff_path.unlink()


if __name__ == "__main__":
    unittest.main()
