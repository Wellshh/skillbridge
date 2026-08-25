## 总体建议

基于 `skillbridge` 实施时，不要让业务代码直接依赖 `Workspace`、`RemoteObject` 和任意字符串 SKILL。更稳妥的目标架构是：

> **skillbridge 通信内核 + Allegro 原子事务边界 + DTO 化 Python SDK + 轻量级内存会话。**

`skillbridge` 已经具备三个很有价值的基础：Python/SKILL 类型转换、远程对象属性访问，以及 Windows 下的 localhost TCP 通道；它的 `Workspace` 甚至已经预留了 `axl` 函数集合。 

当前通信内核已经具备帧收发、严格串行执行、Windows timeout、超时后响应排空、SKILL callback 缓冲和写请求不自动重发。Python/SKILL 单次 RPC 事务、savepoint batch 与 dry-run 也已通过 Windows Allegro 实机验收。`Allegro` 窗口生命周期和最小内存 `Session` 门面已经落地；下一阶段从 board 开始建立严格校验的只读领域 API。CLI 启动已出现旧 listener 被误认作新实例的真实故障，因此允许使用仅在本地启动阶段回读的实例 nonce；它不进入 RPC envelope，不承担认证、授权或请求去重。除此之外，在没有真实需求或故障证据前，不引入 UUID envelope、安全 token、结果缓存或更多恢复状态。

---

# 架构共识决议（2026-08 架构对齐）

| 维度 | 决策方案 | 实施准则 |
| :--- | :--- | :--- |
| **1. Session 架构 (Phase 4)** | **轻量级内存会话 (In-Memory `Session`)** | 仅聚焦于所有权、连接代际 (`generation`) 与生命周期。**暂不引入 SQLite 持久化和应用级逆向 Undo 日志**，保持架构极简与敏捷。 |
| **2. 只读查询与协议记录 (Phase 5)** | **纯 RPC + SKILL 单次投影 + Pydantic 严格验收** | SKILL 一次投影返回 DPL/list，沿用现有 Translator 解码；Python 仅在 `client/api` 信任边界严格校验，不增加第二套序列化。**仅在实测出现帧或性能瓶颈时才增加 Bulk 通道**。 |
| **3. 领域写操作与批处理 (Phase 6)** | **单写即时原子 + `with session.batch():` 延迟复合事务** | 单个写方法（如 `components.move()`）立即发起单次 RPC 原子提交；多操作组合时支持客户端上下文管理器收集指令，退出上下文时编译为单个 SKILL 复合事务一次性提交（All-or-Nothing）。 |
| **4. 交互冲突策略 (Active Command)** | **严格非侵入式 (Fail-Fast)** | 若 Allegro 正忙（`axlOKToProceed` 为 `nil`），立即抛出 `BUSY_ACTIVE_COMMAND`，**绝不自动发送 done/cancel 中断用户前台交互**，保障人工设计安全。 |
| **5. SDK 入口与命名空间** | **分层封装 (`Allegro` + `Session`)** | 顶层统一从 `allegrobridge` 导出 `Allegro` 与 `Session`；领域 API 位于 `allegrobridge.client.api`，底层裸 `Workspace` 收敛在 `session.raw` 下供高级调试使用。 |

---

# 一、目标架构

```text
┌───────────────────────────────────────────────────────────┐
│ Python 应用 / 自动化脚本 / Agent                           │
├───────────────────────────────────────────────────────────┤
│ Allegro Domain SDK                                        │
│ board / components / symbols / nets / layers / properties │
│ 返回不可变 DTO，不暴露裸 DBID                               │
├───────────────────────────────────────────────────────────┤
│ In-Memory Session                                         │
│ 代际跟踪 (generation)、batch 批处理收集、领域服务分发       │
├───────────────────────────────────────────────────────────┤
│ Raw Workspace Adapter (`session.raw`)                     │
│ 基于 skillbridge 的函数调用、类型转换、RemoteObject          │
├───────────────────────────────────────────────────────────┤
│ TCP Protocol                                               │
│ 127.0.0.1 / Unix socket + 现有长度帧                      │
├───────────────────────────────────────────────────────────┤
│ Python Relay Process                                       │
│ Allegro 通过 ipcBeginProcess 启动                           │
│ Pipe 串行执行 + reader thread                              │
├───────────────────────────────────────────────────────────┤
│ Allegro SKILL Bridge                                       │
│ 通用 py* server + Allegro 专属 __abRunTransaction         │
├───────────────────────────────────────────────────────────┤
│ Allegro AXL-SKILL API                                      │
│ axlDBGetDesign / axlDBTransaction* / 其他 axl*              │
└───────────────────────────────────────────────────────────┘

按需旁路通道（仅在超大数据瓶颈时启用）：
Allegro SKILL ──写 CSV/TSV 临时文件──> Python Bulk Reader
```

这里数据流分为主要 RPC 路径与按需 Bulk 路径：

**RPC 路径**为默认路径，用于控制、小结果查询、全量 DTO 列表拉取和写操作（例如读取板信息、查询/投影元件列表、移动器件、保存设计）。

**Bulk 路径**为按需扩展，仅在千万级图形或大属性导出证明现有 RPC 帧通道成为瓶颈时引入。优先通过 SKILL 内部投影避免逐个 `RemoteObject` 查询造成的 N+1 往返。

---

# 二、必须坚持的设计原则

| 原则 | 实施方式 |
|---|---|
| Allegro 命令严格串行 | 复用现有 `Pipe` 执行锁 |
| 写操作必须具有事务边界 | 一次 RPC 内开启事务，成功 commit，失败 rollback |
| 写操作绝不盲目重试 | 传输失败直接报错，不重发同一命令 |
| 业务 API 不暴露 DBID | 对外返回 `ComponentInfo`、`NetInfo` 等 DTO |
| 大列表不逐项访问 | 在 SKILL 内一次投影，写入共享临时文件 |
| 事务优先于 Undo | 第一版先保证 Commit/Rollback，原生 Undo 后做 |
| 不自动结束用户当前命令 | Allegro Busy 时返回 `BUSY_ACTIVE_COMMAND` |
| 保存必须显式调用 | 修改操作不隐式 `save` |
| Raw eval 默认关闭 | 只在调试模式开放任意 SKILL |
| 同一 Allegro 实例一个 session | 多实例通过不同端口和 session 文件区分 |
| DBID 具有代际 | 换板、删除、Undo 后旧 handle 必须失效 |

