from collections import defaultdict
import json
from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import (
    tap_log_parser as log_parser,
)

if __name__ == "__main__":
    with open("swebench/scripts/test_input.txt", "r") as f:
        log = f.read()

    test_status_map = log_parser(log)

    results = {
        "FAIL_TO_PASS": [],
        "PASS_TO_PASS": [],
        "FAIL_TO_FAIL": [],
    }

    for test, status in test_status_map.items():
        if status == TestStatus.FAILED.value:
            # only for three.js, should be commented out for other log formats
            if "# TODO" in test:
                results["FAIL_TO_FAIL"].append(test)
            else:
                results["FAIL_TO_PASS"].append(test)
        elif status == TestStatus.PASSED.value:
            results["PASS_TO_PASS"].append(test)

    print(json.dumps(results))
