## 总体建议

基于 `skillbridge` 实施时，不要让业务代码直接依赖 `Workspace`、`RemoteObject` 和任意字符串 SKILL。更稳妥的目标架构是：

> **skillbridge 通信内核 + Allegro 专用 RPC 适配层 + DTO 化 Python SDK + 串行执行器 + 大数据文件通道。**

`skillbridge` 已经具备三个很有价值的基础：Python/SKILL 类型转换、远程对象属性访问，以及 Windows 下的 localhost TCP 通道；它的 `Workspace` 甚至已经预留了 `axl` 函数集合。 

但不能原样用于生产。当前 Windows server 不支持超时；TCP 收发存在“假设一次 `recv` 就拿到完整长度头”的问题；多线程 TCP handler 共用一条 Allegro stdin/stdout 管道；客户端还会在断线后自动重连并重发请求；响应解析使用了 Python `eval()`。这些都必须先加固。    

---

# 一、目标架构

```text
┌───────────────────────────────────────────────────────────┐
│ Python 应用 / 自动化脚本 / Agent                           │
├───────────────────────────────────────────────────────────┤
│ Allegro Domain SDK                                        │
│ board / components / symbols / nets / layers / geometry   │
│ 返回 DTO，不返回裸 DBID                                    │
├───────────────────────────────────────────────────────────┤
│ AllegroSession                                             │
│ 单写者锁、超时状态机、事务批次、幂等键、能力检查             │
├───────────────────────────────────────────────────────────┤
│ Raw Workspace Adapter                                      │
│ 基于 skillbridge 的函数调用、类型转换、RemoteObject          │
├───────────────────────────────────────────────────────────┤
│ TCP Protocol                                               │
│ 127.0.0.1 + 长度帧 + JSON envelope + token                 │
├───────────────────────────────────────────────────────────┤
│ Python Relay Process                                       │
│ Allegro 通过 ipcBeginProcess 启动                           │
│ ExecutionDispatcher + PipeReader + Result Cache            │
├───────────────────────────────────────────────────────────┤
│ Allegro SKILL Bridge                                       │
│ ABOnData / ABEval / ABGetCapabilities / ABRunTransaction   │
├───────────────────────────────────────────────────────────┤
│ Allegro AXL-SKILL API                                      │
│ axlDBGetDesign / axlDBTransaction* / 其他 axl*              │
└───────────────────────────────────────────────────────────┘

另一路：
Allegro SKILL ──写 CSV/TSV 临时文件──> Python Bulk Reader
```

这里分为两条数据路径。

**RPC 路径**用于控制、小结果查询和写操作，例如读取板信息、查询一个元件、移动一个器件、保存设计。

**Bulk 路径**用于大量元件、网络、引脚、图形和属性导出。当前 skillbridge 默认最大传输长度是 1,000,000 字节，大型 PCB 很容易超过；而逐个 RemoteObject 查询会造成严重的 N+1 往返。 

---

# 二、必须坚持的设计原则

| 原则 | 实施方式 |
|---|---|
| Allegro 命令严格串行 | 所有请求进入单一 `ExecutionDispatcher` |
| 写操作绝不盲目重试 | 超时后返回 `UNKNOWN_COMMIT_STATE` |
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

# 三、推荐项目结构

不要继续沿用 `skillbridge` 包名作为最终业务包名。建议新建独立 namespace：

