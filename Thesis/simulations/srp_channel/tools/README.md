# Porous-Resistance Calibration Tool

`fit_porous_resistance.py` fits Project Eqs. P1-P2 to pressure-drop data after subtracting a measured baseline. It uses only the Python standard library.

## Input contract

The CSV requires these columns:

- `case_id`: unique measurement identifier;
- `velocity_m_s`: superficial velocity through the tested porous region;
- `pressure_drop_pa`: measured total pressure drop;
- `baseline_pressure_drop_pa`: holder and empty-mesh pressure drop measured under the same condition;
- `pressure_drop_uncertainty_pa`: positive uncertainty of the total pressure-drop measurement;
- `baseline_pressure_drop_uncertainty_pa`: positive uncertainty of the matching baseline measurement; and
- `split`: `calibration` or `validation`.

The total and baseline uncertainties are combined in quadrature before weighted fitting.

The porous length, air viscosity, and density are explicit command-line inputs because they must come from the experiment. The tool fits

`delta_p/L = A U + B U^2`

and reports `alpha = mu/A` and `C2 = 2B/rho`, predictions, residuals, and separate calibration/validation error metrics as JSON.

## Synthetic verification

The included data use `L = 0.2 m`, `mu = 0.01 Pa s`, and `rho = 1.25 kg/m^3`, with known `alpha = 0.02 m^2` and `C2 = 1.6 1/m`:

```sh
python3 fit_porous_resistance.py synthetic_pressure_drop.csv \
  --porous-length-m 0.2 \
  --dynamic-viscosity-pa-s 0.01 \
  --density-kg-m3 1.25
```

Run the unit tests from this directory:

```sh
python3 -m unittest -v test_fit_porous_resistance.py
```

Do not use the preliminary Excellion plot as physical SRP calibration input. Its geometry, baseline losses, velocity definition, bead loading, and uncertainty are not sufficiently documented.

## Cross-grid geometry verification

`verify_grid_geometry.py` creates coarse, target, and fine initialization or short-flow cases with Ensight output disabled. It verifies the actual solver-emitted rod-area and physical flow-band audits, paired-band symmetry, fraction sums, CFL, divergence, and mass balance. The output directory must not already exist.

From `Thesis/simulations/srp_channel`:

```sh
python3 tools/verify_grid_geometry.py \
  --executable ./nga.dp.gnu.opt.mpi.exe \
  --output-dir runs/YYYY-MM-DD_grid_consistency_smoke \
  --max-time 0.02
```

With the default `--max-time 0`, the tool performs initialization-only geometry checks. The production rod mask uses `64 x 64` deterministic subcell samples only in circle-boundary cells; full and empty cells are classified directly. The accepted rod-area and cross-grid-spread tolerance is `0.1%`.

## NGA2 multi-velocity verification

`verify_porous_scaling.py` runs the uniform `32 x 4 x 4` slab with Darcy-only, Forchheimer-only, and combined resistance at velocities `0.5`, `1`, and `2`. It compares the final-window mean pressure drop with Project Eq. P1, checks mass conservation, and writes a summary CSV. The output directory must not already exist so preserved evidence cannot be overwritten accidentally.

From `Thesis/simulations/srp_channel`:

```sh
python3 tools/verify_porous_scaling.py \
  --executable ./nga.dp.gnu.opt.mpi.exe \
  --output-dir runs/YYYY-MM-DD_multivelocity_porous_verification
```
