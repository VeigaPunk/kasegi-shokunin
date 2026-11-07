# ReviewC1Labels — round-94 wave 1, attempt 1 (C1 tranche 9)

Seat: `ReviewC1Labels` (leaf, non-author). Wave `kasegi-r94-w1`, 13 seats.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Pinned revs: base `dff5a0a01e8aafe6be81f4ee61567745c3c4c485`, freeze
`96b5033f4dfa8d6605c13e0c9aad458be3cd7df3`, C1 landing
`d51220aeb4a538b7b211bb2629e83210669cd56d`, C2 landing
`996460861d4130ddb2da6b7554e905d3e47504a3`.
Read-only on the lane's git/jj state: this seat wrote only
`.ufo/waves/round-94/w1/ReviewC1Labels.md` and
`.ufo/waves/round-94/w1/ReviewC1Labels-receipts/`. Scratch
`/fast/scratch/hyaku/kasegi-r94/ReviewC1Labels` removed on exit.

## Verdict

**C1 STANDS on P1–P3, re-derived here from the pinned bytes; P4 is not fully
re-derived (2 of 12 controls re-run by this seat, the other 10 cited from the
frozen 12/12 receipt).** The 19 repoints are byte-exact at their labelled
anchors and the meter/path/sha limbs reproduce. Content check of the 19 landed
rows: **18 CORRECT / 1 PARTIAL / 0 WRONG** (the PARTIAL is row 151, a routed
qualifier — it re-scores nothing because the frozen predicate is about the edit
set, not cell truth). Of the ten frozen `EXCLUDED` rows, **9 are correctly
excluded and 1 (row 396) is token-fixable in substance**; the round-95 next
tranche therefore carries **2 labels** (396, 436), both re-derived by a
committed-byte verifier (`ROUND95-LABELS-VERIFY ... PASS rc=0`).

No claim verdict change: C1's operative statement (19 repoints applied
byte-exactly; the ten mapped-away rows stay unmapped with a frozen reason each)
holds as written. The one characterisation nuance — row 435's label asks for a
token drop, not a reword (Q8) — does not touch the predicate. The meter
movement it reports is real but is distinct-token churn, not a correctness gain
(Q2 below).

## Claim check (C1's frozen predicate)

Re-derived at `d51220a` with the frozen counter/map/labels:

- **P1 — PASS.** `KNOWLEDGE-METER-RESULT pass rc=0`; M0 `base=1008/1999`,
  M1 `after=1009/2000`, M3 `same_files=True bad_lines=0 old_not_once=0
  dup_rows=0`, M4 `bad=none`, M5 `out_of_range=none`, M9 `rows=19
  unbound=none`, M10 `labelled=29 want=19 mapped=19
  kinds=excluded=10,range=19 unknown=none`, M6
  `sha256=11de45a74337b945b5179645e18e0f710a2f9ec54935450806a0e4bda7a78847`,
  `after_rev=d51220a…` (`meter-c1.txt`).
- **P2 — PASS.** Counter `03947734…61f67`, map `11de45a7…78847`, labels
  `41bc438b…a556b`: worktree bytes and `git show 96b5033:<path>` are equal
  (`landing-paths.txt`).
- **P3 — PASS.** `git diff-tree --no-commit-id --name-status -r d51220a` prints
  exactly `M corpus/knowledge/considerthese-proposals-ledger.md` and
  `M corpus/knowledge/triage-thresholds.md` (2 files, 18 insertions / 18
  deletions: 17 triage lines + 1 ledger line; line 397 carries two tokens)
  (`landing-paths.txt`).
- **P4 — frozen receipt 12/12, this seat re-ran 2.** `c1-controls-r94.txt`
  shows `C1-CONTROLS-RESULT pass controls=12`, including the two discriminating
  fixtures (`m3-union-applied` rc 0 vs the round-93 counter
  `m3-union-applied-before-r93` rc 1 with Traceback; `m5-cell-repair-lane-root`
  rc 1 with `LIMB M5 FAIL out_of_range=…`). I re-derived the candidate
  (`rc=0`, same 12 lines) and the do-nothing control (`rc=1`, M1
  `after=1008/1999`, M3 `bad_lines=18`) (`do-nothing-control.txt`). The other
  10 controls were not re-run by this seat.

