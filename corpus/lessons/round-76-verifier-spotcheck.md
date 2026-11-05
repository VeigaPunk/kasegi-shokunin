# kasegi round-76 verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi 76 (attempt 2). Report `.ufo/reports/round-76/kasegi.md` (fleet commit
`894dab3025684d29337dcee5d5d10061ecd5876e`); lane landing `2c3345a1336cbb9e9ad332288457de5fc3fb9fae`;
freeze `5da54cd4451cbbb9e4b87e2f83475feb13c65c9e`; base `a788021675873a96e09e91aa033d8c26ac2fe212`.
This verifier authored no part of the round and ran only read-only re-checks plus the closure writes.

## 1. Conformance (step 1)

- Report identity: `git log --format='%an %H' -- .ufo/reports/round-76/kasegi.md` →
  `kasegi-shokunin 894dab3025684d29337dcee5d5d10061ecd5876e`. Lane identity ✓.
- `SHONEN` heading: `grep -c '^## SHONEN'` = 1; 4 lines for the 4 SHONEN.md boxes ([~],[ ],[~],[~]). ✓
- Cited commits exist and are ancestors of the branch ref (jj-colocated; tested against `master`, not `@{u}`):
  `git merge-base --is-ancestor 2c3345a1… master` → YES; `5da54cd4…` → YES; base `a7880216…` → YES.
- Pushed and clean: `jj-lane.sh state` → `branch=master local=2c3345a1… remote=2c3345a1… ahead=0 behind=0`;
  `git status --porcelain` empty; `git ls-remote origin refs/heads/master` = `2c3345a1…`. No uncommitted
  round work; attempt-1 leftovers disposed of by the reverts the report names (verified below).
- Dispatched prompt `.ufo/prompts/kasegi-round-76.md` (95,032 B) carries the full template contract:
  §1 MISSION/AXES binding, §2 claims 1–3 each falsifiable, §2b frontier step, §3 L2 floor (≥8 in ONE
  batched call — matches current `MISSION.md` §L2 concurrency "at least 8"), §4 report path
  (`.ufo/reports/round-76/kasegi.md`) with required sections, SHONEN-heading rule and commit-hash
  citation rule, §5 commit-then-push ordering, push scope, L0 side channel, §6 hyaku addendum. No L2
  route map is quoted in the prompt, so the bucket-match check is vacuous.
- Watchdog digest (copied verbatim from `.ufo/watchdog.log`):
  - `2026-11-05T07:34:13-03:00 launch kasegi round=76 pgid=128264 driver=hyaku-inline attempt=1`
  - `2026-11-05T08:12:11-03:00 lane-dead-no-report kasegi round=76; retry same round (attempt=1: report missing/unchanged/no SHONEN/<400B)`
  - `2026-11-05T08:12:13-03:00 launch kasegi round=76 pgid=3984440 driver=hyaku-inline attempt=2`
  - `2026-11-05T08:59:25-03:00 complete kasegi round=76; hyaku-inline attempt=2`
- Report is a real report, not a marker: work performed, evidence pointers, landed changes tied to
  LOG.md (round-76 entry at `LOG.md:2813` naming freeze/base hashes), checkable hashes throughout.
- L0 lines: both open items present in `.ufo/l0-questions.md` (`kasegi | round-76` Q01-manifest and
  S111-id-collision), routed around, no answer assumed. ✓
- Fleet census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` →
  `kasegi ok …/corpus/SOURCES.md`, rc 0, with the six inherited W04 duplicate-URL warnings
  (S028, S029, S072, S076, S080, S085) unchanged.

## 2. Claim re-checks (step 2)

- **C1 — depth:verifiability (4 → 4, delta 0; NOT VERIFIED as declared). Re-measured on committed
  bytes:** `git diff a7880216… 2c3345a1… -- corpus/instruments/recheck-cwd-census.py` → empty; the
  counter is byte-identical to base, so nothing landed and no score can move. **Gate evidence
  verified, sibling gate not executed (§Gate standard):** committed
  `.ufo/waves/round-76/controls/m2b-survivor.txt` ends `selftest cases=8 failures=0` (rc 0) for
  committed `controls/m2b-conjunct-removed.py` — the consuming-conjunct mutant survives, so the
  frozen kill rule fails; `w1/ReviewC1.md` records A1 8/0, A2/A4 real-tree parity, A5 exec surface,
  and `w1/ExecC1Amend.mutant-m2a-run.txt` shows the A3 case-6 kill was a NameError from deleting the
  `res6` assignment, not an assertion kill (QUALITY R127). Revision measured: frozen bytes from
  `git archive 5da54cd4 corpus` per the report. The lane's refusal to land C1 is correct.
- **C2 — coverage (8 → 8, delta 0; NOT VERIFIED as declared). Re-measured on committed bytes:**
  `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → base 110,
  landed 111 (S111 row at line 123, tier A docs, status `queued`, used-by `—`);
  `git ls-tree … corpus/knowledge/ | grep -c '\.md$'` → 91 → 91 (no admitted entry; the draft sits at
  `.ufo/waves/round-76/c2-unadmitted/osv-api-surface-and-limits.md.draft`). **B5 evidence-verified:**
  committed `w1/ReviewC2.md` records the real run `S111:Q01-api-version UNAVAILABLE
  reason=quote-too-short-to-be-evidence`, rc=2; this verifier re-derived it without executing the
  gate: the committed manifest's Q01 quote `API (1.0)` normalizes to 9 characters <
  `MIN_QUOTE_CHARS = 12` (`corpus/instruments/source-recheck.py:33`), so rc 2 is forced. **B6
  distinctness re-opened:** `corpus/source-snapshots/round-73/S108.txt:5-9` holds `POST
  /v1/querybatch`, `GET /v1/vulns/{id}`, `GET /v1experimental/importfindings`, `POST
  /v1experimental/determineversion`, `POST /v1experimental/ubuntu/binary-to-source` (with `POST
  /v1/query` the line above) — the endpoint ground C2 claimed is already held (F51/S080 too). The
  lane's refusal to admit C2 is correct.
