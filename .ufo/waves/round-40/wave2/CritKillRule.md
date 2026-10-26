# CritKillRule — round-40 wave-2 receipt (C1 kill-rule attack)

Seat: `CritKillRule` (critic, leaf). Item: attack the **C1 kill rule** —
construct states where a real defect exists but the frozen kill rule does NOT
fire. Axes touched: **depth:verifiability** (primary), **coverage**. No lane,
fleet, or source-tree file was edited; no subagents; no tool installs; no
network fetches. Read-only git only.

**Verdict: 7 distinct escape states reproduced.** The frozen C1 kill rule has
hardening gaps in the H6 scratch scan (name family, depth, tolerance chain, and
a fail-open scan root), the pending-marker clause (single byte spelling), and
the working-tree-clean clause (git-status blindness). Each is a counter/hardening
defect the L1 must know about. All escapes are reproduced against the **committed
bytes** (export of J5 `3074c7679d6f527ec3930d7748ccce1dbae4a58a`), not against
inference.

---

## 1. Method (what was run, against what)

- Instrument: `corpus/instruments/r40-closure.sh` at J5 (committed blob
  `bdbd18a3239c3467c79b5c487a8e3256c2cae1678752cea2487a5eaa12897f1e`,
  byte-identical to the live worktree file and to `suite-sha256` in the Y
  receipt `final-gates/all-gates.txt`).
- The H6 limb was extracted verbatim from the committed tree for the hermetic
  probe fixture; the full suite was also run end-to-end (export mode) for every
  scratch scenario, and the H6 payload lines taken from the real run transcripts.
- Scratch sandboxes under `/tmp` / the seat scratch; the live root
  `/fast/scratch/hyaku` was only ever **read** (scanned), never written outside
  the seat's own scratch dir. The seat scratch is removed before yield.
