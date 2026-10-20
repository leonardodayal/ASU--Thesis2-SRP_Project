# Provisional Three-Sheet Stack Smoke Test

Purpose: verify the configurable `stacked_aligned_rods_z` mask and solver path on the target mesh. The geometry and resistance are synthetic and must not be interpreted as physical SRP values.

- Base code revision: `40e3727`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `256 x 64 x 64` / `4 x 1 x 1`
- Sheet count / spacing / stack center: `3 / 0.5 / x = 2`
- Derived center-to-center stack span: `1.0`
- Derived porous streamwise depth including rod diameter: `1.1`
- Rods per sheet / diameter / first-to-last y-center span: `4 / 0.1 / 0.6`
- Provisional resistance: `alpha = 0.01`, `C2 = 0`
- Steps / final time: `10 / 0.02`

## Mask verification

The exported EnSight `porous_mask` contains:

- range `0` to `1`;
- `23,040` porous cells total;
- three separated six-cell streamwise groups at x-index ranges `93-98`, `125-130`, and `157-162`;
- `7,680` porous cells per sheet, exactly matching the verified single-sheet mask;
- four separated six-cell y groups per sheet at index ranges `11-16`, `23-28`, `35-40`, and `47-52`; and
- 60 porous z cells at indices `2-61`, matching the open passage and excluding all wall-padding cells.

Thus the target mask contains three separated sheets with four separated rods per sheet, the requested spacing, and no wall clipping.

## Solver smoke-test result

- Final CFL: `0.142256`
- Final maximum divergence: `2.18902e-13`
- Final relative mass-flow error: `3.33206e-15`
- Final four-band fraction sum: `1.0`
- Final symmetric band fractions: `0.245733`, `0.254267`, `0.254267`, `0.245733`
- Pressure iterations / reported pressure error: `1 / 0`
- NaN, infinity, fatal-error, and solver-failure scan: none found
- Result: pass for mask construction, flow-split bookkeeping, and short-time numerical stability.

A separate rerun of the historical `aligned_rods_z` input reproduced its original final pressure drop and velocity maxima exactly at monitor precision, confirming backward compatibility. This stack run is too short for convergence, and its pressure drop is not a physical result.
