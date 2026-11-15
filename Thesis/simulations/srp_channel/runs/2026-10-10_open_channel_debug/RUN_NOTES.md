# Open-Channel Debug Run

Purpose: verify the empty 3D inflow/outflow implementation on a small four-rank mesh before running the target mesh.

- Branch: `CodexAttempt1`
- Mesh: `32 x 12 x 12`
- MPI decomposition: `4 x 1 x 1`
- Steps/final time: `4 / 0.02`
- Final CFL: `0.0419867` (configured maximum `0.8`)
- Final maximum divergence: `2.20e-14`
- Final inlet/outlet mass-flow rates: `0.976563 / 0.976562`
- Final relative mass-flow error: `1.82e-15`
- Result: completed normally with finite monitor values.

The dimensions, properties, and inlet velocity are provisional nondimensional smoke-test inputs. The reported transient pressure drop is not a physical prediction.

Run from this directory with:

```sh
mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input
```
