# To-Do List (Leonardo Dayal)

Based on the meeting with Justin Flory and Marcus Herrmann.

**Priority:** Get the pure-flow pressure drop simulation running first. It can run on the side while the adsorption model is worked out.

## Progress snapshot (2026-10-19)

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
- **Completed:** A calibration-ready fitting tool now handles baseline subtraction, independent measurement/baseline uncertainties, calibration/validation splits, and Project Eqs. P1-P2 conversion. It recovers known synthetic `alpha` and `C2` values to floating-point precision, including a held-out validation point.
- **Completed:** Nine multi-velocity NGA2 slab cases verify the linear Darcy term, quadratic Forchheimer term, and their sum at velocities `0.5`, `1`, and `2`; all final-window pressure drops match Project Eq. P1 within printed precision.
- **Completed:** A configurable downstream flow-split monitor reports equal-width band mass-flow rates, fractions, and Project Eq. P7 maldistribution. Its four-band MPI test conserves the total flow at monitor precision, preserves symmetry, and historical inputs retain one-band defaults.
- **Completed:** A one-flow-through provisional four-rod run passes the numerical convergence rule and produces stable, symmetric four-band results. Its absolute CV includes wall-profile effects and is not yet an isolated rod contribution.
- **Next milestone:** Run the matching converged open-channel four-band baseline, then add configurable stacked-sheet geometry while awaiting the physical inputs.
- **Current blockers for physical predictions:** Confirmed contactor dimensions/operating conditions, rod-orientation priorities, and calibration-quality empty-mesh and bead-filled-sheet data are still outstanding.

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
- [x] Add a verified porous-medium test region with lower permeability than the surrounding open space. Bead-rod geometry remains pending.
- [x] Implement and independently verify the Darcy and Forchheimer resistance terms used by the radial paper. Physical coefficients still require Justin's data.
- [x] Place a provisional four-rod aligned reference across the 64-cell width; replace its dimensions if advisor values differ.
- [ ] Try several arrangements: same orientation, rotated 90 degrees, offset, or angled.
- [ ] Get the flow path and overall pressure drop from each.
- [x] Add and verify equal-width downstream flow-split and maldistribution monitoring; geometry-specific rod/sheet comparisons remain pending.
  - The provisional aligned four-rod case has now been run to numerical convergence. A matching converged open-channel flow-split baseline is still needed to isolate the rods' incremental effect.

## 3. Literature review (with Marcus)

- [x] Read the intro and literature overview of the radial paper, the first one Justin sent.
  - Reviewed the modeling alternatives, assumptions, limitations, and cited basis for LDF kinetics, Toth equilibrium, Ergun resistance, and non-equilibrium heat transfer.
- [x] Note how it models CO2 adsorption, since its results showed CO2 profiles inside the bead material.
  - Documented the paper's original Eqs. (1)-(27), explicit SRP/NGA2 adaptations, and project-added equations in [SRP_CO2_COLLECTOR_EQUATION_SHEET.md](./SRP_CO2_COLLECTOR_EQUATION_SHEET.md).
- [ ] Check the papers it cites to see whether that model applies to these specific beads.

## 4. Later, once the flow setup is running

- [ ] Add the CO2, moisture, and temperature equations on top of the flow model as a source term.
- [ ] Treat regeneration with humid air as the same submodel with the sign flipped, driven by the water concentration difference between the beads and outside.
- [ ] Compare against Justin's experimental pressure drop, then explore packing density, spacing, and thickness.

## Things to confirm

- [ ] Ask Marcus which rod orientations he wants first (he only suggested options).

## Waiting on others

- **Justin/experimental team:** raw pressure-drop data and metadata for flow *through* the empty holder, empty mesh, and bead-filled sheets. A measurement request is active for 2026-10-23; other configurations with flow along normally mounted packets come later.
- **Justin (possible):** small wind-tunnel experiment on the box of beads for system-level validation.
- **Sherry:** follow-up note to be sent.
