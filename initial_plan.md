# `python_server.il` → SKILL++ `.ils` 迁移实施计划

## 基线与计划落盘

- 实施基线锁定为 `ast-refactor@2982805e8303`。
- 当前用户 WIP 为 `sync-allegrobridge.sh`；实施开始及每阶段审核前重新执行 `git status --short`，所有既有 WIP 均不得修改、暂存或提交。
- 最终计划的唯一落盘位置为 `tmp/python-server-ils-migration-plan.md`。当前 Plan Mode 禁止写文件；退出 Plan Mode 后，第一步先将本计划原样写入该路径，再修改代码。
- 每阶段完成后停止，提交文件清单、`git diff`、检查结果、覆盖率、已知风险及下一阶段范围；仅在用户明确批准后继续。不创建 commit、PR 或兼容分支。

## 已纠正的关键结论

- 不保留 `python_server.il` compatibility loader；原文件直接原子改名为 `.ils`。
- 不在 classic `.il` 中先实现 per-child closure。SKILL 动态作用域不能让异步 callback 持有局部 buffer；也不引入马上会被删除的全局 buffer registry。
- qcover 必须先支持 whole-file `.ils` 插桩，但不实现 scope stack；统一使用 `file::lexical#N` 即可。
- lexical unbound 使用 `boundp('result theEnvironment())` 检测，不使用附件中无效的 `_unbound` sentinel。
- warning 捕获必须保存、替换并恢复 SKILL 全局 `woport`；普通 lexical `let((woport ...))` 无效。
- callback child ID 保持现有 `equal/==` 比较，不改为未经验证的 `eq`。
- 当前 `pyproject.toml` 没有 `skillbridge` package-data。新增精确条目：

```toml
skillbridge = [
    "py.typed",
    "server/python_server.ils",
]
```

- rename、加载路径、测试、文档、MANIFEST、package-data 和 `.gitattributes` 必须在同一原子阶段完成。
- 不修改 Python serializer、`RemoteVariable`、Remote symbol 命名或 wire protocol。当前分支其他 Python wire 变化属于既有提交，不纳入迁移。

## Golden contract

公开兼容范围只包括以下六个 callable；原有 `pyStartServer.*`、`pyRunScript.logName`、`pyShowLog.logName`、`pyReloadServer.filename` function properties 明确定义为内部实现，不继续暴露。

| API | 必须保持的签名与行为 |
|---|---|
| `pyStartServer` | `@key id="default", logLevel="INFO", singleMode=nil, timeout=nil, python="python", forceTcp=nil, "ttggtg"`；成功 `t`，已运行或启动失败 `nil` |
| `pyKillServer` | 无参数；未运行返回 `nil`，否则请求停止并返回 `t` |
| `pyRestartServer` | 无参数；未运行时直接启动；运行中保持 restart/RST 语义 |
| `pyReloadScript` | 请求停止旧 server、加载当前 `.ils`、返回 `t`；不自动启动；旧 closure 不得执行 late data |
| `pyShowLog` | `@optional length=20, "x"`；保留校验、输出和返回值 |
| `pyRunScript` | `script @key python="", args=nil, block=nil, "ttlg"`；非阻塞返回 child handle，阻塞返回 `ipcWait` 结果 |

协议 golden：

- 请求仍是 newline-terminated classic SKILL expression，并显式使用 `evalstring(line 'il)`。
- server 输出仍为 `STX/NAK/RST + payload + RS`。
- script 输出仍为 `success <payload>\n` 或 `failure <payload>\n`。
- blank line 忽略；CR 仅在已完成 CRLF 行尾删除。
- 未收到 `\n` 不执行；`pyRunScript` child 结束时丢弃未终止 tail。
- `nil` → `None`；missing table entry → `error('unbound')`。
- warning 仍包装为 `warning(<warning>, <value>)`。
- Remote/Table/Vector 继续使用 `gensym + set` 写入 SKILL global value slot；kill、restart、reload 均不清理这些 symbols。

## Golden code reference

以下片段是规范实现，不得恢复为附件中的双层 lambda 参数、property `setq` 或 sentinel 方案。

### 流式拆行

