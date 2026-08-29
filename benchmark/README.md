# Performance gates

Run local micro benchmarks without coverage:

```console
pytest benchmark/test_micro.py -o addopts='' --benchmark-save=micro
```

On the same Windows Allegro host, save a baseline and two candidate runs:

```console
pytest benchmark/test_allegro.py --allegro -o addopts='' --benchmark-json=baseline.json
pytest benchmark/test_allegro.py --allegro -o addopts='' --benchmark-json=first.json
pytest benchmark/test_allegro.py --allegro -o addopts='' --benchmark-json=second.json
python benchmark/check_regression.py baseline.json first.json second.json
```

The final command fails only when both candidate medians exceed the baseline median plus its
IQR on the same host and Python runtime.
