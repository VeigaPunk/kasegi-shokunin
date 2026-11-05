# ExecC1Controls — C1 controls battery verification (round-76 wave 1)

Seat: ExecC1Controls (leaf executor). Scope: verify the C1 controls battery for the
frozen claims at /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-76/claims.json
(read in full before starting). Freeze commit 5da54cd4451cbbb9e4b87e2f83475feb13c65c9e
(= HEAD at start), base a788021675873a96e09e91aa033d8c26ac2fe212. No lane-tree writes;
read-only git only; scratch /fast/scratch/hyaku/kasegi-r76/ExecC1Controls (deleted before
this report was finalized; all receipts copied into the wave dir first).

## Step 1 — base do-nothing receipts re-derived from base bytes: PASS (byte-identical)

- Extract: `git -C <lane> show a7880216…e212:corpus/instruments/recheck-cwd-census.py > $S/base.py`.
  `sha256sum $S/base.py` → `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`
  — matches the claims.json C1 `target_instrument` pin exactly. rc=0.
- Selftest: `cd $S && TMPDIR=$S/tmp python3 -B $S/base.py --selftest` → rc=0, stderr empty.
  All six case lines and `selftest cases=6 failures=0` byte-match the receipt
  `.ufo/waves/round-76/controls/c1-donothing-selftest-r76.txt`; the single diff line is the
  `tmpdir-parent` diagnostic echo `dirs=...` (the receipt was generated with TMPDIR unset →
  `dirs=None,None,None`; my bounds-compliant run echoes my scratch TMPDIR). Re-run with the
  receipt's environment (`env -u TMPDIR python3 -B …`): **diff empty, byte-identical**,
  sha256 `738027ba2d7fbcc42e378d7227dc382b813bd689a7d8503a2b459f6fc951e5f3` on both sides.
  Receipt: ExecC1Controls-step1-selftest.txt.
- Real-tree census: `cd $S && TMPDIR=$S/tmp python3 -B $S/base.py --root <lane> --lane <lane>`
  → rc=0, stderr empty, 3.8 s. **diff vs
  `.ufo/waves/round-76/controls/c1-donothing-realtree-r76.txt` empty, byte-identical**,
  sha256 `f3efe698843a725167a94b952717f385092d98be31822bf00a2f7b5cf08826ae` both sides:
  `RECHECK-CWD entries=91 noprefix=0 exit2_foreign=0 exit0_foreign=69 exit1_foreign=22
  exit_other=0 norecheck=0 restoration_only=0` / `RECHECK-CWD-RESULT conformant` / rc=0.
  Receipt: ExecC1Controls-step1-census.txt.

## Step 2 — three committed base-byte mutants: red-before reproduces: PASS

Extracted each mutant from the freeze (`git show 5da54cd4…c9e:.ufo/waves/round-76/controls/mut/<m>.py`),
ran `TMPDIR=$S/tmp python3 -B $S/<m>.py --selftest` from $S. All three: rc=0, last stdout
line `selftest cases=6 failures=0` — identical to the committed receipt
`c1-redbefore-mutant-survival-r76.txt`. Mutation sites (diff -U0 vs base.py):

- m1-forged-relabel: census() classification block (base lines 92–98) — the
  `if has_restoration_recheck(path): restoration_only else: norecheck` inner branch replaced
  by unconditional `restoration_only` (norecheck bucket relabeled away).
- m2-result-limb-removed: case-6 check (base line 244) — `and not marker6 and ret6 == 1 and
  "RECHECK-CWD-RESULT nonconformant" in out6` → `and not marker6` (RESULT limb computed but
  unconsumed).
- m3-restoration-forces: same classification block (base lines 92–98) — `if value is None:`
  → `if value is None or has_restoration_recheck(path):` with unconditional
  `restoration_only` (any restoration-recheck: carrier relabeled, even with a recheck: line).

Receipt: ExecC1Controls-step2-mutants.txt (includes each full mutation diff).

## A5 measurement method (demonstrated on base bytes; reused on amended bytes below)

