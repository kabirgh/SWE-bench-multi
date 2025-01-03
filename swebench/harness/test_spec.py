import hashlib
import json
import platform
import re

from dataclasses import dataclass
from typing import Any, Optional, Union, cast

from swebench.harness.adapters.adapter import Adapter
from swebench.harness.adapters.registry import ADAPTERS
from swebench.harness.constants import (
    DIFF_MODIFIED_FILE_REGEX,
    SWEbenchInstance,
    KEY_INSTANCE_ID,
    FAIL_TO_PASS,
    PASS_TO_PASS,
    MAP_REPO_TO_INSTALL,
    MAP_REPO_VERSION_TO_SPECS,
    USE_X86,
)
from swebench.harness.dockerfiles import (
    get_dockerfile_base,
    get_dockerfile_env,
    get_dockerfile_instance,
)
from swebench.harness.utils import (
    get_requirements,
    get_environment_yml,
    get_test_directives,
)


@dataclass
class TestSpec:
    """
    A dataclass that represents a test specification for a single instance of SWE-bench.
    """

    instance_id: str
    repo: str
    version: str
    repo_script_list: list[str]
    eval_script_list: list[str]
    env_script_list: list[str]
    arch: str
    FAIL_TO_PASS: list[str]
    PASS_TO_PASS: list[str]
    adapter: Optional[Adapter] = None

    @property
    def setup_env_script(self):
        return (
            "\n".join(["#!/bin/bash", "set -euxo pipefail"] + self.env_script_list)
            + "\n"
        )

    @property
    def eval_script(self):
        return (
            "\n".join(["#!/bin/bash", "set -uxo pipefail"] + self.eval_script_list)
            + "\n"
        )
        # Don't exit early because we need to revert tests at the end

    @property
    def install_repo_script(self):
        return (
            "\n".join(["#!/bin/bash", "set -euxo pipefail"] + self.repo_script_list)
            + "\n"
        )

    def adapter_common_key(self):
        if self.adapter:
            return f"{self.adapter.starting_image_name.replace(':', '_')}.{self.adapter.dockerfile_key}"
        raise ValueError("Adapter not found")

    @property
    def base_image_key(self):
        if self.adapter:
            return f"sweb.base.{self.arch}.{self.adapter_common_key()}:latest"
        return f"sweb.base.{self.arch}:latest"

    @property
    def env_image_key(self):
        """
        The key for the environment image is based on the hash of the environment script list.
        If the environment script list changes, the image will be rebuilt automatically.

        Note that old images are not automatically deleted, so consider cleaning up old images periodically.
        """
        hash_object = hashlib.sha256()
        hash_object.update(str(self.env_script_list).encode("utf-8"))
        hash_value = hash_object.hexdigest()
        val = hash_value[:22]  # 22 characters is still very likely to be unique

        if self.adapter:
            return f"sweb.env.{self.arch}.{self.adapter_common_key()}.{val}:latest"
        return f"sweb.env.{self.arch}.{val}:latest"

    @property
    def instance_image_key(self):
        if self.adapter:
            return f"sweb.eval.{self.arch}.{self.adapter_common_key()}.{self.instance_id}:latest"
        return f"sweb.eval.{self.arch}.{self.instance_id}:latest"

    def get_instance_container_name(self, run_id=None):
        name = f"sweb.eval.{self.instance_id}"
        if self.adapter:
            name = (
                f"sweb.eval.{self.arch}.{self.adapter_common_key()}.{self.instance_id}"
            )
        if run_id:
            name = f"{name}.{self.instance_id}"
        return name

    # This code is pretty messy, hard to follow what strings are used for what.
    @property
    def base_dockerfile(self) -> str:
        return get_dockerfile_base(
            platform=self.platform,
            arch=self.arch,
            dockerfile_key=self.adapter.dockerfile_key if self.adapter else None,
            starting_image_name=self.adapter.starting_image_name
            if self.adapter
            else None,
        )

    @property
    def env_dockerfile(self) -> str:
        return get_dockerfile_env(
            platform=self.platform,
            arch=self.arch,
            dockerfile_key=self.adapter.dockerfile_key if self.adapter else None,
            base_image_name=self.base_image_key,
            starting_image_name=self.adapter.starting_image_name
            if self.adapter
            else None,
        )

    @property
    def instance_dockerfile(self) -> str:
        return get_dockerfile_instance(
            platform=self.platform,
            dockerfile_key=self.adapter.dockerfile_key if self.adapter else None,
            env_image_name=self.env_image_key,
        )

    @property
    def platform(self):
        if self.arch == "x86_64":
            return "linux/x86_64"
        elif self.arch == "arm64":
            return "linux/arm64/v8"
        else:
            raise ValueError(f"Invalid architecture: {self.arch}")


def get_test_specs_from_dataset(
    dataset: Union[list[SWEbenchInstance], list[TestSpec]],
) -> list[TestSpec]:
    """
    Idempotent function that converts a list of SWEbenchInstance objects to a list of TestSpec objects.
    """
    if isinstance(dataset[0], TestSpec):
        return cast(list[TestSpec], dataset)
    return list(map(make_test_spec, cast(list[SWEbenchInstance], dataset)))


def make_repo_script_list(specs, repo, repo_directory, base_commit, env_name):
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
    if "pre_install" in specs:
        for pre_install in specs["pre_install"]:
            setup_commands.append(pre_install)

    if "install" in specs:
        setup_commands.append(specs["install"])
    return setup_commands


