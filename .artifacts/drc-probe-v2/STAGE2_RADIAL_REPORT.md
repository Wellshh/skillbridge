# Stage II-B radial probe offline analysis

本报告只派生自已接受的实机 raw manifest，未修改 raw run，也未重新启动 Allegro。输入为 [run manifest](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-radial/run-20260912-224358-093/manifest.json)，计算结果见 [analysis.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-radial-analysis-v4/analysis.json)。

四个 case 均为 `C=(300,400), S=(310,400), E=(300,410), CCW, R=10, W=.15` 的 quarter arc。target via 使用实际回读位置重新取 pad 和 DRC item。Pad 实测为 `CIRCLE`，局部 bbox 为 `[-.15,.15]²`，offset 为 `(0,0)`。

分析先将 wire 的 binary64 值转为 `Fraction.from_float`，再在 Decimal precision 100 下计算：

`radial_gap = hypot(V-C) - 10 - .15 - .075`。

同时计算 vertical-at-x 模型和 vertical-extremum 模型。实际 radial gap 为约 `.039999999999986365906146...`（两例）和 `.199999999999977270959128...`（两例）。实测 DRC arc/target-via pattern 为：`.04` 两例均 flagged，`.20` 两例均 clean。

因此本次 raw 证据与 radial finite geometry 一致，并排除两种 vertical 替代模型：`.04` 样本中 vertical-at-x 预测 clean，而实测 flagged；`.20` 样本中 vertical-extremum 预测 flagged，而实测 clean。marker 原文、count、bits 和 Decimal100 派生值均保存在 JSON；重复 marker 未去重。

这只证明本次受控几何下的行为模式，不单独证明内部 comparator 的完整实现或 epsilon 上界。
