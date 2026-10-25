# BaselineFalsify — is the C1 baseline a real fail-before, and which cases carry it?

Seat: `L1Kasegi23.BaselineFalsify-2` (critic, leaf, no dispatch). Round-23 FALSIFY only.
Read-only against the repo: the only repo write is this file. All scratch work is in
`/tmp/kasegi-r23-falsify-baseline/`. No commit, push, index/jj touch, admission or score claim.
Tooling record: **no installs or updates** (stock `python3` 3.14.8, `sha256sum`, `diff`, `git` plumbing).

---

## 0. Answer in one paragraph

The fail-before relation is **real in all five generations of the package I measured**: the
baseline resolver fails exactly the escape cases and nothing else, every one of those failures
becomes a PASS under the fixed bytes, and **no control ever moves** in class or status. Two of the
three assigned verifications hold only *inside* a generation: `matrix_sha256` is identical across
the two receipts **of one generation** and necessarily differs between generations, because the
fixtures, checker and resolver were all rewritten **during this falsify wave** — 13 cases at
`953c278`, then 17, 20, 22 and finally 23 cases across four receipt regenerations between
`03:43:07` and `03:48:29` (5 min 22 s), with five distinct fixture digests, three distinct
resolver digests and two distinct checker digests observed. So "frozen
matrix" is not a property of this package yet; the durable invariant is the baseline derangement,
and that invariant held at every measurement. I also found that the case `glob-expansion-escape`
was **inert** in the 20- and 22-case generations (baseline already `GONE`, for the vacuous reason
that no glob match existed on either side); it was rewritten at `03:48:20` (fixtures
`158a423c` → `332a5fe9`) with a note that states exactly that defect, and in the current 23-case
matrix no escape case is non-discriminating.

---

## 1. The artifacts moved under the measurement

`sha256` of the file as it stood in each revision (reproduced with `sha256sum` and `git show`):

| gen | revision / time | resolve.py | checker | fixtures | cases (esc/ctl) | receipt `generated_at` |
|---|---|---|---|---|---|---|
| **A** | `953c278` (committed) | `ed9a9dae…` | `1bc2db10…` | `5e61a33e…` | 13 (6/7) | *(no field)* |
| **B** | worktree `03:43:07` | `8dd45bc8…` | `53742c8d…` | `5c64e014…` | 17 (7/10) | `06:43:07Z` |
| **C** | `4d9231e` `03:46:26` | `fce5b84b…` | `53742c8d…` | `4e39f65c…` | 20 (9/11) | `06:46:26Z` |
| **D** | worktree `03:47:58` (uncommitted at measurement) | `fce5b84b…` | `53742c8d…` | `158a423c…` | 22 (10/12) | `06:47:58Z` |
| **E** | `12edac4`, unchanged at HEAD `8acb255` | `fce5b84b…` | `53742c8d…` | `332a5fe9…` | 23 (11/12) | `06:48:29Z` |

The **baseline resolver never moved**: `sha256 d6a3c3f1a1d8…` in all five generations, and it is
byte-identical to the pre-fix detector:

```
git rev-parse 922a4dd:corpus/instruments/resolve.py            → 2b1e2528a064f918c5e82c03e109a456e1e72589
git rev-parse HEAD:.ufo/waves/round-23/c1-baseline-resolver.py → 2b1e2528a064f918c5e82c03e109a456e1e72589
```

(the same blob id at `8bf9807` and `953c278`). So the "do-nothing control" is genuine pre-fix
bytes, not a strawman — the one part of the C1 package that cannot have been tuned. `resolve.py`
itself also changed inside the wave (`8dd45bc8` → `fce5b84b`, `03:44:59`→`03:46:26`, reverting the
root-only bounty mirror probe at `resolve.py:243` to `(None, None)`), so even the "after" bytes are
not the bytes the first receipt claimed.

Drift timeline (wall clock, this host):

- `03:43:07` receipts B written (17 cases, `5c64e014`).
- `03:43:38` fixtures → 20 cases (`4e39f65c`): **receipt B's matrix identity was stale 31 s after
  it was generated.**
- `03:46:26` receipts C written; `03:46:46` HEAD → `4d9231e`.
- `03:47:58` receipts D (22 cases, `158a423c`) — still carrying the inert glob case.
- `03:48:20` fixtures repaired (`158a423c` → `332a5fe9`, the glob case rewritten).
- `03:48:29`/`03:48:30` receipts E (23 cases, `332a5fe9`) — the first pair that matches the
  repaired matrix and the last generation I measured; fixtures still `332a5fe9` at `03:49:07`.

**Every number below is pinned to a `sha256`, not to a path.** A reader re-running
`corpus/instruments/mirror-containment-check.py` today will get whatever generation is current.

