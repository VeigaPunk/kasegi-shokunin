author: ExecKillRuleCheck
round: kasegi 34 — hyaku run 8, leaf executor (L2 wave 1)
lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin
lane base: 014ee2d7aa8c3c095ff57ae51097606a9906228c · claims freeze 29f606dbdd28aff6fd4573ab4b90788bbb90af13
date: 2026-10-26
claim touched: C1 depth:verifiability — the survivor-mutant counter `corpus/instruments/kill-rule-check.py`
role: implementation only. No commits, no gate runs (build/lint/unittest of the round), no writes outside
this lane. The target instrument was landed by ExecCaptureBindingHarden during this wave; I edited no
instrument other than the new counter.

# Round 34 — ExecKillRuleCheck

## Report

### 0. Final generation, and why the bytes moved

**Frozen counter bytes:** `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61`
(43138 B, 881 lines); every run header prints `counter_sha256=c279d952…`. No edit by me after the run
quoted in §3.

The tool was hardened four times during the wave because three seats attacked it while it was live. Those
measured generations are named here so a reviewer can tell a stale quote from a defect:

| generation | counter sha256 | trigger | state |
|---|---|---|---|
| draft | `77ff705c…` | initial write | `--selftest` arithmetic defect, fixed before gen 1 |
| gen 1 | `e33a300f…` (34914 B, 743 lines) | 3 probes, controls, `--row-file`, `--selftest` | measured by `MutKillRuleMutants`, `MutSelftestSummary` |
| gen 2 | `c51ac05a…` (36376 B, 771 lines) | `MutKillRuleMutants` survivor `unnamed-id-guard-removal` | measured by `RevKillRule` |
| gen 3 | `7a20e724…` (37730 B, 793 lines) | widened malformed fixture (both malformed paths) | declared frozen, then attacked |
| interim | `183fd9a0…`, `b8e4fb4c…`, `732e1e31…` | in-edit states while the pins/gates/probes landed | transient; **not** review targets |
| **final** | **`c279d952…`** (43138 B, 881 lines) | `MutKillRuleMutants` `url-token-normalization-removal`; `CritC1Kill` false-zero path | this receipt |

The moving target is a wave defect for which I am the cause: I declared gen 3 final and then hardened it
under attack. `RevKillRule`'s battery2 straddled a rewrite (its determinism check failed for that reason
only). The final bytes have not changed since the runs in §3–§8, and I have asked the reviewer to take
one clean pass at `c279d952`.

### 1. Deliverables and digests

