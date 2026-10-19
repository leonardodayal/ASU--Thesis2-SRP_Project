#!/usr/bin/env python3
"""Run uniform-slab cases that verify Darcy-Forchheimer velocity scaling."""

import argparse
import csv
import subprocess
from pathlib import Path


PHYSICS = {
    "darcy": {"permeability": 0.01, "forchheimer": 0.0},
    "forchheimer": {"permeability": 1.0e30, "forchheimer": 2.0},
    "combined": {"permeability": 0.01, "forchheimer": 2.0},
}
VELOCITIES = (0.5, 1.0, 2.0)
DENSITY = 1.0
VISCOSITY = 0.01
POROUS_LENGTH = 1.0


def input_text(velocity, permeability, forchheimer):
    return f"""Partition : 4 1 1
nx : 32
ny : 4
nz : 4
Wall padding cells : 0
Lx : 4
Ly : 1
Lz : 1
Density : {DENSITY}
Dynamic viscosity : {VISCOSITY}
Inlet velocity : {velocity}
Porous permeability : {permeability}
Forchheimer coefficient : {forchheimer}
Porous slab start : 1.5
Porous slab end : 2.5
Pressure sample upstream : 1.4375
Pressure sample downstream : 2.5625
Max timestep size : 5e-3
Max cfl number : 0.8
Max time : 4
Ensight output period : 10
"""


def numeric_rows(path):
    rows = []
    with path.open(encoding="utf-8") as stream:
        for line in stream:
            fields = line.split()
            if not fields:
                continue
            try:
                rows.append([float(value) for value in fields])
            except ValueError:
                continue
    if not rows:
        raise RuntimeError(f"no numeric monitor rows in {path}")
    return rows


def summarize_case(case_dir, expected_pressure_drop):
    flow_rows = numeric_rows(case_dir / "monitor" / "flow_balance")
    simulation_rows = numeric_rows(case_dir / "monitor" / "simulation")
    final_time = flow_rows[-1][1]
    steady_rows = [row for row in flow_rows if row[1] >= 0.75 * final_time]
    pressure_drops = [row[10] for row in steady_rows]
    mean_pressure_drop = sum(pressure_drops) / len(pressure_drops)
    relative_error = abs(mean_pressure_drop - expected_pressure_drop) / expected_pressure_drop
    return {
        "expected_pressure_drop": expected_pressure_drop,
        "mean_pressure_drop": mean_pressure_drop,
        "relative_error": relative_error,
        "range_over_mean": (
            max(pressure_drops) - min(pressure_drops)
        ) / mean_pressure_drop,
        "max_mass_flow_error": max(row[4] for row in flow_rows),
        "max_cfl": max(row[3] for row in simulation_rows),
        "max_divergence": max(row[8] for row in simulation_rows),
    }


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--pressure-tolerance", type=float, default=1.0e-8)
    parser.add_argument("--mass-flow-tolerance", type=float, default=1.0e-10)
    return parser.parse_args()


def main():
    args = parse_args()
    executable = args.executable.resolve()
    if not executable.is_file():
        raise SystemExit(f"executable not found: {executable}")
    args.output_dir.mkdir(parents=True, exist_ok=False)

    summaries = []
    for name, coefficients in PHYSICS.items():
        for velocity in VELOCITIES:
            case_name = f"{name}_u{velocity:g}".replace(".", "p")
            case_dir = args.output_dir / case_name
            case_dir.mkdir()
            (case_dir / "input").write_text(
                input_text(velocity, coefficients["permeability"], coefficients["forchheimer"]),
                encoding="utf-8",
            )
            command = ["mpiexec", "-n", "4", str(executable), "-i", "input"]
            completed = subprocess.run(
                command,
                cwd=case_dir,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            (case_dir / "launcher.log").write_text(completed.stdout, encoding="utf-8")
            if completed.returncode != 0:
                raise RuntimeError(f"{case_name} failed; see {case_dir / 'launcher.log'}")

            expected = POROUS_LENGTH * (
                VISCOSITY / coefficients["permeability"] * velocity
                + 0.5 * DENSITY * coefficients["forchheimer"] * velocity**2
            )
            summary = summarize_case(case_dir, expected)
            summary.update({"case": case_name, "physics": name, "velocity": velocity})
            summaries.append(summary)

    fieldnames = (
        "case",
        "physics",
        "velocity",
        "expected_pressure_drop",
        "mean_pressure_drop",
        "relative_error",
        "range_over_mean",
        "max_mass_flow_error",
        "max_cfl",
        "max_divergence",
    )
    with (args.output_dir / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)

    failures = [
        row
        for row in summaries
        if row["relative_error"] > args.pressure_tolerance
        or row["max_mass_flow_error"] > args.mass_flow_tolerance
    ]
    if failures:
        names = ", ".join(row["case"] for row in failures)
        raise SystemExit(f"verification tolerance failed: {names}")
    print(f"verified {len(summaries)} cases; summary: {args.output_dir / 'summary.csv'}")


if __name__ == "__main__":
    main()
