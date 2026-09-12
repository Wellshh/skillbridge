# 最终实验审计（2026-09-12）

## 结论先行

本轮证据不能支持“统一 round4 或一个 grid 容差即可无损重建”的结论。实际链路至少包含 Python binary64 wire、SKILL API 前 echo、创建后 committed 值和独立 requery 四个观测边界；其中应相等的是 Python 实际 wire 解码与 API 前 echo，以及同一事务 committed 与独立 requery 的对应字段 bits。echo 到 committed 允许量化或 canonicalization，且正是本实验要辨识的差异。

在已完成的 IA180 中，实际域内唯一存活的解释是 `MUL10000_B64 + nearest ties-even`；这是一组观测域的候选筛选结果，不是 Allegro 内部统一规则的证明。I-B 的 off-grid 结果也显示，提交半径与请求几何的差异约为 `1.39e-5..2.63e-5 mm`，而以实际 committed 端点计算的 endpoint-mean 残差约为 `5e-14 mm` 量级；后者不是严格零，不能包装成内部 mean-radius 算法已被证明。

生产代码没有修改。实验只使用 disposable board copy、owned Allegro 进程和独立端口；未写入用户原板、用户 session、memory 或 commit。`git diff` 当前为空；工作区的两个 tracked `batch_drc.log,*` 状态来自本任务早期运行污染后的恢复状态，单独保留 status 与 diff 的区别。

## 证据索引

|阶段|实际证据|状态与边界|
|---|---|---|
|Stage 0|[run-37248 manifest](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage0-gate/run-37248-1789193361092813400/manifest.json)|已接受的 gate/capture；不等于完整 effective-rule resolver。|
|I-A|[IA quantizer run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/ia-quantizer-60/run-64000-1789189177779421800)、[IA scalar run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/ia-scalar-120/run-51340-1789190383784285200)|180 个样本、6 roles 各 30；候选筛选结果为 MUL10000_B64 + nearest ties-even。|
|I-B center|[IB center run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/ib-center-40/run-66284-1789189802536493400)、[IB alpha run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/ib-alpha-36/run-11788-1789189996641797000)|40 beta 与 36 alpha 样本；tiny beta 有 16 个 center 变化，alpha36 中数学 beta=0 仍有 6 个实际 wire center 变化，不能硬归类为“保持”。|
|I-B off-grid|[off-grid raw run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-offgrid-order/run-20260912-231222-629)、[v2 analysis](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-offgrid-order-analysis-v2/analysis.json)|16/16 reset fingerprint 一致；prePath end/center 与请求 bits 一致，committed 端点经量化。|
|save|[save/reopen-4 history](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/save-reopen-4)、[beta capture/save run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-beta-replay-v2/run-83092-1789228648195193500)、[beta reopen run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage1-beta-reopen/run-52936-1789229074638350500)|save 同 session 的 minus/plus 四对象唯一回读且 DTO bits 稳定；beta 新 session reopen 已独立 gate 通过，PID 48424/76748、均 `poll=1`，saved source/copy hash 匹配，4 DTO 与 save-after 完全相等。|
|II-A|[sweep run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-sweep/run-54268-1789223811387679300)、[diag run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-sweep-diag/run-63160-1789225091207869200)|已接受 finite sweep 的 F/C/C/F；重复 marker、stale/null snapshot 原样保留，但其原因尚未证明。|
|II-C|[11-search raw](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary)、[10-repeat raw](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary-repeat)|固定 center 参数的 11-search 与 10-repeat、δ 数值和目标重复已通过独立审计；不把它提升为内部 comparator epsilon 上界。|
|II-D|[math v5 analysis](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary/analysis-v5/analysis-v5.json)|数学 v5 与 21 case gate/repeat 已接受；FULL δ 区间和 GRID `NON_SEPARATING` 已复算。条件区间是实验模型约束，不代表内部 epsilon。|
|II-B pad|[pad probe](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-pad-probe/run-20260912-222619-975)|VIA_ALL_0103 TOP regular 为 CIRCLE，local bbox ±0.15、offset 0；figureSize 未当作回读字段，`radius` 未当作 circle 半径。|
|II-B radial|[radial raw](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-radial/run-20260912-224358-093)、[v4 analysis](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-radial-analysis-v4/analysis.json)|四 case 实际目标 pair F/F/C/C；B64 radial gap 约 0.04/0.20，排除 vertical-at-x 与 vertical-extremum 两模型。自动 matcher 仅辅助筛选，完整有效性依 root 独立审计。|
|III translation|[translation run](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage3-translation/run-29568-1789228092086311600)|9 gates（6 FLAGGED、3 CLEAN）已接受；9 个 owned PID 均 `poll=1`，记录 raw geometry 差异，不外推为固定点重导入无损。|

