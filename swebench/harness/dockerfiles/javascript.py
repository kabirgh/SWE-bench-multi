# If you change the base image, you need to rebuild all images (run with --force_rebuild)
_DOCKERFILE_BASE_JAVASCRIPT = r"""
FROM --platform={platform} {image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
    wget \
    git \
    build-essential \
    jq \
    gnupg \
    ca-certificates \
    apt-transport-https

# Install Chrome for browser testing
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set up Chrome environment variables
ENV CHROME_BIN /usr/bin/google-chrome
ENV CHROME_PATH /usr/bin/google-chrome

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_JAVASCRIPT = r"""FROM --platform={platform} {image_name}

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
