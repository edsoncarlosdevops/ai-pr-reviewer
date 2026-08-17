"""
CLI entry point.
"""
import argparse
import sys
from pathlib import Path

# Support running both as a script and as a module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.config import load_config
from core.context_loader import ContextLoader
from core.diff_analyzer import DiffAnalyzer
from core.jira_client import JiraClient
from core.llm_client import LLMClient
from core.prompt_builder import PromptBuilder


def main():
    parser = argparse.ArgumentParser(description="AI PR Reviewer")
    parser.add_argument("--diff", type=str, required=True, help="Path to the diff/patch file")
    parser.add_argument("--workspace", type=str, required=True, help="Path to the workspace")
    parser.add_argument("--output", type=str, help="Path to save the review output")
    parser.add_argument("--model", type=str, help="Model to use")
    parser.add_argument("--provider", type=str, help="Provider to use")
    parser.add_argument("--base-url", type=str, help="Base URL for the provider")
    parser.add_argument("--jira", type=str, help="Jira issue key")
    parser.add_argument(
        "--exclude",
        type=str,
        default="",
        help="Comma separated list of glob patterns to exclude from review (e.g. 'tests/**,*.md')",
    )

    args = parser.parse_args()

    workspace_path = Path(args.workspace)
    diff_path = Path(args.diff)

    if not workspace_path.is_dir():
        print(f"Error: Workspace {args.workspace} is not a directory")
        sys.exit(1)

    config = load_config(workspace_path)

    if args.model:
        config.llm.model = args.model
    if args.provider:
        config.llm.provider = args.provider
    if args.base_url:
        config.llm.base_url = args.base_url

    exclude_patterns = [p.strip() for p in args.exclude.split(",") if p.strip()]
    diff_analyzer = DiffAnalyzer(diff_path, exclude_patterns)
    scope = diff_analyzer.analyze()

    context_loader = ContextLoader(workspace_path, config.extra_context_files)
    context_data = context_loader.load_context()

    jira_data = None
    if args.jira and config.jira.enabled:
        jira_client = JiraClient(config.jira)
        jira_data = jira_client.get_issue(args.jira)

    prompt_builder = PromptBuilder(
        scope,
        context_data,
        jira_data,
        model_name=config.llm.model,
        language=config.llm.language
    )
    prompt = prompt_builder.build()

    try:
        llm_client = LLMClient(config.llm)
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    formatted_review = llm_client.generate_review(prompt)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(formatted_review)
        print(f"Review saved to {args.output}")
    else:
        print(formatted_review)

if __name__ == "__main__":
    main()
