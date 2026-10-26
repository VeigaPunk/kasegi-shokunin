# ScribeConsiderthese — round-37 considerthese disposition ledger (calibration)

Seat `ScribeConsiderthese` (scribe, calibration). Item: draft `corpus/considerthese-ledger.md` (new
file) covering the 2026-10-24/25/26 considerthese proposals with columns date/file | proposal # |
one-line proposal | status | disposition evidence, plus the round-37 lesson's
`## considerthese dispositions` section. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD
`b362068195d5489aa94b31e6ec8f880c367e0ba0` (claims freeze `224df74d…`; frozen claims read, not edited;
claims-erratum-1 `b3620681` read). Write scope honoured: **no lane file was written except this
receipt**; both drafts lived under `/fast/scratch/hyaku/kasegi-r37/ScribeConsiderthese/` (removed before
yield). No mutating git command, no tool installed, no score move claimed, no `agent://all` message, no
swarm.

Result in one line: an 18-row ledger (5 + 6 + 7 proposals) where every status carries a committed
`path:line`, commit subject or measured command; zero `declined` rows stated as a finding, not omitted;
and a lesson section that records old → new for all seven 2026-10-26 items plus three re-pins of the
round-30 knowledge ledger.

## 1. Inputs read (read-only)

- `considerthese/2026-10-24.md` (5 proposals), `considerthese/2026-10-25.md` (6), `considerthese/2026-10-26.md` (7) — the 18 rows.
- `corpus/QUALITY.md` — Q8 `:57`, Q9 `:64`, R14 `:83`, R15 `:89`, R23 `:227`, R26 `:249`, R27 `:250`, R28 `:263`.
- `corpus/lessons/round-23.md` … `round-36.md` — landing and disposition paragraphs (line cites in the table).
- `corpus/knowledge/considerthese-proposals-ledger.md` — round-30 ledger, base rows `:11-16`, round-31 flip block `:28-33`.
- `corpus/README.md` — F06–F08 `:207-209`, F13 `:264`, F17 `:361`; `PROVINCE.md:77`; `SHONEN.md:164-166`; `SCORECARD.md:309-321` and `:331`.
- `corpus/instruments/r36-closure.sh:93-108` (E9 limbs a–d); `corpus/instruments/score-gap.py` (`THRESHOLD_RE` at `:76`, score-5 line only).
- `corpus/source-snapshots/round-23/manifest.json` present; commit subject `953c278` read via `git log`.

## 2. Facts measured this round (commands and outputs)

```
$ git ls-files | wc -l
7266
$ git ls-files | grep -c '^\.ufo/'
6990                      # 96.2 % of tracked files
$ git ls-files -z | xargs -0 stat -c %s | awk '{s+=$1} END {print s}'
119222967
$ git ls-files -z -- '.ufo/*' | xargs -0 stat -c %s | awk '{s+=$1} END {print s}'
113443672                 # 95.1 % of tracked bytes
$ grep -rn -e readme-corpus-legibility -e 'draft PR #1' -e cursor/readme LOG.md corpus/lessons/ | wc -l
0
$ grep -c 'Threshold for 8' SCORECARD.md
0
$ grep -c raw_sha256 corpus/instruments/capture-source.py
0
$ grep -c render corpus/instruments/capture-source.py
0
```

Line pins in the evidence cells were read with `sed -n` / `grep -n` at the same HEAD (e.g. `QUALITY.md:263`
starts `| R28 |`; `round-36.md:39` is the round-36 dispositions line; `PROVINCE.md:77` starts
`[r36 Frontier amendment, appended 2026-10-26 …] F18`).

## 3. Delivery 1 — `corpus/considerthese-ledger.md` (new file)

Drafted only (write scope is this receipt). 18 data rows, 5 cells each (pipe count checked in scratch),
9184 bytes, sha256 `7c23298319a581720a5a66f63ea0b97ca65f2b9f3dd858bfd019fd86abc43706`.

````markdown
# considerthese proposal disposition ledger

