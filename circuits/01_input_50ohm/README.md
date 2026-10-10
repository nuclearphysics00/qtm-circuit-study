# 01: 50 Ω入力回路

1 Vのパルス電圧源と50 Ωの終端抵抗から、入力電流と入力電荷を求める回路です。この回路はQTMへの信号入力を表しており、QTM内部回路を再現したものではありません。

## ファイル

- `01_input_50ohm.cir`：ngspiceモデル
- `draw_01_input_50ohm.py`：回路図を生成するコード
- `01_input_50ohm.svg`：生成した回路図

## 回路図

![50 Ω終端された入力回路](01_input_50ohm.svg)

## 回路の説明

- 入力：電圧源`Vin`が生成する、0 Vから1 Vへ立ち上がる幅10 nsのパルス
- 回路：`input`ノードとGNDの間を`Rterm = 50 Ω`で終端
- 観測量：`V(input)`、終端抵抗を流れる`I(input)`、電流を時間積分した入力電荷`Qin`

電圧パルスは1 nsに立ち上がり、11 nsに立ち下がります。終端抵抗にはパルス電圧に比例した電流が流れます。

理想的な50 Ω終端では、入力電圧と入力電流の関係は

$$
I_{\mathrm{in}}(t)=\frac{V_{\mathrm{in}}(t)}{R_{\mathrm{term}}}
$$

です。1 V、10 nsのパルスでは、

$$
I_{\mathrm{in}}=\frac{1\ \mathrm{V}}{50\ \Omega}=20\ \mathrm{mA},
\qquad
Q_{\mathrm{in}}=\int I_{\mathrm{in}}(t)\,dt=200\ \mathrm{pC}
$$

となります。

## ノードと時間関係

| 信号 | 1 nsより前 | 1--11 ns | 11 ns以後 |
|---|---:|---:|---:|
| `V(input)` | 0 V | 1 V | 0 V |
| `I(input)` | 0 mA | 20 mA | 0 mA |

抵抗だけの理想モデルなので、`V(input)`と`I(input)`の時間差、および正弦波入力時の位相差は0です。実回路では配線、入力容量、帯域による遅延が加わります。

## 実行方法

リポジトリのルートから実行します。

```bash
python circuits/01_input_50ohm/draw_01_input_50ohm.py
ngspice -b circuits/01_input_50ohm/01_input_50ohm.cir
```

回路図の基本的な生成処理は次の形です。

```python
drawing = schemdraw.Drawing(show=False)
drawing.config(unit=3, fontsize=12)

source = drawing.add(elm.SourcePulse().up().label("Vin(t)"))
drawing.add(elm.Line().right().at(source.end).length(4))
drawing.add(elm.Resistor().down().label("50 Ω"))
drawing.add(elm.Line().to(source.start))
drawing.add(elm.Ground().at(source.start))
```

SPICEモデルの主要部分は次のとおりです。

```spice
Vin input 0 PULSE(0 1 1n 1p 1p 10n 30n)
Rterm input 0 50
```

- `PULSE(0 1 1n 1p 1p 10n 30n)`：1 ns後に立ち上がる1 V、幅10 nsのパルス
- `Rterm input 0 50`：`input`とGND間の50 Ω終端
- `meas ... MAX ...`：指定時間内の最大電流
- `meas ... INTEG ...`：電流の時間積分から求める電荷
