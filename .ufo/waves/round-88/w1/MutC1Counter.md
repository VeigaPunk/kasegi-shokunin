# MutC1Counter — mutation test of the frozen round-88 C1 counter

Seat: `MutC1Counter` (w1, round-88 attempt 1). Scope: **one** probe — mutation-test
`.ufo/waves/round-88/c1/knowledge-meter.py` against the C1 control battery and report
killed/survived per mutant. This is a coverage reading of the counter, not a re-scoring of
C1: the claim is judged on its frozen predicates elsewhere.

## Artifacts (read-only inputs)

| artifact | sha256 |
|---|---|
| `.ufo/waves/round-88/c1/knowledge-meter.py` | `b4127597c4ee1ee29562450903f777afd29699c59bb0b1dedb687c3f45c98b55` (before and after this seat) |
| `.ufo/waves/round-88/c1/repair-map.json` | `5a731401a1f9145e24898a13c8a47be2135beabedde4352170cf2d2daa5d7960` |
| `corpus/instruments/resolve.py` | `db5e0767c60ce00ea6c9cfb4ddd3e159e9a86525e5c8417c4a0a73e2e6d45667` |
| base rev | `6beead9148945fa695cf3139e8fc9d8e91cc5fd0` |
| target | `742/1743` (base 703/1754) |

Scratch: `/fast/scratch/hyaku/kasegi-r88/MutC1Counter/` (clones, mutants, per-run outputs;
removed before this seat yielded). Every lane script ran `python3 -B`; no git/jj write
happened in the lane (clones are `git clone --shared` + `checkout` **inside scratch**, and
the one index write — `git add` of a decoy file — happened in a scratch clone whose
`rev-parse --show-toplevel` was asserted equal to that clone).

## Method

1. The frozen counter is read into scratch; each mutant is **one** textual single-point
   change (asserted to occur exactly once in the frozen bytes). Mutant sha256 and the exact
   `old`/`new` line pair are in `MutC1Counter-receipts/mutants.tsv`.
2. Controls are the frozen eight, replicated step-for-step from
   `.ufo/waves/round-88/controls/c1-controls-r88.sh` — per-control `git clone --shared` of
   the lane, `checkout 6beead91`, `apply-map.py` with the frozen or forged map, then the
   counter with the same `--base-rev/--target/--map-sha256/--work`. Trees are built once and
   reused (byte-identical to the frozen script's trees; verified by the baseline below).
3. Detection basis: **per-control LIMB verdict vector** (M1..M8 pass/FAIL) plus rc. A mutant
   is *killed* by a control when that control's seven-limb vector or rc differs from the
   pristine counter's on the same tree. rc alone is the claim-level detector (`P1` reads
   `KNOWLEDGE-METER-RESULT pass rc=0`); limb-level differences are reported separately
   because several mutants change a limb without changing rc.
4. Baseline: the pristine counter on the frozen eight reproduces
   `.ufo/waves/round-88/controls/c1-controls-r88.txt` **exactly** — all 7 limbs on all 8
   controls, `BASELINE_MATCH=True`
   (`MutC1Counter-receipts/baseline-match.txt`). A baseline mismatch would have made every
   verdict below inconclusive; there is none.

### Control battery, pristine signature

Frozen eight (`F-*`):

| control | tree / map | pristine rc | failing limbs |
|---|---|---|---|
| do-nothing | clone(base), frozen map | 1 | M1 M2 M3 |
| positive | base+apply(frozen map) | 0 | — |
| partial | base+apply(first 25 keys) | 1 | M1 M2 M3 |
| pad | positive + 2 extra resolving cites | 1 | M1 M2 M3 |
| drift-forge | base+apply(map + `mission-control.md:41-45`) | 1 | M1 M8 |
| not-entry-forge | base+apply(map + `SOURCES.md`→`corpus/SOURCES.md`) | 1 | M1 M4 M5 |
| ufo-copy | base+apply(map, `claim-gates.md:32-33` → `.ufo/...`) | 1 | M4 M5 |
| map-sha | positive, frozen map, all-zero sha | 1 | M6 |

