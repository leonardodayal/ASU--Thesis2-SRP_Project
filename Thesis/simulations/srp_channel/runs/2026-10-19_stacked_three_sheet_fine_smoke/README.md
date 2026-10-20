# Finer-Grid Three-Sheet Feasibility Smoke Test

Purpose: verify that a finer-than-target provisional stack fits in memory, resolves the rod masks as intended, and advances stably before committing to a full matched active/control grid-sensitivity pair. This short transient is not a converged result or physical SRP prediction.

- Code revision before the run: `61dfbdd`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `384 x 96 x 96` / `4 x 1 x 1`
- Wall padding: three cells, preserving the target mesh's physical padding thickness
- Resistance: `alpha = 0.01`, `C2 = 0`
- Steps / final time: `10 / 0.02`
- Wall-clock interval from the NGA2 log: about `16 s`, including startup and final field output

## Geometry and numerical checks

- Each sheet occupies 10 separated streamwise cell columns.
- Each circular rod cross-section contains 72 `x-y` cell centers, close to the continuous-area expectation at this resolution.
- With 90 open spanwise cells, each sheet contains `25,920` porous cells.
- All three sheets have identical counts, remain separated by 48 streamwise cells center-to-center, and exclude wall-padding cells.
- Final relative mass-flow error: `1.73227e-14`
- Final maximum CFL: `0.219908`
- Final maximum divergence: `1.08864e-13`
- Final pressure iterations / reported error: `1 / 0`
- Sheet-pressure closure error: `0` at monitor precision
- NaN, infinity, fatal-error, and solver-failure scan: none found

The run successfully allocates and completes on four local MPI ranks. Scaling the target run by cell count projects about `41.4 min` per full run; directly extrapolating this short smoke test gives about `53.3 min`. A full matched active/control pair should therefore be budgeted at roughly `83–107 min`, excluding analysis.
