# AI PR Reviewer

<p align="center">
  <img src="assets/banner.jpg" alt="AI PR Reviewer Banner Logo" width="680" />
</p>

<p align="center">
  <a href="https://github.com/edsoncarlosdevops/ai-pr-reviewer/releases"><img src="https://img.shields.io/github/v/release/edsoncarlosdevops/ai-pr-reviewer?style=for-the-badge&color=6C3FB5" alt="GitHub release"></a>
  <a href="https://github.com/marketplace/actions/ai-pr-reviewer"><img src="https://img.shields.io/badge/Marketplace-AI%20PR%20Reviewer-blue?style=for-the-badge&logo=github" alt="Marketplace"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License"></a>
  <a href="https://github.com/edsoncarlosdevops/ai-pr-reviewer/stargazers"><img src="https://img.shields.io/github/stars/edsoncarlosdevops/ai-pr-reviewer?style=for-the-badge&color=gold" alt="GitHub Stars"></a>
</p>

---

## 📌 Overview & Value Proposition

**AI PR Reviewer** is an enterprise-grade, multi-platform, AI-driven code review engine designed to automate code reviews across GitHub Actions, Azure DevOps, and GitLab CI. 

Unlike simple diff summarizers or proprietary SaaS tools, **AI PR Reviewer** provides an **agnostic, local-first Python CLI engine** powered by **DeepSeek Pro** (or OpenAI / Anthropic). It evaluates git patches against repository-specific guidelines (`AGENTS.md`), architecture specifications, and specialized domain rules (Terraform, ROS 2, Docker, Kubernetes, Python, CI/CD).

### Why AI PR Reviewer over PR-Agent, Qodo, or SaaS Alternatives?

| Feature | AI PR Reviewer | Traditional SaaS Tools | Basic GitHub Actions |
| :--- | :---: | :---: | :---: |
| **Agnostic Core CLI** | ✅ Runs locally, in Docker, or on any CI/CD runner | ❌ Vendor lock-in | ❌ GitHub Actions only |
| **DeepSeek Pro Native** | ✅ $0.003/review (90% cheaper than GPT-4o) | ❌ High subscription fees | ❌ Hardcoded models |
| **Multi-Language Feedback** | ✅ Multilingual output support (EN, PT, ES, FR, DE) | 🟡 English only | ❌ English only |
| **Context Aware (`AGENTS.md`)** | ✅ Ingests internal governance & repository guides | ❌ Requires workspace indexing | ❌ Diff only |
| **Strict Quality Scoring** | ✅ Standardized 0-10 score & explicit emoji severities | 🟡 Varied formatting | ❌ Generic text |
| **Zero Data Leakage** | ✅ Direct API calls to LLM endpoint | ❌ Third-party SaaS storage | 🟡 Direct API |

---

## 🌟 Key Features

- **Multi-Cloud & Infrastructure Native**: Built-in prompts for **Terraform/OpenTofu**, **ROS 2 robotics telemetry**, **Docker multi-stage**, **Kubernetes manifests**, and **GitHub Actions workflows**.
- **Multilingual Feedback Support**: Configurable feedback language output (English, Portuguese, Spanish, French, German) via `.pr_reviewer.toml`.
- **Agnostic Core Architecture**: The core Python engine is decoupled from CI/CD runners. Use it via GitHub Actions, Azure DevOps Pipelines, GitLab CI, or terminal CLI.
- **Cost-Optimized Intelligence**: Uses **DeepSeek V4-Pro** by default (~$0.003 per review with frontier coding capabilities), with standard fallbacks to OpenAI (`gpt-4o`, `gpt-4o-mini`) or Anthropic (`claude-3.5-sonnet`).
- **Operational Risk Assessment**: Identifies missing files, breaking cross-repository dependencies, and unhandled runtime exceptions before merging.
- **Optional Jira Requirements Validation**: Matches PR titles/branches to Jira issues and verifies Acceptance Criteria completion.

---

## 🚀 Quickstart & Integration Guides

### 1. GitHub Actions

Add `.github/workflows/ai-review.yml` to your repository:

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

### 2. Azure DevOps Pipelines

Include the reusable pipeline template in `azure-pipelines.yml`:

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

### 3. GitLab CI

Add the include block to `.gitlab-ci.yml`:

