# ExecC1RealTree — P5 real-tree census for C1 (round 79, attempt 1)

Seat: ExecC1RealTree (leaf). Scope: P5 measurement only — the live-lane census run of the
frozen C1 candidate, the archive parity probe, and BASE-vs-candidate output parity.
No lane-tree edit, no verdict on C1 as a whole, no gate suite.

Scratch: `/fast/scratch/hyaku/kasegi-r79/ExecC1RealTree` (created with `mkdir -p`, `TMPDIR`
passed explicitly, deleted before yield).

## Frozen inputs (verified)

| Item | sha256 |
|---|---|
| candidate `.ufo/waves/round-79/c1/recheck-cwd-census.py` | `eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f` (matches claim) |
| candidate copied into archive tree `corpus/instruments/recheck-cwd-census.py` | same `eda49d32…091f2f` (re-hashed after copy) |
| BASE `git show 9d0b1eb:corpus/instruments/recheck-cwd-census.py` | `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` (matches claim) |
| live lane `corpus/instruments/recheck-cwd-census.py` (pre-integration) | `e666ae11…a21a` — candidate not yet landed, as expected mid-wave |

Freeze commit `9d0b1eb0709e47c3c6decc09138b5012a8968924`; base `d16d2124fd5262f5a8088aa598f1e628f897d3ab`.

## (1) Archive tree construction

```
S=/fast/scratch/hyaku/kasegi-r79/ExecC1RealTree
mkdir -p $S/tree $S/t
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive \
  9d0b1eb0709e47c3c6decc09138b5012a8968924 | tar -x -C $S/tree
cp .../.ufo/waves/round-79/c1/recheck-cwd-census.py $S/tree/corpus/instruments/recheck-cwd-census.py
```

Result: `sha256sum $S/tree/corpus/instruments/recheck-cwd-census.py` =
`eda49d3214eaa4760bdb74fd73bc45d0993051618fbce01a3082102419091f2f`.
`ls $S/tree/corpus/knowledge/*.md | wc -l` = **92**.

## (2a) Archive parity probe (candidate, archive tree)

```
cd /
TMPDIR=$S/t python3 -B $S/tree/corpus/instruments/recheck-cwd-census.py \
  --root $S/tree --lane $S/tree
```

rc = **1**. stdout (94 lines: 92 `ENTRY` + 2 summary), stderr empty:

```
RECHECK-CWD entries=92 noprefix=92 exit2_foreign=0 exit0_foreign=70 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT nonconformant
```

`ENTRY` lines: 92, every one `noprefix=1`; bucket tally `foreign_exit=0` 70, `foreign_exit=1` 22,
`foreign_exit=2` 0. Sample:

```
ENTRY ai-assisted-finding-validation.md noprefix=1 foreign_exit=0
ENTRY citation-bases.md noprefix=1 foreign_exit=1
ENTRY zdi-disclosure-process-and-vendor-coordination.md noprefix=1 foreign_exit=0
```

Interpretation (reported, not judged): every recheck line in the frozen tree carries the
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ` prefix naming the **live** lane, so under
`--lane $S/tree` all 92 are prefix-less by construction and the verdict is `nonconformant`.
This is the expected parity artefact, not a candidate defect: the executed command bodies are
unchanged, and the foreign-exit distribution (70/22/0) is identical to the live-lane run below.

## (2b) Live-lane run — the P5 measurement

```
cd /
TMPDIR=$S/t python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/c1/recheck-cwd-census.py \
  --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

rc = **0**. stdout in full (2 lines), stderr empty:

```
RECHECK-CWD entries=92 noprefix=0 exit2_foreign=0 exit0_foreign=70 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
```

`ENTRY` lines: **0** (the counter emits an ENTRY line only for prefix-less or exit-2 rows).

Ground truth at the same tree:

```
ls /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge/*.md | wc -l
→ 92
```

P5 clause check (claim P5: entries == knowledge `.md` count, `noprefix=0`, `exit2_foreign=0`,
`exit_other=0`, `norecheck=0`, `restoration_only=0`, `RECHECK-CWD-RESULT conformant`, exit 0):

