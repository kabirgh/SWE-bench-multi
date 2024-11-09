# If you change the base image, you need to rebuild all images (run with --force_rebuild)
_DOCKERFILE_BASE_CPLUSPLUS = r"""
FROM --platform={platform} {image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Uncomment deb-src lines. Only works on Ubuntu 22.04 and below
RUN sed -i 's/^# deb-src/deb-src/' /etc/apt/sources.list

# Includes dependencies for all C/C++ projects
RUN apt update && \
    apt install -y wget git build-essential libtool automake autoconf tcl bison flex cmake python3 python3-pip python3-venv python-is-python3 && \
    apt build-dep systemd -y && \
    rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_CPLUSPLUS = r"""FROM --platform={platform} {image_name}

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
