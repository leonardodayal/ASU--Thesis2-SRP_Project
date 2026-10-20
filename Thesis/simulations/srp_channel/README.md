# SRP Channel Simulation

This directory contains the thesis-owned NGA2 case for the Phase 2 pressure-drop simulation. NGA2 remains an external source dependency in the repository-level `NGA2/` directory.

## Status

The empty 3D channel is implemented and has completed finite four-rank MPI smoke tests on both a debug mesh and the target `256 x 64 x 64` mesh. A subsequent target-mesh run over one provisional flow-through time met the documented numerical convergence rule. None of these runs is a physical pressure-drop prediction because the dimensions and operating conditions remain provisional.

Darcy-Forchheimer resistance, a uniform verification slab, and a configurable provisional aligned four-rod mask are implemented. A configurable downstream monitor also reports equal-width band mass-flow rates, fractions, their sum, and the Project Eq. P7 coefficient of variation. Physical coefficients, confirmed rod dimensions, and advisor-selected arrangements remain pending.

A dependency-free calibration tool in `tools/` fits baseline-corrected multi-velocity pressure-drop data to Project Eqs. P1-P2, preserves calibration/validation splits, combines measurement and baseline uncertainties, and reports fitted `alpha` and `C2` with residual metrics. Its synthetic test recovers known coefficients to floating-point precision. It has not yet been applied to physical SRP data.

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
- Optional Darcy-Forchheimer porous slab selected by streamwise bounds, permeability, and inertial coefficient.
- Optional `aligned_rods_z` geometry with configurable rod count, diameter, first-to-last center span, and sheet location.
- Finite end time, Ensight velocity/pressure/wall-volume-fraction/porous-mask output, CFL and solver monitors, inlet/outlet mass-flow balance, area-averaged pressure drops at configurable planes, and equal-width flow-band diagnostics at a configurable downstream plane.

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

## Darcy slab verification (2026-10-16)

The paired `2026-10-16_darcy_uniform_control` and `2026-10-16_darcy_uniform_verification` runs test the Darcy source in a fully open periodic cross-section. With `mu = alpha = 0.01`, `Lp = 1`, and `U = 1`, Project Eq. P1 predicts an excess pressure drop of `1`. The simulation produced exactly `1` within printed precision, with zero final-window variation and mass-flow error. The successful run also exports the cell-centered `porous_mask` for geometry inspection.

This verification coefficient is intentionally synthetic. It is not a bead-rod material value and must not be used for physical predictions.

## Forchheimer slab verification (2026-10-16)

The paired `2026-10-16_forchheimer_uniform_control` and `2026-10-16_forchheimer_uniform_verification` runs independently test the quadratic term with negligible Darcy resistance. With `rho = 1`, `C2 = 2`, `Lp = 1`, and `U = 1`, Project Eq. P1 predicts an excess pressure drop of `1`. The simulation produced exactly `1` within printed precision, with zero final-window variation and mass-flow error.

`Forchheimer coefficient` has units of inverse length and defaults to zero when absent so historical inputs remain readable. Its verification value is synthetic and is not an SRP material coefficient.

## Multi-velocity porous-resistance verification (2026-10-19)

Nine uniform `32 x 4 x 4` slab cases tested Darcy-only, Forchheimer-only, and combined resistance at velocities `0.5`, `1`, and `2`. Every final-window mean matched Project Eq. P1 exactly within printed precision. Across the set, maximum relative mass-flow error was `9.99201e-16`, maximum CFL was `0.08`, and maximum divergence was `2.68307e-13`. The dated run directory preserves the inputs, monitors, and machine-readable summary. These remain synthetic numerical-verification cases, not physical SRP predictions.

## Flow-split diagnostic verification (2026-10-19)

The `2026-10-19_flow_split_debug` run divides the detected open passage into four equal-width `y` bands at `x = 3`. At the final step, the band rates sum to `0.976562`, consistent with inlet/outlet `0.976563` at monitor precision, the fractions sum to `1.0`, and symmetric band pairs agree. The P7 coefficient of variation is `0.0608306` for this developing wall-bounded profile. A historical input without the new keys also retains its one-band defaults and original pressure-drop result.

The implementation integrates NGA2's staggered `x`-face mass flux directly over each band. It does not multiply by cell volume fraction a second time because the immersed-boundary treatment is already represented in the face velocity; doing so would undercount near-wall flow. `Flow split plane` defaults to the downstream pressure plane, `Flow split bands` defaults to one, and an out-of-domain split plane is rejected at startup.

## Provisional aligned four-rod geometry (2026-10-16)

The `2026-10-16_aligned_four_rods_target_smoke` case verifies four cylindrical porous rods with axes along `z` on the `256 x 64 x 64` mesh. Each provisional `0.1`-diameter rod is resolved by six cells in both diameter directions, and the exported mask contains four separated groups confined to the 60-cell open passage. The short MPI run remained stable and conserved mass, but it is not converged or physically calibrated.

The preserved ParaView screenshots include the porous-mask geometry and pressure/velocity views. The latest velocity-magnitude slice shows four lower-velocity bands aligned with the rods and faster flow through the gaps. This is qualitative evidence that the Darcy-Forchheimer source affects the velocity field; because the image is from `t = 0.02` with provisional geometry and resistance, it must not be used as a quantitative pressure-drop result.

## Provisional converged four-rod run (2026-10-19)

The `2026-10-19_aligned_four_rods_provisional` case advances the same synthetic four-rod geometry through one flow-through time and applies the four-band diagnostic at `x = 3`. Over `t = 3` to `4`, total pressure-drop range/mean is `0.117198%`, maximum relative mass-flow error is `1.91038e-14`, maximum CFL is `0.246105`, and maximum divergence is `2.61609e-13`. It therefore passes the same numerical rule as the provisional open channel.

The mean band fractions are `0.178338`, `0.321662`, `0.321662`, and `0.178338`; mean P7 coefficient of variation is `0.286648` with final-window range/mean `0.103262%`. The exact band-pair symmetry is a useful implementation check.

The matched `2026-10-19_open_channel_flow_split_provisional` case has mean CV `0.289743`. Relative to it, the rods reduce CV by `1.06811%`, move `0.0773705` percentage points of flow into each outer band, and increase total pressure drop by `0.0478910` (`2.65518%`). Thus this synthetic aligned arrangement slightly flattens the four-band distribution at the cost of pressure loss. It remains unsuitable for physical design conclusions.

## Next work (not implemented)

Add a configurable stacked-sheet geometry without assigning unconfirmed physical dimensions, then verify its mask and flow-split bookkeeping on a short MPI run. Obtain confirmed rod dimensions, Marcus's first orientation, and calibration-quality empty-mesh and bead-filled-sheet data before replacing the provisional aligned reference values. Do not interpret any synthetic verification coefficient as an SRP material property.
