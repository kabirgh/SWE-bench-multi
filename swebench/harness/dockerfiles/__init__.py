from swebench.harness.dockerfiles.go import (
    _DOCKERFILE_BASE_GO,
    _DOCKERFILE_INSTANCE_GO,
)
from swebench.harness.dockerfiles.python import (
    _DOCKERFILE_BASE_PYTHON,
    _DOCKERFILE_ENV_PYTHON,
    _DOCKERFILE_INSTANCE_PYTHON,
)


def get_dockerfile_base(platform: str, arch: str, language: str | None):
    if arch == "arm64":
        conda_arch = "aarch64"
    else:
        conda_arch = arch
    return _dockerfiles[language or "python"]["base"].format(
        platform=platform, conda_arch=conda_arch
    )


def get_dockerfile_env(platform: str, arch: str, language: str | None) -> str | None:
    file = _dockerfiles[language or "python"]["env"]
    if not file:
        return None
    return file.format(platform=platform, arch=arch)


def get_dockerfile_instance(platform: str, env_image_name: str, language: str | None):
    return _dockerfiles[language or "python"]["instance"].format(
        platform=platform, env_image_name=env_image_name
    )


_dockerfiles = {
    "go": {
        "base": _DOCKERFILE_BASE_GO,
        "env": None,  # No env needed for go repos
        "instance": _DOCKERFILE_INSTANCE_GO,
    },
    "python": {
        "base": _DOCKERFILE_BASE_PYTHON,
        "env": _DOCKERFILE_ENV_PYTHON,
        "instance": _DOCKERFILE_INSTANCE_PYTHON,
    },
}
