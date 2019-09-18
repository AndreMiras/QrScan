# Docker image for installing dependencies on Linux and running tests.
# Build with:
#   docker build --tag=qrscan .
# Run with:
#   docker run qrscan /bin/sh -c 'make test'
# Or for interactive shell:
#   docker run -it --rm qrscan
FROM ubuntu:18.04

ENV USER="user"
ENV HOME_DIR="/home/${USER}"
ENV WORK_DIR="${HOME_DIR}/app"

# configure locale
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

# install system dependencies
RUN apt update -qq > /dev/null && apt install --yes --no-install-recommends \
    build-essential \
    ccache \
    cmake \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libpython3.7-dev \
    libzbar-dev \
    lsb-release \
    make \
    pkg-config \
    python3.7 \
    python3.7-dev \
    sudo \
    virtualenv

# prepare non root env
RUN useradd --create-home --shell /bin/bash ${USER}
# with sudo access and no password
RUN usermod -append --groups sudo ${USER}
RUN echo "%sudo ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

WORKDIR ${WORK_DIR}
COPY . ${WORK_DIR}
RUN chown -R ${USER}:${USER} ${WORK_DIR}
USER ${USER}

RUN make virtualenv
