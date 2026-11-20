#!/usr/bin/env python3
"""Plot active, control, and net sheet-pressure convergence histories."""

from pathlib import Path
import argparse

import matplotlib.pyplot as plt


def numeric_rows(path):
    rows = []
    for line in path.read_text().splitlines():
        try:
            rows.append([float(field) for field in line.split()])
        except ValueError:
            continue
    return rows


def pressure_by_time(case_dir):
    rows = numeric_rows(case_dir / "monitor" / "sheet_pressure")
    return {row[1]: row[4] for row in rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("active", type=Path)
    parser.add_argument("control", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--window-start", type=float, default=3.0)
    args = parser.parse_args()

    active = pressure_by_time(args.active)
    control = pressure_by_time(args.control)
    times = sorted(set(active) & set(control))
    active_values = [active[time] for time in times]
    control_values = [control[time] for time in times]
    net_values = [active[time] - control[time] for time in times]

    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)
    for axis, start, title in (
        (axes[0], 0.0, "Full time history"),
        (axes[1], args.window_start, "Verified averaging window"),
    ):
        selected = [index for index, time in enumerate(times) if time >= start]
        axis.plot([times[i] for i in selected], [active_values[i] for i in selected], label="Active")
        axis.plot([times[i] for i in selected], [control_values[i] for i in selected], label="Control")
        axis.plot([times[i] for i in selected], [net_values[i] for i in selected], label="Active - control")
        axis.set_title(title)
        axis.set_xlabel("Nondimensional time")
        axis.set_ylabel("Sheet pressure drop")
        axis.grid(alpha=0.25)
    axes[0].legend()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=180)


if __name__ == "__main__":
    main()
