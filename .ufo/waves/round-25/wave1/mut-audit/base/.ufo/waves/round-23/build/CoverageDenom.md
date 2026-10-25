# CoverageDenom — C2 audit (read-only seat)

Scope: `claims.json` C2 only — "frozen eight public-practice frontier surfaces and
lost-root score denominator remain separate." Evidence: `claims.json`,
`SCORECARD.md` r22/r23 sections, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/QUALITY.md` (uncommitted Q7–R9), three untracked candidate entries,
`corpus/source-snapshots/round-23/*.txt` + `opened-source-snapshots.json`.
Read-only; nothing edited.

## Finding 1 — the frozen counting command admits a status-flip without the claim's own conditions

`claims.json` C2.count defines success as "Count admitted F06–F08 rows in
corpus/README.md" (scorecard's r22 command: `grep -cE '^\| F0[6-8] .*\|
admitted \|'`). The claim text separately requires opened official text, exact
located quotes, and executable local rechecks. Falsifier (real, in tree now):
the three untracked entries' `recheck:` lines invoke
`python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-23/manifest.json` — **neither
`corpus/instruments/source-recheck.py` nor `manifest.json` exists** in the
tree (`ls corpus/instruments/` shows only density/resolve/anchorcheck/README/
test_resolve/citation-survival). As committed, every recheck exits
ENOENT — a Q7 violation on all three entries — while the grep count still
reports 3/3 the moment the README rows flip to `admitted`. The count command
is therefore weaker than the claim and can certify non-admissible rows.
Smallest correction: extend the frozen count to a conjunct — for each admitted
row, its `entry` file exists, its `source:` S-id resolves to a `mined`
SOURCES row whose `used-by` names the entry, and its `recheck:` command
executes with exit 0 plus a failing missing/corrupted-source control (Q7).

## Finding 2 — F08 verbatim quote is not verbatim (Q3)

`corpus/knowledge/cra-manufacturer-reporting-duties.md` quotes, under
"Exact located quotes | Article 71": `"It shall apply from 11 December 2027."`
Snapshot `S029.txt:122` reads `2.This Regulation shall apply from 11
December 2027.` — the quoted token is "This Regulation", not "It". Every
other located quote in all three entries matches the captured bytes
whitespace-normalized (S018 6/6, S030 6/7 modulo `<u>` markup at line 165,
S029 5/6). Falsifier: a recheck that string-matches quotes against the
captured excerpt fails this row. Smallest correction: change the quote to
"This Regulation shall apply from 11 December 2027." — one-word fix, no
structural change.

## Finding 3 — in-tree F06→S-id provenance inconsistency

`corpus/SOURCES.md` (uncommitted r23 edit) flips S018 `queued → mined`,
`used-by → corpus/knowledge/multiparty-vulnerability-coordination.md`, but
leaves `opened 2026-10-19` — while the entry says `verified-at: 2026-10-20`
and `opened-source-snapshots.json` records `"opened": "2026-10-20"` with
sha256 `d366bf40…`. Two opened dates for one source row is exactly the
false-provenance class R8 was minted for (immutable fields; a corrected field
is a new row or a recorded old→new change). Same defect shape applies to
the README F06–F08 `sources` cells: F07 still names S022 (v4.1.0) and F08
names S024 (Article 14 never reached) while the entries actually cite S030
(v4.2.0, opened today) and S029. A verifier checking "their entries, source
rows" (C2.count's own words) sees a queued/non-current row behind every
admitted frontier row. Smallest correction: README `sources` cells carry
`S018`, `S030 (supersedes S022)`, `S029 (supersedes S024)`; S018's
`opened` is corrected to 2026-10-20 with the change recorded in the
round-23 lesson per R8, or a `S031 supersedes S018` row is minted.

## Finding 4 — eight-topic frontier denominator silently supersedes the r22-proposed denominator

R22 recorded, for explicit adoption this round, a coverage denominator of
"20 corpus-attested Core items + 5 Frontier topics → (20+5)/25"
(`SCORECARD.md:328`, and the r22 next-plan: "Adopt the r22 coverage
denominator (20 Core + Frontier admitted / total) by explicit claim").
The frozen C2 instead freezes the denominator at the eight declared F-ids
only, keeping score 7 held. That is defensible (r22 critic: don't redefine
a denominator in the round that benefits), but it silently drops the
planned adoption rather than recording deferral — and "8/8" reads as
frontier saturation while SOURCES.md still holds 7 further `queued` public
rows (S016, S017, S019, S020, S021, S023, S025) with no F-id. Premature-
saturation risk: the next reader sees a complete frontier. Smallest
correction: C2 wording "the eight Frontier topics declared at base
(F01–F08); the registry's remaining queued sources are unmined, not
out-of-scope" plus an explicit defer-or-adopt line on the r22 denominator.

## Finding 5 — denominator separation is asserted but uncounted

The claim says the eight-surface frontier and the lost-root denominator
"remain separate," but the only frozen check is the frontier grep; nothing
verifies the lost-root side stayed historical (README "0/18 surfaces are
present", coverage cell still `7`, score7 held). An integration edit that
folded frontier admissions into the lost-root score would pass the frozen
count. Smallest correction: add a no-harm conjunct —
`grep -c '0/18 surfaces are present' corpus/README.md` = 1 and the coverage
score cell remains `7` — to the C2 count.

## Non-findings checked and cleared

- F07 "current CNA rules": entries correctly cite 4.2.0 via new S030
  (approved 2026-08-20, effective 2026-08-25), not the stale S022 pin —
  the version-substitution falsifier does not fire.
- CRA Article 14/71 and CNA quotes: 11/12 located strings verified
  byte-for-byte against captured snapshots (normalized whitespace).
- Lost-root cells: `corpus/README.md` line 204 "0/18 surfaces are present"
  and the r15 coverage definition are untouched in the working diff —
  separation holds on current bytes.

## Scope limits

Entries are wave artifacts in flight; `corpus/README.md` is still unmodified
(F06–F08 `queued`), so Findings 1–3 are pre-integration defects, fixable
inside this wave. No network re-open performed; "current CNA rules" rests on
the S030 row's self-report plus snapshot header. No claim of admission or
rejection is made here — these are falsifiers for the canonical judge.
