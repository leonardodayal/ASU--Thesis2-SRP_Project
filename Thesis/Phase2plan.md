# Phase 2 Plan: Wind-Driven Contactor Hydrodynamics

## Goal

Build and validate a separate NGA2 model of airflow through the rectangular SRP contactor. The contactor contains stacked mesh sheets holding bead rods. Phase 2 establishes the hydrodynamic model first, then uses it to compare sheet geometry, spacing, packing, and contactor depth before CO2 and water-vapor transport are added.

This work supports proposal Task 1.1 and Deliverable D1.1. It also supplies the CFD side of Task 1.2/D1.2 experimental validation. The full M1.1 milestone additionally requires predicted CO2 capture productivity and therefore cannot be completed by the pressure-drop model alone.

Phase 2 is complete when:

- a 3D `256 x 64 x 64` streamwise/cross-section mesh runs with explicit inflow and outflow;
- the empty-channel solution is stable and conserves mass;
- porous resistance is implemented and checked against a simple Darcy/Forchheimer reference case;
- the porous coefficients are calibrated against wind-tunnel pressure-drop/airflow measurements when available;
- the requested bead-rod and stacked-sheet configurations run from the same baseline settings; and
- each configuration has documented pressure drop, airflow distribution, bypassing, and flow-field output.

The hydrodynamic design target inherited from proposal Milestone M1.1 is a contactor pressure drop no greater than `10 Pa` while maintaining useful airflow under representative Southwestern wind conditions up to `2 m/s` average wind. Passing the pressure-drop target does not by itself establish capture productivity.

## Current status

