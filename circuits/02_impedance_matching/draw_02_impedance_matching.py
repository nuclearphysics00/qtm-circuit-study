"""Draw a source, transmission line, and load with matched impedances."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("02_impedance_matching_circuit.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=3, fontsize=12)

    source = drawing.add(elm.SourcePulse().up())
    drawing.add(elm.Ground().at(source.start))

    drawing.add(elm.Resistor().right().at(source.end))
    drawing.add(elm.Dot())

    coax = drawing.add(elm.Coax().right())
    drawing.add(elm.Dot())
    drawing.add(elm.Resistor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Line().down().at(coax.shieldstart).length(0.7))
    drawing.add(elm.Ground())
    drawing.add(elm.Line().down().at(coax.shieldend).length(0.7))
    drawing.add(elm.Ground())

    drawing.add(elm.Label().at((-1.2, 1.5)).label("Vin\n2 V, 10 ns"))
    drawing.add(elm.Label().at((1.5, 3.55)).label("Rsource = 50 Ω"))
    drawing.add(
        elm.Label().at((4.5, 4.1)).label(
            "Transmission line\nZ0 = 50 Ω, TD = 5 ns"
        )
    )
    drawing.add(elm.Label().at((3.0, 2.45)).label("line_in"))
    drawing.add(elm.Label().at((5.65, 2.35)).label("line_out"))
    drawing.add(elm.Label().at((7.2, 1.5)).label("Rload = 50 Ω"))
    drawing.add(
        elm.Label().at((3.2, -1.6)).label(
            "Rsource = Z0 = Rload = 50 Ω  →  ΓL = 0"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
