# If you change the base image, you need to rebuild all images (run with --force_rebuild)
_DOCKERFILE_BASE_RUBY = r"""
FROM --platform={platform} {image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
wget \
git \
build-essential \
jq \
&& rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_RUBY = r"""FROM --platform={platform} {image_name}

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
