# R48Probe11 — Bounded grammar probe: SHONEN.md box-1 removal

- **Seat:** R48Probe11 (mutation-tester, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`)
- **Probe class:** negative mutant on a scratch copy — remove box 1 only, keep boxes 2–4 unchanged
- **Date:** 2026-10-30

## Verdict

The frozen checker **defeats** the box-1-removed mutant: `canonical=0 finding=SF-BOX exit=1`, stable across re-run. The unmodified positive reads `canonical=1 finding=SF-CLEAN exit=0`. This transformation is **not** semantically permitted — the canonical grammar is exactly four boxes in a fixed order, so no defect is fabricated here; the SF-BOX finding is a genuine, correct rejection.

## Transformation applied

Source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`), copied byte-identical to scratch, then box 1 deleted = removal of exactly two lines:

1. `- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources`
2. `      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.`

Boxes 2–4 left byte-unchanged (verified in mutant content below). Result: 12 lines → 10 lines; mutant sha256 `96616128fb95ad2046bef33b458eee3cbc0fd2b8ece406469b6f8bab9acb65a7`.

Mutant content (full):

```text
# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [ ] At least one end-to-end domain task executed and logged in LOG.md
      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
- [~] Instructions executable by an agent without oral context
      Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
```

## Observed commands and output (verbatim)

Frozen checker sha256 at observation: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (`corpus/instruments/shonen-form.py`). No installs this seat.

**RUN 1 — unmodified positive (`--file` on pristine scratch copy):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe11/pristine-SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

Pristine scratch copy sha256 equals production SHONEN.md (`b1352168...`); `diff` clean.

**RUN 2 — mutant, box 1 removed (`--file`):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe11/mutant-box1-removed.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1
```

**RUN 3 — frozen claim counter_cmd form (no `--file`, default `SHONEN.md` at root), positive control:**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

Matches claim C1 `expect_after` (`shonen-form canonical=1 finding=SF-CLEAN exit=0`) at the current tree.

**RUN 4 — stability re-run of the mutant:**

```text
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1
```

Identical bytes/predicate across runs — the finding is stable, not flaky.

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box 1 removed | nonclean, stable SF finding | `canonical=0 finding=SF-BOX exit=1`, stable on re-run | yes |
| Unmodified positive | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Root default (claim counter_cmd) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why SF-BOX (mechanism, read-only from frozen source)

The grammar is positional. After the 4-line preamble check, the checker fullmatches line *i* against `- \[([ ~x])\] <LABELS[0]>`, where `LABELS[0]` is the box-1 SKILL.md label. Deleting box 1 promotes box 2's line (`- [ ] At least one end-to-end domain task...`) into position 1; it fails the fullmatch against the box-1 label, so the checker returns `SF-BOX` before reaching boxes 2–4. Note the finding is `SF-BOX`, not `SF-MISSING-BOX` (that verdict requires the line stream to end early — e.g. all four boxes removed). A single-box removal is therefore caught at the first mispositioned box.

## Semantic-permission analysis

Removing box 1 is **not** semantically permitted under the protocol: the Promotion-gates text (protocol-source.txt, "Promotion gates" §) requires *every* `SHONEN.md` box checked with a named reviewer, and the frozen grammar encodes exactly the four labels in fixed order. A three-box file is not an alternative valid form. The defeat is genuine.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe11/` created explicitly; all fixtures and `probe-output.txt` lived there; **removed after this report was written** (receipts preserved here).
- No production file, fleet file, sibling, git/jj state, or `~/.local/bin` touched. No commit/push, no delegation, no background jobs, no tool installs.
- Bounded probe only; no build/lint blanket verification run beyond the assigned counter executions.
- Counter bytes/predicate treated as frozen: observed behavior reported, nothing amended.

## Residual limits

- One mutant shape only (full box-1 line + Evidence line removal), per seat spec. Sibling shapes (box-1 line removed but Evidence left dangling; box reordered; label text edited) were not run — other seats cover the broader battery.
- The checker's first-failure short-circuit means one mutant yields one finding code; no claim about which of several concurrent mutations would be reported.
