# Flow-Split Diagnostic Verification

Purpose: verify the downstream equal-width flow-band monitor and Project Eqs. P6-P7 before applying it to rod or stacked-sheet comparisons.

- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `32 x 12 x 12` / `4 x 1 x 1`
- Split plane: `x = 3`
- Bands: four equal-width bands across the detected open passage
- Steps / final time: `4 / 0.02`

At the final step, the band mass-flow rates were `0.229289`, `0.258992`, `0.258992`, and `0.229289`. Their sum was `0.976562`, consistent with the inlet and outlet value `0.976563` at monitor precision, and the fractions summed to `1.0`. The symmetric band pairs agreed exactly at monitor precision. The P7 coefficient of variation was `0.0608306`; this reflects the developing wall-bounded profile in the open-channel smoke test and is not a physical SRP maldistribution result.

The monitor files contain no NaN, infinity, fatal error, or solver failure. A separate run of the historical Darcy verification input, which contains neither flow-split setting, confirmed the backward-compatible one-band defaults: fraction `1.0`, coefficient of variation `0.0`, and unchanged pressure drop `1.0`.

Result: pass. This verifies diagnostic accounting and defaults, not rod geometry or calibrated physical performance.
