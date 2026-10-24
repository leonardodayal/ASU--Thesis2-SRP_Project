# Target-Grid Three-Sheet Time-Step Sensitivity

Purpose: repeat the provisional resistance-active three-sheet stack with half the original maximum timestep. This is a synthetic numerical-sensitivity case, not a physical SRP prediction.

- Code revision before the run: `61dfbdd`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Original / smaller maximum timestep: `0.002 / 0.001`
- All other physical, geometry, sampling, and resistance inputs: unchanged
- Steps / final time: `4000 / 4`
- Wall-clock interval from the NGA2 log: about `1,657 s`
- Working acceptance criterion declared before the run: less than `1%` change in total pressure drop, per-sheet pressure drop, and per-sheet P7 CV

## Convergence results

Over the final 25% (`t = 3` to `4`):

- Samples: `1,001`
- Mean total pressure drop: `1.95186987013`
- Total pressure-drop range / mean: `0.104003%` — pass
- Maximum relative mass-flow error: `1.99923e-14` — pass
- Maximum CFL over the full run: `0.122065` — pass
- Maximum divergence over the full run: `2.66620e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

The mean sheet-drop sum and sampled stack drop are both `0.650795688312`; maximum closure error is `1.70616e-16`. Every sheet-flow plane has mass-flow sum `0.999583`, fraction sum `1.0`, and paired-band symmetry at monitor precision.

## Time-step comparison

The relative change uses the smaller-timestep value as the denominator.

| Quantity | `dt = 0.002` | `dt = 0.001` | Relative change |
|---|---:|---:|---:|
| Total pressure drop | `1.94622081836` | `1.95186987013` | `0.289417%` |
| Sampled stack drop | `0.649667976048` | `0.650795688312` | `0.173282%` |
| Sheet 1 pressure drop | `0.224763616766` | `0.225166761239` | `0.179043%` |
| Sheet 2 pressure drop | `0.215792808383` | `0.216168063936` | `0.173594%` |
| Sheet 3 pressure drop | `0.209111606786` | `0.209460717283` | `0.166671%` |
| Sheet 1 P7 CV | `0.246710365269` | `0.247222141858` | `0.207011%` |
| Sheet 2 P7 CV | `0.260803838323` | `0.261329227772` | `0.201045%` |
| Sheet 3 P7 CV | `0.271920133733` | `0.272449068931` | `0.194141%` |

Every declared comparison is below `0.3%`, so the representative target-grid result passes the `1%` working time-step-sensitivity criterion.
