# Windows 交叉验证与后续优化交付手册

> 交付日期：2026-09-08 · 适用仓库：`RAG_SKILL_AGENT/.claude/`（extract 版）+ 上游完整仓库（含 `.agents/`、`docs/html/`）+ `skillbridge`（Windows Allegro 测试环境）
>
> 目标：把在 macOS 上离线建成、**从未在真实 SKILL 环境验证过**的五层质量栈（校验器 / 语义检索 / 评估门 / 生成评测 / LSP）拿到 Windows Allegro 17.2 上做交叉验证，并根据实测结果继续优化。

## 2026-09-10 至 2026-09-11 Windows 迭代记录

本轮已将本交付物中的 Cadence 共享内容提升到 `.agents/skills/cadence-skill-agent`，并由规范源重新生成 `.claude` 副本；Claude 独有的 memory、OrCAD 语料、OrCAD 索引脚本和本手册保留在 `.claude`。

- 真实环境确认：`D:\Cadence\Cadence_SPB_17.2-2016\tools\bin\allegro.exe`，目标 Allegro 17.2-2016 S048；本轮注入用户级 `CDS_LIC_FILE` 后 `tests/allegrobridge/test_integration.py --allegro -q` 实际通过 135 项。首次启动因当前 PowerShell 未继承该变量而超时，诊断已归档 `.artifacts/allegro-startup-diagnosis.json`；按手册注入后真实桥接恢复。
- 阶段 A 批次 1 已归档到 `.artifacts/iscalable-matrix-17.2-S048.json`：12 个缺口全部完成 `isCallable/arglist` 实测；9 个可调用、3 个不可调用。
- 阶段 A 批次 2 已归档到 `.artifacts/iscalable-matrix-17.2-S048-full.json`：1417 个索引行、1411 个大小写不敏感唯一条目、1408 个可探测符号；1396 个可调用、12 个不可调用，所有可调用条目均有 `arglist` 返回。
- 已新增 `.artifacts/arglist-reconciliation-17.2-S048.json` 及 `reconcile_arglist.py`：按官方 `arglist` 结构完成自动分类；1103 条简单位置参数记录中 980 条 exact、14 条实测落在文档范围内且已完成来源审阅、87 条 S048 真机验证的文档调用契约、3 条 `runtime-boundary`（`axlDBCreateModuleInstance`、`axlPadstackSetType`、`skillDebugger`）、4 条确认是紧凑可变参数编码、11 条完成 S048 运行时/来源审阅裁决（含 `listFunctions`），另有 4 条 `runtime-context-dependent`（`gcsummary`、`listVariables`、`loadContext`、`saveContext`），不再保留未裁决的文档范围落在实测范围内项；另外 293 条不可作固定 arity 比较的记录已拆为 89 条 `special-encoding`、151 条 `unsupported-encoding`、53 条 `non-countable-documentation`。
- `listFunctions` 的新增裁决已由独立 disposable-board Allegro session 复测：零参数和两参数调用均失败，单字符串参数调用成功；证据为 `.artifacts/listFunctions-adjudication-real-allegro-17.2-S048.json`，事实已同步至 `.agents` 与 `.claude`。
- 9 个只读/显示查询 API 的公开调用形式已在一个 fresh disposable-board S048 session 中逐一成功；证据为 `.artifacts/documentation-within-actual-readonly-real-allegro-17.2-S048.json`，未据此扩大公开文档或 stub 签名。
- 8 个 CNS/xsection getter 的公开调用形式也已在一个 fresh disposable-board S048 session 中逐一成功；证据为 `.artifacts/documentation-within-actual-cns-readonly-real-allegro-17.2-S048.json`，未据此扩大公开文档或 stub 签名。
- 7 个通用 SKILL 的文件/字符串/宏调用形式已在一个 fresh disposable-board S048 session 中成功；`listVariables` 在字符串、符号和 `nil` 形式下均需额外运行时上下文，已单独标为 `runtime-context-dependent`；证据为 `.artifacts/documentation-within-actual-skill-readonly-real-allegro-17.2-S048.json`，未据此扩大公开文档或 stub 签名。
- `makeTable` 的一参数、二参数形式及缺省值查表已在 fresh disposable-board S048 session 中成功；证据为 `.artifacts/documentation-within-actual-maketable-real-allegro-17.2-S048.json`，仅创建进程内临时表，未扩大公开文档或 stub 签名。
- `fileTell` 的一参数输入端口形式已在 fresh disposable-board S048 session 中成功，并确认端口关闭；证据为 `.artifacts/documentation-within-actual-filetell-real-allegro-17.2-S048.json`。
- `read` 与 `lineread` 的 supplied-port 形式已在 fresh disposable-board S048 session 中成功，并确认两个临时输入端口关闭；证据为 `.artifacts/documentation-within-actual-read-lineread-real-allegro-17.2-S048.json`。
- 选择集的 `axlAddSelectAll`、`axlClearSelSet` 与计数查询已在 fresh disposable-board S048 session 中成功返回并完成清理；fixture 没有可选对象，未扩大解释为全选效果通过。证据为 `.artifacts/documentation-within-actual-selection-real-allegro-17.2-S048.json`。
- `getMethodSpecializers` 已在 fresh disposable-board S048 session 中用进程内定义的 generic function 验证返回 `number` specializer，并验证非 generic 的 `car` 错误路径；证据为 `.artifacts/get-method-specializers-real-allegro-17.2-S048.json`，未扩大公开文档或 stub 签名。
- `gets` 的变量加 supplied-port 形式已在 fresh disposable-board S048 session 中成功读取一行并关闭端口；同批 `gcsummary` 明确返回 `skillDev not enabled`，已标为运行时上下文依赖；证据为 `.artifacts/gcsummary-gets-real-allegro-17.2-S048.json`。
- `defvar` 的一参数与带值形式已在 fresh disposable-board S048 session 中成功赋值并返回预期值；变量仅存在于独占进程；证据为 `.artifacts/defvar-real-allegro-17.2-S048.json`。
- `createDir` 与 `deleteDir` 已在 fresh disposable-board S048 session 中对 probe-owned 空目录完成创建、删除及重复删除检查；证据为 `.artifacts/create-delete-dir-real-allegro-17.2-S048.json`，目标目录已确认不存在。
- `unprofile` 的零参数形式已在 fresh disposable-board S048 session 中返回 `t`；保留文档中的 Windows profiler 限制说明，不扩大为 profiler 状态验证；证据为 `.artifacts/unprofile-real-allegro-17.2-S048.json`。
- `axlAutoOpenFindFilter`、`axlOpenFindFilter`、`axlCloseFindFilter` 和 `axlSubSelectAll` 已在 fresh disposable-board S048 session 中完成调用与清理；空 fixture 下 `axlSubSelectAll`/`axlClearSelSet` 返回 nil 被按文档作为合法 no-op；证据为 `.artifacts/find-filter-selection-real-allegro-17.2-S048.json`。
- `axlColorPrioritySet`、`axlDesignFlip`、`axlZoomFit` 和 `axlZoomWorld` 已在 fresh disposable-board S048 session 中完成公开调用；兼容性调用返回 `t`，flip 从 normal 状态切换后恢复，两个 zoom 调用返回 `t`；证据为 `.artifacts/view-display-real-allegro-17.2-S048.json`，未扩大公开文档或 stub 签名。
- `axlAddSelectName`、`axlAddSelectObject`、`axlSingleSelectObject`、`axlSubSelectName` 和 `axlSubSelectObject` 已在 fresh disposable-board S048 session 中完成公开调用；不存在的 refdes 与 nil dbid 均保持空选择集并按文档返回 nil no-op；证据为 `.artifacts/selection-object-name-real-allegro-17.2-S048.json`，未扩大公开文档或 stub 签名。
- `axlAltSymbolList`、`axlAltSymbolOK` 和 `axlCNSEcsetValueGet(nil)` 已在 fresh disposable-board S048 session 中完成公开调用；有效组件 `C1` 返回其替代封装列表，非法替代封装返回 nil，ECset nil 查询返回支持值控制项列表；证据为 `.artifacts/readonly-query-real-allegro-17.2-S048.json`，未扩大公开文档或 stub 签名。
- `axlExportXmlDBRecords(nil)`、`axlDBTuneSectorSize()` 和 callback-free `axlExtractMap("net_baseview" nil nil)` 已在 fresh disposable-board S048 session 中完成公开调用；参数组查询返回列表、sector tuning 返回 nil（无需调优）、extract 在无匹配项时返回 nil；证据为 `.artifacts/readonly-map-performance-real-allegro-17.2-S048.json`，未扩大公开文档或 stub 签名。
- `axlColorSet` 已在 fresh disposable-board S048 session 中读取并原值写回 color 1，`axlPadSuppressSet(nil nil)` 以 no-op 形式返回成功；颜色前后相同，未改变 pad suppression；证据为 `.artifacts/display-settings-real-allegro-17.2-S048.json`，未扩大公开文档或 stub 签名。
- `axlMsgContextInBuf` 与 `axlMsgContextRemove` 已在 fresh disposable-board S048 session 中检查并移除唯一探测消息；前者返回 nil、后者返回 t，均无 SKILL 错误；证据为 `.artifacts/message-context-real-allegro-17.2-S048.json`。
- `axlPackageDesignCheckDrcError` 与 `axlPackageDesignCheckLogError` 已在 fresh disposable-board S048 session 中完成一次性 DRC/log 探测；两者均无 SKILL 错误并返回 nil，未保存 board；证据为 `.artifacts/package-check-real-allegro-17.2-S048.json`。
- `axlSetAlias` 与 `axlSetFunckey` 已在 fresh disposable-board S048 session 中用临时 `~Q` 键设置并恢复；两者均返回 t，最终值恢复为原始 nil；证据为 `.artifacts/alias-funckey-real-allegro-17.2-S048.json`。
- `axlCNSDesignModeSet` 与 `axlCNSDesignValueSet` 已在 fresh disposable-board S048 session 中读取完整列表、原样写回并再次读取；前后列表相等，分别返回 t 与 nil（无变化），未改变约束状态；证据为 `.artifacts/cns-design-set-real-allegro-17.2-S048.json`。
- `ipcSetPriority` 已在 fresh disposable-board S048 session 中将当前优先级 15 原样写回并确认保持 15；`axlDrawObject(nil)` 与 `axlEraseObject(nil)` 均完成合法空 dbid no-op；证据为 `.artifacts/priority-display-real-allegro-17.2-S048.json`。
- `axlCNSPhysicalModeSet` 与 `axlCNSSpacingModeSet` 已在 fresh disposable-board S048 session 中读取完整 mode 列表、原样写回并再次读取；前后列表相等，两个 setter 均返回 t；证据为 `.artifacts/cns-physical-spacing-real-allegro-17.2-S048.json`。
- `axlCNSAssemblyModeSet` 与 `axlCNSSameNetModeSet` 已在 fresh disposable-board S048 session 中读取完整 mode 列表、原样写回并再次读取；前后列表相等，两个 setter 均返回 t；证据为 `.artifacts/cns-assembly-samenet-real-allegro-17.2-S048.json`。
- `encrypt` 已在 fresh disposable-board S048 session 中使用官方 `tstub.il` 生成 probe-owned 非空加密文件，返回 t；证据为 `.artifacts/encrypt-real-allegro-17.2-S048.json`。
- `axlPadstackEdit(nil nil)` 已在 fresh disposable-board S048 session 中完成只读 editable-attribute 查询并返回完整属性列表，未供应 padstack dbid 或修改值；证据为 `.artifacts/padstack-edit-query-real-allegro-17.2-S048.json`。
- `axlDBAssignNet(nil nil)` 已在 fresh disposable-board S048 session 中完成空对象 no-op 调用并返回 nil；未修改任何对象、net 或 cline；证据为 `.artifacts/assign-net-real-allegro-17.2-S048.json`。
- `axlDBChangeText` 已在 fresh disposable-board S048 session 中对临时创建的 text dbid 原样改写并立即删除；变更调用无 SKILL 错误，删除返回 t；证据为 `.artifacts/change-text-real-allegro-17.2-S048.json`。
- `axlUIWHelpRegister(nil)` 已在 fresh disposable-board S048 session 中完成只读 help-command 清单查询并返回当前列表，未注册或删除 help；证据为 `.artifacts/ui-help-query-real-allegro-17.2-S048.json`。
- `axlDBCreateCloseShape` 已在 fresh disposable-board S048 session 中创建临时 open shape、完成 close 并删除 close 后的新 shape dbid；未保存 board，证据为 `.artifacts/close-shape-real-allegro-17.2-S048.json`。该调用涉及立即 DRC，因此不宣称可回滚。
- `axlDBSetLock` 已在 fresh disposable-board S048 session 中设置唯一临时 comment 锁、通过 `axlDBGetLock` 读回并用 `axlDBDelLock()` 删除；最终无锁且未保存 board，证据为 `.artifacts/set-lock-real-allegro-17.2-S048.json`。锁操作仅存在于 owned process。
- `axlUIMenuInsert` 已在 fresh disposable-board S048 CLI session 中插入唯一临时 command，并按 command 名找回后用 `axlUIMenuDelete` 删除；证据为 `.artifacts/menu-insert-real-allegro-17.2-S048.json`，未写入用户菜单文件或使用用户 GUI session。
- `axlDiffPair` 已在 fresh disposable-board S048 session 中从 fixture 实际读取 `VCC`/`GND` net 名称，创建唯一临时 diff pair，随后用返回 dbid 删除并确认 `axlDiffPairDBID` 返回 nil；证据为 `.artifacts/diff-pair-real-allegro-17.2-S048.json`，未保存 board。
- `axlFormColorize` 已在 fresh disposable-board S048 CLI session 中使用官方 `colorTest.form` 创建临时 form，对真实 `colors` 字段执行背景色恢复并关闭 form；证据为 `.artifacts/form-colorize-real-allegro-17.2-S048.json`，未显示用户 GUI。
- `debugQuit()` 已在 fresh disposable-board S048 CLI session 的普通上下文中返回 `nil`，未进入 interactive debugger；证据为 `.artifacts/debug-quit-real-allegro-17.2-S048.json`。随后对 `skillDebugger()` 做了真实 S048、有界 15 秒探针；调用未返回，符合文档所述进入 `debug #>` 交互顶层的边界，owned Python/Allegro 子进程已按精确命令行和父子关系清理，证据为 `.artifacts/skill-debugger-real-allegro-17.2-S048.json`。该 API 标为 `runtime-boundary`，不生成普通成功契约。
- `axlDBCreatePin` 已在 Cadence 官方 `cap400.dra` package-symbol drawing 中使用官方 `pad60cir36d.pad`、probe-owned `PADPATH` 和 fresh disposable S048 CLI session 成功创建机械 pin，并在同一 session 删除返回 dbid；证据为 `.artifacts/create-pin-symbol-real-allegro-17.2-S048.json`，未编译或保存 symbol drawing。
- `axlDBCreateModuleDef` 在 disposable board 上用真实 component 成功生成 probe-owned module definition，但随后六参数 `axlDBCreateModuleInstance` 在同一 S048 session 返回 `nil`；证据为 `.artifacts/create-module-instance-real-allegro-17.2-S048.json`。因此将 module-instance 记录为 `runtime-boundary`，没有把它提升为成功契约，也没有重放该失败写入。
- 进一步将生成的 `.mdd` 以绝对 basename 传入，在 fresh disposable S048 session 中结果仍为 `nil`，且 module definition 文件确实生成；证据为 `.artifacts/create-module-instance-absolute-real-allegro-17.2-S048.json`。该 API 保留为运行时设计复用边界，不继续猜测路径或参数。
- `saveContext/loadContext` 已在无 board 的 fresh S048 CLI session 中再次尝试；两者均返回 errset nil，且未生成 context 文件，证据为 `.artifacts/context-io-no-board-real-allegro-17.2-S048.json`。因此正式标为 `runtime-context-dependent`，不生成成功契约或 stub 扩展。
- `axlPadstackSetType` 已在 fresh disposable-board S048 session 中检查全部 `design->padstacks`；fixture 没有 `bbvia/uvia` 类型候选，因此未执行 setter，证据为 `.artifacts/padstack-type-real-allegro-17.2-S048.json`。随后又按官方 `CreateBBvia` 示例在 disposable board 创建临时 padstack；S048 将其分类为 `smd`/`through`，setter 返回 nil 且类型不变，证据为 `.artifacts/padstack-type-create-real-allegro-17.2-S048.json`；先改 `usage` 的路径还出现无返回边界，已按 owned 进程清理，证据为 `.artifacts/padstack-type-usage-hang-real-allegro-17.2-S048.json`。现标为 `runtime-boundary`，不宣称 setter 成功。
- 进一步尝试先用官方 `axlPadstackEdit(... 'usage 'Bbvia)` 改分类时，S048 CLI probe 无返回；owned 进程已按父子关系清理，证据为 `.artifacts/padstack-type-usage-hang-real-allegro-17.2-S048.json`，不把该路径当作成功或可重放写入。
- `axlDBCreatePropDictEntry` 已在 fresh disposable-board S048 session 中创建唯一临时 STRING 属性并立即删除；创建返回 property dbid、删除返回 t、删除后查无该属性；证据为 `.artifacts/propdict-real-allegro-17.2-S048.json`。
- `axlCNSEcsetModeSet` 与 `axlCNSEcsetValueSet` 已在 fresh disposable-board S048 session 中读取现有 ECset 状态、原样写回并再次读取；mode 列表相等，`UPREVED_DEFAULT` 的 `Maximum_Via_Count` 保持为 4；证据为 `.artifacts/cns-ecset-set-real-allegro-17.2-S048.json`。
- 当前 S048 `verified_facts` 共 42 条，其中 37 条 verified，并将明确 `isCallable=true` 的平台扩展接入 validator/LSP；validator 官方样例 unknown-api 从 35 降至 7，剩余均对应真实不可调用条目。
- LSP 真实 stdio 闭环通过：已验证扩展无诊断、编造 API 报 `unknown-api`、`didChange` 刷新、`didClose` 清空、hover 和 completion 返回真实语料结果。
- 阶段 C 已准备一次性 VS Code extension-host harness（`.artifacts/vscode-skill-lsp-smoke/`），并完成 `node --check`；通过现有 VS Code CLI 已实际进入 1.136.1 extension host，跨记录运行观测到 initialize、unknown-api、didChange、hover、completion、didClose。此前大文档检查的 harness payload 已发现并修正；安装目录直接启动受 `vscode-updating` mutex 影响，且 `--disable-updates`/`VSCODE_DEV=1` 均未形成可观测 extension-host。随后 11:11 使用安装内完整 1.137.0 versioned resources 创建任务自有临时 launch root（复制启动 exe、junction 引入完整 version 目录、使用全新 user-data-dir/extensions-dir）完成单进程全清单验收：7/7 checks 通过，2101 行诊断无错误，耗时 35.7ms。证据为 `launch-blocker.json` 与 `stage-c-clean-real-2026-09-11.json`；此前 portable Electron 副本的独立启动另有 ICU descriptor 错误记录。
- LSP 大文档性能已单独拆分测量：对 2101 行文件，直接 server `didOpen` 为 41.53ms、重复 `didChange` 为 27.93ms，未触发增量缓存优化条件；VS Code 观测到的约 1.7s 属于 extension-host 启动/集成路径，不把它误判为诊断算法延迟。证据为 `.artifacts/lsp-diagnostic-timing.json`，探针为 `.artifacts/lsp_timing_probe.py`。
- 阶段 B 三个种子脚本已逐个通过真实 Allegrobridge session：每个使用新 Allegro 进程、唯一端口和 disposable board，均 `load=True`；`report-net-name` 的 `'net` 类型参数和事务 wrapper 的 `funcall(thunk)` 调用已根据 S048 真机错误修正，commit 返回 `t`、rollback 返回 `nil`。
- 本轮重新执行完整 `tests/allegrobridge/test_integration.py --allegro -q`，真实 Allegro 17.2-2016 S048 返回 `135 passed, 10 warnings`（253.19s）。期间确认 copied SKILL suite 的冷启动可能超过全局 60s pytest timeout，已对该测试加局部 300s 标记；这只容纳已观测的 Allegro 启动延迟，不放宽 bridge 内部连接语义或跳过断言。
- 阶段 B 已补齐 7 个只读任务，当前 10 个 `.il` 样本全部通过真实 Allegro S048 load/call smoke；证据归档于 `.artifacts/stage-b-supplemental-real-allegro-17.2-S048.json`。这 7 个样本由当前 Cadence agent 生成，未冒充 Claude CLI 会话。
- 按用户要求补做了不经 AllegroBridge 的裸进程验证：直接启动 `D:\Cadence\Cadence_SPB_17.2-2016\tools\bin\allegro.exe -p <owned-run-dir> -s startup.scr`，注入已配置的 `CDS_LIC_FILE=5280@localhost`，在 probe-owned `shape1.brd` 副本中由 Allegro 自己 `load()` 并调用 10 个样例入口；10/10 加载成功、10/10 调用完成。原始结果为 `.artifacts/direct-allegro-real-17.2-S048.json`，探针为 `.artifacts/direct_allegro_smoke.py`。同样方式加载交付测试树已进入真实 qtest/qcover（44/44 framework self-tests、qcover 18/18 与 2/2），但 `run.ils` 最后的 `qcover::reset` 在裸启动路径于第 50 行返回 load error；该 suite 结果不计作全绿，既不掩盖也不影响上面的 10/10 脚本 load/call 结论。
- 阶段 B 的 3 个独立 Claude CLI 生成会话已完成闭环：report-selection-count 首轮通过，report-design 与 report-conductor-layers 经 validator 反馈后各由新的独立会话修正；3 个最终候选均通过词法/API 门和真实 Allegrobridge S048 load/call。完整 stdout/stderr、SHA-256、首轮失败候选及修正结果见 `.artifacts/claude-cli-agent-runs/manifest.json`，真实结果见 `validated-candidates/report-selection-count-real-allegro-17.2-S048.json` 与 `validated-candidates/corrected-candidates-real-allegro-17.2-S048.json`；CLI 的 `unrecognized_model` 警告原样保留，不把它隐藏为干净路由。
- `sklint` 已按要求只通过独占 Allegrobridge S048 进程真实调用，使用 disposable `shape1.brd` 与 probe-owned `.il`/输出路径；默认调用因缺少 `cdsFuncs.cxt` 返回 `Can't load context`。进一步在 fresh owned session 显式加载安装内 `SKILL35.00/context/64bit/skillDev.cxt`，`loadContext` 返回 `t`，且 `axlLicFeatureExists("skillDev")` 返回 `t`；但 bridge 路径的 `axlLicIsProductEnabled("skillDev")` 与 `skillDevStatus()` 均为 `nil`，随后 `?checkPubFuncs t` 仍失败。补充的直接 `il_allegro.exe` REPL 探针设置安装自带 `TELENV=share/pcb/text/env` 后可启动，`loadContext` 与 `skillDevStatus()` 均返回 `t`，但完整 lint 仍在实际入口因同一个 `tools/dfII/etc/context/64bit/cdsFuncs.cxt` 缺失返回 `nil`；证据为 `.artifacts/sklint-skilldev-direct-real-17.2-S048.json`。只读 `lmutil lmstat -f skillDev` 显示 server 可达、feature 已发布（999 issued / 0 in use）；安装内 `share/pcb/examples/skill/FAQ/contextes.txt:24-26` 明确写明该版本 Skill developers license 仅 UNIX 可用。结合整棵 Cadence 安装均找不到 `cdsFuncs.cxt`，当前结论收敛为 Windows S048 安装缺少完整 SkillDev 公共函数 context，而非 bridge、启动环境或普通 lint 不可用。已有 EL5 真实 bridge 证据表明 `checkPubFuncs=False` 的普通 lint 可返回 PASS，但不能替代完整公共函数 lint 门。证据为 `.artifacts/sklint-skilldev-real-allegro-17.2-S048.json`、`.artifacts/sklint-skilldev-direct-real-17.2-S048.json`、`.artifacts/sklint-license-server-2026-09-10.json`、`.artifacts/sklint-windows-license-assessment-2026-09-10.json`、`.artifacts/el5-routing/finish/public-lint-error.txt`、`.artifacts/el5-routing/finish/topology.lint`、探针 `.artifacts/sklint_skilldev_probe.py`、`.artifacts/sklint_skilldev_direct_probe.py` 和评估前置 `.artifacts/sklint-skilldev-assessment.json`；Windows lint 门仍 incomplete，不能用离线静态检查替代。
- 23:17 的最新只读 license 复核用 `lmutil lmstat -c 5280@localhost -f skillDev` 得到 server `UP`、`999 issued / 0 in use`；随后再次用新 disposable board 和独占 Allegrobridge S048 进程运行 `sklint_skilldev_probe.py`，仍得到 `context_loaded=true`、`skilldev_feature_exists=true`、`skilldev_license_enabled=false`、`skilldev_status=nil`，并在 bridge 入口处因 `cdsFuncs.cxt` 缺失失败。该结果确认先前 Windows SkillDev runtime-boundary 没有变化，未将普通 lint 当作完整门。
- 11:45 的新鲜安装级复核再次确认 `SKILL35.00/context/64bit/skillDev.cxt` 存在，但整棵 Windows 安装没有 `cdsFuncs.cxt`；本机 FlexLM `skillDev` 仍为 `999 issued / 0 in use`。随后在新 disposable board / 独占 Allegrobridge S048 进程中重新运行探针：`loadContext=t`、`axlLicFeatureExists=t`、`axlLicIsProductEnabled=nil`、`skillDevStatus=nil`，`sklint` 入口实际到达后仍因缺失 `cdsFuncs.cxt` 失败；新结果已写入 `.artifacts/sklint-skilldev-real-allegro-17.2-S048.json`。这把剩余阻塞进一步限定为 Windows 安装/许可证边界，而非 bridge、探针或候选 SKILL 文件问题。
- 随后使用正确 `TELENV` 的直接 `il_allegro` REPL 做参数矩阵：默认 `sklint`、`?context "skillDev"`、`?skPath <install>` 三种调用均加载规则后寻找同一个缺失的 `tools/dfII/etc/context/64bit/cdsFuncs.cxt`，均返回 `nil`；REPL 内 `loadContext=t`、`skillDevStatus=t`，但进程存活期间 `lmutil lmstat -f skillDev` 仍显示 `0 in use`。因此不能把 `skillDevStatus` 或服务端 issued 数字当作完整公共函数 context 已存在的证据，最终门仍以 `?checkPubFuncs t` 的实际输出为准。
- §3.3 步骤 5 的越界前缀抽样已完成：在独占真实 S048 Allegrobridge session 中抽取 20 个来自 `ash*`/`tsel*`/`hi*` 的实际语料调用名，全部 `isCallable=nil`；同一表达式的控制项 `axlDBGetDesign` 与 `printf` 均为 `t`，证明探针和返回值解码有效。结论是维持 validator 对这些前缀的“不判定”策略，不把当前未加载/不可调用的辅助函数误纳入公共 API 语料；证据为 `.artifacts/overflow-prefix-real-allegro-17.2-S048.json`，探针为 `.artifacts/overflow_prefix_probe.py`。
- 早期 Claude CLI 路由探针（`settings.json` 中的旧模型映射）仍保留其不可用/`unrecognized_model` 原始记录，不计入评测；最终 3 个独立生成会话及其修正闭环已按第 67 条计入阶段 B，不把两类结果混为一谈。
- 本轮追加的 `opus` 非交互探针仍未得到可用生成结果，且报告了 `unrecognized_model` 路由；证据为 `.artifacts/claude-cli-routing-probe.json`，不把该探针计入阶段 B。
- 当前 `scripts/generate_axl_stubs.py` 已从 792 条 `api_names.txt` 重新生成 `allegrobridge/client/_axl_stubs.pyi`；生成器 `--check`、stub contract/type 测试及仓库全量测试 646 passed / 188 skipped 均通过。
- `docs/reference/domain-apis.md` 的 DTO 文档引用已统一指向实际定义所在的 `allegrobridge.client.api.record` 模块；`mkdocs build --strict` 已通过，修复了原先因别名模块路径错误导致的 DTO 收集失败。
- 基于 S048 `arglist` 的明确证据，stub 生成器新增 5 条平台签名 override：除已有 `axlCnsPurgeCsets(s_type)`、`axlCnsPurgeObjects(s_type)`、`axlGetDieStackMemberSet(g_stackArg)` 外，新增 `axlDBChangeDesignUnits(t_units/nil x_accuracy/nil)`、`axlUIWMove(r_window/nil l_xy)`；未对其余差异作猜测性改动。
- 离线门禁：Claude 副本 258 tests、`.agents` 副本 247 tests 通过；检索/生成/事实/签名/OrCAD 门禁通过。PDF 转换 `--check` 仍受当前机器缺少 `pdftotext` 限制，未将其结果冒充通过。
- 评估门已接入 `.github/workflows/pythonpackage.yml` 的 Python 3.10 job：CI 执行 `test_verify_assessment.py` 并对固定真实索引 fixture 运行 `verify_assessment.py`；Windows 本地验证为 20 tests，fixture 为 1 evidence entry、0 errors/0 warnings。
- CI 现同时校验 Cadence 参考索引/签名生成物与 OrCAD 索引生成物：`build_reference_indexes.py --check`、`check_signatures.py`、`build_orcad_index.py --check` 均已加入 Python 3.10 job；OrCAD 当前为 5100 scanned / 4569 unique rows / 15 parts。TCL 调用点语义校验仍未伪造为已完成。
- retrieval benchmark 已随 10 个任务集扩容到 38 个意图用例；重录基线有明确的样本扩充依据，`top1=0.6053`、`MRR=0.6819`、`recall@5=0.8158`，均高于原 32 用例基线（0.5625/0.6500/0.8125），canonical 与 `.claude` 两份检查均通过。

