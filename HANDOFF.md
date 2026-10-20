# Project Handoff

Last updated: 2026-10-19

## Objective

Develop and validate an NGA2 CFD model of SRP's porous bead-rod CO2 collector. The model should predict airflow and pressure drop first, then add level-resolved CO2 adsorption. Moisture, temperature, and humid-air regeneration are later extensions.

## Sources of truth

- Current checklist: [`Thesis/leo_todo_list.md`](./Thesis/leo_todo_list.md)
- Equation provenance and adaptations: [`Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md`](./Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md)
- Research-component assessment: [`OtherResearch/USABLE_RESEARCH_COMPONENTS.md`](./OtherResearch/USABLE_RESEARCH_COMPONENTS.md)
- Primary methodological paper: [`OtherResearch/Adsorption performance of radial-flow contactors for direct air capture: A computational study.pdf`](./OtherResearch/Adsorption%20performance%20of%20radial-flow%20contactors%20for%20direct%20air%20capture%3A%20A%20computational%20study.pdf)

Read the checklist before treating this handoff as current. Update both files when a milestone is verified.

## Verified current status

- NGA2 has been compiled successfully.
- The stock channel example has run successfully with four MPI ranks.
- The preserved baseline is in `NGA2/examples/channel/runs/2026-10-05_baseline/`.
- The baseline reached simulation time `425.34` with a final maximum CFL of approximately `0.764`.
- The baseline was manually interrupted because the stock case has no finite stopping time.
- The radial paper's literature overview, assumptions, limitations, and Eqs. (1)-(27) have been reviewed.
- The equation sheet distinguishes original paper equations, SRP/NGA2 adaptations, and independently added project equations.
- The thesis-owned `Thesis/simulations/srp_channel` case now implements a 3D rectangular open channel with explicit inflow/outflow, stationary immersed walls, finite stopping time, flow/pressure outputs, and conservation monitors.
- Four-rank MPI smoke tests completed on `32 x 12 x 12` and `256 x 64 x 64` meshes. The target run reached `t = 0.02` with final CFL `0.142256`, maximum divergence about `2.1e-13`, and relative mass-flow error about `7e-15`.
- A provisional `256 x 64 x 64` run completed one flow-through time (`t = 4`) and passed the predeclared final-window numerical convergence rule: pressure-drop range/mean `0.123082%`, maximum relative mass-flow error `1.84374e-14`, maximum CFL `0.247208`, and maximum divergence `2.65364e-13`.
- A Darcy-only porous mask and momentum source are implemented. Paired uniform control/slab runs reproduce the Project Eq. P1 analytical excess pressure drop of `1` exactly within printed precision.
- The Forchheimer source is also implemented and independently reproduces its Project Eq. P1 analytical excess pressure drop of `1` exactly within printed precision.
- A configurable provisional `aligned_rods_z` mask places four separated rods on the target mesh. Each diameter spans six cells in both diameter directions, the rods occupy only the 60-cell open passage, and the short MPI smoke test remains stable and conservative.
- ParaView inspection of the four-rod smoke-test output confirms that the porous mask resolves four distinct rods. The latest velocity-magnitude slice shows four corresponding lower-velocity bands and faster flow through the gaps, providing qualitative evidence that the porous source is coupled to the velocity field. This is an early-time (`t = 0.02`) visualization, not a converged or calibrated pressure-drop result.
- Justin's 2026-10-19 email in `SupportingDocuments/Measure pressure drop through an empty packet in wind tunnel.eml` includes a preliminary plot for a 20-sheet Excellion assembly at 5 mm spacing: `4.5`, `12.7`, `25.8`, `44.3`, and `65.2 Pa` at `1` through `5 m/s`, respectively. The email also requests an empty-packet or single-mesh through-flow measurement by 2026-10-23 with pore size and percent open area recorded.
- The Excellion plot is aggregate system evidence only. It does not document enough geometry, baseline losses, uncertainty, bead loading, or velocity definition to assign physical NGA2 permeability or inertial-resistance coefficients.
- A dependency-free calibration tool in `Thesis/simulations/srp_channel/tools` now reads a documented pressure-drop CSV, subtracts the matching baseline, combines measurement and baseline uncertainties, preserves calibration/validation splits, and fits Project Eqs. P1-P2. Its synthetic test recovers `alpha = 0.02 m^2` and `C2 = 1.6 1/m` to floating-point precision, including a held-out validation point.
- Nine uniform-slab NGA2 cases now verify Darcy-only, Forchheimer-only, and combined pressure-drop scaling at velocities `0.5`, `1`, and `2`. Every final-window mean matches Project Eq. P1 within printed precision; maximum relative mass-flow error is `9.99201e-16`, maximum CFL is `0.08`, and maximum divergence is `2.68307e-13`.
- A configurable downstream flow-split monitor now reports equal-width band mass-flow rates, fractions, their sums, and the Project Eq. P7 coefficient of variation. Its four-band MPI test conserves total flow at monitor precision and preserves symmetry; a historical input verifies the backward-compatible one-band defaults.
- Matched one-flow-through open and provisional four-rod runs both pass the numerical convergence rule. The open mean P7 CV is `0.289743`; the rod value is `0.286648`. The synthetic rods therefore reduce four-band CV by `1.06811%`, move `0.0773705` percentage points of flow into each outer band, and increase total pressure drop by `0.0478910` (`2.65518%`). These are numerical comparison results only.
- The dimensions and operating conditions are provisional; no physically grounded or experimentally validated pressure-drop result exists yet.

## Important limitation of the stock baseline

The completed baseline is the unmodified stock channel case:

