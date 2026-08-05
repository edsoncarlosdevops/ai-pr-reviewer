# Shell Script Review Rules

Verify Shell and Bash scripts for production readiness:
- Ensure `set -euo pipefail` is present at top of scripts for fail-fast behavior.
- Check proper quoting of all variables (`"$VAR"`) to prevent word splitting and injection.
- Verify exit code handling for background processes and subshells.
- Ensure temporary files use `mktemp` and are cleaned up with `trap`.