| path | sha256 | size |
|---|---|---|
| `corpus/instruments/kill-rule-check.py` (new, committed) | `c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61` | 43138 B, 881 lines |
| `corpus/instruments/README.md` (§ Round-34 additions appended; nothing above moved) | `d021b317d2bad47d35d866617962906211df642730bc0f1c3849d4224ac19907` | 960 lines |
| `.ufo/waves/round-34/wave1/ExecKillRuleCheck.json` (written by `--json`) | `fd82557a9e5da55aeb2ead931b384d04a5b5829ccb7c92b44d702db1784bbea8` | 8071 B |
| target: `corpus/instruments/capture-binding-check.py` (not edited by me) | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` | 40556 B, 892 lines |
| control: `.ufo/waves/round-34/c1-controls/fake-killrule.py` (pre-frozen; not edited by me) | `7ca5d4fa97c6dadcb8f8b63a8f86f12a75d41335fdded8e46b1475a6cbb3b1af` | 305 B |

The target digest is measured at run time and printed in the header; it is not hardcoded. Every row's
`find` must occur exactly once, so different instrument bytes produce `status=invalid:find-count` and
exit 1 instead of a silent `survivors=0`.

### 2. Contract implemented

Three layers, all replayed against a **copy** of the instrument bytes in a scratch tree
(`tempfile.mkdtemp`, removed in `finally`; `TMPDIR`/`HYAKU_SCRATCH` redirected into it):

1. **`selftest-shape`** — accepts one `selftest case=<name> exit=N want=N verdict=pass` line per case, a
   `selftest cases=N failures=0` summary whose N equals the case-line count, the pristine case-name
   multiset, and (pristine side only) `N >= CASE_FLOOR=19`. Summary-only spans are `summary-only`; a
   forged `cases=0` summary fails the floor and `case-set-mismatch`.
2. **Eight external fixtures**, one per documented failure family, none reading the mutant's own
   selftest: `record-without-url` (exit 1, `detail=absent`, `unbound=1`), `per-file-orphan` (exit 1,
   `rule=orphan-capture`, `orphans=1 orphan=S009.txt`), `unnamed-record-id` (exit 1, `rule=no-row
   record=<unnamed>`), `stale-orphan-declaration` (exit 1, `rule=orphan-declared-missing`),
   `malformed-fetched-utc` (exit 1, `detail=malformed` for both an impossible UTC-shaped stamp and an
   unparsable string), `punctuated-url-cell` (exit 0, `url_bound=1`: a registry cell URL ending in `.`
   still binds), `malformed-orphan-declaration` (exit 2, `reason=manifest-shape`), `nested-legacy-round`
   (exit 0: `round-31/inner` is legacy, so an archival record passes).
3. **Row pins and gates** — `ROW_PINS` holds the literal `find` and `find\0replace` sha256 of each named
   row (a substituted named patch is `invalid:anchor-mismatch`); the `named-rows` gate requires the
   pinned name set to equal `MUTANTS` with each name present exactly once; `killed` with an empty
   `killed_by` is `invalid:inconsistent-kill`; `--row-file` rows may not reuse a named row's name.

Each row: exactly-once `find` → bytes changed → `py_compile` → probes. `killed` iff a probe the
pristine bytes pass is failed by the mutant. An unevaluable row is `invalid:<reason>`, counted
separately, never relabelled killed or survivor. `--selftest` checks only the verdict arithmetic.

### 3. Plain run at the landed bytes (the claim's counting command)

```
$ HYAKU_SCRATCH=/fast/scratch/hyaku/kasegi-r34/ExecKillRuleCheck \
  python3 corpus/instruments/kill-rule-check.py \
    --json .ufo/waves/round-34/wave1/ExecKillRuleCheck.json
