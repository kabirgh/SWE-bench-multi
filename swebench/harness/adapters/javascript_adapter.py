from dataclasses import dataclass
import re
from typing import Callable

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter

JEST_JSON_JQ_TRANSFORM = """jq -r '.testResults[].assertionResults[] | "[" + (.status | ascii_upcase) + "] " + ((.ancestorTitles | join(" > ")) + (if .ancestorTitles | length > 0 then " > " else "" end) + .title)'"""


@dataclass
class JavaScriptAdapter(Adapter):
    version: str
    log_parser: Callable[[str], dict[str, str]]

    @property
    def language(self):
        return "javascript"

    @property
    def base_image_name(self):
        """
        Returns:
            str: the "real" base image for the dockerfile, e.g. golang:1.23 or ubuntu:22.04
        """
        return f"node:{self.version}"

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return self.log_parser


def jest_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with Jest. Assumes --verbose flag.

    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

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


def jest_json_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with Jest. Assumes the --json flag has been
    piped into JEST_JSON_JQ_TRANSFORM. Unlike --verbose, tests with the same name
    in different describe blocks print with different names.
    """
    test_status_map = {}

    pattern = r"^\[(PASSED|FAILED)\]\s(.+)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name = match.groups()
            if status == "PASSED":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "FAILED":
                test_status_map[test_name] = TestStatus.FAILED.value
    return test_status_map


def vitest_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with vitest. Assumes --reporter=verbose flag.
    """
    test_status_map = {}

    pattern = r"^\s*(✓|×|↓)\s(.+?)(?:\s(\d+\s*m?s?|\[skipped\]))?$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status_symbol, test_name, _duration_or_skipped = match.groups()
            if status_symbol == "✓":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status_symbol == "×":
                test_status_map[test_name] = TestStatus.FAILED.value
            elif status_symbol == "↓":
                test_status_map[test_name] = TestStatus.SKIPPED.value
    return test_status_map
