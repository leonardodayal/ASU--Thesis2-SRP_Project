# Eight-Stick Single-Layer GCI Study

This study implements the advisor-directed normal-flow packet topology as one
`aligned_rods_z` layer containing eight porous sticks.  It uses the constant
refinement-ratio sequence:

| Level | Grid | Cells |
|---|---:|---:|
| G1 | `192 x 48 x 48` | 442,368 |
| G2 | `384 x 96 x 96` | 3,538,944 |
| G3 | `768 x 192 x 192` | 28,311,552 |
| G4 | `1536 x 384 x 384` | 226,492,416 |

Each refinement has `r = 2`.  G1-G3 are the initial GCI set.  G4 remains
conditional on a successful memory and timing smoke test.

## Geometry status

- The packet opening is represented by `Ly = Lz = 1`, corresponding to the
  reported `10 cm x 10 cm` opening.
- Eight centers span `0.875`, giving the reported `1.25 cm` center pitch.
- The provisional circular diameter is `0.105`, leaving `0.020` between
  adjacent circles, corresponding to the reported `2 mm` thermo-sealed line.
- The circular shape therefore assumes a `1.05 cm` streamwise thickness.  That
  thickness is **not measured** and must be replaced when the filled packet
  thickness arrives.
- Wall-padding counts scale as `2, 4, 8, 16` so all physical grid spacings
  refine by exactly two.

All resistance values remain synthetic.  These runs are numerical resolution
tests, not experimentally calibrated pressure-drop predictions.

## Execution order

1. Run `input.g1.smoke` with `smoke_128.sbatch` to verify the `16 x 8 x 1`
   decomposition, eight-stick mask, stability, memory, and Slurm launch.
2. Create and smoke-test G2 and G3 using the same physical geometry.
3. Run matched active and zero-resistance controls for G1-G3.
4. Calculate observed order, Richardson extrapolation, and GCI with `r = 2`.
5. Attempt G4 only if its smoke-test resource estimate is acceptable.

The original job `1105006` tested `16 x 4 x 2` and failed before solver
initialization because NGA2's FFT constructor requires at least one
non-decomposed direction.  The corrected `16 x 8 x 1` layout leaves `z`
undecomposed.  Post-run checks now reject missing or incomplete monitors so an
MPI task failure cannot be reported as a successful batch job.

Corrected Sol job `1120483` completed ten steps on 128 ranks in 13 solver
seconds.  It produced all required monitors, eight identical rod areas with
`0.00668939%` error, eight equal-width bands, no failure markers, and exit code
`0`.  The largest reported task RSS was `138236K`.

`input.g2.smoke100` and `smoke_g2_64.sbatch` define the next resource test:
100 steps on the `384 x 96 x 96` G2 grid, using `16 x 4 x 1`, 64 ranks,
128 GB, and a 15-minute limit.  This tests whether 64 ranks can keep a full G2
run near the 15-minute target without waiting for an entire 128-core node.

`input.g3.smoke100` and `smoke_g3_64.sbatch` define the subsequent G3 test
using the same 64-core allocation strategy as G2.

G2 Sol job `1122564` completed 100 steps on 64 ranks in 53 solver seconds.
All eight rod areas agree with `0.00802438%` error, all eight bands are equal,
and no failure markers were found.  A linear 2,000-step projection is about
`17:40`, slightly above the 15-minute target.  The first G3 request, job
`1122809`, was cancelled while pending without consuming resources.  G3 was
changed to 64 ranks and 128 GB to reduce queue wait and keep allocations
consistent for the initial resource study.

Replacement G3 job `1123065` completed 100 steps on 64 ranks in `6:13`
solver time.  It passed with exit code `0`, no failure markers, eight identical
rod areas (`-0.000986796%` error), equal bands, maximum CFL `0.500787`, final
maximum divergence `1.71010e-11`, relative mass-flow error `1.44336e-14`, and
maximum reported task RSS `759928K`.  The linear 2,000-step projection is
about `2:04:20`.  G4 needs a separately sized memory/time request.
