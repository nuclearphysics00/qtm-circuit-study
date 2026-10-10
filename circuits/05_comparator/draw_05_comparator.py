"""Draw the threshold comparator circuit."""

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("05_comparator_circuit.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=2.7, fontsize=12)

    comparator = drawing.add(elm.Opamp().at((5, 3)))

    drawing.add(
        elm.Arrow().right().at((0, comparator.in2[1])).to(comparator.in2)
        .label("V(cap)\n2 V → 0 V", loc="bottom")
    )
    drawing.add(
        elm.Arrow().right().at((0, comparator.in1[1])).to(comparator.in1)
        .label("Vth = 0.1 V", loc="top")
    )

    drawing.add(elm.Line().right().at(comparator.out).length(2))
    drawing.add(elm.Dot())

    drawing.add(elm.Label().at((6.0, 4.25)).label("Comparator: Boutput"))
    drawing.add(
        elm.Label().at((8.7, 3.2)).label("node: comparator_output")
    )
    drawing.add(
        elm.Label().at((2.2, 0.6)).label(
            "Vout = 1 V if V(cap) > Vth; otherwise 0 V"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