Cadence 的数据库对象通过 DBID 操作；DBID 会随设计变化，对象删除或 AXL-SKILL 上下文结束后也可能变成 out-of-scope，因此不能把它当作跨设计、跨生命周期的永久标识。

---

# 三、当前项目边界

保留现有两层，不提前拆分 `protocol/`、`transport/`、`bulk/` 或多个领域包：

```text
skillbridge/                 # 现有通信、编码与远程对象内核
allegrobridge/
├── allegro.py               # Allegro 窗口生命周期
├── client/
│   ├── session/             # Session 生命周期门面
│   ├── api/                 # 按实际交付逐个增加领域 API 与协议记录
│   ├── workspace.py         # Allegro Workspace 与 transaction 原语
│   └── translator.py        # Allegro 函数名映射
└── server/
    ├── __init__.py
    └── allegro_server.il     # Allegro 专属 SKILL 扩展
```

通用 `skillbridge/server/python_server.il` 不得引用任何 `axl*` API。`allegro_server.il` 作为库扩展被加载，不是独立用户命令，因此不需要为内部 procedure 额外注册 `axlCmdRegister`。该 `.il` 文件必须加入 wheel package-data，并增加 wheel 内文件存在性测试。

`client/api` 不预先创建空模块；board、components、nets 依次随首个真实方法落地。每个模块同时保存该领域的 API 对象、少量公开返回记录和模块级校验器，避免横向拆成 models/schemas/serializers/service 层。LGPL-3.0 许可与归属继续保留。

---

# 四、当前基线与延后项

## 1. `skillbridge/server/python_server.py`

长度帧精确读取、`sendall()`、`Pipe` 串行化、reader thread timeout 与 SKILL callback 缓冲已完成。下面 1.1～1.4 保留为当前基线的设计记录，不再作为后续阶段。

### 1.1 已实现 `recv_exact`

旧实现曾直接：

```python
length = self.request.recv(10)
```

TCP 不保证一次 `recv(10)` 返回 10 字节。应改为：

```python
def recv_exact(sock: socket.socket, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size

    while remaining:
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionError(f"Connection closed with {remaining} bytes remaining")
        chunks.append(chunk)
        remaining -= len(chunk)

    return b"".join(chunks)
```

当前长度头和 payload 都通过 `Socket.recv()` 精确读取。

### 1.2 已将所有响应改为 `sendall`

旧 server 使用 `send()` 返回长度和内容，可能出现部分发送。

改成：

```python
self.request.sendall(f"{len(result):10}".encode("ascii"))
self.request.sendall(result)
```

### 1.3 已串行化 SKILL pipe

当前 `ThreadingTcpServer` 的多个 handler 会共用：

```text
stdout → Allegro
stdin  ← Allegro
```

这是一个单工序列通道，不能并发。

当前由 `Pipe.execute()` 的执行锁统一保证串行，不再新增第二个 dispatcher 抽象。早期方案曾设想：

```python
class ExecutionDispatcher:
    def __init__(self, pipe_reader: PipeReader) -> None:
        self._lock = threading.RLock()
        self._pipe_reader = pipe_reader
        self._state = ServerState.READY

    def execute(self, request: RpcRequest) -> RpcResponse:
        with self._lock:
            ...
```

即使允许多个 TCP 客户端连接，真正进入 Allegro 的请求仍然必须严格串行。

MVP 可以先直接强制：

```skill
pyStartServer(?singleMode t)
```

### 1.4 已用 reader thread 实现 Windows timeout

旧实现在 Windows 上会进入阻塞的 `stdin.readline()`。

改成：

```python
class PipeReader(threading.Thread):
    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.queue: queue.Queue[str | BaseException] = queue.Queue()

    def run(self) -> None:
        try:
            for line in sys.stdin:
                self.queue.put(line.rstrip("\r\n"))
        except BaseException as exc:
            self.queue.put(exc)

    def read(self, timeout: float) -> str:
        item = self.queue.get(timeout=timeout)
        if isinstance(item, BaseException):
            raise item
        return item
```

注意：Python timeout 并不能中断 Allegro 内部正在运行的 SKILL。因此发生超时后不能立刻执行下一条请求。

推荐状态机：

```text
STOPPED
   ↓
STARTING
   ↓
READY → EXECUTING → READY
             │
             └── timeout → DRAINING → DEGRADED
                                      │
                                      └── recover + ping → READY
```

`DRAINING` 或 `DEGRADED` 时拒绝任何新写请求。

### 1.5 按需再加 request ID 和结果缓存

当真实应用需要在断线重连后去重时，请求才需要带 UUID：

```json
{
  "version": 1,
  "request_id": "6e00d828-97e9-4e39-bb93-e27a6dc04cf4",
  "operation": "call",
  "function": "ABGetBoardInfo",
  "args": [],
  "timeout_ms": 5000,
  "mutation": false
}
```

relay 缓存最近 128～512 个结果：

```python
result_cache[request_id] = response
```

同一 request ID 重复到达时直接返回缓存结果，避免重复执行。

但如果 relay 本身重启，而 Allegro 操作可能已经提交，则不能自动重试写操作，应返回：

```text
UNKNOWN_COMMIT_STATE
```

---

## 2. `skillbridge/client/channel.py`

当前 channel 可在断线后重建连接，但不会自动重发已发送的 payload，已满足事务写操作的最小要求。只有真实需要只读自动重试时，才考虑引入：

```python
class RetryPolicy(Enum):
    NEVER = "never"
    IDEMPOTENT_ONLY = "idempotent_only"
```

请求对象明确标识：

```python
request.mutation
request.idempotent
```

规则：

```text
只读 + idempotent → 可以在握手后重试一次
写操作             → 绝不自动重发
未知执行状态       → UNKNOWN_COMMIT_STATE
```

此外，客户端也要使用 `recv_exact(10)`，不能直接假设一次 `recv(10)` 得到完整长度头。当前客户端存在相同问题。

---

## 3. `skillbridge/client/translator.py`

