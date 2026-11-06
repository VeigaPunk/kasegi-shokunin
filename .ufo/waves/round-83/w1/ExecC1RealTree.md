# ExecC1RealTree — round-83 C1 real-tree census + G1–G4 probes + landing pins

Seat: ExecC1RealTree (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze: `0cd499dbdfc0bf9ce3095681af9bc76588d76f31` (base `834bf78e`). No lane file edited, no git/jj
write, no corpus/instrument edit; scratch `/fast/scratch/hyaku/kasegi-r83/ExecC1RealTree` (removed at
exit). No tool installs were needed (nothing installed, nothing upgraded).

Frozen bytes measured here:

| object | sha256 |
|---|---|
| `.ufo/waves/round-83/c1/recheck-cwd-census.py` (candidate) | `343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9` |
| `corpus/instruments/recheck-cwd-census.py` (base, still unlanded) | `81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050` |
| `.ufo/waves/round-83/c1/mutant-table.json` | `5b1d99f59cede6cffa36d554ce7e8256bf1eba1cb84a9591bfbb9f7f386b6f44` |

Candidate sha matches the value in the assignment; the base instrument is still the r82 bytes, so the
successor exists only in the wave dir (pre-landing state confirmed, not assumed).

## Verdicts

| item | verdict | one line |
|---|---|---|
| 1 P5 analogue (real-tree census) | **PASS** | `entries=97 … RESULT conformant`, rc 0; 97 = `ls corpus/knowledge/*.md \| wc -l`, uncommitted F59 draft included |
| 2 G1–G4 probes | **PASS** (one table-accuracy observation, not a claim failure) | each row kills its declared case; G1 additionally kills `bucket-over` |
| 3 P8 pins | **PASS** | 2 sites carry `cases=24`; exact replacement lines written to `ExecC1RealTree-pins.txt` |
| 4 TMPDIR-only scratch | **PASS** | no hard-coded `/tmp`; every fixture/run dir is `tempfile.mkdtemp(dir=$TMPDIR)` |

## 1 — P5 analogue: census on the real lane tree

Command (run from the lane root, `TMPDIR` = scratch):

```
TMPDIR=$S python3 -B .ufo/waves/round-83/c1/recheck-cwd-census.py \
  --root /home/vgpnk/Projects/shokunin/kasegi-shokunin \
  --lane /home/vgpnk/Projects/shokunin/kasegi-shokunin
```

Output (receipt `ExecC1RealTree-receipts/c1-real-tree-census.txt`, captured by the same command; two
runs byte-identical):

```
RECHECK-CWD entries=97 noprefix=0 exit2_foreign=0 exit0_foreign=75 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
rc=0
```

Entry-count comparison: `ls corpus/knowledge/*.md | wc -l` = **97**; census `entries=97`. The
uncommitted, L1-authored draft `corpus/knowledge/osv-faq-post-import-record-lifecycle.md` **is counted**
— `git status --porcelain -- corpus/knowledge` shows it as `??` (untracked), and the census globs the
working tree, so the untracked file is inside the count. Direct per-entry evidence from the G4 verbose
run on the same tree: `ENTRY osv-faq-post-import-record-lifecycle.md noprefix=0 foreign_exit=0` — the
draft's own `recheck:` header (`cd <lane> && python3 corpus/instruments/source-recheck.py --manifest
corpus/source-snapshots/round-83/manifest.json --source S117`, draft line 5) passes from a foreign cwd.

Bucket profile: `exit0_foreign=75` + `exit1_foreign=22` = 97 = `entries`, and all four RESULT-gate
buckets (`noprefix`, `exit2_foreign`, `norecheck`, `restoration_only`) are 0, so the bucket sum is exact
and the RESULT limb is load-bearing on real data, not vacuous.

Observation (scope, not a defect): `exit1_foreign=22` is outside the RESULT gate by design
(`conform_ok` requires `noprefix == 0 and exit2_foreign == 0 and norecheck == 0 and
restoration_only == 0 and buckets == entries`). The 22 are the lane's own process entries
(`citation-bases`, `claim-anatomy-sample`, `ev-model`, `evidence-dir`, `intake-and-finalize`,
`intake-surface`, `mission-control`, `mission-ledger`, `operator-queue`, `ops-invariants`,
`policy-access-playbook`, `program-quirks`, `repo-git-state`, `retirement-autopsies`,
`source-tree-loss-2026-09-28`, `submitted-registry`, `target-checkouts`, `terminal-classes`,
`triage-thresholds`, `ufo-archive-2026`, `ufo-workspaces`, `vdp-disclosure-packages`), whose recheck
runs a checker that reports findings. The census measures cwd-foreignness, not entry health; the count is
inherited from r82, not introduced by the successor.

## 2 — G1–G4 on the real tree (row applied once, exact scratch copies)

Derivation: `row.anchor -> row.replacement` applied once, then each `row.extra` pair once; every anchor
asserted to occur exactly once in the candidate before substitution (all four: 1 occurrence; G4: 1
anchor + 1 extra). Manifest with mutant sha256s and the literal anchor/replacement strings:
`ExecC1RealTree-receipts/g-mutants-derivation.txt`.

| row | mutant sha256 | selftest rc | FAIL lines | declared kill_cases | lane-tree run |
|---|---|---|---|---|---|
| G1 | `e7a078f3…bff114` | 1 | `bucket-other`, **`bucket-over`** | `bucket-other` | `RESULT conformant`, rc 0 |
| G2 | `9e25eb71…5f72b2a` | 1 | `bucket-over` | `bucket-over` | `RESULT conformant`, rc 0 |
| G3 | `a66a5612…975185af` | 1 | `main-verbose` | `main-verbose` | `RESULT conformant`, rc 0 |
| G4 | `c9b1ad33…9391d46a` | 1 | `main-verbose` | `main-verbose` | `RESULT conformant`, rc 0 |

Exact selftest lines (receipts `g<n>-selftest.log`, `g<n>-selftest.rc`):

```
g1: selftest case=bucket-other FAIL exit_other=1 main_ret=1
    selftest case=bucket-over FAIL over=True
    selftest cases=27 failures=2                     rc=1
g2: selftest case=bucket-over FAIL over=True
    selftest cases=27 failures=1                     rc=1
g3: selftest case=main-verbose FAIL verbose_entries=5 default_entries=5 ret=1
    selftest cases=27 failures=1                     rc=1
g4: selftest case=main-verbose FAIL verbose_entries=6 default_entries=6 ret=1
    selftest cases=27 failures=1                     rc=1
```

Each row's declared expectation is met: G1 → `bucket-other` FAIL; G2 → `bucket-over` FAIL; G3 and G4 →
`main-verbose` FAIL (G4 with the verbose default flipped, `verbose_entries == default_entries == 6`).
The mutant runs also re-confirm the candidate's own count: every run prints `cases=27`, so the pin below
is grounded on executed output, not only on the docstring.

**Observation (table accuracy, not a claim failure).** G1's transform drops the `exit_other` term from
`conform_ok`'s bucket sum (`+ counts["exit_other"] + counts["norecheck"]` → `+ counts["norecheck"] +
counts["norecheck"]`), so it breaks two cases with one root cause:

- case 23 (`bucket-other`): `oth = {entries:2, exit0_foreign:1, exit_other:1}` → mutated sum 1 ≠ 2 →
  `conform_ok(oth)` False where the check requires True → FAIL;
- case 24 (`bucket-over`): `over = dict(oth, entries=1)` → mutated sum 1 == 1 → `conform_ok(over)` True
  where the check requires False → FAIL (its `exit_other=2` limb also flips, `exit0_foreign=0` limb
  still holds; the printed detail `over=True` is the first limb).

`kill_cases` for G1 therefore under-declares by one case. This does **not** falsify the frozen P3:
`mutbat.verdict()` returns `KILLED` when at least one FAIL case is in `kill_cases` and not all of those
are exception-class; extra FAIL cases are ignored, and `MISKILLED` is only reached when *no* declared
case fails. So `killed=64 … miskilled=0` remains reachable with the table as frozen, and the table
docstring's wording ("the selftest case ids its transform is *meant* to break") reads as intent, not an
exhaustive set. Advisory for the L1 only (no edit made here): either add `bucket-over` to G1's
`kill_cases`, or state the subset convention in the table docstring so a future reviewer does not read
the two-kill row as a keying error.

**Observation (real tree is non-discriminating for these four rows).** All four mutants are
`RESULT conformant` with rc 0 on the real lane tree (`g<n>-lane.log`), because the real counts have
`exit_other=0` and `norecheck=0` (G1's sum is unchanged), `buckets == entries` (G2's `>=` is satisfied),
and no `--verbose` flag is passed (G3/G4). G4 does leak all 97 `ENTRY` lines to stdout on the real tree
while still exiting 0 — the real-tree run cannot see any of the four gaps; only the selftest can. That is
the intended division of labour, and it is why the r82 controls (base bytes → G1–G4 SURVIVED) are the
right negative control.

## 3 — P8 pre-landing pins

`grep -n 'cases=24' SKILL.md corpus/instruments/README.md` → exactly two sites:
`SKILL.md:982` and `corpus/instruments/README.md:354`. No other `cases=2x` / "twenty-four" mention of
this instrument exists in either file (checked). Exact replacement lines (old and new, full text) are in
`ExecC1RealTree-pins.txt`; both are single-token edits `cases=24` → `cases=27`, nothing else changed.

Sha pin: neither line carries a digest today — the sha the landing must record is
`343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9` (prefix `343b21e4`) for
`.ufo/waves/round-83/c1/recheck-cwd-census.py`, against base
`81677e9dc030ed59d2e3481c8b1c2bc8d083e6805cc06fbb25052a685773e050` for the landed instrument before the
cutover. Both are recorded as comment lines in the pins file so the L1 has the value in hand.

Not pinned by me (observation only): `SKILL.md:982`'s "pinned-value path" column still points at
`.ufo/waves/round-75/controls/c1-after-r75.txt`. The assignment scoped the pin to the count and the sha,
so I left that cell alone; if the L1 wants the registry row to point at r83 evidence, that is a third
edit in the same line.

## 4 — TMPDIR-only scratch audit

- `grep -n '/tmp'` over the candidate returns exactly one hit, docstring line 27: "path come from
  tempfile, which honors TMPDIR; no path is hard-coded under /tmp." No literal `/tmp` in code.
- Only two scratch-creation sites: line 308 `tempfile.mkdtemp(prefix="recheck-cwd-selftest-",
  dir=os.environ.get("TMPDIR") or None)` (the selftest root) and line 117
  `tempfile.mkdtemp(prefix="recheck-cwd-", dir=env_tmp)` with `env_tmp = os.environ.get("TMPDIR") or
  None` (the per-entry foreign cwd, also exported to the child as `TMPDIR`).
- The three round-83 checks (cases 23/24/25) build their fixtures through `fixture(name)` →
  `os.path.join(scratch, name)` where `scratch` is the TMPDIR-rooted mkdtemp; they write only via
  `write_entry(kdir, …)` under that root and run `main()` in-process, so no other path is touched. The
  selftest removes the root in a `finally: shutil.rmtree(scratch, ignore_errors=True)`.
- Precise caveat, not a defect: when `TMPDIR` is unset both `dir=` arguments are `None`, so `tempfile`
  falls back to the platform default (`/tmp`). That is the documented `tmpdir-unset` case (case 18:
  unset TMPDIR is neither refused nor raises). Every run in this report set `TMPDIR` to the seat scratch
  explicitly.

## Risks / blockers

- No blockers. Nothing in the frozen bytes contradicted the assignment.
- Residual risk for the L1: the G1 `kill_cases` under-declaration (above) is invisible to `mutbat`'s
  verdict but visible to any reviewer who runs the G1 mutant's selftest; decide whether to widen the row
  or document the subset convention before the table is cited as "case-matched".
- `exit1_foreign=22` keeps the real-tree run green while 22 process entries' own recheck commands exit 1;
  if a later round wants the census to speak about entry health, that is a new check, not a pin.

## Files written

- `.ufo/waves/round-83/w1/ExecC1RealTree.md` (this report)
- `.ufo/waves/round-83/w1/ExecC1RealTree-pins.txt`
- `.ufo/waves/round-83/w1/ExecC1RealTree-receipts/c1-real-tree-census.txt`
- `.ufo/waves/round-83/w1/ExecC1RealTree-receipts/g-mutants-derivation.txt`
- `.ufo/waves/round-83/w1/ExecC1RealTree-receipts/{g1,g2,g3,g4}-selftest.log`, `…-selftest.rc`,
  `…-lane.log`, `…-lane.rc`
