# SRP CO2 Collector Equation Sheet

## Source and transcription policy

Primary source: K. Zaynetdinov et al., ["Adsorption performance of radial-flow contactors for direct air capture"](../OtherResearch/Adsorption%20performance%20of%20radial-flow%20contactors%20for%20direct%20air%20capture%3A%20A%20computational%20study.pdf), *Chemical Engineering Science* 339 (2027) 125236, DOI: `10.1016/j.ces.2026.125236`.

This sheet distinguishes three types of equations:

- **Original paper equation:** transcribed using the paper's notation and original equation number.
- **SRP/NGA2 adaptation:** a deliberately changed form, shown next to the original with the reason for the change.
- **Project equation:** an equation added for implementation, validation, or post-processing. These are labeled `P1`, `P2`, and so on and are not attributed to the radial paper.

The paper models a 2D axisymmetric radial contactor in Ansys Fluent. The SRP model uses a 3D Cartesian channel with porous bead rods in NGA2. The adsorption methodology transfers; the radial geometry does not.

> **Terminology:** uptake by the solid beads is **adsorption**, not liquid-phase absorption.

---

## 1. Adsorption model and experimental parameter extraction

### Paper Eq. (1): linear driving force model

**Original paper equation:**

\[
\boxed{
\frac{\partial q}{\partial t}
=k_{\mathrm{LDF}}\left(q_{\mathrm{eq}}-q\right)
}
\qquad\text{[Paper Eq. (1), p. 3]}
\]

Here, \(q\) is the actual amount of adsorbed CO2, \(q_{\mathrm{eq}}\) is the equilibrium adsorption capacity, and \(k_{\mathrm{LDF}}\) is the mass-transfer coefficient.

**SRP/NGA2 adaptation:**

\[
\boxed{
\frac{\partial q_{CO_2}}{\partial t}
=k_{\mathrm{LDF},CO_2}
\left(q_{\mathrm{eq},CO_2}-q_{CO_2}\right)
}
\tag{A1}
\]

**Change and reason:** Only subscripts were added. They distinguish CO2 loading from the future water-loading variable. The kinetics are otherwise unchanged.

### Paper Eq. (2): experimental CO2 mass balance

**Original paper equation:**

\[
\boxed{
\frac{\partial m_{CO_2}}{\partial t}
=\dot n_{\mathrm{tot}}M_{CO_2}
\left[y_{\mathrm{in}}-y_{\mathrm{out}}(t)\right]
}
\qquad\text{[Paper Eq. (2), p. 4]}
\]

This equation converts the inlet-outlet CO2 mole-fraction difference in a breakthrough experiment into a captured CO2 mass rate.

**SRP use:** No mathematical change is required. Apply it to Justin's breakthrough data only if total molar flow and time-resolved inlet/outlet mole fractions are available.

### Paper Eq. (3): amount of CO2 adsorbed

**Original paper equation:**

\[
\boxed{
n_{CO_2}
=\dot n_{\mathrm{tot}}
\int_{t_0}^{t_1}
\left[y_{\mathrm{in}}-y_{\mathrm{out}}(t)\right]dt
}
\qquad\text{[Paper Eq. (3), p. 4]}
\]

**SRP use:** No change. This is useful for converting a measured breakthrough curve into total moles captured.

### Paper Eq. (4): equilibrium capacity from an experiment

**Original paper equation:**

\[
\boxed{
q_{\mathrm{eq}}=\frac{n_{CO_2}}{m_{\mathrm{ads}}}
}
\qquad\text{[Paper Eq. (4), p. 4]}
\]

**SRP use:** No change if \(q_{\mathrm{eq}}\) is reported in mol CO2 per kg of dry adsorbent. Keep the mass basis consistent.

### Paper Eq. (5): captured mass rate from loading rate

**Original paper equation:**

\[
\boxed{
\frac{\partial m_{CO_2}}{\partial t}
=m_{\mathrm{ads}}M_{CO_2}\frac{\partial q}{\partial t}
}
\qquad\text{[Paper Eq. (5), p. 4]}
\]

**SRP use:** No change. This equation links bead loading to removal from the gas phase.

### Paper Eq. (6): LDF form of the captured mass rate

**Original paper equation:**

\[
\boxed{
\frac{\partial m_{CO_2}}{\partial t}
=k_{\mathrm{LDF}}m_{\mathrm{ads}}M_{CO_2}
\left[q_{\mathrm{eq}}-q(t)\right]
}
\qquad\text{[Paper Eq. (6), p. 4]}
\]

**SRP use:** No change. Paper Eq. (6) follows by substituting Paper Eq. (1) into Paper Eq. (5).

### Paper Eq. (7): LDF coefficient estimated from breakthrough data

**Original paper equation:**

