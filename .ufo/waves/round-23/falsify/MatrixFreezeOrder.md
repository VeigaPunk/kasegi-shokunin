# MatrixFreezeOrder — C1 fixture-matrix freeze order and control falsifiability

Seat: `L1Kasegi23.MatrixFreezeOrder-2` (critic, read-only). Frozen claim read: `.ufo/waves/round-23/claims.json` C1. Artifacts attacked:
`corpus/instruments/mirror-containment-fixtures.json`, `corpus/instruments/mirror-containment-check.py`,
`.ufo/waves/round-23/c1-baseline{,-resolver}.{json,py}`, `c1-fixed.json`.
All probes ran on copies under `/tmp/kasegi-r23-falsify-MatrixFreezeOrder`; nothing in the repo was written except this report.

Axes: `depth:verifiability` (does the freeze order support the fail-before/pass-after contrast) and `coverage` (which C1 cases are pinned at all).

---

## 1. Answer to the assigned question: tuning after the baseline run is **excluded**; tuning before it is **not**

**Excluded, by content-addressed binding plus inode time.** Both receipts record the matrix they ran:

```text
$ sha256sum corpus/instruments/mirror-containment-fixtures.json
5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9
$ python3 -c "import json;[print(f, json.load(open(f))['matrix_sha256']) for f in ('.ufo/waves/round-23/c1-baseline.json','.ufo/waves/round-23/c1-fixed.json')]"
.ufo/waves/round-23/c1-baseline.json 5e61a33e…b5e76a9
.ufo/waves/round-23/c1-fixed.json    5e61a33e…b5e76a9
```

`stat` shows one inode lifetime, not an edit history (`ctime == mtime` to the nanosecond, so the file was created and never touched afterwards):

```text
corpus/instruments/resolve.py                      mtime=2026-10-25 03:27:44.381977020
corpus/instruments/mirror-containment-fixtures.json mtime=2026-10-25 03:28:11.864283451 ctime=same
corpus/instruments/mirror-containment-check.py      mtime=2026-10-25 03:28:25.572284895
.ufo/waves/round-23/c1-baseline-resolver.py         mtime=2026-10-25 03:28:28.805308795
.ufo/waves/round-23/c1-baseline.json                mtime=2026-10-25 03:28:29.159339383
.ufo/waves/round-23/c1-fixed.json                   mtime=2026-10-25 03:28:32.643994999
```

The matrix predates both receipts; any expectation edited after the baseline run would break the recorded `matrix_sha256`, and no second matrix version exists in VCS (see §2). The receipts also reproduce exactly — I replayed both:

```text
$ python3 mirror-containment-check.py --json A-fixed.json | tail -1
cases=13 escape=6 controls=7 pass=13 fail=0 resolver_sha256=ed9a9dae… matrix_sha256=5e61a33e…
$ python3 mirror-containment-check.py --resolver c1-baseline-resolver.py --json B-baseline.json | tail -1
cases=13 escape=6 controls=7 pass=7 fail=6 resolver_sha256=d6a3c3f1… matrix_sha256=5e61a33e…
committed==replayed baseline per-case: True
committed==replayed fixed per-case: True
```

The do-nothing control is genuine provenance, not a weakened copy: `c1-baseline-resolver.py` is byte-identical to the ancestor blob.

```text
$ git show 922a4dd:corpus/instruments/resolve.py | sha256sum   → d6a3c3f1…d869f903
$ sha256sum .ufo/waves/round-23/c1-baseline-resolver.py        → d6a3c3f1…d869f903   (cmp - → CMP-IDENTICAL)
```

**Evidence anchor.** Every replay below ran against `resolve.py` sha256 `ed9a9dae…2840e9`, the exact bytes named by `c1-fixed.json` and committed at `953c278`. During this review the working tree moved (§1.1); the results are labelled by which bytes produced them.

### 1.1 The working tree diverged from the receipts while this review ran

