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
- Optional `aligned_rods_z` geometry with configurable rod count, diameter, first-to-last center span, and sheet location. Circular boundary cells use conservative fractional coverage so the represented area remains physically consistent across grids.
- Optional `stacked_aligned_rods_z` geometry that repeats the aligned sheet using configurable sheet count, center-to-center spacing, and stack center. Its streamwise porous depth is `(Sheet count - 1) * Sheet spacing + Rod diameter`.
- Finite end time, optional Ensight velocity/pressure/wall-volume-fraction/porous-mask output, CFL and solver monitors, inlet/outlet mass-flow balance, interpolated area-averaged pressure drops at exact physical planes, per-sheet and whole-stack pressure-drop closure, and physically equal flow-band diagnostics at both a configurable downstream plane and every sheet's downstream sampling plane.

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

The implementation integrates NGA2's staggered `x`-face mass flux directly over each physical band. A row that crosses a band edge is split by its geometric overlap, so all grids measure the same band widths. It does not multiply by cell volume fraction a second time because the immersed-boundary treatment is already represented in the face velocity; doing so would undercount near-wall flow. `Flow split plane` defaults to the downstream pressure plane, `Flow split bands` defaults to one, and an out-of-domain split plane is rejected at startup. `Write Ensight output` defaults to true and may be disabled for lightweight diagnostic runs.

## Provisional aligned four-rod geometry (2026-10-16)

The `2026-10-16_aligned_four_rods_target_smoke` case verifies four cylindrical porous rods with axes along `z` on the `256 x 64 x 64` mesh. Each provisional `0.1`-diameter rod is resolved by six cells in both diameter directions, and the exported mask contains four separated groups confined to the 60-cell open passage. The short MPI run remained stable and conserved mass, but it is not converged or physically calibrated.

The preserved ParaView screenshots include the porous-mask geometry and pressure/velocity views. The latest velocity-magnitude slice shows four lower-velocity bands aligned with the rods and faster flow through the gaps. This is qualitative evidence that the Darcy-Forchheimer source affects the velocity field; because the image is from `t = 0.02` with provisional geometry and resistance, it must not be used as a quantitative pressure-drop result.

## Provisional converged four-rod run (2026-10-19)

The `2026-10-19_aligned_four_rods_provisional` case advances the same synthetic four-rod geometry through one flow-through time and applies the four-band diagnostic at `x = 3`. Over `t = 3` to `4`, total pressure-drop range/mean is `0.117198%`, maximum relative mass-flow error is `1.91038e-14`, maximum CFL is `0.246105`, and maximum divergence is `2.61609e-13`. It therefore passes the same numerical rule as the provisional open channel.

The mean band fractions are `0.178338`, `0.321662`, `0.321662`, and `0.178338`; mean P7 coefficient of variation is `0.286648` with final-window range/mean `0.103262%`. The exact band-pair symmetry is a useful implementation check.

The matched `2026-10-19_open_channel_flow_split_provisional` case has mean CV `0.289743`. Relative to it, the rods reduce CV by `1.06811%`, move `0.0773705` percentage points of flow into each outer band, and increase total pressure drop by `0.0478910` (`2.65518%`). Thus this synthetic aligned arrangement slightly flattens the four-band distribution at the cost of pressure loss. It remains unsuitable for physical design conclusions.

## Provisional stacked-sheet geometry (2026-10-19)

The `2026-10-19_stacked_three_sheet_target_smoke` case verifies three separated sheets centered at `x = 1.5`, `2.0`, and `2.5`, with four aligned rods per sheet. The exported mask contains `23,040` porous cells: three separated six-cell x groups, four separated six-cell y groups per sheet, and 60 open-passage z cells with no wall-padding cells. Each sheet has `7,680` cells, exactly matching the verified single-sheet mask.

The ten-step MPI run completed with final CFL `0.142256`, maximum divergence `2.18902e-13`, relative mass-flow error `3.33206e-15`, and symmetric four-band flow. A historical single-sheet input also reproduces its prior result with the new executable. This verifies geometry construction and short-time stability only; the stack dimensions and resistance remain synthetic.

## Per-sheet pressure diagnostics (2026-10-19)

The `2026-10-19_stacked_three_sheet_pressure_smoke` case samples area-averaged pressure on both sides of every sheet. With sample planes halfway between adjacent sheets, final transient sheet drops are `0.765813`, `0.765851`, and `0.765825`; their sum and the sampled whole-stack drop both equal `2.29749`, producing zero closure error at monitor precision. Non-rod and historical single-sheet regression runs also pass.

`Sheet pressure offset` controls the distance from each sheet center. It defaults to half the sheet spacing for a multi-sheet stack and one rod diameter for a single sheet. Multi-sheet sample regions may touch at their shared midpoint but may not overlap.

## Per-sheet flow-split diagnostics (2026-10-19)

The `2026-10-19_stacked_three_sheet_flow_split_smoke` case applies the same four-band mass-flow and P7 calculation after every sheet. At the final step, each sheet-plane band sum is `0.999583`, each fraction sum is `1.0`, and paired bands remain symmetric. Transient CV values after sheets 1-3 are `0.0182707`, `0.0182705`, and `0.0183899`.

