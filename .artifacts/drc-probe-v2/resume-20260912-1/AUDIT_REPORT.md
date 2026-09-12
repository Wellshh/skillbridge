# DRC Probe v2 最终审计报告

状态：`INCOMPLETE / REJECTED`。本次任务包含早期 Stage 0 的三份 runtime 证据；Stage I runtime 从未启动，本轮代码审核拒绝后也未再启动 Allegro。当前仅归档审计结论，未杀进程。

## 已接受的离线证据

`B_GRID_EQ` 与 `B_STAIR_n6` 的原始日志几何、规则和 marker 已从 [probe_b.b9phteksv.log](D:/AutoPlacer/skillbridge/.artifacts/drc-probe/logs/probe_b.b9phteksv.log) 读取。GRID_EQ 的 Fraction 几何 clearance 是 `0.06`，旧 float GRID oracle 复现为 FLAGGED，差异约 `-2.0458e-14 mm`，属于旧 oracle false positive；STAIR_n6 的精确值是 `0.0599`，旧 float 与精确判断都 FLAGGED，污染不改变 verdict。旧 `model_GRID` 的 GRID_EQ FLAGGED 复现已由 [oracle_regression.py](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/oracle_regression.py) 断言，输出为 [oracle_regression.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/oracle_regression.json) 中的 `OFFLINE_REGRESSIONS_PASS`。

`C_CC_GOLD` 原始日志位于 [probe_c.run2-full-success.bvc57j0lt.log](D:/AutoPlacer/skillbridge/.artifacts/drc-probe/logs/probe_c.run2-full-success.bvc57j0lt.log)。日志中的 committed FULL clearance 为 `0.0599510038616914098241750252782367169857025146484375`，raw/BINARY64、GRID 记录均 FLAGGED，DRC marker 为 `Line to Line Spacing`，expected `0.06 MM`、actual `0.0599 MM`。当前离线工具只保留该值和 Decimal grid candidate 计算，尚未补 raw binary64 的 Fraction 重算与 C 的强断言；`source='prompt fixture'` 不能作为最终来源。

历史勘误完整保留如下：GRID_EQ 误差是约 `-2.0458e-14 mm`；STAIR_n6/n7 不是 float false-negative counterexample 而是两侧均 FLAGGED；B requery 只覆盖 5/19 arcs；C 原始 arc 数是 18；`2.5e-6 / 5.6e-14` 约 7.65 个数量级；旧 GRID oracle 经 float 往返污染了格点值；CC_GOLD 报告表格与 raw log verdict 冲突，raw log 优先；rp calibration 区间为 `(0.14994626897, 0.15004626893]` 且有 `rp∈gZ` prior；旧 ARC–Via 窗口没有区分 radial 与 vertical measurement；旧“axlAirGap 不可用”结论已被正式 API 和本地证据否定，仍需重新审计 mode/return payload。

## 运行身份和仓库状态

历史 Stage 0 目录对应三组不同 runtime 身份：`port=63705,pid=13076,board=drc-v2-s0-rjidbgo7`；`port=58193,pid=28164,board=drc-v2-s0-b9bmt3bv`；`port=51571,pid=51316,board=drc-v2-s0-egfo637d`。当前只读检查未发现这些 PID 存活，也未发现这些端口仍有 TCP listener；没有执行终止操作。cleanup raw machine transcript：`MISSING`；实际启动命令审计记录：`MISSING`，不能从目录名补写。

源板 hash（只读核验）：`allegrobridge/assets/route/EL5_MIAN_FPC.brd` SHA-256 = `2B919C474D7D8032A53AB36F5731F899D3AA24B7D8D2226B0E8AD3112D292F4C`。

`git rev-parse HEAD` = `57a4483a8c4ef5e680e857827eb9651418dc79ac`；`git status --short` 仅报告 `M batch_drc.log,2` 与 `M batch_drc.log,3`；`git diff --numstat` 和指定 diff 内容为空。该状态属于既有工作区状态，未修改。production diff：`EMPTY_NOT_MODIFIED`。这两份 tracked 日志来自本任务早期运行污染后的内容恢复；归档副本位于 [batch_drc.log,2.runtime-contamination](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/batch_drc.log,2.runtime-contamination) 与 [batch_drc.log,3.runtime-contamination](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/batch_drc.log,3.runtime-contamination)，不是用户既有改动。

`allegrobridge/_kernel/server/python_server.ils:186-207` 的当前 serializer 使用 `%.17g` 并补 `.0`；默认 `%L` 仅是历史风险。高精度 request→echo→committed→requery 合同仍待本任务真实链路验证。

## 各阶段状态