尚未完成的交付项：Windows S048 PCB 运行时缺失的完整 SkillDev 公共函数 lint 能力（bridge 路径的 SkillDev token 未 checkout，直接 `il_allegro` 在正确 `TELENV` 下虽可得到 `skillDevStatus=t`，但安装中仍缺失 `cdsFuncs.cxt`）。阶段 B 的 3 个独立 Claude CLI agent 会话、阶段 C 的一次干净单进程 extension-host 全清单报告均已完成；对账报告中的 3 条文档范围落在实测范围内记录已逐条裁决为 `runtime-boundary`（`axlDBCreateModuleInstance`、`axlPadstackSetType`、`skillDebugger`），保留原始范围与真实运行边界，不生成猜测性 stub。`axlDBCreatePin` 已完成 symbol-editor 真实验证，loadContext/saveContext 已明确标为运行时上下文依赖，未计入成功契约；特殊编码记录已明确标为不可作固定 arity 比较，不将其误报为普通未处理差异。样本数量与裸 Allegro load/call smoke 门已达到 10/10；完整 SkillDev lint 门尚未完成，裸 `tests/skill/run.ils` 的最后清理阶段另有独立失败记录。

恢复条件：在提供完整 `tools/dfII/etc/context/64bit/cdsFuncs.cxt` 的 Cadence SkillDev 安装（或合规 UNIX SkillDev 环境）后，先在新独占运行时确认 context 与 `skillDevStatus()`，再直接重跑 bridge 探针 `.artifacts/sklint_skilldev_probe.py`；Windows 直接 `il_allegro` 探针 `.artifacts/sklint_skilldev_direct_probe.py` 只能证明 SkillDev 运行时可启动，不能替代 Allegrobridge `?checkPubFuncs t` 门。不得把 `checkPubFuncs=False` 或离线检查当作完整 lint 门。裸 Allegro 的脚本 load/call 已有独立 10/10 证据；后续若修复 `run.ils` 裸路径清理错误，应沿用 `.artifacts/direct_allegro_skill_suite.py` 的 disposable-board/owned-process 约束。Claude CLI 生成闭环已完成，但后续新增模型路由仍需保留原始告警并通过同样的质量门。

