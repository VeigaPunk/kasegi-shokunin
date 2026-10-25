# MutateRelConfine — relative mirror-fallback confinement mutant (round-23 falsify)

Seat: `L1Kasegi23.MutateRelConfine-2` (mutation-tester, leaf; no subagent dispatch).
Assignment: apply the same mutation method as the bounty-confinement seat, but only to the
**relative mirror fallback** in `corpus/instruments/resolve.py`; report which matrix cases flip,
whether the flipped set is disjoint from the bounty mutation's set, and whether any control flips
(matrix coupling).

All work happened in `/tmp/kasegi-r23-falsify-MutateRelConfine-2` (scratch). No production file,
lane tree, git/jj state, sibling scratch, or fleet repo was written. No tools were installed
(tooling record: none — stock `python3` 3.14.8, `sha256sum`, `diff`, `env`).

## 1. Bytes under test (pinned)

| artifact | sha256 |
|---|---|
| `corpus/instruments/resolve.py` (pristine at seat start, 03:27 mtime) | `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9` |
| `corpus/instruments/mirror-containment-fixtures.json` | `5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9` |
| `.ufo/waves/round-23/c1-baseline-resolver.py` | `d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903` |

**Working-tree drift observed mid-seat (not mine).** While this seat was writing its report, another
party rewrote `corpus/instruments/resolve.py` at `2026-10-25 03:40:40.438084141 -0300`. Current
bytes are sha256 `9e0b5751e820a6868edfff70571e38212763a30446204d7d8522cb0f525d7cde`, differing from
the seat-start bytes in four lines, none of them in `under_mirror()` (`:215-220`) or the relative
branch (`:248-255`):

```
@@ -208  bounty_suffix:            return base[len(root) + 1:]  ->  ... + 1:].lstrip("/")
@@ -231  bounty fallback:          exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)
                                   ->  exists_any(os.path.join(mirror_root, suffix) if suffix else mirror_root)
@@ -347/348: max(...)               ->  max((...), default=0)   (empty-row denominator guards)
```

I did not write, revert, or integrate any of it. To keep the assignment honest against current
landed bytes, §2b re-runs the assigned mutation and the bounty comparison on `9e0b5751…`; the
relative locus is byte-identical there, so the results are unchanged. All §3-§5 work is on the
seat-start bytes `ed9a9dae…`, which is stated per run. Side fact for the integrator: the pinned
receipt `.ufo/waves/round-23/c1-fixed.json` records `resolver_sha256
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9`, so that receipt no longer
matches the working tree after the 03:40:40 write; reconciling it is outside this seat's
read-only mandate.

Setup command (verbatim, scratch only):

```
S=/tmp/kasegi-r23-falsify-MutateRelConfine-2
mkdir -p "$S/orig"
SRC=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments
cp "$SRC/resolve.py" "$S/orig/resolve.py"
cp "$SRC/mirror-containment-check.py" "$S/orig/mirror-containment-check.py"
cp "$SRC/mirror-containment-fixtures.json" "$S/orig/mirror-containment-fixtures.json"
```

Pristine control replay (detector must pass first, otherwise any mutant result is inconclusive):

```
python3 orig/mirror-containment-check.py --resolver orig/resolve.py --json orig/pristine.json
```
→ `cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=ed9a9dae… matrix_sha256=5e61a33e…`, exit 0.
So the baseline is green; the mutant runs below are interpretable.

## 2. Assigned mutation (relative fallback only)

Locus: `corpus/instruments/resolve.py:251-254`, the relative branch's mirror fallback. The
smallest behaviour-bearing point is the `under_mirror()` conjunct at
`corpus/instruments/resolve.py:253`.

```
251:    if base not in ("", ".", ".."):
252:        m, p = exists_any(os.path.join(mirror_root, base))
253:        if m and under_mirror(p, mirror_root):      # <-- mutated to: if m:
254:            return "MIRROR-EQUIVALENT", p, m, "rel"
```

Exact mutant diff (`relmut.diff`, scratch copy `relmut/resolve.py`,
sha256 `7fed2c1a11f4a0b58d0910ea6666d6f5991dcaa69c36d310150fbb302a1d1694`):

