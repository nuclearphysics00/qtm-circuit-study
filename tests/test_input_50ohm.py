import re
import shutil
import subprocess
from pathlib import Path

import pytest


NETLIST = (
    Path(__file__).parents[1]
    / "circuits"
    / "01_input_50ohm"
    / "01_input_50ohm.cir"
)


def test_ngspice_input_50ohm():
    if shutil.which("ngspice") is None:
        pytest.skip("ngspice is not installed")

    result = subprocess.run(
        ["ngspice", "-b", str(NETLIST)],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout + result.stderr

    current_match = re.search(
        r"peak_current\s*=\s*([\d.eE+-]+)",
        output,
    )
    charge_match = re.search(
        r"input_charge\s*=\s*([\d.eE+-]+)",
        output,
    )

    assert current_match is not None
    assert charge_match is not None

    peak_current = float(current_match.group(1))
    input_charge = float(charge_match.group(1))

    assert peak_current == pytest.approx(20e-3, rel=1e-4)
    assert input_charge == pytest.approx(200e-12, rel=1e-3)
