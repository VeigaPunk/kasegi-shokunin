# MutC1 — independent C1 mutant battery (round 77, attempt 1)

Seat: MutC1 (leaf, read-only against frozen bytes at 539a43877809bd90b6f506e8fd24a6d871598cd5).
Frozen inputs checked: `.ufo/waves/round-77/c1-amended-reference.py` sha256 `18bfc439…588a33` (matches the table); `.ufo/waves/round-77/c1-mutant-transforms.md` sha256 `0bc7073a…e22130`.
Base counter `corpus/instruments/recheck-cwd-census.py` at 2e53fc74: sha256 `e666ae11…ab52a21a` (matches the table).
Evidence copies: `.ufo/waves/round-77/w1/MutC1-evidence/` (run receipts, my mutant copies, SHA256SUMS.mine / SHA256SUMS.committed).

Process: I derived all mutants from the transform table and the reference (lines 264-265, 253, 329, 281-284; plus extras at 305-310 and 240-241) before opening any `controls/m*.py`. Edits were applied with the edit tool to scratch copies. Every run used `TMPDIR` set to a per-run scratch dir and `python3 -B <file> --selftest`. No tooling was installed. No git mutation was run.

## 1. Verdict matrix (own derivations, `python3 -B <mutant> --selftest`)

| mutant | rc | failure class (observed lines) | final line | expected (table) | match |
|---|---|---|---|---|---|
| K-M1 registration removed | 1 | assertion: `gate-regs FAIL registered=[]`; `gate-consume FAIL no-registration`; `gate-negpolarity FAIL no-registration` | `cases=12 failures=3` | gate-regs FAIL + both no-registration FAILs, no traceback | YES |
| K-M2 closure body → `True` | 1 | assertion: `gate-consume ok clean_ok=True`; `gate-negpolarity FAIL neg_ok=True` | `cases=12 failures=1` | gate-consume ok clean_ok=True; gate-negpolarity FAIL neg_ok=True | YES |
| K-M3 case-6 `main()` call deleted | 1 | exception: `gate-consume FAIL exception=NameError("name 'out6' is not defined")`; `gate-negpolarity FAIL not-evaluated-after-exception` | `cases=12 failures=2` | NameError logged distinctly | YES |
| K-M4 `neg_ok is False` → `is True` | 1 | assertion: `gate-consume ok clean_ok=True`; `gate-negpolarity FAIL neg_ok=False` | `cases=12 failures=1` | neg_ok=False FAIL | YES |
| K-M5 `both-headers` check call deleted | 1 | assertion: `gate-checkids FAIL missing=['both-headers'] extra=[]` | `cases=11 failures=1` | missing=['both-headers'], cases=11 | YES |
| K-M6 (extra) case-8 `relabel-detection` check call deleted (ref lines 305-310) | 1 | assertion: `gate-checkids FAIL missing=['relabel-detection'] extra=[]` | `cases=11 failures=1` | gate-checkids FAIL missing=['relabel-detection'], rc 1 | YES |
| K-M7 (extra, class generalization) `first-line` check call deleted (ref lines 240-241) | 1 | assertion: `gate-checkids FAIL missing=['first-line'] extra=[]` | `cases=11 failures=1` | n/a (generalization probe) | generalizes |
| K-M8 (extra, OUT of named classes) `relabel-detection` body neutered to `check("relabel-detection", True, "forced")` (ref lines 305-310) | **0** | none | `cases=12 failures=0` | n/a | **SURVIVED** |

No run produced a Python traceback (`grep -l Traceback run/*.out` → 0 files).

### Committed-control comparison (controls/m*.py)

