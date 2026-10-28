
## Round 46 evidence

Draft notes, one per `SHONEN.md` box (all four boxes are `[~]` at base; this seat writes no `[x]`, which is operator-owned per `corpus/lessons/round-45-verifier-spotcheck.md` §7). Each note states the evidence present at base and freeze and what would make the box `[x]`.

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence (round 46, freeze `9f23aab`): `SKILL.md` is not among the round-46 claim paths; `density.py` is not a round-46 claim surface. `[[FILL-BY-L1: SKILL.md base→tip byte diff and density.py sha256 at tip]]`. Would become `[x]`: a non-author check of the SKILL.md decision tables and cited sources, plus the density instrument reading above the frozen bar at the tip; neither is run in this seat.

- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence (round 46): none. The round is documentation-only (`claims.json` "Live-target testing is refused"); the closest work is the S073 capture (`corpus/source-snapshots/round-46/S073.txt`, sha256 `66c96a61…1930`, `source-recheck.py` `S073:sha256 OK`, `S073:Q1-Q8 OK`). Would become `[x]`: an executed domain task that the operator authorizes; none is authorized in this round. Stays `[~]`.

- [~] Instructions executable by an agent without oral context
      — evidence (round 46): `r46-c1-gate.py` and `r46-c2-gate.py` run from a `git archive 9f23aab` export and print `c1-gate fixed=1/7 exit=1` and `c2-gate fixed=2/7 exit=1` at freeze (do-nothing control reproduced byte-identically at base). `[[FILL-BY-L1: tip counter values]]`. Would become `[x]`: `c1-gate fixed=7/7 exit=0` and `c2-gate fixed=7/7 exit=0` at the tip, re-run by a non-author from a clean export, plus the counters' selftests green.

- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence (round 46): `[[FILL-BY-L1: PROVINCE.md base→tip byte diff; sibling sweep for "private vulnerability reporting" overlap for F28 with any sibling lane entry]]`. The round-46 C2 entry (F28, GitHub private vulnerability reporting) is a new topic; a sibling overlap, if any, is an L0 scope ruling, not an in-lane decision. Would become `[x]`: operator-owned; needs the sibling sweep printed with its command and an L0 ruling for any overlap found.