At 2026-10-25 03:40:40 (after the 03:28:32 fixed receipt and after my first replays) a sibling changed `corpus/instruments/resolve.py` to sha256 `9e0b5751…5d7cde`, 27436 bytes, 4 lines:

```text
-                return base[len(root) + 1:]
+                return base[len(root) + 1:].lstrip("/")
-        m, p = exists_any(os.path.join(mirror_root, suffix)) if suffix else (None, None)
+        m, p = exists_any(os.path.join(mirror_root, suffix) if suffix else mirror_root)
-    maxfiles = max(r["nfiles"] for r in rows)
-    maxocc = max(r["occ"] for r in rows)
+    maxfiles = max((r["nfiles"] for r in rows), default=0)
+    maxocc = max((r["occ"] for r in rows), default=0)
```

Consequences to state plainly:

- `c1-fixed.json` names `ed9a9dae…`; the worktree is `9e0b5751…`. **No receipt binds the current bytes**, so "matrix 13/13" is now a statement about `ed9a9dae` only. The matrix hash is unchanged, but the resolver half of the pair is stale.
- The landed matrix still passes 13/13 on the new bytes (`resolver_sha256=9e0b5751… matrix_sha256=5e61a33e…`), so the divergence does not move the matrix figure; it does mean the receipt set cannot be cited as evidence for the tree as it now stands.
- The `max(..., default=0)` change fixes the empty-corpus abort I reproduced below; the expansion over-rejection does **not** change (see §3, replayed on both versions).

**Not excluded, and observable: the matrix was authored with the fixed bytes already on disk, and its only committed version arrives in the same commit as the fix.** `resolve.py` (fixed) is written 27 s *before* the matrix file, and there is no pre-registered matrix hash anywhere:

```text
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-23/claims.json'));print(sorted(d));print(sorted(d['C1']))"
['C1','C2','admission','base','round','supporting_corrections']
['after','axis','before_observed','claim','detector','guard']          # no hash/fixture field
$ git log --format='%h %ad %s' --date=iso --follow -- corpus/instruments/mirror-containment-fixtures.json
953c278 2026-10-25 03:35:35 -0300 round-23: … matrix receipts; admit F06-F08 with pinned-source rechecks
$ git rev-parse {953c278,52ee05c,87dbd03,b284aff}:corpus/instruments/mirror-containment-fixtures.json
4ede1bcc… (identical blob in all four)
$ git cat-file -e 8bf9807:corpus/instruments/mirror-containment-fixtures.json
fatal: path '…mirror-containment-fixtures.json' exists on disk, but not in '8bf9807'
```

So the committed record contains exactly one matrix version and it is co-authored with the fix and its receipts. The freeze *order* that can actually be observed is: fixed code → matrix → checker → baseline receipt → fixed receipt, all inside 48 s, then one commit 7 min later. Nothing in the landed evidence dates the expectations before the first fixed-resolver run. (An independent seat, `ClaimsIntegrity-2`, reports the same first-appearance commit; I verified it above rather than accepting it.)

---

## 2. The authoring record contradicts the landed matrix: 15 IDs / 8 escapes → 13 IDs / 6 escapes, undocumented

`.ufo/waves/round-23/build/CountMirror.md` is the seat that authored the fixtures. It is present in commit `8bf9807` (`git show 8bf9807:.ufo/waves/round-23/build/CountMirror.md` returns this text), its on-disk mtime is 2026-10-20 18:46:39, and it states:

> `:30` The committed JSON matrix has 15 IDs. Its eight distinct escaped-path cases all pin `GONE`:
> … `placeholder-expansion-escape`, `glob-expansion-escape`, `canonical-tilde-alias-parent-escape`, `canonical-absolute-alias-symlink-escape`, … `empty-citation-produces-no-row`

The landed matrix has 13 IDs and 6 escapes, and four of those named IDs appear nowhere but that note:

