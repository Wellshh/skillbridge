from enum import auto
from enum import Enum
from __future__ import annotations

# One physical SKILL IPC channel is owned by exactly one SkillPipe instance.
# The SkillPipe owns one daemon reader thread; no TCP handler or application
# thread may read directly from the SKILL response stream.
#
# The Python TCP server may handle multiple client connections concurrently,
# but the underlying Cadence SKILL runtime is a single serialized resource.
# At most one command may be sent without having consumed its complete response.
#
# With the direct API, TCP handler threads may call SkillPipe.execute()
# concurrently. SkillPipe serializes complete command/response transactions.
# A blocked handler thread does not block the whole Python server.
#
# A higher-level dispatcher may optionally provide:
#   - a bounded FIFO request queue,
#   - one executor worker,
#   - one Future per submitted job,
#   - deterministic admission order,
#   - queue backpressure and cancellation-before-dispatch.
#
# The dispatcher queue is used for command admission, not for response routing.
# Each caller waits on its own Future. Only the SkillPipe reader thread reads
# SKILL responses.
#
# A local request/job ID is useful for tracing, metrics, timeout diagnosis, and
# late-response auditing. It is not required for response correlation while
# the channel permits exactly one in-flight request.
#
# A wire-level request ID is required only if multiple requests are allowed to
# be outstanding on the same protocol stream. This design intentionally does
# not permit that, because SKILL execution is single-threaded and pipelining
# would add timeout and recovery complexity without increasing throughput.
#
# "Fast" and "slow" are scheduling or timeout policies, not pipe operations.
# A running slow SKILL command cannot be preempted by a later fast command.
#
# After a response timeout, the remote execution outcome is unknown. Draining
# a late response restores protocol synchronization only; it does not cancel
# or roll back SKILL-side changes.

"""
# ===== Skill Server ======

class SkillExec:
    req_id: int = -1 # starting message is at starting 0
    mem = []

    # The real Cadence skill runtime environment
    def _mem_load(self, data):
        load_into(self.mem, data)
    
    def _mem_read(self, req_id):
        return mem[req_id]

    def _recv(data, timeout): 
        req_id += 1
        _mem_load(data)

    def _exec_fast(self, skill_code, timeout):
        _recv(skill_code)
        _mem_read(self.req_id)

        log(Fast execution of script {skill_code})
        
        # seconds later....
        return exec(data)

    def _exec_slow(self, skill_code, timeout):
        _recv(skill_code)
        _mem_read(self.req_id)

        log(Slow execution of script {skill_code})

        # thousands of years later...
        return exec(data)

# ======== Python Client ========

def skill_raise(reason):
    # timeout, something wrong during skill execution
    raise SkillExecError(reason)

# Slow algo running in python
def _slow(module):
    # modulized operation

    module = prepare(module)
    _ok, _res = _send(module, timeout=timeout) 
    if not _ok:
        skill_raise("Some reasons...)

    result = run(module)

    # Waiting for skill execution
    ok, res = _send(result, timeout=timeout)
    
    if not ok:
        skill_raise("Some reasons...")

    return res

# Quick skill script execution
def _fast(skill_code):
    ok, res = _send(skill_code, timeout=timeout)

    if not ok:
        skill_raise("Some reasons...)

def _send(data, timeout):
    # send to skill execution 
    return SkillExec.exec_fast(data, timeout=timeout) 

def algo(ignore_module_error):
    # module_1: fast python, slow skill
    # module_2: slow python, fast skill
    modules = [module_1, module_2]

    for module in modules:
        try:
            # ==== Enter slow zone ====
            # May use `ThreadPoolExecutor` to accelerate
            res =  _foo(module)

            # ==== Exit Slow zone ====

            res_ = _fast(skill_code)
    
        except SkillExecError:
            if ignore_module_error:
                continue
            raise 

    modules
"""

class _PipeState(Enum):
    READY = auto()
    EXECUTING = auto()
    DRAINING = auto()
    DESYNCHRONIZED = auto()
    BROKEN = auto()
    CLOSED = auto()

class Pipe:
    
    __slots__ = (

    )

    
