# MutArmC1 — mutation test, bounties arm of anchorcheck.py (round 28 wave 1)

Role: mutation-tester (leaf). Seat: `MutArmC1`. Time: 2026-10-25 UTC.
Milestone: round-28. Judged on: depth:verifiability (C1).

## State of the instrument during this attack (honesty label)

- Committed lane base: `c9f8b115a098c65356e4b3b6048af45a37ab8395` (round-28 freeze commit).
- Instrument committed at HEAD: `c2a9e6c6088015968b3c6ea7f12a0ea66699c3ecb2a21db362659db8e95ef748`
  (PRE-CHANGE bytes, sha256 of `git show HEAD:corpus/instruments/anchorcheck.py`).
- Instrument in working tree while I ran: `95333e29ee5acce549f8e0b6328c6dcab3c542cf16bc295d6a6ae70c6f144514`
  (stable across repeated reads; compiles; passes smoke: bounties fixture → exactly 1
  BOUNTIES-ABSENT line, exit 1; bad fixture → BASE-ABSENT, exit 1). ExecImplC1 landed in the
  working tree mid-run; HEAD bytes are still pre-change.
- Receipt is therefore labeled **PRE-STATE (pre-commit)**: mutants and scores are against the live
  working-tree bytes `95333e29…`, snapshot at `wave1/MutArmC1/base-landed.py`.
- Post-change re-run for the L1 (after the instrument is committed):
  ```
  cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  sha256sum corpus/instruments/anchorcheck.py && \
  python3 corpus/instruments/anchorcheck.py .ufo/waves/round-27/c1-controls/bounties-fixture.md 2>/dev/null | grep -c BOUNTIES-ABSENT && \
  python3 corpus/instruments/anchorcheck.py SKILL.md >/dev/null 2>&1; echo skill_exit=$? ; \
  python3 corpus/instruments/anchorcheck.py SKILL.md 2>/dev/null | sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'
  ```
  My probes reuse identical bytes (`base-landed.py` == live `anchorcheck.py` at hash
  `95333e29…`), so post-commit re-run should reproduce every row below if the impl is unchanged.

## Mutation base

`base-landed.py` = live working-tree bytes (`95333e29…`), containing the full bounties arm:
`_BOUNTIES_CANDIDATES = (~/Projects/bounties,)`; `BOUNTIES_ROOT = _derive_root('KASEGI_BOUNTIES', _BOUNTIES_CANDIDATES)`;
`BOUNTIES_ABSENT`; CITE alternative `~/Projects/bounties/…`; realpath containment
(`requiredpath` + `commonpath` → OUTSIDE-BASE before BOUNTIES-ABSENT); `BOUNTIES-ABSENT`
bucket printed among first verdicts (not in the summary line); `FAIL_CLASSES` incl.
`BOUNTIES-ABSENT` → exit 1.

## Mutants (each exactly one behavior-bearing point; scratch copies only)

| # | Mutation | Exact change (diff vs base) |
|---|----------|------------------------------|
| M1 | Remove the bounties alternative from CITE entirely | delete line `r"|~/Projects/bounties/[\w./-]+\.(?:mjs\|sh\|json\|md\|csv\|jsonl\|txt)"` from `_CITE_PATH` (bounties cites become invisible again) |
| M2 | Remove realpath confinement for the bounties arm only | `path = os.path.realpath(os.path.join(bounties_root, …))` + try/except `commonpath` + `if not within_bounties: … OUTSIDE-BASE` → `path = os.path.join(bounties_root, …)`; escapes no longer classify OUTSIDE-BASE |
| M3 | Point the bounties root at the mirror candidates by mistake | `BOUNTIES_ROOT = _derive_root('KASEGI_BOUNTIES', _BOUNTIES_CANDIDATES)` → `_derive_root('KASEGI_BOUNTIES', _MIRROR_CANDIDATES)` |

All three compile (`python3 -m py_compile`). Hashes: M1 `fa964baee3e6996048aa787927ef9f14cd9718951974c6c59251dad513908efa`,
M2 `a8f7501e6a4dc56ae3c71fcf73793d01a1d9c9b7a5e170470f02383f271d2be8`,
M3 `ac7664e229e2c37ea4e4bb70488f7b920426284c548774d72eaa392d82b5cb19`.

## Fixtures (scratch, in `wave1/MutArmC1/fixtures/`)

- `bounties-fixture.md` — copy of the committed r27 fixture (unmarked `~/Projects/bounties/ops/claim-check.mjs:96`).
- `escape-fixture.md` — written by me:
  - `~/Projects/bounties/../etc/passwd.txt:1` (spec-shaped `…/../etc/passwd:1`-escape; target absent)
  - `~/Projects/bounties/../shokunin/kasegi-shokunin/SCORECARD.md:1` (escape onto a real lane file;
    a decoy copy is staged at `tmp/shokunin/kasegi-shokunin/SCORECARD.md` and `tmp/etc/passwd.txt`
    so a confinement-free mutant reads them IN-RANGE under a present temp root).
- `inrange-fixture.md` — written by me: `~/Projects/bounties/ops/claim-check.mjs:1` run under
  `KASEGI_BOUNTIES=$SCRATCH/tmp/bounties-root` (real temp dir containing `ops/claim-check.mjs`,
  2 lines — decoy). Base verdict: IN-RANGE, exit 0.

Env notes: hosts at run time — `~/Projects/bounties`, `~/Projects/the-bounty-hunter`,
`~/Projects/origin-work/open-bug-bounties` all ABSENT (verified). Temp roots staged under scratch:
`tmp/bounties-root` (real dir), `tmp/mirror-root` (real dir).

