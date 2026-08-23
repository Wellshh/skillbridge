# Agent Memory

## qtest / qcover 真实运行基线

- 2026-08-20 上一次已验证基线：用户在 Windows Allegro 中加载 `tests/skill/run.ils`，全部测试通过；`python_server.il` branch coverage 为 `62/62 (100.0%)`。
- 当前 coverage 验收只保留在 `tests/skill/run.ils`，由 `qcover::report ?minimum 100.0` 统一执行；不再用 TestCase 锁定 decision 数量。
- `tests/skill/run.ils` 是唯一入口：依次运行 qtest/reporter/qcover 自测和项目测试，先打印 summary 并传播测试失败，再执行 100% coverage 阈值。

## 已验证的实现经验

- `qtest::runTests` 必须在每个 TestCase 边界用 `errset` 捕获未处理错误，将其转成包含测试名和 `errset.errset` 的 `Fail`，然后继续后续测试。不要再写固定路径诊断文件。
- `errset` 成功时返回包含表达式结果的 list，因此测试正常返回 `nil` 与抛错仍可区分。
- remote regex 分支必须用 `pcreCompile("abc")` 生成真实 `pcreobj@0x...` 对象触发；伪造 symbol 的 `%L` 表示会被转义，无法覆盖该分支。

## 查证入口

- 当前代码：`tests/skill/qtest/src/qtest/core.ils`、`tests/skill/qtest/src/qtest/test_assertions.ils`、`tests/skill/test_server.ils`、`tests/skill/run.ils`。
- 本地 API：`.agents/skills/cadence-skill-agent/skill-references/sklangref/funcprog.part01.md` 的 `errset`；`sklangref/stringfunc.part01.md` 的 `pcreCompile`。
- 更早 Windows/SKILL 经验：`.claude/agent-memory/cadence-skill-agent/`。
