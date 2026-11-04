# Round 61 verifier spot-check — kasegi (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Verified against lane tip `ebf3e597fa33bb5b7abc9c385bc6c1fd4138a8d7`; base `c33d24ddd11abf1ebdea0dccf7327e9069dd9104`. Report: `.ufo/reports/round-61/kasegi.md` (fleet commit `a73792e6d6680e11dbcbf79ff86513bcd53d6e3e`, author `kasegi-shokunin <kasegi@shokunin.local>`, 2026-11-04 11:52:51 -0300 — lane identity, filed before driver complete line 11:53:30).

## 1. Step-1 conformance

| check | result |
|---|---|
| Report committed by lane identity | PASS — `git log --format='%an %H' -- .ufo/reports/round-61/kasegi.md` → `kasegi-shokunin a73792e6d6680e11dbcbf79ff86513bcd53d6e3e` |
| `SHONEN` heading, one line per box | PASS — `## SHONEN` with 4 `[~]`/`[ ]` lines matching the 4 canonical boxes; no promotion claim asserted |
| Cited lane commits exist and are ancestors | PASS — 6f88f3a7, 13c8060b, 87712747, c819159a, ebf3e597 each `git merge-base --is-ancestor <h> refs/heads/master` → 0/5 failures (jj-colocated; tested against branch ref) |
| No uncommitted round work; pushed | PASS — `scripts/hyaku/jj-lane.sh state` → `branch=master local=ebf3e597… remote=ebf3e597… ahead=0 behind=0`; `git status --porcelain` shows only 4 inherited untracked `w1.ready.dispatched` markers (rounds 57–60), disclosed by the report as left untouched/excluded — not round-61 work (defect note below) |
| Dispatch/completion evidence | PASS — `.ufo/watchdog.log:2375` launch `2026-11-04T11:09:59-03:00 launch kasegi round=61 pgid=3449207 driver=hyaku-inline attempt=1`; `:2389` `2026-11-04T11:53:30-03:00 complete kasegi round=61; hyaku-inline attempt=1`. Prompt committed `b8fa8c7e` |
| Prompt carries template contract | PASS — `.ufo/prompts/kasegi-round-61.md` §1–§5 is a verbatim template rendering (MISSION/AXES binding, 1–3 falsifiable claims incl. lowest-axis rule, frontier step with census command, L2 floor ≥8 one-batched-wave, report contract with SHONEN heading + marker rule, commit-then-push, push scope, L0 channel); hyaku addendum §6 (run-15) present. Five child-lane items all present: report path (:101), commit-before-report ordering (:516 "The report lands last and cites the pushed lane hash"), SHONEN heading requirement (:118,:521), commit-hash citation rule (:106–110), write scope (:448). L2 route language matches MISSION.md (no role pins; host route table) |
| Wave shape | PASS — 11 seats ≥8 in one v1 wave (`w1-spec.json`, `w1-dispatch.json`, `w1-results.json`); attack share 5/11 = 45% ≥25%; connector 1 ≤2; planner held by L1 per addendum convention (same as r59/r60); WAVE-DONE received before report filing |

## 2. Claim re-checks

C1 rests on a lane-owned gate/selftest (figure-audit) — per PROTOCOL §Gate standard (Closure consequence) its **committed evidence** was verified (self-test tally, frozen-run verdict, revision measured); the gate was NOT executed by this closure. Plain byte-level re-derivations were run additionally.

### C1 — depth:verifiability, nominal instrument repair, 4 held → **improved**

