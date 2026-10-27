# ScoutKillRuleSpec — round-41 wave-1 receipt

Seat: `ScoutKillRuleSpec` (scout, leaf). Item: extract the committed CritKillRule
escape states from `.ufo/waves/round-40/wave2/` into a byte-clean input table for
`ExecI11KillRule`. Axes: depth:verifiability (primary), coverage. No lane file
other than this receipt + the deliverable was written; no subagents; no tool
installs; no network fetches; read-only git only (no git commands run at all).

## Deliverable

`wave1/ScoutKillRuleSpec.txt` — the eight escape states as a numbered table
`name | setup | limb escaped | missed clause | fix`, verbatim where the source
gives shell. 102 lines, sha256
`7469eee739c13f07c6ff3ef72e0b3d18110c48e5062984383ce468220dd3c704`.

## Sources read (fully)

- `wave2/CritKillRule.md` — 237 lines, all of sections 1-3 read (plus 4-5 for
  fix and hygiene context).
- `wave2/CritKillRule.pending-variants.md` — 49 lines (F7 fixture).
- `wave2/CritKillRule.worktree-clean.sh` — 38 lines (F8 fixture).
- `claims.json` (round-41 frozen claims, read first, unedited).
- `wave1/CORRECTIONS-L1.md` (mid-wave freeze corrections, authoritative).

## Cross-check: all eight present

The file's own count line (CritKillRule.md line 9) reads:

> **Verdict: 7 distinct escape states reproduced.**

The committed section-2 headings, however, enumerate EIGHT `### F` escape
states — F1, F2, F3, F4, F5, F6, F7, F8 (grep `^### F[0-9]` → lines 41, 58, 80,
94, 107, 127, 142, 152). **CORRECTIONS-L1.md item 2 (authoritative) resolves the
7-vs-8 conflict: the committed headings win; I11's target is all eight states
(`escapes=8 red=8` naming F1-F8); the intro prose "7 distinct" is a freeze-typo
undercount (M41 row).** The deliverable therefore lists all eight. (Section 4's
combined `F1/F2` correction bullet is the likely source of the prose "7" — the
two share one fix — but per the correction they remain two distinct escape
states.)

Name-column fidelity verified byte-for-byte: the eight spec `[n] name:` cells
match the source `### F<n> — …` heading text exactly (stripping only each
heading's trailing parenthetical gloss, which is preserved inside the row).

## Field completeness per entry (8 rows x 4 fields = 32, all present)

Each row carries: `name` | `setup` (verbatim shell where the file gives it:
mkdir/ln/bash lines and observed `H6 payload=… closed=…` outputs; for F7/F8 the
fixture-file commands and transcripts) | `limb escaped` (F1-F6: the H6
scratch-leftover scan; F7: the pending-marker kill clause `` `grep -c
'⟨pending' corpus/lessons/round-40.md` != 0 ``; F8: the working-tree-clean clause
enforced via `git -C <lane> status --porcelain` per
`scripts/hyaku/closure-prompt.md`) | `missed clause` | `fix` (the section-4
recommendation, quoted).

Limb mapping for the I11 implementer: F1-F6 red the H6 limb; F7 reds the
pending-marker clause; F8 reds the clean-tree clause. Unicode payloads preserved
byte-exact: U+27E8 `⟨` (5 `⟨pending` occurrences), U+2329 `〈` (4), U+2011
non-breaking hyphen in `kasegi‑r40‑stray`, U+2212 in `kasegi−r40−stray`.

## Correction log (M41 handling)

The dispatched spec text said "the EXACT seven escape states" and gave a 38-char
base literal. Per CORRECTIONS-L1.md: (1) the base is the 40-char
`5b29ea1439450b712581edf5f0f0bf98dfb262ab` (irrelevant to this read-only seat —
no export run needed); (2) the I11 target is eight states F1-F8. Deliverable
updated from a 7-row draft to the committed 8-row shape before receipt write.

## Hygiene

- No `git`/`jj` mutations run anywhere; extraction was read-only.
- Scratch `S=/fast/scratch/hyaku/kasegi-r41/ScoutKillRuleSpec/` removed before
  yield (`rm -rf`); nothing kasegi-r41-family survives from this seat.
- Disk guard not consulted (read-only extraction, <50KB of writes total).
- No tools installed; no pacman; no writes to PATH dirs or fleet-root tracked
  files; /home/vgpnk/Projects/shokunin and /home/vgpnk/Projects/shokuknow
  untouched.
