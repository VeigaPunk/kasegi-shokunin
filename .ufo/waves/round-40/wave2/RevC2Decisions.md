# RevC2Decisions — wave-2 attack receipt (round 40, falsify wave 2)

Seat: `RevC2Decisions` · Lane: `kasegi-shokunin` · Run-utc: 2026-10-26T22:13:08Z
Item attacked: **the C2 decision set at Y** — the nine queued registry rows S016/S017/S019/S020/S021/S022/S023/S024/S025, their round-40 lesson change-log lines, the S022→S030 / S024→S029 flips, the knowledge-entry citations, and the rejected rows' row-level reason+flip.
Method: every C2 counting command from the frozen `claims.json` re-run against committed bytes (`git archive` of the lane tip into scratch; never the working tree), instruments re-run, deliverable↔committed byte-diffs, live mutation probes of the counters.

## Ref resolution (read-only)

- Lane tip at attack time: `3074c7679d6f527ec3930d7748ccce1dbae4a58a`; working tree clean except untracked `.ufo/waves/round-40/{final-gates,wave2,kasegi-r40-falsify.ready*}`.
- **No commit ever added `.ufo/waves/round-40/final-gates/all-gates.txt`** (`git log --all -- <path>` empty; the directory is untracked). So the claims' `judged_head_rule` ("lane tip Y = J + the receipt only", `git diff --name-only J Y` = the receipt) has no matching commit at attack time — Y-as-commit does not exist; the receipt lives untracked in the working tree.
- Judged head J = `4766b9d` ("integrate wave1"). Post-freeze commits `bfca9ae`/`8717b8b`/`94abbff`/`3074c76` (J2–J5) touch only `declared-blocks.txt`, `LOG.md`, `SCORECARD.md`, `SHONEN.md` — **no C2-relevant file** (`corpus/SOURCES.md`, `corpus/lessons/round-40.md`, `corpus/knowledge/`, snapshots) differs between `4766b9d` and the tip. All commands below therefore ran against the tip's committed bytes; the verdict is ref-robust across J..tip.
- Scratch `S=/fast/scratch/hyaku/kasegi-r40/RevC2Decisions/` (removed before yield; disk-guard checked: 614G free on /fast).

## Counting commands re-run (claims C2, verbatim, over `git archive 3074c76`)

