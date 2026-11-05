# Round-71 quarantine slice — per-row verdicts (attempt 2, hand-checked by L1 KasegiR71)

Slice re-derived this attempt (`assimilation/attempt2/quarantine-slice`, 7 rows, same rows as
attempt 1). Register read-only; register header and `## By lane` totals are stale, the slice is
derived from data rows only (`$2 ~ "`kasegi`" && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/`).
Lane registry state read from `corpus/SOURCES.md` at lane tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`.

Verdict vocabulary (CORPUS.md quarantine rule): `unverifiable` = the register's unchecked family
(prose class cell: source could not be fetched / payload absent). It is **not** fabrication; absent
payload is refused as a row, never adopted. `already-held` = the lane registry already carries the
id, and the id's own capture (where mined) is the lane's evidence, so nothing from the package is
appended and no duplicate row is created.

| row | S-id | register cell | lane registry state (file:line) | capture in lane | verdict |
|---|---|---|---|---|---|
| 1 | S037 | `payload-absent` | `corpus/SOURCES.md:43`, kind docs, tier A, status **mined**, opened 2026-10-25, recheck 180d, used-by `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` | `corpus/source-snapshots/round-25/S037.txt` | **already-held + unverifiable (payload absent in the staged package)** — no append; the lane's mined row and its capture stand unchanged |
| 2 | S054 | `payload-absent` | `corpus/SOURCES.md:60`, docs, tier A, **mined**, opened 2026-10-26, recheck 90d, used-by `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` | `corpus/source-snapshots/round-37/S054.txt` | **already-held + unverifiable (payload absent)** — no append |
| 3 | S048 | "cited source could not be fetched, so no quote was checked" | `corpus/SOURCES.md:54`, docs, tier A, **mined**, opened 2026-10-25, recheck 180d, used-by `corpus/knowledge/vendor-third-party-finding-coordination.md` | `corpus/source-snapshots/round-31/S048.txt` | **already-held + unverifiable (register's unchecked family; unreachable is not fabrication)** — no append |
| 4 | S065 | same prose class | `corpus/SOURCES.md:71`, spec, tier A, **rejected**, opened 2026-10-28, recheck on-release, used-by — | none | **already-held (rejected) + unverifiable** — the lane's rejection reason stands; nothing to adopt |
| 5 | S068 | same prose class | `corpus/SOURCES.md:74`, docs, tier B, **rejected**, opened 2026-10-28, recheck on-release, used-by — | none | **already-held (rejected) + unverifiable** — no append |
| 6 | S069 | same prose class | `corpus/SOURCES.md:75`, docs, tier A, **mined**, opened 2026-10-28, recheck 180d, used-by `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md` | `corpus/source-snapshots/round-44/S069.txt` | **already-held + unverifiable** — no append |
| 7 | S070 | same prose class | `corpus/SOURCES.md:76`, docs, tier C, **rejected**, opened 2026-10-28, recheck 180d, used-by — | none | **already-held (rejected) + unverifiable** — no append |

Result: **0 rows adopted, 0 rows refused as fabrication, 7 rows unverifiable, 7 rows already held.**
No register or campaign file was edited. Mass id drift is measured independently: at this attempt the
lane holds 106 registry ids and the staged package 94, with **76 colliding ids**
(`assimilation/attempt2/collisions`), so adoption stays closed this round and the L0 question filed in
round 70 remains the routing item.
