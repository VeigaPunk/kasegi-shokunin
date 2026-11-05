# MutAuditC1 — independent mutation audit of the C1 counter amendment

Seat: MutAuditC1 (leaf mutation-tester, no subagents). Lane: kasegi round 74 attempt 1, wave w1.
Scope: `corpus/instruments/recheck-cwd-census.py` only, the `--selftest` of the amended counter, per
claims.json C1 kill rule (a). The lane was not written; the patch was applied only to a scratch clone.
No git mutation was run in the lane. No `census` run was made (the census executes recheck values through
`bash -c`; RC-8 stays unexpanded). No tooling was installed or updated.

## 1. Provenance and timing

- Scratch: `/fast/scratch/hyaku/kasegi-r74/MutAuditC1` (removed before yield; receipts copied below).
- Clone: `git clone --shared /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/lane` (exit 0). Clone HEAD = `847b53792d2d29d161cad7d21a33c89df9e52e8d` (freeze).
- Host guard before every clone mutation: `git -C $S/lane rev-parse --show-toplevel` = `$S/lane`.
- Base counter sha256 = `854456db322db2ee7263a0339a2b841515d36ae165c146eaa2708dfc59d3538e` (matches the r73 `orig` sha in K73MutateCounter.md).
- The patch `ExecC1Amend.patch` appeared in `w1/` about 09:00Z, inside the 25-minute window. Its wait used one background watcher (exit 0 when the file appeared), not per-turn polling.
- `git apply --check` exit 0; `git apply` exit 0. Diffstat: 1 file, 99 insertions, 23 deletions.
- Amended counter sha256 = `5ef12c7ff09937524df00a76ca3498afa1b23a52983f6e06bd4e3fc6575e2574`.
- Parse check: `python3 -c "import ast; ast.parse(...)"` exit 0.

## 2. Mutant set (designed before reading the patch)

Generator: `MutAuditC1-mutate.py` (receipt). Each mutant is one exact, count-checked substitution scoped to one
function span; a non-matching pattern aborts (exit nonzero), so no mutant is a silent no-op. The generator was run
on the base counter (red-before) and again on the amended counter (`mutate.py <src> <outdir>`, exit 0 both times).

| ID | Change | Source of the idea |
|---|---|---|
| M4p | `conform = True` in `main` (forced conformant, line and exit) | r73 M4 / RC-1 |
| M4b | RESULT line always `conformant`, exit unchanged | r73 M4 variant |
| M5p | `dir=env_tmp` → `dir="/tmp"` in `run_foreign` | r73 M5 / RC-2 |
| M6p | `shutil.rmtree` in `run_foreign` → `pass` | r73 M6 / RC-3 |
| M7p | `first_recheck` returns the LAST `recheck:` line | r73 M7 (last-line reader; no RC number assigned in claims.json) |
| M8p | `noprefix = False` (prefix comparison removed) | own (the spec's M8') |
| M8b | `noprefix = not value.startswith("cd ")` (no lane comparison) | own |
| M9p | `run_foreign` `cwd=scratch` → `cwd=DEFAULT_LANE` | own (the spec's M9') |
| M10p | `elif code == 0` → `elif code in (0, 1)` (exit 1 bucketed as 0) | own |
| M11p | `main` returns 0 unconditionally | own |
| M12p | `run_foreign` timeout returns 0 instead of -1 | own |
| E1–E6 | behaviour-preserving rewrites: `universal_newlines=True`; `line[:8] == "recheck:"`; `TIMEOUT = 121`; `dir=env_tmp or None`; reordered `verbose` operands; `dir=None` | step 5, equivalent-mutant hunt |

## 3. Results against the amended selftest

Runner: `MutAuditC1-battery.py` (receipt). Verdict rule from claims.json C1 kill rule (a): exit 0 = SURVIVED, nonzero = KILLED.
Command: `TMPDIR=<per-run dir> python3 <mutant> --selftest`, one private TMPDIR per run.

