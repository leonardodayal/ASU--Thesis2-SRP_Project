# Multi-Velocity Porous-Resistance Verification

Purpose: verify the Darcy, Forchheimer, and combined source scaling against Project Eq. P1 at multiple velocities.

- Simulation source revision: `60ba3cc` (no later changes to `src/`)
- Runner: `tools/verify_porous_scaling.py`
- Command: `python3 tools/verify_porous_scaling.py --executable ./nga.dp.gnu.opt.mpi.exe --output-dir runs/2026-10-19_multivelocity_porous_verification`
- Mesh / decomposition: `32 x 4 x 4` / `4 x 1 x 1`
- Fully open periodic cross-section: `Wall padding cells = 0`
- Porous slab: `x = 1.5` to `2.5`, so `Lp = 1`
- Velocities: `0.5`, `1`, and `2`
- Final-window statistics: final 25% of each run (`t = 3` to `4`)
- Acceptance tolerances: relative pressure-drop error `<= 1e-8`; maximum relative mass-flow error `<= 1e-10`

## Cases and results

| Source terms | Expected pressure drop at U = 0.5, 1, 2 | Simulated final-window means | Maximum relative error |
|---|---:|---:|---:|
| Darcy, `mu = alpha = 0.01`, `C2 = 0` | `0.5, 1, 2` | `0.5, 1, 2` | `0` within printed precision |
| Forchheimer, `alpha = 1e30`, `rho = 1`, `C2 = 2` | `0.25, 1, 4` | `0.25, 1, 4` | `0` within printed precision |
| Combined, `mu = alpha = 0.01`, `rho = 1`, `C2 = 2` | `0.75, 2, 6` | `0.75, 2, 6` | `0` within printed precision |

Across all nine cases, the final-window pressure-drop range/mean was zero within printed precision. The maximum relative mass-flow error was `9.99201e-16`, maximum CFL was `0.08`, and maximum divergence was `2.68307e-13`. The log scan found no NaN, infinity, fatal error, or solver failure.

Result: pass. The simulations reproduce the linear Darcy contribution, quadratic Forchheimer contribution, and their sum at all three velocities. All coefficients and units in this verification are synthetic and must not be interpreted as SRP material properties.

`summary.csv` contains the machine-readable results. Each case directory preserves its input, launcher output, and NGA2 monitors; Ensight fields are ignored because the uniform fields add no verification evidence beyond the monitors.
