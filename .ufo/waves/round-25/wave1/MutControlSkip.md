# MutControlSkip — phase-4 skip controls against C1 (round 25, wave 1)

Seat: `L1Kasegi25.MutControlSkip` (read-only lane; writes confined to
`.ufo/waves/round-25/wave1/`). Base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.

## Method

Detector = the frozen counter, unmodified, run in its frozen form from each scratch root:

```
python3 corpus/instruments/recheck-audit.py --json <out> --quiet
```

Each control lives in its own copy under `.ufo/waves/round-25/wave1/mut-skip/<control>/`:

* `corpus/` copied from the lane at base revision; all 35 `corpus/knowledge/*.md` files
  verified byte-identical to `git show b49948f:corpus/knowledge/<file>` (35 checked,
  0 differ). The live lane tree was already dirty from a sibling scribe when this ran
  (30 modified knowledge files); the copies deliberately predate that and reproduce the
  frozen before-receipt.
* only the `recheck:` line(s) named in each control were rewritten; nothing else touched.

Baseline first (a baseline failure would make every verdict inconclusive):

| run | receipt | exit |
|---|---|---|
| pristine copy | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1` | 1 |

This matches `.ufo/waves/round-25/c1-before.json` field for field, so the detector is
live and the baseline is the frozen one.

## Controls (a) — one row each

| # | control (what the 35 lines become) | receipt summary | exit | reaches `pass=35`? |
|---|---|---|---|---|
| 1 | delete every `recheck:` line (35 files, 35 deletions) | `lines=0 pass=0 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` | 0 | no — `pass=0`, and `lines=0` |
| 2a | `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true` | `lines=35 pass=0 ... paths_fail=35 exit=1` | 1 | no |
| 2b | `recheck: cd ~/Projects/shokunin/kasegi-shokunin && true` | `lines=35 pass=35 fail-closed=0 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` | 0 | **YES** |
| 3 | `recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && test -e corpus/knowledge/<own file>` | `lines=35 pass=35 ... exit=0` | 0 | **YES** |
| 4 | audit pointed at a copy whose `corpus/knowledge/` is empty (instruments only) | `lines=0 pass=0 ... exit=0` | 0 | no — no crash, silent zero |
| 5 | delete only the 29 non-passing lines, keep the 6 passing ones | `lines=6 pass=6 fail-closed=0 ... exit=0` | 0 | no — but `exit=0` |
| 6 | `recheck: cd <lane> && python3 corpus/instruments/recheck-audit.py --selftest` | `lines=35 pass=35 ... exit=0` | 0 | **YES** |
| 7 | honest fix landed **and** C2's 36th entry admitted | `lines=36 pass=36 ... exit=0` | 0 | no — literal target says 35 |
| 8 | control 7 minus **one** `recheck:` line (36 entries → 35 lines) | `lines=35 pass=35 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` | 0 | **YES, exactly** |

Control 7 was built by applying the honest fix (strip the `on-restoration — … (fails closed …)`
prose wrapper, prefix `cd <lane> &&`, prefix `cd <lane> &&` on the 6 cwd-dependent lines) and
then adding one knowledge entry carrying a `source:` header, as C2 requires. Control 8 then
removes the `recheck:` line from `citation-bases.md` only.

Control 1 and control 4 do **not** crash: `audit_entry` returns `None` for an entry with no
`recheck:` line and `collect` silently drops it, so the entry disappears from `lines` and
`main` returns `0 if passed == len(entries)` → `0 == 0` → exit 0.

## (b) Verdicts on controls 1 and 2 — plainly

**Control 1 (delete all lines): does not reach `pass=35`.** It prints `lines=0 pass=0 …
exit=0`. The frozen *target string* (`lines=35 pass=35 exit=0`) blocks it; the frozen
*counter's exit status* does not. If the L1's after-check reads only `exit=0`, control 1 is a
full pass and C1 is void. The counter must be read on the full summary line, not the exit code.

**Control 2 (replace every line with `cd <lane> && true`): reaches `pass=35` — as written with
a `~/Projects/` prefix.** `recheck: cd ~/Projects/shokunin/kasegi-shokunin && true` scores
`lines=35 pass=35 … exit=0`. It parses, it is cwd-identical (empty output, exit 0 from both
`lane/` and `/`), and limb (c) is satisfied by `HOME_BASE_RE.search`, which matches the `cd`
target itself — no path is ever tested. Only the absolute-path spelling
(`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true`) is blocked, and only because it
contains no `~/Projects/` substring.

So: **C1 as currently instrumented is reachable by a do-nothing control (2b), and C1's literal
target is reachable by a one-line deletion (8). By the phase-4 rule, the target as implemented
is a wrong target. It is not yet void — the instrument can be tightened before the after
receipt, and the honest fix already measures `lines=35 pass=35 exit=0` under the tightened
instrument (see below) — but it becomes void if the L1 measures with the frozen bytes as they
stand.**

## What the frozen predicate blocks and what it misses

| control | blocked by predicate text? | blocked by the counter as implemented? |
|---|---|---|
| 1 delete all | yes — `lines=35` in the target | **no** — exit 0, `lines=0` |
| 2a absolute `cd … && true` | yes — limb (c) | yes — `paths_fail=35` |
| 2b `~/Projects` `cd … && true` | text says "a ~/Projects/ **base test**"; a `cd` is not a test | **no** — regex matches the `cd` |
| 3 `test -e` own entry file | text says the line is "the entry's own verifiability instrument"; a tautology is not one | **no** — token exists, exit/digest identical |
| 4 empty dir | yes — `lines=35` | **no** — exit 0 |
| 5 delete non-passing lines | yes — kill_rule ("deleting its fail-closed test … the claim is void") | **no** — `exit=0`, and the kill_rule has no mechanical detector |
| 6 `--selftest` on every line | no clause covers it | **no** — `35/35` |
| 8 one deletion from the honest 36-state | yes — `lines=35` is met, but only by deletion | **no** — prints the exact target string |

The root cause is one line in `audit_entry`:

```python
named = bool(tokens) or bool(HOME_BASE_RE.search(line))
```

`HOME_BASE_RE` matches any `~/Projects/…` substring, including a `cd` destination, so limb (c)
accepts a line that names no artifact at all. `root-loss-2026-10-12.md` legitimately depends on
the `~/Projects/` disjunct (its line is `test ! -e ~/Projects/bounties && … && test -e
~/Projects/ufo-fsd-alpha`, no `corpus/` token), so the disjunct cannot simply be removed — it
must be narrowed to a real test.

## (c) One-line limbs that block the surviving controls

Measured on the same copies. Variant scripts: `mut-skip/variant-abc.py`, `mut-skip/variant-abcd.py`
(copies of the frozen instrument with only the lines below changed).

**Limb A — narrow the `~/Projects/` disjunct to a base *test* (blocks 2b):**

```python
named = bool(tokens) or bool(re.search(r"test\s+-[de]\s+~/Projects/", line))
```

**Limb B — the line must name something other than its own knowledge file, or run a real base
test (blocks 3):**

```python
limbs["paths"] = named and not missing and (any(os.path.normpath(t) != own for t in tokens)
    or bool(re.search(r"test\s+-[de]\s+~/Projects/", line)))
