# Project Handoff

Last updated: 2026-11-11

## Objective

Develop and validate an NGA2 CFD model of SRP's porous bead-rod CO2 collector. The model should predict airflow and pressure drop first, then add level-resolved CO2 adsorption. Moisture, temperature, and humid-air regeneration are later extensions.

## Sources of truth

- Current checklist: [`Thesis/leo_todo_list.md`](./Thesis/leo_todo_list.md)
- Equation provenance and adaptations: [`Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md`](./Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md)
- Research-component assessment: [`OtherResearch/USABLE_RESEARCH_COMPONENTS.md`](./OtherResearch/USABLE_RESEARCH_COMPONENTS.md)
- Primary methodological paper: [`OtherResearch/Adsorption performance of radial-flow contactors for direct air capture: A computational study.pdf`](./OtherResearch/Adsorption%20performance%20of%20radial-flow%20contactors%20for%20direct%20air%20capture%3A%20A%20computational%20study.pdf)

Read the checklist before treating this handoff as current. Update both files when a milestone is verified.

## Verified current status

- Repository guidance is organized around one root `README.md`. Root-level `SETUP.md` contains native and Docker setup, while specialized model, review, tool, and run records use descriptive filenames beside the artifacts they document.
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
- Justin's 2026-10-19 message in the consolidated thread `SupportingDocuments/PhysicalMeasurments/pressure_drop_email_thread_2026-10-19_to_2026-11-05.pdf` includes a preliminary plot for a 20-sheet Excellion assembly at 5 mm spacing: `4.5`, `12.7`, `25.8`, `44.3`, and `65.2 Pa` at `1` through `5 m/s`, respectively. The message also requests an empty-packet or single-mesh through-flow measurement with pore size and percent open area recorded.
- The Excellion plot is aggregate system evidence only. It does not document enough geometry, baseline losses, uncertainty, bead loading, or velocity definition to assign physical NGA2 permeability or inertial-resistance coefficients.
- Ramesh's 2026-10-19 reply and attached `MT 125 micron Mesh dP data RK 10:19.pdf` provide 29 pressure-drop measurements for two layers of MT 125-micron polyester mesh on a custom 3D-printed stand in a closed-loop wind tunnel. From `0.1` to `2.9 m/s`, pressure drop rises from `1.6` to `75.6 Pa`. An unweighted zero-intercept fit reproduces the plotted correlation, `Delta p = 13.3676 U + 4.42639 U^2` in Pa, with `RMSE = 0.313 Pa` and `R^2 = 0.999805`. The `3.0 m/s` table entry is blank; the correlation predicts `79.94 Pa` there, so it is not a measured point.
- The source table is transcribed without interpolation in `SupportingDocuments/PhysicalMeasurments/mt_125_micron_two_layer_raw.csv`: 29 rows are marked `measured`, and the blank `3.0 m/s` row is retained as `missing` for provenance. The transcription and reproduced fit were independently checked on 2026-10-20.
- The new result is useful physical evidence for the tested two-layer mesh/stand assembly but is not yet sufficient to assign NGA2 bead-bed `alpha` and `C2`. The document omits an empty-stand baseline, percent open area, test-section and pressure-tap geometry, mesh thickness/effective porous length, uncertainty or repeats, air properties, and an explicit statement that the tabulated wind speed is the superficial velocity through the mesh. Ramesh stated that the 25-micron nylon-mesh dataset would be available by 2026-10-23.
- The complete email thread through 2026-11-05 adds a `10 cm x 10 cm` packet fill opening, eight horizontal pockets nominally `1.25 cm` wide before subtracting seal width, and about `0.3 g` of unexchanged Purolite A501P chloride-form resin per pocket. Samantha identifies a CMS25 nylon packet (`25 micrometre`, `12.02%` open), while Ramesh describes a packed-bead test using a `40-micrometre` filter; these are likely separate configurations, but the run-to-configuration mapping is missing. Ramesh reports that one-filter, blank-frame, and packed-bead tests were completed, but the referenced `Pressure Drop of Filter.xlsx`, holder drawing, openness deck, and photos are not present in the repository or common local download folders. These new results cannot be calibrated until the spreadsheet and configuration metadata are recovered. The consolidated source review is in `SupportingDocuments/EVIDENCE_SUMMARY.md`.
- Samantha's 2026-11-06 response confirms that the eight pockets are rod-like and bulge in both directions, are separated by nominally solid `2 mm` thermo-sealed lines, and have a fill-dependent thickness. Wet beads swell. Measurements of the existing `0.3 g` fill and a fully packed packet, empty-stick and fully packed runs, and a wind-tunnel humidity-capability check were planned; seal airtightness and all new numeric results remain pending. On 2026-11-09 Leonardo proposed a paired defined-aperture empty/filled experiment to isolate bead resistance. The experiment plan and readiness gates are tracked in `SupportingDocuments/EXPERIMENT_TRACKER.md`.
- Advisor-directed grid planning reported 2026-11-11 now uses the constant-ratio sequence `192 x 48 x 48`, `384 x 96 x 96`, `768 x 192 x 192`, and `1536 x 384 x 384` for a single experimental-style layer with eight sticks and up to 128 Sol cores. Each refinement halves grid spacing (`r = 2`), which supports standard three-grid GCI using the first three levels. The 226,492,416-cell fourth grid is conditional on memory and per-step timing from short smoke jobs. The MPI decomposition and physical stick thickness also remain to be frozen.
- The first G1 smoke input and 128-rank Slurm script are under `Thesis/simulations/srp_channel/studies/2026-11-11_eight_stick_gci`. They use one `aligned_rods_z` layer, eight centers spanning `0.875`, provisional circular diameter `0.105`, and eight flow bands. This reproduces the reported pitch and `2 mm` separator in normalized geometry but assumes an unmeasured `1.05 cm` streamwise thickness. A local four-rank copy passed ten steps on 2026-11-11. Sol job `1105006` then showed that `16 x 4 x 2` is invalid because NGA2's FFT constructor requires one non-decomposed direction. Corrected job `1120483` used `16 x 8 x 1` on 128 ranks and completed ten steps to `t = 0.02` in 13 solver seconds (16 batch seconds), with exit code `0`, no error markers, eight identical represented rod areas (`0.00668939%` error), eight `0.125`-width bands, and final maximum divergence `2.10491e-14`. The largest reported task RSS was `138236K`; G2-G3 still require their own memory/timing smoke tests.
- The prior `384 x 96 x 96` result cannot serve as G2 for this GCI sequence because it used four sticks per sheet and three sheets. The next resource test is therefore a new 100-step, eight-stick, single-layer G2 using `16 x 4 x 1`, 64 ranks, 128 GB, and a 15-minute limit. Its measured seconds per step decide whether 64 ranks meet the full-run target or G2 needs 128. A 128-rank G3 smoke is prepared but remains unsubmitted until G2 is reviewed.
- Sol job `1122564` verified the new G2 topology on 64 ranks. It started without queue delay and completed 100 steps in 53 solver seconds (58 batch seconds), with exit code `0`, no failure markers, eight identical rod areas (`0.00802438%` error), eight equal-width bands, maximum CFL `0.245134`, final maximum divergence `7.41629e-14`, and relative mass-flow error `1.11044e-15`. Linear extrapolation gives about `17:40` solver time for 2,000 steps. The initial 128-rank G3 request, job `1122809`, was cancelled while pending with zero allocated CPU time. Replacement G3 job `1123065` used 64 ranks and completed 100 steps in `6:13` solver time (`6:17` batch), with exit code `0`, no failure markers, eight identical rod areas (`-0.000986796%` error), equal bands, maximum CFL `0.500787`, final maximum divergence `1.71010e-11`, relative mass-flow error `1.44336e-14`, and maximum reported task RSS `759928K`. A 2,000-step linear projection is about `2:04:20`. G4 is eight times larger by cell count and requires a separately sized high-memory/time request rather than the current 64-rank, 128 GB, 15-minute template.
- The November 5 workbook was recovered on 2026-11-11. Its packed 40-micrometre-filter series has 21 points over `0.00-0.20 m/s` and `0.0-28.4 Pa`. A zero-intercept Darcy fit gives `Delta p = 139.8293 U Pa` (`RMSE 0.8344 Pa`, `R^2 0.98934`). An unconstrained Darcy-Forchheimer fit has a negative quadratic coefficient, so the provisional physical fit uses `C2 = 0`. With the explicitly provisional `10.5 mm` thickness and `mu = 1.81e-5 Pa s`, its effective assembly permeability is `1.35916e-9 m^2`. The corresponding normalized solver inputs use `L_ref=0.10 m`, `U_ref=0.20 m/s`, `rho_ref=1.204 kg/m^3`, nondimensional viscosity `7.51661e-4`, and permeability `1.35916e-7`. G1 active/control 100-step inputs are prepared; a short active G1 must pass before generating or submitting G2/G3. The first 128-rank request, job `1126264`, was cancelled while pending with zero allocated CPU time and replaced by a 64-rank `16 x 4 x 1` request to reduce queue pressure. This is an effective packed-filter fit, not an isolated bead coefficient, and remains provisional pending thickness and matched-control metadata.
- A dependency-free calibration tool in `Thesis/simulations/srp_channel/tools` now reads a documented pressure-drop CSV, subtracts the matching baseline, combines measurement and baseline uncertainties, preserves calibration/validation splits, and fits Project Eqs. P1-P2. Its synthetic test recovers `alpha = 0.02 m^2` and `C2 = 1.6 1/m` to floating-point precision, including a held-out validation point.
- Nine uniform-slab NGA2 cases now verify Darcy-only, Forchheimer-only, and combined pressure-drop scaling at velocities `0.5`, `1`, and `2`. Every final-window mean matches Project Eq. P1 within printed precision; maximum relative mass-flow error is `9.99201e-16`, maximum CFL is `0.08`, and maximum divergence is `2.68307e-13`.
- A configurable downstream flow-split monitor now reports equal-width band mass-flow rates, fractions, their sums, and the Project Eq. P7 coefficient of variation. Its four-band MPI test conserves total flow at monitor precision and preserves symmetry; a historical input verifies the backward-compatible one-band defaults.
- Matched one-flow-through open and provisional four-rod runs both pass the numerical convergence rule. The open mean P7 CV is `0.289743`; the rod value is `0.286648`. The synthetic rods therefore reduce four-band CV by `1.06811%`, move `0.0773705` percentage points of flow into each outer band, and increase total pressure drop by `0.0478910` (`2.65518%`). These are numerical comparison results only.
- A configurable `stacked_aligned_rods_z` option repeats the verified aligned sheet by count and center-to-center spacing about a stack center. A three-sheet target-mesh smoke test produces exactly three separated six-cell x groups, four separated six-cell y groups per sheet, `7,680` cells per sheet, and no wall-padding cells. The run is stable and conservative, and the historical single-sheet input remains backward-compatible.
- A conditional `sheet_pressure` monitor now samples both sides of every rod sheet and reports each pressure drop, their sum, the whole-stack sampled drop, and closure error. The three-sheet test reports final drops `0.765813`, `0.765851`, and `0.765825`; their sum and the stack drop both equal `2.29749` at monitor precision. Non-rod and single-sheet regression tests pass.
- A conditional `sheet_flow_split` monitor now reports equal-width band mass flow, fractions, and Project Eq. P7 CV after every sheet. In the three-sheet smoke test, every plane sums to total mass flow with fraction sum `1.0`, paired bands remain symmetric, and open/single-sheet regressions preserve their earlier results.
- The provisional three-sheet stack completed one flow-through time and passes the numerical convergence rule: total pressure-drop range/mean `0.105332%`, maximum mass-flow error `1.92149e-14`, maximum CFL `0.243918`, and maximum divergence `2.63684e-13`. A matched zero-resistance stack control also converged and exactly reproduces the earlier open-channel mean total pressure drop. Control subtraction gives local sheet-plane pressure increments `0.0340160`, `0.0421726`, and `0.0463172`; resistance lowers P7 CV relative to control by `3.20851%`, `4.42426%`, and `4.61025%` after sheets 1-3.
- A matched `128 x 32 x 32` resistance-active/control pair passes the numerical checks. Relative to the `256 x 64 x 64` pair, Project Eq. P15 changes are `3.98685%` for corrected total pressure drop, at most `4.00174%` for local sheet increments, and at most `2.86352%` for corrected P7 CV changes. A finer-than-target pair is still needed for formal grid independence.
- A target-grid time-step sensitivity run halves the maximum timestep from `0.002` to `0.001`. It passes the numerical checks, and the changes are `0.289417%` for total pressure drop, at most `0.179043%` for individual sheet drops, and at most `0.207011%` for per-sheet P7 CV. All pass the predeclared `1%` working criterion.
- A short `384 x 96 x 96` finer-grid feasibility run allocates and completes stably on four ranks. It resolves each rod diameter with 10 streamwise cells, gives identical `25,920`-cell masks for all three sheets, and ends with CFL `0.219908`, relative mass-flow error `1.73227e-14`, and maximum divergence `1.08864e-13`. A full matched pair is projected at roughly `83–107 min` total.
- The full matched `384 x 96 x 96` active/control pair completed one flow-through time and passes the numerical checks. Active-minus-control gives total excess pressure drop `0.136410538922`, local sheet increments `0.032471768463`, `0.040393670659`, and `0.044265325349`, and P7 CV changes `-0.007432313373`, `-0.010921227545`, and `-0.011863766467`.
- Project Eq. P15 target-to-fine changes are `4.49272%` for corrected total pressure, `4.40392-4.75564%` for local sheet increments, and `10.0345-10.7750%` for corrected P7 changes. Coarse and fine corrected pressure agree within `0.326755%` overall and `0.918400%` locally, so the pressure sequence is non-monotonic rather than cleanly convergent. Fine-grid P7 also uses 90 open cells that cannot be divided evenly into four integer-cell bands. Formal grid independence is not established.
- The grid diagnosis identified two concrete changes in represented physics. The binary rod mask gave each coarse and target rod `6.1033%` excess projected area but only `0.2087%` excess on the fine grid. Whole-row flow-band assignment produced alternating widths of `0.233333/0.266667` on the coarse grid and `0.244444/0.255556` on the fine grid, while the target bands were `0.25` wide.
- The production code now uses fractional coverage in circular rod-boundary cells, overlap-weighted physical flow bands, and interpolation to requested physical pressure and velocity planes. Machine-readable rod and band audits are emitted, and Ensight output can be disabled for lightweight diagnostics. The corrected three-grid ten-step MPI test gives maximum rod-area error `0.002874%`, cross-grid rod-area spread `0.00287824%`, exact `0.25` band widths, maximum CFL `0.219908`, maximum divergence `2.28660e-13`, maximum relative mass-flow error `3.34239e-14`, and pressure closure no worse than `1.34292e-16`.
- All nine uniform Darcy, Forchheimer, and combined slab cases were rerun with executable SHA-256 `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`; every mean pressure drop still matches Project Eq. P1 exactly at recorded precision. The old full-duration grid results remain diagnostic history and cannot be combined with corrected fractional-geometry results.
- Corrected full-duration coarse, target, and fine active/control pairs pass every numerical check. Active-minus-control total excess pressure increases monotonically from `0.118040415170` to `0.122476005988` to `0.124160157685`. Project Eq. P15 target-to-fine changes are `1.35643%` for total pressure, `1.21755-1.45490%` for sheet increments, and `2.04532-2.57712%` for corrected P7 changes. These pass the working `2%` pressure and `5%` P7 gates, identifying the coarse grid as pre-asymptotic and accepting the target grid for provisional aligned-stack comparisons. The fine pair completed in about `119 min` total; across it, maximum relative mass-flow error is `5.11908e-14`, maximum CFL is `0.374454`, maximum divergence is `1.92513e-13`, and maximum pressure closure error is `2.21644e-16`.
- On 2026-11-06, ASU Sol job `614569` reproduced the corrected `384 x 96 x 96` fine active case with four ranks in `55:43` of solver time, versus about `63 min` on the Mac. Sol job `624047` used an `8 x 1 x 1` decomposition and completed in `42:20`, a `1.316x` speedup over the Sol four-rank run and about `65.8%` strong-scaling efficiency for the rank doubling. Both jobs reached `t = 4` in 2,000 steps with exit code `0:0`; all reported final pressure, CFL, flow, and flow-split quantities agree at printed precision. Differences in divergence, mass-balance error, and pressure closure are roundoff-scale. Evidence is the user-reported Sol `sacct` records and final monitor rows; full outputs remain under `/scratch/ldayal/srp_benchmark` and are not backed up in this repository.
- A reproducible pre-calibration Docker review package now lives in `Thesis/simulations/srp_channel/review`. Its multi-stage Ubuntu 24.04 build fetches NGA2 commit `28a58d937af89dd506456048be1cad58f6d383a9`, compiles the thesis-owned source, and exposes `nga2Adsorption --config ... --output ... --ranks ...`. The automated suite rejects non-finite values and checks one MPI smoke case plus Darcy, Forchheimer, and combined analytical slabs. On 2026-10-20, the finalized `linux/arm64` image and the macOS Apple Silicon wrapper both passed all four cases; analytical drops were exactly `1`, `1`, and `2` at recorded precision. A PowerShell wrapper targets Intel Windows through Docker Desktop's Linux-container mode. `linux/amd64` is not yet verified because Colima/QEMU produced nondeterministic `gfortran` segmentation faults during strict rebuilds; it requires the wrapper suite to pass on a native x86-64 host. All bundled geometry and porous coefficients are explicitly provisional.
- The dimensions and operating conditions are provisional. Physical two-layer empty-mesh/stand pressure-drop evidence now exists, but no bead-filled porous coefficient or experimentally validated NGA2 pressure-drop result exists yet.

