#!/usr/bin/env python3
"""Check the predeclared convergence rule for a matched horizon pair."""

from pathlib import Path
import argparse
import math


def numeric_rows(path):
    rows = []
    for line in path.read_text().splitlines():
        fields = line.split()
        if not fields:
            continue
        try:
            rows.append([float(field) for field in fields])
        except ValueError:
            continue
    return rows


def relative_range(values):
    mean = sum(values) / len(values)
    if mean == 0.0:
        return mean, math.inf
    return mean, (max(values) - min(values)) / abs(mean)


def load_case(case_dir, final_time, window_start):
    monitor = case_dir / "monitor"
    pressure = numeric_rows(monitor / "sheet_pressure")
    flow = numeric_rows(monitor / "flow_balance")
    simulation = numeric_rows(monitor / "simulation")
    if not pressure or not flow or not simulation:
        raise ValueError(f"Incomplete monitor data in {case_dir}")
    if abs(simulation[-1][1] - final_time) > 1.0e-10:
        raise ValueError(
            f"{case_dir} ended at t={simulation[-1][1]:g}, expected {final_time:g}"
        )
    window = [row for row in pressure if row[1] >= window_start]
    if len(window) < 2:
        raise ValueError(f"Too few final-window samples in {case_dir}")
    return {
        "pressure": {row[0]: row[4] for row in window},
        "max_mass_error": max(abs(row[4]) for row in flow),
        "max_cfl": max(row[3] for row in simulation),
        "max_divergence": max(abs(row[8]) for row in simulation),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("active", type=Path)
    parser.add_argument("control", type=Path)
    parser.add_argument("--final-time", type=float, default=4.0)
    parser.add_argument("--window-fraction", type=float, default=0.25)
    parser.add_argument("--pressure-tolerance", type=float, default=0.01)
    parser.add_argument("--mass-tolerance", type=float, default=1.0e-10)
    parser.add_argument("--cfl-limit", type=float, default=0.8)
    args = parser.parse_args()

    window_start = args.final_time * (1.0 - args.window_fraction)
    active = load_case(args.active, args.final_time, window_start)
    control = load_case(args.control, args.final_time, window_start)
    common_steps = sorted(set(active["pressure"]) & set(control["pressure"]))
    if len(common_steps) < 2:
        raise ValueError("Active and control have too few aligned final-window samples")

    series = {
        "active": [active["pressure"][step] for step in common_steps],
        "control": [control["pressure"][step] for step in common_steps],
        "net": [
            active["pressure"][step] - control["pressure"][step]
            for step in common_steps
        ],
    }
    passed = True
    print(f"final window: t={window_start:g} to {args.final_time:g}")
    print(f"aligned samples: {len(common_steps)}")
    for name, values in series.items():
        mean, variation = relative_range(values)
        check = math.isfinite(variation) and variation <= args.pressure_tolerance
        passed &= check
        print(
            f"{name} pressure mean={mean:.12g} "
            f"range/mean={100.0 * variation:.6g}% "
            f"{'PASS' if check else 'FAIL'}"
        )

    for name, case in (("active", active), ("control", control)):
        diagnostics_ok = (
            math.isfinite(case["max_mass_error"])
            and math.isfinite(case["max_cfl"])
            and math.isfinite(case["max_divergence"])
            and case["max_mass_error"] <= args.mass_tolerance
            and case["max_cfl"] <= args.cfl_limit
        )
        passed &= diagnostics_ok
        print(
            f"{name} max mass error={case['max_mass_error']:.6g} "
            f"max CFL={case['max_cfl']:.6g} "
            f"max divergence={case['max_divergence']:.6g} "
            f"{'PASS' if diagnostics_ok else 'FAIL'}"
        )

    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