---

## 0. 现状快照（2026-09-11 Windows 当前状态）

离线门禁保持绿灯；skillbridge 全量测试为 646 passed / 188 skipped，`.agents` 与 `.claude` 的同步副本均已单独通过各自测试（同名测试不能在一次 pytest 收集中混跑）：

| 层 | 脚本 | 基线文件 | 当前基线值 |
|---|---|---|---|
| 语料校验（生成后） | `validate_skill_api.py` | `validate_skill_api_baseline.json` | 137 官方示例中 1 文件有 error；7 errors / 111 warnings 均为已登记的语料覆盖或签名差异；校验器逻辑误报 = 0 |
| 评估门（生成前） | `verify_assessment.py` | —（无基线，逐次判定） | 冒烟通过：能拦编造 API 并给真实候选 |
| 语义检索 | `search_api.py` + `eval_retrieval.py` | `eval_retrieval_baseline.json` | 38 用例：top1=0.6053 / mrr=0.6819 / recall@5=0.8158；4 条 MISS 为已登记 frontier case |
| 生成质量 | `eval_generation.py` | `eval_generation_baseline.json` | `.claude/eval-samples/` 10 个样例全净（hallucination_rate=0） |
| 经验库增长门 | `validate_facts.py --check` | `verified_facts_baseline.json` | 42 条事实（37 verified），总数/verified 数只许增长 |
| 编辑器 LSP | `skill_lsp.py` | —（24 个协议单测） | stdio 冒烟通过；**真实环境交叉验证 = 本手册主题** |