- NGA2 and the stock periodic channel example have already been built and run with four MPI ranks.
- `Thesis/simulations/srp_channel` contains the implemented thesis-owned empty-channel case, build configuration, debug/target inputs, and dated run evidence.
- Four-rank MPI smoke tests have completed on `32 x 12 x 12` and target `256 x 64 x 64` meshes with bounded CFL/divergence and mass-flow balance near machine precision.
- The target-mesh Ensight output has been opened and inspected successfully in ParaView; the fluid passage and velocity, pressure, and wall-volume-fraction fields render as intended.
- Work Plan Steps 2 and 3 are complete for the provisional numerical model. Steps 4 and 5 are partially complete: resistance scaling, the aligned single-sheet geometry, a provisional stack, matched open/rod runs, and per-sheet pressure accounting are verified, while physical calibration and advisor-selected arrangements remain pending.
- Physical dimensions and operating conditions remain provisional. The one-flow-through open, single-sheet, three-sheet, and matched zero-resistance control runs are numerically converged under those provisional inputs; none is a calibrated physical pressure-drop prediction.
- A Darcy-Forchheimer porous slab and exported porous mask are implemented. The linear and inertial terms were independently verified against uniform analytical references. A configurable provisional four-rod aligned mask also passes a target-mesh geometry and solver smoke test. Fitted material coefficients and advisor-selected physical geometry remain pending.
- ParaView slices from the four-rod smoke test show velocity deficits aligned with all four porous rods and acceleration through the intervening gaps. This confirms qualitative source/flow interaction at the short final time (`t = 0.02`), but does not establish a converged or physically meaningful pressure drop.
- A 2026-10-19 email from Justin includes a preliminary plot for a 20-sheet Excellion assembly at 5 mm spacing and requests an empty-packet or single-mesh through-flow measurement by 2026-10-23. The aggregate plot lacks the metadata needed to assign physical porous coefficients, so the calibration blocker is only partially advanced.
- Ramesh's 2026-10-19 reply supplies 29 measurements for two MT 125-micron polyester-mesh layers on a custom stand: `1.6-75.6 Pa` over `0.1-2.9 m/s`. The table reproduces the plotted assembly correlation `Delta p = 13.3676 U + 4.42639 U^2` Pa (`RMSE = 0.313 Pa`, `R^2 = 0.999805`). The blank `3.0 m/s` row is not a measured point. Missing empty-stand baseline, geometry, percent-open-area, effective-length, uncertainty, air-property, and velocity-definition metadata still prevent a defensible mesh-only or bead-bed coefficient fit.
- The source values are preserved in `SupportingDocuments/PhysicalMeasurments/mt_125_micron_two_layer_raw.csv` as 29 measured rows plus the explicit missing row; the transcription and reproduced fit were independently verified on 2026-10-20.
- A calibration-ready fitting tool now implements Project Eqs. P1-P2 with baseline subtraction, uncertainty weighting, calibration/validation splits, and synthetic coefficient-recovery tests. Physical calibration remains pending.
- Nine uniform-slab NGA2 cases verify the linear Darcy term, quadratic Forchheimer term, and their sum at velocities `0.5`, `1`, and `2`; all final-window pressure drops match Project Eq. P1 within printed precision.
- A configurable downstream flow-split monitor implements Project Eqs. P6-P7 over equal-width bands. Its four-band MPI verification conserves total mass flow at monitor precision, preserves symmetry, and remains backward-compatible with historical inputs.
- Matched one-flow-through open and provisional aligned four-rod runs pass the numerical convergence rule. Relative to the open case, the synthetic rods reduce four-band CV by `1.06811%` and increase total pressure drop by `2.65518%`; physical interpretation remains blocked by unconfirmed geometry and coefficients.
- A configurable provisional stack now repeats the verified aligned sheet by count and spacing. A three-sheet target-mesh smoke test confirms three separated sheet groups, four separated rods per sheet, exclusion of wall padding, stable flow, and backward-compatible single-sheet behavior.
- Per-sheet pressure diagnostics report each sheet drop, the sum, the sampled whole-stack drop, and closure error. A three-sheet smoke test telescopes exactly at monitor precision; non-rod and historical single-sheet regression cases pass.
- Per-sheet flow-split diagnostics now report equal-width band rates, fractions, and P7 CV after every sheet. A three-sheet smoke test conserves flow at every plane, preserves symmetry, and passes open/single-sheet regressions.
- The provisional three-sheet stack and matched zero-resistance control completed one flow-through time and pass the numerical convergence rule. Control subtraction shows local sheet-plane pressure increments of `0.0340160`, `0.0421726`, and `0.0463172`; resistance lowers P7 CV relative to control by `3.20851%`, `4.42426%`, and `4.61025%`. The raw downstream CV increase is primarily background wall-profile development.
- A matched `128 x 32 x 32` resistance-active/control pair passes the same checks. Relative to the `256 x 64 x 64` pair, Project Eq. P15 changes are at most `4.00174%` for corrected pressure quantities and `2.86352%` for corrected P7 CV changes. A finer-than-target pair is still required for formal grid independence.
- Halving the target-grid timestep from `0.002` to `0.001` changes total pressure drop by `0.289417%`, sheet drops by at most `0.179043%`, and per-sheet P7 CV by at most `0.207011%`, passing the predeclared `1%` working time-step-sensitivity criterion.
- A short `384 x 96 x 96` feasibility run fits in memory and completes stably on four ranks. It resolves each rod diameter with 10 streamwise cells and gives identical `25,920`-cell masks for all three sheets. A full matched finer-grid pair is projected to require about `83–107 min` total.
- The full matched `384 x 96 x 96` active/control pair now completes one flow-through time and passes the numerical checks. Project Eq. P15 target-to-fine changes are `4.49272%` for corrected total pressure, up to `4.75564%` for local sheet increments, and up to `10.7750%` for corrected P7 changes. Coarse and fine corrected pressure agree more closely than target and fine, and the 90-cell fine passage cannot be divided evenly into four integer-cell bands. The result is non-monotonic and does not establish formal grid independence.
- The diagnosis found that binary cell-center masking overrepresented coarse and target rod area by `6.1033%`, compared with `0.2087%` on the fine grid, and that whole-row assignment gave unequal physical band widths on the coarse and fine grids. The solver now uses fractional circular-cell coverage, physical-overlap band integration, and exact-plane interpolation. A three-grid ten-step MPI test reduces maximum rod-area error to `0.002874%`, limits cross-grid area spread to `0.00287824%`, makes all bands exactly `0.25` wide, and passes the numerical checks. The analytical nine-case porous regression remains exact at recorded precision.
- Corrected full-duration coarse, target, and fine active/control pairs pass all numerical checks. Corrected total pressure and per-sheet quantities vary monotonically across the three grids. Project Eq. P15 target-to-fine changes are `1.35643%` for total corrected pressure, `1.21755-1.45490%` for sheet increments, and `2.04532-2.57712%` for corrected P7 changes. These pass the working `2%` pressure and `5%` P7 gates, identifying the coarse grid as pre-asymptotic and accepting the target grid for provisional aligned-stack comparisons.
- A multi-stage Docker review package now pins the NGA2 dependency and exposes the thesis case through `nga2Adsorption --config ... --output ... --ranks ...`. Its one smoke and three analytical cases automatically enforce finite diagnostics, CFL, divergence, mass balance, and Darcy/Forchheimer pressure-drop tolerances. The finalized `linux/arm64` image passed locally on 2026-10-20. `linux/amd64` remains build-targeted pending a native x86-64 run because local QEMU builds failed nondeterministically inside `gfortran`. This is pre-calibration packaging evidence only; every bundled geometry and porous coefficient remains provisional.

## Assumptions and decisions still needed

