# Communication performance benchmarks

Install the project development dependencies before running the suite. A local micro run checks
the Python protocol hot paths, but it is not a canonical Windows Allegro baseline.

Run the micro benchmarks without coverage:

```console
python -m pytest benchmark/test_micro.py --no-cov --benchmark-only \
    --benchmark-json=results/micro-1.json
```

Canonical end-to-end reports require the same dedicated Windows host, Python 3.12, Allegro 17.2
S048, board fixture, power plan, and locked dependencies. Do not use xdist, coverage, a debugger,
or a profiler. Set the Allegro installation and user-level license in the current PowerShell
process, then verify the existing integration suite before collecting performance data:

```powershell
$env:Sigrity_EDA_DIR = 'D:\Cadence\Cadence_SPB_17.2-2016'
$env:CDS_LIC_FILE = [Environment]::GetEnvironmentVariable('CDS_LIC_FILE', 'User')
.venv\Scripts\python.exe -m pytest tests/allegrobridge/test_integration.py --allegro -q
```

Commit the revision and verify the worktree is clean before collecting; the analyzer intentionally
rejects dirty reports. Collect at least three independent pytest processes for each revision:

```powershell
1..3 | ForEach-Object {
    .venv\Scripts\python.exe -m pytest benchmark/test_allegro.py --allegro --no-cov `
        --benchmark-only --benchmark-json="results/baseline-$_.json"
}
```

Repeat the loop at the candidate revision with `candidate-$_.json`, then generate the report:

```console
python benchmark/check_regression.py \
    --baseline results/baseline-1.json results/baseline-2.json results/baseline-3.json \
    --candidate results/candidate-1.json results/candidate-2.json results/candidate-3.json
```

The analyzer accepts canonical Allegro E2E JSON only. Micro JSON intentionally has no Allegro or
board context and is rejected. Dirty or incomparable reports also exit 2. A valid comparison exits
0 and reports median deltas, within-run IQR noise, and cross-process MAD noise; it does not yet fail
on a slowdown. Collect at least ten same-revision processes before proposing a hard threshold.
