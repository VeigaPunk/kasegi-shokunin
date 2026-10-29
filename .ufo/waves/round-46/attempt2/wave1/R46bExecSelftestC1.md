VERDICT: DRAFT-READY

# R46bExecSelftestC1 — extend the C1 selftest with the round-46 mutant-table gaps

Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (kasegi round 46, attempt 2; frozen base
`04af9bc92229232ea5cce8b32bfe59dd969eb26d`, freeze commit `fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4`).
Seat: builder (draft only). Nothing outside my draft dir and this report was written; no git/jj
mutation, no commit, no push.

## 0. Inputs, and how the gap list was derived

* The gap scout's spec was **not** on disk when I ran:
  `glob .ufo/waves/round-46/attempt2/wave1/R46bScoutSelftestC1Gap.md` → `Path not found`.
  I therefore derived the gap list from the frozen before-value receipt
  `.ufo/waves/round-46/attempt2/controls/mutbat-before.txt`, as the card allows.
* That receipt's C1 block (quoted verbatim from the file):

```
mutbat counter=c1 mutants=20 caught=13 equivalent=0 uncaught=7 baseline_failures=0
```

  → the seven **uncaught** C1 mutants to attack are
  `M06-L3-home-dropped`, `M07-L3-home-no-abs`, `M13-L6-control-dropped`, `M14-L6-exit-ignored`,
  `M18-anchor-dirs-wide`, `M19-L2-eq-relaxed`, `M20-syntax-ignored`.
* The lane's committed selftest is untouched: `corpus/instruments/r46-counters-selftest-c1.py`
  sha256 `8b17164aadbd9c6925b5edd4111e3174936388e60e81e09465df0f00c04ec770` (unchanged from the
  pre-existing file I copied at the start).

## 1. What was built

Draft (complete file, ready to drop in at the lane path):
`.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/r46-counters-selftest-c1.py`
sha256 `03079421b07639baabfc942ef4a022c9a8798ff8bc81f029d4b73c6a8b54e2fd` — 76 → **83 cases**,
same `case ...` line format, same CLI (`--lane/--pure/--counter/--work/--jobs/--keep`).

Seven new cases, one per uncovered limb:

| new case | limb | recipe (what the tree looks like) | why the counter must reject it |
|---|---|---|---|
| `L3-home-path-in-trailing-comment` | L3 | contract recheck line = the exact shape **+ `  # ... ~/notes`** | the cd part is stripped *before* the HOME test, so the trailing comment is the **only** channel `HOME_RE` can still see; a home-relative path in the line must red L3 |
| `L3-absolute-home-path-in-trailing-comment` | L3 | same, comment carries an absolute `/home/...` path | `HOME_RE` also covers `/home/`; the two comments are independent (M07 keeps `~/`, M06 drops the whole regex) |
| `L2-newly-gated-entry-not-gated-at-base` | L2 | `considerthese-proposals-ledger.md` (executes at BASE) becomes gated at tree (its line points at a missing round-99 manifest) | the gated set at tree is then **not a subset** of the BASE gated set; L2's count equality `len(gt) == len(gb)-len(reg)` must fail |
| `X-anchor-dir-outside-the-whitelist` | L1/L2/L7 | contract row G8 re-anchored on `corpus/knowledge/triage-thresholds.md` (a knowledge entry, not `corpus/instruments/` nor `corpus/source-snapshots/`) | the anchor-dir whitelist must reject it; a rejected row makes the entry fall back into the gated set, so the signal is L1/L2/L7 (same shape as the harness's existing `ROWLEVEL` convention) |
| `L1-cd-target-is-not-valid-bash` | L1 | `cisa-kev-catalog.md` recheck line: the cd target carries an unbalanced `(` | the line is not valid bash; the cd part is stripped before the line is *executed*, so only `bash -n` sees it — without that check the line runs green |
| `L6-anchor-escapes-the-scratch-copy` | L6 | contract row G9 anchored through an **absolute** symlink into the tree | the anchor resolves inside the tree but **outside** the counter's scratch copy of `corpus/`; the L6 unmutated-copy control must fire and must say so (`survivors=...:unmutated-copy-not-green`) |
| `L6-section-ids-not-unique` | L6 | contract section carries a duplicate row id (G2 → G1); contract recheck line switched to `density.py` so the entry stays in `reg` | every row still reads `ok=1`, yet the entry can never be green (ids must be unique) — the unmutated-copy control must fire, so L6 must read 0 |

Four small harness extensions, each needed by a case above (all backward compatible; the committed
76 cases behave exactly as before):

* `BASE_LINE_ALL` — two of the recipes (the `bash -n` case and the L2 case) rewrite the recheck
  line of an *arbitrary* entry, so the harness now records every entry's BASE recheck line (it
  previously recorded only the two regrounded ones).
