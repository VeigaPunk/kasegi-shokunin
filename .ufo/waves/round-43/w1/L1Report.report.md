# kasegi — round 43 (attempt 1)

Lane `kasegi-shokunin`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`, one v2 wave, 73 seats.
Report drafted by the lane's own L1; every figure below is re-derivable from a committed pointer.

## Work performed

Declared claims (frozen in `.ufo/waves/round-43/claims.json`, digest `a4c03e1e…`, freeze record
`.ufo/waves/round-43/freeze.txt`): **C1 on `depth:verifiability` (4, held)** — a new closure suite
`corpus/instruments/r43-closure.sh` whose six new checks K14–K19 make the round-42 verifier's narrative
defects machine-gradable; **C2 on `coverage` (8, held; capability acquisition)** — an executable gate for the
six-file claim-package contract (`corpus/instruments/claim-package-check.py`) with a worked exemplar built on
one public disclosure captured this round.

- C1 suite: `corpus/instruments/r43-closure.sh` (19 checks: K1–K7 and K9–K13 carry the r42 J-checks verbatim
  from the export's own `r42-closure.sh`; K8 is the round-43 receipt check; K14–K19 are the six
  narrative-evidence limbs under `corpus/instruments/r43-limbs/`). Evidence: the suite, `bash -n` clean, and
  the run/verification transcripts under `.ufo/waves/round-43/final-gates/`.
- C1 routed defects RD42-1/2/3/4/5/6/8 closed by appended correction lines: `SCORECARD.md` (RD42-1),
  `LOG.md` (RD42-2), `corpus/lessons/round-42.md` (RD42-3/4), `.ufo/waves/round-42/claims-erratum-5.md`
  (RD42-8), `.ufo/waves/round-43/claims-erratum-1.md` (RD42-6), and the `de09313` ref-bytes transcripts
  (RD42-5).
- C2 gate: `corpus/instruments/claim-package-check.py` + `corpus/instruments/claim-package-selftest.py`,
  exemplar `corpus/instruments/fixtures/claim-package/exemplar/`, nine `defect-<k>-<class>` fixtures, entry
  `corpus/knowledge/claim-package-gate.md`, capture `corpus/source-snapshots/round-43/S067.txt` +
  `manifest.json`, registry rows S067 (mined) and S068 (rejected with flip), coverage-map note.
- CONNECTOR: `ConnCrossClaims` landed the landing order (E0–E10) and four measured requirements, all followed.

## Landed changes

| change | LOG entry | commit |
|---|---|---|
| claims freeze + controls + freeze record + wave spec/dispatch | `## Round 43` | `4cb6d4ae` |
| C2 gate, selftest, exemplar, nine fixtures, capture, rows, entry, coverage note | `## Round 43` | `5b4a8503` |
| Correction (round 43) lines + claims-erratum-5 + claims-erratum-1 | `## Round 43` | `a6c1d462` |
| C1 suite + six limbs | `## Round 43` | `ffe197d1` |
| round records (lesson, SCORECARD, SHONEN, QUALITY, ledger) | `## Round 43` | `<pending: J>` |
| receipt (J-run) | `## Round 43` | `<pending: Y>` |
| at-Y verification transcript | `## Round 43` | `<pending: Y2>` |

## Before → after measurements

| claim | axis | before (base `ab98fac9`) | after (Y) | counting command |
|---|---|---|---|---|
| C1 | depth:verifiability | suite absent; the r42 stand-in over the base export prints `closed=12/13 exit=1` while all six routed defects sit in committed bytes (`c1-controls/do-nothing.txt`) | `<pending: run>` | `bash corpus/instruments/r43-closure.sh --export-ref <Y>` and `--selftest --export-ref <Y>` |
| C2 | coverage | gate absent; registry 66; knowledge 61; binding 56/56; audit expected=61 (`c2-controls/before.txt`) | gate `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`, `selftest cases=10 failures=0`; registry 68; knowledge 62; binding 57/57; audit expected=62; census exit 0 | `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar`; `--selftest`; the nine C2 counters in `claims.json` |

## Sources & frontier

SOURCES: registry 66 → 68 (S067 `mined`, opened 2026-10-28; S068 `rejected` with reason + flip). Census
before: `.ufo/waves/round-43/census-before.txt` — two standing W04 warnings (`S028`, `S029`) and `ok`, exit 0.
Census after: same two W04 warnings and `ok`, exit 0 (registry 68). Capture binding 56 → 57 bound, 0 unbound;
`recheck-audit` 61 → 62 entries; frontier harness `entries=28 pass=28` (no frontier row changes: F01–F25 held);
measure 45/45 = 1.000 unchanged. `Assimilation: none` — the §10 collision check was re-run read-only
(36 id collisions, all source-distinct apart from S042) and nothing was adopted, no renumber map filed.
Frontier rows advanced: none this round (the round moves documentation ground to an instrumented surface
instead, recorded in the `corpus/README.md` round-43 note).

## Trend verdicts

- **expansion — improved.** Registry 66 → 68 with one mined row opened this round and one recorded reject with
  its flip, knowledge 61 → 62 (`corpus/knowledge/claim-package-gate.md` citing S067), and a new executable
  capability (`claim-package-gate`) enters the repertoire table with its demonstration command. The frontier
  count is deliberately held rather than padded.
- **quality — improved.** The r42 suite was green while six routed narrative defects sat in committed bytes;
  K14–K19 now grade exactly those classes, each red at base and each rejecting a mutant built from the committed
  defeat bytes, and the missing `de09313` transcript is committed so the one unbound quote is bound.
- **discernment — improved.** The gate is exercised against one real public disclosure with `claimable: false`
  and its operator gates named, nine deliberate defects are rejected by their own rule, and a degenerate
  always-pass gate is rejected by the selftest; the round reports what its instruments show and nothing more.

## SHONEN

[to be filled from SHONEN.md at filing]

## Stale-lane

Respawn-per-round driver; no other mission of this lane is open.

## Tooling

None installed or upgraded this round: no pacman transaction (host-wide pause honoured), no `uv tool`, no
`npx`, no PATH write.