**Unmutated amended selftest** (own clone): `TMPDIR=$S/tmp/unmut python3 $S/lane/corpus/instruments/recheck-cwd-census.py --selftest` → exit 0;
last line `selftest cases=5 failures=0`; all five cases `ok`; leftover scratch 0. Receipt: `MutAuditC1-evidence.txt`, section "unmutated amended selftest".

| Mutant | rc | Verdict | Failing case line (amended selftest) |
|---|---|---|---|
| M4p forced-conformant | 1 | KILLED | `result-main FAIL nonconformant ret=0 conformant ret=0` |
| M4b result-line-only | 1 | KILLED | `result-main FAIL nonconformant ret=1 conformant ret=0` |
| M5p /tmp parent | 1 | KILLED | `tmpdir-parent FAIL calls=3 dirs='/tmp','/tmp','/tmp'` |
| M6p no rmtree | 1 | KILLED | `scratch-cleanup FAIL calls=3 leftover=3` |
| M7p last-line | 1 | KILLED | `first-line FAIL got=…exit0_foreign=1…noprefix=0 want=…noprefix=1` |
| M8p prefix removed | 1 | KILLED | `prefix-census FAIL … noprefix=0 want noprefix=2` (and first-line) |
| M10p exit1 as exit0 | 0 | **SURVIVED** | none |
| M11p result exit always 0 | 1 | KILLED | `result-main FAIL nonconformant ret=0 conformant ret=0` |
| M12p timeout as pass | 0 | **SURVIVED** | none |
| M8b cd-only prefix | 0 | **SURVIVED** | none |
| M9p foreign cwd = lane | 0 | **SURVIVED** | none |

Equivalent rows (step 5): E1, E2, E3, E4, E5, E6 all rc 0, SURVIVED. Survival is the correct result for behaviour-preserving
mutants. None is killed, so the shipped selftest is not over-fitted on this set.

Summary: the four enumerated classes (M4, M5, M6, M7) are each killed, so kill rule (a) holds for my independent set.
The selftest is not vacuous for the RC classes. Three surviving mutants (M8b, M9p, M10p, M12p) sit outside the four enumerated classes.

**Red-before on the BASE counter** (same generator and battery, `battery-base.txt`): M4p, M4b, M5p, M6p, M7p, M11p, M10p, M12p, M8b, M9p survive
the single-case base selftest (`cases=1 failures=0`, rc 0). M8p is killed by the retained prefix-census case. So the amendment changes M4/M5/M6/M7 from
survivor to killed, and changes nothing for M8b/M9p/M10p/M12p.

## 4. Findings (survivors, with the vacuous limb named)

**F1 — M8b, prefix checked against `cd ` only, not the lane (coverage gap, outside kill rule (a)).**
Vacuous limb: `prefix-census` and `first-line` only use values whose prefix equals `cd <root>` where root = lane. No case has a `cd <other>` value
with lane ≠ value. Proposed fixture P-lane (`recheck: cd /nonexistent-other-lane && true` in a tree with lane=root, expect `noprefix=1`):
M8b gives `noprefix=0` (FAIL); amended counter passes (`P-lane PASS got=entries=1,noprefix=1`). Command: `TMPDIR=<dir> python3 MutAuditC1-proposed.py <counter>`,
rc 0 amended, rc 1 M8b.

**F2 — M9p, foreign run uses cwd = lane (coverage gap, outside kill rule (a)). Answer to the L1 question: the shipped fixtures do NOT pin the foreign cwd tightly enough.**
Vacuous limb: the exit-2 expectation in `prefix-census` (`b-relative`: `python3 corpus/instruments/missing.py`) and in `first-line` gives exit 2 in
any cwd, including the real lane, because the file is absent in both. `tmpdir-parent` checks the `mkdtemp` `dir=` argument, not the subprocess cwd.
Proposed fixture P-foreign (`case "$(pwd -P)" in "<realpath TMPDIR>"/recheck-cwd-*) exit 0;; *) exit 3;; esac`, expect `exit0_foreign=1`):
M9p gives `exit_other=1` (FAIL); amended passes. The same fixture (the r73 `F-foreign` class) also fails M9p in my run of the r73 driver (`MutAuditC1-evidence.txt`, section "r73 fixture driver on base mutants").

