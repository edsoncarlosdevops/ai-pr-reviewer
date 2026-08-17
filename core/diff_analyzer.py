"""
Analyzes git patch files to extract metadata about changes.
"""
import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set


@dataclass
class DiffScope:
    files_changed: List[str] = field(default_factory=list)
    directories_touched: Set[str] = field(default_factory=set)
    has_ddl: bool = False
    has_fe_ux: bool = False
    has_runtime: bool = False
    commit_count: int = 1
    raw_diff: str = ""

FILE_HEADER_RE = re.compile(r"^diff --git a/(.+?) b/(.+?)$", re.MULTILINE)
COMMIT_HEADER_RE = re.compile(r"^From [0-9a-f]{40}", re.MULTILINE)

class DiffAnalyzer:
    def __init__(self, diff_path: Path, exclude_patterns: Optional[List[str]] = None):
        self.diff_path = diff_path
        self.exclude_patterns = exclude_patterns or []

    def _is_excluded(self, file_path: str) -> bool:
        return any(fnmatch.fnmatch(file_path, pattern) for pattern in self.exclude_patterns)

    def _strip_excluded_files(self, content: str) -> str:
        """Removes whole per-file sections from the raw diff for excluded files."""
        if not self.exclude_patterns:
            return content

        headers = list(FILE_HEADER_RE.finditer(content))
        if not headers:
            return content

        kept_chunks = []
        for i, match in enumerate(headers):
            chunk_start = match.start()
            chunk_end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
            file_path = match.group(2)
            if not self._is_excluded(file_path):
                kept_chunks.append(content[chunk_start:chunk_end])

        return "".join(kept_chunks)

    def analyze(self) -> DiffScope:
        scope = DiffScope()
        if not self.diff_path.exists():
            return scope

        with open(self.diff_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = self._strip_excluded_files(content)
        scope.raw_diff = content

        for match in FILE_HEADER_RE.finditer(content):
            file_path = match.group(2)
            scope.files_changed.append(file_path)
            scope.directories_touched.add(str(Path(file_path).parent))

            ext = Path(file_path).suffix.lower()
            if ext in [".sql"]:
                scope.has_ddl = True
            if ext in [".js", ".ts", ".jsx", ".tsx", ".css", ".scss", ".html", ".vue"]:
                scope.has_fe_ux = True
            if ext in [".py", ".java", ".go", ".rs", ".cpp", ".c", ".rb"]:
                scope.has_runtime = True

        # Commit count approximation
        commits = len(COMMIT_HEADER_RE.findall(content))
        scope.commit_count = commits if commits > 0 else 1

        return scope
