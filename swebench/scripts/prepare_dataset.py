from collections import defaultdict
import argparse

# Add argument parsing
parser = argparse.ArgumentParser(
    description="Prepare dataset and create dummy predictions."
)
parser.add_argument(
    "--output_dir",
    type=str,
    default=os.path.join("dataset", "all"),
    help="Output directory for merged instances and dummy predictions",
)
args = parser.parse_args()
# Dictionary to store instance counts for each repo
repo_instance_counts = defaultdict(int)

    if "tokio" in instances_file or "caddy" in instances_file:
        with open(instances_file, "r") as f:
            for line in f:
                # Parse each line as JSON and add to the list
                instance = json.loads(line.strip())
                all_instances.append(instance)
                # Count instances for each repo
                repo_instance_counts[instance["repo"]] += 1
output_dir = args.output_dir
os.makedirs(output_dir, exist_ok=True)
                    "FAIL_TO_PASS": instance["FAIL_TO_PASS"],
                    "PASS_TO_PASS": instance["PASS_TO_PASS"],
# Print the number of instances in each repo file
# print("\nNumber of instances in each repo:")
# for repo, count in repo_instance_counts.items():
#     print(f"{repo}: {count}")

    f"Created predictions file to apply dummy patch: {os.path.join(output_dir, 'dummy_predictions.json')}"