```text
allegro-python-bridge/
├── pyproject.toml
├── README.md
├── src/
│   └── allegro_bridge/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── session.py
│       ├── state.py
│       │
│       ├── protocol/
│       │   ├── framing.py
│       │   ├── messages.py
│       │   ├── errors.py
│       │   └── codec.py
│       │
│       ├── transport/
│       │   ├── tcp_channel.py
│       │   ├── dispatcher.py
│       │   ├── pipe_reader.py
│       │   └── server.py
│       │
│       ├── raw/
│       │   ├── workspace.py
│       │   ├── translator.py
│       │   ├── function_registry.py
│       │   ├── remote_object.py
│       │   └── handles.py
│       │
│       ├── api/
│       │   ├── board.py
│       │   ├── components.py
│       │   ├── symbols.py
│       │   ├── nets.py
│       │   ├── layers.py
│       │   ├── geometry.py
│       │   ├── properties.py
│       │   └── transactions.py
│       │
│       ├── models/
│       │   ├── common.py
│       │   ├── board.py
│       │   ├── component.py
│       │   ├── net.py
│       │   └── operation.py
│       │
│       ├── bulk/
│       │   ├── reader.py
│       │   ├── manifest.py
│       │   └── cleanup.py
│       │
│       └── resources/
│           └── skill/
│               ├── allegro_bridge.il
│               ├── serializer.il
│               ├── session.il
│               ├── transactions.il
│               ├── board.il
│               ├── components.il
│               ├── nets.il
│               ├── geometry.il
│               └── compatibility.il
│
└── tests/
    ├── unit/
    ├── protocol/
    ├── mock_skill/
    ├── windows_integration/
    └── boards/
```

代码来源方面，建议先 fork `skillbridge` 做验证，再把真正需要的核心文件迁入新 namespace。skillbridge 是 LGPL-3.0，fork 和分发时需要保留对应许可与归属。

---

# 四、对 skillbridge 各文件的具体改造

## 1. `skillbridge/server/python_server.py`

这是改造优先级最高的文件。

当前 Windows 路径已经使用 localhost TCP，并尝试启用 `SIO_LOOPBACK_FAST_PATH`，因此可以保留整体方向。 

必须修改：

### 1.1 实现 `recv_exact`

现在代码直接：

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
            raise ConnectionError(
                f"Connection closed with {remaining} bytes remaining"
            )
        chunks.append(chunk)
        remaining -= len(chunk)

    return b"".join(chunks)
```

长度头和 payload 都必须使用 `recv_exact`。

### 1.2 所有响应改为 `sendall`

当前 server 使用 `send()` 返回长度和内容，也可能出现部分发送。

改成：

```python
self.request.sendall(f"{len(result):10}".encode("ascii"))
self.request.sendall(result)
```

### 1.3 删除多线程直接操作 SKILL pipe

当前 `ThreadingTcpServer` 的多个 handler 会共用：

```text
stdout → Allegro
stdin  ← Allegro
```

这是一个单工序列通道，不能并发。

新增：

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

生产版仍建议保留 dispatcher，因为 Python 应用内部也可能多线程调用。

### 1.4 用 reader thread 实现 Windows timeout

当前 Windows 上 `win_data_ready()` 永远返回 `True`，然后进入阻塞的 `stdin.readline()`；项目也明确禁止 Windows timeout。  

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

### 1.5 加 request ID 和结果缓存

请求必须带 UUID：

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

当前 channel 断线时会自动 reconnect，然后重发 payload。对于读取操作通常问题不大，但对于“移动元件、删除图形、保存设计”等写操作，可能造成重复执行。

应改成：

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

长期可以把 SKILL wire format 改成 tagged JSON，但 AST 白名单方案改造量更小，适合第一版生产化。

---

## 4. `skillbridge/server/python_server.il`

这个文件是 Allegro 适配核心。

现有代码已经完成：

- `ipcBeginProcess`
- `evalstring`
- 成功/失败返回
- Python/SKILL 类型转换
- RemoteObject 保存

  

建议复制为：

```text
resources/skill/allegro_bridge.il
```

并把所有 `py*`、`__py*` 前缀改为 `AB*` 或 `__ab*`，避免与其他 Cadence SKILL 工具冲突。

需要增加：

```skill
ABStartServer()
ABStopServer()
ABRestartServer()
ABStatus()
ABOnData()
ABOnError()
ABOnFinish()
ABGetCapabilities()
ABGetSessionInfo()
ABReleaseHandle()
ABReleaseAllHandles()
ABEval()
ABLoadFile()
ABRunTransaction()
```

### 4.1 增加接收缓冲区

当前 handler 使用：

```skill
foreach(line parseString(data "\n") ...)
```

但 `ipcBeginProcess` callback 的 `data` 不应假设永远按完整行切块。

应保留一个全局 buffer：

```text
ABReceiveBuffer = ABReceiveBuffer + data
不断提取完整的 "\n" 行
最后不足一行的部分留到下次 callback
```

具体字符串定位 API 应根据目标 Allegro 版本验证，但设计上必须存在这一层。

### 4.2 禁止直接发送多行代码

Python relay 到 Allegro 的 pipe 只传单行表达式。

多行脚本处理方式：

1. Python 写入临时 `.il` 文件；
2. 将路径中的 `\` 统一为 `/`；
3. 发送单行：

```skill
load("C:/Users/.../temp/request_123.il")
```

Cadence 的 Allegro SKILL 可以在命令行进入 SKILL 环境并加载 `.il`，也可以通过 `axlCmdRegister` 注册命令；Windows 路径建议使用 `/`。

### 4.3 注册管理命令

```skill
axlCmdRegister(
    "ab_start"
    'ABStartServer
    ?cmdType "general"
)

