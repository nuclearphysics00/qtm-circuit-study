"""Draw the one-channel QTC behavioral circuit."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("06_qtc_behavioral_circuit.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=2.5, fontsize=11)

    input_source = drawing.add(
        elm.SourcePulse().up().at((0, 0))
    )
    drawing.add(elm.Ground().at(input_source.start))

    input_node = input_source.end
    drawing.add(elm.Line().right().at(input_node).length(2))
    drawing.add(elm.Dot())
    termination_node = drawing.here
    drawing.add(elm.Resistor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Arrow().right().at(termination_node).length(2))
    drawing.add(elm.Rect((4, 2.25), (7.5, 3.75)).at((0, 0)))
    drawing.add(
        elm.Label().at((5.75, 3.0)).label(
            "Bcharge\nV/I conversion\nCharge gate"
        )
    )

    drawing.add(elm.Arrow().right().at((7.5, 3)).length(1.5))
    capacitor_node = drawing.here
    drawing.add(elm.Dot())
    drawing.add(elm.Capacitor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Line().right().at(capacitor_node).length(2))
    drawing.add(elm.Resistor().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Line().right().at(capacitor_node).length(4))
    discharge_node = drawing.here
    drawing.add(elm.Dot())
    drawing.add(elm.SourceI().down())
    drawing.add(elm.Ground())

    drawing.add(elm.Arrow().right().at(discharge_node).length(2))
    drawing.add(elm.Rect((15, 2.25), (18.8, 3.75)).at((0, 0)))
    drawing.add(
        elm.Label().at((16.9, 3.0)).label(
            "Boutput\nV(cap) > Vth\nOR Charge gate"
        )
    )
    drawing.add(elm.Arrow().right().at((18.8, 3)).length(1.5))
    drawing.add(elm.Label().at((20.6, 3.25)).label("qtc_output"))

    drawing.add(
        elm.Arrow().down().at((5.75, 6.0)).to((5.75, 3.75))
        .label("charge_gate\n1–401 ns", loc="right")
    )
    drawing.add(
        elm.Arrow().down().at((13, 6.0)).to((13, 3.2))
        .label("discharge_gate\n401–751 ns", loc="right")
    )

    drawing.add(elm.Label().at((-1.5, 1.7)).label("Vin\n1 V, 10 ns"))
    drawing.add(elm.Label().at((2, 3.45)).label("node: input"))
    drawing.add(elm.Label().at((2.8, 1.5)).label("Rterm\n50 Ω"))
    drawing.add(elm.Label().at((9, 3.45)).label("node: cap"))
    drawing.add(elm.Label().at((8.15, 1.45)).label("Cint\n100 pF"))
    drawing.add(elm.Label().at((11.5, 1.45)).label("Rleak\n1 TΩ"))
    drawing.add(
        elm.Label().at((14.6, 1.7)).label("Bdischarge\nIdis = 1 mA")
    )
    drawing.add(
        elm.Label().at((7.0, -1.1)).label(
            "Input charge → V(cap) → constant-current discharge → output width"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
