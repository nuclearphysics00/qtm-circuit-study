"""Draw a simplified timing chart for one QTC event."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


OUTPUT_PATH = Path(__file__).with_name("02_qtc_timing.svg")


def gate(time: np.ndarray, start: float, stop: float) -> np.ndarray:
    """Return a unit-height gate between start and stop."""
    return ((time >= start) & (time < stop)).astype(float)


def integrated_charge(
    time: np.ndarray,
    amplitude: float,
    charge_start: float,
    discharge_start: float,
    discharge_stop: float,
) -> np.ndarray:
    """Return a normalized charge-and-discharge waveform."""
    charge = np.zeros_like(time)
    charging = (time >= charge_start) & (time < discharge_start)
    discharging = (time >= discharge_start) & (time < discharge_stop)

    charge[charging] = amplitude * (
        (time[charging] - charge_start) / (discharge_start - charge_start)
    )
    charge[discharging] = amplitude * (
        1 - (time[discharging] - discharge_start) / (discharge_stop - discharge_start)
    )
    return charge


def main() -> None:
    time = np.linspace(0, 1050, 5251)

    trigger = 100.0
    charge_end = 500.0
    discharge_end = 850.0
    cycle_end = 1000.0
    threshold = 0.20

    pmt = -np.exp(-0.5 * ((time - 110.0) / 9.0) ** 2)
    delayed = -np.exp(-0.5 * ((time - 130.0) / 9.0) ** 2)

    charge_small = integrated_charge(time, 0.45, 130, charge_end, discharge_end)
    charge_medium = integrated_charge(time, 0.70, 130, charge_end, discharge_end)
    charge_large = integrated_charge(time, 0.95, 130, charge_end, discharge_end)

    crossing_times = []
    for waveform in (charge_small, charge_medium, charge_large):
        indices = np.flatnonzero((time >= charge_end) & (waveform <= threshold))
        crossing_times.append(time[indices[0]])

    figure, axes = plt.subplots(
        7,
        1,
        figsize=(11, 9),
        sharex=True,
        gridspec_kw={"height_ratios": [1.1, 0.7, 0.7, 0.7, 0.9, 1.6, 1.1]},
    )

    axes[0].plot(time, pmt, color="black", label="PMT input")
    axes[0].plot(time, delayed, color="#2563eb", linestyle="--", label="LPF delayed")
    axes[0].legend(loc="lower right", frameon=False, ncol=2)

    axes[1].step(time, gate(time, trigger, 125), where="post", color="#dc2626")
    axes[1].set_ylabel("Qtrg")

    axes[2].step(time, gate(time, trigger, 110), where="post", color="#ea580c")
    axes[2].set_ylabel("HIT")

    axes[3].step(time, gate(time, trigger, charge_end), where="post", color="#16a34a")
    axes[3].set_ylabel("Charge\ngate")

    axes[4].step(
        time,
        gate(time, charge_end, discharge_end),
        where="post",
        color="#7c3aed",
        label="Discharge gate",
    )
    axes[4].step(
        time,
        gate(time, discharge_end, cycle_end),
        where="post",
        color="#64748b",
        linestyle="--",
        label="VETO / recovery",
    )
    axes[4].step(
        time,
        gate(time, discharge_end - 5, discharge_end + 5),
        where="post",
        color="black",
        label="Reset",
    )
    axes[4].set_ylabel("Control")
    axes[4].legend(loc="upper right", frameon=False, ncol=3)

    for waveform, label, color in (
        (charge_small, "lower input Q", "#60a5fa"),
        (charge_medium, "middle input Q", "#2563eb"),
        (charge_large, "higher input Q", "#1e3a8a"),
    ):
        axes[5].plot(time, waveform, color=color, label=label)
    axes[5].axhline(threshold, color="#dc2626", linestyle=":", label="comparator threshold")
    axes[5].set_ylabel("Integrated\ncharge\n(normalized)")
    axes[5].legend(loc="upper right", frameon=False, ncol=2)

    for stop, label, color in zip(
        crossing_times,
        ("lower input Q", "middle input Q", "higher input Q"),
        ("#60a5fa", "#2563eb", "#1e3a8a"),
        strict=True,
    ):
        axes[6].step(
            time,
            gate(time, trigger, stop),
            where="post",
            color=color,
            label=label,
        )
    axes[6].set_ylabel("LVDS\noutput")
    axes[6].set_xlabel("Time [ns]")
    axes[6].legend(loc="upper right", frameon=False, ncol=3)

    for axis in axes:
        axis.set_yticks([])
        axis.set_xlim(0, 1050)
        axis.grid(axis="x", color="#d1d5db", linewidth=0.6)
        axis.spines[["top", "right", "left"]].set_visible(False)
        for boundary in (trigger, charge_end, discharge_end, cycle_end):
            axis.axvline(boundary, color="#9ca3af", linewidth=0.8, linestyle=":")

    axes[3].text(300, 1.12, "400 ns", ha="center", va="bottom")
    axes[4].text(675, 1.12, "350 ns", ha="center", va="bottom")
    axes[4].text(925, 1.12, "150 ns", ha="center", va="bottom")

    figure.suptitle("QTC ASIC: simplified timing chart for one event", fontsize=15)
    figure.text(
        0.5,
        0.015,
        "Redrawn from Nishino et al., NIM A 610 (2009), Fig. 5. "
        "Amplitudes are normalized; nominal timings are not current QTM settings.",
        ha="center",
        fontsize=9,
    )
    figure.tight_layout(rect=(0.04, 0.045, 0.99, 0.96))
    figure.savefig(OUTPUT_PATH, format="svg")
    plt.close(figure)


if __name__ == "__main__":
    main()