当前 `_skill_value_to_python()` 使用 Python `eval()`。

第一版不必立即重写整个 SKILL serializer，可以用 Python AST 白名单解析，兼容现有：

```text
Remote(...)
Symbol(...)
warning(...)
error(...)
list
dict
number
string
None
True
False
```

禁止：

```text
属性访问
import
lambda
推导式
任意函数调用
下标表达式中的执行逻辑
```

结构可以是：

```python
_ALLOWED_CALLS = {
    "Remote": create_remote,
    "Symbol": Symbol,
    "warning": create_warning,
    "error": create_error,
}
```

解析过程使用 `ast.parse(..., mode="eval")`，逐节点解释，不直接执行。

只有安全边界需要开放给不可信输入时，才进一步引入 AST 白名单或 tagged JSON。

---

## 4. `skillbridge/server/python_server.il`

这个文件继续作为 Cadence 宿主无关的通用内核，不直接调用 `axlDBTransaction*` 或任何其他 Allegro AXL API。它只负责：

- `ipcBeginProcess`
- 单行 command 执行
- 成功/失败返回
- Python/SKILL 类型转换
- RemoteObject 保存
- server 启动、停止和重启生命周期

不复制、重命名或 fork 该文件；`allegrobridge` 通过独立 extension 在其上叠加 Allegro 能力。

---

## 5. `allegrobridge/server/allegro_server.il`

该文件只存放 Allegro 专属 procedure，统一使用 `__ab*` 内部前缀。当前已实现：

```text
__abRunTransaction(command)
__abRunSavepointBatch(commands)
__abRunDryTransaction(command)
```

不在本阶段增加第二套 start/stop/restart、callback、serializer、handle table 或 capability 系统。

### 5.1 加载责任

CLI 模式的 startup script 按顺序执行：

```skill
skill load(".../skillbridge/server/python_server.il")
skill load(".../allegrobridge/server/allegro_server.il")
skill pyStartServer(...)
```

在 `allegrobridge.Workspace._create_workspace()` 完成 Allegro 宿主探测后，对 Allegro Workspace 检查上述三个 procedure 是否都可调用；缺失时调用 `load()`，然后再次检查。加载或复核失败时，关闭刚创建的 workspace 再抛出错误。Virtuoso 等非 Allegro 宿主仍返回通用 Workspace，不加载该扩展。

不覆写 `Workspace.open()`：该方法已有实例缓存，`_create_workspace()` 只在缓存未命中时执行，使扩展初始化天然只发生一次。CLI 模式也经过这一复核，因此 startup script 加载失败不会被误报为就绪。`Workspace.transaction` 门面只调用已加载的 procedure，不在每次写操作前部署文件。

### 5.2 包装与路径

`allegrobridge/server/__init__.py` 作为资源定位点；Python 从已安装包的 `__file__` 定位同目录 `.il` 文件，转为 `/` 分隔的绝对路径再交给 SKILL。`pyproject.toml` 的 package-data 与 `MANIFEST.in` 都必须包含 `allegrobridge/server/allegro_server.il`，分别保障 wheel 和 source distribution。

---

## 6. `allegrobridge/client/workspace.py` 与 `translator.py`

`Workspace` 继承自 `skillbridge.client.workspace.Workspace`，并绑定了专用的 `allegrobridge.client.translator.Translator`。

### 6.1 `axl*` 函数名与缩写映射（已实现）

对于 `axlDBGetDesign`、`axlCNSGetSpacing`、`axlUIPopupDefine` 等带有大写缩写的 Allegro AXL 函数名，如果直接使用默认规则可能无法得到正确的驼峰命名。

当前已通过 `allegrobridge/util.py` 和 `allegrobridge/client/translator.py` 实现完整映射方案：

1. **真实 API 资源清单**：`allegrobridge/assets/api_names.txt` 包含了 792 个真实 Cadence Allegro `axl*` 函数；
2. **规范化 Lookup 字典**：`build_snake_to_axl_map()` 启动时通过正则拆分 token，构建双向映射表：
   - 领域+动作：`"db_get_design"` → `"axlDBGetDesign"`
   - 完整蛇形：`"axl_db_get_design"` → `"axlDBGetDesign"`
   - 原名直通：`"axlDBGetDesign"` → `"axlDBGetDesign"`
3. **透明拦截转换**：`Translator.format_function_name()` 优先从 `_SNAKE_TO_AXL` 查表匹配，支持 `ws.axl.db_get_design()`、`ws.axl.axl_db_get_design()` 与 `ws["axlDBGetDesign"]()` 无缝调用。

```python
# 示例调用
design = ws.axl.db_get_design()  # 自动解析为 axlDBGetDesign
spacing = ws.axl.cns_get_spacing()  # 自动解析为 axlCNSGetSpacing
```

不过高层 API（Phase 5/6 领域 SDK）仍将调用专有的固定过程或 DTO 函数，而不是让业务层直接分散调用底层的数百个裸 `axl*` 函数。

---

## 7. `skillbridge/client/objects.py`

现有 `RemoteObject` 支持：

```python
obj.attribute
obj["ExactAttribute"]
obj.attribute = value
dir(obj)
```

这些能力对 Allegro DBID 很有价值。 

但需要增加两个概念。

### 7.1 Session generation

每次打开、关闭或切换 `.brd` 时：

```python
session.generation += 1
```

RemoteObject 保存创建时的 generation：

```python
if self.generation != session.generation:
    raise StaleHandleError(...)
```

### 7.2 Handle 释放

现有 SKILL serializer 会把 remote object 保存到全局变量中，长期运行后会不断积累。

新增：

```python
remote.close()
session.release_all_handles()
```

SKILL 侧使用统一 handle table：

```text
ABHandleTable[id] = dbid
```

而不是无限生成全局变量。

高层 SDK 则完全不暴露 RemoteObject，避免大部分 handle 生命周期问题。

---

# 五、实施阶段

## Phase 0：建立 fork 和基线

目标：不改行为，只确认 skillbridge 在开发环境可构建。

实施：

1. Fork `unihd-cag/skillbridge`。
2. 保存 `upstream/master`。
3. 创建 `allegro-main`。
4. 修改项目名称为 `allegro-skillbridge-core` 或迁入新 namespace。
5. 在 Windows 上运行纯 Python 测试。
6. 保存原有 LGPL 许可证和 attribution。
7. 固定一个 upstream commit，不直接跟随浮动 master。

