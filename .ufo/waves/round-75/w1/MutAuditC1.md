# MutAuditC1 — C1 amendment mutation battery (kasegi r75, wave w1)

Seat: MutAuditC1 (mutation-tester, leaf). Date: 2026-11-05.
Target invariant: the C1 amendment of `corpus/instruments/recheck-cwd-census.py` (claims.json C1 target (i)–(iv), kill rule A3).
Detector: the amended counter's own `--selftest`, run under an explicit `TMPDIR`.

Report: .ufo/waves/round-75/w1/MutAuditC1.md

## Provenance

- Base export: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 748dfb666280adfb1e249fcf6a265c5d9951eefb:corpus/instruments/recheck-cwd-census.py` → exit 0, 238 lines / 10349 bytes, sha256 `5ef12c7ff09937524df00a76ca3498afa1b23a52983f6e06bd4e3fc6575e2574`.
- Amendment: ExecC1Amend's patch `.ufo/waves/round-75/w1/ExecC1Amend.patch`, applied with `git apply --check -p1` then `git apply -p1` in scratch → exit 0 both. Amended sha256 `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a`. Full diff evidence: `MutAuditC1-amended.diff` beside this report.
- Timing note (required by tasking): at my first check the patch file was absent (only SentinelCounter evidence present), so I prepared a self-derived amendment per claims.json; the patch appeared before the battery ran, so the battery below ran against the REAL ExecC1Amend.patch bytes. The self-derived copy was discarded unused; SentinelCounter-derived-C1.diff was not needed.
- All work in scratch `/fast/scratch/hyaku/kasegi-r75/MutAuditC1/` (removed before yield, see Restoration). No lane-tree writes except this report + the `MutAuditC1-*` evidence files beside it. No tool installs were needed or made (nothing to record under RULES.md). Pacman untouched.

## (1) Pristine run (amended counter, unmutated)

Command: `TMPDIR=/fast/scratch/hyaku/kasegi-r75/MutAuditC1/tmp python3 /fast/scratch/hyaku/kasegi-r75/MutAuditC1/amended/recheck-cwd-census.py --selftest` (exit 0)

```
selftest cases=6 failures=0
```

PASS — matches frozen A1 shape. Receipt: `MutAuditC1-pristine.txt`.

Control (unamended base counter, same detector): `selftest cases=5 failures=0`, exit 0 — the unamended counter survives its own 5-case selftest, matching claims C1 `before.selftest` and A3's survival clause. Receipt: `MutAuditC1-base-control.txt`.

## (2)+(3) Mutants — byte-edit, selftest's own failing output, exit code, verdict

Each mutant is a copy of the amended file with one minimal behavior-bearing edit (sha256 of each mutant is in its receipt). Run command for every mutant: `TMPDIR=<scratch>/tmp python3 <scratch>/mutants/<name>.py --selftest`.

| mutant | byte-edit (line refs = amended file) | selftest output (failing line) | exit | verdict |
|---|---|---|---|---|
| M-P1 | L93-94: `counts["restoration_only"] += 1` → `counts["norecheck"] += 1` in the restoration-only branch (norecheck incremented, restoration_only stays 0) | `selftest case=restoration-only FAIL got=…norecheck=1,restoration_only=0 want=…norecheck=0,restoration_only=1 marker_present=False main_ret=1` + `selftest cases=6 failures=1` | 1 | **killed=yes** (A3 class M-A) |
| M-P2 | L274-275: RESULT gate drops the `restoration_only == 0` conjunct | `selftest case=restoration-only FAIL got==want marker_present=False main_ret=0` + `selftest cases=6 failures=1` (counts right, but main() wrongly reports conformant) | 1 | **killed=yes** (A3 class M-B, minimal form) |
| M-P3 | L274: whole gate expression → `conform = True` (nonconformant limb asserted to a tautology) | `selftest case=result-main FAIL nonconformant ret=0 conformant ret=0` AND `selftest case=restoration-only FAIL … main_ret=0` + `selftest cases=6 failures=2` | 1 | **killed=yes** |
| M-P4 | L243: marker-absent conjunct `and not marker6` deleted from case 6's check | `selftest cases=6 failures=0` | 0 | **killed=no — SURVIVED** (see Finding F-1) |
| M-P5 | L94-96: restoration value read from r.md and routed through `run_foreign(...)` — i.e. executed via `bash -c`; counting unchanged | `selftest case=restoration-only FAIL … marker_present=True main_ret=1` + `selftest cases=6 failures=1` (the touch marker got created) | 1 | **killed=yes** (A3 class M-C) |
| M-P6 | docstring-only amendment: base behavior kept, patch's docstring hunks + case 6 + `cases=6` print applied; no `restoration_only` key/routing/gate change | case 6 assertion evaluation raises `KeyError: 'restoration_only'` (in `got6[k]`) before `check()` can print; traceback, no `cases=` line | 1 | **killed=yes** (case 6 fails — behavioral, not documentation) — shape deviation, see Finding F-2 |

Battery summary (verbatim from `MutAuditC1-battery.txt`):

```
control=base-unamended survived=yes expected=yes exit=0 selftest="selftest cases=5 failures=0"
pristine=amended pass=yes exit=0 selftest="selftest cases=6 failures=0"
mutant=M-P1 killed=yes exit=1 cases="selftest cases=6 failures=1" fails=1 crash=False
mutant=M-P2 killed=yes exit=1 cases="selftest cases=6 failures=1" fails=1 crash=False
mutant=M-P3 killed=yes exit=1 cases="selftest cases=6 failures=2" fails=2 crash=False
mutant=M-P4 killed=no exit=0 cases="selftest cases=6 failures=0" fails=0 crash=False
mutant=M-P5 killed=yes exit=1 cases="selftest cases=6 failures=1" fails=1 crash=False
mutant=M-P6 killed=yes exit=1 cases="None" fails=0 crash=True
```

## Findings (coverage observations; NOT contract changes — the claims text stays as frozen)

- **F-1 (M-P4 survival, coverage finding):** the "restoration value is never executed" guard is single-stranded. The marker-absent conjunct (`not marker6`) is the ONLY detector of restoration-value execution: M-P5's kill depends entirely on it (its counts all stay correct; only `marker_present=True` fails), so deleting that conjunct (M-P4) leaves nothing that fails — `cases=6 failures=0`, exit 0. A selftest cannot detect edits to its own assertions; killing an assertion-removal mutant would require a redundant second detector (e.g. asserting the census made no `run_foreign` call for restoration entries), which would be an amendment change — L1's call, not mine.
- **F-2 (M-P6 failure shape):** under a pure docstring-only amendment (M74-6 class), case 6 does fail — the mutant dies exit 1 — but via an unguarded `KeyError: 'restoration_only'` inside case 6's `got6[k]` lookup, not via the selftest's own `FAIL` line (the crash happens before `check()` prints, so no `selftest cases=6 failures=1` line is emitted). Supplementary run **M-P6b** (same doc-only counter but keeping an inert `restoration_only=0` dict key + summary field, routing and gate reverted) produces the prescribed shape: `selftest case=restoration-only FAIL got=…norecheck=1,restoration_only=0 want=… marker_present=False main_ret=0` + `selftest cases=6 failures=1`, exit 1 (`MutAuditC1-M-P6b-supplementary.txt`). Together: case 6 is behavioral, not documentation — the M74-6 class is falsified as claimed. If ExecC1Amend wants doc-only mutants to die with a printed FAIL line instead of a KeyError, `.get()`-based access in case 6 is the hygiene fix; flagging only, not changing.
- **M-P3 reading note:** "case 6's main() nonconformant limb removed or asserted to a tautology" is implemented on the main() side (`conform = True`): the test-side reading (deleting/weakening case 6's own assertion) cannot fail a selftest by construction — same reasoning as F-1. Main-side tautology kills via BOTH case 2 (result-main) and case 6, `failures=2`.
- **M-P5 / RC-8:** the mutant demonstrates exactly the hazard RC-8 flags — routing restoration values through `run_foreign` executes them (marker created, caught by case 6). The amended counter itself keeps exactly ONE `bash -c` call site: `grep '"bash", "-c"' amended/recheck-cwd-census.py` → single hit at line 70 inside `run_foreign` (exit 0). Exec-surface continuity holds for the amendment as patched.

## (4) Restoration evidence

- Mutants are separate copies; nothing edited the pristine or base bytes in place. sha256 before == after the whole battery, including a post-battery rerun of pristine:
  - base `5ef12c7ff09937524df00a76ca3498afa1b23a52983f6e06bd4e3fc6575e2574` (unchanged)
  - amended `e666ae11fd9d50ecea107b8835090eed0dc798e8e8a233324b9fbd59ab52a21a` (unchanged), rerun after battery: `selftest cases=6 failures=0`, exit 0 (`MutAuditC1-pristine-rerun.txt`)
- Scratch `/fast/scratch/hyaku/kasegi-r75/MutAuditC1/` removed after receipts were copied into this wave dir; cleanup verified by the follow-up `test -d` (absent).

## Verdict for integration

A1 shape holds on ExecC1Amend's patched counter (pristine `cases=6 failures=0` exit 0). A3's kill rule is satisfied: mutant classes M-A (M-P1), M-B (M-P2), M-C (M-P5) all die `cases=6 failures=1`, exit 1, plus M-P3 (`failures=2`) and M-P6 (exit 1, case-6 crash). One honest exception to the "all six killed" battery expectation: M-P4 as prescribed (delete the marker-absent assertion) survives by construction — recorded above as finding F-1, not a claim failure; A1–A4 are unaffected.

Report: .ufo/waves/round-75/w1/MutAuditC1.md
