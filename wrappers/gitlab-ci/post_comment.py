"""
Posts (or updates) the AI PR Reviewer output as a note on a GitLab merge request.

Required environment variables:
  CI_API_V4_URL              - provided automatically by GitLab CI
  CI_PROJECT_ID              - provided automatically by GitLab CI
  CI_MERGE_REQUEST_IID       - provided automatically by GitLab CI (merge request pipelines only)
  GITLAB_TOKEN                - a project/personal access token with 'api' scope, set as a
                                masked CI/CD variable. Falls back to CI_JOB_TOKEN, which only
                                has permission to post notes on GitLab 16.0+ with the
                                "expanded job token permissions" project setting enabled.
"""
import argparse
import os
import sys

import requests

STICKY_TAG = "<!-- ai-pr-reviewer-report -->"


def main() -> int:
    parser = argparse.ArgumentParser(description="Post AI PR Reviewer output to a GitLab merge request")
    parser.add_argument("--review", type=str, required=True, help="Path to the generated review markdown file")
    args = parser.parse_args()

    if not os.path.isfile(args.review):
        print(f"Error: review file not found at {args.review}")
        return 1

    with open(args.review, "r", encoding="utf-8") as f:
        review_body = f.read()

    api_url = os.environ.get("CI_API_V4_URL")
    project_id = os.environ.get("CI_PROJECT_ID")
    mr_iid = os.environ.get("CI_MERGE_REQUEST_IID")

    missing = [
        name
        for name, value in [
            ("CI_API_V4_URL", api_url),
            ("CI_PROJECT_ID", project_id),
            ("CI_MERGE_REQUEST_IID", mr_iid),
        ]
        if not value
    ]
    if missing:
        print(f"Error: missing required environment variables: {', '.join(missing)}")
        print("This step only runs on merge request pipelines (CI_PIPELINE_SOURCE == 'merge_request_event').")
        return 1

    token = os.environ.get("GITLAB_TOKEN")
    headers = {"PRIVATE-TOKEN": token} if token else {"JOB-TOKEN": os.environ.get("CI_JOB_TOKEN", "")}

    notes_url = f"{api_url.rstrip('/')}/projects/{project_id}/merge_requests/{mr_iid}/notes"
    comment_body = f"{STICKY_TAG}\n{review_body}"

    notes_resp = requests.get(notes_url, headers=headers, params={"per_page": 100}, timeout=30)
    notes_resp.raise_for_status()
    notes = notes_resp.json()

    existing_note = next((n for n in notes if STICKY_TAG in (n.get("body") or "")), None)

    if existing_note:
        update_url = f"{notes_url}/{existing_note['id']}"
        resp = requests.put(update_url, headers=headers, json={"body": comment_body}, timeout=30)
    else:
        resp = requests.post(notes_url, headers=headers, json={"body": comment_body}, timeout=30)

    if not resp.ok:
        print(f"Error posting MR note: {resp.status_code} {resp.text}")
        return 1

    print("AI PR Reviewer note posted successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