语料规模：`api_index.part*.md` 795 行（axl）+ `sklang_api_index.part*.md` 622 行 = 1411 个唯一符号；OrCAD 侧 `orcadcapture/api_index.part01–15.md` 4569 行（`build_orcad_index.py` 生成）。

**当前已验证与剩余边界**：1411 个唯一语料符号已完成 S048 `isCallable/arglist` 对账，另有 20 个越界前缀样本完成真实 `isCallable` 抽样；已知不可调用与运行时边界均已登记，`unknown-api` 仍保留“用真机 `isCallable` 复核语料缺口”的逃生路径。尚未完成的是 SkillDev license/context lint 门；3 个 Claude CLI 生成会话和阶段 C 单进程 VS Code 1.137.0 全清单均已有通过证据。

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
python -m pytest tests -q          # 当前副本约 258 项；完整 skillbridge 测试基线为 646 passed / 188 skipped
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

> 当前状态：该探针流程已在真实 Allegro 17.2-2016 S048 完成小样本与全语料运行；`isCallable`/`arglist` 对账结果和异常字段均已归档。后续新增 API 仍须按同样的 disposable-board、独占进程和唯一端口约束执行。

### 3.2 批次 1：已知语料缺口（12 个名字，已完成）

历史上 `validate_skill_api.py --self-test` 的 35 个 unknown-api error 全部来自这 12 个名字；当前已完成真机裁决并回灌，剩余基线为 7 个真实不可调用条目：

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
   当前实现：`python .claude/scripts/reconcile_arglist.py .artifacts/iscalable-matrix-17.2-S048-full.json --references .claude/skill-references --output .artifacts/arglist-reconciliation-17.2-S048.json`。报告将非 exact 简单记录细分为 `within-documentation`、`documentation-within-actual`、`runtime-boundary`、`runtime-context-dependent`、`overlap-only`、`disjoint`，避免把“实测暴露额外可选参数”和“文档允许更宽范围”混在一起。