---

## 2. Fail-before, per generation

Replay command shape (identical for every generation; `--resolver` selects the frozen pre-fix bytes):

```
python3 <checker> --resolver .ufo/waves/round-23/c1-baseline-resolver.py \
                  --fixtures <pinned fixtures> --json /tmp/.../genN-baseline.json
python3 <checker> --resolver <pinned resolve.py> --fixtures <pinned fixtures> --json /tmp/.../genN-fixed.json
```

| gen | baseline | fixed | fail-before set == fixed-flip set | PASS→FAIL | controls differing |
|---|---|---|---|---|---|
| A (13) | `pass=7 fail=6` | `pass=13 fail=0` | **yes**, 6 ids | none | none |
| B (17) | `pass=10 fail=7` | `pass=17 fail=0` | **yes**, 7 ids | none | none |
| C (20) | `pass=12 fail=8` | `pass=20 fail=0` | **yes**, 8 ids | none | none |
| D (22) | `pass=13 fail=9` | `pass=22 fail=0` | **yes**, 9 ids | none | none |
| E (23) | `pass=12 fail=11` | `pass=23 fail=0` | **yes**, 11 ids | none | none |

Generation E (current, `332a5fe9` / `fce5b84b`) fail set — identical to its 11 declared escapes:

```
bounty-parent-traversal, bounty-parent-traversal-vault, relative-mirror-fallback-escape,
bounty-fallback-symlink-escape, relative-fallback-symlink-escape, bounty-prefix-sibling-confusion,
absolute-prefix-sibling-confusion, brace-expansion-escape, glob-expansion-escape,
mirror-root-prefix-sibling-escape, absolute-parent-traversal
```

Generation A, replayed from git objects (`git show 953c278:<path>` extracted to `head/`) so later
edits could not contaminate it:

```
cases=13 escape=6 controls=7 pass=7  fail=6  resolver=d6a3c3f1… matrix=5e61a33e…
cases=13 escape=6 controls=7 pass=13 fail=0  resolver=ed9a9dae… matrix=5e61a33e…
```
and my replay of those bytes at `03:38` (worktree then == `953c278`) is field-for-field identical
to the committed receipt pair.

Receipt reproduction: for B, C, D and E my fresh run reproduces the on-disk receipt **field for
field** except `generated_at` and the absolute `matrix`/`resolver` paths my scratch invocation
supplies (`cases`, `matrix_sha256`, `resolver_sha256`, `checker_sha256`, `totals` all equal).

---

## 3. `matrix_sha256` identity

| pair | baseline receipt | fixed receipt | identical |
|---|---|---|---|
| A | `5e61a33ed5fa…` | `5e61a33ed5fa…` | **yes** |
| B | `5c64e0149f66…` | `5c64e0149f66…` | **yes** |
| C | `4e39f65c7c1b…` | `4e39f65c7c1b…` | **yes** |
| D | `158a423cfd85…` | `158a423cfd85…` | **yes** |
| E | `332a5fe95b94…` | `332a5fe95b94…` | **yes** |

Independently, `sha256sum corpus/instruments/mirror-containment-fixtures.json` equals the
`matrix_sha256` printed by the run in each generation, so the field is a real digest of the matrix
bytes rather than a constant. The check the assignment asks for — "identical across both receipts"
— holds at every generation. It does **not** hold across generations, which is the drift in §1 and
not a defect in either receipt.

---

## 4. "No control case is credited differently" — true, with one caveat

Class and resolved path are identical for **every control in every generation** (7, 10, 11, 12, 12
respectively). I re-ran each case through the real CLI for both resolvers and compared whole TSV
rows, normalising only the case root:

```
case                                        class+path identical   domain identical
confined-bounty-fallback-control                    yes                  yes
confined-relative-fallback-control                  yes                  yes
missing-bounty-target-control                       yes                  yes
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
`home/Projects/bounties-legacy/README.md` in both runs, but pre-fix it reached that answer *inside
the bounty domain* (`base.startswith(BOUNTY_PREFIXES)` true) and post-fix it is routed through
domain `other`, because `bounty_suffix()` returns `None`. Class and path are stable; the route is
not.

This matters for verifiability because the checker records neither `method` nor `domain`
(`path_verdict` at `mirror-containment-check.py:140–160`, PASS at `:221`). A receipt-only
comparison therefore cannot observe a control being re-routed — and the exact-root half of C1 *is*
a routing change. "No control is credited differently" is true exactly as far as the two columns
the receipt keeps.

---

## 5. Non-discriminating cases

### 5.1 All controls are non-discriminating for fail-before — and only load-bearing against over-rejection

Every control has the same class in both runs, so none can witness the defect. Which controls can
ever move was measured with six one-hunk variants of the detector (base `ed9a9dae`, 13-case matrix
`5e61a3`, all under `/tmp/kasegi-r23-falsify-baseline/`):

| variant (one hunk changed) | sha256 | FAIL set |
|---|---|---|
| V1 `bounty_suffix` prefix semantics | `203c2977…` | **`bounty-prefix-sibling-confusion`** (1 escape) |
| V2 both containment guards removed | `c73dc622…` | 5 escapes, all but the prefix case |
| V3 `under_mirror` lexical (`normpath`, no `realpath`) | `47b9757e…` | the 2 symlink escapes |
| V4 bounty-branch guard only | `7fed2c1a…` | the 2 relative escapes |
| V5 `under_mirror` → `False` | `afa4071f…` | 3 controls: confined-bounty, confined-relative, canonical-alias-confined |
| V6 `bounty_suffix` → `base` (unbounded) | `be4d02a4…` | 2 controls: lane-relative-parent-internal, canonical-alias-confined |

Reading: **V1–V4 — every under-enforcement defect, i.e. the direction C1 is about — move zero
controls.** The control set is load-bearing only against over-rejection (V5) and against a grossly
unbounded boundary (V6). "The controls survived" is therefore evidence that the fix did not
over-reject; it is not evidence that the fix is confined. V2 and V4 reproduce the mutants already
published by `L1Kasegi23.MutateBountyConfine-2` / `MutateRelConfine-2` (`pass=8 fail=5`, disjoint
sets) — reproduced here, not originated.

### 5.2 `bounty-parent-traversal-vault` is dominated by `bounty-parent-traversal`

Same domain (`bounty`), same expression (`exists_any(join(mirror_root, suffix))`, `resolve.py:243`),
same predicate (`under_mirror`), same flipped verdict in **all nine** resolver variants I ran
(baseline, V1–V6, V1b, and the fixed bytes). The two differ only in target filename and depth
(`../outside.md` vs `../outside-vault/secret.mjs`). No containment policy among realpath, lexical,
`..`-shaped or no-guard separates them; only a filename-specific rule could, and that is not a
plausible sound fix. It is a duplicate probe — so the matrix's 23 cases carry 11 declared escapes
but fewer independent escape *mechanisms*.

### 5.3 `glob-expansion-escape` was inert, and was repaired mid-wave

As frozen in generations C (`4e39f65c`) and D (`158a423c`), the case was
`corpus/instruments/mirror-containment-fixtures.json:210`:

```json
{"id": "glob-expansion-escape", "nature": "escape",
 "cite": "~/Projects/bounties/<name>.md:1",
 "dirs": ["relocated/outside-vault"],
 "files": {"relocated/outside-vault/x.md": "glob match outside the mirror\n"},
 "expect": "GONE"}
