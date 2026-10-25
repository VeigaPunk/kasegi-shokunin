# CritC1Kill — adversarial review of C1

Scope: review only, against the frozen C1 predicate in `.ufo/waves/round-29/claims.json`; no production edits. Axes impacted: **depth:verifiability** (test oracle quality, isolation and hermeticity) and **coverage** (whether advertised limb coverage really denotes exercised verdict paths). Evidence below is from the live working-tree bytes SHA-256 `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`; those bytes were uncommitted during this review. The canonical receipt file exists and pins the same digest, but that does not by itself prove the bytes were committed or immutable when recorded.

## Findings

### C1. Critical: `limbs=9 covered=9` does not prove fixtures were run

The coverage accounting is based on `executed.append(c['name'])`, but the PIN-BROKEN missing-git path appends the name and continues without executing its fixture (working-tree `anchorcheck.py:328-334`). It reports `SKIP pin-broken`, yet still counts that fail limb as covered. Thus `covered=9` means case names were visited or skipped, not that nine isolating failing fixtures ran.

**Reproduction receipt:** exact frozen no-Git shape (Python-only PATH) against production working-tree bytes:

```text
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
nogit_exit=0
```

This is a legitimate graceful no-Git skip, but the same numeric coverage claim is false in that environment: eight failing fixtures run and PIN-BROKEN does not. This disproves the counter's asserted semantic equivalence between `covered=9` and “every declared limb has an isolating failing fixture.” A further source-level counterexample: the registry maps names to class strings, but `covered` only checks whether each registry name appears in `executed`; it never checks that the corresponding case is marked fail/expected exit 1 or that its expected vector contains the mapped class exactly once. A registry-only mismatch can still print 9/9 if names remain.

**Smallest safe correction:** track `executed_failures` separately from skips; print `limbs=9 covered=8 skipped=1` (or equivalent) when Git is absent, and do not claim all nine fixture limbs covered. Assert registry name → case mapping plus `expected[class] == 1`, all other fail counts zero, and expected exit 1. If the C1 requirement demands exit 0 without Git, retain the clean skip but let the receipt disclose the missing PIN-BROKEN coverage rather than manufacturing it.

### C2. Critical: all frozen output counters pass a fixture-less hardcoded printer

The frozen counters assert stdout strings and a zero exit; they do not bind stdout to subprocess execution or to the subject bytes. A stub can print the expected lines and succeed while running no fixture at all.

**Reproduction receipt:** `/tmp/stub-anchorcheck.py` was a 333-byte script containing only fixed prints and exit 0; it did not create a temporary directory, invoke Git, or launch fixture cases. All three C1 counters accepted it:

```text
=== counter1 vs stub ===
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9
exit=0
=== counter2 vs stub ===
selftest cases=12 failures=0
limbs=9 covered=9
grep_exit=0
=== counter3 vs stub ===
nogit_exit=0
```

A more relevant no-op mutation of the proposed instrument (`/tmp/mutant-anchorcheck.py`) printed only `selftest cases=12 failures=0` and `limbs=9 covered=9`; the `--selftest` invocation returned 0 with no fixture execution. This is a direct strongest-counterexample to C1's conjunctive counter predicate: the predicate tests reported numbers, not construction/exercise.

**Smallest safe correction:** make the selftest's output a derived receipt over actual subprocess results, and add a discriminating mutation/control run on the actual instrument bytes to the canonical evidence (e.g. replace one case's target with a deliberately wrong class and require nonzero; suppress a fixture launch and require coverage failure). Do not accept hardcoded output alone as evidence of limb execution. The round-29 frozen claim does not explicitly require mutation resistance, so treat this as a verifier limitation unless the L1's canonical acceptance policy requires the counters themselves to authenticate the subject.

### C3. Medium: “environment sanitization” only filters `GIT_*`; remaining environment is inherited

The selftest constructs child env by retaining all parent keys except `GIT_*`, then overrides four KASEGI roots (`anchorcheck.py:323-327`). Consequently `PYTHONPATH`, `PYTHONHOME`, `HOME`, `PATH`, locale, temp-directory controls, and arbitrary Python startup/import-affecting variables remain ambient. This is not a reproduced verdict bypass for the tested `PYTHONPATH=/tmp`, `KASEGI_BOUNTIES=/nonexistent`, or `umask 077` cases (all returned the same 12/12 / 9/9 success); it is a test-isolation gap, not evidence that C1 currently fails on those values. The implementation correctly prevents ambient `GIT_DIR`/other Git variables from redirecting the pin fixture.

**Reproduction receipt:**

```text
(umask 077; python3 corpus/instruments/anchorcheck.py --selftest)
selftest cases=12 failures=0
limbs=9 covered=9
exit=0
PYTHONPATH=/tmp python3 corpus/instruments/anchorcheck.py --selftest
selftest cases=12 failures=0
limbs=9 covered=9
KASEGI_BOUNTIES=/nonexistent python3 corpus/instruments/anchorcheck.py --selftest
selftest cases=12 failures=0
limbs=9 covered=9
```