def make_env_script_list(instance, specs, env_name):
    """
    Creates the list of commands to set up the conda environment for testing.
    This is the setup script for the environment image.
    """
    HEREDOC_DELIMITER = "EOF_59812759871"
    reqs_commands = [
        "source /opt/miniconda3/bin/activate",
    ]
    # Create conda environment according to install instructinos
    pkgs = specs.get("packages", "")
    if pkgs == "requirements.txt":
        # Create environment
        cmd = f"conda create -n {env_name} python={specs['python']} -y"
        reqs_commands.append(cmd)

        # Install dependencies
        reqs = get_requirements(instance)
        path_to_reqs = "$HOME/requirements.txt"
        reqs_commands.append(
            f"cat <<'{HEREDOC_DELIMITER}' > {path_to_reqs}\n{reqs}\n{HEREDOC_DELIMITER}"
        )
        cmd = f"conda activate {env_name} && python -m pip install -r {path_to_reqs}"
        reqs_commands.append(cmd)
        reqs_commands.append(f"rm {path_to_reqs}")
    elif pkgs == "environment.yml":
        # Create environment from yml
        reqs = get_environment_yml(instance, env_name)
        path_to_reqs = "environment.yml"
        reqs_commands.append(
            f"cat <<'{HEREDOC_DELIMITER}' > {path_to_reqs}\n{reqs}\n{HEREDOC_DELIMITER}"
        )
        if "no_use_env" in specs and specs["no_use_env"]:
            # `conda create` based installation
            cmd = (
                f"conda create -c conda-forge -n {env_name} python={specs['python']} -y"
            )
            reqs_commands.append(cmd)

            # Install dependencies
            cmd = f"conda env update -f {path_to_reqs}"
            reqs_commands.append(cmd)
        else:
            # `conda env create` based installation
            cmd = f"conda env create --file {path_to_reqs}"
            reqs_commands.append(cmd)

            cmd = f"conda activate {env_name} && conda install python={specs['python']} -y"
            reqs_commands.append(cmd)

        # Remove environment.yml
        reqs_commands.append(f"rm {path_to_reqs}")
    else:
        # Create environment + install dependencies
        cmd = f"conda create -n {env_name} python={specs['python']} {pkgs} -y"
        reqs_commands.append(cmd)

    reqs_commands.append(f"conda activate {env_name}")

    # Install additional packages if specified
    if "pip_packages" in specs:
        pip_packages = " ".join(specs["pip_packages"])
        cmd = f"python -m pip install {pip_packages}"
        reqs_commands.append(cmd)
    return reqs_commands


def make_eval_script_list(
    instance, specs, env_name, repo_directory, base_commit, test_patch
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
            MAP_REPO_VERSION_TO_SPECS[instance["repo"]][instance["version"]][
                "test_cmd"
            ],
            *get_test_directives(instance),
        ]
    )
    eval_commands = [
        "source /opt/miniconda3/bin/activate",
        f"conda activate {env_name}",
        f"cd {repo_directory}",
    ]
    if "eval_commands" in specs:
        eval_commands += specs["eval_commands"]
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
    if "install" in specs:
        eval_commands.append(specs["install"])
    eval_commands += [
        reset_tests_command,
        apply_test_patch_command,
        test_command,
        reset_tests_command,  # Revert tests after done, leave the repo in the same state as before
    ]
    return eval_commands


def make_test_spec(instance: SWEbenchInstance) -> TestSpec:
    if isinstance(instance, TestSpec):
        return instance
    instance_id = instance[KEY_INSTANCE_ID]
    repo = instance["repo"]
    version = instance["version"]
    base_commit = instance["base_commit"]
    problem_statement = instance["problem_statement"]
    hints_text = instance["hints_text"]  # Unused
    test_patch = instance["test_patch"]

    def _from_json_or_obj(key: str) -> Any:
        """If key points to string, load with json"""
        if isinstance(instance[key], str):
            return json.loads(instance[key])
        return instance[key]

    pass_to_pass = _from_json_or_obj(PASS_TO_PASS)
    fail_to_pass = _from_json_or_obj(FAIL_TO_PASS)

    env_name = "testbed"
    repo_directory = f"/{env_name}"

    if repo in ADAPTERS:
        adapter = ADAPTERS[repo][version]
        repo_script_list = adapter.make_repo_script_list(
            repo, repo_directory, base_commit, env_name
        )
        env_script_list = adapter.make_env_script_list(instance, env_name)
        eval_script_list = adapter.make_eval_script_list(
            instance, env_name, repo_directory, base_commit, test_patch
        )
    else:
        specs = MAP_REPO_VERSION_TO_SPECS[repo][version]

        repo_script_list = make_repo_script_list(
            specs, repo, repo_directory, base_commit, env_name
        )
        env_script_list = make_env_script_list(instance, specs, env_name)
        eval_script_list = make_eval_script_list(
            instance, specs, env_name, repo_directory, base_commit, test_patch
        )

    if platform.machine() in {"aarch64", "arm64"}:
        # use arm64 unless explicitly specified
        arch = "arm64" if instance_id not in USE_X86 else "x86_64"
    else:
        arch = "x86_64"

    return TestSpec(
        instance_id=instance_id,
        repo=repo,
        env_script_list=env_script_list,
        repo_script_list=repo_script_list,
        eval_script_list=eval_script_list,
        version=version,
        arch=arch,
        FAIL_TO_PASS=fail_to_pass,
        PASS_TO_PASS=pass_to_pass,
        adapter=adapter,
    )