| P5 clause | measured | holds |
|---|---|---|
| entries == `ls corpus/knowledge/*.md \| wc -l` | 92 == 92 | yes |
| noprefix | 0 | yes |
| exit2_foreign | 0 | yes |
| exit_other | 0 | yes |
| norecheck | 0 | yes |
| restoration_only | 0 | yes |
| RESULT line | `conformant` | yes |
| exit code | 0 | yes |

Note: this is the live tree **before** the C2 entry lands (92 `.md`); the count is compared
against the tree as measured, which is what P5 states. If C2 lands a 93rd entry, P5 must be
re-measured at the landing commit by the integrating seat — the counter's `entries` value is
tree-derived, not pinned, so no code change is implied.

## (3) BASE parity (same live-lane invocation)

```
git -C .../kasegi-shokunin show 9d0b1eb…:corpus/instruments/recheck-cwd-census.py > $S/base.py
cd /
TMPDIR=$S/t python3 -B $S/base.py --root .../kasegi-shokunin --lane .../kasegi-shokunin
```

rc = **0**. Output:

```
RECHECK-CWD entries=92 noprefix=0 exit2_foreign=0 exit0_foreign=70 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
```

Byte comparison against the candidate's live run:

```
cmp $S/base.out $S/live.out      → identical (diff_rc=0)
sha256sum $S/base.out $S/live.out → 9cf7a93a92bb1aee754bf72a0c1101280d65866ddbe0ee12ee18de2eb8c2b88b (both)
grep '^RECHECK-CWD ' … | cmp     → RECHECK line identical, 128 bytes each
```

**Parity verdict: PASS.** BASE and candidate produce byte-identical stdout on the live lane,
including the `RECHECK-CWD` count line and the `RECHECK-CWD-RESULT` verdict. The candidate's
additions (gate predicates, gate wiring, TMPDIR refusal) are behaviourally inert on this tree,
which is the required property for a successor counter.

## Sanity: frozen candidate selftest (not a P1 verdict — recorded for the reader)

```
cd / && TMPDIR=$S/t python3 -B .../c1/recheck-cwd-census.py --selftest
→ selftest cases=15 failures=0   (rc 0)
```

## Side-effect check (counter writes nothing outside TMPDIR)

- `git -C .../kasegi-shokunin status --porcelain` after both runs: only the pre-existing
  untracked wave files (`.ufo/waves/round-79/w1/`, `w1-dispatch.json`, `w1-spec.json`,
  `w1.ready`, `w1.ready.dispatched`). No tracked file changed, no new lane file from this seat.
- `ls $S/t | wc -l` after the runs = **0** — the counter removed its own foreign-cwd scratch
  under `TMPDIR`; no residue, no `/tmp` hard-coding observed.

## Verdict

**P5 verdict: met** — on the live lane the frozen candidate prints
`RECHECK-CWD entries=92 … noprefix=0 exit2_foreign=0 exit_other=0 norecheck=0 restoration_only=0`
and `RECHECK-CWD-RESULT conformant`, exit 0, with `entries` equal to the tree's
`corpus/knowledge/*.md` count (92).

**Parity verdict: PASS** — archive probe is the expected `noprefix=92` artefact of the live-lane
prefix (reported, not judged); BASE-vs-candidate live stdout is byte-identical.

## Risks / caveats

1. P5 was measured on the live tree at 92 entries. If C2's S113 entry lands in the same
   integration, the landing-commit P5 must be re-run (expected `entries=93`); the counter needs
   no change.
2. The archive probe cannot be conformant by construction (frozen `cd` prefixes name the live
   lane). It is a parity probe only; do not read `nonconformant` there as a candidate defect.
3. `exit1_foreign=22` is the documented fail-closed bucket (absent lost-base dependencies), not
   a failure of the counter; it is identical in BASE and candidate.
4. This seat did not run the mutant battery, the selftest as a P1 judgement, P4, P6 or P7 —
   those belong to other seats / the integrating L1.

## Files written by this seat

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/ExecC1RealTree.md` (this report)

No other lane-tree file was created or modified. Scratch
`/fast/scratch/hyaku/kasegi-r79/ExecC1RealTree` removed before yield. No tool installed or
upgraded (nothing needed).
