# BaselineFalsify — is the C1 baseline a real fail-before, and which cases carry it?

Seat: `L1Kasegi23.BaselineFalsify-2` (critic, leaf, no dispatch). Round-23 FALSIFY only.
Read-only against the repo: the only repo write is this file. All scratch work is in
`/tmp/kasegi-r23-falsify-baseline/`. No commit, push, index/jj touch, admission or score claim.
Tooling record: **no installs or updates** (stock `python3` 3.14.8, `sha256sum`, `diff`, `git` plumbing).

---

## 0. Answer in one paragraph

The fail-before relation is **real in every generation of the package I could measure**: the
baseline resolver fails exactly the escape cases and nothing else, and every one of those failures
is turned into a PASS by the fixed bytes, with **no PASS→FAIL regression and no control moving**.
But two of the three assigned verifications hold only *inside* a generation: the `matrix_sha256`
is identical across the two receipts **of one generation** and differs between generations, because
the fixtures, the checker and the resolver were all rewritten *during this falsify wave* — the
13-case pair committed at `953c278`, a 17-case pair generated `06:43:07Z`, and the 20-case pair now
at `4d9231e` generated `06:46:26Z`. In the current matrix **one declared escape case,
`glob-expansion-escape`, is not discriminating at all**: the baseline already reports `GONE`, and it
does so for a vacuously true reason (no glob match exists on either side), so the case cannot fail
before the fix and cannot detect a regression of it.

---

## 1. The artifacts moved under the measurement

`sha256` of the file as it sits in each revision (all reproduced with `sha256sum` and `git show`):

| generation | resolve.py | checker | fixtures | cases | receipt `generated_at` |
|---|---|---|---|---|---|
| **A** `953c278` (committed) | `ed9a9dae…` | `1bc2db10…` | `5e61a33e…` | 13 | *(no field)* |
| **B** worktree `03:43:07` | `8dd45bc8…` | `53742c8d…` | `5c64e014…` | 17 | `2026-10-25T06:43:07Z` |
| **C** `4d9231e` (HEAD now) | `fce5b84b…` | `53742c8d…` | `4e39f65c…` | 20 | `2026-10-25T06:46:26Z` |

The baseline resolver never moved: `sha256 d6a3c3f1a1d8e97d42d66a8aa3cb34530b7bc1c18b194e487ef8d580d869f903`
in all three generations, and it is **byte-identical to the pre-fix detector**:

```
git rev-parse 922a4dd:.ufo/waves/round-23/c1-baseline-resolver.py 2>/dev/null   # absent at 922a4dd
git rev-parse 922a4dd:corpus/instruments/resolve.py            → 2b1e2528a064f918c5e82c03e109a456e1e72589
git rev-parse HEAD:.ufo/waves/round-23/c1-baseline-resolver.py → 2b1e2528a064f918c5e82c03e109a456e1e72589
```
(the same blob id at `8bf9807` and `953c278`). So the "do-nothing control" is genuine pre-fix
bytes, not a strawman — this is the one part of the C1 package that cannot have been tuned.

Drift observed while measuring, with wall clock:

- `03:43:07` receipts B written (17 cases, matrix `5c64e014`).
- `03:43:38` fixtures rewritten to 20 cases (`4e39f65c`) — **receipt B's matrix identity was
  already stale 31 seconds after it was generated**; no case was added or removed from B, three
  were appended.
- `03:44:59` → `03:46:26` `resolve.py` changed `8dd45bc8` → `fce5b84b`, reverting the root-only
  bounty mirror probe (`if suffix else mirror_root` → `(None, None)` at `resolve.py:243`), then
  was committed with receipts C.
- `03:46:46` HEAD advanced again to `4d9231e`.

**Consequence for the report's own status:** every "frozen" number below is pinned to a `sha256`,
not to a path. A later reader who re-runs `corpus/instruments/mirror-containment-check.py` today
gets generation C; if the wave moves again, C is stale too.

Commands (representative, all reproduced):

```
python3 corpus/instruments/mirror-containment-check.py \
    --resolver /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-23/c1-baseline-resolver.py \
    --json /tmp/kasegi-r23-falsify-baseline/gen3-baseline.json
python3 corpus/instruments/mirror-containment-check.py \
    --json /tmp/kasegi-r23-falsify-baseline/gen3-fixed.json
```

---

## 2. Fail-before, per generation

### Generation A (`953c278`, 13 cases, matrix `5e61a3`)

Replayed from git objects (`git show HEAD_at_953c278:<path>` → `/tmp/.../head/`), so the run cannot
be contaminated by later edits:

```
../head/check.py --resolver c1-baseline-resolver.py --fixtures head/fixtures.json
  cases=13 escape=6 controls=7 pass=7  fail=6  resolver=d6a3c3f1… matrix=5e61a33e…
../head/check.py --resolver head/resolve.py          --fixtures head/fixtures.json
  cases=13 escape=6 controls=7 pass=13 fail=0  resolver=ed9a9dae…  matrix=5e61a33e…
```

- baseline fail set = `{bounty-parent-traversal, bounty-parent-traversal-vault,
  relative-mirror-fallback-escape, bounty-fallback-symlink-escape,
  relative-fallback-symlink-escape, bounty-prefix-sibling-confusion}`
- **fixed-flip set = the same six ids** (set equality, not just equal cardinality)
- PASS→FAIL regressions: **none**; controls differing: **none**
- my replay of these bytes at `03:38` (worktree then == `953c278`) is field-for-field identical to
  the committed pair: `norm(replay) == norm(c1-*.json)` → `True`.

### Generation B (`06:43:07Z`, 17 cases, matrix `5c64e014`)

Replayed at `03:43:44` against a pinned snapshot `snap-0343/` (`53742c8d` / `5c64e014` / `8dd45bc8`):

```
cases=17 escape=7 controls=10 pass=10 fail=7   (baseline d6a3c3f1, matrix 5c64e014)
cases=17 escape=7 controls=10 pass=17 fail=0   (fixed    8dd45bc8, matrix 5c64e014)
```
Both receipts reproduce **exactly**, field for field, differing only in `generated_at`
(`norm(a)==norm(b)` → `True`). Fail set == flip set (7 ids); no control differs.

### Generation C (`4d9231e`, 20 cases, matrix `4e39f65c`) — current

```
cases=20 escape=9 controls=11 pass=12 fail=8   (baseline d6a3c3f1, matrix 4e39f65c)
cases=20 escape=9 controls=11 pass=20 fail=0   (fixed    fce5b84b, matrix 4e39f65c)
```
Both receipts reproduce exactly except `generated_at`. Fail-before set (8):

```
bounty-parent-traversal, bounty-parent-traversal-vault, relative-mirror-fallback-escape,
bounty-fallback-symlink-escape, relative-fallback-symlink-escape, bounty-prefix-sibling-confusion,
absolute-prefix-sibling-confusion, brace-expansion-escape
```
Fixed-flip set = the same eight. PASS→FAIL regressions: **none**. Controls differing in class or
status: **none**.

Note the asymmetry that the headline `9 escape / 9 detected` hides: 9 escape cases are declared,
but only **8** fail on the baseline. See §5.3.

---

## 3. `matrix_sha256` identity

| pair | baseline receipt | fixed receipt | identical |
|---|---|---|---|
| A (`953c278`) | `5e61a33ed5fa…` | `5e61a33ed5fa…` | **yes** |
| B (`06:43:07Z`) | `5c64e0149f66…` | `5c64e0149f66…` | **yes** |
| C (`4d9231e`) | `4e39f65c7c1b…` | `4e39f65c7c1b…` | **yes** |

And independently: `sha256sum corpus/instruments/mirror-containment-fixtures.json` equals the
`matrix_sha256` printed by the run, in every generation — the field is a real digest of the matrix
bytes, not a constant. Across generations the value *must* differ; a reader who compares receipt A
to receipt C and calls it a mismatch would be measuring the wave's edits, not a defect in either
receipt.

---

## 4. "No control case is credited differently" — true, with one caveat

Class and resolved path are identical for **all 11** current controls (and all 7 in A, all 10 in B):
I re-ran every case through the real CLI for both resolvers and compared the full TSV rows
(`citation, class, resolved_path, method, domain`), normalising only the case root:

```
case                                         class+path identical   domain identical
confined-bounty-fallback-control                     yes                  yes
confined-relative-fallback-control                   yes                  yes
missing-bounty-target-control                        yes                  yes
lane-relative-parent-internal-control                yes                  yes
literal-prefix-sibling-control                       yes                  NO  (bounty → other)
canonical-alias-confined-control                     yes                  yes
canonical-alias-escape-control                       yes                  yes
bounty-literal-present-traversal                     yes                  yes
bounty-literal-symlink-present                       yes                  yes
absolute-bounty-fallback-control                     yes                  yes
brace-expansion-confined-control                     yes                  yes
```

`literal-prefix-sibling-control` (`~/Projects/bounties-legacy/README.md:1`) is `RESOLVES` on
`home/Projects/bounties-legacy/README.md` in **both** runs, but pre-fix it reached that answer
*through the bounty domain* (`base.startswith(BOUNTY_PREFIXES)` true, mirror probe misses, GONE→ no,
literal hit first) and post-fix it is routed through domain `other` because `bounty_suffix()`
returns `None`. Class and path are stable; the route is not.

