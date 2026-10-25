# round-4 aggregator corpus audit — kasegi

- **Round:** aggregator round-4 (steered; `.ufo/state/aggregator.round`=4), 2026-09-28.
- **Author:** aggregator lane (L1 m_qwen + one L2 `reviewer` subagent; non-author
  of the audited entries). Corrections are this new entry — no lane file edited.
- **Scope:** round-4 delta at commits `d6b71c0` + `0bde2e0`:
  `knowledge/mission-ledger.md`, `knowledge/evidence-dir.md`,
  `lessons/round-4.md`, `README.md`. Round-5+ commits (`d87f2fa`…`4ff0296`)
  excluded from the verdict.
- **Method:** 18 citations independently re-executed against
  `~/Projects/bounties` per `CORPUS.md`.

**Verdict: NOT CONFORMANT** — two major rule failures (negative-without-sweep,
missing index row). All 18 numeric claims reproduced exactly; the failures are
formal-rule, not accuracy.

## What reproduced (18/18 numeric claims)

718 lines / 260 mission_ids / 218 programs (`wc -l ledger/missions.jsonl`;
python set-count over `mission_id`, `program|program_id`); SCOPED→PLANNED→LEARNED
×207 (exact-sequence count); SUBMITTED ×3 = mozilla-security-bounties,
hackerone-spotify, hackerone-airtable (`jq -r 'select(.transition=="SUBMITTED") | .program'`);
telemetry 7218 lines / dispatcher_tick 3680 / 3 unparseable (git conflict
markers — tolerant JSON parse); mission_parked 1188 / lease_claimed 107 /
attempt_reset 68 (naive grep under-counts parked at 1164 — the entry's tolerant
parse is the correct method); `appendLedger` 3500-byte cap at `ops/shared.mjs:55`
+ `gitMutationBlocker` at `:36-47` (`rg -n '3500|appendLedger|gitMutationBlocker'`);
14 `ops/*.mjs` tools; candidates.jsonl 8 records, run_ids
b1k-{060,082,128,165,209,212,248,253}; first board_imported `counts.written`=1087;
evidence/ 592 program dirs, scope-snapshot 583, raw/ 244, history/ 154,
custodian/ 27, honest-zero-record 346, status.json 275 (`find` min/maxdepth per
the entry's cited depth rule); vgn-bounty-lab 0 commits / 0 non-.git files
(`git rev-list --count --all`; `find … ! -path '*/.git/*' | wc -l`).

## Major defects

1. **Negative claim without its sweep** (`evidence-dir.md`): "`george/` has zero
   `claims/` references" cites no search command. Re-run:
   `rg -l 'george' ~/Projects/bounties/claims/ | wc -l` → 0 — claim true,
   evidence absent. CORPUS.md: *a negative claim carries its sweep*.
2. **Missing index row** (`README.md`): coverage map has no row for
   `knowledge/program-quirks.md` (on disk since round-1; only prose-mentioned in
   gaps). Command: `comm -23 <(ls corpus/knowledge/*.md | xargs -n1 basename | sort) <(grep -oE 'knowledge/[^\`]+\.md' corpus/README.md | xargs -n1 basename | sort -u)`.
   CORPUS.md: *an index row is a claim* — every disk file earns a row.

## Minor defects

- `mission-ledger.md`: no count carries the required `<n> — <command> <date>`
  form; date-only header ("Counted 2026-09-28"). Numbers reproduce, rule form
  violated (`rg -n ' — ' corpus/knowledge/mission-ledger.md` → no count rows).
- `evidence-dir.md`: "b1k-NNN under ~30 program dirs" — observed **33**
  (`find ~/Projects/bounties/evidence -mindepth 2 -maxdepth 2 -type d -name 'b1k-*' | wc -l`).
- `mission-ledger.md`: "one line per transition" — 8 of 718 lines lack
  `.transition` (park/scope event shapes).

## Prior-audit defect status (refresh of AGGREGATE §9.1)

- Defect 8 ("275 claim packages"): **closed as documented conflation** — the
  count reproduces from the wrong store (`find evidence -maxdepth 2 -name
  status.json | wc -l` = 275); round-4's `evidence-dir.md` separates the two
  stores correctly and the lesson names the depth trap.
- Defects 4 (Pendle `claim_review` attribution) and 9 (31 autopsies): round-4
  report silent — **still open**.

## Gaps filed for next lane round

1. Repair both major defects (sweep command on the george row; program-quirks
   index row) in lane-owned files.
2. Attach per-count commands to the mission-ledger and evidence-dir tables.
3. Defects 4/9 from the round-1 audit remain unrepaired.
