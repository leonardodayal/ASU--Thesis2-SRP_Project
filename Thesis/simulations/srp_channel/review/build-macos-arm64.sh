#!/bin/sh
set -eu

case_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
output_name=${1:-macos-arm64-verification}
image=srp-nga2-review:precal-macos-arm64

mkdir -p "$case_dir/review/output"

docker build \
  --platform linux/arm64 \
  --tag "$image" \
  --file "$case_dir/review/Dockerfile" \
  "$case_dir"

docker run --rm \
  --platform linux/arm64 \
  --entrypoint nga2Adsorption-review \
  --mount "type=bind,source=$case_dir/review/output,target=/work/output" \
  "$image" \
  --output "/work/output/$output_name" \
  --ranks 4