- `subprocess.run` call sites: 1 (run_foreign, line 65 area) — `grep -c 'subprocess\.run'` = 1.
- `"bash", "-c"` literal pairs: 1 — `grep -c '"bash", "-c"'` = 1.
- `tempfile.mkdtemp` call sites: 2 real (run_foreign line 65: `dir=env_tmp` where
  `env_tmp = os.environ.get("TMPDIR") or None`; selftest line 132: `dir=os.environ.get("TMPDIR") or None`);
  the other four grep matches are a comment and the case-3 recording monkeypatch plumbing.
- No hard-coded tmp path: the only `/tmp` occurrence is docstring line 25 ("no path is
  hard-coded under /tmp").

## Step 3 — ExecC1Amend.patch applied; amended selftest and re-derived mutants

### 3a/3b — patch apply and amended selftest: PASS

- `patch -p1 --dry-run` then `patch -p1` on `$S/patchwork/corpus/instruments/recheck-cwd-census.py`
  (= base.py): dry-run rc=0, apply rc=0, 3 hunks. (First attempt used a wrong layout —
  `instruments/` directly under patchwork — and patch correctly refused with "can't find
  file to patch"; no bytes changed; re-run with the `corpus/instruments/` layout succeeded.
  Recorded because the failed run's "amended selftest" was really the base selftest.)
- Byte parity: my patched copy sha256 `e25d3c006f0820ceccfbf974e94634d1554ee07d253766d2ef8980a3806bac28`
  = the author's (ExecC1Amend-3) `ExecC1Amend.amended.py` hash, per their message. Identical.
- Amended selftest: `TMPDIR=$S/tmp python3 -B $S/amended.py --selftest` → rc=0, stderr empty,
  last line `selftest cases=8 failures=0` — the A1 after-state shape (cases=8) confirmed
  independently of the author's run. Receipt: ExecC1Controls-step3-amended.txt.

### 3c — exec surface on amended bytes (A5 method): PASS

`subprocess.run` sites: 1; `"bash", "-c"` pairs: 1; real `tempfile.mkdtemp` call sites: 2
(both `dir=` from `os.environ.get("TMPDIR")`); only `/tmp` mention is the docstring; the only
non-tempfile `open()` writes are selftest fixtures inside the mkdtemp scratch. Unchanged vs base.

### 3d — three amended-byte mutants, re-derived by this seat: ALL KILLED

Sites re-derived by reading the amended source (not copied from the author's diffs):

- **m1a-forged-relabel** — census() classification else-branch (amended lines 96–98)
  `counts["norecheck"] += 1 / print("NORECHECK …")` → `counts["restoration_only"] += 1 /
  print("RESTORATION-ONLY …")`. **rc=1, `selftest cases=8 failures=1`**; killed by the NEW
  case 7 relabel-pair: got `norecheck=0,restoration_only=2` vs want `norecheck=1,restoration_only=1`
  (exact tally asserted — forged relabel of the neither-header bucket fails).
- **m2a-computation-removed** (claim-literal M-R2, per C1 (ii) "removing its computation …
  makes the amended selftest exit nonzero") — deleted line 246
  `res6 = (ret6 == 1 and "RECHECK-CWD-RESULT nonconformant" in out6)`. **rc=1, NameError:
  name 'res6' is not defined** (traceback at line 331 `sys.exit(main(sys.argv))`; the check's
  condition and detail format still consume res6 — the computation line is load-bearing).
- **m3a-restoration-forces** — classification block (amended lines 92–99) →
  `if value is None or has_restoration_recheck(path):` unconditional `restoration_only`
  (replicates the committed m3 shape exactly, collapse included). **rc=1,
  `selftest cases=8 failures=2`**: relabel-pair FAIL and both-headers FAIL
  (got `restoration_only=1,exit0_foreign=1` vs want `restoration_only=0,exit0_foreign=2`
  on case 8 — the both-headers fixture is classified normal on the amended bytes, so forcing
  restoration_only on any restoration-recheck: carrier breaks it).
- Cross-check consistency: my m3a double-kill (relabel-pair+both-headers) and m1a relabel-pair
  kill match ExecC1Amend-3's independently produced receipts
  (ExecC1Amend.mutant-m1a/-m2a/-m3a-run.txt). Receipt: ExecC1Controls-step3-mutants-amended.txt.

**Observation (not a frozen mutant class, recorded for the L1):** a consumption-only variant
(`and not marker6 and res6,` → `and not marker6,` while res6 stays computed and formatted in
the detail string) **survives** with rc=0 (`cases=8 failures=0`). The claim's M-R2 commits to
the computation-removal shape, which is killed via NameError; the RESULT limb's gating power
on a surgical condition-term removal rests on the detail-string reference, i.e. removal of the
computation crashes, but weakening only the condition does not fail. No action required by the
frozen predicates; noted as residual coupling strength information.

## Step 4 — A2 drift expectation on a synthetic tree: PASS

Synthetic tree = full copy of lane `corpus/knowledge` (91 files) + `exec-c1-controls-drift-probe.md`
whose sole recheck line is `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true` (92 entries).
`TMPDIR=$S/tmp python3 -B $S/amended.py --root $S/synth --lane <lane>` → rc=0:

```
RECHECK-CWD entries=92 noprefix=0 exit2_foreign=0 exit0_foreign=70 exit1_foreign=22 exit_other=0 norecheck=0 restoration_only=0
RECHECK-CWD-RESULT conformant
```

Exactly the A2 drift expectation: entries 91→92, exit0_foreign 69→70, every other field equal
to the base receipt, RESULT conformant. Receipt: ExecC1Controls-step4-drift.txt.

**Live-tree observation (read-only, not a claim verdict):** re-running the amended census
against the real lane at measurement time printed the same `entries=92 exit0_foreign=70`
shape — the working tree now contains `corpus/knowledge/osv-api-surface-and-limits.md`
(absent at freeze 5da54cd4, which has 91 `.md`; read-only `git ls-tree` + `ls` comparison).
That is the C2 S111 knowledge entry appearing in the lane; the live tree matches the A2
post-C2 drift expectation at the time of measurement. Judging integration state is the L1's.

## Verdict summary for the battery

| Check | Result |
|---|---|
| Step 1 base do-nothing selftest byte-identical | PASS (sha 738027ba…e5f3 both sides) |
| Step 1 base real-tree census byte-identical | PASS (sha f3efe698…26ae both sides) |
| Step 2 red-before: 3 base mutants rc=0 cases=6 failures=0 | PASS (reproduces) |
| Step 3 amended selftest cases=8 failures=0 exit 0 | PASS (independent apply+run) |
| Step 3 amended exec surface unchanged (A5 method) | PASS (1 bash -c, 1 subprocess.run, mkdtemp-only writes) |
| Step 3 amended-byte mutants m1a/m2a/m3a rc≠0 | PASS (all killed; kill cases identified) |
| Step 4 drift expectation entries=92 exit0_foreign=70 | PASS (exact field-for-field match) |

## Seat compliance

- Writes: only this report + the six ExecC1Controls-step*.txt receipt files under
  `.ufo/waves/round-76/w1/`, plus scratch `/fast/scratch/hyaku/kasegi-r76/ExecC1Controls/`
  (deleted before finalization). No lane-tree edits; read-only git only (`show`, `rev-parse`,
  `cat-file`, `ls-tree`); no jj; no commits.
- TMPDIR: every substantive run passed `TMPDIR=$S/tmp` explicitly. One byte-identity
  reproduction run used `env -u TMPDIR` deliberately to match the receipt's recorded
  environment (self-cleaning byte-scale fixtures; dirs=None echo). The base selftest/census
  runs wrote only inside tempfile.mkdtemp dirs honoring TMPDIR.
- Network: none used. Tools installed: none.
- Scratch deleted at finalize (verified absent in the terminal yield).