## The 19 landed repoints, one row each

Base value → landed value; the citing cell and the anchor bytes are quoted.
The full citing lines and all anchor lines are in `cited-lines-19.txt`.

| # | site | old → new | citing cell (quoted) | anchor bytes (quoted) | verdict |
|---|---|---|---|---|---|
| 1 | `triage-thresholds.md:143` | `SKILL.md:526` → `SKILL.md:251-253` | `\| \`LEASE_MS\` \| \`2 * 3600 * 1000\` = 7,200,000 ms = 2 h \| 45 \| MATCHES: \`mission-control.md:29\`, \`SKILL.md:251-253\` \|` | `SKILL.md:251-253`: "`ops/fleet-dispatch.mjs` is the `/loop` engine: tmux panes under `ufo_sighting:fleet-grid`, 2 h leases in `fleets/leases.json`, slot rotation…" | **CORRECT** — the anchor states the 2 h lease the row values; `LEASE_MS` and the `3600*1000` expression are mirror-only (`fleet-dispatch.mjs:45`), which the label itself records. Old `:526` was the parking-keyword list (`in_scope_assets empty`, `no testing grant`, `auth-walled`). |
| 2 | `triage-thresholds.md:151` | `SKILL.md:526` → `SKILL.md:251-253` | `\| grid/session \| \`SESSION='ufo_sighting'\`, \`GRID='formation'\` \| 27, 65 \| MATCHES: \`SKILL.md:251-253\` \|` | same 251-253 | **PARTIAL** — the anchor carries the tmux target `ufo_sighting:fleet-grid` (the `SESSION` value) but **not** `GRID`/`formation` (`GRID` has 0 occurrences in `SKILL.md`; the only `formation` substring is inside "informational" at `SKILL.md:1081`, not a grid constant). The label's own fix said "keep the tie only for the pane target or drop it"; the token-only landing did neither. |
| 3 | `triage-thresholds.md:153` | `SKILL.md:14-15` → `SKILL.md:264-266` | `\| off-peak window \| \`h = (getUTCHours() − 3 + 24) % 24; offpeak = h >= 12 && h < 22\` (UTC−3) \| 298-299 \| MATCHES: \`mission-control.md:54-55\`, \`SKILL.md:264-266\` \|` | `SKILL.md:264-266`: "Model routing is a time-windowed decree (UTC-3 12:00–22:00 → deepseek-v4-pro, else gpt-6-astra)…" | **CORRECT** — the decree states the row's UTC−3 12:00–22:00 interval; the `getUTCHours` formula is mirror-only (`fleet-dispatch.mjs:298-299`), as labelled. Old `:14-15` was the 2026-09-28 tree-loss date. |
| 4 | `triage-thresholds.md:220` | `SKILL.md:90-91` → `SKILL.md:157-158` | `\| scope signal \| … \`custodian decision <action>: scope_signal must be exactly NO_SCOPE_OBJECTION\` \| 84 \| MATCHES: \`claim-gates.md:32-33\`, \`SKILL.md:157-158\` \|` | `SKILL.md:157-158`: "non-empty custodian chain where every `scope_signal` is exactly `NO_SCOPE_OBJECTION` and `head_sha256` == last decision ==" | **CORRECT** — exact requirement. Old `:90-91` was `coverage.missing`/`coverage.status`. |
| 5 | `triage-thresholds.md:267` | `SKILL.md:94-95` → `SKILL.md:161-162` | `\| reviewer shape \| \`reviewer.role !== 'kx-reviewer'\` … \| 133-141 \| MATCHES: \`claim-gates.md:72-73\`, \`SKILL.md:161-162\` \|` | `SKILL.md:161-162`: "`APPROVED` review by a distinct `kx-reviewer` (role, requested/resolved model, fallback flag)…" | **CORRECT** — role/model/fallback are the three fields the cell's required text names. Old `:94-95` was `normalized_scope_sha256`/`content_hash_basis`. |
| 6 | `triage-thresholds.md:310` | `SKILL.md:498` → `SKILL.md:828` | `\| \`p_success\` \| \`p_in_scope × p_reproducible × p_unique × p_accepted\` … \| MATCHES: \`ev-model.md:14\`, \`SKILL.md:828\` \|` | `SKILL.md:828`: "p_success    = p_in_scope × p_reproducible × p_unique × p_accepted" | **CORRECT** — exact formula. Old `:498` was RETRY_\* requeue text. |
| 7 | `triage-thresholds.md:311` | `SKILL.md:499` → `SKILL.md:829` | `\| \`gross_value\` \| \`p_success × expected_reward\` … \| MATCHES: \`ev-model.md:15\`, \`SKILL.md:829\` \|` | `SKILL.md:829`: "gross_value  = p_success × expected_reward" | **CORRECT**. Old `:499` was the `rmSync`/window sentence. |
| 8 | `triage-thresholds.md:312` | `SKILL.md:500-501` → `SKILL.md:830-831` | `\| \`total_cost\` \| \`effort_hours × opportunity_rate + direct_cost + delay_cost + expected_risk_cost\` … \| MATCHES: \`ev-model.md:16-17\`, \`SKILL.md:830-831\` \|` | `SKILL.md:830-831`: "total_cost   = effort_hours × opportunity_rate + direct_cost + delay_cost / + expected_risk_cost" | **CORRECT**. Old `:500-501` was RETIRE_AUTH/autopsy text. |
| 9 | `triage-thresholds.md:313` | `SKILL.md:502` → `SKILL.md:832` | `\| \`adjusted_ev\` \| \`gross_value − total_cost\` … \| MATCHES: \`ev-model.md:18\`, \`SKILL.md:832\` \|` | `SKILL.md:832`: "adjusted_ev  = gross_value − total_cost" | **CORRECT**. Old `:502` was the `docs/autopsies/<id>.md` sentence. |
| 10 | `triage-thresholds.md:355` | `SKILL.md:522` → `SKILL.md:999` | `\| record \| \`additionalProperties: false\` at top level \| 5 \| MATCHES: \`SKILL.md:999\` \|` | `SKILL.md:999`: "- `~/Projects/bounties/bounty-map/schema.json` — program record schema (draft-07, fail-closed `additionalProperties:false`)" | **CORRECT** — states the fail-closed `additionalProperties:false` on the program-record schema; "at top level" is the row's schema.json:5 detail, not contradicted. Old `:522` was the parking-invisibility sentence. |
| 11 | `triage-thresholds.md:374` | `SKILL.md:111-112` → `SKILL.md:910-913` | `\| \`mission_state\` \| enum, 12 values in order: \`DISCOVERED, … LEARNED\` \| 54 \| MATCHES: \`SKILL.md:910-913\` (decorative in practice) \|` | `SKILL.md:910-913`: "`stateOrder` … is the 12-step pre-terminal ladder DISCOVERED → NORMALIZED → … → SUBMISSION_PREPARED → LEARNED" | **CORRECT** — the same 12 names in the same order. Old `:111-112` was provenance-pin shapes. |
| 12 | `triage-thresholds.md:390` | `SKILL.md:525` → `SKILL.md:321-324` | `\| \`BANNED\` \| \`['cursor', 'opencode']\` \| 9 \| MATCHES: \`ops-invariants.md:18\`, \`SKILL.md:321-324\` \|` | `SKILL.md:321-324`: "`ops/shared.mjs` … owns the constants every ops file imports: `BANNED = ['cursor','opencode']`" | **CORRECT** (spacing differs; the values are identical). Old `:525` was the parking-keyword sentence. |
| 13 | `triage-thresholds.md:394` | `SKILL.md:525` → `SKILL.md:340-346` | `\| \`TELEMETRY_EVENTS\` \| 8 registry kinds: \`lane_parked, …, provenance_drift\` \| 15-24 \| MATCHES: \`ops-invariants.md:22\`, \`SKILL.md:340-346\` \|` | `SKILL.md:340-346`: "**`TELEMETRY_EVENTS` is a decorative whitelist** … declares 8 event names (`lane_parked`, …, `provenance_drift`)" | **CORRECT** — the same 8 names plus the decorative-whitelist finding. |
| 14 | `triage-thresholds.md:397` | `SKILL.md:146` → `SKILL.md:224-226` | `\| \`appendLedger\` \| appends \`{ts, ...entry}\` to \`ledger/<kind>.jsonl\`; … **3500 bytes** … \| 53-58 (cap 55) \| MATCHES: \`ops-invariants.md:25\`, \`SKILL.md:224-226\`, \`SKILL.md:331-335\` \|` | `SKILL.md:224-226`: "`ledger/missions.jsonl` … (writer: `ops/shared.mjs::appendLedger`, 3500-byte line cap for O_APPEND atomicity)" | **CORRECT** for the cap half. Old `:146` was the RETIRED auth-walled table row. |
| 15 | `triage-thresholds.md:397` | `SKILL.md:246` → `SKILL.md:331-335` | same cell | `SKILL.md:331-335`: "`appendLedger` caps a line at **3500 bytes** … replaces an oversize entry with a `truncated:true` stub … appends to `ledger/<kind>.jsonl`" | **CORRECT** for cap+stub+path; the cell's "recording `bytes`" detail is not in `SKILL.md` nor elsewhere in `corpus/knowledge` (the mirror is absent), so it is a residual qualifier, not a repoint target. Old `:246` was the mission-ledger/evidence-dir paragraph. |
| 16 | `triage-thresholds.md:446` | `SKILL.md:115` → `SKILL.md:184-187` | `\| 9.14 \| "~1040 records" … **1024** (796 zero + 228 one) … \| census §2.2 \| \`SKILL.md:184-187\` \|` | `SKILL.md:184-187`: "(round-13 correction: earlier text omitted `is_live(1)`) — exactly 1024 of 1088 records score 0 (796) or 1 (228)" | **CORRECT** — the 1024/796/228 figures and the correction. Old `:115` was a provenance pin. |
| 17 | `triage-thresholds.md:459` | `SKILL.md:146, 245-247` → `SKILL.md:224-226,335-338` | `\| appendLedger 3500 B cap / gitMutationBlocker \| \`SKILL.md:224-226,335-338\` \| MATCHES \|` | 224-226 = appendLedger 3500-byte cap; 335-338 = "`gitMutationBlocker` (fail-closed on rebase/merge/cherry-pick or non-main HEAD) is **absent from the mirror**" | **CORRECT** — each part lands on its statement. Old 146/245-247 were the RETIRED row and the mission-ledger/evidence-dir paragraph. |
| 18 | `triage-thresholds.md:460` | `SKILL.md:113-117` → `SKILL.md:191` | `\| \`attempts() ≥ 2\` as real termination \| \`SKILL.md:191\` \| MATCHES \|` | `SKILL.md:191`: "status-file TERMINAL + telemetry `attempts()≥2`." | **CORRECT** — the same target already landed for rows 58/144. Old `:113-117` was provenance-pin shapes. |
| 19 | `considerthese-proposals-ledger.md:156` | `SKILL.md:1163` → `SKILL.md:1164` (both occurrences) | "…carries registry rows at `SKILL.md:1164` and `corpus/instruments/README.md:1000` … committer clocks only (`SKILL.md:1164`, "date-order (committer clocks only)")…" | `SKILL.md:1164`: the `r46-landing-gate.py` registry row, whose post-report checks include "date-order (committer clocks only), shonen-heading" | **CORRECT** — both occurrences on the line were repointed (registry-row pointer + quote); `:1163` is the `r46-c2-gate.py` row. |

