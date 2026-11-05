# ReviewerC1 — kasegi round-70 w1 — C1 independent reproduction from committed bytes

- Seat: ReviewerC1 (leaf; no subagents dispatched; read-only on the lane except this file).
- Revs: base `e7c02bddaa32…`, frozen claims/pins `e74ba6b5d522…`, C1 implementation `c1051749571c…`, C2 landing `b4afd8a0206b…` (C2 not judged by this seat).
- Method: `git -C <lane> archive c1051749… corpus/instruments .ufo/waves/round-70/controls | tar -x -C /fast/scratch/hyaku/kasegi-r70/ReviewerC1/export`; every run used `/usr/bin/python3` (3.14.8), `/usr/bin/git` (2.56.0), `/usr/bin/sort` (GNU coreutils 9.12), with `TMPDIR`/`HYAKU_SCRATCH` inside the seat scratch. The frozen counter is committed code; no tool installs were needed (PACMAN GUARD respected — nothing installed). Scratch tree removed before yield; decisive receipts are embedded below.
- Frozen inputs read first: `.ufo/waves/round-70/claims.json` and `.ufo/waves/round-70/controls/pins-r70.txt` at `e74ba6b5…`.

## 1. Exported-byte pins (item 1) — PASS

```
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  45967  corpus/instruments/figure-audit.py
aaee62290853791d0d0768fa7633f908e32ae5783c6c72a8cc354050f5276176  13674  .ufo/waves/round-70/controls/c1-probe-run-r70.py
c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde  41790  .ufo/waves/round-70/controls/base-gate-r70.py
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  45967  .ufo/waves/round-70/controls/candidate-gate-r70.py
```

All four match `pins-r70.txt` (frozen at `e74ba6b5…`), which lists exactly these hashes for these paths. `cmp` exported gate vs `candidate-gate-r70.py` → rc 0 (byte-identical). Export tree: 271 files.

## 2. Frozen counter runs (item 2) — REPRODUCE

Commands (each with its own `--work` under the seat scratch; `python3 -B`, probe sha `aaee6229…`):

```
python3 -B .ufo/waves/round-70/controls/c1-probe-run-r70.py --gate <export>/corpus/instruments/figure-audit.py --work S/work-cand --mode candidate   # rc=0
python3 -B .ufo/waves/round-70/controls/c1-probe-run-r70.py --gate <export>/.ufo/waves/round-70/controls/base-gate-r70.py --work S/work-base --mode base   # rc=1
```

Candidate (rc=0):

```
MEASURE P1-python-root-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P2-python-root-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P3-python-root-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P4-python-out-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P5-python-out-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P6-python-out-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE P7-python-json-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest ok selftest cases=96 failures=0 rc=0
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=12 failures=0 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=candidate
```

Base (rc=1):

```
MEASURE P1-python-root-space FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE P2-python-root-equals FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE P3-python-root-abbrev FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE P4-python-out-space FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE P5-python-out-equals FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE P6-python-out-abbrev FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE P7-python-json-space FAIL rc=1 refused=0 marker_runs=1 wrote=1
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest FAIL selftest cases=86 failures=0 rc=0
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=4
VERIFY measurements=12 failures=9 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
```

Predicate match: candidate `VERIFY measurements=12 failures=0` + exit 0 ✓; base `measurements=12 failures=9` + exit 1 ✓; P1/P2/P3 ran the fixture entry's recheck payload through `bash -c` (marker_runs=1) ✓; P4/P5/P6 wrote their named outside file (wrote=1) ✓; P7 did both (marker_runs=1 wrote=1) ✓. The 9th/8th base failures are the selftest pin (cases=86 ≠ probe's `EXPECTED_SELFTEST cases=96 failures=0`) and the write-side-effect measurement (4 exec markers), matching the frozen do-nothing control's failure anatomy. Both runs printed the pinned gate sha in `VERIFY`. Read-only controls stayed admitted 8/8 in both modes (no blanket refusal).

## 3. Selftest pin re-derivation from bytes (item 3) — 96 IS PINNED

```
$ git -C <lane> show c1051749…:corpus/instruments/figure-audit.py | grep -cE '^\s+run_case\('
96
$ … | grep -n 'EXPECTED_CASES'
124:EXPECTED_CASES = 96  # R17 pin: … R69: +9 class refusal; R70: +10 python-head option and git-show limb pins)
789:    if len(cases) != EXPECTED_CASES:
790:        print("selftest pin cases=%d expected=%d verdict=fail" % (len(cases), EXPECTED_CASES))
```

