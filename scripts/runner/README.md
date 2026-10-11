# GPU runner on Podman

The checks workflow uses the `cuda` label and requires an NVIDIA GPU.
Run `config.cmd` from the `scripts/runner` directory to build and register
`github-runner`. The registration token is short-lived; obtain a fresh one
from the repository's Settings > Actions > Runners page for first setup.

## Restarting

To resume the already-registered runner after Windows logon:

```cmd
podman machine start
podman start github-runner
podman logs --tail 50 github-runner
```

Use Task Scheduler at logon under the same Windows user to automate these
commands. The `--restart=unless-stopped` policy restarts an exited container
but does not boot the Windows Podman machine. Do not run `config.cmd` on each
reboot: it rebuilds and replaces the container.

## Updating the runner or its registration

The `sir-github-runner-data` volume keeps the entire
`/home/runner/actions-runner` directory, including registered credentials
and runner binaries. Podman copies files from an image only when the volume
is initially empty. Consequently, rebuilding the image with an updated
`RUNNER_VERSION` does not replace these persisted binaries; GitHub's runner
self-update mechanism may update them separately.

A change to runner name, labels, group, or work directory does not update an
existing registration. To pick up an image's runner binaries or change these
registration settings, obtain a new registration token, then run:

```cmd
podman stop github-runner
podman rm github-runner
podman volume rm sir-github-runner-data
config.cmd --url https://github.com/HRAshton/series-intro-recognizer --token YOUR_NEW_REGISTRATION_TOKEN
```

This permanently deletes the runner's stored registration and local work
data. If the old runner is no longer present under the same name, remove
its stale record in GitHub's runner settings. Never commit or print tokens.

Persistent self-hosted runners must only execute trusted pull-request code:
untrusted code can access runner-local credentials and GPU host resources.