| mutant | my sha256 (first 16) | committed sha256 (first 16) | byte-identical | delta |
|---|---|---|---|---|
| m1 | c274649223deecdc | c274649223deecdc (committed table prefix c2746492) | YES | none |
| m2 | 9bf8f877 0a75e01a | b7772949 f3b70f16 | NO | layout only: committed collapses the lambda to one line `lambda out, ret: True`; mine keeps `lambda out, ret: (` / `True)`. `diff` shows the two-line difference only. Full selftest stdout is receipt-equivalent (see below). |
| m3 | 1fd8d29a d085ce03 | 1fd8d29a … | YES | none |
| m4 | 7f5bb9360d9eaa38 | 7f5bb9360d9eaa38 | YES | none |
| m5 | b7af7722 23131dc6 | b7af7722 … | YES | none |

Each `diff` of my mutant against the frozen reference shows only the intended transform (m1: lines 264-265 deleted; m2: line 265 changed; m3: line 253 deleted; m4: line 329 `is False`→`is True`; m5: lines 281-284 deleted).

Receipt comparison: my runs versus `controls/m*.out` agree line for line, after normalising the per-run TMPDIR path in the `tmpdir-parent` line (the committed receipt ran with TMPDIR unset and prints `dirs=None`). The five verdict/rc pairs match.

## 2. K-M2 required-kill call

**KILLED-BY-ASSERTION.** The registered closure returns True on the case-2 negative-polarity input (`neg_ok=True`), which trips the `neg_ok is False` assertion at reference line 329, with `gate-negpolarity FAIL neg_ok=True`, rc 1, and no exception. The kill comes from a boolean assertion, not from an exception path.

## 3. Extra mutants and class generalization

- K-M6 and K-M7 both fail `gate-checkids` by name (`missing=['relabel-detection']`, `missing=['first-line']`), alongside K-M5 (`missing=['both-headers']`). Three different case checks have now been shown to be caught, so the gate detects deletion of any named check, not only the one named in the table.
- Limit (from the code, reference lines 334-336; verified by K-M8): `gate-checkids` compares only the set of names in `done`. It does not look at each check's verdict or at duplicate calls [INFERENCE for duplicates; not run].
- K-M8 is the real gap. Neutering a case-level check body to `True` leaves the gate green (`rc 0`, `cases=12 failures=0`). The transform table's known-limits paragraph names only the `neg_ok` boolean and composite mutants. A case-body neutering is not listed in that paragraph, so this is a routed survivor for the next round. It does not overturn the five frozen kills. It does show that the eight case checks are verified only by presence, not by their own assertions.

## 4. Red-before

- Base counter (2e53fc74, `corpus/instruments/recheck-cwd-census.py`, sha `e666ae11…`): `python3 -B … --selftest` → `selftest cases=6 failures=0`, rc 0. This matches `controls/c1-donothing-selftest-r77.txt`.
- r76 survivor receipt: `.ufo/waves/round-76/controls/m2b-conjunct-removed.py` (blob 6c807f65, read from the freeze commit), run with `TMPDIR` set → `selftest cases=8 failures=0`, rc 0. This matches `controls/c1-redbefore-r76-survivor-r77.txt`. The r76 survivor (a conjunct-removed mutant that still passes its own selftest) stands.

## 5. Findings for the planner

1. Five frozen kills reproduce as stated in the transform table (K-M1..K-M5). K-M2 is KILLED-BY-ASSERTION.
2. K-M2 committed control differs from my derivation in line layout only (behaviourally identical; receipts match). Byte-level: `controls/m2-consumption-neutered.py` sha `b7772949…` vs my `9bf8f877…`.
3. Routed survivor (not a frozen claim failure): K-M8, a neutered case-level check, passes the gate. Suggested next-round kill: a `gate-checkids` that also requires each check's detail or verdict to be consumed, or per-check mutants. Routed, not edited.
4. No file in the lane tree was modified. Scratch dir `/fast/scratch/hyaku/kasegi-r77/MutC1/` is removed before yield. Evidence copies live in `.ufo/waves/round-77/w1/MutC1-evidence/`.

Tools installed this seat: none. Commands run: `python3 -B`, `diff`, `cmp`/`sha256sum`, `cp`, `git show` / `git ls-tree` (read-only).
