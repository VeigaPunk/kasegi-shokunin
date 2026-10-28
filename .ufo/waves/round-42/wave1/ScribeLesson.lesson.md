# Round 42 — kasegi

Lane: `kasegi-shokunin`. Revisions: base `5053a7f46de35784cff4b56756906e9014a38276`; claims-freeze commit
`0566bd66e93d429b2df8b6751cf10cbdc391e79b` (`.ufo/waves/round-42/claims.json`). Judged head J = the lane
commit carrying every round-42 change except the receipt (`<pending>`); verification ref Y = J + the
receipt `.ufo/waves/round-42/final-gates/all-gates.txt` only (`<pending>`). Lane files never name J by hash
(a commit cannot contain its own hash); the report names J and Y. Counting commands run over the suite run
at Y; negative controls run at base `5053a7f46de35784cff4b56756906e9014a38276` and round-41 judged head
`1f7464612ac4c44e39886b82e812610d3c039b13`. Shape: two v1 waves; wave 1 `kasegi-r42-build` dispatched 64
seats (32–64 band), and wave 2 and the round total are counted from the wave-2 dispatch when it lands,
never estimated: `<pending>`. Every wave carries connector seats this round (the D-r41-5 routed item):
wave 1 carries 2 (`ConnCrossClaims`, `ConnWave2Seed`); wave 2's count is `<pending>`.

Attack share: wave 1 `kasegi-r42-build` 21/64 = 32.8% (reviewer 8 + critic 8 + mutation-tester 5, counted
from the `wave1-dispatch.json` registry members, `counts.spawn` 64); wave 2 and the round total are counted
from the wave-2 dispatch when it lands: `<pending>`.

## Frozen claims

Before → after, as frozen in `.ufo/waves/round-42/claims.json` (2026-10-28T12:05:00Z, KasegiR42).

| Claim | Axis | Before | After |
|---|---|---|---|
| C1 | depth:verifiability (4, held) | suite absent — base export exits 127 and nothing prints `closed=13/13` (`c1-controls/do-nothing.txt`); the r41 suite at base prints `selftest cases=12 failures=8`, `closed=8/12 exit=1`, with I1's per-block evidence union and I3's mangled-token acceptance alive; routed queue open: I1 per-correction evidence, I3 token boundary, I7 bare-pipe/leading-whitespace, I5/I12 declaration completeness, I6 outside-configured-root stray, capture-binding missing-path/URL variants, frontier-counter status-flip blind spot (`corpus/lessons/round-41-verifier-spotcheck.md` §5 item 6); D-r41-1 duplicated `Correction (round 41)` blocks, D-r41-3 SKILL registry split table + duplicate `r40-closure.sh` row | `r42-closure.sh` landed export-mode only (plain run exits 2); `closed=13/13 exit=0` at Y; graded `selftest cases=13 failures=0` with both transcripts teed in the receipt; base and round-41-head exports each red (`closed<13/13 exit=1`); J1–J13 close the routed families, and every repaired check carries a replay limb that re-executes its committed defeat artifact against the current suite bytes and requires rejection |
| C2 | coverage (8, held) | frontier 24 (F25 absent); registry 63 (S064+ absent); entries citing S064+ 0; knowledge 60; harness `entries=27 pass=27`; binding `records=55 bound=55`; audit `expected=60`; census exit 0 (`W04 S028`/`W04 S029` only) — `c2-controls/before.txt` | frontier 25 (F25 admitted); registry 64+R (S064 mined, ≥1 screened reject S065+ with reason + flip); entry citing S064 1; knowledge 61; harness `entries=28 pass=28` incl `PASS F25`; binding 56/56; audit `expected=61`; census exit 0; measure 45/45 = 1.000 |

## Mistakes

| id | class | event | evidence | captured-by | fix | able to fail |
|---|---|---|---|---|---|---|
| M42-1 | evidence-union (per-correction evidence not enforced) | the round-41 suite's I1 collected correction evidence as a cross-record union, so its own selftest fixture that removes one correction's named evidence still reported `evidence=3/3` and the check accepted it | `.ufo/waves/round-41/wave2/CritC1KillRule.md` and `RevC1Counters.md`: `selftest detail=I1 mutant=evidence-not-named rejected=0 rc=0 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0`; the r41 instrument collects evidence across records (lines 902–906); routed at `corpus/lessons/round-41-verifier-spotcheck.md` §5 item 6 | new round-42 QUALITY criterion (per-record verdicts: evidence claims are per-correction, never union aggregates; id `<pending>` until the append lands) | J1 (F-EVID): every record block's own `Correction (round N)` line set must name its evidence, with no cross-block union; J1's replay limb re-executes the committed `evidence-not-named` defeat and requires rejection | `selftest case=J1` must print `mutants=1/1 positive=pass ... verdict=pass`, and `check_j1` over the `evidence-not-named` fixture must print `closed=0`; the r41 I1 printed `rejected=0` with `evidence=3/3` on that same input |
| M42-2 | token-boundary (counted value matched as a substring, not a whole token) | the round-41 suite's I3 accepted a mangled tally: replacing a correction value with `closed=10/100` still satisfied the value-presence tally, so the check reported every record valid | `.ufo/waves/round-41/wave2/RevC1Counters.md` item 1 and `CritC1KillRule.md`: `selftest detail=I3 mutant=mangled-value-token rejected=0 rc=0 payload=exact=2/2,substring=2/2,records=3,tally=3/3,mangled=0` (mutant written at r41 instrument lines 1757–1759; value limb 438–459) | J2 (F-TOKEN) | J2 extracts every `closed=<n>/<m>`, `failures=<k>` and `cases=<k>` value as a whole token bounded by non-digit non-slash characters (word boundaries are not sufficient), and its replay limb re-executes the `mangled-value-token` defeat requiring rejection | `selftest case=J2` must print `mutants=1/1 ... verdict=pass`, and `check_j2` over `closed=10/100` must print `closed=0`; the r41 I3 printed `tally=3/3` on that input |

## Census

Before (`census-before.txt`): `W04 S028`, `W04 S029`, `ok`, exit 0. After
(`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi`): `<pending>`.
Registry 63 → 64+R rows: the appended block adds S064 (status mined, opened this round) and at least one
screened reject S065+ (status rejected, reason + flip); no existing row cell changes; `PROVINCE.md`,
`SKILL.md`, `SOURCES.md`, `corpus/README.md` and the search log receive appended blocks only.

## Gate

`<pending>` — landed by the round-42 C2 gate seat as `wave1/ScribeC2Gate.gate-block.txt`: the admitted
F25 / S064 block (registry row, source with URL and access date, capture and manifest, ≤25-word located
quotes, knowledge entry, frontier admission, limit) plus the recorded screened reject (S065+, reason +
flip, URL, access date, ≤25-word located quote — closes D-r41-2).

## Wave-2 falsification

`<pending>` — appended when the round-42 falsify wave reports: per-claim verdicts, attack tallies counted
from the wave-2 dispatch (never estimated), each routed family named with the J-check that reds it, and
each committed defeat artifact re-executed by its replay limb.
