# If you change the base image, you need to rebuild all images (run with --force_rebuild)
# TODO: don't install mvnd on gradle images. This probably means separating the dockerfiles.
_DOCKERFILE_BASE_JAVA = r"""
FROM --platform={platform} {image_name}

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt update && apt install -y \
wget \
git \
build-essential \
ant \
unzip \
&& rm -rf /var/lib/apt/lists/*

RUN curl -fsSL -o mvnd.zip https://downloads.apache.org/maven/mvnd/1.0.2/maven-mvnd-1.0.2-linux-amd64.zip
RUN unzip mvnd.zip -d /tmp
RUN mv /tmp/maven-mvnd-1.0.2-linux-amd64 /usr/local/mvnd
RUN rm mvnd.zip
RUN rm -rf /tmp/maven-mvnd-1.0.2-linux-amd64

ENV MVND_HOME=/usr/local/mvnd
ENV PATH=$MVND_HOME/bin:$PATH

RUN adduser --disabled-password --gecos 'dog' nonroot
"""

_DOCKERFILE_INSTANCE_JAVA = r"""FROM --platform={platform} {image_name}

COPY ./setup_repo.sh /root/
RUN /bin/bash /root/setup_repo.sh

WORKDIR /testbed/
"""
