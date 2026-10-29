VERDICT: INFO

# R46bScoutRoutedDefects — inherited-defect sweep, round 46 attempt 2

Seat: read-only scout. No files outside this report were written; no scratch dir was created (read-only sweep, no fixtures); no tools installed. All git calls read-only (`log`, `status`, `ls-tree`, `diff`, `diff --quiet`), all absolute under `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Method and control

Files swept: `corpus/lessons/round-42.md`, `round-43.md`, `round-44.md`, `round-45.md`, `round-46.md`, `round-45-verifier-spotcheck.md` (grep tool, path glob `corpus/lessons/round-4[2-6].md` + spotcheck; case-insensitive).

Control (do-nothing): `grep QQQQNOSUCHTOKEN` over the same six files → `No matches found`. The matcher does not match vacuously.

Finding 0 — the five assignment-enumerated phrases under-match this corpus. `grep 'routed to round|append in a later round|repair next round|fix in round|owed'` returned only two near-misses, neither a routed defect:
- `round-43.md:145` — "7 of 7 proposals **rowed** at the round-43 base" (substring `owed` in "rowed").
- `round-44.md:174` — "Crit01's 'the report-**owed** sections are unfiled'" — a quoted critique explicitly dismissed two lines later ("Not changed, with reasons: … the normal order").

The corpus's actual route vocabulary (broadened sweep `rout|owe|flip:|still open|stays open|unresolved|defer` plus `open questions|still open|unexercised|queue open|unresolved|open for|not appended|NOT appended` and `parked|box 2|SHONEN box`): "the lane must fix these in round 46" (spotcheck §6 heading, `round-45-verifier-spotcheck.md:93`), "C1 targets eight routed R43 defects" (`round-44.md:3`), "routed queue open" (`round-42.md:24`), "flip: a later round whose claim is the ZDI deadline rule" (`round-46.md:25`), "appended in a later round together with a pin amendment" (`round-46.md:29`), "routed at" (`round-42.md:31`).

## Committed-bytes basis (all re-run this session)

`git log --oneline -6`:
```
ee03806 round-46 (attempt 2): wave a2w1 spec (64 seats, v2) + dispatch payload + builders + ready file
fe0f56b round-46 (attempt 2): freeze claims C1 counter-mutation coverage + C2 frontier F29, counters v1 (mutbat, f29-gate), S074 capture + manifest-a2, R50 receipt, controls
04af9bc hyaku run12: remove stale round-42 falsify.ready (orphan of closed round; run-11 wrapup residue)
7eb7786 round-46: wave-2 selftest-mutation report (honest stop)
510a2d5 round-46: lesson, LOG, SCORECARD, SHONEN, registry rows, QUALITY correction, final measurement
eb874bc round-46: QUALITY R50-R52, counter errata E2, final-measure script, wave-2 reports
```
`git status --porcelain` (tip): only `.ufo/waves/round-46/attempt2` wave files (` M` build-wave2-spec.py, wave2-spec.json; `??` a2w1.ready.dispatched, controls/final-measure.sh, counter-errata.md, digest-wave.py, wave1/, wave2/). **No corpus path is modified or untracked** — every working-tree corpus read below is committed base bytes (`04af9bc`).

`git ls-tree --name-only 04af9bc9… -- <paths>` (present at base): `corpus/instruments/r46-c1-gate.py`, `r46-c2-gate.py`, `r46-counters-selftest-c1.py`, `r46-counters-selftest-c2.py`, `r46-landing-gate.py`, `r46-plain-measure.sh`, `.ufo/waves/round-46/counter-errata.md`, `.ufo/waves/round-46/controls/plain-rows.sh`. Absent at base: `r46-mutbat.py`, `r46-f29-gate.py`.

`git ls-tree --name-only fe0f56b7… -- …`: `corpus/instruments/r46-f29-gate.py`, `corpus/instruments/r46-mutbat.py`, `corpus/source-snapshots/round-46-a2/S074.txt`, `corpus/source-snapshots/round-46-a2/manifest.json` — committed at the freeze.

`git diff --quiet 04af9bc9… fe0f56b7… -- corpus/instruments/r46-c1-gate.py corpus/instruments/r46-c2-gate.py && echo …` → `counters byte-identical base..freeze` (the frozen counters are unamended; amendments are L1-integration errata only).

`git diff --stat 04af9bc9… -- corpus/lessons/round-46.md corpus/SOURCES.md corpus/README.md corpus/knowledge/considerthese-proposals-ledger.md corpus/instruments/r46-c2-gate.py corpus/instruments/r46-mutbat.py corpus/instruments/r46-counters-selftest-c1.py corpus/instruments/r46-counters-selftest-c2.py corpus/knowledge/github-repository-security-advisories.md` → only `corpus/instruments/r46-mutbat.py | 184 +++…` (the freeze-commit addition). **The ledger append and the r46-c2-gate.py pin amendment are not yet in committed bytes.**

## Part 1 — routes already closed (verified chain, for discrimination)

| Routed at | Defect set | Closed where | Evidence (path:line) |
|---|---|---|---|
| `round-42.md:24` before-cell ("routed queue open: I1, I3, I7, I5/I12, I6, capture-binding missing-path/URL variants, frontier-counter status-flip blind spot"; plus D-r41-1, D-r41-3) | r41-spotcheck §5 item 6 queue | Round 42 | after-cell of `round-42.md:24`: "`r42-closure.sh` landed export-mode … `closed=13/13 exit=0` at Y … J1–J13 close the routed families"; M42-1/M42-2 fixes are J1/J2 (`round-42.md:31-32`) |
| `round-43.md:31` "all seven routed by the round-42 verifier spot-check (§9.6)" | RD42-1…6, RD42-8 (routes at `round-42-verifier-spotcheck.md:173-177`, `:64`, `:297-303`) | Round 43 (K15/K16/K17/K18, erratum-3, correction lines) | `round-43.md:37-43` fix cells; re-measured `.ufo/waves/round-43/c1-controls/do-nothing.txt` §C; round-44's counter later reads the R43 set `total=8 fixed=8 unresolved=0 exit=0` (`round-44.md:83-84`) |
| Round-43 spot-check §6 (eight routes, named at `round-44.md:3`, `:78-80`) | D1–D8 | Round 44 attempt 2 | `round-44.md:83-84` `routed-defects total=8 fixed=8 unresolved=0 exit=0`; v1 counter falsified and replaced (`round-44.md:125,166,189`) |
| Round-44 spot-check §6 items (five, named at `round-45.md:3`) | R1–R5 | Round 45, independently verified | `round-45-verifier-spotcheck.md:28-38`: "5/5 plain", counter `total=5 fixed=5 unresolved=0 exit=0` |
| Round-45 spot-check §6 item 1 | report/commit ordering | Round 46 attempt 1 — did not reproduce | `round-46.md:11` (item 1 → M46-2), M46-2 row `round-46.md:16` |

## Part 2 — round-46.md `## Routed defects` items 1–5 (spot-check §6 → round 46): closed by committed bytes?

