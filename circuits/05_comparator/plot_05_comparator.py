"""Run the ideal comparator netlist and plot its node voltages."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("05_comparator_only.cir")
OUTPUT_PATH = Path(__file__).with_name("05_comparator.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time plus comparator input and output voltages."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata comparator.dat v(cap) v(comparator_output)
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
        return np.loadtxt(directory / "comparator.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    input_voltage = data[:, 1]
    output_voltage = data[:, 2]

    figure, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

    axes[0].plot(time_ns, input_voltage, color="#2563eb")
    axes[0].axhline(0.1, color="#dc2626", linestyle=":", label="Vth = 0.1 V")
    axes[0].axvline(190.0, color="#64748b", linestyle="--", label="crossing")
    axes[0].set_ylabel("V(cap) [V]")
    axes[0].legend(loc="upper right", frameon=False, ncol=2)

    axes[1].plot(time_ns, output_voltage, color="#ea580c")
    axes[1].axvline(190.0, color="#64748b", linestyle="--")
    axes[1].set_ylabel("V(comparator_output) [V]")
    axes[1].set_xlabel("Time [ns]")

    for axis in axes:
        axis.set_xlim(0, 210)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("Ideal threshold comparator: ngspice simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "The ideal behavioral comparator changes state at V(cap) = Vth = 0.1 V",
        ha="center",
        fontsize=10,
    )
    figure.tight_layout(rect=(0.04, 0.05, 0.99, 0.95))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
