# If you change the base image, you need to rebuild all images (run with --force_rebuild)
_DOCKERFILE_BASE_JAVASCRIPT = r"""
FROM --platform={platform} {base_image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Install nvm. Instances may later install a different version of node
ENV NVM_DIR /root/.nvm
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash \
    && . $NVM_DIR/nvm.sh

RUN apt update && apt install -y \
wget \
git \
build-essential \
jq \
&& rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_JAVASCRIPT = r"""FROM --platform={platform} {env_image_name}

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
