from dataclasses import dataclass
import re
from typing import Callable
import xml.etree.ElementTree as ET

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


@dataclass(kw_only=True)
class CPlusPlusAdapter(Adapter):
    log_parser: Callable[[str], dict[str, str]]

    @property
    def language(self):
        return "cpp"

    @property
    def starting_image_name(self):
        """
        Returns:
            str: the starting image for the dockerfile, e.g. golang:1.23 or ubuntu:22.04
        """
        return "ubuntu:22.04"

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

    pattern = r"^\[(ok|err|skip|ignore)\]:\s(.+?)(?:\s\((\d+\s*m?s)\))?$"

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


def doctest_log_parser(log: str) -> dict[str, str]:
    """
    Assumes test binary runs with -s -r=xml.
    """
    test_status_map = {}

    # Extract XML content
    start_tag = "<doctest"
    end_tag = "</doctest>"
    start_index = log.find(start_tag)
    end_index = (
        log.find(end_tag, start_index) + len(end_tag) if start_index != -1 else -1
    )

    if start_index != -1 and end_index != -1:
        xml_string = log[start_index:end_index]
        root = ET.fromstring(xml_string)

        for testcase in root.findall(".//TestCase"):
            testcase_name = testcase.get("name")
            for subcase in testcase.findall(".//SubCase"):
                subcase_name = subcase.get("name")
                name = f"{testcase_name} > {subcase_name}"

                expressions = subcase.findall(".//Expression")
                subcase_passed = all(
                    expr.get("success") == "true" for expr in expressions
                )

                if subcase_passed:
                    test_status_map[name] = TestStatus.PASSED.value
                else:
                    test_status_map[name] = TestStatus.FAILED.value

    return test_status_map


def systemd_test_log_parser(log: str) -> dict[str, str]:
    test_status_map = {}
    tests_started = False
    current_test_name = None
    current_test_status = TestStatus.PASSED.value

    test_name_pattern = r"^/\*\s*(.+?)\s*\*/$"
    test_fail_string = "Assertion failed"
    test_logs_ended_string = "Full log written to"

    for line in log.split("\n"):
        if "✀" in line:
            tests_started = True
            continue

        if not tests_started:
            continue

        test_name_match = re.match(test_name_pattern, line.strip())
        # New test
        if test_name_match:
            # Save the status of the previous test
            if current_test_name is not None:
                test_status_map[current_test_name] = current_test_status

            # Get the new test name
            current_test_name = test_name_match.groups()[0]
            # Reset current test status to pass
            current_test_status = TestStatus.PASSED.value
            continue

        # Only set the test status to failed if we see the fail string
        if test_fail_string in line:
            current_test_status = TestStatus.FAILED.value
            continue

        # Save results of the last test
        if test_logs_ended_string in line:
            test_status_map[current_test_name] = current_test_status
            break

    return test_status_map


def micropython_test_log_parser(log: str) -> dict[str, str]:
    test_status_map = {}

    pattern = r"^(pass|FAIL|skip)\s+(.+)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name = match.groups()
            if status == "pass":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "FAIL":
                test_status_map[test_name] = TestStatus.FAILED.value
            elif status == "skip":
                test_status_map[test_name] = TestStatus.SKIPPED.value

    return test_status_map
