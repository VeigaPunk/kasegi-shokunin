# R48Probe13 — Bounded grammar probe: box-1 label byte change

- Seat: R48Probe13 (executor, lane `kasegi-shokunin`, round 48 wave 1)
- Axis: depth:verifiability
- Frozen claim probed: C1 (`claims.json`), predicate = "SHONEN.md conforms to the canonical
  four-box author-assessment grammar" — form validation only, not promotion or evidence truth.
- Round-47 route context: `corpus/lessons/round-47-verifier-spotcheck.md:85` (R1 — SHONEN.md
  canonical-form drift) names this exact repair; R2 (plain-target phrasing) is unrelated to
  this probe and was read for context only.
- No production edits. No git/jj mutation. No tool installs (python3 3.14.8 at /usr/bin/python3
  sufficed — nothing installed, nothing upgraded; pacman untouched).

## Probe design

Transformation: on a scratch copy of canonical `SHONEN.md`, box 1 only, change exactly one
label byte — `SKILL.md contains` → `SKILL.md containz` (single character `s` → `z` on the
box-1 label line). Box character (`[~]`), box-1 evidence line, and boxes 2–4 left unchanged.

Byte-level verification of the fixture (before running the counter):

```
$ cd /fast/scratch/hyaku/kasegi-r48/R48Probe13
$ cmp -l SHONEN.positive.md SHONEN.mut-label-byte.md
106 163 172
cmp_exit=1
$ diff SHONEN.positive.md SHONEN.mut-label-byte.md
5c5
< - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
---
> - [~] SKILL.md containz real decision tables, error patterns, checklists, cited sources
```

`cmp -l` reports exactly one differing byte: file offset 106 (1-based), octal 163 (`s`)
→ octal 172 (`z`). `diff` shows the only changed line is line 5 (the box-1 label line).

Fixture hashes:

```
SHA256 b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0  SHONEN.positive.md   (identical to production SHONEN.md)
SHA256 6a315159846cfdce42dc9b4ba41049e86380c78d337cf9445a8e247bfd0531f2  SHONEN.mut-label-byte.md
SHA256 0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd  corpus/instruments/shonen-form.py (frozen checker, unmodified)
```

## Observed results

### Unmodified positive (scratch copy of canonical SHONEN.md)

Command (exactly as executed):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe13/SHONEN.positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

- Expected: `canonical=1 finding=SF-CLEAN exit=0` (matches claims.json `expect_after`).
- Observed: matches exactly; process exit 0. Re-run once more later in the session with the
  same result.

### Mutant (box-1 label, one byte)

Command (exactly as executed, run 3 times):

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe13/SHONEN.mut-label-byte.md
shonen-form canonical=0 finding=SF-BOX exit=1
PROCESS_EXIT=1
```

- Expected per seat spec: nonclean and stable SF finding (grammar reading: `SF-BOX` — the
  box line can no longer `re.fullmatch` the frozen `LABELS[0]` string).
- Observed runs 1/2/3: all three printed `shonen-form canonical=0 finding=SF-BOX exit=1`,
  process exit 1. Finding is byte-for-byte identical across runs — deterministic, no state,
  no time dependence. **Probe expectation met.**

## Expected vs observed summary

| Case | Expected | Observed | Match |
|---|---|---|---|
| Unmodified positive | canonical=1 SF-CLEAN exit=0 | canonical=1 SF-CLEAN exit=0 | yes |
| Mutant (1 label byte, box 1) | nonclean, stable SF finding | canonical=0 SF-BOX exit=1, stable ×3 | yes |

## Why this rejection is correct, not a fabricated defect

The frozen checker pins each box label verbatim (`re.fullmatch` against the `LABELS` tuple at
`shonen-form.py:30`). The canonical form per the protocol source (Promotion gates: "the seed
below changes only with this gate text") and the round-47 R1 route ("seed verbatim + marks
confined to the box character plus one indented evidence line per box, no other prose") leaves
no room for label-text drift: any single-byte change to a label is a canonical-form violation
by definition. The transformation is therefore **not** semantically permitted — the `SF-BOX`
finding is the checker's designed behavior for exactly this mutation, and reporting it
requires no generosity. The checker also stops at the first failing box, so a label mutation
in any box reads as `SF-BOX`.

Positive run additionally confirms the production `SHONEN.md` at the freeze satisfies the
frozen canonical grammar (form-only; semantic evidence and promotion remain independently
judged, and the `[~]` marks are author assertion by design — the checker itself rejects `x`
with `SF-VERIFIER`).

## Hygiene

- Fixtures lived only under `/fast/scratch/hyaku/kasegi-r48/R48Probe13/`; receipts are the
  commands/outputs above. Scratch dir removed after this report was written.
- Production tree, fleet root, siblings, git/jj state: untouched (read-only access only).
