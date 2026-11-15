# Project Setup

The reproducible Docker review is the shortest path to running the verified numerical checks. A native build is useful for development and full simulation work.

## Repository checkout

Clone this repository, then clone NGA2 into the repository root as a separate checkout:

```sh
git clone https://github.com/desjardi/NGA2.git NGA2
```

The native case expects this layout:

```text
ASU--Thesis2-SRP_Project/
├── NGA2/
└── Thesis/simulations/srp_channel/
```

NGA2 is intentionally not an outer-repository submodule. Do not remove its `.git` directory or commit it to the thesis repository.

## Docker review workflow

Requirements:

- Docker Desktop or Colima on macOS
- Docker Desktop in Linux-container mode on Windows
- enough memory and disk space to compile NGA2 and retain review output

The image pins the reviewed NGA2 revision and runs four MPI checks: an open-channel smoke case plus Darcy-only, Forchheimer-only, and combined analytical cases.

### Apple Silicon macOS

From the repository root:

```sh
cd Thesis/simulations/srp_channel
./review/build-macos-arm64.sh
```

Pass a unique output name when retaining more than one result:

```sh
./review/build-macos-arm64.sh macos-arm64-second-run
```

The finalized `linux/arm64` workflow is locally verified.

### Intel Windows

From PowerShell at the repository root:

```powershell
cd Thesis/simulations/srp_channel
.\review\build-windows-intel.ps1
```

Use a unique output name for another run:

```powershell
.\review\build-windows-intel.ps1 -OutputName windows-amd64-second-run
```

The `linux/amd64` image is a supported build target but still requires verification on a native x86-64 host.

Outputs are written below `Thesis/simulations/srp_channel/review/output/`. The wrappers reject an existing result directory so earlier evidence is not overwritten. See [the Docker review notes](Thesis/simulations/srp_channel/review/DOCKER_REVIEW.md) for manual image builds, individual configurations, platform details, and the review checks.

## Native NGA2 workflow

The native build requires:

- a Fortran toolchain supported by NGA2;
- MPI;
- FFTW; and
- the separate `NGA2/` checkout described above.

From the thesis-owned case directory:

```sh
cd Thesis/simulations/srp_channel
FFTW_DIR=/path/to/fftw make -j4
```

On Homebrew installations, the FFTW path is commonly:

```sh
FFTW_DIR=/opt/homebrew/opt/fftw make -j4
```

Each preserved run has its own local `input` file. Run a four-rank case from that run directory:

```sh
cd Thesis/simulations/srp_channel/runs/<run-name>
mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input
```

The MPI rank count must match the product of the input file's `Partition` values. Start with a debug or review case before launching a full target-grid run.

For model parameters and verified numerical results, read [the simulation guide](Thesis/simulations/srp_channel/SIMULATION_GUIDE.md).

## Calibration and verification tools

The dependency-free porous-resistance fitting tool and its unit tests live in `Thesis/simulations/srp_channel/tools/`:

```sh
cd Thesis/simulations/srp_channel/tools
python3 -m unittest -v test_fit_porous_resistance.py
```

See [the calibration and verification notes](Thesis/simulations/srp_channel/tools/CALIBRATION_AND_VERIFICATION.md) for input requirements and numerical verification commands.

