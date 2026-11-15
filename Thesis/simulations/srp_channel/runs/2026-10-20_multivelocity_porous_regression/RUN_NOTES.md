# Darcy-Forchheimer Regression After Grid-Consistency Changes

Purpose: confirm that fractional rod geometry, physical-band weighting, and sampling-plane interpolation do not alter the independently verified uniform-slab pressure-loss behavior.

- Executable SHA-256: `d3f92b1f970ebe4ad9f6042abfd758b9fe2a052f8bf67568c7d567c1674687d2`
- Cases: Darcy-only, Forchheimer-only, and combined resistance at velocities `0.5`, `1`, and `2`
- Total cases: `9`

All nine final-window mean pressure drops match Project Eq. P1 exactly at the precision written to `summary.csv`. Maximum relative mass-flow error is `9.99201e-16`, maximum CFL is `0.08`, and maximum divergence is `2.68307e-13`.

The verification inputs omit the optional flow-band settings, so this run also preserves the historical one-band default while exercising the new pressure-plane interpolation.
