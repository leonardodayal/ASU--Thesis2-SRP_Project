# To-Do List (Leonardo Dayal)

Based on the meeting with Justin Flory and Marcus Herrmann.

**Priority:** Finish the remaining hydrodynamic diagnostics while physical geometry and calibration data are pending, then calibrate and validate the pressure-drop model before adding adsorption.

## Progress snapshot (2026-10-20)

- **Completed:** NGA2 has been built and successfully run with MPI using the stock channel example.
- **Completed:** The radial paper's introduction, literature overview, and governing adsorption equations have been reviewed and documented in [SRP_CO2_COLLECTOR_EQUATION_SHEET.md](./SRP_CO2_COLLECTOR_EQUATION_SHEET.md).
- **Completed:** A separate thesis-owned 3D SRP case now builds and completes finite MPI smoke tests with explicit inflow/outflow on debug and target `256 x 64 x 64` meshes.
- **Completed:** The target-mesh Ensight output has been opened and inspected successfully in ParaView, including the fluid passage, velocity, pressure, and wall-volume-fraction fields.
- **Completed:** The provisional target-mesh setup ran for one flow-through time and met its documented numerical convergence rule; this is not yet a physical pressure-drop prediction.
- **Completed:** A Darcy-only porous slab and exported mask reproduce the uniform analytical pressure drop exactly within printed precision.
- **Completed:** The Forchheimer term independently reproduces its uniform analytical pressure drop exactly within printed precision.
- **Completed:** A configurable provisional four-rod aligned mask passes target-mesh resolution, placement, wall-clipping, and solver smoke checks.
- **Completed:** ParaView inspection shows four velocity-deficit bands aligned with the four porous rods and faster flow through the gaps, confirming qualitative porous/velocity coupling at `t = 0.02`. This short transient is not a converged or calibrated pressure-drop result.
- **New measurement evidence:** Justin's 2026-10-19 email includes a preliminary pressure-drop plot for 20 Excellion sheets at 5 mm spacing and requests an empty-packet or single-mesh through-flow test by 2026-10-23. The plot is not sufficient to assign physical porous coefficients because key geometry, baseline, uncertainty, bead-loading, and velocity-definition metadata are absent.
- **New measurement evidence:** Ramesh supplied 29 points for two MT 125-micron polyester-mesh layers on a custom 3D-printed stand. Over `0.1-2.9 m/s`, pressure drop is `1.6-75.6 Pa`; the table reproduces `Delta p = 13.3676 U + 4.42639 U^2` Pa with `RMSE = 0.313 Pa` and `R^2 = 0.999805`. The blank `3.0 m/s` row is not a measurement. This characterizes the tested mesh/stand assembly but does not isolate mesh or bead-bed resistance.
- **Completed:** The 29 measurements and blank `3.0 m/s` source row are transcribed with provenance and measurement status in `SupportingDocuments/PhysicalMeasurments/mt_125_micron_two_layer_raw.csv`; the transcription and fitted coefficients were independently verified on 2026-10-20.
- **Completed:** A calibration-ready fitting tool now handles baseline subtraction, independent measurement/baseline uncertainties, calibration/validation splits, and Project Eqs. P1-P2 conversion. It recovers known synthetic `alpha` and `C2` values to floating-point precision, including a held-out validation point.
- **Completed:** Nine multi-velocity NGA2 slab cases verify the linear Darcy term, quadratic Forchheimer term, and their sum at velocities `0.5`, `1`, and `2`; all final-window pressure drops match Project Eq. P1 within printed precision.
- **Completed:** A configurable downstream flow-split monitor reports equal-width band mass-flow rates, fractions, and Project Eq. P7 maldistribution. Its four-band MPI test conserves the total flow at monitor precision, preserves symmetry, and historical inputs retain one-band defaults.
- **Completed:** A matched converged open-channel baseline isolates the provisional rods' effect. The rods reduce four-band CV by `1.06811%` while increasing total pressure drop by `2.65518%`; these are synthetic numerical results, not physical design findings.
- **Completed:** A configurable provisional stack repeats the verified aligned sheet by sheet count and center-to-center spacing. A three-sheet, four-rods-per-sheet target-mesh smoke test verifies separated masks, no wall clipping, conservative flow, and backward-compatible single-sheet behavior.
- **Completed:** Per-sheet pressure monitors now report every sheet drop, their sum, whole-stack sampled drop, and closure error. The three-sheet smoke test closes exactly at monitor precision and regression tests cover non-rod and historical single-sheet inputs.
- **Completed:** Flow split and Project Eq. P7 maldistribution are now reported after every sheet. The three-sheet smoke test conserves each plane's total flow, preserves symmetry, and passes open/single-sheet regressions.
- **Completed:** The provisional three-sheet stack completed one flow-through time and passed the convergence rule. Mean sheet drops are `0.224764`, `0.215793`, and `0.209112`; downstream P7 CV values are `0.246710`, `0.260804`, and `0.271920`.
- **Completed:** The matched zero-resistance three-sheet control completed one flow-through time and reproduced the open-channel total pressure drop. Control subtraction shows that the provisional resistance adds `0.142539` total pressure drop and reduces P7 CV by `3.20851%`, `4.42426%`, and `4.61025%` after sheets 1-3.
- **Completed:** A matched `128 x 32 x 32` active/control pair gives Project Eq. P15 changes of at most `4.00174%` for corrected pressure quantities and `2.86352%` for corrected P7 CV changes versus the target pair. A finer-than-target pair is still needed for formal grid independence.
- **Completed:** Halving the target-grid timestep to `0.001` changes total pressure drop by `0.289417%`, sheet drops by at most `0.179043%`, and per-sheet P7 CV by at most `0.207011%`; all pass the predeclared `1%` working criterion.
- **Completed:** A short `384 x 96 x 96` feasibility test fits in memory, resolves each rod diameter with 10 streamwise cells, produces identical `25,920`-cell masks for all three sheets, and completes stably. A full matched pair is projected at `83–107 min` total.
- **Completed:** The full matched `384 x 96 x 96` resistance-active/control pair completed one flow-through time and passes the convergence, CFL, mass-balance, divergence, and pressure-closure checks.
- **Grid-sensitivity result:** Target-to-fine Project Eq. P15 changes are `4.49272%` for corrected total pressure, at most `4.75564%` for local sheet increments, and at most `10.7750%` for corrected P7 changes. Coarse and fine corrected pressure agree within `0.918400%`, making the three-grid pressure sequence non-monotonic. Formal grid independence is not established.
- **Completed diagnosis:** The binary mask overrepresented each coarse/target rod area by `6.1033%`, versus `0.2087%` on the fine grid. Whole-cell flow bands also had unequal physical widths on the coarse and fine grids.
- **Completed correction and smoke verification:** Rod-boundary cells now use fractional coverage, band flux uses physical overlap, and pressure/flow diagnostics interpolate to requested physical planes. Across three ten-step MPI cases, maximum rod-area error is `0.002874%`, cross-grid area spread is `0.00287824%`, all four bands are exactly `0.25` wide, and the numerical checks pass. Nine Darcy/Forchheimer slab regressions still match Project Eq. P1 exactly at recorded precision.
- **Completed corrected three-grid sequence:** Full-duration coarse, target, and fine active/control pairs pass the numerical checks. Corrected total pressure is monotonic (`0.118040415170`, `0.122476005988`, `0.124160157685`). Target-to-fine Project Eq. P15 changes are `1.35643%` for total pressure, `1.21755-1.45490%` for sheet increments, and `2.04532-2.57712%` for corrected P7 changes, passing the working `2%` pressure and `5%` P7 gates. The coarse grid is pre-asymptotic; the target grid is accepted for provisional aligned-stack comparisons.
- **Completed:** A multi-stage pre-calibration Docker review package pins NGA2, provides the `nga2Adsorption` launcher, and automatically checks one smoke and three analytical MPI cases while labeling every geometry and porous coefficient provisional. The finalized `linux/arm64` image and four-case suite passed locally on 2026-10-20. `linux/amd64` is a documented build target pending native x86-64 verification because local QEMU compiler emulation was unstable.
- **Next milestone:** Obtain Marcus's first orientation and confirmed rod dimensions, then run the supported configuration on the accepted target grid. Keep old binary-mask results separate from the corrected fractional-mask sequence.
- **Current blockers for physical predictions:** Confirmed contactor dimensions/operating conditions, rod-orientation priorities, an empty-stand baseline and measurement metadata for the new two-layer mesh data, and bead-filled-sheet data are still outstanding.