This matters for verifiability because **the receipt does not record `method` or `domain`**
(`mirror-containment-check.py` compares only `class` and `resolved_path`, `path_verdict` at
`:140–160`, PASS at `:221`). A receipt-only check therefore *cannot* see a control being re-routed,
and the exact-root half of C1 is precisely a routing change. The claim "no control is credited
differently" is true as written only if "credited" means the two columns the receipt keeps.

---

## 5. Non-discriminating cases

### 5.1 All controls are non-discriminating for fail-before — by construction, and only that

Every control has the same class in both runs in every generation, so none of them can witness the
defect. Which controls can ever move was measured with six scratch variants of the detector
(base `ed9a9dae`, 13-case matrix `5e61a3`, all in `/tmp/kasegi-r23-falsify-baseline/`):

| variant (one hunk changed) | sha256 | multi-case FAIL set |
|---|---|---|
| V1 `bounty_suffix` prefix semantics | `203c2977…` | **`bounty-prefix-sibling-confusion`** |
| V2 both containment guards removed | `c73dc622…` | 5 escapes except the prefix case |
| V3 `under_mirror` lexical (`normpath`, no `realpath`) | `47b9757e…` | the 2 symlink escapes |
| V4 bounty-branch guard only | `7fed2c1a…` | the 2 relative escapes |
| V5 `under_mirror` → `False` | `afa4071f…` | 3 controls: confined-bounty, confined-relative, canonical-alias-confined |
| V6 `bounty_suffix` → `base` (unbounded) | `be4d02a4…` | 2 controls: lane-relative-parent-internal, canonical-alias-confined |

Reading: **V1–V4 (all under-enforcement defects, i.e. the direction C1 is about) move zero
controls.** The control set is load-bearing only against over-rejection (V5) and against a grossly
unbounded boundary (V6). "The controls survived" is therefore not evidence that the fix is
confined; it is evidence that the fix did not over-reject. V2 and V4 reproduce the mutants already
published by `L1Kasegi23.MutateBountyConfine-2` / `MutateRelConfine-2` (`pass=8 fail=5`, disjoint
sets) — I am not re-claiming those.

### 5.2 `bounty-parent-traversal-vault` is dominated by `bounty-parent-traversal`

Same domain (`bounty`), same expression (`exists_any(join(mirror_root, suffix))` at
`resolve.py:243`), same predicate (`under_mirror`), same flipped verdict in **all seven** resolver
generations I ran (baseline, V1–V6, fixed): the two differ only in the target filename and depth
(`../outside.md` vs `../outside-vault/secret.mjs`). No containment policy among realpath, lexical,
`..`-shaped or no-guard separates them; only a filename-specific rule could, and that is not a
plausible sound fix. It is a duplicate probe: the matrix carries 9 escape cases but at most 8
independent escape mechanisms, and in generation A 6 cases covered 5 mechanisms plus the boundary.

### 5.3 `glob-expansion-escape` is an escape case the baseline already passes — and it is vacuous

Current matrix, `mirror-containment-fixtures.json:210`:

```json
{"id": "glob-expansion-escape", "nature": "escape",
 "cite": "~/Projects/bounties/<name>.md:1",
 "dirs": ["relocated/outside-vault"],
 "files": {"relocated/outside-vault/x.md": "glob match outside the mirror\n"},
 "expect": "GONE"}
```

Baseline **PASS** (`GONE`), fixed **PASS** (`GONE`) — no discrimination. The reason is not
confinement; it is that no match is reachable on either side. Built with the checker's own
`build_case`, the case tree contains:

```
home/Projects/            (empty)          → glob(~/Projects/bounties/*.md) → []
relocated/tbh/            (empty)          → glob(<mirror>/*.md)           → []
relocated/outside-vault/  ['x.md']         ← unreachable from either root
```

`<name>` is rewritten to `*` **inside one path segment** (`PLACEHOLDER.sub("*", p)` in
`exists_any`), so `<mirror>/*.md` cannot reach `relocated/outside-vault/x.md`; the case's own note
(“matches only outside the mirror through a relative hop”) describes a hop the citation does not
contain. The pinned `GONE` is therefore a zero-match `GONE`, identical before and after the fix.

Minimal correction, tested: give the glob a reachable out-of-mirror match.
`fixtures-glob-reachable.json` (sha256 `236048a7…`) adds
`symlinks: {"relocated/tbh/x.md": "@ROOT@/secret/x.md"}` and `files: {"secret/x.md": …}`; then