Landing edit set: exactly the 18 lines above (17 triage + 1 ledger), 18
insertions / 18 deletions; no other path changed (P3).

## The meter's `1008/1999 -> 1009/2000` is token churn, not repair

Resolve.py counts *distinct backticked path-like tokens* in
`corpus/knowledge/*.md` and only marks a token non-`GONE`; it never looks at
the anchor's content. At the landing the base and after token sets differ by:

- **15 removed distinct tokens, all `INTERNAL` at base**: `SKILL.md:111-112`,
  `113-117`, `115`, `1163`, `14-15`, `146`, `246`, `498`, `499`, `500-501`,
  `502`, `525`, `526`, `90-91`, `94-95`.
- **16 added distinct tokens, all `INTERNAL` at after**: `SKILL.md:1164`,
  `157-158`, `161-162`, `184-187`, `224-226`, `251-253`, `264-266`, `321-324`,
  `331-335`, `340-346`, `828`, `829`, `830-831`, `832`, `910-913`, `999`.

`1008 − 15 + 16 = 1009` and `1999 − 15 + 16 = 2000` (`token-delta.txt`). Every
old anchor already resolved `INTERNAL` (in range), so the meter could never
have called the old anchors wrong; the +1 is the dedup arithmetic of 19 rows
producing 15/16 distinct token identities (e.g. `SKILL.md:251-253` twice,
`SKILL.md:191` already present). **The +1 must not be cited as a coverage or
correctness gain.** Two consequences for any future counter:

