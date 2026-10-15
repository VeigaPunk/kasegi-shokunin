# round-20 re-census — instruments re-derive their roots; both domain roots still lost

2026-10-14. Steered round 20. Advisory inventories:
`../.ufo/waves/shokunin12h-20261014-p1-repair/members/Kasegi*.md`.

## Verdict lines (measured)

- `python3 corpus/instruments/anchorcheck.py SKILL.md` → exit 0,
  `7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / OUTSIDE-BASE=0 /
  BASE-ABSENT=0`.
- `python3 corpus/instruments/density.py SKILL.md --label r20-recensus` → exit 0,
  `645` path-citation instances across 18 blocks.
- `python3 corpus/instruments/resolve.py .` → exit 0, regenerated
  `citation-survival.tsv` / `citation-survival.md`.

## No gate change

Both instruments already DERIVE their roots
(`$KASEGI_MIRROR`/`$KASEGI_ORIGIN_ROOT` → first existing candidate → canonical
absent), and explicit bad overrides stay bad. `$UFO_SRC` is not a real consumer
here: the anchor regex does not match `~/Projects/ufo-fsd-alpha/`.

## Named debt (append-only, not repaired in place)

- `TRIAGE-LOST-BASE-MISPREFIX`, `CLAIM-CHECK-96-MIRROR-MISBASE`,
  `BLOB-PIN-LOWERCASE-PATH`, `CENSUS-NOTE-NEVER-LANDED`, `UFO-DOT-LISTING-DRIFT`,
  `UFO-HISTORY-NOT-INTACT` — plus the standing `RECEIPT-STORE-LOST`,
  `MIRROR-SOURCE-LOST`, `ORIGIN-REPO-LOST`.
- The 50-file-deletion sentence does not reproduce: reachable history is an
  orphan 3-commit line rooted at `72ab84a8`; cross-history `--diff-filter=D` is
  970. Do not adopt 50.
- Scorecard corpus/lane rates (`116/1142`, `132/1469`) do not match the
  regenerated census (`116/1144`, `132/1471`).
- A suffix-join onto the derived override roots is the one narrow
  root-default change available; left unlanded by decision, named here.