- **No owned axis harmed:** `git diff a7880216… 2c3345a1… -- SCORECARD.md` shows only an appended
  round-76 section with no score change (depth:verifiability 4, depth:density 9, coverage 8 held);
  the non-wave diff is exactly the 7 declared files (LOG, SCORECARD, QUALITY, SOURCES, lesson,
  S111.txt, manifest.json); SKILL.md, PROVINCE.md, corpus/README.md, corpus/knowledge/, both gate
  instruments and `knowledge-expected.txt` have empty diffs — the claimed attempt-1 reverts are real.
- Frozen `claims.json` (`.ufo/waves/round-76/claims.json`) declares C1 depth:verifiability (lowest
  non-retired axis) and C2 coverage — matches the report's declared claims.

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| depth:verifiability | unchanged | counter byte-identical to base (empty diff); kill rule failed; score 4 held |
| depth:density | unchanged | not targeted; SCORECARD round table 9 → 9 |
| coverage | unchanged | S111 `queued` only; knowledge 91 → 91; B5 rc 2 + B6 ground held |
| calibration | unchanged | SCORECARD/SHONEN match observed state; both claims honestly refused (honest-stop) |
| adjacency | unchanged | contested scope named (S111 id collision, assimilation 80/94) routed to L0, not absorbed |

## 4. Discernment spot-check (step 3, LEARNING.md)

The round's Gate block has **candidates: 1 (F54), admits: none, rejects: none-as-rows**, plus the
R119 distinctness reject line for C2. With zero admits this round there is no admit decision to
sample — recorded as a finding, not a defect (an honest-stop round has no admits to check). Both
checkable decisions were re-opened:

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| F54 → C2 knowledge entry | rejected (B5 rc 2; B6 ground held) | committed `w1/ReviewC2.md` run record; my own 9<12-char derivation from committed manifest + `source-recheck.py:33`; `corpus/source-snapshots/round-73/S108.txt:5-9` | **agree** | the pinned quote is below the instrument's own floor and the endpoint strings are already held; admitting would enter unverified bytes into a gate |
| S111 SOURCES.md row (new this round) | written as `queued`, used-by `—` | live refetch of `https://google.github.io/osv.dev/api/` on 2026-11-05 → quotes "API (1.0)", "Currently there are no limits on the API.", "six different types of requests" all FOUND in the page text; raw 15,262 bytes matches the manifest record; located quote at `S111.txt:36` = 8 words (≤25) | **agree** | capture fresh, quotes locate, scope exclusions correct; `queued` (not `opened`-for-admission) matches the failed B5/B6 |
| new QUALITY rows R124–R127 | added, each citing its grounding lesson | `corpus/QUALITY.md:576-579` — R124→M76-4/F1, R125→M76-1/F12, R126→M76-2 + the rc-2 reproduction, R127→M76-3 + the m2b survivor | **agree** | every criterion cites the lesson that produced it (QUALITY contract) |

## 5. Trend verdicts

- **expansion: unchanged** — no admitted knowledge entry on uncovered ground (91 → 91); one `queued`
  row with its gate record; F54 refused.
- **quality: unchanged** — no admitted entry superseded or re-verified; both gate instruments
  byte-identical to base (empty diffs); R124–R127 are grounded criteria (the path to improved) but
  no measured quality move landed.
- **discernment: unchanged** — the attack-seat disagreements came from seats the lane dispatched,
  which count as the lane (LEARNING.md); the non-author check is this closure file, and it agrees
  with the round's gate decisions; SHONEN/SCORECARD match observed state. Honest-stop discipline
  verified, no measured calibration move.

## 6. Routed items for the lane's next round (fix list)

- **V-A (from lesson R-A/M76-3):** the successor C1 predicate must make the case-6 RESULT a consumed
  assertion and kill by assertion failure — the `m2b` conjunct-removal survivor class is the
  required kill; a NameError kill does not count.
- **V-B (R-B/M76-2):** freeze a fresh manifest whose quotes all pass `source-recheck.py`
  (≥12 normalized chars each) before the freeze; the frozen Q01 is not repaired in place (L0 option
  A/B is operator-owned).
- **V-C (R-C/M76-1):** before freezing a subject's ground, sweep admitted entries as well as
  captures (R125); the five non-query OSV endpoint contracts need their own capture and
  distinctness sweep.
- **V-D:** two L0 questions remain open (frozen-Q01 option A/B; S111 id collision, 80/94 staged ids
  collide) — keep routed around; never assume an answer.
- **V-E (note, status-neutral):** the round-start registry count 110 was carried from an attempt-1
  receipt rather than re-run in attempt 2 (disclosed in the report). Closure re-measured base 110
  from `a7880216…` and it stands; next round re-runs its own round-start census.
- **Operator note:** no SHONEN box reached `[x]` this round and none is claimed non-author-verified
  (boxes 1/3/4 are `[~]` with pointers, box 2 `[ ]` — no end-to-end bounty task this round);
  nothing here flags a promotion candidate. Promotion stays operator-owned.
