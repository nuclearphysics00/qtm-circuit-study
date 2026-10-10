"""Run the passive RC differentiator netlist and plot its node voltages."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("08_rc_differentiator.cir")
OUTPUT_PATH = Path(__file__).with_name("08_rc_differentiator.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time plus input and output voltages."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata rc_differentiator.dat v(input) v(output)
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
        return np.loadtxt(directory / "rc_differentiator.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    input_voltage = data[:, 1]
    output_voltage = data[:, 2]

    figure, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

    axes[0].plot(time_ns, input_voltage, color="black")
    axes[0].set_ylabel("V(input) [V]")

    axes[1].plot(time_ns, output_voltage, color="#ea580c")
    axes[1].axhline(0, color="#64748b", linewidth=0.8)
    axes[1].axvline(5, color="#16a34a", linestyle=":", label="rising edge")
    axes[1].axvline(15, color="#7c3aed", linestyle=":", label="falling edge")
    axes[1].set_ylabel("V(output) [V]")
    axes[1].set_xlabel("Time [ns]")
    axes[1].legend(loc="upper right", frameon=False, ncol=2)

    for axis in axes:
        axis.set_xlim(0, 25)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("Passive RC differentiator: ngspice simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "Rdiff = 1 kohm, Cdiff = 1 pF, tau = 1 ns; pulse width = 10 ns",
        ha="center",
        fontsize=10,
    )
    figure.tight_layout(rect=(0.04, 0.05, 0.99, 0.95))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
