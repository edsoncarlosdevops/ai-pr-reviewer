# AI PR Reviewer

![AI PR Reviewer Logo](assets/logo.jpg)

[![GitHub release](https://img.shields.io/github/v/release/edsoncarlosdevops/ai-pr-reviewer)](https://github.com/edsoncarlosdevops/ai-pr-reviewer/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

AI PR Reviewer is an automated pull request code review tool powered by DeepSeek Pro (OpenAI/Anthropic compatible). It analyzes git diffs, checks context files (`AGENTS.md`, `README.md`), verifies Jira acceptance criteria (when enabled), and generates structured, professional code reviews.

---

## Features

- **Agnostic Core Architecture**: Python CLI core decoupled from CI/CD runners.
- **DeepSeek Pro Default**: Ultra-low cost (~$0.003/review) with frontier model coding intelligence.
- **Multi-Platform Wrappers**: Native integration templates for GitHub Actions, Azure DevOps, and GitLab CI.
- **Context-Aware**: Automatically scans workspace for `AGENTS.md` and repository guidelines.
- **Language Specialist Prompts**: Specialized rule sets for Terraform, Docker, Kubernetes, Python, ROS 2, and GitHub Actions workflows.
- **Optional Jira Integration**: Validates pull requests against Jira acceptance criteria when configured.

---

## Integration Guides

### GitHub Actions

Add the workflow `.github/workflows/ai-review.yml`:

```yaml
name: AI PR Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: edsoncarlosdevops/ai-pr-reviewer@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          deepseek_api_key: ${{ secrets.DEEPSEEK_API_KEY }}
```

### Azure DevOps

Include the pipeline template in `azure-pipelines.yml`:

```yaml
trigger: none
pr:
  branches:
    include:
      - main

resources:
  repositories:
  - repository: ai-reviewer
    type: github
    name: edsoncarlosdevops/ai-pr-reviewer
    ref: refs/tags/v1
    endpoint: github-service-connection

stages:
- template: wrappers/azure-devops/ai-pr-review-template.yml@ai-reviewer
  parameters:
    model_name: deepseek-chat
    deepseek_api_key: $(DEEPSEEK_API_KEY)
```

### GitLab CI

Include the review job in `.gitlab-ci.yml`:

```yaml
include:
  - remote: 'https://raw.githubusercontent.com/edsoncarlosdevops/ai-pr-reviewer/v1/wrappers/gitlab-ci/.ai-review.yml'

variables:
  DEEPSEEK_API_KEY: $DEEPSEEK_API_KEY
  AI_REVIEW_MODEL: "deepseek-chat"
```

### Local CLI

```bash
git clone https://github.com/edsoncarlosdevops/ai-pr-reviewer.git
cd ai-pr-reviewer
pip install -r requirements.txt

export DEEPSEEK_API_KEY="your-api-key"

git diff origin/main...HEAD > /tmp/pr.patch
python core/cli.py --diff /tmp/pr.patch --workspace . --output review.md
```

---

## Configuration (`.pr_reviewer.toml`)

Place a `.pr_reviewer.toml` in your target repository root to customize behavior:

```toml
[reviewer]
name = "AI PR Reviewer"
model = "deepseek-chat"
provider = "deepseek"
severity_threshold = "low"

[context]
extra_context_files = [
  "docs/architecture.md"
]

[jira]
enabled = false
base_url = "https://your-org.atlassian.net"
```

---

## Publishing to GitHub Marketplace

1. Verify `action.yml` is present in the repository root.
2. Tag a release version using semantic versioning (`git tag -a v1.0.0 -m "Release v1.0.0"`).
3. On GitHub, create a new release from the tag and check **"Publish this Action to the GitHub Marketplace"**.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