axlCmdRegister(
    "ab_stop"
    'ABStopServer
    ?cmdType "general"
)

axlCmdRegister(
    "ab_status"
    'ABStatus
    ?cmdType "general"
)
```

不要在加载 `allegro_bridge.il` 时无条件自动启动。启动行为应由配置控制，以免每次 Allegro 打开都占用端口。

---

## 5. `skillbridge/client/workspace.py`

`Workspace` 已定义 `axl: FunctionCollection`，但函数名中的大写缩写需要特殊处理。

例如：

```text
axlDBGetDesign
```

不能简单认为 Python 名一定是：

```python
ws.axl.db_get_design()
```

现有转换更可能暴露成带缩写大小写的形式。PoC 阶段直接使用精确函数名：

```python
design = ws["axlDBGetDesign"]()
```

生产版新增 `AllegroFunctionRegistry`：

1. 启动时枚举真实 `axl*` 函数名；
2. 建立规范化 alias；
3. 保留 exact-name escape hatch；
4. 遇到歧义时拒绝自动映射。

例如：

```python
registry.resolve("db_get_design") == "axlDBGetDesign"
registry.resolve("ui_popup_define") == "axlUIPopupDefine"
```

不过高层 API 最好调用你自己的固定函数：

```python
ws["ABListComponents"](...)
```

而不是让业务层直接动态调用数百个 `axl*` 函数。

---

## 6. `skillbridge/client/objects.py`

现有 `RemoteObject` 支持：

```python
obj.attribute
obj["ExactAttribute"]
obj.attribute = value
dir(obj)
```

这些能力对 Allegro DBID 很有价值。 

但需要增加两个概念。

### 6.1 Session generation

每次打开、关闭或切换 `.brd` 时：

```python
session.generation += 1
```

RemoteObject 保存创建时的 generation：

```python
if self.generation != session.generation:
    raise StaleHandleError(...)
```

### 6.2 Handle 释放

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

## Phase 2：通信层生产化

目标：形成可以长时间运行的可靠 RPC 内核。

实施顺序：

1. 实现 `recv_exact()`。
2. 全部 `send()` 改 `sendall()`。
3. 加 `ExecutionDispatcher`。
4. Windows stdin 改 reader thread。
5. 增加请求 UUID。
6. 增加 protocol version。
7. 增加 server state machine。
8. 增加 token 鉴权。
9. 删除写操作自动重发。
10. 加结果缓存和重复 request ID 检测。
11. SKILL callback 加行缓冲。
12. 多行代码统一走临时 `.il` 文件。
13. 加 `ping`、`status`、`recover`。

建议错误码：

```python
class ErrorCode(str, Enum):
    NO_DESIGN = "no_design"
    BUSY_ACTIVE_COMMAND = "busy_active_command"
    SKILL_ERROR = "skill_error"
    TIMEOUT = "timeout"
    UNKNOWN_COMMIT_STATE = "unknown_commit_state"
    STALE_HANDLE = "stale_handle"
    SERVER_DOWN = "server_down"
    PROTOCOL_ERROR = "protocol_error"
    TRANSACTION_ROLLED_BACK = "transaction_rolled_back"
    UNSUPPORTED_CAPABILITY = "unsupported_capability"