```skill
(setq feedLines
  (lambda (buffer data)
    (letseq ((remaining (strcat buffer data))
             (lines nil)
             (newlineTail (index remaining "\n"))
             (lineLength 0)
             (line ""))
      (while newlineTail
        (setq lineLength
          (difference
            (strlen remaining)
            (strlen newlineTail)))

        (when
          (and
            (greaterp lineLength 0)
            (equal
              (substring remaining lineLength 1)
              (strcat (intToChar 13))))
          (setq lineLength (difference lineLength 1)))

        (setq line
          (if
            (greaterp lineLength 0)
            (substring remaining 1 lineLength)
            ""))

        (setq remaining
          (or (substring newlineTail 2) ""))

        (when
          (greaterp (strlen line) 0)
          (setq lines (cons line lines)))

        (setq newlineTail (index remaining "\n")))

      (list (reverse lines) remaining))))
```

### Warning 与 lexical unbound

```skill
(setq captureWarnings
  (lambda (thunk)
    (letseq ((tempPort (outstring))
             (oldWoport nil)
             (captured ""))
      (unless tempPort
        (error "cannot create warning port"))

      (setq oldWoport (symeval 'woport))

      (unwindProtect
        (progn
          (set 'woport tempPort)
          (funcall thunk)
          (warn "")
          (getWarn)
          (setq captured
            (or (getOutstring tempPort) "")))
        (progn
          (set 'woport oldWoport)
          (close tempPort)))

      captured)))

(setq evaluateLine
  (lambda (line)
    (let ((result nil)
          (completed nil)
          (failurePayload nil)
          (capturedWarning "")
          (pythonCode nil))
      (setq capturedWarning
        (funcall captureWarnings
          (lambda ()
            (setq completed
              (errset
                (setq result
                  (evalstring line 'il))))
            (unless completed
              (setq failurePayload
                (lsprintf "%L" errset.errset))))))

      (cond
        ((null completed)
         (list 'failure failurePayload))

        ((not
           (boundp 'result (theEnvironment)))
         (list 'success "error('unbound')"))

        (t
         (setq pythonCode
           (funcall skillToPython result))

         (when
           (and
             (not (equal capturedWarning ""))
             (not
               (equal capturedWarning "*WARNING* ")))
           (setq pythonCode
             (lsprintf
               "warning(%L, %s)"
               capturedWarning
               pythonCode)))

         (list 'success pythonCode))))))
```

`errset.errset` 必须在 warning flush 或其他 cleanup 前复制。warning 字节结果仍须经过 Allegro 17.2 gate。

### qcover qualification fixture

```skill
(letseq ((counter 0)
         (hidden nil))
  (setq hidden
    (lambda (value)
      (if value
          (progn
            (setq counter (add1 counter))
            'yes)
          'no)))

  (defglobalfun qcoverFixtureCall (value)
    (funcall hidden value))

  (defglobalfun qcoverFixtureCount ()
    counter))
```

## Phase 0：锁定 qcover 契约

仅添加 qcover `.ils` qualification fixture 和红灯测试，不修改 qcover 或生产 server。

- 固定现有 classic fixture 的 9 个 decision／18 个 branch outcomes。
- 新 fixture 验证 lexical closure、`defglobalfun`、quoted branch-shaped data、condition 单次执行及 closure 在 load 返回后仍有效。
- 增加 malformed `.ils`、source identity、reset 后重载和临时文件 cleanup 的预期测试。
- 记录当前失败，证明 post-load `getFunctions/pp/getd/putd/loadstring(... 'il)` 无法覆盖 private lexical closure。
- Windows 当前基线应重新运行；历史 `python_server.il` 的 `62/62` 只能作为参考，不冒充本次验证。

审核通过后才进入 Phase 1。

## Phase 1：实现最小 `.ils` qcover

只修改 qcover 基础设施、fixture、对应开发文档和 `.gitignore`，生产 server 保持 `.il`。

- `qcover::load` 按精确扩展名分派：
  - `.il` 完全保留现有 post-load 插桩。
  - `.ils` 使用 `infile + lineread` 读取全部 logical forms；不得使用只读首个 form 的 `linereadstring`。
