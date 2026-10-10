# Reference register

参照資料の原本は別projectに保持し、このrepositoryへ無断で複製しません。manual記載値はhistorical specificationとして扱い、E609実機の現行設定値とは区別します。

## Local sources

- `/Users/furukawafumiya/fumiya/61_book_git/mimir/experiments/e609/ref2-QTM_Manual20100601B.pdf`
  - QTM model TT1 manual, Version 1.0, document date 2020-05-27, 25 pages.
  - QTM architecture、attenuator、QTC、CAL、HIT、OTR、USB/EEPROM、signal I/O、specificationsを収録。
- `/Users/furukawafumiya/fumiya/61_book_git/mimir/build/experiments/e609-operations/materials/HISTORICAL-QTC-ASIC-NIM-A610-2009.pdf`
  - Iwatsu CLC101 QTC ASICの原理と性能を扱う論文。
- `/Users/furukawafumiya/fumiya/61_book_git/mimir/build/experiments/e609-operations/materials/HISTORICAL-QTM-TT2-manual-2012.pdf`
  - QTM TT2 v1.1とされるhistorical manual。本文のTT1表記など不整合あり。

## Evidence rule

- manualで確認できるblock、signal、nominal specificationと、学習用modelの仮定を分ける。
- 回路図にない抵抗・capacitor・電流値は教育用parameterとして明記する。
- simulation一致を実機動作確認として扱わない。