验收：

```text
Python 单元测试通过
Windows TCP mock 测试通过
wheel 可以安装
CLI 可以打印 SKILL 文件位置
```

---

## Phase 1：在目标 Allegro 版本完成原始 PoC

先不做架构重构，直接验证 skillbridge 的核心 IPC 是否能在目标 Windows Allegro 中工作。

在 Allegro SKILL prompt 中：

```skill
load("C:/path/to/skillbridge/server/python_server.il")

pyStartServer(
    ?id "7777"
    ?singleMode t
    ?python "C:/path/to/.venv/Scripts/python.exe"
)
```

Python：

```python
from skillbridge import Workspace

ws = Workspace.open("7777")

assert ws["plus"](1, 2) == 3

design = ws["axlDBGetDesign"]()
print(design.obj_type)

components = design.components
print(len(components))
```

Allegro 的 `axlDBGetDesign()` 返回 design DBID，数据库对象通过 `->` 读取属性；`components` 是所有逻辑组件，而 `symbols` 主要对应已放置 symbol，并可能包含机械、格式类 symbol，因此你的 Python API 中必须将两者分开定义。 

PoC 验收标准：

```text
1. 1+2 返回 3
2. 能获取 design objType
3. 能读取 components 数量
4. 能读取 nets 数量
5. 连续执行 1,000 次 ping 无乱序、无挂死
6. 停止 server 后可以重新启动
7. Allegro 无鼠标操作时 callback 仍持续工作
```

若第 5～7 项失败，应先停止后续 API 开发，集中解决 Windows IPC callback 和 pipe 处理。

---

## Phase 2：双端原子事务（已完成）

目标：让一条可能修改 Allegro 数据库的 SKILL command，在单次 RPC 内要么全部成功，要么全部回退。

状态：基础原子事务、savepoint batch 和 dry-run 已完成 Python/SKILL 封装，并已通过 Windows Allegro 真实数据库验收。

### 2.1 SKILL 端事务包装

在 `allegrobridge/server/allegro_server.il` 增加 `__abRunTransaction(command)`，接收单条 SKILL expression 字符串：

```text
mark = axlDBTransactionStart()
事务启动失败          → 返回 failure
errsetstring(command) 成功 → axlDBTransactionCommit(mark)
command 解析或执行出错  → axlDBTransactionRollback(mark)，返回 failure
commit 失败              → 尝试 rollback，返回 failure
rollback 也失败        → 同时报告原错误和 rollback failure
```

`errsetstring()` 成功时返回包含执行结果的列表，因此 command 正常返回 `nil` 不能被误判为失败。执行出错时必须在 rollback 前保存 `errset.errset`，不能用统一的“transaction rolled back”丢失原始 SKILL 错误。

Cadence 事务 mark 不得跨 Allegro command 保留。Start、command、Commit/Rollback 必须全部在这一次 SKILL 调用内完成；打开或保存设计也不得放入该事务。

### 2.2 Python 端委托

在 Allegro `Workspace` 提供最小能力：

```python
result = ws.transaction(SkillCode("axlDBChangeSomething(...)"))
preview = ws.transaction.preview(SkillCode("axlDBChangeSomething(...)"))
results = ws.transaction.batch([SkillCode("command1()"), SkillCode("command2()")])
```

这是 Raw Workspace 的底层原语，不是面向业务代码的写操作 API。后续领域 API 仍应调用固定 SKILL procedure，并在内部复用该事务边界。

`Workspace.transaction` 返回绑定的 `Txn` 门面：

1. `ws.transaction(command)` 调用 `__abRunTransaction`，保持全有或全无语义。
2. `ws.transaction.preview(command)` 调用 `__abRunDryTransaction`，成功执行后仍回滚。
3. `ws.transaction.batch(commands)` 调用 `__abRunSavepointBatch`，返回逐项结果；空列表直接返回 `[]`。

不在 Python 端暴露 `begin()` / `commit()` / `rollback()`，因为那会让远程 transaction 跨越多次 RPC，违反 Allegro 的事务生命周期。

### 2.3 TDD 实施顺序

1. 先新建 `tests/skill/test_allegro_server.ils`，覆盖 transaction start、commit、rollback、原错误保留和 `nil` 结果，并接入 `tests/skill/run.ils`。
2. 实现 `allegro_server.il`，并达到该文件 statement/branch 100% coverage。通用 `test_server.ils` 不引入 Allegro transaction 测试。
3. 在 Python 单元测试中先定义 `Workspace.transaction()` 的委托行为，以及 CLI 预加载、`_create_workspace()` 缺失时加载、已加载时不重复加载、非 Allegro 不加载和加载失败清理连接的行为。
4. 增加 wheel 包含 `allegrobridge/server/allegro_server.il` 的打包测试。
5. 最后在 `tests/allegrobridge/test_integration.py` 用真实 Allegro 数据库验证扩展自动加载、commit 与 rollback。

### 2.4 验收

```text
只读 command 可正常返回值
返回 nil 的 command 仍 commit
单个写 command 成功后 commit
写入后主动抛出 SKILL error，数据库恢复到执行前
语法错误不留下部分修改
transaction start/commit 失败时不返回假成功
原始 SKILL 错误不被 rollback 提示覆盖
CLI 和 manual 模式都能加载扩展，且已加载时不重复 load
传输中断后客户端不自动重发写 command
```
---

### 2.5 Transaction 模式扩展

基础 transaction 通过 Windows qtest/qcover 验证后，已增加两个独立能力；`__abRunTransaction(command)` 继续保持全有或全无语义：

| API | 语义 | 持久化条件 |
| :--- | :--- | :--- |
| `__abRunSavepointBatch(commands)` | 逐项保存点，允许部分成功 | 只有 outer mark 最终 commit 后，成功项才持久化 |
| `__abRunDryTransaction(command)` | 试运行 | 无论 command 成功或失败都 rollback |

#### 2.5.1 Savepoint batch

`__abRunSavepointBatch(commands)` 的固定时序：

