# Windows 交叉验证与后续优化交付手册

> 交付日期：2026-09-08 · 适用仓库：`RAG_SKILL_AGENT/.claude/`（extract 版）+ 上游完整仓库（含 `.agents/`、`docs/html/`）+ `skillbridge`（Windows Allegro 测试环境）
>
> 目标：把在 macOS 上离线建成、**从未在真实 SKILL 环境验证过**的五层质量栈（校验器 / 语义检索 / 评估门 / 生成评测 / LSP）拿到 Windows Allegro 17.2 上做交叉验证，并根据实测结果继续优化。

## 2026-09-10 Windows 迭代记录

本轮已将本交付物中的 Cadence 共享内容提升到 `.agents/skills/cadence-skill-agent`，并由规范源重新生成 `.claude` 副本；Claude 独有的 memory、OrCAD 语料、OrCAD 索引脚本和本手册保留在 `.claude`。

- 真实环境确认：`D:\Cadence\Cadence_SPB_17.2-2016\tools\bin\allegro.exe`，目标 Allegro 17.2-2016 S048；`tests/allegrobridge/test_integration.py --allegro -q` 通过 134 项。
- 阶段 A 批次 1 已归档到 `.artifacts/iscalable-matrix-17.2-S048.json`：12 个缺口全部完成 `isCallable/arglist` 实测；9 个可调用、3 个不可调用。
- 阶段 A 批次 2 已归档到 `.artifacts/iscalable-matrix-17.2-S048-full.json`：1417 个索引行、1411 个大小写不敏感唯一条目、1408 个可探测符号；1396 个可调用、12 个不可调用，所有可调用条目均有 `arglist` 返回。
- 已新增 24 条 S048 `verified_facts`（总计 31 条，其中 26 条 verified），并将明确 `isCallable=true` 的平台扩展接入 validator/LSP；validator 官方样例 unknown-api 从 35 降至 7，剩余均对应真实不可调用条目。
- LSP 真实 stdio 闭环通过：已验证扩展无诊断、编造 API 报 `unknown-api`、`didChange` 刷新、`didClose` 清空、hover 和 completion 返回真实语料结果。
- 阶段 B 三个种子脚本已逐个通过真实 Allegrobridge session：每个使用新 Allegro 进程、唯一端口和 disposable board，均 `load=True`；`report-net-name` 的 `'net` 类型参数和事务 wrapper 的 `funcall(thunk)` 调用已根据 S048 真机错误修正，commit 返回 `t`、rollback 返回 `nil`。
- 本机 Claude CLI 的真实生成会话尚未计入阶段 B：默认模型路由到不可用的 `deepseek-v4-flash-260731`，显式 `sonnet` 也被改写为不可用的 `qwen3.8-flash-next`；未将该失败伪装为 agent 评测结果。
- 离线门禁：Claude 副本 255 tests、`.agents` 副本 244 tests 通过；检索/生成/事实/签名/OrCAD 门禁通过。PDF 转换 `--check` 仍受当前机器缺少 `pdftotext` 限制，未将其结果冒充通过。

尚未完成的交付项：阶段 B 的 3 个独立真实 agent 会话及扩展到 10 个样本、阶段 C 的真实编辑器接入/大文件延迟测量，以及完整语料与真实 `arglist` 参数数量的逐条人工裁决。当前结果已足以作为下一轮迭代基线。

---

## 0. 现状快照（离开 macOS 时的状态）

全部离线门禁绿灯，241 个单测通过（5 个 `test_sync_claude.py` 失败是 extract 仓库缺上游 `.agents/` 的预期行为）：