- comma-combined tokens (`SKILL.md:146, 245-247`,
  `SKILL.md:224-226,335-338`, and the still-present
  `SKILL.md:113-114,175-176`) are **not path-like** to `resolve.py` and are
  absent from both token sets, so rows 90 and 459 are invisible to the meter
  (`token-delta.txt`).
- M5 only checks that a written anchor is in range; content truth is the label
  set's job, not the meter's (the round-93 F5 finding still holds).

## The ten frozen `EXCLUDED` rows

The question for each: is the exclusion right, or would a token repoint alone
have left the cell true? (Cell text and proposed anchor quoted in
`excluded-10.txt`.)

| site | key | proposed | exclusion right? | token repoint alone? |
|---|---|---|---|---|
| `triage:88` | `SKILL.md:113-114` | `SKILL.md:182-184` | yes | **false**: the cell's parenthetical "(four terms, no `is_live`)" describes the old anchor; 182-184 is five-termed **with** `is_live(1)` and carries the correction note. Repointing alone makes the cell false. |
| `triage:88` | `SKILL.md:175-176` | `SKILL.md:255-257` | yes | **false**: "(same omission; names the term `curated-EV`)" is false about 255-257, which says `curated` is a boolean on non-empty `ev_inputs`, never an EV magnitude; `curated-EV` has 0 occurrences in `SKILL.md`. |
| `triage:89` | `SKILL.md:175` | `SKILL.md:182-184` | yes | **false**: "that line writes `reward.min`" is false about 184, which writes `reward.min×1000`. |
| `triage:90` | `SKILL.md:113-114,175-176` | `SKILL.md:182-184,255-257` | yes | **false**: "(term omitted)" is false about both new anchors, which carry the round-13 corrections. |
| `triage:356` | `SKILL.md:522` | `SKILL.md:999` | yes | **false**: the cell's required-key list (`id, name, source_kind, official_url, …`) is not at 999; `official_url` has 0 occurrences in `SKILL.md` (the list is `schema.json:6`). |
| `triage:396` | `SKILL.md:245-247` | `SKILL.md:335-338` | **no — token-fixable** | **true**: the cell's first tie, `ops-invariants.md:24`, already carries every marker and both codes; 335-338 states the blocker's fail-closed rule; the landed row 459 cites the same `SKILL.md:335-338` value under the same MATCHES framing. The frozen reason ("the marker/code list is ops-invariants.md, not SKILL.md") does not make the cell false. Reclassified in the round-95 labels below. |
| `triage:433` | `SKILL.md:113-114` | `SKILL.md:182-184` | yes | **false**: the cell's "omit it" is present tense about an anchor that now explicitly carries `is_live(1)` and records the earlier omission. |
| `triage:433` | `SKILL.md:175-176` | `SKILL.md:182-184` | yes | **false**: same sentence; the repoint would also produce a duplicate `SKILL.md:182-184 and SKILL.md:182-184`. |
| `triage:434` | `SKILL.md:175` | `SKILL.md:182-184` | yes | **false**: "`SKILL.md:175` writes `reward.min`" is false about 184 (`reward.min×1000`). |
| `triage:435` | `SKILL.md:10-11` | drop | yes | **no target exists**: "EV ordering" has 0 occurrences in `SKILL.md` and `git log -S 'EV ordering' -- SKILL.md` is empty; dropping `` `SKILL.md:10-11` `` leaves a dangling "-style" suffix, so the cell needs a prose edit, not a token move. |