1. 调用 `axlOKToProceed()`；忙碌时返回 `BUSY_ACTIVE_COMMAND`，不结束用户命令。
2. 创建 outer mark；失败则终止 batch。
3. 每个 command 创建 inner mark：
   - `errsetstring()` 成功（包括返回 `nil`）：commit inner，记录 success。
   - command 失败：先保存 `errset.errset`，再 rollback inner，记录 failure 并继续。
   - inner commit 失败：尝试 rollback inner；成功则记录该项 failure 并继续。
   - inner start 或 rollback 失败：事务栈已不可信，rollback outer 并终止整个 batch。
4. 全部项处理后 commit outer。若失败，尝试 rollback outer 并让整个 batch 失败；之前记录的 success 不得视为已持久化。

只在 outer commit 成功后返回每项纯数据结果：

```text
[
  {index, status: "success", value},
  {index, status: "failure", error}
]
```

inner commit 只结束当前嵌套层，不代表最终提交。空 `commands` 由 Python 客户端直接返回 `[]`，不发送 RPC。

#### 2.5.2 Dry run

`__abRunDryTransaction(command)` 的固定时序：

1. 检查 Allegro 空闲并创建 mark。
2. 用 `errsetstring()` 完整执行 command。
3. command 失败时，先保存原错误，再 rollback 并返回 failure。
4. command 成功时也必须 rollback；只有 rollback 成功后才返回预演 DTO。
5. rollback 失败时返回 `DRY_RUN_ROLLBACK_FAILED`，不返回误导性预演结果。

预演 DTO 只能包含数字、字符串、布尔、列表和 DPL。新建 DBID 必须在 rollback 前投影为数量、类型、名称、位置等稳定数据，不得返回 rollback 后已失效的 raw DBID。

database transaction 不会回滚 SKILL 全局变量、文件 IO、selection set 或 DRC 开关。dry-run command 必须避免这些外部副作用，或使用 `unwindProtect` 恢复。

通用 wrapper 不自动统计或刷新 DRC。领域 preview procedure 可按需将 DRC 数据写入 DTO：`axlDRCGetCount()` 可能返回过期计数；需要准确全板检查时，必须将高成本的 `axlDRCUpdate(nil)` 作为显式选项，并恢复原 `axlDBControl('drcEnable)` 状态。

#### 2.5.3 性能与验收

- Savepoint batch 每项增加一次 start 和 commit/rollback，复杂度为 O(n)；只用于确实需要 partial success 的场景。
- Dry-run 后若正式应用，同一操作会执行两遍；这是显式预演成本，不自动运行全板 DRC。
- qtest/qcover 覆盖每项 success、`nil`、command failure、inner commit failure；inner start/rollback failure 触发 outer rollback；outer commit/rollback failure；dry-run success/error/rollback failure；以及 cleanup 前保存 `errset.errset`。
- Windows Allegro 集成测试使用 board 副本验证：savepoint batch 只保留成功项，atomic batch 仍全部回滚，dry-run 前后数据库对象数和属性完全一致，DTO 不含 DBID，执行后 server 仍可响应。

不增加 `axlDBTransactionMark/Oops`、自动 retry、自动 cloak 或 DRC 自动刷新。Python 侧通过 `ws.transaction.batch()` 和 `ws.transaction.preview()` 暴露两种独立语义，不给原子 `ws.transaction()` 增加模式参数。

---

## Phase 3：Allegro 窗口生命周期（已完成）

目标：统一表示手动打开或由 Python 启动的 Allegro 窗口。

`Allegro.open(mode="manual" | "cli")`、上下文管理、CLI 路径探测、startup script 与 `Workspace.open()` 接续已完成并通过 Windows 实机验收。

```python
from allegrobridge import Allegro

with Allegro.open(mode="manual", workspace_id="7777") as allegro:
    assert allegro.workspace["plus"](1, 2) == 3
```

- `manual` 模式只断开 Workspace 连接；
- `cli` 模式还负责优雅终止自己拉起的 Allegro 进程；
- `Allegro` 直接保存已打开的 `Workspace`，不绕过公开连接流程读取私有缓存。

---

## Phase 4：In-Memory Session 与 Raw Workspace Adapter（已完成）

目标：保留 skillbridge 的底层灵活性，但将其安全收敛在明确的底层接口。

第一步只包装现有对象，不重写通信接口：

```python
with Allegro.open(mode="manual", workspace_id="7777") as allegro:
    session = allegro.session
    assert session.raw is allegro.workspace
```

- `Session` 持有 `Allegro`，`raw` 直接返回其 `Workspace`，关闭语义保持幂等。
- `generation` 先表示当前连接代际；等实际增加换板或重连 API 时，再在那个共享边界递增。
- 不新增 `raw.call()` / `raw.eval()` / `raw.load_file()` 包装；现有 `Workspace` 已覆盖这些底层能力。
- 不实现 batch DSL、handle table、心跳或能力握手。

---

## Phase 5：严格只读领域 API（下一阶段）

目标：让 `Session` 提供 Pythonic 领域命名空间，通过固定 SKILL 投影一次返回稳定数据，并在 Python 边界用 Pydantic 严格识别协议漂移。Pydantic 只负责校验，不替换现有 Translator，也不承担 JSON 序列化。

### 5.1 目录与依赖边界

按真实交付顺序增加模块，首个垂直切片只需要 `board.py`：

```text
allegrobridge/client/api/
├── __init__.py       # 只显式导出已经实现的公开 API/记录
├── _record.py        # 唯一共享的严格、不可变 Pydantic 基类
├── board.py          # BoardApi + BoardInfo
├── components.py     # 第二步：ComponentsApi + ComponentInfo
└── nets.py           # 第三步：NetsApi + NetInfo
```

不创建独立的 `models/`、`schemas/`、`serializers/`、`requests/` 或 `responses/`。一个领域的 API 和返回记录放在同一模块；symbols/layers/properties 等模块等到首个真实方法出现再创建。

当前项目声明 Python `>=3.8`，而新的 Pydantic 版本已经提高 Python 下限。实施前必须在同一提交中明确二选一：保留 Python 3.8 时锁定仍支持它的 Pydantic v2 版本；或先正式提高项目 Python 下限。不得加入在声明支持版本上无法安装的依赖。

### 5.2 协议校验：少量记录，不造第二套序列化