* optional per-case BASE (6th tuple element) — the L6 anchor case plants an absolute symlink; L4
  compares BASE vs TREE bytes, so that case's own BASE copy must carry the same symlink, otherwise
  L4 would read red for a second, unrelated reason.
* optional limb-**reason marker** (7th tuple element) — pins *which* reason the counter must report
  for a limb (used for `unmutated-copy-not-green`), so a mutant that keeps the accept/reject verdict
  but changes what the counter *reports* is still caught.
* `--only <substring>` — run a subset of cases (used for the focused probes below; absent ⇒ all cases).

## 2. Baseline, before and after (last lines quoted)

**Before** — the committed selftest, unchanged, against the frozen pure export:

```
$ python3 corpus/instruments/r46-counters-selftest-c1.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/w --jobs 8
case P-trailing-comment-on-recheck-line           L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=76 failures=0
```
(full log: `receipts/01-before-committed-selftest.txt`)

**After** — the extended draft selftest (same counter, same pure export):

```
$ python3 .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/r46-counters-selftest-c1.py --pure /fast/scratch/hyaku/kasegi-r46/L1/pure2 --work $S/f-plain --jobs 4
case L6-section-ids-not-unique                    L1=1 L2=1 L3=0 L4=0 L5=1 L6=0 L7=1 fixed=4/7 exit=1 targets=L6 verdict=OK
case X-stubbed-gate-copy-alone                    L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=- verdict=OK
residual-false-greens=1 (disclosed mechanical limits, not counted as failures: R-claim-text-unrelated-to-anchor)
selftest cases=83 failures=0
```
(full log: `receipts/02-after-extended-selftest.txt`)

The four control rows are unchanged in both runs: `TIP-7of7` reads 7/7, `CONTROL-do-nothing` 1/7,
`HOME-bounties-do-nothing` 2/7, `HOME-bounties-tip` 2/7.

## 3. Per-mutant verification (the extended selftest vs a scratch-mutated counter)

