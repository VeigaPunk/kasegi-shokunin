# AttackF1 — Final scope sweep (round 26, wave 2)

Seat: L1Kasegi26.AttackF1 (leaf, read-only sentinel)
Date: 2026-10-25 UTC
Milestone: final scope sweep
Base: 1b076fa7f2fb5e7dd9d87449514eba526043421b
Ownership baseline reused: `.ufo/waves/round-26/wave1/c4-ownership.txt`

Snapshot note: this sweep executed while wave-2 seats were still landing reports. All
findings are as observed at run time. Later additions under `.ufo/waves/round-26/wave2/`
are within the allowed wave2-report class.

## Check 1 — Working-tree changes since base ⊆ owned paths (+ allowed additions)

Method: `git status --porcelain=v1 -uall` in the lane (1208 entries), every path classified
against c4-ownership.txt plus the two explicit allowances (wave2 reports; lesson amend;
c1-controls additions).

Tracked modified (7) — all match owners 1:1:
| Path | Owner (c4-ownership) |
|---|---|
| LOG.md | w7 ScribeLogProvince |
| PROVINCE.md | w7 ScribeLogProvince |
| SCORECARD.md | w6 ScribeScorecard |
| SKILL.md | e4 ExecSkillRegistry |
| corpus/README.md | w4 ScribeReadme |
| corpus/SOURCES.md | w1 ScribeSourcesAppend |
| corpus/instruments/recheck-audit.py | e1 ExecAuditFix |

Untracked (1201 files) — every path falls in exactly one class:
- **Owned production paths**: `corpus/source-snapshots/round-26/` (S041.txt, S040-live.txt,
  manifest.json; e5/e6), `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` +
  `iso-29147-divergence-and-clause-crosswalk.md` (w2/w3), `corpus/instruments/knowledge-expected.txt`
  (e2), `corpus/lessons/round-26.md` (w5 — the allowed lesson amend),
  `.ufo/waves/round-26/c1-receipt-index.txt` + `c1-instrument-digest.txt` + `c1-live.json` (e3),
  `.ufo/waves/round-26/c1-controls/` (e1, m1, m2, m3; includes `fixtures/` mirrors m1a–m1e/base —
  c1-controls addition class), `.ufo/waves/round-26/c2-controls/` (e7 `do-nothing.json`, m3
  `m3-gameability.txt`), `.ufo/waves/round-26/wave1/` (per-seat reports, all matching the named
  outputs in c4-ownership).
- **Wave2 reports (allowed)**: `.ufo/waves/round-26/wave2/` — currently AttackA3/A4/A6/A8/B1/B2/B4/
  B5/B6/B7/C1/D2/E1/G1/J1/K1/L1/M1.md, ScribeLessonAmend.md, lowercase aliases (a3,a6,b1,b4,b5,b6,
  b7,d2,e1,j1,k1,l1,m1,z2.md), h1-live-regen.json, m1-scratch/, b8/.
- **L1 orchestrator artifacts** (13 top-level items; attributed to the L1 main session, not to any
  seat — [INFERENCE] by creation time predating/paralleling dispatch and by role as spec builders):
  `assimilation/` (4 files, 09:24), `build-wave1-spec.py`, `wave1-spec.json`, `wave1-dispatch.json`,
  `wave1-plan.json` (09:32), `build-wave2-spec.py`, `wave2-spec.json`, `wave2-dispatch.json` (09:49).

Classified unmatched after the set subtraction: **zero** (the only apparent gap was SKILL.md, which
is owned by e4; my first classifier rule had a path typo, not a real violation).

Verdict: **PASS** — every seat-attributable change is within owned paths; the declared allowances
(wave2 reports, lesson amend, c1-controls additions) hold.

## Check 2 — No fleet-root / shokuknow / sibling writes

- **Fleet root** (`git status` of /home/vgpnk/Projects/shokunin): only platform/harness-managed paths
  changed — `.ufo/state/*.report-baseline` (14 lanes; mtimes 03:31–09:50, incl. kasegi at
  09:22:35, round start), `.ufo/watchdog.log` (09:50), `scripts/hyaku/hyaku.env` (03:22),
  `scripts/hyaku/lane-addendum.md` + `.scratch/goal-20261025-hyaku-12h.md` (09:29),
  `.ufo/waves/round-24/` (new, 05:55), `m-rev-vs-rev.py` (09:36). None are round-26 kasegi seat
  products; no round-26 artifact appears at fleet root.
- **shokuknow**: located at `/home/vgpnk/Projects/shokuknow` (sibling of fleet root, not inside it).
  Filesystem is rw btrfs `@home` (read-only is a convention, not enforced at FS level). Today's only
  write is `lanes/tabi/round8/.work/ratelimit-series.tsv` — a different lane's different-round work
  file; nothing from kasegi round 26.
- **Sibling lanes**: per-lane `git status` scans (20 sibling repos, kasegi excluded) show own-lane
  changes in chousa(3), kama(102), kengaku(10), kotodama(8), revenger(1), souji(12), tabi(1),
  tameshi(1). Grep for `kasegi|round-26` across all sibling status paths returned **zero hits** — no
  cross-lane leakage in either direction.

Verdict: **PASS**.

## Check 3 — claims.json byte-equal freeze (sha 343e568e…)

- `sha256sum` of `.ufo/waves/round-26/claims.json` =
  `343e568e7113f0d63ea63f7c9b8d7c18f44e310a67717d490a35ae1adec6741f` — matches the expected prefix
  `343e568e…` exactly.
- Working-tree claims.json is byte-identical to the HEAD version (`git diff` empty; git blob
  `05ee31857e61e3627a8cbb807b07294f91c972a5`).
- HEAD (1b076fa7) is itself the freeze commit: “round-26: freeze claims.json (C1 gate conformance,
  C2 F11 assimilation) before any measurement or dispatch”.

Verdict: **PASS**.

## Check 4 — HEAD still at base; no VCS writes by any seat

- `git rev-parse HEAD` = `1b076fa7f2fb5e7dd9d87449514eba526043421b` = base exactly. No seat has
  committed.
- Staging area empty (`git diff --cached` produces nothing).

Verdict: **PASS**.

## Overall

All four checks **PASS** as of the snapshot. One classification note for the L1: the 13 orchestrator
files (`assimilation/` + `build-wave*-spec.py` + `*-spec.json`/`*-dispatch.json`/`wave1-plan.json`)
sit outside the seat ownership matrix and the two explicit allowances; they are lane-internal L1
orchestration, not seat writes, but the literal allowance set should be amended to include them if
strict set-membership is intended.

## Tooling

No tools installed (nothing needed beyond git/coreutils/stdlib). No pacman activity.
