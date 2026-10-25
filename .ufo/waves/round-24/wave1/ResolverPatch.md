# ResolverPatch — r24 minimal `resolve.py` dispatch fix (private clone)

Seat: `L1Kasegi24.ResolverPatch` (executor, leaf). Private clone
`/tmp/kasegi-r24-ResolverPatch`, `git clone --no-hardlinks` of the lane.

State pinned before any edit:

```
clone HEAD                          c2480b143120364728b40397926ffcf30a7309c8   (= master tip; parent d0a3f6a)
lane master                         c2480b143120364728b40397926ffcf30a7309c8
git diff --stat d0a3f6a..HEAD       corpus/lessons/round-23-verifier-spotcheck.md | 142 +
resolve.py at clone HEAD sha256     690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
.ufo/waves/round-24/c1-baseline-…   690153ad…  (identical bytes: the patch base is the frozen baseline)
patched clone resolve.py sha256     3979fad15edc2e23a9f06ff64801dac686e71cb6dca04a50fc38b21881b73ce7
```

Only `/tmp/kasegi-r24-ResolverPatch/corpus/instruments/resolve.py` was edited. Nothing was
written inside the lane except this report. No commit, no jj, no push, no subagent dispatch,
no installs (no tool was needed). Generated `citation-survival.tsv/.md` produced by the CLI runs
were restored in the clone, so its working-tree diff is the resolver hunk alone
(`git status --short` → ` M corpus/instruments/resolve.py`).

---

## 1. Findings

**F1 — The two-hunk fix takes the committed C1 counter-B instrument from 4/8 exit 1 to 8/8 exit 0.**
`corpus/instruments/resolve-dispatch-check.py` (landed by the LivenessMatrix seat at 04:16:24,
checker sha256 `88090efca9860a83677f7118813f0e34e945b09aaaf2dc8a584464b7b2b47b69`, matrix
`5133e98e656f07d2454f1f4799d4b0b5e5ab260ea69b1fd9d1cade3e0f9628b6`) was run three times with
`--resolver` pointed at each byte set. Baseline → `cases=8 pass=4 exit=1`; patched → `cases=8
pass=8 exit=0`. The four baseline failures are exactly the four liveness cases, each for the
stated reason:
`lane-brace-empty-first-alternative` GONE, `lane-brace-empty-second-alternative` GONE,
`bounty-brace-empty-alternative-mirror-fallback` GONE, and `glob-dangling-first-match` INTERNAL
with `path=<CASE>/lane/refs/a-lure.md path_check=path-missing-on-disk`. Evidence: §3 A/B.

**F2 — No corpus regression: the census is byte-identical on class and path.**
`python3 corpus/instruments/resolve.py <clone root>` before and after the patch:

```
before  distinct=1669 resolves=14 mirror=0 internal=218 other=0 gone=1437 skill=40/513 corpus=217/1344 all=232/1669
after   distinct=1669 resolves=14 mirror=0 internal=218 other=0 gone=1437 skill=40/513 corpus=217/1344 all=232/1669
```

`cmp` of the two `citation-survival.tsv` files → identical, so the per-citation `(class,
resolved_path)` map is unchanged for all 1669 cites; a parsed row diff reports
`class_changed: [] path_changed: []`. The only diff in `citation-survival.md` is the *line-count
column* of the four `corpus/instruments/resolve.py:…` self-citations, `598 → 604` (the patched file
is 6 lines longer); their class, path and `in range` verdict are unchanged. So the instrument
change is provably content-neutral on this corpus, and the round-over-round census delta stays
attributable to content, not to the detector.

