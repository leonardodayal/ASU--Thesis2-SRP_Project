# Corrected Fine-Grid Three-Sheet Run

Purpose: evaluate target-to-fine convergence after fractional rod geometry, physical flow-band integration, and interpolated pressure/velocity sampling. This is the resistance-active half of a matched active/control pair.

- Executable SHA-256: `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `384 x 96 x 96` / `4 x 1 x 1`
- Resistance: `alpha = 0.01`, `C2 = 0`
- Steps / final time: `2000 / 4`
- Ensight output: disabled
- Wall time: about `63.0 min`
- Final-window samples: `501` over `t = 3` to `4`

## Corrected active-minus-control results

| Quantity | Fine value | Project Eq. P15 target-to-fine change | Working gate |
|---|---:|---:|---:|
| Total excess pressure drop | `0.124160157685` | `1.35643%` | `2%` |
| Sheet 1 pressure increment | `0.032321866267` | `1.45490%` | `2%` |
| Sheet 2 pressure increment | `0.040273886228` | `1.41316%` | `2%` |
| Sheet 3 pressure increment | `0.044128461078` | `1.21755%` | `2%` |
| Sheet 1 P7 CV change | `-0.007520493014` | `2.04532%` | `5%` |
| Sheet 2 P7 CV change | `-0.011054329341` | `2.51561%` | `5%` |
| Sheet 3 P7 CV change | `-0.012022251497` | `2.57712%` | `5%` |

The target-to-fine comparison passes every working gate. The corrected coarse, target, and fine values are monotonic, identifying the coarse grid as pre-asymptotic under these criteria. The target grid is therefore accepted for the provisional aligned-stack studies; this is a numerical sensitivity result, not physical validation.

## Fine-pair numerical checks

The active and matched control both terminated normally at `t = 4`. Across the pair, maximum relative mass-flow error is `5.11908e-14`, maximum CFL is `0.374454`, maximum divergence is `1.92513e-13`, maximum pressure iterations are `1` with zero reported pressure error, and maximum sheet-pressure closure error is `2.21644e-16`. The largest final-window total-pressure range/mean is `0.0345973%`. No NaN, infinity, fatal-error, or solver-failure condition was observed.

The fine active P7 CV values are `0.252607586826`, `0.267116806387`, and `0.278365015968`; the matched control values are `0.260128079840`, `0.278171135729`, and `0.290387267465`. Resistance therefore reduces P7 CV by `2.89107%`, `3.97393%`, and `4.14008%` relative to the fine control.
