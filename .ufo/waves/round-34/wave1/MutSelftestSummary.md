# MutSelftestSummary — kasegi round 34, wave 1

Seat assignment: forge-summary mutant against the landed `corpus/instruments/capture-binding-check.py`
selftest runner — replace the per-case lines with only `selftest cases=0 failures=0` (exit 0); the
landed bytes must reject it (exit != 0, marker `summary-only-selftest-rejected`); likewise a forged
`selftest cases=19 failures=0` with no per-case lines must be rejected. Demonstrate both against the
landed bytes in scratch. Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze
`29f606dbdd28aff6fd4573ab4b90788bbb90af13`. Lane writes by this seat: this receipt only.

## Report

### 0. Invariant under test and provenance

- Frozen claim C1 (`.ufo/waves/round-34/claims.json`, "after" bullet): `capture-binding-check
  --selftest` prints `selftest cases=N failures=0`, N>=19, incl. named case
  `summary-only-selftest-rejected`.
- Mutant provenance (round 33): M4 `skip-selftest` printed `selftest cases=9 failures=0` exit 0
  without running a fixture and **survived** the frozen kill rule
  (`corpus/lessons/round-33.md:233`; `corpus/lessons/round-33-verifier-spotcheck.md:79-84` F-5;
  R4 at `:173-177`). The landed defense: `judge_selftest_report`
  (`corpus/instruments/capture-binding-check.py:758-791`) appends problem `summary-only-report`
  when a report carries no `selftest case=` line (`:767-768`), and `REPORT_CASES` (`:806-810`)
  exercises it as case `summary-only-selftest-rejected` (must be rejected) against control
  `complete-selftest-report-accepted` (must be accepted).

### 1. Landed bytes and pristine baseline

Command (cwd = lane root; scratch under the seat tree):

```sh
S=/fast/scratch/hyaku/kasegi-r34/MutSelftestSummary && mkdir -p "$S/pristine" "$S/mutA" "$S/mutB" "$S/runs" && cp corpus/instruments/capture-binding-check.py "$S/pristine/capture-binding-check.py" && sha256sum corpus/instruments/capture-binding-check.py "$S/pristine/capture-binding-check.py" && python3 corpus/instruments/capture-binding-check.py --selftest --scratch "$S/runs/selftest-scratch" 2>"$S/runs/pristine-selftest.err" | tee "$S/runs/pristine-selftest.out"; echo "pristine-selftest-exit=${PIPESTATUS[0]}"; echo "--- stderr bytes:"; wc -c "$S/runs/pristine-selftest.err"
```

Output (verbatim):

```text
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  /fast/scratch/hyaku/kasegi-r34/MutSelftestSummary/pristine/capture-binding-check.py
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=shared-url-between-two-records exit=0 want=0 verdict=pass
selftest case=duplicate-id-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest case=fetched-utc-pending-rejected exit=1 want=1 verdict=pass
selftest case=fetched-utc-local-offset-rejected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-detected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-listed exit=0 want=0 verdict=pass
selftest case=nested-snapshot-dir exit=0 want=0 verdict=pass
selftest case=nested-snapshot-missing-manifest exit=1 want=1 verdict=pass
selftest case=dup-record-in-manifest exit=1 want=1 verdict=pass
selftest case=double-https-row exit=1 want=1 verdict=pass
selftest case=rejected-row-anchor exit=1 want=1 verdict=pass
selftest case=summary-only-selftest-rejected exit=1 want=1 verdict=pass
selftest case=complete-selftest-report-accepted exit=0 want=0 verdict=pass
selftest cases=23 failures=0
pristine-selftest-exit=0
--- stderr bytes:
0 /fast/scratch/hyaku/kasegi-r34/MutSelftestSummary/runs/pristine-selftest.err
```