```python
from pydantic import BaseModel, ConfigDict, TypeAdapter


class _Record(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid", frozen=True)


class BoardInfo(_Record):
    path: str
    units: str
    component_count: int
    symbol_count: int
    net_count: int
    session_generation: int


_BOARD_INFO = TypeAdapter(BoardInfo)
```

约束如下：

- 固定 `__ab*` procedure 返回 DPL 或 list-of-DPL；继续由现有 Translator 转成 `dict` / `list`。
- 每个投影在同一次 SKILL 求值内先用 `axlDBRefreshId(axlDBGetDesign())` 取得当前 design，再遍历其子 DBID 并立即投影为纯值；不得把 `components`、`nets` 等子 DBID 跨 RPC 当作稳定快照，也不得在 Python 端逐个刷新这些远程 handle。
- 每个公开返回实体最多一个小型 Pydantic record；列表直接复用模块级 `TypeAdapter(list[ComponentInfo])`，不增加 list wrapper/root model。
- `TypeAdapter` 在模块加载时创建并复用，API 方法只调用 `validate_python(..., strict=True)`。
- 缺字段、额外字段或错误标量类型都视为协议错误；不使用 field validator 做隐式兼容或字符串/数字强转。
- `nil` 在当前 Translator 中表示 `None`，无法同时稳定表达布尔 `False`。会丢失语义的二态字段使用明确的字符串 `Literal`，`None` 只表示缺失；字段 wire 形式必须先经真实 Allegro 验证。
- 不调用 `model_dump()` / `model_dump_json()`，不增加 JSON round-trip、请求 envelope、响应 envelope 或通用 `OperationResult`。
- 校验失败统一在 API 边界转成一个 `AllegroProtocolError`，附带 procedure 名并以原始 `ValidationError` 为 cause；业务异常和现有 transaction 异常继续按异常抛出。

公开方法参数优先依靠类型标注和 Python 签名；只有参数确实来自不可信调用边界且包含非平凡约束时，才使用 `@validate_call(config=ConfigDict(strict=True))`。不为每个方法创建 request model，也不为内部 helper 添加装饰器。

### 5.3 Session 命名空间与语法糖

复用 `FunctionCollection` / `RemoteFunction` 已有的调用风格，避免 `.list()` / `.get()` 样板：

```python
board = session.board()
components = session.components(include_unplaced=True)
r101 = session.components["R101"]
gnd = session.nets["GND"]
```

- `Session.board`、`components`、`nets` 使用 `cached_property` 返回轻量 API 对象，并由它们调用 `session.raw` 下的固定 `__ab*` procedure。
- `Api.__call__()` 表示该领域的默认查询；`__getitem__()` 表示按稳定业务 key 精确取一个对象。
- 不实现 `__iter__()`、`__len__()` 或会隐藏 RPC 的数据 property，避免看似本地的表达式意外触发远程 IO。
- records 不保存 DBID、`RemoteObject`、Workspace 或 Channel；记录包含创建时的 `session_generation`，需要长期保存时由调用方自行决定。
- 底层调试仍使用 `session.raw`；领域 API 不接受任意 SKILL 字符串。

### 5.4 实施顺序

1. `BoardApi.__call__() -> BoardInfo`：建立最小 `_Record`、协议错误和一个 `__abProjectBoard` 投影，完成 Python + Windows Allegro 垂直验收。
2. `ComponentsApi.__call__()` / `__getitem__()`：单次 SKILL 遍历返回所有稳定字段，禁止逐项 RemoteObject 查询。
3. `NetsApi.__call__()` / `__getitem__()`：沿用相同边界；只有这三个模块稳定后再评估 symbols/layers/properties。

Bulk 文件通道、通用分页器、缓存、handle table 和 capability negotiation 均不属于首批 API；只有实测数据证明单次投影无法满足帧大小或性能要求时再设计。

### 5.5 测试门槛

- 所有领域 API、record 与协议边界测试统一放在 `tests/allegrobridge/test_integration.py`，不创建 `test_api.py`。
- 现有 `TestApi` 只保留连接、Session 和 transaction 基础设施验收；领域测试分别进入 `TestBoardApi`、`TestComponentsApi`、`TestNetsApi`，以后也按一个领域一个测试类扩展。
- 每个领域类覆盖正确 payload、缺字段、额外字段、错误类型、冻结行为、调用/索引语法、固定 procedure、单次 RPC 与协议异常。
- Windows CLI 实机测试验证 `session.board()`，随后逐步增加 components/nets；断言结果类型、稳定字段和无 DBID。Unix manual 环境只执行只读行为，不修改用户已打开的设计。
- 实机 expected 必须通过独立的单次 `evalstring` 生成纯值快照；不得从跨 RPC 的 `RemoteObject` 子 DBID 构造 expected，也不得用 `or ()` 等容错掩盖意外 `nil`。
- 新增 Python 模块 statement/branch 双 100%；SKILL 投影继续通过 qtest/qcover 和 Windows 实机运行门槛。
- 不测试 Pydantic 自身的 JSON 序列化，因为该层不使用它。

---

## Phase 6：领域写操作与批处理（混合模式）

写操作必须通过固定的 Allegro SKILL procedure，复用 Phase 2 已验证的单次 RPC 事务边界。

### 6.1 混合提交模型

1. **单写即时原子提交**：
   调用单个方法（如 `session.components.move()`）时，立即作为单个独立的 RPC 事务执行并自动 Commit：
   ```python
   result = session.components.move(
       refdes="R101",
       x=120.0,
       y=45.0,
       rotation=90.0,
   )
   ```
2. **延迟复合批处理（`with session.batch():`）**：
   多操作组合时，通过客户端上下文管理器在本地收集指令列表，在退出 context 时一次性编译为一个复合 SKILL 事务下发（All-or-Nothing）：
   ```python
   with session.batch("place decouple capacitors") as batch:
       batch.components.move("C101", x=120.0, y=45.0, rotation=90.0)
       batch.components.move("C102", x=125.0, y=45.0, rotation=90.0)
       batch.properties.set(object_kind="component", object_key="C101", name="FIXED", value=True)
   # 退出 context 时：自动在单个 axlDBTransaction 内部顺序执行以上三条指令
   # 全部成功则 Commit；任何一条失败则整批回滚，并在 Python 端抛出对应异常
   ```

