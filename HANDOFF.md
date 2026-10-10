# Project Handoff

Last updated: 2026-10-10

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

## Important limitation of the baseline

The completed baseline is the unmodified stock channel case:

- Grid: `128 x 40 x 1`
- Geometry: effectively two-dimensional
- Streamwise boundary: periodic
- Driving method: body force

It is **not** the required 3D SRP channel with explicit inflow and outflow. Do not mark the 3D channel or open inflow/outflow tasks complete based on this run.

## Immediate next task

Create a separate SRP simulation case with a 3D Cartesian channel and explicit inflow and outflow. Run and verify the open channel before adding porous bead rods.

### Success criteria

1. The SRP case is separate from the stock NGA2 channel example.
2. The mesh is genuinely three-dimensional; use a smaller debug mesh before the target `64 x 64 x 256` mesh if needed.
3. Inlet, outlet, and wall boundary conditions are documented.
4. The case builds and runs reproducibly with a finite stopping condition.
5. Inlet and outlet mass flow agree within a stated tolerance.
6. Pressure and velocity fields are physically reasonable and viewable in the selected post-processing format.
7. The run directory records the code revision, input file, command, runtime, and key diagnostics.

## Planned implementation sequence

1. Create and verify the 3D open-channel case.
2. Add tagged porous bead-rod cells.
3. Add Darcy-Forchheimer resistance based on radial-paper Eq. (10).
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

- **Justin:** through-sheet pressure-drop data for empty sheets and bead-filled sheets.
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

These commands verify the stock example only. The new SRP case must document its own build and run procedure.

## Repository caution

At the time of this handoff, the outer repository reports `NGA2/`, `OtherResearch/`, and `Thesis/` as untracked. `NGA2/` is also a nested Git repository. A new chat in the same workspace can read these files, but another computer will not receive them through the outer repository until the Git structure is deliberately resolved and the intended files are committed.

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
