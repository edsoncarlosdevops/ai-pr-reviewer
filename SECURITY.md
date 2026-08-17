# Security Policy

## Supported Versions

AI PR Reviewer is pre-1.0 and currently ships as a single rolling `v1` release line.
Security fixes are applied to the latest release on the `main` branch.

| Version | Supported |
| ------- | --------- |
| latest (`main`) | ✅ |
| older tagged releases | ❌ |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report it privately using [GitHub's private vulnerability reporting](https://github.com/edsoncarlosdevops/ai-pr-reviewer/security/advisories/new)
for this repository. If that is not available, open a draft security advisory or
contact the maintainer directly through their GitHub profile.

Please include:

- A description of the vulnerability and its potential impact
- Steps to reproduce (a minimal repro repo/diff is ideal)
- The platform involved (GitHub Actions, Azure DevOps, GitLab CI, or local CLI)

We aim to acknowledge reports within 5 business days.

## Handling of Secrets

AI PR Reviewer reads LLM provider API keys (`DEEPSEEK_API_KEY`, `OPENAI_API_KEY`,
`ANTHROPIC_API_KEY`) and, optionally, Jira and CI-platform tokens exclusively from
environment variables / CI secret stores. Keys are never written to disk, logged, or
included in the generated review output. Diff content and any repository context files
(`AGENTS.md`, `README.md`, etc.) are sent directly to the LLM provider endpoint you
configure — review your provider's data retention policy before enabling this action on
private repositories.
