# CritClaimsContradiction — seat receipt (round 40, wave 1)

Seat: `CritClaimsContradiction` — leaf critic. Lane: `kasegi-shokunin`.
Scanned state: lane HEAD `5e985b74075dd3813a63d7750966bf8abf693465` (claims-freeze commit); working tree
clean except untracked `.ufo/waves/round-40/*` (round-in-progress artifacts, untouched by this seat).

## Scope (as specified)
Scan committed records SCORECARD.md / LOG.md / SHONEN.md / corpus/lessons/round-39.md for:
(a) state still claiming r39 C1 8/8 at Y without the appended correction (R2 class);
(b) future-dated `run-utc`;
(c) `⟨pending` markers;
(d) score/count mismatches vs the round-40 freeze controls (c1/c2-controls/before.txt, census-before.txt).
Deliver list of exact lines/records needing `Correction (round 40)` treatment or a fix. No lane edits made.

## Deliverable
`wave1/CritClaimsContradiction.txt` — 16 lines, 1371 bytes, sha256 `34f54922b2561dc796242bf47e6603263719738ed0080418773c83f7971ecf5b`.

## Finding (a) — R2 class: r39 C1 8/8-at-Y overstatement (5 records)
Final r39 receipt (`.ufo/waves/round-39/final-gates/all-gates.txt` v5 at HEAD) records `closed=7/8 exit=1`
(G2 red, line 17) and `selftest cases=8 failures=1` (line 79) — the values the corrections must name.

| record | stale claim | correction state |
|---|---|---|
| SCORECARD.md:1567 | "`closed=8/8 exit=0` at Y, graded `selftest cases=8 failures=0`" | `Correction (round 39)` @1580 calls 8/8 "not independent proof" but does NOT name final 7/8 / failures=1 (final values only in claims table @1583) |
| LOG.md:1709 | "`closed=8/8 exit=0` at Y, graded `selftest cases=8 failures=0`" | `Correction (round 39)` @1719 ALREADY names final values (7/8, failures=1) |
| SHONEN.md:194 (box 1) | "suite `--selftest` graded cases=8 failures=0 at the verification ref" | Correction @203 does not name final values |
| SHONEN.md:198 (box 3) | "r39 suite run + graded selftest at the verification ref Y (all-gates.txt)" | same gap |
| corpus/lessons/round-39.md:15 | "`closed=8/8 exit=0` at Y; graded `selftest cases=8 failures=0`" | NO correction block in file (0 `Correction (round 39)` lines); final values only in narrative :86/:91-92 |

All four files currently have 0 `^Correction (round 40)` lines (freeze control "R2 overstatement corrections
absent … SCORECARD.md:0 LOG.md:0 SHONEN.md:0 corpus/lessons/round-39.md:0" reproduces). The five records above
are enumerated in the deliverable with the required treatment.

Evidence commands (run at HEAD 5e985b7):
- `grep -nE 'closed=8/8|8/8 exit=0|failures=0|cases=8' SCORECARD.md LOG.md SHONEN.md corpus/lessons/round-39.md` → r39-relevant hits exactly: SCORECARD:1567, LOG:1709, SHONEN:194, SHONEN:198, round-39.md:15 (other hits are r23–r38 rows; corrections @1560/@1580/@1704/@1719/@190/@203 are already-tagged lines).
- `grep -c '^Correction (round 39)'` → SCORECARD 3, LOG 2, SHONEN 2, round-39.md 0.
- `grep -c '^Correction (round 40)'` → 0 each.

## Finding (b) — future-dated run-utc
None in current committed records. Per-file check (run-utc vs last commit touching the receipt):
- r39 final v5: `run-utc=2026-10-26T20:54:44Z` ≤ commit 8371e7ac @ `2026-10-26T17:55:17-03:00` (=20:55:17Z) ✓
- r37 v1: `18:00:21Z` ≤ commit aa88877b @ 18:00:25Z ✓
- r38 v2: carries no `run-utc` header line ✓
The only future-dated instance in history is the superseded attempt-1 receipt @5006097a v3
(`21:35:00Z` > commit 20:12:12Z), already disclosed at round-39.md:86 and wave-2 findings; must not recur in
r40 receipts (H5/H7 guard). `git grep -i 'run-utc' HEAD` shows no other receipt record.

## Finding (c) — ⟨pending markers
None in the four scanned files (0 each). Lane-wide `git grep` shows ⟨pending only in the historical
`corpus/lessons/round-37.md` (7 markers: lines 10/90/95/216/265/300/320), resolved by the round-38
"Pending-marker resolutions" section; `corpus/lessons/round-39.md` count 0 (kill-rule target for round-40.md
trivially clean — file absent, must be created without markers).

## Finding (d) — score/count mismatches vs freeze controls
All before-controls reproduce exactly on the committed tree at freeze HEAD:

| control | expected | observed |
|---|---|---|
| queued among S016/S017/S019/S020/S021/S022/S023/S024/S025 | 9 | 9 |
| mined among the nine | 0 | 0 |
| knowledge entries citing the nine | 0 | 0 |
| S060+ rows | 0 | 0 |
| frontier rows (corpus/README.md) | 22 | 22 |
| registry rows (corpus/SOURCES.md) | 59 | 59 |
| knowledge count | 51 | 51 |
| harness `frontier-recheck-count.py` | entries=25 pass=25 exit=0 | entries=25 pass=25 exit=0 |
| census validate | exit 0, W04 S028/S029 only | same |
| `corpus/instruments/r40-closure.sh` | absent | absent |

SCORECARD r39 rows consistent (4→4, 7→7, 9→9); move log and round-39 lesson C2 after-values match freeze.
Note for round-40 records: use the freeze base measure 42/51 (frontier 22 + queued 9); do not carry the
r39-base 41/50 from SCORECARD.md:1553 (that section measured at the r39 base dcd31701, frontier 21).

## Environment / hygiene
- Scratch `/fast/scratch/hyaku/kasegi-r40/CritClaimsContradiction/` used for TMPDIR and all work copies; no
  other scratch created. Removed before yield (`rm -rf`).
- No tool installs/upgrades (nothing needed). No lane/fleet files edited; read-only git only.
- Disk guard green at start (26% used on /fast/scratch/hyaku, 600.9G free).