```diff
@@ -250,7 +250,7 @@
         return "INTERNAL", p, m, "rel"
     if base not in ("", ".", ".."):
         m, p = exists_any(os.path.join(mirror_root, base))
-        if m and under_mirror(p, mirror_root):
+        if m:
             return "MIRROR-EQUIVALENT", p, m, "rel"
     return "GONE", "", "", "rel"
```

Only line 253 changed. The bounty conjunct (`:232`) and canonical-alias conjunct (`:241`) are
untouched, so the mutant is exactly "the relative fallback loses realpath confinement".

Detector run (same bytes, same matrix):

```
python3 orig/mirror-containment-check.py --resolver relmut/resolve.py --json relmut/receipt.json
```

Output (per-case, verbatim tail):

```
relative-mirror-fallback-escape            escape  expect=GONE             actual=MIRROR-EQUIVALENT FAIL
relative-fallback-symlink-escape           escape  expect=GONE             actual=MIRROR-EQUIVALENT FAIL
cases=13 escape=6 controls=7 pass=11 fail=2 resolver_sha256=7fed2c1a… matrix_sha256=5e61a33e…
```

**Verdict: KILLED** (2/13 cases fail, exit 1).

Flipped set (pristine class → mutant class), computed by diffing the two JSON receipts:

| case | pristine | mutant |
|---|---|---|
| `relative-mirror-fallback-escape` (`../outside-vault/secret.mjs:1`) | GONE | MIRROR-EQUIVALENT |
| `relative-fallback-symlink-escape` (`nested/leak.md:1`) | GONE | MIRROR-EQUIVALENT |

Controls: **0/7 flipped** (all seven keep their pinned class). Escape detection drops from 6/6
to 4/6; the two lost cases are precisely the two relative-branch escapes.

Mechanism, reproduced through the real CLI (not just the checker) on a persistent fixture:

```
env -i HOME=$F/home KASEGI_MIRROR=$F/relocated/tbh PATH=/usr/bin:/bin \
  LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  python3 $F/tool/resolve.py $F/lane
```

Traversal case — TSV row under the mutant:

```
../outside-vault/secret.mjs:1	MIRROR-EQUIVALENT	$ROOT/relocated/tbh/../outside-vault/secret.mjs	1	literal	rel	1	SKILL
REAL_MIRROR=$ROOT/relocated/tbh
REAL_CREDITED=$ROOT/relocated/outside-vault/secret.mjs      # realpath is OUTSIDE the mirror
```

Symlink case — TSV row under the mutant vs pristine on identical bytes:

```
mutant:   nested/leak.md:1	MIRROR-EQUIVALENT	$ROOT/relocated/tbh/nested/leak.md	1	literal	rel	1	SKILL
pristine: nested/leak.md:1	GONE		1		rel	1	SKILL
REAL_LINK=$ROOT/secret/second.md      # realpath leaves the mirror through the symlink
```

Depth note: in the symlink case the *printed* `resolved_path` is literally inside the mirror root
string; only realpath resolution distinguishes it. A downstream verifier that string-matches
`resolved_path` against the mirror root would accept the mutant's output. This is why the
`under_mirror()` call is load-bearing and why the matrix's only physical evidence for it in the
relative locus is those two cases.

## 2b. Re-run on the current working-tree bytes (`9e0b5751…`)

Same method, same matrix, applied to a copy of the post-drift bytes (`newbytes/resolve.py`,
sha256 `9e0b5751e820a6868edfff70571e38212763a30446204d7d8522cb0f525d7cde`).

Pristine drifted bytes: `cases=13 escape=6 controls=7 pass=13 fail=0`, sha `9e0b5751…` — green.

Relative-conjunct-only mutant on drifted bytes (`newrelmut/resolve.py`, sha256
`a8f0760d1c59e870f6d577db162bc3448839a8affb957d6ddd43099643e71e41`):

```
pass=11 fail=2
REL_FLIPS = ['relative-fallback-symlink-escape', 'relative-mirror-fallback-escape']
REL_CONTROL_FLIPS = []
```

Bounty-conjunct comparison on drifted bytes (`newbountymut/resolve.py`, sha256
`c0fa4f8f764201956b1eaa0d968ea161748a396ecb065cfda68895fe10e2b9d1`):