- Digest recompute: `git show ebf3e597:corpus/instruments/figure-audit.py | sha256sum` → `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`; `figure-audit-mutbat.py` → `f94393d981eeb93a05f6c57782b787faabfc56bfa5b4775f1c319f405fdd353c`. Both equal the values frozen in `.ufo/waves/round-61/claims.json` → measured bytes = frozen bytes.
- Before receipt `controls/c1-probes-base-r61.txt` (instrument sha 35f7bcd3…): P1/P2/P3 each `exit=1 markers=1` (escape executed); P4 `exit=2 markers=0`; P5/P6 + quoted-semicolon/plain-count controls admitted (35/35/35/1). Matches claims.json `before`.
- After receipts `controls/c1-probes-standin-r61.txt` (sha 051083a2…): P1/P2/P3 `exit=2 markers=0 reason=derive-not-read-only`; P4 still refused; P5/P6/controls pass. Matches the frozen sentence exactly.
- Guard receipt `controls/c1-standin-r61.txt`: selftest `cases=24 failures=0` exit 0 (24 named cases incl. python-traversal/symlink/absolute-refused); mutbat `killed=3/3 survivors=0 controls=pass` exit 0; ledger `figures=35 ok=35 stale=0` exit 0; red fixture `figures=2 ok=0 stale=2 exit=1` (intended negative preserved).
- Frozen-run verdict at named revision: `controls/final-verification-r61.txt` starts `$ git rev-parse master` → `c819159ad7baec5b9d194f13d9ae81fde38ceddc` and reproduces all C1 predicates plus C2 counters post-wave. Kill rule not triggered.
- SCORECARD `diff c33d24d..ebf3e59 -- SCORECARD.md`: depth:verifiability 4→4 delta 0 (nominal per QUALITY R58 — figure gate does not feed the citation-resolution metric), honestly recorded with commands and measured commit.
- Instrument diff contains the repair: derive script paths resolved against the derive root with symlink following (P1/P2/P3 now refused; confinement-off mutant killed per mutbat receipt).

### C2 — coverage, F42 on S094, 8 held → **improved**

Plain re-derivations over committed bytes (lane instruments not executed):

- Registry rows: base 93 → tip 94 (`grep -cE '^\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md`). Knowledge entries: base 79 → tip 80 files (`git ls-tree`); frontier rows and instrument-entry counts each +1 at tip — all deltas match the reported 41→42 / 93→94 / 44→45 moves.
- S094 row shape: NF=13 (11 columns), kind `docs`, tier `A`, status `mined`, opened `2026-11-04`, recheck `90d`, anchor carries revision date (2024-Nov-01) + capture path with line anchors, used-by the new entry. No registry row id/URL removed or changed (diff shows only the S094 row addition + lead-bullet reconciliation).
- Snapshot integrity: `git show ebf3e597:corpus/source-snapshots/round-61/S094.txt | sha256sum` → `663ac16df13b7c93c2d9848265854625c46e8f59d0c39a5bbb4d68bf6573e804` = manifest `sha256` = claims.json `source_digest`. Anchor lines 18/24-25/112/113/118 carry the quoted material.
- Quote word counts (own `awk NF` over the seven pinned quotes): 17/17/14/12/9/5/15 — all ≤25 and equal to the lesson's claimed counts.
- Entry `corpus/knowledge/project-zero-big-sleep-sqlite-variant-analysis.md`: provenance trio first (source: S094 + URL + capture sha; verified-at: 2026-11-04; recheck: source-recheck command), `ground: F42`, falsifiable rules per claim, explicit scope limits (no reproduction, no benchmark conclusion, 150 CPU-hours attributed not measured).
- F42 rows landed: `corpus/README.md:1019` (admitted, S094, preserve-qualifications rule) and `PROVINCE.md:211` (r61 frontier amendment, adjacency limits: chousa research method / kengaku evaluation stay adjacent; live-target refused).
- Frozen counter evidence: `controls/do-nothing-c2-r61.txt` (base rows=41 registry=93 entries=44 capture=76) and `controls/c2-standin-r61.txt` (rows=42 registry=94 FRONTIER-PASS F42 ids=S094 entries=45 capture=77 unbound=0, seven Q-OK) — receipts match claims.json before/after; post-wave re-run pinned in final-verification receipt at c819159a.

### No axis harmed

`diff c33d24d ebf3e59 -- SCORECARD.md`: depth:verifiability 4→4, coverage 8→8, depth:density 9→9 held; no other owned axis row changed; lowest non-retired axis (depth:verifiability 4) worked directly by C1 as required. No capability acquisition claimed (r60 D8 correction of record appended).

## 3. Discernment spot-check (LEARNING.md — non-author)

