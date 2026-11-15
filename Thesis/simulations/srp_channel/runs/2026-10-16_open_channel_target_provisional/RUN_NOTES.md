# Provisional Converged Open-Channel Run

Purpose: test numerical convergence of the target-mesh empty channel before confirmed dimensional inputs are available. This is not a physical pressure-drop prediction and must not be compared with the `10 Pa` project target.

- Code revision before the run: `131a26f2919d3534d95ee96a0d458689ac55754b`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / MPI decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Provisional inputs: `Lx = 4`, `Ly = Lz = 1`, `rho = 1`, `mu = 0.01`, `Uin = 1`
- Flow-through time: `Lx/Uin = 4`
- Steps / final time: `2000 / 4`
- Wall-clock runtime reported by NGA2: `780.771 s`

## Predeclared convergence rule

After at least one flow-through time, evaluate the final 25% of the run (`t = 3` to `4`). Require:

1. pressure-drop range divided by its mean no greater than `1%`;
2. relative inlet/outlet mass-flow error no greater than `1e-10`;
3. maximum CFL no greater than the configured limit of `0.8`; and
4. finite, bounded divergence and pressure-solver diagnostics.

## Results

- Final-window samples: `501`
- Mean pressure drop: `1.80368173653` (provisional nondimensional value)
- Pressure-drop minimum / maximum: `1.80196 / 1.80418`
- Pressure-drop range / mean: `0.00123082` (`0.123082%`) — pass
- Maximum final-window relative mass-flow error: `1.84374e-14` — pass
- Maximum CFL over the full run: `0.247208` — pass
- Maximum divergence over the full run: `2.65364e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found
- Result: the provisional target-mesh empty channel meets the numerical convergence rule.

The confirmed physical dimensions, air properties, inlet condition, and pressure-tap locations remain required before this can become the quantitative empty-channel baseline.
