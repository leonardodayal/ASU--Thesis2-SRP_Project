# Project Execution and Problem Log

Last updated: 2026-11-23

## Purpose

This is the concise thesis-ready record of major implementation steps, verified results, problems, and resolutions for the SRP porous bead-rod airflow model. Values labeled **provisional** depend on dimensions or resistance data that have not been experimentally confirmed.

## Model development

### Baseline and open channel — October 2026

- Compiled NGA2 and verified the stock channel example with four MPI ranks.
- Created the thesis-owned 3D open-channel case with explicit inlet/outlet boundaries, immersed walls, finite stopping time, pressure monitoring, and mass-conservation checks.
- Verified `32 x 12 x 12` and `256 x 64 x 64` meshes. The target smoke run reached `t=0.02` with CFL `0.142256`, divergence about `2.1e-13`, and mass-flow error about `7e-15`.
- Ran the provisional target mesh to one flow-through time, `t=4`. The final-window pressure variation was `0.123082%`, with stable CFL, divergence, and conservation.

### Porous resistance and packet geometry

- Implemented Darcy and Forchheimer momentum resistance. Uniform-slab tests reproduced the analytical excess pressure drop within printed precision.
- Added configurable porous rods, stacked sheets, sheet-pressure sampling, downstream flow splits, and maldistribution monitoring.
- Added a separate retaining-mesh annulus and integrated mesh-resistance inputs. A corrected G1 audit retained `4,200` mesh-only cells outside the bead mask.
- Added seven internal separator walls and two outer closures. A four-rank smoke test found all nine wall segments and remained stable and conservative.

### Verification and reproducibility tooling

- Added automated checks for geometry, finite diagnostics, CFL, divergence, mass balance, Darcy/Forchheimer pressure loss, convergence windows, and completed timestep count.
- Verified nine uniform-slab analytical cases spanning Darcy-only, Forchheimer-only, and combined resistance at three velocities.
- Added a calibration tool that subtracts matched baselines, carries measurement uncertainty, separates calibration/validation points, and passed a synthetic coefficient-recovery test.
- Hardened the GCI calculator to align timestep and physical time and reject invalid ratios, zero values, oscillatory sequences, and undefined denominators. Six focused GCI tests and two porous-resistance regressions passed.
- Built a multi-stage Docker review package with macOS Apple Silicon support. Native x86-64 verification remains pending because local QEMU builds failed nondeterministically in `gfortran`.

### Experimental evidence and provisional calibration

- Transcribed the two-layer 125-micrometre mesh measurements: 29 measured points from `0.1–2.9 m/s`. The reproduced fit was `Delta p = 13.3676 U + 4.42639 U^2 Pa`, with `RMSE=0.313 Pa` and `R^2=0.999805`.
- Recovered the November 5 packed 40-micrometre-filter data: 21 points from `0–0.20 m/s` and `0–28.4 Pa`.
- The physically constrained Darcy fit was `Delta p = 139.8293 U Pa`, with `RMSE=0.8344 Pa` and `R^2=0.98934`. A free quadratic fit produced a nonphysical negative coefficient, so the provisional model uses `C2=0`.
- Assuming an unverified `10.5 mm` filled thickness gives permeability `1.35916e-9 m^2`, or nondimensional `1.35916e-7`. This is an effective packed-filter assembly value, not an independently validated bead coefficient.

## Grid and geometry study

- Adopted the constant-ratio sequence G1 `192 x 48 x 48`, G2 `384 x 96 x 96`, G3 `768 x 192 x 192`, and conditional G4 `1536 x 384 x 384`, with refinement ratio `r=2`.
- Replaced the circular stick approximation with fractional ellipse coverage. `Rod diameter` is the long `y` axis; input-controlled `Rod thickness` is the short streamwise `x` axis.
- The provisional ellipse uses axes `0.105 x 0.060`. With 4,096 cut-cell samples, G1 area error was `0.0187043%`, and the change from 1,024 samples was `0.0467246%`.
- The combined ellipse/mesh/wall smoke verified eight separate sticks, `4,564` mesh-only cells, all nine walls, CFL `0.00561629`, divergence `3.11723e-13`, and mass error `6.77761e-15`.
- ParaView rendering distinguishes the fractional solver mask from the display-only `0.5` contour and separately renders mesh, walls, pressure, and velocity when available.

## Convergence and production runs

### Startup tests

- Matched 100-step G1–G3 active/control jobs all completed stably. Their early net pressure drops were approximately `4.12`, `2.94`, and `1.75 Pa`.
- These values were rejected for GCI because `t*=0.01` is a startup transient. A longer horizon was required before production.
- A G3 visualization rerun produced a verified 1.4 GB Ensight dataset. It is retained as startup-flow visualization, not a converged result.

### G1 horizon and visualization — November 20

- Active job `2121903` and control `2121904` completed 40,000 steps to `t*=4` in `25:25` and `25:43` on 64 cores.
- Over 10,001 aligned samples from `t*=3–4`, the net mean sheet drop was `223.512215474` nondimensional, about `10.7643 Pa` provisionally. Net range/mean was `0.000447403%`.
- This established `t*=4` and the `t*=3–4` averaging window for all production grids.
- Visualization job `2122903` completed in `24:42` and produced a 26 MB final-time dataset. Rendered views confirmed eight ellipses, separate contours, mesh/walls, pressure drop, and downstream jets.

### G2 production — November 20

- Active job `2123042` and control `2123043` completed in `4:43:01` and `4:47:15` on 64 cores with exit code `0`.
- The aligned `t*=3–4` net mean drop was `286.715485141` nondimensional, about `13.8082 Pa` provisionally. Net range/mean was `0.000233681%`.
- Maximum CFL was `0.028604`, divergence `6.5682e-13`, and mass error `1.2659e-14`. Geometry and failure-marker checks passed.

