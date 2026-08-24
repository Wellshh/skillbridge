# Windows Allegro 集成测试启动与验收

## 2026-08-25 实测环境

- Allegro 17.2 S048：`D:/Cadence/Cadence_SPB_17.2-2016/tools/bin/allegro.exe`
- 安装根目录：`D:/Cadence/Cadence_SPB_17.2-2016`
- 用户级许可证变量：`CDS_LIC_FILE=5280@localhost`
- Python：项目 `.venv`

Codex/IDE 子进程不一定继承后来写入的用户环境变量。测试前应读取用户级变量并只设置
当前 PowerShell 进程，不要永久修改系统环境：

```powershell
$env:Sigrity_EDA_DIR = 'D:\Cadence\Cadence_SPB_17.2-2016'
$env:CDS_LIC_FILE = [Environment]::GetEnvironmentVariable('CDS_LIC_FILE', 'User')
```

## 环境失败的判别顺序

1. `FileNotFoundError: could not find ... allegro.exe`：当前进程的 `PATH`、`CDSROOT`、
   `Sigrity_EDA_DIR` 没有安装目录。先用显式 executable 或设置当前进程的
   `Sigrity_EDA_DIR`，不要改产品代码。
2. Allegro 约 20–30 秒后 exit code 1：读取工作目录 `allegro.jrl`。若包含
   `license server search path is defined as <none>`，说明当前进程没有继承
   `CDS_LIC_FILE`；这发生在 startup.scr 执行前，不是 server 或 board 打开回归。
3. 只有 executable 和 license 都生效后，才调查 startup.scr、modal、server readiness
   或端口问题。

## Python 集成测试流程

先跑一个真实启动 smoke，缩短环境诊断时间：

```powershell
.venv\Scripts\python.exe -m pytest `
  tests/allegrobridge/test_integration.py::TestApi::test_session_uses_opened_workspace `
  --allegro -q
```

然后跑完整集成套件：

```powershell
.venv\Scripts\python.exe -m pytest -q `
  tests/allegrobridge/test_integration.py --allegro
```

端口/孤儿进程修复必须紧接着再跑一轮相同命令。两轮都使用默认 Windows TCP 端口
7777；第二轮能立即启动是端口释放的端到端证明。2026-08-25 实测结果为连续两轮
`17 passed`，每轮约 43 秒。

集成 fixture 会复制 `allegrobridge/assets/shape1.brd` 到 pytest 临时目录；不要直接在
版本库样板上运行写数据库测试。

## SKILL/qcover 实机门槛

创建临时 `.scr`，内容仅为：

```text
skill load("D:/AutoPlacer/skillbridge/tests/skill/run.ils")
exit
```

用同一 executable 和当前进程许可证环境运行 `allegro.exe -s <script>`。Allegro GUI
进程可能在启动命令返回后继续运行，因此以 `allegro.jrl` 的 `Journal end` 和测试摘要为
准。2026-08-25 实测基线：

- `74 passed, 0 failed, 0 skipped, 0 xfailed`
- `qcover: 124/124 branches covered (100.00%)`

完成后删除临时脚本，并检查：

```powershell
Get-Process allegro,python_server -ErrorAction SilentlyContinue
Get-NetTCPConnection -LocalPort 7777 -State Listen -ErrorAction SilentlyContinue
```

两条命令均应无输出。`allegro.jrl` 是运行产物；在 dirty worktree 中不要把它当作待提交
源码，也不要覆盖或还原用户已有的 journal 改动。
