#!/usr/bin/env bash
cd /d/AutoPlacer/skillbridge/.artifacts/drc-probe
PY=/d/AutoPlacer/skillbridge/.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8
echo "=== RUN5 PHASE S1 (creates work, saves F1, EXITS) start=$(date +%s) ==="
"$PY" probe_d.py --phase s1 > run5_s1.out 2>&1
echo "S1_RC=$? end=$(date +%s)"
STATE=$(sed -n 's/^STATE_FILE //p' run5_s1.out | tail -1 | tr '\' '/')
echo "STATE=$STATE"
if [ -z "$STATE" ] || [ ! -f "$STATE" ]; then
  echo "NO STATE FILE - ABORT"; tail -40 run5_s1.out; exit 1
fi
echo "=== RUN5 PHASE S2 (fresh process; S1 python DEAD) start=$(date +%s) ==="
"$PY" probe_d.py --phase s2 "$STATE" > run5_s2.out 2>&1
echo "S2_RC=$? end=$(date +%s)"
echo "=== RUN5 PHASE S3 (fresh process) start=$(date +%s) ==="
"$PY" probe_d.py --phase s3 "$STATE" > run5_s3.out 2>&1
echo "S3_RC=$? end=$(date +%s)"
echo "=== RUN5 DONE ==="