## 已核实的数值与模型

IA 使用实际 preEcho wire 的 binary64 展开：`RAW = Fraction.from_float(h)/g`，`MUL10000_B64` 先对 `float(preEcho)*10000` 再做候选舍入，`DIV_B64` 使用真实 float 除法后展开。输入不是理想数学 H。对六种角色（line endpoint X/Y、via X/Y、arc endpoint X/Y）分别统计，180 样本均只有 MUL10000_B64 与 nearest ties-even 存活；该结果只描述当前 accuracy=4 的观测域。

I-B center 分析从 preEcho C0、实际 S/E 和 committed Cdb 分开计算。tiny beta 的 16 个样本可由 mean-radius preserving 重构解释，但不证明正交投影；big beta 保留 non-bisector center。alpha36 中 6 个数学 beta=0 样本仍出现 `4.263e-14` 或 `5.684e-14` 级 center 变化，说明数学 beta=0 不等于实际 wire 完全 bisector。

II-D 的早期派生脚本 v1/v2/v3/v4 均不采用，不能引用其中的 PASS 字段；其中曾有 GRID float 污染、CENTER 未减规则 R 以及词法 min/max 问题。现以 [math v5 analysis](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary/analysis-v5/analysis-v5.json) 和 root 已通过的 21 条 gate/repeat 为准：`FULL LOδ=-6909794169/36028797018963968`、`HIδ=-3457596473/36028797018963968`；11 条 search 与 10 条 repeat 的 GRID clearance 均为 `3/50 mm = 0.06 mm`，因此 GRID 是 `NON_SEPARATING`。M1 条件区间约为 `[9.596758035e-8,1.917853145e-7)`，这是该实验模型的条件约束，不能称 Allegro 内部 epsilon。

off-grid 16 个样本固定 S=(-620,-70)，四方向和两尺度各扫正负端点偏移。实际 lonely arc 的 net 为 nil；查询使用实际 DTO，未回填请求 net。`Rdb-R_REQUEST_MEAN` 的绝对差为约 `1.39e-5..2.63e-5 mm`，`Rdb-R_Q_ENDPOINT_MEAN` 约 `-5.1720e-14..+4.2941e-14 mm`。这些是有限精度观察，不是严格等式。

beta replay 的 minus/plus/positive 三 case 已由独立审计复核：minus、plus 均为 CLEAN，positive 为 FLAGGED；六组 gate 均分别为 0、0、1。minus/plus 四对象 DTO 完全相同，save hash 与实读一致，保存前后所有字段相同。owned 进程 PID 为 60124、4284、22264，均 `poll=1`。这只说明在本已测域中 beta 请求没有额外改变判决，不证明隐藏状态永不参与。

pad/radial 证据使用实际 pad DB 字段和 polygon 投影。pad 的 CIRCLE bbox 半径为 0.15 B64；global bbox 半宽与 local radius 相减得到约 `-2.273e-14 mm`，这是两个导出表示的浮点差异，不能称 pad 变形。radial 的完整 B64 模型必须使用 committed arc center/radius/width、actual via 坐标和 pad bbox；名义值 `.15/.065` 只作为 API nominal 对照。

