# Cadence SKILL reference map

本文件只负责导航。代理工作流以 `.claude/agents/cadence-skill-agent.md` 为准，API 事实以索引指向的正文为准。

| 需求 | 先查 | 再读 |
| --- | --- | --- |
| Allegro `axl*` API | `.claude/skill-references/api_index.part*.md` | 命中的 `algroskill/*.md` 完整 API 条目 |
| 通用 SKILL API | `.claude/skill-references/sklang_api_index.part*.md` | `sklangref/` |
| IPC | `.claude/skill-references/sklang_api_index.part*.md` | `skipcref/` |
| lint、debugger、profiler | `.claude/skill-references/sklang_api_index.part*.md` | `skdevref/` |
| SKILL++ 对象系统 | `.claude/skill-references/sklang_api_index.part*.md` | `skoopref/` |
| 语义、作用域、IO、性能范式 | `.claude/skill-references/sklang_topic_index.md` | 命中的 `sklanguser/` 段落 |
| 可复用调用形状 | 仓库中已测试的 `.il` / `.ils` | `.claude/skill-references/examples/` |

实现结构优先复用已在目标版本测试的项目代码，其次是官方/golden example。API 名称和签名必须以正式正文为准，并由目标 Allegro 运行验证。示例不是签名证据；索引与正文不一致时不得猜测。
