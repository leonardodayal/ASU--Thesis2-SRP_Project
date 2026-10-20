# Provisional Converged Four-Rod Run

Purpose: apply the verified flow-split diagnostic to the provisional aligned four-rod geometry for one flow-through time. The geometry and resistance are synthetic and this is not a physical SRP prediction.

- Code revision before the run: `b4ef3e2`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / MPI decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Provisional inputs: `Lx = 4`, `Ly = Lz = 1`, `rho = 1`, `mu = 0.01`, `Uin = 1`
- Rods: four `aligned_rods_z`, diameter `0.1`, center span `0.6`, sheet plane `x = 2`
- Synthetic resistance: `alpha = 0.01`, `C2 = 0`
- Flow-split plane / bands: `x = 3` / four equal-width `y` bands
- Steps / final time: `2000 / 4`
- Wall-clock interval from the NGA2 log: about `836 s`

## Predeclared convergence rule

The final 25% (`t = 3` to `4`) uses the same rule as the provisional open-channel run: pressure-drop range/mean no greater than `1%`, relative mass-flow error no greater than `1e-10`, maximum CFL no greater than `0.8`, and finite/bounded solver diagnostics.

## Results

- Final-window samples: `501`
- Mean total pressure drop: `1.85157273453`
- Pressure-drop minimum / maximum: `1.84989 / 1.85206`
- Pressure-drop range / mean: `0.117198%` — pass
- Mean sample-plane pressure drop: `0.755875359281`
- Maximum final-window relative mass-flow error: `1.91038e-14` — pass
- Maximum CFL over the full run: `0.246105` — pass
- Maximum divergence over the full run: `2.61609e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

The final-window mean band fractions were `0.178337974052`, `0.321662025948`, `0.321662025948`, and `0.178337974052`. The band sums matched inlet mass flow exactly at monitor precision. Mean P7 coefficient of variation was `0.286648125749`; its final-window range/mean was `0.103262%`.

The symmetric band pairs confirm that the aligned geometry and diagnostic preserve cross-channel symmetry. The matched converged open-channel run has mean P7 CV `0.289742902196`, so the rods reduce CV by `0.003094776447` (`1.06811%`) while increasing total pressure drop by `0.047890998` (`2.65518%`). This specific synthetic arrangement therefore makes the four-band split slightly more uniform at the cost of pressure loss.

For context only, the earlier provisional open-channel mean total pressure drop was `1.80368173653`; this rod case is higher by `0.047890998` (`2.65518%`). Because all dimensions and the Darcy coefficient remain synthetic, neither value may be compared with the physical `10 Pa` design target.
