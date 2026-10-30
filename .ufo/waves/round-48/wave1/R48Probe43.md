# R48Probe43 — Bounded grammar probe: SHONEN.md box-4 one-label-byte change

- **Seat:** R48Probe43 (executor, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`; frozen claim `.ufo/waves/round-48/claims.json`)
- **Probe class:** negative mutant on a scratch copy — change exactly one label byte in box 4 only, keep boxes 1–3 and the box-4 evidence line unchanged
- **Date:** 2026-10-30

## Verdict

The frozen checker **defeats** the box-4 label-byte mutant: `canonical=0 finding=SF-BOX exit=1`, stable across re-run. The unmodified positive reads `canonical=1 finding=SF-CLEAN exit=0`, and the production tree (claim counter_cmd form, no `--file`) also reads `canonical=1 finding=SF-CLEAN exit=0`, matching C1 `expect_after`. This transformation is **not** semantically permitted — the canonical grammar pins the four box labels byte-exact, so no defect is fabricated here; the SF-BOX finding is a genuine, correct rejection.

## Transformation applied

Source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`), copied byte-identical to scratch (`pristine-SHONEN.md`, same sha256), then exactly one byte mutated on the box-4 label line:

- Line 11: `- [~] No cross-domain bleed (PROVINCE.md still accurate)` → `- [~] No cross-domain bleed (PROVINCE.md still accuratd)`
- Single byte at file offset 673 (1-based): `0x65` (`e`) → `0x64` (`d`). `cmp -l pristine mutant` lists exactly one differing byte: `673 145 144`.

Everything else byte-unchanged, verified two ways:

- `diff` shows the single line 11 hunk above; no other hunks.
- `diff` over lines 1–10 and 12 of both files: empty (`OTHERS-IDENTICAL-OK`), including the box-4 evidence line `      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.`

Mutant sha256: `b048078f1df186495a90c398d486fed9f8f6549f12762093b55b451d93a758f4`. Full mutant content:

```text
# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
- [ ] At least one end-to-end domain task executed and logged in LOG.md
      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
- [~] Instructions executable by an agent without oral context
      Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
- [~] No cross-domain bleed (PROVINCE.md still accuratd)
      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
```

## Observed commands and output (verbatim)

Frozen checker sha256 at observation: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (`corpus/instruments/shonen-form.py`). No installs this seat. Python `3.14.8`.

**RUN 1 — unmodified positive (`--file` on pristine scratch copy):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe43/pristine-SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

Pristine scratch copy sha256 equals production SHONEN.md (`b1352168...`).

**RUN 2 — mutant, box 4 one label byte (`--file`):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe43/mutant-box4-labelbyte.md
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
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe43/mutant-box4-labelbyte.md
shonen-form canonical=0 finding=SF-BOX exit=1
EXIT=1
```

Identical bytes/predicate across runs — the finding is stable, not flaky.

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box 4 label, one byte changed | nonclean, stable SF finding | `canonical=0 finding=SF-BOX exit=1`, stable on re-run | yes |
| Unmodified positive | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Root default (claim counter_cmd) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why SF-BOX (mechanism, read-only from frozen source)

The grammar is positional. After the 4-line preamble check, the checker iterates the frozen `LABELS` tuple and fullmatches line *i* against `- \[([ ~x])\] <label>` (`re.fullmatch` over the escaped label). Boxes 1–3 match, advancing the cursor to line 11; the mutated box-4 line fails the fullmatch against `LABELS[3]` (`No cross-domain bleed (PROVINCE.md still accurate)` — note `accuratd` ≠ `accurate`), so the checker returns `SF-BOX` at the first (here only) deviation. Because the mutation is a mid-label substitution rather than an early stream end, the finding is `SF-BOX`, not `SF-MISSING-BOX`; the evidence pointer on the mutated line is never evaluated. The SF-BOX code alone does not name which box failed — localization to box 4 comes from the single controlled mutation.

## Semantic-permission analysis

Changing a label byte is **not** semantically permitted under the protocol. The File contract (protocol-source.txt, `SHONEN.md` row) requires the seed block to "diff byte-identical modulo `<name>` = the repo's directory name, and marks are confined to the box character plus one indented evidence line per box — no other prose, added boxes, or removed boxes". The label text is part of the verbatim seed; the frozen checker encodes the four labels byte-exact in `LABELS`. A misspelled label is not an alternative valid form — the defeat is genuine, and this author-side form check remains silent on semantic evidence truth, per C1 `mechanical_limits`.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe43/` created explicitly; fixtures (`pristine-SHONEN.md`, `mutant-box4-labelbyte.md`) lived only there; **removed after this report was written** (receipts preserved here).
- No production file, fleet file, sibling, git/jj state, or `~/.local/bin` touched. No commit/push, no delegation, no background jobs, no tool installs.
- Bounded probe only; no build/lint blanket verification run beyond the assigned counter executions.
- Counter bytes/predicate treated as frozen: observed behavior reported, nothing amended.

## Residual limits

- One mutant shape only (single in-place label byte `e→d` in box 4), per seat spec. Sibling shapes (box removal/duplication, HTML comment wrap, code indent, Unicode lookalike, evidence-line edits, missing-pointer) were not run — other seats cover the broader battery.
- The checker's first-failure short-circuit means one mutant yields one finding code; no claim about which of several concurrent mutations would be reported.
- Round-47 routes R1 (SHONEN.md canonical-form drift — the defect C1 repairs) and R2 (frozen plain-target phrasing) were read as context in `corpus/lessons/round-47-verifier-spotcheck.md`; neither changes this probe's execution or verdict.