\[
\boxed{
k_{\mathrm{LDF}}
=\frac{
\dot n_{\mathrm{tot}}
\left[y_{\mathrm{in}}-y_{\mathrm{out}}(t)\right]
}{
m_{\mathrm{ads}}
\left[q_{\mathrm{eq}}-q(t)\right]
}
}
\qquad\text{[Paper Eq. (7), p. 4]}
\]

**SRP use:** The structure is unchanged, but the SRP bead data must be used. Do not copy the paper's value \(k_{\mathrm{LDF}}=0.001\ \mathrm{s^{-1}}\).

### Paper Eq. (8): bead specific heat capacity

**Original paper equation:**

\[
\boxed{
c_p=\frac{e^2}{\rho k}
}
\qquad\text{[Paper Eq. (8), p. 4]}
\]

Here, \(e\) is thermal effusivity, \(\rho\) is adsorbent density, and \(k\) is thermal conductivity.

**SRP use:** No change if SRP measures those three bead properties using compatible definitions.

---

## 2. Governing CFD equations

### Paper Eq. (9): steady continuity

**Original paper equation:**

\[
\boxed{
\nabla\cdot(\rho\vec v)=0
}
\qquad\text{[Paper Eq. (9), Table 1, p. 4]}
\]

The paper solves a steady flow field before solving transient CO2 and energy transport.

**SRP/NGA2 adaptation:**

For the constant-density NGA2 airflow case:

\[
\boxed{
\nabla\cdot\mathbf{u}=0
}
\tag{A2}
\]

**Change and reason:** Density is taken outside the divergence and canceled because the initial SRP pressure-drop simulation assumes constant-density air. \(\vec v\) was renamed \(\mathbf{u}\) to match common NGA2 velocity notation. The equation remains three-dimensional.

### Paper Eq. (10): steady momentum with porous resistance

**Original paper equation:**

\[
\boxed{
\nabla\cdot(\rho\vec v\vec v)
=-\nabla p
+\nabla\cdot
\left[\mu\left(\nabla\vec v+\nabla\vec v^{\mathsf T}\right)\right]
-\left(
\frac{\mu}{\alpha}\vec v
+C_2\frac{1}{2}\rho\lVert\vec v\rVert\vec v
\right)
}
\qquad\text{[Paper Eq. (10), Table 1, p. 4]}
\]

**SRP/NGA2 adaptation:**

\[
\boxed{
\frac{\partial(\rho\mathbf{u})}{\partial t}
+\nabla\cdot(\rho\mathbf{u}\mathbf{u})
=-\nabla p
+\nabla\cdot
\left[\mu\left(\nabla\mathbf{u}+\nabla\mathbf{u}^{\mathsf T}\right)\right]
-\chi_p\left(
\frac{\mu}{\alpha}\mathbf{u}
+C_2\frac{1}{2}\rho\lVert\mathbf{u}\rVert\mathbf{u}
\right)
}
\tag{A3}
\]

**Changes and reasons:**

1. The transient momentum term was added because NGA2 advances the flow in time even when the desired final result is statistically steady.
2. The mask \(\chi_p\) was added: \(\chi_p=1\) inside bead-rod cells and \(\chi_p=0\) in the open channel. The paper does not need an explicit mask because its porous resistance is assigned only to the Fluent porous zone.
3. The velocity symbol was renamed. The Darcy-Forchheimer physics and signs were not changed.

### Paper Eq. (11): transient CO2 transport

**Original paper equation:**

\[
\boxed{
\frac{\partial}{\partial t}
\left(\varepsilon\rho Y_{CO_2}\right)
+\nabla\cdot\left(\rho\vec vY_{CO_2}\right)
=-\nabla\cdot\vec J_{CO_2}+S_{CO_2}
}
\qquad\text{[Paper Eq. (11), Table 1, p. 4]}
\]

**SRP/NGA2 adaptation:**

\[
\boxed{
\frac{\partial}{\partial t}
\left(\varepsilon\rho Y_{CO_2}\right)
+\nabla\cdot\left(\rho\mathbf{u}Y_{CO_2}\right)
=-\nabla\cdot\mathbf{J}_{CO_2}
+\chi_p S_{CO_2}
}
\tag{A4}
\]

**Change and reason:** A porous-region mask was added to prevent adsorption outside the bead rods. The velocity and flux typography changed, but the transport equation did not.

### Paper Eq. (12): fluid-zone energy equation

**Original paper equation:**

\[
\boxed{
\frac{\partial}{\partial t}
\left(\varepsilon\rho_fE_f\right)
+\nabla\cdot\left[\vec v(\rho_fE_f+p)\right]
=\nabla\cdot\left(
\varepsilon k_f\nabla T_f-h_{CO_2}\vec J_{CO_2}
\right)
+h_{fs}A_{fs}(T_s-T_f)
+S_E
}
\qquad\text{[Paper Eq. (12), Table 1, p. 4]}
\]

