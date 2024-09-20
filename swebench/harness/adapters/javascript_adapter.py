from dataclasses import dataclass
import re
from typing import Callable

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


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
    Parser for test logs generated with Jest. Assumes --verbose flag but not
    --json. We could use --json but the test output contains extraneous lines,
    so parsing is not as straightforward.

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