**Smallest safe correction:** establish a documented child-env allowlist (at least controlled `PATH`, `HOME`, locale and `TMPDIR`, with Python environment isolation such as `-I` or controlled startup) while preserving `sys.executable`; explicitly set umask only if filesystem mode is part of the tested contract. Add environment mutation cases for variables that affect imports, Git discovery and root selection. Do not imply the current four-root override is full hermeticity.

### C4. High: git-absence detection conflates absent Git with a non-executable `git` entry

`shutil.which('git', path=...) is None` is treated as “git not found” and PIN-BROKEN is skipped. A PATH containing a `git` file that exists but lacks execute permission is therefore treated as absence, even though the more precise distinction requested is “git absent” versus “git present but broken.” This does not raise a traceback, but can silently convert an unusable installed Git into a successful reduced-coverage selftest. Conversely, an executable but broken `git` is handled fail-closed: a reproduction script exiting 127 caused `selftest FAIL pin-broken: git init exit 127`, `covered=8`, and exit 1.

**Reproduction receipts:**

```text
# PATH has python3 symlink + non-executable git (mode 0644)
broken_git_selftest_exit=0
SKIP pin-broken (git not found)
selftest cases=12 failures=0
limbs=9 covered=9

# Same PATH, git executable but exits 127
broken_git_exec_selftest_exit=1
selftest FAIL pin-broken: git init exit 127
selftest FAIL limb coverage: missing executed cases pin-broken
selftest cases=12 failures=2
limbs=9 covered=8
```

**Smallest safe correction:** distinguish no directory entry named `git` from a found-but-not-executable candidate; skip only a true absence, otherwise fail with a named “git present but unusable” result. Keep nonzero `git init` fail-closed behavior. Align the reported skip/coverage count with C1 above.

### C5. Low: current matrix is explicit and exercises both base-absent/escape arms, but its registry and count remain hand-maintained

Positive evidence: the landed diff adds explicit outside-root cases for bounties, mirror, and origin, plus BASE-ABSENT cases for mirror and origin; the normal selftest run reported `cases=12 failures=0`, `limbs=9 covered=9`, exit 0. The arm cases use absolute prefixed spellings and expected complete class vectors, so they address the two round-28 omissions called out by frozen C1. The loop iterates the concrete `cases` list; it is not a bounded 9-iteration coverage loop or shell brace expansion.

Remaining blind spot: `LIMBS` and `cases` are separate declarations. The output's case count is simply `len(cases)` (not an independently frozen expected 12), and coverage compares names only. A developer can delete or misconfigure a case and update its name/registry coherently, with no independent expectation of nine/12. This is a maintainability/anti-regression weakness rather than a failure reproduced against the current matrix.

**Smallest safe correction:** validate exact registry-to-case mapping and expected failure vector programmatically; pin expected case/limb totals as explicit contract constants or derive them from a single declarative case registry. Add a test mutation that deletes/renames one case and must make the completeness assertion fail.

### C6. High: receipt timing / committed identity is not independently established by the receipt

At review time, production `anchorcheck.py` was modified in the worktree, not committed (`git status` showed `M corpus/instruments/anchorcheck.py`); its worktree hash matched the canonical receipt's `instrument_sha256`. The receipt states it re-hashed immediately before writing and says “landed production bytes,” but the receipt alone does not demonstrate a commit containing those bytes, nor that a later post-commit recheck used the commit tree rather than mutable worktree bytes. The frozen C1 kill rule says “committed anchorcheck.py digest.” The round-28 lesson specifically records report-before-commit as routed M28-2 and says a marker is not a round (R4). The current receipt is therefore useful live-work evidence but is not yet proof of the frozen committed-byte clause.

**Reproduction receipt:**

```text
HEAD at review: 46e07f6 (round-29 dispatch)
worktree: M corpus/instruments/anchorcheck.py
worktree sha256: 68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97
canonical receipt line 3: same sha256
receipt line 5: claims re-hash immediately before write
```

The receipt exists after the implementation report and after the matching production digest was present, so there is no evidence it predates this specific implementation; the unresolved problem is identity/commit binding, not a proven race.

**Smallest safe correction:** after the implementation commit, independently compute `git show <commit>:corpus/instruments/anchorcheck.py | sha256sum`, compare that digest to the receipt, and record the commit hash plus post-commit rerun. Do not claim committed-digest satisfaction until this is observed.

## C1 verdict for L1

C1 has materially improved test construction: nine declared failure arms and three controls are present, and ordinary/selftest + no-Git executions on the worktree bytes exit 0. But the strongest literal interpretation of `covered=9` is currently false in the very no-Git case C1 requires: PIN-BROKEN is skipped yet counted covered. The frozen observable predicate is met, but its semantic statement (“every declared verdict limb has an isolating failing fixture”) is not. Hardcoded output demonstrates that the frozen counters alone are not an authenticated test oracle. The canonical judge should decide whether these are kill-level gaps or limitations outside the stated measurable predicate; they are fixable, not evidence of a production citation-class regression.
