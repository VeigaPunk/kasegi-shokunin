# RevengerC1 — anchorcheck fidelity review (round 28)

## Scope and state

Reviewed the frozen C1 contract, anchorcheck history (`eb5b590` r15, `ed44a92` r18, `d1e6e8f` r19, `94aace2` root-alias fix), lessons round 15–27, instrument README, and the ExecImplC1 diff against the live instrument. The live file is now at SHA-256 `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514` (523 lines); the reviewed diff declares the same digest. LSP device/server was unavailable in this seat; history was reconstructed with git show/diff and literal file reads. No production files edited.

## Reconstructed preservation contract / evidence chain

- **Verdict separation is longstanding.** The r15 implementation had only MISSING-FILE/PAST-EOF and printed source lines. The r18 rewrite explicitly records the round-16 critic ruling: keep IN-RANGE variants, MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN and LOST-RECORDED distinct; range validity feeds separate semantic review. Round-19 added BASE-ABSENT without folding it into another class. Round-28 must add BOUNTIES-ABSENT while preserving that separation.
- **LOST-RECORDED semantics must remain recorded-not-fail.** r18 specifies marked lost anchors are reported separately, not checked, and never counted as validated; r19 extends accepted markers from `[lost-tree]` to `[lost-tree]` or `[lost-base]`. Round-27 carry-forward explicitly says LOST-RECORDED is not a fail class. The diff retains its separate bucket and excludes it from FAIL_CLASSES; marked citations continue through the existing early recorded-loss branch.
- **Pins and resolution order must remain intact.** r18 documents pin-first lookup (`git show <hash>:<relpath>`), ORIGIN, lane-base, explicit MIRROR, then unprefixed mirror. `PIN-BROKEN` remains a separate verdict. `LANE_DIRS` remains `('.', 'corpus/knowledge', 'corpus/lessons', 'corpus/instruments')`; bare-name lane search order and lane-root-relative slash paths are unchanged in the diff. Existing ORIGIN/MIRROR realpath confinement and derived-root behavior are retained; r19 defines env override, first existing candidate, canonical absent fallback. Round-28 adds BOUNTIES root derivation with `KASEGI_BOUNTIES` then canonical `~/Projects/bounties`, and confines it with realpath like the existing absolute roots.
- **Review output is a consumer contract.** Since r15 the summary has the `== <src>: N in-range cite instances, M bad; K distinct anchors` prefix. r18 adds the separated summary buckets; r19 adds `BASE-ABSENT=B`. The instrument README documents printed source lines as semantic-review input. The diff keeps the per-cite `OK md:<line> <token>  [<source>]` form and existing fail-line forms; adds `BOUNTIES-ABSENT md:<line> ...` to the fail-first lines; leaves `bad` as the historical MISSING-FILE + PAST-EOF + OUTSIDE-BASE count. It deliberately does not append `BOUNTIES-ABSENT=` to the summary, because the frozen fixture counter counts matching lines and expects exactly one.
- **Round-25–27 routed debt is the intended change, not a regression.** Round-25 records that every class exited 0 (`main()` fell through) and CITE lacked the bounties arm; round-26 carries both; round-27 carry-forward 2 specifies FAIL_CLASSES = MISSING-FILE, PAST-EOF, OUTSIDE-BASE, PIN-BROKEN, BASE-ABSENT, BOUNTIES-ABSENT, with isolated selftest fixtures. The diff implements precisely these six exit-failing classes, adds the bounties arm and `--selftest`, and retains 0 for a file whose only losses are LOST-RECORDED.

## Diff findings

No documented resolution or verdict behavior appears removed or weakened in the reviewed diff. Pin-first behavior, lane lookup order, origin/mirror resolution and confinement, LOST-RECORDED treatment, per-line source text, and historical summary fields remain. BOUNTIES-ABSENT is a new distinct class; a present bounties file uses plain IN-RANGE (same convention as mirror), an absent root uses BOUNTIES-ABSENT, and an escape uses OUTSIDE-BASE. Exit semantics intentionally change per frozen C1.

Selftest implementation in the diff contains a fixture for each of the six fail classes plus bounties-in-range, LOST-RECORDED, and clean controls. Its assertions compare the complete parsed verdict vector and process status. This is code review only; this seat did not execute `--selftest`.

## Output-pattern check / discrepancy

Observed landed `SKILL.md` summary:

`== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`

The frozen LOST-RECORDED sed pattern extracts `306` correctly. The bounties fixture's frozen `grep -c BOUNTIES-ABSENT` returns `1`. However, the literal frozen bad-count sed from `claims.json` — `sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'` — prints no line against the observed summary, because the summary has `0 bad;`, not `bad; 0 bad`. Thus the output format itself retains the established `M bad;` format, but that exact frozen sed shape does **not** match it. This is a frozen-counter/summary-pattern discrepancy to disclose; do not claim that sed counter passed. The summary directly shows the expected `0 bad` and `LOST-RECORDED=306` values.

## Confidence

High on history-derived contract and diff fidelity (direct git history, lessons, and diff/live digest). High on observed output formatting and the frozen sed mismatch. Runtime selftest/isolation behavior is unverified by this reviewer and must be established by the assigned verification run.
