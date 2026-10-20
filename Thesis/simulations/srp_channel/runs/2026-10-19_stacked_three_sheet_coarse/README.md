# Coarse-Grid Three-Sheet Sensitivity Pair

Purpose: compare the resistance-active and zero-resistance provisional stacks on a systematically coarser mesh, then evaluate Project Eq. P15 against the matched `256 x 64 x 64` pair. These are synthetic numerical-sensitivity cases, not physical SRP predictions.

- Code revision before the runs: `f76f9be`
- Command: `mpiexec -n 4 ../../nga.dp.gnu.opt.mpi.exe -i input`
- Coarse mesh / decomposition: `128 x 32 x 32` / `4 x 1 x 1`
- Target mesh: `256 x 64 x 64`
- Wall padding: one coarse cell versus two target cells
- Active resistance: `alpha = 0.01`, `C2 = 0`
- Control resistance: `alpha = 1e30`, `C2 = 0`
- Steps / final time: `2000 / 4` for each case
- Wall-clock intervals from the logs: about `214 s` active and `727 s` control

## Coarse-pair convergence

Over the final 25% (`t = 3` to `4`), both cases use `501` samples.

| Quantity | Active | Control |
|---|---:|---:|
| Mean total pressure drop | `1.75640766467` | `1.61955139721` |
| Pressure-drop range / mean | `0.154862%` | `0.182149%` |
| Maximum relative mass-flow error | `6.45004e-15` | `7.11729e-15` |
| Maximum CFL | `0.118202` | `0.119834` |
| Maximum divergence | `2.67961e-14` | `2.76868e-14` |

Both runs completed normally with one pressure iteration, zero reported pressure error, and no NaN, infinity, fatal-error, or solver-failure matches.

## Active-minus-control and grid change

Project Eq. P15 uses the target pair as `phi_fine` and this pair as `phi_coarse`.

| Corrected quantity | Coarse | Target | `delta_grid` |
|---|---:|---:|---:|
| Total excess pressure drop | `0.136856267460` | `0.142539081830` | `3.98685%` |
| Sheet 1 local pressure increment | `0.032748259481` | `0.034016007984` | `3.72692%` |
| Sheet 2 local pressure increment | `0.040484940120` | `0.042172576846` | `4.00174%` |
| Sheet 3 local pressure increment | `0.044671858283` | `0.046317219560` | `3.55237%` |
| Sheet 1 P7 CV change | `-0.007943930140` | `-0.008178111777` | `2.86352%` |
| Sheet 2 P7 CV change | `-0.011854520959` | `-0.012072760479` | `1.80770%` |
| Sheet 3 P7 CV change | `-0.012882538922` | `-0.013142085828` | `1.97493%` |

The signs and conclusions are unchanged: resistance adds pressure loss and reduces the four-band P7 CV at all three downstream planes. The target-grid corrected quantities differ from the coarse pair by at most `4.00174%`.

## Discretization caveat

The coarse passage has 30 open cells across the flow-split direction, which cannot be divided evenly among four physical bands. The coarse band fractions therefore lose the target grid's exact paired symmetry. Because active and control use the same coarse discretization, subtraction cancels most of this baseline bias, but a finer-than-target run is still required before claiming formal grid independence.
