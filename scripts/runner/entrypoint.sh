#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/actions-runner

if [[ ! -f .runner || ! -f .credentials ]]; then
    : "${GITHUB_URL:?GITHUB_URL is required}"
    : "${GITHUB_TOKEN:?GITHUB_TOKEN is required}"

    ./config.sh \
        --unattended \
        --replace \
        --url "$GITHUB_URL" \
        --token "$GITHUB_TOKEN" \
        --name "${RUNNER_NAME:-github-runner}" \
        --work "${RUNNER_WORKDIR:-_work}" \
        --labels "${RUNNER_LABELS:-self-hosted,linux,cuda,gpu}" \
        --runnergroup "${RUNNER_GROUP:-Default}"
fi

exec ./run.sh