**SRP use:** Preserve this equation if a full gas-energy model is implemented. For the February core model, isothermal flow may be used first, provided that the limitation is stated and temperature sensitivity is evaluated later.

### Paper Eq. (13): solid-zone energy equation

**Original paper equation:**

\[
\boxed{
\frac{\partial}{\partial t}
\left[(1-\varepsilon)\rho_sE_s\right]
=\nabla\cdot\left[(1-\varepsilon)k_s\nabla T_s\right]
+h_{fs}A_{fs}(T_f-T_s)
}
\qquad\text{[Paper Eq. (13), Table 1, p. 4]}
\]

**SRP/NGA2 adaptation:** Multiply the solid storage, conduction, and interphase-transfer terms by \(\chi_p\), or solve the solid equation only on bead-rod cells.

**Change and reason:** The paper's solid zone spatially coincides with its complete porous bed. The SRP mesh also contains open-channel cells with no solid bead phase.

### Paper Eq. (14): CO2 diffusion flux

**Original paper equation:**

\[
\boxed{
\vec J_{CO_2}
=-\rho D_{m,CO_2}\nabla Y_{CO_2}
}
\qquad\text{[Paper Eq. (14), Table 1, p. 4]}
\]

**SRP/NGA2 adaptation:**

\[
\boxed{
\mathbf{J}_{CO_2}
=-\rho
\left(D_{m,CO_2}+\frac{\nu_t}{Sc_t}\right)
\nabla Y_{CO_2}
}
\tag{A5}
\]

**Change and reason:** The paper uses laminar molecular diffusion. The added \(\nu_t/Sc_t\) term represents turbulent scalar transport if the SRP simulation uses an LES subgrid model. Set \(\nu_t=0\) for a laminar simulation.

### Paper Eq. (15): gas-phase CO2 adsorption sink

**Original paper equation:**

\[
\boxed{
S_{CO_2}
=-\frac{m_{\mathrm{ads}}M_{CO_2}}{V_{\mathrm{cell}}}
\frac{\partial q}{\partial t}
}
\qquad\text{[Paper Eq. (15), p. 4]}
\]

**SRP/NGA2 adaptation:**

If cell adsorbent mass is calculated from void fraction and solid density,

\[
\boxed{
S_{CO_2}
=-(1-\varepsilon)\rho_sM_{CO_2}
\frac{\partial q_{CO_2}}{\partial t}
}
\tag{A6}
\]

because

\[
m_{\mathrm{ads,cell}}
=(1-\varepsilon)\rho_sV_{\mathrm{cell}}.
\tag{A7}
\]

**Change and reason:** Paper Eq. (15) is retained algebraically, but the adsorbent mass per cell is written using quantities that can be stored as NGA2 fields. Use the original equation instead if SRP supplies adsorbent mass directly for each rod or cell.

### Paper Eq. (16): fluid-energy source

**Original paper equation:**

\[
\boxed{
S_E
=S_{CO_2}
\left[
c_p(T-T_{\mathrm{ref}})
-\frac{\Delta H}{M_{CO_2}}
\right]
}
\qquad\text{[Paper Eq. (16), p. 4]}
\]

**SRP use:** No change should be made until the sign convention and units for SRP's adsorption enthalpy are confirmed. This source is omitted in an isothermal first model.

---

## 3. Adsorption, pressure-loss, and heat-transfer closures

### Paper Eq. (17): Toth equilibrium isotherm

**Original paper equation:**

\[
\boxed{
q_{\mathrm{eq}}
=\frac{q_mbp_{CO_2}}
{\left[1+(bp_{CO_2})^{t_{\mathrm{Toth}}}\right]^{1/t_{\mathrm{Toth}}}}
}
\qquad\text{[Paper Eq. (17), p. 5]}
\]

**SRP/NGA2 adaptation:**

\[
\boxed{
q_{\mathrm{eq},CO_2}
=\frac{q_{m,CO_2}b_{CO_2}p_{CO_2}}
{\left[1+(b_{CO_2}p_{CO_2})^{t_{\mathrm{Toth},CO_2}}\right]^{1/t_{\mathrm{Toth},CO_2}}}
}
\tag{A8}
\]

**Change and reason:** Only CO2 subscripts were added to prepare for a later water model. All parameters must be fitted to the SRP beads; none should be copied from the paper's commercial resin.

### Paper Eq. (18): Ergun viscous resistance

**Original paper equation:**

\[
\boxed{
\frac{1}{\alpha}
=150\frac{(1-\varepsilon)^2}{d_p^2\varepsilon^3}
}
\qquad\text{[Paper Eq. (18), p. 5]}
\]

**SRP use:** Use as an initial estimate only. Prefer permeability fitted to Justin's pressure-drop measurements because the SRP bead rods may not behave like the paper's randomly packed spherical bed.

