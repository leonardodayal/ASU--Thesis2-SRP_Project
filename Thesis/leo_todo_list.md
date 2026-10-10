# To-Do List (Leonardo Dayal)

Based on the meeting with Justin Flory and Marcus Herrmann.

**Priority:** Get the pure-flow pressure drop simulation running first. It can run on the side while the adsorption model is worked out.

## Progress snapshot (2026-10-10)

- **Completed:** NGA2 has been built and successfully run with MPI using the stock channel example.
- **Completed:** The radial paper's introduction, literature overview, and governing adsorption equations have been reviewed and documented in [SRP_CO2_COLLECTOR_EQUATION_SHEET.md](./SRP_CO2_COLLECTOR_EQUATION_SHEET.md).
- **Partial:** A baseline channel run exists, but it is the stock 2D periodic, body-force-driven case (`128 x 40 x 1`), not the required 3D SRP inflow/outflow channel.
- **Next milestone:** Create a separate 3D Cartesian SRP case with explicit inflow and outflow, first without porous rods.
- **Current blockers:** Rod-orientation priorities and Justin's through-sheet pressure-drop data are still outstanding.

## 1. Get set up

- [x] Install NGA2 and make sure it's ready to run.
  - Verified by the compiled channel executable and the documented MPI baseline run in `NGA2/examples/channel/runs/2026-10-05_baseline/`.

## 2. Build the first simulation (pressure drop)

- [ ] Set up a 3D Cartesian mesh channel, about 64 x 64 x 256 cells, small enough to run on a laptop or desktop.
  - **Partial:** The stock `128 x 40 x 1` channel case has been built and run; a separate 3D SRP case has not been created.
- [ ] Run it first as a pure open channel with inflow and outflow.
  - **Partial:** The stock periodic, body-force-driven channel ran successfully to simulation time `425.34` with maximum CFL about `0.764`. Explicit inflow/outflow boundaries remain to be implemented and verified.
- [ ] Add a porous-medium region by modeling the bead rods as cells with lower permeability than the surrounding open space.
- [ ] Use Darcy's law for the resistance, along with the correction one of the papers used for bead structures.
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
