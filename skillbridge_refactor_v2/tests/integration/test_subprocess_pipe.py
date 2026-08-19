from __future__ import annotations

import subprocess
import sys

import pytest
from skillbridge.pipe import SkillPipe, SkillPipeState, SkillPipeTimeoutError


@pytest.mark.integration
def test_real_subprocess_frames_errors_multiline_and_timeout_recovery() -> None:
    script = r"""
import sys
import time

STX = "\x02"
NAK = "\x15"
RS = "\x1e"

def send(marker, payload):
    sys.stdout.write(marker + payload + RS)
    sys.stdout.flush()

for line in sys.stdin:
    command = line.rstrip("\n")
    if command == "error":
        send(NAK, "remote failure")
    elif command == "multiline":
        send(STX, "one\ntwo")
    elif command == "slow":
        time.sleep(0.15)
        send(STX, "late")
    elif command == "quit":
        send(STX, "bye")
        break
    else:
        send(STX, "reply:" + command)
"""
    process = subprocess.Popen(
        [sys.executable, "-u", "-c", script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0,
    )
    assert process.stdin is not None
    assert process.stdout is not None

    pipe = SkillPipe(
        process.stdout,
        process.stdin,
        drain_timeout=1.0,
    )
    try:
        assert pipe.execute("hello", timeout=2.0).payload == "reply:hello"
        assert pipe.execute("multiline", timeout=2.0).payload == "one\ntwo"
        err_res = pipe.execute("error", timeout=2.0)
        assert not err_res.ok
        assert err_res.payload == "remote failure"
        assert pipe.state is SkillPipeState.READY

        with pytest.raises(SkillPipeTimeoutError):
            pipe.execute("slow", timeout=0.03)
        assert pipe.state is SkillPipeState.DRAINING
        assert pipe.wait_until_ready(1.0)
        assert pipe.execute("after", timeout=2.0).payload == "reply:after"
        assert pipe.execute("quit", timeout=2.0).payload == "bye"
    finally:
        pipe.close()
        process.stdin.close()
        process.wait(timeout=2.0)
        pipe.join_reader(2.0)
