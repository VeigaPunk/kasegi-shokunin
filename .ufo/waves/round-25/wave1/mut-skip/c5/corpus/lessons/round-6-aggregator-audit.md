# kasegi-shokunin — round 6 aggregator audit

Provenance: auditor = aggregator L1 non-author review, 2026-09-28 (probes
21:2x–21:3x UTC). Repo HEAD `fb9ac8e` (round-11); all round-12 work
uncommitted. Pinned: `SCORECARD.md` 18:26:25 -03 `14ceb62e…`, `SKILL.md`
18:22:29 `6d1dce1e…`, `LOG.md` 18:21:01 `af495a5a…`, `corpus/README.md`
18:22:29 `efe8c205…`. Evidence commands are re-runnable against
`/home/vgpnk/Projects/bounties`.

Anchor revision: main-repo `PROTOCOL.md`/`ROADMAP.md` were being edited by the live
protocol lane during this audit (`wc -l PROTOCOL.md` 387 → 576; `sha256sum` →
`9e700d691307…`). Their line numbers below are soft — the quoted clause text is the
durable pointer.

## Verdict

**NOT CONFORMANT.** Failed rules:

- **4** (counts carry their command) — `corpus/knowledge/mission-ledger.md`
  count tables carry no `<n> — <command> <date>`; `SCORECARD.md:23` counts
  carry none.
- **5** (negatives carry their sweep) — `corpus/knowledge/evidence-dir.md:78`
  "`george/` … Zero claims dirs reference it" cites no search command.
- **7** (index row = claim / index-vs-disk) — `corpus/README.md` coverage map
  has no row for `knowledge/program-quirks.md`, which exists on disk; the
  `README.md:30` lessons range implies a non-existent `lessons/round-2.md`.
- **9** (corrections are new entries, never rewrites) — *contested*:
  `corpus/README.md:82` declares the r12 repairs were made "in place".
- Falsified pointers/counts uncorrected after routing (rules 1/6 in effect).

