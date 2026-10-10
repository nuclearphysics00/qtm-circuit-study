"""Run the isolated integrator netlist and plot its simulated waveforms."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("03_integrator_only.cir")
OUTPUT_PATH = Path(__file__).with_name("03_integrator.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time, input current, and capacitor voltage."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata integrator.dat i(Vsense) v(cap)
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
        return np.loadtxt(directory / "integrator.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    input_current_ma = data[:, 1] * 1e3
    capacitor_voltage = data[:, 2]
    accumulated_charge_pc = 100e-12 * capacitor_voltage * 1e12

    figure, axes = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)

    axes[0].plot(time_ns, input_current_ma, color="black")
    axes[0].set_ylabel("I(Vsense) [mA]")

    axes[1].plot(time_ns, accumulated_charge_pc, color="#16a34a")
    axes[1].axhline(
        200.0, color="#dc2626", linestyle=":", label="Expected 200 pC"
    )
    axes[1].set_ylabel("Q(Cint) [pC]")
    axes[1].legend(loc="lower right", frameon=False)

    axes[2].plot(time_ns, capacitor_voltage, color="#2563eb")
    axes[2].axhline(2.0, color="#dc2626", linestyle=":", label="Expected 2 V")
    axes[2].set_ylabel("V(cap) [V]")
    axes[2].set_xlabel("Time [ns]")
    axes[2].legend(loc="lower right", frameon=False)

    for axis in axes:
        axis.set_xlim(0, 20)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("Isolated charge integrator: ngspice simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "20 mA x 10 ns = 200 pC; 200 pC / 100 pF = 2 V",
        ha="center",
        fontsize=10,
    )
    figure.tight_layout(rect=(0.04, 0.045, 0.99, 0.95))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
