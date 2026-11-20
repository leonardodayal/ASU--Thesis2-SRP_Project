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

## November 5 effective-resistance smoke sequence

The recovered packed 40-micrometre-filter data support a provisional
Darcy-only effective assembly fit.  With the unverified `10.5 mm` thickness,
the physical permeability is `1.35916e-9 m^2`; normalized using a `0.10 m`
reference length and `0.20 m/s` reference velocity, the solver inputs are
`mu*=7.51661e-4`, `alpha*=1.35916e-7`, and `C2*=0`.

Matched active/control 100-step jobs completed on all three grids:

| Grid | Active job | Control job | Active/control solver time | Net sheet pressure at `t*=0.01` |
|---|---:|---:|---:|---:|
| G1 | `1126388` | `1126397` | `11/10 s` | `4.12 Pa` |
| G2 | `1126507` | `1126508` | `33/33 s` | `2.94 Pa` |
| G3 | `1126509` | `1126510` | `4:03/4:02` | `1.75 Pa` |

All jobs exited zero, completed 100 steps at `dt*=1e-4`, conserved mass, and
showed no failure markers.  The pressure values are startup transients and do
not form a valid GCI sequence.  A longer time-history study must define a
converged pressure averaging window before production GCI runs are submitted.

## G3 ParaView dataset

Sol job `1131103` reran the active G3 case with Ensight output enabled.  It
completed in `6:17` solver time (`6:22` batch) on 64 ranks with exit code `0`,
no failure markers, and maximum task RSS `791272K`.  The output is `1.4 GB`
and contains two states of geometry, wall volume fraction, porous mask,
pressure, and velocity.

The authoritative cluster copy is:

`$SCRATCH/srp_benchmark/nov5_g3_visualization100_64/ensight`

Copy it to the Git-ignored `paraview_data/` directory beside this README and
open `paraview_data/srp_channel/nga.case`.  The final state is startup flow at
`t*=0.01`; it is appropriate for explaining the model and mesh, not for a
converged pressure or GCI claim.

## Sealed-wall and retaining-mesh geometry smoke

`input.g1.walls_mesh.smoke` opts into the packet refinements added on
2026-11-15. It represents the seven `0.02`-thick internal thermo-sealed
dividers and closes the two outer-stick gaps to the channel walls. The sharp
immersed-boundary geometry uses a one-cell minimum numerical wall thickness
when the requested seal is under-resolved. It also wraps every bead stick in a
separate one-cell porous annulus exported as `mesh_mask`.

The mesh source accepts integrated `Mesh linear resistance` and
`Mesh quadratic resistance` values and divides them by the actual represented
layer thickness. Each value describes one traversal of the mesh skin; normal
flow through the closed annulus crosses its upstream and downstream sides. The
input's value is synthetic and tests implementation only.
A local four-rank, two-step G1 run found exactly nine wall segments and distinct
nonempty `porous_mask` and `mesh_mask` fields. The corrected mask contains
`4,200` mesh-positive cells outside the bead mask, confirming that the complete
annulus is represented. Representative reruns ended with
CFL about `0.0056`, maximum divergence about `3.2e-13`, and relative mass-flow
error about `5e-15`.
Do not use this smoke result as a calibrated pressure-drop prediction.

## Ellipse geometry smoke

`input.g1.ellipse_walls_mesh.smoke` changes the provisional stick cross-section
to a `0.105` long `y` axis and `0.060` short streamwise `x` axis while retaining
the separate mesh annulus and nine separator/closure walls. The short axis and
mesh resistance are synthetic pending measurements.

A local four-rank, two-step run on 2026-11-20 completed with eight represented
sticks at `0.0187043%` area error, eight connected porous regions at the `0.5`
contour, `4,564` mesh-only cells, final CFL `0.00561629`, maximum divergence
`3.11723e-13`, and relative mass-flow error `6.77761e-15`.

Render any resulting Ensight case with:

```bash
/Applications/ParaView-6.1.1.app/Contents/bin/pvpython \
  render_ellipse_smoke.py path/to/nga.case path/to/screenshots
```

The three outputs intentionally distinguish the fractional cell field used by
the solver, its display-only `0.5` contour, and the separate mesh/wall geometry.