4. 回灌规则：
   - `callable=false` → verified_facts 记 `status: "verified"`、`constraint: "17.2 S048 上 isCallable=false，调用前必须守卫"`。**不要删语料条目**（可能是版本文档差异）。
   - arglist 不一致 → 逐条人工裁决：语料错（修转换器/登记 `SIGNATURE_OVERRIDES`）还是平台特化（verified_facts 记差异）。这类发现同时反哺 `check_signatures.py` 的门。
5. 顺手抽样 20 个**越界前缀**名字（`dbc*`/`tsel*`/`ash*`/`hi*`——校验器对它们不判定），确认"不判定"策略的漏报规模，决定是否值得为高频前缀补语料。

### 3.4 验收标准（阶段 A）

- [x] 12 个缺口名字全部有 isCallable/arglist 实测结论并回灌（语料 or verified_facts）。
- [x] `validate_skill_api.py --check` 基线下降或持平（35 → 7，剩余对应真实不可调用条目）。
- [x] 全语料对账清单归档（`.artifacts/iscalable-matrix-17.2-S048-full.json` 与 `.artifacts/arglist-reconciliation-17.2-S048.json`），verified_facts 当前为 42 条 S048 事实，其中 37 条 verified。
- [x] `validate_facts.py --check` 已确认增长基线不回退（42 facts / 37 verified；历史基线仍为 31 / 26）。
- [x] 越界前缀抽样已完成（20 个 `ash*`/`tsel*`/`hi*`，控制项通过，样本均 `isCallable=nil`）；维持“不判定”策略，证据为 `.artifacts/overflow-prefix-real-allegro-17.2-S048.json`。

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

