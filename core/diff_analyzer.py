"""
Analyzes git patch files to extract metadata about changes.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set

@dataclass
class DiffScope:
    files_changed: List[str] = field(default_factory=list)
    directories_touched: Set[str] = field(default_factory=set)
    has_ddl: bool = False
    has_fe_ux: bool = False
    has_runtime: bool = False
    commit_count: int = 1
    raw_diff: str = ""

class DiffAnalyzer:
    def __init__(self, diff_path: Path):
        self.diff_path = diff_path

    def analyze(self) -> DiffScope:
        scope = DiffScope()
        if not self.diff_path.exists():
            return scope
            
        with open(self.diff_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        scope.raw_diff = content
        
        # Simple extraction
        file_pattern = re.compile(r"^diff --git a/(.+?) b/(.+?)$", re.MULTILINE)
        for match in file_pattern.finditer(content):
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
        commit_pattern = re.compile(r"^From [0-9a-f]{40}", re.MULTILINE)
        commits = len(commit_pattern.findall(content))
        scope.commit_count = commits if commits > 0 else 1
        
        return scope