```

验收：

```text
10,000 次连续 ping 无错位
故意拆分长度头后仍能正确接收
两个 Python 线程并发调用时 Allegro 端仍严格串行
只读 timeout 后能够 drain + recover
写 timeout 返回 UNKNOWN_COMMIT_STATE
断线不会自动重复执行写操作
非法 token 被拒绝
```

---

## Phase 3：Allegro bootstrap 和生命周期

目标：用户不再手工找文件、输入长命令。

新增 Python CLI：

```text
allegro-bridge init
allegro-bridge path
allegro-bridge doctor
allegro-bridge status
allegro-bridge shell
allegro-bridge config
```

`init` 生成：

```text
%LOCALAPPDATA%/AllegroBridge/config.json
%LOCALAPPDATA%/AllegroBridge/runtime/
%LOCALAPPDATA%/AllegroBridge/logs/
%LOCALAPPDATA%/AllegroBridge/skill/
```

再生成一个 SKILL 配置文件：

```skill
ABPython = "C:/Users/user/project/.venv/Scripts/python.exe"
ABPort = 7777
ABToken = "随机生成的长 token"
ABLogDir = "C:/Users/user/AppData/Local/AllegroBridge/logs"
```

在用户 `allegro.ilinit` 中只保留：

```skill
load("C:/Users/user/AppData/Local/AllegroBridge/skill/bootstrap.il")
```

`bootstrap.il` 再加载：

```text
serializer.il
session.il
transactions.il
board.il
components.il
nets.il
allegro_bridge.il
```

Cadence 支持通过加载 SKILL 文件和 `axlCmdRegister` 将自定义命令注册到 Allegro shell。

`doctor` 至少检查：

```text
Python executable 是否存在
Python 版本
端口是否占用
token 是否存在
SKILL 文件路径
日志目录可写
Allegro bridge 是否可连接
协议版本是否兼容
当前是否打开设计
目标 Allegro 是否具备所需 axl* 函数
```

---

## Phase 4：Raw Allegro Workspace

目标：保留 skillbridge 的灵活性，但放到明确的底层接口。

建议 API：

```python
session.raw.call("axlDBGetDesign")
session.raw.eval("axlDBGetDesign()->nets~>name")
session.raw.load_file(Path("my_script.il"))
session.raw.release_all_handles()
```

`eval()` 默认关闭：

```python
session = AllegroSession.connect(
    port=7777,
    allow_raw_eval=False,
)
```

只有调试环境显式开启：

```python
allow_raw_eval=True
```

Raw 返回类型可以包括：

```text
int
float
str
bool
None
list
dict
Symbol
AllegroRemoteObject
```

但业务层不得直接返回 `AllegroRemoteObject`。

---

## Phase 5：只读领域 SDK

建议第一批实现：

```python
session.board.get_info()
session.board.get_units()
session.board.get_extents()

session.components.list()
session.components.get(refdes)
session.symbols.list()

session.nets.list()
session.nets.get(name)
session.nets.get_connections(name)

session.layers.list()
session.properties.get(...)
```

DTO 示例：

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class ComponentInfo:
    refdes: str
    package: str | None
    component_class: str | None
    placed: bool
    xy: Point | None
    rotation: float | None
    mirrored: bool | None


@dataclass(frozen=True)
class BoardInfo:
    path: str | None
    units: str
    component_count: int
    placed_symbol_count: int
    net_count: int
    session_generation: int
```

不要这样实现：

```python
components = design.components
for component in components:
    print(component.name)
    print(component.symbol.xy)
```

这会产生大量远程对象和 RPC。

应在 SKILL 中一次投影：

```text
foreach component:
    提取 refdes/package/class/symbol/xy/rotation
    写入结果文件
```

然后 Python 一次读取。

建议：

```python
components = session.components.list()
```

内部调用：

```skill
ABExportComponents("C:/.../request-123.csv")
```

响应只返回：

```json
{
  "bulk_ref": {
    "path": "C:/.../request-123.csv",
    "rows": 8243,
    "checksum": "..."
  }
}
```

