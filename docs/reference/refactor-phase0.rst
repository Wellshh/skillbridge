Pythonic refactor Phase 0 baseline
==================================

Scope
-----

This baseline was recorded from commit ``290645e`` on 2026-08-27. It separates
local evidence from Windows Allegro evidence.

Compatibility and static gates
------------------------------

* Supported Python versions are 3.10 through 3.14.
* Ruff, mypy, and Pyright use Python 3.10 semantics.
* ``Self``, ``override``, ``assert_type``, and ``ParamSpec`` come from
  ``typing_extensions``.
* The generated Allegro stub check reports 792 total APIs, 782 exact, 3 fallback,
  1 missing, and 6 document-only.
* Clean Python 3.10, 3.11, 3.12, 3.13, and 3.14 environments each report
  415 passed and 158 skipped with Pydantic 2.13.4. Allegro tests remain skipped
  without ``--allegro``.

Wire and collection contracts
-----------------------------

* Python ``tuple`` and ``list`` values both encode as SKILL lists.
* SKILL ``nil`` decodes to ``None`` by default. Collection APIs normalize it to
  an empty list only when their operation metadata explicitly requests that policy.
* Remote tables retain their native SKILL default-value behavior.
* The legacy remote-vector iterator stops at the first unbound slot. Fixed-length
  sparse snapshots with an ``UNBOUND`` sentinel belong to Phase 4 and must replace,
  rather than silently preserve, this legacy behavior.

RPC baseline
------------

The unit suite fixes these steady-state costs:

* a high-level read is one RPC;
* an immediate write is one transaction RPC;
* a preview is one dry-transaction RPC;
* a non-empty batch is one transaction RPC;
* command construction and an empty batch are zero RPCs.

Local micro-latency
-------------------

Measurements used Python 3.11.14 on macOS 26.5 arm64, 100,000 iterations and
9 repeats. Values are median nanoseconds with interquartile range in parentheses.

* ``Socket.encode_header``: 156.1 ns (2.2 ns)
* ``Socket.decode_header``: 123.2 ns (0.3 ns)
* ``Translator.encode_call``: 1,796.5 ns (21.6 ns)
* ``Translator.decode``: 2,905.1 ns (26.0 ns)
* ``Response.recv`` over a reset ``StringIO``: 818.6 ns (3.5 ns)

These are local implementation baselines, not IPC or full RPC measurements.

Windows Allegro gate
--------------------

No Windows Allegro latency was measured in this checkout. The first Windows run
must record median and interquartile range for steady-state ``plus``, request and
response payload sizes, and ``session.board()``, ``session.components()``, and
``session.nets()``. Live ``ws[...]()`` measurements are full-stack RPC results and
must not be presented as Socket, Pipe, or SKILL-parser latency.
