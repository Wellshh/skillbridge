---
name: phase2a-correction-lessons
description: Windows Allegro 17.2 verified Phase 2A qtest and SKILL++ correction rules
metadata:
  type: reference
---

# Phase 2A 纠错经验（Windows Allegro 17.2）

- `qtest::TestCase` 是宏：每个 body form 在展开时被编译成一个零参数
  `(lambda () ...)`，随后由 `qtest:::runTestCase` 逐个 `funcall`。因此，宏展开/套件构造错误发生在
  `qtest::runTests` 能捕获单个 case 之前，通常没有带 case 名称的 `Fail`；运行期错误则由
  `runTests` 外层 `errset` 转成该 case 的 `Fail`。诊断时先用只含一个 `TestSuite`、一个
  `TestCase`、最小常量 body 的诊断宏/展开 probe，确认 suite 能构造，再逐步加入 body；不要把
  构造失败误判为被测函数运行失败。
- SKILL++ `unwindProtect` 必须明确两个参数：受保护 body 和 cleanup body。资源获取、主体、唯一
  cleanup 路径应按这两个参数组织；不要使用省略参数、隐式 cleanup 或多条相互竞争的恢复路径。
- `setq` 的左值只能是 symbol。像 `obj.prop`、`obj->prop` 这样的属性位置必须用 `=`（或测试
  helper）；不要写 `(setq obj.prop value)`。表元素仍用 `table[key] = value`/`setarray`。
- 不要把 conventional 调用压缩进 Lisp 外层括号，尤其不要写 `(f(?key value))` 或连续挤压嵌套的
  `car`/`cadr`/`nth` 调用；SKILL++ 可能把返回值再次当函数求值，或让 reader 粘连参数。统一采用
  `(f ?key value)` 的 Lisp 分组，复杂子式分行并显式保留空格。
- 目标 Allegro 17.2 上用 `(not (null (getd 'name)))` 检查已有函数定义；`isCallable` 不可用/并非
  可依赖的检查 API 时，不要猜测或伪造它。保存和恢复测试替换也使用 `getd`/`putd`。
- 远程对象序列化测试必须使用真实可构造的 `pcreobj`（例如 `pcreCompile` 返回值）或真实 port；
  `qtest:::Result` 只是测试结果对象，不是该序列化分支识别的远程对象，不能拿它覆盖分支证据。
- expected-red reader 片段中，每个片段以及最终 `strcat` 拼接串都必须可以独立求值。先分别验证
  片段，再验证拼接后的串；避免不完整括号、引号或参数粘连带来的额外 reader 噪声掩盖预期错误。
- Windows Allegro 启动前，在当前 PowerShell 进程从 User 级读取许可证：
  `$env:CDS_LIC_FILE = [Environment]::GetEnvironmentVariable('CDS_LIC_FILE', 'User')`；同时补齐
  安装根/显式 executable。不要把后写入的用户变量假定为已被 Codex/IDE 子进程继承，也不要为此修改产品代码。
- 每个修复轮次使用新 Allegro 进程、新数字 TCP 端口和新 board 副本；验证前后确认没有遗留进程或
  监听端口。Phase 2A 最终隔离实测为 `141 total = 136 passed / 5 failed`，仅 expected-red
  ID `30、52、53、54、55` 失败；不得把这五项改成绿来掩盖目标行为。
- Phase 2A 仅改变测试侧的 `tests/skill/test_server.ils`；生产
  `allegrobridge/_kernel/server/python_server.il` SHA-256 保持
  `76BD57830BA6496F55827DAFFE38AF915AB2722AC617D63D145FE5912CA72FEA`。后续阶段若生产文件变化，
  必须重新记录基线与每轮验证事实。