- Positive controls reproduced (the suite's machinery works when it fires):
  plain run refused exit 2; stray dir `kasegi-r40-stray` reds H6
  (`strays=1,read=ok closed=0`); dangling symlink, unreadable dir (chmod 000)
  and regular file with a family name all red fail-closed (`read=fail`);
  symlink to the work dir itself is tolerated; clean root is green.

---

## 2. Escape states (each: escape → evidence → why the kill rule misses it)

### F1 — a leftover scratch dir nested under any top-level container is invisible (top-level-only scan)

The H6 limb scans only `find $root -mindepth 1 -maxdepth 1` (one level). A real
leftover `kasegi-r40-*` dir placed under any top-level sibling — e.g.
`/fast/scratch/hyaku/<something>/kasegi-r40-stray` — is never seen.

```
$ mkdir -p $SB/scratch/container/kasegi-r40-stray
$ bash r40-closure.sh --export-ref 3074c76 --lane <LANE> \
      --scratch-root $SB/scratch --work $SB/work
H6 payload=strays=0,read=ok closed=1
```

Kill-rule text: "any leftover kasegi-r39*/r40 scratch entry at filing other
than the passed --work dir" — no depth qualifier; a nested leftover is a real
leftover. The instrument only audits one directory level of one root.

### F2 — on the live host, the round's own scratch container either reds H6 or hides every leftover, depending only on where --work sits

`/fast/scratch/hyaku/kasegi-r40` (the round's scratch container, top-level,
family-matching) exists at filing. Verified with the **real** default root:

```
# work genuinely outside the container (/tmp):
$ bash r40-closure.sh --export-ref 3074c76 --lane <LANE> --work /tmp/crk-out.XXXX
H6 payload=strays=1,read=ok closed=0        # the container itself is "a leftover"

# work inside the container (standard layout):
$ bash r40-closure.sh --export-ref 3074c76 --lane <LANE> --work .../kasegi-r40/<x>/work
H6 payload=strays=0,read=ok closed=1        # green; every seat scratch inside is nested & invisible
```

So the scratch clause fires only when work sits outside the container — and in
that case it fires on the round's own container, not on any actual leftover. In
the standard layout (work inside the container) the clause is green regardless
of what junk any seat left behind anywhere inside the container tree. The kill
clause is not a stable predicate of "leftovers exist"; it is a predicate of the
invocation geometry.

### F3 — dotfile scratch dir escapes (contradicts the wave-1 frozen contract)

The committed limb does **not** strip a leading dot before matching the family
(`b=${e##*/}; case $b in kasegi-r39*|kasegi-r40*)`). `.kasegi-r40-seat` is
invisible. The wave-1 frozen-contract probe (`ExecH6ScratchFixtures.sibling-dir.sh`)
explicitly specified "after stripping one leading dot … `sibling-dotdir expect=red`";
the committed instrument deviates and goes green:

```
$ mkdir -p $SB/scratch/.kasegi-r40-seat
$ bash r40-closure.sh --export-ref 3074c76 --scratch-root $SB/scratch --work $SB/work
H6 payload=strays=0,read=ok closed=1
```

### F4 — case / Unicode-separator name variants escape the family match

Family match is byte-literal and case-sensitive:
- `Kasegi-r40-stray` (capital K) → green.
- `kasegi‑r40‑stray` (U+2011 non-breaking hyphen instead of `-`) → green.
- (`kasegi_r40_stray`, `kasegi−r40−stray` U+2212, U+2329/27E8 look-alikes similarly.)

```
$ mkdir -p "$SB/scratch/Kasegi-r40-stray" "$SB/scratch/$(printf 'kasegi\u2011r40\u2011stray')"
$ bash r40-closure.sh --export-ref 3074c76 --scratch-root $SB/scratch --work $SB/work
H6 payload=strays=0,read=ok closed=1
```

### F5 — ancestor-prefix tolerance does not require a clean chain

Tolerance is `case $realw in "$r"|"$r"/*) continue ;;` — a raw path prefix. A
family-named top-level **symlink** whose realpath is *any ancestor* of `--work`
is silently tolerated, even though it is not the work dir and contains far more
than a clean chain (the wave-1 contract required "every level from the entry
down to --work contains exactly the next component and nothing else"):

```
$ ln -s $SB $SB/scratch/kasegi-r40-link     # sandbox root containing work + lots else
$ bash r40-closure.sh --export-ref 3074c76 --scratch-root $SB/scratch --work $SB/work
H6 payload=strays=0,read=ok closed=1
```

(Symlink → `/` actually **reds** for the wrong reason: with `r=/`, the pattern
becomes `"$r"/*` → `//*`, which never matches a normal work path. The escape is
real for any non-root ancestor.) A real directory named `kasegi-r40-*` that
contains `--work` and also other junk is likewise tolerated — the chain is
never checked for cleanliness.

### F6 — a nonexistent (or non-directory) `--scratch-root` silently disables the scan (fail-open)

`check_h6`: `if [ -d "$root" ]` — when false, the whole scan is skipped and the
limb prints `strays=0,read=ok` and returns green. Verified:

```
$ bash r40-closure.sh --export-ref 3074c76 --scratch-root $SB/scratch-nonexistent --work $SB/work
H6 payload=strays=0,read=ok closed=1
```

Any caller who controls `--scratch-root` (the counting command does not pass it,
but the tool accepts it) can green H6 regardless of the real scratch state. The
documented posture is "fail-closed on a scan error"; a missing root is a scan
error and is treated as clean.

### F7 — a pending marker spelled differently does not fire the literal grep

Kill clause: `` `grep -c '⟨pending' corpus/lessons/round-40.md` != 0 `` fires
only on the exact bytes U+27E8 `⟨` + `pending`. Respellings with identical
intent — `⟨ pending` (space), `〈pending` (U+2329), `<pending` (ASCII), `⟨Pending`,
`⟨PENDING` — all yield count 0 (verified; fixture
`CritKillRule.pending-variants.md`). The clause enforces one byte spelling, not
the semantic state "no unfinished markers in the round lesson". Current
`round-40.md` has no `⟨` at all (`grep -c '⟨pending'` = 0).

### F8 — a working tree that appears clean while a file changed (git-status blindness)

The "lane working tree not clean at filing" clause is enforced outside the
instrument with `git -C <lane> status --porcelain`
(`scripts/hyaku/closure-prompt.md`). Two mechanisms make that command report
clean while a real uncommitted change exists (verified in fixture
`CritKillRule.worktree-clean.sh`, full transcript inside):

```
# (a) tracked file changed after `git update-index --skip-worktree` (same for --assume-unchanged):
git status --porcelain: []        # clean
git diff HEAD stat:     []        # also empty — both gates miss the change
# (b) untracked file matching .gitignore / .git/info/exclude:
git status --porcelain: []
# control without the flag, same file change:
git status --porcelain: [ M tracked.txt]
```

A defect committed as an uncommitted edit to a skip-worktree/assume-unchanged
tracked file (or an ignored new file) therefore escapes the clean-tree kill
clause — and also escapes `git diff HEAD`.

---

## 3. Positive reproductions (controls, all against the committed bytes)

| scenario | H6 payload | exit/closed | expected |
|---|---|---|---|
| clean root | `strays=0,read=ok` | green (closed=1) | green |
| stray dir `kasegi-r40-stray` | `strays=1,read=ok` | red (closed=0) | red |
| dangling symlink `kasegi-r40-dangling` | `strays=0,read=fail` | red | red |
| unreadable dir (chmod 000) | `strays=0,read=fail` | red | red |
| regular file `kasegi-r40-file` | `strays=0,read=fail` | red | red |
| symlink → work dir | `strays=0,read=ok` | green | green |
| plain run (no --export-ref) | — | exit 2 | exit 2 |
| committed suite digest | `bdbd18a3…` | matches receipt `suite-sha256` | match |

At J5 the suite prints `closed=9/10 exit=1` (H7 red, receipt absent from tree —
the documented green window is Y = J + receipt).

---

## 4. Smallest safe corrections (per escape)

- F1/F2: scan the scratch root recursively for the name family (bounded depth,
  e.g. `find -maxdepth 3`), or at minimum also audit the round container's
  immediate children when `--work` is inside it, and tolerate only the single
  clean chain to `--work`.
- F3/F4: normalize the family match — strip one leading dot, match
  case-insensitively, and normalize Unicode separators (`-`, `‑`, `−`, `_`,
  whitespace) before comparison.
- F5: replace the raw path-prefix tolerance with the wave-1 contract's clean
  chain check (each level between entry and work must contain exactly the next
  component and nothing else; a symlink is tolerated only if it resolves
  directly to the work dir).
- F6: treat a missing/non-directory `--scratch-root` as `read=fail` (fail-closed),
  and reject `--scratch-root` values that are not a real directory.
- F7: broaden the pending-marker grep to a normalized class
  (`⟨[[:space:]]*[Pp]ending`, `〈pending`, `<pending`, case variants) and/or
  require a resolved-marker table in the round lesson (round-39 precedent).
- F8: at filing, also run `git diff HEAD --name-status` (catches skip-worktree
  hidden tracked changes only if combined with `--no-skip-worktree` listing —
  the durable fix is to forbid `skip-worktree`/`assume-unchanged` markers in the
  lane and to check `git ls-files -v` for them) and check untracked files with
  `--untracked-files=all` plus a scan that does not honor `.gitignore`
  (`git status --porcelain --untracked-files=all --ignored` is a stricter gate).

## 5. Hygiene

- Disk guard green before/after (`/fast/scratch/hyaku` 24%, 616.7G free).
- No tool installed/upgraded; no pacman; no network; no writes to
  `~/.local/bin` or fleet-root tracked files; no mutating git anywhere.
- Lane untouched: `git status --porcelain` shows only the pre-existing
  untracked `.ufo` entries plus the wave-2 receipts.
- Seat scratch `/fast/scratch/hyaku/kasegi-r40/CritKillRule/` removed before
  yield (`trap 'rm -rf -- "$S"' EXIT`); no `kasegi-r40*` sibling survives from
  this seat at filing.
- Deliverables (only writes): this receipt (`wave2/CritKillRule.md`) and the
  three byte-exact attack fixtures:
  - `wave2/CritKillRule.h6-escapes.sh` (sha256
    `2f154c7de7547f633bbb15d18cac94f47429ab8ef052b2febcc49f753080ec44`) — 11
    scenarios, all verdicts pass, sandbox cleaned;
  - `wave2/CritKillRule.pending-variants.md` (sha256
    `c0f3124c13e8f7d138e0c6aa68d26d0bcfea95d113137fea30cde078eb649269`);
  - `wave2/CritKillRule.worktree-clean.sh` (sha256
    `1b3811aea87f8cdb799b769b24c72ff2e449370fc1c4951e894a9431bd5dc82b`).
