"""Draw a passive RC integrator."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("07_rc_integrator_circuit.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=3, fontsize=12)

    source = drawing.add(elm.SourcePulse().up())
    drawing.add(elm.Ground().at(source.start))
    drawing.add(elm.Resistor().right().at(source.end))
    drawing.add(elm.Dot())
    drawing.add(elm.Capacitor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Label().at((-1.2, 1.5)).label("Vin\n1 V, 10 ns"))
    drawing.add(elm.Label().at((-0.45, 3.65)).label("node: input"))
    drawing.add(elm.Label().at((1.5, 4.15)).label("Rint = 1 kΩ"))
    drawing.add(elm.Label().at((3.45, 3.65)).label("node: output"))
    drawing.add(elm.Label().at((4.4, 1.5)).label("Cint = 100 pF"))
    drawing.add(
        elm.Label().at((1.5, -1.2)).label(
            "τ = Rint Cint = 100 ns;  Vout ≈ (1/τ) ∫Vin dt"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
