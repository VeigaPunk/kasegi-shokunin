# RevFreshStart — round 42 wave 1 (fresh-start discipline review)

Receipt-only. No lane file edited, no mutating git/jj command, no network fetch, no tool installed.
Lane HEAD at review: `0566bd6` (child of base `5053a7f`, `git merge-base --is-ancestor` true).
`claims.json` sha256 `313b24ce3a35884bf70112743b8b0089802b2128dd3b6f80bbacf1cf006fcb08`, equal to
`git show HEAD:.ufo/waves/round-42/claims.json | sha256sum` (frozen bytes unmodified; `git diff HEAD` on it empty).
Disk guard green (`/fast/scratch/hyaku` 27% used).

## Verdict

**Fresh-start discipline holds, with three findings (none blocks).** (1) The last three rejected closures were read and every
routed item maps to a frozen check or a stated non-claim. (2) Do-nothing controls were re-run by me; neither claim's after-state
is reachable. (3) The claims have not narrowed since the freeze. The frozen text has one wrong control value and two
exposure points.

## 1. Last three rejected closures read and routed queues match claims.json

Files exist and are committed: `corpus/lessons/round-39-verifier-spotcheck.md` (18449 B), `round-40-verifier-spotcheck.md`
(19163 B), `round-41-verifier-spotcheck.md` (15057 B). Verdicts read from their section 2/6: r39 C1 NOT VERIFIED; r40 C1
NOT VERIFIED (`rejected-honest-stop`); r41 C1 NOT VERIFIED and C2 NOT VERIFIED (scope challenge upheld).

Queue to claim mapping (routed item -> frozen check):

| Routed item (source) | Frozen check |
|---|---|
| r41 s5.6 I1 per-correction evidence | J1 F-EVID |
| r41 s5.6 I3 token boundary; r40 D3 H2 | J2 F-TOKEN |
| r41 s5.6 I7 bare-pipe/leading-whitespace; r41 D-r41-3 split table + duplicate r40 row; r40 D6, D3 H1 | J3 F-TABLE |
| r41 s5.6 I5/I12 declaration completeness; r40 D3 H9 symlink | J4 F-DECL |
| r41 s5.6 I6 outside-root stray; r40 D3 H6; r39 R4/R7 G6 | J5 F-SCAN |
| r41 s5.6 capture-binding missing-path/URL | J6 F-BIND |
| r41 s5.6 frontier-counter status-flip blind spot | J7 F-FLIP |
| r39 R7 G2 payload binding; r40 D2, D3 H5 | J8 receipt integrity |
| r40 D3 H8 unkillable predicate; r41 I10 | J9 negative controls |
| r40 D3 H7 payload isolation | J10 selftest isolation |
| r41 D-r41-1 duplicated Correction blocks | J11 |
| r41 no-harm guard (I12), density byte-identity | J12 / J13 |
| r41 D-r41-2 no screened reject | C2 Gate reject |
| r41 L0 scope question (F24/RFC 9116) | F24 PARKED, never referenced as candidate (consistent with `.ufo/l0-questions.md:189`, still open) |

Routed items NOT claimed (state so, not narrowing, since claims.json never promised them): r41 D-r41-4 (Stale-lane report
line), D-r41-5 (connectors in wave 2), r40 D5/D7 (record hygiene, protocol ambiguity), r39 R1-R3/R5/R6 (already closed r40/r41).
`wave1-spec.json` carries `ConnCrossClaims`/`ConnWave2Seed` connector seats, so D-r41-5 is at least staffed.

Defeat artifacts the replay limbs must re-execute, checked for existence in `git ls-files`:
`round-41/wave2/MutSkillTablePipes.md` and `.findings.md`, `CritDeclarationCoverage.md`, `MutScratchTiming.md`,
`MutBindingExistence.md` (missing-path + URL case + trailing-slash variants, all "survived"), `MutC2Chain.md` (mutation A:
F24 `admitted` -> `explored` gave `entries=26 pass=26 exit=0`), `CritC1KillRule.md`/`RevC1Counters.md` (I1 union, `closed=10/100`),
`round-40/wave2/RevC1Counters.defeats.txt` (T7 symlink, `## D2` line 21). All exist.

