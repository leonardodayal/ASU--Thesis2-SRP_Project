# Finer-Grid Three-Sheet Zero-Resistance Control

Purpose: provide the matched `384 x 96 x 96` zero-resistance baseline for the full finer-grid three-sheet sensitivity pair. This is a numerical control, not a physical SRP prediction.

- Executable SHA-256: `dc5a0598a4540af36c7095de39def9e672f7c9375339f39350dc62592afa1ac7`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Geometry, sampling, timestep, and end time: identical to `../2026-10-20_stacked_three_sheet_fine`
- Control resistance: `alpha = 1e30`, `C2 = 0`
- Steps / final time: `2000 / 4`
- Wall-clock interval from the NGA2 log: about `61.3 min`

## Convergence results

Over the final 25% (`t = 3` to `4`):

- Samples: `501`
- Mean total pressure drop: `1.88239996008`
- Total pressure-drop range / mean: `0.111560%` - pass
- Maximum relative mass-flow error: `4.80816e-14` - pass
- Maximum CFL over the full run: `0.374454` - pass
- Maximum divergence over the full run: `1.96232e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

| Sheet plane | Mean local pressure drop | Mean downstream P7 CV |
|---:|---:|---:|
| 1 | `0.195148718563` | `0.261414115768` |
| 2 | `0.177541514970` | `0.279355822355` |
| 3 | `0.166410073852` | `0.291509407186` |

The local drops sum to the sampled stack drop `0.539100542914`; maximum closure error is `2.17200e-16`. The active-minus-control results and grid comparison are documented in `../2026-10-20_stacked_three_sheet_fine/README.md`.
