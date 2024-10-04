from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import re
from typing import Callable, List, Optional

from swebench.harness.constants import (
    DIFF_MODIFIED_FILE_REGEX,
    SWEbenchInstance,
    TestStatus,
)


@dataclass(kw_only=True)
class Adapter(ABC):
    test: List[str]
    pre_install: List[str] = field(default_factory=list)
    install: List[str] = field(default_factory=list)
    build: List[str] = field(default_factory=list)
    eval_commands: List[str] = field(default_factory=list)
    dockerfile_key_override: Optional[str] = None
    clone_submodules: bool = True

    @property
    @abstractmethod
    def language(self) -> str:
        pass

    @property
    @abstractmethod
    def base_image_name(self) -> str:
        pass

    @abstractmethod
    def get_log_parser(self) -> Callable[[str], dict[str, str]]:
        pass

    @property
    def dockerfile_key(self) -> str:
        return self.dockerfile_key_override or self.language

    def make_env_script_list(
        self,
        instance: SWEbenchInstance,
        env_name: str,
        repo_directory: Optional[str] = None,
    ):
        """
        Creates the list of commands to set up the environment for testing.
        This is the setup script for the environment image.
        Unlike python, where the dependencies are enumerated and installed in
        the conda environment without downloading the repository, we use a
        generic install command. So we return an empty list here and handle
        environment setup in the instance image, in therepo script list.
        """
        return []

    def make_repo_script_list(
        self, repo: str, repo_directory: str, base_commit: str, _env_name: str
    ):
        """
        Create a list of bash commands to set up the repository for testing.
        This is the setup script for the instance image.
        """
        setup_commands = [
            f"git clone {'--recurse-submodules ' if self.clone_submodules else ''}-o origin https://github.com/{repo} {repo_directory}",
            f"chmod -R 777 {repo_directory}",  # So nonroot user can run tests
            f"cd {repo_directory}",
            f"git reset --hard {base_commit}",
            # Remove the remote so the agent won't see newer commits.
            "git remote remove origin",
        ]
        setup_commands.extend(self.pre_install)
        setup_commands.extend(self.install)
        setup_commands.extend(self.build)
        return setup_commands

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

        return [
            f"cd {repo_directory}",
            *self.eval_commands,
            f"git config --global --add safe.directory {repo_directory}",  # for nonroot user
            f"cd {repo_directory}",
            "git status",  # This is just informational, so we have a record
            # "git show",
            f"git diff {base_commit}",
            reset_tests_command,
            apply_test_patch_command,
            *self.build,
            *self.test,
            reset_tests_command,  # Revert tests after done, leave the repo in the same state as before
        ]


def tap_log_parser(log: str) -> dict[str, str]:
    """
    Parser for test logs generated with TAP

    Args:
        log (str): log content
    Returns:
        dict: test case to test status mapping
    """
    test_status_map = {}

    # Pattern to match TAP result lines
    pattern = r"^(ok|not ok) (\d+) (.+)$"

    for line in log.split("\n"):
        match = re.match(pattern, line.strip())
        if match:
            status, _test_number, test_name = match.groups()
            if status == "ok":
                test_status_map[test_name] = TestStatus.PASSED.value
            elif status == "not ok":
                test_status_map[test_name] = TestStatus.FAILED.value

    return test_status_map