| 层 | 脚本 | 基线文件 | 当前基线值 |
|---|---|---|---|
| 语料校验（生成后） | `validate_skill_api.py` | `validate_skill_api_baseline.json` | 137 官方示例中 7 文件有 error；35 errors 全部为语料真实缺失（见 §3.2 名单）；校验器逻辑误报 = 0 |
| 评估门（生成前） | `verify_assessment.py` | —（无基线，逐次判定） | 冒烟通过：能拦编造 API 并给真实候选 |
| 语义检索 | `search_api.py` + `eval_retrieval.py` | `eval_retrieval_baseline.json` | 32 用例：top1=0.5625 / mrr=0.6500 / recall@5=0.8125；3 条 MISS 为已登记 frontier case |
| 生成质量 | `eval_generation.py` | `eval_generation_baseline.json` | `.claude/eval-samples/` 3 个种子样例全净（hallucination_rate=0） |
| 经验库增长门 | `validate_facts.py --check` | `verified_facts_baseline.json` | 7 条事实（2 verified），总数/verified 数只许增长 |
| 编辑器 LSP | `skill_lsp.py` | —（23 个协议单测） | stdio 冒烟通过；**真实环境交叉验证 = 本手册主题** |

语料规模：`api_index.part*.md` 795 行（axl）+ `sklang_api_index.part*.md` 622 行 = 1411 个唯一符号；OrCAD 侧 `orcadcapture/api_index.part01–15.md` 4569 行（`build_orcad_index.py` 生成）。

**尚未验证的核心假设**：语料签名与 Windows Allegro 17.2 S048 的真实行为一致；unknown-api 的判定不会把真实存在的 Allegro 扩展误杀（已知 10 个真实 API 缺失，见下）。

---

## 1. 转运清单（macOS → Windows）

需要带到 Windows 机的东西：

1. **本 extract 仓库整个 `.claude/` 目录**（scripts / tests / skill-references / eval-samples / agents / agent-memory）。全部是纯文本 + Python，无二进制依赖。
2. **上游完整仓库**（有 `.agents/`、`docs/html/algroskill/`、CI 的那个）——语料若需扩充要从 CHM 源头走转换器，且 `sync_claude.py` 只在上游布局下工作。
3. **`skillbridge` 仓库**：Windows Allegro 测试环境所在（`allegrobridge`、`tests/allegrobridge/`、`benchmark/`）。交叉验证的 SKILL 执行通道用它。
4. Python 3.10+（离线栈只需要标准库，无第三方依赖；skillbridge 侧按其 `pyproject.toml` 装）。

转运后第一件事——确认离线栈在 Windows 上原样通过（这一步只验证转运没坏东西，不需要 Allegro）：

```powershell
cd <repo>\.claude
python -m pytest tests -q          # 预期 241 passed + 5 个 test_sync_claude 失败（extract 仓库预期）
python scripts\validate_skill_api.py --check
python scripts\eval_retrieval.py --check
python scripts\eval_generation.py --samples eval-samples --check
python scripts\validate_facts.py --check
python scripts\build_orcad_index.py --check
python scripts\check_signatures.py
```

若路径分隔符或编码在 Windows 上引发失败，那本身就是第一个要修的 bug（所有脚本都用 `pathlib`，理论上无碍；读文件均显式 `encoding="utf-8"`）。

---

## 2. Windows 环境启动（skillbridge 约定）

以下约定来自 `skillbridge/benchmark/README.md` 与 agent runbook，照抄即可：

```powershell
$env:Sigrity_EDA_DIR = 'D:\Cadence\Cadence_SPB_17.2-2016'
$env:CDS_LIC_FILE = [Environment]::GetEnvironmentVariable('CDS_LIC_FILE', 'User')
# 先确认既有集成套件是绿的，再开始交叉验证
.venv\Scripts\python.exe -m pytest tests/allegrobridge/test_integration.py --allegro -q
```

执行纪律（runbook 已有，交叉验证同样适用）：

- `Allegro.open(mode="cli")`、**唯一数字 TCP 端口**、**测试 board 副本**（不用生产 board）。
- Python 传给 SKILL 的路径一律 `Path.resolve().as_posix()`。
- 装载用 `load` 不用 `loadi`（后者吞错误）。
- 每轮验证用新 Allegro 进程 + 新 board 副本；环境启动类失败可重试 1 次，`KeyboardInterrupt` 与意外 Python 错误必须上抛。
- 并发跑时串行化或分配独立端口。

---

## 3. 阶段 A：isCallable / arglist 交叉验证（最高优先级）

这是"真实权威"对离线栈的第一次对账。分两个批次。

