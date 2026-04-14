#!/usr/bin/env bash
set -euo pipefail

cd /home/runner/actions-runner

: "${GITHUB_URL:?Set GITHUB_URL to your repo/org/enterprise URL}"
: "${GITHUB_TOKEN:?Set GITHUB_TOKEN to a registration token}"
RUNNER_NAME="${RUNNER_NAME:-$(hostname)}"
RUNNER_WORKDIR="${RUNNER_WORKDIR:-_work}"
RUNNER_LABELS="${RUNNER_LABELS:-self-hosted,linux,cuda,gpu}"
RUNNER_GROUP="${RUNNER_GROUP:-Default}"

cleanup() {
  if [[ -f .runner ]]; then
    echo "Removing runner registration..."
    ./config.sh remove --unattended --token "${GITHUB_TOKEN}" || true
  fi
}
trap cleanup EXIT INT TERM

./config.sh \
  --unattended \
  --replace \
  --url "${GITHUB_URL}" \
  --token "${GITHUB_TOKEN}" \
  --name "${RUNNER_NAME}" \
  --work "${RUNNER_WORKDIR}" \
  --labels "${RUNNER_LABELS}" \
  --runnergroup "${RUNNER_GROUP}"

exec ./run.sh
