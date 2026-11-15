# Matched Open-Channel Flow-Split Baseline

Purpose: provide a converged four-band baseline matched to the provisional four-rod run so wall-profile and rod effects can be separated. All dimensions remain synthetic and this is not a physical SRP prediction.

- Code revision before the run: `100e87c`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / MPI decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Provisional inputs: `Lx = 4`, `Ly = Lz = 1`, `rho = 1`, `mu = 0.01`, `Uin = 1`
- Porous source: disabled by equal slab bounds at `x = 2`
- Flow-split plane / bands: `x = 3` / four equal-width `y` bands
- Steps / final time: `2000 / 4`
- Wall-clock interval from the NGA2 log: about `719 s`

## Convergence results

Over the final 25% (`t = 3` to `4`):

- Final-window samples: `501`
- Mean total pressure drop: `1.80368173653`
- Pressure-drop minimum / maximum: `1.80196 / 1.80418`
- Pressure-drop range / mean: `0.123082%` — pass
- Mean sample-plane pressure drop: `0.711502554890`
- Maximum relative mass-flow error: `1.78820e-14` — pass
- Maximum CFL over the full run: `0.247208` — pass
- Maximum divergence over the full run: `2.60354e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

The mean band fractions were `0.177564269461`, `0.322435730539`, `0.322435730539`, and `0.177564269461`. Mean P7 coefficient of variation was `0.289742902196`, with final-window range/mean `0.106646%`. The exact band-pair symmetry confirms that most of this absolute CV is the wall-bounded channel profile rather than geometric asymmetry.

## Matched rod comparison

Relative to this baseline, the provisional aligned four rods:

- increase mean total pressure drop by `0.047890998` (`2.65518%`);
- increase mean sample-plane pressure drop by `0.044372804391` (`6.23649%`);
- reduce mean P7 CV by `0.003094776447` (`1.06811%`); and
- move `0.0773705` percentage points of total flow into each outer band, with the same amount removed from each inner band.

The rods therefore make this specific synthetic four-band split slightly more uniform while adding pressure loss. This is a numerical comparison only; it does not establish physical SRP performance or preferred rod geometry.