**F3 — M10p, exit 1 bucketed as exit 0 (coverage gap, outside kill rule (a)).**
Vacuous limb: `exit1_foreign=0` in the `want` dicts of `prefix-census` and `first-line` is satisfied by zero exit-1 values. No fixture produces exit 1.
Proposed P-exit1 (`recheck: false`, expect `exit1_foreign=1 exit0_foreign=0`): M10p fails; amended passes.

**F4 — M12p, timeout counted as pass (coverage gap, outside kill rule (a)).**
Vacuous limb: no fixture exceeds `TIMEOUT`. Proposed P-timeout (monkey-patch `TIMEOUT=1`, `recheck: sleep 4`, expect `exit_other=1`): M12p fails
(`exit0_foreign=1`); amended passes (`exit_other=1`, ~4 s).

None of F1–F4 breaks kill rule (a) as written. Each is a survivor the claim's enumerated class list does not name. Folding P-lane, P-exit1, P-timeout, and
P-foreign into the existing five cases would close them without adding a case (the claim pins `cases=5`). Any such fold changes the after-predicate
wording, so it is the owner's decision.

## 5. Kill-rule (d) check (exec surface)

`grep -n bash $S/amended.py` (exit 0): one code call site, line 52 `subprocess.run(["bash", "-c", value], ...)`, identical to base. The other hit is a docstring
line 9. The amendment adds no `bash -c` call site.

## 6. Verification ledger (every number, with command and exit)

| Check | Command (abridged) | Exit |
|---|---|---|
| clone | `git clone --shared <lane> $S/lane` | 0 |
| toplevel guard | `git -C $S/lane rev-parse --show-toplevel` | 0 |
| base sha | `sha256sum orig-base.py` | 0 |
| generator, base | `python3 mutate.py orig-base.py mut-base` | 0 |
| red-before battery | `ORIG=orig-base.py python3 battery.py mut-base $S` | 0 (rows in battery-base.txt) |
| patch check/apply | `git apply --check` / `git apply` | 0 / 0 |
| amended sha | `sha256sum amended.py` | 0 |
| unmutated selftest | `python3 …/recheck-cwd-census.py --selftest` (own clone) | 0 (`cases=5 failures=0`) |
| generator, amended | `python3 mutate.py amended.py mut-amended` | 0 |
| battery, amended | `ORIG=amended.py python3 battery.py mut-amended $S` | 0 (rows in battery-amended.txt) |
| proposed fixtures | `python3 proposed.py <amended or mutant>` | 0 amended; 1 each for M8b, M9p, M10p, M12p |
| r73 fixture driver on base mutants | `python3 fixtures.py <mutant>` | rc listed in `MutAuditC1-evidence.txt` |
| exec surface | `grep -n bash amended.py` | 0 (one call site, line 52) |

Receipts (under this wave dir): `MutAuditC1-evidence.txt` (all raw battery and fixture outputs and the unmutated selftest),
`MutAuditC1-mutate.py`, `MutAuditC1-battery.py`, `MutAuditC1-proposed.py`.

## 7. Limits

- Mutants are one-line substitutions. Multi-site or semantic mutants are not in this set.
- The battery runs the selftest only. The parity limb and the census on the implementation tree are ExecC1Amend's and ReviewC1's to run;
  I did not run them, so I make no claim about kill rule (b) or about the census after-values.
- The `/tmp` leftover column in the battery counts `recheck-cwd-*` dirs created under `/tmp` during each run; it is 0 for every row. At yield, nine empty `/tmp/recheck-cwd-*` dirs (owner vgpnk, mtime 2026-11-05T05:59:06Z) are present. They predate this seat's first command (its clone was created about 08:4x Z) and this seat's runs left none, so I did not create or remove them; their origin is not established here.
- No tool was installed, upgraded, or updated. Pacman was not used.
- Scratch `$S` removed before yield (receipts copied first). Lane and fleet-root files were not written.
