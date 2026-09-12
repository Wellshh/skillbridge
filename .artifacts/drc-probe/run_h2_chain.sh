#!/usr/bin/env bash
cd /d/AutoPlacer/skillbridge/.artifacts/drc-probe
PY=/d/AutoPlacer/skillbridge/.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8
WORK="C:/Users/BAIJUN~1/AppData/Local/Temp/drc-probe-h2-b20p_7q8"
F1="$WORK/probe_d_F1.brd"
SAVE_TS=1789198227.509
port() { "$PY" -c "import sys; sys.path.insert(0,'.'); import probe_d as pd; print(pd._free_port())"; }
echo "F1 exists: $(ls -la "$F1")"
P1=$(port); NOW=$(date +%s)
echo "=== STEP1 YOUNG_DEAD_NOENV port=$P1 now=$NOW age=$((NOW - ${SAVE_TS%.*}))s ==="
"$PY" probe_d_attempt.py "$WORK" "$F1" "$P1" YOUNG_DEAD_NOENV
echo "STEP1_RC=$?"
P2=$(port); NOW=$(date +%s)
echo "=== STEP2 YOUNG_DEAD_ENV port=$P2 now=$NOW age=$((NOW - ${SAVE_TS%.*}))s ==="
ALLEGROBRIDGE_LOG_DIRECTORY="$WORK" "$PY" probe_d_attempt.py "$WORK" "$F1" "$P2" YOUNG_DEAD_ENV
echo "STEP2_RC=$?"
P3=$(port)
echo "=== STEP3 LATE_RUN4_F1 port=$P3 ==="
"$PY" probe_d_attempt.py "C:/Users/BAIJUN~1/AppData/Local/Temp/drc-probe-d-t6qj7k4b" "C:/Users/BAIJUN~1/AppData/Local/Temp/drc-probe-d-t6qj7k4b/probe_d_F1.brd" "$P3" LATE_RUN4_F1
echo "STEP3_RC=$?"
echo "=== CHAIN DONE ==="
