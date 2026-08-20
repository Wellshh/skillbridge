---
name: allegro-cli-launch-preset-script
description: 用 allegro.exe -s script.scr 命令行启动有 GUI 的 Allegro 并播放预设 AllegroScript 的经验：skill 前缀、数字端口要传字符串、验证脚本是否执行的调试手段
metadata:
  type: reference
---

经验来源：在 Allegro 17.2（`D:\Cadence\Cadence_SPB_17.2-2016\tools\bin\allegro.exe`）命令行注入 skillbridge / skillbridge.py 的 server 启动脚本，全程只改 /tmp 下的 `.scr`，未动仓库代码。

## 命令行启动 + 播放预设脚本

- 启动并加载 SKILL 就用的 `-s <abs/script.scr>`（`-s` 播放 AllegroScript；不加 `-exit` 则 GUI 保持存活，可继续收命令）。GUI 是每次起的，进程名 `allegro.exe`，内存涨到 ~470-500MB 才算完全加载。
- **AllegroScript 语法：`skill` 关键字必须是每行行首前缀，且 SKILL 调用跟在同一行**：`skill load "d:/path/file.il"`、`skill pyStartServer ?id "7777"`。若把 `skill` 单独一行、下一行写 `load(...)` **会报 `Command not found: load(...)`**。
- 启动时的产品选择对话框本机已记住/自动跳过（窗口直接进 "unnamed.brd"），同事的 PyQt5 runner 也是 `allegro -s "{scr}" [-exit] "{brd}"` 同款。

## 关键陷阱

1. **`pyStartServer ?id` 必须传字符串**：KEY 类型模板 `"ttggtg"` 里 `?id` 是 `"t"`（string/symbol），传整数 `?id 7777` 直接 `*Error* pyStartServer: argument for keyword ?id should be a string - 7777`。要写 `?id "7777"`。python checker 里 `int(id_)`，所以 `"7777"`→7777。客户端默认 `Workspace.open()`（id=None）连 `('localhost', 7777)`。

2. **后台 wrapper 的生命周期会连带杀掉脱离的 GUI**：从 bash 后台任务 `allegro.exe ...` 启动的 detached GUI，若那个 wrapper 命令退出/被清理，GUI 可能被连带杀掉。要保活就用 `allegro.exe -s scr; while true; do sleep 10; done` 收尾让 wrapper 不退出，再用**另一条**前台命令去轮询。

3. **多实例共享同一工程目录时，第二个实例的 `-s` 脚本可能根本不执行**（无 banner、marker 都不写）。用 `-p <独立工程目录>` 隔离，或保证只跑单实例。

## 验证 `.scr` 是否执行到某一行

stdout 重定向到 `allegro_launchN.log` 通常只见 `libpng warning: iCCP` 噪声，脚本输出时有时无（不稳定）。**最可靠的是脚本内用 SKILL 写标记文件**，逐步定位停在哪：

```
skill let((p) p=outfile("C:/.../step2.txt") fprintf(p "step2 loaded il\n") close(p))
```

## 相关日志文件

- `allegro_launchN.log` — 被启动 exe 的 stdout/stderr（`libpng warning` + 偶尔的 banner `Allegro PCB Designer 17.2 S048`）。
- `skillbridge_server.log` — python 子进程日志（写在其 cwd 或 `SKILLBRIDGE_LOG_DIRECTORY`）。
- `skillbridge_skill.log` — `ipcBeginProcess` 的 logName（通常 0 字节即证明 spawn 过程被触发）。

## server-refactor 的 `<pipe-error>` 根因（协议不匹配）

连上也通了、请求到得了 SKILL 侧，但返回 `failure <pipe-error>`。原因：fork 的 python 管道协议期望**二进制帧** `\x02<payload>\x1e`（成功）`\x15<...>\x1e`（失败）`\x12<...>\x1e`（restart，`skillbridge/protocol/response.py`），而 Allegro 侧 `__pyOnData` 写的是**明文** `"success %s\n"`——首字符 `s` 被解析成 restart，然后一直等 `\x1e` 等不到 → 管道断 → `<pipe-error>`。要让端到端通，`__pyOnData` 必须改成输出帧标记。相关：[[write-protect-mocking-builtins]]