Scope: every proposal in `considerthese/2026-10-24.md` (5), `considerthese/2026-10-25.md` (6) and
`considerthese/2026-10-26.md` (7) — 18 rows. Written in round 37 by `ScribeConsiderthese`; **R31**
(`corpus/QUALITY.md`, round-37 append-only block) names this file as the tracked home of each
disposition. Read-only at HEAD `b362068195d5489aa94b31e6ec8f880c367e0ba0`; every evidence cell cites a
committed `path:line`, a commit subject, or a command this seat ran. Documentation only: no score move,
no instruction to probe, scan, log in to, or submit against any target.

Status vocabulary (R31): `mined → landed` — a committed criterion, lesson sentence or instrument carries
the proposal, and the cell cites it; `mined → landed (partial)` — a named plank landed and a named plank
is still open, both cited; `open` — no landing and no refusal on record (operator-owned asks stay here,
never read as refusals); `declined` — a round refused it with a recorded reason. **No row is
`declined`**: no consulted round record refuses any of the 18 proposals with a reason.

| date/file | proposal # | one-line proposal | status | disposition evidence |
|---|---|---|---|---|
| 2026-10-24 | 1 | Rechecker normalizes and pins (exactly-once or anchor), not substring-only | mined → landed r24 | `corpus/QUALITY.md:57` (Q8, grounded in proposals 1–2) and `:64` (Q9 exactly-once-or-anchor); `corpus/lessons/round-24.md:131-137` records the landing |
| 2026-10-24 | 2 | Snapshot capture stores clean text, not converter markup | mined → landed (partial) | Instance landed r23 as the normalized `S031` capture replacing the tag-carrying `S030` (`corpus/lessons/round-24.md:136-138`); the later record `corpus/lessons/round-25.md:213-218` re-mines the record-field limb (`render` and `raw_sha256`) and defers the code — measured this round: `grep -c raw_sha256 corpus/instruments/capture-source.py` → 0 and `grep -c render corpus/instruments/capture-source.py` → 0 |
| 2026-10-24 | 3 | Close-r23 dossier with exact diffs (F08 quote, S030 de-tag, manifest, README rows) | mined → landed r23 | Commit `953c278` "round-23: mirror-fallback confinement with matrix receipts; admit F06-F08 with pinned-source rechecks"; `corpus/source-snapshots/round-23/manifest.json` present; `corpus/README.md:207-209` F06–F08 `admitted`; `corpus/lessons/round-23.md:71,149-169` (attempt 2, F06–F08 0/3 → 3/3) |
| 2026-10-24 | 4 | Downshift cadence while idle; reflect on events, not a timer | mined → landed r34 (R23), superseded r35 (R27) | `corpus/QUALITY.md:227` (R23) and `:250` (R27); `corpus/lessons/round-34.md:343-358`; `corpus/lessons/round-35.md:387` ("mined round 34 → R23, citation superseded by R27"). The same ask as 2026-10-25 #6; this row replaces `corpus/lessons/round-24.md:138`'s `operator-owned` classification with the later landing |
| 2026-10-24 | 5 | Decide the fate of draft PR #1 and the eight README branches | open (operator-owned) | `grep -rn -e readme-corpus-legibility -e 'draft PR #1' -e cursor/readme LOG.md corpus/lessons/` → 0 matches (measured this round); `considerthese/2026-10-26.md` records both unchanged since 2026-10-17. Needs João; no lane round may merge or prune them |
| 2026-10-25 | 1 | Cap or externalise wave-evidence bloat; measure per-round repo growth | mined → landed r28 (R14), measured r33 | `corpus/QUALITY.md:83` (R14); `corpus/lessons/round-28.md:219-225`; `corpus/lessons/round-33.md:100-101` re-measured `.ufo/waves/round-33` at 1,366,042 B / 27.3 % of the round's budget |
| 2026-10-25 | 2 | Track distance to the next score, not only "improved, held" | mined → landed r31 (instrument) and r35 (R26) | `corpus/instruments/score-gap.py` (read-only reporter, asserts no score move); `corpus/lessons/round-31.md:127-131`; `corpus/QUALITY.md:249` (R26); `corpus/lessons/round-35.md:352-360` re-ran it (`gap: 24 of 47 …`) |
| 2026-10-25 | 3 | Point a round at bounty craft and SHONEN box 2 (severity tables plus an end-to-end task) | mined → landed (partial) | Severity plank landed: `corpus/README.md:264` (F13, r29) and `:361` (F17, r34). End-to-end task plank open: `SHONEN.md:164-166` box 2 `[~]` at round 36 |
| 2026-10-25 | 4 | Give the bot's own proposals a status ledger | mined → landed r30, re-pinned r37 | `corpus/knowledge/considerthese-proposals-ledger.md:11-16` (round-30 ledger, 2026-10-25 rows only); `corpus/lessons/round-30.md:80-85`; this file plus R31 re-pin it for all three dates (§ Re-pin) |
| 2026-10-25 | 5 | Keep an open-defects ledger with runnable closure checks | mined → landed r29 (R15), applied r36–r37 | `corpus/QUALITY.md:89` (R15); `corpus/lessons/round-29.md:217-221`; `corpus/lessons/round-35.md:384-386` (D1–D7 inside `r35-defect-closure.sh`, `closed=7/7`); `corpus/instruments/r36-closure.sh` carries the E1–E9 checks |
| 2026-10-25 | 6 | Event-driven reflections | mined → landed r34 (R23), superseded r35 (R27) | `corpus/QUALITY.md:227` (R23) and `:250` (R27); `corpus/lessons/round-34.md:343-358` records the landing and its narrowing; `corpus/lessons/round-35.md:387` |
| 2026-10-26 | 1 | Make distance-to-next-score thresholds explicit in `SCORECARD.md` §Saturation | open | `corpus/lessons/round-36.md:39` — gap computed (`gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`); `SCORECARD.md:309-321` declares the saturation line only; `corpus/instruments/score-gap.py` reads one threshold (`SCORECARD.md:331`, score 5) and `grep -c 'Threshold for 8' SCORECARD.md` → 0 (coverage-8 undefined) |
| 2026-10-26 | 2 | Run one end-to-end domain task round (SHONEN box 2) | open | `SHONEN.md:164-166` — box 2 `[~]`, "no new end-to-end domain hunt ran" (round-36 state); no round lesson records such a task |
| 2026-10-26 | 3 | Add a quiescence gate before `complete` | mined → landed r36 (R28 + E9) | `corpus/QUALITY.md:263` (R28); `corpus/instruments/r36-closure.sh:93-108` (E9 limbs a–d); `corpus/lessons/round-36.md:7` (E1–E9 suite) |
| 2026-10-26 | 4 | Cap or externalise wave evidence (keep digests, move raw transcripts out) | open | `corpus/QUALITY.md:83` (R14 criterion only). Measured this round at HEAD: `git ls-files` → 7266 tracked files, `.ufo/` 6990 (**96.2 %**); bytes 119,222,967 total vs 113,443,672 `.ufo` (**95.1 %**); no release/LFS artefact committed. The externalisation decision is operator-owned |
| 2026-10-26 | 5 | Land the owed F18 `PROVINCE.md` amendment | mined → landed r36 | `PROVINCE.md:77` — "F18 — CISA Known Exploited Vulnerabilities catalog … admitted round 35", appended 2026-10-26 |
| 2026-10-26 | 6 | Re-tune the reflection's own cadence and depth | open (recorded, no change) | `corpus/lessons/round-36.md:39` item 6 — "recorded, no change"; no second daily run, per-round digest section, or weekly cloud pass is committed |
| 2026-10-26 | 7 | Keep a proposal-status ledger (proposed → adopted → declined) | mined → landed r37 (R31 + this file) | R31 in the `corpus/QUALITY.md` round-37 append-only block; this file; the round-37 lesson's § considerthese dispositions records old → new |

