# qtest / qcover

This directory vendors a modified copy of **qtest**, the SKILL unit-testing
framework from [SKILL_Tools](https://github.com/MatthewLoveQUB/SKILL_Tools)
by MatthewLoveQUB, used under the MIT License — see [LICENSE](LICENSE).
Modifications remain under the same license.

| Folder | Origin |
|---|---|
| `src/qtest/` | upstream, modified — test suites, test cases, assertions, reporter |
| `src/std/` | upstream, subset — helper functions the framework depends on |
| `src/qcover/` | original to AllegroBridge — branch-coverage instrumenter for classic SKILL, LGPL-3.0-or-later (see file headers) |

Local changes include a reporter module with run summary, a reframed
`runTests`, and Windows path normalization.

The framework is loaded by `tests/skill/run.ils`; see
[docs/qtest.md](../../../docs/qtest.md) for the testing guide.
