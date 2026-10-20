# Corrected Target-Grid Fractional-Geometry Pair

Purpose: repeat the full-duration target active/control comparison after making rod area, band boundaries, and sampling planes physically consistent across grids. This remains a synthetic numerical case.

- Executable SHA-256: `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`
- Mesh: `256 x 64 x 64`
- Active resistance: `alpha = 0.01`, `C2 = 0`
- Matched control: `../2026-10-20_stacked_three_sheet_target_fractional_control`
- Steps / final time: `2000 / 4`
- Active / control wall time: about `15.5 / 15.5 min`
- Final-window samples: `501` over `t = 3` to `4`

| Corrected active-minus-control quantity | Target value | Project Eq. P15 coarse-to-target change |
|---|---:|---:|
| Total excess pressure drop | `0.122476005988` | `3.62160%` |
| Sheet 1 pressure increment | `0.031851616766` | `3.19208%` |
| Sheet 2 pressure increment | `0.039704752495` | `3.79845%` |
| Sheet 3 pressure increment | `0.043591175649` | `3.36597%` |
| Sheet 1 P7 CV change | `-0.007674311377` | `6.34070%` |
| Sheet 2 P7 CV change | `-0.011332413174` | `7.42464%` |
| Sheet 3 P7 CV change | `-0.012332079840` | `7.82729%` |

Both pair members pass the numerical checks. The largest final-window pressure range/mean is `0.0376113%`, maximum relative mass-flow error is `1.96591e-14`, maximum CFL is `0.247208`, maximum divergence is `2.58070e-13`, and maximum sheet-pressure closure error is `2.21627e-16`.

The corrected geometry eliminates the previously identified area and band-definition biases, but the coarse-to-target solution exceeds the working `2%` pressure and `5%` P7 gates. The later corrected fine pair shows monotonic convergence and target-to-fine changes of at most `1.45490%` for pressure quantities and `2.57712%` for corrected P7 changes, so the target grid passes the working criteria. See `../2026-10-20_stacked_three_sheet_fine_fractional/README.md`.
