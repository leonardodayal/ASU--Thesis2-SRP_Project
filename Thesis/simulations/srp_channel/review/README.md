# Pre-Calibration Docker Review Package

This package compiles and runs the thesis-owned NGA2 airflow case in a reproducible Linux container. It is intended for numerical and code review before experimental calibration.

> **Important:** every bundled geometry dimension and porous-resistance coefficient is provisional or synthetic. The image does not provide a validated SRP pressure-drop prediction, bead model, or CO2-adsorption result.

## Reproducibility boundary

- NGA2 is fetched from `https://github.com/desjardi/NGA2.git` at commit `28a58d937af89dd506456048be1cad58f6d383a9`.
- The builder uses Ubuntu 24.04, GNU Fortran, Open MPI, and FFTW from the Ubuntu repositories.
- The review build removes NGA2's `-ffast-math` flag so non-finite values retain IEEE behavior and cannot be optimized past the automated checks. On `linux/arm64`, it also removes the unconditional `-lquadmath` linker flag because Ubuntu does not publish an arm64 quadmath runtime and this double-precision case does not use quadmath. The pinned source itself is otherwise unchanged.
- Only the compiled executable, Python 3, Open MPI runtime, FFTW runtime, launcher, and short review cases enter the final image.
- Existing host executables, build products, long-run evidence, and Ensight fields are excluded from the Docker context.

Ubuntu provides the required packages for both `linux/amd64` and `linux/arm64`, and NGA2 is compiled from source for the selected platform. A platform is supported only after the image builds and the review suite passes on that platform; see the verified-platform section below.

## Build

Run from `Thesis/simulations/srp_channel`:

```sh
docker build \
  --platform linux/arm64 \
  --tag srp-nga2-review:precal \
  --file review/Dockerfile \
  .
```

Use `--platform linux/amd64` on an x86-64 host or when the local Docker installation has working amd64 emulation. The pinned NGA2 repository and commit can be overridden with build arguments for controlled experiments, but such an image is no longer the reviewed build.

When cross-building under QEMU, use one compiler job to avoid emulator/compiler resource failures:

```sh
docker buildx build \
  --platform linux/amd64 \
  --build-arg BUILD_JOBS=1 \
  --load \
  --tag srp-nga2-review:precal-amd64 \
  --file review/Dockerfile \
  .
```

## Run a configuration

The image entrypoint is:

```text
nga2Adsorption --config CONFIG --output OUTPUT --ranks N
```

The launcher rejects an existing output directory and rejects a rank count that differs from the input file's `Partition` product. It uses Open MPI's TCP transport for consistent native and emulated container behavior, copies the input into the output directory, and records hashes, platform, rank count, command, provisional-status notice, and return code in `manifest.json`.

Example using the bundled smoke input and a host-mounted output directory:

```sh
mkdir -p review/output
docker run --rm \
  --platform linux/arm64 \
  --volume "$PWD/review/output:/work/output" \
  srp-nga2-review:precal \
  --config /opt/nga2/review/cases/smoke.input \
  --output /work/output/manual-smoke \
  --ranks 4
```

For a host input file, mount it read-only and provide its container path. On native Linux, add `--user "$(id -u):$(id -g)"` if reviewer-owned output files are required.

## Automated review suite

The suite runs:

1. a short open-channel MPI smoke test;
2. a Darcy-only uniform slab with analytical pressure drop `1`;
3. a Forchheimer-only uniform slab with analytical pressure drop `1`; and
4. a combined slab with analytical pressure drop `2`.

It requires normal NGA2 completion, finite monitor values, CFL below `0.8`, maximum divergence and relative mass mismatch no greater than `1e-10`, and analytical relative pressure error no greater than `1e-8`.

```sh
mkdir -p review/output
docker run --rm \
  --platform linux/arm64 \
  --entrypoint nga2Adsorption-review \
  --volume "$PWD/review/output:/work/output" \
  srp-nga2-review:precal \
  --output /work/output/verification \
  --ranks 4
```

The command writes one isolated directory per case plus `summary.csv` and `summary.json`.

## Verified platforms

Verification on 2026-10-20 used Docker with Colima on an Apple Silicon host:

- `linux/arm64` is locally verified. The final image built successfully and all four cases passed. The smoke case reached `t = 0.02` with maximum CFL `0.0176375`, maximum divergence `3.86870e-15`, and maximum relative mass error `5.79247e-16`. The Darcy, Forchheimer, and combined cases reached `t = 0.05` and reproduced pressure drops `1`, `1`, and `2` exactly at recorded precision.
- `linux/amd64` remains a supported build target but is not locally verified. Under Colima/QEMU, one build completed before the strict finite-value check was added, but its analytical runs produced non-finite values; subsequent strict rebuilds ended in nondeterministic emulated `gfortran` segmentation faults at different source files, even with one build job. A native x86-64 host must build the final Dockerfile and pass this same four-case suite before `linux/amd64` is called verified.

These checks establish packaging and numerical consistency only. They do not validate the provisional geometry or porous coefficients against SRP experiments.
