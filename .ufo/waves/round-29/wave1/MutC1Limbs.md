# MutC1Limbs — mutation probe of the anchorcheck.py selftest (C1 limbs)

Round 29, wave 1, seat MutC1Limbs. 2026-10-25. Leaf role: no delegation, no
background jobs. All work on /tmp copies; the live instrument was never
opened for write by this seat.

## Subject and snapshot discipline

- Subject: `corpus/instruments/anchorcheck.py` (round-29 fixed selftest, 561
  lines, `LIMBS` registry of 9 named limbs, 12 cases = 9 failing + 3 controls).
- The live file was being edited by a sibling while I read it (531 -> 561
  lines between two reads). I therefore froze one snapshot at t0 and probed
  only that copy; at t0 the snapshot digest equaled the live digest:
  - pristine sha256: `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97`
- Lab: `/tmp/mutc1limbs-r29/` (disposable scratch; retained for audit).
- Write scope honored: zero writes outside `/tmp/mutc1limbs-r29/` and this
  report file. Live instrument digest at probe end (read-only check):
  `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` —
  unchanged by this seat.
- Tooling receipt: no tools installed or upgraded (none needed; pacman paused
  per orchestrator 2026-10-20).

## Detector (frozen before runs)

The claim detector is the frozen C1 counter set (claims.json) restricted to
the selftest surface, run as `python3 <copy> --selftest`:

- D1 exit code of the selftest;
- D2 parse `selftest cases=N failures=M`;
- D3 parse `limbs=L covered=C`;
- red iff exit != 0 OR failures > 0 OR covered < 9 (tasking red condition);
- frozen kill rule additionally requires cases == 12 and limbs == 9.

Baseline (pristine stage): `exit=0`, `selftest cases=12 failures=0`,
`limbs=9 covered=9`. Baseline green, so all mutant verdicts below are
conclusive (a baseline failure would have been inconclusive).

## Stage records

### Pristine

- sha256 `68e1bdc6…` (full digest above); output:
  `selftest cases=12 failures=0` / `limbs=9 covered=9`; exit 0.

### M1 — drop the mirror-outside-base fixture case

- Diff (unique-anchor removal of the whole `add('outside-base-mirror', …)`
  block, lines 262-265 of pristine):

```diff
--- pristine.py
+++ mutant-m1.py
@@ -260,8 +260,4 @@
         "`~/Projects/bounties/../selftest-escape.md:1`\n",
         want(**{'OUTSIDE-BASE': 1}), 1)
-    add('outside-base-mirror',
-        "Mirror cite escaping its root: "
-        "`~/Projects/the-bounty-hunter/../selftest-escape.md:1`\n",
-        want(**{'OUTSIDE-BASE': 1}), 1)
     add('outside-base-origin',
         "Origin cite escaping its root: "
```

- Mutant sha256: `a2c3188b69d39b048a80dda1bd1a6b78c1afe040944d1598d3a5716e874421a7`
- Output:

```
selftest FAIL limb coverage: missing executed cases outside-base-mirror
selftest cases=11 failures=1
limbs=9 covered=8
```

- Exit: 1.
- Verdict: **KILLED** — red on every axis (exit != 0, failures > 0,
  covered 8 < 9, cases 11 != 12). The LIMBS-registry vs executed-set
  assertion is load-bearing and fires with the exact missing limb named.

### M2 — delete the `limbs=` completeness print

- Diff (removal of `print(f"limbs={len(LIMBS)} covered={covered}")`, line 369):

```diff
--- pristine.py
+++ mutant-m2.py
@@ -367,5 +367,4 @@
         print(line)
     print(f"selftest cases={len(cases)} failures={n_fail}")
-    print(f"limbs={len(LIMBS)} covered={covered}")
     return 0 if not n_fail else 1
 
```

- Mutant sha256: `76a58d997f9dc038547cc31ec4042d05dc39b1ef86bb73c11c3ae0a0674b6188`
- Output: `selftest cases=12 failures=0` (no `limbs=` line at all).
- Exit: 0.
- Verdict: **KILLED via the frozen C1 counter only** — the counter command
  `--selftest | grep -E 'selftest cases=|limbs='` loses its `limbs=9
  covered=9` line, so the kill rule's `limbs == 9 and covered == 9` cannot be
  established and the claim fails. Recorded nuance (coverage finding F1): the
  tasking red condition (non-zero exit / failures > 0 / covered < 9) does NOT
  fire — the instrument's own exit status is blind to this deletion. The
  print is report-only; the kill comes exclusively from the claim counter's
  presence requirement.

### M3 — make `covered` always print 9 regardless of cases

- Diff:

```diff
--- pristine.py
+++ mutant-m3.py
@@ -367,5 +367,5 @@
         print(line)
     print(f"selftest cases={len(cases)} failures={n_fail}")
-    print(f"limbs={len(LIMBS)} covered={covered}")
+    print(f"limbs={len(LIMBS)} covered=9")
     return 0 if not n_fail else 1
 
```

