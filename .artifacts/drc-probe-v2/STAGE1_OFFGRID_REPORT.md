# Stage I-B off-grid ordering analysis

派生自已完成的 [16-case raw manifest](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-offgrid-order/run-20260912-231222-629/manifest.json)，结果见 [analysis.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-offgrid-order-analysis/analysis.json)。未修改 raw。

每个样本分别保存 request、pre-path、committed、requery。分析严格从实际 wire/DTO 读取 binary64，先转换为 `Fraction.from_float`，平方根在 Decimal precision 100 下计算并标明近似。

`R_REQUEST_MEAN` 使用 request 的 S/C/E；`R_Q_ENDPOINT_MEAN` 使用回读端点与 request center；`P_Q(Creq)` 使用实际回读端点投影 request center；另计算 DB endpoint/center 的均值半径与 center recenter 候选。request→committed 的差异允许存在并原样记录；committed→requery 的字段 bits 是一致性边。

16 个样本均 PASS，reset fingerprint 16/16 恢复；实际 lonely arc net 为 nil，没有请求 net fallback。该结果可区分 endpoint quantization 与 center/radius 候选，不能单独证明内部精确算法。