## Re-pin of the round-30 knowledge ledger

`corpus/knowledge/considerthese-proposals-ledger.md` (mined r30, `corpus/lessons/round-30.md:80-85`)
covers the 2026-10-25 six proposals only. It is left byte-unchanged here (append-only bar; its
`recheck:` line still audits). Two of its rows are behind later rounds, and this file is the current
tracked home R31 names:

| knowledge-ledger row | recorded there | current status (this file) | why |
|---|---|---|---|
| `:12` (base table) and `:28` (round-31 flip) proposal 2 | `open`, flipped to `mined round 31` in its appended block | mined → landed r31 (instrument) and r35 (R26) | `score-gap.py` and R26 (`corpus/QUALITY.md:249`) postdate the base table; its own r31 append already carries the instrument flip |
| `:16` (base table) and `:33` (round-31 flip) proposal 6 | `open`, restated `unchanged` at r31 | mined → landed r34 (R23), citation superseded r35 (R27) | R23 lands at `corpus/QUALITY.md:227` and R27 at `:250`; the r31 append predates both |
| `:11`, `:13`, `:14`, `:15` proposals 1, 3, 4, 5 | mined r28 / partially landed r29 / mined r30 / mined r29 | unchanged, except proposal 4's home | Same landings are cited above; proposal 4's tracked home moves from the knowledge entry to this file |

