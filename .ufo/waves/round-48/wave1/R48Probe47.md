# R48Probe47 — Bounded grammar probe: SHONEN.md box-4 evidence-line removal

- **Seat:** R48Probe47 (executor, leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`)
- **Probe class:** negative mutant on a scratch copy — remove box 4's evidence line only, keep boxes 1–3 (marks and evidence) byte-unchanged
- **Date:** 2026-10-30

## Verdict

The frozen checker **defeats** the box-4-evidence-removed mutant: `canonical=0 finding=SF-EVIDENCE exit=1`, byte-identical across re-run. The unmodified positive reads `canonical=1 finding=SF-CLEAN exit=0`. This transformation is **not** semantically permitted — a `[~]` mark requires its evidence pointer under the protocol's Promotion-gates/File-contract grammar — so no defect is fabricated here; the SF-EVIDENCE finding is a genuine, correct rejection.

## Transformation applied

Source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, 12 lines + trailing newline), copied byte-identical to scratch, then exactly one line deleted:

1. `      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.`

The box-4 mark line `- [~] No cross-domain bleed (PROVINCE.md still accurate)` is retained. Boxes 1–3 left byte-unchanged (verified by `diff` below). Result: 12 lines → 11 lines; mutant sha256 `148937fb94b9d0415cc6f6347e65399834318ba3282ac5ddc598f4551f07fc83`; last byte `0x0a` confirmed (`tail -c 1 | od -c` → `\n`), so no SF-NEWLINE confound.

`diff pristine-SHONEN.md mutant-box4-evidence-removed.md` observed:

```text
12d11
<       Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
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
```

## Observed commands and output (verbatim)

Frozen checker sha256 at observation: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (`corpus/instruments/shonen-form.py`). No installs this seat (no tool/version/channel/reason entries). All commands run with cwd `/fast/scratch/hyaku/kasegi-r48/R48Probe47`.

**RUN 1 — unmodified positive (`--file` on pristine scratch copy):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe47/pristine-SHONEN.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
EXIT=0
```

Pristine scratch copy sha256 equals production SHONEN.md (`b1352168...`); `diff` clean.

**RUN 2 — mutant, box-4 evidence line removed (`--file`):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe47/mutant-box4-evidence-removed.md
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
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
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
EXIT=1
```

Identical bytes/predicate across runs — the finding is stable, not flaky.

Full captured log preserved during the seat run at `/fast/scratch/hyaku/kasegi-r48/R48Probe47/probe-output.txt` (scratch removed on exit; contents reproduced verbatim above).

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box-4 evidence line removed | nonclean, stable SF finding | `canonical=0 finding=SF-EVIDENCE exit=1`, stable on re-run | yes |
| Unmodified positive (`--file`) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Root default (claim counter_cmd) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why SF-EVIDENCE (mechanism, read-only from frozen source)

After the 4-line preamble check, the checker walks boxes positionally. For each box it fullmatches the mark line (`- \[([ ~x])\] <label>`), then tests whether the next line starts with `      Evidence: `. If yes, it validates the pointer and — for mark `x` — returns SF-VERIFIER; otherwise it advances. If no evidence line is present and the mark is not a plain space, it returns `SF-EVIDENCE`. Box 4 carries `[~]`, and with its evidence line deleted the stream ends immediately after the mark line, so the `elif mark != ' '` branch fires: `SF-EVIDENCE`. Note this differs from the box-removal sibling probes (e.g. R48Probe11's SF-BOX): the mark line itself still matches LABELS[3] positionally, so the failure localizes precisely to the missing evidence, not to a mispositioned box.

## Semantic-permission analysis

Removing box 4's evidence line is **not** semantically permitted. The protocol's canonical-form text (protocol-source.txt, `SHONEN.md` row of the File contract) requires marks confined to the box character plus one indented evidence line per box, with `[~]` asserted by the lane *with its evidence pointer*; the Promotion-gates text requires each checked box to cite its evidence pointer. A dangling `[~]` with no pointer is exactly the attestation-without-evidence pattern the grammar bars. The defeat is genuine.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe47/` created explicitly; all fixtures and `probe-output.txt` lived there; **removed after this report was written** (receipts preserved here).
- No production file, fleet file, sibling, git/jj state, or `~/.local/bin` touched. No commit/push, no delegation, no background jobs, no tool installs.
- Bounded probe only; no build/lint blanket verification run beyond the assigned counter executions.
- Counter bytes/predicate treated as frozen: observed behavior reported, nothing amended.
- Context reads: `/home/vgpnk/.omp/agent/RULES.md`, `.ufo/waves/round-48/controls/protocol-source.txt`, `.ufo/waves/round-48/controls/do-nothing.txt`, round-47 `freeze.txt` / `counter-errata.md` / `corpus/lessons/round-47.md`, and the wave-1 spec (round-47 verifier routes R1/R2 reviewed as context; this seat's box-4-evidence mutant is local grammar, so no R1/R2 dependency is claimed).

## Residual limits

- One mutant shape only (box-4 evidence line removed, mark retained), per seat spec. Sibling shapes (mark changed to `[x]` with evidence present → SF-VERIFIER; box 4 fully removed → SF-BOX; evidence line garbled → SF-POINTER) were not run — other seats cover the broader battery.
- The checker's short-circuit means one mutant yields one finding code; no claim about concurrent mutations.
- Author-side form only: this probe validates grammar, not promotion readiness or the semantic truth of box-4's PROVINCE.md assertion.
