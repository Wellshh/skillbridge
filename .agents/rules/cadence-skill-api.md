# Cadence SKILL & API 查询规范

在进行任何 Cadence API、SKILL 语言相关调用或 `.il` 脚本编写/修改时，必须严格遵守 `cadence-skill-agent` 的规范与本地文档检索协议（Zero-Hallucination）：

1. **强制本地文档检索**：
   - 严禁凭空猜测或直接编写未验证参数签名的 `axl*` 或内置 SKILL 函数。
   - 黄金样例优先：在 `.agents/skills/cadence-skill-agent/skill-references/examples/` 中搜索类似功能示例。
   - 索引与签名定位：
     - Allegro `axl*` API：检索 `.agents/skills/cadence-skill-agent/skill-references/api_index.part*.md`。
     - 通用 SKILL、IPC、开发工具及 SKILL++ API：检索 `.agents/skills/cadence-skill-agent/skill-references/sklang_api_index.part*.md`。
     - 查验源文档（`sklangref/`, `skipcref/`, `skdevref/`, `skoopref/` 等）核实函数名、参数类型、返回值、副作用与错误处理。

2. **执行流程协议**：
   - 阶段 1：先输出架构与 API 评估 JSON（确认目标对象、所需 API、参考样例与风险预警）。
   - 阶段 2：经过评估确认后生成完整、规范、作用域隔离（`let`/`prog` 包裹）、带命名空间前缀的工业级 `.il` 代码。
