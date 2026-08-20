# Memory Index

- [SKILL 路径处理冷门 API](skill-path-handling-apis.md) — axlDMFileParts 替代 dirname；axlOSSlash 分隔符归一化；get_filename 分隔符无官方文档；rindex 返回子串非索引
- [DPL 顺序与遍历](dpl-ordering-and-traversal.md) — ->?/->??/propNames 顺序未定义；DPL 物理存储 LIFO；用 cddr 遍历原始列表才确定
- [表赋值与函数定义 API](table-assignment-and-funcdef-apis.md) — makeTable 元素赋值用 tableName[key]=value（setq 不接受表索引）；getd/putd 保存恢复函数定义
- [SKILL 属性位置与变量赋值](skill-ils-value-slot-globals.md) — `setq` 左值必须是 symbol；`obj.prop`/`obj->prop` 属性位置用 `=`，不要与 table `[]`/`setarray` 混淆
- [重定义受保护内置函数](write-protect-mocking-builtins.md) — internal(C内置)标志不可清除，debugMode 也无法绕过；无 advice/traceFunc/facility；唯一出路是 SUT 调用用户自定义 wrapper
- [命令行启动 Allegro 并播放预设脚本](allegro-cli-launch-preset-script.md) — allegro.exe -s scr.scr；skill 前缀须同行；pyStartServer ?id 传字符串；用 marker 文件验证脚本执行；后台 wrapper 保活；<pipe-error> 是 __pyOnData 明文 vs python 帧协议不匹配
