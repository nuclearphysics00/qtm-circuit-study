# QTM circuit study

QTM（Charge to Time Converter Module）の資料を読みながら、回路を一段ずつPythonとSPICEで再構成するprojectです。

各段階を小さなGit差分として残します。

## Directory

```text
circuits/                 SPICE netlist。回路を一つずつ追加する
references/               参照資料の所在と読取り記録
src/qtm_circuit_study/    Python code
tests/                    式・netlist・simulation結果のtest
outputs/                  SVG、CSV、PNGなどの生成物（Git対象外）
```

## 環境構築

Python 3.12とngspiceを使用します。

```bash
cd $HOME/fumiya/56_project/qtm-circuit-study
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 環境の読み込み

作業を始めるたびに、repositoryへ移動して仮想環境を読み込みます。

```bash
cd $HOME/fumiya/56_project/qtm-circuit-study
source .venv/bin/activate

export SPICE_LIB_DIR=/opt/homebrew/opt/ngspice/share/ngspice
export XDG_DATA_HOME="$PWD/.cache/xdg"
export XDG_CACHE_HOME="$PWD/.cache"
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
```

確認：

```bash
python --version
ngspice --version
pytest --version
```

終了するときは次を実行します。

```bash
deactivate
```
