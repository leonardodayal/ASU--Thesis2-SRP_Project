# Uniform-Flow Darcy Control

Paired control for `2026-10-16_darcy_uniform_verification`. Zero wall-padding cells select a fully open periodic cross-section for this analytical test; production channel cases retain positive padding and immersed walls.

- Base code revision: `c304399`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Mesh / decomposition: `32 x 4 x 4` / `4 x 1 x 1`
- Porous slab: disabled by equal start/end coordinates
- Steps / final time / runtime: `800 / 4 / 0.748134 s`
- Final-window (`t = 3` to `4`) mean sampled pressure drop: `0`
- Mean mass flow: `1`
- Maximum CFL / divergence: `0.04 / 0`
- Result: pass; the control contributes no sampled pressure loss.
