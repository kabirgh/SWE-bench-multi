import json
from swebench.harness.constants import TestStatus
from swebench.harness.adapters.javascript_adapter import (
    jest_log_parser as log_parser,
)

if __name__ == "__main__":
    with open("swebench/scripts/test_input.txt", "r") as f:
        log = f.read()

    test_status_map = log_parser(log)
    results = {
        "FAIL_TO_PASS": [
            test
            for test, status in test_status_map.items()
            if status == TestStatus.FAILED.value
        ],
        "PASS_TO_PASS": [
            test
            for test, status in test_status_map.items()
            if status == TestStatus.PASSED.value
        ],
    }
    print(json.dumps(results))
