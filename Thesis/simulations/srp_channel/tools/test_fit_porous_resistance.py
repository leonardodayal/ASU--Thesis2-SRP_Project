import csv
import tempfile
import unittest
from pathlib import Path

from fit_porous_resistance import fit_resistance, load_measurements


class FitPorousResistanceTest(unittest.TestCase):
    def setUp(self):
        self.rows = []
        porous_length = 0.2
        linear_coefficient = 0.5
        quadratic_coefficient = 1.0
        for index, velocity in enumerate((0.5, 1.0, 1.5, 2.0)):
            baseline = 0.05 * velocity
            net_pressure_drop = porous_length * (
                linear_coefficient * velocity + quadratic_coefficient * velocity**2
            )
            self.rows.append(
                {
                    "case_id": f"synthetic_{index + 1}",
                    "velocity_m_s": velocity,
                    "pressure_drop_pa": baseline + net_pressure_drop,
                    "baseline_pressure_drop_pa": baseline,
                    "pressure_drop_uncertainty_pa": 0.01,
                    "baseline_pressure_drop_uncertainty_pa": 0.01,
                    "net_pressure_uncertainty_pa": 2**0.5 * 0.01,
                    "split": "calibration" if index < 3 else "validation",
                    "net_pressure_drop_pa": net_pressure_drop,
                }
            )

    def test_recovers_known_coefficients_and_validates_holdout(self):
        result = fit_resistance(self.rows, 0.2, 0.01, 1.25)

        self.assertAlmostEqual(result["permeability_alpha_m2"], 0.02, places=12)
        self.assertAlmostEqual(
            result["forchheimer_coefficient_C2_m_inv"], 1.6, places=12
        )
        self.assertAlmostEqual(
            result["metrics"]["validation"]["rmse_pa"], 0.0, places=12
        )

    def test_csv_loader_subtracts_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "measurements.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(
                    stream,
                    fieldnames=(
                        "case_id",
                        "velocity_m_s",
                        "pressure_drop_pa",
                        "baseline_pressure_drop_pa",
                        "pressure_drop_uncertainty_pa",
                        "baseline_pressure_drop_uncertainty_pa",
                        "split",
                    ),
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "case_id": "example",
                        "velocity_m_s": 1.0,
                        "pressure_drop_pa": 1.25,
                        "baseline_pressure_drop_pa": 0.25,
                        "pressure_drop_uncertainty_pa": 0.04,
                        "baseline_pressure_drop_uncertainty_pa": 0.03,
                        "split": "calibration",
                    }
                )

            loaded = load_measurements(path)

        self.assertEqual(loaded[0]["net_pressure_drop_pa"], 1.0)
        self.assertAlmostEqual(loaded[0]["net_pressure_uncertainty_pa"], 0.05)


if __name__ == "__main__":
    unittest.main()
