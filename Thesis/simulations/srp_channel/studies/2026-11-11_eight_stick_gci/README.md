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