```yaml
include:
  - remote: 'https://raw.githubusercontent.com/edsoncarlosdevops/ai-pr-reviewer/v1/wrappers/gitlab-ci/.ai-review.yml'

variables:
  DEEPSEEK_API_KEY: $DEEPSEEK_API_KEY
  AI_REVIEW_MODEL: "deepseek-chat"
```

### 4. Local CLI / Terminal Execution

```bash
# Clone and install dependencies
git clone https://github.com/edsoncarlosdevops/ai-pr-reviewer.git
cd ai-pr-reviewer
pip install -r requirements.txt

# Export your API Key
export DEEPSEEK_API_KEY="your-deepseek-api-key"

# Generate local git patch and run review
git diff origin/main...HEAD > /tmp/pr.patch
python core/cli.py --diff /tmp/pr.patch --workspace . --output review.md

# View generated review
cat review.md
```

---

## ⚙️ Configuration (`.pr_reviewer.toml`)

Create a `.pr_reviewer.toml` file in the root of your target repository to customize reviewer persona, model provider, and feedback language:

```toml
[reviewer]
name = "AI PR Reviewer"
model = "deepseek-chat"
provider = "deepseek"
severity_threshold = "low"

# Feedback Language Option: "english", "portuguese", "spanish", "french", "german"
# Configures the language in which AI PR Reviewer writes comments and findings.
language = "portuguese"

[context]
# Extra context files to scan alongside AGENTS.md and README.md
extra_context_files = [
  "docs/architecture.md",
  "CONTRIBUTING.md"
]

[jira]
# Set enabled = true to validate PRs against Jira Acceptance Criteria
enabled = false
base_url = "https://your-org.atlassian.net"
```

---

## 📊 Sample Output Preview

```markdown
# 🔍 PR Review — Clark VanScoder

### 📋 Review scope

| Check | Result |
|-------|--------|
| git fetch + diff | `origin/master..HEAD` — 1 commit(s) — edsoncarlosdevops |
| Files touched | `ros2_nodes/drone_telemetry/telemetry/subscriber.py` (+11 / -4) |
| Directories touched | `ros2_nodes/drone_telemetry/telemetry/` |
| DDL / Schema changes | None |
| Runtime / FE / UX code | Runtime ROS 2 telemetry subscriber code |

### 🎫 Jira Context
No Jira ticket linked or Jira integration disabled.

### 📖 Context consulted
- `README.md`
- `prompts/ros2.md`

### 📝 Findings
The PR modifies `odom_callback` in `subscriber.py` to compute instantaneous telemetry frame rate. While rate monitoring is useful, the implementation contains critical runtime flaws that will freeze or crash the telemetry node during swarm operation.

### ⚠️ Issues

🔴 **Critical** — `[ros2_nodes/.../subscriber.py:125]` — Potential `ZeroDivisionError` when computing `rate = 1.0 / dt`. In high-frequency ROS 2 topics (e.g., 100Hz odometry), consecutive frame timestamps can match within nanosecond precision, resulting in `dt = 0`. Wrap this calculation with `if dt > 0:`.

🟠 **High** — `[ros2_nodes/.../subscriber.py:130]` — File handle leak inside ROS 2 subscriber callback. Opening `/tmp/subscriber_debug.log` with `open()` on every incoming message without closing it will exhaust system file descriptors (`EMFILE`) within minutes. Use a logger or managed context manager outside the high-frequency loop.

### 📊 Overall

**Quality Score:** `4.5 / 10` — Unhandled division by zero and file descriptor leak in high-frequency ROS 2 callback.

**Merge Recommendation:** `Request changes` — Fix critical division by zero risk and descriptor leak before merge.

**Evaluator:** `deepseek-chat`
```

---

## 🏷️ Keywords & Search Optimization (SEO)

`ai code review` `github action code review` `deepseek code review` `automated pull request review` `pr agent alternative` `qodo merge alternative` `terraform ai code review` `ros2 ai review` `azure devops ai pr review` `gitlab ci ai review` `iac security scanner` `llm code auditor`

---

## 🤝 Contributing & Star History

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue.

If you find **AI PR Reviewer** helpful, give us a ⭐ on GitHub to support the project!

---

## ⚖️ License

MIT License. Copyright (c) 2026 Edson Carlos. See [LICENSE](LICENSE) for details.
