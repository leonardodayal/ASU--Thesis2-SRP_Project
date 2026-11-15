# Supporting Evidence Summary

Last reviewed: 2026-11-11

## Purpose and evidence rules

This document is the entry point for experimental correspondence, measurements, project requirements, and advisor feedback used by the SRP CFD work. It consolidates the facts needed for modeling while retaining the unique source files for provenance. Values are labeled as measured, reported, derived, provisional, or pending so that incomplete evidence is not treated as a calibrated physical input.

## Current conclusions

- The current NGA2 circular-stick cases are numerical verification configurations, not confirmed representations of the physical packet.
- The latest email thread provides a `10 cm x 10 cm` packet fill opening, eight horizontally stacked sorbent pockets, and a nominal `1.25 cm` pocket width before subtracting the thermal-seal width.
- Each pocket reportedly contains about `0.3 g` of unexchanged Purolite A501P in chloride form, or about `2.4 g` nominal across eight pockets. The resin had been stored humid and was dried for only a few hours, so the actual dry mass may be lower.
- Samantha reported CMS25 nylon mesh with `25 micrometre` pore size and `12.02%` open area for one packet. The same email thread says the latest tests included packed beads in a `40-micrometre` filter. These are likely different packet configurations; the missing spreadsheet and photographs are needed to map each measurement series to its mesh, frame, and bead loading before calibration.
- The latest advisor feedback, reported by Leonardo on 2026-11-06, recommends at least 10 cells across each physical stick thickness. The pockets are now confirmed to be rod-like and to bulge in both directions, but the filled thickness remains unresolved.
- The existing synthetic `0.1`-diameter stick has about six cells across it on the `256 x 64 x 64` grid and about ten on the `384 x 96 x 96` grid. This is a resolution comparison only, not a physical scale assignment.
- Preserve the present normal-through-sheet case as the test-stand/calibration configuration. Treat the later rotated packet arrangement with flow parallel to the packets and open passages above and below the sheets as a separate geometry.
- Samantha's 2026-11-06 response confirms that the pockets are rod-like and bulge in both directions, adjacent pockets are separated by `2 mm` solid thermo-sealed lines, thickness depends on fill, and the beads swell when wet. Thickness and seal airtightness remain pending.

## Latest email thread through 2026-11-05

The consolidated thread reports the following chronology.

### Pressure-drop request and orientation

- On 2026-10-19, Justin requested pressure-drop measurements through a mesh sheet or packet, with pore size and percent open recorded.
- The immediate test is flow normal through the sheet/packet for CFD calibration.
- Flow parallel to normally mounted packets is a later system-design configuration.

### Mesh tests and openness

| Material | Reported pore size | Reported openness | Status and notes |
|---|---:|---:|---|
| CMS25 CellMicroSieves nylon | `25 micrometre` | `12.02%` | New histogram result reported 2026-11-02; identified as the mesh used for the packet in Samantha's 2026-11-05 message. |
| MT125 Sefar Mechanical Tree polyester | `125 micrometre` | `32.98%` | New histogram result reported 2026-11-02; two-layer pressure-drop series is available. |
| APC25 AZPressCo | `25 micrometre` | `4.51%` | New histogram result reported 2026-11-02. |
| A25 Amazon nylon | `25 micrometre` | `8%` | Historical report value; not the CMS25 mesh used in Ramesh's later test. |
| MM40 polyester | `40 micrometre` | `25%` | Historical AUDACity report value. |

- Ramesh reported approximately `32 Pa` at `0.6 m/s` for the 25-micrometre nylon test, with large sensor fluctuations that limited the testable speed range. The complete numeric series is not present in the repository.
- The openness values were obtained from image histograms. The method deck referenced in the email is missing, so uncertainty and threshold sensitivity are not yet documented here.

### Latest packet and test information

- Ramesh reported completing runs with one filter, a blank frame, and packed beads.
- The packet fill opening is reported as `10 cm x 10 cm`.
- There are eight horizontally stacked individual sorbent pockets, also called sticks.
- Each pocket is nominally `1.25 cm` wide minus the thermal-seal width.
- Each pocket contains approximately `0.3 g` of unexchanged Purolite A501P in chloride form.
- The sorbent had been stored humid and was dried for a few hours in a hood; actual dry mass may therefore be below the nominal mass.
- Ramesh described a packed-bead test using a `40-micrometre` filter, while Samantha described a CMS25 nylon packet with `25-micrometre` pores and `12.02%` openness. Treat these as likely separate configurations, but do not assign data to either configuration until the missing spreadsheet and photographs establish the run mapping.

## Existing quantitative pressure-drop evidence

### MT125 two-layer normal-flow test

