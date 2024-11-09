import json
from collections import defaultdict


def find_duplicate_instance_ids(file_path):
    instance_id_count = defaultdict(int)
    duplicate_ids = set()

    with open(file_path, "r") as file:
        for line in file:
            try:
                data = json.loads(line)
                instance_id = data.get("instance_id")
                if instance_id:
                    instance_id_count[instance_id] += 1
                    if instance_id_count[instance_id] > 1:
                        duplicate_ids.add(instance_id)
            except json.JSONDecodeError:
                print(f"Warning: Invalid JSON in line: {line.strip()}")

    return duplicate_ids


def main():
    file_path = "claudesonnet3.5_all_preds.jsonl"
    duplicate_ids = find_duplicate_instance_ids(file_path)

    if duplicate_ids:
        print("The following instance_ids appear more than once:")
        for instance_id in duplicate_ids:
            print(instance_id)
    else:
        print("No duplicate instance_ids found.")


if __name__ == "__main__":
    main()
