# Usable Research Components for the SRP Multi-Level CO2 Collector Thesis

## Thesis scope used for this assessment

SRP has tasked the project with analyzing a multi-level CO2 collector using CFD. The model must transport CO2 through the collector and account for the amount absorbed at each level. This assessment therefore focuses on components that help answer:

1. How does the flow distribute across the collector levels?
2. How much CO2 does each level remove?
3. How do upstream levels affect the CO2 available to downstream levels?
4. What pressure drop and energy cost accompany the capture?
5. How do geometry, wind, and operating conditions change total and per-level performance?

The two papers use different capture systems. Zaynetdinov et al. model **adsorption by a solid amine sorbent**, while Eftekharian et al. model a cooling-tower-style **liquid absorption system** through an experimentally fitted capture-rate relation. Their equations must not be combined without first identifying the SRP collector's capture medium.

## Recommended thesis model

The most useful model is a staged scalar-transport CFD calculation:

\[
\frac{\partial (\rho Y_{CO_2})}{\partial t}
+ \nabla \cdot (\rho \mathbf{u}Y_{CO_2})
= \nabla \cdot (\rho D_{eff}\nabla Y_{CO_2}) + S_{CO_2}
\]

where each collector level has its own CO2 sink, \(S_{CO_2,\ell}\). The flow solver determines how much air reaches level \(\ell\), and the absorption model determines the sink within that level. The depleted outlet from one level naturally becomes the inlet to downstream levels.

For every level, report the flux-based capture fraction

\[
\eta_\ell = 1-\frac{\dot m_{CO_2,out,\ell}}{\dot m_{CO_2,in,\ell}},
\qquad
\dot m_{CO_2,captured,\ell}
=\dot m_{CO_2,in,\ell}-\dot m_{CO_2,out,\ell}.
\]

The total collector removal must be computed from the external inlet and outlet, or equivalently from the sum of all level sinks. Do **not** add level percentages directly. A downstream level receives less CO2 after upstream capture, and recirculation may cause flow to cross a level more than once.

## Component-selection matrix

| Component | Source | Use in this thesis | Priority | Required adaptation |
|---|---|---|---|---|
| CO2 advection-diffusion equation | Both papers | Core equation for CO2 transport between levels | Essential | Implement CO2 as a bounded scalar in NGA2 and include molecular plus turbulent diffusivity |
| Per-level CO2 mass balance | Both papers, adapted | Quantifies absorption on every level and checks conservation | Essential | Define inlet/outlet sampling planes or tagged level volumes and integrate CO2 mass flux |
| Velocity-dependent capture relation | Eftekharian et al. | Practical reduced-order absorption model for each level | High if the SRP collector is liquid-absorbent | Fit a new relation from SRP data; do not assume the paper's coefficients apply |
| Volumetric CO2 sink | Zaynetdinov et al. | Represents distributed removal inside a packed or sorbent level | High | Select kinetics appropriate to the SRP absorbent/adsorbent |
| Porous-media momentum resistance | Both papers | Represents packing pressure loss and changes in flow split among levels | High for packed levels | Add Darcy-Forchheimer/Ergun momentum sources to NGA2 and calibrate them for the actual packing |
| Pressure drop and specific energy | Zaynetdinov et al. | Connects capture performance to fan/pumping cost | High | Measure pressure drop by level and for the full unit; include fan efficiency if estimating electrical energy |
| Atmospheric boundary-layer inlet | Eftekharian et al. | Tests outdoor wind-speed and wind-direction sensitivity | Medium; later phase | Use after the still-air/fan-driven collector model is validated |
| LES and turbulent scalar diffusivity | Eftekharian et al.; NGA2 | Resolves unsteady level-to-level flow, wakes, and plume recirculation | High if the collector flow is turbulent | Perform grid and sampling-time studies; specify the scalar Schmidt number |
| Breakthrough/saturation tracking | Zaynetdinov et al. | Needed if capture capacity decays with time | Conditional | Use for finite-capacity solid sorbents; usually omit for a continuously regenerated liquid absorber |
| Toth equilibrium isotherm plus LDF kinetics | Zaynetdinov et al. | A tractable solid-sorbent adsorption submodel | Conditional | Use only for a solid adsorbent and refit all coefficients to SRP material data |
| Dual-temperature gas/solid energy model | Zaynetdinov et al. | Captures heat released by adsorption and its effect on capacity | Conditional/advanced | Add only if temperature changes materially affect capture |
| CO2-depleted plume recirculation | Eftekharian et al. | Detects whether exhaust is pulled back into a level or unit inlet | High for full-device CFD | Keep the external domain and model the outlet plume, rather than prescribing fresh-air concentration at every level |
| Geometry parametric study | Zaynetdinov et al. | Compares level spacing, packing depth, open area, and number of levels | High | Hold an appropriate quantity constant, such as footprint, packing volume, or fan power |
| Wind-speed/wind-angle matrix | Eftekharian et al. | Evaluates siting/orientation sensitivity | Medium | Use site-relevant wind data rather than copying their seven speeds and five angles |
| Grid independence, validation, and uncertainty | Both papers | Makes the CFD results thesis-defensible | Essential | Validate both airflow/pressure drop and CO2 removal, not only one of them |

