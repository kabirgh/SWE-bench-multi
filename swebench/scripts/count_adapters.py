from collections import defaultdict
import argparse
from swebench.harness.adapters.registry import ADAPTERS


def print_table(data):
    # Print header
    print("| Language | Repository | Issue Count |")
    print("|----------|------------|-------------|")

    # Print rows
    for language, repos in data.items():
        for repo, count in repos.items():
            print(f"| {language:<8} | {repo:<38} | {count:<11} |")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Count adapters and optionally display as a table."
    )
    parser.add_argument(
        "--table", action="store_true", help="Display results in a table format"
    )
    args = parser.parse_args()

    num = 0
    language_counts = defaultdict(int)
    table_data = defaultdict(lambda: defaultdict(int))

    for repo, config in ADAPTERS.items():
        if repo != "scikit-learn/scikit-learn":
            repo_count = len(config)
            num += repo_count
            for adapter in config.values():
                language_counts[adapter.language] += 1
                table_data[adapter.language][repo] += 1

    if args.table:
        print_table(table_data)
    else:
        for language, count in language_counts.items():
            print(f"{language}: {count}")

    print(f"--- Total: {num} ---")