96 is pinned: 96 `run_case(` sites, `EXPECTED_CASES = 96`, enforced (selftest fails if `len(cases) != 96`), and the counter independently pins the exact line `selftest cases=96 failures=0`.

## 4. Gate diff `e74ba6b5…` → `c1051749…` (item 4) — CLEAN

```
corpus/instruments/figure-audit.py | 71 ++++++++++++++++++++++++++++++++++++--
1 file changed, 68 insertions(+), 3 deletions(-)
```

- `READ_ONLY_HEADS`: 0 occurrences anywhere in the diff; imported sets equal base↔candidate: `['cat','cut','grep','head','ls','sha256sum','sort','tail','tr','wc']` — no read-only head added.
- Implementation byte-identical to the pre-freeze candidate trial (`cmp` rc 0, same sha `7a8d52eb…` as `candidate-gate-r70.py`).
- Substantive changes: new `PY_DENIED_FLAGS` + `python_flags_ok` (name + unique-abbreviation + short `-o` refusal, `--` separator ⇒ operands), wired into `python_head_ok`; 3-line doc/comment edits; `EXPECTED_CASES` 86→96; +10 `run_case` cases: `python-head-{root-space,root-equals,root-abbrev,out-space,out-equals,out-abbrev,json}-refused`, `python-head-dashdash-operand-admitted`, `git-show-no-operand-refused`, `git-show-separator-refused`.

## 5. R103 cases (item 5b)

Presence: both present at candidate gate lines 672–674, counted in the 96 pin, and both pass on the candidate selftest:

```
selftest case=git-show-no-operand-refused exit=2 want=2 verdict=pass
selftest case=git-show-separator-refused exit=2 want=2 verdict=pass
```

Behavior pre-exists the round: driving the committed probe's own `probe()`/`build_fixture()` fixture, both base and candidate gates refuse both derives at parse time (`rc=2`, `reason=derive-not-read-only`) — consistent with claims.json `non_claims` ("pin existing refusal behaviour … not a separate claim").

Own-reason isolation (scratch-only mutants of the exported gate; lane untouched):

- mutA (only the no-operand limb of `git_show_operands_ok` removed): `git-show-no-operand-refused` FLIPS to fail — `exit=1 want=2 verdict=fail reasons=derive-exit-128` — while `git-show-separator-refused` still passes; selftest `cases=96 failures=1`. Unit: mutA admits bare `git show` (True) where intact refuses (False). → the no-operand case fails for its own reason: it is load-bearing.
- mutB (only the `--`-separator limb removed): `git-show-separator-refused` STILL PASSES (`exit=2 verdict=pass`, selftest `cases=96 failures=0`). Reason: the per-operand colon rule independently refuses the case's derive — trailing operand `g.txt` has no `:`. Unit proof: mutB refuses the frozen-case form (False, via colon limb) but admits `git show HEAD:g.txt -- HEAD:g.txt` (True) where intact refuses it (False — separator limb). → the separator case does NOT fail for its own limb's removal; its refusal is over-determined, so it pins refusal of its exact input but cannot detect deletion of the separator limb.

## 6. Verdict (item 5a)

**C1 VERIFIED** against its frozen predicate. Every limb reproduced from committed bytes only: pins (§1), candidate counter 12/0 exit 0 (§2), byte-identical base counter 12/9 exit 1 with the exact P1–P7 failure anatomy (§2), selftest pin 96 (§3), byte-identity to the pre-freeze candidate trial and untouched `READ_ONLY_HEADS` (§4). Kill rule not triggered: no FAIL `MEASURE` at the candidate gate, candidate exit 0, gate sha equals the frozen candidate, base run fails P1–P7 exactly as pinned.

R103 statement: both cases are present and pass; `git-show-no-operand-refused` fails for its own reason under limb isolation; `git-show-separator-refused` passes but is over-determined by the colon rule and does not isolate the separator limb (residual pin-strength note, non-defeating — the frozen predicate requires presence + selftest pass, both hold, and the refusal itself is real on both gates).

Residual notes (non-defeating, for the record):
- The declared short `-o` refusal is implemented (`python_flags_ok` refuses `-o`, `-oVALUE`; unit checks 19/19 incl. admission of `--`-separated `--root`, `--rootless`, `-x`) but is exercised by no counter probe (P1–P7 enumerate long forms only) and no selftest case. Declared-vs-pinned gap; the frozen predicate's scope is the enumerated P1–P7 set, so C1 stands.
- C2 was not in this seat's scope and was not measured.
