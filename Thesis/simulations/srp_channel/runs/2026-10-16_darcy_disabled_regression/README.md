# Darcy-Disabled Channel Regression

Purpose: confirm that the production positive-wall-padding path still behaves normally when the porous slab is disabled by equal bounds.

- Base code revision: `c304399`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `32 x 12 x 12` / `4 x 1 x 1`
- Wall padding: `2` cells
- Steps / final time: `4 / 0.02`
- Final CFL: `0.0419867`
- Final maximum divergence: `2.20256e-14`
- Final relative mass-flow error: `1.81899e-15`
- NaN, infinity, fatal-error, and solver-failure scan: none found
- Result: pass.