So the frozen statement "the ten label rows that ask for a prose reword stay
unmapped" holds literally (each label's `fix` does ask for a reword/qualify),
but one exclusion (396) is stronger than truth requires. That is a routed
qualifier, not a predicate failure: M10 matches the frozen `EXCLUDED` set
exactly and P1 passed.

One precision note on that sentence: nine of the ten labels ask for a
reword/qualify in their `fix` text; row 435 asks for a **drop** ("Drop the
`SKILL.md` token"), and the reword is in the frozen `EXCLUDED` reason (the
dangling "-style" suffix), not in the label itself. The operative claim (all
ten stay unmapped, each with a reason) is true; only the "ask for a prose
reword" characterisation is loose for 435. Q8.

## Next tranche (round 95) — labels proved

File: `.ufo/waves/round-94/w1/ReviewC1Labels-receipts/round95-labels.tsv`
(5 columns, same schema as `.ufo/waves/round-94/c1/labels.tsv`). Verifier:
`verify-round95-labels.py`, output `verify-round95-labels.txt`
(`ROUND95-LABELS-VERIFY rev=d51220a… rows=2 failures=0`, `PASS rc=0`).

| line | key | label | why |
|---|---|---|---|
| `corpus/knowledge/triage-thresholds.md:436` | `corpus/knowledge/mission-control.md:21-23` | `corpus/knowledge/mission-control.md:21-27` | The row's "Supersedes" tie stops mid-sentence: 21-23 ends at "Round-13 correction: the "negative-EV dispatches carry an"; the correction's substance (dead `ev_note` branch at 204, `adjusted_ev` can never be a number, 0/1088 records, every `mission_dispatched` logs `adjusted_ev:"unknown"`) is on 23-27. The verifier asserts the new range contains `ev_note`, `adjusted_ev`, `0/1088`, `unknown` and the old range contains none of them. |
| `corpus/knowledge/triage-thresholds.md:396` | `SKILL.md:245-247` | `SKILL.md:335-338` | A pure token repoint of the round-94 excluded row; the cell stays true because `ops-invariants.md:24` (same cell) carries the marker/code list, and 335-338 states the blocker's fail-closed rule. The verifier also checks row 459's landed use of the same value as precedent. |

