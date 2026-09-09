# Cadence validation workflows

Paths below are relative to the repository root. Use the sections relevant to the current change; the assessment template is optional.

## Static and Windows validation

1. Run the lexical check for changed scripts:
   `python3 .agents/skills/cadence-skill-agent/scripts/skill_lint.py <file.il>`
   (also accepts `.ils`). This checks lexical structure without starting Allegro; it is stricter than the 17.2 reader in some cases and does not replace `sklint`.
2. In the target Allegro process, use `isCallable` for uncertain function availability and `arglist` where signatures remain unclear.
3. Run `sklint` with `?checkPubFuncs t` and `?outputFile`; retain the diagnostic output for investigating failures.
4. Use `load`, not error-suppressing `loadi`. For qcover tests, use the suite's instrumented load instead of loading the same file twice.
5. Run the nearest qtest/qcover suite or a public-entry smoke check. Assert return values, database postconditions, and cleanup; distinguish unexpected `unbound` output from explicit unbound-value tests.

The full SKILL suite runs on Windows through:

```console
python -m pytest tests/allegrobridge/test_integration.py --allegro -k TestSkill
```

See `docs/skill-testing.md` for test organization and coverage, and `benchmark/README.md` for comparable performance evidence.

## Launch, isolation, and recovery

- Automatic destructive validation uses `Allegro.open(mode="cli")`, a disposable board copy, an owned process, and a unique numeric TCP port. Parallel runs need independent ports and boards; qcover loads/runs remain serial within a process.
- Pass Python paths to SKILL with `Path.resolve().as_posix()`.
- After a failure that may contaminate the design or process, use a fresh process and board copy. Always close owned processes and connections on exit.
- Retry only after a concrete correction, new diagnostic evidence, or an environment change. If another attempt cannot add evidence, report the failure and the missing prerequisite instead of repeating it.
- Let `KeyboardInterrupt` and unexpected Python errors propagate. Do not hide them as retryable startup failures or automatically replay failed writes.

## Optional assessment template

For changes where a structured assessment improves review, this template can capture the relevant evidence. Ordinary prose is sufficient for a small change; it is not an approval gate.

```json
{
  "agent": "cadence-skill-agent",
  "phase": "assessment",
  "payload": {
    "target_objects": [],
    "reuse_candidates": [],
    "api_evidence": [
      {
        "api": "",
        "source": "",
        "line": 0,
        "signature": "",
        "returns": "",
        "constraints": "",
        "platform": ""
      }
    ],
    "lifecycle": {
      "acquire": [],
      "cleanup": [],
      "observable_postconditions": []
    },
    "risks": []
  }
}
```
