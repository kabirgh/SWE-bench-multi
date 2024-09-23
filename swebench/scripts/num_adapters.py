from swebench.harness.adapters.registry import ADAPTERS


if __name__ == "__main__":
    num = 0
    for repo, config in ADAPTERS.items():
        if repo != "scikit-learn/scikit-learn":
            num += len(config)
    print(num)
