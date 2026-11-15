# Uniform-Flow Darcy Slab Verification

Purpose: verify the Darcy-only momentum source against Project Eq. P1 in a uniform-flow reference case.

- Base code revision: `c304399`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `32 x 4 x 4` / `4 x 1 x 1`
- Fully open periodic cross-section: `Wall padding cells = 0`
- `mu = 0.01`, `alpha = 0.01`, `U = 1`
- Porous slab: `x = 1.5` to `2.5`, so `Lp = 1`
- Pressure sample planes: `x = 1.4375` and `2.5625`
- Steps / final time / runtime: `800 / 4 / 0.775359 s`

Project Eq. P1 with `C2 = 0` predicts

`delta_p = mu Lp U / alpha = 1`.

Over the final 25% of the run (`t = 3` to `4`):

- control sampled pressure drop: `0`;
- porous sampled pressure drop: `1`;
- simulated excess Darcy pressure drop: `1`;
- relative error from the analytical result: `0` within printed precision;
- pressure-drop range / mean: `0`;
- mean inlet/outlet mass flow: `1 / 1`;
- maximum relative mass-flow error: `0`;
- maximum CFL / divergence: `0.04 / 0`; and
- NaN, infinity, fatal-error, and solver-failure scan: none found.

Result: pass. The source acts only through the exported `porous_mask`, opposes velocity, and reproduces the Darcy reference pressure drop.
