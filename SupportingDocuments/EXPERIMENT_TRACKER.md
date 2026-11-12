# Wind Tunnel Experiment Tracker

Last reviewed: 2026-11-11

## Purpose

This document tracks the wind-tunnel configurations needed to calibrate and validate the SRP airflow model. It separates measurements that exist from tests that are planned, records the metadata required for each run, and prevents data from different meshes, frames, fill levels, or humidity states from being combined accidentally.

## Current experimental conclusion

The physical packet contains eight horizontally stacked pockets that bulge in both directions like rods. Adjacent pockets are separated by nominally solid `2 mm` thermo-sealed lines. Pocket thickness depends on sorbent fill and has not yet been reported. The existing `0.3 g`-per-pocket packet is underfilled and visibly uneven, so it may support a proof-of-concept comparison but is not the preferred clean calibration geometry.

The preferred calibration experiment is a paired empty/filled measurement in which all flow is blocked except through a defined bead-filled aperture. This should isolate bead resistance from the frame and packet shape. A fully packed eight-stick packet and an empty eight-stick packet are also planned for geometry validation. Moisture-dependent testing is relevant because the beads swell when wet, but the wind tunnel's controllable maximum humidity is not yet known.

## Reported packet geometry

| Field | Current value | Evidence status |
|---|---:|---|
| Fill opening | `10 cm x 10 cm` | Reported 2026-11-05 |
| Pocket count | 8 horizontal pockets | Reported 2026-11-05 |
| Nominal pocket width | `1.25 cm` minus seal width | Reported 2026-11-05 |
| Cross-sectional shape | Rod-like, bulging in both directions | Confirmed 2026-11-06 |
| Separator width | `2 mm` or approximately `0.079 in` | Confirmed 2026-11-06 |
| Separator construction | Solid thermo-sealed line | Reported 2026-11-06; airtightness still awaiting confirmation |
| Filled thickness for `0.3 g` | Pending measurement | Samantha planned measurement for 2026-11-09 |
| Fully packed thickness | Pending measurement | Planned with fully packed run |
| Sorbent per pocket in existing run | Approximately `0.3 g` | Reported 2026-11-05 |
| Nominal total sorbent | Approximately `2.4 g` | Derived from 8 pockets x `0.3 g` |
| Sorbent | Unexchanged Purolite A501P, chloride form | Reported 2026-11-05 |
| Moisture behavior | Beads swell when wet | Confirmed 2026-11-06; quantitative swelling unknown |

## Mesh and packet configurations

These configurations must remain separate until the spreadsheet and photographs map every run to its specimen.

| Internal configuration label | Mesh/specimen | Known information | Calibration status |
|---|---|---|---|
| `MT125_TWO_LAYER` | Two MT125 polyester layers | `125 micrometre`, `32.98%` open; 29 pressure-drop points from `0.1-2.9 m/s` | Assembly evidence only; lacks matched blank and metadata |
| `CMS25_STICK_03G` | Eight-stick CMS25 nylon packet | `25 micrometre`, `12.02%` open; approximately `0.3 g` per pocket; visibly underfilled/uneven | Proof-of-concept only until spreadsheet, blank pairing, and thickness arrive |
| `FILTER40_PACKED` | Packed-bead packet using a `40-micrometre` filter | Mentioned by Ramesh; likely distinct from CMS25 | Cannot use until run mapping and data arrive |
| `EMPTY_FRAME` | Frame without packet resistance | Reported completed | Spreadsheet and exact pairing missing |
| `FILTER_ONLY` | One filter/mesh without packed beads | Reported completed | Mesh identity and spreadsheet mapping missing |

The labels above are project tracking labels, not names supplied by the experimental team.

## Requested and planned test matrix

| Priority | Test | Purpose | Status |
|---:|---|---|---|
| 1 | Defined-aperture empty fixture | Measure fixture, cover, and seal baseline | Proposed by Leonardo and Marcus on 2026-11-09 |
| 1 | Same defined aperture filled with beads | Isolate bead resistance by subtracting the paired empty fixture | Proposed; experimental feasibility awaiting response |
| 2 | Empty eight-stick packet | Measure mesh, seals, and stick structure without sorbent | Suggested by Justin; Samantha plans to run |
| 2 | Existing eight-stick packet at `0.3 g` per pocket | Preserve comparison to the completed underfilled case | Existing data referenced but spreadsheet missing |
| 2 | Fully packed eight-stick packet | Establish thickness and pressure drop for a repeatable filled geometry | Samantha plans to prepare and measure |
| 3 | Higher-humidity packet run | Test whether wet-bead swelling changes packet thickness and pressure drop | Beads confirmed to swell; tunnel humidity capability pending |
| 3 | Flow-parallel packet configuration | Validate later operating orientation and bypass channels | Later system-design experiment, not current calibration |

