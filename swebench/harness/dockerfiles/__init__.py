from swebench.harness.dockerfiles.cplusplus import (
    _DOCKERFILE_BASE_CPLUSPLUS,
    _DOCKERFILE_INSTANCE_CPLUSPLUS,
)
from swebench.harness.dockerfiles.go import (
    _DOCKERFILE_BASE_GO,
    _DOCKERFILE_INSTANCE_GO,
)
from swebench.harness.dockerfiles.java import (
    _DOCKERFILE_BASE_JAVA,
    _DOCKERFILE_INSTANCE_JAVA,
)
from swebench.harness.dockerfiles.javascript import (
    _DOCKERFILE_BASE_JAVASCRIPT,
    _DOCKERFILE_INSTANCE_JAVASCRIPT,
)
from swebench.harness.dockerfiles.python import (
    _DOCKERFILE_BASE_PYTHON,
    _DOCKERFILE_ENV_PYTHON,
    _DOCKERFILE_INSTANCE_PYTHON,
)
from swebench.harness.dockerfiles.rust import (
    _DOCKERFILE_BASE_RUST,
    _DOCKERFILE_INSTANCE_RUST,
)


def get_dockerfile_base(
    platform: str,
    arch: str,
    dockerfile_key: str | None,
    base_image_name: str | None,
):
    if arch == "arm64":
        conda_arch = "aarch64"
    else:
        conda_arch = arch

    if not base_image_name:
        base_image_name = "ubuntu:22.04"

    print(f"Getting dockerfile base for {dockerfile_key} on {platform} {arch}")
    return _dockerfiles[dockerfile_key or "python"]["base"].format(
        platform=platform, conda_arch=conda_arch, base_image_name=base_image_name
    )


def get_dockerfile_env(
    platform: str, arch: str, dockerfile_key: str | None, base_image_name: str | None
) -> str:
    if not base_image_name:
        base_image_name = "ubuntu:22.04"

    return _dockerfiles[dockerfile_key or "python"]["env"].format(
        platform=platform,
        arch=arch,
        dockerfile_key=dockerfile_key,
        base_image_name=base_image_name,
    )


def get_dockerfile_instance(
    platform: str, env_image_name: str, dockerfile_key: str | None
):
    return _dockerfiles[dockerfile_key or "python"]["instance"].format(
        platform=platform, env_image_name=env_image_name
    )


_dockerfiles = {
    "python": {
        "base": _DOCKERFILE_BASE_PYTHON,
        "env": _DOCKERFILE_ENV_PYTHON,
        "instance": _DOCKERFILE_INSTANCE_PYTHON,
    },
    "go": {
        "base": _DOCKERFILE_BASE_GO,
        # No env needed for go repos, return base since rest of code expects env to be built
        "env": _DOCKERFILE_BASE_GO,
        "instance": _DOCKERFILE_INSTANCE_GO,
    },
    "java": {
        "base": _DOCKERFILE_BASE_JAVA,
        "env": _DOCKERFILE_BASE_JAVA,  # Skip env
        "instance": _DOCKERFILE_INSTANCE_JAVA,
    },
    "javascript": {
        "base": _DOCKERFILE_BASE_JAVASCRIPT,
        "env": _DOCKERFILE_BASE_JAVASCRIPT,  # Skip env
        "instance": _DOCKERFILE_INSTANCE_JAVASCRIPT,
    },
    "c++": {
        "base": _DOCKERFILE_BASE_CPLUSPLUS,
        "env": _DOCKERFILE_BASE_CPLUSPLUS,  # Skip env
        "instance": _DOCKERFILE_INSTANCE_CPLUSPLUS,
    },
    "rust": {
        "base": _DOCKERFILE_BASE_RUST,
        "env": _DOCKERFILE_BASE_RUST,  # Skip env
        "instance": _DOCKERFILE_INSTANCE_RUST,
    },
}
