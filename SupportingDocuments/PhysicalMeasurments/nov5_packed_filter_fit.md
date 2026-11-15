# November 5 packed-filter provisional fit

Source: `Pressure Drop of Filter.xlsx`, received locally 2026-11-11.  The
workbook labels the packed series `With Beads Filled in 40 micron Filter` and
contains 21 points from `0.00` to `0.20 m/s` and `0.0` to `28.4 Pa`.

## Reproduced fit

The physically constrained, zero-intercept Darcy fit is

`Delta p = 139.8292683 U` Pa.

It has `RMSE = 0.8344 Pa` and `R^2 = 0.98934` over all 21 points.  An
unconstrained zero-intercept Darcy-Forchheimer fit produces a negative
quadratic coefficient (`-22.8743 Pa/(m/s)^2`), so it is rejected as
nonphysical.  The CFD input therefore uses `C2 = 0` rather than forcing a
positive inertial term unsupported by this velocity range.

Assuming air dynamic viscosity `1.81e-5 Pa s` and the current provisional
filled thickness `L = 0.0105 m`,

`alpha = mu L / 139.8292683 = 1.359157509e-9 m^2`.

For the CFD normalization `L_ref = 0.10 m`, `U_ref = 0.20 m/s`, and
`rho_ref = 1.204 kg/m^3`, the corresponding inputs are:

- `Density = 1`
- `Dynamic viscosity = 7.516611296e-4`
- `Inlet velocity = 1`
- `Porous permeability = 1.359157509e-7`
- `Forchheimer coefficient = 0`

The fit is an **effective packed-filter assembly fit**, not an isolated bead
fit.  The workbook does not report repeatability, sensor uncertainty, air
properties, pressure-tap geometry, or filled thickness.  The 10.5 mm length
is inherited from the provisional circular-stick geometry and must be
replaced when the measured thickness arrives.  The sheet-only series has only
six points and is not paired point-for-point with the packed series, so mesh
subtraction is not defensible yet.
