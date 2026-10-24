# SRP CO2 Collector Modeling

This repository supports an ASU thesis project developing and validating an NGA2 computational-fluid-dynamics model of SRP's porous bead-rod CO2 collector.

The current model focuses on airflow, pressure drop, and flow distribution. CO2 adsorption, moisture, temperature, and regeneration are later phases. Geometry, operating conditions, and porous-resistance values in the current simulations are provisional unless a document explicitly identifies them as measured or validated.

## Start here

- [SETUP.md](SETUP.md): install requirements and run the native or Docker workflows.
- [HANDOFF.md](HANDOFF.md): current project status, verified results, blockers, and the immediate next task.
- [Thesis/leo_todo_list.md](Thesis/leo_todo_list.md): working checklist and milestones.
- [Thesis/Phase2plan.md](Thesis/Phase2plan.md): Phase 2 scope, validation criteria, and execution plan.
- [Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md](Thesis/SRP_CO2_COLLECTOR_EQUATION_SHEET.md): equation provenance and project-specific adaptations.

## Repository map

| Location | Contents |
| --- | --- |
| `Thesis/simulations/srp_channel/` | Thesis-owned NGA2 channel model, inputs, tools, and preserved runs |
| `Thesis/simulations/srp_channel/SIMULATION_GUIDE.md` | Model implementation, numerical evidence, and simulation-specific notes |
| `OtherResearch/` | Research papers and notes on reusable methods |
| `SupportingDocuments/` | Experimental correspondence, measurements, and supporting sources |
| `NGA2/` | External NGA2 checkout used to build native simulations |

The `NGA2/` directory is intentionally a separate Git repository and is not tracked by this repository. A fresh checkout of this project therefore requires NGA2 to be cloned separately; see [SETUP.md](SETUP.md).

## Current state

The 3D channel, Darcy-Forchheimer resistance, provisional rod-sheet geometries, pressure diagnostics, and flow-split diagnostics are implemented and numerically verified. A corrected target grid has been accepted for provisional aligned-stack comparisons.

The model is not yet a physical SRP pressure-drop prediction. Confirmed geometry, experimental metadata, baseline-corrected bead-filled measurements, and advisor-selected arrangements are still required for calibration and validation. See [HANDOFF.md](HANDOFF.md) for the latest evidence and blockers.

## Working with results

Preserved simulation directories contain a `RUN_NOTES.md` file alongside their inputs, monitors, and outputs. Treat synthetic verification, provisional numerical comparisons, and experimental validation as separate evidence classes.