| 阶段 | 状态 | 证据或阻断 |
|---|---|---|
| Stage 0 | `FROZEN / CODE_REVIEW_REJECTED` | [stage0_ia.py](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage0_ia.py) 未建立有效 board/run/cleanup 证据；历史三组身份保留，不能汇总为通过。 |
| Stage I-A | `REJECTED / NOT RUN` | 旧草稿把仅 line/via 误标为 `line+via+arc_endpoint`，并错误写入 `COMPLETE`；该标签作废。new Stage I smoke 未 run，旧 line/via 采样也不构成有效 Stage I 通过证据。 |
| Stage I-B | `NOT IMPLEMENTED` | 正式 API 已确认 `axlPathGetPathSegs`、`axlPathGetLastPathSeg`、`axlPathSegGetEndPoint`、`axlPathSegGetArcCenter`、`axlPathSegGetArcClockwise`、width getter；没有完成实机边界实验。 |
| Stage I-C | `NOT STARTED / API LIMITED` | ArcCenter API 不适用独立 radius 变量；radius/angle 替代入口未测。 |
| Stage II-A | `NOT STARTED` | 未完成 finite complementary sweep。 |
| Stage II-B | `BLOCKED` | ARC–Via 仍缺独立 padstack 层形状尺寸证据，旧窗口模型不足。 |
| Stage II-C | `NOT STARTED` | 未完成固定 center 参数的 adaptive flip bracket 及重复验证。 |
| Stage II-D | `NOT STARTED` | 未完成竞争比较模型的 epsilon/quantization 辨识。 |
| Stage III-A | `NOT STARTED` | 未完成平移提交与 DRC 分离验证。 |
| Stage III-B | `NOT STARTED` | 未完成 marker 显示语义验证。 |
| Stage III-C | `NOT STARTED` | 未完成各域模型边界、optimizer、commit-emulator 前置总结。 |

## Stage I 代码复核结论

[stage1_smoke.py](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.py) 与 [stage1_smoke.il](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.il) 在本轮最终审核中为 `REJECTED`，且没有得到实机授权运行。确定缺陷如下：

1. request echo 不是 API 前精度链；当前 Python 只做 command substring 检查，未将 Python 输入 bits 与 same-RPC 返回 echo 数值闭环比较。
2. child 异常路径新建简化 error 对象，可能丢失已有 report 的 wire/committed/pid；cleanup 只是占位文本，未形成现场证据。
3. main 失败返回码与 manifest 状态不能作为完整三 case 成功门；固定 manifest 复用风险未消除。
4. bounds 只记录布尔值，未形成空区域选择和无旧对象干扰的有效门。
5. route width 匹配仍使用请求 width（stage1_smoke.py:241）；创建结果只取首 path/首 segment，未完整验证创建结果的唯一性。
6. `length17`（[stage1_smoke.il:28](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.il:28)，[stage1_smoke.py:90](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.py:90)） 只保存，未与 numeric committed 和独立 requery bits 互校；无法宣称全字段闭环。
7. [assessment_checks/exitcodes.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/assessment_checks/exitcodes.json) 曾记录 `verify_assessment=1, skill_lint=0, validate_skill_api=0`；之后单独 verify 输出曾为 0，不能把旧汇总文件改写成全绿，两个时间点必须分开审计。

关键缺陷定位：[request 构造及 substring 检查 stage1_smoke.py:151](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.py:151)；[child 异常处理 stage1_smoke.py:266](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.py:266)；[main 返回与 manifest stage1_smoke.py:295-299](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.py:295)；[WIDTH 请求匹配 stage1_smoke.py:241](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.py:241)；[length17 生成 stage1_smoke.il:28](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/stage1_smoke.il:28)；旧 model_GRID：[arc_oracle.py:112](D:/AutoPlacer/skillbridge/.artifacts/drc-probe/arc_oracle.py:112)，新回归入口：[oracle_regression.py:25](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/oracle_regression.py:25)；早期污染日志：[batch_drc.log,2](D:/AutoPlacer/skillbridge/batch_drc.log,2) 与 [batch_drc.log,3](D:/AutoPlacer/skillbridge/batch_drc.log,3)。行号按当前工作区文件读取，未执行 runtime。

当前 serializer 证据：[python_server.ils:186-207](D:/AutoPlacer/skillbridge/allegrobridge/_kernel/server/python_server.ils:186) 使用 `%.17g` 并补 `.0`；默认 `%L` 是历史路径，高精度合同仍未由本任务真实链路证明。

静态工具的最新实现输出分别保存在 [verify_assessment.stdout](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/assessment_checks/verify_assessment.stdout)、`skill_lint.stdout`、`validate_skill_api.stdout` 和 [implementation_exitcodes.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/assessment_checks/implementation_exitcodes.json)。这些只是静态门，不能替代 S048 runtime；SKILL lint/validate 没有证明创建、回读或 cleanup 成功。

## 下一步最小动作

先修证据链和失败状态：应分别校验两条相等边——Python 实际 wire 解码与 SKILL API 前 echo 相等；same-RPC committed 与独立 requery 相等，并对各自 17g 文本做 bits 互校。echo 到 committed 之间允许且正要研究 Allegro 的 quantization/canonicalization，必须记录差值，不能因 request 与 committed bits 不等就判失败。让异常 finally 保存完整 report、traceback、真实 PID 和 cleanup；使用不可覆盖的 run manifest，并在三 case 全部通过后才允许 PASS。随后由 root 审核代码，再以每 case 新 board copy、新 Allegro 进程和唯一端口进行一次三 case smoke。完成这些之前不扩矩阵、不运行 DRC、不推断生产规则，也不建议修改生产代码。








