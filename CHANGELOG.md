# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- `setup.py` console-script entry point pointed at a nonexistent `cli.reviewer:main`
  module; it now correctly points at `core.cli:main`.
- `Dockerfile` `ENTRYPOINT` pointed at a nonexistent `cli/reviewer.py`; now runs `core/cli.py`.
- Azure DevOps and GitLab CI wrappers referenced the same nonexistent script path and
  never actually fetched the review engine at all. They now clone the pinned engine
  version at run time and call `core/cli.py` directly.
- Azure DevOps and GitLab CI wrappers never posted the generated review anywhere — they
  only produced a local file. Both now post (and update on re-run) a sticky comment on
  the pull/merge request via the platform's REST API.
- `exclude_patterns` was accepted as an input on every integration but silently ignored.
  It's now implemented in `core/diff_analyzer.py` and wired through the CLI and all
  three CI platform configs.
- Removed `core/review_formatter.py`: it was dead code (never invoked) and contained a
  bug where it emitted a literal `\n` instead of a newline.
- `core/config.py` and `core/context_loader.py` silently swallowed all exceptions,
  including malformed `.pr_reviewer.toml` files, making misconfiguration invisible.
  They now print a clear warning to stderr and fall back to defaults.
- `core/llm_client.py` silently used a `"dummy-key"` placeholder when no provider API
  key was configured, producing a confusing upstream auth error. It now fails fast with
  a clear message listing the expected environment variables.
- Duplicated, out-of-sync copy of the GitHub Action under `wrappers/github-action/`
  removed in favor of the single source of truth at the repository root (`action.yml`).

### Added
- Real unit test coverage for `core/diff_analyzer.py`, `core/context_loader.py`,
  `core/prompt_builder.py`, `core/config.py`, and `core/llm_client.py` (previously
  placeholder `assertTrue(True)` stubs).
- CI workflow (`.github/workflows/ci.yml`) running `ruff` and `pytest` on every push
  and pull request, across Python 3.10–3.12.
- `requirements-dev.txt` and `pyproject.toml` with `ruff`/`pytest` configuration.
- Community health files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
  issue templates, and a pull request template.

## [0.1.0] - 2026-08-05

### Added
- Initial release: agnostic Python review engine (`core/`) with pluggable LLM
  provider support (DeepSeek, OpenAI, Anthropic, or any OpenAI-compatible endpoint).
- GitHub Action, Azure DevOps pipeline template, and GitLab CI template integrations.
- Recursive `AGENTS.md` / `*.prompt.md` / `.cursorrules` context discovery.
- Language-specialist prompt rules for Terraform, Docker, Kubernetes, Python, Go,
  Rust, JavaScript/TypeScript, Shell, ROS 2, and GitHub Actions workflows.
- Multilingual feedback output via `.pr_reviewer.toml`.
- Optional Jira issue/acceptance-criteria validation.

[Unreleased]: https://github.com/edsoncarlosdevops/ai-pr-reviewer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/edsoncarlosdevops/ai-pr-reviewer/releases/tag/v0.1.0