Answer section is committed at base: `corpus/lessons/round-46.md` `## Routed defects (round-45 spot-check §6)` (items at `:58-62`; file byte-identical to base since absent from the base..worktree diff).

| Item | Answer (committed) | Closed by committed bytes? | Evidence |
|---|---|---|---|
| 1 report/commit ordering | M46-2 (not reproduced on committed clocks); gate built anyway: `r46-landing-gate.py --pre-report` / `--post-report`; report names the lane hash only after `ls-remote` | YES — instrument committed at base | `git ls-tree 04af9bc9…` lists `corpus/instruments/r46-landing-gate.py`; selftest `cases=30` (`round-46.md:16`) |
| 2 counter classification | Decided in-round, before closure: counter erratum, objection + partial-disagreement recorded | YES — erratum file committed at base | `git ls-tree 04af9bc9…` lists `.ufo/waves/round-46/counter-errata.md`; `round-46.md:60` |
| 3 plain second measure per claim | `r46-plain-measure.sh` + `controls/plain-rows.sh`, every claim carries a `plain` list | YES — both committed at base; attempt-2 `claims.json` carries `plain` lists for C1 and C2 (read this session) | `git ls-tree 04af9bc9…` lists `corpus/instruments/r46-plain-measure.sh`, `.ufo/waves/round-46/controls/plain-rows.sh` |
| 4 S072/S070 supersede pair | Recorded in `## Registry changes` | YES — committed, and worktree SOURCES.md is byte-identical to base | `corpus/SOURCES.md:162`: "- Supersede-pair note (round-45 spot-check section 6 item 4, `corpus/lessons/round-45-verifier-spotcheck.md:98`): S072 supersedes S070 … The census therefore prints W04 for S072, which is expected." |
| 5 per-held-axis next promotion limb | Named (verifiability: "the next claim targets the remaining 22" gated recheck lines; coverage: "No 8 → 9 criterion is written; this lesson does not invent one") | The DECISION is committed; its substance is OPEN — see table below (O-2, O-3). Attempt 2's C1 targets counter mutation coverage instead of the 22, and C2 is a +1 expansion row, so neither limb moves | `round-46.md:62`; attempt-2 `claims.json` C1 before-value = mutbat before receipt |

