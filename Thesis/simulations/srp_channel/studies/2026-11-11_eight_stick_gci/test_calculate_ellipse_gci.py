import tempfile
import unittest
from pathlib import Path

from calculate_ellipse_gci import calculate_gci, net_drop


class CalculateEllipseGciTest(unittest.TestCase):
    def write_case(self, directory, rows):
        monitor = directory / "monitor"
        monitor.mkdir(parents=True)
        with (monitor / "sheet_pressure").open("w", encoding="utf-8") as stream:
            for step, time, pressure in rows:
                stream.write(f"{step} {time} 0 0 {pressure}\n")

    def test_net_drop_aligns_active_and_control_timesteps(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            active = root / "active"
            control = root / "control"
            active.mkdir()
            control.mkdir()
            self.write_case(
                active,
                [(1, 3.0, 12.0), (2, 3.5, 14.0), (3, 4.0, 16.0)],
            )
            self.write_case(
                control,
                [(1, 3.0, 2.0), (2, 3.5, 6.0), (3, 4.0, 4.0), (4, 3.75, 100.0)],
            )

            self.assertAlmostEqual(net_drop(active, control, 3.0, 4.0), 10.0)

    def test_net_drop_rejects_empty_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            active = root / "active"
            control = root / "control"
            active.mkdir()
            control.mkdir()
            self.write_case(active, [(1, 3.0, 12.0), (2, 3.5, 14.0)])
            self.write_case(control, [(3, 3.0, 2.0), (4, 3.5, 4.0)])

            with self.assertRaisesRegex(ValueError, "Too few aligned"):
                net_drop(active, control, 3.0, 4.0)

    def test_net_drop_rejects_mismatched_physical_times(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            active = root / "active"
            control = root / "control"
            active.mkdir()
            control.mkdir()
            self.write_case(
                active,
                [(1, 3.0, 12.0), (2, 3.5, 14.0), (3, 4.0, 16.0)],
            )
            self.write_case(
                control,
                [(1, 3.0, 2.0), (2, 3.5000001, 4.0), (3, 4.0, 6.0)],
            )

            with self.assertRaisesRegex(ValueError, "mismatched physical times"):
                net_drop(active, control, 3.0, 4.0)

    def test_invalid_grid_sequences(self):
        with self.assertRaisesRegex(ValueError, "oscillatory"):
            calculate_gci(1.0, 0.75, 1.0)
        for values in ((0.0, 0.5, 0.25), (1.0, float("inf"), 0.25)):
            with self.assertRaises(ValueError):
                calculate_gci(*values)
        with self.assertRaisesRegex(ValueError, "Refinement ratio"):
            calculate_gci(1.0, 0.5, 0.25, refinement_ratio=1.0)
        with self.assertRaisesRegex(ValueError, "safety factor"):
            calculate_gci(1.0, 0.5, 0.25, safety_factor=0.0)

    def test_known_second_order_convergence(self):
        order, extrapolated, fine_gci, medium_gci, ratio = calculate_gci(
            1.0, 0.75, 0.6875
        )
        self.assertAlmostEqual(order, 2.0)
        self.assertAlmostEqual(extrapolated, 2.0 / 3.0)
        self.assertGreater(fine_gci, 0.0)
        self.assertGreater(medium_gci, 0.0)
        self.assertAlmostEqual(ratio, 11.0 / 12.0)

    def test_invalid_averaging_window(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory)
            (case / "monitor").mkdir()
            with (case / "monitor" / "sheet_pressure").open(
                "w", encoding="utf-8"
            ) as stream:
                stream.write("1 3.0 0 0 1.0\n")

            with self.assertRaisesRegex(ValueError, "greater than window start"):
                net_drop(case, case, 4.0, 3.0)


if __name__ == "__main__":
    unittest.main()
