#!/usr/bin/env python3
"""Verify that rod masks and flow bands represent the same physical geometry."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path


GRIDS = (
    ("coarse", 128, 32, 1),
    ("target", 256, 64, 2),
    ("fine", 384, 96, 3),
)


def input_text(nx: int, ny: int, padding: int, max_time: float) -> str:
    return f"""# Initialization-only grid-consistency verification.
Partition : 4 1 1
nx : {nx}
ny : {ny}
nz : {ny}
Wall padding cells : {padding}
Lx : 4
Ly : 1
Lz : 1
Density : 1
Dynamic viscosity : 0.01
Inlet velocity : 1
Porous permeability : 0.01
Forchheimer coefficient : 0
Porous geometry : stacked_aligned_rods_z
Porous slab start : 2
Porous slab end : 2
Rod count : 4
Rod diameter : 0.1
Rod center span : 0.6
Sheet count : 3
Sheet spacing : 0.5
Stack center x : 2
Sheet pressure offset : 0.25
Pressure sample upstream : 1
Pressure sample downstream : 3
Flow split plane : 3
Flow split bands : 4
Max timestep size : 2e-3
Max cfl number : 0.8
Max time : {max_time:.16g}
Write Ensight output : F
"""


def read_monitor_rows(path: Path) -> list[list[float]]:
    lines = path.read_text().splitlines()
    return [[float(value) for value in line.split()] for line in lines[2:]]


def read_final_flow(path: Path) -> tuple[list[float], float, float]:
    values = read_monitor_rows(path)[-1]
    fractions = [values[3], values[5], values[7], values[9]]
    return fractions, values[10], values[11]


def verify_case(case_dir: Path) -> dict[str, float]:
    with (case_dir / "monitor/geometry_audit.csv").open(newline="") as stream:
        rods = list(csv.DictReader(stream))
    if len(rods) != 12:
        raise RuntimeError(f"{case_dir.name}: expected 12 rod audit rows, found {len(rods)}")

    areas = [float(row["represented_area"]) for row in rods]
    errors = [abs(float(row["error_percent"])) for row in rods]
    if max(errors) > 0.1:
        raise RuntimeError(f"{case_dir.name}: rod-area error {max(errors):.6g}% exceeds 0.1%")
    if max(areas) - min(areas) > 1.0e-12:
        raise RuntimeError(f"{case_dir.name}: rods do not have identical represented areas")

    with (case_dir / "monitor/flow_band_geometry.csv").open(newline="") as stream:
        bands = list(csv.DictReader(stream))
    if len(bands) != 4:
        raise RuntimeError(f"{case_dir.name}: expected four band audit rows")
    widths = [float(row["width"]) for row in bands]
    if max(abs(width - 0.25) for width in widths) > 1.0e-12:
        raise RuntimeError(f"{case_dir.name}: physical band widths are not all 0.25")

    fractions, mass_sum, fraction_sum = read_final_flow(case_dir / "monitor/flow_split")
    if abs(fraction_sum - 1.0) > 1.0e-12:
        raise RuntimeError(f"{case_dir.name}: band fractions do not sum to one")
    if abs(fractions[0] - fractions[3]) > 1.0e-12 or abs(fractions[1] - fractions[2]) > 1.0e-12:
        raise RuntimeError(f"{case_dir.name}: symmetric flow does not preserve paired bands")

    simulation = read_monitor_rows(case_dir / "monitor/simulation")
    flow_balance = read_monitor_rows(case_dir / "monitor/flow_balance")
    max_cfl = max(row[3] for row in simulation)
    max_divergence = max(abs(row[8]) for row in simulation)
    max_mass_error = max(abs(row[4]) for row in flow_balance)

    return {
        "represented_rod_area": areas[0],
        "max_rod_area_error_percent": max(errors),
        "final_band_1_fraction": fractions[0],
        "final_band_2_fraction": fractions[1],
        "final_mass_flow_sum": mass_sum,
        "final_time": simulation[-1][1],
        "max_cfl": max_cfl,
        "max_divergence": max_divergence,
        "max_relative_mass_error": max_mass_error,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ranks", type=int, default=4)
    parser.add_argument("--max-time", type=float, default=0.0)
    args = parser.parse_args()

    executable = args.executable.resolve()
    output_dir = args.output_dir.resolve()
    if not executable.is_file():
        raise SystemExit(f"Executable not found: {executable}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)

    summaries: dict[str, dict[str, float]] = {}
    for name, nx, ny, padding in GRIDS:
        case_dir = output_dir / name
        case_dir.mkdir()
        (case_dir / "input").write_text(input_text(nx, ny, padding, args.max_time))
        completed = subprocess.run(
            ["mpiexec", "-n", str(args.ranks), str(executable), "-i", "input"],
            cwd=case_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        (case_dir / "stdout.log").write_text(completed.stdout)
        if completed.returncode != 0:
            raise RuntimeError(
                f"{name}: NGA2 exited with {completed.returncode}; see {case_dir / 'stdout.log'}"
            )
        summaries[name] = verify_case(case_dir)

    represented = [summary["represented_rod_area"] for summary in summaries.values()]
    nominal = 3.141592653589793 * 0.05**2
    spread_percent = 100.0 * (max(represented) - min(represented)) / nominal
    if spread_percent > 0.1:
        raise RuntimeError(f"Cross-grid rod-area spread {spread_percent:.6g}% exceeds 0.1%")

    with (output_dir / "summary.csv").open("w", newline="") as stream:
        fieldnames = ["grid", *next(iter(summaries.values())).keys()]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for name, summary in summaries.items():
            writer.writerow({"grid": name, **summary})
    print(f"PASS: cross-grid rod-area spread = {spread_percent:.6g}%")
    print(f"Evidence written to {output_dir}")


if __name__ == "__main__":
    main()
