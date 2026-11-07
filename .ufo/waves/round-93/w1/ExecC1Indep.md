# ExecC1Indep — round-93 wave-1: independent byte check of C1 (tranche 8)

Seat: ExecC1Indep (leaf). Scope: byte-level re-derivation of the C1 landing
`ae53b3c6e7e2ce070c2f022d01c1677a8908df1b` against base
`e15996bfd2f6eca4af39507a7c5973afbeca8347` (freeze `5bad9e55d3d9319446e3d9b63bc2dece633cdb68`,
verified ancestor chain base→freeze→landing). Trees built with `git archive` into
scratch; the on-disk labels.tsv sha256 equals the frozen pin
`51b4f3eb3ccc44c9138c29a1052dbb08f951001c9cc0f9dd2971c25f0b670dff`. No counter code
imported: expected edits were reconstructed from the label rows (kind + key + label
text) by my own checker, and the knowledge meter was recounted by my own extractor
written from the documented resolver semantics (`corpus/instruments/resolve.py`
docstring extraction rule and classification domains; `citation-bases.md`).

## Verdict

**AGREE** — the arithmetic and the byte set both re-derived independently.

- All 8 label rows reconstruct byte-exactly against the after tree.
- The base→after diff of `corpus/knowledge/triage-thresholds.md` is exactly 5 changed
  line positions — {58, 144, 437, 438, 454}; the other 482 lines are byte-identical
  (487 lines in both trees, count unchanged).
- The 3 CORRECT no-edit rows are unchanged (their files are byte-identical).
- Every old token occurs exactly once on its base line (5/5).
- No other line changed, and no other path changed in the landing commit: its parent
  is the freeze and `git diff-tree --no-commit-id --name-only -r` prints exactly
  `corpus/knowledge/triage-thresholds.md` (P3 shape reproduced).
- Independent knowledge-meter recount prints base=`1007/2001` and after=`1009/2000`
  (resolved/total distinct path-like backticked tokens over `corpus/knowledge`) — the
  frozen printed values hold, and the token-set diff decomposes to resolved +2,
  GONE −3, total −1 with no class flips.

## Per-row results (`line key kind expected==after`)

| line | key | kind | expected==after |
|---|---|---|---|
| corpus/knowledge/citation-bases.md:14 | claim-gates.md:3 | CORRECT | True (line unchanged) |
| corpus/knowledge/citation-bases.md:14 | ops-invariants.md:18 | CORRECT | True (line unchanged) |
| corpus/knowledge/japanese-domestic-disclosure-workflow.md:7 | japanese-domestic-disclosure-workflow.md | CORRECT | True (line unchanged) |
| corpus/knowledge/triage-thresholds.md:437 | intake-surface.md:75-76 | cell-repair | True (whole last cell replaced by label `fix` text after "Replace cell with: ") |
| corpus/knowledge/triage-thresholds.md:438 | mission-control.md:37-38 | cell-repair | True (same) |
| corpus/knowledge/triage-thresholds.md:454 | SKILL.md:494-506 | SKILL.md:827-848 | True (key→label token replace, backticks included) |
| corpus/knowledge/triage-thresholds.md:58 | SKILL.md:117 | SKILL.md:191 | True (same) |
| corpus/knowledge/triage-thresholds.md:144 | SKILL.md:117 | SKILL.md:191 | True (same) |

Kind distribution matches the frozen M10 shape: cell-repair=2, no-edit(CORRECT)=3,
range=3 (the three lane-root `SKILL.md:N[-M]` label values).

## Changed-line set (exactly 5)

`diff -u` of the two trees' `triage-thresholds.md` (receipt 03): hunks at
@@ -55,7 +55,7 @@ (line 58), @@ -141,7 +141,7 @@ (line 144), @@ -434,8 +434,8 @@ (lines 437–438),
@@ -451,7 +451,7 @@ (line 454). Five `-`/`+` pairs, nothing else. Whole-file `diff -rq`
between the archives shows the only other differing paths are the pre-freeze
wave-support files (claims.json, counters, controls, SOURCES.md,
capture-secret-allow.tsv, round-93 source snapshot, tracked round-31 validate
copies) — all landed before the freeze; freeze..landing name-status is the single
M on triage-thresholds.md (receipt 02).

## Old-token uniqueness and no-edit integrity

`grep -o -F` counts on each base line: `SKILL.md:117` ×1 at lines 58 and 144,
`intake-surface.md:75-76` ×1 at 437, `mission-control.md:37-38` ×1 at 438,
`SKILL.md:494-506` ×1 at 454. `cmp` on citation-bases.md and
japanese-domestic-disclosure-workflow.md: identical across trees.