Added isolating controls (`N*`, all from clones of the same base; definitions and the exact
`--map/-sha256/--target` per control in `MutC1Counter-receipts/controls.txt`):

| control | what it isolates | pristine failing limbs |
|---|---|---|
| N1-drift-target | M8 alone: drift-forge tree/map/sha, `--target 743/1743` | M8 |
| N2-pos-denom | M1 denominator: positive tree, frozen map, `--target 742/1742` | M1 |
| N3-dups | M4 `bybase` clause: positive tree + tracked `corpus/notes/claim-gates.md` | M4 M5 |
| N4-ghost-key | key not present in base bytes (`claim-gates.md:200`) | M2 M3 M4 M5 M8 |
| N5-zero-anchor | `:0-3` anchor (as N4, still caught by M4) | M2 M3 M4 M5 M8 |
| N6-big-anchor | `:1-99999` anchor (as N4, still caught by M4) | M2 M3 M4 M5 M8 |
| N7-single-drift | excluded single-anchor drift key `claim-gates.md:3` | M2 M3 M8 |
| N8-trunc | M3 line-count (`citation-bases.md` last line dropped) | M1 M2 M3 |
| N9-slash-key | `corpus/../claim-gates.md` key | M2 M3 M4 M5 |
| N10-mixed-drift | M8 "EVERY citing line": `claim-gates.md:42-47` (share pattern True/False) | M2 M3 M8 |
| N11-deleted-entry | M4 `INTERNAL` clause: positive tree, `claim-gates.md` deleted from worktree, still tracked | M1 M2 M3 M4 M5 |
| N12-truncated-target | M5 upper bound: `claim-gates.md` cut to 12 lines, map key `:15` | M1 M2 M3 M5 |
| N13-dot-entry | KEY leading `.`: tracked `corpus/knowledge/.hidden.md` + map key `.hidden.md` | M2 M3 M4 M5 |
| N14-slash-anchored | KEY slash admission: map key `x/claim-gates.md:3` | M2 M3 M4 M5 |
| N15-word4-share | M8 WORD threshold: `claim-gates.md:59-61` needs a **4-char** identifier | M2 M3 M8 |

## Results — 36 mutants

Frozen killer abbreviations: DN=do-nothing, PO=positive, PA=partial, PD=pad, DF=drift-forge,
NE=not-entry-forge, UC=ufo-copy, MS=map-sha. `—` = none.