### G3 production — November 20–22

- Timing job `2123044` completed 100 steps on 128 cores in `2:17` solver time. It indicated about 57 GiB aggregate memory and initially projected a 15.2-hour full run.
- Active job `2128356` completed on node `sc110` in `20:58:35` with exit code `0`. Final CFL was `0.0808682`, divergence `1.05178e-11`, and stick-area error about `-0.00232178%`; no failure markers were found.
- Original control `2128357` was numerically stable but ran about 2.6 times slower on `sc047` (`4.93 s/step`) than the active case (`1.89 s/step`). Its projected runtime was about 55 hours, beyond the 36-hour limit.
- Sol rejected an in-place time-limit extension because the job was already running. Replacement control `2219204` was submitted separately with `sc047` excluded.
- The replacement sustained the expected rate on `sc050` and completed in `20:59:10` with exit code `0`. The slow original was cancelled after `19:17:51` at step 14,068.
- The valid G3 pair passed the `t*=3-4` checks. Net mean drop was `280.380090557` nondimensional, about `13.5031 Pa`, with `0.000356659%` range/mean.
- G1/G2/G3 net drops were `223.512215474`, `286.715485141`, and `280.380090557`. The sign reversal makes standard monotonic GCI invalid. The calculator correctly rejected the oscillatory sequence.
- At the November 23 advisor meeting, G4 was paused in favor of G3 flow-field inspection. Production history showed that `t*=3` is sufficient for visualization (`0.000293%` pressure and `0.127%` transverse-velocity-maximum difference from the mature state). Running 64-core job `2314557` later slowed on `sc051` to about `4.88 s/step`, projecting roughly three hours beyond its 36-hour limit. Slurm rejected a user-level extension. A 128-core, 24-hour hedge `2356718` was submitted with `sc047` and `sc051` excluded while an administrator extension of at least six hours is requested.

## Problems and resolutions

| Problem | Effect | Resolution |
|---|---|---|
| Stock channel had no finite stopping time | Baseline required manual interruption | Thesis case added a finite end time and completion checks |
| `16 x 4 x 2` decomposition violated the FFT requirement | Job `1105006` failed before solver initialization | Changed to `16 x 8 x 1`, leaving one direction undecomposed |
| Earlier G2 result used the wrong topology | Could not support the eight-stick GCI sequence | Repeated G2 with the correct single-layer, eight-stick geometry |
| Initial 128-core jobs waited excessively | Delayed smoke testing | Used 64 cores where measured runtime allowed it; retained 128 cores for G3 |
| Early G1–G3 pressure values changed strongly with grid | Startup transient could be mistaken for grid convergence | Established `t*=4` and averaged only over `t*=3–4` |
| Binary/circular geometry did not represent bulged sticks | Geometry was not physically representative | Added fractional ellipse coverage and input-controlled thickness |
| Walls thinner than a G1 cell were under-resolved | Physical `2 mm` separators could disappear numerically | Enforced a one-cell minimum until the physical thickness is resolved |
| GCI post-processing could misalign samples or accept invalid sequences | Risk of misleading convergence results | Aligned timestep and physical time, added validation, and added six focused tests |
| ParaView pressure/velocity arrays were not always present | Renderer could fail on geometry-only output | Made those renders conditional on array availability |
| G3 timing smoke underestimated full runtime | Initial 15.2-hour estimate was optimistic | Used a 36-hour production limit and monitored sustained throughput |
| Node `sc047` ran G3 control about 2.6 times too slowly | Original control would time out | Submitted isolated retry `2219204` excluding `sc047`; cancelled the slow duplicate only after the retry proved faster |
| The 64-core G3 visualization slowed on `sc051` | Projected runtime exceeded its 36-hour allocation | Submitted 128-core hedge `2356718`, excluded both slow nodes, and requested an administrator time extension for the running job |
| Highest-fidelity G3 production disabled spatial output | Monitors survived, but flow-field inspection required a full rerun | Added a project rule requiring mature 3D fields and durable off-scratch preservation for each new highest-fidelity milestone |
| G1-G3 net pressure sequence was oscillatory | Standard monotonic GCI was mathematically invalid | Calculator rejected the sequence; advisor decision on G4 or alternative uncertainty treatment is pending |
| SSH control sockets became stale or were created from inside Sol | Remote monitoring temporarily failed | Removed stale local socket and created the multiplexed connection from the Mac |

## Current interpretation and limitations

- Active/control pressure differences behave qualitatively as intended: the control removes bead resistance while retaining matched geometry.
- Current pressure results are **calibration-informed, not independent experimental validation**. The permeability was derived from the same packed-filter series used for comparison.
- Filled pocket thickness, seal airtightness, holder/test-section geometry, tap locations, run-to-configuration mapping, air properties, and measurement uncertainty remain incomplete.
- Standard monotonic GCI cannot be reported from the present G1-G3 sequence.
- G4 is on hold while the converged G3 flow fields are inspected. Grid independence remains unclaimed.

## Evidence locations

- Current state and run evidence: `HANDOFF.md`
- Milestones and remaining work: `Thesis/leo_todo_list.md`
- Phase 2 method and completion criteria: `Thesis/Phase2plan.md`
- GCI inputs, scripts, tests, and study notes: `Thesis/simulations/srp_channel/studies/2026-11-11_eight_stick_gci/`
- Equation provenance: `Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md`
- Experimental evidence review: `SupportingDocuments/EVIDENCE_SUMMARY.md`