历史离线 oracle 已纠正并并列保留两种模型：B/C 的 `ALL_B64_WIDTH`（几何、线宽、弧宽均取 raw binary64）与 `B64_GEOMETRY_IDEAL_WIDTH`（几何取 B64、宽度取理想 `.15`）。`3/20 - Fraction.from_float(.15) = 1/180143985094819840`，该正差是 binary64 宽度与理想 `.15` 的差，不是 Decimal 舍入。grid-normalized 展示值为 `.06/.0599/.06`，不能替代 raw 运算。

## API/规则边界

`axlCNSGetSpacing` 可读 cset/layer 的 numeric 与 text 值，`axlCNSSpacingModeGet('all)` 可读 board-wide mode；已查入口还包括 design nets、class/classTable、region、properties 与 csets。当前没有发现可独立读取完整 net/class/region 优先级并返回最终 effective comparator 的 resolver，因此 spacing 值只能表述 API 暴露值及其条件上下文，不能冒充有效规则解析。API_R 的 line-line 二进制对照为 `0.06 mm`，via-line nominal 对照为 `0.065 mm`，实验域为 accuracy=4 的 mm 设计；二者不同，nominal 值不等于隐藏 comparator 的 exact 内部值。

DRC marker 的正式字段和本轮 raw 观察分开记录。实际 marker 的 `t`/类型不能单独解释为“已修复完成”；必须同时保存 `violations` figure 数、waived/fixed 字段、marker count、name、figure pair 和 before/after snapshot，不能仅按 marker name 去重。旧资料中任何把 fixed 字段直接等同于修复完成的说法均不纳入结论。

## 已作废或失败的材料

`results/stage0_ia.json` 首部历史 `status=COMPLETE`、`phase=stage0+I-A` 及 `arc_endpoint` 标签作废，不聚合为通过；其旧标签把仅 line+via 误标为含 arc endpoint。早期 `run-46808-pending`（port 58193, pid 28164, board `drc-v2-s0-b9bmt3bv`）与 `run-64320-51571`（port 51571, pid 51316, board `drc-v2-s0-egfo637d`）以及 `stage0_ia`（port 63705, pid 13076, board `drc-v2-s0-rjidbgo7`）是三组不同运行身份，不能按目录数说成两次。

历史 beta 失败包括 wire 将 `-620.0` 拼成 SKILL 整数、错误 helper 的 `(+ ...)` 浮点转换、创建后才生成 request echo、异常分支丢失 child report、固定 manifest 覆盖、父进程错误返回 0、bounds 只有布尔值、route/via 以 requested 而非 committed 匹配、只取首 path/segment、length17 未互校、完整 sklint 因缺 `cdsFuncs.cxt` 不可用等。当前 beta 三 case 的 capture/save run 已保留原始 stdout/stderr；这些历史失败不被覆盖成成功。

## 模型辨识结果与剩余限制

|模型|结果|
|---|---|
|M0 `d<R`|被 CLEAN 观察反驳。|
|M1 `d<R-epsilon`|可在实验样本拟合；条件 epsilon 区间约 `[9.596758035e-8,1.917853145e-7)`。|
|M2 `d<R+epsilon`|正 epsilon 版本被反驳。|
|M3 量化归一化|更细测距量化/归一化仍未被唯一排除；本次统一 round4 GRID 被 F/C 同值反驳。|
|M4 字段/规则语义|尚未唯一辨识；marker 字段、effective rule 优先级和隐藏状态仍需上下文。|

FULL δ 区间宽为 `9.581773419e-8`；CENTER 两端约为 `-1.91785300285419063238e-7` 与 `-9.59675663518067567513e-8`。这些数值是实验模型边界，不能当作内部 epsilon 的直接测量。

