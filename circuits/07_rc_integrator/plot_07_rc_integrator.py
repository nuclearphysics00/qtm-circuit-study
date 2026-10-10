"""Run the passive RC integrator netlist and plot its node voltages."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("07_rc_integrator.cir")
OUTPUT_PATH = Path(__file__).with_name("07_rc_integrator.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time plus input and output voltages."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata rc_integrator.dat v(input) v(output)
"""
    netlist = netlist.replace(".endc", output_commands + ".endc", 1)

    with tempfile.TemporaryDirectory() as temporary_directory:
        directory = Path(temporary_directory)
        temporary_netlist = directory / NETLIST_PATH.name
        temporary_netlist.write_text(netlist, encoding="utf-8")

        subprocess.run(
            ["ngspice", "-b", str(temporary_netlist)],
            cwd=directory,
            capture_output=True,
            text=True,
            check=True,
        )
        return np.loadtxt(directory / "rc_integrator.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    input_voltage = data[:, 1]
    output_voltage = data[:, 2]

    figure, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

    axes[0].plot(time_ns, input_voltage, color="black")
    axes[0].set_ylabel("V(input) [V]")

    axes[1].plot(time_ns, output_voltage, color="#2563eb")
    axes[1].axvspan(1, 11, color="#dbeafe", alpha=0.5, label="input high")
    axes[1].set_ylabel("V(output) [V]")
    axes[1].set_xlabel("Time [ns]")
    axes[1].legend(loc="upper right", frameon=False)

    for axis in axes:
        axis.set_xlim(0, 40)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("Passive RC integrator: ngspice simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "Rint = 1 kohm, Cint = 100 pF, tau = 100 ns; pulse width = 10 ns",
        ha="center",
        fontsize=10,
    )
    figure.tight_layout(rect=(0.04, 0.05, 0.99, 0.95))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
