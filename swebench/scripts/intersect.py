import json
import argparse
from typing import Dict, List


def load_jsonl(file_path: str) -> Dict[str, dict]:
    data = {}
    with open(file_path, "r") as f:
        for line in f:
            obj = json.loads(line.strip())
            if "instance_id" in obj:
                data[obj["instance_id"]] = obj
    return data


def intersect_jsonl(file1: str, file2: str) -> List[dict]:
    data1 = load_jsonl(file1)
    data2 = load_jsonl(file2)

    common_ids = set(data1.keys()) & set(data2.keys())
    return [data1[id] for id in common_ids]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Intersect two JSONL files based on instance_id"
    )
    parser.add_argument("file1", help="Path to the first JSONL file")
    parser.add_argument("file2", help="Path to the second JSONL file")
    args = parser.parse_args()

    result = intersect_jsonl(args.file1, args.file2)
    print([r["instance_id"] for r in result])
