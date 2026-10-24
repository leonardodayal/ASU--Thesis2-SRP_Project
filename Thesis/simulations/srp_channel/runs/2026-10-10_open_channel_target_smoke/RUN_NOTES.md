# Open-Channel Target-Mesh Smoke Run

Purpose: verify that the empty 3D inflow/outflow implementation advances and terminates on the requested target mesh.

- Branch: `CodexAttempt1`
- Mesh: `256 x 64 x 64`
- MPI decomposition: `4 x 1 x 1`
- Steps/final time: `10 / 0.02`
- Final CFL: `0.142256` (configured maximum `0.8`)
- Final maximum divergence: approximately `2.1e-13`
- Final inlet/outlet mass-flow rates: `0.999583 / 0.999583`
- Final relative mass-flow error: approximately `7e-15`
- Result: completed normally with finite monitor values.

The dimensions, properties, and inlet velocity are provisional nondimensional smoke-test inputs. The reported transient pressure drop is not a physical prediction or a comparison with the project's `10 Pa` target.

Run from this directory with:

```sh
mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input
```
