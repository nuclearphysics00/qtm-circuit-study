"""Run the constant-current discharge netlist and plot its waveforms."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("04_discharge_only.cir")
OUTPUT_PATH = Path(__file__).with_name("04_discharge.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time plus the capacitor-node voltage."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata discharge.dat v(cap)
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
        return np.loadtxt(directory / "discharge.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    capacitor_voltage = data[:, 1]
    capacitor_charge_pc = 100e-12 * capacitor_voltage * 1e12
    discharge_current_ma = np.full_like(time_ns, 1.0)

    figure, axes = plt.subplots(3, 1, figsize=(9, 7.5), sharex=True)

    axes[0].plot(time_ns, discharge_current_ma, color="black")
    axes[0].set_ylabel("I(discharge) [mA]")
    axes[0].set_ylim(0, 1.25)

    axes[1].plot(time_ns, capacitor_charge_pc, color="#16a34a")
    axes[1].axhline(10.0, color="#dc2626", linestyle=":", label="Q at Vth")
    axes[1].set_ylabel("Q(Cint) [pC]")
    axes[1].legend(loc="upper right", frameon=False)

    axes[2].plot(time_ns, capacitor_voltage, color="#2563eb")
    axes[2].axhline(0.1, color="#dc2626", linestyle=":", label="Vth = 0.1 V")
    axes[2].axvline(190.0, color="#64748b", linestyle="--", label="t = 190 ns")
    axes[2].set_ylabel("V(cap) [V]")
    axes[2].set_xlabel("Time [ns]")
    axes[2].legend(loc="upper right", frameon=False, ncol=2)

    for axis in axes:
        axis.set_xlim(0, 195)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("Constant-current discharge: ngspice simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "Cint = 100 pF, Idis = 1 mA: V(cap) falls from 2.0 V to 0.1 V in 190 ns",
        ha="center",
        fontsize=10,
    )
    figure.tight_layout(rect=(0.04, 0.045, 0.99, 0.95))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
