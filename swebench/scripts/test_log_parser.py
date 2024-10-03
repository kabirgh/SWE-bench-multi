import json
from swebench.harness.constants import TestStatus
from swebench.harness.adapters.go_adapter import (
    _log_parser as log_parser,
)

if __name__ == "__main__":
    with open("swebench/scripts/input.txt", "r") as f:
        log = f.read()

    test_status_map = log_parser(log)

    results = {
        "FAIL_TO_PASS": [],
        "PASS_TO_PASS": [],
    }

    for test, status in test_status_map.items():
        if status == TestStatus.FAILED.value:
            results["FAIL_TO_PASS"].append(test)
        elif status == TestStatus.PASSED.value:
            results["PASS_TO_PASS"].append(test)

    print(json.dumps(results))
