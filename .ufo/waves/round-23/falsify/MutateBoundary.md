# MutateBoundary — C1 prefix-boundary mutation probe (round 23)

Seat: `L1Kasegi23.MutateBoundary-2` (mutation-tester, leaf). Date: 2026-10-25.
Host: linux 7.2.11-arch1-1, Python 3.14.8. All writes confined to
`/tmp/kasegi-r23-falsify-MutateBoundary-2/`. No production file, lane tree, index,
or sibling artifact was touched; no tool was installed, upgraded, or configured.

Pins for every result below — re-verified against `corpus/instruments/` at write time
(they are byte-identical to my scratch snapshots `pristine3/`):

| artifact | sha256 |
|---|---|
| `corpus/instruments/resolve.py` | `8dd45bc8d9aedbb25247a64fbd6094a1b9e7b9a3b3facdb58001c59ef3868848` |
| `corpus/instruments/mirror-containment-fixtures.json` | `4e39f65c7c1bdc7d6a390f0aeefe5fa88af67ea84659aa9ff36b84d271c2400b` |
| `corpus/instruments/mirror-containment-check.py` | `53742c8d9529dffb8c40c39b3448de7388b774b548d7831670598d5534bff5d1` |

Frozen matrix at this pin: **20 cases, 9 escape / 11 control**; baseline replay
**20/20 PASS** (`pristine3/receipt-main.json`, sha256 `b669a64c…`).

## 0. The artifact set moved twice while I probed (observation, not a claim)

Three distinct instrument sets appeared between 03:35 and 03:45: the 13-case
matrix `5e61a33e…` with class-only checker `1bc2db10…` and resolver `ed9a9dae…`; a
schema-2 checker `fc9550f0…`; then the live pair above. `.ufo/waves/round-23/c1-{baseline,fixed}.json`
were both rewritten at 03:43. I re-pinned and re-ran rather than reporting the
superseded pin.

One false-positive of my own, recorded so it is not mistaken for a finding: pairing the
**new** checker with my **stale** 13-case fixtures copy produced
`lane-relative-parent-internal-control FAIL path_check=path-outside-internal` (12/13).
That red is a matrix/checker version mismatch — the landed fixtures carry the
lane-branch carve-out — and it vanishes on matched pins (20/20). Checker and matrix
must be pinned together; the receipts' `matrix_sha256` is what makes that detectable.

## 1. Assigned mutant (A)

The boundary decision is one expression, `resolve.py:234` (`suffix = bounty_suffix(base)`);
`bounty_suffix()` is `resolve.py:210-221`. A reverts **only** that boundary/suffix
derivation to the pre-fix form from `.ufo/waves/round-23/c1-baseline-resolver.py`
(`startswith(BOUNTY_PREFIXES)` + `split("/Projects/bounties", 1)[1]`):

```diff
--- pristine3/resolve.py
+++ mutA3/resolve.py              (sha256 39d0e720d66837c17dd92bfe6584e7ec7df8c96137a70a2780325e71a979993c)
@@ resolve.py:232-235
 def classify(tok, lane_root, mirror_root):
     base, anchor = strip_anchor(tok)
-    suffix = bounty_suffix(base)
+    suffix = (base.split("/Projects/bounties", 1)[1].lstrip("/")
+              if base.startswith(BOUNTY_PREFIXES) else None)
     if suffix is not None:
```

Both `under_mirror()` calls (`resolve.py:244`, `resolve.py:264`) are left intact, so A
isolates the prefix boundary and is not a disguised containment revert.
`bounty_suffix()` remains defined but uncalled (unreachable by construction).
Differential probe over 20 fixture cites + 9 boundary neighbours: 5 diverged, all
prefix siblings — the mutation is the boundary and nothing else:

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
| pristine (`8dd45bc8…`) | **20/0** | — |
| **A (`39d0e720…`)** | **18/2** | `bounty-prefix-sibling-confusion`: GONE → MIRROR-EQUIVALENT; `absolute-prefix-sibling-confusion`: GONE → MIRROR-EQUIVALENT |

**Verdict: killed** — two independent cases observe it, one per spelling of the
bounty root (tilde and absolute). Every control, every traversal case, both relative
escapes, and both expansion escapes are unchanged.

Path-level trace on live bytes (`probe_trace3.py`, isolated `HOME` = case home, the
same environment the CLI sees; `classify` returns class/domain as 4th field):

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
see this defect, and the literal control keeps its class while its domain flips.