### Paper Eq. (19): Ergun inertial resistance

**Original paper equation:**

\[
\boxed{
C_2
=3.5\frac{1-\varepsilon}{d_p\varepsilon^2}
}
\qquad\text{[Paper Eq. (19), p. 5]}
\]

**SRP use:** Use the paper's exact porosity convention only when reproducing its formulation. Other Ergun/solver conventions can place a different power of \(\varepsilon\) in the coefficient, so the NGA2 velocity definition and pressure-drop data must determine the appropriate implementation.

### Paper Eqs. (20)-(23): interphase heat-transfer closure

**Original paper equations:**

\[
\boxed{
Nu=2+1.1Re_p^{0.6}Pr^{1/3}
}
\qquad\text{[Paper Eq. (20), p. 5]}
\]

\[
\boxed{
Nu=\frac{h_{fs}d_p}{k_f}
}
\qquad\text{[Paper Eq. (21), p. 5]}
\]

\[
\boxed{
Re_p=\frac{\rho d_pv_\infty}{\mu}
}
\qquad\text{[Paper Eq. (22), p. 5]}
\]

\[
\boxed{
A_{fs}=\frac{6(1-\varepsilon)}{d_p}
}
\qquad\text{[Paper Eq. (23), p. 5]}
\]

**SRP use:** No algebraic change is proposed. Before use, confirm that the spherical-particle Wakao-Kaguei and interfacial-area assumptions reasonably describe the SRP beads.

---

## 4. Paper geometry and performance equations

These equations are included for provenance but are not all appropriate for SRP's Cartesian rod geometry.

### Paper Eq. (24): radial-bed aspect ratio

\[
\boxed{
AR=\frac{L}{R-r}
}
\qquad\text{[Paper Eq. (24), p. 5]}
\]

**SRP decision:** Do not reuse this definition unless the SRP device is represented as a radial annular bed. Define Cartesian spacing, thickness, and orientation parameters instead.

### Paper Eq. (25): radial-bed radius ratio

\[
\boxed{
RR=\frac{r}{R}
}
\qquad\text{[Paper Eq. (25), p. 5]}
\]

**SRP decision:** Not applicable to a Cartesian bead-rod channel.

### Paper Eq. (26): radial flow-uniformity index

\[
\boxed{
\eta
=\sqrt{\frac{\Delta p_{\mathrm{in}}}{\Delta p_{\mathrm{out}}}}
}
\qquad\text{[Paper Eq. (26), p. 7]}
\]

The paper defines \(\Delta p_{\mathrm{in}}\) and \(\Delta p_{\mathrm{out}}\) as radial bed pressure drops near the axial inlet and outlet.

**SRP decision:** Do not call this the SRP uniformity index without an equivalent geometric definition. Use the project flow-maldistribution metric `P7` below for multiple rods or levels.

### Paper Eq. (27): specific energy requirement

**Original paper equation:**

\[
\boxed{
SER
=\frac{\Delta p\,\dot m\,t_{\mathrm{sat}}}
{\rho m_{CO_2}}
}
\qquad\text{[Paper Eq. (27), p. 7]}
\]

**SRP/NGA2 adaptation:**

If electrical rather than ideal fluid energy is required,

\[
\boxed{
SER_{\mathrm{electric}}
=\frac{\Delta p\,Q\,t}
{\eta_{\mathrm{fan}}m_{CO_2}}
}
\tag{A9}
\]

**Change and reason:** Paper Eq. (27) uses \(Q=\dot m/\rho\) and represents ideal pressure-volume work. The adapted equation explicitly includes fan efficiency. If \(\eta_{\mathrm{fan}}\) is unknown, report the paper's ideal SER and label it clearly.

---

## 5. Project equations not copied from the radial paper

These equations are needed for the SRP implementation and validation, but they do not appear as numbered equations in the radial paper.

### Project Eqs. (P1)-(P2): fit the porous pressure-drop data

Starting from the one-dimensional form of Paper Eq. (10):

\[
\boxed{
\frac{\Delta p}{L_p}
=\frac{\mu}{\alpha}U_s
+\frac{1}{2}\rho C_2U_s^2
}
\tag{P1}
\]

Fit the experimental data to

\[
\frac{\Delta p}{L_p}=AU_s+BU_s^2,
\]

then calculate

\[
\boxed{
\alpha=\frac{\mu}{A},
\qquad
C_2=\frac{2B}{\rho}
}.
\tag{P2}
\]

**Why added:** Paper Eqs. (18)-(19) calculate resistance from bead diameter and porosity. The SRP project expects experimental pressure-drop data, which should be used to calibrate the actual rods.

### Project Eq. (P3): area-averaged pressure drop

\[
\boxed{
\bar p_A=\frac{1}{A}\int_Ap\,dA,
\qquad
\Delta p=\bar p_{\mathrm{in}}-\bar p_{\mathrm{out}}
}
\tag{P3a}
\]

