import argparse
import json
from swebench.harness.constants import TestStatus
from swebench.harness.adapters.cplusplus_adapter import (
    redis_log_parser as log_parser,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test a log parser on a log file.")
    parser.add_argument("test_output", help="Path to the test output file")
    args = parser.parse_args()

    with open(args.test_output, "r") as f:
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