## Components from each paper

### 1. Zaynetdinov et al.: radial-flow solid-sorbent contactor

Source: [Adsorption performance of radial-flow contactors for direct air capture: A computational study](./1-s2.0-S0009250926019512-main.pdf), DOI `10.1016/j.ces.2026.125236`.

This paper is most useful for modeling the **inside of a capture level**.

Components worth using:

- Treat a packed capture region as a porous zone rather than resolving every particle.
- Add viscous and inertial resistance using a Darcy-Forchheimer form. The paper calculates resistance from the Ergun correlation using particle diameter and porosity.
- Apply a CO2 sink only in tagged capture-level cells.
- Use a separate state variable for loading/capacity if the level contains a finite-capacity solid sorbent.
- For solid adsorption, use the linear-driving-force model

  \[
  \frac{dq}{dt}=k_{LDF}(q_{eq}-q)
  \]

  and obtain \(q_{eq}\) from a fitted equilibrium isotherm such as Toth.
- Start with one-way coupling if justified: solve the steady flow first, then transient CO2 transport. This is valid only when changing CO2 concentration and adsorption heat have negligible influence on the velocity field.
- Use breakthrough curves, time to a stated saturation threshold, flow uniformity, pressure drop, productivity, and energy per mass of CO2 as performance measures.
- Follow its verification pattern: test time-step sensitivity and mesh sensitivity using both pressure drop and capture behavior.

What can be used only as a benchmark, not as SRP input:

- The listed particle diameter, porosity, density, resistance coefficients, heat-transfer coefficient, and \(k_{LDF}\) describe the paper's commercial amine-functionalized resin.
- The 430 ppm inlet, 200 Pa base-case pressure drop, geometrical aspect ratios, and 0.1 s time step are case choices, not universal design values.
- The axisymmetric radial geometry is not automatically representative of a stacked or multi-level SRP collector.

### 2. Eftekharian et al.: external wind and liquid-absorption collector

Source: [Ambient wind direction impacts on the performance of a CO2 direct air capture system determined using large eddy simulations](./1-s2.0-S1750583626002240-main.pdf), DOI `10.1016/j.ijggc.2026.104792`.

This paper is most useful for modeling the **whole collector, its surroundings, and a reduced-order absorption response**.

Components worth using:

