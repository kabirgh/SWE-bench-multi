from dataclasses import dataclass, field
import re
from typing import Callable, List, Optional

from swebench.harness.constants import (
    DIFF_MODIFIED_FILE_REGEX,
    SWEbenchInstance,
    TestStatus,
)
from swebench.harness.adapters.adapter import Adapter


@dataclass
class JavaScriptAdapter(Adapter):
    version: str
    install: List[str]
    test_cmd: str
    log_parser: Callable[[str], dict[str, str]]
    pre_install: Optional[str] = None
    eval_commands: Optional[List[str]] = None
    pre_test_commands: List[str] = field(default_factory=list)

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

    def make_repo_script_list(
        self,
        repo: str,
        repo_directory: str,
        base_commit: str,
        _env_name: str,
    ):
        """
        Create a list of bash commands to set up the repository for testing.
        This is the setup script for the instance image.
        """
        setup_commands = [
            f"git clone -o origin https://github.com/{repo} {repo_directory}",
            f"chmod -R 777 {repo_directory}",  # So nonroot user can run tests
            f"cd {repo_directory}",
            f"git reset --hard {base_commit}",
            # Remove the remote so the agent won't see newer commits.
            "git remote remove origin",
        ]

        # Run pre-install set up if provided
        if self.pre_install:
            for pre_install in self.pre_install:
                setup_commands.append(pre_install)

        if self.install:
            setup_commands.extend(self.install)

        return setup_commands

    def make_env_script_list(
        self,
        instance: SWEbenchInstance,
        env_name: str,
        repo_directory: Optional[str] = None,
    ):
        """
        Creates the list of commands to set up the environment for testing.
        This is the setup script for the environment image.

        This is unused in this adapter since each PR likely has a different set of package versions to install.
        Installation happens in the instance image (make_repo_script_list).
        """
        return []

    def make_eval_script_list(
        self,
        instance: SWEbenchInstance,
        env_name: str,
        repo_directory: str,
        base_commit: str,
        test_patch: str,
    ):
        """
        Applies the test patch and runs the tests.
        """
        HEREDOC_DELIMITER = "EOF_114329324912"
        test_files = re.findall(DIFF_MODIFIED_FILE_REGEX, test_patch)
        # Reset test files to the state they should be in before the patch.
        reset_tests_command = f"git checkout {base_commit} {' '.join(test_files)}"
        apply_test_patch_command = (
            f"git apply -v - <<'{HEREDOC_DELIMITER}'\n{test_patch}\n{HEREDOC_DELIMITER}"
        )

        base_eval_commands = [
            f"cd {repo_directory}",
            *(self.eval_commands or []),
            f"git config --global --add safe.directory {repo_directory}",  # for nonroot user
            f"cd {repo_directory}",
            "git status",  # This is just informational, so we have a record
            # "git show",
            f"git diff {base_commit}",
            reset_tests_command,
            apply_test_patch_command,
            *self.pre_test_commands,
            self.test_cmd,
            reset_tests_command,  # Revert tests after done, leave the repo in the same state as before
        ]

        # Remove empty commands
        eval_commands = [cmd for cmd in base_eval_commands if cmd]

        return eval_commands

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