Each mutant was applied to a scratch copy of the committed counter
(`receipts/make_mutant.py`, which asserts the edit occurs exactly once) and the **whole** 83-case
selftest was re-run against it (`--counter <mutant>`). Unmutated column = the same case on the
unmutated counter (from §2's run).

| mutant | new case that must fail | unmutated reading | mutant reading | verdict |
|---|---|---|---|---|
| `M06-L3-home-dropped` | `L3-home-path-in-trailing-comment` | `L3=0 fixed=6/7 exit=1 verdict=OK` | `L3=1 fixed=7/7 exit=0 verdict=FALSE-GREEN` | caught |
| `M06-L3-home-dropped` | `L3-absolute-home-path-in-trailing-comment` | `L3=0 fixed=6/7 verdict=OK` | `L3=1 fixed=7/7 exit=0 verdict=FALSE-GREEN` | caught |
| `M07-L3-home-no-abs` | `L3-absolute-home-path-in-trailing-comment` | `L3=0 fixed=6/7 verdict=OK` | `L3=1 fixed=7/7 exit=0 verdict=FALSE-GREEN` | caught |
| `M13-L6-control-dropped` | `L6-anchor-escapes-the-scratch-copy` | `L6=0 fixed=6/7 verdict=OK` | `L6=1 fixed=6/7 verdict=UNEXPECTED` | caught |
| `M13-L6-control-dropped` | `L6-section-ids-not-unique` | `L6=0 fixed=4/7 verdict=OK` | `L6=1 fixed=5/7 verdict=UNEXPECTED` | caught |
| `M18-anchor-dirs-wide` | `X-anchor-dir-outside-the-whitelist` | `L1=0 L2=0 L7=0 fixed=4/7 verdict=OK` | `fixed=7/7 exit=0 verdict=FALSE-GREEN` | caught |
| `M19-L2-eq-relaxed` | `L2-newly-gated-entry-not-gated-at-base` | `L2=0 fixed=5/7 verdict=OK` | `L2=1 fixed=6/7 verdict=UNEXPECTED` | caught |
| `M20-syntax-ignored` | `L1-cd-target-is-not-valid-bash` | `L1=0 fixed=6/7 verdict=OK` | `fixed=7/7 exit=0 verdict=FALSE-GREEN` | caught |
| `M14-L6-exit-ignored` | — | — | — | **equivalent**, see §4 |

Selftest totals per mutant (last line of each run, quoted):

```
M06-L3-home-dropped    selftest cases=83 failures=2
M07-L3-home-no-abs     selftest cases=83 failures=1
M13-L6-control-dropped selftest cases=83 failures=2
M18-anchor-dirs-wide   selftest cases=83 failures=1
M19-L2-eq-relaxed      selftest cases=83 failures=1
M20-syntax-ignored     selftest cases=83 failures=1
```

The four mutants that were already caught before this change (M01–M05, M08–M12, M15–M17) are
untouched by the extension: the harness change is behaviour-preserving for the committed cases —
comparing the before and after runs case by case, **all 76 committed case readings are identical**
(`common cases whose reading CHANGED between before and after: none`; the seven new cases are the
only additions). I did not re-run those thirteen mutants against the extended file (each run is a
full 83-case selftest); the L1's `mutbat` run covers them.

**Example of the discriminating reading** (M13, `L6-section-ids-not-unique`; the case lines are in
`receipts/03-mutant-M13-L6-control-dropped.txt`, the raw `gate` lines below come from the same two
counters run on that one case tree) — the limb itself flips:

```
unmutated : gate L6 pass=0 read=mutants=7 survivors=claim-package-contract.md:unmutated-copy-not-green
M13       : gate L6 pass=1 read=mutants=15 survivors=none
```

and for M20 the whole tree turns green (`fixed=7/7 exit=0`), i.e. a true false-green:

```
case L1-cd-target-is-not-valid-bash               L1=1 L2=1 L3=1 L4=1 L5=1 L6=1 L7=1 fixed=7/7 exit=0 targets=L1 verdict=FALSE-GREEN
```

## 4. `M14-L6-exit-ignored` is equivalent — no case can catch it, and here is the proof

M13's table entry drops `p.returncode == 0 or` from the L6 survivor test:

```
unmutated : survivor iff (p.returncode == 0 or red != [r[0]])
M14       : survivor iff (red != [r[0]])
```

`p` is the counter re-run on a scratch copy of `corpus/` with one row's token blanked, and
`entry_mode()` returns 0 **iff** every row printed `ok=1` (`ok == len(rows)`), hence

```
p.returncode == 0  =>  red == []  =>  red != [r[0]]  =>  BOTH flag a survivor
p.returncode != 0  =>  the second clause decides         =>  BOTH agree
```

so the two predicates are equal on every input. Empirically (15 trees: the TIP plus the 14
L6-relevant recipes of the harness, each read by the unmutated counter and by the M14 counter,
comparing the `gate ...`/`c1-gate ...` lines byte-for-byte;
script: `receipts/m14-equivalence-differential.py`):

```
tree=TIP                    identical=True
tree=m_token_absent         identical=True
tree=m_anchor_moved         identical=True
tree=m_short_token          identical=True
tree=m_hash_token           identical=True
tree=m_planted_in_place     identical=True
tree=m_overlap_tokens       identical=True
tree=m_dup_token            identical=True
tree=m_dup_anchor_range     identical=True
tree=m_tautology            identical=True
tree=m_one_anchor_file      identical=True
tree=m_five_rows            identical=True
tree=m_pipe_token           identical=True
tree=m_anchor_symlink       identical=True
tree=m_anchor_outside       identical=True
m14-equivalence trees=15 differing=0
```

**Recommendation to the L1:** record `M14-L6-exit-ignored` in the battery's `--equivalent` map with
this proof, rather than leaving it as `uncaught`. (It is the only one of the seven uncaught mutants
that no selftest case can catch.)

## 5. Discrimination against a do-nothing control

* The harness's own do-nothing control is unchanged: `CONTROL-do-nothing` (tree = baseline = pure)
  reads `fixed=1/7 exit=1`, and the synthetic tip reads `fixed=7/7 exit=0`, in the before and after
  runs alike — the new cases did not loosen the harness. Case-by-case diff of the two runs:

```
before cases=76 after cases=83 common=76 new=7
common cases whose reading CHANGED between before and after: none
new cases: ['L1-cd-target-is-not-valid-bash', 'L2-newly-gated-entry-not-gated-at-base',
            'L3-absolute-home-path-in-trailing-comment', 'L3-home-path-in-trailing-comment',
            'L6-anchor-escapes-the-scratch-copy', 'L6-section-ids-not-unique',
            'X-anchor-dir-outside-the-whitelist']
```
* Every new case is *specific*: on the unmutated counter it reds exactly the limb(s) it names and
  nothing else (quoted in §3's "unmutated reading" column; e.g. the two L3 cases red only L3,
  the L1-cd case reds only L1, the L6-anchor case reds only L6). No case relies on "the tree is red
  somewhere".
* The `X-anchor-dir-outside-the-whitelist` case is the one whose signal spans limbs, and it is
  deliberate: a row that the counter rejects makes its entry fall back into the gated set, so L4
  (which only inspects entries still in `reg`) stays green while L1/L2/L7 read red. This is the
  harness's pre-existing `ROWLEVEL` convention (the committed cases `L4-row-anchor-moved` etc. are
  re-targeted to `{L1,L2}` for exactly this reason); the case description says so.