I-C 中 ArcCenter 不适用独立 radius 变量，已如实标记 N/A；这不是阻断全部实验的未测替代入口。II-D 数学 v5 与 gate/repeat 已通过，但其 epsilon 仍只是条件模型区间。beta 新 session reopen 已通过受控 gate。II-A 的 finite F/C/C/F 已接受，重复 marker/stale/null 的原因仍未证明。III-A 平移提交与 DRC 分离已形成观测。III-B 的 STAIR_n6 FULL floor clearance 为 `0.0598`，marker 为 `0.0599`；对正数而言 floor 与向零在该样本不可区分。III-C 中 lambda 只适用于已验证 S/E/sweep 的局部优化：固定 S/E 时若 `C=M+λp`、`p=(-vy,vx)`、`v=E-S`，λ 无量纲，圆心位移为 `|Δλ|·|v|`；每个候选仍需 DB 回读和 DRC，不能把全部值 round4。commit emulator 只能覆盖有限构造域；radius 修正的多模型和 DRC 偏移尚未唯一辨识，因此外部 CLEAN 不作为放行依据。外部 create 后重新导入的 fixed-point 与无损性尚未证明。

后续可做的最小实验是：对已导出的实际 S/E/C 按同一正式 API 重新 create，再 fresh 查询全字段 fixed-point 和 DRC 差分；本轮不执行。完整 `checkPubFuncs`/full sklint 仍受 Windows 环境缺失 context 限制，不能用普通 lint 冒充完整 lint。

历史勘误保留如下：B 原始只回查 5/19 arcs，C 原始为 18 arcs；B_GRID 浮点往返误差为约 `-2.0458e-14`；STAIR_n6/n7 不能称 false-negative；CC_GOLD 旧表写 CLEAN，但 raw marker 为 FLAGGED，以 raw 为准；`2.5e-6/5.6e-14≈4.46e7`，即 7.65 个数量级；旧 “axlAirGap 不可用” 结论已被正确原生调用反证，但 AirGap 不等同中心线距离。CLI 的未加引号参数会少位，字符串化修复已归档于 [quoted.txt](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage3-translation-cli/quoted.txt) 与 [quoted-explicit.txt](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage3-translation-cli/quoted-explicit.txt)。III 使用完整 [run-29568](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage3-translation/run-29568-1789228092086311600)，不是被截断的旧 run-73932。

## 环境与可复算元数据

- HEAD：`57a4483a8c4ef5e680e857827eb9651418dc79ac`
- 源板 hash：`2b919c474d7d8032a53ab36f5731f899d3aa24b7d8d2226b0e8ad3112d292f4c`。
- Allegro：Cadence 17.2-2016 S048；设计单位 mm；accuracy=4。
- 当前 serializer：[python_server.ils](D:/AutoPlacer/skillbridge/allegrobridge/_kernel/server/python_server.ils) 186-207 使用 `%.17g` 并为无小数点文本补 `.0`；默认 `%L` 是历史问题。高精度合同仍以真实 wire/echo/committed/requery 链验证。
- 每个 run 的脚本快照、argv、cwd、stdout/stderr、端口和 owned process 记录应以对应目录为准；缺少的原始 machine transcript 仍标 `MISSING`，不补写想象命令。
- 归档索引：[RUN_INDEX.md](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/RUN_INDEX.md)、[ENV_SNAPSHOT.txt](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/ENV_SNAPSHOT.txt)、[Stage0 gate audit](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage0-gate/run-37248-1789193361092813400/audit.json)、[II-C/D gate audit](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-boundary/gate-reaudit/audit.json)、[III v2 analysis](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage3-translation-analysis/stage3_translation_analysis_v2.json)。

总状态：计划内实机取证完成；尚未证明唯一内部模型或无损重导入；完整 Windows lint 未完成。上述限制不否定已接受的实机阶段结果。本报告替代旧 [AUDIT_REPORT.md](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/AUDIT_REPORT.md) 的进度结论；旧文件保留作历史归档。