Clean: **rule 8** (credential sweep clean — the single `op://` hit is a literal
string inside a prior sweep's description); SHONEN seed byte-identical; no
`[x]` marks without verifier.

## Re-executed citations

claim (file:line) | command | observed | pass/fail

- `SKILL.md:8` 274 dirs / 295 pkgs / 280 gated | `ls -d claims/*/ \| wc -l`; `ls -d claims/*/*/ \| wc -l`; `ls -d claims/*/*/status.json \| wc -l` | 274 / 295 / 280 | PASS
- `SKILL.md:459` + `submitted-registry.md:195` histogram 248/15/15/2 | `python3` tally of `state` over `claims/*/*/status.json` | PARKED 248, DONE 15, BLOCKED 15, SUBMITTED 2 | PASS
- `README.md:23` 20 `claim-*` report.json | `ls -d fleets/ufo-archive-2026/missions/claim-*/ \| wc -l` | 20 (and 20 report.json) | PASS
- `ufo-archive-2026.md:11` "19 hardening missions" (same file `:5` = 20) | (same) | 20 | **FAIL**
- `ufo-archive-2026.md:36` "16 per-program L0 mission briefs" | `ls fleets/ufo-archive-2026/inquiries/bounty-fleet-2026-09-06/` | 15 per-program + farmscout + feeder (+dispatch.log) | **FAIL**
- `submitted-registry.md:17-19` only mozilla has `submit/receipt.md` | `find claims -name receipt.md` | 1 — mozilla only | PASS
- `SKILL.md:188,529` 22 bh audits (20 BLOCKED / 2 READY) | `ls .ufo-mission-report-bh*.md \| wc -l`; `grep -hoE 'Outcome:[^A-Za-z]*[A-Z]+'` | 22; 2 READY (bh557fda669b20, bh0cb2eb6ca20b) | PASS
- `SKILL.md:314,518` 31 autopsies | `ls docs/autopsies/*.md \| wc -l` | 31 | PASS
- `README.md:19` 592 evidence dirs | `ls -d evidence/*/ \| wc -l` | 592 | PASS
- `SKILL.md:10` 1088 map records; 486 verdict lines (430/50/6) | `ls bounty-map/programs/*.json \| wc -l`; `wc -l docs/review-verdicts.jsonl` | 1088; 486 (430/50/6) | PASS
- `mission-control.md` 703 status files / 584 missions | `ls fleets/run/*.status.json \| wc -l`; `ls fleets/missions/*.md \| wc -l` | 703; 584 | PASS
- `repo-git-state.md:15` 903 dirty / 198 tracked vs 3361 disk | `git status --porcelain \| wc -l`; `git ls-files claims \| wc -l`; `find claims -type f \| wc -l` | 903; 198; 3361 | PASS
- `repo-git-state.md` stalled rebase; `.ufo/missions/` never existed | `git status` (bounties); `ls .ufo/missions` | rebase in progress, HEAD `58acb6d8`; dir absent | PASS
- `target-checkouts.md:8` pendle `f242659…`=v6.10.0 | `git -C pendle-core-v2-public log -1 --format=%H` | `f24265966bb5…` (grafted) | PASS
- `SCORECARD.md` 25 `bh*` workspaces | `ls -d .ufo/bh*/ \| wc -l`; `ls -d .ufo/bounty-fleet/sessions/bh*/ \| wc -l` | 19 + 6 = 25 | PASS
- `evidence-dir.md:56` "b1k-NNN under ~30 dirs" | `find evidence -mindepth 2 -maxdepth 2 -type d -name 'b1k-*' \| wc -l` | 33 | **FAIL (minor)**
- `mission-ledger.md:19` "One line per transition" | `python3` over `ledger/missions.jsonl` | 8/718 lines lack `transition` (7,11,13,18,19,20,45,385) | **FAIL (minor)**
- `SCORECARD.md:23` "19 `corpus/knowledge/` entries" | `ls corpus/knowledge/*.md \| wc -l` | 20 | **FAIL (minor)**

## Defects

1. **MAJOR — falsified "19" archive-mission count, four sites.**
   Standing claim: `corpus/knowledge/ufo-archive-2026.md:11` "19 hardening
   missions", `SKILL.md:385` "19 L1 hardening missions",
   `corpus/lessons/round-8.md:10` "19 `missions/claim-*/report.json`",
   `corpus/README.md:49` "19-mission defect taxonomy".
   Command: `ls -d fleets/ufo-archive-2026/missions/claim-*/ | wc -l` → **20**;
   `find …/claim-*/ -maxdepth 1 -name report.json | wc -l` → **20**.
   `ufo-archive-2026.md:5` and `README.md:23` already say 20 — the same files
   contradict themselves. Correction form: **appended correction entry** (never
   rewrite history); owning lane: kasegi.
2. **MAJOR — falsified L0-brief count.**
   `corpus/knowledge/ufo-archive-2026.md:36` "16 per-program L0 mission briefs".
   Command: `ls fleets/ufo-archive-2026/inquiries/bounty-fleet-2026-09-06/` →
   15 per-program briefs + `farmscout-hidden.md` + `feeder01-sources.md` +
   `dispatch.log` (18 entries). Owned: kasegi.
3. **MAJOR — Pendle `claim_review` attribution falsified (routed round-1/4).**
   `SKILL.md:323` names `claims/cantina-pendle/ingestion-20260915/` as the
   verification base for the six-file contract table whose last row asserts a
   `status.json` "`claim_review` block with hard_gates + subchecks".
   Command: `python3 -c "import json;print('claim_review' in
   json.load(open('claims/cantina-pendle/ingestion-20260915/status.json')))"` →
   **False** (only a prose mention inside `resume_condition`). The block exists
   on `claims/bugcrowd-seek/honest-zero/status.json`. Owned: kasegi.
4. **MAJOR — index-vs-disk: `program-quirks.md` has no row (routed round-4).**
   `corpus/README.md` coverage map rows (19) vs `corpus/knowledge/*.md` (20);
   `comm -13` → `knowledge/program-quirks.md`. Owned: kasegi.
5. **MAJOR — negative claim without its sweep (routed round-4).**
   `corpus/knowledge/evidence-dir.md:78` ("Zero claims dirs reference it").
   Command: `grep -rl 'george' claims/ | wc -l` → 0; the sweep appears only in
   the aggregator's own lesson, not in the lane's file. Owned: kasegi.
6. **MAJOR — SCORECARD not landed; `/tmp`-only depth evidence.**
   `git -C kasegi-shokunin ls-files SCORECARD.md | wc -l` → **0** (untracked);
   `git rev-parse round-12` → fatal (HEAD is `fb9ac8e`). Depth-axis evidence
   pointer = `/tmp/kasegi-r12/reviewer.md`; `PROTOCOL.md:394` forbids tmpfs
   paths as durable evidence. Owned: kasegi (commit + durable pointer).
7. **MAJOR — stale falsified counts in lesson files.**
   `corpus/lessons/round-5.md:16` "21 reports, every verdict BLOCKED" (live 22,
   20 BLOCKED / 2 READY) and `corpus/lessons/round-9.md:33` histogram
   "…BLOCKED 16…OPERATOR_GATED 1" = **282** (live 280, BLOCKED 15). The r12
   repairs landed in SKILL.md/corpus but not in these lessons. Owned: kasegi.
8. **MINOR — cited-base contradiction still open (routed round-5 mirror).**
   `SKILL.md:8` sets the base to `/home/vgpnk/Projects/bounties`;
   `SKILL.md:86` cites `corpus/knowledge/claim-gates.md` repo-relative with no
   base clause (`grep -n "repo-relative" SKILL.md` → none). Owned: kasegi.
9. **MINOR — b1k "~30 dirs"** (`evidence-dir.md:56`) vs 33; **"one line per
   transition"** (`mission-ledger.md:19`) vs 8/718; mission-ledger counts lack
   the commanded form; `SCORECARD.md:23` "19 entries" vs 20; `README.md:30`
   range implies missing `lessons/round-2.md`. Owned: kasegi.
10. **MINOR — lane-report form.** `grep -rLE '^#{1,6} *SHONEN'
    .ufo/reports/round-*/kasegi.md` → r1/r3/r4/r5/r7/r8/r9/r10/r11/r12 lack the
    heading (only round-6 has one) → those checklist assessments are
    author-asserted, disqualified as promotion evidence. Owned: kasegi.
11. **MINOR — commit identity.** `git config --local user.name` unset; 11
    commits by `Joao Pedro Veiga <jpveigao10@gmail.com>`, 4 by `shokunin
    <shokunin@local>`; none use `kasegi-shokunin`/`kasegi@shokunin.local`.
    Owned: operator/lane.

## Fleet-2 axis-framework state

- `SCORECARD.md` exists on disk, **untracked**; contract fields axes/planned/
  retired all present; declared axes `depth`+`coverage` match `MISSION.md:13`;
  before→after for r12 recorded (coverage 7→9; depth 8→8).
- Gaps: not committed; `depth` evidence pointer is a `/tmp` path (forbidden);
  "19 knowledge entries" stale (live 20); "18 sections" uncommanded count.
- Round-12 report (`.ufo/reports/round-12/kasegi.md`, appeared 18:25:59 -03
  mid-audit) claims ``Commit `round-12` `` — unresolvable.

## Routed-defect rows for the ledger

```
kasegi-shokunin | archive "19 hardening missions/report.json" (ufo-archive-2026.md:11, SKILL.md:385, lessons/round-8.md:10, README.md:49; live 20) | r9 | open | ls -d fleets/ufo-archive-2026/missions/claim-*/ | wc -l
kasegi-shokunin | "16 per-program L0 mission briefs" (ufo-archive-2026.md:36; live 15) | r9 | open | ls fleets/ufo-archive-2026/inquiries/bounty-fleet-2026-09-06/
kasegi-shokunin | Pendle claim_review attribution (SKILL.md:323) | r1/r4 | open | python3 -c "import json;print('claim_review' in json.load(open('claims/cantina-pendle/ingestion-20260915/status.json')))"
kasegi-shokunin | README row missing for knowledge/program-quirks.md | r4 | open | comm -13 <(grep -oP 'knowledge/[a-z0-9-]+\.md' corpus/README.md|sort -u) <(ls corpus/knowledge/*.md|sed 's|^corpus/||'|sort)
kasegi-shokunin | george row negative without sweep (evidence-dir.md:78) | r4 | open | grep -rl 'george' claims/ | wc -l
kasegi-shokunin | SCORECARD.md uncommitted + /tmp-only depth evidence | r12 | open | git -C kasegi-shokunin ls-files SCORECARD.md | wc -l
kasegi-shokunin | lessons/round-5.md:16 "21/all-BLOCKED"; lessons/round-9.md:33 histogram 282 | r9 | open | ls .ufo-mission-report-bh*.md | wc -l ; ls -d claims/*/*/status.json | wc -l
kasegi-shokunin | SKILL.md citation base contradiction (:8 vs :86) | r5 | open | grep -n 'repo-relative' SKILL.md
kasegi-shokunin | evidence-dir.md:56 b1k "~30" vs 33; mission-ledger.md:19 universal transition claim | r4 | open | find evidence -mindepth 2 -maxdepth 2 -type d -name 'b1k-*' | wc -l
kasegi-shokunin | 10 lane reports lack SHONEN heading (r1/r3/r4/r5/r7/r8/r9/r10/r11/r12) | r9 | open | grep -rLE '^#{1,6} *SHONEN' .ufo/reports/round-*/kasegi.md
kasegi-shokunin | commit identity: operator personal + shokunin@local, no lane identity | r6 | open | git -C kasegi-shokunin config --local user.name
```

No credential material appears anywhere in this draft.