## Part 3 — OUTSTANDING-DEFECT TABLE (what the report's Mistakes section needs)

Dispositions: **touches** = attempt 2 is executing the close (per frozen `claims.json`); **silent** = attempt 2 neither closes nor carries it; **carry** = must carry forward to a later round.

| ID | Routed at (path:line) | Outstanding item | Attempt-2 disposition | Evidence this session |
|---|---|---|---|---|
| O-1 | `round-46.md:29` | considerthese ledger append `## Round-46 dispositions` + the `r46-c2-gate.py` G6 ledger-exemption **pin amendment** | **touches — the one this round closes** (in flight, NOT yet in committed bytes; lands at L1 integration "if the wave verifies it, else the deferral is carried") | `claims.json` `frontier_step`: "considerthese ledger dispositions append (the attempt-1 routed item) lands this round together with the r46-c2-gate.py ledger-exemption amendment"; `git diff --stat base` shows both files unchanged vs base |
| O-2 | `round-46.md:62` (item 5, verifiability half) | The 22 remaining gated recheck lines (`gated=22` of 65; "the next claim targets the remaining 22") | **silent** — attempt-2 C1 is counter mutation coverage, not the 22 re-grounds; the attempt-1 stated "next claim" was superseded by M46-4/QUALITY R50 (mutation coverage shipped unmeasured). **Must carry forward**, and the report should note the deviation from the recorded intent | `claims.json` C1 before/after (mutbat uncaught=7/13 → 0); `round-46.md:15` M46-1 row |
| O-3 | `round-46.md:62` (item 5, coverage half) | No `8 → 9` coverage criterion written | **silent** — attempt-2 C2 is "+1 frontier row = expansion count, not a coverage-ratio move" (`round-45-verifier-spotcheck.md:71`). **Carry forward**: the criterion still needs writing | `round-46.md:62`; spotcheck §3 coverage row |
| O-4 | `round-46.md:29` tail; `round-45-verifier-spotcheck.md:103` | SHONEN box 2 (end-to-end domain task) still unexercised | **silent** — no attempt-2 claim exercises it. **Carry forward** | spotcheck: "Box 2 … is not exercised"; `claims.json` has no box-2 claim |
| O-5 | `round-46.md:15` (M46-1) | Attempt-1 counters shipped with no mutant battery — the residual is exactly attempt-2 C1 | **touches** — in flight; before-value frozen (`mutbat-before.txt`: c1 uncaught=7, c2 uncaught=13); uncaught=0 is the after | `claims.json` C1 `expect_before`; freeze-tree reading in C1 block |
| O-6 | `round-46.md:25` flip (2) | ZDI policy lead — "flip: a later round whose claim is the ZDI deadline rule, opened and cited by that round" | **silent** — not a defect, an admitted-lead flip; no attempt-2 claim takes it. **Carry as a lead** | `claims.json` C2 = F29 advisories only |
| O-7 | `round-46.md:25` flip (3) | `date-order-author` landing check withdrawn (M46-2) — "flip: a clock that survives amends is found" | **silent** — flip condition, no attempt-2 claim. **Carry as a flip** | M46-2 row `round-46.md:16` |

Not routed defects, listed to keep the sweep honest: `round-44.md:56` "Existing RFC 9116 cross-lane question remains parked and unchanged" — parked, no round owns it, attempt 2 silent; `round-45.md:50` "no proposal adopted (the scout seat died)" — resolved by round 46 attempt 1 adopting proposal 3 (`round-46.md:29`).

## Limitations

1. Mid-flight wave: O-1/O-5's "touches" is read from the frozen `claims.json` and the wave spec commit `ee03806`, not from landed bytes — no corpus byte has changed since base `04af9bc`. Whether the close lands is the L1 integration's to prove.
2. The r41 I-queue (O-table Part 1 row 1) is classified closed from `round-42.md:24`'s after-cell and the absence of any later reopen in the swept files; `round-41-verifier-spotcheck.md` §5 item 6 itself is outside the assigned sweep set and was not read.
3. `round-42-verifier-spotcheck.md`, `round-43-verifier-spotcheck.md`, `round-44-verifier-spotcheck.md` are outside the assigned sweep set; their routes were captured indirectly via the lessons' RD42-*/D*/R* rows.
4. I executed no counter, battery, or gate (executors own those runs); the before-values quoted here are quoted from `claims.json`/lessons, not re-measured by me.
5. Grep line numbers are working-tree lines; the corpus files are byte-identical to base `04af9bc` (proved by the empty base..worktree diff over them), so the pointers are committed-byte pointers.