## 3. Are `literal-prefix-sibling-control` and `bounty-prefix-sibling-confusion` discriminated by this mutation alone?

**One-sidedly, and the control carries no boundary information.**

- Class level: escape FAIL vs control PASS → the run separates them. All separating
  power sits on the escape side.
- The control's verdict is produced at `resolve.py:237-239` (`exists_any(base)`), which
  runs **before** the mutated fallback (`resolve.py:243-245`). A cannot reach it.
- The only observable A produces on the control is the `domain` field `other`→`bounty`
  (trace above). The checker asserts `citation`, `class`, and `resolved_path`
  (`mirror-containment-check.py:120-134`); `domain` is written at `resolve.py:341` but
  never compared. So even the one signal that moves is unasserted.
- The two cases are also not independent inputs: both cite the identical string
  `~/Projects/bounties-legacy/README.md` and differ only in filesystem layout — which is
  why the control flips only under a literal-branch mutation (C: `RESOLVES`→`GONE`).
  The pair witnesses literal-hit precedence, not boundary exactness.
- Live matrix now has a second, differently spelled witness
  (`absolute-prefix-sibling-confusion`), so the *claim* no longer rests on one case; the
  *control* is still inert.

## 4. Attribution probes (same harness and matrix; A is the assigned mutant)

Each row is a single independent change from the live resolver; every one keeps
`under_mirror()` unless stated.

| id | change | resolver sha256 (12) | pass/fail (20) | flips |
|---|---|---|---|---|
| A | boundary → `startswith`+`split` | `39d0e720d668` | 18/2 | tilde + absolute sibling confusion |
| J | boundary loosened on tilde arm only | `27f6c4bd8cbe` | 19/1 | tilde sibling only (absolute arm exact) |
| D | bounty-fallback `under_mirror` dropped | `1f72a5df2de9` | 16/4 | 2 traversal + bounty symlink escape + brace-expansion escape |
| E | relative-fallback `under_mirror` dropped | `2d2dcb4edac1` | 18/2 | both relative escapes |
| B | A + D | `5a1fd64a9582` | 14/6 | exactly A ∪ D (no interaction) |
| C | A + literal-hit branch suppressed | `01870941cfeb` | 15/5 | both sibling escapes + `literal-prefix-sibling-control` + both literal carve-outs (`bounty-literal-present-traversal`, `bounty-literal-symlink-present`) |
| F | `classify` returns GONE always | `a2f53034a117` | 11/9 | 9 controls (all MIRROR-EQUIVALENT, INTERNAL, RESOLVES controls) |
| G | `BOUNTY_PREFIXES` loses `/home/vgpnk/Projects/bounties` | `2d06d656eba4` | 19/1 | `absolute-bounty-fallback-control` |
| H | `BOUNTY_PREFIXES` loses `~/Projects/bounties` | `d3ac99b9d422` | 18/2 | `confined-bounty-fallback-control`, `brace-expansion-confined-control` |
| K | boundary admits `root + "_"` siblings | `eedc6effe307` | **20/0 (SURVIVED)** | none |

A-on-decoy-removed variant (`fixtures3-nodecoy.json`, sha256 `d362073f…`, the
`bounty-prefix-sibling-confusion` `files` emptied): **19/1** — A still killed by the
absolute sibling, so the tilde witness is no longer the sole detector.

## 5. Findings (falsifiable)

1. **F1 — A is killed, twice.** Reverting the exact-root boundary is observed by
   `bounty-prefix-sibling-confusion` and `absolute-prefix-sibling-confusion` (18/20).
   Falsifier: any additional flip, or either case passing — receipt `dd5d918f…`.
2. **F2 — the boundary coverage is now redundant across spellings, but each spelling is
   necessary.** Dropping only the tilde arm (J) leaves the absolute sibling green;
   removing only the tilde decoy (nodecoy) leaves the absolute witness. Falsifier: J
   flipping the absolute case, or nodecoy A passing 20/20.
3. **F3 — the literal control is boundary-blind.** Identical class under pristine and A;
   only a literal-branch mutation moves it (C). The `domain` flip A induces is written
   (`resolve.py:341`) but unasserted (`mirror-containment-check.py:120-134`). Falsifier:
   a boundary-only mutant that flips `literal-prefix-sibling-control`.
