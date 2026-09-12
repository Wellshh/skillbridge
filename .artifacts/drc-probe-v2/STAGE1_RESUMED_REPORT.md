# Stage 1 Resumed Offline Analysis

状态：`INCOMPLETE_DERIVED_ANALYSIS`。本文只描述已保存数据的离线派生分析，不表示 Stage II/III 或整项研究完成。

## 输入与执行

分析读取以下既有 JSONL：I-A `ia-quantizer-60/run-64000-1789189177779421800`（60 条）与 `ia-scalar-120/run-51340-1789190383784285200`（120 条）；I-B center-40 与 alpha-36（合计 76 条）；save-reopen-4（4 条）。最新执行源码与输出位于 [subrun-20260912-8](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-analysis/subrun-20260912-8)，执行 exit 0，stdout/stderr 已保存。

## I-A Q 分析

实际共 180 条，六角色各 30 条：`line_x`、`line_y`、`via_x`、`via_y`、`arc_x`、`arc_y`。所有候选均以 transaction request echo 的实际 binary64 `h` 为输入，不以 intended H 替代。

- RAW：`Fraction.from_float(h) / Fraction(1,10000)`。
- MUL：`Fraction.from_float(h*10000)`。
- DIV：`Fraction.from_float(h/float(g))`，其中 `g=0.0001`。
- 八个 mode 为 floor、ceil、toward-zero、nearest ties-even、nearest ties-away-zero、nearest ties-toward-zero、ties +inf、ties -inf。

每个未存活候选保留首个反例、H、实际 echo、observed committed、predicted value 及 bits；未按预期 survivor 调整数据。机器结果包含 combined 与 `ia_by_role` 独立结果。

## I-B 几何派生

C0 唯一来自 request preEcho 的 center x17/y17；C_db 独立来自 committed center。使用 `S/E/C0` 的 exact Fraction 计算垂足 `P(C0)`；端点半径和 mean radius 由 C0 计算。recenter 候选使用 Decimal precision 100 的平方根，并保存 `meanR−exportedR`、`C_db−C0`、`P(C0)−C_db` 及 `C_db−recenter` 字符串残差。结果是描述性几何证据，不宣称正交投影或内部 canonicalization 公式。

76/76 样本的 alpha/beta 非空，`r_end` 均为 numeric；I-B 输出按实际 input intent/H tuple 来源记录系数。

## Save/reopen

4/4 条记录通过显式字段检查：save fresh requery count=1、reopen target match count=1、两侧 stable 状态一致、process poll=1。该证据支持保存后 fresh requery 与新 session 对象稳定，不证明 Allegro 内部存储语义。

限制：这些分析不调用 DRC，不能归因 DRC comparator；Decimal-100 只用于高精度派生显示，不能替代底层 exact API 语义。历史 run 的 wrapper/stdout/helper/reset fingerprint 缺口仍按原始 manifest 保留。

机器结果见 [stage1_analysis.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_analysis.json)。
