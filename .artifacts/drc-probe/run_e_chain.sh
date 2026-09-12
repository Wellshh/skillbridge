#!/usr/bin/env bash
# Probe E chain: process-separated phases (run5-proven mitigation for the
# empty-design open refusal).  S1 saves F1a/F1 and exits; S2/S3 run in fresh
# processes AFTER the saving python exited.
cd /d/AutoPlacer/skillbridge/.artifacts/drc-probe
PY=/d/AutoPlacer/skillbridge/.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8
echo "=== RUN_E PHASE E1 (creates work, saves F1a/F1, EXITS) start=$(date +%s) ==="
"$PY" probe_e.py --phase e1 > run_e_s1.out 2>&1
echo "E1_RC=$? end=$(date +%s)"
STATE=$(sed -n 's/^STATE_FILE //p' run_e_s1.out | tail -1 | tr '\\' '/')
echo "STATE=$STATE"
if [ -z "$STATE" ] || [ ! -f "$STATE" ]; then
  echo "NO STATE FILE - ABORT"; tail -40 run_e_s1.out; exit 1
fi
echo "=== RUN_E PHASE E2 (fresh process; E1 python DEAD) start=$(date +%s) ==="
"$PY" probe_e.py --phase e2 "$STATE" > run_e_s2.out 2>&1
echo "E2_RC=$? end=$(date +%s)"
echo "=== RUN_E PHASE E3 (fresh process) start=$(date +%s) ==="
"$PY" probe_e.py --phase e3 "$STATE" > run_e_s3.out 2>&1
echo "E3_RC=$? end=$(date +%s)"
echo "=== RUN_E DONE ==="
