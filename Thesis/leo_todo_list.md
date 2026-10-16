# To-Do List (Leonardo Dayal)

Based on the meeting with Justin Flory and Marcus Herrmann.

**Priority:** Get the pure-flow pressure drop simulation running first. It can run on the side while the adsorption model is worked out.

## Progress snapshot (2026-10-16)

- **Completed:** NGA2 has been built and successfully run with MPI using the stock channel example.
- **Completed:** The radial paper's introduction, literature overview, and governing adsorption equations have been reviewed and documented in [SRP_CO2_COLLECTOR_EQUATION_SHEET.md](./SRP_CO2_COLLECTOR_EQUATION_SHEET.md).
- **Completed:** A separate thesis-owned 3D SRP case now builds and completes finite MPI smoke tests with explicit inflow/outflow on debug and target `256 x 64 x 64` meshes.
- **Completed:** The target-mesh Ensight output has been opened and inspected successfully in ParaView, including the fluid passage, velocity, pressure, and wall-volume-fraction fields.
- **Completed:** The provisional target-mesh setup ran for one flow-through time and met its documented numerical convergence rule; this is not yet a physical pressure-drop prediction.
- **Completed:** A Darcy-only porous slab and exported mask reproduce the uniform analytical pressure drop exactly within printed precision.
- **Completed:** The Forchheimer term independently reproduces its uniform analytical pressure drop exactly within printed precision.
- **Next milestone:** Fit permeability and inertial resistance when Justin's pressure-drop data arrive, then replace the slab with bead-rod geometry.
- **Current blockers:** Confirmed contactor dimensions/operating conditions, rod-orientation priorities, and Justin's through-sheet pressure-drop data are still outstanding.

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
- [ ] Place 4 or 5 rods across the 64-cell width.
- [ ] Try several arrangements: same orientation, rotated 90 degrees, offset, or angled.
- [ ] Get the flow path and overall pressure drop from each.

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

- **Justin:** pressure-drop data for flow *through* the sheet (empty sheets and sheets with beads), needed soon for Darcy's law. Other configurations (along the sheet) come later.
- **Justin (possible):** small wind-tunnel experiment on the box of beads for system-level validation.
- **Sherry:** follow-up note to be sent.
