"""Draw the isolated educational charge integrator circuit."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("03_integrator_only.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=2.5, fontsize=12)

    source = drawing.add(
        elm.SourceI().up().label("Iinput\n20 mA, 10 ns", loc="left")
    )
    drawing.add(elm.Line().right().at(source.end).length(1))
    drawing.add(elm.SourceV().right())
    drawing.add(elm.Line().right().length(1))
    capacitor_node = drawing.here
    drawing.add(elm.Dot())

    drawing.add(elm.Capacitor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Line().right().at(capacitor_node).length(2))
    drawing.add(elm.Resistor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Label().at((2.25, 3.15)).label("Vsense = 0 V"))
    drawing.add(elm.Label().at((4.5, 3.15)).label("node: cap"))
    drawing.add(elm.Label().at((2.6, 1.25)).label("Cint = 100 pF"))
    drawing.add(elm.Label().at((8.2, 1.25)).label("Rleak = 1 TΩ"))

    drawing.add(
        elm.Label().at((3.5, -1.2)).label(
            "Educational model: Q = ∫Iinput dt,  V(cap) = Q / Cint"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
