FROM python:3.10.12-slim-bullseye

# The installer requires wget (and certificates) to download the release archive
# RUN apt update && apt install -y --no-install-recommends wget unzip ca-certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    ca-certificates \
    git \
    vim \
    build-essential \
    procps \
    dumb-init \
    && apt-get clean && rm -rf /var/lib/apt/lists/* 

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# uv 설치 경로를 PATH에 추가 (기본 설치 위치: /root/.cargo/bin)
ENV PATH="/root/.cargo/bin:$PATH"
WORKDIR /workspaces