A later round that wants the knowledge entry itself to read current appends a flip block there
(R9/R6: never an in-place rewrite). This ledger does not edit it.

## Limits

- Statuses are documentary: `mined → landed` means a committed lane record names the landing, not that
  the landing's completeness was re-measured here. Every partial row carries its open plank in the same
  cell.
- Line numbers were measured at HEAD `b362068…` while the round-37 wave was running; untracked
  `.ufo/waves/round-37/` artifacts were not consulted for any status.
- This file is append-only after landing: a later flip lands as a new `## … flips` section, never as an
  edit to an existing row.
- No score move is claimed; no axis is affected by this ledger.
````

## 4. Delivery 2 — round-37 lesson section `## considerthese dispositions`

Merge target: `corpus/lessons/round-37.md` (owned by `ScribeGateLesson`; the file was absent at draft
time). 2583 bytes, sha256 `5e7f0f6a8534081782ec2e239134a72dec952889c132035802b3289056efe09b`.

````markdown
## considerthese dispositions

`corpus/considerthese-ledger.md` lands this round under **R31** (`corpus/QUALITY.md`, round-37
append-only block): every proposal in the 2026-10-24 (5), 2026-10-25 (6) and 2026-10-26 (7)
reflections now carries one status and one evidence pointer. Old → new against the last recorded
disposition:

1. **2026-10-26 #1 distance-to-next-score thresholds** — `open` → `open`: the gap is computed
   (`corpus/lessons/round-36.md:39`, `gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0
   gated unsupported claims`), but the thresholds plank is unlanded — `SCORECARD.md:309-321` declares the
   saturation line only, `score-gap.py` reads one threshold (`SCORECARD.md:331`), and
   `grep -c 'Threshold for 8' SCORECARD.md` → 0.
2. **2026-10-26 #2 end-to-end domain task** — `open` → `open`: `SHONEN.md:164-166` keeps box 2 `[~]`.
3. **2026-10-26 #3 quiescence gate** — `open` → `mined → landed r36`: R28 (`corpus/QUALITY.md:263`) plus
   E9's four limbs (`corpus/instruments/r36-closure.sh:93-108`).
4. **2026-10-26 #4 cap/externalise wave evidence** — `open` → `open`: R14's criterion exists
   (`corpus/QUALITY.md:83`) but the practice does not — measured this round, 6990 of 7266 tracked files
   (96.2 %) and 113,443,672 of 119,222,967 bytes (95.1 %) are under `.ufo/`, with no release/LFS artefact.
5. **2026-10-26 #5 F18 PROVINCE amendment** — `open` → `mined → landed r36`: `PROVINCE.md:77`.
6. **2026-10-26 #6 cadence/depth** — `open` → `open` (recorded, no change; `corpus/lessons/round-36.md:39`).
7. **2026-10-26 #7 proposal-status ledger** — `open` → `mined → landed r37`: R31 plus
   `corpus/considerthese-ledger.md`.

