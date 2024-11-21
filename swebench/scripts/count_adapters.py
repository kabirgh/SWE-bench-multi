from collections import defaultdict
import argparse
from swebench.harness.adapters.registry import ADAPTERS


def print_table(data):
    # Find maximum widths for each column
    max_lang_width = max(len(lang) for lang in data.keys())
    max_repo_width = max(len(repo) for repos in data.values() for repo in repos.keys())
    max_count_width = max(
        len(str(count)) for repos in data.values() for count in repos.values()
    )

    # Ensure minimum widths for header
    max_lang_width = max(max_lang_width, len("Language"))
    max_repo_width = max(max_repo_width, len("Repository"))
    max_count_width = max(max_count_width, len("Issue Count"))

    # Print header with dynamic widths
    print(
        f"| {'Language':<{max_lang_width}} | {'Repository':<{max_repo_width}} | {'Issue Count':<{max_count_width}} |"
    )
    print(
        f"|{'-' * (max_lang_width + 2)}|{'-' * (max_repo_width + 2)}|{'-' * (max_count_width + 2)}|"
    )

    # Print rows with dynamic widths
    for language, repos in data.items():
        for repo, count in repos.items():
            print(
                f"| {language:<{max_lang_width}} | {repo:<{max_repo_width}} | {count:<{max_count_width}} |"
            )


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