**F3 — Round-23 containment matrix holds: 24/24 exit 0 on both byte sets.**
`python3 corpus/instruments/mirror-containment-check.py` in the clone (committed checker
`dddd55496b55eb49138613e3b7143834412cdb104b7f8f6b6e85210f3dd98f8a`, matrix
`d05b1e0cf62738ac8bf06497334c16a392089a5792ca9fd930f0cbf73e69b809` — both byte-identical to the
lane's copies): baseline bytes `pass=24 fail=0 exit 0` (`resolver_sha256=690153ad…`), patched bytes
`pass=24 fail=0 exit 0` (`resolver_sha256=3979fad1…`). Escape and control halves both 12/12; no
containment, precedence or confinement case moves.

**F4 — The lane working tree is ALREADY patched by another seat, and LivenessMatrix.md's byte claim
is stale-false.** `corpus/instruments/resolve.py` in the lane has mtime `04:14:32` and sha256
`035f8844e66357f6dbe6f1158776978f2ce1103108e222d0746afdef9521b661`, i.e. it is **not** `690153ad…`.
`wave1/LivenessMatrix.md` states "production `resolve.py` was not touched (its bytes stay
`690153ad…`)"; that was already false when the report was written (04:18). The lane's applied
change is the same two hunks in a different shape (`sorted(set(out))[:64]` dedupe, comments citing
fixture names `L1/L2/L4` that no longer exist in the landed fixtures, and no bare-`{}` guard).
It scores `cases=8 pass=8 exit=0` and `24/24 exit 0` as well. My clone patch is therefore
**redundant against the lane working tree**; L1 must decide which byte set stands rather than
applying mine on top. I did not touch the lane copy.

**F5 — The two implementations differ in exactly one outcome, and it is the bare `{}` placeholder.**
Running the lane bytes on the same clone root (`/tmp/lanecheck/resolve.py`, output in
`/tmp/lanecheck/citation-survival.tsv`) gives
`distinct=1669 resolves=14 mirror=0 internal=219 other=0 gone=1436 skill=40/513 corpus=218/1344 all=233/1669`
— one row more than baseline, and the differing row is the single token `{}`:

```
('{}', mine=('GONE', ''), lane=('INTERNAL', '/tmp/kasegi-r24-ResolverPatch/'))
```

That is a false positive: `{}` is a template placeholder (`noise_flags` already tags it
`synthetic`), and crediting it as INTERNAL makes the *lane root directory* a resolved citation,
inflating `internal`/`all` by one for a reason unrelated to dispatch liveness. My patch keeps the
pre-r24 non-expansion for a group with no comma (`{}` → no candidates) while keeping the literal
empty alternative inside a real alternative set (`{,x}`, `{x,}`, `{,}`) — the exact defect in the
claim. Unit evidence §3-D. **Recommendation: keep the guard**; it makes the round's census diff
empty (F2) so the C1 instrument change cannot move the coverage numbers by itself.

**F6 — The bound, determinism and sort order are preserved; the change is inert outside the defect.**
`brace_expand` still returns `sorted(...)[:64]` with the same `len(out) > 64` early break; two
consecutive patched CLI runs over unchanged bytes produce a byte-identical TSV. A 400-case
randomised differential against the frozen baseline bytes (1–3 brace groups per path, 2–4
non-empty alternatives sampled from a fixed alphabet, **no** empty alternatives) reports
`diffs=0`. Explicit unit table (§3-D): `{}` → `[]` (unchanged), `x{}y` → `[]` (unchanged),
`{ ,x}/y` → `['x/y']` (unchanged), `{a,}{b,}` → `['', 'a', 'ab', 'b']` (previously `['ab']`).

**F7 — The scratch probe and the committed check agree, so no second instrument is needed.**
Before `resolve-dispatch-check.py` existed I materialised the same eight frozen cases myself
(`/tmp/kasegi-r24-probe/resolve-dispatch-probe.py`, scratch, **not** in the clone or the lane). Its
verdict set is identical to the committed checker's on both byte sets (4/8 baseline, 8/8 patched,
same case ids, same classes, same `path_check` reasons), which is a cross-check on the landed
instrument rather than a competing one. Its only extra assertions are the `path_verdict` reuse and
per-case isolation; it should not be promoted while `resolve-dispatch-check.py` is in the tree.

**F8 — Claims.json `before_expected: 4/8` is correct against the landed fixtures; LivenessMatrix.md
F1's "baseline measures 5/8" does not reproduce.** With the landed fixtures (matrix sha256
`5133e98e…`) the frozen baseline scores 4/8, not 5/8, on both the committed checker and my
independent probe. LivenessMatrix.md's L4 was evidently a different case shape (a brace whose live
alternative is second) than case 4 of the landed matrix
(`bounty-brace-empty-alternative-mirror-fallback`, which fails on baseline with GONE). No claim
correction is needed; the counter as frozen reproduces.