## Knowledge-meter recount (own extractor)

Extraction = the documented path-like rule (backticked spans, trailing `.,;:`
stripped, space rule, ext/anchor/`/`/`~`/`{`/`<`/`..` triggers, `http`/`xd://`/
`skill://` excluded). Classification = documented domains (OTHER → exists;
BOUNTY → literal else mirror fallback; REL → lane-root exists → INTERNAL else
mirror fallback → GONE; `[lost-*]`/absent bases → GONE). Host state measured:
`mirror-present=False bounty-present=False KASEGI_MIRROR=None`, matching the
frozen meter line's `mirror_absent=True`.

| tree | resolved | total | gone | by_class |
|---|---|---|---|---|
| base | 1007 | 2001 | 994 | RESOLVES 23, INTERNAL 984, GONE 994, MIRROR-EQUIVALENT 0 |
| after | 1009 | 2000 | 991 | RESOLVES 23, INTERNAL 986, GONE 991, MIRROR-EQUIVALENT 0 |

Both printed values hold. Token-set diff (distinct, corpus/knowledge scope):

- removed (6): `SKILL.md:111`, `SKILL.md:117`, `SKILL.md:494-506` (INTERNAL);
  `intake-surface.md:75-76`, `mission-control.md:37-38`,
  `openai-oauth/gpt-6-astra:max` (GONE)
- added (5): `SKILL.md:176-178`, `SKILL.md:191`, `SKILL.md:827-848`,
  `corpus/knowledge/intake-surface.md:89-93`,
  `corpus/knowledge/mission-control.md:55-57` (all INTERNAL)
- class flips: none; noise flips: none (458 noise tokens both trees — the meter
  counts noise; noise-adjusted would be 1543/1542, not the printed totals)

Arithmetic: resolved −3 +5 = +2 (1007→1009); GONE −3 +0 = −3 (994→991);
total −6 +5 = −1 (2001→2000). Exactly the frozen statement's shape.

Anchor-range sanity (consistent with M4/M5, not re-verified semantically):
intake-surface.md 179 lines ≥ 93; mission-control.md 171 ≥ 57; SKILL.md 1251 ≥
848 in both trees.

## Oracle cross-check

Against the committed `citation-survival.tsv` (genuine resolve.py output,
byte-identical in both trees, stale for post-its-round tokens): 1082 shared
tokens, 3 real class disagreements — `.git`, `.git/`, `../MISSION.md:49-56` —
all archive-materialization artifacts (they exist beside the live lane root,
not beside a `git archive` tree), class-stable across base/after, hence
meter-neutral. Zero semantic disagreements. The meter's exact reproduction under
archive materialization on both trees (1010 would have printed had it resolved
against the live lane) confirms the convention.

## Receipts

- `01-commits-and-archive.txt` — rev-parse of all four commits, ancestry checks,
  git-archive extraction, base..after name-status.
- `02-landing-p3-and-tree-diff.txt` — `git show` of the landing (parent = freeze),
  `diff-tree` single-path output, freeze..landing name-status, full `diff -rq`.
- `03-unified-diff-triage.txt` — the complete 5-hunk unified diff.
- `04-tokens-noedit-sha.txt` — old-token occurrence counts, no-edit `cmp`,
  labels.tsv sha256 vs frozen pin, line counts.
- `06-meter-recount.md` — full checker output: 8/8 rows OK, both meter lines,
  token-set diff, OVERALL PASS.
- `07-meter_check-source.py`, `08-compare_ref-source.py` — my extractor and
  oracle-comparison sources for audit.
- `09-committed-census-compare.txt` — per-token class comparison vs the
  committed resolver census.
- `10-resolver-service.txt` — same-tree oracle service lifecycle.

## Risks / blockers

- A fresh same-tree `resolve.py` oracle (service `resolve-rerun`, pid 276716)
  was still mid-run at settle time; it was killed before producing TSVs. The
  committed-census comparison already shows zero semantic disagreements, and the
  meter values reproduced exactly on both trees, so this is residual assurance
  only, not a gap in the verdict.
- My extractor's first pass under-counted resolved by 4 (glob-meta existence
  test); corrected to the documented brace/glob semantics before the reported
  numbers — disclosed for transparency.
- No tools installed; python3 stdlib only. No files written outside the report,
  the receipts directory, and scratch (removed at seat end).