```text
$ grep -rln "empty-citation-produces-no-row\|placeholder-expansion-escape\|glob-expansion-escape\|canonical-tilde-alias-parent-escape" --exclude-dir=.git .
./.ufo/waves/round-23/build/CountMirror.md        # only hit
$ python3 -c "import json;d=json.load(open('corpus/instruments/mirror-containment-fixtures.json'));print(len(d['cases']),sum(1 for c in d['cases'] if c['nature']=='escape'))"
13 6
$ for c in 893b816 f9462ad e812b74 8bf9807; do git ls-tree -r --name-only $c | grep -i mirror-containment; done
(no output: no mirror-containment file in any pre-953c278 commit)
$ for c in 8bf9807 e812b74 f9462ad 893b816; do git grep -l "placeholder-expansion-escape" $c; done
8bf9807:.ufo/waves/round-23/build/CountMirror.md
e812b74:.ufo/waves/round-23/build/CountMirror.md
f9462ad:.ufo/waves/round-23/build/CountMirror.md
893b816:.ufo/waves/round-23/build/CountMirror.md
```

The dropped IDs occur in four commits, always and only inside that note; no commit carries a 15-ID matrix.

So the note's 15/8 is not a description of any artifact that was ever committed, the landed matrix is the *smaller* one, and no landed file explains the reduction. That is the freeze-order defect: the escape denominator moved from 8 to 6 between the authoring note and the bytes, in the window where the fixed resolver already existed.

The checker is also not the one the note describes. `CountMirror.md` claims JSON-Lines output, "missing/duplicate/unexpected citations" checking, and "bounds … for matrix size, case/setup counts, path lengths":

```text
$ grep -n "distinct\|duplicate\|unexpected\|MAX_\|bound\|len(matrix" corpus/instruments/mirror-containment-check.py
NONE FOUND
```

The landed checker compares only `classes.get(case["cite"], "NO-ROW") == case["expect"]`, with a schema/cases check. It cannot detect duplicates, it never asserts anything about the class *distribution*, and it has no size bounds. That gap is what makes the next two findings possible.

---

## 3. Falsifiable finding: the landed matrix pins **zero** expansion cases, and the landed expansion behaviour contradicts its own build note

```text
$ python3 -c "import json;d=json.load(open('corpus/instruments/mirror-containment-fixtures.json'));print(sum(1 for c in d['cases'] if any(ch in c['cite'] for ch in '*?[{}<>')), 'of', len(d['cases']))"
0 of 13
```

Every landed cite is a literal path: 2 parent-traversals, 1 relative-mirror `../`, 2 symlinks, 1 prefix sibling, 7 controls. No brace, glob, or `<placeholder>` citation exists — yet brace/glob/placeholder expansion is exactly where `resolve.py` changed (`exists_any()` → `under_mirror()` on the *first sorted* candidate).

Reconstructing the build note's own shapes in scratch (`fixtures-probe.json` = landed 13 + 4), against unmodified landed bytes `ed9a9dae` and again against the earlier §1.1 bytes `9e0b5751`:

```text
$ python3 mirror-containment-check.py --fixtures fixtures-probe.json     # resolver ed9a9dae (receipted)
glob-confined-alongside-escaping-sibling   control expect=MIRROR-EQUIVALENT actual=GONE FAIL
placeholder-escaped-only                   escape  expect=GONE             actual=GONE PASS
brace-confined-alongside-escaping-sibling  control expect=MIRROR-EQUIVALENT actual=GONE FAIL
empty-citation-produces-no-row             control expect=NO-ROW           actual=NO-ROW FAIL problems=cli-exit-1
cases=17 escape=7 controls=10 pass=14 fail=3

$ python3 mirror-containment-check.py --resolver resolve-cur.py --fixtures fixtures-probe.json   # resolver 9e0b5751 (worktree)
glob-confined-alongside-escaping-sibling   control expect=MIRROR-EQUIVALENT actual=GONE FAIL
placeholder-escaped-only                   escape  expect=GONE             actual=GONE PASS
brace-confined-alongside-escaping-sibling  control expect=MIRROR-EQUIVALENT actual=GONE FAIL
empty-citation-produces-no-row             control expect=NO-ROW           actual=NO-ROW PASS
cases=17 escape=7 controls=10 pass=15 fail=2
```

