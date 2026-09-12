# DRC probe v2 checkpoint 0

This directory is independent of `.artifacts/drc-probe/`; historical evidence is untouched. At this checkpoint I only recorded the actual checkout, source board hash, old probe hashes, API contract evidence, and an execution design. Allegro was not started.

## Historical audit and errata

The old report is tied to HEAD `57a4483a8c4ef5e680e857827eb9651418dc79ac` and a clean worktree. It reports the B/C observations, but v2 must register these corrections before relying on them: B GRID_EQ error is about `-2.0458e-14 mm` (Line–ARC), B STAIR_n7 is flagged on both sides, B re-query compared 5 of 19 arcs and C had 18 arcs, `2.5e-6 / 5.6e-14` is about 7.65 orders of magnitude, the old GRID oracle converted quantized values through float, CC_GOLD text/verdict is inconsistent in places, the rp calibration interval was `(0.14994626897, 0.15004626893]` with an `rp∈gZ` prior, and the old ARC–Via window did not distinguish radial from vertical measurement. The old claim that `axlAirGap` was unavailable is also a v2 erratum: its documented contract is present and the prior local measurement evidence should be re-audited rather than treated as an API absence.

## Stage 0 checker gate design

Use a fresh disposable copy and an owned CLI Allegro process on a unique port. First snapshot all existing markers and DRC settings/category/waiver context. Create one unmistakable spacing violation as a positive control, call the item checker, and compare returned marker list, count mode, and post-update marker snapshot. Repeat the positive control to observe duplicate suppression. For each candidate negative, require a complete marker snapshot and exact target/partner identity (type, net, layer, unique object identity or complete geometry); an empty or unmatched list remains `AMBIGUOUS`/`NOT_TESTED` until this gate passes. `axlDRCGetCount` is supporting evidence only because its documentation allows stale totals; `axlDRCUpdate` is immediate and must not be treated as rollbackable.

## Minimal discriminating samples

After the gate: (1) B `GRID_EQ`, `FLIP_LO`, `FLIP_HI` at the same absolute placement and learned rule R, to separate exact-grid equality from sub-grid center movement; (2) Stage I exact binary64 half-grid values `0.03125` and `0.09375` plus `nextafter` sides, with negative counterparts, separately on Line endpoint, Via position, and ARC endpoint; (3) ARC center horizontal, vertical, 45° and `(0.7,1.1)` chords with beta then alpha scans; (4) Stage II finite non-semicircle sweep controls and a non-axis ARC–Via sample only after padstack geometry is read independently; (5) Stage III translated copies with identical relative geometry and one wide-margin control.

## Decisions for main-agent review

1. Approve Stage 0 checker gate as a hard prerequisite for CLEAN and boundary searches.
2. Confirm whether the first Windows run may use the existing route board only through a disposable copy, with no changes to its source asset.
3. Confirm Stage II ARC–Via remains conditional until padstack geometry is independently read; otherwise prioritize Line–ARC/ARC–ARC.
4. Keep `axlAirGap` as an auxiliary measurement channel until its mode/return payload is verified on S048; never equate it automatically with DRC.
