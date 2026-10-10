"""Run the matched transmission-line netlist and plot its node voltages."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("02_impedance_matching.cir")
OUTPUT_PATH = Path(__file__).with_name("02_impedance_matching.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time plus source, line-input, and load voltages."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata impedance_matching.dat v(source) v(line_in) v(line_out)
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
        return np.loadtxt(directory / "impedance_matching.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    source_voltage = data[:, 1]
    line_input_voltage = data[:, 2]
    load_voltage = data[:, 3]

    figure, axes = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)

    axes[0].plot(time_ns, source_voltage, color="black")
    axes[0].set_ylabel("V(source) [V]")

    axes[1].plot(time_ns, line_input_voltage, color="#16a34a")
    axes[1].axhline(1.0, color="#dc2626", linestyle=":", label="launched 1 V")
    axes[1].set_ylabel("V(line_in) [V]")
    axes[1].legend(loc="upper right", frameon=False)

    axes[2].plot(time_ns, load_voltage, color="#2563eb")
    axes[2].axvline(6.0, color="#64748b", linestyle="--", label="5 ns delay")
    axes[2].set_ylabel("V(line_out) [V]")
    axes[2].set_xlabel("Time [ns]")
    axes[2].legend(loc="upper right", frameon=False)

    for axis in axes:
        axis.set_xlim(0, 22)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("50-ohm impedance matching: ngspice simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "Rsource = Z0 = Rload = 50 ohm; the load receives 1 V after TD = 5 ns",
        ha="center",
        fontsize=10,
    )
    figure.tight_layout(rect=(0.04, 0.045, 0.99, 0.95))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
