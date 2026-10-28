VERDICT: HOLDS

Seat: R46ScoutMerge (read-only assimilation scout, kasegi round 46).
Scope honored: read-only on /home/vgpnk/Projects/shokuknow/merge/kasegi (nothing written there, no campaign tool run); all writes were this Report file plus /fast/scratch/hyaku/kasegi-r46/R46ScoutMerge/ (removed before yield). Lane repo untouched except this Report.

## Finding 1 — The staged package's id premise is stale; 42/94 ids collide with committed rows

Attacked: the package's claim (MERGE-REPORT.md, line 4) that "lane registry currently holds **30** rows; first staged id is **S031**".

Commands (scratch was /fast/scratch/hyaku/kasegi-r46/R46ScoutMerge):

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort > committed.ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md | grep -oE 'S[0-9]+' | sort > staged.ids
comm -12 committed.ids staged.ids > collisions.ids
echo "committed=$(wc -l < committed.ids) staged=$(wc -l < staged.ids) collisions=$(wc -l < collisions.ids)"
```

Output (quoted):

```
committed=72 staged=94 collisions=42
```

- committed ids: 72, all unique, S001..S072 contiguous (`first=S001 last=S072`, count=72 unique=72). Matches frozen claim C2's base "72 SOURCES rows".
- staged ids: 94 (matches the 94 accepted rows in MERGE-REPORT.md), range S031..S124.
- collisions (comm -12): exactly S031..S072, i.e. 42 contiguous ids. The package was cut when the lane had 30 rows; the lane now ends at S072, so adopting the package as-is would create 42 duplicate ids.

Cross-check that the package predates the current registry: staged rows S032/S033 (Bugcrowd VRT README / CWE mapping, raw.githubusercontent.com/bugcrowd/vulnerability-rating-taxonomy) are the same sources the committed registry already holds as S044/S045 (SOURCES.md lines 50-51) — duplicate content under different ids, confirming the staged id space is not the lane's current id space.

## Finding 2 — The guard itself is proven, including against indentation

Attacked: the guard regex on a scratch registry containing an indented duplicate row.

```
SCRATCH=/fast/scratch/hyaku/kasegi-r46/R46ScoutMerge/guard-proof
printf '%s\n' '# scratch registry A (committed-like)' '| S001 | alpha |' '| S002 | beta  |' > "$SCRATCH/registry-committed.md"
printf '%s\n' '# scratch registry B (staged, one row indented by two spaces)' '  | S002 | beta-duplicate-indented |' '| S099 | new |' > "$SCRATCH/registry-staged.md"
cat -A "$SCRATCH/registry-staged.md"
```

`cat -A` proves the indentation is real (quoted):

```
# scratch registry B (staged, one row indented by two spaces)$
  | S002 | beta-duplicate-indented |$
| S099 | new |$
```

Same guard run on both scratch registries, `comm -12` (quoted):

```
committed=2 staged=2 collisions=1
S002
```

The indented `  | S002 |` row is captured (2 leading spaces are inside `^ {0,3}`) and reported as a collision — the guard is not evadable by light indentation.

Boundary (documented, tested): four leading spaces do evade the pattern. Input `    | S003 | four-space-indented |` (cat -A shows `    | S003 |...$`) gives `hits=0`. This is a limitation of the prescribed pattern, not of this run: `grep -cE '^ {4,}\|'` over both real registries returns `0` for corpus/SOURCES.md and `0` for SOURCES.append.md, so no real row hides beyond the pattern's reach.

## Finding 3 — No staged theme/entry covers GitHub private vulnerability reporting (F28)

Attacked: coverage of F28's theme anywhere in the staged package (67 knowledge files — `find ... -name '*.md' | wc -l` prints `67`, matching the merge report's "proposed knowledge entries: **67**").

```
grep -rniE 'private vulnerability reporting|privately report|security\.advisories|private fork|temporary private|CVE request|report a security vulnerability' /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/
```

Output: empty (zero hits).

`grep -rniE 'github' ...` over the staged knowledge dir + report hits only incidental hostnames in source URLs (Bugcrowd VRT on raw.githubusercontent.com, S032/S033; CNNVD spec on raw.githubusercontent.com, S099) — no entry is about the GitHub platform's reporter-side private vulnerability reporting flow (private fork, security advisory draft, credit/collaborator mechanics, SECURITY.md contrast).

Control (do-nothing discrimination): the committed lane corpus also lacks the theme —
`grep -rliE 'private vulnerability reporting|privately report' corpus/knowledge corpus/SOURCES.md corpus/README.md` → `committed-census-hits=0`. So the staged package neither covers nor duplicates coverage of F28; the frozen C2 claim "held nowhere in corpus/" remains true of the package too. (Committed S068 is a public GitHub Advisory Database entry — a different thing from the private reporter flow.)

## Finding 4 — Adoption this round is not possible without touching frozen claims

Three independent blockers, each anchored:

1. Id displacement of the frozen C2 row. freeze.txt line 6 pins `S073-sha256 66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930`, and claims.json `sourced_claim` says "C2 rests on S073 (opened 2026-10-28T22:56Z by the L1; snapshot corpus/source-snapshots/round-46/S073.txt)" with `frontier_step` = "SOURCES rows 72 -> >=73 (S073 tier A mined)". The staged package's own S073 (SOURCES.append.md line 49) is a different source entirely: "最高人民法院关于发布第20批指导性案例的通知（法〔2018〕347号...". Adopting would put a Chinese court case where the frozen gate expects the GitHub row; controls/freeze-controls.txt gates read `row-S073` (G3: `pass=0 read=row-S073=absent-or-malformed` at base) against the F28 row specifically ("c2 junk-row (F28 + S073 rows ...)").
2. 42 id collisions (Finding 1) would force rewriting/renumbering the staged rows — an edit to the shokuknow package (forbidden to me, and out of this round's frozen scope: the freeze pins claims-sha256 e56ebf87..., freeze commit 9f23aab4..., base 914ca0b6...).
3. Even a renumbered adoption would write corpus/SOURCES.md and corpus/knowledge/* — exactly the files the round-46 counters (r46-c1-gate.py over gated `recheck:` entries, r46-c2-gate.py over the S073 row/entry) validate, while the seat charter for round 46 is C1 + C2 only. The claims' own C2 "before" grep (`grep -rliE 'private vulnerability reporting|privately report' corpus/...` prints nothing) is part of the frozen evidence; the adoption would churn that state mid-round.

## Assimilation

**Assimilation: none.** Reason: the staged kasegi package (94 rows S031–S124, 67 entries) contains no coverage of GitHub private vulnerability reporting or anything F28 touches (zero theme hits across all 67 staged knowledge files), and it is unadoptable this round regardless — its id space is cut against a 30-row registry and collides with committed S031–S072 (42 ids), and its S073 is not the frozen C2 S073. The frozen claims hold; nothing in the package advances or endangers them.

## Limitations

- Theme search is grep-level, not semantic reading of all 67 files; terms mirror the frozen claims' own census grep (`private vulnerability reporting|privately report`) plus advisory/fork/CVE-request synonyms. The zero-hit result is exact for those terms.
- Guard boundary at ≥4 leading spaces is a property of the prescribed pattern (tested, `hits=0`); both real registries contain no such rows, so the reported counts are unaffected.
- MERGE-REPORT.json exists alongside the .md; I did not parse it (the .md is the human report my item named). No other staged artifacts were assumed.
- Scratch /fast/scratch/hyaku/kasegi-r46/R46ScoutMerge/ (including guard-proof/) was removed after this Report was written; all outputs quoted above were re-runable one-liners.
