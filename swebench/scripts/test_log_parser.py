import json
import argparse
from swebench.harness.constants import TestStatus
from swebench.harness.adapters.cplusplus_adapter import redis_log_parser
from swebench.harness.adapters.go_adapter import _log_parser as go_log_parser
from swebench.harness.adapters.rust_adapter import _cargo_log_parser as rust_log_parser


# Map parser names to parser functions
PARSERS = {
    "redis": redis_log_parser,
    "go": go_log_parser,
    "rust": rust_log_parser,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse test logs with specified parser"
    )
    parser.add_argument(
        "-p",
        "--parser",
        choices=PARSERS.keys(),
        help="Specify which log parser to use",
    )
    args = parser.parse_args()

    with open("swebench/scripts/input.txt", "r") as f:
        log = f.read()

    # Use the selected parser
    log_parser = PARSERS[args.parser]
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