Scope and method for "every remaining wrong-but-token-fixable citation I can
prove":

- I enumerated all 197 `corpus/knowledge/*.md:N[-M]` citation occurrences and
  all 27 distinct `SKILL.md` tokens at `d51220a` (`citation-scan.txt`).
- Prior tranches are fully applied: the round-89 `tranche5` WRONG/UNCLEAR
  pairs and the round-90/91/92 edit rows have **0 pending** old keys at the
  landing (`citation-scan.txt` §1). The only non-applied rows are the
  deliberate CORRECT/MENTION no-edit verdicts.
- Three scans for provable anchor defects: table-row key-token absent (6 hits,
  all explained: `LEASE_MS` value-level tie, `TERMINAL`/`MODEL`
  case-variant, `p_*` wildcard, `ev_inputs` "subset validator" tie,
  `is_live` vs `freshness.live`); row-identifier absent (20 hits, hand-read:
  17 are exact quotes/paraphrases or prior adjudications, 1 is the new 436
  defect, 1 is `linux-kernel:37`'s F15/F06 attribution slip, 1 is
  `osv-high-quality:70`'s quote-tail anchor); anchors starting mid-sentence
  (19 hits, hand-read: all state their row's key on the cited line or within
  the range); blank/structural anchors (0) (`citation-scan.txt` §§2a-2d).
- The r88 `WRONG`/`UNCLEAR` anchors that are still cited
  (`claim-gates.md:21-23`, `:35-36`, `:4-5`) were re-read at the landing: the
  entry was corrected since r88 and the current bytes state the citing rows'
  content; `:4-5` remains a partial tie (the usage-message half is mirror-only,
  Q6) (`citation-scan.txt` §3).

Prose-only residuals I could **not** turn into token labels (no
`corpus/knowledge` or `SKILL.md` anchor states the missing detail): row 152's
"tail = last `20000` chars" (0 occurrences anywhere in `corpus/knowledge`
except the row itself); row 157's regex literal (`qwen` 0 occurrences in
`mission-control.md`); row 176's usage message (no `usage` in
`claim-gates.md`); row 397's "recording `bytes`" (not in `SKILL.md` or
`corpus/knowledge`; the mirror is absent); row 396's marker list (already in
`ops-invariants.md:24`, so not a defect); `linux-kernel-security-bugs-reporting-process.md:37`'s "F15 holds the
rule" (the cited 91-96 ends by attributing the recording rule to F06; the row
needs a prose correction, not a repoint).

