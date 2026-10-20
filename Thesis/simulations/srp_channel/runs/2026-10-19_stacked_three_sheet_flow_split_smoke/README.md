# Three-Sheet Flow-Split Smoke Test

Purpose: verify per-sheet flow-band and Project Eq. P7 maldistribution reporting on the provisional three-sheet geometry. This short run and all geometry/resistance values are synthetic.

- Base code revision: `73d79e6`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Geometry: three sheets centered at `x = 1.5`, `2.0`, and `2.5`, with four aligned rods per sheet
- Sampling planes: each sheet's downstream pressure plane at `x = 1.75`, `2.25`, and `2.75`
- Flow bands: four equal-width y bands at every sampling plane
- Steps / final time: `10 / 0.02`

At the final step, every sheet-plane band sum was `0.999583` and every fraction sum was `1.0`. Paired outer and inner bands remained symmetric. The final transient P7 coefficients of variation were `0.0182707`, `0.0182705`, and `0.0183899` after sheets 1, 2, and 3, respectively.

The solver remained conservative and stable: final relative mass-flow error `3.66526e-15`, maximum CFL `0.142256`, maximum divergence `2.32201e-13`, and no NaN, infinity, fatal error, or solver failure.

Regression checks passed:

- the non-rod debug case reproduced its preserved downstream band values exactly and created no sheet-specific monitor; and
- the historical single-sheet case preserved its total pressure/flow result and produced a backward-compatible one-band sheet monitor with fraction `1.0` and CV `0.0`.

Result: pass for per-sheet flow accounting, symmetry, conditional behavior, and regression stability. The transient CV values are not converged physical results.