## Scores

| Mutant | Detector (bounties fixture, default env) | Detector (escape fixture, default env) | Detector (escape fixture, under `KASEGI_BOUNTIES=tmp/bounties-root`) | Detector (inrange fixture, under `KASEGI_BOUNTIES=tmp/bounties-root`) | SKILL.md (no new movement) | Verdict |
|--------|----|----|----|----|----|---------|
| BASE | 1× `BOUNTIES-ABSENT`, exit 1 (names `~/Projects/bounties/ops/claim-check.mjs`) | 2× `OUTSIDE-BASE`, exit 1 | 2× `OUTSIDE-BASE`, exit 1 | 1× `IN-RANGE`, exit 0 | exit 0, bad=0, LOST-RECORDED=306, all classes unchanged | — |
| M1 | **0 BOUNTIES lines**, exit 0 (cite invisible) | 0 verdict lines, exit 0 | 0 lines, exit 0 | 0 lines, exit 0 | identical to BASE (byte-equal output) | **KILLED** (expected: 0 BOUNTIES lines) |
| M2 | 1× `BOUNTIES-ABSENT`, exit 1 (same as BASE) | **2× `BOUNTIES-ABSENT`, exit 1** (absences preempt escapes: no OUTSIDE-BASE) | **2× `IN-RANGE`, exit 0** (escapes read the decoys: not OUTSIDE-BASE) | 1× `IN-RANGE`, exit 0 (same as BASE) | identical to BASE | **KILLED** (expected: escape not OUTSIDE-BASE — under a present root it classifies in-range; under the absent root the escapes flip to BOUNTIES-ABSENT) |
| M3 | 1× `BOUNTIES-ABSENT`, exit 1 but **names `~/Projects/the-bounty-hunter/ops/claim-check.mjs`** (wrong root) | 2× `OUTSIDE-BASE` **against `~/Projects/the-bounty-hunter`** (wrong root) | 2× `OUTSIDE-BASE` against wrong root | **1× `BOUNTIES-ABSENT`, exit 1** while the declared root is PRESENT (wrong absence verdict; the `$KASEGI_BOUNTIES` override is ignored — `_derive_root` only honors the env when fed the right candidates; mirror candidates are absent on this host) | identical to BASE | **KILLED** (expected: wrong absence verdict — shown by inrange-under-present-root and by correct-root naming differences; note the frozen `grep -c BOUNTIES-ABSENT` counter alone does NOT discriminate M3 on this host, because both candidate roots are absent — a counter-sensitivity finding, see below) |

## Kill-rule check

- No counter reached its "after" value from the do-nothing bytes (BASE rows are the pre-change
  behavior; the frozen `grep -c BOUNTIES-ABSENT` = 1 only under BASE and M3, where M1 = 0 and M2
  depends on env).
- No mutant re-used another mutant's bytes; all three are single-hunk, single-concept diffs
  (shown above, verified by `diff`).
- SKILL.md: all four runs byte-identical output, exit 0, bad=0, LOST-RECORDED=306,
  BASE-ABSENT=0, PIN-BROKEN=0, OUTSIDE-BASE=0 → no harm, no new movement.
- Restoration evidence: I never wrote the live instrument; it is untouched by me (live sha at
  start and end of my run: `95333e29…`, unchanged — I only read/copied it). Scratch files live
  in `wave1/MutArmC1/`; fixtures `fixtures/`, temp roots `tmp/`, outputs `out/`.

## Findings / coverage notes

1. M1: the CITE arm is load-bearing. Deleting the alternative makes bounties cites silently
   invisible again (0 lines, exit 0) — exactly the round-25 debt class. Killed.
2. M2: the realpath/commonpath containment is load-bearing for escapes. Without it, escapes
   classify in-range under a present root (reads external files) and degrade to
   BOUNTIES-ABSENT on the absent-root host (order inversion: absence preempts escape). Killed.
3. M3: the root-candidate source is load-bearing but the frozen kitchen-sink counter
   (`grep -c BOUNTIES-ABSENT`) is **insensitive to which root tree is named**: on this host,
   where BOTH the bounties root and the mirror candidates are absent, M3 still emits exactly 1
   `BOUNTIES-ABSENT` line (count 1, exit 1) — the same count as the correct implementation —
   and only the resolved-root text differs. The wrong absence verdict is visible in my inrange
   probe (root present via `$KASEGI_BOUNTIES`, still BOUNTIES-ABSENT) and in every detail line.
   This is a counter-sensitivity finding: a would-be survivor against the frozen grep-counter is
   killed by a text-level probe. It is not a contract change; it is an argument for a stronger
   counter (assert the resolved root equals the canonical `~/Projects/bounties`).
4. The landed implementation's ordering on the absent-root host (escape → OUTSIDE-BASE, not
   BOUNTIES-ABSENT) is confirmed by BASE rows; M2 flips that ordering (BOUNTIES-ABSENT), so
   the ordering itself is a mutation-vulnerable observable and should stay as landed.

## Files

- `wave1/MutArmC1.md` — this report.
- `wave1/MutArmC1/base-landed.py` — snapshot of the instrument base (sha `95333e29…`).
- `wave1/MutArmC1/m1.py`, `m2.py`, `m3.py` — mutants (hashes above).
- `wave1/MutArmC1/fixtures/` — escape/inrange fixtures (written by me) + bounties fixture copy.
- `wave1/MutArmC1/tmp/` — staged temp roots/decoys.
- `wave1/MutArmC1/out/` — full raw outputs (base/m1/m2/m3 × SKILL.md).
- `receipts/MutArmC1.txt` — short per-seat receipt.