### 3.1 探针脚本

把下面的 SKILL 存为 `probe_iscalable.il`（在 Allegro SKILL 控制台 `load` 或经 allegrobridge 执行）。先小样本试跑确认 `arglist` 用法，再放全量：

```skill
; probe_iscalable.il — 批量探测符号在真实 Allegro 中的可调用性与参数表
; 输入: 每行一个符号名的文本文件; 输出: 每行一条 JSON 的文本文件
procedure( axlProbeIsCallable(t_inFile t_outFile)
    let((inPort outPort name result callable args)
        inPort = infile(t_inFile)
        outPort = outfile(t_outFile)
        when( inPort && outPort
            while( gets(line inPort)
                name = pcreReplace(pcreCompile("[\\r\\n\\s]+$") line "" 0)
                when( name != ""
                    callable = isCallable(name)
                    args = ""
                    when( callable
                        ; arglist 的入参形态 (函数值 or 符号名) 以实测为准, 见 §3.2 步骤 1
                        args = sprintf(nil "%L" arglist(evalstring(name)))
                    )
                    result = sprintf(nil "{\"name\": \"%s\", \"callable\": %s, \"arglist\": %s}"
                        name
                        if(callable then "true" else "false")
                        if(args == "" then "null" else sprintf(nil "\"%s\"" pcreReplace(pcreCompile("\"") args "\\\\"" 0)))
                    )
                    fprintf(outPort "%s\n" result)
                )
            )
            close(inPort)
            close(outPort)
            t
        )
    )
)
```

> 注意：这段探针本身**没过真实 Allegro**（这正是本阶段要解决的鸡生蛋问题）。`isCallable`/`arglist`/`pcreReplace` 的准确用法先在小样本上人工核对一次，跑通后再批量化。`arglist` 对某些 builtin 可能报错——用 `errset` 包一层兜底，把异常也记成 JSON 字段。

### 3.2 批次 1：已知语料缺口（12 个名字，5 分钟）

`validate_skill_api.py --self-test` 的 35 个 unknown-api error 全部来自这 12 个名字（在官方 Cadence 示例中出现、但语料未收录）：

| 符号 | 出现次数 | 预判 |
|---|---|---|
| `axlXSectionAssign` | 14 | 真实 Allegro API（叠层截面） |
| `axlXSectionCreateStackup` | 4 | 真实 |
| `axlXSectionRemove` | 2 | 真实 |
| `axlXSectionRename` | 1 | 真实 |
| `axlSnapEnableAtRMB` | 2 | 真实 |
| `axlSnapDisableAtRMB` | 1 | 真实 |
| `axlSwapSymbols` | 2 | 真实 |
| `axlDBCreate1SegLine` | 1 | 真实 |
| `axlCMDBInit` | 1 | 真实 |
| `axlCMDBExit` | 1 | 真实 |
| `axlTestDriver` | 4 | 示例外部定义名（测试驱动），**预期 isCallable=false** |
| `axlPerformance` | 2 | 同上 |

步骤：

1. **先人工验证 `arglist` 的调用形态**：对 1 个已知符号（如 `axlDBFindByName`）分别试 `arglist('axlDBFindByName)`、`arglist(evalstring("axlDBFindByName"))` 等，确认哪种在 17.2 S048 上返回参数表。把结论记入 verified_facts（这是第一条交叉验证事实）。
2. 12 个名字写入 `names_batch1.txt`，跑探针，收集 JSON。
3. **按结果回灌**（三种去向）：
   - `callable=true` 且能在上游 `docs/html/algroskill/` 源里 grep 到文档 → 是**转换器漏收**：修 `convert_html_references.py` 的收录范围，重跑转换器管线 + `build_reference_indexes.py` + `check_signatures.py`，语料扩充后 `validate_skill_api.py --write-baseline` 重录（error 数应下降）。
   - `callable=true` 但源文档没有 → 语料无法收录，落 **verified_facts**（含实测 arglist），格式见 §4。
   - `callable=false`（预期 `axlTestDriver`/`axlPerformance`）→ 落 verified_facts 记"该名字在 17.2 S048 不可调用，属示例外部定义"，防止未来 agent 把它们当真实 API。
