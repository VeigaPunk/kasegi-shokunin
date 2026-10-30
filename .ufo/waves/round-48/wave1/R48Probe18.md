# R48Probe18 — bounded grammar probe: box-1 evidence pointer to a missing file

Seat: R48Probe18 (mutation-tester, leaf; no delegation, no background jobs)
Axis: depth:verifiability
Lane root: /home/vgpnk/Projects/shokunin/kasegi-shokunin
Frozen claim: .ufo/waves/round-48/claims.json at 3546f7089c224ac6c8adc68208b1e648bbf3e6a5
Detector (frozen, unmodified): /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
  sha256 0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd
Canonical input: /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
  sha256 b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0 (before and after the probe; production bytes never edited)
Scratch: /fast/scratch/hyaku/kasegi-r48/R48Probe18/ (created explicitly; removed on exit after receipts saved here)
Runtime: Python 3.14.8 (pre-existing). Tool installs: none (pacman transactions paused host-wide; none needed).

## Mutant

On a scratch copy of canonical SHONEN.md, box 1 only: the evidence pointer token
`SKILL.md` was replaced with `MISSING-R48Probe18.md`, a repo-relative plain path confirmed
absent under `--root` (`test ! -e .../MISSING-R48Probe18.md` passed before the run). All other
boxes, marks, labels, evidence text, preamble and trailing newline are byte-unchanged:

```
--- SHONEN.pristine.md	2026-10-30 11:59:46.532433736 -0300
+++ SHONEN.mutant.md	2026-10-30 12:00:44.724918082 -0300
@@ -3,7 +3,7 @@
 Promotion to shokunin requires all of:
 
 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
-      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
+      Evidence: MISSING-R48Probe18.md — Author assertion; outside promotion verification remains required.
 - [ ] At least one end-to-end domain task executed and logged in LOG.md
       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
 - [~] Instructions executable by an agent without oral context
```
(diff exit=1, exactly one line changed.)

Expected detector behavior (from the frozen predicate, read before running): the evidence token
is a non-absolute, `..`-free posix path, so it passes the shape checks; `(root / token).resolve()`
stays inside root but `resolved.is_file()` is False for a missing file, so `grade()` returns
`SF-POINTER` and `main()` prints `canonical=0 finding=SF-POINTER exit=1`, shell exit 1. The
unmodified positive must print `SF-CLEAN exit=0` (all four canonical pointers — SKILL.md, LOG.md,
corpus/lessons/round-47-verifier-spotcheck.md, PROVINCE.md — were confirmed to exist under root
beforehand, so the baseline is not inconclusive).

## Observed commands and full output

### 1. Unmodified positive (pristine scratch copy)

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe18/SHONEN.pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
shell-exit=0
```
Expected exit 0 / SF-CLEAN; observed exit 0 / SF-CLEAN. MATCH. Fixture sha256 before mutation:
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0 (identical to production SHONEN.md).

### 2. Mutant, run 1

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe18/SHONEN.mutant.md
shonen-form canonical=0 finding=SF-POINTER exit=1
shell-exit=1
```
Expected nonclean, specifically SF-POINTER, exit 1; observed SF-POINTER, exit 1. MATCH.

### 3. Mutant, run 2 (finding stability)

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe18/SHONEN.mutant.md
shonen-form canonical=0 finding=SF-POINTER exit=1
shell-exit=1
```
Identical finding and exit across runs: the SF finding is stable. Mutant fixture sha256:
653d24552626ad110a5863872dd13eed768bcffd77e901bc49ac975368c39b56.

### 4. Restored bytes, detector re-run

```
$ cp SHONEN.pristine.md SHONEN.mutant.md
$ sha256sum SHONEN.pristine.md SHONEN.mutant.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.pristine.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.mutant.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
$ cmp SHONEN.pristine.md SHONEN.mutant.md && echo 'restored bytes identical to pristine'
restored bytes identical to pristine
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe18/SHONEN.mutant.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
shell-exit=0
```
Expected SF-CLEAN exit 0 on restored bytes; observed SF-CLEAN exit 0. MATCH.

## Verdict

KILLED. The box-1 missing-evidence-target mutant is defeated by the frozen predicate with the
expected, stable finding `SF-POINTER` and exit 1, against a valid clean baseline (positive
SF-CLEAN exit 0) and a byte-identical restore that returns to SF-CLEAN. No counter bytes or
predicate were modified; no production file, fleet file, sibling, domain tree, or git/jj state
was touched. Author-side form result only — not promotion evidence and not semantic truth.

## Semantic-permission check

The mutation is NOT semantically permitted, so this is a genuine defect rather than a permitted
transformation: the protocol's box-1 bar (protocol-source.txt, Promotion gates) requires each of
the decision table, error-pattern list and checklist to cite "a resolvable source (repo path,
command output, or external document)". Pointing the evidence at a nonexistent repo file makes
the pointer unresolvable, and the canonical form's one evidence line per box (round-47 verifier
route R1) is exactly where that resolvability is anchored. The frozen checker's SF-POINTER limb
and the protocol requirement agree here; no explanation of permissibility is owed.

## Round-47 verifier routes R1/R2 relevance

R1 (corpus/lessons/round-47-verifier-spotcheck.md §R1, "SHONEN.md canonical-form drift"): the
round-48 repair restored SHONEN.md to the canonical seed form — four boxes, marks confined to
the box character, one indented evidence line per box, no other prose. This probe exercises the
repaired form's pointer-resolution limb on box 1 only, with the positive control demonstrating
the repaired canonical bytes grade SF-CLEAN. R2 (plain-target phrasing in frozen grep targets)
concerns a different instrument class and is not applicable to this grammar probe; nothing here
modifies or re-pins any frozen target.

## Scope and cleanup

Writes: this report plus the named scratch fixtures SHONEN.pristine.md / SHONEN.mutant.md under
/fast/scratch/hyaku/kasegi-r48/R48Probe18/. All receipts (commands, outputs, hashes, diff) are
saved in this report; the scratch directory was removed on exit and its removal verified.
No tool installs or updates were performed. No builds, lints, or blanket verification were run;
only the assigned bounded probe above was executed.

Report: .ufo/waves/round-48/wave1/R48Probe18.md