| mutant | round-88 construct mutated | frozen killers | added killers | verdict |
|---|---|---|---|---|
| m01 M1 `an==tn` (numerator only) | M1 | NE | N2 | killed |
| m02 M1 `True` | M1 | DN PA PD DF NE | N2 N11 N12 | killed |
| m03 `rate()` counts only INTERNAL | M1 | PO UC MS | 12 controls | killed |
| m04 M2 drop `removed==keys` | M2 | DN PA | N4 N5 N6 N7 N9 N10 N11 N12 N13 N14 N15 | killed |
| m05 M2 `removed<=keys` | M2 | DN PA | N4 N5 N6 N7 N9 N10 N13 N14 N15 | killed |
| m06 M2 drop `added<=vals` | M2 | PD | — | killed |
| m07 M3 skip the replacement | M3 | DN PO DF NE UC MS | N1 N2 N3 | killed |
| m08 M3 drop the line-count check | M3 | PD | — | killed |
| m09 M3 drop `hit==keys` | M3 | — | N4 N5 N6 N9 N14 | killed |
| m10 M4 drop `bybase.get(name)==[path]` | M4 (.ufo/ exclusion / sibling-entry binding) | — | N3 | killed |
| m11 M4 drop `bcls.get(k)=="GONE"` | M4 | — | N4 N5 N6 | killed |
| m12 M4 drop `classify(v)=="INTERNAL"` | M4 | — | N11 | killed |
| m13 M4 keep the anchor in `path` | M4 | DN PO PA PD DF MS | 7 controls | killed |
| **m14 M5 drop `1<=lo_i`** | M5 | — | — | **SURVIVED** |
| m15 M5 drop `hi_i<=nlines` | M5 | — | N12 | killed |
| m16 M5 `not m5bad and not m4bad` → `not m5bad` | M5 | NE UC | 8 controls | killed |
| m17 M6 `True` | M6 | MS | — | killed |
| **m18 M6 drop `.lower()`** | M6 | — | — | **SURVIVED** (stricter) |
| m19 M8 `True` | M8 | DF | N1 N4 N5 N6 N7 N10 N15 | killed |
| m20 M8 `any`→`all` (one line enough) | M8 all-lines rule | — | N10 | killed |
| m21 M8 slice `[lo-1:hi-1]` | M8 anchor slicing | DN PO PA PD NE UC MS | 8 controls | killed |
| m22 M8 WORD `{4,}`→`{3,}` | M8 idents/WORD | — | N15 | killed |
| m23 M8 WORD `{4,}`→`{5,}` | M8 idents/WORD | DN PO PA PD NE UC MS | 8 controls | killed |
| m24 M8 drop the PATHLIKE exclusion | M8 idents | DF | N1 N7 | killed |
| m25 M8 `cites[:1]` (first citing line only) | M8 all-lines rule | — | N10 | killed |
| m26 M8 skip single-line anchors | M8 | — | N4 N7 | killed |
| m27 M8 drop `not cites` | M8 | — | N4 N5 N6 | killed |
| m28 KEY without the anchor group | KEY regex | all 8 (uncaught `IndexError`: no LIMB/RESULT line, rc=1) | all 15 | killed |
| m29 KEY without the range group | KEY regex | all 8 (same crash) | all 15 | killed |
| m30 KEY admits `/` | KEY regex | — | N14 (M8 becomes stricter) | killed |
| **m31 KEY admits a leading `.`** | KEY regex | — | — | **SURVIVED** |
| **m32 scope `count("/")>=2`** | rev scope | — | — | **SURVIVED** |
| **m33 rev scope without the `.md` filter** | rev scope | — | — | **SURVIVED** |
| **m34 worktree scope without the `.md` filter** | worktree scope | — | — | **SURVIVED** |
| m35 drop the `.ufo/` exclusion (`if True`) | M4 `.ufo/` exclusion | DN PO PA PD DF MS | 7 controls | killed |
| **m36 `.ufo` prefix without the slash** | M4 `.ufo/` exclusion | — | — | **SURVIVED** |

Machine-readable form: `MutC1Counter-receipts/mutants.tsv` (sha256 + exact delta) and
`MutC1Counter-receipts/summary.json` (per-mutant × per-control rc and limb vector).

## Totals

- mutants: **36** (plus the pristine control row; 16+ required, 36 built)
- killed: **29**
  - killed by the **frozen eight** as frozen: **18**
  - killed **only** by the added isolating controls: **11**
    (m09, m10, m11, m12, m15, m20, m22, m25, m26, m27, m30)
- survived every control: **7** (m14, m18, m31, m32, m33, m34, m36)
  - equivalence (behaviour unreachable on the frozen base/tree): **6**
  - stricter-only mutation, no weakening: **1** (m18)
- No mutant that *weakens* the counter survives once the added controls are included.
- The frozen eight alone: **9/36** killed at rc granularity (`RESULT … rc`), **18/36** killed
  at limb granularity. Every weakening of M1, M2, M3, M4, M5, M6 or M8 survives the frozen
  eight at rc granularity except the two that crash the counter (m28/m29) and three that flip
  `positive` (m03, m07, m13/m21/m23/m35 family).

## Survivor analysis