- transformer 只进入 `lambda` 和 `defglobalfun` 的函数体；不登记 outer module 初始化分支，也不推断匿名 lambda 名称。
- 每个 `.ils` 文件设置 `_currentFunction = 'lexical`，decision ID 为 `original-file::lexical#N`。
- 用 `pprint` 将 transformed forms 写入同目录、唯一且以 `.ils` 结尾的 `.qcover-*` 文件，再用 `load` 加载，从而保留 `get_filename(piport)` 的目录深度。
- 临时文件保留到 `qcover::reset`，支持 instrumented `pyReloadScript`；自动 Windows runner 已在 `TemporaryDirectory` 的仓库副本中运行。
- 从 AST 收集 `defglobalfun` exports，在 instrumented load 前保存原 function slots。reset 时：
  1. 恢复这些 pre-load global slots；
  2. 恢复 classic definitions；
  3. 删除 qcover 拥有的临时文件；
  4. 清空 counters 和 registry。
- 不 reload 原始 `.ils`，避免再次执行模块顶层副作用。
- `qcover::load` 继续累计多个文件；只有显式 `qcover::reset` 清状态。
- 加入 `**/.qcover-*.ils` crash-residue ignore。
- 明确 qcover `.ils` 只支持可写 source sibling、串行 qtest；不宣称支持只读 wheel 路径。

验收：

- classic fixture 仍为 `18/18`。
- lexical fixture 达到 100%。
- malformed load 恢复 `debugMode`、global slots、端口和临时文件。
- `get_filename(piport)` 目录正确。
- reset 后重载无旧 counters/temp。
- Allegro 17.2 实际运行通过后停审。

## Phase 2：测试先行的原子 `.ils` 迁移

本阶段先提交红灯证据，随后在同一审核单元完成生产迁移；不在旧 `.il` 中建立临时 buffer registry。

### 生产结构

- `git mv skillbridge/server/python_server.il skillbridge/server/python_server.ils`。
- 单一 outer `letseq` lexical module：
  - immutable `_filename`、`_moduleFolder`、log paths、STX/NAK/RST/RS；
  - private DPL `_state`，仅含 `ipc/id/logLevel/singleMode/timeout/python/forceTcp/restartPending/requestIpc/receiveBuffer/acceptData`；
  - private feed/evaluate/serialize/spawn/callback helpers；
  - 不增加 `state` 字段、class、Backend、registry 或多文件 package。
- DPL 写入使用 `_state->field = value`。
- 保留四个 global test seams：
  - `__pyIpcBeginProcess`
  - `__pyIpcKillProcess`
  - `__pyIpcWriteProcess`
  - `__pyIpcWait`
- 六个公开入口使用 `defglobalfun` 捕获 lexical state。
- server 和 `pyRunScript` 均复用 `feedLines/evaluateLine`。
- `pyRunScript` 每次调用创建独立 callback closure 和 buffer。
- server callback 用 `acceptData && equal(id _state->ipc)` 过滤。
- `requestIpc` 必须由 `unwindProtect` 清理。
- reload 在 kill/load 前把旧 `_state->acceptData` 设为 `nil`；新模块保持 stopped，用户需重新调用 `pyStartServer`。
- spawn 成功后才启用 `acceptData`；finish 清理当前 handle，stale finish 不修改新 state。
- serializer 递归传 lexical function object，不再引用 quoted private function symbol。
- 所有 Remote symbol 创建继续使用 global `set`。

### 行为测试

重构 `tests/skill/test_server.ils`，通过 fake IPC seam 从 `pyStartServer/pyRunScript` 捕获 callback，再直接 `funcall`；不暴露 private helper。

覆盖：

- 六个公开入口及其参数、返回值。
- server partial line、split CRLF、blank line、同 chunk 多行。
- 两个 interleaved script child 的独立 tail。
- child ID 复用、finish 后旧 tail 不进入新 child。
- 非阻塞/阻塞 `pyRunScript`。
- `nil`、unbound、inner caught error、outer uncaught error。
- warning 包装及连续请求无泄漏。
- request 内 restart 的 RST、finish 后恰好一次 spawn。
- stale data/finish callback。
- reload late-data 拒绝、六个新 public globals 仍 callable、无自动 spawn。
- serializer/write 抛错时 `requestIpc` 仍清理。
- `pyShowLog` 通过 load 前设置 `SKILLBRIDGE_LOG_DIRECTORY` 测试，不恢复 function-property test hook。
- qcover 达到新 `.ils` 文件 100% branch coverage。