- Mutant sha256: `a3306f9036467a87653e9050649452a4b18aecb62eb3bf44c097e75f690a6233`
- Output: `selftest cases=12 failures=0` / `limbs=9 covered=9`; exit 0.
- Output sha256 `40fa12b8461614d88269f548efd08bf49b8118edd781024bcb5ef8c946dcbe3f`
  is byte-identical to the pristine run's output sha256 (same digest) — on
  green bytes the hardcoded print is indistinguishable from the computed one.
- Verdict: **SURVIVED** (coverage finding F2). Neither the tasking red
  condition nor the frozen counter can distinguish "covered=9 computed" from
  "covered=9 hardcoded"; the kill rule's covered check has no teeth against a
  lying print. Material risk is low (see AUX probe): the actual completeness
  guarantee does not flow through the print but through the missing-limb
  assertion, which still flips failures/exit. Finding only — no contract
  change made or implied.

### M4 — add a duplicate case name

- Diff (verbatim second `add('clean', …)` — the minimal copy-paste accident):

```diff
--- pristine.py
+++ mutant-m4.py
@@ -296,4 +296,7 @@
         want(**{'IN-RANGE': 1}), 0,
         files=(('lane', 'present.md', 'one\ntwo\nthree\n'),))
+    add('clean', "Clean lane cite: `present.md:2`\n",
+        want(**{'IN-RANGE': 1}), 0,
+        files=(('lane', 'present.md', 'one\ntwo\nthree\n'),))
 
     base = tempfile.mkdtemp(prefix='anchorcheck-selftest-')
```

- Mutant sha256: `a14b5e7aacdd06ae6e1ab389f3cac5ae646e246e81d618d653c017e8338586b3`
- Output: `selftest cases=13 failures=0` / `limbs=9 covered=9`; exit 0.
- Verdict: **KILLED via the frozen C1 counter only** — kill rule
  `cases != 12` fires (13). Recorded nuance (coverage finding F3): the
  selftest has no internal duplicate-name guard; the duplicate runs green
  (exit 0, failures 0, covered 9). Same-named cases also share the temp dir
  `base/<name>` (sequential fixture overwrite — benign for identical
  fixtures, silently interacting for divergent ones).

### AUX probe — M3+M1 combined (hardcode covered AND drop the mirror case)

Not one of the four assigned mutants; run once to characterize F2.

- Mutant sha256: `f20cf45a85d08a8862482606102f81cd43a7b2270b8a43aeb1ce177d83f7ee27`
- Output:

```
selftest FAIL limb coverage: missing executed cases outside-base-mirror
selftest cases=11 failures=1
limbs=9 covered=9
```

- Exit: 1. The run is red via failures/exit even while the printed
  `covered=9` is now false (truly 8). Confirms the print is cosmetic and the
  missing-limb assertion carries the completeness guarantee.

## Verdict summary

| Mutant | Change | Exit | cases/failures | limbs/covered | Selftest-red | C1-counter | Verdict |
|---|---|---|---|---|---|---|---|
| M1 | drop `outside-base-mirror` case | 1 | 11 / 1 | 9 / 8 | RED | RED | KILLED |
| M2 | delete `limbs=` print | 0 | 12 / 0 | absent | green | RED (line absent ⇒ ≠9) | KILLED via counter only |
| M3 | `covered=9` hardcoded | 0 | 12 / 0 | 9 / 9 | green | green | SURVIVED |
| M4 | duplicate case name `clean` | 0 | 13 / 0 | 9 / 9 | green | RED (cases ≠ 12) | KILLED via counter only |

## Findings (coverage findings only — no contract change)

- F1 (from M2): the `limbs=/covered=` line is the only surface the C1 kill
  rule checks for completeness reporting, yet the instrument's exit status is
  independent of it. C1's protection against its deletion lives entirely in
  the counter's presence requirement. Worth keeping the frozen counter as-is;
  the instrument alone would not catch it.
- F2 (from M3): the counter cannot verify that `covered` is computed. The
  printed value is not evidence; the enforced property is "every LIMBS name
  appears in executed, else failures += 1". Any future claim wording that
  treats the printed covered as a checked number should note this ceiling.
- F3 (from M4): no internal case-name uniqueness guard; `cases=` count and
  the shared `base/<name>` fixture dir are the only observable differences.
  The frozen counter's `cases == 12` equality is the sole guard.

## Restoration evidence

- Pristine snapshot re-hash after all mutant runs:
  `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` —
  exact before/after match.
- Post-mutation pristine re-run: exit 0, `selftest cases=12 failures=0` /
  `limbs=9 covered=9`, output byte-identical to the first pristine run.
- Live lane instrument re-hash at probe end (read-only):
  `68e1bdc63e39faf116107673123d197939f77f0c00e277269f12d70ddf97ca97` —
  this seat performed zero writes to the live tree.
- Artifacts retained under `/tmp/mutc1limbs-r29/` (disposable):
  `pristine.py`, `mutant-m{1,2,3,4}.py`, `mutant-m31.py`, per-mutant
  `*.diff`, `out-*.txt`, `pristine.out`, `pristine-post.out`.

Report: .ufo/waves/round-29/wave1/MutC1Limbs.md
