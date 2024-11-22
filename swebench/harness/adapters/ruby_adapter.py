from dataclasses import dataclass
import re
from typing import Callable

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


@dataclass(kw_only=True)
class RubyAdapter(Adapter):
    version: str

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
        return _minitest_log_parser


def _minitest_log_parser(log: str) -> dict[str, str]:
    """
    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    pattern = r"^(.+)\. .*=.*(\.|F).*$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            test_name, outcome = match.groups()
            if outcome == ".":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif outcome == "F":
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map
