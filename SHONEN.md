# kasegi-shokunin — Promotion checklist

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources
      — evidence: `corpus/instruments/density.py SKILL.md` mean 154.0, 652 path-citation
      instances, 19 blocks; `anchorcheck.py SKILL.md` bad=0 (round-25 receipts in
      `.ufo/waves/round-25/wave1/ScoutNoHarm.md`). `SKILL.md` bytes untouched by round 25.
- [~] At least one end-to-end domain task executed and logged in LOG.md
      — evidence: LOG.md round-25 entry; round report `.ufo/reports/round-25/kasegi.md`;
      both claims land with measured before→after receipts.
- [~] Instructions executable by an agent without oral context
      — evidence: every `corpus/knowledge/*.md` `recheck:` line is one cwd-independent command;
      `recheck-audit.py` exits 0 with `executes=14 gated=23 broken=0` (`c1-receipt-index.txt`);
      `frontier-recheck-count.py` entries=12 pass=12 exit=0.
- [~] No cross-domain bleed (PROVINCE.md still accurate)
      — evidence: PROVINCE.md frontier F01–F10; connector seat found no sibling lane holds the
      F10 ground (chousa cedes bounty-program scope; kake refuses disclosure timing), adjacency
      reported, nothing absorbed.