KILL-RULE instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa bytes=40556 lines=892 floor=19 counter_sha256=c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61
probe selftest-shape pristine=pass exit=0
probe record-without-url pristine=pass exit=1
probe per-file-orphan pristine=pass exit=1
probe unnamed-record-id pristine=pass exit=1
probe stale-orphan-declaration pristine=pass exit=1
probe malformed-fetched-utc pristine=pass exit=1
probe punctuated-url-cell pristine=pass exit=0
probe malformed-orphan-declaration pristine=pass exit=2
probe nested-legacy-round pristine=pass exit=0
pristine selftest cases=23 case-lines=23 floor=19 floor_met=1
mutant-patch name=skip-selftest-summary patch_sha256=c457083e5d99f9f0 find_sha256=e6262244cffa1e1e find_count=1 status=ok
mutant-bytes name=skip-selftest-summary pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=b9d40dbee7521dbd
mutant-probe name=skip-selftest-summary probe=selftest-shape pristine=pass mutant=fail exit=0 reasons=summary-only;case-set-mismatch
mutant-probe name=skip-selftest-summary probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=skip-selftest-summary probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=skip-selftest-summary probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=skip-selftest-summary probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=skip-selftest-summary killed=1
mutant-patch name=accept-record-without-url patch_sha256=83cbd622ad2fd1e2 find_sha256=cbf461982c746e9d find_count=1 status=ok
mutant-bytes name=accept-record-without-url pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=5897a1f044bcbf3f
mutant-probe name=accept-record-without-url probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=1;case-verdict
mutant-probe name=accept-record-without-url probe=record-without-url pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='detail=absent';missing='unbound=1'
mutant-probe name=accept-record-without-url probe=per-file-orphan pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=accept-record-without-url probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=accept-record-without-url probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=accept-record-without-url probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=accept-record-without-url killed=1
mutant-patch name=per-file-binding-removal patch_sha256=f872ef12408d9162 find_sha256=f1a44079b9477ef2 find_count=1 status=ok
mutant-bytes name=per-file-binding-removal pristine_sha256=3d9e5e0ddbaaccf9 mutant_sha256=616ce9dd0637a23b
mutant-probe name=per-file-binding-removal probe=selftest-shape pristine=pass mutant=fail exit=1 reasons=exit=1;failures=2;case-verdict
mutant-probe name=per-file-binding-removal probe=record-without-url pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=per-file-orphan pristine=pass mutant=fail exit=0 reasons=exit=0 want=1;missing='rule=orphan-capture';missing='orphans=1 orphan=S009.txt'
mutant-probe name=per-file-binding-removal probe=unnamed-record-id pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=stale-orphan-declaration pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=malformed-fetched-utc pristine=pass mutant=pass exit=1
mutant-probe name=per-file-binding-removal probe=punctuated-url-cell pristine=pass mutant=pass exit=0
mutant-probe name=per-file-binding-removal probe=malformed-orphan-declaration pristine=pass mutant=pass exit=2
mutant-probe name=per-file-binding-removal probe=nested-legacy-round pristine=pass mutant=pass exit=0
mutant=per-file-binding-removal killed=1
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
control=CTL-nocompile verdict=invalid:nocompile expect=invalid:nocompile ok=1
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 fake=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/c1-controls/fake-killrule.py fake_exit=0 fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0 fake_survivors=0 real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
controls=4 rejected=4
GATE ok name=named-rows
GATE ok name=pristine-selftest
GATE ok name=pristine-fixtures
GATE ok name=pristine-determinism
GATE ok name=rows-valid
GATE ok name=controls
GATE ok name=survivors-zero
mutants=3 killed=3 survivors=0 invalid=0
gates=7 failed=0
survivors=0
exit=0
```

Determinism: a second invocation without `--json` printed byte-identical stdout,
`sha256 85d80cb2c8c6cbf237bba0941617b7ad9904db6fbaabac0d5e7066b9f3bb9027` (same as the first run). Every
probe is itself run twice inside the tool (`run_twice`), and `GATE ok name=pristine-determinism` records
that both runs agreed on `(exit, stdout)`.

### 4. Mutant diffs (exactly-once patches over the pristine bytes)

Produced by importing the tool's own `MUTANTS` rows and applying `prepare_patch()` to a scratch copy
(the pristine copy carries the target digest `3d9e5e0d…`):

```
== mutant skip-selftest-summary ==
status=ok detail=None find_count=1
mutant_sha256=b9d40dbee7521dbd9e492655df734e062fde69f43b3333df1b1227c7a3becc97
--- a/capture-binding-check.py
+++ b/capture-binding-check.py
@@ -821,2 +821,4 @@
 def selftest(scratch_arg=None, out=sys.stdout):
+    print("selftest cases=0 failures=0", file=out)
+    return 0
     base = scratch_base(scratch_arg)

== mutant accept-record-without-url ==
status=ok detail=None find_count=1
mutant_sha256=5897a1f044bcbf3fe90e21f8222a5336bd5b604dfe897fed16cbea6721b688b7
--- a/capture-binding-check.py
+++ b/capture-binding-check.py
@@ -298,3 +298,3 @@
     if not (isinstance(url, str) and url.strip()):
-        return False, ["rule=url-mismatch record=%s detail=absent" % record_id]
+        return True, []
     if len(tokens) > 1:

== mutant per-file-binding-removal ==
status=ok detail=None find_count=1
mutant_sha256=616ce9dd0637a23b8738ee1ae97e0668319507a828dfbb212536c79b6a8769cd
--- a/capture-binding-check.py
+++ b/capture-binding-check.py
@@ -439,5 +439,4 @@
                 continue
-            orphans.append((name, capture))
             if capture not in declared:
-                failures.append("FAIL rule=orphan-capture file=%s dir=%s" % (capture, name))
+                pass  # mutant: per-file orphan detection dropped
         for stale in sorted(set(declared) - set(captures)):
```

`find_sha256` / `patch_sha256` per row (also pinned as constants in `ROW_PINS`):
`e6262244cffa1e1e…` / `c457083e5d99f9f0…`; `cbf461982c746e9d…` / `83cbd622ad2fd1e2…`;
`f1a44079b9477ef2…` / `f872ef12408d9162…`. `MutKillRuleMutants` reproduced all three mutant byte
digests (`b9d40dbe…`, `5897a1f0…`, `616ce9dd…`) with an independent patch script; they are unchanged in
the final generation because neither the instrument nor the patches moved.

### 5. Raw mutant behaviour (the observations the frozen `before` text names)

```
== pristine on record-without-url fixture ==
exit=1
MANIFEST round-30 records=2 url_bound=1 fetched=1 archival=1
AUDIT records=2 with_url=1 with_fetched_utc=1 with_archival=1 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
FAIL rule=url-mismatch record=S002 detail=absent dir=round-30
records=2 bound=1 unbound=1