---

## 2. Patch (exact, `git diff -U3 -- corpus/instruments/resolve.py` in the clone)

```diff
diff --git i/corpus/instruments/resolve.py w/corpus/instruments/resolve.py
index c92f0fa..abcc401 100755
--- i/corpus/instruments/resolve.py
+++ w/corpus/instruments/resolve.py
@@ -1,5 +1,5 @@
 #!/usr/bin/env python3
-"""kasegi r15 live citation-resolvability census; r18 self-input/leading-dot fixes; r23 mirror-fallback confinement.
+"""kasegi r15 live citation-resolvability census; r18 self-input/leading-dot fixes; r23 mirror-fallback confinement; r24 brace/glob dispatch liveness.
 
 Usage: python3 resolve.py <root-of-lane-repo>
 
@@ -171,10 +171,14 @@ def brace_expand(path):
     if not m:
         return [path]
     out = []
-    for alt in sorted(m.group(1).split(",")):
-        if not alt.strip():
-            continue          # `{}` / `{,x}` empty alternative is not a resolvable expansion
-        out.extend(brace_expand(path[: m.start()] + alt + path[m.end():]))
+    alts = sorted(m.group(1).split(","))
+    for alt in alts:
+        # r24: inside a real alternative set the empty alternative is a literal
+        # expansion (`{,sub}` -> the group disappears); dropping it made every
+        # citation whose only on-disk member is that expansion GONE. A bare `{}`
+        # is a placeholder, not a set, and still expands to nothing.
+        if alt.strip() or (not alt and len(alts) > 1):
+            out.extend(brace_expand(path[: m.start()] + alt + path[m.end():]))
         if len(out) > 64:
             break
     return sorted(out)[:64]
@@ -191,9 +195,11 @@ def exists_any(path):
             return "brace", c
     q = PLACEHOLDER.sub("*", p)
     if any(ch in q for ch in GLOBMETA):
-        matches = sorted(globmod.glob(q, recursive=True))
-        if matches:
-            return "glob", matches[0]
+        # r24: credit the first match that EXISTS. sorted(glob)[0] may be a
+        # dangling symlink, which produced a resolved_path no re-check corroborates.
+        for c in sorted(globmod.glob(q, recursive=True)):
+            if os.path.exists(c):
+                return "glob", c
     return None, None
 
```

Two behaviour changes only: the empty alternative of a multi-alternative brace set is a real
expansion, and the glob branch returns the first *existing* sorted match. No new verdict class, no
containment change, no change to `under_mirror`, `mirror_suffix`, `bounty_suffix`, `classify`,
`collect`, `noise_flags` or the report writer. The docstring hunk only extends the existing
round-list line and adds no new claim.

Reconciliation with the lane's applied `035f8844…`: taking mine drops `sorted(set(out))` (duplicate
candidates are idempotent for `exists_any`; the only visible effect is `{,}` returning `['', '']`
instead of `['']`) and adds the bare-`{}` guard. If L1 prefers the lane's byte set, the only change
needed to reach parity on F5 is the three-line `alts`/`if alt.strip() or (not alt and len(alts) > 1)`
guard in `brace_expand`.

---

## 3. Commands and outputs (verbatim)

### A. Counter B, frozen baseline bytes (exit 1)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/resolve-dispatch-check.py \
    --resolver .ufo/waves/round-24/c1-baseline-resolver.py \
    --fixtures corpus/instruments/resolve-dispatch-fixtures.json --json /tmp/dispatch-before.json
