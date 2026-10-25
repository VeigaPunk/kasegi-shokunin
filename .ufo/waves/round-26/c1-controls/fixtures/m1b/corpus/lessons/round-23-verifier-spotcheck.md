# Round 23 — verifier spot-check (kasegi)

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25
reviewed lane endpoints: `1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a` → `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-23/kasegi.md`
claims frozen at: `.ufo/waves/round-23/claims.json` (base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`)

## Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | OK — `git log --format='%an %ae %H' -- .ufo/reports/round-23/kasegi.md` → 5 commits, all `kasegi-shokunin <kasegi@shokunin.local>` (tip `9ef8e2542cd40964554ab232dc4e110cc3eef0c0`). |
| `SHONEN` heading, one line per box | OK — `## SHONEN` with 4 `[~]` lines + pointers; no `[x]` claimed (correct: no non-author verifier yet). |
| Cited lane commits exist and are ancestors | OK — all 12 cited hashes (`f6966d4d`, `5842ef72`, `c8ec0a6b`, `d0a3f6a4`, `922a4dde`, `1fafde8f`, `953c2788`, `2712c992`, `4d9231e7`, `12edac47`, `bf9ce024`, `8acb255d`) pass `git merge-base --is-ancestor <h> master`. |
| No uncommitted round work | OK — `git status --porcelain` empty; `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`, branch `master`, local = remote = `d0a3f6a4`. |
| Prompt carries template contract | OK — `templates/round-prompt.md` rendering present (report path, commit-before-report, SHONEN heading, hash-citation rule, write scope) + hyaku addendum §6; L2 route map matches MISSION.md §L2 (≥8 in one batched call, host route table). |
| Driver digest (watchdog.log, mutable — copied) | launch 2026-10-20T18:30:58-03:00 pgid=1137022; launch 2026-10-23T20:41:47-03:00 pgid=3508145; launch 2026-10-25T03:23:48-03:00 pgid=1759483; complete 2026-10-25T03:57:08-03:00; all `driver=hyaku-inline attempt=1`. |

Dispatch evidence present; the lane-round reported. Status `ok`.

## Per-claim re-checks

### C1 — `depth:verifiability` (frozen: MIRROR-EQUIVALENT soundness)

**Evidence-verified via committed receipts** (lane-owned instrument; per
PROTOCOL §Gate standard "Closure consequence" the committed evidence is
verified, the sibling's checker is not executed by the integrator).

- Receipts `.ufo/waves/round-23/c1-baseline.json` (do-nothing control) and
  `c1-fixed.json` (landed bytes) parsed and tallied by the verifier:
  - `c1-baseline.json`: `resolver_sha256=d6a3c3f1…f903`, 12/24 PASS — all 12
    `nature=escape` cases FAIL with `expect=GONE actual=MIRROR-EQUIVALENT`;
    12/12 controls PASS (2 GONE, 2 INTERNAL incl. the disclosed
    `carve-out:path-outside-internal`, 4 MIRROR-EQUIVALENT, 4 RESOLVES).
    → escape **0/12 GONE**, matrix 12/24, exit 1. Matches report.
  - `c1-fixed.json`: `resolver_sha256=690153ad…ea2d`, 24/24 PASS — all 12
    escapes `actual=GONE`; all 12 controls unchanged. → escape **12/12 GONE**,
    matrix 24/24, exit 0. Matches report.
- Integrity binds re-derived: `sha256sum` of the live files reproduces
  `matrix_sha256=d05b1e0c…b809` (`mirror-containment-fixtures.json`),
  `checker_sha256=dddd5549…f98a` (`mirror-containment-check.py`),
  `resolver_sha256=690153ad…ea2d` (`corpus/instruments/resolve.py`), and
  `d6a3c3f1…f903` (`c1-baseline-resolver.py`) — same matrix in both runs, so
  the delta is the resolver only; do-nothing control cannot meet the target.
- No-harm guard: `falsify/NoHarmDiff.md` — `git archive 922a4dd` export through
  both detectors produced byte-identical TSV (`sha256:80ef1504…`),
  `changed=0 added=0 dropped=0`, `distinct=1589`. Seat also proves the guard
  **vacuous on this host** (`mirror=0`; `~/Projects/the-bounty-hunter`,
  `~/Projects/bounties*` absent, `KASEGI_MIRROR` unset) — published as vacuity
  in the report and in `falsify/VacuityDisclosure.md`, not hidden.
- Verdict: **improved** (score held 4 per SCORECARD — recorded as
  improved/held, honest). The `bounty_suffix()`/`under_mirror()` fix is
  confined to `resolve.py`; lane-relative `INTERNAL` and the literal bounty
  hit are named carve-outs pinned as controls.

### C2 — `coverage` (frozen: F06–F08 admission, frontier 5/8 → 8/8)

**Re-measured by the verifier over committed bytes.**

- `awk -F'|' '$2 ~ /^ *F0[6-8] / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}'
  corpus/README.md` → **3** (before at `922a4dd` → **0**). Matches.
- F01–F08 variant → **8** (before → **5**). Matches.
- `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → **31**
  (before `git show 922a4dd:…` → **27**): +S028 (rejected), +S029, +S030,
  +S031. Matches.
- Recheck receipts (committed, not re-executed):
  `.ufo/waves/round-23/c2-recheck-S0{18,29,30,31}.txt` all `EXIT=0`
  (7/10/11/11 OK lines per header + file); `c2-controls.txt` records three
  failing controls — flipped digest exit 1, missing source exit 2, fabricated
  quote exit 1 — the checker is shown able to fail. Knowledge entries
  carry `source:`/`verified-at:`/`recheck:` trios citing S018/S031/S029.
- The F07 correction (S031 4.2.6 supersedes S030 4.2.0; 4.2.11 SHOULD→MUST) is
  real and materially improved the claim: verified against the pinned
  snapshot `S031.txt` (`Version: 4.2.6`, `Approved 2026-October-14`,
  `Effective 2026-October-20`, rule 4.2.11 MUST) — see spot-check table.
- Verdict: **improved** (score held 7; frontier surface 5/8 → 8/8).

## No axis harmed

`git diff 1fafde8f…d0a3f6a4 -- SCORECARD.md` is append-only (new
`## Round 23` result section + errata block; prior scores and r22 corrections
untouched). `PROVINCE.md` unchanged; `SKILL.md` untouched. The only
instrument touched under `corpus/instruments/` is `resolve.py` plus two new
committed files (checker + fixtures); density inputs (`SKILL.md`,
`citation-survival.*`) are byte-same or regenerated identically per the guard.
Sourced-claim duty satisfied (C2 entries cite S018/S029/S031 opened this
round). `Assimilation: none` declared with reason; one `considerthese/`
proposal landed as QUALITY.md Q8 — within contract.

## Spot-check table (discernment — non-author)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S028 (admit as rejected row: `rejected`, flip recorded) | Reject duplicate-row proposal for HackerOne Safe Harbor FAQ | Live re-open `https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq` (2026-10-25, 122 973 B fetched) | **agree** | Quote "Adopting a Safe Harbor does not change the program scopes." located verbatim under "How to Enable Safe Harbors (Program Owners & Admins)". S006's row already names the correct heading — the error was in the r22 lesson Gate, not the source row; a second row for the same URL+scope would be a duplicate (census correctly flags W04). Rejection with flip is the right call. |
| S029 (admit, `mined`, supersedes S024) | Admit Regulation (EU) 2024/2847 as A-tier for F08 | Committed snapshot `corpus/source-snapshots/round-23/S029.txt:14` | **agree** | Quote "no later than 14 days after a corrective or mitigating measure is available" is verbatim in Article 14(2)(c); anchor (OJ 20.11.2024, Art. 14/15/16/71) resolves; `used-by` → `cra-manufacturer-reporting-duties.md` exists. |
| S031 (new row, `mined`, supersedes S030) | Admit CNA Rules v4.2.6 as current authority | Committed snapshot `corpus/source-snapshots/round-23/S031.txt` (49 350 B, normalized `pdftotext`) | **agree** | Title block verbatim "Version: 4.2.6 Approved date: 2026-October-14 Effective date: 2026-October-20"; rule 4.2.11 reads "CNAs MUST assign different CVE IDs to different, Independently Fixable Vulnerabilities." — the SHOULD→MUST flip that forced F07's rewrite is real, ≤25-word located quotes honored. |

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin kasegi` → `ok`, rc=0; the two W04
duplicate-URL warnings (S028, S029) match the report's pasted output and are
cross-scope duplicates of the registry's own historical rows — disclosed.

## Trend verdicts

- **expansion — improved.** 3/3 frontier topics admitted (F06–F08; 5/8→8/8),
  +4 SOURCES rows incl. a current-version pin (S031), one capability row
  entered (`mirror-containment-matrix`).
- **quality — improved.** Post-attack repairs each carry a reproduction
  (M7–M18); the rechecker normalizes and pins rather than substring-matching;
  checker hardened (confinement, `resolved_path` assertion, digest binds).
- **discernment — improved.** Lane rejected its own first-landing F07 on a
  machine check (inherited `build/CnaFix.md` supersession evidence), kept the
  literal carve-out rather than widening the frozen predicate, and the
  outside sample here agrees on the checked admit and the checked reject.

## Defects routed to the lane (next round)

1. F01–F05 `recheck:` lines exit 2 `not-listed` — no capture exists for
   S001–S015. Already disclosed by the lane as residual debt
   (`falsify/Q7ControlsClaim.md`, lesson); routing so it stays on the queue.
2. Detector liveness debt (pre-existing, disclosed): first-match brace/glob
   suppression and never-resolving empty brace alternative
   (`falsify/BraceGlobProbe.md`) — outside the frozen predicate; fix or
   retire next round.
3. Attempt numbering: the report self-labels "attempt 2" while the driver
   logged all three launches `attempt=1` — naming nit only; record the
   convention used.
4. SCORECARD r23 result-table C1 cell still shows the first landing's
   "6/6, 13/13" with an appended errata (append-only is correct); consumers
   should read the errata block. Cosmetic.

## Notes

- The round's waves: build 64 seats (inherited registry, 44 reports) +
  falsify 36 seats (36 reports), total 100 inside the 32–128 band; wave-2
  first dispatch refused at host job limit, refusal receipt committed, payload
  resent unchanged. SHONEN boxes are asserted `[~]` — they look mechanically
  checkable by a non-author next pass; promotion remains operator-owned.
- C1 verdict is *improved with score held 4*: a real, bounded soundness fix
  on the lowest non-retired axis with a do-nothing control that cannot meet
  the counter — the strongest claim shape this lane has filed.
