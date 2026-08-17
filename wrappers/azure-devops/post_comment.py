"""
Posts (or updates) the AI PR Reviewer output as a comment thread on an Azure DevOps pull request.

Required environment variables (all provided automatically by Azure Pipelines,
except SYSTEM_ACCESSTOKEN which must be explicitly forwarded from the pipeline):
  SYSTEM_ACCESSTOKEN            - OAuth token for the build (enable "Allow scripts to
                                   access the OAuth token" or pass $(System.AccessToken))
  SYSTEM_COLLECTIONURI          - e.g. https://dev.azure.com/my-org/
  SYSTEM_TEAMPROJECT            - project name
  BUILD_REPOSITORY_ID           - repository id
  SYSTEM_PULLREQUEST_PULLREQUESTID - pull request id
"""
import argparse
import os
import sys

import requests

STICKY_TAG = "<!-- ai-pr-reviewer-report -->"
API_VERSION = "7.1"


def main() -> int:
    parser = argparse.ArgumentParser(description="Post AI PR Reviewer output to an Azure DevOps PR")
    parser.add_argument("--review", type=str, required=True, help="Path to the generated review markdown file")
    args = parser.parse_args()

    if not os.path.isfile(args.review):
        print(f"Error: review file not found at {args.review}")
        return 1

    with open(args.review, "r", encoding="utf-8") as f:
        review_body = f.read()

    token = os.environ.get("SYSTEM_ACCESSTOKEN")
    collection_uri = os.environ.get("SYSTEM_COLLECTIONURI")
    project = os.environ.get("SYSTEM_TEAMPROJECT")
    repo_id = os.environ.get("BUILD_REPOSITORY_ID")
    pr_id = os.environ.get("SYSTEM_PULLREQUEST_PULLREQUESTID")

    missing = [
        name
        for name, value in [
            ("SYSTEM_ACCESSTOKEN", token),
            ("SYSTEM_COLLECTIONURI", collection_uri),
            ("SYSTEM_TEAMPROJECT", project),
            ("BUILD_REPOSITORY_ID", repo_id),
            ("SYSTEM_PULLREQUEST_PULLREQUESTID", pr_id),
        ]
        if not value
    ]
    if missing:
        print(f"Error: missing required environment variables: {', '.join(missing)}")
        print("This step only runs meaningfully on pull request triggered builds.")
        return 1

    base_url = (
        f"{collection_uri.rstrip('/')}/{project}/_apis/git/repositories/"
        f"{repo_id}/pullRequests/{pr_id}/threads"
    )
    auth = ("", token)
    comment_body = f"{STICKY_TAG}\n{review_body}"

    threads_resp = requests.get(base_url, params={"api-version": API_VERSION}, auth=auth, timeout=30)
    threads_resp.raise_for_status()
    threads = threads_resp.json().get("value", [])

    existing_thread_id = None
    for thread in threads:
        for comment in thread.get("comments", []):
            if STICKY_TAG in (comment.get("content") or ""):
                existing_thread_id = thread.get("id")
                break
        if existing_thread_id:
            break

    if existing_thread_id:
        comment_url = f"{base_url}/{existing_thread_id}/comments"
        resp = requests.post(
            comment_url,
            params={"api-version": API_VERSION},
            auth=auth,
            json={"content": comment_body, "commentType": 1},
            timeout=30,
        )
    else:
        resp = requests.post(
            base_url,
            params={"api-version": API_VERSION},
            auth=auth,
            json={
                "comments": [{"content": comment_body, "commentType": 1}],
                "status": 1,
            },
            timeout=30,
        )

    if not resp.ok:
        print(f"Error posting PR comment: {resp.status_code} {resp.text}")
        return 1

    print("AI PR Reviewer comment posted successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