resolver_sha256=690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d
matrix_sha256=5133e98e656f07d2454f1f4799d4b0b5e5ab260ea69b1fd9d1cade3e0f9628b6
checker_sha256=88090efca9860a83677f7118813f0e34e945b09aaaf2dc8a584464b7b2b47b69
FAIL     lane-brace-empty-first-alternative                   expect=INTERNAL         actual=GONE             method=         path=- path_check=missing-path
FAIL     lane-brace-empty-second-alternative                  expect=INTERNAL         actual=GONE             method=         path=- path_check=missing-path
FAIL     glob-dangling-first-match                            expect=INTERNAL         actual=INTERNAL         method=glob     path=<CASE>/lane/refs/a-lure.md path_check=path-missing-on-disk
FAIL     bounty-brace-empty-alternative-mirror-fallback       expect=MIRROR-EQUIVALENT actual=GONE             method=         path=- path_check=missing-path
PASS     control-literal-hit                                  expect=INTERNAL         actual=INTERNAL         method=literal  path=<CASE>/lane/plain/present.md
PASS     control-absent-face                                  expect=GONE             actual=GONE             method=         path=-
PASS     control-glob-two-live-matches                        expect=INTERNAL         actual=INTERNAL         method=glob     path=<CASE>/lane/refs4/a-live.md
PASS     control-skill-brace-idiom                            expect=INTERNAL         actual=INTERNAL         method=brace    path=<CASE>/lane/ops/finalize-all.mjs
cases=8 pass=4 exit=1
$(echo $?) → 1
```

### B. Counter B, patched clone bytes (exit 0)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/resolve-dispatch-check.py \
    --resolver /tmp/kasegi-r24-ResolverPatch/corpus/instruments/resolve.py \
    --fixtures corpus/instruments/resolve-dispatch-fixtures.json --json /tmp/dispatch-after.json
resolver_sha256=3979fad15edc2e23a9f06ff64801dac686e71cb6dca04a50fc38b21881b73ce7
matrix_sha256=5133e98e656f07d2454f1f4799d4b0b5e5ab260ea69b1fd9d1cade3e0f9628b6
checker_sha256=88090efca9860a83677f7118813f0e34e945b09aaaf2dc8a584464b7b2b47b69
PASS     lane-brace-empty-first-alternative                   expect=INTERNAL         actual=INTERNAL         method=brace    path=<CASE>/lane/notes//a.md
PASS     lane-brace-empty-second-alternative                  expect=INTERNAL         actual=INTERNAL         method=brace    path=<CASE>/lane/notes//b.md
PASS     glob-dangling-first-match                            expect=INTERNAL         actual=INTERNAL         method=glob     path=<CASE>/lane/refs/z-live.md
PASS     bounty-brace-empty-alternative-mirror-fallback       expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT method=brace    path=<CASE>/relocated/tbh//rank.mjs
PASS     control-literal-hit                                  expect=INTERNAL         actual=INTERNAL         method=literal  path=<CASE>/lane/plain/present.md
PASS     control-absent-face                                  expect=GONE             actual=GONE             method=         path=-
PASS     control-glob-two-live-matches                        expect=INTERNAL         actual=INTERNAL         method=glob     path=<CASE>/lane/refs4/a-live.md
PASS     control-skill-brace-idiom                            expect=INTERNAL         actual=INTERNAL         method=brace    path=<CASE>/lane/ops/finalize-all.mjs
cases=8 pass=8 exit=0
$(echo $?) → 0
```

Lane working-tree bytes (`--resolver corpus/instruments/resolve.py`, sha `035f8844…`) → `cases=8
pass=8 exit=0` as well.

### C. Round-23 containment matrix (frozen), both byte sets

```
$ cd /tmp/kasegi-r24-ResolverPatch && python3 corpus/instruments/mirror-containment-check.py
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=690153ad… matrix_sha256=d05b1e0c…   exit=0   # baseline
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=3979fad1… matrix_sha256=d05b1e0c…   exit=0   # patched
$ python3 corpus/instruments/mirror-containment-check.py --resolver /tmp/lanecheck/resolve.py
cases=24 escape=12 controls=12 pass=24 fail=0 resolver_sha256=035f8844… matrix_sha256=d05b1e0c…   exit=0   # lane bytes
```

### D. CLI before/after on the clone root (class counts)

```
$ cd /tmp/kasegi-r24-ResolverPatch && python3 corpus/instruments/resolve.py .
before: distinct=1669 resolves=14 mirror=0 internal=218 other=0 gone=1437 skill=40/513 corpus=217/1344 all=232/1669
after : distinct=1669 resolves=14 mirror=0 internal=218 other=0 gone=1437 skill=40/513 corpus=217/1344 all=232/1669
both   exit 0; /tmp/before/citation-survival.tsv vs clone tsv → cmp clean (byte-identical)
       md diff = only `resolve.py:…` line-count column 598 → 604
       second patched run → same counts, tsv byte-identical (determinism held)
```