1. **任务集**：`.claude/eval-samples/eval_tasks.json` 当前有 10 个任务，每个带 prompt 与 expected_apis。在 Windows 上把每个任务作为独立会话喂给 cadence-skill-agent（上游 `.agents/skills/cadence-skill-agent` 是规范源）。
2. **收集产出**：agent 生成的 `.il` 按任务 id 命名，落进 `.claude/eval-samples/`。评估 JSON 也保留（先过 `verify_assessment.py`，再进入实现——这是 runbook 强制顺序）。
3. **打分**：

   ```powershell
   python scripts\eval_generation.py --samples eval-samples --report
   ```

   关注四个数字：`hallucination_rate`（unknown-api/文件数）、`arity_warnings`、`keyword_warnings`、`expected_api_missing`（检索失败信号——agent 绕开了文档 API 通常意味着 `search_api.py` 没把任务词映射到正确符号）。
4. **真实门收尾**：每份产出走完整 Windows 门（isCallable 守卫确认 → 裸 Allegro S048 `allegro.exe -s` 的 `load`/调用 smoke；可用时再通过独占 Allegrobridge S048 进程调用 `sklint ?checkPubFuncs t ?outputFile ...` → `load` → smoke/qtest），lint 文本原样回馈修复轮；本轮已完成裸 Allegro 10/10 load/call，另实测确认 bridge 入口可达，显式 `loadContext(skillDev.cxt)` 返回 `t` 且 `axlLicFeatureExists("skillDev")` 返回 `t`，但 bridge PCB 路径的 SkillDev 状态未签出，且直接 `il_allegro` 路径也缺少 `cdsFuncs.cxt`，因此完整 public-context lint 门仍 incomplete；本机没有独立 `sklint` 可执行文件时不得用静态检查冒充该门。
5. **闭环回灌**：
   - `expected_api_missing` 非空 → 给 `eval_retrieval.py` 的 CASES 加用例（query=任务措辞，expected=agent 最终实际用对的符号），跑 `--check` 看现有排序是否命中；不命中就调 `search_api.py` 再重录基线。这是检索质量随真实使用增长的机制。
   - Windows 门发现而离线校验器没发现的缺陷（比如 arity 在真实平台更宽松/更严）→ 修校验器或落 verified_facts，两边基线重录。