- Use LES when wakes, level-to-level interactions, fluctuating inlet flow, or depleted-plume recirculation are important.
- Transport CO2 as a passive scalar coupled to the instantaneous velocity field.
- Represent unresolved capture physics with a local response relation. The paper uses a quadratic capture fraction, \(\eta=aU^2+bU+c\), fitted to experiments.
- Evaluate the response locally or level by level rather than applying one capture percentage to the whole collector.
- Compute mean captured mass by time-integrating the instantaneous mass-removal rate. Multiplying independently averaged velocity, concentration, and capture fraction can lose their correlations and produce a biased answer.
- Model the fan/exhaust so that depleted air can re-enter the collector naturally.
- Use an atmospheric boundary-layer power-law inlet for outdoor cases and vary both wind speed and direction.
- Diagnose horseshoe vortices, shear-layer separation, wakes, inlet-flow imbalance, and exhaust recirculation because these mechanisms change the air and CO2 delivered to each level.
- Validate the flow solver against suitable aerodynamic data and validate the absorption relation independently against collector experiments.

What must not be copied directly:

- The quadratic coefficients \(a=0.0672\), \(b=-0.3269\), and \(c=0.7588\) were fitted to a particular amine-based experimental unit, at a stated inlet-concentration range and operating setup. They are not a general absorption law.
- The 50% capture rate at 1 m/s, 43.55 m3/s fan flow, geometry, packing, and wind cases belong to that system.
- A fitted outlet boundary is useful for a whole unresolved unit. For this thesis, placing an equivalent relation at **each level** is more appropriate only if level-scale calibration data exist and the relation remains valid under the local conditions.

## Choosing the absorption model for each level

The capture medium determines the correct branch:

### If SRP uses a liquid absorbent

Prefer one of these, in increasing physical detail:

1. **Measured level response:** \(\eta_\ell=f(U_\ell, C_{in,\ell})\). This is closest to Eftekharian et al. and is the recommended first thesis model if SRP can supply test data.
2. **Volumetric first-order sink:** \(S_{CO_2,\ell}=-K_\ell a_\ell C_{CO_2}\), where \(K_\ell a_\ell\) is calibrated for the packing, solvent flow, temperature, and loading.
3. **Two-film/reactive mass transfer:** resolve gas-liquid interfacial transport and liquid chemistry. This is much more expensive and should be used only if the thesis explicitly requires it and the needed properties are available.

The liquid flow rate, solvent concentration/loading, temperature, wetting, and packing area must either appear in the model or be held within the calibration range of the empirical relation.

### If SRP uses a solid adsorbent

Use the Zaynetdinov et al. structure: porous resistance + CO2 transport + LDF loading + a fitted equilibrium isotherm. Store \(q_\ell(\mathbf{x},t)\) so each level can saturate at a different rate. Add the thermal model if adsorption heat significantly changes equilibrium capacity.

### If the capture medium is not yet confirmed

Implement the airflow, CO2 scalar, tagged levels, per-level flux monitors, and a replaceable sink interface first. Keep the capture law in a separate routine so the empirical liquid model or solid LDF model can be inserted later without rebuilding the CFD solver.

## Mapping to the current NGA2 repository

### Directly reusable NGA2 capabilities

- Cartesian structured meshes and parallel domain decomposition.
- Constant-density incompressible and variable-density low-Mach flow solvers.
- Constant- and variable-density scalar transport.
- Scalar diffusivity as a field, which can incorporate turbulent diffusion.
- LES subgrid models: dynamic Smagorinsky, constant Smagorinsky, and Vreman.
- Immersed-boundary support for the collector structure.
- Time tracking, monitors, restart data, and Ensight output.
- Existing examples for scalar transport, turbulent channels, jets, wakes, and immersed obstacles.

### New thesis-specific implementation

- A geometry definition and integer/tag mask for every collector level.
- A CO2 scalar configured in concentration, mole fraction, or mass fraction with explicit, consistent unit conversions.
- A per-level absorption/adsorption sink added to the scalar residual.
- Per-level inlet/outlet mass-flux integrations and cumulative capture monitors.
- Porous momentum sources for packing regions.
- A fan or prescribed-flow model consistent with the physical collector.
- An atmospheric inlet profile and turbulent inflow method for outdoor cases.
- Optional level state variables such as sorbent loading, solvent loading, or temperature.
- Global conservation diagnostics that compare external inlet-outlet removal with the integrated sinks across all levels.

