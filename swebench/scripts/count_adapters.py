from collections import defaultdict
from swebench.harness.adapters.registry import ADAPTERS


if __name__ == "__main__":
    num = 0
    language_counts = defaultdict(int)

    for repo, config in ADAPTERS.items():
        if repo != "scikit-learn/scikit-learn":
            num += len(config)
            for adapter in config.values():
                language_counts[adapter.language] += 1

    for language, count in language_counts.items():
        print(f"{language}: {count}")
    print(f"--- Total: {num} ---")
