# Corrected Coarse-Grid Fractional-Geometry Pair

Purpose: repeat the full-duration coarse active/control comparison after making rod area, band boundaries, and sampling planes physically consistent across grids. This remains a synthetic numerical case.

- Executable SHA-256: `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`
- Mesh: `128 x 32 x 32`
- Active resistance: `alpha = 0.01`, `C2 = 0`
- Matched control: `../2026-10-20_stacked_three_sheet_coarse_fractional_control`
- Steps / final time: `2000 / 4`
- Active / control wall time: about `1.33 / 1.43 min`
- Final-window samples: `501` over `t = 3` to `4`

| Corrected active-minus-control quantity | Coarse value |
|---|---:|
| Total excess pressure drop | `0.118040415170` |
| Sheet 1 pressure increment | `0.030834888224` |
| Sheet 2 pressure increment | `0.038196586826` |
| Sheet 3 pressure increment | `0.042123910180` |
| Sheet 1 P7 CV change | `-0.008160916168` |
| Sheet 2 P7 CV change | `-0.012173804391` |
| Sheet 3 P7 CV change | `-0.013297347305` |

Both pair members pass the numerical checks. The largest final-window pressure range/mean is `0.0523713%`, maximum relative mass-flow error is `7.22850e-15`, maximum CFL is `0.119834`, maximum divergence is `2.76868e-14`, and maximum sheet-pressure closure error is `2.21940e-16`.

Against the corrected target pair, Project Eq. P15 changes are `3.62160%` for total excess pressure, `3.19208-3.79845%` for sheet increments, and `6.34070-7.82729%` for corrected P7 changes. These exceed the working `2%` pressure and `5%` P7 gates, so a corrected fine pair was not launched.
