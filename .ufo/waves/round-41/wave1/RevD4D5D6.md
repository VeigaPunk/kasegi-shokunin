# RevD4D5D6 — receipt (round 41, wave 1)

Seat: RevD4D5D6 (reviewer, leaf). Item: produce the three routed-record repairs D4/D5/D6 from
`corpus/lessons/round-40-verifier-spotcheck.md` §5 — (1) an appended `Erratum (round 41)` block for
`corpus/lessons/round-40.md`, (2) the SHONEN.md r40 tally fix if the wrong tally propagated there,
(3) the SKILL.md registry-table repair block. Each deliverable is landable bytes only; evidence lives
here. No lane files were edited; no mutating git/jj run; no installs or upgrades; no network fetches.
Disk guard checked green before work (`use%`: /tmp 3%, /var/tmp 35%, /fast/scratch 25%).

## Deliverables

| file | lines | bytes | sha256 |
|---|---|---|---|
| `wave1/RevD4D5D6.lesson-erratum.txt` | 22 | 1,728 | `23967f32afb5b66159952de4ef965e520556109deda209ab37918fb9dd532404` |
| `wave1/RevD4D5D6.shonen-tally-fix.txt` | 0 | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `wave1/RevD4D5D6.skill-table-fix.txt` | 4 | 968 | `37d2b49d31d9235a4a9b9a35ca6105a6507bd63944c4ba1fc808c05b5eff70a6` |

Report trailer path: `.ufo/waves/round-41/wave1/RevD4D5D6.md` (this file).

## Defect ground truth re-derived (commands + observed output)

1. **D4a — duplicated `## Gate`.** `sed -n '29,33p' corpus/lessons/round-40.md` prints:
   `## Gate` (L29), blank, `## Gate` (L31), blank, `Every source below was opened this round …` (L33).
   The second heading introduces the gate-review content; the first is a stray duplicate.
2. **D4b — garbled census line.** `sed -n '27p' corpus/lessons/round-40.md | cat -A` shows the literal
   bytes `tier A +3?mined S016/S017/S019/S020/S021/S023/S025/S060, rejected S061/S062, carried
   S022/S024 flips)` — `?` where a `(` belongs and an unmatched trailing `)`. The wave-2 reading the
   verifier cited is committed in the same file at L243–L245: "tier A +3 (mined S016/S017/S019/S020/
   S021/S023/S025/S060; rejected S061/S062; carried S022/S024 flips)".
3. **D5 — wrong tally.** `sed -n '9p' corpus/lessons/round-40.md`:
   `= 89 total (64-128 band). Attack share: wave 1 17/54 = 31.5%; wave 2 33/35 = 94%; round total 50/89.`
4. **D6 — broken table.** `sed -n '1119,1122p' SKILL.md`: header row `| name | type | … | owner |`,
   separator `|---|---|---|---|---|---|---|---|`, blank L1121, then the `r40-closure.sh` row at L1122.
   The blank line ends the Markdown table, orphaning the row. `wc -l SKILL.md` = 1122 — the row is the
   file's last line and ends `| 1734 lines) |`.

## D5 arithmetic (shown from the committed dispatch JSONs)

- `wave2-dispatch.json` (wave name `kasegi-r40-falsify` — the file my item spec calls
  `kasegi-r40-falsify-dispatch.json`; same object): `registry.members` is a dict of 35 members.
  `collections.Counter` of member roles → `reviewer: 12, critic: 7, mutation-tester: 6, scout: 8,
  connector: 1, sentinel: 1`. Attack roles = 12 + 7 + 6 = **25** → wave 2 = **25/35 = 71.4%**,
  not 33/35 = 94%.
- `wave1-dispatch.json` (`kasegi-r40-build`, 54 members): `executor: 18, scout: 11, reviewer: 12,
  scribe: 6, connector: 1, sentinel: 1, critic: 3, mutation-tester: 2`. Attack = 12 + 3 + 2 = **17**
  → 17/54 = 31.5%, matching L9 as committed (wave-1 figure is correct).
- Round total: 17 + 25 = **42** → **42/89 = 47.2%**, not 50/89.
- Cross-check: the lesson's own role lists — L7–L8 "(reviewer 12, scout 8, critic 7, mutation-tester 6,
  connector 1, sentinel 1)" and the Wave-2 falsification preamble L213 — independently sum to 25
  attack roles in wave 2; L9 is a transcription error.
- Percentages in the deliverable are rounded to one decimal, matching the lesson's own style
  (`31.5%`); 25/35 = 71.428…, 42/89 = 47.191….

## SHONEN.md — tally NOT propagated; zero-byte deliverable

Greps over `SHONEN.md` (219 lines):
- `grep -n "33/35\|50/89\|94%\|25/35\|42/89" SHONEN.md` → no match.
- `grep -cn "seats\|share" SHONEN.md` → 1, and the match is L208 `Correction (round 40)` ("the seats
  populate" — unrelated prose).
- R40 region read (L193–L219): the boxes record instrument verdicts only (`closed=10/10`, `selftest
  cases=10 failures=0`, `entries=26 pass=26`, …); no seat counts or attack shares anywhere.
- So the L9 error did not propagate to `SHONEN.md`; there is nothing to append. `shonen-tally-fix.txt`
  is an empty file (landable-bytes discipline: zero bytes = nothing to land).
- **Observation, outside my item's named targets:** the same wrong round total is committed at
  `LOG.md` L1733 — `… = 89 (64–128 band; attack share 50/89)`. Flagging for the L1; fixing it is not
  one of my three named deliverables, so no repair bytes were produced for LOG.md.

## SKILL.md D6 repair — what the deliverable is

`skill-table-fix.txt` = a leading blank line, then L1119 (header) + L1120 (separator) + L1122 (the
`r40-closure.sh` row) copied **byte-exact** from the committed `SKILL.md`. Byte-identity verified per
line: `sed -n '2p' deliverable | cmp - <(sed -n '1119p' SKILL.md)` → identical; same for
separator/1120 and row/1122 (`cmp` silent). The leading blank line makes the appended block a table
wherever it lands (matches the `## Round-36 Gates & probes registry addition` pattern: heading, blank,
header). Appending it at EOF puts the r40 row inside a header/separator pair, per the verifier's fix
("an appended, correctly formed row block"); the committed orphan at L1122 is left untouched
(append-only repair, no rewrite). Note the row deliberately keeps its committed unescaped `|` inside
backticked spans (e.g. `` `closed=0|1` ``) — verbatim means verbatim; delimiter pipes count = 9,
matching the 8-cell header.

## Landing notes for the L1

- `lesson-erratum.txt`: append verbatim to the end of `corpus/lessons/round-40.md` (file ends with a
  blank line, so no extra leading blank needed; the block's first bytes are `## Erratum (round 41)`).
- `skill-table-fix.txt`: append verbatim at EOF of `SKILL.md` (L1122 ends with `\n`; the deliverable's
  leading blank line supplies separation).
- `shonen-tally-fix.txt`: empty — do not append; nothing to repair in SHONEN.md.

## Tooling / process record

- Tools: standard coreutils + `grep`/`sed`/`cmp`/`python3` (stdlib only); no installs or upgrades were
  needed — nothing recorded per the install ledger rule.
- Scratch: `/fast/scratch/hyaku/kasegi-r41/RevD4D5D6/` (one temp file `L1122.txt`, removed at cleanup
  before yield).
- Scope: writes only under `.ufo/waves/round-41/wave1/` (three deliverables + this receipt) and the
  scratch dir. Read-only elsewhere; no fleet-root writes; no mutating git/jj; no network.
