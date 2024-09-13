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

    # Filter out files with 'test' in the path
    filtered_patch = PatchSet(
        "\n".join(str(file) for file in patch if "test" not in file.path.lower())
    )

    return filtered_patch


def write_patch_to_json(target_file: str, patch: PatchSet, instance_id: str):
    d = {
        "instance_id": instance_id,
        "model_patch": str(patch),
        "model_name_or_path": "gold",
    }

    try:
        with open(target_file, "r+") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
            except json.JSONDecodeError:
                data = []

            data.append(d)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except FileNotFoundError:
        with open(target_file, "w") as f:
            json.dump([d], f, indent=2)


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
    write_patch_to_json(args.target_file, patch, f"{repo_id}-{pr_number}")