3. **三种事务模式对应 API**：

| Python API | 用途 | 事务与提交行为 |
| :--- | :--- | :--- |
| `session.batch()` | 原子批处理 (Atomic) | 未来将多个领域操作编译为一条 command，任一失败则整批 Rollback |
| `ws.transaction(command)` | 原子单命令 (Atomic) | 已实现；单次 RPC 内 Commit 或 Rollback |
| `session.savepoint_batch()` | 容错批处理 (Savepoint) | 未来委托 `ws.transaction.batch()`；成功项在 outer Commit 时持久化 |
| `session.dry_run()` | 试运行预演 (Dry-run) | 未来委托 `ws.transaction.preview()`；始终 Rollback，仅返回稳定 DTO |

### 6.2 交互冲突策略（Fail-Fast）
写操作发出前，底层通过 `axlOKToProceed()` 检查 Allegro 状态：
* **严格非侵入（Fail-Fast）**：若 Allegro 处于交互命令阻塞中（返回 `nil`），立即抛出 `BUSY_ACTIVE_COMMAND` 异常。
* **绝对不强行中断**：绝不擅自发送 `done` / `cancel` 或 `axlCancelEnterFun`，确保人工交互与自动化脚本安全隔离。

### 6.3 原生 Undo
第一版先聚焦并保证事务级别的 Commit 与 Rollback。后续需要接入 Allegro 原生 Undo 栈的高频宏命令，再通过 `axlCmdRegister(?cmdType "interactive" ?undo t)` 独立注册。

---

## Phase 7：按需加固通信层

只在实际部署、故障注入或长时间运行暴露了明确问题时，才增加对应机制：

```text
需要跨网络访问       → token 与连接安全
需要在断线后去重     → request ID 与有界结果缓存
需要协议独立升级       → protocol version
发现现有恢复能力不足 → status / recover 管理命令
发现大结果存在性能瓶颈 → bulk 文件通道
```

---

# 六、Python 对外接口设计

顶层只导出生命周期对象；领域 API 与协议记录从 `allegrobridge.client.api` 显式导出：

```python
from allegrobridge import Allegro, Session
from allegrobridge.client.api import BoardInfo, ComponentInfo

with Allegro.open(mode="manual", workspace_id="7777") as allegro:
    pcb: Session = allegro.session
    assert pcb.raw is allegro.workspace

    board: BoardInfo = pcb.board()
    components: list[ComponentInfo] = pcb.components(include_unplaced=True)
    r101: ComponentInfo = pcb.components["R101"]

    # Phase 6：成功返回更新后的记录，失败抛出现有事务或领域异常
    updated: ComponentInfo = pcb.components.move(
        refdes="R101",
        x=120.0,
        y=45.0,
        rotation=90.0,
    )

    with pcb.batch("align filter capacitors") as batch:
        batch.components.move("C101", x=120.0, y=45.0)
        batch.components.move("C102", x=125.0, y=45.0)
```

公开语义保持简单：

- 查询一个对象返回 record，查询集合返回 `list[record]`，无对象时按方法契约返回 `None` 或抛出明确的 not-found 异常。
- 写操作成功时返回更新后的领域 record，纯命令成功时返回 `None`；失败使用现有异常链，不包装 `ok/value/error`。
- savepoint batch 只有在“部分成功”本身是业务语义时才返回逐项结果，不把这种特殊结构推广到所有 API。
- `Session.raw` 是唯一 raw escape hatch；高级调用者继续使用现有 `Workspace`、`RemoteFunction.lazy()`、`var()` 和 transaction API。

---

# 七、能力握手（延后）

当前 Allegro 探测已经由 `Workspace.open()` 的轻量握手完成。Phase 5 不增加 `ABGetCapabilities()`、`ABGetSessionInfo()` 或 capability Pydantic model。

只有真实支持多个不兼容的 AllegroBridge server 版本时，才设计最小的版本/capability 响应；届时同样使用一个严格 record 校验，不在业务层散布版本判断。

---

# 八、日志和审计（延后）

Phase 5 沿用现有 Python/SKILL 日志，不增加 request ID、idempotency key、JSONL 审计模型或日志目录。API 边界只补充 procedure 名和校验失败上下文，且默认不记录完整 SKILL 源码。

只有 Agent 实际执行写操作并产生可审计需求时，才根据部署环境设计最小审计事件；审计协议与领域查询 record 分开，不提前污染 `client/api`。

---

# 九、测试方案

## API 测试结构与数据库隔离

所有领域 API 测试集中在 `tests/allegrobridge/test_integration.py`，沿用现有真实 `Allegro` fixture，不在其他文件复制 Workspace mock 或领域断言：

```text
TestApi             连接、Session、transaction 基础设施
TestBoardApi        session.board() 与 BoardInfo 协议
TestComponentsApi   session.components() / [refdes]
TestNetsApi         session.nets() / [name]
```

测试方法按行为命名，不按实现函数逐项镜像；共享 fixture 只负责资源生命周期，不在 fixture 中隐藏业务断言。

### 事务隔离边界

不得实现跨测试 RPC 的 `isolate_db` transaction-mark fixture：

```python
mark = ws['axlDBTransactionStart']()
yield
ws['axlDBTransactionRollback'](mark)
```

Allegro 会在当前 SKILL command 结束时取消仍活动的 transaction，transaction mark 不能跨 Allegro commands 保存。fixture 的 Start、测试内 API 和 finally Rollback 分属不同 RPC，因此不能提供函数级回滚保证；即使简单场景偶然通过，也不能作为隔离契约。

采用资源所有权清晰的两级隔离：

1. **只读 API**：继续使用 class-scope `allegro` / `ws` / `session`。Windows 每个测试类复制一次 `shape1.brd` 并启动自己的 CLI Allegro；Unix manual 只连接现有 server，测试不得写设计。
2. **写 API**：使用 function-scope `isolated_session`。每个测试复制新的 `shape1.brd`、启动独立 CLI Allegro、执行测试，并由 context manager 关闭进程后丢弃副本。它只在 Windows CLI 环境运行，不接触 manual 用户窗口。
3. **事务语义**：一次写操作自身仍必须通过固定 `__ab*` procedure 在单 RPC 内 start/commit/rollback。rollback 与 dry-run 用“调用前快照 == 调用后快照”验证；commit 用预期字段变化验证。
4. **失败清理**：不论断言、API 还是 teardown 抛错，`Allegro` context 都必须关闭 Workspace 和自己启动的进程。源 `allegrobridge/assets/shape1.brd` 从不直接打开。

