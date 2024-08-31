"""
Write to a jsonl file in the given format for a given patch
```json
{
    "instance_id": "<Unique task instance ID>",
    "model_patch": "<.patch file content string>",
    "model_name_or_path": "<Model name here (i.e. SWE-Llama-13b)>",
}
```
"""

import requests
import json
import argparse
from urllib.parse import urlparse
from unidiff import PatchSet, PatchedFile


def extract_pr_info(url: str):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip("/").split("/")
    return f"{path_parts[0]}__{path_parts[1]}", path_parts[-1]


def make_patch(url: str):
    response = requests.get(url)
    response.raise_for_status()
    patch = PatchSet(response.text)
    return patch[0]


def write_patch_to_jsonl(target_file: str, patch: PatchedFile, instance_id: str):
    d = {
        "instance_id": instance_id,
        "model_patch": str(patch),
        "model_name_or_path": "fake_model",
    }
    with open(target_file, "w+") as f:
        f.write(json.dumps([d]) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a patch file from a GitHub PR URL."
    )
    parser.add_argument("url", help="GitHub PR URL")
    parser.add_argument("target_file", help="File to write patch to")
    args = parser.parse_args()

    repo_id, pr_number = extract_pr_info(args.url)
    patch_url = args.url + ".patch"

    patch = make_patch(patch_url)
    write_patch_to_jsonl(args.target_file, patch, f"{repo_id}-{pr_number}")