== accept-record-without-url on record-without-url fixture ==
exit=0
AUDIT records=2 with_url=1 with_fetched_utc=1 with_archival=1 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=2 bound=2 unbound=0

== pristine on per-file-orphan fixture ==
exit=1
MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=1 orphan=S009.txt
FAIL rule=orphan-capture file=S009.txt dir=round-30
records=1 bound=1 unbound=0

== per-file-binding-removal on per-file-orphan fixture ==
exit=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=1 bound=1 unbound=0

== skip-selftest-summary: --selftest ==
exit=0 stdout='selftest cases=0 failures=0\n' stderr=''
```

Mutant 2 reproduces the frozen before-line `records=2 bound=2 unbound=0` exit 0 exactly; the landed
counter kills it on two independent probes (its own selftest reports `failures=1`, and the external
url-less fixture no longer prints `detail=absent`/`unbound=1`). Mutant 3 drops `orphans=0` and exits 0
where the pristine bytes print `orphans=1 orphan=S009.txt` and exit 1. Mutant 1 forges the round-33 F-5
summary; the counter rejects it as `summary-only;case-set-mismatch`.

### 6. Controls (quoted)

```
control=CTL-noop verdict=invalid:noop expect=invalid:noop ok=1
control=CTL-nocompile verdict=invalid:nocompile expect=invalid:nocompile ok=1
control=CTL-equivalent verdict=survivor expect=survivor ok=1 witness_survivors=1 witness_exit=1
control=CTL-fake-killrule verdict=opaque expect=opaque ok=1 fake=…/c1-controls/fake-killrule.py fake_exit=0 fake_mutant_lines=0 fake_patch_digests=0 fake_mutants_line=0 fake_survivors=0 real_mutant_lines=3 witness_survivors=1 differs=1 stable=1
controls=4 rejected=4
```

- **CTL-noop** — a `find`/`replace` pair whose strings are identical (`SCHEMA_VERSION = 1`): bytes
  unchanged → `invalid:noop`; `killed` is never awarded to it.
- **CTL-nocompile** — drops the colon from `def parse_round(dirname):` (exactly once): `py_compile` fails
  before any probe → `invalid:nocompile`. A mutant that cannot compile cannot be killed.
- **CTL-equivalent** — rewrites only the `# --- selftest ---…` banner comment: compiles, changes bytes,
  no probe can see it → `survivor`, with `witness_survivors=1 witness_exit=1` from the shared
  `summarise()`.
- **CTL-fake-killrule** — the frozen do-nothing runner:

```
$ cat .ufo/waves/round-34/c1-controls/fake-killrule.py
#!/usr/bin/env python3
"""Do-nothing control for C1's survivor-mutant counter.

Prints the claimed after-state (survivors=0) without replaying any mutant.
The real kill-rule-check.py must replay each mutant against the landed
instrument bytes and print the actual survivor count.
"""
print("survivors=0")

$ python3 .ufo/waves/round-34/c1-controls/fake-killrule.py; echo "exit=$?"
survivors=0
exit=0
```

  Its whole span is one line: 0 `mutant=` lines, 0 patch digests, no `mutants=` line → `verdict=opaque`,
  and it prints `survivors=0` on the survivor witness where the real evaluator prints `survivors=1`/exit
  1 (`differs=1`). An `evidential` fake fails the control (`ok=0`). The path is discovered as the newest
  `.ufo/waves/round-*/c1-controls/fake-killrule.py` under the lane root (`--fake` overrides); a moved path
  makes the control `absent` (`ok=0`, a failed gate), never silently skipped.

### 7. Attack-seat survivors: reported, then pinned (never relabelled)

Five behaviour-bearing survivors were reported at earlier generations, each fed through `--row-file`
(no tool edit). All five are killed at the final bytes, each by the probe that pins its limb and by that
probe alone (`selftest-shape` prints `mutant=pass` for all five):