## 1. Get set up

- [x] Install NGA2 and make sure it's ready to run.
  - Verified by the compiled channel executable and the documented MPI baseline run in `NGA2/examples/channel/runs/2026-10-05_baseline/`.

## 2. Build the first simulation (pressure drop)

- [x] Set up a 3D Cartesian mesh channel, about 64 x 64 x 256 cells, small enough to run on a laptop or desktop.
  - Implemented in `Thesis/simulations/srp_channel` with a `256 x 64 x 64` target mesh and a smaller debug input.
- [x] Run it first as a pure open channel with inflow and outflow.
  - Four-rank debug and target-mesh smoke tests completed normally on 2026-10-10. The target run ended at `t = 0.02` with final CFL `0.142256`, maximum divergence about `2.1e-13`, and relative inlet/outlet mass-flow error about `7e-15`.
  - The target-mesh output was successfully visualized in ParaView on 2026-10-12.
  - A one-flow-through-time target run met the provisional numerical convergence rule on 2026-10-16. The current values remain provisional and are not a validated pressure-drop result. See `Thesis/simulations/srp_channel/README.md`.
- [x] Add a verified porous-medium test region with lower permeability than the surrounding open space.
  - Uniform-slab, single-sheet rod, and provisional stacked-sheet masks are implemented and verified. Their current dimensions and resistance values remain synthetic.
