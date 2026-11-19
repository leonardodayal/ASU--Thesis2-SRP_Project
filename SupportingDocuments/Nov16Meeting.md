# November 16 Advisor Meeting Notes

**Meeting date:** 2026-11-16
**Original source:** Leonardo Dayal's handwritten notes in [`Nov16Meeting.jpg`](./Nov16Meeting.jpg)
**Clarifications recorded:** 2026-11-17, from Leonardo's follow-up explanations

This document separates the original handwritten notes from later clarification and interpretation. Items marked **provisional** require advisor confirmation or additional experimental/model information.

## Handwritten notes transcribed

- Darcy source term inside the stick; use fractional volume.
- Interior: masked cell.
- Cannot be a single cell layer.
- `0.5` isosurface.
- Perform a coordinate transformation, or brute-force it by adding more mesh refinement.
- NGA2 can calculate every time step.
- Calculate area-averaged pressure upstream and downstream.
- Gas fields:
  - moisture;
  - CO2 mass fraction;
  - water mass fraction; and
  - temperature.
- Stick fields:
  - adsorbed CO2 quantity; and
  - adsorbed water quantity.
- Same idea as Darcy.

## Confirmed interpretation

### Fractional stick geometry and resistance

- In a cell cut by a stick boundary, multiply the local Darcy/Forchheimer momentum source by the fraction of the cell occupied by the stick. The source is zero outside a stick and reaches its full value in a completely occupied stick cell.
- The sticks are not perfect cylinders. Their filled cross-sections are closer to ovals, so the physical geometry should not remain circular once dimensions are available.
- The comment that the geometry cannot be a single cell layer refers to the solid walls/separators between adjacent sticks, not the porous stick thickness.
- A practical Cartesian-grid approach is to evaluate an analytic oval/ellipse at subcell sample points and set each CFD cell's stick fraction to the fraction of samples inside the shape. This refines geometry construction without globally refining the flow mesh.
- The advisor mentioned a coordinate transformation as an alternative that could preserve simple formulas. Subcell geometric sampling is currently the simpler candidate because it avoids transforming the flow equations. No implementation choice has been approved yet.

### Pressure diagnostics

- The handwritten symbol is pressure `p`, not density `rho`.
- Upstream and downstream pressure should be area-averaged.
- The physical sampling locations should match the experiment's pressure-tap locations. Those locations are not yet known.
- The thesis NGA2 case already interpolates pressure to configurable physical planes, area-averages it over the open cross-section, combines MPI contributions, and writes upstream pressure, downstream pressure, and their difference every time step.
- Full cell fields do not need to be written every time step; selected scalar monitors can be written every step while full-field output remains less frequent.

### Future coupled species and adsorption model

- The inlet should continuously prescribe constant CO2 and water-vapor concentrations for a simple, general study.
- CO2 and water vapor should be transported through the gas. Adsorption by a stick removes each species locally from the gas, so the downstream concentration should emerge naturally as lower than the inlet concentration.
- The same transfer must appear with opposite signs in the gas and stick balances so species mass is conserved.
- Gas cells will need pressure, temperature, CO2 mass fraction, and one clearly defined water-vapor/moisture variable. "Moisture" and "water mass fraction" are currently understood to refer to the same quantity.
- Stick cells will need adsorbed CO2 and adsorbed water state variables. Their exact definitions and units must follow the selected adsorption model; adsorbed loading may be more appropriate than mass fraction.
- A model discussed in earlier meetings is expected to provide equilibrium/loading and uptake-rate relationships. It should account for competition between CO2 and water and for moisture and temperature effects.
- Heat released by adsorption is not currently expected to be modeled, but this is **provisional**. Temperature may still be required because it can affect adsorption.
- Coupled CO2/water adsorption is later work. It should not block the current geometry, hydrodynamic, pressure-drop, and calibration work.

## Provisional interpretations requiring confirmation

- The `0.5` isosurface may mean rendering the fractional stick mask at a value of `0.5` to inspect the nominal stick boundary. Leonardo recorded the phrase but is unsure of the advisor's intended meaning.
- "One cell split into 256 cells" may mean 256 subcell geometry samples per CFD cell, not a 256-fold increase in the global flow mesh. The sample arrangement and required convergence check remain undefined.
- Adsorption heat is omitted initially unless the selected model or advisor guidance shows that thermal coupling is material.
- Constant inlet species concentrations are a deliberate simplifying boundary condition for a general understanding, not yet an experimentally matched inlet history.

## Open inputs and decisions

1. Identify the adsorption model mentioned in earlier meetings and record its equations, state variables, units, parameters, and supporting source.
2. Confirm what the advisor intended by the `0.5` isosurface.
3. Confirm whether `256` means subcell samples per CFD cell and select a sampling layout using a geometry-fraction convergence check.
4. Obtain the filled oval cross-sectional dimensions, separator-wall thickness/airtightness, and any wet-swelling dimensions.
5. Obtain the experiment's upstream and downstream pressure-tap locations.
6. Decide whether heat of adsorption can be neglected after reviewing the selected adsorption model and material data.
7. Define the single gas-phase water variable and the stick loading variables consistently with the selected model.

## Near-term scope boundary

Continue the hydrodynamic model by resolving the physical oval geometry, fractional cell coverage, separator walls, pressure sampling, and porous calibration. Defer gas-species transport and competitive CO2/water adsorption until the hydrodynamics are physically supported and the prior adsorption model is identified.
