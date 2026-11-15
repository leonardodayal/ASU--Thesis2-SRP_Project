# Uniform-Flow Forchheimer Slab Verification

Purpose: independently verify the inertial momentum source against the quadratic term in Project Eq. P1 while making Darcy resistance negligible.

- Base code revision: `67ef7fe`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `32 x 4 x 4` / `4 x 1 x 1`
- Fully open periodic cross-section: `Wall padding cells = 0`
- `rho = 1`, `C2 = 2`, `U = 1`, `alpha = 1e30`
- Porous slab: `x = 1.5` to `2.5`, so `Lp = 1`
- Pressure sample planes: `x = 1.4375` and `2.5625`
- Steps / final time: `800 / 4`

Project Eq. P1 predicts the inertial pressure drop

`delta_p = 0.5 rho C2 Lp U^2 = 1`.

Over the final 25% of the run (`t = 3` to `4`):

- control sampled pressure drop: `0`;
- Forchheimer sampled pressure drop: `1`;
- simulated excess inertial pressure drop: `1`;
- relative error from the analytical result: `0` within printed precision;
- pressure-drop range / mean: `0`;
- mean inlet/outlet mass flow: `1 / 1`;
- maximum relative mass-flow error: `0`;
- maximum CFL / divergence: `0.04 / 0`; and
- NaN, infinity, fatal-error, and solver-failure scan: none found.

Result: pass. The inertial source has the Project Eq. P1 magnitude and opposes the local velocity.