6. **扩任务集**：3 个任务太少。从真实工作里每完成一个 SKILL 需求就沉淀一个任务（prompt + expected_apis + 干净参考实现），样本数只增不减（`--check` 会拦缩水）。

验收：≥10 个真实任务样本；hallucination_rate 保持 0；每次检索 MISS 都有对应新 eval 用例。

---

## 6. 阶段 C：LSP 在真实编辑器 + 真实代码上的验证

`skill_lsp.py` 是 stdio JSON-RPC 壳（diagnostics/hover/completion 全复用离线原语），协议层已有 24 个单测，编辑器集成与真实代码两维验证均已有本手册中的独立证据。

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
   - [x] 打开含已知缺口 API（如 `axlXSectionAssign`，阶段 A 回灌前）的文件 → 出 unknown-api error 诊断，消息含 isCallable 逃生口；**回灌后同一文件诊断消失**（这是语料↔诊断闭环的直接证明）。
   - [x] hover 在 `axlDBFindByName` 上 → 签名 + `source:line` + 描述摘要。
   - [x] 输入 `axlDb` 触发补全 → 出现 `axlDbidName` 等，detail 是文档签名；同时修正了大小写不敏感候选截断导致的不可见问题，并加入回归测试。
   - [x] 编辑（didChange）后诊断实时刷新；关文件（didClose）诊断清空。
   - [x] 大文件（>2000 行）不卡顿——2101 行真实语料探针无诊断，当前测得约 36ms；校验仍是全文件重跑，后续若规模增大再评估增量缓存 `collect_local_names`。

   精确清单的协议级证据归档于 `.artifacts/lsp-checklist-real-2026-09-11.json`；VS Code 1.137.0 extension-host 的单进程全清单证据仍见 `.artifacts/vscode-skill-lsp-smoke/stage-c-clean-real-2026-09-11.json`。