```
baseline: glob-expansion-escape  expect=GONE  actual=MIRROR-EQUIVALENT  FAIL
fixed:    glob-expansion-escape  expect=GONE  actual=GONE              PASS
```
i.e. the case becomes a genuine pre-fix escape credit and the fix kills it. As frozen, it inflates
the escape count and cannot detect a regression.

### 5.4 The exact-root boundary had exactly one pin in generation A

V1 (boundary reverted, containment intact) fails **one** case in the 13-case matrix:
`bounty-prefix-sibling-confusion`; all five containment cases stay GONE because the decoy is
*inside* the mirror (verified: baseline's credited path for that case is
`relocated/tbh/-legacy/README.md`, realpath inside the mirror, so no containment test can reject
it). Dropping that single case would leave the exact-root half of C1 unpinned while the suite still
reported green. Rebuilt on the current base, V1b (`62f34c08…`) fails two cases —
`bounty-prefix-sibling-confusion` **and** `absolute-prefix-sibling-confusion` — so generation C
closed that single-pin by adding the absolute-spelling twin. This is the one coverage gap I
observed that the wave itself fixed.

---

## 6. Findings (falsifiable)

1. **Fail-before holds, exactly.** In every generation the baseline's FAIL set equals the fixed
   run's PASS set restricted to that FAIL set: A 6/6, B 7/7, C 8/8; zero PASS→FAIL regressions;
   zero controls differing in class or status. Falsifier: any case where the baseline is `GONE` and
   the fixed bytes are not, or vice versa, outside the escape set.
2. **The baseline is genuine pre-fix bytes**, blob `2b1e2528…` at `922a4dd`/`8bf9807`/`953c278`,
   file sha `d6a3c3f1…` — identical to the blob, so no thinning.
3. **The receipts are not frozen during the wave.** Three generations exist; generation B's
   `matrix_sha256` was stale 31 s after it was written; only generation C matches the tree at
   `03:46:46`, and it too is one edit away from being stale. `matrix_sha256` is identical within a
   pair and necessarily different across pairs. Falsifier: a receipt whose `matrix_sha256` equals
   the on-disk fixtures *and* an earlier receipt at the same path with a different count.
4. **`glob-expansion-escape` is non-discriminating and vacuous**: baseline `GONE` before the fix,
   because both glob roots are empty (`relocated/tbh/` empty, `home/Projects/bounties` absent).
   It is declared `escape` but proves nothing about confinement. Falsifier: exhibit a match either
   side reaches with the frozen fixture bytes.
5. **All controls are non-discriminating for fail-before, and only load-bearing against
   over-rejection.** Under-enforcement mutations (V1–V4) move no control; over-rejection (V5) moves
   three; an unbounded boundary (V6) moves two.
6. **One control changes route while keeping its class**: `literal-prefix-sibling-control` is
   `RESOLVES` on the same path in both runs but moves from domain `bounty` to `other`, and the
   receipt schema records neither `method` nor `domain`, so the receipts cannot show it.
7. **`bounty-parent-traversal-vault` is a duplicate probe** of `bounty-parent-traversal`
   (same branch, same predicate, same verdict across seven resolver variants).

---

## 7. Scope limits

- Classification only. Nothing here establishes source availability, corpus attribution, C2
  (F06–F08) coverage, or any score movement; no admission claimed, no lane edit performed.
- The variant map (§5.1) is built on generation A's bytes and matrix; on generation C I only ran
  V1b (boundary) and the glob-reachability probe. Mutation durability across the 20-case matrix is
  the mutation seats' lane, not mine — V2/V4 there are reproduced, not originated.
- The newest fixtures introduced `path_check` / `path_tolerance` (checker `:140–222`), so a PASS in
  generation C means "class matches **and** the recorded path corroborates it, or the case declares
  a carve-out". Generation A receipts have no such field, so A and C are not directly comparable
  field-for-field even at the same case id.
- `absolute-bounty-fallback-control` and `absolute-prefix-sibling-confusion` are host-dependent by
  design; both preconditions hold on this host (`/home/vgpnk/Projects/bounties/ops/rank.mjs`,
  `/home/vgpnk/Projects/bounties-legacy/README.md` and `/home/vgpnk/Projects/outside.md` absent).
- Not in my lane: the resolver's root-only-bounty behaviour changed between `8dd45bc8` and
  `fce5b84b` (mirror-root probe removed) with no matrix case covering it; I flag it as observed
  churn only.
- Scratch `/tmp/kasegi-r23-falsify-baseline/` holds: `head/` (generation A objects), `snap-0343/`,
  `snap-0344/`, `head-*.json`, `snap-*.json`, `gen3-*.json`, `v1…v6`, `v1b`, `fixtures-glob-reachable.json`.
