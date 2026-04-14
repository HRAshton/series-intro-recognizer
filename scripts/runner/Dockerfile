FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive
ARG RUNNER_VERSION=2.333.1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    jq \
    unzip \
    sudo \
    python3 \
    python3-pip \
    iputils-ping \
    libicu70 \
    libkrb5-3 \
    zlib1g \
    libssl3 \
    liblttng-ust1 \
    libcurl4 \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/runner -s /bin/bash runner \
    && usermod -aG sudo runner \
    && echo "runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

WORKDIR /home/runner

RUN mkdir -p /home/runner/actions-runner \
    && cd /home/runner/actions-runner \
    && curl -fsSL -o actions-runner.tar.gz \
      "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz" \
    && tar -xzf actions-runner.tar.gz \
    && rm actions-runner.tar.gz \
    && ./bin/installdependencies.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh \
    && chown -R runner:runner /home/runner /entrypoint.sh

USER runner
ENV RUNNER_ALLOW_RUNASROOT=0
ENTRYPOINT ["/entrypoint.sh"]