Three re-pins on the earlier sets, where the round-30 knowledge ledger
(`corpus/knowledge/considerthese-proposals-ledger.md:11-16`, last flip block `:28-33`) predates later
rounds: 2026-10-25 #2 `open` → `mined → landed r31 + r35` (R26, `corpus/QUALITY.md:249`); 2026-10-25 #6
`open`/`unchanged` → `mined → landed r34`, citation superseded r35 (R23 `corpus/QUALITY.md:227`, R27
`:250`); and 2026-10-24 #4, the same cadence ask, recorded as landed rather than the `operator-owned`
classification at `corpus/lessons/round-24.md:138`. The 2026-10-24 #1–#3 and 2026-10-25 #1, #3, #4, #5
rows keep the landings already cited in those lessons. No row is `declined`: no round record refuses any
proposal with a reason, and 2026-10-24 #5 (draft PR #1 / README branches) stays `open` as operator-owned
(`grep -rn 'draft PR #1' LOG.md corpus/lessons/` → 0 matches).
````

## 5. Calibration notes — conflicts recorded, not smoothed

1. **10-24 #2 is partial, not unqualified-landed.** `round-24.md:136-138` records proposals 2–3 as
   "already landed in round 23"; `round-25.md:213-218` re-mines the same proposal because the record-field
   limb (`render` / `raw_sha256`) is absent — measured again this round, `capture-source.py` contains
   neither string. The row therefore reads `mined → landed (partial)` and names both the landed instance
   (normalized `S031` capture) and the open limb.
2. **10-24 #4 reverses r24's `operator-owned` call.** `round-24.md:138` classified proposals 4–5 as
   operational/operator-owned; `round-34.md:343-358` landed 2026-10-25 #6 — the same cadence ask — as R23
   (`QUALITY.md:227`). The ledger records the later landing and the superseded classification in the same
   cell instead of rewriting the r24 sentence (R9).
3. **The round-30 knowledge ledger is stale on two rows.** Its base table says proposal 2 `open` (`:12`) and
   proposal 6 `open` (`:16`), and its round-31 flip block restates 6 as `unchanged` (`:33`) — but r31 landed
   `score-gap.py` and r34 landed R23. The new ledger carries a `## Re-pin of the round-30 knowledge ledger`
   section with old → new and leaves the knowledge entry byte-unchanged (append-only bar; its `recheck:`
   line still audits).
4. **No `declined` rows, and that is stated as a finding.** No consulted round record refuses any of the 18
   proposals with a reason; the operator-owned asks (10-24 #5, 10-26 #4) are `open`, not `declined`.
5. **10-26 #1 stays `open` even though the gap is computed.** `round-36.md:39` proves the measurement;
   `SCORECARD.md:331` defines only the score-5 threshold and `grep -c 'Threshold for 8' SCORECARD.md` → 0,
   which is the plank the proposal asks the lane to land.
6. **R31 is cited by id, not line.** R31 lands in the round-37 append-only `corpus/QUALITY.md` block drafted
   by `ScribeQualityRows`; no line number exists at draft time, so both blocks cite the row id and the
   block.
7. **10-26 #4's measurement is current, not copied.** The reflection's 96 % / ~109 MB figure was
   re-measured at HEAD: 96.2 % of tracked files and 95.1 % of tracked bytes under `.ufo/` (numbers above),
   so the `open` status rests on this round's bytes.

## 6. Limits / out of scope

- Both blocks are drafts for the integration owner; this seat wrote no lane file, so nothing here is
  claimed as landed.
- Line pins are true at HEAD `b362068…`. `QUALITY.md` is append-only after its current tail, so a sibling
  R30/R31 append does not renumber the cited rows (`:57`, `:64`, `:83`, `:89`, `:227`, `:249`, `:250`, `:263`).
- Untracked `.ufo/waves/round-37/` artifacts were not used as status evidence.
- No claim about C1 or C2, no axis attribution and no score move; calibration is the only axis this seat
  touched.
- The 2026-10-19 … 2026-10-23 reflections are outside the item's scope and are not covered by the ledger.