4. **F4 — boundary and containment are orthogonal.** D (4 flips) and E (2 flips) are
   disjoint; B's 6 flips equal A ∪ D exactly; A's decoy is inside the mirror
   (`under_mirror` true). Falsifier: a containment-only mutant flipping a
   prefix-sibling case, or B ≠ A ∪ D.
5. **F5 — the matrix is not GONE-collapsible.** A GONE-everything `classify` fails 9 of
   20 (11/20), all on controls. Falsifier: F reaching 20/20.
6. **F6 — residual narrow hole: the boundary is tested for one non-`/` continuation.**
   K (admits `root + "_"` siblings) survives 20/20, and dies only on a probe case I
   added (21st): `~/Projects/bounties_legacy/README.md` with a decoy at
   `<mirror>/legacy/README.md` (sha256 `e693c305…`; pristine 21/21 PASS, K 20/21 FAIL).
   So "reject sibling-root prefix confusion" is witnessed for `-x` siblings, not for
   arbitrary non-`/` continuations. Scope: contrived one-separator mutant; closing it is
   one fixture case, and the current code is not wrong on these inputs — it is the
   *general* property that is unwitnessed. Falsifier: an existing case flipping under K.
7. **F7 — receipt/live-bytes coupling.** The C1 receipts now pin resolver `8dd45bc8…` +
   matrix `4e39f65c…` + checker `53742c8d…`; a checker/matrix mismatch silently
   mis-scores a control (my §0 false positive). Falsifier: reproducing 20/20 from the
   receipt's three hashes while mixing either file from an earlier pin.

## 6. Restoration evidence

- `mutA3/resolve.py` exists only as a probe; the pristine copy was never mutated.
  Re-verified: `pristine3/resolve.py` sha256 == live `corpus/instruments/resolve.py`
  sha256 == `8dd45bc8…`; fixtures `4e39f65c…`, checker `53742c8d…` also equal live.
- No scratch file under test was left mutated: every mutant lives in its own
  `mut<id>3/` directory alongside an untouched `pristine3/`; the assigned mutation was
  applied once to `mutA3/` and reproduced byte-identically from `pristine3/` in a second
  pass (same `39d0e720…`).
- Determinism: pristine replayed at each of the three pins with the same case map; live
  pin replayed twice (20/20 both times).
- The mid-wave changes to `resolve.py`, `mirror-containment-check.py`, and the fixture
  file were made by other seats (mtimes 03:42–03:43), not by me; I re-pinned and re-ran
  instead of reverting them.

## 7. Scope limits

- Detector-only: class + `resolved_path`/carve-out verdicts for 20 frozen cases (+2
  probe variants). No statement about source availability, quote fidelity, C2
  (F06-F08), or any score.
- One mutation point per mutant; A is the assigned probe, J-K and the variants are
  attribution/coverage controls and are labelled as such.
- `domain` is unasserted, so domain statements rest only on the direct trace in §2.
- The absolute-form cases are host-dependent by fixture design (they require
  `/home/vgpnk/Projects/bounties*` to stay absent on the run host — verified absent here
  via `ls`); results using them do not transfer to a host that has those paths.
- `K`'s probe case is mine, not frozen; it is evidence about the matrix's generality,
  not a defect report against the resolver.
- Single execution per mutant; pristine repeated. No statistical claim.

## 8. Reproduction

```
SCR=/tmp/kasegi-r23-falsify-MutateBoundary-2
SRC=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments
mkdir -p $SCR/pristine3 && cp $SRC/{resolve.py,mirror-containment-fixtures.json,mirror-containment-check.py} $SCR/pristine3/
mv $SCR/pristine3/mirror-containment-fixtures.json $SCR/pristine3/fixtures.json
mv $SCR/pristine3/mirror-containment-check.py $SCR/pristine3/check.py
python3 $SCR/rebuild3.py          # applies the §1/§4 edits, asserting 1 occurrence each
python3 $SCR/run_all3.py          # baseline + A..H + nodecoy
python3 $SCR/run_jk.py            # arm-separated (J), sibling-class (K), underscore probe
```

Receipt hashes (live pin): pristine `b669a64c…`, A `dd5d918f…`, B `5c16c8be…`,
C `c1c4c2e1…`, D `0dcf1b47…`, E `75ba2380…`, F `e79fbd21…`, G `1d22ea60…`,
H `1eaf90ef…`, J `72981593…`, K `82cebb06…`, A-nodecoy `4d45e217…`,
K-nodecoy `c7b514e1…`, pristine-underscore2 `d48074ef…`, K-underscore2 `5e61305e…`.
