import re
import shutil
import subprocess
from pathlib import Path

import pytest


NETLIST = (
    Path(__file__).parents[1]
    / "circuits"
    / "06_qtc_behavioral"
    / "06_qtc_behavioral.cir"
)


def measured_value(output: str, name: str) -> float:
    match = re.search(rf"^{name}\s*=\s*([\d.eE+-]+)", output, re.MULTILINE)
    assert match is not None, f"measurement {name!r} was not found"
    return float(match.group(1))


def test_qtc_behavioral_model():
    if shutil.which("ngspice") is None:
        pytest.skip("ngspice is not installed")

    result = subprocess.run(
        ["ngspice", "-b", str(NETLIST)],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout + result.stderr

    assert measured_value(output, "positive_input_charge") == pytest.approx(
        200e-12, rel=1e-3
    )
    assert measured_value(output, "capacitor_peak") == pytest.approx(2.0, rel=1e-3)
    assert measured_value(output, "discharge_time") == pytest.approx(190e-9, rel=2e-3)
    assert measured_value(output, "output_width") == pytest.approx(590e-9, rel=2e-3)
