param(
    [string]$OutputName = "windows-amd64-verification"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$CaseDir = Split-Path -Parent $PSScriptRoot
$OutputRoot = Join-Path $PSScriptRoot "output"
$Image = "srp-nga2-review:precal-windows-amd64"

New-Item -ItemType Directory -Force -Path $OutputRoot | Out-Null

docker build `
    --platform linux/amd64 `
    --tag $Image `
    --file (Join-Path $PSScriptRoot "Dockerfile") `
    $CaseDir
if ($LASTEXITCODE -ne 0) {
    throw "Docker image build failed with exit code $LASTEXITCODE"
}

docker run --rm `
    --platform linux/amd64 `
    --entrypoint nga2Adsorption-review `
    --mount "type=bind,source=$OutputRoot,target=/work/output" `
    $Image `
    --output "/work/output/$OutputName" `
    --ranks 4
if ($LASTEXITCODE -ne 0) {
    throw "Docker review suite failed with exit code $LASTEXITCODE"
}