```

Baseline **PASS** (`GONE`), fixed **PASS** (`GONE`) — no discrimination despite the `escape`
label. The cause was not confinement but unreachability, verified with the checker's own
`build_case`:

```
home/Projects/            (empty)     → glob(~/Projects/bounties/*.md) → []
relocated/tbh/            (empty)     → glob(<mirror>/*.md)           → []
relocated/outside-vault/  ['x.md']    ← unreachable from either root
```

`<name>` is rewritten to `*` **inside one path segment** (`PLACEHOLDER.sub("*", p)` in
`exists_any`), so `<mirror>/*.md` cannot reach `relocated/outside-vault/x.md`; the case's note
("matches only outside the mirror through a relative hop") described a hop the citation did not
contain. The pinned `GONE` was a zero-match `GONE`, identical before and after the fix, so the case
inflated the escape count and could not detect a regression.

I demonstrated a reachable variant before the repair landed: `fixtures-glob-reachable.json`
(sha `236048a7…`) added `symlinks: {"relocated/tbh/x.md": "@ROOT@/secret/x.md"}` plus
`files: {"secret/x.md": …}`, and the case then behaved as an escape should:

```
baseline: glob-expansion-escape  expect=GONE  actual=MIRROR-EQUIVALENT  FAIL
fixed:    glob-expansion-escape  expect=GONE  actual=GONE              PASS
```

In generation E the case has been rewritten (fixtures `158a423c` → `332a5fe9`, mtime `03:48:20`) to
`~/Projects/bounties/<name>/../../outside-vault/x.md:1` with `relocated/tbh/sub` present and the
note "A bare `<name>.md` glob cannot cross `/` and would pass on baseline too, so it is not used
here" — the same defect, closed a different way. In E the case is discriminating
(baseline `MIRROR-EQUIVALENT`, fixed `GONE`) and no escape case remains non-discriminating.

### 5.4 The exact-root boundary had exactly one pin in generation A

V1 (boundary reverted, containment intact) fails **one** case in the 13-case matrix:
`bounty-prefix-sibling-confusion`; the five containment cases stay `GONE` because that case's decoy
is *inside* the mirror (baseline's credited path is `relocated/tbh/-legacy/README.md`, realpath
inside), so no containment test can reject it. Dropping that single case would have left the
exact-root half of C1 unpinned while the suite still reported green. Rebuilt on a later base, V1b
(`62f34c08…`) fails two cases — the relative `bounty-prefix-sibling-confusion` **and** the absolute
`absolute-prefix-sibling-confusion` — so later generations closed that single pin with the
absolute-spelling twin.

---

## 6. Findings (falsifiable)

1. **Fail-before holds exactly, at every generation.** Baseline FAIL set == fixed-run flip set
   (A 6/6, B 7/7, C 8/8, D 9/9, E 11/11); zero PASS→FAIL regressions; zero controls differing in
   class or status. Falsifier: one case where the baseline and the fixed bytes disagree outside the
   declared escape set, or a control whose class differs between runs.
2. **The baseline is genuine pre-fix bytes** — blob `2b1e2528…` at `922a4dd`/`8bf9807`/`953c278`,
   file sha `d6a3c3f1…`, identical to the blob. Not thinned to make the red state easier.
3. **The receipts are not frozen during the wave**: five generations in under six minutes
   (`03:43:07`–`03:48:29`), four receipt regenerations, and generation B's `matrix_sha256` was
   stale 31 s after it was written. `matrix_sha256` is identical within each pair and necessarily
   differs across pairs. Falsifier: a receipt pair at these paths whose `matrix_sha256` matches the
   on-disk fixtures at some later read *and* was not regenerated in between.
4. **`glob-expansion-escape` was non-discriminating in generations C and D** — an `escape` case the
   baseline already passed, because no glob match was reachable on either side (`relocated/tbh/`
   empty; `home/Projects/bounties` absent). Closed in generation E. The C and D receipt pairs
   recorded it as a passing escape (they survive only in my scratch copies, having been overwritten
   on disk), so those receipts overstate discrimination on their own.
5. **All controls are non-discriminating for fail-before and load-bearing only against
   over-rejection**: under-enforcement mutants (V1–V4) move no control; the fail-closed guard (V5)
   moves three; an unbounded boundary (V6) moves two.
6. **One control changes route while keeping its class** — `literal-prefix-sibling-control` is
   `RESOLVES` on the same path in both runs but moves from domain `bounty` to `other`; the receipt
   schema records neither `method` nor `domain`, so the receipts cannot show it.
7. **`bounty-parent-traversal-vault` is a duplicate probe** of `bounty-parent-traversal`: same
   branch, same predicate, same verdict under every resolver variant tested.

---

## 7. Scope limits

- Classification only. Nothing here establishes source availability, corpus attribution, C2
  (F06–F08) coverage, or any score movement; no admission claimed, no lane edit performed.
- The variant map (§5.1) is built on generation A's bytes and 13-case matrix. On later generations
  I ran only V1b (boundary) and the glob-reachability probe; mutation durability across the 23-case
  matrix is the mutation seats' lane.
- Generations C–E carry a `path_check` / `path_tolerance` gate (`:140–222`), so PASS there means
  "class matches **and** the recorded path corroborates it, or the case declares a carve-out".
  Generation A's receipts have no such field; A and E are not field-for-field comparable at the
  same case id.
- `absolute-bounty-fallback-control`, `absolute-prefix-sibling-confusion` and
  `absolute-parent-traversal` are host-dependent by design; the required literals are absent on
  this host (`/home/vgpnk/Projects/bounties/ops/rank.mjs`,
  `/home/vgpnk/Projects/bounties-legacy/README.md`, `/home/vgpnk/Projects/outside.md`,
  `/home/vgpnk/Projects/outside-vault` all absent), so their preconditions hold.
- Not in my lane: the root-only-bounty behaviour changed between `8dd45bc8` and `fce5b84b` (the
  mirror-root probe was removed) and no matrix case covers it; flagged as observed churn only.
- Scratch `/tmp/kasegi-r23-falsify-baseline/` is ephemeral and is *not* evidence: it holds `head/`
  (generation A objects), `snap-0343/`, `snap-0344/`, `snap-0348/`, `snap-0348e/`, the
  `head-*.json` / `snap-*.json` / `gen3…gen5` receipts, variants `v1…v6`, `v1b`, and
  `fixtures-glob-reachable.json`. Every claim above is re-derivable from the `sha256` values plus
  `git show <rev>:<path>`, without that directory.
