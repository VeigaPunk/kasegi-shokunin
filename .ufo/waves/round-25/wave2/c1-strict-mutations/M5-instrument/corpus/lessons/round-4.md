# Round-4 lessons

Round: 4 (2026-09-28). Evidence: `LOG.md` round-4 entry, commit `round-4`,
report `/home/vgpnk/projects/shokunin/.ufo/reports/round-4/kasegi.md`.

## What I closed

- **`evidence/` per-program store → `knowledge/evidence-dir.md`.** 592-dir
  census: `scope-snapshot.json` leads at 583; `raw/` 244, `history/` 154
  subdirs; `honest-zero/v1` schema read out of `bugcrowd-seek`. Established
  it is a separate tree from `claims/*/*/evidence/` — missions append
  freely, only the claim package is manifest-strict.
- **`ledger/*.jsonl` → `knowledge/mission-ledger.md`.** Transition census
  over 718 `missions.jsonl` lines: 260 missions, dominant path
  `SCOPED→PLANNED→LEARNED` (207). `appendLedger` is the sole writer with a
  3500-byte O_APPEND/PIPE_BUF cap; `gitMutationBlocker` fail-closes every
  git-mutating op on active rebase/merge or non-main HEAD. `candidates.jsonl`
  = `the-bounty-hunter` intake keyed by `b1k-NNN` run_ids (matching
  `evidence/<program>/b1k-NNN/` output dirs). Ops inventory table included.
- **`vgn-bounty-lab/` resolved trivially** — empty `git init`, zero commits.
  Worth confirming emptiness before scheduling a walk; the "gap" was a dir
  listing, not content.

## Friction

- `find -maxdepth 2` flat listing conflated nested dirs (`b1k-NNN` under
  programs) with program-level dirs — needed a parent-path reduction pass
  before counting. Census claims now cite depth explicitly.
- `telemetry.jsonl` has 3 unparseable lines out of 7218 (0.04%) — count
  tolerantly, don't let one bad line kill a census.

## Parked / open

- `george/` (49G comma.ai workspace): zero `claims/` references → parked as
  unlinked research substrate, not claim-corpus material.
- `fleets/registry.json` lane→model routing: still likely cross-domain
  (fleet mechanics), left for the aggregator to adjudicate.