## 2. Do-nothing controls, run by me

Scratch `/fast/scratch/hyaku/kasegi-r42/RevFreshStart` (removed before yield).

C1:
```
$ bash corpus/instruments/r42-closure.sh                      -> No such file or directory, exit=127
$ bash corpus/instruments/r41-closure.sh   (plain run)        -> exit=2
$ r41-closure.sh --export-ref 5053a7f... (base)               -> selftest cases=12 failures=8 / closed=8/12 exit=1
   I1=1 I2=0 I3=1 I4=1 I5=0 I6=0 I7=1 I8=1 I9=1 I10=1 I11=1 I12=0
$ r41-closure.sh --export-ref 1f74646... (r41 J)              -> selftest cases=12 failures=6 / closed=10/12 exit=1
   I1=1 I2=0 I3=1 I4=1 I5=1 I6=0 I7=1 I8=1 I9=1 I10=1 I11=1 I12=1
```
The base result matches `c1-controls/do-nothing.txt` exactly (8/12, failures=8). The J-head result reproduces the r41
verifier's receipt (`closed=10/12`, `failures=6`). Do-nothing cannot print `closed=13/13 exit=0` (suite absent).

C2 (read-only counters at HEAD): frontier rows 24, F25 rows 0; registry rows 63, S064 rows 0; knowledge 60, entries citing
S064 0; harness `entries=27 pass=27 exit=0` (last PASS line F24); binding `records=55 bound=55 unbound=0`; audit
`expected=60 missing=0 unexpected=0 exit=0`; census exit 0 with W04 S028/S029 only; `corpus/source-snapshots/round-42` absent.
Matches `c2-controls/before.txt`; none of the after-values (25, 64, 1, 61, 28/28, 56/56, 61) is reached.

## 3. Findings

- **F1 (frozen-text error, minor).** `claims.json` C1 `before[0]` says the r41 suite at base prints `closed=10/12 exit=1`.
  The control file and my run both show `closed=8/12` at base; `10/12` is the r41 judged head J. The after-state is
  unreachable either way; the control file is the authoritative value. Cite 8/12 for base in the report and note the
  claims.json wording as an erratum if the lane keeps `errata[]` (currently empty; claims.json is frozen, add to
  `claims-erratum-1`-style file rather than edit).
- **F2 (replay-limb exposure).** Most committed defeat artifacts are prose (`.md`), not executables; only
  `RevC1Counters.defeats.txt` and `CritKillRule.h6-escapes.sh` carry runnable forms. A "replay" of the F-FLIP, F-BIND, F-TABLE
  and F-SCAN artifacts must therefore re-derive the mutation from prose in suite code. The kill rule requires the replay
  limb to exist and not be skipped; it does not require the mutation bytes to be committed. Suggest the build commit each
  replayed mutation as a fixture (mutant manifest, mutated README, pipe-variant SKILL table) so a verifier can run the replay
  without trusting suite-embedded literals.
- **F3 (inherited-coverage drop).** The J1-J13 set does not carry r41's I4 (fence awareness), I11 (eight kill-rule escape
  states) or I2's ref-commit time-basis as separately named checks; J8 covers receipts only. The claims never promised them,
  so this is not narrowing, but a regression of those families would pass an r42 `closed=13/13`. Cheapest cure: have J12
  (or a limb of J8/J11) invoke the r41 suite's I4/I11 on the same export, or state they are retired by r42 explicitly.

## 4. No narrowing checks (to repeat after landing)

At landing, a verifier should confirm: `claims.json` sha256 above unchanged; thirteen `J<n>` payload lines (J1-J13) and thirteen
graded `selftest case=J<n>` lines with `positive=pass`; seven family names F-EVID/F-TOKEN/F-TABLE/F-DECL/F-SCAN/F-BIND/F-FLIP
each tied to a replay limb that is not skipped; C2 counters 25/64/1/61/28-28/56-56/61 and one screened reject with URL, date,
<=25-word located quote; `Correction (round 42)` text that grades any miss, not a re-scoped predicate.
At freeze time (now): no narrowing, `errata: []`.