For the Cartesian NGA2 implementation, a pressure plane at streamwise cell index \(i_s\) is evaluated with the fluid volume fraction \(VF\):

\[
\boxed{
\bar p_{i_s}
=
\frac{
\sum_{j,k}p_{i_s,j,k}\,VF_{i_s,j,k}\,\Delta y_j\Delta z_k
}{
\sum_{j,k}VF_{i_s,j,k}\,\Delta y_j\Delta z_k
},
\qquad
\Delta p_s=\bar p_{i_{\mathrm{up}}}-\bar p_{i_{\mathrm{down}}}
}
\tag{P3b}
\]

The sample indices are the cells containing the configured upstream and downstream pressure coordinates. The domain-boundary pressure drop uses the same area weighting at the first and last streamwise pressure cells.

**Why added:** This defines exactly how simulation pressure drop is calculated for comparison with experiments and documents the discrete volume-fraction weighting used by the implemented monitor.

For a stack with sheet centers \(x_m\) and pressure-sampling offset \(\delta_p\), the implemented per-sheet and whole-stack diagnostics are

\[
\boxed{
\Delta p_m=\bar p_A(x_m-\delta_p)-\bar p_A(x_m+\delta_p),
\qquad
\Delta p_{\Sigma}=\sum_{m=1}^{N_s}\Delta p_m,
}
\tag{P3c}
\]

\[
\boxed{
\Delta p_{\mathrm{stack}}
=\bar p_A(x_1-\delta_p)-\bar p_A(x_{N_s}+\delta_p),
\qquad
\epsilon_{\Delta p}
=\frac{|\Delta p_{\Sigma}-\Delta p_{\mathrm{stack}}|}
{\max(|\Delta p_{\mathrm{stack}}|,\epsilon_{\mathrm{mach}})}.
}
\tag{P3d}
\]

For a regularly spaced multi-sheet stack, the default \(\delta_p=S_s/2\) places shared planes halfway between sheets, so the per-sheet differences telescope to the sampled stack pressure drop. A configurable offset supports future experimental tap locations, but overlapping sample regions are rejected.

### Project Eqs. (P4)-(P5): flow and airflow conservation

\[
\boxed{
Q=\int_A\mathbf{u}\cdot\mathbf{n}\,dA,
\qquad
\dot m=\int_A\rho\mathbf{u}\cdot\mathbf{n}\,dA
}
\tag{P4}
\]

\[
\boxed{
\epsilon_{\dot m}
=\frac{|\dot m_{\mathrm{in}}-\dot m_{\mathrm{out}}|}
{\dot m_{\mathrm{in}}}
}
\tag{P5a}
\]

The implemented monitor protects the denominator when the inlet flow is zero:

\[
\boxed{
\epsilon_{\dot m}^{\mathrm{NGA2}}
=
\frac{|\dot m_{\mathrm{in}}-\dot m_{\mathrm{out}}|}
{\max\!\left(|\dot m_{\mathrm{in}}|,\epsilon_{\mathrm{mach}}\right)}
}
\tag{P5b}
\]

**Why added:** These provide a basic numerical correctness check for every flow case. `P5b` records the exact denominator protection used in the code; it is equivalent to `P5` for every nonzero-flow case.

### Project Eqs. (P6)-(P7): flow split and maldistribution

\[
\boxed{
f_\ell
=\frac{\dot m_\ell}{\sum_{j=1}^{N}\dot m_j},
\qquad
\sum_{\ell=1}^{N}f_\ell=1
}
\tag{P6}
\]

\[
\boxed{
CV_{\dot m}
=\frac{
\sqrt{\frac{1}{N}\sum_{\ell=1}^{N}
(\dot m_\ell-\overline{\dot m})^2}
}{\overline{\dot m}}
}
\tag{P7}
\]

**Why added:** Paper Eq. (26) is specific to its radial geometry. `P7` measures flow maldistribution among SRP rods or levels without assuming a radial inlet and outlet.

**Current NGA2 implementation:** At a configurable `x`-face, the detected open passage is divided into `N` equal-width `y` bands. Each \(\dot m_\ell\) is the sum of \(\rho U\,\Delta y\,\Delta z\) over the staggered faces in that band. NGA2's immersed-boundary treatment is already represented in the face velocity, so the diagnostic does not multiply by cell volume fraction again. The monitor reports every band rate and fraction, their sums, and `P7`. These bands are a cross-passage diagnostic; they are not yet per-rod or per-sheet control volumes.

### Project Eq. (P8): ppm conversion

\[
\boxed{
y_{CO_2}=C_{ppm}\times10^{-6},
\qquad
Y_{CO_2}
=\frac{y_{CO_2}M_{CO_2}}
{\sum_jy_jM_j}
}
\tag{P8}
\]