```
mutant=url-token-normalization-removal killed=1
  probe: punctuated-url-cell  exit=1 want=0; missing='MANIFEST round-30 records=1 url_bound=1 fetched=1 archival=0'
mutant=unnamed-id-guard-removal killed=1
  probe: unnamed-record-id    missing='rule=no-row record=<unnamed>'
mutant=stale-orphan-listing-removal killed=1
  probe: stale-orphan-declaration  exit=0 want=1; missing='rule=orphan-declared-missing file=S077.txt'
mutant=malformed-stamp-fallthrough-acceptance killed=1
  probe: malformed-fetched-utc  missing='record=S002 dir=round-32 detail=malformed'
mutant=malformed-stamp-impossible-acceptance killed=1
  probe: malformed-fetched-utc  missing='record=S001 dir=round-32 detail=malformed'
mutant=attack-comment-only killed=0
mutants=9 killed=8 survivors=1 invalid=0 ; exit=1
```

The single survivor is the deliberately comment-only red row; its `survivors=1`/exit 1 is the red
aggregate (§8). `MutKillRuleMutants` also confirmed independently that the tasked example
(rule-B url-limb removal with different wording, mutant `64c4d586…`) is killed by
`selftest-shape` + `record-without-url` — the probes are behavioural, not wording-dependent.

### 8. Red aggregate through the public CLI

```
$ python3 corpus/instruments/kill-rule-check.py --row-file red-only.json
mutant=attack-comment-only killed=0
GATE fail name=survivors-zero
mutants=4 killed=3 survivors=1 invalid=0
survivors=1
exit=1
```

`--row-file PATH` (`{"rows":[…]}` or a bare list, repeatable) is the sanctioned path for attack seats;
extra rows are measured by the same prepare/evaluate path and counted in `survivors`. The three named
rows always run, and a row file may not reuse their names.

### 9. Critic's false-zero path: closed, measured three ways

`CritC1Kill` reported that a two-edit self-mutation — substitute a named row's patch with a
probe-invisible defect **and** force `result["verdict"]="killed"` — could print `survivors=0` with every
probe passing. Three copies of the final counter were built in scratch and run:

```
== self-mutant A (row 2's replace rewritten to a probe-invisible variant + forced verdict) ==
mutant=accept-record-without-url killed=0
mutant-invalid name=accept-record-without-url status=invalid:anchor-mismatch detail=find-or-patch-digest
GATE fail name=rows-valid
GATE fail name=controls
mutants=3 killed=2 survivors=0 invalid=1 ; exit=1

== self-mutant B (A + pin check replaced by `pinned = None` + row substituted by a comment-only patch) ==
mutant=per-file-binding-removal killed=0
mutant-invalid name=per-file-binding-removal status=invalid:inconsistent-kill detail=
GATE fail name=rows-valid
GATE fail name=controls
mutants=3 killed=2 survivors=0 invalid=1 ; exit=1

== self-mutant C (a named row renamed; pin check intact) ==
mutant=per-file-binding-removal-x killed=1
GATE fail name=named-rows
mutants=3 killed=3 survivors=0 invalid=0 ; exit=1
```

A: the pin refuses the substituted patch. B: with the pin removed, the consistency guard refuses a
`killed` verdict with no killing probe. C: the name-set gate refuses a redefined matrix. All three exit 1.
**Precision (peer-measured correction):** my A/B forced the verdict unconditionally, which also breaks
`CTL-equivalent` (it becomes `killed`, so the survivor witness disappears) and fires
`GATE fail name=controls`. With the force scoped to the named row only, `controls` stays ok and
`GATE fail name=rows-valid` is the gate that catches A — the two gates are independent, and the critic
reproduced both readings. What remains indefensible in-band is a *consistent* rewrite: a substituted
named patch plus re-pinned `ROW_PINS` plus an exemption from the guard reports green (the critic's D2,
counter digest `d9bc0c0b…`). The only defence is binding `counter_sha256` to a constant compared outside
the tool — see §13.10.

### 9b. Known survivor, measured first-hand: `parse_round` non-round-directory exemption

The critic named a limb no probe pins, and I reproduced it at the frozen bytes through `--row-file`
(no tool edit):

```
mutant=parse-round-nonround-dir-archival-exemption killed=0
mutant-probe … all nine probes … mutant=pass
GATE fail name=survivors-zero
mutants=4 killed=3 survivors=1 invalid=0
survivors=1 ; exit=1
```

