# Provisional Aligned Four-Rod Target-Mesh Smoke Test

Purpose: verify the configurable `aligned_rods_z` porous mask and solver path on the target mesh. This geometry is a provisional reference, not an advisor-selected or dimensionally confirmed SRP configuration. Its synthetic permeability must not be used for physical conclusions.

- Base code revision: `e3272a0`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Rod axes: `z`
- Rod count / diameter / first-to-last center span: `4 / 0.1 / 0.6`
- Rod centers: `x = 2`; `y = -0.3, -0.1, 0.1, 0.3`
- Provisional resistance: `alpha = 0.01`, `C2 = 0`
- Steps / final time / runtime: `10 / 0.02 / 3.34909 s`

## Mask verification

ParaView's EnSight reader reported:

- mask range: `0` to `1`;
- four separated `y` groups;
- `7,680` porous cells;
- six cells across each rod diameter in `x`;
- six cells across each rod diameter in `y`; and
- 60 porous cells along `z`, matching the open passage and excluding all wall-padding cells.

The porous-cell-center bounds are `x = 1.9609375` to `2.0390625`, `y = -0.34166667` to `0.34166667`, and `z = -0.49166666` to `0.49166666`.

## Solver smoke-test result

- Final CFL: `0.142256`
- Final maximum divergence: `2.26618e-13`
- Final relative mass-flow error: `9.99617e-16`
- Pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found
- Result: pass for geometry construction and short-time numerical stability.

The run is too short for convergence, and its provisional pressure drop is not a physical result.