验收：

```text
有未放置组件时 placed=False
机械 symbol 不混入 components
10,000 个对象不会产生 10,000 次 RPC
大型设计结果不受 1 MB 限制
换板后旧 DTO 保持普通数据，旧 RemoteObject 被判 stale
```

---

## Phase 6：写操作和事务

写操作必须通过固定的 Allegro SKILL procedure，而不是 Python 拼接任意数据库表达式。

推荐 API：

```python
result = session.components.move(
    refdes="R101",
    x=120.0,
    y=45.0,
    rotation=90.0,
)

result = session.properties.set(
    object_kind="component",
    object_key="R101",
    name="MY_PROPERTY",
    value="abc",
)

session.board.save()
```

第一版支持的写操作应控制在较小范围：

```text
设置用户属性
移动/旋转已放置元件
创建有限类型的图形
删除明确指定的对象
修改文本
保存设计
```

布线、交互式选择、复杂约束、Constraint Manager 等放到后续。

### 6.1 事务 wrapper

结构示意：

```skill
procedure(ABRunTransaction(functionSymbol args)
  let((transaction result)
    transaction = axlDBTransactionStart()

    if(errset(
         result = apply(functionSymbol args)
       ) then
      axlDBTransactionCommit(transaction)
      list('success result)
    else
      axlDBTransactionRollback(transaction)
      list('failure errset.errset)
    )
  )
)
```

Cadence 的 `axlDBTransactionStart`、`Commit` 和 `Rollback` 分别用于开始、提交和回滚数据库更改，并支持嵌套事务。

Python 侧推荐提供 batch，而不是跨很多 RPC 长时间持有远端 transaction：

```python
with session.batch("normalize passive placement") as batch:
    batch.components.move("R101", x=10, y=20)
    batch.components.rotate("R101", degrees=90)
    batch.components.move("C203", x=15, y=25)
```

退出 context 后，整个 batch 编译成一个 SKILL 调用：

```text
start transaction
执行全部操作
全部成功 → commit
任何失败 → rollback
```

### 6.2 Active command policy

写操作发出前：

```text
检查是否有用户交互命令正在进行
如果有，不自动发 done
返回 BUSY_ACTIVE_COMMAND
```

不要为了自动化便利擅自结束用户正在进行的 move、route、add connect 等命令。

### 6.3 原生 Undo

第一版先只实现 transaction rollback。

需要进入 Allegro 原生 Undo 栈的操作，再注册专门命令：

```skill
axlCmdRegister(
    "ab_move_components"
    'ABMoveComponentsCommand
    ?cmdType "interactive"
    ?undo t
)
```

Cadence 说明修改数据库的自定义命令通常应以 interactive 类型注册，`?undo t` 可将其纳入 Undo；同时仍应使用数据库事务。对大规模修改，Cadence 也提示不要无条件启用 Undo，因为 Undo 内存存在限制。

批量写入性能稳定后，可以评估 `axlDBCloak`，将动态 shape、显示或其他数据库更新延迟到批次结束，但正确性和事务回滚必须先完成。

---

# 六、Python 对外接口设计

建议最终接口如下：

```python
from allegro_bridge import AllegroSession


with AllegroSession.connect(port=7777) as pcb:
    status = pcb.status()
    print(status.allegro_version)
    print(status.design_path)

    board = pcb.board.get_info()

    components = pcb.components.list(
        include_unplaced=True,
    )

    r101 = pcb.components.get("R101")

    result = pcb.components.move(
        "R101",
        x=120.0,
        y=45.0,
        rotation=90.0,
    )

    if not result.ok:
        raise RuntimeError(result.error)

    pcb.board.save()
```

统一结果类型：

```python
@dataclass(frozen=True)
class OperationError:
    code: ErrorCode
    message: str
    details: dict[str, object]


@dataclass(frozen=True)
class OperationResult[T]:
    ok: bool
    value: T | None
    error: OperationError | None
    request_id: str
    elapsed_ms: float
```

写操作还应包括：

