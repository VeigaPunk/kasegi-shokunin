PASS assigned pristine C1 checks; COVERAGE FINDING: two valid additional mutants survive both frozen detectors.

# MutationPython — round 61 wave 1

Axes: depth:verifiability and coverage. This report does not amend the frozen C1 predicate or claim a sandbox. C2 was not assigned to this seat and was not checked.

Implementation pinned in an isolated shared clone at `13c8060b343e002339ffd72da37ff74514f82765`; lane HEAD matched that pin. Frozen claims read before source inspection. Instrument digests matched claims before and after probes. No production edits, commits, installs, background agents, or other runtimes.

## Findings

- Committed battery: exit 0, killed 3/3, survivors 0, controls pass. m4 removes a test, so its kill is the 24-case pin, not a behavioral-path kill; m6 disables the non-Python allowlist; m7 disables final Python containment. These are not comprehensive per-limb coverage.
- Additional four non-equivalent mutants: **2/4 killed by selftest**, **1/4 killed by named probe outcomes**. Prefix-off and boundary-separator-off survive both. Distinguishing direct-gate witnesses establish they are not equivalent: absolute-inside admission flips False→True for prefix-off; a sibling-directory path flips False→True for boundary-separator-off. These are coverage findings beyond the frozen named predicate, not failures of pristine C1.
- Root-target-unbound: selftest kills it (`python-inside-admitted exit=2 want=0`); named runner survives because it sets cwd equal to root. Selftest leaves cwd distinct from its temporary --root.
- Symlink-resolution-off replaces target realpath with abspath, retaining lexical normalization. Selftest kills it (`python-symlink-refused exit=0 want=2`). Named P3 changes to exit=1 markers=1 derive-empty; this is a behavioral kill even though the outer runner exits 0.
- Runner exit 0 is only harness completion, NOT an assertion of the C1 outcomes. Every runner phase here returned 0, including the demonstrably killed symlink mutant. Grade the printed probe tuples, not runner status alone.
- Equivalent controls retained: trailing whitespace, and deleting the explicit target==base guard. The latter is redundant because `base.startswith(base + os.sep)` is false. Neither changes selftest, named outputs, or witness results.

## Source evidence (absolute production paths)

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:181`: literal prefix limb; `:183-184`: root-bound realpath; `:185-187`: exact-dir and separator boundary.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py:305-306`: selftest subprocess has --root but no cwd override; `:333-336`: four Python cases (absolute case is outside, not absolute-inside).
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py:23-29`: committed mutation definitions; `:88-97`: selftest-exit grading.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-61/controls/c1-probe-run-r61.sh:34-38`: per-probe exits captured/printed rather than asserted; `:43-54`: exact named probes and controls.

## Setup and execution

All actual probe commands below ran with cwd `/fast/scratch/hyaku/kasegi-r61/MutationPython` and TMPDIR explicitly set to its `tmp` child. Each subprocess had a 600-second bound; tool execution completed normally. Per-mutant full phase order was pristine → mutated → restored at the same instrument pathname, with identical detector commands and exact-byte restoration in a finally block. Each replacement site occurred exactly once. An initial independent baseline/mutant pass preceded these full three-phase receipts and gave the same classifications.

Setup commands (exit 0):
```sh
mkdir -p /fast/scratch/hyaku/kasegi-r61/MutationPython/tmp
env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin clone --shared --no-checkout /home/vgpnk/Projects/shokunin/kasegi-shokunin /fast/scratch/hyaku/kasegi-r61/MutationPython/clone
env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp git -C /fast/scratch/hyaku/kasegi-r61/MutationPython/clone rev-parse --show-toplevel
# output: /fast/scratch/hyaku/kasegi-r61/MutationPython/clone
env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp git -C /fast/scratch/hyaku/kasegi-r61/MutationPython/clone checkout --detach 13c8060b343e002339ffd72da37ff74514f82765
# output: HEAD is now at 13c8060 round-61: confine python probe paths and admit sourced F42 SQLite account
```

Pristine SHA256: `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`. Every pristine and restored phase below has this full hash. The original battery file SHA256 before/after is `f94393d981eeb93a05f6c57782b787faabfc56bfa5b4775f1c319f405fdd353c`.

