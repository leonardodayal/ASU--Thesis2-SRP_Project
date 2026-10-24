# Three-Sheet Pressure-Monitor Smoke Test

Purpose: verify configurable per-sheet pressure sampling and whole-stack pressure-drop closure on the provisional three-sheet geometry. The run is short and all dimensions and resistance values remain synthetic.

- Base code revision: `b5fd530`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Geometry: three sheets centered at `x = 1.5`, `2.0`, and `2.5`, with four aligned rods per sheet
- Sheet pressure offset: `0.25`, placing shared sampling planes halfway between neighboring sheets
- Steps / final time: `10 / 0.02`

At the final step, the per-sheet pressure drops were `0.765813`, `0.765851`, and `0.765825`. Their sum was `2.29749`, equal to the pressure drop between the first upstream and last downstream sample planes at monitor precision. The reported closure error was zero.

The solver result remained conservative and stable: final relative mass-flow error `3.44313e-15`, maximum CFL `0.142256`, maximum divergence `2.33458e-13`, and no NaN, infinity, fatal error, or solver failure.

Regression checks also passed:

- a non-rod input completed normally without creating a sheet-pressure monitor; and
- the historical single-sheet input preserved its original total pressure/flow result while the default offset produced distinct upstream/downstream sheet pressures and a nonzero local sheet drop.

Result: pass for per-sheet pressure accounting and conditional behavior. These transient pressure values are not converged physical results.
