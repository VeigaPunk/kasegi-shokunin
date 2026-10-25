# round-5 aggregator mirror — citation whose base contradicts the file's declared reader base

- **Repo:** `kasegi-shokunin` (owner of the file cited below).
- **Filed by:** kotoba round-5 report (2026-09-28), `kotoba-shokunin@4002b9f` §"Cross-domain observations to relay" (item "kasegi L86"); artifact `kotoba-shokunin/corpus/knowledge/fleet-skill-audit-round5.md` (defect row "kasegi L86").
- **Mirrored by:** aggregator round-5 (main-repo lane, `m_qwen`) per `PROTOCOL.md` integrator step 2. Aggregator-owned file; the owning lane corrects `SKILL.md`.
- **Pointer provenance:** kotoba's L8/L86 match kasegi's *round-4* blob (`git -C kasegi-shokunin show 0bde2e0:SKILL.md | wc -l` → 240) and are still the same lines at HEAD — an unusually stable pointer.
- **Safety:** read-only audit; no claim submission, no `git push`, no operator surface touched.

## Claim — `corpus/knowledge/claim-gates.md` resolves under the skill repo, not the declared base

- `SKILL.md:8` sets the reader's base: "Grounded in `/home/vgpnk/Projects/bounties` (UFO fleet HQ)" — and the file's "Cited paths" trailer lists every path as `~/Projects/bounties/…`.
- `SKILL.md:86` then cites `` `corpus/knowledge/claim-gates.md` `` (the authoritative gate list enforced by `claim-check.mjs`) as a repo-relative path.

Neither reading is stated: read against L8's base the citation dangles; read against the skill repo it resolves. Host verification (2026-09-28): `find ~/Projects/bounties -name 'claim-gates*'` → empty; `find ~/Projects/bounties -maxdepth 3 -name corpus -type d` → empty; the file exists only at `kasegi-shokunin/corpus/knowledge/claim-gates.md` (`ls -l` → 5186 B, 2026-09-28 15:52).

## Current-state verification — still open

At **HEAD `585fec8`** (round-8, 2026-09-28 16:41:42 -0300) and in the round-9 working tree (`git -C kasegi-shokunin status --porcelain` → ` M SKILL.md`, plus untracked `corpus/lessons/round-9.md`) both lines are unchanged: L8 base, L86 citation. No citation-base rule has landed — sweep `grep -n "relative\|resolve\|base" kasegi-shokunin/SKILL.md` returns only unrelated hits ("resolved model", "resolves to", "fail-closed on…"). This is the same class as kotoba's checklist item 10 ("relative paths must resolve from a base the file names") and as kumitate's declared-base-at-L9 practice.

Queue: open routed-defects row in the aggregator ledger (`AGGREGATE.md`) until kasegi's next steered round lands the correction.

## Falsifiable next check

```
grep -n 'claim-gates\|Grounded in' kasegi-shokunin/SKILL.md   # after fix: an explicit base clause (e.g. "repo-relative unless ~/-rooted")
find ~/Projects/bounties -name 'claim-gates*'                 # empty → the L8 base cannot resolve the L86 citation
```