## Committed battery receipt

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/corpus/instruments/figure-audit-mutbat.py
PRISTINE selftest_exit=0 last='selftest cases=24 failures=0'
CONTROL c-equivalent-trailing-space selftest_exit=0 must_not_be_killed=held last='selftest cases=24 failures=0'
MUT m4-drop-stale-literal-case sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=23 failures=1'
MUT m6-readonly-gate-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=24 failures=4'
MUT m7-python-confinement-off sites=1 py_compile=0 selftest_exit=1 killed=1 last='selftest cases=24 failures=2'
mutbat killed=3/3 survivors=0 controls=pass
exit=0
```

## Bounded distinguishing detector source

This only calls the inspected gate on three fixed arguments; it does not execute script payloads. The sibling argument starts with the required literal prefix but resolves into instruments-evil, not instruments. This additional witness does not replace or expand C1's frozen named predicate.

`/fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py`:
```python
import os, runpy, sys
from pathlib import Path
r=Path(sys.argv[2]); (r/'corpus/instruments').mkdir(parents=True,exist_ok=True)
f=runpy.run_path(sys.argv[1])['python_head_ok']
print('absolute-inside-admitted='+str(f(str(r),'python3 '+str(r/'corpus/instruments/ok.py'))))
print('sibling-prefix-admitted='+str(f(str(r),'python3 corpus/instruments/../instruments-evil/out.py')))
print('same-directory-admitted='+str(f(str(r),'python3 corpus/instruments/')))
```

## Exact replacements and three-phase receipts

Selftest receipts retain summary and every failure line; named runner receipts retain all probe outputs. Expected pristine/restored: selftest 24/0 exit 0; P1–P4 exit 2 markers 0 reason derive-not-read-only; P5/P6 and quoted control exit 0 derived 35; count control exit 0 derived 1; all markers zero.

### prefix-off

Exact-once old/new replacement (JSON escaped):
```json
{
  "old": "if len(parts) < 2 or not parts[1].replace(\"\\\\\", \"/\").startswith(\"corpus/instruments/\"):",
  "new": "if len(parts) < 2:"
}
```
Mutated SHA256: `336cabbc73af4053ab80279cab601fd36b327f7c9e5e2e6881a1314cf2e5d8aa`.

#### pristine

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-prefix-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:38Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-prefix-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### mutated

SHA256 `336cabbc73af4053ab80279cab601fd36b327f7c9e5e2e6881a1314cf2e5d8aa`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-prefix-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py sha256=336cabbc73af4053
run-utc=2026-11-04T14:27:38Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-prefix-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=True
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### restored

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-prefix-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:39Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-prefix-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/prefix-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

### boundary-separator-off

Exact-once old/new replacement (JSON escaped):
```json
{
  "old": "return target.startswith(base + os.sep)",
  "new": "return target.startswith(base)"
}
```
Mutated SHA256: `e83dd9d5bc080a82a81b4a93ce3d1785f55bf1090a23822432b325c870662af9`.

#### pristine

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-boundary-separator-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:40Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-boundary-separator-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### mutated

SHA256 `e83dd9d5bc080a82a81b4a93ce3d1785f55bf1090a23822432b325c870662af9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-boundary-separator-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py sha256=e83dd9d5bc080a82
run-utc=2026-11-04T14:27:41Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-boundary-separator-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=True
same-directory-admitted=False
exit=0
```

#### restored

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-boundary-separator-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:42Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-boundary-separator-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/boundary-separator-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

### root-target-unbound

Exact-once old/new replacement (JSON escaped):
```json
{
  "old": "target = os.path.realpath(os.path.join(root or \".\", parts[1]))",
  "new": "target = os.path.realpath(parts[1])"
}
```
Mutated SHA256: `28b29856aac47085f590436ca8af21f8011e20e28ea2f43e695ed4d5215ce734`.

#### pristine

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-root-target-unbound
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:43Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-root-target-unbound/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### mutated

SHA256 `28b29856aac47085f590436ca8af21f8011e20e28ea2f43e695ed4d5215ce734`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py --selftest
selftest case=python-inside-admitted exit=2 want=0 verdict=fail
selftest cases=24 failures=1
exit=1
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-root-target-unbound
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py sha256=28b29856aac47085
run-utc=2026-11-04T14:27:43Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-root-target-unbound/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### restored

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-root-target-unbound
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:44Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-root-target-unbound/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/root-target-unbound.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

### symlink-resolution-off

Exact-once old/new replacement (JSON escaped):
```json
{
  "old": "target = os.path.realpath(os.path.join(root or \".\", parts[1]))",
  "new": "target = os.path.abspath(os.path.join(root or \".\", parts[1]))"
}
```
Mutated SHA256: `800b3d99b0385144a43adc6f88e2a806317339e3012cb9f143d6f21360f98b78`.

#### pristine

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-symlink-resolution-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:45Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-symlink-resolution-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### mutated

SHA256 `800b3d99b0385144a43adc6f88e2a806317339e3012cb9f143d6f21360f98b78`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py --selftest
selftest case=python-symlink-refused exit=0 want=2 verdict=fail
selftest cases=24 failures=1
exit=1
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-symlink-resolution-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py sha256=800b3d99b0385144
run-utc=2026-11-04T14:27:46Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=1 markers=1 :: FIG P3-symlink-out recorded=35 derived=UNAVAILABLE reason=derive-empty stale
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-symlink-resolution-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### restored

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-symlink-resolution-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:47Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-symlink-resolution-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/symlink-resolution-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

### equivalent-same-dir-guard-off

Exact-once old/new replacement (JSON escaped):
```json
{
  "old": "    if target == base:\n        return False\n",
  "new": ""
}
```
Mutated SHA256: `94061e9c195fd377400b25ba478e29e90b8f2641bdd4196fbbf8ab74f94e59e7`.

#### pristine

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-same-dir-guard-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:47Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-same-dir-guard-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### mutated

SHA256 `94061e9c195fd377400b25ba478e29e90b8f2641bdd4196fbbf8ab74f94e59e7`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-same-dir-guard-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py sha256=94061e9c195fd377
run-utc=2026-11-04T14:27:48Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-same-dir-guard-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### restored

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-same-dir-guard-off
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:49Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-same-dir-guard-off/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-same-dir-guard-off.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

### equivalent-whitespace

Exact-once old/new replacement (JSON escaped):
```json
{
  "old": "return target.startswith(base + os.sep)",
  "new": "return target.startswith(base + os.sep)  "
}
```
Mutated SHA256: `f857cff6af7e83a3581f0392239e4ce7a15a46c761ef9c23638cfab21a3ee9da`.

#### pristine

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-whitespace
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:50Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-whitespace/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### mutated

SHA256 `f857cff6af7e83a3581f0392239e4ce7a15a46c761ef9c23638cfab21a3ee9da`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-whitespace
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py sha256=f857cff6af7e83a3
run-utc=2026-11-04T14:27:51Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-whitespace/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

#### restored

SHA256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py --selftest
selftest cases=24 failures=0
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp bash /fast/scratch/hyaku/kasegi-r61/MutationPython/clone/.ufo/waves/round-61/controls/c1-probe-run-r61.sh /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-whitespace
instrument=/fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py sha256=051083a2dd3b76f9
run-utc=2026-11-04T14:27:51Z
probe=P1-traversal-2up derive=python3 corpus/instruments/../../outside-P1-traversal-2up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P1-traversal-2up
probe=P2-traversal-3up derive=python3 corpus/instruments/../../../outside-P2-traversal-3up.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P2-traversal-3up
probe=P3-symlink-out derive=python3 corpus/instruments/link-P3-symlink-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P3-symlink-out
probe=P4-absolute-out derive=python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/probe-equivalent-whitespace/outside-P4-absolute-out.py exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only id=P4-absolute-out
probe=P5-inside-ok derive=python3 corpus/instruments/tiny-ok.py exit=0 markers=0 :: FIG P5-inside-ok recorded=35 derived=35 ok
probe=P6-inside-normalized derive=python3 corpus/instruments/../instruments/tiny-ok.py exit=0 markers=0 :: FIG P6-inside-normalized recorded=35 derived=35 ok
probe=CTRL-quoted-semicolon derive=cat g.txt | grep -e '35' -e ';' exit=0 markers=0 :: FIG CTRL-quoted-semicolon recorded=35 derived=35 ok
probe=CTRL-plain-count derive=cat g.txt | wc -l exit=0 markers=0 :: FIG CTRL-plain-count recorded=1 derived=1 ok
exit=0
```

