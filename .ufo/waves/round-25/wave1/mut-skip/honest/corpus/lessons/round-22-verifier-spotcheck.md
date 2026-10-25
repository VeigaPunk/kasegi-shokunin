# round-22 — non-author verification and spot-check (orchestrator, kaika)

Written by the integrator, not the lane (CORPUS.md: corrections and outside reviews are new
files; the lane owns `round-22.md`). Verifiers were fresh agents dispatched by the orchestrator
after the round landed at `c8b719d22`; full reports are committed in the fleet repo at
`.ufo/waves/kaika-w3/kasegi-review.md` and `kasegi-critic.md`.

## Spot-check (LEARNING.md — at least one admit and one reject)

| decision | sample | verifier | result |
|---|---|---|---|
| admit | 3 admits sampled (CVSS v4, disclosure timelines, safe-harbor-vs-scope entries) — reviewer re-opened 14 rows incl. tier-A; quotes match except S006's Gate location; 3/3 agree | W3ReviewKasegi | agree |
| reject | 2 rejects sampled (S026 rejection holds — its sweep should name the linked PDF; second tier-C rejection) — 2/2 agree | W3ReviewKasegi | agree |

## Adjudication

REJECTED-HONEST-STOP: C1's declared axis depth:verifiability is defined by `resolve.py`/`anchorcheck.py` (SCORECARD.md:33-38); both are unchanged and the score held at 4, so the claim does not move its axis — the header-trio backfill (0/25→25/25) and 31 stale lines marked historical are real provenance/freshness work, landed but not credited. C2 verified: coverage improved (5 frontier entries admitted; map rows 25→33; PROVINCE Core/Frontier/Adjacent) and capability `sources-registry` admitted (27 rows, census ok). Trends: expansion improved; quality unchanged (23/25 legacy rechecks exit 1 — their bases are gone); discernment improved (5/5 spot-check agree). Corrections owed next round: M1 placeholder row replaced, M2 new entries' rechecks are prose (exit 2), M3/M4 stale lesson pointers and deletion count (22 vs 32), M5 S006 Gate location.
