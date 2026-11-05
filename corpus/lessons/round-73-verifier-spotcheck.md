# Round 73 — verifier spot-check (non-author integrator)

author: hyaku closure (non-author integrator, @m_zfl)

Subject: kasegi r73 (attempt 1). Lane HEAD measured: `6582d14672315ac84b1632eb69c879ba23b709a4`. Base: `fdf17413f20ea1b19989a090397ece5f49881b9e`. Freeze: `3b53ff839d0747530f95d432aec1ea7b4308fe96`. Report: `.ufo/reports/round-73/kasegi.md` (fleet commit `84cd2260611c472c070c943fea677a904daaa266`, author `kasegi-shokunin <kasegi@shokunin.local>`). Lane lesson under review: `corpus/lessons/round-73.md`.

Dispatch digest (copied from `.ufo/watchdog.log`, mutable):
- `2026-11-05T04:18:30-03:00 launch kasegi round=73 pgid=2187296 driver=hyaku-inline attempt=1`
- `2026-11-05T05:05:57-03:00 complete kasegi round=73; hyaku-inline attempt=1`

Method. Plain measurements over committed bytes (`git show`, `git ls-tree`, `grep`, `sort`, `sha256sum`, `python3` stdlib). The lane-owned gates (`recheck-cwd-census.py`, `frontier-recheck-count.py`, `capture-binding-check.py`) were **not executed**; their committed evidence was read instead (PROTOCOL §Gate standard). Re-executed: one knowledge entry's own recheck line, `sources-census.sh validate`, and live re-opens of two sources.

## 1. Step-1 conformance

| check | command / evidence | observed | result |
|---|---|---|---|
| report by lane identity | `git log --format='%an %H' -- .ufo/reports/round-73/kasegi.md` | `kasegi-shokunin 84cd2260…` | ok |
| SHONEN heading, one line per box | report line 99 `## SHONEN`, four box lines | `[~] [ ] [~] [~]` with pointers | ok |
| cited hashes resolve | `git rev-parse --verify -q <h>^{commit}` | `6582d146…`, `3b53ff83…`, `fdf17413f20ea…` all resolve | ok |
| ancestry against branch ref | `git merge-base --is-ancestor <h> master` | all three exit 0; base is ancestor of freeze and head | ok |
| pushed | `git ls-remote origin refs/heads/master` | `6582d14672315ac84b1632eb69c879ba23b709a4` | ok |
| lane clean and pushed | `jj-lane.sh state …`; `git status --porcelain` | `branch=master local=remote=6582d146 ahead=0 behind=0`; porcelain empty | ok |
| census before/after (fleet) | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok`, exit 0 (W04 duplicate-URL warnings S028 S029 S072 S076 S080 S085, inherited) | ok |
| prompt fidelity | `.ufo/prompts/kasegi-round-73.md` §1–§5 | binding and claim cap (§1–2), L2 floor 8 (§3; wave is 10 seats), report sections (§4), commit-then-push and push scope and L0 (§5), write scope (line 448), commit-hash citation (line 107), SHONEN (§4) | ok with defects R73-V5, R73-V8 |
| dispatch digest matches prompt context | watchdog digest above | identical to the lines given at closure | ok |

Status: the report is a real report naming landed, ancestral, pushed commits. Status `ok`.

Conformance defects (status-neutral): see §5 (R73-V5, R73-V8). Not checked here: the §6 L2 route map against the current `MISSION.md` bucket.

## 2. Claims

### C1 — depth:verifiability (lowest non-retired axis, score 4)

Frozen predicate (`.ufo/waves/round-73/claims.json` at `3b53ff83`): every knowledge recheck carries the lane-root `cd` prefix; census on the C1 tree prints `entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22`, conformant, exit 0; `tree_scope`: the C1 population is the 88 base entries.

Re-measured (plain, committed bytes):

1. First `recheck:` line per knowledge file, prefix-less count:
   - `git ls-tree -r fdf17413… corpus/knowledge/` → 88 files; prefix-less first recheck lines: **11** (matches report `noprefix=11`).
   - `git ls-tree -r 6582d146… corpus/knowledge/` → 89 files; prefix-less first recheck lines: **0**. Distinct prefix on all 89: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && `.