Baseline: exit 0, N=23 (>= 19), all 23 case lines `verdict=pass`, including the landed bytes' own
exercise of the rejection — `selftest case=summary-only-selftest-rejected exit=1 want=1
verdict=pass` (the forged report's observed exit is 1, i.e. exit != 0, exactly the marker case).

### 2. Detector = the landed bytes, unmodified

- The detector is `judge_selftest_report` from the **landed** file, imported by absolute path via
  `importlib` (module-level code is constants/functions only — `:148-176` — so import has no side
  effects). The landed file was never opened for writing by this seat.
- Expected names computed with the landed runner's own arithmetic (`:825-826`):
  N=23 = 21 `CASES` + 2 `REPORT_CASES`:
  `clean-all-pass, missing-manifest-dir, record-without-url, shared-url-between-two-records,
  duplicate-id-rows, url-mismatch, no-row, shared-url-not-a-failure,
  round-32-record-without-fetched_utc, pre-round-32-record-without-archival,
  round-32-record-with-fetched_utc-passes, pre-round-32-archival-passes,
  fetched-utc-pending-rejected, fetched-utc-local-offset-rejected, per-file-orphan-detected,
  per-file-orphan-listed, nested-snapshot-dir, nested-snapshot-missing-manifest,
  dup-record-in-manifest, double-https-row, rejected-row-anchor, summary-only-selftest-rejected,
  complete-selftest-report-accepted`.
- "Exit != 0" is evaluated with the landed runner's own observed-exit arithmetic (`:849`):
  `observed = 0 if not problems else 1`.

### 3. Forgery A — `selftest cases=0 failures=0`, no per-case lines

Input text: `"selftest cases=0 failures=0\n"`. Landed detector verdict: **observed_exit=1** with
exactly 25 problems (verbatim):

```python
['summary-only-report', 'case-line-count case=clean-all-pass count=0', 'case-line-count case=missing-manifest-dir count=0', 'case-line-count case=record-without-url count=0', 'case-line-count case=shared-url-between-two-records count=0', 'case-line-count case=duplicate-id-rows count=0', 'case-line-count case=url-mismatch count=0', 'case-line-count case=no-row count=0', 'case-line-count case=shared-url-not-a-failure count=0', 'case-line-count case=round-32-record-without-fetched_utc count=0', 'case-line-count case=pre-round-32-record-without-archival count=0', 'case-line-count case=round-32-record-with-fetched_utc-passes count=0', 'case-line-count case=pre-round-32-archival-passes count=0', 'case-line-count case=fetched-utc-pending-rejected count=0', 'case-line-count case=fetched-utc-local-offset-rejected count=0', 'case-line-count case=per-file-orphan-detected count=0', 'case-line-count case=per-file-orphan-listed count=0', 'case-line-count case=nested-snapshot-dir count=0', 'case-line-count case=nested-snapshot-missing-manifest count=0', 'case-line-count case=dup-record-in-manifest count=0', 'case-line-count case=double-https-row count=0', 'case-line-count case=rejected-row-anchor count=0', 'case-line-count case=summary-only-selftest-rejected count=0', 'case-line-count case=complete-selftest-report-accepted count=0', 'summary-cases=0 want=23']
```

**REJECTED** (exit != 0): `summary-only-report` (`:767-768`), one `case-line-count` per expected
name, and the summary's `cases=0` contradicts N=23 (`summary-cases=0 want=23`).

### 4. Forgery B — `selftest cases=19 failures=0`, no per-case lines

Input text: `"selftest cases=19 failures=0\n"`. Landed detector verdict: **observed_exit=1** with
the same 25-problem shape, the tail differing only in the summary clause:
`[... 'case-line-count case=complete-selftest-report-accepted count=0', 'summary-cases=19 want=23']`.
So the forged count 19 is rejected twice over: as a summary-only report and because 19 != the
landed case count 23. **REJECTED** (exit != 0).

### 5. Mutant runs — the F-5 shape reproduced on scratch copies

Mutation point (smallest behavior-bearing point for the emitted report): the emission loop
`corpus/instruments/capture-binding-check.py:859-860`
(`for line in report:` / `print(line, file=out)`) replaced by a single
`print("selftest cases=0 failures=0", file=out)` (mutA) / `print("selftest cases=19 failures=0",
file=out)` (mutB). The internal report list and the structural self-check (`:861-865`) are
untouched, so the mutant exits 0 while emitting summary-only bytes — the exact round-33 F-5
survivor shape (the frozen kill rule read only the summary/exit and did not bite).

Probe source (the executed cell, verbatim; `phase(...)` is the kernel's section logger):

```python
import hashlib, importlib.util, os, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
LANDED = LANE + "/corpus/instruments/capture-binding-check.py"
S = "/fast/scratch/hyaku/kasegi-r34/MutSelftestSummary"
PRISTINE = S + "/pristine/capture-binding-check.py"
MUTA = S + "/mutA/capture-binding-check.py"
MUTB = S + "/mutB/capture-binding-check.py"

def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()

phase("0. landed digest before")
h_before = sha(LANDED)
print("landed sha256 (before):", h_before)

phase("1. scratch copies of landed bytes")
landed_bytes = open(LANDED, "rb").read()
for p in (PRISTINE, MUTA, MUTB):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as fh:
        fh.write(landed_bytes)
print("pristine copy sha256:", sha(PRISTINE), "matches landed:", sha(PRISTINE) == h_before)

phase("2. build mutants: smallest behavior-bearing point = emission loop (lines 859-860)")
TARGET = '        for line in report:\n            print(line, file=out)\n'
src = landed_bytes.decode()
n = src.count(TARGET)
print("emission-loop target occurrences in landed bytes:", n)
assert n == 1, "mutation target not unique"
mutA_src = src.replace(TARGET, '        print("selftest cases=0 failures=0", file=out)\n')
mutB_src = src.replace(TARGET, '        print("selftest cases=19 failures=0", file=out)\n')
with open(MUTA, "w") as fh:
    fh.write(mutA_src)
with open(MUTB, "w") as fh:
    fh.write(mutB_src)
print("mutA sha256 (mutated):", sha(MUTA))
print("mutB sha256 (mutated):", sha(MUTB))

phase("3. detector = landed bytes, imported unmodified")
spec = importlib.util.spec_from_file_location("cbcheck_landed", LANDED)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
expected = [nm for nm, _b, _w, _l in mod.CASES] + [nm for nm, _f, _e in mod.REPORT_CASES]
print("expected names N=%d" % len(expected))
for nm in expected:
    print("   ", nm)

def judge(text, label):
    problems = mod.judge_selftest_report(text, expected)
    observed = 0 if not problems else 1  # landed arithmetic, capture-binding-check.py:849
    print("%s\n  observed_exit=%d\n  problems=%s" % (label, observed, problems))
    return problems, observed

phase("4. accept control: detector on pristine emitted report")
pristine_out = open(S + "/runs/pristine-selftest.out").read()
p_pristine, o_pristine = judge(pristine_out, "pristine --selftest stdout (bash run, saved)")
print("  accepted:", o_pristine == 0)

phase("5. forgery A: summary-only 'selftest cases=0 failures=0'")
forgeryA = "selftest cases=0 failures=0\n"
pA, oA = judge(forgeryA, "forgery A %r" % forgeryA)

phase("6. forgery B: summary-only 'selftest cases=19 failures=0', no per-case lines")
forgeryB = "selftest cases=19 failures=0\n"
pB, oB = judge(forgeryB, "forgery B %r" % forgeryB)

phase("7. control: well-formed report must be accepted (not an always-reject limb)")
pC, oC = judge(mod.forged_complete(expected), "forged_complete(expected)")

phase("8. mutant runs (F-5 shape: summary-only stdout, exit 0)")
verdicts = {}
for tag, mutp, want_stdout in (("mutA", MUTA, "selftest cases=0 failures=0\n"),
                               ("mutB", MUTB, "selftest cases=19 failures=0\n")):
    proc = subprocess.run([sys.executable, mutp, "--selftest", "--scratch", S + "/runs/scrub-" + tag],
                          capture_output=True, text=True)
    print("%s --selftest exit=%d stdout=%r stderr=%r" % (tag, proc.returncode, proc.stdout, proc.stderr))
    shape_ok = proc.returncode == 0 and proc.stdout == want_stdout and proc.stderr == ""
    print("  F-5 shape (summary-only stdout, exit 0):", shape_ok)
    p, o = judge(proc.stdout, "%s emitted report" % tag)
    verdicts[tag] = "KILLED (landed detector rejects emitted report)" if p else "SURVIVED"
    print("  %s verdict: %s" % (tag, verdicts[tag]))

phase("9. restoration: exact landed bytes back over mutant copies")
for p in (MUTA, MUTB):
    with open(p, "wb") as fh:
        fh.write(landed_bytes)
print("mutA restored sha256:", sha(MUTA), "== landed:", sha(MUTA) == h_before)
print("mutB restored sha256:", sha(MUTB), "== landed:", sha(MUTB) == h_before)
h_after = sha(LANDED)
print("landed sha256 (after):", h_after, "== before:", h_after == h_before)

phase("10. summary")
print("forgery A (cases=0):", "REJECTED observed_exit=%d" % oA if pA else "ACCEPTED -- INVARIANT BROKEN")
print("forgery B (cases=19):", "REJECTED observed_exit=%d" % oB if pB else "ACCEPTED -- INVARIANT BROKEN")
print("mutA:", verdicts["mutA"])
print("mutB:", verdicts["mutB"])
print("controls: pristine accepted=%s, forged_complete accepted=%s" % (o_pristine == 0, oC == 0))
```

Measured results (key lines verbatim; the full 25-entry problems lists are quoted in §3/§4 —
the mutant-emitted reports are byte-identical to the forgeries, so their lists are the same):

```text
emission-loop target occurrences in landed bytes: 1
mutA sha256 (mutated): 7b04332799bd3188dcbda418e3affc71b77c8183c0883c3d042c0c8e3fc378af
mutB sha256 (mutated): 2cc2f65be2c70040460f5fa7af4d1d2fb7d29302069e038f20bd366da5c13ca0
mutA --selftest exit=0 stdout='selftest cases=0 failures=0\n' stderr=''
  F-5 shape (summary-only stdout, exit 0): True
  mutA emitted report: observed_exit=1  problems=[... 25 entries as §3 ...]
  mutA verdict: KILLED (landed detector rejects emitted report)
mutB --selftest exit=0 stdout='selftest cases=19 failures=0\n' stderr=''
  F-5 shape (summary-only stdout, exit 0): True
  mutB emitted report: observed_exit=1  problems=[... 25 entries as §4 ...]
  mutB verdict: KILLED (landed detector rejects emitted report)
```

Both mutants emitted exactly the forged summary and exited 0 (the F-5 survivor shape against the
frozen round-33 kill rule); the landed report checker rejects both emitted reports
(observed_exit=1). **KILLED / KILLED.**

### 6. Controls — the checker is not an always-reject limb

- Pristine emitted report (the bash baseline stdout of §1): `observed_exit=0, problems=[]` —
  accepted.
- `mod.forged_complete(expected)` (per-case lines + true summary, `:799-803`):
  `observed_exit=0, problems=[]` — accepted, matching the landed case
  `complete-selftest-report-accepted exit=0 want=0 verdict=pass` in the baseline run.
  The rejection is therefore discriminative, not unconditional.

### 7. Corroboration — the committed kill-rule counter kills the same mutant end-to-end

Command (cwd = lane root, scratch confined to the seat tree):

```sh
python3 corpus/instruments/kill-rule-check.py --scratch "$S/runs/killrule-scratch"
```

Key output (verbatim; full log in the seat transcript):

```text
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=77ff705c785f2b01f7d2c974fffb1090734dc7bfdd54ae53edbc17c20f690b52
mutant-patch name=skip-selftest-summary patch_sha256=c457083e5d99f9f0 find_sha256=e6262244cffa1e1e find_count=1 status=ok
mutant-bytes name=skip-selftest-summary pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=b9d40dbee7521dbd
mutant-probe name=skip-selftest-summary probe=selftest-shape pristine=pass mutant=fail exit=0 reasons=summary-only;case-set-mismatch
mutant=skip-selftest-summary killed=1
mutants=3 killed=3 survivors=0 invalid=0
gates=6 failed=0
survivors=0
killrule-exit=0
```

The counter's own `skip-selftest-summary` row (`kill-rule-check.py:113-122`) patches the loop
entry (not the emission point) to the same forged `selftest cases=0 failures=0` + `return 0`, and
its OUTPUT SHAPE gate (`:15-21`, `CASE_FLOOR = 19` at `:103`) rejects the mutant's emitted stdout
with `reasons=summary-only;case-set-mismatch`. The forged summary is rejected both at the report
checker (§3-§5) and by the committed counter that replays it against copied instrument bytes.

### 8. Side finding (outside the assigned probe; recorded for the L1, not fixed here)

`python3 corpus/instruments/kill-rule-check.py --selftest` (cwd = lane root, no other arguments)
prints `selftest cases=3 failures=1` and **exits 1** (stderr empty):

```text
selftest case=all-killed got=(3, 0, 0, 0) want=(3, 0, 0, 0) verdict=pass
selftest case=one-survivor got=(2, 1, 0, 1) want=(2, 1, 0, 1) verdict=pass
selftest case=one-invalid got=(2, 0, 1, 1) want=(1, 0, 1, 1) verdict=fail
selftest cases=3 failures=1
killrule-selftest-exit=1
```

Cause, measured on the landed bytes: the `one-invalid` scenario (`kill-rule-check.py:525`) feeds
`summarise(["killed", "invalid:find-count", "killed"])` — a vector with **two** `"killed"` strings
— while `summarise` (`:438-443`) counts `killed` as exact matches, so the arithmetically correct
tuple for that input is `(2, 0, 1, 1)`; the recorded `want=(1, 0, 1, 1)` matches a one-killed
vector. The scenario's want and its input vector are mutually inconsistent, so the counter's own
`--selftest` cannot pass on the landed bytes. Scope notes: C1's counting commands run the counter
without `--selftest` (that run prints `survivors=0`, exit 0 — §7), and the C1 kill rule's
selftest clause names the *suite* (`r-defect-closure.sh --selftest`), so this failure is outside
the frozen claim's counted surface; a grep of `.ufo/waves/round-34/` and the lane found no prior
record of `one-invalid` failing. Reported, not fixed — outside this seat's assignment.
(Re-checked post-fix in §8a: fixed on `e33a300f…`, `--selftest` now `cases=3 failures=0` exit 0.)

### 8a. Addendum — re-check on current bytes (finding → fixed)

RevKillRule reported the §8 want/input inconsistency fixed on newer counter bytes and asked this
seat to re-run the check and record the byte move. Re-measured (cwd = lane root; scratch recreated
under the seat tree, then removed again — see §9):

```sh
S=/fast/scratch/hyaku/kasegi-r34/MutSelftestSummary && mkdir -p "$S/runs" && sha256sum corpus/instruments/kill-rule-check.py corpus/instruments/capture-binding-check.py && python3 corpus/instruments/kill-rule-check.py --selftest 2>"$S/runs/kr-selftest.err" | tee "$S/runs/kr-selftest.out"; echo "kr-selftest-exit=${PIPESTATUS[0]}"; python3 corpus/instruments/kill-rule-check.py --scratch "$S/runs/kr-scratch" 2>"$S/runs/kr-full.err" | tee "$S/runs/kr-full.out"; echo "kr-full-exit=${PIPESTATUS[0]}"
```

```text
e33a300fc7341f8d6e254fc12441de1ba0ec6252483aeaf6e8806622dba0fc15  corpus/instruments/kill-rule-check.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
selftest case=all-killed got=(3, 0, 0, 0) want=(3, 0, 0, 0) verdict=pass
selftest case=one-survivor got=(2, 1, 0, 1) want=(2, 1, 0, 1) verdict=pass
selftest case=one-invalid got=(2, 0, 1, 1) want=(2, 0, 1, 1) verdict=pass
selftest cases=3 failures=0
kr-selftest-exit=0
```

- Byte move: at this seat's §7/§8 runs the counter's own header printed
  `counter_sha256=77ff705c785f2b01f7d2c974fffb1090734dc7bfdd54ae53edbc17c20f690b52`;
  `sha256sum` now reads `e33a300fc7341f8d6e254fc12441de1ba0ec6252483aeaf6e8806622dba0fc15`. The
  `one-invalid` want is now `(2, 0, 1, 1)` — the arithmetically consistent tuple §8 derived — and
  `--selftest` prints `selftest cases=3 failures=0`, exit 0 (stderr 0 bytes).
- Full counter re-run on the same current bytes: `mutants=3 killed=3 survivors=0 invalid=0`,
  `gates=6 failed=0`, `survivors=0`, exit 0; `skip-selftest-summary` still killed with
  `reasons=summary-only;case-set-mismatch`. The instrument under test is still
  `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` — §1-§6 probe bytes
  unaffected.
- Status: §8 is a finding → fixed on current bytes, not an open defect. This seat made no edits to
  `kill-rule-check.py`; the fix belongs to the kill-rule seat.

### 9. Hashes, restoration, cleanup, tooling

- Landed instrument `corpus/instruments/capture-binding-check.py`:
  sha256 `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` before == after
  (40556 bytes / 892 lines per the counter header in §7). Never modified by this seat.
- Scratch mutants (mutated): mutA `7b04332799bd3188dcbda418e3affc71b77c8183c0883c3d042c0c8e3fc378af`,
  mutB `2cc2f65be2c70040460f5fa7af4d1d2fb7d29302069e038f20bd366da5c13ca0`.
- Restoration: landed bytes written back over both mutant copies;
  `mutA restored sha256 == landed: True`, `mutB restored sha256 == landed: True` (exact-byte
  restoration, verified by digest).
- Kill-rule counter digest (its own header): `77ff705c785f2b01f7d2c974fffb1090734dc7bfdd54ae53edbc17c20f690b52`.
- Cleanup: `rm -rf -- "$S"` then `test ! -e "$S"` → `scratch removed and verified absent:
  /fast/scratch/hyaku/kasegi-r34/MutSelftestSummary` (cleanup-exit=0). No seat tree left on disk.
- Tooling: nothing installed or upgraded (stdlib-only work; operator authorization unused).

### 10. Verdict

- Forgery A (`selftest cases=0 failures=0`, exit 0, no per-case lines): **REJECTED** by the landed
  bytes — 25 problems, observed exit 1.
- Forgery B (`selftest cases=19 failures=0`, exit 0, no per-case lines): **REJECTED** — 25
  problems incl. `summary-cases=19 want=23`, observed exit 1.
- Both F-5 mutants (scratch copies; emission point `:859-860`): **KILLED** — each emits exactly the
  forged summary with exit 0, and the landed `judge_selftest_report` rejects the emitted bytes.
- Marker case `summary-only-selftest-rejected` is exercised on the landed bytes at
  `exit=1 want=1 verdict=pass` (§1), and the committed kill-rule counter independently kills the
  same mutant shape (`reasons=summary-only;case-set-mismatch`, §7). The claimed invariant holds.
- Coverage note (measured, not a defect claim): the runner's own structural self-check
  (`:861-865`) judges the internal report list, not the emitted bytes — both mutants passed it and
  exited 0 while emitting summary-only stdout. Rejection of *emitted* bytes is enforced where
  reports are judged: the report-verifier limb (`REPORT_CASES`, `:806-810`) and the kill-rule
  counter's shape gate applied to captured stdout (§7). This is precisely the defense the frozen
  round-33 kill-rule clause lacked (F-5).
- Side finding §8 recorded for the L1: `kill-rule-check.py --selftest` fails on the landed bytes
  (`one-invalid` want/input inconsistency), outside C1's counted surface.
