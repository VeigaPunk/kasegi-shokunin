# MutateBoundary — C1 prefix-boundary mutation probe (round 23)

Seat: `L1Kasegi23.MutateBoundary-2` (mutation-tester, leaf).
Date: 2026-10-25. Host: linux 7.2.11-arch1-1, Python 3.14.8.
Target under test (read-only): `corpus/instruments/resolve.py`
(`sha256 ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9`),
`corpus/instruments/mirror-containment-fixtures.json`
(`sha256 5e61a33ed5fa530547aff197fad9380d86d5850374bbb4f2a8f99df44b5e76a9`),
`corpus/instruments/mirror-containment-check.py` (`sha256 1bc2db10dfbc59ef863e68afce475cd1d317da517137922804d7fc09cd46cecb`).
Scratch (all writes): `/tmp/kasegi-r23-falsify-MutateBoundary-2/`.

I read `resolve.py:89-263`, `mirror-containment-check.py:29-215`, the full frozen
matrix, `.ufo/waves/round-23/c1-baseline-resolver.py`, and the two receipts before
mutating. No production file, lane tree, index, or sibling artifact was modified;
no tool was installed or upgraded (no package transaction was attempted).

## 1. Assigned mutant (A): pre-fix boundary in `bounty_suffix`'s call site

The boundary decision lives in one expression, `resolve.py:225` (pristine):
`suffix = bounty_suffix(base)`; `bounty_suffix()` itself is `resolve.py:201-213`.
The assigned mutation reverts only that boundary/suffix derivation to the pre-fix
form (`.ufo/waves/round-23/c1-baseline-resolver.py`, `classify` body):

```diff
--- pristine/resolve.py
+++ mutA/resolve.py
@@ -222,7 +222,8 @@
 def classify(tok, lane_root, mirror_root):
     base, anchor = strip_anchor(tok)
-    suffix = bounty_suffix(base)
+    suffix = (base.split("/Projects/bounties", 1)[1].lstrip("/")
+              if base.startswith(BOUNTY_PREFIXES) else None)
     if suffix is not None:
         dom = "bounty"
```

`under_mirror()` calls are left in place on both fallbacks, so this mutation
isolates the *prefix boundary* alone and does not double as the containment revert.
`bounty_suffix()` remains defined but uncalled (unreachable by design of the mutant).
Bytes: `mutA/resolve.py` = `13cdb2cf39f9ac8df69c8f4875876c958ac19533f5f32173473ce529a82fce9e`
(reproduced byte-identically in `mutT/` by a second, independent edit pass).

Differential probe (`probe_diff.py`) over the 13 fixture cites plus 9 boundary
neighbours: **20 probed, 5 diverged**, all prefix siblings, and nothing else —
i.e. the mutation is exactly the boundary and not a side effect:

```
~/Projects/bounties-legacy/README.md      pristine=None mutant='-legacy/README.md'
~/Projects/bounties-vault/a.json          pristine=None mutant='-vault/a.json'
~/Projects/bountiesary/x.md               pristine=None mutant='ary/x.md'
/home/vgpnk/Projects/bounties-legacy/a.md pristine=None mutant='-legacy/a.md'
/home/vgpnk/Projects/bountiesz/b.md       pristine=None mutant='z/b.md'
```

## 2. Detector replay: pristine, mutant A, restored

Command (identical for every run; only `--resolver`/`--fixtures`/`--json` vary):

```
cd /tmp/kasegi-r23-falsify-MutateBoundary-2/<dir> \
  && python3 ../pristine/check.py --resolver ./resolve.py \
       --fixtures ../pristine/fixtures.json --json ./receipt-<tag>.json
```

| run | resolver sha256 (12) | pass/fail | flips vs pristine |
|---|---|---|---|
| pristine | `ed9a9dae1002` | 13/0 | — |
| **A (assigned)** | `13cdb2cf39f9` | **12/1** | **`bounty-prefix-sibling-confusion: GONE → MIRROR-EQUIVALENT`** |
| A, restored | `ed9a9dae1002` | 13/0 | none (case-for-case equal to pristine) |

Mutant A output (excerpt, `mutA/receipt-mutA.json`):