2. Prefix-only proof, all 11 repaired files: stripping `cd … && ` from the head recheck line reproduces the base line exactly, and each file's diff is two changed lines (one `-`, one `+`). Output: `PREFIX-ONLY` ×11.
3. Entry F51 recheck, run verbatim from `/tmp` (`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-73/manifest.json --source S108`): `S108:sha256 OK`, `S108:Q01…Q31 OK` (31 of 31), exit 0.
4. Population invariance (basis for reading the 88-entry population on the landed tree): `grep` over head recheck lines for `round-73|SOURCES|knowledge-expected|osv-post` matches only the F51 entry itself. `git diff --stat fdf17413… 6582d146… -- corpus/instruments corpus/SOURCES.md` shows only `knowledge-expected.txt` (+1), `recheck-cwd-census.py` (+162, freeze commit), and `SOURCES.md` (+3). No base entry's inputs changed beyond its 11 prefixes. [INFERENCE, well-supported] On the landed tree the 88 base entries therefore reproduce the C1-only receipt.
5. Evidence-verified (committed receipt, not re-run): `.ufo/waves/round-73/w1/K73ExecRecheck.census-after.txt` tail reads `RECHECK-CWD entries=88 noprefix=0 exit2_foreign=0 exit0_foreign=66 exit1_foreign=22 exit_other=0 norecheck=0`, `RECHECK-CWD-RESULT conformant`, `AFTER-EXIT=0`. This equals the frozen after-predicate. Selftest, lane receipt `K73ExecRecheck.selftest.txt`: `selftest cases=1 failures=0`, `SELFTEST-EXIT=0` (not re-run).
6. Landed-tree census line (reported): `entries=89 … exit0_foreign=67`. Not re-run (gate). Consistent with 66 + 1, where the one extra is the F51 entry, measured exit 0 in item 3. `K73Falsify-ev-c1-sim-89th-entry.txt` simulates the same line.

Ruling. The lane's `tree_scope` clause is falsified as written: the shipped counter counts the C2 entry in the printed C1 line (lane RC-6, confirmed). That is a counter-scope defect in a lane-owned gate, which the Gate standard (Closure consequence) makes status-neutral. It is not a predicate failure, because the frozen population (88 base entries) measures 66/22/0 on the landed tree by items 2–5. Operator note: if the operator reads the kill rule's literal merged-tree census line as binding, C1 fails on the landed tree and admission flips. This verdict does not depend on that reading being resolved here.

Re-measured: noprefix 11→0; entries 88→89; prefix-only diff; F51 recheck exit 0. Evidence-verified: exit0/1/2 on the C1 tree (committed receipt); selftest (lane receipt). Not verified by me: the landed-tree census line.

Verdict: C1 verifies on its frozen population. Axis `depth:verifiability`: **improved**. The integer score stays 4 (SCORECARD) because the scored `resolve.py` census did not move; the grade rests on the claim counters, which are re-derivable.

### C2 — coverage (score 8)

Frozen target (claims.json): F51, OSV.dev `POST /v1/query`, admitted on S108 with one knowledge entry.

Re-measured (plain):
- Registry rows, `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`: base **107** → head **108**. Only change: the S108 row (`status mined`, `opened 2026-11-05`, `recheck 90d`, `used-by corpus/knowledge/osv-post-v1-query-contract.md`).
- Knowledge files, `git ls-tree`: **88 → 89**.
- `knowledge-expected.txt`: lines **90 → 91**, non-comment rows **88 → 89**. Set-equal to the 89 knowledge filenames (`diff` clean). `LC_ALL=C sort -c` clean. Duplicates: 0.
- PROVINCE: one new frontier line; `grep -c 'F51 —'` = 1.
- Capture: `sha256sum corpus/source-snapshots/round-73/S108.txt` = `304baa7db33000b03fe3b9dda9c1823bccbf980f0a69d9a74a936fb312ffc6b9`, matches the manifest and the S108 row; 150 lines.
- Manifest quotes: 31 of 31 are substrings of the capture at their anchor line (python stdlib check: `bad_anchor []`, none over 25 words).
- New entry recheck: exit 0 from `/tmp` (see C1 item 3).
- `sources-census.sh validate … kasegi`: exit 0 (`kasegi ok`).
- Live re-open of S108 (see §4): quote at line 24 is identical; payload keys, version rule, Git-tag query, pagination triggers (1,000 vulnerabilities / 20 s), and 32 MiB HTTP/1.1 limit all reproduce.