- Source: Ramesh's August wind-tunnel run, sent 2026-10-19.
- Configuration: two layers of MT125 mesh on a custom 3D-printed stand in a closed-loop wind tunnel.
- Measurements: 29 points from `0.1` to `2.9 m/s`, increasing from `1.6` to `75.6 Pa`.
- The `3.0 m/s` row is blank and is not a measurement.
- A reproduced unweighted zero-intercept fit is

  `Delta p = 13.3676 U + 4.42639 U^2` Pa.

- Fit diagnostics: `RMSE = 0.313 Pa`, `R^2 = 0.999805`.
- The raw transcription is preserved in `PhysicalMeasurments/mt_125_micron_two_layer_raw.csv`.
- This series characterizes the tested mesh/stand assembly. It cannot yet isolate mesh resistance because the empty-stand baseline, pressure-tap geometry, effective porous length, air properties, uncertainty, repeats, and velocity definition are missing.

### Historical Excellion assembly

- Configuration: 20 spacers populated with 20 sorbent-membrane sheets at `5 mm` vertical spacing in an Omega WT 4401D-D wind tunnel.
- Reported pressure drop is `4.5 Pa` at `1 m/s`; approximately `20 Pa` occurs at `2.5 m/s`.
- The preserved graph was previously read as `4.5`, `12.7`, `25.8`, `44.3`, and `65.2 Pa` at `1` through `5 m/s`.
- This is aggregate assembly evidence and must not be used as a bead-bed porous coefficient without geometry, baseline, and uncertainty metadata.

### November 5 blank, filter, and packed-bead workbook

- `Pressure Drop of Filter.xlsx` was recovered locally on 2026-11-11 and transcribed without filling its blank cells into `pressure_drop_filter_2026-11-05_raw.csv`.
- The packed series is labeled `With Beads Filled in 40 micron Filter` and contains 21 points from `0.00-0.20 m/s`, rising from `0.0-28.4 Pa`.
- The two-layer 40-micrometre filter series contains six points from `0.1-0.6 m/s` and `4.8-32.2 Pa`.  The blank stand is zero at `0.1-1.4 m/s` and rises to `1.8 Pa` at `3.0 m/s`.
- A zero-intercept Darcy fit to the complete packed-filter series gives `Delta p = 139.8293 U Pa`, `RMSE = 0.8344 Pa`, and `R^2 = 0.98934`.  A free Darcy-Forchheimer fit gives a negative quadratic term and is rejected as nonphysical; the provisional model therefore sets `C2 = 0`.
- Assuming the still-unverified `10.5 mm` filled thickness and `mu = 1.81e-5 Pa s`, the provisional effective assembly permeability is `1.35916e-9 m^2`.  This is not an isolated bead property, because matched mesh subtraction, thickness, air properties, and uncertainty remain unavailable.

## Historical sorbent and packet evidence

The 2023 AUDACity report provides useful context but is not a direct calibration source for the current pressure-drop model.

- A501 sorbent wind-tunnel tests used dry air around `3-5 ppt H2O` and approximately `25 degrees C`.
- Tests compared wind speeds of `0.7`, `2.5`, and `5 m/s` after one hour of desorption in `100 mM Na2CO3`.
- Reported full loading times were about `3.8`, `2.5`, and `2 h`, respectively.
- The elongated pixie-stick form dried in about `0.4 h` and reached about `670 micromole CO2/g` in `2 h` at `5 m/s`; a packed mesh bag took about `1.8 h` to begin adsorption and reached about `355 micromole CO2/g` after `12 h`.
- The report explicitly cautions that a suspected wind-tunnel leak or inaccessible sorbent in tight packing may explain the apparent capacity difference.
- These adsorption results may inform later transport work, but the present Phase 2 model must validate hydrodynamics and pressure loss first.

## Current project requirements

The current proposal defines a wind-driven rectangular contactor containing stacked mesh-encapsulated ion-exchange sorbent sheets. CFD and experiments are expected to evaluate pressure drop, sheet spacing, packing density, contactor length, flow-path geometry, airflow distribution, and bypassing.

Key deliverables are:

- D1.1: validated hydrodynamic CFD model of airflow distribution and pressure drop by Month 3;
- D1.2: experimental validation across multiple sheet spacings and contactor geometries by Month 4;
- D1.3: screening model linking wind, turbine/contactor behavior, ambient conditions, geometry, and capture productivity by Month 5;
- M1.1: identify a configuration with pressure drop no greater than `10 Pa` under representative conditions with average wind no greater than `2 m/s` by Month 5.

The 2026-10-29 team-meeting summary assigned Leonardo to calibrate the CFD model with blank and bead-filled pressure-drop data and prepare visual progress updates. Samantha was assigned to provide mesh geometry/openness and conduct packet and blank-stand tests. The Zoom summary is AI-generated and should be checked against participant recollection before being treated as a formal decision record.

## Geometry requirements still pending