### 原子影响面

与 rename 同时更新：

- 三个运行时路径消费者：`skillbridge/__main__.py`、`allegrobridge/__main__.py`、`allegrobridge/allegro.py`。
- qtest 和三个 Python 路径/复制测试。
- `MANIFEST.in` 精确包含 `python_server.ils`。
- `pyproject.toml` 新增精确 `skillbridge` package-data，不保留 `server/*.il`。
- `.gitattributes` 增加 `*.ils text eol=lf`。
- `quickstart.md`、`architecture.md`、`architecture.svg` 和 `allegrobridge/PLAN.md` 的有效路径。
- `.agents/MEMORY.md` 中 `python_server.il 62/62` 是历史验证记录，保留不改。
- README 和 installation 当前没有旧路径，不做无意义修改。

旧名检查使用：

```bash
rg -n --pcre2 'python_server\.il(?!s)' \
  skillbridge allegrobridge tests docs README.md \
  MANIFEST.in pyproject.toml .gitattributes
```

结果必须为零；不能使用会把 `.ils` 也误判为命中的普通 `git grep 'python_server\.il'`。

## Phase 3：本地发布验收

不扩展实现，只处理 Phase 2 暴露的直接问题。

- 运行相关 qcover/qtest 的已记录 Windows结果；本机无法运行的项目明确标注。
- 运行：

```text
poetry run pre-commit run --all-files
poetry run mkdocs build --strict
python -m build
```

- wheel 和 sdist 必须包含：
  - `skillbridge/server/python_server.ils`
  - `skillbridge/py.typed`
- wheel 和 sdist不得包含 `skillbridge/server/python_server.il`。
- 在全新 venv 安装 wheel 后运行：
  - `skillbridge path`
  - `python -m allegrobridge path`
- 两条命令打印的 `.ils` 路径必须存在；项目并没有 `allegrobridge` console script，因此不测试不存在的 `allegrobridge path`。
- 保存构建文件清单、安装输出和全部检查结果后停审。

## Phase 4：Windows Allegro 17.2 硬门

使用新 Allegro 进程、唯一 workspace ID/端口和测试仓库副本。

- `load(".../python_server.ils")`，不使用 `loadi`。
- 对六个 public globals 执行 `isCallable`，必要时用 `arglist` 核对签名。
- 运行 `sklint`，启用 public-function 检查并保存原始输出。
- 真实 `ipcBeginProcess` smoke 必须证明：
  - lexical data/finish function object 被异步保留和调用；
  - callback 返回后仍持有 lexical buffer；
  - child ID/exit status 正确。
- 运行 `tests/skill/run.ils`，要求零失败且 100% branch coverage。
- 运行 Python Allegro integration：
  - connect 与普通 scalar/list/DPL/Table/Vector/Remote RPC；
  - fragmented 和并发 `pyRunScript`，分别覆盖 `block=nil/t`；
  - warning、nil、unbound、inner/outer error；
  - restart RST 与 epoch 自动重连；
  - restart 前创建的 RemoteTable/RemoteVector 在重连后仍可访问；
  - reload 后旧 closure late data 不执行，新模块保持 stopped，手动 start 可恢复；
  - stale callbacks 不产生 duplicate spawn。
- 不把 DBID 或 open-file handle 加入稳定性硬门。
- 退出后确认无遗留 Python child、Allegro child 或监听端口。
- function-object callback 若在真实 17.2 失败，本阶段判定 blocked；不自动加入 global adapter fallback，须重新审核设计。

## 明确不做

- RemoteRegistry、release/generation API 或 Remote symbol cleanup。
- JSON/tagged wire、Python `eval()` 移除或 serializer redesign。
- Server/Backend class、对象系统、多实例、多文件 server package。
- global callback compatibility adapter。
- reload 自动重启或新的 lifecycle API。
- client Remote API、`.pyi`、Agent 检索路线或 Allegro transaction 扩展。
- 任何对实施开始时既有用户 WIP 的修改。