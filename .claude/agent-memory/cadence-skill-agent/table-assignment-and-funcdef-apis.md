---
name: table-assignment-and-funcdef-apis
description: SKILL 关联表 (makeTable) 元素赋值正确语法是 tableName[key]=value（setq 不接受表索引表达式）；getd/putd 保存与恢复函数定义的模式
metadata:
  type: reference
---

Findings when authoring SKILL/SKILL++ code that writes to an association table or saves/restores a function definition.

**关联表元素赋值 — 必须用 `tableName[key] = value`，绝不能用 `setq`。**
- `setq( s_variableName g_newValueExp )` 是语法形式，第一参**必须是符号**（变量名），且不被求值。`setq is the same as the assignment (=) operator`，但它的第一参位置只接受变量符号。源：`sklangref/dataoperator.md:1259`（setq 项）。
- 用 `(setq tableName[key] value)` 会报 `setq: argument #1 should be a symbol`，因为 `tableName[key]` 不是符号而是 array-subscript 表达式。
- 正确写法是 statement 形式 `tableName[key] = value`，它是 `setarray` 的隐式调用。源：`sklangref/datastruct.md` `### setarray`（:413）原文 "Normally this function is invoked implicitly using the array-subscription syntax, such as, x[i] = v"；例 `mytab[9] = 3  => 3  ; same as setarray(mytab 9 3)`。`### makeTable`（:337）例 `myTable[1] = "blue" / myTable["two"] = '(r e d) / myTable['three] = 'green`，并注 "You can refer to and set the contents of an association table with the standard syntax for accessing array elements"。
- 编程指南：`sklanguser/chap4.md` "Initializing Tables"（:934）"To refer to and add elements, use the syntax for standard array access"。
- 等价显式函数调用：`setarray(o_table g_key g_value)`（函数形式，签名 `setarray( a_array x_index g_value )` / `setarray( o_table g_key g_value )`，:416）。
- `=` 赋值运算符是语法形式（同 setq），`x[i]=v` 作为表达式可出现在任意 body（for/foreach/let/prog/when/unless）。证据：`sklanguser/chap4.md` "Implementing Sparse Arrays"（:1048）在嵌套 `for` 内 `trSparseTimesTable[ list(i j) ] = i*j`；"Traversing Association Tables"（:1020）`foreach( key myTable ... myTable[key] ...)`。
- 读访问 `tableName[key]` 与写 `tableName[key]=value` 共用同一 array-subscript 语法；唯一需要的改动就是把 `setq tableName[key] value` 换成 `tableName[key] = value`。

**SKILL (.il) 与 SKILL++ (.ils) 对表赋值无差异。**
- `chap13.md` "About SKILL++ and SKILL"（:6）：二者共存、`All existing SKILL code can still run without any changes`，数据结构与下标语法一致。SKILL++ 的差异仅在词法作用域与 functions-as-data，不涉及 table/array 下标赋值。

**getd/putd — 保存与恢复函数定义（操作符号的 function slot）。**
- `getd( s_functionName ) => g_definition | nil`：返回符号的函数绑定；SKILL 函数返回 funobj，原语返回 binary 定义，未定义返回 nil。源：`sklangref/funcprog.part01.md` `### getd`（:1023）。注 "This function is not needed in SKILL++ because functions are treated as regular values"。
- `putd( s_functionName u_functionDef ) => u_functionDef`：把函数/lambda/nil 绑定到符号名；传 nil 可 undefine；write-protected 符号不能改。源：`sklangref/funcprog.part02.md` `### putd`（:268）。例 `putd( 'mySqrt getd( 'sqrt ))` 复制定义。
- 保存/恢复模式：`orig = getd('fn)` →（替换/包装）→ `putd('fn orig)` 恢复。
- SKILL++ 语义（`sklanguser/chap13.md:280` 起的符号三槽表与 "How SKILL++ Uses Symbols" :292）：`getd/putd` 只作用于符号的 **function slot**。SKILL++ 全局变量默认绑定到同名符号的 function slot，所以 SKILL/SKILL++ 能共享函数；但 SKILL++ 里纯词法闭包（仅存于局部变量、未进 function slot）用 `getd` 取不到。对顶层 `procedure/defun` 安装进 function slot 的函数，getd/putd 在 .ils 下同样可用。

Related: [[dpl-ordering-and-traversal]] (DPL 用 `->`/`putpropq`，与 table 的 `[]`/`setarray` 是两套机制；`putpropq`/`->=` 用于符号属性/DPL，见 `sklangref/dataoperator.md:896`)。
