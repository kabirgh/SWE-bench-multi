from abc import ABC, abstractmethod
from typing import List

from swebench.harness.constants import SWEbenchInstance


class Adapter(ABC):
    @property
    @abstractmethod
    def language(self) -> str:
        pass

    @abstractmethod
    def make_repo_script_list(
        self,
        repo: str,
        repo_directory: str,
        base_commit: str,
        env_name: str,
    ) -> List[str]:
        pass

    @abstractmethod
    def make_env_script_list(
        self,
        instance: SWEbenchInstance,
        env_name: str,
    ) -> List[str]:
        pass

    @abstractmethod
    def make_eval_script_list(
        self,
        instance: SWEbenchInstance,
        env_name: str,
        repo_directory: str,
        base_commit: str,
        test_patch: str,
    ) -> List[str]:
        pass