## Important limitation of the stock baseline

The completed baseline is the unmodified stock channel case:

- Grid: `128 x 40 x 1`
- Geometry: effectively two-dimensional
- Streamwise boundary: periodic
- Driving method: body force

It is **not** the required 3D SRP channel with explicit inflow and outflow. The separate thesis-owned case now satisfies that smoke-test milestone; the stock run remains useful only as an NGA2 installation check.

## Immediate next task

Validate an eight-stick, single-layer smoke case on the advisor-directed four-grid, constant-`r = 2` sequence before submitting the resolution sweep on Sol. Use no more than the approved 128 cores, but benchmark the decomposition rather than assuming 128 ranks is optimal. Complete G1-G3 for standard GCI first and treat the 226,492,416-cell G4 as conditional on measured memory and timing. The sweep remains a numerical study until filled thickness, seal airtightness, holder dimensions, and calibrated porous coefficients arrive.

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
- **Samantha/experimental team:** provide the planned filled-thickness measurements for the `0.3 g` and fully packed packets; confirm whether the `2 mm` solid thermo-seals are airtight; assess the paired defined-aperture empty/filled calibration; and report the wind tunnel's maximum controllable humidity. The rod-like, two-sided bulging shape and wet-bead swelling are now confirmed, but exact thickness, airtightness, quantitative swelling, alignment/offset, and complete stand dimensions remain unresolved.
- **Justin/experimental team:** recover `Pressure Drop of Filter.xlsx`, `windTunnelHolder.pdf`, the openness-method deck, and the latest photos; map every blank, filter-only, and packed-bead series to its CMS25 (`25 micrometre`) or `40-micrometre` packet configuration; and supply pressure-tap geometry, effective porous length, air properties, uncertainty/repeats, velocity definition, dry packing density, and the blank-to-packed pairing. The email confirms that blank-frame and packed-bead tests exist, but their numeric results are not yet available locally.
- **Marcus:** which stick orientation should be simulated first and confirmation that at least 10 cells across the physical diameter is the intended production-resolution criterion in both cross-sectional directions.
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

These commands verify the stock example only. The thesis-owned case build/run procedure and smoke-test evidence are documented in `Thesis/simulations/srp_channel/SIMULATION_GUIDE.md`.

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
