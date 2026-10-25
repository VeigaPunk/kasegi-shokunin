# Round 29 — registry review (RevC2Registry)

Scope: `corpus/SOURCES.md` additions S043–S045, registry-change log, and C2 registry checks. Read the frozen claims, SCORECARD, QUALITY (Q1–Q10/R1–R14), SOURCES contract-v1, corpus map, round-28 lesson and verifier spot-check, proposal file, read-only merge package, instrument guidance, and `sources-census.sh` validation rules.

## Re-derived results

- **Registry rows: 45.** Direct parse of the registry table: 45 ids, sequential S001–S045; no duplicate ids. Every row has 13 pipe-delimited fields (`awk -F'|'` convention); malformed rows: **0**.
- **Enums / tier inflation: 0.** Kinds are within the existing `docs|spec|dataset|paper|community|own-work` set, tiers within A/B/C, statuses within queued/mined/rejected. Counts: A=42, B=1, C=2; S043/S044/S045 are each tier A. No invalid enum or added tier.
- **Mined used-by targets:** all mined rows' comma-separated used-by paths exist on disk (**0 missing**).
- **F13 pointer:** each of S043/S044/S045 has used-by exactly `corpus/knowledge/program-severity-ladders-and-reward-scales.md`; it is the sole knowledge file whose `source:` headers cite any of S043–S045. The three rows are the only additions after S042 in the current registry.
- **Row contents:** no embedded literal `|` in any source-row cell. Every recheck cell is a date, cadence (`90d`, etc.), or symbolic cadence (`on-release`/`annual`); no prose recheck cell.
- **Change log:** read-only diff against requested base `7a6591c1eb8a14f427297980a96fa8bb339f29ee` shows SOURCES changes are only the three appended rows and four appended registry-log bullets. Each S043/S044/S045 row addition and its staged-to-landed opened-date/anchor/used-by changes are described in its own bullet; the final bullet records S041/S042 unchanged and the 42→45 count. No existing-row edits are absent from the log in this diff. Prior S040/S041 changes remain documented in the pre-existing log.
- **Frozen census command, post-append:** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `kasegi ok .../corpus/SOURCES.md`, `census_exit=0`. It emits the known W04 duplicate-URL-across-scopes warnings for S028/S029; these are warnings, not validation failures.

Evidence: structural checks run against the current `corpus/SOURCES.md`; direct tree existence checks; knowledge-header search; and `GIT_OPTIONAL_LOCKS=0 git --no-optional-locks diff --no-ext-diff --unified=0 <base> -- corpus/SOURCES.md` (additions-only diff). The raw `SOURCES.md` contains the exact rows and appended log bullets noted above. No repository modifications were made by this review except this report.

LSP was unavailable among this session's mounted tools; no LSP semantic result is claimed. The checks above are direct file/structure and path-existence evidence. No build, tests, or instrument runs beyond the requested census were needed for this scoped review.

## Verdict

No actionable defect found in the assigned registry rows/change log checks. C2's requested registry and census predicates are re-derived as passing; census exit 0 includes the disclosed W04 warnings.
