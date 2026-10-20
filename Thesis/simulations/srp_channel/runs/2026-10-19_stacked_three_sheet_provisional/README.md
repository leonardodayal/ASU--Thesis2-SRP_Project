# Provisional Converged Three-Sheet Stack

Purpose: advance the synthetic three-sheet stack through one flow-through time and evaluate final-window total/per-sheet pressure and per-sheet flow maldistribution. This is not a physical SRP prediction.

- Code revision before the run: `da58a17`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Sheets: three centers at `x = 1.5`, `2.0`, and `2.5`; four aligned rods per sheet
- Synthetic resistance: `alpha = 0.01`, `C2 = 0`
- Steps / final time: `2000 / 4`
- Wall-clock interval from the NGA2 log: about `736 s`

## Convergence results

Over the final 25% (`t = 3` to `4`):

- Samples: `501`
- Mean total pressure drop: `1.94622081836`
- Total pressure-drop range / mean: `0.105332%` — pass
- Maximum relative mass-flow error: `1.92149e-14` — pass
- Maximum CFL over the full run: `0.243918` — pass
- Maximum divergence over the full run: `2.63684e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

## Per-sheet pressure

| Sheet | Mean pressure drop | Range / mean |
|---:|---:|---:|
| 1 | `0.224763616766` | `0.000889824%` |
| 2 | `0.215792808383` | `0.00880474%` |
| 3 | `0.209111606786` | `0.0430392%` |

The mean sheet-drop sum and sampled stack drop are both `0.649667976048`. Maximum closure error is `1.70911e-16`.

## Per-sheet flow distribution

| Downstream of sheet | Mean band fractions, outer / inner / inner / outer | Mean P7 CV | CV range / mean |
|---:|---|---:|---:|
| 1 | `0.188322 / 0.311678 / 0.311678 / 0.188322` | `0.246710365269` | `0.00162133%` |
| 2 | `0.184799 / 0.315201 / 0.315201 / 0.184799` | `0.260803838323` | `0.0107360%` |
| 3 | `0.182020 / 0.317980 / 0.317980 / 0.182020` | `0.271920133733` | `0.0514857%` |

Every plane has mass-flow sum `0.999583`, fraction sum `1.0`, and exact paired-band symmetry at monitor precision.

Relative to the earlier matched open-channel total pressure drop, the three-sheet case adds `0.14253908183` (`7.90267%`). This is `2.97632` times the provisional single-sheet increment, so the synthetic total-pressure penalty is nearly linear with sheet count. The decreasing sheet drops and increasing downstream CV are resolved numerical trends, but they cannot yet be attributed solely to porous sheets because the wall-bounded profile also develops with `x`. A converged zero-resistance stack control using the same three sampling planes is required for that separation.
