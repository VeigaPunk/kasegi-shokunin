## Distance-to-next-score (round 39, mined from considerthese 2026-10-26 proposal 1)

Mined from `considerthese/2026-10-26.md` proposal 1 ("Make 'distance to next score' explicit"), written 2026-10-26, and landed in round 39. This section states the two promotion bars as criteria a non-author can re-run, and the measured distance at round-39 base `480b1a505a2dfc14a4f718d16d63808247214d0a`. It asserts no score move: a measured distance is not a claim that a score is due, and every figure below is the printed output of the command beside it.

### depth:verifiability, 4 → 5

Both limbs must read at the judged head:

1. **0 gated rechecks.** `python3 corpus/instruments/recheck-audit.py --root . --quiet` prints `executes=<n> gated=0 broken=0` together with `lines=<n> total=<n> pass=<n> ... parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`. A `gated` line is one that runs and fails closed, either on an absent base (`test -d ~/Projects/...`) or on a `LOST-RECORDED` anchor; it is an unsupported current claim until its base exists or its anchor is re-based.
2. **The score-5 audit bar.** `SCORECARD.md:331`: "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims." The dispositions row that restates it is `corpus/knowledge/considerthese-proposals-ledger.md:54`.

**Measured at base** (`python3 corpus/instruments/recheck-audit.py --root .`): `strict pass=50/50 cdroot_fail=0 instrument_fail=0 own_fail=0`, `executes=26 gated=24 broken=0`, `lines=50 total=50 pass=50 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`. `python3 corpus/instruments/score-gap.py` prints `gap: 24 of 50 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims`.

**Distance: 24 gated lines to 0.** 23 of the 24 open with a `test -d ~/Projects/...` guard; all 23 name `~/Projects/bounties` (one of them its `.git`), 6 also test `~/Projects/the-bounty-hunter` and 1 also `~/Projects/origin-work`. The 24th, `corpus/knowledge/citation-bases.md`, fails `anchorcheck.py` on a `LOST-RECORDED` anchor (`md:52`) and a `BASE-ABSENT` anchor (`md:31`). The 23 guards fail on the absent trees (`PROVINCE.md:5-19`), so they turn green only when a base exists; an entry could instead be re-grounded on a committed capture or have its anchors marked `LOST-RECORDED`, and neither has been done for these 23 because it changes what the recheck proves. The lane's reachable half is negative-only: do not add a gated line.

### coverage, 7 → 8

**Criterion** (the r22 measure, `SCORECARD.md:332`; planned for adoption at `SCORECARD.md:178` and never adopted — round 23 kept the r15 denominator, `corpus/lessons/round-23.md:173-177`):

`(20 + F_admitted) / (20 + F_total) = 1.000`, with `F_total` = frontier rows in `corpus/README.md` § Frontier (`grep -cE '^\| F[0-9]+ \|' corpus/README.md`) plus every `corpus/SOURCES.md` registry row still `queued` (an unmined in-scope source stays an uncovered surface until its row is admitted as a frontier topic or rejected with reason and flip — the r23 audit's own point, `.ufo/waves/round-23/build/CoverageDenom.md` § Finding 4), `F_admitted` = those frontier rows whose status cell is `admitted` (`awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md`), and every admitted row's entry passing `python3 corpus/instruments/frontier-recheck-count.py` (`pass` equal to `entries`, exit 0). The Core term stays 20: it is the r22 proposal's constant with no per-item derivation in the lane (`git grep -n '20 corpus-attested' -- SCORECARD.md PROVINCE.md corpus/` returns only `SCORECARD.md:332`), so it holds and the frontier and queued terms carry the move.

**Measured at base**: `F` rows 21, admitted 21, non-admitted 0, queued registry rows 9 (S016, S017, S019, S020, S021, S022, S023, S024, S025), so `F_total = 30` and `(20+21)/(20+30) = 41/50 = 0.820`; `frontier-recheck-count.py` prints `entries=24 pass=24 exit=0`. The frontier-only reading gives `(20+21)/(20+21) = 41/41 = 1.000`: numerator and denominator grow together because every topic enumerated so far was admitted in the round that enumerated it, so that reading cannot discriminate 7 from 8 and is not the criterion.

**Distance: 9 queued rows to 0.** 7 are unmined public sources (S016, S017, S019, S020, S021, S023, S025); 2 are superseded-but-unflipped (S022 by S030, S024 by S029) and need a rejected-with-flip row, not new mining. Both exits are in-lane work. A separate cap stays operator-owned: the adopted r15 denominator holds `0/18` domain surfaces present (`corpus/README.md:55-56`, `PROVINCE.md:121-122`), so the ratio above measures the corpus-facing half of coverage only.

**gap@r39:** depth:verifiability `gated=24` of `lines=50` (5 needs 0) · coverage `41/50 = 0.820` strict, `41/41 = 1.000` frontier-only (non-discriminating) · coverage's operator half `0/18` domain surfaces present.
