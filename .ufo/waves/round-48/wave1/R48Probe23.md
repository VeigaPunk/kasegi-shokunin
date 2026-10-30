# R48Probe23 — Bounded grammar probe: box-2 label single-byte mutation

- **Seat:** R48Probe23 (leaf probe; godseed lane, no subagent dispatch)
- **Round/wave:** 48 / wave1 (one v2 wave, 64 seats)
- **Claim probed:** C1 (`depth:verifiability`) — SHONEN.md canonical four-box author-assessment grammar; frozen predicate `shonen-form canonical=1 finding=SF-CLEAN exit=0`
- **Frozen claim bytes:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-48/claims.json` sha256 `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`
- **Verifier route context:** round-47 verifier spotcheck R1 (`corpus/lessons/round-47-verifier-spotcheck.md:85`) — canonical form = seed verbatim + marks confined to the box character + one indented evidence line per box, no other prose. R2 (plain-target phrasing) read; not exercised by this probe.
- **Probe type:** author-side form validation only. No promotion claim, no semantic-evidence claim, no target testing, no production edits.

## Verdict

**PASS — frozen checker defeats the box-2 one-byte label mutation exactly as the frozen grammar requires, and the unmodified positive stays clean. No counter bytes/predicate touched; no fabricated defect.**

| Case | Expected (per frozen grammar) | Observed | Match |
|---|---|---|---|
| Unmodified canonical copy (positive) | `canonical=1 finding=SF-CLEAN exit=0` | `canonical=1 finding=SF-CLEAN exit=0` | yes |
| Box-2 label 1-byte mutant | nonclean, stable SF finding | `canonical=0 finding=SF-BOX exit=1`, byte-identical on re-run | yes |
| Live tree, frozen counter_cmd (read-only) | `canonical=1 finding=SF-CLEAN exit=0` (C1 `after`) | `canonical=1 finding=SF-CLEAN exit=0` | yes |

## Frozen inputs (identity evidence)

- Checker: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py`, worktree sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`.
  - `git show HEAD:corpus/instruments/shonen-form.py | sha256sum` → `0ab32a2c…b313dd` (worktree == HEAD blob; `git status --porcelain` clean for checker and SHONEN.md).
  - Note: the checker is **absent at the claims base** `903d47e13058982460f0d90c1c2b9c7c02680646` (`git show base:…` → path not in tree). It lands with the repair commit; round-48 `measure.py` freezes it from the `after` revision. Probe therefore used the HEAD/worktree copy, which is the only existing canonical instance.
- Canonical SHONEN.md (live tree): sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` (worktree == `git show HEAD:SHONEN.md`).
- `HEAD` = `3d7e042ecbb1f17662f5042e8d3da3290722c031` (read-only observation).
- Route R1 source: `corpus/lessons/round-47-verifier-spotcheck.md:85` (13 accumulated assessment blocks / 52 `[~]` lines = the `before` drift now removed; current file is the 4-box seed shape).

## Fixture construction (scratch only)

Scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Probe23/` (created for this seat, removed on exit; receipts saved inline below).

1. `SHONEN.positive.md` = byte-for-byte copy of live canonical `SHONEN.md` (sha256 `b1352168…a46d0`, identical to production file).
2. `SHONEN.box2-label-byte.md` = positive with **exactly one byte** changed, in **box 2's label only**, all other boxes/preamble/evidence lines byte-identical:

```
=== byte diff (cmp -l, 1-based octal) ===
308 153 155
```

Byte offset 308: octal `153` (`k`, U+006B) → octal `155` (`m`, U+006D): label `… domain task executed …` → `… domain tasm executed …`.

```
=== unified diff ===
--- SHONEN.positive.md
+++ SHONEN.box2-label-byte.md
@@ -4,7 +4,7 @@
 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
       Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
-- [ ] At least one end-to-end domain task executed and logged in LOG.md
+- [ ] At least one end-to-end domain tasm executed and logged in LOG.md
       Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
 - [~] Instructions executable by an agent without oral context
       Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
```

Fixture hashes: positive `b1352168…a46d0`; mutant `814543596b1de5b79b3de6efb5bcdc39a9caa94087e405d009bf3224d1697bd5`.

## Observed commands and full output

All runs used the frozen checker with the lane root so evidence pointers resolve against the real tree.

```
TOOL=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py
ROOT=/home/vgpnk/Projects/shokunin/kasegi-shokunin
```

### RUN 1 — positive control (unmodified canonical copy)

```
$ python3 "$TOOL" --root "$ROOT" --file /fast/scratch/hyaku/kasegi-r48/R48Probe23/SHONEN.positive.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

### RUN 2 — mutant (box-2 label one byte: task→tasm)

```
$ python3 "$TOOL" --root "$ROOT" --file /fast/scratch/hyaku/kasegi-r48/R48Probe23/SHONEN.box2-label-byte.md
shonen-form canonical=0 finding=SF-BOX exit=1
PROCESS_EXIT=1
```

### RUN 3 — positive re-run (stability)

```
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

### RUN 4 — mutant re-run (stability)

```
shonen-form canonical=0 finding=SF-BOX exit=1
PROCESS_EXIT=1
```

### RUN 5 — frozen counter_cmd on the live tree (default `--file`, read-only)

```
$ python3 "$TOOL" --root "$ROOT"
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

## Expected vs observed

- Mutant: expected nonclean with a stable SF finding → observed `canonical=0 finding=SF-BOX exit=1`, reproduced byte-identically on re-run. The checker's box loop (`re.fullmatch(r'- \[([ ~x])\] ' + re.escape(label), …)`) rejects the mutated label at box 2 with `SF-BOX` before any later box is read. Stable, deterministic, single-finding.
- Positive: expected clean → observed `SF-CLEAN exit=0`, reproduced.
- Live tree (C1 counter): matches claims.json `after` (`canonical=1 finding=SF-CLEAN exit=0`) at observed `HEAD 3d7e042e…`; kill-rule trip condition (`canonical=0` at final measured revision) not observed here.

## Semantic-permission check (no fabricated defect)

The mutation is **not** semantically permitted: the four labels are frozen grammar bytes in `LABELS`; box 2's label is normative text of the checklist form, and a one-byte corruption of it is exactly the `SF-BOX` class the checker exists to catch. The frozen fixture set (`controls/fixtures.json`, `wrong-label-1`) independently covers the same rejection class for box 2 (label append `LOG.mdx` → exit 1). This probe adds a *substitution* variant (interior `k`→`m`) on a distinct byte, distinct from the frozen append fixtures, and confirms the finding code and stability. Nothing about the checker's behavior observed here is a defect; the predicate holds.

## Constraints honored

- No production/fleet/sibling/domain-tree edits; no git/jj state changes (all git invocations read-only); no commit/push; no delegation; no background jobs.
- No tool installs (nothing needed; system `python3 3.14.8`).
- Frozen counter bytes/predicate untouched; scratch fixtures only under the named scratch dir.
- Evidence pointers in fixtures resolve because `--root` stayed the real lane root while `--file` pointed at scratch copies.

## Risks / blockers

- None blocking. Context note for the integrator: the frozen checker has no blob at claims base `903d47e1` (added by the repair); round-48 `measure.py` already freezes it from the `after` revision, so scoring should key on that `after` copy, not the base tree.
- Scratch dir `/fast/scratch/hyaku/kasegi-r48/R48Probe23/` removed after report write; all receipts preserved in this report.
