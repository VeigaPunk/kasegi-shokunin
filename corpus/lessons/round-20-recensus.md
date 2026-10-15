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

## Independent audit erratum (appended 2026-10-14)

Independent audit: all three instruments re-ran exit 0 with matching counters; the census was regenerated after the round-20 lesson entered the walk (census now matches the tree). Identity/pathspec/record confirmed. Dead-path sweep found **22 live lines** at the round commit (`citation-bases.md:72` + `triage-thresholds.md:12` lowercase `~/projects` `git -C`; `submitted-registry.md` ×12 calling `~/Projects/origin-work/open-bug-bounties` a LIVE corpus; `intake-and-finalize.md`, `ops-invariants.md`, `operator-queue.md` how-tos into the absent root; `SCORECARD.md:174` still calling the origin-work package surviving) — named debt, owner kasegi, unblock: mark those lines lost-base or historical. Six deleted-path classes have zero citations.

### Audit detail (appended 2026-10-14)

Historical-marking audit (`.ufo/waves/shokunin12h-20261014-p1-audit/members/KasegiHistoricalMarking.md`): describe-don't-pin does not hold for several living pins — stale census rates at `SCORECARD.md:134`/`LOG.md:812` and `instruments/README.md:16-17`; `$UFO_SRC` still claimed at `root-loss-2026-10-12.md:55`/`SCORECARD.md:164` though no instrument reads it; `citation-bases.md:16,:29,:41,:105` point at lines that no longer hold those rules; `root-loss-2026-10-12.md:15` "history intact" false (3-commit orphan); the exclusive `.ufo/` list has gained `contract-sync`/`rs-self-iter-blocked.json`; `:29-30` still states 50 deletions; `citation-bases.md:43-44` cites a note never committed; lost-tree line numbers marked as mirror lines at `triage-thresholds.md:21,:52-438` and `claim-package-contract.md:19-22`; missing-file content hashes asserted as current identity at `submitted-registry.md:108-109`, `SKILL.md:321,:477,:816-820`, `ev-model.md:8-10`; `repo-git-state.md:7,:15,:21` still call the absent bounties repo an ACTIVE hazard with a 903-entry count. Do not mark `964f443e` or the 600-line ufo `SKILL.md` superseded — both still true.