Per-citation row diff (`citation` → `(class, resolved_path)`), parsed from both TSVs:
`cites_equal: True`, `class_changed: []`, `path_changed: []`.

### E. Unit / differential on `brace_expand` (patched vs frozen baseline bytes, imported)

```
'notes/{,sub}/a.md'                    base=['notes/sub/a.md']                            new=['notes//a.md', 'notes/sub/a.md']
'notes/{sub,}/b.md'                    base=['notes/sub/b.md']                            new=['notes//b.md', 'notes/sub/b.md']
'ops/{import-board,finalize-all}.mjs'   base=[…] new=[…]                                  identical
'{}'                                   base=[]                                            new=[]
'x{}y'                                 base=[]                                            new=[]
'{,}'                                  base=[]                                            new=['', '']
'plain/path.md'                        base=['plain/path.md']                             new=['plain/path.md']
'a/{b,c}/{d,e}/f'                      base=['a/b/d/f','a/b/e/f','a/c/d/f','a/c/e/f']    new=same
'{ ,x}/y'                              base=['x/y']                                       new=['x/y']
'{a,}{b,}'                             base=['ab']                                        new=['', 'a', 'ab', 'b']
bounded len=64 <=64=True deterministic=True sorted=True
differential no-empty cases=400 diffs=0
```

### F. Scratch probe (independent cross-check, `/tmp/kasegi-r24-probe/resolve-dispatch-probe.py`)

```
baseline  cases=8 liveness=4 controls=4 pass=4 fail=4  exit=1
patched   cases=8 liveness=4 controls=4 pass=8 fail=0  exit=0
lane      cases=8 liveness=4 controls=4 pass=8 fail=0  exit=0
```

Verdicts identical to §3-A/B case for case (same ids, classes, `path_check` reasons).

---

## 4. Risks and notes for the integrator

1. **Two dirty candidates, one lane.** The lane already carries an uncommitted resolver fix
   (`035f8844…`, 04:14:32) written by a seat that also wrote `resolve-dispatch-check.py`
   (`??`), `resolve-dispatch-fixtures.json` (`??`) and `corpus/source-snapshots/round-24/` (`??`)
   into the lane. Decide the byte set before `git add`; do not apply my hunk blind on top of it.
2. **`{}` (F5).** If the lane bytes stand, `distinct` stays 1669 but `internal` becomes 219 and
   `all` 233 → 234/1669 for a placeholder token resolving to the lane root directory. That is a
   census inflation inside the round that moves the coverage axis. Keep the guard.
3. **`resolved_path` cosmetics.** Empty-alternative hits keep the doubled separator the citation
   wrote (`<CASE>/lane/notes//a.md`). POSIX collapses it, `os.path.exists`/`realpath` and the
   containment verdict are unaffected, and no lane corpus citation has an empty alternative, so the
   committed TSV is unchanged. Do not normalise in this round: `normpath` would also rewrite the
   `resolved_path` of existing literal citations and break the F2 zero-diff property.
4. **Generated census files.** Running the CLI rewrites `corpus/instruments/citation-survival.{tsv,md}`
   next to the script. After a lane run, the md will differ by the `resolve.py` line-count column
   alone (598 → 604); that is expected and not a content change.
5. **`{,}` duplicates.** Mine yields two equal `''` candidates where the lane's `sorted(set(...))`
   yields one. Idempotent for `exists_any`; only relevant if a future consumer counts candidates.
6. **UNVERIFIED:** who wrote the lane's `035f8844…` bytes. I can only pin bytes, mtime and the
   divergence from every seat's declared scratch path (`/tmp/r24-ref/resolve.py` is `1bb89770…`,
   which differs from the lane bytes by the dedupe and the comment text). No shell history, git
   reflog or jj op log was read to attribute it.
7. **No install, no package-manager command, no network fetch** was performed by this seat.