```
pass=10 fail=3
BOUNTY_FLIPS = ['bounty-fallback-symlink-escape', 'bounty-parent-traversal', 'bounty-parent-traversal-vault']
INTERSECTION = []
```

Both flip sets are byte-for-byte the seat-start results; the drift touches no locus this seat
mutated, and the disjointness/control conclusions hold on the current bytes.

## 3. Disjointness from the bounty mutation

Independent comparison run in my own scratch (not taken from any peer): same method applied only
to `corpus/instruments/resolve.py:232` (`bountymut/resolve.py`, sha256
`163f54b07adb30a28913e2df772b87e2cb3bc21b1bd27b89cb251f11f04a2e31` — byte-identical hash to the
hash the bounty seat reported, so the mutants are provably the same defect):

```
python3 orig/mirror-containment-check.py --resolver bountymut/resolve.py --json bountymut/receipt.json
```
→ `pass=10 fail=3`, flipped set
`{bounty-parent-traversal, bounty-parent-traversal-vault, bounty-fallback-symlink-escape}`.

Set comparison (machine-computed from receipts):

```
REL_FLIPSET    ['relative-fallback-symlink-escape', 'relative-mirror-fallback-escape']
BOUNTY_FLIPSET ['bounty-fallback-symlink-escape', 'bounty-parent-traversal', 'bounty-parent-traversal-vault']
INTERSECTION   []
REL_CONTROL_FLIPS    []
BOUNTY_CONTROL_FLIPS []
```

**Finding: the two flip sets are disjoint.** Escape cases `1,2,4` respond only to the bounty
conjunct (`:232`); cases `3,5` respond only to the relative conjunct (`:253`). No case needs both,
and no control moves under either single mutation.

Additive-partition corroboration (both fallback conjuncts removed, `:232` **and** `:253`; boundary
and canonical-alias branches intact; `combinedmut/resolve.py`,
sha256 `c73dc622ce8f7ee35862fed95e0c38cdf04f1b37fd55c9ef53d6048f3757db24`):

```
pass=8 fail=5; flips = 3 bounty-branch cases ∪ 2 relative-branch cases
bounty-prefix-sibling-confusion stays GONE
```