The original single downstream monitor is preserved. Non-rod cases create no sheet-specific monitor, and open/single-sheet regression cases reproduce their prior pressure and flow results.

## Provisional converged three-sheet stack (2026-10-19)

The `2026-10-19_stacked_three_sheet_provisional` case completed one flow-through time and passes the numerical convergence rule. Over `t = 3` to `4`, mean total pressure drop is `1.94622081836` with range/mean `0.105332%`; maximum relative mass-flow error is `1.92149e-14`, maximum CFL is `0.243918`, and maximum divergence is `2.63684e-13`.

Mean sheet drops are `0.224764`, `0.215793`, and `0.209112`, summing exactly to sampled stack drop `0.649668` at monitor precision. Mean downstream P7 CV values are `0.246710`, `0.260804`, and `0.271920` after sheets 1-3. Total pressure increase above the matched open case is `0.142539` (`7.90267%`), or `2.97632` times the provisional single-sheet increment. These remain synthetic results; a matched zero-resistance stack control is needed to remove streamwise wall-profile development from the per-sheet trends.

## Matched zero-resistance stack control (2026-10-19)

The `2026-10-19_stacked_three_sheet_control` case preserves the three masks and all sampling planes but uses `alpha = 1e30` and `C2 = 0`. It completed one flow-through time and reproduces the open-channel mean total pressure drop exactly at monitor precision. Subtracting this control gives local sheet-plane pressure increments of `0.0340160`, `0.0421726`, and `0.0463172`. The resistance-active case lowers P7 CV relative to control by `3.20851%`, `4.42426%`, and `4.61025%` after sheets 1-3. Thus the raw downstream CV increase is mainly background profile development, while the provisional porous resistance slightly improves this four-band uniformity metric.

## Coarse-grid sensitivity pair (2026-10-19)

Matched `128 x 32 x 32` active/control runs also complete one flow-through time and pass the numerical checks. Against the `256 x 64 x 64` pair, Project Eq. P15 changes are `3.98685%` for corrected total pressure drop, `3.55237%` to `4.00174%` for local sheet pressure increments, and `1.80770%` to `2.86352%` for sheet-plane P7 CV changes. The conclusions retain their signs. Because the coarse passage has 30 open cells across four bands, it loses exact paired-band symmetry; a finer-than-target run is still needed for formal grid independence.

## Time-step sensitivity (2026-10-19)

The `2026-10-19_stacked_three_sheet_dt001` case halves the target-grid maximum timestep from `0.002` to `0.001` with all other inputs unchanged. Relative to the smaller-step result, total pressure drop changes by `0.289417%`, individual sheet drops by `0.166671%` to `0.179043%`, and sheet-plane P7 CV by `0.194141%` to `0.207011%`. All are below the predeclared `1%` working criterion.

## Finer-grid feasibility (2026-10-19)

A short `384 x 96 x 96` run successfully allocated and completed ten steps on four ranks. The subsequent full matched active/control pair completed one flow-through time and passes the numerical checks. Active-minus-control gives total excess pressure drop `0.136410538922`, local sheet increments `0.032471768463`, `0.040393670659`, and `0.044265325349`, and P7 CV changes `-0.007432313373`, `-0.010921227545`, and `-0.011863766467`.

Against the target pair, Project Eq. P15 changes are `4.49272%` for corrected total pressure, `4.40392-4.75564%` for local sheet increments, and `10.0345-10.7750%` for corrected P7 changes. Coarse and fine corrected pressure agree within `0.326755%` overall and `0.918400%` locally, so the three-grid pressure sequence is non-monotonic. The fine passage also has 90 open cells, which cannot be split evenly into four integer-cell bands. Formal grid independence is not established.

The subsequent code audit found that the binary mask represented each coarse and target rod with `6.1033%` excess projected area, versus only `0.2087%` on the fine grid. Whole-row flow bands also alternated between unequal widths on the coarse and fine grids. The corrected fractional mask and overlap-weighted bands pass a three-grid, ten-step MPI test: maximum rod-area error is `0.002874%`, cross-grid area spread is `0.00287824%`, every band is exactly `0.25` wide, and all numerical smoke checks pass. The earlier full-duration values must not be mixed with the corrected discretization.

Corrected full-duration coarse, target, and fine matched pairs then completed successfully. Active-minus-control total excess pressure increases monotonically from `0.118040415170` to `0.122476005988` to `0.124160157685`. Although coarse-to-target changes exceed the working gates, target-to-fine Project Eq. P15 changes are `1.35643%` for total pressure, `1.21755-1.45490%` for individual sheet increments, and `2.04532-2.57712%` for corrected P7 changes. These pass the working `2%` pressure and `5%` P7 gates. The coarse grid is pre-asymptotic under this criterion, and the target grid is accepted for provisional aligned-stack comparisons. This numerical acceptance does not validate the provisional physical inputs.

## Next work (not implemented)

Obtain confirmed rod dimensions, Marcus's first orientation, and calibration-quality empty-mesh and bead-filled-sheet data before replacing the provisional aligned reference values. Use the accepted target grid for the next supported configuration, and retain the corrected fine pair as the grid-sensitivity reference.