**Why added:** The paper specifies an inlet concentration in ppm but does not provide a numbered conversion equation. NGA2 must use a clearly defined scalar basis.

### Project Eq. (P9): per-level CO2 capture

\[
\boxed{
\dot m_{CO_2,A}
=\int_A
\left(\rho Y_{CO_2}\mathbf{u}+\mathbf{J}_{CO_2}\right)
\cdot\mathbf{n}\,dA
}
\tag{P9a}
\]

\[
\boxed{
\dot m_{\mathrm{capt},\ell}
=\dot m_{CO_2,\mathrm{in},\ell}
-\dot m_{CO_2,\mathrm{out},\ell},
\qquad
\eta_\ell
=1-\frac{\dot m_{CO_2,\mathrm{out},\ell}}
{\dot m_{CO_2,\mathrm{in},\ell}}
}
\tag{P9b}
\]

**Why added:** The thesis requires capture resolved by rod or level. The radial paper reports whole-contactor results rather than this specific SRP accounting definition.

### Project Eq. (P10): global transient CO2 conservation

\[
\boxed{
\dot m_{CO_2,\mathrm{in}}
-\dot m_{CO_2,\mathrm{out}}
=\frac{d}{dt}
\int_V\varepsilon\rho Y_{CO_2}\,dV
-\int_VS_{CO_2}\,dV
}
\tag{P10}
\]

**Why added:** This checks that the decrease in gas-phase CO2 equals accumulation plus adsorption. It should be verified before interpreting capture predictions.

### Project Eq. (P11): stable LDF time update

For approximately constant \(q_{\mathrm{eq}}\) over one numerical step, the exact update of Paper Eq. (1) is

\[
\boxed{
q^{n+1}
=q_{\mathrm{eq}}
+\left(q^n-q_{\mathrm{eq}}\right)
e^{-k_{\mathrm{LDF}}\Delta t}
}
\tag{P11}
\]

**Why added:** This integrates the paper's LDF equation more robustly than a forward-Euler source update. It does not change the LDF model.

### Project Eqs. (P12)-(P13): proposed water and regeneration extension

The radial paper does **not** explicitly solve water transport, competitive adsorption, or regeneration. A possible extension is

\[
\boxed{
\frac{\partial}{\partial t}(\varepsilon\rho Y_{H_2O})
+\nabla\cdot(\rho\mathbf{u}Y_{H_2O})
=-\nabla\cdot\mathbf{J}_{H_2O}+S_{H_2O}
}
\tag{P12}
\]

\[
\boxed{
\frac{\partial q_{H_2O}}{\partial t}
=k_{\mathrm{LDF},H_2O}
\left(q_{\mathrm{eq},H_2O}-q_{H_2O}\right),
\qquad
S_{H_2O}
=-\frac{m_{\mathrm{ads}}M_{H_2O}}{V_{\mathrm{cell}}}
\frac{\partial q_{H_2O}}{\partial t}
}
\tag{P13}
\]

with competitive equilibrium relations such as

\[
q_{\mathrm{eq},CO_2}=f(p_{CO_2},p_{H_2O},T),
\qquad
q_{\mathrm{eq},H_2O}=g(p_{CO_2},p_{H_2O},T).
\]

**Why added:** The to-do list calls for moisture and humid-air regeneration, but the radial paper only embeds humidity indirectly through CO2 parameters fitted to humid experiments. The project needs additional material data before `P12`-`P13` can be treated as a validated model.

Regeneration should arise when changed conditions produce \(q_{CO_2}>q_{\mathrm{eq},CO_2}\). Paper Eq. (1) then gives \(\partial q_{CO_2}/\partial t<0\), and Paper Eq. (15) naturally becomes a positive gas-phase CO2 source. The sign should not be reversed manually.

### Project Eq. (P14): convective CFL number

\[
\boxed{
CFL
=\Delta t\left(
\frac{|u|}{\Delta x}
+\frac{|v|}{\Delta y}
+\frac{|w|}{\Delta z}
\right)
}
\tag{P14}
\]

**Why added:** This provides a time-step stability diagnostic for the Cartesian NGA2 simulation.

### Project Eq. (P15): grid-change metric

\[
\boxed{
\delta_{\mathrm{grid}}
=100\frac{|\phi_{\mathrm{fine}}-\phi_{\mathrm{coarse}}|}
{|\phi_{\mathrm{fine}}|}\%
}
\tag{P15}
\]

**Why added:** The paper performs mesh and time-step sensitivity studies but does not assign a numbered equation to the comparison. Apply this to pressure drop, flow split, and adsorption performance.

### Project Eq. (P16): implemented porous-slab mask

For the current verification geometry, the cell-centered porous mask is

