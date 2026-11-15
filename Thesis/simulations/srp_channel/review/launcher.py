#!/usr/bin/env python3
"""Run the thesis-owned NGA2 channel case in an isolated output directory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


EXECUTABLE = Path("/opt/nga2/bin/nga2-srp-channel")
PROVISIONAL_NOTICE = (
    "PRE-CALIBRATION REVIEW ONLY: current geometry and porous coefficients are provisional."
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def partition_size(config: Path) -> int:
    pattern = re.compile(r"^\s*Partition\s*:\s*(\d+)\s+(\d+)\s+(\d+)\s*$", re.I)
    for line in config.read_text(encoding="utf-8").splitlines():
        match = pattern.match(line)
        if match:
            values = [int(value) for value in match.groups()]
            return values[0] * values[1] * values[2]
    raise SystemExit(f"Configuration has no valid 'Partition : X Y Z' line: {config}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="nga2Adsorption",
        description=(
            "Launch the thesis-owned NGA2 airflow case. "
            "All bundled geometry and resistance values are provisional."
        ),
    )
    parser.add_argument("--config", type=Path, required=True, help="NGA2 input file")
    parser.add_argument(
        "--output", type=Path, required=True, help="new directory for input and results"
    )
    parser.add_argument("--ranks", type=int, required=True, help="MPI rank count")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = args.config.resolve()
    output = args.output.resolve()
    if not config.is_file():
        raise SystemExit(f"Configuration not found: {config}")
    if args.ranks < 1:
        raise SystemExit("--ranks must be a positive integer")
    expected_ranks = partition_size(config)
    if expected_ranks != args.ranks:
        raise SystemExit(
            f"--ranks {args.ranks} does not match configuration partition product "
            f"{expected_ranks}"
        )
    if output.exists():
        raise SystemExit(f"Output directory already exists: {output}")
    if not EXECUTABLE.is_file():
        raise SystemExit(f"Container executable is missing: {EXECUTABLE}")

    output.mkdir(parents=True)
    copied_config = output / "input"
    shutil.copyfile(config, copied_config)
    command = [
        "mpiexec",
        "--allow-run-as-root",
        "--oversubscribe",
        "--mca",
        "btl",
        "self,tcp",
        "-n",
        str(args.ranks),
        str(EXECUTABLE),
        "-i",
        "input",
    ]
    manifest = {
        "status": "provisional_pre_calibration",
        "notice": PROVISIONAL_NOTICE,
        "config_sha256": sha256(copied_config),
        "executable_sha256": sha256(EXECUTABLE),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "ranks": args.ranks,
        "partition_product": expected_ranks,
        "command": command,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print(PROVISIONAL_NOTICE, flush=True)
    environment = os.environ.copy()
    environment["OMPI_ALLOW_RUN_AS_ROOT"] = "1"
    environment["OMPI_ALLOW_RUN_AS_ROOT_CONFIRM"] = "1"
    with (output / "launcher.log").open("w", encoding="utf-8") as log:
        completed = subprocess.run(
            command,
            cwd=output,
            env=environment,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
    manifest["returncode"] = completed.returncode
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if completed.returncode != 0:
        print(f"NGA2 failed with exit code {completed.returncode}: {output / 'launcher.log'}")
        return completed.returncode
    print(f"NGA2 completed: {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
