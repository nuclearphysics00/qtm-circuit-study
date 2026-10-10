# circuits

練習用の回路図とSPICE回路を置きます。現在の50 Ω入力回路は、QTM実機の内部回路ではありません。

## ファイル

- `draw_01_input_50ohm.py`: Schemdrawで回路図を描くPythonコード
- `01_input_50ohm.svg`: Pythonコードから生成した回路図
- `01_input_50ohm.cir`: ngspiceで計算する回路

## 回路図を作る

```bash
source .venv/bin/activate
python circuits/draw_01_input_50ohm.py
```

### Schemdrawの呼び出し例

```python
drawing = schemdraw.Drawing(show=False)
drawing.config(unit=3, fontsize=12)

source = drawing.add(elm.SourcePulse().up().label("Vin(t)"))
drawing.add(elm.Line().right().at(source.end).length(4))
drawing.add(elm.Resistor().down().label("50 Ω"))
drawing.add(elm.Line().to(source.start))
drawing.add(elm.Ground().at(source.start))
drawing.add(elm.Label().at((4, 3.45)).label("QTM input"))

drawing.save("circuits/example.svg")
```

- 図面を作る：`schemdraw.Drawing()`
- 部品を置く：`drawing.add(elm.部品名())`
- 部品の向きを変える：`.up()`、`.down()`、`.left()`、`.right()`
- 部品を指定位置に置く：`.at(...)`
- 配線を指定位置まで引く：`elm.Line().to(...)`
- 部品や配線の長さを変える：`.length(...)`
- 文字を付ける：`.label(...)`
- SVGを保存する：`drawing.save(...)`

## SPICE計算をする

```bash
ngspice -b circuits/01_input_50ohm.cir
```

### ngspiceの呼び出し例

```spice
* 1 V、幅10 nsのパルス電圧源
Vin input 0 PULSE(0 1 1n 1p 1p 10n 30n)

* inputとGNDの間に50 ohmの抵抗を置く
Rterm input 0 50

.control
tran 0.01n 15n
let input_current = -i(Vin)
meas tran peak_current MAX input_current FROM=1n TO=11n
meas tran input_charge INTEG input_current FROM=1n TO=11.001n
.endc

.end
```

各行の読み方：

- `Vin input 0 ...`
  - `Vin`は電圧源の名前、`input`は接続点、`0`はGND
- `PULSE(0 1 1n 1p 1p 10n 30n)`
  - 0 Vから1 Vへ変化するパルス
  - 1 ns後に開始、立ち上がりと立ち下がりは1 ps
  - パルス幅は10 ns、周期は30 ns
- `Rterm input 0 50`
  - `input`とGNDの間に50 Ωの抵抗を接続する
- `tran 0.01n 15n`
  - 0.01 ns刻みで15 nsまで計算する
- `let input_current = -i(Vin)`
  - 入力方向の電流に`input_current`という名前を付ける
- `meas ... MAX ...`
  - 指定した時間内の最大電流を測る
- `meas ... INTEG ...`
  - 指定した時間内の電流を積分して電荷を求める

現在の設定は、1 V、10 nsのパルスを50 Ωへ入力します。期待値は20 mA、約200 pCです。