建议 fixture 形态：

```python
@pytest.fixture(scope='class')
def session(allegro: Allegro) -> Session:
    return allegro.session


@pytest.fixture
def isolated_session(tmp_path: Path) -> Iterator[Session]:
    if platform != 'win32':
        pytest.skip('write API isolation requires a disposable Windows Allegro window')
    board = Path(copy2(_TEST_BOARD, tmp_path))
    with Allegro.open(mode='cli', board=board) as allegro:
        yield allegro.session
```

不增加自动 restore fixture：对临时 board 做恢复没有价值，对 manual 用户 board 则不安全。需要在同一测试中继续观察 rollback 后状态时，显式采集前后快照；其余隔离由 disposable board/process 保证。当前 Allegro integration suite 使用固定 workspace id，必须串行运行；只有实际引入并行执行时再分配独立 id。

### API 类的最小覆盖矩阵

每个 `Test<Category>Api` 只覆盖四类边界：

```text
默认调用或集合查询      -> 返回严格 record / list[record]
__getitem__ 精确查询    -> 命中与 not-found 语义
协议不匹配              -> 缺字段、额外字段、错误类型转 AllegroProtocolError
数据库写入（Phase 6）   -> fresh isolated_session 上验证 commit/rollback
```

协议错误分支允许在同一测试文件中用最小 stub 注入畸形 DPL 解码结果；不需要为每个字段排列组合，也不测试 Pydantic 自身。因为 `tests/allegrobridge/conftest.py` 会把整个文件标记为 `allegro`，这些测试只在显式 `--allegro` 时运行，这是“所有 API 测试集中为集成测试”的已知成本。

## Python 单元测试

覆盖：

```text
函数名映射
Workspace.transaction() 的命令编码
transaction 成功结果解码
transaction rollback failure 转为 Python 异常
transaction.preview() 委托 dry-run
transaction.batch() 委托 savepoint batch，空列表不发 RPC
CLI startup script 先加载 core，再加载 Allegro extension
Allegro Workspace 初始化时缺失 extension 则加载，已存在时不重复加载
非 Allegro Workspace 不加载 extension
extension 加载失败时关闭新建连接
wheel 包含 allegro_server.il
写命令传输失败后不重发
```

## Mock SKILL 测试

沿用 skillbridge 现有 mock 思路。项目已有 TCP/Unix channel、类型转换、RemoteObject 和 reconnect 测试，可继续扩展。 

增加：

```text
transaction start 成功/失败
command 返回值或 nil
command 语法错误
command 执行中抛错
commit 成功/失败
rollback 被调用且原错误传回 Python
savepoint batch 的单项失败与 outer transaction 失败
dry-run 成功、command 失败与 rollback 失败
```

## Allegro Windows 集成测试

准备一个固定小型 `.brd`：

```text
2 个已放置元件
1 个未放置元件
3 个网络
若干 pin/via/shape
至少一个用户属性
```

用例：

```text
连接和断开
CLI 和 manual 模式都可调用 __abRunTransaction
事务内只读 command 返回值
写入成功后 commit
写入后强制 SKILL error，数据库无变化
读取 board info
读取 placed/unplaced component
读取 net
用户处于交互命令时写操作返回 BUSY
端口冲突
Python 路径含空格
设计路径含空格和中文
```

## 压力验收

以下只在进入 Phase 7 通信加固时作为验收，不阻塞当前 transaction 实现：

```text
10,000 次顺序 ping：0 次错位
1,000 次 board info：0 次死锁
100 次强制 rollback：数据库差异为 0
100 次 server stop/start：状态可恢复
连续运行 8 小时：handle 和内存无持续线性增长
大型结果：不经过 1 MB RPC 通道
```

---

# 十、推荐里程碑和工作量

以下按一名熟悉 Python、具备基础 SKILL 经验的工程师估算。

| 里程碑 | 内容 | 典型工作量 |
|---|---|---:|
| M0 | 原始 skillbridge 在 Windows Allegro 跑通（已完成） | 2–4 天 |
| M1 | Python/SKILL 原子 transaction、savepoint batch 与 dry-run（已完成） | 2–4 天 |
| M2 | Allegro 窗口生命周期（已完成） | 2–4 天 |
| M3 | 轻量 `Session` 与 Raw Workspace 入口（已完成） | 1–2 天 |
| M4 | board/components/nets 严格只读 API（下一阶段） | 1–2 周 |
| M5 | 第一批领域写操作 | 1–2 周 |
| M6 | 按需增加批处理、Undo 或通信加固 | 按实际需求评估 |

当前进入 M4，先交付 `session.board() -> BoardInfo` 的单个端到端切片，再依次增加 components 和 nets。不为尚未出现的部署需求预估通信生产化工期。

---

# 十一、第一版建议冻结的范围

第一版只交付：

```text
Windows 本机连接
Allegro.open() 的 cli/manual 生命周期
Allegro Workspace 与真实 API 名映射
allegro_server.il 与通用 python_server.il 分层加载
单次 RPC 原子 transaction
成功 commit，SKILL error rollback
savepoint batch 部分成功语义
dry-run 执行后强制 rollback
写 command 传输失败后不自动重发
```

第一版暂不交付：

```text
跨机器远程控制
多个并发 Allegro writer
鼠标和 UI 自动化
自动结束用户交互命令
完整布线 API
完整 Constraint Manager API
所有写操作原生 Undo
任意 Agent 默认执行 raw SKILL
RPC UUID envelope、安全 token、请求去重、结果缓存
doctor、常驻配置和自动修改 allegro.ilinit
bulk 文件通道
```

最合理的执行顺序是：用现有实机集成测试保持 Phase 1–4 基线，然后实施 **Phase 5 的 `session.board()` 严格协议切片**。只有测试或真实使用暴露通信问题时，才进入 Phase 7 加固对应部分。
