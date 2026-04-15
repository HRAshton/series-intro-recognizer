# Usage: ./run-runner-in-podman.ps1 --url https://github.com/HRAshton/series-intro-recognizer --token ABCDEFG
param (
    [string]$urlOpt,
    [string]$url,
    [string]$tokenOpt,
    [string]$token
)

$ErrorActionPreference = 'Stop'

$imageName = "hra-cuda-runner:latest"
$runnerName = "github-runner"

podman build -t $imageName .
Write-Host "Built image $imageName"

Write-Host "Removing any existing container named $runnerName"
try {
    podman stop $runnerName
    podman rm $runnerName
    Write-Host "Removed existing container $runnerName"
} catch {
    Write-Host "No existing container named $runnerName to remove"
}

Write-Host "Running container $runnerName with image $imageName. URL: $url; Token: $token"
podman run `
    --rm -it `
    --name $runnerName `
    --device nvidia.com/gpu=all `
    -e RUNNER_NAME=$runnerName `
    -e GITHUB_URL=$url `
    -e GITHUB_TOKEN=$token `
    -v ${PWD}/entrypoint.sh:/entrypoint.sh `
    $imageName `
    /entrypoint.sh