That last row is the observed reason the third C1 locus exists: `bounty-prefix-sibling-confusion`
is guarded by `bounty_suffix()`'s exact-root boundary (`.ufo/waves/round-23/c1-baseline-resolver.py`
vs `resolve.py` diff, @@ −201/+222 hunk), not by `under_mirror()`. The six escapes partition
cleanly: 3 from `:232`, 2 from `:253`, 1 from the boundary. (The boundary-only mutant is the
bounty seat's other probe; I did not run it and do not claim its result.)

## 4. Does any control flip? (matrix coupling)

**No.** Under the assigned relative mutant all 7 controls keep their pinned classes, including
the two that touch the same code path:
`confined-relative-fallback-control` (GONE→ stays MIRROR-EQUIVALENT) and
`lane-relative-parent-internal-control` (`../outside.md` stays INTERNAL via the lane branch).
The matrix therefore does **not** couple the bounty and relative containment fixes through any
control: each escape case is a single-locus discriminator, and each control is insensitive to the
`:253` conjunct.

## 5. Extra probes on the same locus (labelled as beyond the assigned mutant)

Each is a separate scratch copy with a one-hunk diff; all were run through the same checker.

### 5a. `abspath` instead of `realpath` — KILLED, but on a 1-case margin

Mutant replaces the relative branch's `under_mirror(p, mirror_root)` with
`os.path.abspath(p).startswith(os.path.abspath(os.path.expanduser(mirror_root)) + os.sep)`
(`abspathmut/resolve.py`, sha256 `aaadaa9031d111f3cd39ea78d1e4dfc001e4eb3ded7292e3e25671effacb8f1d`).

```
relative-mirror-fallback-escape   PASS  (abspath normalizes the '..' — mutant looks correct here)
relative-fallback-symlink-escape  FAIL  GONE -> MIRROR-EQUIVALENT
pass=12 fail=1
```

Verdict: **killed**, but the symlink case is the *sole* discriminator between normalized-path
confinement and realpath confinement in the relative locus. Drop `relative-fallback-symlink-escape`
and a naive-abspath regression would score 13/13.

### 5b. Lane-first ordering removed — SURVIVED

Mutant reverses the relative branch to mirror-first, lane-second
(`ordermut/resolve.py`, sha256 `8cf28fb002cf269b3695d52e74b787688904d58c3761df948b01a5637fa29601`).

```
cases=13 escape=6 controls=7 pass=13 fail=0        # 13/13 PASS
```

Verdict: **SURVIVED**. This is a coverage finding, not an equivalent mutant: with a relative
citation present in *both* the lane tree and the mirror, the behaviour changes. Manual proof on
identical fixture bytes (`lane/docs/note.md` and `mirror/docs/note.md` both exist; cite
`docs/note.md:1`):

```
pristine: docs/note.md:1	INTERNAL	 $ROOT/lane/docs/note.md
ordermut: docs/note.md:1	MIRROR-EQUIVALENT	 $ROOT/relocated/tbh/docs/note.md
```

Why the matrix misses it: `lane-relative-parent-internal-control` uses `../outside.md`, which
exists only at `lane/../outside.md` (the mirror-relative sibling `relocated/outside.md` does not
exist), and `confined-relative-fallback-control` makes its file exist only in the mirror. So no
case has the same relative token resolvable in both trees. The fixture note on that control says
"the lane-repo branch runs first, so this stays INTERNAL" — my probe shows the case passes under
mirror-first ordering too, i.e. **the frozen matrix does not actually pin lane-first precedence**.

### 5c. `commonpath` replaced by a separator-less prefix test — SURVIVED

Mutant changes `under_mirror()` (`corpus/instruments/resolve.py:215-220`) from
`os.path.commonpath((r, p)) == r` to `p.startswith(r)` (`prefixmut/resolve.py`, sha256
`1e9f8d46df5593404ad1fc22ef02710031f021400bb0af2203a1bdc8d4e13dd1`), which credits
`.../tbh-evil/...` under mirror root `.../tbh`.

```
cases=13 escape=6 controls=7 pass=13 fail=0        # 13/13 PASS
```

Verdict: **SURVIVED**. Behaviour-bearing manual proof on identical fixture bytes
(file at `relocated/tbh-evil/decoy.md`, cite `../tbh-evil/decoy.md:1`):

```
pristine:  ../tbh-evil/decoy.md:1	GONE
prefixmut: ../tbh-evil/decoy.md:1	MIRROR-EQUIVALENT	 $ROOT/relocated/tbh/../tbh-evil/decoy.md
```

The matrix has a prefix-sibling case for the **bounty** root
(`bounty-prefix-sibling-confusion`, guarded by `bounty_suffix()`) and
`literal-prefix-sibling-control` for the literal `~/Projects` root, but **no case exercises a
prefix sibling of the selected mirror root**. This is the same defect class C1's own claim text
names ("reject sibling-root prefix confusion"), and it is unpinned for the mirror root in the
relative locus.

## 6. Falsifiable findings (mine, from observed outputs)

1. **The relative conjunct is detected exactly twice, never more.** Removing it flips exactly
   `{relative-mirror-fallback-escape, relative-fallback-symlink-escape}` on the 13-case matrix
   (escape 6/6 → 4/6) and exactly the same two on the final 20-case matrix (escape 9/9 → 7/9).
   Controls never move. Any "all escapes GONE" claim is only as strong as those two cases for the
   relative locus; the four cases added later are all bounty-branch or bracket-expansion cases.
2. **The bounty and relative containment fixes are disjoint in fixture terms.** Independent
   receipts give an empty intersection and no control movement on both snapshots. On the final
   20-case matrix: relative mutant flips 2 (both relative), bounty mutant flips 4 (three bounty
   traversal/symlink cases plus `brace-expansion-escape`), intersection empty. On the 13-case
   matrix a combined mutant's flips were exactly the union of the two single-locus sets (5 = 3 + 2).
   The matrix does not couple the two fixes.
3. **Coverage gap (surviving, behaviour-bearing, persists on the final 20-case matrix):** the
   matrix cannot distinguish lane-first from mirror-first relative resolution, although a control's
   note asserts lane-first semantics. `f1_order` scores 20/20.
4. **Coverage gap (surviving, behaviour-bearing, persists on the final 20-case matrix):** the
   matrix cannot distinguish `commonpath`-confinement from separator-less prefix confinement, i.e.
   it does not reject a mirror-root prefix sibling (`.../tbh-evil`) in the relative fallback.
   `f1_prefix` scores 20/20. Note the final matrix added `absolute-prefix-sibling-confusion`, which
   is a **bounty-root** prefix sibling — it does not cover the mirror-root case.
5. **Thin margin (holds on both snapshots):** realpath-vs-abspath confinement in the relative locus
   is carried by one case (`relative-fallback-symlink-escape`); the traversal case does not
   discriminate (abspath normalizes `..`). `f1_abspath` fails exactly 1/20.

Findings 3-5 are coverage findings; I do not claim the landed bytes are wrong (pristine replay is
13/13 on seat-start bytes and 20/20 on the final snapshot; the manual prefix-sibling and
both-trees-ordering cases are GONE/INTERNAL under pristine). Only the matrix's discriminating power
is at issue.

## 7. Restoration evidence

Every mutant resolver copy was restored from the pristine copy; the mutant bytes remain available
as the `.diff` files above, and all receipts are on disk.

```
$ sha256sum orig/resolve.py relmut/resolve.py bountymut/resolve.py combinedmut/resolve.py \
            abspathmut/resolve.py ordermut/resolve.py prefixmut/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  orig/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  relmut/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  bountymut/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  combinedmut/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  abspathmut/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  ordermut/resolve.py
ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9  prefixmut/resolve.py

$ sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/resolve.py
ed9a9dae…  …/corpus/instruments/resolve.py     # at 03:39, seat-start bytes (all §2-§5 runs)
9e0b5751e820a6868edfff70571e38212763a30446204d7d8522cb0f525d7cde  …/corpus/instruments/resolve.py
                                                # at 03:41+, after another party's 03:40:40 write
```

Post-restore replays (identical to the pre-mutation control, on the respective bytes):

```
python3 orig/mirror-containment-check.py --resolver orig/resolve.py
  cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=ed9a9dae… matrix_sha256=5e61a33e…
python3 orig/mirror-containment-check.py --resolver /…/corpus/instruments/resolve.py   # at 03:39
  cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=ed9a9dae… matrix_sha256=5e61a33e…
python3 orig/mirror-containment-check.py --resolver newbytes/resolve.py                 # at 03:41
  cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=9e0b5751… matrix_sha256=5e61a33e…
```

Drift-generation copies were restored to the drifted bytes, not to `ed9a…`:

```
9e0b5751…  newbytes/resolve.py
9e0b5751…  newrelmut/resolve.py
9e0b5751…  newbountymut/resolve.py
```

Production integrity: my only writes were inside `/tmp/kasegi-r23-falsify-MutateRelConfine-2` and
this report. The production file's mtime moved from `03:27:44.381977020` to
`03:40:40.438084141 -0300` (code change) and then `03:42:37.811829694 -0300` (docstring-only), both
by **different seats'** writes; the checker and the fixture matrix were also rewritten under this
seat (§9). I neither performed nor reverted any of it, per the read-only mandate. No git/jj
operation was run by this seat.

## 8. Scope limits

- Detector exercised: `corpus/instruments/mirror-containment-check.py` over the 13-case
  seat-start matrix and the 20-case final snapshot (§9), plus real-CLI replays on five ad-hoc
  fixtures of my own construction (persistent under scratch, not admitted to the matrix).
- Only `classify()`'s relative branch (`resolve.py:248-255` on seat-start bytes; `:256-264` after
  the docstring growth) and its `under_mirror()` helper (`:215-220` / `:224-229`) were mutated. No
  C2 artifact, source snapshot, knowledge entry, README/SOURCES/QUALITY row, receipt, or claim was
  touched or re-verified.
