# ExecC1Indep — round-97 w1 — independent re-derivation of C1's numbers

Seat: ExecC1Indep (leaf). Base b06af5e07efbd961a8449f7de6b57eeea62c6bd3, freeze daf7fc6a627d615178c27594110e956e592e4cd9, C1 landing 75a471809cba265c8981ece1c0ed29c7895d9308.
Consumed frozen artifacts (sha256 observed, all equal the pins in claims.json): counter a56198d0…, map f4ed7387…, labels 5155959d…, harness 471feda7…. `corpus/instruments/resolve.py` is byte-identical at base and landing (cmp rc=0), so the census semantics are revision-stable.

Method note: I wrote and ran my own census/patch implementation in my scratch (`/fast/scratch/hyaku/kasegi-r97/ExecC1Indep`, deleted after the seat); I did not execute the lane's counter. I did read the frozen counter and `resolve.py` to pin the exact predicate semantics before implementing them myself; every number below is my own code's output over my own `git archive` extracts.

## My census rules (stated, as required)

- Scope: `corpus/knowledge/*.md` (105 regular files at both revisions; the Goal's "16 files" are the map's edit sites, not the census scope).
- Extraction: per line, every non-overlapping inline span `` `([^`\n]+)` ``; token = span `.strip().rstrip(".,;:")`. Token is path-like iff: non-empty; not (contains a space with no `/`); not prefixed `http`/`xd://`/`skill://`; and (ends with a tracked extension .mjs/.md/.json/.jsonl/.yml/.yaml/.py/.sh/.txt/.git/.gitignore case-insensitively, or ends `/`, or starts `~/`|`/`, or contains `/`,`<`,`{`,`~` or `..`, or ends with a tracked extension after stripping one trailing `:N`/`:N–N` line anchor). Distinct tokens = set over the scope.
- Classification (mirror absent on this host — `~/Projects/the-bounty-hunter` and `~/Projects/origin-work/the-bounty-hunter` both missing, `KASEGI_MIRROR` unset, so no mirror fallback): strip one trailing line anchor (`:N`, `:N-N`, `:N–N`) else `::sym`; bounty-rooted tokens → host-exists ? RESOLVES : GONE; mirror-rooted → GONE; `~`/`/`-rooted → host-exists ? RESOLVES : GONE; relative → exists against that revision's full tree extract (literal, then bounded `{a,b}` brace expansion, then `<…>`→`*` glob) ? INTERNAL : GONE.
- Rate = (class ≠ GONE, total distinct).

## Item 1 — census: AGREE

My numbers, reproduced exactly:

- base: **1040/2041** (GONE=1001, INTERNAL=1017, RESOLVES=23)
- landing: **1043/2035** (GONE=992, INTERNAL=1020, RESOLVES=23)
- delta: denominator 2041→2035 (**−6**), numerator 1040→1043 (**+3**)

Decomposition matches the claim's "+3 new to scope / −6 already existed": exactly 3 tokens are new at the landing, all INTERNAL — `corpus/instruments/density.py`, `corpus/instruments/resolve.py`, `corpus/instruments/source-recheck.py`; all 9 bare basenames are GONE at base and have 0 occurrences at the landing (they leave the scope entirely). The other 6 qualified paths (`anchorcheck.py`, `capture-source.py`, `capture-secret-scan.py`, `claim-package-check.py`, `r35-defect-closure.sh`, `r36-closure.sh`) already existed as INTERNAL tokens at base, so they only shrink the denominator. Corroboration: base occurrences of the 9 basenames are 5+6+5+9+2+2+1+1+2 = **33** — exactly the 33 map rows, i.e. the map rewrites every bare occurrence in scope.

## Item 2 — map applied by hand vs landing: AGREE

`repair-map.tsv` = 33 rows, 30 distinct (file:line) sites, **16 files**. Row shape verified: every `old` is exactly `` `key` `` with a bare basename key (no separator/anchor), every `new` is a `corpus/instruments/…` path tracked at the landing and outside `.ufo/` (9 distinct keys: anchorcheck×6, capture-secret-scan×2, capture-source×5, claim-package-check×1, density×2, r35-defect-closure×1, r36-closure×2, resolve×5, source-recheck×9). I applied the rows to my `git archive` of the base (replace-all of `old` per mapped line) and compared bytes against `git archive` of the landing: **all 16 patched files are byte-identical to the landing** (sha256 prefixes equal per file, e.g. capture-intake-gate.md 8252fd44474b both sides), each changed vs base, and map_files == diff_files (16 == 16, same_files=True).

Routed textual qualifier (not a verdict limb): the seat item said "the twelve files" and the claims *surface* says "33 bare lane-instrument basenames in 12 corpus/knowledge files", but the map, the diff, and the claims *statement* all say **sixteen** files. The "12" texts are stale/incorrect counts; I diffed all sixteen. Does not re-score C1 — predicate M3 compares map vs diff (both 16).

## Item 3 — changed-line count: AGREE

`git diff --numstat base landing -- corpus/knowledge`: **16 files, 30 added + 30 deleted lines**. The claim's "33 rows on 30 lines" reads exactly: 33 map rows on 30 distinct lines; the 3 two-row lines are `capture-intake-gate.md:11`, `considerthese-proposals-ledger.md:125`, `root-loss-2026-10-12.md:54` (uniq -d on the site column).

## Verdict

AGREE on all three items — re-derived independently: meter 1040/2041 → 1043/2035 with +3 numerator/−6 denominator and the claimed 3-new/6-existing decomposition; map application is byte-exact at all sixteen labelled files; 33 rows land on 30 changed lines. One routed qualifier: the "12 corpus/knowledge files" count in the claims surface (and seat item 2) contradicts the actual sixteen-file map/diff and the frozen statement. No verdict change to C1; no tools installed.

## Receipts

Directory: `.ufo/waves/round-97/w1/ExecC1Indep-receipts/`

- `numstat-corpus-knowledge.txt` — `git diff --numstat b06af5e0 75a47180 -- corpus/knowledge` (16 files, 30+/30−) and awk totals `files=16 added=30 deleted=30`; rc=0.
- `census-run.txt` — `python3 -B census.py` over `git archive` extracts of both revs: CENSUS base rate=1040/2041, land rate=1043/2035, DELTA lines, nine-basename classification/occurrence table; rc=0.
- `apply-map-run.txt` — `python3 -B apply_map.py`: rows=33 distinct_sites=30 files=16, 9 key histogram, all-qualify-lane shape/tracked assertions, per-file `patched==land:True patched!=base:True` with sha prefixes, `map_files=16 diff_files=16 same_files=True`, APPLY-AND-COMPARE PASS; rc=0.
- `pins-and-identity.txt` — sha256sum of counter/map/labels/gen-c1.py/harness (all equal frozen pins), `cmp` resolve.py base vs land (identical rc=0), `uniq -d` site column (3 two-row lines).
- Scratch (extracts, census TSVs, patched tree, scripts) removed after the seat per wave rules.
