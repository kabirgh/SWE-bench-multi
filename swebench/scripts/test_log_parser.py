import argparse
import json
import re
from swebench.harness.constants import TestStatus


def jest_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with Jest

    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    # Updated pattern to match test result lines without duration
    pattern = r"^\s*(✓|✕|○)\s(.+?)(?:\s\((\d+\s*m?s)\))?$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status_symbol, test_name, _duration = match.groups()
            if status_symbol == "✓":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status_symbol == "✕":
                test_status_map[test_name] = TestStatus.FAILED.value
            elif status_symbol == "○":
                test_status_map[test_name] = TestStatus.SKIPPED.value

    return test_status_map


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test a log parser on a log file.")
    parser.add_argument("test_output", help="Path to the test output file")
    args = parser.parse_args()

    with open(args.test_output, "r") as f:
        log = f.read()

    test_status_map = jest_log_parser(log)
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