NGA2 currently advertises Cartesian meshes; cylindrical support is listed as future development. Therefore, a radial collector should be represented in 3D Cartesian coordinates, potentially with immersed boundaries, rather than assuming that the paper's 2D axisymmetric workflow transfers directly. The scalar solver exposes its residual to the application-level time-integration code, so the level sinks can be added there, but NGA2 does not appear to include a ready-made DAC or porous-adsorption module.

## Minimum viable simulation campaign

### Phase 1: airflow and pressure-drop validation

- Build the exact SRP geometry and level tags.
- Simulate the fan-driven flow without CO2 removal.
- Compare total and per-level flow rates and pressure drops with measurements or vendor correlations.
- Perform mesh and time-step studies.

### Phase 2: level-resolved CO2 capture

- Enable the CO2 scalar.
- Add a replaceable sink model to each level.
- Run a no-wind design condition.
- Verify mass conservation and compare overall capture with SRP data.
- Report per-level inlet concentration, outlet concentration, capture fraction, captured mass rate, pressure drop, and flow uniformity.

### Phase 3: design study

- Vary the number of levels, level spacing, packing depth, open area, fan flow, and capture-model parameters.
- Compare total capture, capture by level, pressure drop, fan energy, and capture uniformity.
- Identify whether later levels add useful capture or mainly add resistance after upstream depletion.

### Phase 4: environmental sensitivity

- Add the external domain and depleted outlet plume.
- Vary site-relevant wind speed and direction.
- Quantify level-flow imbalance and depleted-plume recirculation.
- Use statistically stationary sampling and report uncertainty in time-averaged capture.

## Required outputs for every case

| Output | Why it matters |
|---|---|
| Air mass flow through each level | Distinguishes weak capture from poor air delivery |
| CO2 mass flux entering and leaving each level | Provides the primary level absorption balance |
| CO2 captured per level and total | Direct SRP performance result |
| Level capture fraction | Allows comparison while accounting for changing inlet concentration |
| Cumulative capture after each level | Shows diminishing returns through the collector |
| Pressure drop per level and total | Connects capture to fan demand |
| Flow/capture uniformity within each level | Identifies bypass and underused packing |
| CO2 concentration contours and outlet plume | Reveals bypass, mixing, and recirculation |
| Time mean, standard deviation, and sampling interval | Required for turbulent/unsteady cases |
| Global CO2 conservation error | Detects implementation or post-processing errors |

## Thesis-quality cautions

- Use **absorption** for uptake into a liquid phase and **adsorption** for binding onto a solid surface. State which mechanism the SRP device uses.
- Do not assign the same fixed capture percentage independently to every level unless experiments support it. Local velocity, inlet concentration, absorbent condition, and upstream depletion all change by level.
- Do not impose fresh ambient CO2 at every level; this would erase the coupling the thesis is meant to study.
- Do not claim chemical-kinetics fidelity when using an empirical capture relation. Present it as a calibrated reduced-order submodel.
- Clamp or otherwise bound empirical \(\eta\) relations to the physical interval \([0,1]\), and never extrapolate beyond their calibration range without an uncertainty study.
- Keep paper-specific material properties and correlations separate from SRP-specific inputs.
- Validate pressure drop and absorption separately before trusting a combined prediction.

## Best synthesis and potential thesis contribution

The strongest combination of these papers is not to reproduce either study. It is to use Zaynetdinov et al.'s level-scale porous-zone and sink methodology together with Eftekharian et al.'s turbulent scalar transport, empirical performance coupling, and plume-recirculation framework. The thesis contribution would then be a **level-resolved CFD model of the SRP collector** that explains where CO2 is removed, why capture differs among levels, and how those differences trade off against pressure drop and operating conditions.

The central result should be a level-by-level capture and pressure-loss map, supported by conservation checks and validation, rather than only a single whole-unit capture percentage.
