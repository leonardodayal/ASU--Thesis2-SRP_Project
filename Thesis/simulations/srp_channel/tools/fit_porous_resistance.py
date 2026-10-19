#!/usr/bin/env python3
"""Fit Darcy-Forchheimer resistance from pressure-drop measurements."""

import argparse
import csv
import json
import math
from pathlib import Path


REQUIRED_COLUMNS = {
    "case_id",
    "velocity_m_s",
    "pressure_drop_pa",
    "baseline_pressure_drop_pa",
    "pressure_drop_uncertainty_pa",
    "baseline_pressure_drop_uncertainty_pa",
    "split",
}


def load_measurements(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"missing CSV columns: {', '.join(sorted(missing))}")

        rows = []
        for line_number, raw in enumerate(reader, start=2):
            try:
                row = {
                    "case_id": raw["case_id"].strip(),
                    "velocity_m_s": float(raw["velocity_m_s"]),
                    "pressure_drop_pa": float(raw["pressure_drop_pa"]),
                    "baseline_pressure_drop_pa": float(raw["baseline_pressure_drop_pa"]),
                    "pressure_drop_uncertainty_pa": float(
                        raw["pressure_drop_uncertainty_pa"]
                    ),
                    "baseline_pressure_drop_uncertainty_pa": float(
                        raw["baseline_pressure_drop_uncertainty_pa"]
                    ),
                    "split": raw["split"].strip().lower(),
                }
            except ValueError as exc:
                raise ValueError(f"invalid numeric value on CSV line {line_number}") from exc

            if not row["case_id"]:
                raise ValueError(f"empty case_id on CSV line {line_number}")
            if row["velocity_m_s"] <= 0.0:
                raise ValueError(f"velocity must be positive on CSV line {line_number}")
            if row["pressure_drop_uncertainty_pa"] <= 0.0:
                raise ValueError(
                    f"pressure-drop uncertainty must be positive on CSV line {line_number}"
                )
            if row["baseline_pressure_drop_uncertainty_pa"] <= 0.0:
                raise ValueError(
                    f"baseline uncertainty must be positive on CSV line {line_number}"
                )
            if row["split"] not in {"calibration", "validation"}:
                raise ValueError(
                    f"split must be calibration or validation on CSV line {line_number}"
                )
            row["net_pressure_drop_pa"] = (
                row["pressure_drop_pa"] - row["baseline_pressure_drop_pa"]
            )
            row["net_pressure_uncertainty_pa"] = math.hypot(
                row["pressure_drop_uncertainty_pa"],
                row["baseline_pressure_drop_uncertainty_pa"],
            )
            rows.append(row)

    if not rows:
        raise ValueError("CSV contains no measurements")
    return rows


def fit_resistance(rows, porous_length_m, dynamic_viscosity_pa_s, density_kg_m3):
    if porous_length_m <= 0.0:
        raise ValueError("porous length must be positive")
    if dynamic_viscosity_pa_s <= 0.0:
        raise ValueError("dynamic viscosity must be positive")
    if density_kg_m3 <= 0.0:
        raise ValueError("density must be positive")

    calibration = [row for row in rows if row["split"] == "calibration"]
    if len(calibration) < 2:
        raise ValueError("at least two calibration measurements are required")

    s11 = s12 = s22 = t1 = t2 = 0.0
    for row in calibration:
        velocity = row["velocity_m_s"]
        gradient = row["net_pressure_drop_pa"] / porous_length_m
        gradient_uncertainty = row["net_pressure_uncertainty_pa"] / porous_length_m
        weight = 1.0 / gradient_uncertainty**2
        linear = velocity
        quadratic = velocity**2
        s11 += weight * linear**2
        s12 += weight * linear * quadratic
        s22 += weight * quadratic**2
        t1 += weight * linear * gradient
        t2 += weight * quadratic * gradient

    determinant = s11 * s22 - s12**2
    if abs(determinant) <= 1.0e-14 * max(abs(s11 * s22), 1.0):
        raise ValueError("calibration velocities do not provide an independent fit")

    linear_coefficient = (t1 * s22 - t2 * s12) / determinant
    quadratic_coefficient = (s11 * t2 - s12 * t1) / determinant
    if linear_coefficient <= 0.0 or quadratic_coefficient < 0.0:
        raise ValueError("fit produced nonphysical Darcy-Forchheimer coefficients")

    permeability_m2 = dynamic_viscosity_pa_s / linear_coefficient
    inertial_coefficient_m_inv = 2.0 * quadratic_coefficient / density_kg_m3

    predictions = []
    for row in rows:
        velocity = row["velocity_m_s"]
        predicted_net = porous_length_m * (
            linear_coefficient * velocity + quadratic_coefficient * velocity**2
        )
        predictions.append(
            {
                "case_id": row["case_id"],
                "split": row["split"],
                "velocity_m_s": velocity,
                "measured_net_pressure_drop_pa": row["net_pressure_drop_pa"],
                "predicted_net_pressure_drop_pa": predicted_net,
                "residual_pa": row["net_pressure_drop_pa"] - predicted_net,
            }
        )

    def metrics(split):
        selected = [row for row in predictions if row["split"] == split]
        if not selected:
            return {"count": 0, "rmse_pa": None, "max_abs_error_pa": None}
        residuals = [row["residual_pa"] for row in selected]
        return {
            "count": len(selected),
            "rmse_pa": math.sqrt(sum(value**2 for value in residuals) / len(residuals)),
            "max_abs_error_pa": max(abs(value) for value in residuals),
        }

    return {
        "model": "delta_p/L = A*U + B*U^2",
        "porous_length_m": porous_length_m,
        "dynamic_viscosity_pa_s": dynamic_viscosity_pa_s,
        "density_kg_m3": density_kg_m3,
        "linear_coefficient_A_pa_s_m2": linear_coefficient,
        "quadratic_coefficient_B_pa_s2_m3": quadratic_coefficient,
        "permeability_alpha_m2": permeability_m2,
        "forchheimer_coefficient_C2_m_inv": inertial_coefficient_m_inv,
        "metrics": {
            "calibration": metrics("calibration"),
            "validation": metrics("validation"),
        },
        "predictions": predictions,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fit Project Eqs. P1-P2 to baseline-corrected pressure-drop data."
    )
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--porous-length-m", type=float, required=True)
    parser.add_argument("--dynamic-viscosity-pa-s", type=float, required=True)
    parser.add_argument("--density-kg-m3", type=float, required=True)
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    return parser.parse_args()


def main():
    args = parse_args()
    result = fit_resistance(
        load_measurements(args.csv_path),
        args.porous_length_m,
        args.dynamic_viscosity_pa_s,
        args.density_kg_m3,
    )
    result["input_csv"] = str(args.csv_path)
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
