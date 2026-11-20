#!/usr/bin/env python3
"""Calculate three-grid GCI from matched ellipse active/control monitors."""

from pathlib import Path
import argparse
import math


def numeric_rows(path):
    rows = []
    for line in path.read_text().splitlines():
        try:
            rows.append([float(field) for field in line.split()])
        except ValueError:
            continue
    return rows


def mean_sheet_drop(case_dir, window_start, final_time):
    if not math.isfinite(window_start) or not math.isfinite(final_time):
        raise ValueError("Averaging-window bounds must be finite")
    if final_time <= window_start:
        raise ValueError("Averaging-window final time must be greater than window start")
    rows = numeric_rows(case_dir / "monitor" / "sheet_pressure")
    window = [
        row[4]
        for row in rows
        if len(row) >= 5 and window_start <= row[1] <= final_time
    ]
    if len(window) < 2:
        raise ValueError(f"Too few averaging-window samples in {case_dir}")
    return sum(window) / len(window)


def net_drop(active, control, window_start, final_time):
    if not math.isfinite(window_start) or not math.isfinite(final_time):
        raise ValueError("Averaging-window bounds must be finite")
    if final_time <= window_start:
        raise ValueError("Averaging-window final time must be greater than window start")

    def pressure_by_step(case_dir):
        rows = numeric_rows(case_dir / "monitor" / "sheet_pressure")
        pressure = {}
        for row in rows:
            if len(row) < 5 or not window_start <= row[1] <= final_time:
                continue
            step = int(row[0])
            if step in pressure:
                raise ValueError(
                    f"Duplicate timestep {step} in {case_dir / 'monitor' / 'sheet_pressure'}"
                )
            pressure[step] = (row[1], row[4])
        return pressure

    active_pressure = pressure_by_step(active)
    control_pressure = pressure_by_step(control)
    common_steps = sorted(active_pressure.keys() & control_pressure.keys())
    if len(common_steps) < 2:
        raise ValueError(
            f"Too few aligned averaging-window samples in {active} and {control}"
        )
    net = []
    for step in common_steps:
        active_time, active_value = active_pressure[step]
        control_time, control_value = control_pressure[step]
        if not math.isclose(active_time, control_time, rel_tol=0.0, abs_tol=1.0e-10):
            raise ValueError(
                f"Timestep {step} has mismatched physical times "
                f"{active_time:g} and {control_time:g}"
            )
        net.append(active_value - control_value)
    return sum(net) / len(net)


def calculate_gci(coarse, medium, fine, refinement_ratio=2.0, safety_factor=1.25):
    if not all(math.isfinite(value) for value in (coarse, medium, fine)):
        raise ValueError("Grid values must be finite")
    if any(value == 0.0 for value in (coarse, medium, fine)):
        raise ValueError("Grid values must be nonzero")
    if not math.isfinite(refinement_ratio) or refinement_ratio <= 1.0:
        raise ValueError("Refinement ratio must be finite and greater than 1")
    if not math.isfinite(safety_factor) or safety_factor <= 0.0:
        raise ValueError("GCI safety factor must be finite and positive")
    medium_fine = medium - fine
    coarse_medium = coarse - medium
    if medium_fine == 0.0 or coarse_medium == 0.0:
        raise ValueError("GCI is undefined for identical consecutive grid values")
    if medium_fine * coarse_medium <= 0.0:
        raise ValueError("Grid sequence is oscillatory; monotonic three-grid GCI is invalid")
    order = math.log(abs(coarse_medium / medium_fine)) / math.log(refinement_ratio)
    if not math.isfinite(order) or order <= 0.0:
        raise ValueError(f"Non-positive observed order p={order:g}")
    denominator = refinement_ratio**order - 1.0
    if not math.isfinite(denominator) or math.isclose(
        denominator, 0.0, abs_tol=1.0e-12
    ):
        raise ValueError("GCI denominator is too close to zero")
    extrapolated = fine + (fine - medium) / denominator
    fine_gci = (
        safety_factor * abs((fine - medium) / fine) / denominator * 100.0
    )
    medium_gci = (
        safety_factor * abs((medium - coarse) / medium) / denominator * 100.0
    )
    asymptotic_ratio = medium_gci / (refinement_ratio**order * fine_gci)
    return order, extrapolated, fine_gci, medium_gci, asymptotic_ratio


def main():
    parser = argparse.ArgumentParser()
    for grid in ("g1", "g2", "g3"):
        parser.add_argument(f"--{grid}-active", type=Path, required=True)
        parser.add_argument(f"--{grid}-control", type=Path, required=True)
    parser.add_argument("--window-start", type=float, default=3.0)
    parser.add_argument("--final-time", type=float, default=4.0)
    parser.add_argument("--refinement-ratio", type=float, default=2.0)
    args = parser.parse_args()

    values = []
    for grid in ("g1", "g2", "g3"):
        value = net_drop(
            getattr(args, f"{grid}_active"),
            getattr(args, f"{grid}_control"),
            args.window_start,
            args.final_time,
        )
        values.append(value)
        print(f"{grid} net mean sheet drop={value:.12g}")

    order, extrapolated, fine_gci, medium_gci, ratio = calculate_gci(
        *values, refinement_ratio=args.refinement_ratio
    )
    print(f"observed order p={order:.12g}")
    print(f"Richardson extrapolated drop={extrapolated:.12g}")
    print(f"fine-grid GCI={fine_gci:.12g}%")
    print(f"medium-grid GCI={medium_gci:.12g}%")
    print(f"asymptotic ratio={ratio:.12g}")


if __name__ == "__main__":
    main()
