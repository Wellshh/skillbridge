# Memory Index

- [SKILL 路径处理冷门 API](skill-path-handling-apis.md) — axlDMFileParts 替代 dirname；axlOSSlash 分隔符归一化；get_filename 分隔符无官方文档；rindex 返回子串非索引
- [DPL 顺序与遍历](dpl-ordering-and-traversal.md) — ->?/->??/propNames 顺序未定义；DPL 物理存储 LIFO；用 cddr 遍历原始列表才确定
- [表赋值与函数定义 API](table-assignment-and-funcdef-apis.md) — makeTable 元素赋值用 tableName[key]=value（setq 不接受表索引）；getd/putd 保存恢复函数定义
- [SKILL 属性位置与变量赋值](skill-ils-value-slot-globals.md) — `setq` 左值必须是 symbol；`obj.prop`/`obj->prop` 属性位置用 `=`，不要与 table `[]`/`setarray` 混淆
- [重定义受保护内置函数](write-protect-mocking-builtins.md) — setFnWriteProtect 只置位不清位；sstatus writeProtect nil 不影响已有受保护函数；唯一正途是 sstatus(debugMode t)
- [SKILL++ 调用分组与 errset 状态](skill-ils-calls-and-errset-state.md) — `(f(...))` 会把 conventional call 返回值再次求值；用当前 `errset` 返回值判定成功，失败描述须在 cleanup 前保存
- [Windows Allegro 集成测试启动与验收](windows-allegro-integration-validation.md) — 当前进程补安装根与用户级许可证变量；单项 smoke、17 项连续两轮、SKILL/qcover、进程与 7777 端口验收
- [qcover `.ils` Phase 1 生命周期](qcover-ils-phase1.md) — SKILL++ loadPort/句柄清理、attempt-local 原子回滚、临时文件所有权、串行执行与验证门槛
- [python_server.il -> python_server.ils Phase 2A 纠错经验](phase2a-correction-lessons.md) — qtest 宏构造/运行期诊断、SKILL++ 清理与调用语法、远程对象 expected-red、Windows 许可证和 141=136/5 验证基线
