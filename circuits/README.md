# circuits

QTM（Charge to Time Converter Module）の動作を、機能ブロックごとに分けて確認します。各ディレクトリのREADMEに、回路または機能モデル、タイミングチャート、数式、実行方法をまとめています。

## 構成

| 番号 | 内容 | 説明 |
|---|---|---|
| 01 | [50 Ω入力回路](01_input_50ohm/README.md) | 入力電圧、入力電流、入力電荷の関係 |
| 02 | [50 Ωインピーダンス整合](02_impedance_matching/README.md) | 信号源、伝送線路、負荷と反射係数 |
| 03 | [電荷積分回路](03_integrator/README.md) | 入力電流から蓄積電荷と積分電圧への変換 |
| 04 | [定電流放電](04_discharge/README.md) | 電荷を一定電流で放電時間へ変換する過程 |
| 05 | [しきい値比較器](05_comparator/README.md) | 積分電圧のしきい値通過と論理出力 |
| 06 | [QTC機能モデル](06_qtc_behavioral/README.md) | 各機能ブロックを接続した過渡応答 |
| 07 | [RC積分回路](07_rc_integrator/README.md) | 電圧波形の積分と位相遅れ |
| 08 | [RC微分回路](08_rc_differentiator/README.md) | 電圧波形の微分と位相進み |

## 波形の読み方

- `V(node)`：ノード`node`のGNDに対する電位
- `I(element)`：素子`element`を流れる枝電流
- `Q(Cint)`：積分コンデンサに蓄積された電荷

矩形パルスには単一の周波数がないため、過渡応答では「位相差」よりも、立ち上がり、しきい値通過、ゲート切り替えの**時間差**を確認します。正弦波に対する位相関係は、該当する回路のREADMEで別に説明します。

## 一括確認

リポジトリのルートから実行します。

```bash
source .venv/bin/activate

python circuits/01_input_50ohm/draw_01_input_50ohm.py
python circuits/02_impedance_matching/draw_02_impedance_matching.py
python circuits/02_impedance_matching/plot_02_impedance_matching.py
python circuits/03_integrator/draw_03_integrator_only.py
python circuits/03_integrator/plot_03_integrator.py
python circuits/04_discharge/draw_04_discharge.py
python circuits/04_discharge/plot_04_discharge.py
python circuits/05_comparator/draw_05_comparator.py
python circuits/05_comparator/plot_05_comparator.py
python circuits/06_qtc_behavioral/draw_06_qtc_behavioral.py
python circuits/06_qtc_behavioral/plot_06_qtc_simulation.py
python circuits/07_rc_integrator/draw_07_rc_integrator.py
python circuits/07_rc_integrator/plot_07_rc_integrator.py
python circuits/08_rc_differentiator/draw_08_rc_differentiator.py
python circuits/08_rc_differentiator/plot_08_rc_differentiator.py

pytest -q
```

個々のSPICEモデルと生成物については、各ディレクトリのREADMEを参照してください。
