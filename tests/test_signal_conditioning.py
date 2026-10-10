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


def test_impedance_matching():
    output = run_ngspice("02_impedance_matching/02_impedance_matching.cir")

    assert measured_value(output, "launched_voltage") == pytest.approx(1.0, rel=1e-3)
    assert measured_value(output, "load_voltage") == pytest.approx(1.0, rel=1e-3)
    assert measured_value(output, "propagation_delay") == pytest.approx(5e-9, rel=1e-3)


def test_rc_integrator():
    output = run_ngspice("07_rc_integrator/07_rc_integrator.cir")

    assert measured_value(output, "output_peak") == pytest.approx(0.0956, rel=2e-3)
    assert measured_value(output, "output_at_11ns") == pytest.approx(0.0949, rel=2e-3)


def test_rc_differentiator():
    output = run_ngspice("08_rc_differentiator/08_rc_differentiator.cir")

    assert measured_value(output, "positive_peak") == pytest.approx(0.975, rel=2e-3)
    assert measured_value(output, "negative_peak") == pytest.approx(-0.975, rel=2e-3)
