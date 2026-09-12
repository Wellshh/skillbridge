#!/usr/bin/env bash
cd /d/AutoPlacer/skillbridge/.artifacts/drc-probe
PY=/d/AutoPlacer/skillbridge/.venv/Scripts/python.exe
export PYTHONIOENCODING=utf-8
OUT=saver_alive.out
rm -f "$OUT"
"$PY" probe_d_save_and_exit.py 300 > "$OUT" 2>&1 &
SPID=$!
echo "SAVER_BASH_PID=$SPID"
for i in $(seq 1 300); do grep -q SAVER_SLEEPING "$OUT" 2>/dev/null && break; sleep 1; done
cat "$OUT"
WORK=$(sed -n 's/^SAVER_SLEEPING.*workdir=//p' "$OUT" | tail -1 | tr '\' '/')
F1="$WORK/probe_d_F1.brd"
SAVE_TS=$(sed -n 's/^SAVE_TS //p' "$OUT" | cut -d. -f1)
WPID=$(sed -n 's/^SAVER_SLEEPING pid=\([0-9]*\).*/\1/p' "$OUT" | tail -1)
echo "WORK=$WORK SAVER_WINPID=$WPID"
tasklist //FI "PID eq $WPID" | grep -i python && echo SAVER_ALIVE=YES || echo SAVER_ALIVE=NO
P=$("$PY" -c "import sys; sys.path.insert(0,'.'); import probe_d as pd; print(pd._free_port())")
NOW=$(date +%s)
echo "=== ATTEMPT ALIVE_UNRELATED port=$P age=$((NOW - SAVE_TS))s saver_pid=$WPID ==="
"$PY" probe_d_attempt.py "$WORK" "$F1" "$P" ALIVE_UNRELATED
echo "ATTEMPT_RC=$?"
tasklist //FI "PID eq $WPID" | grep -i python && echo SAVER_STILL_ALIVE=YES || echo SAVER_STILL_ALIVE=NO
wait $SPID
echo "SAVER_FINAL_RC=$?"
echo "=== CONTROL DONE ==="
