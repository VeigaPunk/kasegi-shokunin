# ResolverAttack — C1 counter-B falsification (round 24, wave 1)

Seat: mutation-tester (read-only on the lane). Resolver under attack:
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/c1-baseline-resolver.py`
sha256 `690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d` — byte-identical to the committed
`corpus/instruments/resolve.py` at base `d0a3f6a` and at master tip `c2480b1`
(`git cat-file -p <rev>:corpus/instruments/resolve.py | sha256sum` → same hash). All work below uses the frozen
copy in scratch, never a lane file. Scratch: `/tmp/kasegi-r24-ResolverAttack/` (copies only; lane untouched except
this report). Python 3.14.8, stdlib only; nothing installed, no package manager used.

Detectors used, all receipts kept under `/tmp/kasegi-r24-ResolverAttack/`:

- `probe` — 23 citation classes, one CLI run over a disposable fixture (`HOME` and `KASEGI_MIRROR` isolated),
  each row compared against the path that exists on disk. `/tmp/kasegi-r24-ResolverAttack/probe-baseline.txt`
- `matrix` — my faithful re-implementation of the **frozen spec text** of the 8 counter-B cases
  (`/tmp/kasegi-r24-ResolverAttack/matrix-baseline.txt`)
- the **real** round-24 checker `corpus/instruments/resolve-dispatch-check.py` (+ fixtures) against the same
  baseline and against each mutant (`/tmp/kasegi-r24-ResolverAttack/real-mut-*.txt`).

Reproduce: `cd /tmp/kasegi-r24-ResolverAttack && python3 harness.py probe baseline.py` and
`python3 harness.py matrix baseline.py`, plus the real checker as invoked in §F4.

---

## F1 (blocker for the counter's framing) — the frozen 4/8 is reached, but L4 is a *control*, not a liveness case

The real checker on the frozen baseline prints 4/8 (`real-…` run above; wrapper receipt in §F4):

```
L4   liveness expect=INTERNAL         actual=INTERNAL         FAIL
     also expect=MIRROR-EQUIVALENT actual=GONE             FAIL path_check=missing-path
