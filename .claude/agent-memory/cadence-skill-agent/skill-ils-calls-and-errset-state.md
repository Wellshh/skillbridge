# SKILL++ 调用分组与 errset 状态

## `.ils` 中不要给 conventional call 再套一层调用括号

SKILL++ 同时支持 Lisp 调用语法 `(f ?port p)` 和 conventional 调用语法
`f(?port p)`。后者本身合法，但写成 `(f(?port p))` 时，外层括号不是普通分组：
它会把内层调用的返回值再次当作函数求值。本项目在带 keyword 参数的 reporter
调用中实际遇到过这个问题。

在 `.ils` 的 Lisp 风格代码中统一写：

```lisp
(qtest::printSummary ?port port)
```

不要写：

```lisp
(qtest::printSummary(?port port))
```

官方依据：`sklangref/appA.md` 的 procedure calls 条目说明 `(f e ...)` 与
`f(e ...)` 都是调用语法；因此额外的最外层括号会形成第二次调用，而不是分组。

## 不要用 `errset.errset` 判断当前 `errset` 是否失败

`errset.errset` 是 symbol property 上的共享错误描述，不是某次调用的局部状态。
被执行表达式若在内部捕获过错误，外层表达式仍可正常返回，但该 property 可能保留
内部错误。用它直接判断外层调用会把成功请求误报为失败。

必须保存并检查当前外层 `errset` 的返回值：

```lisp
completed = errset(result=evalstring(line))
if(completed then
  ; success
else
  ; 此时立即读取 errset.errset
)
```

`errset` 成功时返回包含表达式结果的 list，失败时返回 `nil`；正常返回 `nil` 仍会得到
`(nil)`，因此可可靠区分。失败后若还要 rollback、cleanup 或调用其他可能触发错误的
函数，必须先复制 `errset.errset`，否则原始错误描述会被覆盖。

项目回归入口：`tests/skill/test_server.ils` 的
`test_on_data_treats_inner_errset_as_success` 与
`test_on_data_script_treats_inner_errset_as_success`。
