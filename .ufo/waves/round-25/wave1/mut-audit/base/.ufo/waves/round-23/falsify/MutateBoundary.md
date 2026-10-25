# MutateBoundary — C1 prefix-boundary mutation probe (round 23)

Seat: `L1Kasegi23.MutateBoundary-2` (mutation-tester, leaf). Date: 2026-10-25.
Host: linux 7.2.11-arch1-1, Python 3.14.8. All writes confined to
`/tmp/kasegi-r23-falsify-MutateBoundary-2/`. No production file, lane tree, index, or
sibling artifact was touched; no tool was installed, upgraded, or configured.

## 0. Pins, and the fact that they moved three times

The C1 instrument set was edited by other seats while I probed. Every result below is
measured on the **tested pin**; the byte-comparison against the live tree is stated
explicitly. Line numbers throughout refer to the tested pin.

| pin | `resolve.py` | fixtures | checker | note |
|---|---|---|---|---|
| tested | `8dd45bc8d9aedbb25247a64fbd6094a1b9e7b9a3b3facdb58001c59ef3868848` (590 ln) | `4e39f65c…` | `53742c8d…` | 20 cases, 9 escape / 11 control; **20/20 PASS** |
| live at write | `fce5b84be4cece914260f03a3a8b739dc1108381f97482bbfc7b22143810a4b0` (593 ln) | `332a5fe9…` | `53742c8d…` | 23 cases, 11 escape / 12 control; **23/23 PASS**; mutant A re-run gives the identical flip set (21/23) |

Between the tested and live pins the matrix gained `relative-priority-lane-first-control`,
`mirror-root-prefix-sibling-escape`, `absolute-parent-traversal`, and a strengthened
`glob-expansion-escape` whose note records that a bare `<name>.md` glob "cannot cross `/`
and would pass on baseline too" — the same masking pattern F2 describes.

