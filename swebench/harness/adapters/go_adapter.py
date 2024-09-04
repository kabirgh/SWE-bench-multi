from dataclasses import dataclass
import re
from typing import Callable, List, Optional

from swebench.harness.constants import (
    DIFF_MODIFIED_FILE_REGEX,
    SWEbenchInstance,
    TestStatus,
)
from swebench.harness.adapters.adapter import Adapter


@dataclass
class GoAdapter(Adapter):
    version: str
    install: str
    test_cmd: str
    pre_install: Optional[str] = None
    eval_commands: Optional[List[str]] = None

    @property
    def language(self):
        return "go"

    @property
    def base_image_name(self):
        """
        Returns:
            str: the "real" base image for the dockerfile, e.g. golang:1.23 or ubuntu:22.04
        """
        return f"golang:{self.version}"

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
            setup_commands.append(self.install)

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
        """
        commands = []
        # if repo_directory:
        #     commands.append(f"cd {repo_directory}")
        # commands.append("go mod download")
        return commands

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
            self.eval_commands,
            f"git config --global --add safe.directory {repo_directory}",  # for nonroot user
            f"cd {repo_directory}",
            "git status",  # This is just informational, so we have a record
            # "git show",
            f"git diff {base_commit}",
            self.install,
            reset_tests_command,
            apply_test_patch_command,
            self.test_cmd,
            reset_tests_command,  # Revert tests after done, leave the repo in the same state as before
        ]

        # Remove empty commands
        eval_commands = [cmd for cmd in base_eval_commands if cmd]

        return eval_commands

    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        return _log_parser


def _log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with 'go test'

    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    # Pattern to match test result lines
    pattern = r"^--- (PASS|FAIL|SKIP): (.+) \((.+)\)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, test_name, _duration = match.groups()
            if status == "PASS":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "FAIL":
                test_status_map[test_name] = TestStatus.FAILED.value
            elif status == "SKIP":
                test_status_map[test_name] = TestStatus.SKIPPED.value

    return test_status_map
