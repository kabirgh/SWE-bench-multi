#!/usr/bin/env python3

"""
Given the `<owner/name>` of a GitHub repo, this script writes the raw information for all the repo's PRs to a single `.jsonl` file.
If `prefilter` is supplied, the script fetches only the PRs that resolve an issue and have one of labels in LABELS.
"""

from __future__ import annotations

import argparse
import json
import logging
import os

from datetime import datetime
from dotenv import load_dotenv
from fastcore.xtras import obj2dict
from swebench.collect.utils import Repo
from typing import Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    msg = "Please set the GITHUB_TOKEN environment variable."
    raise ValueError(msg)

# GraphQL API is case-insensitive
BUG_LABELS = [
    "bug",
    "type: bug",
    "type::bug",
    "kind/bug",
    "issue-bug",
    "bug :bug:",
    "bug :lady_beetle:",  # eg https://github.com/caddyserver/caddy
]
EASY_LABELS = ["good first issue", "easy", "good first issue :baby_chick:"]
REGRESSION_LABELS = ["regression", "type: regression"]
FEATURE_LABELS = ["feature", "type: feature", "enhancement", "type: enhancement"]
LABELS = BUG_LABELS + EASY_LABELS + REGRESSION_LABELS + FEATURE_LABELS


def log_all_pulls(
    repo: Repo,
    output: str,
    max_pulls: Optional[int] = None,
    cutoff_date: Optional[str] = None,
) -> None:
    """
    Iterate over all pull requests in a repository and log them to a file

    Args:
        repo (Repo): repository object
        output (str): output file name
    """
    cutoff_date = (
        datetime.strptime(cutoff_date, "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%SZ")
        if cutoff_date is not None
        else None
    )

    with open(output, "w") as file:
        for i_pull, pull in enumerate(repo.get_all_pulls()):
            setattr(pull, "resolved_issues", repo.extract_resolved_issues(pull))
            print(json.dumps(obj2dict(pull)), end="\n", flush=True, file=file)
            if max_pulls is not None and i_pull >= max_pulls:
                break
            if cutoff_date is not None and pull.created_at < cutoff_date:
                break


def log_prefiltered_pulls(
    repo: Repo,
    output: str,
    cutoff_date: Optional[str] = None,
    max_pulls: Optional[int] = None,
) -> None:
    cutoff_date = (
        datetime.strptime(cutoff_date, "%Y%m%d").strftime("%Y-%m-%dT%H:%M:%SZ")
        if cutoff_date is not None
        else None
    )

    with open(output, "w") as file:
        for pull in repo.get_prefiltered_pulls(
            labels=LABELS, cutoff_date=cutoff_date, max_pulls=max_pulls
        ):
            print(json.dumps(pull.to_dict()), end="\n", flush=True, file=file)


def main(
    repo_name: str,
    output: str,
    token: Optional[str] = None,
    max_pulls: Optional[int] = None,
    cutoff_date: Optional[str] = None,
    prefilter: Optional[bool] = False,
):
    """
    Logic for logging all pull requests in a repository

    Args:
        repo_name (str): name of the repository
        output (str): output file name
        token (str, optional): GitHub token
    """
    if token is None:
        token = os.environ.get("GITHUB_TOKEN")
    owner, repo = repo_name.split("/")
    repo = Repo(owner, repo, token=token)
    if prefilter:
        log_prefiltered_pulls(
            repo, output, max_pulls=max_pulls, cutoff_date=cutoff_date
        )
    else:
        log_all_pulls(repo, output, max_pulls=max_pulls, cutoff_date=cutoff_date)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_name", type=str, help="Name of the repository")
    parser.add_argument("output", type=str, help="Output file name")
    parser.add_argument("--token", type=str, help="GitHub token")
    parser.add_argument(
        "--max_pulls", type=int, help="Maximum number of pulls to log", default=None
    )
    parser.add_argument(
        "--cutoff_date",
        type=str,
        help="Cutoff date for PRs to consider in format YYYYMMDD",
        default=None,
    )
    parser.add_argument(
        "--prefilter",
        action="store_true",
        help="If supplied, prefilter pulls to get only those that resolve an issue and have one of the following labels: "
        + ", ".join(LABELS),
    )
    args = parser.parse_args()
    main(**vars(args))
