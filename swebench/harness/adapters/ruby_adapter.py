from dataclasses import dataclass
import re
from typing import Callable

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


@dataclass(kw_only=True)
class RubyAdapter(Adapter):
    version: str
    log_parser: Callable[[str], dict[str, str]]

    @property
    def language(self):
        return "ruby"

    @property
    def starting_image_name(self):
        """
        Returns:
            str: the starting image for the dockerfile, e.g. golang:1.23 or ubuntu:22.04
        """
        return f"ruby:{self.version}"

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return self.log_parser


def minitest_log_parser(log: str) -> dict[str, str]:
    """
    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    pattern = r"^(.+)\. .*=.*(\.|F|E).*$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            test_name, outcome = match.groups()
            if outcome == ".":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif outcome in ["F", "E"]:
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map


def cucumber_log_parser(log: str) -> dict[str, str]:
    """
    Assumes --format progress is used.
    """
    test_status_map = {}

    pattern = r"^(.*) \.+(\.|F)"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            test_name, outcome = match.groups()
            if outcome == ".":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif outcome == "F":
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map


def ruby_unit_log_parser(log: str) -> dict[str, str]:
    test_status_map = {}

    pattern = r"^\s*(?:test: )?(.+):\s+(\.|E\b|F\b|O\b)"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            test_name, outcome = match.groups()
            if outcome == ".":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif outcome in ["E", "F"]:
                test_status_map[test_name] = TestStatus.FAILED.value
            elif outcome == "O":
                test_status_map[test_name] = TestStatus.SKIPPED.value

    return test_status_map