- [x] Implement and independently verify the Darcy and Forchheimer resistance terms used by the radial paper. Physical coefficients still require Justin's data.
- [x] Place a provisional four-rod aligned reference across the 64-cell width; replace its dimensions if advisor values differ.
- [x] Assemble the aligned reference into a configurable provisional stack with explicit sheet count, spacing, stack center, and derived streamwise depth.
- [x] Add per-sheet pressure sampling and verify that the sheet drops sum to the sampled whole-stack drop.
  - In the three-sheet smoke test, final transient sheet drops `0.765813`, `0.765851`, and `0.765825` sum to the stack value `2.29749` with zero closure error at monitor precision.
- [ ] Try several arrangements: same orientation, rotated 90 degrees, offset, or angled.
- [ ] Get the flow path and overall pressure drop from each.
- [x] Add and verify equal-width downstream flow-split and maldistribution monitoring; geometry-specific rod/sheet comparisons remain pending.
  - Matched converged open and provisional aligned four-rod cases now isolate the rods' incremental pressure-drop and four-band flow-split effects.
- [x] Extend flow-split and Project Eq. P7 maldistribution reporting to every sheet plane in a stack.

## 3. Literature review (with Marcus)

- [x] Read the intro and literature overview of the radial paper, the first one Justin sent.
  - Reviewed the modeling alternatives, assumptions, limitations, and cited basis for LDF kinetics, Toth equilibrium, Ergun resistance, and non-equilibrium heat transfer.
- [x] Note how it models CO2 adsorption, since its results showed CO2 profiles inside the bead material.
  - Documented the paper's original Eqs. (1)-(27), explicit SRP/NGA2 adaptations, and project-added equations in [SRP_CO2_COLLECTOR_EQUATION_SHEET.md](./SRP_CO2_COLLECTOR_EQUATION_SHEET.md).
- [ ] Check the papers it cites to see whether that model applies to these specific beads.

## 4. Coupled transport and experimental validation

- [ ] Calibrate Darcy-Forchheimer coefficients against baseline-corrected empty-mesh and bead-filled-sheet measurements, then validate against held-out airflow rates.
- [ ] Add CO2 scalar transport after the hydrodynamic model is physically calibrated and validated.
- [ ] Add bead loading, equilibrium, and adsorption/desorption kinetics using SRP material data; do not model regeneration by manually reversing a source sign.
- [ ] Add moisture and temperature only after the core CO2-flow coupling is verified.
- [ ] Compare experimentally supported packing density, spacing, thickness, and advisor-selected arrangements.

## Things to confirm

- [ ] Ask Marcus which rod orientations he wants first (he only suggested options).

## Waiting on others

- **Justin/experimental team:** empty-stand baseline; percent open area; test-section, sample, and pressure-tap geometry; mesh thickness/effective porous length; air properties; uncertainty/repeats; confirmation of the velocity definition; and bead-filled-sheet measurements. The two-layer MT 125-micron mesh/stand data are available, and the 25-micron nylon dataset was promised by 2026-10-23. Configurations with flow along normally mounted packets come later.
- **Justin (possible):** small wind-tunnel experiment on the box of beads for system-level validation.
- **Sherry:** follow-up note to be sent.
