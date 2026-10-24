# Finer-Grid Three-Sheet Resistance-Active Run

Purpose: run the provisional three-sheet stack for one flow-through time on the `384 x 96 x 96` mesh as the resistance-active half of the matched finer-grid sensitivity pair. This is a synthetic numerical comparison, not a physical SRP prediction.

- Executable SHA-256: `dc5a0598a4540af36c7095de39def9e672f7c9375339f39350dc62592afa1ac7`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `384 x 96 x 96` / `4 x 1 x 1`
- Resistance: `alpha = 0.01`, `C2 = 0`
- Steps / final time: `2000 / 4`
- Wall-clock interval from the NGA2 log: about `46.5 min`

## Convergence results

Over the final 25% (`t = 3` to `4`):

- Samples: `501`
- Mean total pressure drop: `2.01881049900`
- Total pressure-drop range / mean: `0.0965915%` - pass
- Maximum relative mass-flow error: `4.66380e-14` - pass
- Maximum CFL over the full run: `0.369856` - pass
- Maximum divergence over the full run: `1.95565e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

## Per-sheet pressure

| Sheet | Mean pressure drop | Range / mean |
|---:|---:|---:|
| 1 | `0.227620487026` | `0.000878656%` |
| 2 | `0.217935185629` | `0.00780048%` |
| 3 | `0.210675399202` | `0.0408211%` |

The mean sheet-drop sum and sampled stack drop are both `0.656230930140`. Maximum closure error is `2.20901e-16`.

## Per-sheet flow distribution

| Downstream of sheet | Mean band fractions | Mean P7 CV | CV range / mean |
|---:|---|---:|---:|
| 1 | `0.180379 / 0.319621 / 0.306713 / 0.193287` | `0.253981802395` | `0.00157492%` |
| 2 | `0.176786 / 0.323214 / 0.310389 / 0.189611` | `0.268434594810` | `0.00968579%` |
| 3 | `0.173996 / 0.326004 / 0.313235 / 0.186765` | `0.279645640719` | `0.0461298%` |

Every plane has mass-flow sum `0.999815` and fraction sum `1.0`. The 90-cell open span is not divisible by four bands, so the fine-grid bands do not preserve exact paired symmetry. Interpret P7 grid changes only after subtracting the matched fine-grid control; pressure comparisons are unaffected by this band-count issue.

## Matched control and grid sensitivity

The matched fine-grid zero-resistance control also completed normally. Subtracting it gives:

| Corrected quantity | Fine | Target | Project Eq. P15 target-to-fine change |
|---|---:|---:|---:|
| Total excess pressure drop | `0.136410538922` | `0.142539081836` | `4.49272%` |
| Sheet 1 local pressure increment | `0.032471768463` | `0.034016007984` | `4.75564%` |
| Sheet 2 local pressure increment | `0.040393670659` | `0.042172576846` | `4.40392%` |
| Sheet 3 local pressure increment | `0.044265325349` | `0.046317219561` | `4.63544%` |
| Sheet 1 P7 CV change | `-0.007432313373` | `-0.008178111776` | `10.0345%` |
| Sheet 2 P7 CV change | `-0.010921227545` | `-0.012072760479` | `10.5440%` |
| Sheet 3 P7 CV change | `-0.011863766467` | `-0.013142085828` | `10.7750%` |

The resistance-active case reduces P7 CV relative to its fine-grid control by `2.84312%`, `3.90943%`, and `4.06977%` after sheets 1-3. The sign of every earlier conclusion is preserved.

The corrected pressure sequence is non-monotonic: the coarse and fine values differ by only `0.326755%` for total excess pressure and at most `0.918400%` for local sheet increments, while the target values are about `4.4-4.8%` above the fine values. The corrected P7 changes differ by `10.0-10.8%` between target and fine and by `6.88-8.59%` between coarse and fine. Formal grid independence is therefore not established. Before another expensive run, inspect the grid-dependent rod-mask representation and replace integer-cell flow bands with physically fixed or fractionally weighted band boundaries.
