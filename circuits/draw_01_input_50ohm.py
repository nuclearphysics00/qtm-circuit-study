"""Generate the practice diagram for a 50-ohm terminated input."""
#　左側のパルス電圧源で Vin を発生させ、右側の50Ω抵抗で終端される回路図を描画する。

from pathlib import Path

import schemdraw
import schemdraw.elements as elm


OUTPUT_PATH = Path(__file__).with_name("01_input_50ohm.svg")


def main() -> None:
    schemdraw.use("svg")

    drawing = schemdraw.Drawing(show=False)
    drawing.config(unit=3, fontsize=12)

    source = drawing.add(elm.SourcePulse().up().label("Input pulse\nVin(t)", loc="bottom"))
    drawing.add(elm.Line().right().at(source.end).length(4))
    drawing.add(elm.Dot())
    termination = drawing.add(elm.Resistor().down())
    drawing.add(elm.Line().left().at(termination.end).to(source.start))
    drawing.add(elm.Ground().at(source.start))

    drawing.add(elm.Label().at((4, 3.45)).label("QTM input", halign="center"))
    drawing.add(elm.Label().at((4.8, 1.5)).label("RT = 50 Ω", halign="left"))

    drawing.add(
        elm.Arrow().right().at((1.2, 3.55)).length(1.6).label(
            "i(t) = Vin(t) / 50 Ω", loc="top"
        )
    )
    drawing.add(
        elm.Label().at((2, -1.2)).label(
            "Q = ∫ i(t) dt = ∫ Vin(t) / 50 Ω dt"
        )
    )

    drawing.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
