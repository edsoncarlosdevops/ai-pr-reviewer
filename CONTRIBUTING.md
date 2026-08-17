# Contributing to AI PR Reviewer

Thanks for your interest in improving AI PR Reviewer! This document explains how to get a
development environment running and how to submit changes.

## Getting started

```bash
git clone https://github.com/edsoncarlosdevops/ai-pr-reviewer.git
cd ai-pr-reviewer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Run the test suite and linter before opening a PR:

```bash
pytest -v
ruff check .
```

Try the CLI end-to-end against a real diff:

```bash
export DEEPSEEK_API_KEY="your-key"
git diff origin/main...HEAD > /tmp/pr.patch
python core/cli.py --diff /tmp/pr.patch --workspace . --output review.md
```

## Project layout

- `core/` — the platform-agnostic review engine (diff analysis, context loading, prompt
  building, LLM client, CLI entry point). This is the only code that should know how to
  talk to an LLM provider.
- `prompts/` — the base review persona and per-language/tool domain rule files, auto-loaded
  based on which file extensions appear in a diff.
- `action.yml` — the GitHub Action (composite) entry point.
- `wrappers/` — integration glue for Azure DevOps and GitLab CI. Each wrapper clones the
  pinned `core/` engine at run time and shells out to `core/cli.py`.
- `examples/consumer-configs/` — copy-pasteable pipeline configs for each supported platform.
- `tests/` — unit tests for `core/`.

## Making changes

- Keep `core/` free of any GitHub/Azure/GitLab-specific code — CI-platform logic belongs in
  `action.yml` or `wrappers/`.
- Add or update tests for any behavior change in `core/`. `tests/` mirrors the module layout.
- Run `ruff check .` — CI enforces a clean lint on every PR.
- If you change the review output format, update the sample output in `README.md` to match.
- Prefer small, focused PRs. Describe the "why", not just the "what", in the PR description.

## Reporting bugs / requesting features

Please use the issue templates under `.github/ISSUE_TEMPLATE/`. Include the platform
(GitHub Actions / Azure DevOps / GitLab CI / local CLI), the model/provider in use, and
reproduction steps or a minimal diff when reporting a bug.

## Security issues

Do not open a public issue for security vulnerabilities — see [SECURITY.md](SECURITY.md).

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
