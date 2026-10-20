#!/usr/bin/env python3
"""Run and check the short pre-calibration Docker review suite."""

from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from pathlib import Path


CASES = (
    ("smoke", None),
    ("darcy", 1.0),
    ("forchheimer", 1.0),
    ("combined", 2.0),
)
CASE_ROOT = Path("/opt/nga2/review/cases")


def numeric_rows(path: Path) -> list[list[float]]:
    rows: list[list[float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = [float(value) for value in line.split()]
        except ValueError:
            continue
        if not all(math.isfinite(value) for value in row):
            raise RuntimeError(f"Non-finite monitor value found in {path}: {line}")
        rows.append(row)
    if not rows:
        raise RuntimeError(f"No numeric rows found in {path}")
    return rows


def check_case(case_dir: Path, expected_drop: float | None) -> dict[str, object]:
    log_text = (case_dir / "monitor/log").read_text(encoding="utf-8")
    if "NGA APPLICATION COMPLETE" not in log_text:
        raise RuntimeError(f"{case_dir.name}: normal completion marker is missing")
    simulation = numeric_rows(case_dir / "monitor/simulation")
    flow = numeric_rows(case_dir / "monitor/flow_balance")
    max_cfl = max(row[3] for row in simulation)
    max_divergence = max(abs(row[8]) for row in simulation)
    max_mass_error = max(abs(row[4]) for row in flow)
    if max_cfl >= 0.8:
        raise RuntimeError(f"{case_dir.name}: CFL {max_cfl:.6g} is not below 0.8")
    if max_divergence > 1.0e-10:
        raise RuntimeError(f"{case_dir.name}: divergence {max_divergence:.6g} exceeds 1e-10")
    if max_mass_error > 1.0e-10:
        raise RuntimeError(f"{case_dir.name}: mass error {max_mass_error:.6g} exceeds 1e-10")

    result: dict[str, object] = {
        "case": case_dir.name,
        "final_time": simulation[-1][1],
        "max_cfl": max_cfl,
        "max_divergence": max_divergence,
        "max_relative_mass_error": max_mass_error,
        "expected_pressure_drop": expected_drop,
        "mean_pressure_drop": None,
        "relative_pressure_error": None,
    }
    if expected_drop is not None:
        final_time = flow[-1][1]
        final_window = [row[10] for row in flow if row[1] >= 0.75 * final_time]
        mean_drop = sum(final_window) / len(final_window)
        relative_error = abs(mean_drop - expected_drop) / expected_drop
        if relative_error > 1.0e-8:
            raise RuntimeError(
                f"{case_dir.name}: pressure error {relative_error:.6g} exceeds 1e-8"
            )
        result["mean_pressure_drop"] = mean_drop
        result["relative_pressure_error"] = relative_error
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="new verification directory")
    parser.add_argument("--ranks", type=int, default=4)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if output.exists():
        raise SystemExit(f"Output directory already exists: {output}")
    output.mkdir(parents=True)

    summaries = []
    for name, expected_drop in CASES:
        case_output = output / name
        command = [
            "nga2Adsorption",
            "--config",
            str(CASE_ROOT / f"{name}.input"),
            "--output",
            str(case_output),
            "--ranks",
            str(args.ranks),
        ]
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            raise RuntimeError(f"{name}: launcher exited with {completed.returncode}")
        summaries.append(check_case(case_output, expected_drop))

    with (output / "summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=summaries[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)
    (output / "summary.json").write_text(
        json.dumps(summaries, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"PASS: {len(summaries)} pre-calibration review cases; evidence: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