- **m14 — M5 `1 <= lo_i` dropped (equivalent under the frozen base).** The clause is
  unreachable without changing the base revision: M4 already requires
  `bcls.get(k) == "GONE"`, i.e. the key must be a *collected base citation*, and no base line
  cites a `*.md:0` anchor (scanned: 0). A key that is not a base citation (N4/N5/N6) is
  already killed by M4, which is why N5's `:0-3` cannot isolate M5. Control that would kill
  it: a base revision citing `name.md:0-N` — not constructible from a fixed `--base-rev`;
  this is defence in depth, not a live gap.
- **m18 — M6 `.lower()` dropped (stricter, not weaker).** The mutant rejects an
  uppercase-hex `--map-sha256`; it can only turn passes into fails. The frozen pin is
  lowercase, so behaviour is identical on the frozen control. No defect.
- **m31 — KEY admits a leading `.` (equivalent under the frozen tree).** A dot-prefixed name
  must still satisfy `path == "corpus/knowledge/" + name`, `bybase[name] == [path]` and
  `bcls.get(k) == "GONE"`; `git ls-files corpus/knowledge/` tracks **0** dot-prefixed
  entries, and no base line cites one, so the widened KEY cannot accept anything. Control
  that would kill it: a base revision citing `.x.md` with a tracked `corpus/knowledge/.x.md`
  — N13's `.hidden.md` map key is still rejected at M4 because the key is not a base
  citation, so the mutant is indistinguishable.
- **m32 — `p.count("/") >= 2` (equivalent under the frozen tree).** `git ls-tree
  corpus/knowledge/` at base lists **99 blobs and 0 trees**, so no entry is nested deeper.
  Even if one were, `scope_files_tree()` is a non-recursive `listdir`, so the extra nested
  file would enter `bfiles` only, making `same_files` false and M3 fail — fail-closed.
- **m33 — rev scope without `.md` (equivalent under the frozen tree).** All 99 base scope
  entries are `.md` (`git ls-tree … | grep -vc '\.md$'` = 0). A non-`.md` entry would be
  filtered out on the worktree side, again making `same_files` false (fail-closed).
- **m34 — worktree scope without `.md` (equivalent under the frozen tree).** 0 non-`.md`
  files in `corpus/knowledge/`; a stray file would enter `afiles` only → `same_files` false
  (fail-closed).
- **m36 — `p.startswith(".ufo")` (equivalent).** `git ls-files | grep -c '^\.ufo[^/]'` = 0:
  no tracked path begins with `.ufo` and continues without `/`, so the looser prefix is
  byte-for-byte identical in classification.

## Routed findings (coverage of the frozen C1 control battery — not a re-score)

**F1 — the frozen battery never isolates M8 (and M1, M2, M3).** `drift-forge` fails M1 *and*
M8, so `m19` (M8 forced to `pass`) still produces `rc=1` on every frozen control; it is
killed only because M8's LIMB line flips, not because the control's expected outcome
changes. At the claim-level detector (`P1`: `RESULT pass rc=0`) an M8-disabling mutation
passes the whole frozen battery: `m19` is one of 27 rc-level survivors of the frozen eight. Re-runnable proof:
`MutC1Counter-receipts/evidence.txt` (`p00-pristine` vs `m19-m8-always` on `drift-forge`),
and the fix is one argument:
`--lane <drift tree> --map <drift.json> --map-sha256 <forged sha> --target 743/1743`
(N1: pristine fails M1-independent, M8 alone; m19 passes).

**F2 — 11/36 mutants escape the frozen eight.** The cheap, clone-only controls that kill
them are N2 (M1 denominator), N3 (M4 `bybase`), N10 (M8 all-lines), N11 (M4 `INTERNAL`),
N12 (M5 upper bound), N14 (KEY slash), N15 (M8 WORD threshold), plus N4/N5/N6/N7/N9 for the
M3-hit/M8-skip/M2-removed family. All are one-liners on top of the existing eight
(`controls.txt` has the exact `--map/--sha256/--target` per control); building them cost
< 3 s per control per counter.