- Linux-only realpath/symlink semantics; no Windows/macOS commonpath edge cases.
- Surviving mutants are reported as matrix coverage findings. They do not assert a live defect in
  the landed bytes, do not move any score, and do not license changing the contract.
- Nothing here is an admission claim; independent non-author closure remains with L1.

## 9. Matrix evolution during this seat (environment churn)

All rows below are other seats' writes observed while this seat held the tree read-only.

| time | artifact | hash | note |
|---|---|---|---|
| 03:27:44 | `resolve.py` | `ed9a9dae…` | seat-start bytes; all §2-§5 runs |
| 03:40:40 | `resolve.py` | `9e0b5751…` | 4-line code change at `:208`, `:231`, `:347-348` (§1) |
| 03:42:37 | `resolve.py` | `8dd45bc8…` | docstring-only vs `9e0b…` (AST equal with docstrings stripped) |
| 03:28:25 | checker | `1bc2db10…` | seat-start checker |
| 03:42:15 → 03:43:01 | checker | `fc9550f0…` → `53742c8d…` | adds `path_check=` reporting |
| 03:28:11 | fixtures | `5e61a33e…` | 13 cases (6 escape / 7 control) |
| 03:42:46 → 03:43:01 | fixtures | `eac8d3ec…` → `5c64e014…` | reformatted, then 17 cases (7 / 10) |
| 03:43:38 | fixtures | `4e39f65c…` | 20 cases (9 escape / 11 control) — final pinned snapshot |
| 03:46:26 | `resolve.py` | `fce5b84b…` | bounty branch only: root-only bounty citations revert to no mirror mapping, with comment; relative branch byte-identical |