## Routed findings (no claim re-score)

- **Q1 — row 151 PARTIAL.** `SKILL.md:251-253` states `ufo_sighting:fleet-grid`
  but not `GRID='formation'`; the label's own fix said to keep the tie only for
  the pane target or drop it, and the token-only landing did neither. The cell
  still asserts a MATCHES that the anchor only half supports. Route to prose.
- **Q2 — the meter delta is token churn.** `1008/1999 -> 1009/2000` is
  `−15 +16` distinct `INTERNAL` tokens; it does not measure anchor
  correctness. The claim's numbers are exact; the *interpretation* "anchor
  repair moved the meter" would be wrong. Also, comma-combined tokens are
  invisible to `resolve.py` (rows 90, 459).
- **Q3 — exclusion 396 is stronger than needed.** A token repoint alone leaves
  the row true (ops-invariants.md:24 is the cell's first tie; row 459 lands the
  same value). Round 95 reclassifies it; the frozen statement stays literally
  true because the label asks to "qualify the tie".
- **Q4 — claim-package prose off by one.** `claims.json` C1 `do_nothing` says
  "M3 with 19 bad lines", but the frozen control receipt and my re-run both
  print `bad_lines=18` (`do-nothing-control.txt`). M3 counts distinct site
  lines; line 397 carries two map rows. The predicate only requires the
  control's rc, so this is a documentation fix, not a limb failure.
- **Q5 — meter blind spots for future counters.** Content-level verification
  must stay in the label set (M5 is in-range only), and comma-joined values
  need an explicit parse if they are to count.
- **Q6 — partial ties left by design.** Rows 143/153/157/397 and
  `claim-gates.md:4-5` tie a mirror-only detail to a corpus line that states
  the surrounding rule; prior rounds accepted value-level ties (e.g. the
  8-of-11 `SYNC_PATHS` tie on row 150). If the lane wants strict per-cell
  truth, these need prose qualifications, not repoints.
- **Q7 — stale r88 verdicts.** The r88 `WRONG` verdicts on
  `claim-gates.md:21-23` and `:35-36` no longer describe the landed bytes; the
  entry was corrected. No action beyond noting that anchor-verdict lists must
  be re-derived at the landing, as this seat did.
- **Q8 — 435 asks for a drop, not a reword.** The frozen sentence says the ten
  rows "ask for a prose reword"; 435's label says "Drop the `SKILL.md` token".
  The excluded reason (dangling "-style" suffix) is the reword requirement, not
  the label's ask. The operative claim (unmapped + reason each) holds; the
  characterisation is loose for one row. Route as prose precision only.

## Residual risk / gaps

- P4: 10 of 12 controls were not re-run by this seat (frozen receipt cited);
  the candidate and do-nothing limbs were re-derived.
- The internal-citation audit is scan-plus-hand-read (197 occurrences). The
  scans are heuristic: a wrong anchor that shares a generic word with its row
  would not be flagged. I hand-read all 20 zero-overlap candidates, all 19
  mid-sentence candidates, the 6 key-token misses, and every still-cited r88
  non-CORRECT anchor; a residual wrong anchor outside those sets is possible
  but not proved.
- The 19 content verdicts are my reading of anchor-vs-cell text at the pinned
  bytes; row 143/153/355/397 accept value-level ties because the counters and
  prior tranches do.