\[
\boxed{
\chi_{p,i,j,k}
=
\begin{cases}
1,
&x_{\mathrm{start}}\le x_{m,i}<x_{\mathrm{end}}
\ \text{and}\ VF_{i,j,k}>0.5,\\[2mm]
0,&\text{otherwise}.
\end{cases}
}
\tag{P16}
\]

Equal bounds, \(x_{\mathrm{start}}=x_{\mathrm{end}}\), disable the porous region. The same mask is exported as `porous_mask` for visual inspection. Bead-rod geometry will replace only this geometric definition; it will not change the resistance law.

For the provisional `aligned_rods_z` geometry, \(N_r\) cylindrical rods have axes parallel to \(z\), common streamwise center \(x_s\), diameter \(d_r\), and first-to-last center span \(S_r\). Their transverse centers are

\[
\boxed{
y_\ell=
\begin{cases}
0,&N_r=1,\\[1mm]
-\dfrac{S_r}{2}
+\dfrac{\ell-1}{N_r-1}S_r,
&N_r>1,
\end{cases}
\qquad \ell=1,\ldots,N_r
}
\tag{P16b}
\]

and the corresponding cell-centered mask is

\[
\boxed{
\chi_{p,i,j,k}=1
\quad\text{if}\quad
\min_{1\le\ell\le N_r}
\left[(x_{m,i}-x_s)^2+(y_{m,j}-y_\ell)^2\right]
\le\left(\frac{d_r}{2}\right)^2
\quad\text{and}\quad VF_{i,j,k}>0.5,
}
\tag{P16c}
\]

with \(\chi_p=0\) otherwise. The current reference uses \(N_r=4\), \(d_r=0.1\), \(S_r=0.6\), and \(x_s=2\); these values are provisional and do not replace advisor-confirmed geometry.

For the provisional stacked extension, \(N_s\) copies of the aligned sheet use center-to-center spacing \(S_s\) about stack center \(x_c\):

\[
\boxed{
x_m=x_c+
\left(m-1-\frac{N_s-1}{2}\right)S_s,
\qquad m=1,\ldots,N_s,
}
\tag{P16d}
\]

and `P16c` takes the minimum over both sheet index \(m\) and rod index \(\ell\). The center-to-center stack span is \((N_s-1)S_s\), while the porous streamwise depth including the rod diameter is

\[
\boxed{D_{\mathrm{stack}}=(N_s-1)S_s+d_r.}
\tag{P16e}
\]

The verified synthetic reference uses three sheets centered at \(x=1.5,2.0,2.5\), each with the same four provisional rods. Sheet count, spacing, center, and resulting depth must be replaced by confirmed contactor geometry before physical use.

### Project Eq. (P17): staggered-face Darcy-Forchheimer source

NGA2 stores velocity components on staggered faces. For a face \(f\), the implemented interpolated mask and speed are

\[
\boxed{
\chi_{p,f}=\mathcal I_f(\chi_p),
\qquad
s_f=\mathcal I_f\!\left(
\sqrt{u_c^2+v_c^2+w_c^2}
\right)
}
\tag{P17a}
\]

where \(\mathcal I_f\) is NGA2's cell-to-face interpolation and the subscript \(c\) denotes cell-centered interpolated velocity. The resistance added to the momentum residual for component \(u_{q,f}\), \(q\in\{x,y,z\}\), is

\[
\boxed{
S_{q,f}^{\mathrm{por}}
=-\chi_{p,f}
\left(
\frac{\mu}{\alpha}
+\frac{1}{2}\rho C_2s_f
\right)u_{q,f}
}
\tag{P17b}
\]

Thus both terms oppose the local velocity. Here \(\alpha>0\) has units of area and \(C_2\ge0\) has units of inverse length. The input `Forchheimer coefficient` defaults to zero when absent, preserving Darcy-only and historical cases.

### Project Eq. (P18): independent uniform-slab reference cases

For a uniform superficial velocity \(U_s\) through a slab of length \(L_p\), the two terms in `P1` were verified separately:

\[
\boxed{
\Delta p_D
=\frac{\mu}{\alpha}U_sL_p,
\qquad
\Delta p_F
=\frac{1}{2}\rho C_2U_s^2L_p
}
\tag{P18}
\]

The Darcy verification used \(\mu=0.01\), \(\alpha=0.01\), \(U_s=1\), \(L_p=1\), and \(C_2=0\), giving \(\Delta p_D=1\). The Forchheimer verification used \(\rho=1\), \(C_2=2\), \(U_s=1\), \(L_p=1\), and effectively infinite permeability, giving \(\Delta p_F=1\). Each simulated excess pressure drop equaled `1` within printed precision.

### Project Eq. (P19): paired-case verification error

The porous contribution is isolated from any common numerical or open-channel pressure loss with a paired control:

