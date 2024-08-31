from dataclasses import dataclass
import re
from typing import List, Optional

from swebench.harness.constants import (
    DIFF_MODIFIED_FILE_REGEX,
    MAP_REPO_TO_INSTALL,
    SWEbenchInstance,
)
from swebench.harness.adapters.adapter import Adapter
from swebench.harness.utils import (
    get_environment_yml,
    get_requirements,
    get_test_directives,
)


@dataclass
class PythonAdapter(Adapter):
    python: str
    install: str
    test_cmd: str
    pre_install: Optional[str] = None
    packages: Optional[str] = None
    pip_packages: Optional[List[str]] = None
    no_use_env: bool = False
    eval_commands: Optional[List[str]] = None

    def language(self):
        return "python"

    def make_repo_script_list(
        self,
        repo: str,
        repo_directory: str,
        base_commit: str,
        env_name: str,
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
            # Make sure conda is available for later use
            "source /opt/miniconda3/bin/activate",
            f"conda activate {env_name}",
            'echo "Current environment: $CONDA_DEFAULT_ENV"',
        ]
        if repo in MAP_REPO_TO_INSTALL:
            setup_commands.append(MAP_REPO_TO_INSTALL[repo])

        # Run pre-install set up if provided
        if self.pre_install:
            for pre_install in self.pre_install:
                setup_commands.append(pre_install)

        if self.install:
            setup_commands.append(self.install)
        return setup_commands

    def make_env_script_list(self, instance: SWEbenchInstance, env_name: str):
        """
        Creates the list of commands to set up the conda environment for testing.
        This is the setup script for the environment image.
        """
        HEREDOC_DELIMITER = "EOF_59812759871"
        reqs_commands = [
            "source /opt/miniconda3/bin/activate",
        ]
        # Create conda environment according to install instructinos
        pkgs = self.packages
        if pkgs == "requirements.txt":
            # Create environment
            cmd = f"conda create -n {env_name} python={self.python} -y"
            reqs_commands.append(cmd)

            # Install dependencies
            reqs = get_requirements(instance)
            path_to_reqs = "$HOME/requirements.txt"
            reqs_commands.append(
                f"cat <<'{HEREDOC_DELIMITER}' > {path_to_reqs}\n{reqs}\n{HEREDOC_DELIMITER}"
            )
            cmd = (
                f"conda activate {env_name} && python -m pip install -r {path_to_reqs}"
            )
            reqs_commands.append(cmd)
            reqs_commands.append(f"rm {path_to_reqs}")
        elif pkgs == "environment.yml":
            # Create environment from yml
            reqs = get_environment_yml(instance, env_name)
            path_to_reqs = "environment.yml"
            reqs_commands.append(
                f"cat <<'{HEREDOC_DELIMITER}' > {path_to_reqs}\n{reqs}\n{HEREDOC_DELIMITER}"
            )
            if self.no_use_env:
                # `conda create` based installation
                cmd = (
                    f"conda create -c conda-forge -n {env_name} python={self.python} -y"
                )
                reqs_commands.append(cmd)

                # Install dependencies
                cmd = f"conda env update -f {path_to_reqs}"
                reqs_commands.append(cmd)
            else:
                # `conda env create` based installation
                cmd = f"conda env create --file {path_to_reqs}"
                reqs_commands.append(cmd)

                cmd = f"conda activate {env_name} && conda install python={self.python} -y"
                reqs_commands.append(cmd)

            # Remove environment.yml
            reqs_commands.append(f"rm {path_to_reqs}")
        else:
            # Create environment + install dependencies
            cmd = f"conda create -n {env_name} python={self.python} {pkgs} -y"
            reqs_commands.append(cmd)

        reqs_commands.append(f"conda activate {env_name}")

        # Install additional packages if specified
        if self.pip_packages:
            pip_packages = " ".join(self.pip_packages)
            cmd = f"python -m pip install {pip_packages}"
            reqs_commands.append(cmd)
        return reqs_commands

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
        test_command = " ".join(
            [
                self.test_cmd,
                *get_test_directives(instance),
            ]
        )
        eval_commands = [
            "source /opt/miniconda3/bin/activate",
            f"conda activate {env_name}",
            f"cd {repo_directory}",
        ]
        if self.eval_commands:
            eval_commands += self.eval_commands
        eval_commands += [
            f"git config --global --add safe.directory {repo_directory}",  # for nonroot user
            f"cd {repo_directory}",
            # This is just informational, so we have a record
            "git status",
            "git show",
            f"git diff {base_commit}",
            "source /opt/miniconda3/bin/activate",
            f"conda activate {env_name}",
        ]
        if self.install:
            eval_commands.append(self.install)
        eval_commands += [
            reset_tests_command,
            apply_test_patch_command,
            test_command,
            reset_tests_command,  # Revert tests after done, leave the repo in the same state as before
        ]
        return eval_commands