3. **严重度分层复核**：诊断的 error/warning 语义与 Windows 门冲突时（LSP 说 unknown-api、真机 isCallable=true），**以 Windows 为准**，走 §4 回灌。这条写进了 runbook，LSP 永远不是权威。
4. **交叉验证记录**：把 LSP 诊断与阶段 A 的 isCallable 矩阵对一遍——理想状态是 LSP 的 error 集合 ⊆ isCallable=false ∪ 语料缺口。有出入就是校验器或探针的 bug。

---

## 7. 优化 backlog（按优先级）

| # | 项目 | 触发条件 / 说明 |
|---|---|---|
| 1 | 语料缺口回灌（§3.2 的 12 名字） | 已完成；校验器基线由 35 降至 7，剩余为真实不可调用条目 |
| 2 | 全语料 isCallable/arglist 对账（§3.3） | 已完成；112 条 S048 来源/运行时/契约记录已裁决，另 3 条标为 runtime-boundary、4 条标为 context-dependent，293 条按特殊编码分类；无剩余未裁决的文档范围落在实测范围内记录 |
| 3 | `eval_retrieval.py` 用例扩容 | 已完成本轮扩容；从 32 增至 38 个任务意图用例，三项指标均提升，后续真实会话继续只增不减 |
| 4 | sklangref 两个超页文件重分页 | 已完成；新增 `scripts/repage_sklangref.py`，仅在顶层 API 标题处重组并切分。当前 `funcprog.part01.md`=12985、`inputoutput.part01.md`=13466，`build_reference_indexes.py --check` 不再报告分页安全线 warning；索引、manifest 与 Claude 副本已自动重建并校验 |
| 5 | 越界前缀（dbc*/tsel*/ash*）覆盖决策 | 已完成；20 个 `ash*`/`tsel*`/`hi*` 实际语料样本在真实 S048 中均 `isCallable=nil`，控制项有效，因此维持“不判定”策略，不扩充公共 API 语料 |
| 6 | LSP 增量诊断 | 已完成触发条件评估；独立实测 2101 行文件 `didChange` 约 28ms，当前无可感知诊断延迟，暂不引入增量缓存 |
| 7 | 评估门接入 CI | 已完成；Python 3.10 job 执行 verifier 单测，并校验 `.agents/.../tests/fixtures/assessment-smoke.json` 与规范语料索引一致 |
| 8 | OrCAD 侧质量栈 | 索引悬空门已接入 CI（5100 scanned / 4569 unique rows）；OrCAD 的“validate_skill_api 等价物”（TCL 调用点校验）尚未建，待出现真实 TCL 需求再做 |

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
Day 2  §5 阶段 B：当前已有 10 个真实 Allegro smoke 样本、离线生成门全净；3 个独立 Claude agent 会话已完成静态/API/真实 Allegro 闭环
Day 2  §6 阶段 C：LSP stdio 与跨运行 extension-host 观察已完成；11:11 已用隔离版安装资源完成单进程全清单验收
Day 3+ §7 backlog 按触发条件滚动推进（#4、#5 已完成）；具备完整 `cdsFuncs.cxt` 的 SkillDev 安装或 UNIX 环境后重跑 sklint 真实门，每个真实需求继续沉淀为 eval-samples 新任务
```

每一步的"完成"都以对应门禁 `--check` 绿灯 + 基线重录为准，不以"看起来跑过了"为准。
