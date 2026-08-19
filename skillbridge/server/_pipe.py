from __future__ import annotations

# Design Principle:
# The python daemon server supports multi thread conection
# by `ThreadMixIn`, while skill command execution is single threaded, 
# must be in order. 
# ----------------------
# We would use two clients, A and B to illustrate multi thread orchestration:
# User Jack is implementating certain algorithm for EDA automation, the psuedocode is as follow:
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
# where there are two types of speed:
# - the python calculation spped (cpu intensive)
# - the skill execution speed (io intensive, because we would be waiting for its return)
# The two modules are independently solved, so multi-thread would be enable --
# each thread corresponds to one TcpServer (tcp connection).
# The in-order execution of skill code DOES not guarantee the return order of results,
# which may result in out of order response fetched by our python daemon.
# To resolve this, learn from TCP protocol, we may add a REQUEST_ID to the message
# and put them into a queue(Queue.queue) -- like what we specify in the mock Skill server.