`diff` tested→live is one hunk at `classify`'s bounty fallback: a 3-line comment plus
root-only bounty citations no longer earning mirror credit
(`exists_any(join(mirror_root, suffix) if suffix else mirror_root)` →
`exists_any(join(mirror_root, suffix)) if suffix else (None, None)`). The boundary
(`bounty_suffix`, `classify`'s branch selection) and both `under_mirror()` calls are
byte-identical across the two pins, which is why A's result transfers; I re-ran it
rather than inferring it (receipts `0585fe72…` vs `dbab6711…`).

Earlier in the wave I also saw a 13-case matrix (`5e61a33e…`, class-only checker
`1bc2db10…`) and a schema-2 checker (`fc9550f0…`); `.ufo/waves/round-23/c1-{baseline,fixed}.json`
were rewritten at 03:43. Recorded so nobody mistakes my earlier numbers for current ones.

One false positive of my own, kept visible: pairing the **new** checker with my
**stale** 13-case fixtures gave `lane-relative-parent-internal-control FAIL
path_check=path-outside-internal` (12/13). It is a pin mismatch — the landed matrix
carries that lane-branch carve-out — and it disappears at 20/20 on matched pins.
Checker and matrix are version-coupled; the receipts' `matrix_sha256` is what exposes
a mismatched pair.

## 1. Assigned mutant (A)

The boundary decision is one expression, `resolve.py:234` (`suffix = bounty_suffix(base)`);
`bounty_suffix()` is `resolve.py:210-221`; `BOUNTY_PREFIXES` is `resolve.py:106`.
A reverts **only** that boundary/suffix derivation to the pre-fix form in
`.ufo/waves/round-23/c1-baseline-resolver.py` (`startswith(BOUNTY_PREFIXES)` +
`split("/Projects/bounties", 1)[1]`):

```diff
--- pristine3/resolve.py                (tested pin, sha256 8dd45bc8…)
+++ mutA3/resolve.py                    (sha256 39d0e720d66837c17dd92bfe6584e7ec7df8c96137a70a2780325e71a979993c)
@@ resolve.py:232-235
 def classify(tok, lane_root, mirror_root):
     base, anchor = strip_anchor(tok)
-    suffix = bounty_suffix(base)
+    suffix = (base.split("/Projects/bounties", 1)[1].lstrip("/")
+              if base.startswith(BOUNTY_PREFIXES) else None)
     if suffix is not None:
```

Both containment calls (`resolve.py:241` bounty fallback, `resolve.py:262` relative
fallback) are left intact, so A isolates the prefix boundary and is not a disguised
containment revert. `bounty_suffix()` stays defined but uncalled (unreachable by
construction). Rebuilt byte-identically from the pinned source by `rebuild3.py`.

Differential probe over the 20 fixture cites + 9 boundary neighbours: **5 diverged, all
prefix siblings, nothing else**, i.e. the mutation is the boundary and not a side effect:

```
~/Projects/bounties-legacy/README.md      pristine=None mutant='-legacy/README.md'
~/Projects/bounties-vault/a.json          pristine=None mutant='-vault/a.json'
~/Projects/bountiesary/x.md               pristine=None mutant='ary/x.md'
/home/vgpnk/Projects/bounties-legacy/a.md pristine=None mutant='-legacy/a.md'
/home/vgpnk/Projects/bountiesz/b.md       pristine=None mutant='z/b.md'
```

## 2. Detector replay

Command (per directory; `--json` tag varies):

```
cd /tmp/kasegi-r23-falsify-MutateBoundary-2/<dir> \
  && python3 ../pristine3/check.py --resolver ./resolve.py \
       --fixtures ../pristine3/fixtures.json --json ./receipt-main.json
```

| run | pass/fail | flipped cases (expect → mutant) |
|---|---|---|
| tested pin, unmutated (`8dd45bc8…`) | **20/0** | — |
| **A on tested pin (`39d0e720…`)** | **18/2** | `bounty-prefix-sibling-confusion`: GONE → MIRROR-EQUIVALENT; `absolute-prefix-sibling-confusion`: GONE → MIRROR-EQUIVALENT |
| live pin, unmutated (`fce5b84b…`) | **20/0** | — |
| **A on live pin (`b4669aa3…`)** | **18/2** | identical two cases |
| newest live pin, unmutated (`fce5b84b…` + 23-case matrix `332a5fe9…`) | **23/0** | — |
| **A on newest live pin (same `b4669aa3…`)** | **21/2** | identical two cases (`path_check=gone-with-path` on both) |

**Verdict: killed** — twice, once per spelling of the bounty root (tilde and absolute).
Every control, every traversal case, both relative escapes and both expansion escapes
are unchanged.

Path-level trace on the tested pin (`probe_trace3.py`, isolated `HOME` = case home, the
same environment the CLI sees; `classify` returns class/domain as its 4th field):

```
CASE bounty-prefix-sibling-confusion
  cite=~/Projects/bounties-legacy/README.md:1
  pristine classify=('GONE', '', '', 'other')
  mutantA  classify=('MIRROR-EQUIVALENT', '<root>/relocated/tbh/-legacy/README.md', 'literal', 'bounty')
CASE absolute-prefix-sibling-confusion
  cite=/home/vgpnk/Projects/bounties-legacy/README.md:1
  pristine classify=('GONE', '', '', 'other')
  mutantA  classify=('MIRROR-EQUIVALENT', '<root>/relocated/tbh/-legacy/README.md', 'literal', 'bounty')
CASE literal-prefix-sibling-control
  cite=~/Projects/bounties-legacy/README.md:1
  pristine classify=('RESOLVES', '<root>/home/Projects/bounties-legacy/README.md', 'literal', 'other')
  mutantA  classify=('RESOLVES', '<root>/home/Projects/bounties-legacy/README.md', 'literal', 'bounty')
```

The credited decoy is *inside* the mirror (`under_mirror` true), so containment cannot
see this defect; the literal control keeps its class while only its domain flips.

## 3. Are `literal-prefix-sibling-control` and `bounty-prefix-sibling-confusion` discriminated by this mutation alone?

**One-sidedly. The escape case is a live witness; the control is inert.**

- Class level: escape FAIL vs control PASS → the run separates them, and all separating
  power sits on the escape side.
- The control's verdict is produced at `resolve.py:237-239` (`exists_any(base)`), which
  runs **before** the mutated fallback at `resolve.py:240-243`. A cannot reach it.
- A's only observable on the control is `domain` `other`→`bounty` (trace above).
  The checker reads `citation`, `class`, and `resolved_path`
  (`mirror-containment-check.py:120-137`); `domain` is emitted at `resolve.py:338` but
  never compared. So even the one signal that moves is unasserted.
- The two cases are not independent inputs: both cite the identical string
  `~/Projects/bounties-legacy/README.md` and differ only in filesystem layout. That is
  why the control moves only under a literal-branch mutation (C below) — the pair
  witnesses literal-hit precedence, not boundary exactness.
- The live matrix now also carries `absolute-prefix-sibling-confusion`, so the *claim*
  no longer rests on a single case; the *control* is still boundary-blind.

## 4. Attribution probes (same harness; A is the only assigned mutant)

Each row is one independent change from the tested pin against the 20-case matrix
(9 escape / 11 control); containment is kept unless the
row says otherwise. `pin` = tested / live.

| id | change | resolver sha256 (12) | pass/fail (20) | flips |
|---|---|---|---|---|
| A | boundary → `startswith`+`split` | `39d0e720d668` | 18/2 | tilde + absolute sibling confusion |
| J | boundary loosened on the tilde arm only | `27f6c4bd8cbe` | 19/1 | tilde sibling only (absolute arm stays exact) |
| D | bounty-fallback `under_mirror` dropped | `1f72a5df2de9` | 16/4 | both traversal cases, bounty symlink escape, brace-expansion escape |
| E | relative-fallback `under_mirror` dropped | `2d2dcb4edac1` | 18/2 | both relative escapes |
| B | A + D | `5a1fd64a9582` | 14/6 | exactly A ∪ D (6 cases, no interaction) |
| C | A + literal-hit branch suppressed | `01870941cfeb` | 15/5 | both sibling escapes + `literal-prefix-sibling-control` + both literal carve-outs (`bounty-literal-present-traversal`, `bounty-literal-symlink-present`) |
| F | `classify` returns GONE always | `a2f53034a117` | 11/9 | 9 controls (all MIRROR-EQUIVALENT, INTERNAL, RESOLVES controls) |
| G | `BOUNTY_PREFIXES` loses `/home/vgpnk/Projects/bounties` | `2d06d656eba4` | 19/1 | `absolute-bounty-fallback-control` |
| H | `BOUNTY_PREFIXES` loses `~/Projects/bounties` | `d3ac99b9d422` | 18/2 | `confined-bounty-fallback-control`, `brace-expansion-confined-control` |
| K | boundary admits `root + "_"` siblings | `eedc6effe307` | **20/0 (SURVIVED)** | none |

Decoy-removal variant (`fixtures3-nodecoy.json`, sha256 `d362073f…`, the
`bounty-prefix-sibling-confusion` `files` emptied): A scores **19/1** — still killed by
`absolute-prefix-sibling-confusion`, so the tilde decoy is no longer the sole detector.

## 5. Findings (falsifiable)

1. **F1 — A is killed twice.** Reverting the exact-root boundary is observed by
   `bounty-prefix-sibling-confusion` and `absolute-prefix-sibling-confusion` — 18/20 on
   the tested pin, 21/23 on the newest live pin, same two cases both times.
   Falsifier: any additional flip, or either case passing — receipts
   `dbab6711…` (tested), `0585fe72…` (live 20), `16cdbf3b…` (live 23).
2. **F2 — boundary coverage is redundant across spellings, but each spelling is
   load-bearing.** Loosening only the tilde arm (J) leaves the absolute sibling green;
   deleting only the tilde decoy (nodecoy) still leaves a killing witness. Falsifier: J
   flipping the absolute case, or A-on-nodecoy reaching 20/20.
3. **F3 — the paired literal control cannot detect boundary regressions.** Identical
   class under pristine and A; it moves only when the literal branch is mutated (C). The
   `domain` flip A induces is emitted (`resolve.py:338`) but unasserted
   (`mirror-containment-check.py:120-137`). Falsifier: a boundary-only mutant that flips
   `literal-prefix-sibling-control`.
4. **F4 — boundary and containment are orthogonal, and separately witnessed.** D (4
   flips) and E (2 flips) are disjoint; B's 6 flips are exactly A ∪ D; A's decoy is
   inside the mirror (`under_mirror` true). Falsifier: a containment-only mutant
   flipping a sibling case, or B ≠ A ∪ D.
5. **F5 — the matrix is not GONE-collapsible.** A GONE-everything `classify` scores
   11/20 with all 9 failures on controls. Falsifier: F reaching 20/20.
6. **F6 — residual narrow hole: only one non-`/` continuation spelling is pinned.** K
   (admits `root + "_"` siblings) survives 20/20 and dies only on a probe case I added
   (21st): cite `~/Projects/bounties_legacy/README.md:1` with a decoy at
   `<mirror>/legacy/README.md` (variant sha256 `e693c305…`; pristine 21/21 PASS, K
   20/21 FAIL). So "reject sibling-root prefix confusion" is evidenced for `-x`
   siblings, not for arbitrary continuations. The current code is not wrong on these
   inputs — it is the *general* property that is unwitnessed, and closing it costs one
   fixture case. Falsifier: any frozen case flipping under K.
7. **F7 — pin coupling is load-bearing.** The receipts now pin resolver + matrix +
   checker; a checker/matrix mismatch silently mis-scores a control (my §0 false
   positive, reproduced from a stale pair). Falsifier: reproducing 20/20 from a
   receipt's three hashes while substituting any one file from an earlier pin.

## 6. Restoration evidence

- The pristine copies were never mutated. Verified at write time:
  `pristine3/resolve.py` sha256 == the tested pin, `pristine4/resolve.py` == the live
  tree, and fixtures `4e39f65c…` / checker `53742c8d…` equal the live tree for both.
- Every mutant was rebuilt from the pinned source by `rebuild3.py` and its sha256
  matches the `resolver_sha256` recorded inside its own receipt (A `39d0e720…`,
  B `5a1fd64a…`, C `01870941…`, D `1f72a5df…`, E `2d2dcb4e…`, F `a2f53034…`,
  G `2d06d656…`, H `d3ac99b9…`, J `27f6c4bd…`, K `eedc6eff…`). No scratch file under
  test was left carrying an unrecorded mutation.
- Determinism: the tested pin was replayed twice (20/20 both times, same case map);
  the live resolver was replayed on both live matrix revisions (20/20 and 23/23), and A
  on it flipped the same two cases each time.
- Mid-wave edits to `resolve.py`, `mirror-containment-check.py`, and the fixture file
  were made by other seats (mtimes 03:42-03:47), not by me; I re-pinned and re-ran
  instead of reverting them.

## 7. Scope limits

- Detector-only: class plus `resolved_path`/carve-out verdicts over 20 tested-pin cases,
  23 live-pin cases, and 3 probe variants. Nothing here speaks to source availability,
  quote fidelity, C2 (F06-F08), or any score.
- One mutation point per mutant; only A is the assigned probe. J, K, B-H and the two
  variants are attribution/coverage controls and are labelled as such.
- `domain` is unasserted, so all domain statements rest on the direct trace in §2.
- The absolute-form cases are host-dependent by fixture design (they require
  `/home/vgpnk/Projects/bounties*` absent on the run host — verified absent here with
  `ls`); those results do not transfer to a host that has those paths.
- K's probe case is mine, not frozen: it is evidence about the matrix's generality, not
  a defect report against `resolve.py`.
- Single execution per mutant (pristine repeated). No statistical claim; a live-tree
  edit after 03:48 would invalidate the "live at write" row only.

## 8. Reproduction

```
SCR=/tmp/kasegi-r23-falsify-MutateBoundary-2
SRC=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments
mkdir -p $SCR/pristine3
cp $SRC/resolve.py $SCR/pristine3/resolve.py
cp $SRC/mirror-containment-fixtures.json $SCR/pristine3/fixtures.json
cp $SRC/mirror-containment-check.py $SCR/pristine3/check.py
python3 $SCR/rebuild3.py            # 10 mutants from pristine3/resolve.py
python3 $SCR/run_final.py           # pristine3/4 + A,B,C,D,E,F,G,H,J,K + nodecoy
python3 $SCR/probe_trace3.py        # per-case classify trace (sets HOME per case)
python3 $SCR/probe_diff.py          # boundary-only divergence set
```

`rebuild3.py [SRC] [SUFFIX]` takes any pinned resolver and emits
`mut{A,B,C,D,E,F,G,H,J,K}<SUFFIX>/resolve.py`, asserting every anchor occurs once.

Receipt hashes (tested pin): pristine `f64029cc…`, A `dbab6711…`, B `ed699772…`,
C `ba68f628…`, D `ffebca4f…`, E `fe69b73a…`, F `e34a7c71…`, G `db7c4489…`,
H `2c4faa4b…`, J `92052823…`, K `124ab39c…`, A-nodecoy `731ec2be…`,
K-nodecoy `d9c92af6…`, pristine-underscore2 `d48074ef…`, K-underscore2 `5e61305e…`.
Live pin: pristine `c4636e30…`, A `0585fe72…`. Newest live pin (23 cases):
pristine `29562c84…`, A `16cdbf3b…`.
