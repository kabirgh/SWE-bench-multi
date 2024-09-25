from dataclasses import dataclass
import re
from typing import Callable

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


@dataclass(kw_only=True)
class CPlusPlusAdapter(Adapter):
    log_parser: Callable[[str], dict[str, str]]

    @property
    def language(self):
        return "c++"

    @property
    def base_image_name(self):
        """
        Returns:
            str: the "real" base image for the dockerfile, e.g. golang:1.23 or ubuntu:22.04
        """
        return "ubuntu:22.04"  # Reuse the same base image as python

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return self.log_parser


def redis_log_parser(log: str) -> dict[str, str]:
    """
    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    pattern = r"^\[(ok|err)\]:\s(.+?)(?:\s\((\d+\s*m?s)\))?$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name, _duration = match.groups()
            if status == "ok":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "err":
                # Strip out file path information from failed test names
                test_name = re.sub(r"\s+in\s+\S+$", "", test_name)
                test_status_map[test_name] = TestStatus.FAILED.value
            elif status == "skip" or status == "ignore":
                test_status_map[test_name] = TestStatus.SKIPPED.value

    return test_status_map


def redis_cluster_test_log_parser(log: str) -> dict[str, str]:
    """
    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    pattern = r"^\[(ok|err)\]:\s(.+?)(?:\s\((\d+\s*m?s)\))?$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name, _duration = match.groups()
            if status == "ok":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "err":
                # Strip out file path information from failed test names
                test_name = re.sub(r"\s+in\s+\S+$", "", test_name)
                test_status_map[test_name] = TestStatus.FAILED.value
            elif status == "skip" or status == "ignore":
                test_status_map[test_name] = TestStatus.SKIPPED.value

    return test_status_map


def jq_log_parser(log: str) -> dict[str, str]:
    """
    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    pattern = r"^\s*(PASS|FAIL):\s(.+)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name = match.groups()
            if status == "PASS":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "FAIL":
                test_status_map[test_name] = TestStatus.FAILED.value
    return test_status_map