The patch is `return int(m.group(1)) if m else None` → `… if m else 0`: a snapshot directory whose name
does not parse as `round-<N>` becomes legacy, so the closed archival exemption re-opens for it. No
fixture uses a non-round directory name, so the defect is invisible to all nine probes.

A ninth probe kills it, tested without touching the counter. Fixture `non-round-dir-archival`
(`corpus/source-snapshots/snapshots-x/` holding one record with `"archival": true`, no `fetched_utc`;
registry row `S001`; assertion `exit 1` + `records=1 bound=0 unbound=1`). Discriminates:

```
== pristine on non-round-dir fixture ==
exit=1
FAIL rule=provenance-missing record=S001 dir=snapshots-x
records=1 bound=0 unbound=1

== parse_round-mutant on non-round-dir fixture ==
exit=0
records=1 bound=1 unbound=0
```

This probe is **not landed**: the tool is frozen at `c279d952…` after a premature freeze and two
reviewers' re-runs, and I committed to report rather than edit under review. The fix is one fixture
entry plus one `PROBES` row using the design above; it is left to the L1 (next round or an amendment).

### 10. `--selftest` (arithmetic) and the defect it caught

```
$ python3 corpus/instruments/kill-rule-check.py --selftest
selftest case=all-killed got=(3, 0, 0, 0) want=(3, 0, 0, 0) verdict=pass
selftest case=one-survivor got=(2, 1, 0, 1) want=(2, 1, 0, 1) verdict=pass
selftest case=one-invalid got=(2, 0, 1, 1) want=(2, 0, 1, 1) verdict=pass
selftest cases=3 failures=0
exit=0
```

**Disclosed defect, fixed before gen 1.** At the draft (`77ff705c…`) the `one-invalid` scenario's *want*
tuple was `(1, 0, 1, 1)` for a vector containing two `killed` strings; `summarise()` was correct and the
selftest failed `got=(2,0,1,1) want=(1,0,1,1)`, `selftest cases=3 failures=1`, exit 1.
`MutSelftestSummary` observed that state and its receipt records the byte move `77ff705c → e33a300f`
with both commands and outputs. The expectation is `(2,0,1,1)` in the final bytes.

### 11. Gates, determinism, README append

All seven gates `ok`: `named-rows` (pinned name set == MUTANTS, each once), `pristine-selftest` (shape
accepted, `cases=23 >= floor=19`), `pristine-fixtures` (all eight fixtures hit their contract lines),
`pristine-determinism` (every probe stable across two runs), `rows-valid` (0 invalid), `controls` (4/4
rejected), `survivors-zero` (0). Exit 0 iff all seven hold and `survivors=0`.

The README section `## Round-34 additions — kill-rule-check.py (C1 survivor-mutant counter)` is appended
at file end (nothing above it moved): contract, eight fixtures, pins/gates, measured figures, the attack
replay and the known limits.

### 12. Write scope, scratch, and what I did not do

- Wrote exactly: `corpus/instruments/kill-rule-check.py`; the appended README section;
  `.ufo/waves/round-34/wave1/ExecKillRuleCheck.json`; this receipt.
- Read-only elsewhere: the target instrument, `claims.json`, `QUALITY.md`/`SOURCES.md`/lessons,
  `SCORECARD.md`, `c1-controls/*`. No VCS mutation (`git add`/`commit`/`push`, `jj` writes) — the L1
  commits.
- All work trees/fixtures lived under `/fast/scratch/hyaku/kasegi-r34/ExecKillRuleCheck/`; every run
  redirected `HYAKU_SCRATCH`/`TMPDIR` there. Deleted and verified absent after the final run:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r34/ExecKillRuleCheck; echo "rm_exit=$?"
