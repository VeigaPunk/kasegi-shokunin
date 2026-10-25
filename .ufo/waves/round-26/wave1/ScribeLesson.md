# ScribeLesson — round-26 lesson (wave 1, build)

Seat: `L1Kasegi26.ScribeLesson` (scribe, leaf). Date: 2026-10-25 (UTC). Lane root:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base/claims-freeze commit
`1b076fa7f2fb5e7dd9d87449514eba526043421b`.

## Deliverable

- `corpus/lessons/round-26.md` — written, **148 lines** (~25.8 KB). Required blocks present:
  `## Overview — claims and counters`, `## Gate — the assimilation set`,
  `## Mistakes`, `## Fixes that can fail`, `## Appendix — counters, confirmation and access-date evidence`
  (+ `## Routed debt`). No Q/R bar relaxed.

## Fix-control #3 (restated) — recorded output

Command (exact, run from lane root twice):

```
grep -rnE '62 assertions\|77 assertions' corpus/instruments/README.md SCORECARD.md corpus/lessons/round-24.md | grep -v 'round-24.md:77' | wc -l
```

Output: **0** (exit 0). Context: the same command without the `grep -v` exclusion returns 1
(`corpus/lessons/round-24.md:77`, the retained historical sentence). Under GNU ERE the frozen
pattern's `\|` is a literal pipe, so the bare pattern alone matches nothing; content ground truth
(proper ERE alternation) shows the only 62/77 hit in the three files is the retained line — both
facts are recorded in the lesson (M26-6).

## Key facts recorded (all observed, none fabricated)

- claims.json frozen at `1b076fa7` before any measurement; bytes match freeze commit
  (sha `343e568e…`). R25-1 complied.
- C1: SKILL.md gate|probe row landed (counter 1); receipt index has a selftest line (counter 1)
  but pins the pre-change digest `c3c19adc…`/cases=14 — the landed instrument is
  `3fc0d751…`/cases=15, so the index must be regenerated at the landed digest before commit
  (open item, recorded). Fix-control 3 = 0. Deletion soundness verified on the landed bytes:
  deleting `multiparty-vulnerability-coordination.md` in a scratch tree → exit 1,
  `missing_entries=['corpus/knowledge/multiparty-vulnerability-coordination.md']`.
- C2: F11 admitted (awk 11); S041 row appended; both knowledge entries landed
  (`iso-29147-and-30111-division-of-labour.md` 54 lines, `iso-29147-divergence-and-clause-crosswalk.md` 67 lines);
  `grep -lE '^source: S04[0-9] '` = 3 (includes round-25 S040 overmatch — recorded).
- Kill-rule status: C1 (a)/(c)/(d) satisfied; (b) pending receipt regeneration. C2: census
  currently exits 1 (E09 S040/S041 recheck-cell prose) — the round-end kill-rule limb is not yet
  satisfied; smallest safe correction recorded (cadence-only cells + `## Registry changes` note).
  E11 (S041 used-by) cleared once both entries landed.
- Quarantine verdicts (s4): S037/S054 fetched no-quote; S048/S069/S070 unfetchable; S065 fetched
  quote-located; S068 already-mined-legacy (S040).
- Rejects with flip conditions: `vendor-cvd-policy-crosswalk-2026-10-23.md` (F20 absent, Q7 prose
  recheck, Q3 four-vs-two conditions — round-25 verifier's reasons carried, re-confirmed by s3)
  and `chinese-criminal-thresholds-and-authorisation.md` (round-24 refusal reason + flip retained).
- Open integration items recorded: F11 README row cites staged suffixed filenames ≠ actual entry
  names → `frontier-recheck-count.py` FileNotFoundError (exit 1) until the row is corrected.

## Verification methods

- Direct runs from lane root (this seat): all frozen counters (a)-(d), C2 awk/grep, census
  validate, `frontier-recheck-count.py`, `py_compile`/`--selftest` on the instrument, deletion
  mutant + rename mutant on scratch copies (/tmp), sha256 checks of claims.json vs freeze commit,
  fix-control #3 with and without exclusion.
- Read of every landed wave-1 receipt relevant to the lesson (ExecCaptureS041, ScoutS040Probe,
  ScoutQuarantine, ScoutQuoteRelocation, ScoutDatawalk, ScoutPackageInventory, ExecReceiptIndex,
  ExecSkillRegistry, ExecExpectedList, ExecAuditFix, ExecManifestRecheck, ExecMirrorCensus,
  ExecFrontierSim, MutDeletionControls, MutRegistryRow, MutGameability, ConnOverlap,
  ConnR25Continuity, ConnOwnership, ScribeReadme, ScribeSourcesAppend, ScribeScorecard,
  ScribeLogProvince, SentScopeSweep, RevDigestLineage, CritVacuityC2, CritNoHarm, n1-sweep).

## Tools

None installed/updated (python3, curl, pdftotext, GNU grep pre-existing; no pacman transaction).

## Files written (owned)

- `corpus/lessons/round-26.md` (new, 148 lines)
- `.ufo/waves/round-26/wave1/ScribeLesson.md` (this report)
