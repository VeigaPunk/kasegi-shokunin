# R48Probe45 — Bounded grammar probe: box-4 indented as code

- Seat: R48Probe45 (executor, leaf — no subagent dispatch)
- Round: 48, kasegi lane; lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
- Frozen claim: `.ufo/waves/round-48/claims.json` sha256 `3546f7089c224ac6c8adc68208b1e648bbf3e6a5` (recomputed `b8022cdf4d4bfa8efb0dabc807318e02a66d1ab1101b726a20f1f31c69f2a345`, matches `freeze.txt` `claims-sha256`; note the assignment header cites the claims content hash, freeze.txt pins the file hash)
- Frozen counter: `corpus/instruments/shonen-form.py` sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (read-only, never edited)
- Canonical: `SHONEN.md` sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`
- Round-47 verifier routes R1/R2: searched round-47 wave/controls trees — no route definitions by that name exist there; R1/R2 appear only as historical verifier references inside `controls/shonen-before.txt` (e.g. "Verifier R2's ask"). Not load-bearing for this grammar probe; noted as context only.

## Task

On a scratch copy of canonical SHONEN.md, for box 4 only, indent the box as code; run the frozen `shonen-form.py` with `--root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file <scratch file>`; expect nonclean + stable SF finding; also run the unmodified positive. No production edits.

## Fixture construction (scratch only)

Scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Probe45/` created explicitly. `SHONEN.md` copied byte-identical from the lane root (hash verified equal above); `SHONEN-unmodified.md` is the untouched positive control.

Mutation (box 4 only — the checkbox line and its evidence line, both indented 4 spaces so the box renders as a Markdown code block; every other byte unchanged):

```diff
11,12c11,12
< - [~] No cross-domain bleed (PROVINCE.md still accurate)
<       Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
---
>     - [~] No cross-domain bleed (PROVINCE.md still accurate)
>           Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
```

(diff exit 1 = files differ; diff is confined to lines 11–12. Trailing newline preserved: last byte `0x0a`.)

## Observed commands and output

Mutant (box 4 as code), run 1:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe45/SHONEN.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1
```

Stability repeats (runs 2–3, identical):

```
shonen-form canonical=0 finding=SF-BOX exit=1   (EXIT=1)
shonen-form canonical=0 finding=SF-BOX exit=1   (EXIT=1)
```

Unmodified positive control:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe45/SHONEN-unmodified.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box 4 indented as code | nonclean, stable SF finding, exit 1 | `canonical=0 finding=SF-BOX exit=1`, identical across 3 runs | yes |
| Unmodified positive | clean, exit 0 | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why the finding is SF-BOX (and not fabricated)

The frozen checker grade() requires each box line to `re.fullmatch(r'- \[([ ~x])\] <label>')` with no leading whitespace. Indenting box 4 by 4 spaces makes line 11 `    - [~] No cross-domain bleed ...`, which fails the fullmatch at the box-4 iteration → `SF-BOX`. The finding fires before any pointer/evidence logic, is deterministic (pure line scan), and the 3 repeat runs return byte-identical output. The transformation is genuinely not semantically permitted: the canonical grammar fixes box lines at column 0, and "indent as code" is precisely the class of surface mutation the grammar rejects. No defect is fabricated — the observed nonclean result is the checker's specified behavior for this mutant.

## Scope and hygiene

- No production files edited; frozen checker read-only; `--root` points at the lane root so evidence-pointer resolution is unchanged.
- `git status` at lane root before reporting showed pre-existing modifications/untracked files (e.g. `M SKILL.md`, sibling probe reports) — none authored by this seat.
- No tool installs were needed or performed this wave (nothing new installed; pacman untouched).
- Scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Probe45/` removed on exit after this report landed; fixtures' content is fully reproduced above.

## Verdict

Bounded grammar probe passes: the frozen canonical-form counter is sensitive to a code-indent mutation of box 4 (`SF-BOX`, exit 1, stable over repeats) and clean on the unmodified canonical file (exit 0). Counter behavior matches the seat's expectation; no counter defeat observed.
