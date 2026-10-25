# ScribeQuality — receipt: R15 landed in corpus/QUALITY.md

Seat: ScribeQuality (scribe, leaf — no subagent dispatch). Round 29, wave 1.
UTC: 2026-10-25. Lane base 7a6591c1eb8a14f427297980a96fa8bb339f29ee; claims-freeze f28ff5d26b29270f93163117e7255e24f0b1d947.

## Item

Land considerthese/2026-10-25.md proposal 5 as a new record criterion **R15** in
`corpus/QUALITY.md`, appended at the end, R6-safe, citing the proposal + date.

## What landed

`corpus/QUALITY.md` gained one section and one record row, appended after R14
(line 83); no existing line moved:

```
## Round-29 additions — open-defects ledger

| id | criterion | grounded in |
|---|---|---|
| R15 | A named open defect stays open only while its runnable closure check exits non-zero; every open-defect row carries its closure-check command (`bash -n`-parseable) and an evidence pointer. | considerthese/2026-10-25.md proposal 5 (2026-10-25) — routed still-open defects (D24-1, D24-4, D24-5, R25-1…R25-5) and carried debt (entry deletion shrinks the audited set while passing; `source-recheck.py --source` single-valued) are named without runnable closure checks, so nothing distinguishes open from closed; the proposal would run each closure check daily, read-only, and report flips. |
```

Criterion text is verbatim from the assignment (itself verbatim from proposal 5's
ledger idea); the `grounded in` cell cites `considerthese/2026-10-25.md` proposal 5
(2026-10-25) and names the open defects that proposal enumerates (D24-1, D24-4,
D24-5, R25-1…R25-5, plus carried debt).

## Evidence (measured before/after)

Before the edit:

- `sha256sum corpus/QUALITY.md` → `00d4b2a3898220f61a8d26477aed3a6fa928fd73bd524eacbd8979df105c9839`
- `wc -l corpus/QUALITY.md` → `83`
- `stat -c%s` → `12560`; last byte `0a` (file ends with newline on line 83)

After the edit:

- `sha256sum corpus/QUALITY.md` → `a39e0b5e2bf4631c07bd75f40209f2fc33a65c5844dca0191b51db9448ca13f9`
- `wc -l corpus/QUALITY.md` → `89` (delta +6 lines: blank, section header, blank, table header, separator, R15 row)
- `stat -c%s` → `13254` (delta +694 bytes)
- Head-bytes identity proof: `head -n 83 corpus/QUALITY.md | sha256sum` →
  `00d4b2a3898220f61a8d26477aed3a6fa928fd73bd524eacbd8979df105c9839` — **byte-identical to the whole pre-edit file**. Because the original file is exactly 83 lines ending in a newline, prefix equality means every existing line is byte-for-byte unchanged at its old number (R6-safe by construction: append-only, no insertions, no same-line rewrites).
- Spot-check anchors still at their pre-edit numbers: Q1@14, R6@40, R13@77, R14@83; R15 lands at line 89.

## R6 conformance

R6 governs edits to files other files cite by line number. All pre-existing
line-number citations to QUALITY.md (e.g. `QUALITY.md:14`, `:19`, `:37`, `:48`,
`:49`, `:50`, `:57` in wave histories/lessons) remain valid: the head-bytes proof
above shows no line number shifted. The edit adds no new `path:line`-shaped
anchors, so anchorcheck citation resolution is unaffected (the file's pre-existing
BASE-ABSENT fail classes carried since rounds 17/24 are untouched — this append
neither adds nor removes one).

## Bounds / process compliance

- Writes only under `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (QUALITY.md + this receipt). No fleet-root, sibling-lane, jj/Git-index, or `/home/vgpnk/Projects/shokuknow` writes.
- No git/jj commands run on the lane; no throwaway identities; no tool installs (nothing installed — no channel/version record applies); no pacman.
- Leaf role: no delegation, no background jobs, no swarm. No counter runs (this item has no counter; the only "before" is the sha256 capture above, which is not a PRE-STATE counter — it is the baseline digest of the file this seat edited).
- No model-dependent inference: the edit is a deterministic byte-append of the assigned text; no answering-model selection was needed or passed.

## Known limits

- `anchorcheck.py` on `corpus/QUALITY.md` exits 1 at the round-28 landed instrument digest due to pre-existing BASE-ABSENT citations (recorded in `corpus/instruments/README.md` §Round-28 amendment); this is unchanged by the R15 append and was not re-run (no before-run exists from this seat; the append-only proof is the R6 evidence).
- `corpus/README.md` / `SCORECARD.md` / lessons were not edited: not in this item's scope.