| # | command (claims.json) | claimed | re-run | verdict |
|---|---|---|---|---|
| 1 | `awk -F'\|' '/^\|\s*S0(16\|17\|19\|20\|21\|22\|23\|24\|25)\s*\|/ … if(s=="queued") …' corpus/SOURCES.md` | 9 → 0 | `queued=0` | **reproduced** |
| 2 | same, `if(s=="mined")` | 0 → ≥4 | `mined=7` | **reproduced** (7 ≥ 4) |
| 3 | `grep -rlE '^source: S0(16\|17\|19\|20\|21\|22\|23\|24\|25)' corpus/knowledge \| wc -l` | = mined count | `7` | **reproduced** (7 = 7) |
| 4 | `grep -cE '^\|\s*S06[0-9]\s*\|' corpus/SOURCES.md` | ≥1 | `3` (S060/S061/S062) | **reproduced** |
| 5 | `grep -rlE '^source: S06[0-9]' corpus/knowledge \| wc -l` | ≥1 | `1` (cyclonedx-analysis-subtree.md) | **reproduced** |
| 6 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 22 → 23 | `23`, all 23 rows `admitted` | **reproduced** |
| 7 | `python3 corpus/instruments/frontier-recheck-count.py` | 25/25 → 26/26 | `entries=26 pass=26 exit=0` | **reproduced** |
| 8 | `bash scripts/sources-census.sh validate --root … kasegi` | exit 0 | `W04 S028`, `W04 S029`, `ok`, exit 0 | **reproduced** (byte-matches the lesson's after-census) |

Supporting instrument re-runs (C2 predicate limbs): `source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json` → 8 records (S016/S017/S019/S020/S021/S023/S025/S060), every `sha256 OK` + quote-anchor `ok`, **exit=0**; `capture-binding-check.py` → `records=54 bound=54 unbound=0`, round-40 `records=8 url_bound=8 fetched=8`, **exit=0**; same instrument at base `a7af2ce` → `records=46 bound=46` (reproduces the lesson's "up from 46"). Independent sha256 recompute of the 8 capture files against the manifest: 8/8 match. Wave-1 receipts cross-checked: `wave1/ExecRecheckAll.txt` is exactly the claimed eight lines `S016 exit=0 ok` … `S060 exit=0 ok`; `wave1/ExecBindingCheck.txt` tail = `records=54 bound=54 unbound=0`. Direct quote spot-checks against committed capture bytes: S016 L17 and S023 L151 contain the lesson's quoted spans verbatim.

## Per-row table (statuses from committed `corpus/SOURCES.md` cells; base = `a7af2ce`)

Cell names per the registry header: anchor=$7, teaches=$8, status=$9, opened=$10, recheck=$11, used-by=$12.

| row | base→Y status | change-log line (lesson §"Nine decided rows — status change log") | knowledge entries citing row | rejected reason+flip in row's teaches cell | flip target named |
|---|---|---|---|---|---|
| S016 | queued → **mined** | ✓ "S016 queued -> mined (opened 2026-10-26; entry …/anthropic-cvd-provenance-and-pacing.md; recheck 90d)" | **1** (anthropic-cvd-provenance-and-pacing.md) | n/a (mined) | — |
| S017 | queued → **mined** | ✓ "S017 queued -> mined (… pz-reporting-transparency-trial.md; recheck 90d)" | **1** (pz-reporting-transparency-trial.md) | n/a | — |
| S019 | queued → **mined** | ✓ "S019 queued -> mined (… nist-sp800-216-vdp-framework.md; recheck on-release)" | **1** (nist-sp800-216-vdp-framework.md) | n/a | — |
| S020 | queued → **mined** | ✓ "S020 queued -> mined (… doj-vdp-framework-scope-and-authorization.md; recheck on-release)" | **1** (doj-vdp-framework-scope-and-authorization.md) | n/a | — |
| S021 | queued → **mined** | ✓ "S021 queued -> mined (… cisa-bod-20-01-vdp-minimums.md; recheck on-release)" | **1** (cisa-bod-20-01-vdp-minimums.md) | n/a | — |
| S022 | queued → **rejected** | ✓ "S022 queued -> rejected (superseded by S030, CNA Rules v4.2.0; **reason+flip in row**)" | 0 (none required) | **✗ NO — teaches still the queued text** "Define who has assignment authority…" | **✓ S030** (Gate + change-log + S030 row teaches "supersedes S022") |
| S023 | queued → **mined** | ✓ "S023 queued -> mined (… cisa-cvd-program-stages.md; recheck 90d)" | **1** (cisa-cvd-program-stages.md) | n/a | — |
| S024 | queued → **rejected** | ✓ "S024 queued -> rejected (superseded by S029, official CRA Article 14 text; **reason+flip in row**)" | 0 (none required) | **✗ NO — teaches still the queued text** "Treat the CRA as a manufacturer-side legal duty…" | **✓ S029** (Gate + change-log + S029 row teaches "supersedes S024") |
| S025 | queued → **mined** | ✓ "S025 queued -> mined (… cve-bench-agent-exploitation-benchmark.md; recheck on-release)" | **1** (cve-bench-agent-exploitation-benchmark.md) | n/a | — |

- Change-log lines: **9/9 present**, byte-identical to the wave-1 deliverable `wave1/ScribeRows.changes.txt`; each line's entry path exists and its recheck cadence matches the row's recheck cell (90d/on-release, 7/7).
- Mined count among the nine: **7 ≥ 4** ✓; queued among the nine **0** ✓; queued in the whole registry **0** ✓.
- 1:1 entry mapping holds: each of the 7 mined rows is cited by exactly one entry, each entry has exactly one `source:` line, no entry cites two of the nine, no entry cites S061/S062. All 8 entries (7 + S060) are substantive (121–322 lines), carry `source:`/`verified-at: 2026-10-26`/`ground:`/executable `recheck:` front-matter, and all 8 appear in `corpus/instruments/knowledge-expected.txt`.
- Cell-level diff base→tip over the nine rows: **exactly** status ($9) on all nine + used-by ($12) on the 7 mined rows — matches the lesson's declared touch set ("status cells … plus seven `used-by` cells"); row line numbers unchanged (22–31); registry 59 → 62 rows, none removed; every row keeps exactly one `https://` token (binding precondition for `capture-binding-check` holds).
- Byte-identity: committed S060 row == `wave1/ScribeNewRows.txt` line 1 ✓ (as the lesson claims). Committed nine rows **differ** from `wave1/ScribeRows.decisions.txt` — see D1.

## Defects

**D1 (medium — contradicted claim detail / dropped integration edit). The committed S022 and S024 rows carry no reason+flip in any cell, while the lesson's change-log lines assert "reason+flip in row".**
Evidence chain, all at committed bytes:
1. `wave1/ScribeRows.decisions.txt` L7 (S022) and L8 (S024) delivers teaches = `REJECTED: superseded by S030 (CNA Rules v4.2.0 …) … flip: re-open only if S030's capture is withdrawn …` / `REJECTED: superseded by S029 (official CRA Article 14 text …) … flip: re-open only if S029's Article 14 capture is withdrawn …` — and the scribe's receipt `wave1/ScribeRows.md` L7/L71/L73 declares "the two rejected rows change `teaches` (to `REJECTED: … ; flip: …`) and `status`", "S022 changed: teaches,status", "S024 changed: teaches,status".
2. The integration commit `4766b9d` applied **only** status (+ used-by on mined rows): the committed teaches cells of S022/S024 (`corpus/SOURCES.md` L28/L30) are byte-identical to the base queued text (cell-diff base→tip shows only $9 changed on those rows). The delivered teaches rewrite was dropped.
3. The lesson change-log (copied verbatim from `ScribeRows.changes.txt`) still says "reason+flip in row" for both rows — **false against the committed registry**.
4. Corpus convention violated: all 8 other rejected rows (S026, S027, S028, S056, S058, S059, S061, S062) carry `REJECTED: …; flip: …` in their own teaches cell; S022/S024 are the only rejected rows that do not.
5. No committed counter catches the drop: census `W02` is `length(teaches)<8` only (both committed teaches cells are ~120/~190 chars — the scribe receipt itself notes the threshold is length-based); the awk/grep counters never read teaches; `capture-binding-check.py` does not read teaches; the lesson's "8 of 8 mined rows pass all four limbs" seam check was run over the **delivered** bytes (its own text says so), not the committed rows.
Mitigation recorded: the decision is **not** evidence-free — the lesson Gate carries the full REJECTED reason+flip for both rows and S030/S029's rows record `supersedes S022`/`supersedes S024` — so the C2 kill rule's letter ("rejected rows need reason+flip" in the Gate block) holds. The defect is the false "in row" claim in the committed change-log plus the convention-violating rows. Fix is one edit: apply the delivered teaches rewrite to SOURCES.md L28/L30 (or amend the two change-log lines to "reason+flip in lesson Gate").

**D2 (minor — garbled lesson text).** Lesson Census section: "Registry 59 → 62 rows; tier A +3?mined S016/…/S060, rejected S061/S062, carried S022/S024 flips)" — mangled parenthesis ("+3?mined", unbalanced `)`), evidently meant "tier A +3 (mined …".

**D3 (minor — duplicated heading).** `corpus/lessons/round-40.md` has two consecutive `## Gate` lines (the deliverable `ScribeGateBlocks.txt` also opens with `## Gate`, so the integrator likely pasted the block under an existing heading).

## Observations (not defects)

- **O1 — flip trigger anchored to a superseded row.** S022's flip re-open condition references S030's capture, but S030 was already superseded by S031 (v4.2.6, mined 2026-10-25) at decision time (2026-10-26). The chain S022→S030→S031 is recorded in the rows (S031 teaches "supersedes S030"), so it is traversable; the seat check "S022's flip names S030" passes as specified.
- **O2 — date-cell semantics.** The nine rows keep opened=2026-10-19 (their open date) while every other mined row's opened cell equals its mining date (S029/S030 2026-10-20, S031 2026-10-25, S060 2026-10-26); the wave-1 deliverable had carried opened=2026-10-26. Disclosed by the lesson's touch-set declaration; no instrument validates opened-vs-status.
- **O3 — counter blind spots (live mutation probes on scratch mirrors).** (a) severing a mined row's used-by to `—` (S023): awk/grep counters stay green (citations 7 == mined 7) and the census prints only `W03 S023 mined but unused` with **exit 0** — no committed instrument reds it; (b) a **rejected** row pointing used-by at a nonexistent entry (S022 → ghost path): no check at all (`usedby_findings` skips non-mined rows), exit 0; (c) reverting S016 to queued: census clean (queued is a valid status) — caught only by the claims' own awk counter (queued=1). The registry↔entry link for mined rows is enforced by warnings and manual seam checks, not by any red-exit instrument.
- **O4 — junk control works.** `c2-controls/junk-decisions.md` (all nine flipped to `rejected`, evidence=none) scores mined=0 < 4 under the frozen counter → rejected as required. The lane-root `c2-controls/junk-f20.md` stray is a round-37 artifact (commit `0acffc8`), pre-dating this round — noted, out of round-40 scope.

## Verdict

**C2's nine-row decision set reproduces at Y on every named check except the row-level reason+flip for the two rejected rows.** Queued 0 ✓; mined among the nine 7 (≥4) ✓; change-log lines 9/9 ✓; S022 flip names S030 ✓ and S024 flip names S029 ✓ (Gate + change-log + supersedes records); mined rows 1:1 with knowledge entries, captures sha256-verified, manifest-bound (54/54), source-recheck green ✓; rejected rows carry reason+flip in the lesson Gate ✓ but **not** in their committed rows (D1) ✗. All eight C2 counting commands reproduce; the junk twin is rejected; the census after-state matches. Defects to fix before the claim's "reason+flip in row" wording can stand: **D1** (apply or reword), plus cosmetic **D2/D3**. No queued row, no missing log, no evidence-free decision found beyond D1's row-level gap.
