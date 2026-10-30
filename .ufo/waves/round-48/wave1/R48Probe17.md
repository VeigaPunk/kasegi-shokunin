# R48Probe17 — Bounded grammar probe: SHONEN.md box-1 evidence-line removal

- **Seat:** R48Probe17 (leaf; no subagent dispatch, no production edits)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis:** depth:verifiability
- **Target claim:** C1 (canonical four-box author-assessment grammar; frozen checker `corpus/instruments/shonen-form.py`)
- **Probe class:** negative mutant on a scratch copy — remove box 1's `Evidence:` line only, keep the box-1 line and boxes 2–4 unchanged
- **Date:** 2026-10-30

## Verdict

The frozen checker **defeats** the box-1-evidence-removed mutant: `canonical=0 finding=SF-EVIDENCE exit=1`, stable across re-run. The unmodified positive reads `canonical=1 finding=SF-CLEAN exit=0`, and the frozen claim's own `counter_cmd` (default `--root` invocation over the production tree) reads `canonical=1 finding=SF-CLEAN exit=0` — matching C1 `expect_after`. This transformation is **not** semantically permitted, so no defect is fabricated here: the SF-EVIDENCE finding is a genuine, correct rejection of a `[~]` mark stripped of its required evidence pointer.

## Transformation applied

Source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`), copied byte-identical to scratch as `SHONEN.positive.md` (same sha256), then exactly one line removed:

- `      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.`

The box-1 checklist line itself (`- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources`) is retained, as are boxes 2–4 with their evidence lines (verified by the unified diff below and the mutant content). Result: 13 lines → 12 lines; mutant sha256 `3dc5b7185f37be4ead29517121d9e9903dd1e3d08153f25319f88934dc9cd7b4`.

Diff (positive → mutant):

```text
--- SHONEN.positive.md
+++ SHONEN.box1-noevidence.md
@@ -3,7 +3,6 @@
 Promotion to shokunin requires all of:

 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
-      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
 - [ ] At least one end-to-end domain task executed and logged in LOG.md
       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
 - [~] Instructions executable by an agent without oral context
```

Mutant content (full, 12 lines):

```text
# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
- [ ] At least one end-to-end domain task executed and logged in LOG.md
      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
- [~] Instructions executable by an agent without oral context
      Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      Evidence: PROVINCE.md — Scope unchanged; live-target testing remains refused.
```

## Observed commands and output (verbatim)

Frozen checker sha256 at observation: `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (`corpus/instruments/shonen-form.py`). No tool installs this seat (none needed; `python3` present on host).

**RUN 1 — unmodified positive (`--file` on pristine scratch copy):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe17/SHONEN.positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

Pristine scratch copy sha256 equals production SHONEN.md (`b1352168...`); copy made with `cp` from the production file.

**RUN 2 — mutant, box-1 evidence line removed (`--file`):**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe17/SHONEN.box1-noevidence.md
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
PROCESS_EXIT=1
```

**RUN 3 — frozen claim counter_cmd form (no `--file`, default `SHONEN.md` at root), positive control over the production tree:**

```text
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

Matches C1 `expect_after` (`shonen-form canonical=1 finding=SF-CLEAN exit=0`) at the current tree; also matches the do-nothing control's expectation (`controls/do-nothing.txt` carries the drift-era `SF-PREAMBLE` before-line only as the historical `expect_before`, which the restored tree no longer reproduces — expected).

**RUN 4 — stability re-runs (positive then mutant again, same commands as RUN 1/2):**

```text
=== RUN file=SHONEN.positive.md ===
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
=== RUN file=SHONEN.box1-noevidence.md ===
shonen-form canonical=0 finding=SF-EVIDENCE exit=1
PROCESS_EXIT=1
```

Identical bytes/predicate across runs — the finding is stable, not flaky.

## Expected vs observed

| Case | Expected | Observed | Match |
|---|---|---|---|
| Box-1 evidence line removed | nonclean, stable SF finding | `canonical=0 finding=SF-EVIDENCE exit=1`, stable on re-run | yes |
| Unmodified positive | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Root default (claim `counter_cmd`) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Why SF-EVIDENCE (mechanism, read-only from frozen source)

The grammar is positional, box-at-a-time. After the 4-line preamble check, the checker fullmatches the box-1 line against `- \[([ ~x])\] <LABELS[0]>` and captures mark `[~]`. It then inspects the next line: `if lines[i].startswith('      Evidence: ')` (6-space indent). In the mutant that next line is box 2's `- [ ] At least one end-to-end domain task...`, which does not start with the evidence prefix, so control reaches `elif mark != ' ':` — the mark is `~`, not blank — and the checker returns `SF-EVIDENCE` immediately (exit 1). Box 2's own well-formedness is never reached; the first-failure short-circuit yields exactly one finding code per mutant.

Contrast with sibling mutant R48Probe11 (entire box-1 line + evidence line removed): that promotes box 2 into position 1, failing the label fullmatch → `SF-BOX`. The two probes together show the checker distinguishes *misplaced/absent box* (`SF-BOX`) from *marked box lacking its evidence line* (`SF-EVIDENCE`) — the finding vocabulary is doing real discriminating work on the box-1 surface.

## Semantic-permission analysis

Removing the evidence line is **not** semantically permitted. The File contract in `protocol-source.txt` (`SHONEN.md` row) confines marks to "the box character plus one indented evidence line per box — `[x] <verifier-id>` or `[~]` with a resolvable pointer; no other prose". A `[~]` assertion without its evidence pointer is precisely the shape the contract excludes, and the instrument's own docstring declares exit 1 = "noncanonical". The defeat is genuine; nothing about this transformation is an alternate valid form.

Relation to C1's kill_rule: the rule fails the claim if "a tested hidden/commented/duplicate checklist passes the frozen checker". This probe is a different negative class — an evidence-stripped checklist — and it too is refused. Combined with sibling probes, the frozen checker rejects both structural and evidentiary violations of the canonical four-box grammar, which is the author-side form behavior the claim's `after` predicate depends on.

## Hygiene

- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe17/` created explicitly; both fixtures (`SHONEN.positive.md`, `SHONEN.box1-noevidence.md`) lived there and were **removed after this report was written**; receipts (sha256s, diffs, verbatim outputs) preserved here.
- No production file, fleet file, sibling seat file, git/jj index or state, or `~/.local/bin` entry touched. No commit/push, no delegation, no background jobs, no tool installs, no host upgrades.
- Probe is author-side form validation only; no promotion or semantic-evidence judgment claimed, per the claim's mechanical limits.
- Counter bytes/predicate treated as frozen: observed behavior reported verbatim, nothing amended in the instrument.

## Residual limits

- One mutant shape only (box-1 evidence line removed, box-1 line retained), per seat spec. Sibling shapes (full box-1 removal, dangling evidence line, mark-only edits) are covered by other seats in this wave.
- The checker's first-failure short-circuit means one mutant yields one finding code; no claim is made about concurrent multi-site mutations.
- Positive control was run both as an explicit `--file` scratch copy and as the frozen `counter_cmd` default over the production tree; both agree, but this seat does not re-verify production conformance beyond that read-only counter execution.
