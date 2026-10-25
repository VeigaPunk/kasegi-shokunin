# round-5 aggregator audit — kasegi-shokunin

- **Round:** aggregator round-5 (steered 16:47:37), 2026-09-28. Audited state:
  round-5 commit `d87f2fa` (16:15:12); current-HEAD cross-checks noted
  separately (rounds 6–8 landed since; round-9 in flight untracked —
  `corpus/knowledge/submitted-registry.md`, `corpus/lessons/round-9.md`
  excluded from the verdict). Method: one read-only reviewer L2 (16 citations
  re-executed) + L1 adjudication of every major (each independently re-run).
- **Verdict (round-5 delta `d87f2fa`): NOT conformant** — 2 majors false at
  write time, 1 major carried from round-4 unrepaired, minors.

## Majors

1. **`.ufo-mission-report-bh*.md` census: "21" is 22 — false at write time.**
   `ls ~/Projects/bounties/.ufo-mission-report-bh*.md | wc -l` → **22**; every
   file's mtime ≤ 2026-09-14 17:38 (`stat -c '%y %n' …| sort | tail`) — the
   surface was frozen 14 days before `d87f2fa`, so this is not drift. The
   false count propagates (P-b sweep owed): `corpus/lessons/round-5.md:16`
   ("21 reports"), `SKILL.md:148` ("21 readiness audits"), round-5 report `:28`.
2. **"all BLOCKED" falsified by ≥2 counterexamples — the universal claim's own
   sweep refutes it.** `grep -l 'Outcome:.*READY' ~/Projects/bounties/.ufo-mission-report-bh*.md`
   → **2 files**: `bh557fda669b20.md` ("**Outcome:** READY — `node
   ops/claim-check.mjs claims/hackerone-superhuman/ingestion-20260914` → **OK**")
   and `bh0cb2eb6ca20b.md` ("Outcome: READY — 1 claimable finding");
   `grep -l 'Outcome:.*BLOCKED' …` → **9** of 22 (remaining files carry other
   outcome shapes). Both READY files mtime 2026-09-14 → falsified at write
   time. `SKILL.md:149` ("all BLOCKED") and the round-5 report share the
   defect; `SKILL.md:413` contradicts both ("22 … 21 BLOCKED, 1 READY:
   intigriti-yahoo" — total right, READY census still wrong vs the 2 observed)
   → SKILL.md is internally inconsistent within the same commit.
3. **Carried from round-4, open a fourth round: README has no
   `knowledge/program-quirks.md` row.** Filed in
   `corpus/lessons/round-4-aggregator-audit.md` (commit `7d1ce75`); still
   absent at `d87f2fa` and at current HEAD (`grep -c 'program-quirks' corpus/README.md`
   → 1, a prose Known-gaps mention, not an index row). An index row is a claim.

## Adjudicated false positive (recorded so the audit loop learns both ways)

- Reviewer major "ledger PLANNED 219 claimed vs 171 observed" — **REJECTED.**
  The reviewer's method was unsound: `grep -c '"transition":"PLANNED"' ledger/missions.jsonl`
  → 171 misses the 48 space-variant lines (`grep -c '"transition": "PLANNED"'`
  → 48; 171+48 = 219). Sound census: `jq -r '.transition // empty' ledger/missions.jsonl | sort | uniq -c`
  → **PLANNED 219** — the claimed value reproduces exactly (as do SCOPED 232,
  LEARNED 244; file mtime 2026-09-11 00:39, frozen). JSON censuses carry a
  `jq` command, never a raw grep on serialized shape.

## Verified reproducing (round-5 census craft, re-executed)

`fleets/missions/` 584 ✓ (`ls | wc -l`); `fleets/run/` 703 status files ✓;
PLANNED 219 / SCOPED 232 / LEARNED 244 ✓ (jq); credentials sweep ✓ (0 `op://`;
H1 report IDs + Bugcrowd receipt UUIDs are public platform receipts = evidence
pointers, not credential material); append-only ✓ (`round-1-aggregator-audit.md`
→ `d6b71c0` only; `round-4-aggregator-audit.md` → `7d1ce75` only; `git diff
d87f2fa HEAD -- LOG.md` has 0 deletions); LOG round-5 entry ✓ (5/5 named
pointers resolve); SHONEN.md ✓ verbatim mint seed (untouched, 4 unchecked —
but the round-5 report filed **no SHONEN assessment at all**, so the report is
disqualified as promotion evidence; substance required since round-1 text).

## Minors

4. **P-d repeat:** round-5 report cites "**Commit:** `round-5`" — no hash
   (`grep -oE '[0-9a-f]{7,}' .ufo/reports/round-5/kasegi.md` → empty). The
   commit is `d87f2faf51fcb8b0325068281cee94f22662aa03`. Root cause is
   fleet-side: the driver prompt template literally said `commit 'round-$n'`
   (ledger §11.3); the lane still owns the fix in its report text.
5. **P-c carry-over unmet:** round-4 defects 4 (Pendle presented as the
   `claim_review`/hard-gate exemplar — `SKILL.md:240,249,253-255` still assert
   a `claim_review` block; the real `claims/cantina-pendle/ingestion-20260915/status.json`
   has no `claim_review` key: `python3 -c "import json;print(sorted(json.load(open('…status.json')).keys()))"`)
   and 9 (autopsies 30 vs 31 — value silently corrected in round-6 corpus
   `d31f4ca`, no named forward-correction entry in any lane lesson:
   `grep -rn 'Pendle\|31 autopsy\|defect 4' corpus/lessons/round-{5,6,7,8,9}.md`
   → 0 hits). Both owed a correction entry next round.

## Falsification

Majors 1–2 re-check with their printed commands against the frozen
`~/Projects/bounties` surface (mtimes pinned above). Major 3 and minor 5 close
when the README row lands and a lesson names the corrections; the majors
themselves are append-only history and never rewrite.
