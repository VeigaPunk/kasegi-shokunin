# AttackB8 — C2 vacuity re-probe on final bytes (coverage)

Seat: L1Kasegi26.AttackB8 (critic, read-only; scratch only). Milestone: C2 vacuity
re-probe. Date: 2026-10-25 UTC. Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## What is attacked

The claimed C2 AFTER state (claims.json C2; coverage score 7 held) on the landed bytes:
F11 admitted (awk 11), entries citing S04x >= 1 (observed 3), sources census exit 0.
Re-probed on the final bytes with scratch trees (wave2/b8/) that mirror the lane
(awk 11 / grep 3 / census 0 / frontier 14-14 / audit 39-39 — identical to integration
measurement) and then apply one mutation at a time.

## (1) Rename/empty of the two F11 entries vs counters

Both mutations were applied to scratch copies of the full `corpus/` tree; every check
below was run on the mutated tree.

| mutation | awk frontier | grep S04x | census | frontier-recheck-count | recheck-audit (expected list) |
|---|---|---|---|---|---|
| baseline (scratch mirror) | 11 | 3 | exit 0 | 14/14 exit 0 | 39/39 exit 0 expect=present |
| rename both files (nothing else) | 11 | 3 | **exit 1 (E11 x2)** | exit 1 (FileNotFoundError on F11 cell) | exit 1 (missing=2 unexpected=2) |
| rename + update S041 used-by cells | 11 | 3 | exit 0 | exit 1 (FileNotFoundError) | exit 1 (missing=2 unexpected=2) |
| empty both files (0 bytes) | 11 | 1 (S040 only) | exit 0 | exit 1 (no-source-line/no-recheck-line/no-source-selection/no-manifest) | exit 1 (lines=37 total=39) |
| empty but keep `source: S041` line | 11 | 3 | exit 0 | exit 1 (no-recheck-line/no-source-selection/no-manifest) | exit 1 (lines=37 total=39) |

Verdict: **the frozen C2 counter set (awk + grep + census) stays green under both rename
and empty.** Rename is invisible to the frozen trio once the S041 used-by cells are kept
consistent (census E11 fires only on the stale-cell variant). Empty is invisible to the
trio in every variant: grep still returns >= 1 because the round-25 S040 entry overmatches
(`^source: S04[0-9] ` matches S040), and census only checks that used-by paths exist, not
that they carry source/recheck content. This re-confirms the wave-1 M26-4 finding on the
final bytes. The non-frozen instruments do catch both: recheck-audit's expected-list
equality (rename) and completeness rule (empty), and the frontier harness contract checks
(empty) / file-open crash (rename). Those are not part of the frozen claim.

### Bodies contain real quoted content (content check, not counter check)
Both entries carry a `source:` header naming S041 (URL + anchor + capture path) and
verbatim quote tables with capture line locations:
- `iso-29147-and-30111-division-of-labour.md`: `source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 付録6 §2 p.45, division paragraph L1667-1672 and 図1 L1676-1678 (capture corpus/source-snapshots/round-26/S041.txt)`; 8-quote table (≤70 chars each).
- `iso-29147-divergence-and-clause-crosswalk.md`: `source: S041 — … 付録6 … §2 (L1666-1678), §3 (L1679-1690), §4 (L1691-1993), 参考1 (L1996-2079), 参考2 (L2082-2100)`; 6-quote table mapped to manifest ids where one exists (Q3/Q4/Q5/Q2b).

Spot verification against the captures: every sampled string exists verbatim at the claimed
capture line — S041.txt L1667, L1669, L1671, L1672, L1677, L1678 (caption repeats at
L1777/L1867/L1908/L1974, documented), L1813 ("6.2 Minimum policy aspects"), L1851
("b）セキュアな通信オプション"), L1868 (divergence sentence), L1916 (7-day receipt);
" The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018" at both
S040-live.txt:58 and round-25 S040.txt:58. The manifest-pinned quotes (Q1a/Q1b/Q2a/
Q2b/Q3/Q4/Q5) are exercised by the running `source-recheck.py --source S041` and both F11
entries PASS exit 0 in the frontier run. The vacuity is in the counters, not in the content.

## (2) Removing the S041 row from SOURCES.md

Mutation: delete the S041 registry row in a scratch copy; run every check.

| check | result |
|---|---|
| sources census (explicit lane dir) | **exit 0** (no E/W code; `ok` line) |
| awk frontier | 11 |
| grep S04x | 3 |
| frontier-recheck-count | 14/14 exit 0 |
| recheck-audit | 39/39 exit 0 |

Verdict: **no check fails when the S041 row is deleted.** The census validates only
table-internal consistency and that used-by paths exist; it never cross-checks that a
source id cited by a knowledge entry has a registry row. The frontier harness never reads
SOURCES.md. The C2 kill-rule limb "a source row is appended without an admitted entry
citing it" has no instrumented converse: rows can be deleted with every gate green.

## (3) F11 row status staged

Mutation: F11 status cell `admitted` → `staged` in scratch README.

| check | result |
|---|---|
| awk frontier | **10** (confirmed: `$4 ~ /^ *admitted *$/` filters staged out) |
| frontier-recheck-count | 12/12 exit 0 (staged row silently dropped from harness) |
| census / grep | unchanged |

Verdict: filtering confirmed — the frozen awk drops to 10 on status staged. The frontier
harness also silently drops the row (12/12), so status alone removes F11 from every gate.

## Verdicts

1. Rename/empty of the two entries is invisible to the frozen C2 counters (awk/grep/
   census); the entries' bodies themselves are real (quotes verbatim at claimed capture
   lines, source headers present, manifest-pinned quotes passing `source-recheck`). The
   non-frozen instruments (recheck-audit expected list/completeness, frontier harness)
   do catch both mutations.
2. Removing the S041 row fails **nothing** — census exit 0, frontier 14/14, audit
   39/39. The kill rule has no instrumented row-deletion converse.
3. F11 → staged drops the awk count to 10 as specified (and drops F11 from the frontier
   harness).

## Smallest safe corrections (for the L1/canonical judge)

- Add a census E-code (reverse E11): every `source:` id appearing in `corpus/knowledge/*.md`
  headers must have a registry row (this closes (2)).
- Anchor the frozen grep to the actual claim: `^source: S041` (or count entries whose
  `source:` id set includes S041) instead of the S04x overmatch, which also fixes the
  do-nothing-control contamination recorded in M26-4 (closes the />=1/ vacuity).
- Optionally have the frontier harness require the F11 cell's files to exist and carry
  non-empty `source:`/`recheck:` lines (already effectively covered by recheck-audit
  completeness; would make the rename crash a clean FAIL instead of a traceback).

## Evidence

All probe runs are on scratch copies under `.ufo/waves/round-26/wave2/b8/` (base, rename,
rename-usedby, empty, empty-src, norow, staged). Baseline scratch = lane bytes:
awk 11; grep 3; census exit 0 (W04 S028/S029 pre-existing warnings); frontier 14/14
exit 0; audit 39/39 exit 0 expect=present. No production bytes modified; no installs.
