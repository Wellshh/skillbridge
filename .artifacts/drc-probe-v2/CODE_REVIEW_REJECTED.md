# Stage 0 draft disposition

Status: `CODE_REVIEW_REJECTED` (implementation defect; no platform failure).

The `stage0_ia.py` draft is frozen and must not be run or used as evidence. Known defects at rejection: it constructed the report with `board=None`; it did not establish run cwd/stdout/stderr/cleanup evidence; and its earlier runtime had contaminated two tracked Allegro log files. Those files were copied into this directory as `batch_drc.log,2.runtime-contamination` and `batch_drc.log,3.runtime-contamination`; their worktree content hashes now equal the HEAD blobs. The draft is not a completed Stage 0 gate.

Runtime repair accounting: two runtime attempts occurred before this disposition (one import failure and one diagnostic run). No further runtime was started after the rejection. This artifact does not claim Stage I–III completion.

## Offline oracle handoff

`oracle_regression.py` and `oracle_regression.json` are the only completed deliverable from this handoff. The script computes B GRID_EQ and STAIR_n6 from Fraction geometry, computes the CC_GOLD grid candidate from explicit logged center/radius Decimal inputs, compares exact grid verdicts with the old binary64 contaminated values, imports the historical `arc_oracle.model_GRID`, and asserts the expected false positive on B GRID_EQ. Its successful status is `OFFLINE_REGRESSIONS_PASS`.