\[
\boxed{
\Delta p_{\mathrm{por,sim}}
=\Delta p_{\mathrm{sample,porous}}
-\Delta p_{\mathrm{sample,control}},
\qquad
\epsilon_{\Delta p}
=\frac{
\left|\Delta p_{\mathrm{por,sim}}-\Delta p_{\mathrm{por,ref}}\right|
}{
\left|\Delta p_{\mathrm{por,ref}}\right|
}
}
\tag{P19}
\]

The control uses the same mesh, boundary conditions, time step, and sampling planes as its resistance case.

### Project Eq. (P20): flow-through time and averaging window

The characteristic flow-through time and the final-window mean of a monitored quantity \(\phi\) are

\[
\boxed{
t_{\mathrm{flow}}=\frac{L_x}{U_{\mathrm{in}}},
\qquad
\overline{\phi}_{W}
=\frac{1}{N_W}\sum_{n\in W}\phi^n
}
\tag{P20}
\]

The provisional target-mesh baseline ran to \(t=t_{\mathrm{flow}}=4\) and used the final 25% of the run, \(W=[3,4]\), containing 501 recorded samples.

### Project Eq. (P21): steady-window pressure-drop criterion

The implemented baseline assessment used the normalized range

\[
\boxed{
R_{\Delta p,W}
=\frac{
\max_{n\in W}(\Delta p^n)-\min_{n\in W}(\Delta p^n)
}{
\left|\overline{\Delta p}_{W}\right|
}
}
\tag{P21}
\]

The predeclared provisional criterion was \(R_{\Delta p,W}\le0.01\), maximum mass-flow error from `P5` no greater than \(10^{-10}\), CFL no greater than `0.8`, and finite bounded divergence and pressure-solver diagnostics. The target-mesh run gave \(R_{\Delta p,W}=0.00123082\), or `0.123082%`.

---

## 6. Equation-to-task map

| SRP task | Equations to use | Status |
|---|---|---|
| Open-channel flow | Paper Eq. (9), adaptation `A2`; Paper Eq. (10) with \(\chi_p=0\); `P20`-`P21` | Implemented and provisionally converged |
| Porous slab verification | Adaptation `A3`; `P16`-`P19` | Darcy and Forchheimer terms independently verified |
| Porous bead-rod flow | Paper Eq. (10), adaptation `A3`; `P16b`-`P16e` | Provisional aligned single-sheet and three-sheet masks verified; advisor geometry pending |
| Initial resistance estimate | Paper Eqs. (18)-(19) | Estimate only |
| Fit Justin's pressure data | `P1`-`P3`, `P19` | Awaiting measured data |
| Flow validation | `P3`-`P7`, `P14`-`P15`, `P19`-`P21` | Pressure, conservation, and equal-width flow-split checks implemented; physical validation pending |
| CO2 scalar transport | Paper Eqs. (11), (14); adaptations `A4`-`A5` | Add after flow validation |
| CO2 bead loading | Paper Eqs. (1), (17); adaptations `A1`, `A8` | Requires SRP material data |
| Gas-phase adsorption sink | Paper Eq. (15), adaptation `A6` | Core capture coupling |
| Per-level capture | `P9`-`P10` | Required thesis output |
| Temperature | Paper Eqs. (12)-(13), (16), (20)-(23) | Later phase |
| Water/regeneration | `P12`-`P13` | Proposed extension, not in paper |

## 7. Paper assumptions that must accompany the equations

The equations should not be cited without their modeling context:

- The paper treats air as an ideal-gas mixture of N2 and CO2.
- The paper assumes laminar flow for its primary simulations.
- The porous bed is homogeneous and isotropic with constant effective porosity.
- Individual particles and pore-scale flow are not resolved.
- The flow field is solved at steady state first; transient species and energy equations are then solved using one-way coupling.
- The paper's CO2 parameters are derived from humid experiments, but water adsorption is not explicitly included in the CFD model.
- The paper's absolute adsorption predictions were not validated against radial-contactor breakthrough data; the model is used primarily for comparative geometry trends.
- All resistance, kinetic, equilibrium, and thermal parameters must be checked or refitted for SRP's beads.

## 8. Minimum February model

The smallest defensible model uses:

1. Paper Eq. (9) / adaptation `A2` for incompressible airflow.
2. Paper Eq. (10) / adaptation `A3` for porous bead-rod resistance.
3. Paper Eqs. (18)-(19) only as initial estimates, followed by `P1`-`P3` calibration.
4. Paper Eqs. (11) and (14) / adaptations `A4`-`A5` for CO2 transport.
5. Paper Eqs. (1), (15), and (17) / adaptations `A1`, `A6`, and `A8` for adsorption.
6. `P3`-`P10` for pressure sampling, conservation, flow distribution, and per-level capture.
7. `P14`-`P21` for time-step, grid, porous-source, and convergence verification.

Temperature and water can be added after this core model is running and validated.

