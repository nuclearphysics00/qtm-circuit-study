"""Run the QTC behavioral netlist and plot its simulated waveforms."""

from pathlib import Path
import subprocess
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


NETLIST_PATH = Path(__file__).with_name("06_qtc_behavioral.cir")
OUTPUT_PATH = Path(__file__).with_name("06_qtc_simulation.svg")


def simulate() -> np.ndarray:
    """Run ngspice and return time plus five simulated voltage traces."""
    netlist = NETLIST_PATH.read_text(encoding="utf-8")
    output_commands = """set wr_singlescale
set wr_vecnames
wrdata qtc_waveforms.dat v(input) v(charge_gate) v(discharge_gate) v(cap) v(qtc_output)
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
        return np.loadtxt(directory / "qtc_waveforms.dat", skiprows=1)


def main() -> None:
    data = simulate()
    time_ns = data[:, 0] * 1e9
    input_voltage = data[:, 1]
    charge_gate = data[:, 2]
    discharge_gate = data[:, 3]
    capacitor_voltage = data[:, 4]
    output_voltage = data[:, 5]

    figure, axes = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(time_ns, input_voltage, color="black")
    axes[0].set_ylabel("Input [V]")

    axes[1].plot(time_ns, charge_gate, label="Charge gate", color="#16a34a")
    axes[1].plot(
        time_ns,
        discharge_gate,
        label="Discharge gate",
        color="#7c3aed",
        linestyle="--",
    )
    axes[1].set_ylabel("Gate [V]")
    axes[1].legend(loc="upper right", frameon=False, ncol=2)

    axes[2].plot(time_ns, capacitor_voltage, color="#2563eb")
    axes[2].axhline(0.1, color="#dc2626", linestyle=":", label="Threshold = 0.1 V")
    axes[2].set_ylabel("Integrator [V]")
    axes[2].legend(loc="upper right", frameon=False)

    axes[3].plot(time_ns, output_voltage, color="#ea580c")
    axes[3].set_ylabel("QTC output [V]")
    axes[3].set_xlabel("Time [ns]")

    for axis in axes:
        axis.set_xlim(0, 900)
        axis.grid(color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right"]].set_visible(False)

    figure.suptitle("QTC behavioral model: ngspice transient simulation", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "Study parameters: Cint = 100 pF, Idis = 1 mA, Vth = 0.1 V. "
        "These are not verified CLC101 internal values.",
        ha="center",
        fontsize=9,
    )
    figure.tight_layout(rect=(0.04, 0.045, 0.99, 0.96))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
