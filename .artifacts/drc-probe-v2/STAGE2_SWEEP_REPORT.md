# Stage II-A finite arc analysis

The source records are the four-case sweep manifest at [run-54268](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-sweep/run-54268-1789223811387679300/manifest.json) and the independent `ccw_lower` diagnostic at [run-63160](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-sweep-diag/run-63160-1789225091207869200/manifest.json). The offline reduction is [stage2_sweep_analysis.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/results/stage2-analysis/stage2_sweep_analysis.json).

The requested arc has S=(300,400), E=(310,400), C=(305,403.75), R=6.25 and the finite line spans x=295..315. The endpoint angles are 216.869897° and 323.130103° in the ordinary [0,360) convention; the derived sweeps are 106.2602047083° and 253.7397952917°. Thus the CCW minor sweep is 106.2602047083° through the lower side; the CW major sweep is 253.7397952917° through the upper side. The relevant radial extrema have x=305, which lies inside the finite line span, so the horizontal-line distance reductions are valid for these four samples.

With both copper widths 0.15, the full-circle candidate gap is 0.05. For CCW lower and CW upper, the covered finite extremum gives 0.05; CCW upper gives 10.05 and CW lower gives 2.55. The expected finite pattern is therefore `CCW lower FLAGGED`, `CCW upper CLEAN`, `CW lower CLEAN`, `CW upper FLAGGED`; the corresponding finite gaps are approximately `0.05`, `10.05`, `2.55`, and `0.05` mm, conditional on the independently read rule threshold. The raw Stage II observations support the two clean cases and the positive `cw_upper`; the `ccw_lower` diagnostic is stable on its fresh path. It does not prove that refreshing caused the earlier duplicate/null anomaly to disappear; the old anomaly remains preserved in run-54268.

The geometry conclusion is specialized to this horizontal chord and these signs. It does not generalize to an infinite-circle or arbitrary finite-line formula without rechecking sweep inclusion and projection.

## Stage III-B display-only evidence

The historical oracle source is [oracle_regression.json](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/oracle_regression.json), with original B/C log citations retained there and in [AUDIT_REPORT.md](D:/AutoPlacer/skillbridge/.artifacts/drc-probe-v2/AUDIT_REPORT.md). `B_STAIR_n6` has `FULL_B64_EXPORTED_RADIUS ≈ 0.0598999999999478`, while the observed marker displays `0.0599`; this contradicts treating the displayed value as direct evidence of a four-decimal floor of FULL. Positive floor and toward-zero remain observationally equivalent for positive values. `C_CC_GOLD` has ideal grid normalization 0.06 but historical marker actual 0.0599; grid normalization is therefore not a verdict proof. `overlap=0` is an observation and does not establish a clamp or epsilon bound.

These are display/model identifiability limits only; no DRC integer rule or epsilon=0 is inferred.