**F3 — ghost keys are killed at M4, not at the limb under test.** Any forged key that is not
a *collected base citation* fails `bcls.get(k)=="GONE"`, so it can never exercise M5/M8 —
N4/N5/N6 all show `M4=FAIL`. Consequence for future counters: an isolating control for M5/M8
must be built on a key that really is cited in the base bytes (as N10, N12, N15 are), or it
tests M4 only. Worth stating in the round-89 counter docstring so the next attempt does not
assume an anchor-forgery control isolates M5.

**F4 — `m28`/`m29` (KEY group removal) are killed by a crash, not by a limb.** With a group
removed, `km.group(2)` raises `IndexError`; the counter prints a traceback, **no** `LIMB`
line and **no** `KNOWLEDGE-METER-RESULT` line, and exits 1. That is fail-closed for `P1`
(a missing RESULT line is not `pass`), but it breaks the counter's own exit-code contract
(usage/read errors are `rc=2`, limb failures `rc=1`). Minor qualifier, no action required for
this landing.

**F5 — M5's `lo_i` guard is currently dead code** (m14) — harmless defence in depth; keep
it, but do not claim M5 coverage from it.

Not a defect: `M4`'s `bybase` clause makes the `/` and leading-`.` widenings of KEY
unreachable (m30 is observable only as a *stricter* M8, m31 is unreachable); the `.ufo/`
exclusion's exact trailing slash is redundant (m36).

## Restoration and hygiene evidence

- Frozen counter sha256 before the sweep and after all 36 mutants:
  `b4127597…c98b55` — identical (`MutC1Counter-receipts/mutants.tsv` header column;
  `baseline-match.txt` line 3).
- The counter was never copied, edited or executed in place; every mutant is a separate file
  in scratch, named `mut/mNN-*.py`, with `old`/`new` recorded.
- No lane file outside `.ufo/waves/round-88/w1/` was written by this seat (`git status` in
  the lane shows only other seats' changes and the w1 wave dir). No git/jj state was written
  in the lane; the only index write was `git add` inside a scratch clone.
- No credential-shaped value exists in any file written here: receipts contain paths,
  counts, sha256 and code lines only (no X-Amz/X-Goog/sig=/AKIA/private-key material; the
  same is true of the map, whose values are `corpus/knowledge/*.md` paths).
- Scratch `/fast/scratch/hyaku/kasegi-r88/MutC1Counter/` deleted before yield.

## Reproducing any row

```bash
S=/fast/scratch/hyaku/kasegi-r88/MutC1Counter; mkdir -p "$S"; TMPDIR=$S
git clone -q --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin "$S/pos"
git -C "$S/pos" checkout -q 6beead9148945fa695cf3139e8fc9d8e91cc5fd0
python3 -B .ufo/waves/round-88/c1/apply-map.py --root "$S/pos" \
  --map .ufo/waves/round-88/c1/repair-map.json
# mutant = the frozen counter with the single old->new pair from mutants.tsv
python3 -B "$S/mut/mNN-name.py" --lane "$S/pos" \
  --base-rev 6beead9148945fa695cf3139e8fc9d8e91cc5fd0 \
  --map <map.json> --target 742/1743 --map-sha256 <sha> --work "$S/w"
```
`MutC1Counter-receipts/MutC1Counter-harness.py` rebuilds the trees, all 36 mutants and the
full verdict matrix; `MutC1Counter-summarize.py` regenerates the table from the per-run
outputs.

## Files written

- `.ufo/waves/round-88/w1/MutC1Counter.md` (this report)
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/baseline-match.txt`
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/controls.txt`
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/mutants.tsv`
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/summary.json`
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/evidence.txt`
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/MutC1Counter-harness.py`
- `.ufo/waves/round-88/w1/MutC1Counter-receipts/MutC1Counter-summarize.py`