## 6. Limitations and caveats

1. **The end-to-end battery was not run by me.** `r46-mutbat.py --counter both` (the `uncaught=0`
   claim's own instrument) is the L1's integration gate; it runs 41 full selftests (~20 min each),
   which is the parent's step. What I ran is the equivalent evidence per mutant: the full 83-case
   extended selftest against each scratch-mutated counter, with the mutant laid out the way
   `r46-mutbat.py`'s `apply_mutant` lays it out.
2. **A mutant counter must live in a tree layout.** My first attempt put the mutant at
   `<scratch>/mut/<id>/r46-c1-gate.py`; the counter resolves its instrument lane from its own path
   (`TOOL_LANE`), so every instrument the recheck lines run went missing and the counter read
   garbage (`gated=63 broken=0`, everything 0/7). That run is **void, not evidence**; it is
   discarded. `receipts/make_mutant.py` reproduces the correct layout
   (`<root>/corpus/instruments/r46-c1-gate.py` with the lane's instruments copied next to it).
3. **M13's catch is limb-level, on trees that are red for another reason.** M13 cannot turn a red
   tree green (the copy is not green exactly when a row is red in it, and that row stays red in
   every per-row copy, so the survivor test still fires); it only changes *what* the counter
   reports, or (when the copy excludes an anchored directory) makes it fail closed. My
   `L6-section-ids-not-unique` case therefore pins the L6 **limb** flipping 0→1 on a tree that is
   already red for L3/L4 reasons. The L1 may prefer to treat M13 as equivalent-with-proof as well;
   both readings are evidenced above.
4. The `M06` and `M07` cases are not independent in one direction: M06 removes the whole `HOME_RE`
   so it trips both cases, while M07 (which only drops `/home/`) trips only the absolute-path case.
   Both still fail under their own mutant, which is what the battery measures.
5. The frozen pure export was only read: `find /fast/scratch/hyaku/kasegi-r46/L1/pure2 -newermt
   "2026-10-29"` lists the export directory itself and **no file inside it** (the directory's own
   mtime is from the L1's copy, not from my runs).
6. Scratch removed: `/fast/scratch/hyaku/kasegi-r46/R46bExecSelftestC1` was deleted after the
   receipts below were copied into the draft directory.

## 7. Files

* Draft (the deliverable): `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/r46-counters-selftest-c1.py`
* This report: `.ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.md`
* Receipts (copied out of the removed scratch):
  `receipts/01-before-committed-selftest.txt`, `receipts/02-after-extended-selftest.txt`,
  `receipts/03-mutant-<id>.txt` (6 files), `receipts/make_mutant.py`,
  `receipts/m14-equivalence-differential.py`, `receipts/04-m14-equivalence.txt`
* No tool was installed or upgraded for this seat (nothing to record under the operator's tooling
  directive); everything used was already present (python3, git read-only).
