# R48Probe35 — Bounded grammar probe: SHONEN.md box-3 code-indentation

- **Seat:** R48Probe35 (mutation-tester, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`; predicate form-validation only, not promotion or evidence truth)
- **Probe class:** negative mutant on a scratch copy — indent box 3 only as code (4-space prefix on both of its lines), keep boxes 1, 2, 4 byte-unchanged
- **Date:** 2026-10-30

## Verdict

The frozen checker **defeats** the box-3-code-indented mutant: `canonical=0 finding=SF-BOX exit=1`, stable across re-run. The unmodified positive reads `canonical=1 finding=SF-CLEAN exit=0`, and the frozen claim `counter_cmd` form (default `--root` read of the production `SHONEN.md`) also reads `canonical=1 finding=SF-CLEAN exit=0`, matching C1 `expect_after` at the current tree. Indenting a checklist box as code is **not** semantically permitted under the canonical four-box grammar — no defect is fabricated here; the SF-BOX finding is a genuine, correct rejection.

## Transformation applied

Source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` for production; pristine scratch copy sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, byte-identical, `diff` clean). Mutant built in scratch by prefixing exactly 4 spaces onto each of box 3's two lines; every other line byte-unchanged. Result: 12 lines → 12 lines; mutant sha256 `c126e837bb521f3470e823719ce97013b5f272d77c662383fd5039b8052fa135`.

`diff pristine-SHONEN.md mutant-box3-code-indented.md` (verbatim, the entire diff):

```text
9,10c9,10
< - [~] Instructions executable by an agent without oral context
<       Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
---
>     - [~] Instructions executable by an agent without oral context
>           Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
```

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
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
```

## Observed commands and output (verbatim)

Frozen checker sha256 at observation: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (`corpus/instruments/shonen-form.py`). Python 3.14.8. No installs this seat (none needed).

**RUN 1 — unmodified positive (`--file` on pristine scratch copy):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe35/pristine-SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

**RUN 2 — mutant, box 3 indented as code (`--file`):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe35/mutant-box3-code-indented.md
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
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe35/mutant-box3-code-indented.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1
```

Identical bytes/predicate across runs — the finding is stable, not flaky.

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box 3 indented as code | nonclean, stable SF finding | `canonical=0 finding=SF-BOX exit=1`, stable on re-run | yes |
| Unmodified positive | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Root default (claim counter_cmd) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why SF-BOX (mechanism, read-only from frozen source)

The grammar is positional. After the 4-line preamble check (`i` = 4), the checker fullmatches each box line against `^\- \[([ ~x])\] <LABELS[k]>$` via `re.fullmatch`, so the `- ` marker must begin at column 0. Indenting box 3's marker with 4 spaces (`    - [~] Instructions executable...`) makes the fullmatch fail at box-position 3 (after boxes 1–2, including box 2's evidence line, consumed cleanly), and the checker returns `SF-BOX` before ever examining the indented evidence line. The indented `Evidence:` line (10 leading spaces) is moot for this mutant, but it was indented too: a code block containing only the marker line while leaving the evidence line at list-continuation indent would be a different mutant shape.

Note the finding is `SF-BOX`, not `SF-POINTER` or `SF-EVIDENCE`: the first failure short-circuits at the box-position fullmatch, so one mutant yields exactly one finding code. Line count is unchanged (12 → 12), so `SF-TRAILING` is not reachable here; the preamble and trailing-newline checks (`SF-PREAMBLE`, `SF-NEWLINE`) are unaffected by the mutation.

## Semantic-permission analysis

Indenting a checklist box as code is **not** semantically permitted under the protocol. The Promotion-gates text (protocol-source.txt, "Promotion gates" §) requires every `SHONEN.md` box checked with a named reviewer against the fixed four-label checklist, and the frozen grammar encodes exactly those four labels in fixed order at column 0 with optional `      Evidence: ` continuations. A box sunk into an indented code block is, in markdown rendering, no longer a checklist entry at all — it exits the list structure — so it is not an alternative valid form of the same assertion. This probe is author-side form validation only: it says nothing about box 3's underlying evidence truth (`corpus/lessons/round-47-verifier-spotcheck.md`, the round-47 R2 "Correction (round 40)" context in controls/shonen-before.txt:208), which remains independently judged. The defeat is genuine and no defect is fabricated.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe35/` created explicitly; all fixtures (`pristine-SHONEN.md`, `mutant-box3-code-indented.md`) and `probe-output.txt` lived there; **removed after this report was written** (receipts preserved here).
- No production file, fleet file, sibling, domain tree, git/jj index or state, or `~/.local/bin` touched. No commit/push, no delegation, no background jobs, no tool installs.
- Bounded probe only; the assigned counter executions are the only verification run.
- Counter bytes/predicate treated as frozen: observed behavior reported, nothing amended; the checker was executed read-only.

## Residual limits

- One mutant shape only (box 3's marker + Evidence lines each prefixed with 4 spaces), per seat spec. Sibling shapes (fenced ``` code block around box 3; marker-only indentation; indentation of box 1 or 4) were not run — other seats cover the broader battery.
- The checker's first-failure short-circuit means one mutant yields one finding code; no claim about which finding several concurrent mutations would report.
- RUN 3 measures the current lane tree; the lane working tree carries unrelated in-flight seat outputs (other wave1 reports, `SKILL.md` modified) that do not intersect this probe's scope.