The two expansion failures are identical on both byte versions, so they are not an artifact of the concurrent edit.

Expectations are not mine; they are the authoring seat's:

- `build/GlobEscape.md:10-11` — "**Expected under C1:** `MIRROR-EQUIVALENT`, with `resolved_path == <selected-mirror>/ops/z-confined.mjs` … the valid confined match must remain usable, while no outside target is credited." Compatibility invariant at `:17-18`: "Filter every glob candidate by realpath containment before selecting the first acceptable result."
- `build/BraceEscape.md:20` — "For bounty fallback, a real file under the selected mirror must remain `MIRROR-EQUIVALENT`."

Landed `classify()` takes `matches[0]` from `exists_any()`, tests `under_mirror()` on that one candidate, and on failure returns `GONE` for the whole citation — discarding the confined `z-confined.mjs` / `z-ok.mjs` that is present in the same directory. That is a false negative against the frozen claim's "Preserve valid confined mirror … controls" and against the note; and because the matrix has no expansion case, no landed figure can move when this behaviour is wrong.

`empty-citation-produces-no-row` is a second dropped case, and the two versions diverge here. On the receipted bytes `ed9a9dae` it cannot pass at all: with one isolated root per case, a lane whose only citation is empty yields zero rows and `main()` aborts on `max() arg is an empty sequence` (predicted in `build/EmptyCorpus.md`), recorded as `problems=cli-exit-1`. The note's workaround ("submitted beside non-empty citations") is unimplementable in an architecture that gives every case its own root. The `max(..., default=0)` edit in `9e0b5751` fixes the abort, and the case then passes — but no receipt covers those bytes, so the dropped case's status is unrecorded in either receipt set.

---

## 4. Control audit: no expected class is logically unfalsifiable, but **none of the seven can supply positive evidence**, and two are satisfied by a degenerate fix

Baseline receipt proves every control's expectation equals its pre-fix class (`c1-baseline.json`, all 7 `PASS`):

| control | expect | pre-fix (baseline) actual | = pre-fix? | failure mode it can still catch |
|---|---|---|---|---|
| `confined-bounty-fallback-control` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT | yes | over-confinement of the literal bounty fallback |
| `confined-relative-fallback-control` | MIRROR-EQUIVALENT | MIRROR-EQUIVALENT | yes | over-confinement of the relative fallback |
| `missing-bounty-target-control` | GONE | GONE | yes | harness/CLI malfunction only |
| `lane-relative-parent-internal-control` | INTERNAL | INTERNAL | yes | confinement wrongly applied to the lane branch |
| `literal-prefix-sibling-control` | RESOLVES | RESOLVES | yes | over-confinement of the literal carve-out |
| `canonical-alias-confined-control` | RESOLVES | RESOLVES | yes | over-confinement of the canonical branch |
| `canonical-alias-escape-control` | GONE | GONE | yes | regression of the pre-existing canonical gate only |

Strict verdict: **no case is unfalsifiable by construction** — each can fail, and I demonstrated the two mechanisms (a degenerate fix fails 5; an over-confining fix fails others). The honest defect is narrower and measurable:

1. **All seven expectations equal the pre-fix class**, so `7/7 controls preserved` is not independent evidence for C1 — it is a restatement of "no control moved". Controls can only detect over-correction.
2. **Two controls (`missing-bounty-target-control`, `canonical-alias-escape-control`) pin `GONE`, the same value as all six escapes.** A classifier that returns `GONE` for everything satisfies them:

```text
$ python3 mirror-containment-check.py --resolver degenerate-gone.py    # every cite → GONE
cases=13 escape=6 controls=7 pass=8 fail=5
# passes: 6 escapes + missing-bounty-target-control + canonical-alias-escape-control
```

So the anti-degeneracy guard is **5 cases, not 7**. `missing-bounty-target-control` is further entitled by construction: the fixture creates no file anywhere, so no confinement policy can move its class — it tests CLI liveness, not C1.
3. **The checker enforces no distribution invariant.** Nothing requires the matrix to contain any non-`GONE` expectation or any expansion case. A matrix of thirteen `GONE` pins would print `13/13, exit 0` — which is precisely the shape the 8→6 escape reduction was moving toward, and why finding §3 matters.

---

## 5. Smallest safe correction

1. **Bind the matrix before the code.** Add `matrix_sha256` (and the 13 IDs) to `claims.json`/the wave spec, dated at freeze time; for this wave, add a one-line addendum stating that the 13-case matrix's inode (03:28:11) postdates the fixed bytes (03:27:44) and that no pre-registration exists. Do not claim the matrix predates the fix.
2. **Reconcile `build/CountMirror.md:30-47` with the landed matrix.** Either land the four named cases, or mark the 15-ID/8-escape description as the unarchived private-clone draft and state that the escape denominator is 6. Today a reader of the note will believe glob/placeholder/brace pins exist; they do not.
3. **Pin the expansion branch one way or the other.** Add the two `confined-alongside-escaping-sibling` cases with `expect: MIRROR-EQUIVALENT` (matching `GlobEscape.md`/`BraceEscape.md`), which turns the current `GONE` into a visible failure and forces the candidate-filtering fix; or add them with `expect: GONE` and record that discarding a valid confined match is accepted C1 behaviour. Leave it unpinned and the 6/6 figure cannot move.
4. **Re-cut `c1-fixed.json` against the current tree, or say why not.** `c1-fixed.json` names resolver `ed9a9dae`; the worktree is `9e0b5751` (§1.1). Either regenerate the fixed receipt so the receipt pair again binds the bytes under review, or record that the 03:40:40 edit is outside the C1 receipt set.
5. **Add the distribution invariant** to `main()`: refuse a matrix with no `MIRROR-EQUIVALENT`/`RESOLVES` expectation. Optionally implement the distinct/duplicate/bounds checks the note already advertises, or delete that sentence from the note.

---

## 6. Scope limits

- Only `/tmp` scratch with copied bytes; the live detector was not run against the corpus, and I make no claim about production `mirror=` counts or score movement.
- Byte anchors: replays in §1–§4 ran against `resolve.py` `ed9a9dae` (receipted at 03:28:32, committed at `953c278`); §1.1/§3 additionally replay `9e0b5751` (the worktree after a sibling's 03:40:40 edit). I wrote only this report; `resolve.py`, `LOG.md`, the three F06–F08 knowledge entries, `manifest.json` and the sibling falsify reports changed during the review under other seats.
- The probe expectations come from the 10-20 build notes (`GlobEscape.md`, `BraceEscape.md`), not from frozen C1 text; C1's "preserve valid confined mirror controls" is the claim-level hook, but it does not explicitly say "expansion controls". I report the behaviour as unpinned and note-contradicting, not as a C1 violation on its own.
- Pattern citations such as `~/Projects/bounties/ops/*.mjs` are synthetic (the resolver flags them `noise=synthetic`); whether the corpus ever contains such a citation is a separate question the guard run does not answer (`mirror=0`, vacuous).
- I did not inspect C2 artifacts, did not run the fleet repo, and did not read any tool beyond local ones. No installs, no network.
- The 5-day authoring gap between the build notes (10-20) and the matrix (10-25) rests on on-disk mtimes plus the git author date of `8bf9807` (2026-10-20T18:30:56). A checkout/export can rewrite mtimes; the git date corroborates but does not independently date the private-clone matrix the note describes.
