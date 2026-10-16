# SRP Channel Simulation

This directory contains the thesis-owned NGA2 case for the Phase 2 pressure-drop simulation. NGA2 remains an external source dependency in the repository-level `NGA2/` directory.

## Status

The empty 3D channel is implemented and has completed finite four-rank MPI smoke tests on both a debug mesh and the target `256 x 64 x 64` mesh. A subsequent target-mesh run over one provisional flow-through time met the documented numerical convergence rule. None of these runs is a physical pressure-drop prediction because the dimensions and operating conditions remain provisional.

No porous-medium or bead-rod model has been added.

## Intended layout

- `GNUmakefile`: builds the case against `../../../NGA2`.
- `input`: target-mesh smoke-test parameters.
- `input.debug`: smaller smoke-test parameters.
- `src/`: thesis-owned rectangular geometry and incompressible-flow driver.
- `runs/`: dated run inputs, logs, monitors, and field outputs.

## Implemented model

- Cartesian mesh with flow along `x`.
- Uniform Dirichlet inlet and clipped-Neumann outlet.
- Stationary rectangular immersed-boundary walls in `y` and `z`.
- FFT pressure solution using periodic padded regions outside the immersed walls, following the approach used by NGA2's pipe example.
- Constant-density, constant-viscosity incompressible flow.
- Finite end time, Ensight velocity/pressure/wall-volume-fraction output, CFL and solver monitors, inlet/outlet mass-flow balance, and area-averaged pressure drop.

`ny` and `nz` include the padded wall cells. With the current target input and two padding cells on each side, the open passage contains `60 x 60` fully open cross-section cells inside the `64 x 64` allocated cross-section.

## Provisional inputs

The current `Lx = 4`, `Ly = 1`, `Lz = 1`, density `1`, viscosity `0.01`, and inlet velocity `1` are nondimensional test values. They must be replaced with confirmed experimental dimensions and air properties before interpreting pressure drop quantitatively.

## Build

From this directory:

```sh
FFTW_DIR=/opt/homebrew/opt/fftw make -j4
```

## Run

NGA2's input parser expects a local filename, so each dated run directory preserves its own file named `input`. From a run directory:

```sh
mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input
```

## Verified runs (2026-10-10)

| Run | Mesh | Steps / final time | Final CFL | Final max divergence | Final relative MFR error |
|---|---:|---:|---:|---:|---:|
| `2026-10-10_open_channel_debug` | `32 x 12 x 12` | `4 / 0.02` | `0.0419867` | `2.20e-14` | `1.82e-15` |
| `2026-10-10_open_channel_target_smoke` | `256 x 64 x 64` | `10 / 0.02` | `0.142256` | approximately `2.1e-13` | approximately `7e-15` |

Both runs reached their configured maximum time and their monitor files contain no NaN or infinity values. The pressure-drop values are transient results from provisional inputs and must not be compared with the `10 Pa` project target.

## Provisional convergence run (2026-10-16)

The `2026-10-16_open_channel_target_provisional` run advanced the target mesh to `t = 4`, one flow-through time based on the provisional `Lx = 4` and `Uin = 1`. The predeclared final-window rule required pressure-drop range/mean no greater than `1%`, relative mass-flow error no greater than `1e-10`, CFL no greater than `0.8`, and finite/bounded solver diagnostics.

Over `t = 3` to `4`, the mean provisional pressure drop was `1.80368173653`, its range/mean was `0.123082%`, and maximum relative mass-flow error was `1.84374e-14`. Full-run maximum CFL and divergence were `0.247208` and `2.65364e-13`. This establishes numerical convergence for the provisional setup only. See the dated run README and monitors for the preserved evidence.

## Next work (not implemented)

Confirm the physical geometry and wind-tunnel operating conditions, rerun the documented convergence check with those inputs, and assess physical plausibility. Porous resistance begins only after that quantitative baseline is accepted.
