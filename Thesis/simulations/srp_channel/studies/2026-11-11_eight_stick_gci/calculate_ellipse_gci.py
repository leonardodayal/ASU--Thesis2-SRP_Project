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
    rows = numeric_rows(case_dir / "monitor" / "sheet_pressure")
    window = [row[4] for row in rows if window_start <= row[1] <= final_time]
    if len(window) < 2:
        raise ValueError(f"Too few averaging-window samples in {case_dir}")
    return sum(window) / len(window)


def net_drop(active, control, window_start, final_time):
    return mean_sheet_drop(active, window_start, final_time) - mean_sheet_drop(
        control, window_start, final_time
    )


def calculate_gci(coarse, medium, fine, refinement_ratio=2.0, safety_factor=1.25):
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