```
bounty-parent-traversal            escape  expect=GONE             actual=GONE             PASS
bounty-parent-traversal-vault      escape  expect=GONE             actual=GONE             PASS
relative-mirror-fallback-escape    escape  expect=GONE             actual=GONE             PASS
bounty-fallback-symlink-escape     escape  expect=GONE             actual=GONE             PASS
relative-fallback-symlink-escape   escape  expect=GONE             actual=GONE             PASS
bounty-prefix-sibling-confusion    escape  expect=GONE             actual=MIRROR-EQUIVALENT FAIL
confined-bounty-fallback-control   control expect=MIRROR-EQUIVALENT actual=MIRROR-EQUIVALENT PASS
...
literal-prefix-sibling-control     control expect=RESOLVES         actual=RESOLVES         PASS
cases=13 escape=6 controls=7 pass=12 fail=1
```

**Verdict for A: killed** (1 of 13 cases observes it), and only by
`bounty-prefix-sibling-confusion`. All 7 controls, all 5 other escapes, and the
two relative escapes are unchanged.

Path-level trace (`probe_trace.py`, isolated `HOME` = case home, same layout the CLI
sees):

```
CASE bounty-prefix-sibling-confusion  (HOME=/tmp/trace-xsv_5voe/home)
  cite=~/Projects/bounties-legacy/README.md:1
  pristine bounty_suffix=None literal=(None, None) classify=('GONE', '', '', 'other')
  mutantA  bounty_suffix=None literal=(None, None) classify=('MIRROR-EQUIVALENT',
             '/tmp/trace-xsv_5voe/relocated/tbh/-legacy/README.md', 'literal', 'bounty')
             under_mirror=True realpath=/tmp/trace-xsv_5voe/relocated/tbh/-legacy/README.md
CASE literal-prefix-sibling-control  (HOME=/tmp/trace-s521410_/home)
  cite=~/Projects/bounties-legacy/README.md:1
  pristine ... classify=('RESOLVES', '.../home/Projects/bounties-legacy/README.md', 'literal', 'other')
  mutantA  ... classify=('RESOLVES', '.../home/Projects/bounties-legacy/README.md', 'literal', 'bounty')
             under_mirror=False
```

Two structural facts follow directly: (a) the defect is not a containment escape —
the decoy sits *inside* the mirror, so `under_mirror()` reports `True` and cannot see
it; (b) both cases share the identical citation string
(`mirror-containment-fixtures.json:55` and `:91`) and differ only in layout.

## 3. Are `literal-prefix-sibling-control` and `bounty-prefix-sibling-confusion` discriminated by this mutation alone?

**Only one-sidedly, and the control contributes no boundary discrimination.**

- Class level: the escape case flips GONE→MIRROR-EQUIVALENT while the control stays
  RESOLVES→RESOLVES. So the mutant run separates them — but all of the separating
  power is on the escape side; the control is *invariant* under the boundary mutation.
- Mechanism: the control's verdict is produced by `exists_any(base)` before the
  mutated mirror-fallback clause runs (`resolve.py:229-233`). It therefore observes
  literal precedence, not boundary exactness. Its only observable change under the
  mutation is the **domain** label (``other`` → ``bounty``), and the checker compares
  `class` only (`mirror-containment-check.py:126-133` indexes `citation` and `class`
  in the TSV header written at `resolve.py:329`, which does carry a `domain` column).
- Witness in the other direction (mutant C = A + literal hit suppressed:
  `m, p = (None, None)` at `resolve.py:229`): 2 flips —
  `bounty-prefix-sibling-confusion` **and** `literal-prefix-sibling-control:
  RESOLVES → GONE`. So the control does load-bear, but for the literal branch, not
  for the boundary.
- They are not independent inputs (same citation string, layout-only difference), so
  the pair cannot establish "prefix siblings are treated as ordinary other roots";
  it establishes only literal-hit precedence over the mirror fallback.

Consequence for C1 verifiability: the claim's `reject sibling-root prefix confusion`
clause rests on exactly one case, and the paired control is inert to it.

## 4. Supplementary attribution probes (same harness, same matrix)

