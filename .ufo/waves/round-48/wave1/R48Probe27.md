# R48Probe27 — box 2 evidence-line removal

## Scope and axes
Axes: depth:verifiability — bounded grammar probe of the frozen canonical-form checker only; author-side
form, no promotion or semantic-truth judgment. Read `/home/vgpnk/.omp/agent/RULES.md`, Godspeed skill,
frozen claim `.ufo/waves/round-48/claims.json`, frozen protocol source
`.ufo/waves/round-48/controls/protocol-source.txt`, and round-47 verifier routes R1/R2
(`corpus/QUALITY.md` rows R1/R2). R1/R2 are evidence-citation routes; both are honored here — every
claim below cites its exact command output, and live-state sentences carry as-of date 2026-10-30.

Probe as assigned: on a scratch copy of canonical `SHONEN.md`, remove the evidence line of box 2 only,
run the frozen `shonen-form.py`, and compare against the unmodified positive.

## Frozen identity and integrity
- Frozen claim `.ufo/waves/round-48/claims.json` pinned identity `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`
  resolves via read-only `jj log -r 3546f7089c22...` to commit `3546f7089c22` "round-48: freeze canonical
  checklist restoration and controls". Claim C1: predicate = four-box author-assessment grammar with local
  evidence pointers; `expect_after` = `shonen-form canonical=1 finding=SF-CLEAN exit=0`.
- Frozen checker `corpus/instruments/shonen-form.py` SHA256
  `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` (hashed before and after the probe;
  unchanged — no checker amendment, per claim kill rule).
- Canonical `SHONEN.md` SHA256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`.
- Python `3.14.8`. No tool installs were needed or performed this seat.

## Mutant and expected detector
Copied `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md` to scratch
`/fast/scratch/hyaku/kasegi-r48/R48Probe27/`:

- `SHONEN.positive.md` — unmodified copy (SHA256 `b1352168...a46d0`).
- `SHONEN.box2-noevidence.md` — removed exactly one line, box 2's evidence line
  (`      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.`).
  Boxes 1, 3, 4 byte-for-byte unchanged (unified diff below). SHA256 `726144cb...ce85`.

Box 2 is the unchecked box, `- [ ] At least one end-to-end domain task executed and logged in LOG.md`.

Seat expectation: nonclean and stable SF finding. Actual expectation derived from the frozen grammar:
**clean**. The checker's per-box branch (`corpus/instruments/shonen-form.py`) is:

```python
if i < len(lines) and lines[i].startswith('      Evidence: '):
    ...pointer checks...
    i += 1
elif mark != ' ':
    return 'SF-EVIDENCE'
```

`SF-EVIDENCE` fires only when the evidence line is absent **and** the mark is asserted (`~` or `x`).
For mark ` ` (unchecked), an absent evidence line is grammar-permitted. So removing box 2's evidence
line should leave the file `canonical=1 finding=SF-CLEAN exit=0`.

## Full detector commands and observed output
Exact commands as executed (all read-only against the production tree; writes confined to scratch):

```sh
# positive control
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe27/SHONEN.positive.md; echo "PROCESS_EXIT=$?"

# mutant, box 2 evidence line removed
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe27/SHONEN.box2-noevidence.md; echo "PROCESS_EXIT=$?"

# claim counter_cmd form, default file = production SHONEN.md (read-only)
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin; echo "PROCESS_EXIT=$?"
```

Observed:

```text
=== CMD1 positive ===
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0

=== CMD2 mutant box2-noevidence ===
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0

=== CMD3 claim counter form (default file, production SHONEN.md, read-only) ===
shonen-form canonical=1 finding=SF-CLEAN exit=0
PROCESS_EXIT=0
```

Determinism re-run of the mutant twice more: both runs printed
`shonen-form canonical=1 finding=SF-CLEAN exit=0` (exit 0 each). Finding is stable.

Mutant diff (only change vs positive):

```diff
--- SHONEN.positive.md
+++ SHONEN.box2-noevidence.md
@@ -5,7 +5,6 @@
 - [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
       Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
 - [ ] At least one end-to-end domain task executed and logged in LOG.md
-      Evidence: LOG.md — No new end-to-end domain task claimed; source and diagnostic work only.
 - [~] Instructions executable by an agent without oral context
       Evidence: corpus/lessons/round-47-verifier-spotcheck.md — Declared-root recheck observations; not promotion.
 - [~] No cross-domain bleed (PROVINCE.md still accurate)
```

## Verdict
- Unmodified positive: `canonical=1 finding=SF-CLEAN exit=0` — matches claim C1 `expect_after`.
- Production claim counter (read-only): `canonical=1 finding=SF-CLEAN exit=0` — C1 after-state reproduces
  at the current tree, as-of 2026-10-30.
- **Box 2 evidence-line removal: `canonical=1 finding=SF-CLEAN exit=0`. The seat's expected nonclean
  finding was NOT observed, and no defect is reported for it** — the transformation is semantically
  permitted by the frozen predicate, exactly as the seat's escape clause anticipates. An unchecked box
  asserts nothing, so the grammar does not require it to carry an evidence pointer; the removed line was
  authorial explanation ("No new end-to-end domain task claimed..."), not a checked pointer. The checker
  distinguishes asserted boxes (`[~]` needs evidence, `[x]` is rejected as `SF-VERIFIER`) from unchecked
  ones (`[ ]` may omit evidence).
- Corroboration from frozen controls: the pre-freeze battery `.ufo/waves/round-48/controls/fixtures.json`
  carries `missing-evidence-0..3`, all expected `SF-EVIDENCE` — and all four use `[~]` marks on every box
  (verified by parsing the fixture texts). The `[ ]`-without-evidence case is undisclosed in the frozen
  battery and passes by design; this probe is therefore a distinct, complementary case, not a contradiction
  of the disclosed fixtures.

## Hygiene
- Wrote only this report and the two scratch fixtures. No production, fleet, sibling, domain-tree, or
  git/jj state edits; no commit/push; no delegation; no background jobs; no installs.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe27/` removed after this report was written; full
  command/output receipts are preserved above.
- Do-nothing control content noted for the record: `.ufo/waves/round-48/controls/do-nothing.txt` =
  `shonen-form canonical=0 finding=SF-PREAMBLE exit=1 / PROCESS_EXIT=1` (expected before-state text).
