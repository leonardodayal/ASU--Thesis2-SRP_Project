# Fractional-Geometry Grid-Consistency Smoke Test

Purpose: verify that the coarse, target, and fine grids represent the same physical rod area and flow-band boundaries after replacing binary rod cells and whole-row band assignment. These are ten-step numerical smoke tests, not converged or physical SRP predictions.

- Executable SHA-256: `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`
- Command: `python3 tools/verify_grid_geometry.py --executable ./nga.dp.gnu.opt.mpi.exe --output-dir runs/2026-10-20_grid_consistency_smoke --max-time 0.02`
- MPI ranks per case: `4`
- Ensight output: disabled for this diagnostic

## Geometry results

The requested area of one `0.1`-diameter circular rod is `0.007853981634`. The production mask now uses a fractional value in boundary cells.

| Grid | Represented rod area | Absolute area error | Cross-grid status |
|---|---:|---:|---|
| `128 x 32 x 32` | `0.007854207357` | `0.002874%` | pass |
| `256 x 64 x 64` | `0.007854207357` | `0.002874%` | pass |
| `384 x 96 x 96` | `0.007853981301` | `0.00000424%` | pass |

The maximum represented-area spread across the three grids is `0.00287824%`, below the predeclared `0.1%` limit. All twelve rods on each grid have identical represented areas at the audit precision.

Every grid now uses the same physical flow-band edges, `-0.5`, `-0.25`, `0`, `0.25`, and `0.5`. Each band is exactly `0.25` wide. Cell rows crossing an edge contribute to both adjacent bands according to physical overlap.

## Short-flow results

| Grid | Maximum CFL | Maximum divergence | Maximum relative mass error |
|---|---:|---:|---:|
| Coarse | `0.068866` | `2.44873e-14` | `2.78019e-15` |
| Target | `0.142256` | `2.28660e-13` | `1.43278e-14` |
| Fine | `0.219908` | `1.82468e-13` | `3.34239e-14` |

Every case reached `t = 0.02`, conserved the four-band fraction sum at `1.0`, preserved paired-band symmetry, and closed the per-sheet pressure sum to at most `1.34292e-16` relative error.

The previous full-duration grid study used the binary rod mask and whole-row bands. Its results remain historical evidence of the diagnosed bias and must not be mixed with new fractional-geometry results. The next gate is a full corrected coarse/target active-control comparison; rerun the fine pair only if that comparison behaves consistently.