```

`L4`'s primary assertion carries **no** `path_check` reason, while every genuinely failing assertion does
(`path_check=missing-path` / `path-missing-on-disk`). In
`corpus/instruments/resolve-dispatch-check.py:188-210`, `status = PASS` iff `cls == expect` **and**
`path_check == ""`; the case-level `FAIL` is the aggregation of the two citations
(`record["status"] = PASS iff all assertions PASS`). Therefore **L4's primary citation
(`brace/{alpha,beta}.md`, dangling first, live second) passes on the frozen baseline.** The case only fails
because of its added bounty/mirror citation `~/Projects/bounties/{ops,}/rank.mjs` — an *empty-alternative*
citation, i.e. the L1/L2 defect under another branch. The fixture says so itself:
`"which is what makes the case fail-before and reproduces the claim's 4/8 without dropping the primary shape"`
(`corpus/instruments/resolve-dispatch-fixtures.json`, L4 `why`).

Independent confirmation with the spec's literal L4 shape (`br/{x,y}.md`: `x.md` dangling symlink, `y.md`
live) in my re-implementation: `PASS L4 got=INTERNAL path=…/lane/br/y.md`; whole matrix `cases=8 pass=5`
(`/tmp/kasegi-r24-ResolverAttack/matrix-baseline.txt`). The reason is structural: `exists_any`'s brace branch
already tests `os.path.exists(c)` (`c1-baseline-resolver.py:190`), and `exists` follows the link, so a dangling
first alternative is skipped before glob/lexists is ever involved.

Consequences, precisely:

- Distinct *defect classes* exercised by the frozen matrix: **two** (empty brace alternative; glob crediting a
  dangling first match), over **three branches** (lane brace, bounty→mirror brace, lane glob). The fourth
  "liveness" case is a post-fix control the baseline already satisfies.
- The matrix's before-receipt cannot show a regression of L4's advertised property: mutant `lexists` (§F4, M2)
  flips L4's primary to `path_check=path-missing-on-disk` yet the pass count stays **4/8**, because the case
  was already failing on its extra citation.
- The claim text "before_expected: 4/8" is reproducible (4/8 measured), but only because an extra citation of
  the *same* class as L1/L2 was added; the spec sentence "L4 brace where the first alternative names a dangling
  symlink and the second is live" describes a case that cannot fail before the fix. Counter-B therefore
  certifies two defects, and no more, while its label claims four liveness cases.

---

## F2 — Input classes where the verdict is not re-derivable from disk

All rows: one CLI run over `/tmp/kasegi-r24-ResolverAttack/fx-probe` (`probe-baseline.txt`); "truth" is a path
that exists on disk and that the citation's own expansion names. `INTERNAL` = lane-relative class.

| # | input class | token (fixture) | CLI returned | CLI resolved_path | on-disk truth | verdict | caught by L1–L4? |
|---|---|---|---|---|---|---|---|
| 1 | empty **first** alternative | `dir/{,sub}/file.md` | GONE | – | `lane/dir/file.md` | FALSE-GONE | **yes** (L1) |
| 2 | empty **second** alternative | `dir/{sub,}/file.md` | GONE | – | `lane/dir/file.md` | FALSE-GONE | **yes** (L2) |
| 3 | both alternatives empty `{,}` | `dir/{,}/file.md` | GONE | – | `lane/dir/file.md` | FALSE-GONE | same code line, **input uncased** |
| 4 | `{}` with a literal `{}` path | `fig/{}/file.md` | INTERNAL/literal | `lane/fig/{}/file.md` | same | OK | n/a (no defect) |
| 5 | `{}` with nothing | `noexist/{}/file.md` | GONE | – | – | OK (correct) | n/a |
| 6 | nested braces **with** empty alt | `nested/{a{,b},c}/f.md` | GONE | – | `lane/nested/a/f.md` | FALSE-GONE | line caught, **nesting uncased** |
| 7 | brace × `<...>` placeholder | `comp/{<n>,b}/f.md` | GONE | – | `lane/comp/x/f.md` | FALSE-GONE | **no** |
| 8 | brace × placeholder (placeholder in file part) | `comp/{x,b}/<f>.md` | GONE | – | `lane/comp/x/f.md` | FALSE-GONE | **no** |
| 9 | glob alone (control) | `comp/<n>/g.md` | INTERNAL/glob | `lane/comp/x/g.md` | same | OK | n/a |
| 10 | brace alone (control) | `comp/{x,b}/g.md` | INTERNAL/brace | `lane/comp/x/g.md` | same | OK | n/a |
| 11 | **>64 combinations** (65 alts, only the 65th exists) | `many/{a01…a64,zzz}/f.md` | GONE | – | `lane/many/zzz/f.md` | FALSE-GONE | **no** |
| 12 | 10 alts (< bound) control | `many10/{a01…a09,zzz}/f.md` | INTERNAL/brace | `lane/many10/zzz/f.md` | same | OK | n/a |
| 13 | glob matching **only** a dangling symlink | `dangonly/*.md` | INTERNAL/glob | `lane/dangonly/a.md` (nonexistent) | – | NONEXISTENT-PATH | same line as L3, shape uncased |
| 14 | glob, dangling first, live later | `dangfirst/*.md` | INTERNAL/glob | `lane/dangfirst/a.md` (nonexistent) | `lane/dangfirst/b.md` | NONEXISTENT-PATH | **yes** (L3) |
| 15 | glob first match is a **directory** | `dirglob/*.md` | INTERNAL/glob | `lane/dirglob/a-dir.md` (dir) | dir + `b-live.md` file | CREDITS-DIRECTORY | **no** |
| 16 | brace alternative that is a **directory** | `dirbrace/{a,b}.md` | INTERNAL/brace | `lane/dirbrace/a.md` (dir) | dir + `b.md` file | CREDITS-DIRECTORY | **no** |
| 17 | glob first match a file (discriminator) | `dirfile/*.md` | INTERNAL/glob | `lane/dirfile/a.md` | same | OK | n/a |
| 18 | `..` inside a brace alternative | `dotdot/{../../outside,sub}/f.md` | INTERNAL/brace | `lane/dotdot/../../outside/f.md` → realpath **outside lane** | `fx-probe/outside/f.md` | OUTSIDE-LANE while class says INTERNAL | **no** |
| 19 | `..` in the glob part | `../outside/*.md` | INTERNAL/glob | `lane/../outside/f.md` → **outside lane** | `fx-probe/outside/f.md` | OUTSIDE-LANE | **no** |
| 20 | `..` escaping the **mirror** in the rel fallback | `mdir2/{../../outside2,zzz}/f.md` | GONE | – | escape target exists, outside mirror | OK (confinement holds) | **no** (and see M1) |
| 21 | **absolute path inside a brace alternative** | `{/tmp/kasegi-r24-ResolverAttack/absalt,rel}/f.md` | GONE | – | `/tmp/kasegi-r24-ResolverAttack/absalt/f.md` | FALSE-GONE | **no** |
| 22 | single-alternative brace (bash keeps it literal) | `single/{only}.md` | INTERNAL/brace | `lane/single/only.md` | same | divergence, benign under the doc | **no** |
| 23 | `<...>` placeholder with no match | `noglob/<nothing>/f.md` | GONE | – | – | OK (correct) | n/a |

Function-level mechanism evidence (same baseline bytes, imported directly):

```
empty-first  : ['/L/dir/sub/file.md']                     # "" dropped
both-empty   : []                                          # `{,}` yields nothing at all
nested-clean : ['/L/n/a/f.md','/L/n/a/f.md','/L/n/ab/f.md','/L/n/c/f.md']   # duplicate candidate
nested-empty : ['/L/n/ab/f.md','/L/n/c/f.md']              # "a" lost
many65 count : 64 | zzz present: False | last: /L/many/a64/f.md            # target dropped by the bound
brace+ph     : ['/L/comp/<n>/f.md','/L/comp/b/f.md'] -> exists_any: (None, None)  # glob never runs on expansions
abs-alt      : ['/L//tmp/x/f.md','/L/rel/f.md']            # absolute alternative swallowed by the base join
```

## F3 — Named defects the four frozen liveness cases miss

1. **Bound truncation (`out > 64` / `sorted(out)[:64]`, `c1-baseline-resolver.py:178,180`).** A citation whose
   only on-disk target sits after the 64th sorted alternative is GONE (row 11). No frozen case has more than
   four alternatives, so the matrix is blind to *any* bound ≥ 2 (§F4 M3 killed, M4 survives).
2. **Brace × glob/placeholder composition.** `exists_any` runs the glob on the *brace-bearing* string after
   brace expansion fails, so a brace alternative that itself needs `<...>`→`*` (or contains `*`) never resolves
   (rows 7, 8). The planned round-24 patch touches neither; the matrix has no composed citation → 8/8 while the
   class stays broken.
3. **Absolute alternative at token start.** Brace expansion is applied *after* the lane/mirror base is joined,
   so `{/abs,x}/f.md` becomes `<base>//abs/f.md` and an existing absolute target is reported GONE (row 21).
   This contradicts the docstring's "deterministic expansion of every `{a,b}` set" read as textual substitution.
4. **Slice-vs-set**: nested braces emit duplicate candidates (`nested-clean` above); harmless, but "sorted set"
   in the docstring is not a set.
5. **Directory credit.** Both branches treat "exists" as "resolved": `glob`'s `matches[0]` and brace's
   `os.path.exists(c)` will return a directory, including one that sorts ahead of the real document
   (rows 15, 16). The planned patch (`os.path.exists` for the glob first-match) *keeps* this behaviour, and
   L3's dangling-symlink shape does not test it.
6. **Case-root escape is not asserted anywhere in counter-B.** `INTERNAL` is returned with a `resolved_path`
   whose realpath is outside the lane root, by literal `..` (documented, pre-existing) and equally by `..`
   inside a brace alternative or a glob (rows 18, 19). Documented as by-design for the literal form; the matrix
   nevertheless has no containment assertion, so it cannot notice a patch that widens the escape. (The round-23
   `mirror-containment-check.py` covers the mirror/bounty side — see M1 — but nothing covers the lane side.)
7. **`{,}` and nested-empty** are the same source line as L1/L2, so a fix that keeps empty alternatives
   anywhere fixes them; but a narrower fix ("keep an empty alternative only when the group has another
   non-empty member") would pass L1/L2 and L4 and still leave `{,}`/nested-empty broken. The matrix cannot
   tell these apart.

---

## F4 — Mutation probes against the real detector

Detector = the real `resolve-dispatch-check.py` with the real fixtures (checker sha256
`acbb687094f0fedb3517c744f0bcda68a4edd96ec760087e667fc70c6a0569e1`, matrix sha256
`fef0f02d6d64cfb68702d245ecd156b6bb7eea95115c2a94216a10f8f9414c8c`), each mutant a one-line change to a
copy of the baseline.

| mutant | one-line change | counter-B | round-23 containment | probe delta | verdict |
|---|---|---|---|---|---|
| M1 `mut-m1-noconfine.py` | rel fallback: `if m and under_mirror(...)` → `if m:` | **4/8, byte-identical failing set** | 21/24 (3 escape cases fail) | `mirror-escape` GONE → MIRROR-EQUIVALENT to a path outside the mirror | **survives counter-B**; killed only by the sibling instrument |
| M2 `mut-m2-lexists.py` | brace branch `os.path.exists(c)` → `os.path.lexists(c)` | 4/8, **pass count unchanged**, L4 primary gains `path_check=path-missing-on-disk` | 24/24 | brace dangling alt now credited | killed only **post-fix**; pre-fix receipt blind (F1) |
| M3 `mut-m3-bound1.py` | bound 64 → 1 | **3/8** (L4 primary flips to GONE, `brace-only` control also fails) | 24/24 | many10/many65 FALSE-GONE | killed |
| M4 `mut-m4-bound8.py` | bound 64 → 8 | **4/8, identical receipt** | **24/24** | `many10/{a01…a09,zzz}/f.md`: `INTERNAL` → **GONE** | **survives the whole lane instrumentation while changing a verdict** |

M4 is the coverage finding: a real behaviour change (a citation that resolved now answers GONE) passes the
round-24 counter-B matrix *and* the round-23 containment matrix, because no case in either has more than four
brace alternatives. sha256 of the mutant files: M1 `a1efcb28…`, M2 `f50f2125…`, M3 `2dc6cc4d…`, M4
`25c5584e36417ceb8cd5f035db25d537cbb2c58ab3a4ce4fb6686a6e450c34b8`.

Receipts: `/tmp/kasegi-r24-ResolverAttack/real-{mut-m1-noconfine,mut-m2-lexists,mut-m3-bound1,mut-m4-bound8}.txt`,
`matrix-mut-*.txt`, `probe-mut-*.txt`.

## F5 — Restoration / non-mutation evidence

- Every mutant is a separate file; the baseline copy was never edited. After all probes:
  `sha256sum baseline.py` = `690153adc3e39f1e86317bd7b4eeb3b04ece5b4beb55f50111d8e98e7ff3ea2d` = sha256 of
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-24/c1-baseline-resolver.py`.
- No lane production file was written by this seat; the only lane write is this report. Observed lane state
  (`git status --short` at `c2480b1`): pre-existing modifications by other seats
  (`corpus/instruments/resolve.py`, `corpus/instruments/source-recheck.py`) plus untracked round-24 artifacts
  (`corpus/instruments/resolve-dispatch-check.py`, `…-fixtures.json`, `corpus/instruments/capture-source.py`,
  `corpus/source-snapshots/round-24/`, `.ufo/waves/round-24/`) — none of them mine, all left as found.
- `corpus/instruments/resolve-dispatch-check.py` does not exist at base d0a3f6a
  (`git ls-tree --name-only d0a3f6a corpus/instruments/` lists no such file), so counter-B had no committed
  receipt before this wave; the 4/8 above is from the working-tree checker produced this wave.

## F6 — What this means for C1 counter-B (for L1, the integration owner)

- Counter-B as frozen is a valid gate for exactly two defect classes plus their branch variants; it is **not**
  evidence that brace/glob dispatch is live. Rows 7, 8, 11, 15, 16, 18, 19, 21 all stay wrong after an 8/8.
- L4 should be re-labelled a **control** (its primary assertion is green on the baseline), and the before-count
  restated as `3 liveness + 4 controls + 1 duplicate-class citation = 4/8`. Editing the matrix after seeing
  this would be a post-hoc rule change (QUALITY R7): either scope the claim to the two named defects, or amend
  the claim before scoring to add cases for the classes above (bound, composition, absolute alternative,
  directory credit, lane-side containment) — which changes what "8/8" means.
- Nothing here asks for a contract change; the surviving defects above the frozen set are coverage findings,
  reported as such.
