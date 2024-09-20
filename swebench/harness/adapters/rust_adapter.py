from dataclasses import dataclass
import re
from typing import Callable

from swebench.harness.constants import TestStatus
from swebench.harness.adapters.adapter import Adapter


@dataclass(kw_only=True)
class RustAdapter(Adapter):
    version: str

    @property
    def language(self):
        return "rust"

    @property
    def base_image_name(self):
        """
        Returns:
            str: the "real" base image for the dockerfile, e.g. golang:1.23 or ubuntu:22.04
        """
        return f"rust:{self.version}"

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return _cargo_log_parser


def _cargo_log_parser(log: str) -> dict[str, str]:
    """
    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    pattern = r"^test\s+(\S+)\s+\.\.\.\s+(\w+)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            test_name, outcome = match.groups()
            if outcome == "ok":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif outcome == "FAILED":
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map
