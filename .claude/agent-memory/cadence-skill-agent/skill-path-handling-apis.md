---
name: skill-path-handling-apis
description: SKILL/Allegro 路径处理冷门 API：axlDMFileParts(dirname 替代)、axlOSSlash/axlOSBackSlash 分隔符转换、get_filename 分隔符文档缺口
metadata:
  type: reference
---

SKILL 核心语言没有 dirname/basename 函数；路径拆分与分隔符归一化依赖 Allegro 扩展 API。

- `axlDMFileParts(t_filespec) => (directory file fileWext ext)` — 官方路径拆分函数，文档在 `algroskill/21filacc.md`（约 349 行）。例：`axlDMFileParts("/usr1/xxx/stuff.txt") -> ("/usr1/xxx/" "stuff" "stuff.txt" "txt")`；相对路径时目录部分取 cwd。`car()` 即得目录（含尾部斜杠）。
- `axlOSSlash(t_directory)` — 反斜杠转正斜杠，文档在 `algroskill/21filacc.md`（约 436 行），UNIX 上原样返回。`axlOSBackSlash(t_directory)` 反向转换，文档在 `algroskill/23utils.md`（约 832 行）。官方原文称 UNIX 风格斜杠 "more amenable to SKILL"。
- `get_filename(p_port)` 官方文档（`sklangref/inputoutput.part01.md` 约 678 行）只说 "Returns the file name of a port"，**未说明 Windows 上返回路径的分隔符形式**；端口名保留打开时传入的原始字符串（`infile("~/test/input.il") => port:"~/test/input.il"`，不做 tilde 展开）。在 Windows 上解析 `get_filename(piport)` 结果前应先过 `axlOSSlash` 归一化。
- `rindex(t_string1 S_string2)` 返回的是**从最后一次匹配处开始的子字符串**（不是索引位置），未找到返回 nil。例：`rindex("dandelion" "d") => "delion"`。要得到目录部分可配合 `strlen` 计算长度后用 `substring`（1-based，第三参是长度非结束位置）。
- `parseString(path "/")` + `buildString(list "/")` 可手工拼路径，但不处理反斜杠，Windows 上需先 `axlOSSlash`。
