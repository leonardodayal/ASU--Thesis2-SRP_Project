#!/usr/bin/env python3
"""Check fractional ellipse area as cut-cell sampling is refined."""

from __future__ import annotations

import argparse
import csv
import math
import subprocess
from pathlib import Path


SAMPLES_PER_DIRECTION = (4, 8, 16, 32, 64, 128)
MAX_AREA_ERROR_PERCENT = 0.1
MAX_REFINEMENT_CHANGE_PERCENT = 0.05


def input_text(samples: int, diameter: float, thickness: float) -> str:
    return f"""# Initialization-only fractional ellipse verification.
Partition : 4 1 1
nx : 192
ny : 48
nz : 48
Wall padding cells : 2
Lx : 4
Ly : 1
Lz : 1
Density : 1
Dynamic viscosity : 0.01
Inlet velocity : 1
Porous permeability : 0.01
Forchheimer coefficient : 0
Porous geometry : aligned_rods_z
Porous slab start : 2
Porous slab end : 2
Rod count : 1
Rod diameter : {diameter:.16g}
Rod thickness : {thickness:.16g}
Rod fraction samples per direction : {samples}
Rod center span : 0
Rod sheet x : 2
Sheet pressure offset : 0.2
Pressure sample upstream : 1
Pressure sample downstream : 3
Flow split plane : 3
Flow split bands : 1
Max timestep size : 2e-3
Max cfl number : 0.8
Max time : 0
Write Ensight output : F
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--diameter", type=float, default=0.105)
    parser.add_argument("--thickness", type=float, default=0.06)
    args = parser.parse_args()

    executable = args.executable.resolve()
    output_dir = args.output_dir.resolve()
    if not executable.is_file():
        raise SystemExit(f"Executable not found: {executable}")
    if output_dir.exists():
        raise SystemExit(f"Output directory already exists: {output_dir}")
    if args.diameter <= 0 or args.thickness <= 0:
        raise SystemExit("Diameter and thickness must be positive")
    output_dir.mkdir(parents=True)

    analytic_area = math.pi * 0.5 * args.diameter * 0.5 * args.thickness
    rows: list[dict[str, float | int]] = []
    for samples in SAMPLES_PER_DIRECTION:
        total_samples = samples**2
        case_dir = output_dir / f"samples_{total_samples}"
        case_dir.mkdir()
        (case_dir / "input").write_text(
            input_text(samples, args.diameter, args.thickness)
        )
        completed = subprocess.run(
            ["mpiexec", "-n", "4", str(executable), "-i", "input"],
            cwd=case_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        (case_dir / "stdout.log").write_text(completed.stdout)
        if completed.returncode != 0:
            raise RuntimeError(
                f"{total_samples} samples: NGA2 exited with {completed.returncode}; "
                f"see {case_dir / 'stdout.log'}"
            )
        with (case_dir / "monitor/geometry_audit.csv").open(newline="") as stream:
            audit_rows = list(csv.DictReader(stream))
        if len(audit_rows) != 1:
            raise RuntimeError(f"{total_samples} samples: expected one audit row")
        represented_area = float(audit_rows[0]["represented_area"])
        rows.append(
            {
                "samples_per_direction": samples,
                "total_samples_per_cut_cell": total_samples,
                "analytic_area": analytic_area,
                "represented_area": represented_area,
                "absolute_error_percent": abs(
                    100.0 * (represented_area / analytic_area - 1.0)
                ),
            }
        )

    for index, row in enumerate(rows):
        if index == 0:
            row["change_from_previous_percent"] = math.nan
        else:
            previous = float(rows[index - 1]["represented_area"])
            current = float(row["represented_area"])
            row["change_from_previous_percent"] = abs(
                100.0 * (current - previous) / analytic_area
            )

    with (output_dir / "summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    for row in rows:
        print(
            f"{row['total_samples_per_cut_cell']:4d} samples: "
            f"area error={row['absolute_error_percent']:.8g}% "
            f"change={row['change_from_previous_percent']:.8g}%"
        )
    accepted = [
        row
        for row in rows[1:]
        if float(row["absolute_error_percent"]) < MAX_AREA_ERROR_PERCENT
        and float(row["change_from_previous_percent"])
        < MAX_REFINEMENT_CHANGE_PERCENT
    ]
    if not accepted:
        raise RuntimeError(
            "No sampling level met the area-error and refinement-change criteria"
        )
    selected = accepted[0]
    print(
        "PASS: selected "
        f"{selected['total_samples_per_cut_cell']} total samples per cut cell "
        f"({selected['samples_per_direction']} per direction)"
    )
    print(f"Evidence written to {output_dir}")


if __name__ == "__main__":
    main()