- Grid: `128 x 40 x 1`
- Geometry: effectively two-dimensional
- Streamwise boundary: periodic
- Driving method: body force

It is **not** the required 3D SRP channel with explicit inflow and outflow. The separate thesis-owned case now satisfies that smoke-test milestone; the stock run remains useful only as an NGA2 installation check.

## Immediate next task

Implement configurable stacked-sheet geometry without inventing physical dimensions, then verify its mask and flow-split bookkeeping on a short MPI run. Obtain confirmed rod dimensions and Marcus's first orientation, then fit permeability and inertial resistance when suitable empty-mesh and bead-filled-sheet data are available. Replace the provisional aligned reference parameters before making physical comparisons.

### Success criteria

1. **Completed:** Define a documented input format for pressure-drop data, geometry, fluid properties, uncertainty, and calibration/validation labels.
2. **Completed:** Recover known Darcy and Forchheimer coefficients from synthetic multi-velocity data within a declared numerical tolerance.
3. **Completed:** Verify simulated linear, quadratic, and combined porous-pressure-drop scaling against Project Eq. P1 at multiple velocities.
4. **Completed for the provisional aligned case:** Pressure drop, mass balance, and equal-width flow maldistribution are emitted to repeatable monitors, with matched converged open/rod summaries preserved. Other arrangements remain future comparisons.
5. Keep synthetic verification, preliminary Excellion correlations, and future calibrated SRP coefficients explicitly separated.

## Planned implementation sequence

1. **Completed:** Create and smoke-test the 3D open-channel case.
2. **Completed:** Add tagged porous bead-rod cells.
3. **Completed:** Add and independently verify Darcy-Forchheimer resistance based on radial-paper Eq. (10).
4. Use radial-paper Eqs. (18)-(19) only as initial estimates.
5. Fit permeability and inertial resistance to Justin's measured pressure-drop data.
6. Place four or five rods and compare the orientations selected by Marcus.
7. Measure flow paths, total pressure drop, per-rod pressure drop, and flow maldistribution.
8. Add CO2 scalar transport using radial-paper Eqs. (11) and (14).
9. Add LDF loading, Toth equilibrium, and the CO2 sink using radial-paper Eqs. (1), (15), and (17).
10. Report CO2 capture and loading separately for every rod or collector level.
11. Add temperature, explicit water transport, and regeneration only after the core model is verified and the required material data are available.

## Important technical decisions

- Use **adsorption** for CO2 binding to the solid beads. Reserve **absorption** for uptake into a bulk liquid phase.
- The radial paper is the primary methodological reference even though SRP uses a Cartesian rod geometry.
- Preserve original paper equation forms and published numbers in research notes.
- Show every SRP/NGA2 alteration separately and explain why it was made.
- Do not copy the radial paper's proprietary material coefficients into the SRP model.
- Treat the porous resistance as Darcy-Forchheimer unless experimental results justify omitting the inertial term.
- Confirm whether the NGA2 porous velocity is superficial or intrinsic before applying an Ergun coefficient.
- Validate airflow and pressure loss before adding adsorption.
- Do not model humid-air regeneration by manually reversing a source sign. Desorption should follow from a validated equilibrium and kinetic model under changed humidity and temperature.
- Treat moisture, temperature, and regeneration as later extensions unless the core scope changes.

## External blockers and questions

- **Justin/Marcus:** confirmed contactor dimensions, inlet/airflow conditions, and pressure-tap locations for the quantitative empty-channel baseline.
- **Justin/experimental team:** raw through-sheet pressure-drop data and metadata for the empty holder, empty mesh, and bead-filled sheets. A measurement request is active for 2026-10-23; the preliminary Excellion plot is not sufficient for porous-coefficient calibration.
- **Marcus:** which rod orientations should be simulated first.
- **Justin, possible:** wind-tunnel test of the bead box for system-level validation.
- **Material data:** SRP bead isotherm, kinetic, humidity, and thermal properties required for a validated adsorption/regeneration model.

## Verified stock build and run commands

From `NGA2/examples/channel/`:

```sh
FFTW_DIR=/opt/homebrew/opt/fftw \
make USE_HYPRE=FALSE USE_LAPACK=FALSE
```

```sh
mpiexec -n 4 ./nga.dp.gnu.opt.mpi.exe -i input
```

These commands verify the stock example only. The thesis-owned case build/run procedure and smoke-test evidence are documented in `Thesis/simulations/srp_channel/README.md`.

## Repository caution

`NGA2/` is intentionally maintained as a separate Git repository and ignored by the outer thesis repository. Its configured remote is `https://github.com/desjardi/NGA2.git`. The thesis documents, research files, `AGENTS.md`, and this handoff are tracked by the outer repository.

A new chat in the same workspace can read the local NGA2 checkout. Another computer must clone NGA2 separately because the outer repository does not contain it or configure it as a submodule.

Do not delete `.git` metadata or convert the nested repository without explicit user approval.

## Instructions for the next chat or agent

Before changing files:

1. Read this file.
2. Read `AGENTS.md`.
3. Read `Thesis/leo_todo_list.md`.
4. Read only the relevant portions of the equation sheet and research papers.
5. Inspect the existing code and run evidence instead of relying only on status prose.
6. State assumptions and define verification criteria before substantial implementation.
7. Make the smallest change that advances the immediate milestone.
8. Update `Thesis/leo_todo_list.md` and this handoff only after results are verified.

Suggested opening prompt for a new chat:

> Read `HANDOFF.md`, `AGENTS.md`, and `Thesis/leo_todo_list.md`. Inspect the existing baseline evidence. Then continue with the immediate next task, using the equation sheet only where relevant. Do not mark a milestone complete without verification.
