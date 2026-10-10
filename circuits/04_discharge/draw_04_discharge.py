"""Draw the constant-current discharge circuit."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("04_discharge_circuit.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=2.7, fontsize=12)

    capacitor_node = (0, 3)
    drawing.add(elm.Dot().at(capacitor_node))
    drawing.add(elm.Capacitor().down().at(capacitor_node))
    drawing.add(elm.Ground())

    drawing.add(elm.Line().right().at(capacitor_node).length(4))
    drawing.add(elm.Dot())
    drawing.add(elm.SourceI().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Label().at((-0.5, 3.55)).label("node: cap"))
    drawing.add(elm.Label().at((2.0, 3.55)).label("V(cap): 2 V → 0.1 V"))
    drawing.add(elm.Label().at((-1.5, 1.5)).label("Cint = 100 pF\nIC = 2 V"))
    drawing.add(elm.Label().at((5.7, 1.8)).label("Idis = 1 mA"))
    drawing.add(
        elm.Label().at((1.2, -1.1)).label(
            "dV(cap)/dt = -Idis / Cint = -0.01 V/ns"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