Not re-run (lane gates): `frontier-recheck-count.py` (FRONTIER-CENSUS 51 / entries 54) and `capture-binding-check.py` (records 87). The committed receipts predate landing: `K73Falsify-ev-c2-frontier-count-head.txt` shows `entries=53` with F50 as last row, and `K73Falsify-ev-c2-capture-binding-lane-tree.txt` shows `records=86` plus `FAIL rule=missing-manifest dir=round-73`. The post-landing totals therefore exist only in the report. Their substance is plain-verified above, and every kill-rule clause (row/entry present and unduplicated, quotes located, capture bound by sha, knowledge-expected equal to file set, recheck exit 0, census exit 0) is checked by me directly.

Verdict: C2 verifies. Axis `coverage`: **improved**. The governed frontier count rose 50→51 by one PROVINCE line; the denominator is operator-owned and untouched by the round. The integer score stays 8 for the same reason as C1.

### Non-claimed axis — depth:density (score 9)
Not targeted. The SCORECARD row is untouched in the diff. **unchanged**.

No axis harmed.

## 3. Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | improved | C1 re-derived: prefix-less 11→0 of 88→89 entries; prefix-only; F51 recheck exit 0; C1-tree receipt 66/22/0; RC-6 is a gate-scope defect |
| coverage | improved | C2 re-derived: registry 107→108; knowledge 88→89; knowledge-expected 90/88→91/89; one PROVINCE F51 line; sha and 31 quotes |
| depth:density | unchanged | untouched |

## 4. Discernment spot-check (LEARNING.md)

Sampled from `corpus/lessons/round-73.md` `## Gate` (admits) and from the round's declared non-admissions (rejects, as recorded in the lesson's Residuals and the report). Re-opened live on 2026-11-05 where a URL exists.

| # | item | decision | re-opened source | agree / disagree | reason |
|---|---|---|---|---|---|
| 1 | `corpus/knowledge/osv-post-v1-query-contract.md` (F51) | admit | `https://google.github.io/osv.dev/post-v1-query/` (live) and `corpus/source-snapshots/round-73/S108.txt` | agree | Quote at capture line 24 identical to live page; payload keys (commit, version, package, page_token), version rule, Git-tag query, pagination triggers, and 32 MiB HTTP/1.1 limit all present on the live page. Entry's recheck exits 0 from `/tmp`. |
| 2 | S108 row, tier A, scope "this endpoint's contract" | admit (registry) | same URL; `sha256sum` of the snapshot | agree | Tier A fits the CORPUS definition for official project docs (maintainer statement for that scope). Quote is 14 words (≤25). Page states no rate-limit or API-key rule, so the row's "(the page has none)" holds on the live page. |
| 3 | OSV overview page `https://google.github.io/osv.dev/api/` | reject (not captured, no row; Residual 2) | same URL (live) | agree on decision, disagree on recording | Live page states "Currently there are no limits on the API" and a 32 MiB HTTP/1.1 limit. Not admitting it is correct: no row without opening it into the snapshot, and its claims are outside S108's scope. But the lesson records this only in Residuals; it is not listed as a rejected candidate or as a lead. See R73-V1, R73-V2. |
| 4 | considerthese OSV / query-API proposal | reject (no assimilation; K73ConnectSiblings §4) | `kasegi-shokunin/considerthese/` at head (8 files) | agree | `git grep -niE 'osv|v1/query|query api|osv\.dev' <head> -- considerthese/` returns no matches. |
| 5 | 11 knowledge recheck repairs (C1) | repair (not a gate admit) | base vs head `recheck:` lines | agree | Each repair is prefix-only (one line removed, one added per file); the check text is unchanged. |