Leonardo's 2026-11-02 email to Samantha Samples, copied to Justin Flory and Marcus Herrmann, explicitly requested the packet cross-sectional shape, filled thickness `t`, clear spacing `d`, a uniform bead layer held between two sheets for porous-coefficient calibration, and confirmation of whether moisture swelling requires pressure-drop tests at multiple moisture contents. Samantha's 2026-11-05 reply partially answered the packet size, count, nominal width, bead mass, and one mesh specification; the forwarded request received the additional response below.

The forwarded request reached Samantha Kneale Taylor on 2026-11-06. She answered that the pockets are rod-like and bulge in both directions; the filled thickness varies with sorbent loading; and adjacent pockets are separated by a solid `2 mm` (`~0.079 in`) thermo-sealed line. She planned thickness measurements for the existing `0.3 g` fill and a fully packed packet, plus empty-stick and fully packed pressure-drop runs. She explained that a single unstructured pocket settles into an inconsistent blob. She also confirmed that wet beads swell and planned to ask about the wind tunnel's maximum controllable humidity. New pressure-drop tests were delayed until Ramesh returned from AIChE the following week.

On 2026-11-09, Leonardo asked whether the seals are airtight and proposed a paired defined-aperture experiment: block all flow except through a controlled bead region, run the fixture empty and filled, and subtract the baseline to isolate bead resistance. He noted that the existing underfilled packet is visibly uneven and may require a more complex nonuniform model if that configuration is retained.

The following must be confirmed before a physical production case is created:

- outer test-section and holder dimensions;
- pressure-tap locations and the definition of measured velocity;
- packet thickness and thermal-seal dimensions;
- filled pocket thickness for the existing and fully packed configurations;
- whether the nominally solid `2 mm` thermo-sealed lines are airtight;
- stick count and alignment/offset between sheets;
- sheet spacing and contactor depth;
- inlet profile, air density, viscosity, temperature, and humidity;
- dry bead mass, packing density, and repeat-to-repeat uncertainty.

## Missing referenced attachments

These files are named in the complete email thread but were not found in the repository, Downloads, Desktop, or Documents during the 2026-11-06 review:

- `Pressure Drop of Filter.xlsx` - latest blank/filter/packed-bead measurements and the mapping between the CMS25 and 40-micrometre configurations;
- `windTunnelHolder.pdf` - jig dimensions;
- `2026 percent open histograms.pptx` - openness method and histograms;
- `IMG_8879.HEIC` and `IMG_8880.HEIC` - latest test photographs.

Recovering the spreadsheet and holder drawing is the highest-priority evidence task.

## Source inventory

| Source | Role | Retention status |
|---|---|---|
| `PhysicalMeasurments/pressure_drop_email_thread_2026-10-19_to_2026-11-05.pdf` | Complete ten-message experimental email thread through 2026-11-05 | Primary correspondence record |
| `PhysicalMeasurments/geometry_and_calibration_request_2026-11-02.pdf` | Leonardo's illustrated request for stick shape, filled thickness, spacing, uniform-layer calibration, and moisture-dependent tests | Retain as request provenance |
| `PhysicalMeasurments/experimental_geometry_followup_2026-11-06_to_2026-11-09.pdf` | Samantha's geometry/moisture response and Leonardo's defined-aperture calibration proposal | Primary current experiment-planning record |
| `PhysicalMeasurments/MT 125 micron Mesh dP data RK 10:19.docx` | Original MT125 measurement document | Retain |
| `PhysicalMeasurments/MT 125 micron Mesh dP data RK 10:19.pdf` | PDF rendering of the MT125 measurement document | Retain for viewing |
| `PhysicalMeasurments/mt_125_micron_two_layer_raw.csv` | Machine-readable transcription with measurement status | Retain as analysis source |
| `PhysicalMeasurments/Milestone 2.1.pdf` | Historical Excellion pressure-drop milestone | Retain |
| `PhysicalMeasurments/Mesh Openness Analysis - AUDACity report FY2023-Q3.pdf` | Extracted historical openness section | Retain for convenient review |
| `PhysicalMeasurments/Progress Report_ASU_Vermaas_EE0009274_FY2023-Q3 1.0.pdf` | Full historical project report | Retain as provenance |
| `Meeting assets for FLEXDAC team meeting Thursdays are ready.pdf` | AI-generated 2026-10-29 meeting summary | Retain with accuracy caveat |
| `Ultra-low energy DAC for load management.pdf` | Current project scope, deliverables, and milestone | Retain as governing project source |
| `InitialContractIdea.docx` | Draft statement of work | Retain separately; it has incomplete dates and compensation-line inconsistencies and is not a technical source |

## Cleanup record

The 2026-11-06 cleanup removes only files that are byte-for-byte duplicates, temporary operating-system/Word files, or partial email exports superseded by the complete ten-message PDF. Unique measurement, proposal, meeting, and historical report sources remain available.
