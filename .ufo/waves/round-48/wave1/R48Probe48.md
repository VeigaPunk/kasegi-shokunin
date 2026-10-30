# R48Probe48 — bounded grammar probe: box 4 evidence → missing file (`shonen-form.py`)

Seat: R48Probe48 (mutation-tester, leaf — no delegation, no background jobs). Round 48 kasegi, wave 1, one v2 wave / 64 seats. Probe executed 2026-10-30. Axes named: depth:verifiability (primary, this seat), coverage (the box-4 guard limb). Scratch: `/fast/scratch/hyaku/kasegi-r48/R48Probe48/` (explicitly created; removed after receipts were saved — the receipts survive verbatim in this report). First file read this session: `/home/vgpnk/.omp/agent/RULES.md`. No tool installs (none needed). No git/jj command of any kind; production tree only read; the only production write is this report file.

## Route context

Round-47 verifier routes (`corpus/lessons/round-47-verifier-spotcheck.md:85-86`): **R1 — SHONEN.md canonical-form drift** (restore the canonical form: seed verbatim + box character + one indented evidence line per box, no other prose) — this round's frozen canonical-form repair, now guarded by the frozen counter `corpus/instruments/shonen-form.py` (0 clean; 1 noncanonical; 2 unreadable; read-only). **R2 — plain-target phrasing** — not this probe's limb. This probe attacks the R1-repaired form at exactly one point: box 4's evidence pointer.

## Fixture provenance (before bytes)

Canonical source copied, never edited in place:
```
$ cp /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md <scratch>/pristine.md
$ cp <scratch>/pristine.md <scratch>/mutant.md
$ sha256sum SHONEN.md pristine.md mutant.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  <scratch>/pristine.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  <scratch>/mutant.md
```
Pre-checks: target path `corpus/lessons/no-such-evidence-r48p48.md` confirmed **absent** under the frozen root (`TARGET-MISSING-CONFIRMED`); the four positive-control evidence pointers (`SKILL.md`, `LOG.md`, `PROVINCE.md`, `corpus/lessons/round-47-verifier-spotcheck.md`) and the counter script all confirmed present.

## Mutation (box 4 only; boxes 1–3 and preamble byte-unchanged)

Single-line edit of the last box's evidence token, keeping the ` — ` explanatory text intact:
```
12c12
<       Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
---
>       Evidence: corpus/lessons/no-such-evidence-r48p48.md — Scope unchanged; live-target testing remains refused.
```

## Detector runs — exact commands and observed output

RUN A — unmodified positive control (pristine bytes):
```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe48/pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
runA-exit=0
```
RUN B — mutant (box 4 evidence → missing file):
```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe48/mutant.md
shonen-form canonical=0 finding=SF-POINTER exit=1
runB-exit=1
```
RUN C — restored bytes (mutant.md overwritten byte-exact from pristine.md):
```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe48/mutant.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
runC-exit=0
```

## Expected vs observed

| Run | Bytes | Expected | Observed | Match |
|---|---|---|---|---|
| A | pristine | `canonical=1 finding=SF-CLEAN`, exit 0 | `canonical=1 finding=SF-CLEAN`, exit 0 | yes |
| B | box-4 missing-evidence mutant | nonclean (`canonical=0`), stable `SF-POINTER`, exit 1 | `canonical=0 finding=SF-POINTER`, exit 1 | yes |
| C | restored | `canonical=1 finding=SF-CLEAN`, exit 0 | `canonical=1 finding=SF-CLEAN`, exit 0 | yes |

## Verdict

**KILLED.** The frozen counter rejects a box-4 evidence pointer that names a repo-relative but nonexistent file with the stable, deterministic finding `SF-POINTER` (deterministic: boxes 1–3 resolve first and pass, so the first failure is exactly the mutated pointer; no traversal nondeterminism). The baseline positive control is green, so this is a conclusive kill, not an inconclusive baseline failure.

**Semantics check (no fabricated defect):** this transformation is a genuine form defect, not a semantically permitted variant. The counter's own contract (`grade()`: one plain repo-relative pointer that must satisfy `resolved.is_relative_to(root)` **and** `resolved.is_file()`) encodes the protocol rule that each checked/asserted box cites resolvable evidence; pointing box 4 at a file that does not exist makes the box's citation unresolvable, so `SF-POINTER` is the correct finding and the mutation is correctly killed. No counter escape was found on this limb.

## Restoration evidence

```
$ cp pristine.md mutant.md   # byte-exact restore
$ sha256sum mutant.md pristine.md /home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  mutant.md (restored)
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  pristine.md
b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.md (lane root, untouched)
$ diff pristine.md mutant.md && echo 'diff restored: identical'
diff restored: identical
```
Before = after hash `b1352168…4a46d0` on all three files; the live lane-root `SHONEN.md` was never written by this seat (read-only `--root` usage of the read-only counter). Scratch directory removed after these receipts were saved; full transcript preserved above.