4. 重录校验器基线：`python scripts\validate_skill_api.py --self-test --write-baseline`。**基线只允许下降**；如果 error 数没降，说明回灌没生效，回步骤 3 查。

### 3.3 批次 2：全语料对账（1411 符号 + 越界前缀抽样，约 1 小时）

目的：验证"语料签名 = 真实签名"这一根本假设，并给 unknown-api 判定一个真值表。

1. 生成名单（存为 `export_names.py` 后在 `.claude\` 目录下跑 `python export_names.py`；PowerShell 没有 heredoc）：

   ```python
   import re
   from pathlib import Path

   ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|")
   names = []
   for pat in ("skill-references/api_index.part*.md",
               "skill-references/sklang_api_index.part*.md"):
       for p in sorted(Path(".").glob(pat)):
           names += [ROW.match(l).group(1)
                     for l in p.read_text(encoding="utf-8").splitlines()
                     if ROW.match(l)]
   unique = list(dict.fromkeys(names))
   Path("names_batch2.txt").write_text("\n".join(unique), encoding="utf-8")
   print(len(unique))   # 预期 1411
   ```

2. 跑探针（1411 个名字在 Allegro 内是秒级的；`arglist` 可能个别报错，errset 兜底即可）。
3. **对账脚本**：把探针 JSON 与索引签名逐条比对——`callable=false` 的语料符号（文档有、平台没有：版本差异或未公开 API）与 `arglist` 和索引签名参数数不一致的条目，分别列清单。
4. 回灌规则：
   - `callable=false` → verified_facts 记 `status: "verified"`、`constraint: "17.2 S048 上 isCallable=false，调用前必须守卫"`。**不要删语料条目**（可能是版本文档差异）。
   - arglist 不一致 → 逐条人工裁决：语料错（修转换器/登记 `SIGNATURE_OVERRIDES`）还是平台特化（verified_facts 记差异）。这类发现同时反哺 `check_signatures.py` 的门。
5. 顺手抽样 20 个**越界前缀**名字（`dbc*`/`tsel*`/`ash*`/`hi*`——校验器对它们不判定），确认"不判定"策略的漏报规模，决定是否值得为高频前缀补语料。

### 3.4 验收标准（阶段 A）

- [ ] 12 个缺口名字全部有 isCallable/arglist 实测结论并回灌（语料 or verified_facts）。
- [ ] `validate_skill_api.py --check` 基线下降或持平（预期 35 → ≤2 或 0）。
- [ ] 全语料对账清单归档（放 `.artifacts/` 下，命名如 `iscalable-matrix-17.2-S048.json`），verified_facts 至少新增 10 条 `status: "verified"` 事实。
- [ ] `validate_facts.py --write-baseline` 重录增长基线。

---

## 4. verified_facts 回灌格式（照抄模板）

`.claude/skill-references/verified_facts.json`，schema_version=1。每条事实：

```json
{
  "id": "axlXSectionAssign-callable-17.2",
  "api": "axlXSectionAssign",
  "constraint": "17.2 S048 实测 isCallable=true；arglist=(...)。语料未收录，调用前无需守卫，但签名以本条为准。",
  "evidence": [
    {"probe": ".artifacts/iscalable-matrix-17.2-S048.json"}
  ],
  "verified_on": {"allegro": "17.2-2016 S048"},
  "status": "verified",
  "source": "probe"
}
```

规则：

- `status` 只有 `verified`（真机实测）/ `documented`(仅文档) / `superseded`（被取代，**保留条目不删除**）。
- `evidence` 每条要么 `{path, line}`（语料出处，path 相对 skill-references，line 必须在文件行数范围内），要么 `{probe}`（实测产物路径）。
- id 命名 `<api>-<主题>`，不得重复。
- 每次回灌后跑 `python scripts\validate_facts.py --check`；增长基线随回灌用 `--write-baseline` 重录（只许涨）。

---

## 5. 阶段 B：cadence-skill-agent 端到端生成评测

离线栈只能证明"校验器和检索不撒谎"，端到端质量要在真实 agent 会话里量。

1. **任务集**：`.claude/eval-samples/eval_tasks.json` 已有 3 个任务（report-net-name / rename-net / with-undo-mark），每个带 prompt 与 expected_apis。在 Windows 上把每个任务作为独立会话喂给 cadence-skill-agent（上游 `.agents/skills/cadence-skill-agent` 是规范源）。
2. **收集产出**：agent 生成的 `.il` 按任务 id 命名，落进 `.claude/eval-samples/`。评估 JSON 也保留（先过 `verify_assessment.py`，再进入实现——这是 runbook 强制顺序）。
3. **打分**：

   ```powershell
   python scripts\eval_generation.py --samples eval-samples --report
   ```

   关注四个数字：`hallucination_rate`（unknown-api/文件数）、`arity_warnings`、`keyword_warnings`、`expected_api_missing`（检索失败信号——agent 绕开了文档 API 通常意味着 `search_api.py` 没把任务词映射到正确符号）。
4. **真实门收尾**：每份产出走完整 Windows 门（isCallable 守卫确认 → `sklint ?checkPubFuncs t ?outputFile ...` → `load` → smoke/qtest），lint 文本原样回馈修复轮。
5. **闭环回灌**：
   - `expected_api_missing` 非空 → 给 `eval_retrieval.py` 的 CASES 加用例（query=任务措辞，expected=agent 最终实际用对的符号），跑 `--check` 看现有排序是否命中；不命中就调 `search_api.py` 再重录基线。这是检索质量随真实使用增长的机制。
   - Windows 门发现而离线校验器没发现的缺陷（比如 arity 在真实平台更宽松/更严）→ 修校验器或落 verified_facts，两边基线重录。
6. **扩任务集**：3 个任务太少。从真实工作里每完成一个 SKILL 需求就沉淀一个任务（prompt + expected_apis + 干净参考实现），样本数只增不减（`--check` 会拦缩水）。

验收：≥10 个真实任务样本；hallucination_rate 保持 0；每次检索 MISS 都有对应新 eval 用例。

---

## 6. 阶段 C：LSP 在真实编辑器 + 真实代码上的验证

`skill_lsp.py` 是 stdio JSON-RPC 壳（diagnostics/hover/completion 全复用离线原语），协议层已有 23 个单测，缺的是**编辑器集成**与**真实代码**两维验证。

1. **编辑器接入**（VS Code 例）：安装通用 LSP 客户端扩展（如 `vscode-languageclient` 样例或现成 SKILL 语法扩展若支持自定义 server），配置：

   ```json
   {
     "command": "python",
     "args": ["<repo>\\.claude\\scripts\\skill_lsp.py"],
     "filetypes": ["il", "ils"]
   }
   ```

   没有现成 SKILL filetype 时，把 `.il` 关联到 plaintext/lisp 亦可——server 不依赖语法高亮。
2. **验证清单**（在真实项目 `.il` 上逐项过）：
   - [ ] 打开含已知缺口 API（如 `axlXSectionAssign`，阶段 A 回灌前）的文件 → 出 unknown-api error 诊断，消息含 isCallable 逃生口；**回灌后同一文件诊断消失**（这是语料↔诊断闭环的直接证明）。
   - [ ] hover 在 `axlDBFindByName` 上 → 签名 + `source:line` + 描述摘要。
   - [ ] 输入 `axlDb` 触发补全 → 出现 `axlDbidName` 等，detail 是文档签名。
   - [ ] 编辑（didChange）后诊断实时刷新；关文件（didClose）诊断清空。
   - [ ] 大文件（>2000 行）不卡顿——校验是全文件重跑，若可感知延迟，优化方向是增量缓存 `collect_local_names` 结果。
3. **严重度分层复核**：诊断的 error/warning 语义与 Windows 门冲突时（LSP 说 unknown-api、真机 isCallable=true），**以 Windows 为准**，走 §4 回灌。这条写进了 runbook，LSP 永远不是权威。
4. **交叉验证记录**：把 LSP 诊断与阶段 A 的 isCallable 矩阵对一遍——理想状态是 LSP 的 error 集合 ⊆ isCallable=false ∪ 语料缺口。有出入就是校验器或探针的 bug。

---

## 7. 优化 backlog（按优先级）

| # | 项目 | 触发条件 / 说明 |
|---|---|---|
| 1 | 语料缺口回灌（§3.2 的 12 名字） | 阶段 A 批次 1，收益直接：校验器基线 35→~0 |
| 2 | 全语料 isCallable/arglist 对账（§3.3） | 一次性投入 ~1h，产出真值表，是后续一切"权威性"论断的地基 |
| 3 | `eval_retrieval.py` 用例扩容 | 随阶段 B 真实会话增长；每条 MISS 都要变成用例 |
| 4 | sklangref 两个超页文件重分页 | `funcprog.part01.md`(13574 tokens)、`inputoutput.part01.md`(13642) 超 15000×0.9 安全线；`build_reference_indexes.py` 已有 warning。改分页后 `check_signatures.py` + 索引 + LSP 语料自动跟随 |
| 5 | 越界前缀（dbc*/tsel*/ash*）覆盖决策 | §3.3 步骤 5 的抽样结果决定：漏报规模大就补语料，小就维持"不判定" |
| 6 | LSP 增量诊断 | 仅当阶段 C 实测有可感知延迟再做 |
| 7 | 评估门接入 CI | `verify_assessment.py` 目前靠 runbook 纪律执行；上游 CI（`pythonpackage.yml`）可加一步：对留档的评估 JSON 批量跑 `--check` |
| 8 | OrCAD 侧质量栈 | `build_orcad_index.py` 只解决了索引悬空；OrCAD 的"validate_skill_api 等价物"（TCL 调用点校验）尚未建，需求出现再做 |

**基线纪律（所有优化共用）**：五个基线文件（validator FP / retrieval / generation / facts growth / pagination manifest）都只允许向好的方向移动；任何 `--write-baseline` 重录必须附一句"为什么这个变化是合理的"（提交信息或 runbook 更新）。

---

## 8. 已知陷阱（踩过或明确预期）

- **`sync_claude.py` 在 extract 仓库必失败**（找不到上游仓库根）——预期行为，不要"修"它；在上游完整仓库里跑。
- **`api_names.txt`（Python bridge 白名单）与 `api_index.part*.md`（文档化条目）口径不同**，高度重叠但不是同一集合，各自正确，不要互相对齐。
- **索引与 `.paginate/pagination_manifest.json` 禁止手工编辑**——全部由生成器产出，`--check` 会拦手改。
- **`validate_skill_api.py` 只对 `axl` 前缀判 unknown-api**——通用 SKILL 内置远多于语言参考索引，其他前缀不在语料范围。改这个策略前先跑 §3.3 步骤 5 的抽样。
- **Windows 路径**：所有脚本 `pathlib` 化过，但新写探针/胶水时记得 `Path.resolve().as_posix()` 再传给 SKILL。
- **探针产物归档**：放 `.artifacts/`（verified_facts 的 `probe` 证据引用该路径），命名带平台版本号（如 `iscalable-matrix-17.2-S048.json`），不覆盖历史。
- **每轮 Allegro 验证用新进程 + 新 board 副本**；环境类失败只重试 1 次。

---

## 9. 一页纸执行顺序

```text
Day 0  转运 + §1 离线自检（不需要 Allegro）
Day 1  §2 环境启动 → §3.2 批次1（12 名字）→ 回灌 → 重录校验器基线
Day 1  §3.3 批次2（全语料对账）→ 归档矩阵 → verified_facts ≥10 条 → 重录增长基线
Day 2  §5 阶段 B：3 个种子任务跑真实 agent 会话 → eval_generation 打分 → MISS 变检索用例
Day 2  §6 阶段 C：编辑器接 LSP → 验证清单逐项过 → 诊断↔isCallable 矩阵对账
Day 3+ §7 backlog 按触发条件滚动推进；每个真实需求沉淀为 eval-samples 新任务
```

每一步的"完成"都以对应门禁 `--check` 绿灯 + 基线重录为准，不以"看起来跑过了"为准。
