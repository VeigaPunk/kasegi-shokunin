# ScribeReadmeC2 — round-28 wave 1 report

Scope: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/README.md` only.
Runtime: lane HEAD `94f387c` (round-28 wave1 spec + dispatch); claims-freeze base `c9f8b11`
verified an ancestor (`git merge-base --is-ancestor … ; echo $?` → 0). Today 2026-10-25 (UTC).
Revised after the knowledge entry landed (Rev 2); superseded Rev 1 values are logged in the receipt
(`.ufo/waves/round-28/receipts/ScribeReadmeC2.txt` §Rev 2).

## Behavior delivered

1. **Frontier row F12** appended as the last row of the Frontier table (line 213), mirroring the
   F01–F11 column shape exactly (`| id | topic | status | entry | sources | next |`, bare entry
   path, comma-separated source ids):

   > `| F12 | Japanese state-coordinated disclosure workflow | admitted | knowledge/japanese-domestic-disclosure-workflow.md | S041, S042 | Use 起算日 — the day the guideline's Ⅳ.4.2) notification was first attempted (S041 footnote 4), not an acknowledgement or a submission date — as the Japanese column when comparing coordinator timelines against F02. The same 45-day figure is triggered differently on each side: S041's publication date is a 目安 of 45 days from 起算日 (Ⅳ.3)), CERT/CC's 45 days runs from the initial report (S004, F02). |`

   The next-step cell names the 起算日 column for future coordinator-timeline comparisons, binds it
   to F02 (the coordinated-disclosure-timelines row), and carries the same-number/different-trigger
   trap (45 days from 起算日 vs 45 days from the initial report).

2. **Admitted-count amendment** (R9): the historical sentence at lines 215–218 ("…11/11 admitted at
   round 26; F01-F08 at round 23, F09 at round 24, F10 at round 25, F11 at round 26…") is retained
   verbatim; a new paragraph at line 220 records **12/12 admitted — F12 at round 28** and states the
   parenthetical is history. The two `0/18` lost-domain sentences are diff context lines — neither
   added nor removed.

3. **Coverage map / expected-list reconciliation note** appended at end of file as
   `## Round-28 reconciliation — coverage map and expected list (appended 2026-10-25)` (lines
   226–245). It names the new entry, its source basis (S041 + S042, `corpus/source-snapshots/
   round-28/`, captured 2026-10-25), gives the count basis, cites
   `.ufo/waves/round-28/receipts/ExecExpectedList.txt` as confirmation, and records the measured
   audit state after landing.

## Gates

| gate | measurement | result |
|---|---|---|
| R6 line stability | `git diff -U0` hunks `@@ -212,0 +213 @@` and `@@ -217,0 +219,27 @@`; lines 1–212 byte-identical to HEAD | PASS |
| R6 cited lines | `corpus/README.md:49`, `:51`, `:82` — per-line sha256 vs `git show HEAD:corpus/README.md` | same bytes, same numbers (49 and 82 are the two README line cites in `instruments/citation-survival.md:144-145`) |
| additive only | `git diff --numstat` → `28 0 corpus/README.md` | 28 insertions, 0 deletions |
| C2 counter 1 (frontier admitted) | `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` — before 11 (HEAD bytes), after **12** | REACHED |
| C2 counter 4 (frontier harness) | `python3 corpus/instruments/frontier-recheck-count.py` → `PASS F12 … ids=S041,S042 exit=0`; `entries=15 pass=15 exit=0`, exit 0 | REACHED (measured post-landing) |
| F12 row shape | row parsed by the harness regex and by the frozen awk counter | accepted |
| non-collision of topic | independent assessment by `ScribeFrontierNote` (nearest F02, Jaccard .333) | no F-row collision |

## Findings

- **Frontier harness now passes for real.** Pre-landing it printed 14 PASS lines then
  `FileNotFoundError: … corpus/knowledge/japanese-domestic-disclosure-workflow.md`, exit 1 — the row
  shape had already been accepted. After ScribeEntryC2 landed the entry (header `source: S041` +
  `source: S042`, recheck selecting both against `corpus/source-snapshots/round-28/manifest.json`)
  the harness reports `entries=15 pass=15 exit=0`.
- **Expected-list reconciliation (r27 carry-forward 4) is closed as a units question.** `wc -l` → 41;
  `grep -c '^#'` → 2; `grep -vc '^#'` → 39 — 41 lines = 39 entries + 2 comments, independently
  confirmed in `ExecExpectedList.txt` §2.
- **Routed debt, not a README defect:** the expected list was not regenerated, so
  `python3 corpus/instruments/recheck-audit.py --quiet` now prints
  `lines=40 total=40 pass=40 … exit=1` and `expect=present expected=39 missing=0 unexpected=1 exit=1`.
  Regenerating `corpus/instruments/knowledge-expected.txt` to 40 entries / 42 lines clears it. That
  file is outside this seat's ownership; the README note records the same state.
- **起算日 / 45-day wording is grounded on this round's captures** (`S041.txt:340`, `:648`/`:786`,
  `S042.txt:145`) and on F02's own quote (`coordinated-disclosure-timelines.md:22`, S004) — not on
  the staged package copy.
- No credential material, session, private URL or plugin markup was written.

## Touched surfaces

- `corpus/README.md` (owned production file; sha256 before `511e15b2…`, after `5f458a7a…`; 217 → 245 lines).
- `.ufo/waves/round-28/receipts/ScribeReadmeC2.txt` (receipt).
- `.ufo/waves/round-28/wave1/ScribeReadmeC2.md` (this report).

## Out of scope — untouched

`corpus/SOURCES.md` (ScribeRegistryC2), `corpus/knowledge/japanese-domestic-disclosure-workflow.md`
(ScribeEntryC2), `corpus/QUALITY.md` (ScribeR14), `corpus/instruments/*` including
`knowledge-expected.txt`, `SKILL.md` (ScribeSkillGate), `corpus/lessons/*`, `LOG.md`,
`SCORECARD.md`, `claims.json`. No VCS write; no subagent dispatch; no tooling installed or upgraded.

## Known limits

The entry's own claim/quote audit is ScribeEntryC2's and the reviewers' deliverable, not this seat's;
the README F12 sources cell asserts S041 + S042 per the frozen claim. `recheck-audit.py` exits 1 for
the expected-list reason above — a measured state of another seat's file, not of this edit.
