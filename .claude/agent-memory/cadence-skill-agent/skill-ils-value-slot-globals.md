---
name: skill-ils-value-slot-globals
description: SKILL .ils 变量、属性位置和 table 元素赋值的语法边界，含 Windows Cadence 实测错误
metadata:
  type: reference
---

## Windows runtime finding

在 Cadence SKILL `.ils` 中，`setq` 的左值必须是 symbol。Windows 实测中，
`(setq pyStartServer.id value)` 会报：

```text
*Error* setq: argument #1 should be a symbol - (pyStartServer.id)
```

不要把 `pyStartServer.id` 这类属性访问表达式作为 `setq` 的第一个参数；更新属性位置应写成：

```skill
pyStartServer.id = value
```

本地 Cadence SKILL Language Reference 的 `setq` 条目明确规定首参
`s_variableName` 是要绑定的 symbol，并说明 `setq` 与变量赋值运算符 `=` 等价：
`.agents/skills/cadence-skill-agent/skill-references/sklangref/dataoperator.md`,
`### setq`, lines 1259-1298。

属性位置是另一种 assignment place：同一文档的 `putpropqq` 条目说明
`obj.prop = value` 等价于 `putpropqq(obj value prop)`；`putpropq` 条目说明
`obj->prop = value` 等价于 `putpropq(obj value prop)`（`dataoperator.md`,
lines 896-940）。因此，`=` 在这里不是把属性表达式当作 `setq` 左值，而是调用对应的属性写入语义。

## Do not conflate table assignment

表元素使用方括号位置，和属性点号位置不是同一套机制：

```skill
myTable[key] = value
setarray(myTable key value)
```

两者等价，都是 association table 的 key 写入。Cadence 文档在
`.agents/skills/cadence-skill-agent/skill-references/sklangref/datastruct.md`
的 `### makeTable`（lines 337-370）和 `### setarray`（lines 413-460）中说明了
`table[key] = value` 与 `setarray(table key value)` 的关系；`[]` 访问也由
`arrayref`/`setarray` 处理。不要把 table 的 `[]`/`setarray` 规则套用到
`obj.prop` 属性位置，也不要为修复属性赋值而改写 table 访问。

Related: [[table-assignment-and-funcdef-apis]].