```python
@dataclass(frozen=True)
class MutationMetadata:
    committed: bool | None
    rolled_back: bool
    commit_state_known: bool
    design_modified: bool | None
```

这里 `committed=None` 表示 timeout 后无法确认 Allegro 内部是否已经完成写入。

---

# 七、能力握手

连接建立后，Python 不应直接执行操作，而应先调用：

```skill
ABGetCapabilities()
ABGetSessionInfo()
```

建议返回：

```json
{
  "bridge_version": "0.1.0",
  "protocol_version": 1,
  "allegro_version": "...",
  "design_loaded": true,
  "design_id": "dbid:12345",
  "session_generation": 7,
  "capabilities": {
    "read_components": true,
    "read_nets": true,
    "write_components": true,
    "transactions": true,
    "native_undo": false,
    "bulk_export": true
  }
}
```

这样可以针对不同 Allegro 版本做兼容适配，而不是在 Python 业务层散布版本判断。

---

# 八、日志和审计

每个请求至少记录：

```text
timestamp
request_id
session_id
operation
mutation
duration_ms
status
error_code
design_path
session_generation
```

写操作额外记录：

```text
idempotency_key
transaction_started
transaction_committed
transaction_rolled_back
commit_state_known
affected_object_count
```

默认不要记录完整 SKILL 源码，因为其中可能包含设计名称、路径和内部属性。调试模式才记录，并做长度限制。

推荐目录：

```text
%LOCALAPPDATA%/AllegroBridge/logs/server.jsonl
%LOCALAPPDATA%/AllegroBridge/logs/client.jsonl
%LOCALAPPDATA%/AllegroBridge/logs/skill.log
```

---

# 九、测试方案

## Python 单元测试

覆盖：

```text
长度帧拆包/粘包
recv_exact
部分 send
请求 UUID
结果缓存
重复请求
AST 安全解析
函数名映射
DTO 校验
状态机
retry policy
```

## Mock SKILL 测试

沿用 skillbridge 现有 mock 思路。项目已有 TCP/Unix channel、类型转换、RemoteObject 和 reconnect 测试，可继续扩展。 

增加：

```text
延迟响应
迟到响应
response 在长度头中间断开
两个客户端同时请求
写请求断线
非法 serializer payload
server restart
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
读取 board info
读取 placed/unplaced component
读取 net
修改属性后 rollback
修改属性后 commit
强制 SKILL error 后数据库无变化
换板后旧 handle stale
用户处于交互命令时写操作返回 BUSY
端口冲突
Python 路径含空格
设计路径含空格和中文
大结果走 bulk channel
```

## 压力验收

建议最低门槛：

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
| M0 | 原始 skillbridge 在 Windows Allegro 跑通 | 2–4 天 |
| M1 | TCP、dispatcher、timeout、状态机加固 | 1–2 周 |
| M2 | bootstrap、CLI、配置、日志 | 3–5 天 |
| M3 | Raw Workspace、handle 生命周期 | 3–5 天 |
| M4 | board/components/nets 只读 SDK | 1–2 周 |
| M5 | 第一批事务化写操作 | 2–4 周 |
| M6 | 原生 Undo、批量性能、版本兼容 | 1–3 周 |

一个可用于内部自动化的只读 MVP，通常落在 **3–5 周**。具备稳定写操作、异常恢复、事务和多版本兼容的版本，通常落在 **6–10 周**。最大的变量不是 TCP，而是需要覆盖多少 Allegro 写操作，以及目标 Allegro 版本之间的 AXL-SKILL 差异。

---

# 十一、第一版建议冻结的范围

第一版只交付：

```text
Windows 本机连接
单 Allegro session
单写者
ping/status
board info
components/symbols/nets/layers 查询
批量 CSV 导出
设置用户属性
少量元件位置类操作
事务 rollback
显式 save
日志和 doctor
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
```

最合理的执行顺序是先完成 **Phase 1 的目标 Allegro 实机 PoC**，尤其验证 1,000 次连续 IPC 调用和无 UI 操作时的 callback 稳定性；该结果会直接决定后续只需加固 skillbridge，还是需要替换 Windows pipe relay。