- Flow is along `x`, so `nx = 256`, `ny = 64`, and `nz = 64`.
- The new case will live in `Thesis/simulations/srp_channel`; the NGA2 source tree and stock channel baseline will not be modified.
- The empty-channel milestone passed its checks before porous resistance and rods were added. Preserve that verified open case as the baseline for subsequent comparisons.
- The NGA2 model is the thesis implementation of the CFD work described with Ansys Fluent in the proposal. Confirm with Marcus and Justin that NGA2 results will satisfy the project deliverable.
- A bead rod is a porous region inside one mesh sheet; multiple sheets are stacked along the contactor flow path. Keep rod-scale arrangement and sheet-scale spacing/depth as separate geometry parameters.
- Physical channel dimensions, fluid properties, inlet velocity/profile, and run duration must be taken from the experiment or agreed with the advisors before quantitative comparison.
- Marcus must prioritize the first rod orientations.
- Calibration-quality empty-mesh and bead-filled-sheet pressure-drop data, including geometry, baseline losses, velocity definition, and uncertainty, are required to fit the final porous coefficients. The MT 125-micron two-layer mesh/stand correlation may be used only as measured assembly evidence until its missing baseline and metadata are supplied; an Ergun estimate or the preliminary Excellion system correlation may be used only as a clearly labeled provisional value.

## Work plan

### 1. Freeze the baseline inputs

- [ ] Record the physical channel length, width, and height.
- [ ] Record the working-fluid density and dynamic viscosity.
- [ ] Define the inlet condition: uniform or developed profile, and its velocity or flow rate.
- [ ] Define the wall conditions and the physical locations used to sample inlet and outlet pressure.
- [ ] Obtain the wind-tunnel test matrix: empty frame/sheet, bead-filled sheet, sheet spacings, packing densities, contactor depths, airflow rates, and pressure-tap locations.
- [ ] Define how turbine/whirlybird performance will be coupled later; do not assume inlet velocity and available pressure independently for a passive system.
- [ ] Calculate the target Reynolds number and expected empty-channel pressure drop for a basic sanity check.

**Verify:** All dimensional values, units, sources, and derived nondimensional values are written in the case README. No placeholder value is used without being labeled.

### 2. Create a separate 3D SRP case

- [x] Add the minimum implementation needed to the `Thesis/simulations/srp_channel` scaffold: input parameters and source files.
- [x] Create a Cartesian grid with `nx = 256`, `ny = 64`, and `nz = 64`.
- [x] Make `x` nonperiodic and retain solid walls on the channel cross-section.
- [x] Choose an MPI partition whose factors match the launched rank count and divide the mesh dimensions exactly.
- [x] Add a finite stopping condition and configurable output intervals.
- [x] Compile the new case without changing the stock channel case.

**Implementation reference:** Reuse the inflow/outflow pattern already demonstrated in `NGA2/examples/pipe/src/simulation.f90` or `NGA2/examples/cylinder/src/simulation.f90`: a Dirichlet inlet, clipped-Neumann outlet, and mass-flow correction. Remove the stock channel's periodic streamwise forcing.

**Verify:** The executable builds cleanly, the startup log reports the intended mesh and decomposition, and a short MPI smoke test completes without NaNs or solver failure.

### 3. Verify the empty-channel flow

- [x] Run a short low-resolution or short-duration test before the full `256 x 64 x 64` run.
- [x] Monitor CFL, maximum divergence, pressure-solver residual/iterations, and inlet/outlet mass flow.
- [x] Add outputs for area-averaged pressure at fixed upstream and downstream planes.
- [x] Compute pressure drop using Project Eq. P3 in `SRP_CO2_COLLECTOR_EQUATION_SHEET.md`.
- [x] Compute mass-flow conservation error using Project Eqs. P4-P5.
- [x] Inspect the target-mesh geometry and velocity, pressure, and wall-volume-fraction output in ParaView.
- [x] Run the provisional target-mesh setup until pressure drop and mass flow are steady, using an explicit convergence rule recorded in the README.
- [x] Save the input, launch command, code revision, runtime, velocity, pressure, and monitor data in a dated run directory.

**Verify:** CFL remains below its configured limit, the solver residuals remain bounded, inlet and outlet mass flow agree within a documented tolerance, and the measured empty-channel pressure drop is physically plausible.

### 4. Add and verify porous resistance

- [x] Add a cell mask `chi_p` that is 1 inside a porous test region and 0 in open fluid.
- [x] Add and verify the Darcy term first, then independently add and verify the Forchheimer inertial term.
- [x] Keep permeability and inertial resistance as named input parameters with units documented.
- [x] Run a simple uniform porous slab before creating rods.
- [x] Compare its simulated pressure gradient with the analytical Darcy prediction.
- [ ] Fit permeability `alpha` and inertial coefficient `C2` to bead-filled-sheet pressure-drop data using Project Eqs. P1-P2.
- [ ] Separate empty-mesh/frame resistance from bead-bed resistance when the measurements permit it.
- [ ] Validate the fitted coefficients at airflow rates not used for fitting; retain provisional Ergun and fitted values as separate runs.

