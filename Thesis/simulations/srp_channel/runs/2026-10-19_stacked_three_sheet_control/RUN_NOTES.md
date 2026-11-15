# Matched Zero-Resistance Three-Sheet Control

Purpose: isolate the background streamwise wall-profile contribution at the same geometry and sampling planes as the provisional resistance-active three-sheet stack. This is a numerical control, not a physical SRP prediction.

- Code revision: `f76f9be`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Geometry and sampling: identical to `2026-10-19_stacked_three_sheet_provisional`
- Control resistance: `alpha = 1e30`, `C2 = 0`
- Steps / final time: `2000 / 4`
- Wall-clock interval from the NGA2 log: about `769 s`

## Convergence results

Over the final 25% (`t = 3` to `4`):

- Samples: `501`
- Mean total pressure drop: `1.80368173653`
- Total pressure-drop range / mean: `0.123082%` — pass
- Maximum relative mass-flow error: `1.93259e-14` — pass
- Maximum CFL over the full run: `0.247208` — pass
- Maximum divergence over the full run: `2.72950e-13`
- Maximum pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found

The mean total pressure drop exactly matches the earlier open-channel mean at monitor precision. The zero-resistance sheet masks therefore add no measurable numerical resistance.

## Matched control values

| Sheet plane | Mean local pressure drop | Mean downstream P7 CV |
|---:|---:|---:|
| 1 | `0.190747608782` | `0.254888477046` |
| 2 | `0.173620231537` | `0.272876598802` |
| 3 | `0.162794387226` | `0.285062219561` |

The local drops sum to the sampled stack drop `0.527162355289`; maximum closure error is `2.10644e-16`. Every downstream plane has mass-flow sum `0.999583`, fraction sum `1.0`, and paired-band symmetry at monitor precision.

## Resistance-active minus control comparison

| Plane | Added local pressure drop | P7 CV change | Relative P7 CV change |
|---:|---:|---:|---:|
| 1 | `0.034016007984` | `-0.008178111777` | `-3.20851%` |
| 2 | `0.042172576846` | `-0.012072760479` | `-4.42426%` |
| 3 | `0.046317219560` | `-0.013142085828` | `-4.61025%` |

The three local increments sum to `0.122505620759`, accounting for `85.9453%` of the total inlet-to-outlet excess pressure drop `0.142539081830`. The remaining excess lies outside the local sheet sampling intervals because the resistance changes the surrounding pressure field.

The raw downstream increase in CV occurs in both cases and is therefore primarily streamwise wall-profile development. Relative to the matched control, the provisional resistance-active sheets reduce CV at every sampled downstream plane. These values remain synthetic and cannot be treated as physical design findings.