Transient observation: at fixtures `eac8d3ec…` one in-repo run of the then-current production
bytes reported `cases=17 … pass=16 fail=1`. The fixture file changed again before I could write a
receipt, so the failing case id is unrecoverable; I record this only as churn evidence, not as a
finding.

Final pinned snapshot (all §9 runs): production `8dd45bc8…`, checker `53742c8d…`, fixtures
`4e39f65c…` (20 cases), copied to `/tmp/kasegi-r23-falsify-MutateRelConfine-2/finalmatrix/`.
Production replay on that snapshot: `cases=20 escape=9 controls=11 pass=20 fail=0`.

Mutant re-runs on that snapshot (each built from `8dd45bc8…`; receipts on disk):

| mutant | sha256 | result | flips |
|---|---|---|---|
| `f1_rel` — relative conjunct removed (assigned) | `2d2dcb4e…` | KILLED, 18/20 | the 2 relative escapes |
| `f1_bounty` — bounty conjunct removed | `1f72a5df…` | KILLED, 16/20 | 3 bounty cases + `brace-expansion-escape` |
| `f1_order` — mirror-first relative branch | `40dff4e8…` | SURVIVED, 20/20 | none |
| `f1_prefix` — helper `p.startswith(r)` | `d54c48e9…` | SURVIVED, 20/20 | none |
| `f1_abspath` — abspath in relative branch | `06a28e61…` | KILLED, 19/20 | 1 symlink escape |

Relative∩bounty flip set on the 20-case snapshot: empty. Control flips: none in any mutant.

Survivors re-proved behaviour-bearing on these exact bytes with the manual fixtures:
both-trees `docs/note.md` → prod `INTERNAL`, `f1_order` `MIRROR-EQUIVALENT`; prefix sibling
`../tbh-evil/decoy.md` → prod `GONE`, `f1_prefix` `MIRROR-EQUIVALENT`.

All §9 copies restored to `8dd45bc8…` after the runs (`sha256sum` verified); the newest-bytes
mutant `f2_rel` was restored to `fce5b84b…`.

Newest-bytes cross-check (`fce5b84b…`, written 03:46:26): production passes the pinned 20-case
matrix `20/20`; the only code change versus `8dd45bc8…` is in the bounty branch (root-only bounty
citations no longer map to the mirror), the relative branch is byte-identical, and the same
relative-conjunct removal rebuilt on those bytes (`f2_rel`, sha256
`c5c15ef1f772319300925df416b37a0419af355e21d4bb1808942bd98d01a897`) flips exactly the same two
cases (18/20). The assigned verdict and the disjointness conclusion are therefore invariant across
all three production revisions this seat observed. Writes after 03:46:26 are not tracked here.
