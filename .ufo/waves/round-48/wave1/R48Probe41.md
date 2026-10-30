# R48Probe41 — Bounded grammar probe: SHONEN.md box-4 removal

- **Seat:** R48Probe41 (mutation-tester, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`)
- **Probe class:** negative mutant on a scratch copy — remove box 4 only, keep boxes 1–3 unchanged
- **Date:** 2026-10-30

## Verdict

The frozen checker **defeats** the box-4-removed mutant: `canonical=0 finding=SF-MISSING-BOX exit=1`, stable across re-run. The unmodified positive reads `canonical=1 finding=SF-CLEAN exit=0`. This transformation is **not** semantically permitted — the canonical grammar is exactly four boxes in a fixed order, so no defect is fabricated here; the SF-MISSING-BOX finding is a genuine, correct rejection.

## Transformation applied

Source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`), copied byte-identical to scratch, then box 4 deleted = removal of exactly two lines:

1. `- [~] No cross-domain bleed (PROVINCE.md still accurate)`
2. `      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.`

Boxes 1–3 left byte-unchanged (verified in mutant content below). Result: 12 lines → 10 lines; mutant sha256 `c7d32380318b8a0f09a140cffb644cc41c43210070c6eab7a14809a9992a2e6c`.

Mutant content (full):

```text
# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
- [ ] At least one end-to-end domain task executed and logged in LOG.md
      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
- [~] Instructions executable by an agent without oral context
      Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
```

## Observed commands and output (verbatim)

Frozen checker sha256 at observation: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (`corpus/instruments/shonen-form.py`). No installs this seat.

**RUN 1 — unmodified positive (`--file` on pristine scratch copy):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe41/SHONEN.canonical.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

Pristine scratch copy sha256 equals production SHONEN.md (`b1352168...`); `diff` clean.

**RUN 2 — mutant, box 4 removed (`--file`):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe41/SHONEN.box4-removed.md
shonen-form canonical=0 finding=SF-MISSING-BOX exit=1
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
shonen-form canonical=0 finding=SF-MISSING-BOX exit=1
EXIT=1
```

Identical bytes/predicate across runs — the finding is stable, not flaky.

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box 4 removed | nonclean, stable SF finding | `canonical=0 finding=SF-MISSING-BOX exit=1`, stable on re-run | yes |
| Unmodified positive | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Root default (claim counter_cmd) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why SF-MISSING-BOX (mechanism, read-only from frozen source)

The grammar is positional. After the 4-line preamble check, the checker consumes each box as a checkbox line plus an optional `      Evidence: ` continuation line. Boxes 1–3 consume lines 4–9, leaving `i = 10` at the start of the box-4 iteration. With box 4 deleted, the file has exactly 10 lines (indices 0–9), so `i >= len(lines)` and the checker returns `SF-MISSING-BOX` before any fullmatch is attempted. Note the finding is `SF-MISSING-BOX`, not `SF-BOX` — that verdict requires a mispositioned non-empty line at a box slot (as in sibling R48Probe11's box-1 removal, where box 2 promoted into box 1's slot and failed the label fullmatch). Trailing-box removal is caught by end-of-stream detection, a distinct code path in the same loop.

## Semantic-permission analysis

Removing box 4 is **not** semantically permitted under the protocol: the Promotion-gates text (protocol-source.txt, "Promotion gates" §) requires *every* `SHONEN.md` box checked with a named reviewer, and the frozen grammar encodes exactly the four labels in fixed order. Box 4 ("No cross-domain bleed (PROVINCE.md still accurate)") is a required gate item, not an optional annotation; a three-box file is not an alternative valid form. The defeat is genuine.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe41/` created explicitly; all fixtures lived there; **removed after this report was written** (receipts preserved here).
- No production file, fleet file, sibling, git/jj state, or `~/.local/bin` touched. No commit/push, no delegation, no background jobs, no tool installs.
- Bounded probe only; no build/lint blanket verification run beyond the assigned counter executions.
- Counter bytes/predicate treated as frozen: observed behavior reported, nothing amended.

## Residual limits

- One mutant shape only (full box-4 line + Evidence line removal), per seat spec. Sibling shapes (box-4 line removed but Evidence left dangling; box reordered; label text edited) were not run — other seats cover the broader battery.
- The checker's first-failure short-circuit means one mutant yields one finding code; no claim about which of several concurrent mutations would be reported.