```text
$ env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp python3 /fast/scratch/hyaku/kasegi-r61/MutationPython/witness.py /fast/scratch/hyaku/kasegi-r61/MutationPython/equivalent-whitespace.py /fast/scratch/hyaku/kasegi-r61/MutationPython/witness-root
absolute-inside-admitted=False
sibling-prefix-admitted=False
same-directory-admitted=False
exit=0
```

## Restoration and cleanup

All six scratch mutant paths were restored byte-for-byte to the pristine SHA256 before deletion. The same selftest, named runner, and witness were rerun after restoration at each identical path; all restored outputs matched pristine expectations. No baseline failed, so none of the classifications is inconclusive.

Final production hash command and cleanup (combined exit 0):
```sh
env TMPDIR=/fast/scratch/hyaku/kasegi-r61/MutationPython/tmp sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py
rm -rf -- /fast/scratch/hyaku/kasegi-r61/MutationPython
test ! -e /fast/scratch/hyaku/kasegi-r61/MutationPython
```
Output:
```text
051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
f94393d981eeb93a05f6c57782b787faabfc56bfa5b4775f1c319f405fdd353c  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit-mutbat.py
```

No tool installs/updates. One setup attempt failed before execution because its requested scratch cwd did not yet exist; rerun from the fleet cwd created only the authorized scratch and succeeded. This had no effect on probes.

## Handoff self-evaluation

Accuracy 4/5: observed outcomes and full hashes retained; witness only proves gate distinction, not execution of sibling/absolute-inside payloads. Completeness 4/5: assigned battery, four limbs, two equivalent controls, three-phase restoration and cleanup covered; no broader sandbox tests were attempted. Clarity 4/5: verdict separates frozen success from coverage findings; repeated receipts are lengthy. Actionability 4/5: exact commands/replacements and decisive outputs retained; scratch must be recreated to replay. Conciseness 4/5: detailed phase evidence deliberately retained rather than summarized away. Overall 4.0. Highest-impact improvements are optional future detector additions for sibling-prefix and absolute-inside cases, with no change to the frozen claim. Self-check: assessment is limited to this seat's evidence, not fleet acceptance.