rm_exit=0
$ ls -d /fast/scratch/hyaku/kasegi-r34/ExecKillRuleCheck; echo "ls_exit=$?"
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/ExecKillRuleCheck': No such file or directory
ls_exit=2
```

- Did not run the round gate (`r-defect-closure.sh`, harness, census, `source-recheck`), did not touch
  `shokuknow`, `bounties`, sibling lanes or the fleet root. No LSP is available for this lane's Python
  (recorded as actual unavailability); symbol work was done by reading the landed instrument bytes.

### 13. Risks and open items for the L1

1. **The bytes moved under review.** §0 lists every generation and its triggers. The final digest is
   `c279d952…`; peer quotes at `e33a300f…` (gen 1), `c51ac05a…` (gen 2), `7a20e724…` (gen 3) and the
   interim `183fd9a0…`/`b8e4fb4c…`/`732e1e31…` are generation-valid, not defects in their receipts. I
   have asked `RevKillRule` for one clean pass at `c279d952`.
2. **Patch anchors are byte-bound** to the instrument's `selftest()` entry (821-822), `bind_record()`'s
   url-absent limb (297-299) and the per-file orphan block (439-441); a later instrument edit yields
   `invalid:find-count` and exit 1 (loud). `ROW_PINS` additionally refuses a substituted named patch.
   Re-running after integration is the check.
3. **The probe set is a bounded oracle.** It pins the limbs attack seats reported before the final
   freeze, plus the named mutants' limbs and one documented family each; a mutant that leaves every
   asserted line intact survives by construction (the comment-only row is the deliberate instance). One
   reported limb is **not** pinned and is disclosed instead: the `parse_round` non-round-directory
   archival exemption (§9b), reported after the freeze, with a tested ninth-probe design ready to land.
4. **`killed` semantics** — "a pristine-passing probe is failed by the mutant", not "the named limb is
   the sole cause". Mutants 2 and 3 are also killed by the instrument's own selftest (`failures=1` /
   `failures=2`); the fixtures are the independent oracle the round-33 rule lacked.
5. **`CASE_FLOOR=19` gates the pristine side only** (C1's frozen conjunct). Below-floor instrument bytes
   print `pristine selftest-refused reasons=cases=N<floor=19` and exit 1. Measured now: 23, met.
6. **Evidence-shape risk in A/B self-mutants** — a forced `killed` verdict also breaks the
   `CTL-equivalent` witness, which is why `GATE fail name=controls` appears there; that is intended
   defence in depth, not a redundant gate. A named-row-scoped force leaves `controls` ok and is caught by
   `rows-valid` alone (peer-measured, §9).
7. **Claim wording check.** `python3 corpus/instruments/kill-rule-check.py` prints `survivors=0` and
   exits 0 at the frozen bytes (scratch root defaults to `$HYAKU_SCRATCH`, then `$TMPDIR`, then
   `/fast/scratch/hyaku`; nothing is written outside it — verified by a bare run with both unset, which
   left no `/tmp/kill-rule-*` behind).
8. **Observed elsewhere, not my claim:** ExecCaptureBindingHarden reports the lane-level
   `capture-binding-check.py` run exits 1 on `FAIL rule=no-row record=S051 dir=round-34` until the C2
   scribe appends `S051`. The counter's `selftest-shape` probe runs the instrument's `--selftest`
   (fixture-built, registry-independent), so this counter is unaffected — but the C1 baseline command
   `python3 corpus/instruments/capture-binding-check.py -> records=… bound=…` reads differently before
   and after the registry append.
9. **Known survivor, disclosed not pinned (L1 decision).** `parse_round`'s non-round-directory branch is
   unpinned (§9b, measured here: `mutant=parse-round-nonround-dir-archival-exemption killed=0`,
   `survivors=1`, exit 1). Closing it is one fixture (`snapshots-x` + an `"archival": true` record) and
   one `PROBES` row asserting exit 1 + `unbound=1`; the design is discrimination-tested in §9b. Landing
   it moves the counter digest, so it is better done as an amendment than under a reviewer's run.
10. **The counter digest is pinned only outside the tool.** A *consistent* self-rewrite (substituted
    named patch + re-pinned `ROW_PINS` + guard exemption) reports green — the critic's D2 at counter
    digest `d9bc0c0b…`. Nothing in-tree compares `counter_sha256`: `claims.json` names only
    `survivors=K`, and `r-defect-closure.sh` never reads the counter. The recommended binding is an
    R-check line of the form
    `test "$(sha256sum corpus/instruments/kill-rule-check.py | awk '{print $1}')" = c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61`
    in the closure suite, with the constant frozen in the claims or the suite — no counter change
    needed. Until that lands, the binding lives in this receipt, the README section and §0/§1.