Summary: 2 admits and 2 rejects sampled; 4 of 4 decisions agree; 1 recording defect (item 3).

## 5. Trend verdicts (evidence)

- **expansion: improved.** One net new admitted entry (F51) on ground F31 names out of scope, citing a `mined` S108 row whose used-by path resolves (`corpus/knowledge/osv-post-v1-query-contract.md`). Re-verified live (item 1).
- **quality: improved.** Eleven recheck lines repaired (prefix-only, re-derived); the new entry's recheck exits 0 from a foreign cwd (measured). No admitted entry found false in this sample. The 88 base entries' exit codes are evidence-verified from the committed C1 receipt, not re-executed by me.
- **discernment: improved.** This integrator is a non-author outside check. 4 of 4 sampled decisions agree, including both rejects. The lane's own `unchanged` verdict predates this check and is superseded here. The lesson's Gate section does not record rejected candidates as LEARNING.md requires (R73-V1), a recording defect that does not change the agreement.

## 6. Routed defects (the lane fixes next round; status-neutral)

- **R73-V1** (lesson, LEARNING §Files: `## Gate` must list candidates considered, admitted, rejected with reasons). The two rejects (overview page; considerthese proposal) appear only in Residuals and the report. Fix: append a correction entry to the round-74 lesson, or add a dated addendum section; never edit `round-73.md` in place.
- **R73-V2** (SOURCES, CORPUS rule 1 and §Shape "Leads (unopened)"). The OSV overview page is opened in no row and recorded nowhere. Fix: add a `## Leads (unopened)` bullet with its URL, the reason it is not a row, and the statements it makes (no rate limit; 32 MiB HTTP/1.1), marked as a lead and not evidence.
- **R73-V3** (counter, RC-1 to RC-3, RC-6). Affirm the lane's routing. The counter prints the C2 entry inside the C1 line, and its selftest does not call `main()`. Fix in a frozen amendment: population-scoped printed line or an amended frozen `tree_scope`, with a fixture that runs `main()`.
- **R73-V4** (evidence durability, PROTOCOL §Evidence standard). The merged-tree census (`/fast/scratch/hyaku/kasegi-r73/census/after-merged.txt`) lies outside the repo, and the committed frontier and capture receipts predate landing (F50 / `records=86`). Fix: commit the post-landing counter outputs under `.ufo/waves/round-73/controls/` in the round-74 closure-correction commit, naming the measured revision.
- **R73-V5** (campaign addendum §6, binding: "each round must leave the lane measurably more capable — a trial run end-to-end on real domain work"). None in round 73; SHONEN box 2 stays `[ ]`. Fix: next round includes one end-to-end trial, or states why one was not admissible.
- **R73-V6** (freeze order; lane lesson M73-2). The baseline census ran before freeze commit `3b53ff83`. Re-derivation here reproduces the base values exactly (11 prefix-less, 107 registry rows, 88 files), so no contamination found. Fix: run a freeze-check replay before any measurement.
- **R73-V7** (seat). `K73AttackC1` returned empty; the C1 attack seat is missing from the record. Status-neutral; the lane disclosed it.
- **R73-V8** (prompt, protocol-lane note only). The dispatched prompt carries all child-lane items in substance, but "report lands last" and "commit before report" are not stated as ordering rules in §4–§5. Operator-side template item, not a lane defect.

Operator rulings pending (named, not decided here): (a) RC-8, whether first `recheck:` values may run inside a counter via `bash -c`; (b) whether the C1 frozen kill rule's literal merged-tree line governs (see C1 ruling).

SHONEN: no box is fully checkable by a non-author this round. Box 2 is untouched. Boxes 1, 3 and 4 remain lane-asserted `[~]`. Box 4 (no cross-domain bleed; PROVINCE accurate) is the nearest candidate for a non-author `[x]`, to be written by the operator-side review. This integrator wrote no `[x]`.
