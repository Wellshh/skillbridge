# II-D 边界数值分析

boundary 11 点 FULL：FLAGGED 最大=2161720911343669/36028797018963968；CLEAN 最小=2161724363541365/36028797018963968；按请求 Cy 单调=True。
repeat 10 点 FULL 按请求 Cy 单调=True；LO 5/5 FLAGGED、HI 5/5 CLEAN。

API_R=1080863910568919/18014398509481984；名义值=3/50。CENTER_FROM_START、CENTER_FROM_END、GRID_NORMALIZED 均独立计算并在 JSON 中逐点列出。

M0 被有效 CLEAN 反驳；M1 仅条件兼容 ε∈[9.596758035e-8,1.917853145e-7)，上界严格小于；M2 被 HI 反驳；M3/M4 不可唯一辨识。100 位 Decimal sqrt 仅显示近似。

审计复核：见 [analysis-v5.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary/analysis-v5/analysis-v5.json) 与 [gate audit](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary/gate-reaudit/audit.json)。21 case gate 重算与 raw verdict 一致；GRID 模型为 NON_SEPARATING。API_R 与 nominal 分离，M0-M4 仅作条件性模型判断，未证明内部 epsilon。

