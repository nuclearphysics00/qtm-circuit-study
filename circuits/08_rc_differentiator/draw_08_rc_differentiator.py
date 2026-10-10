"""Draw a passive RC differentiator."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("08_rc_differentiator_circuit.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=3, fontsize=12)

    source = drawing.add(elm.SourcePulse().up())
    drawing.add(elm.Ground().at(source.start))
    drawing.add(elm.Capacitor().right().at(source.end))
    drawing.add(elm.Dot())
    drawing.add(elm.Resistor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Label().at((-1.2, 1.5)).label("Vin\n1 V, 10 ns"))
    drawing.add(elm.Label().at((-0.45, 3.65)).label("node: input"))
    drawing.add(elm.Label().at((1.5, 4.15)).label("Cdiff = 1 pF"))
    drawing.add(elm.Label().at((3.45, 3.65)).label("node: output"))
    drawing.add(elm.Label().at((4.3, 1.5)).label("Rdiff = 1 kΩ"))
    drawing.add(
        elm.Label().at((1.5, -1.2)).label(
            "τ = Rdiff Cdiff = 1 ns;  Vout ≈ τ dVin/dt"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
