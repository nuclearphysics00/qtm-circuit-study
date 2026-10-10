import re
import shutil
import subprocess
from pathlib import Path

import pytest


CIRCUITS_DIR = Path(__file__).parents[1] / "circuits"


def run_ngspice(filename: str) -> str:
    if shutil.which("ngspice") is None:
        pytest.skip("ngspice is not installed")

    result = subprocess.run(
        ["ngspice", "-b", str(CIRCUITS_DIR / filename)],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout + result.stderr


def measured_value(output: str, name: str) -> float:
    match = re.search(rf"^{name}\s*=\s*([\d.eE+-]+)", output, re.MULTILINE)
    assert match is not None, f"measurement {name!r} was not found"
    return float(match.group(1))


def test_integrator_only():
    output = run_ngspice("03_integrator/03_integrator_only.cir")

    assert measured_value(output, "input_charge") == pytest.approx(200e-12, rel=1e-3)
    assert measured_value(output, "capacitor_peak") == pytest.approx(2.0, rel=1e-3)


def test_discharge_only():
    output = run_ngspice("04_discharge/04_discharge_only.cir")

    assert measured_value(output, "threshold_time") == pytest.approx(190e-9, rel=2e-3)
    assert measured_value(output, "voltage_at_190ns") == pytest.approx(0.1, rel=2e-3)


def test_comparator_only():
    output = run_ngspice("05_comparator/05_comparator_only.cir")

    assert measured_value(output, "input_crossing") == pytest.approx(190e-9, rel=2e-3)
    assert measured_value(output, "output_fall") == pytest.approx(190e-9, rel=2e-3)