Re-opened sources: the S094 URL was fetched live (not from the lane's capture) and the snapshot/lesson paths re-read from committed bytes. Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit 0, `kasegi ok …/corpus/SOURCES.md`, six pre-existing W04 duplicate-URL warnings (S028/S029/S072/S076/S080/S085) unchanged from the round-start receipt.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| Admit F42 knowledge entry on S094 (dated Big Sleep SQLite finding account) | admit | Live `https://projectzero.google/2024/10/from-naptime-to-big-sleep.html` — HTTP 200, 56257 bytes (= manifest fetched bytes); 5/5 distinctive quote substrings present in live page | **agree** | Dated 2024 first-party account; all seven quote anchors located at the cited snapshot lines; entry preserves the pre-release qualification, seeded-commit setup, harness-bound negative and experimental caveat; genuinely distinct from held F04 principles, F40 tracker, F41 V8 comparison (neighbor screen ran pre-freeze). Tier A appropriate for a first-party report |
| Reject: universal agent-superiority / "fuzzing cannot find this class" reading of S094 | reject | Snapshot path re-open: `S094.txt:112–113,118` in committed bytes (Q4/Q5/Q6/Q7) | **agree** | The source's own text contradicts the universal reading ("highly experimental"; "target-specific fuzzer would be at least as effective"); rejection is correct taste, flip condition (comparative evidence, declared population, comparable budgets) stated, and no fake rejected-source row was fabricated |
| New SOURCES row S094 — ≤25-word located quotes | admit (row) | Same live URL + recomputed snapshot digest | **agree** | Seven quotes, word counts 17/17/14/12/9/5/15 independently recounted — all ≤25, each located (file:line), teaching grounded in the actual page |

Gate sample: ≥1 admit + ≥1 reject re-opened and agreed; newly written registry row re-opened and quote-checked. The sampled decisions agree with this closure's reading.

## 4. Trend verdicts (closure, agreeing with the report's verdicts)

- **expansion: improved** — plain counts show registry 93→94 and +1 knowledge entry on mined S094; F42 is new coverage-map ground (README F-table + PROVINCE frontier), entry `source:` cites the mined row. Evidence: commands in §2.
- **quality: unchanged** — no superseded/weaker entry claimed; corrections append-only (D1–D8 dispositions, M61-1..5 with red-before R79/R80 0/0→1/1 in `controls/carry-in-r61.txt`); frozen guards green in committed receipts; known residuals (shell expansion, two surviving mutants, instrument-under-scratch deletion, dependency masking) explicitly retained, not sold as safety. Agree.
- **discernment: improved** — round-60 outside findings became restored criteria + new R83 guard and appended corrections; this closure's outside spot-check (§3) agrees on the sampled admit and reject, supplying the independent judgment the report correctly left owed rather than self-certifying via L1 fallbacks.

## 5. Per-axis verdicts

| axis | verdict |
|---|---|
| depth:verifiability | improved (C1 verifies on committed frozen evidence; score 4→4 nominal per R58, honestly recorded) |
| coverage | improved (C2 verifies; 8→8 held) |
| depth:density | unchanged (9 held, not targeted or re-measured) |

## 6. Routed defects / notes (status-neutral)

1. **Lane owes its own repo (next freeze):** the figure-audit docstring retains the overbroad phrase "the audit never runs a mutating command", contradicted by known residuals — the lane itself disavows it (lesson Limits) and plans correction before the next digest freeze. Routed: fix before the next instrument digest freeze; a later claim must not freeze the phrase again.
2. **Two valid additional mutants survive** (report's honest limitation) and the new runner's instrument-under-scratch deletion + masked dependency errors are open: routed as already-planned next-round items (SCORECARD planned 1) — keep them under a new pre-data predicate, without amending round-61 frozen evidence.
3. **Registry hygiene (standing):** six pre-existing W04 duplicate-URL warnings unchanged since round start — dedupe or scope-split S028/S029/S072/S076/S080/S085 in a future frontier pass.
4. **Driver debris:** four inherited untracked `w1.ready.dispatched` markers (rounds 57–60) remain in the lane worktree, disclosed and excluded by the lane; not round-61 work. Operator-side cleanup (untracking rule) still owed from prior rounds.
5. **Wave honesty note:** three seats (ScoutSource-11, EntryClaims, SiblingOverlap-12) died on provider model unavailability (`permission_denied` swe-2/devin, then 401 deepseek route) with terminal proc statuses expired; error telemetry preserves this honestly, no fabricated successes, and the lane did not count L1 fallbacks as independent seat votes. Consequence: independent in-round reviewer coverage rested on the 8 delivering seats; the owed outside admit/reject judgment is discharged by §3 above. Operator-owned route recovery (live @m_zfl authority) untouched by the lane — correct.
6. **SHONEN/promotion:** boxes are honestly marked `[~]`/`[ ]` with no self-written `[x]`; box 2 (end-to-end bounty task) remains open and is not checkable by a non-author this round — promotion remains an operator decision; nothing here constitutes promotion evidence.
7. Conformance: none beyond the notes above. Report, prompt, dispatch evidence, commit ancestry, push state and wave shape all conform.
