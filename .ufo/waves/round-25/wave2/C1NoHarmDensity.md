# Round 25 wave 2 — falsify ScoutNoHarm baseline (C1NoHarmDensity)

Seat: `L1Kasegi25.C1NoHarmDensity` · read-only · lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
Attacked item: `density.py SKILL.md` and `anchorcheck.py SKILL.md` re-run vs `wave1/ScoutNoHarm.md` baseline.
Run at 2026-10-25T09:00Z. All commands from lane root.

## Verdict

**BASELINE CONFIRMED, with one factual typo.** Every reproducible claim in `wave1/ScoutNoHarm.md`
holds: both instrument outputs regenerate **byte-identical** (same sha256), same exit 0, same line
counts and counters. `SKILL.md` is still byte-equal to `b49948f`, so the no-harm gate on
depth:density passes trivially — nothing the round did moved the density or anchor proxies.
The only wrong number in the baseline is a **byte-count typo** (stated `3209`, actual `3232`); it is
informational metadata, not a gate input, so it does not weaken any conclusion.

## Reproduced runs

| command | exit | stdout sha256 | lines |
|---|---:|---|---:|
| `python3 corpus/instruments/density.py SKILL.md --label r25-before` | 0 | `d1708ba3a28d4356e60aae1e29a13bcc87fab74f5e2ef3c3680eb1b9cd2cba56` | 31 |
| `python3 corpus/instruments/anchorcheck.py SKILL.md` | 0 | `61abb8f6ab3b8749465eb5094ba430a37cdba4e8929ed20fef4608bf2d858464` | 315 |

Both digests **equal the baseline's published digests exactly**. stderr was empty in both runs, so
stdout and combined stdout+stderr digests coincide. A second independent re-run of each produced the
same digest again (determinism confirmed twice more on top of the baseline's own twice).

### anchorcheck counters (re-derived, not just digest)

- header verbatim: `== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`
- `grep -c '^LOST-RECORDED'` → **306** (baseline's 306 ✓; a bare `grep 'LOST-RECORDED'` gives 307 only because the header line itself contains the token)
- `grep -c '^OK '` → **7** ✓
- LOST `md:` span → **57 … 989** ✓ (first LOST line is output line 3, `md:57`)

### density counters (re-derived)

- file lines `1023`, blocks `19`, mean dens `154.0`, total path-citation instances `652` — all equal baseline.
- stdout byte count: `wc -c` → **3232**. Baseline section 1 states `3209`. Since the sha256 is identical the content is identical; the `3209` is a transcription typo. **Smallest correction: change `3209` to `3232`** in `wave1/ScoutNoHarm.md` §1 ("3209 bytes" → "3232 bytes"). No code change.

## Protected-file check vs `b49948f` (live tree now)

`git rev-parse master` = `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` (unchanged base). `git show <base>:<f> | sha256sum` vs working tree:

| file | result |
|---|---|
| `SKILL.md` | **SAME** (`f74a9f33…24af`) |
| `corpus/instruments/density.py` | SAME (`ee803726…4710`) |
| `corpus/instruments/anchorcheck.py` | SAME (`c2a9e6c6…f748`) |
| `corpus/instruments/resolve.py` | SAME (`db5e0767…5667`) |
| `corpus/README.md` | DIFF (round-25 C2 rows + F10 line) |
| `SCORECARD.md` | DIFF (round-25 claims table + D24-2/3 residual rewrites) |

The two diffs are **round-owned surfaces, not unexplained drift**: `corpus/README.md` gains the F10
admitted row + r25 correction line (C2's own claim surface); `SCORECARD.md` gains the "Round 25 —
frozen claims C1/C2" claims table whose `depth:density` row records exactly these same numbers
(mean 154.0, 652 instances, bad=0, LOST=306 — self-consistent with this re-run). The baseline's own
escape clause covers this: hashes must be unchanged *"unless a round item explicitly owns that file"*.

`git status --porcelain` now shows 38 modified + 6 untracked (C1 instrument, two new C2 entries,
round-25 lesson, source snapshots, `.ufo/`) — consistent with the round's landed work, none of it
touching the measured surface.

## Falsifiability note

The baseline is falsifiable and survives: any round edit to `SKILL.md` would have changed both
output digests; any edit to the two instruments would change their blob sha at `b49948f` comparison.
Neither happened. The gate's real teeth (`mean ≥154.0`, `cites ≥652`, `bad=0`, `LOST ≤306`) are all
satisfied with equality, so the round was genuinely no-harm on depth:density — the claim cannot be
voided.

## Tool install/update record

None — `python3`, `git`, `sha256sum`, `wc`, `grep` already present; per RULES no install attempted.
