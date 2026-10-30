# R48Probe14 — bounded grammar probe: box 1 wrapped in HTML comment

Round 48 kasegi, wave 1. Seat R48Probe14 (mutation-tester, leaf — no delegation, no background jobs).
Frozen claim: `.ufo/waves/round-48/claims.json` @ `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`.
Scope: author-side canonical form only (`corpus/instruments/shonen-form.py`), not promotion, not semantic truth, no production edits, no target testing.

## Godspeed axes

1. **Depth** — full exact commands, stdout, exit codes, and before/after byte hashes for every run.
2. **Verifiability** — every command is reproducible verbatim against the frozen lane-root counter; hashes pin all inputs and outputs.
3. **Safety** — zero writes outside this report and the named scratch dir; canonical and counter bytes hashed before and after.

## Provenance (frozen bytes)

- Canonical source: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/SHONEN.md`
  sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`
- Frozen counter: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py`
  sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`
- Scratch (created, then removed): `/fast/scratch/hyaku/kasegi-r48/R48Probe14/`
  - `SHONEN.pristine.md` — byte-identical copy of canonical (sha256 `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`)
  - `SHONEN.mutant-box1-comment.md` — the mutant, sha256 `261f20f680c79f21901a7c0dbaa59298ed5758997d2b2ef17385b50d2285773f`

No tools installed (none needed). All pacman transactions honored as paused; no upgrades, no restarts.

## Mutation (smallest behavior-bearing point)

Box 1 only — the `- [~]` item **and its 6-space Evidence continuation line** — wrapped in an HTML comment. Boxes 2–4 and the preamble untouched.

Before (lines 5–7 of the pristine copy):

```
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
- [ ] At least one end-to-end domain task executed and logged in LOG.md
```

After:

```
<!--
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      Evidence: SKILL.md — Author assertion; outside promotion verification remains required.
-->
- [ ] At least one end-to-end domain task executed and logged in LOG.md
```

## Expected detector (from frozen counter source)

`grade()` consumes the 4-line preamble, then `re.fullmatch(r'- \[([ ~x])\] <label>', lines[i])` for each of the four labels in order. Line 5 of the mutant is `<!--`, which fails the box-1 fullmatch ⇒ `SF-BOX`, exit 1. Pristine copy ⇒ `SF-CLEAN`, exit 0.

## Runs — expected vs observed (full outputs)

Run 1 — mutant:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe14/SHONEN.mutant-box1-comment.md
shonen-form canonical=0 finding=SF-BOX exit=1
exit=1
```

Expected: nonclean, stable `SF-BOX`, exit 1. Observed: exactly that. Match.

Run 2 — unmodified positive:

```
$ python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/shonen-form.py --root /home/vgpnk/Projects/shokunin/kasegi-shokunin --file /fast/scratch/hyaku/kasegi-r48/R48Probe14/SHONEN.pristine.md
shonen-form canonical=1 finding=SF-CLEAN exit=0
exit=0
```

Expected: `SF-CLEAN`, exit 0. Observed: exactly that. Match.

Note both runs used the frozen lane root as `--root` per seat spec, so the evidence pointers (`SKILL.md`, `LOG.md`, `corpus/lessons/round-47-verifier-spotcheck.md`, `PROVINCE.md`) resolved against the lane and did not contaminate either result.

## Verdict

**KILLED** — baseline (pristine positive) passed, so the mutant result is conclusive: the frozen counter detects the box-1 HTML-comment wrap with the stable, correctly-attributed finding `SF-BOX` at the exact box position. This is a coverage confirmation, not a contract change.

## Is the transformation semantically permitted?

No — the defeat is legitimate, not a form-check false positive. An HTML comment is *valid Markdown syntax*, but it is invisible when rendered: the rendered checklist would show only boxes 2–4, silently dropping the box-1 requirement ("SKILL.md contains real decision tables…") and its evidence line from every rendered view of the file. That changes the document's author-side meaning, so the canonical-form invariant correctly rejects it. The counter's proximate reason is line grammar (`<!--` fails the box pattern) rather than rendered-content analysis, but it lands on a real defect.

## Restoration evidence

- Production canonical `SHONEN.md` sha256 before runs `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0`, after runs `b1352168dd7322e73f7ab2ff3e4793c77084845305d1b3a9a9e6a94a034a46d0` — identical; never modified (all mutation happened on the scratch copy).
- Frozen counter sha256 before `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd`, after — identical.
- No git/jj commands issued; no commits; no sibling or fleet files touched.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Probe14/` removed after these receipts were saved into this report (`rm -rf` at exit; removal confirmed).

No gate/integration action taken or implied; findings reported to the sole integration owner (KasegiR48) via this file.
