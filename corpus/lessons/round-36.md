# Round 36 — kasegi

Lane: `kasegi-shokunin`. Base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`; final lane commit `FINAL_LANE_HASH` (filled at closure). Shape: one v2 wave `kasegi-r36-build`, 64 seats (executor 18, scribe 12, reviewer 10, critic 6, scout 6, mutation-tester 5, connector 3, sentinel 2, simplifier 2; attack roles 23/64 = 35.9%).

## Frozen claims — before → after

C1 depth:verifiability (4, held): `corpus/instruments/r36-closure.sh` — export-mode only (`--export-ref <hash>`; plain run refused exit 2) — nine checks E1–E9 close the round-35 verifier spot-check's routed defects and the closure-order defects. Baseline runs: r35 base `3266c993` → `closed=0/9 exit=1`; r35 judged head `0aee0ef` → `closed<9/9 exit=1`; final lane head → `closed=9/9 exit=0`; `--selftest` → `cases=9 failures=0`.

C2 coverage (7, held): Frontier F19 (FIRST EPSS) admitted 18→19; registry S053 row (tier A, mined, opened 2026-10-26); entry `corpus/knowledge/epss-exploit-prediction-scoring.md` cites `source: S053`; harness `entries=22 pass=22 exit=0` incl. `PASS F19 … ids=S053`; `source-recheck S053` exit 0; census exit 0; knowledge 47→48; junk twin `c2-controls/junk-f19.md` rejected.

## Gate

### Admitted — F19 / S053 (FIRST EPSS documentation page)
- URL: `https://www.first.org/epss/` — HTTP 200, no redirect, 26804 served bytes, fetched 2026-10-26T15:35:10Z, normalized capture `S053.txt` 244 lines / 8448 bytes, sha256 `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`.
- Quote (≤25 words, located): `"(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days."` — S053.txt L216 (25 words); Q2/Q3 L217; Q4 L235. All `occurrences=1`.
- Recheck: `cd <lane> && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-36/manifest.json --source S053` → exit 0.

### Rejected
- `c2-controls/junk-f19.md` (fabricated guarantee sentence) — `grep -cF` = 0 in the capture; pinned comparison prints `S053:J1 MISMATCH reason=quote-not-found` exit 1; wrong-source twin fails `not-listed`/`quote-not-found` (ExecC2JunkControl).
- Standings refusals: 7 staged package entries unchanged, flip conditions unmet (ScoutStandingRefusals).
- Quarantine slice: 7 rows, 0 adopted (1 present-and-located duplicate S040; 2 absent quote-form; 4 unreachable).

### Assimilation: none adopted
Id-collision rerun: registry 52 × staged 94 → 22 collisions (S031–S052), guard load-bearing and fail-closed; 23 predicted once S053 lands against a different staged S053 (METI rule).

### Contested scope — none
F19/S053 uncontested across 20 sibling lanes (ConnSibling ruling); doctrine lacks a first.org host row (report-only observation).

## Mistakes

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M36-1 | landing / closure-order | round-35 lane kept committing claim-bearing paths after `complete` (04:00:34): 8ce6fb4 04:01:12 … 980aa3d 04:19:52; judged head lacks S052 capture | `wave1/ScribeMistakes.md` | none (new); criterion missed R4 | E9 quiescence gate + export-bound suite (r36-closure.sh) | dirty-tree red vs clean green |
| M36-2 | stale-premise | round-35 lesson Gate "source-recheck exit 0 on committed bytes" false at `0aee0ef` (capture absent; instrument exit 2) | same receipt | R16 | E8 correction recorded in round-36 lesson | 0aee0ef red / 5a25337 green |
| M36-3 | counter-discrimination | r35 suite's D3 near-name literal satisfied by `r-defect-closure.sh` row; exact basename `r35-defect-closure.sh` absent (0) | same receipt | R17 limb / R11 | E3 exact-basename rows (r35 + r36) | near-name-only fixture red; exact rows green |
| M36-4 | landing | report re-filed three times after `complete` (e4eb5140, 63ce2a63, 8cfcb5b6, 375f9514) | same receipt | R4 | full integration before the single report commit; report lands last | epoch predicate red at first filing, green at final |

## considerthese 2026-10-26 dispositions
1 distance-to-next-score: computed (`gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`); thresholds-in-§Saturation plank remains unlanded (coverage-8 threshold undefined). 2 end-to-end domain task round: not this round (SHONEN box 2 open). 3 quiescence gate: adopted (R28 + E9). 4 cap/externalise wave evidence: not this round (operator/LFS decision). 5 F18 PROVINCE amendment: adopted this round (with F19). 6 cadence/depth: recorded, no change. 7 proposal-status ledger: recorded, not started (existing ledger re-pin owed).

## Census
Before → after: both `sources-census.sh validate --root … kasegi` exit 0 (W04 S028/S029 only).

## No-harm
`SKILL.md`/`PROVINCE.md` base lines untouched (EOF appends only); `density.py` no density move claimed.