No new wind-tunnel pressure-drop tests were expected until the week after 2026-11-09 because Ramesh was attending AIChE.

## Required record for every run

Every experimental row or series should include:

- unique run identifier and date;
- operator;
- specimen label and photograph;
- mesh material, pore size, and percent openness;
- frame and exposed-flow dimensions;
- separator/seal geometry and whether it is airtight;
- pocket count, filled thickness, and clear spacing;
- dry sorbent mass per pocket and total dry mass;
- sorbent condition, exchange form, moisture content, and packing method;
- airflow orientation;
- wind-tunnel velocity definition and measurement location;
- pressure-tap locations and measured pressure difference;
- air temperature, pressure, humidity, density, and viscosity;
- repeated measurements or sensor uncertainty;
- matching blank/control run identifier;
- notes on leakage, settling, uneven fill, or deformation.

## Calibration readiness gates

A configuration is ready for Darcy-Forchheimer fitting only when:

1. velocity and pressure-drop values are available in machine-readable form;
2. a geometrically identical empty/control series is available;
3. the mesh, frame, aperture, fill, and humidity state are identified;
4. the effective porous length and flow area are defined;
5. calibration and validation velocities can be separated; and
6. uncertainty or repeatability information is available or explicitly marked unavailable.

The November 5 workbook is now local and supplies the packed-filter series,
filter-only series, MT125 series, and blank-stand series.  It still does not
pass the full calibration gates because the filled thickness, uncertainties,
pressure-tap/holder geometry, air properties, photographs, and unambiguous
specimen mapping are missing.  A provisional effective-assembly Darcy fit is
documented in `PhysicalMeasurments/nov5_packed_filter_fit.md`; it must not be
described as an isolated bead permeability.

## CFD mapping

- Use the defined-aperture paired experiment to fit porous coefficients with the simplest supported geometry.
- Use the empty and fully packed stick packets to validate explicit pocket geometry after calibration.
- Treat the underfilled `0.3 g` packet as an uneven-fill sensitivity case if its geometry can be reconstructed.
- Do not represent the thermo-sealed regions as porous until airtightness is confirmed. If airtight, model them as solid blockage.
- Resolve the confirmed filled thickness with at least the advisor-requested minimum cell count before production runs.
- Treat the later flow-parallel assembly with upper and lower bypass passages as a separate model.

## Open actions

- **Samantha:** confirm whether the `2 mm` thermo-sealed lines are airtight.
- **Samantha:** provide filled thickness for the `0.3 g` packet and the fully packed packet.
- **Samantha/Ramesh:** assess the defined-aperture paired calibration fixture.
- **Samantha/Ramesh/Lindsey:** report the maximum controllable wind-tunnel humidity.
- **Experimental team:** provide `windTunnelHolder.pdf`, the openness-method deck, the two photographs, filled thickness, and measurement uncertainty.
- **Leonardo:** map each received series to the configuration labels above before fitting coefficients.

## Source files

- `PhysicalMeasurments/pressure_drop_email_thread_2026-10-19_to_2026-11-05.pdf`
- `PhysicalMeasurments/geometry_and_calibration_request_2026-11-02.pdf`
- `PhysicalMeasurments/experimental_geometry_followup_2026-11-06_to_2026-11-09.pdf`
- `PhysicalMeasurments/MT 125 micron Mesh dP data RK 10:19.docx`
- `PhysicalMeasurments/MT 125 micron Mesh dP data RK 10:19.pdf`
- `PhysicalMeasurments/mt_125_micron_two_layer_raw.csv`
- `PhysicalMeasurments/Pressure Drop of Filter.xlsx`
- `PhysicalMeasurments/pressure_drop_filter_2026-11-05_raw.csv`
- `PhysicalMeasurments/nov5_packed_filter_fit.md`
