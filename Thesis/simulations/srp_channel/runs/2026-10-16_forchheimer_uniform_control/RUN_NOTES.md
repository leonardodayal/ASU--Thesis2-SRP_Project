# Uniform-Flow Forchheimer Control

Paired control for `2026-10-16_forchheimer_uniform_verification` with the same active mask, negligible Darcy resistance, and `C2 = 0`.

- Base code revision: `67ef7fe`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `32 x 4 x 4` / `4 x 1 x 1`
- Steps / final time: `800 / 4`
- Final-window mean sampled pressure drop: `0`
- Mean mass flow: `1`
- Maximum CFL / divergence: `0.04 / 0`
- Result: pass.