**Verify:** The porous source acts only where `chi_p = 1`, opposes the local velocity, and the slab pressure drop agrees with the reference calculation within a declared tolerance.

### 5. Create the bead-rod and stacked-sheet geometry

- [x] Represent a provisional four-rod aligned reference across the 64-cell cross-section using the verified porous mask.
- [x] Check the provisional rod resolution: each diameter spans six target-mesh cells in both diameter directions, and the four masks are separated and unclipped.
- [ ] Implement only the arrangements selected for the first comparison: aligned, 90-degree rotation, offset, or angled.
- [x] Assemble the validated sheet representation into a configurable stack with explicit sheet count and spacing; derive contactor depth from the first-to-last sheet span plus rod diameter.
- [x] Add per-sheet pressure drops, their sum, the sampled whole-stack drop, and a closure-error monitor.
- [ ] Define packing density from measurable geometry or bead mass/volume rather than an unlabeled tuning factor.
- [x] Output the porous mask with the flow fields so each geometry can be inspected.

**Verify:** Cell counts and rendered slices confirm the intended rod size, count, placement, and orientation with no accidental overlap or boundary clipping.

### 6. Validate against the wind-tunnel contactor

- [ ] Reproduce the measured sheet spacings, contactor depths, packing densities, airflow rates, and pressure-tap locations.
- [ ] Compare simulated and measured pressure drop and airflow rate across the anticipated operating range.
- [ ] Report absolute and relative error for each validation point and define the acceptance tolerance before judging agreement.
- [ ] Use discrepancies to calibrate porous coefficients only within the selected calibration cases; reserve other cases for validation.
- [ ] Document measurement uncertainty and propagate it into the model-comparison plots when those data are available.

**Verify:** The model meets the predeclared pressure-drop and airflow error tolerances on validation cases that were not used to fit the porous coefficients.

### 7. Run and compare configurations

- [ ] Sweep the experimentally supported airflow rates, including conditions representative of wind speeds up to `2 m/s`.
- [ ] Compare sheet spacing, packing density, contactor length/depth, and selected rod/flow-path arrangements.
- [ ] Use the same domain, fluid properties, sampling planes, and convergence rule within each controlled comparison.
- [ ] Record total pressure drop, inlet/outlet mass balance, and runtime for each case.
- [x] Implement and numerically verify equal-width downstream flow-split fractions and the Project Eq. P7 coefficient of variation.
- [ ] Apply the flow-split monitor to converged rod and stacked-sheet cases, and save center-plane velocity and pressure fields plus streamlines or equivalent views that expose bypassing and flow maldistribution.
- [ ] Summarize the results in one table and identify configurations at or below the `10 Pa` hydrodynamic target.
- [x] Repeat the representative porous active/control case on corrected coarse, target, and fine meshes. Project Eq. P15 target-to-fine changes pass the working `2%` pressure and `5%` P7 criteria; retain the target grid for provisional comparisons.
- [x] Repeat one representative case at a smaller maximum time step to check time-step sensitivity separately from grid sensitivity.

**Verify:** Every reported comparison uses converged cases with controlled settings, the configuration conclusions are not materially changed by the grid/time-step checks, and any case claimed to meet the design target has total contactor pressure drop `<= 10 Pa` at the stated airflow condition.

## Required outputs

For every quantitative case, retain:

- total and per-sheet pressure drop;
- inlet, outlet, and per-sheet airflow/mass flow;
- mass-conservation error;
- a flow-uniformity or maldistribution metric across each sheet;
- velocity and pressure fields showing bypass paths;
- CFL, divergence, solver convergence, averaging interval, and runtime; and
- geometry parameters, porous coefficients, mesh, boundary conditions, and input provenance.

CO2 capture rate, water-vapor transport, working capacity, and contactor productivity are later coupled-model outputs. Phase 2 should preserve locations/tags for these future monitors but should not claim them from the airflow-only model.

## Suggested execution order

1. Collect or confirm baseline inputs.
2. Build and smoke-test the separate empty 3D case.
3. Run the empty case to convergence and verify conservation.
4. Implement and verify a porous slab, then calibrate it with through-sheet data.
5. Add the first advisor-selected bead-rod sheet and validate it against wind-tunnel data.
6. Build the stacked-sheet contactor and compare spacing, packing, depth, airflow, and flow-path configurations.
7. Check the best-supported cases for grid and time-step sensitivity.

## Immediate next action

Obtain Marcus's first orientation and confirmed rod dimensions, then run that supported configuration on the accepted target grid. Keep historical binary-mask results separate from the corrected fractional-mask sequence. Fit permeability and inertial resistance with Project Eqs. P1-P2 when calibration-quality data arrive.

