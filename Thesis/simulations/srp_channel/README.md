# SRP Channel Simulation

This directory contains the thesis-owned NGA2 case for the Phase 2 pressure-drop simulation. NGA2 remains an external source dependency in the repository-level `NGA2/` directory.

## Status

The directory and build configuration are scaffolded, but the solver is not implemented yet. The files in `src/` are explicit placeholders and the case is not expected to compile until the empty 3D inflow/outflow channel is implemented.

## Intended layout

- `GNUmakefile`: builds the case against `../../../NGA2`.
- `input`: case parameters; currently contains only the target mesh and a provisional MPI partition.
- `src/`: thesis-owned Fortran source and its NGA2 package list.
- `runs/`: dated run inputs, logs, monitors, and field outputs.

## Planned first milestone

Implement and verify an empty `256 x 64 x 64` Cartesian channel with flow along `x`, explicit inflow and outflow, and solid cross-section walls. Physical dimensions and operating conditions must be confirmed before a quantitative run.

Build commands will be documented here once the initial solver implementation is complete.