Each mutant is a single additional change from pristine; every one keeps
`under_mirror()` unless stated. Full diffs are reproducible from the pristine copy.

| id | single change | sha256 (12) | pass/fail | flips |
|---|---|---|---|---|
| A | boundary → `startswith` + `split` | `13cdb2cf39f9` | 12/1 | prefix-sibling-confusion |
| B | A + bounty-fallback `under_mirror` dropped | `ad309e0570a8` | 9/4 | A's flip + `bounty-parent-traversal`, `bounty-parent-traversal-vault`, `bounty-fallback-symlink-escape` |
| C | A + literal hit suppressed | `67f8c0bee32c` | 11/2 | A's flip + `literal-prefix-sibling-control: RESOLVES→GONE` |
| D | bounty-fallback `under_mirror` dropped only | `163f54b07adb` | 10/3 | `bounty-parent-traversal`, `…-vault`, `bounty-fallback-symlink-escape` |
| E | relative-fallback `under_mirror` dropped only | `7fed2c1a11f4` | 11/2 | `relative-mirror-fallback-escape`, `relative-fallback-symlink-escape` |
| F | `classify` returns GONE always | `2e1edc7792ed` | 8/5 | 5 controls: both confined MIRROR-EQUIVALENT, INTERNAL, both RESOLVES controls |
| G | `BOUNTY_PREFIXES` loses `/home/vgpnk/Projects/bounties` | `f032c4ca9153` | **13/0 (SURVIVED)** | none |
| H | `BOUNTY_PREFIXES` loses `~/Projects/bounties` | `853a8eeab9e0` | 12/1 | `confined-bounty-fallback-control: MIRROR-EQUIVALENT→GONE` only |

B's flip set is exactly A ∪ D (no interaction). D and E are disjoint, so the two
containment calls are separately witnessed. F shows the control set is not
GONE-collapsible (the escape set alone would be cheated by a GONE-everything
detector; the controls reject it 5/13).

G is the material coverage finding: deleting the absolute-home bounty prefix changes
real behaviour (`/home/vgpnk/Projects/bounties/…` loses the confined mirror fallback
and becomes plain-GONE) yet survives the frozen matrix untouched, because no case
uses that form. I verified a concrete witness and its host dependence:
`fixtures-abscase.json` (`sha256 680559edaf37…`) adds one `absolute-bounty-fallback-control`
citing `/home/vgpnk/Projects/bounties/ops/rank.mjs:1` with the file only in the mirror.

```
pristine, 14 cases: cases=14 ... pass=14 fail=0   (absolute case PASS = MIRROR-EQUIVALENT)
G,        14 cases: absolute-bounty-fallback-control expect=MIRROR-EQUIVALENT actual=GONE FAIL
                   cases=14 ... pass=13 fail=1
```

That witness is not hermetic: it requires `/home/vgpnk/Projects/bounties/ops/rank.mjs`
to be absent on the host (it is, on this host: `ls` → No such file or directory), which
breaks the fixture's own stated invariant that "paths never leave the case root except
by the traversal the citation itself performs" (matrix line 3). Closing G therefore
needs a harness change (redirect the bounty literal root the way `KASEGI_MIRROR`
redirects the mirror), not a fixture-only case.

## 5. Findings (falsifiable)

1. **F1 — single-witness boundary.** Reverting `bounty_suffix()`'s exact-root boundary
   to `startswith(BOUNTY_PREFIXES)` + `split()` is killed by exactly one of 13 frozen
   cases (`bounty-prefix-sibling-confusion` → MIRROR-EQUIVALENT). Falsified if any other
   case flips: none did (receipt `63107a2f…`, sha `13cdb2cf…`).
2. **F2 — decoy-load-bearing witness.** With that case's `files` emptied
   (`fixtures-nodecoy.json`, `sha256 d70d46dc3bbac48ac2186dbe91872313662b4cccc38801a42dbd1289538b45ab`),
   the same mutant passes 13/13. The escape case therefore only detects the boundary
   while its decoy at `<mirror>/-legacy/README.md` is pinned; removing the decoy
   silently deletes all boundary coverage while the suite still reports 13/13.
