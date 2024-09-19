import json
import glob
import os

# Directory containing the repo-specific instance files
input_dir = os.path.join("dataset")
# Print the full input_dir path
print(f"Full input directory path: {os.path.abspath(input_dir)}")

# List to store all instances
all_instances = []

# Find all instances.jsonl files in subdirectories
for instances_file in glob.glob(
    os.path.join(input_dir, "*", "verified", "instances.jsonl")
):
    with open(instances_file, "r") as f:
        for line in f:
            # Parse each line as JSON and add to the list
            instance = json.loads(line.strip())
            all_instances.append(instance)

# Sort instances by repo, then version, to ensure consistent ordering
all_instances.sort(key=lambda x: (x["repo"], x["version"]))

# Output directory
output_dir = os.path.join(input_dir, "all")
output_file = os.path.join(output_dir, "instances.jsonl")
# So python server.py can see it
output_file_all = os.path.join(output_dir, "all-task-instances.jsonl")

# Write all instances to the output file as json
with open(output_file, "w+") as f, open(output_file_all, "w+") as f_all:
    for instance in all_instances:
        # Write selected fields to output_file for uploading to Hugging Face
        f.write(
            json.dumps(
                {
                    "repo": instance["repo"],
                    "instance_id": instance["instance_id"],
                    "base_commit": instance["base_commit"],
                    "patch": instance["patch"],
                    "test_patch": instance["test_patch"],
                    "problem_statement": instance["problem_statement"],
                    "hints_text": instance["hints_text"],
                    "created_at": instance["created_at"],
                    "version": instance["version"],
                    "FAIL_TO_PASS": json.dumps(instance["FAIL_TO_PASS"]),
                    "PASS_TO_PASS": json.dumps(instance["PASS_TO_PASS"]),
                }
            )
            + "\n"
        )
        # Write the entire instance to output_file_all
        f_all.write(json.dumps(instance) + "\n")

print(f"Merged {len(all_instances)} instances into {output_file} and {output_file_all}")