```

**Limb C — `lines` is an invariant, not a by-product; an entry with no `recheck:` line is a
failure (blocks 1, 4, 5, 8):**

```python
total = len(glob.glob(os.path.join(root, "corpus/knowledge/*.md")))
return 0 if (passed == len(entries) and len(entries) == total and total > 0) else 1
```

**Limb D — the line must touch its own entry or a source manifest (blocks 6):**

```python
limbs["own"] = (own in [os.path.normpath(t) for t in tokens]
    or any(t.startswith("corpus/source-snapshots/") and "--source" in line for t in tokens)
    or bool(re.search(r"test\s+-[de]\s+~/Projects/", line)))
```

Measured effect (frozen baseline in the same table for regression checking):

| root | frozen counter | A+B+C (`variant-abc`) | A+B+C+D (`variant-abcd`) |
|---|---|---|---|
| pristine (before) | `lines=35 pass=6 exit=1` | `lines=35 pass=6 exit=1` | `lines=35 pass=6 exit=1` |
| honest fix, 35 entries | `lines=35 pass=35 exit=0` | — | `lines=35 pass=35 exit=0` |
| 1 delete all | `lines=0 pass=0 exit=0` | `lines=0 pass=0 exit=1` | — |
| 2a absolute | `pass=0 exit=1` | `pass=0 exit=1` | — |
| 2b `~/Projects` | `pass=35 exit=0` | `pass=0 paths_fail=35 exit=1` | `pass=0 exit=1` |
| 3 own-file `test -e` | `pass=35 exit=0` | `pass=0 paths_fail=35 exit=1` | `pass=0 exit=1` |
| 4 empty dir | `lines=0 pass=0 exit=0` | `lines=0 pass=0 exit=1` | — |
| 5 delete non-passing | `lines=6 pass=6 exit=0` | `lines=6 pass=6 exit=1` | — |
| 6 `--selftest` | `pass=35 exit=0` | `pass=35 exit=0` | `pass=0 exit=1` |
| 8 one deletion, 36-state | `lines=35 pass=35 exit=0` | — | `lines=35 pass=34 exit=1` |

No honest line regresses under A+B+C+D: pristine stays `pass=6` with the same 23 parse and 6
cwd failures, and the honest-fix simulation stays `35/35`.

Note on the receipt: the summary line prints only `parse_fail/cwd_fail/paths_fail`, so a limb-D
failure shows as `pass=0 … paths_fail=0 exit=1` (control 6). Add `own_fail` to the summary
print, or the after receipt will look self-contradictory.

Residual ceiling: this is a form-only predicate. Limb D raises the cheapest uniform cheat from
`&& true` to "invoke an existing corpus instrument and name the entry or a source manifest",
which is roughly the cost of writing the honest line — but it still cannot prove the command
*verifies* anything (e.g. a `--source` flag on the wrong entry passes). The only mechanical
block is a negative control: re-run each line in a scratch copy with the entry's own file
renamed and require the exit status or digest to change. That is not a one-liner; the L1 should
treat it as optional hardening, not as a precondition for C1.

## What the L1 must tighten before the after-measurement

1. **Limb A is mandatory.** Without it, control 2b reaches `pass=35` and the claim is void.
2. **Limb C is mandatory.** Without it, `exit=0` is reachable by deleting lines (1, 4, 5, 8);
   control 8 is the exact phase-4 case — the literal frozen target reached by deleting one line.
3. **Restate the C1 target arithmetic.** C2 requires a new knowledge entry, so the honest after
   state is `lines=36 pass=36 exit=0` (measured, control 7). The frozen target `lines=35 pass=35`
   is then satisfiable *only* by deleting a line. The after predicate must be
   `lines == pass and lines >= 35 and exit == 0`, not the literal string.
4. **Limb B and D are recommended** (controls 3 and 6 are one-line cheats that survive otherwise).
5. Read the summary line, never the bare exit status.

## Evidence and restoration

* No production edit: nothing under `corpus/` was written by this seat. Lane `corpus/knowledge`
  was concurrently modified by a sibling scribe (30 files) *before* the copies were taken; the
  copies were verified byte-identical to base `b49948f` (35/35), so the baseline is the frozen
  pre-fix state, not the sibling's in-flight state.
* Scratch copies are disposable per tasking and left in place for inspection:
  `mut-skip/{pristine,c1,c2abs,c2tilde,c3,c4,c5,c6,c7,c8,honest}` plus
  `baseline.json`, `c1.json`, `c2abs.json`, `c2tilde.json`, `c3.json`, `c4.json`, `c5.json`,
  `c6.json`, `c7.json`, `c8.json`, `honest-frozen.json`, `honest-abcd.json`, `abcd-pristine.json`.
* Tooling: none installed or upgraded (no pacman, no uv, no network).