- C2 is out of this seat; not assessed.
- No resume path exists in this claim package (no `resume_continuity_v1`
  reference in `.ufo/waves/round-94/` or the round-93 artefacts), so that
  reviewer check is not applicable here. The same holds for the
  one-canonical-runtime / same-identity-rerouting / saturation checks: C1 and
  C2 in this package assert no runtime, rerouting or saturation, so the only
  applicable reviewer surfaces are the label set and the frozen predicate
  checked above.
- Worktree files may be modified by sibling seats; every check above reads
  `git show` at the pinned revs, not the worktree.

## Receipts

All under `.ufo/waves/round-94/w1/ReviewC1Labels-receipts/` unless noted.

| command (abridged) | observed |
|---|---|
| `git diff-tree --no-commit-id --name-status -r d51220a` | rc 0, 2 lines: `M corpus/knowledge/considerthese-proposals-ledger.md`, `M corpus/knowledge/triage-thresholds.md` (`landing-paths.txt`) |
| `sha256sum .ufo/waves/round-94/c1/{knowledge-meter.py,repair-map.tsv,labels.tsv}` and `git show 96b5033:<path> \| sha256sum` | rc 0, 6 hashes; all equal to the frozen pins `03947734…`, `11de45a7…`, `41bc438b…` (`landing-paths.txt`) |
| `python3 -B .ufo/waves/round-94/c1/knowledge-meter.py --lane . --base-rev dff5a0a --after-rev d51220a --map …/repair-map.tsv --labels-rev 96b5033 --base-target 1008/1999 --target 1009/2000 --map-sha256 11de45a7… --work $S/work` | rc 0, 12 lines; `LIMB M0…M6, M9, M10 pass`; `KNOWLEDGE-METER-RESULT pass rc=0` (`meter-c1.txt`) |
| same with `--after-rev dff5a0a` (do-nothing) | rc 1; M1 `FAIL after=1008/1999`, M3 `FAIL bad_lines=18` (`do-nothing-control.txt`) |
| python read of `corpus/knowledge` at both revs via `git archive` + `resolve.collect/classify` | base 1999/1008, after 2000/1009; 15 removed + 16 added, all `INTERNAL`; comma-combined tokens in neither set (`token-delta.txt`) |
| python dump of the 19 map rows: citing line + anchor lines at `d51220a` | rc 0, 153 lines (`cited-lines-19.txt`) |
| python dump of the 10 EXCLUDED pairs: base line, reason, proposed anchor | rc 0, 91 lines (`excluded-10.txt`) |
| `python3 -B scan-citations.py` | rc 0; prior-label pending=0; key-token misses=6; zero-overlap=20; mid-sentence=19; blank/structural=0; r88 non-CORRECT still cited=7 (`citation-scan.txt`, 71 lines) |
| `python3 -B verify-round95-labels.py` | rc 0; `CHECK …436 new_has=4/4`; `CHECK …396 new_has=3/3`; `CHECK skill_tokens=27 expected=27 unaccounted=0`; `CHECK excluded_pairs_present=10/10`; `ROUND95-LABELS-VERIFY … rows=2 failures=0`; `PASS` (`verify-round95-labels.txt`) |
| `wc -l round95-labels.tsv`; `awk -F'\t' '{print NR": "NF" fields"}'`; `sha256sum` | 3 lines (header + 2 rows), each 5 fields; TSV sha256 `33acda87…2d415`, verifier sha256 `5903a62c…93c0a` (`file-inventory.txt`) |
| `git log -S 'EV ordering' -- SKILL.md`; `grep -c -F` for `formation`, `GRID`, `curated-EV`, `official_url`, `20000`, `qwen` | `git log -S` empty; SKILL.md counts: `formation` 1 (only "informational" at :1081), `GRID` 0, `curated-EV` 0, `official_url` 0, `EV ordering` 0, `20000` 0, `qwen` 1 (a model id at `SKILL.md:907`, not the limit-family regex); the corpus hits for `curated-EV`/`EV ordering`/`20000` include the audited rows themselves (`token-greps.txt`) |

Frozen control receipt cited (not re-run by this seat):
`.ufo/waves/round-94/controls/c1-controls-r94.txt` — `C1-CONTROLS-RESULT pass
controls=12`.