3. **F3 — the paired literal control is boundary-blind.** `literal-prefix-sibling-control`
   is RESOLVES under both pristine and mutant A; it only moves under a literal-branch
   mutation (C). The distinguishing signal the mutation *does* produce for it — the
   `domain` column flipping `other`→`bounty` — is never asserted by
   `mirror-containment-check.py`, which compares `class` only.
4. **F4 — unwitnessed absolute-home bounty root.** `BOUNTY_PREFIXES[1]`
   (`/home/vgpnk/Projects/bounties`) has no fixture witness; G survives 13/13 with a
   genuine behavioural change, and the verified remedy case is host-anchored, outside
   the harness's hermetic envelope.
5. **F5 — boundary and containment are orthogonal.** `under_mirror()` reports `True`
   for the sibling-confusion decoy (trace above); D/E flip disjoint sets. Neither
   mechanism can substitute for the other, so the claim needs both kinds of witness —
   which the frozen matrix currently has.
6. **F6 — matrix not GONE-collapsible.** A GONE-everything `classify` fails 5 of 7
   controls (8/13 overall), so the escape set is not trivially satisfiable.

None of these is a claim of admission, score movement, or source accuracy; F1/F2/F4 are
detector-strength findings about the C1 instrument, F3 is about the control's
evidential value, F5/F6 are supporting observations.

## 6. Restoration evidence

- `mutA/resolve.py` restored from `pristine/resolve.py`; before/after sha256 both
  `ed9a9dae10024bbb2be5db12776f798309fd4615585c3ad93adaab12702840e9`.
- Restored bytes replayed on the frozen matrix: `cases=13 ... pass=13 fail=0`
  (`mutA/receipt-mutA-restored.json`); its per-case `(expect, actual, status)` map is
  identical to the pristine receipt (verified programmatically: `restored==pristine: True`).
- Production artifacts re-hashed after all runs:
  `resolve.py ed9a9dae…`, `mirror-containment-fixtures.json 5e61a33e…`,
  `mirror-containment-check.py 1bc2db10…`. Determinism: pristine was run twice, same
  case map both times.

## 7. Scope limits

- Detector-only: one class per case, 13 frozen cases (+1 probe case), classification
  semantics of the copied CLI TSV. Nothing here measures source availability, quote
  fidelity, corpus attribution, C2 (F06-F08), or score.
- One mutation point per mutant; A is the assigned probe, B-H are attribution controls
  run on the same matrix and are reported as such, not as additional contract findings.
- The `domain` column is unasserted, so all statements about domain rest on the direct
  trace in §2, not on the matrix.
- Host-dependent absolute-path probe (§4) is valid only while
  `/home/vgpnk/Projects/bounties` is absent; on another host the same case would read
  the host literal and the probe result would not transfer.
- Single run per mutant (pristine twice). No claim of statistical robustness.

## 8. Reproduction commands

```
SCR=/tmp/kasegi-r23-falsify-MutateBoundary-2
SRC=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments
mkdir -p $SCR/{pristine,mutA}
cp $SRC/resolve.py $SCR/pristine/resolve.py
cp $SRC/mirror-containment-fixtures.json $SCR/pristine/fixtures.json
cp $SRC/mirror-containment-check.py $SCR/pristine/check.py
cp $SCR/pristine/resolve.py $SCR/mutA/resolve.py
# apply the §1 diff to $SCR/mutA/resolve.py, then:
cd $SCR/pristine && python3 check.py --resolver ./resolve.py --fixtures ./fixtures.json --json ./receipt-pristine.json
cd $SCR/mutA    && python3 ../pristine/check.py --resolver ./resolve.py --fixtures ../pristine/fixtures.json --json ./receipt-mutA.json
cd $SCR         && python3 probe_diff.py && python3 probe_trace.py
```

Receipt hashes: pristine `bcf854e7…`, A `63107a2f…`, A-restored `482b9211…`,
B `a9aa8ba3…`, C `79fdb05d…`, D `9625e5aa…`, E `e5c9b70d…`, F `f8ef42fe…`,
G `0e0b4521…`, G+abscase `67279672…`, H `8cfe9f1a…`, A-nodecoy `5d3358a9…`,
pristine+abscase `650f8513…`.
