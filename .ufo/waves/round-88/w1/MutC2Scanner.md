# MutC2Scanner — round 88 attempt 1, C2 mutation probe

Seat: MutC2Scanner (leaf, mutation tester). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `6beead91`, freeze `7f2ebebf`, C1 landing `fd33e1bf`, C2 landing `b43dc215` (`landing.json`).

Bytes under mutation: `corpus/instruments/capture-secret-scan.py` at the C2 landing, sha256
`d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417` — byte-equal to
`.ufo/waves/round-88/c2/candidate/capture-secret-scan.py` (P2 pin). Detector: the frozen counter
`.ufo/waves/round-88/c2/capability-check.py`, sha256 `7bf648df5c72bf2e89bbafb1dad1447fc7b45b5ad4caa18c3382368ddf75ecdc`.

Statement of scope: claims are judged only on their frozen predicates. Everything below is a routed
defect / coverage qualifier for round 89, not a re-score of C2.

## Method

For every mutant, exactly as `.ufo/waves/round-88/controls/c2-controls-r88.sh` builds its positive
control: `git clone --shared` of the lane, `checkout` of base `6beead91`, toplevel asserted equal to the
clone, the mutated instrument copied into `corpus/instruments/` beside the frozen
`capture-secret-allow.tsv`, `c2/candidate/scorecard-row.txt` written over SCORECARD.md's single
`| capture-secret-scan |` row, one commit with identity `fixture@invalid`, then

```
python3 -B .ufo/waves/round-88/c2/capability-check.py --lane <clone> --rev HEAD --work <scratch>
```

**without** `--instrument-sha256` and **without** `--gate-sha256`, so K1's selftest is the only byte
check and every other limb must catch the mutation behaviourally.

Each mutation is a single substring replacement (`source.count(old) == 1` asserted before writing); the
mutated instrument's sha256 is recorded in its receipt. 24 mutants, one per line of the table below.

Positivity control first (pristine candidate, same clone recipe, no pins): all six limbs pass, rc=0 —
so a mutant failing a limb is a kill, not a broken harness.

```
BASELINE __baseline__ SURVIVED rev=1fd8442cf05ee2398805f91776aef8e66ff03fac
LIMB K1 pass  LIMB K2 pass  LIMB K3 pass  LIMB K4 pass  LIMB K6 pass  LIMB K5 pass
CAPABILITY-CHECK-RESULT pass rc=0
```

## Result: 24 mutants, 9 killed, 15 survived, 0 inconclusive

No mutant was caught by K2, K3, K5 or K6. K6 reads the fixed `BASE_REV` instrument, so it is
candidate-independent by construction (`claims.json` says so). K5 reads SCORECARD.md, not the
instrument. K2/K3 are unaffected because no mutant changes what the landing tree contains.

| # | mutant (single point) | expected detector | observed | verdict | killing limb (as printed) |
|---|---|---|---|---|---|
| 1 | `_SEP` loses `&amp;` | K1 `azure-html-amp` | `selftest_rc=1` | KILLED | K1 `selftest_rc=1` |
| 2 | `_SEP` loses `\u0026` | K1 `azure-json-escaped`, K4 `live-c.json` | selftest rc=1; K4 `missing=w/z-receipts/live-c.json\|azure-sas-signature` | KILLED | K1, K4 |
| 3 | `_PARAM` intervening bound `{0,20}` -> `{0,1}` | K4 (needs 2+ intervening params) | all limbs pass | **SURVIVED** | — |
| 4 | `_PARAM` name width `[A-Za-z]{2,6}` -> `{2,3}` | K4 (needs a 4-6 letter param name) | all limbs pass | **SURVIVED** | — |
| 5 | `_SIG` floor `{40,}` -> `{64,}` | K1 + K4 | `missing=E1.txt\|azure-sas-signature,live-c.json\|azure-sas-signature`; `files_ok=False` | KILLED | K1, K4 |
| 6 | `_SIG` floor `{40,}` -> `{32,}` | K4 (needs a 32-39 char negative) | all limbs pass | **SURVIVED** | — |
| 7 | `_SIG` drops `(?:=\|%3D){0,2}` | — (equivalent mutant) | all limbs pass; no fixture separates | **SURVIVED (equivalent)** | — |
| 8 | `_SV` -> literal `sv=2022-11-02` | K4 (needs a second service version) | all limbs pass | **SURVIVED** | — |
| 9 | `_SV` -> `sv=\d{4}-\d{2}` | K1 `azure-sv-first`, K4 `E1` | selftest rc=1; `missing=E1.txt\|azure-sas-signature` | KILLED | K1, K4 |
| 10 | alternation loses the sig-first branch | K1 `azure-sig-first`, K4 `live-c.json` | `missing=w/z-receipts/live-c.json\|azure-sas-signature` | KILLED | K1, K4 |
| 11 | alternation loses the sv-first branch | K1 `azure-sv-first`, K4 `E1` | `missing=E1.txt\|azure-sas-signature` | KILLED | K1, K4 |
| 12 | lookbehind deleted | K4 (needs a `sv=` run into a longer name as a negative) | all limbs pass | **SURVIVED** | — |
| 13 | lookbehind `(?<![A-Za-z0-9_])` -> `(?<![A-Za-z0-9])` | K4 (needs an `_sv=` negative) | all limbs pass | **SURVIVED** | — |
| 14 | GCS hex floor `{64,}` -> `{128,}` | K4 (needs a 64-127 hex positive) | all limbs pass | **SURVIVED** | — |
| 15 | GCS hex floor `{64,}` -> `{80,}` | K4 (needs a 64-79 hex positive) | all limbs pass | **SURVIVED** | — |
| 16 | GCS pattern loses `(?i)` | K4 (needs a lower-case name) | all limbs pass | **SURVIVED** | — |
| 17 | GCS name `X-Goog-Signature` -> `X-Goog-Sign` | K1 + K4 | selftest rc=1; `missing=S004.txt\|gcs-signed-url-signature` | KILLED | K1, K4 |
| 18 | GCS separator loses the quote after `:` | K1 `gcs-json-key` | `selftest_rc=1` (K4 has no JSON-key GCS plant and still passes) | KILLED | K1 only |
| 19 | practice scope `len(parts) >= 5` -> `>= 6` | K1 scope case + K4 `E1`/`E2` | `missing=E1.txt\|azure-sas-signature,E2.json\|aws-sts-session-token,E2.json\|credential` | KILLED | K1, K4 |
| 20 | practice scope `parts[:2] == [...]` -> `parts[0] == "corpus"` | K4 (needs an out-of-scope sibling tree negative) | all limbs pass | **SURVIVED** | — |
| 21 | practice scope `parts[3] == "evidence"` -> `parts[-2] == "evidence"` | K4 (needs a deeper-than-`<pkg>/evidence/` negative) | all limbs pass | **SURVIVED** | — |
| 22 | selftest deletes `gcs-json-key` | K1 (only if it pins case names/count) | `SELFTEST-RESULT pass cases=32` vs pristine `cases=33`, rc=0, all limbs pass | **SURVIVED** | — |
| 23 | selftest deletes `azure-html-amp` | K1 (only if it pins case names/count) | `cases=32`, all limbs pass | **SURVIVED** | — |
| 24 | selftest prints `cases=0` | K1 (only if it pins the count) | `SELFTEST-RESULT pass cases=0`, all limbs pass | **SURVIVED** | — |

Per-mutant counter stdout (LIMB lines, rev, mutated instrument sha256): `MutC2Scanner-receipts/<mutant>.txt`
(25 receipts; `__baseline__.txt` is the positivity control).

Reading of the kill pattern: K1's selftest is the only limb with ground on `&amp;` and on the GCS
colon/JSON-key form (mutants 1, 18 are K1-only kills); K4's plants give a second, independent kill for
everything the plants actually exercise (mutants 2, 5, 9, 10, 11, 17, 19). Every survivor is exactly a
point where neither limb has ground.

## Survivors: the planted case that would kill each one

Probe = both instruments (frozen and mutant) run on one generated fixture; every probe below
**separates** (frozen and mutant disagree), so the stated plant is a working kill case. Fixture bodies
are generated at runtime; receipts carry rc and shape-level HIT/summary lines only.

| survivor | killing planted case (in the counter's K4 fixture) | limb that would then fire | probe (frozen vs mutant) |
|---|---|---|---|
| #3 `param-bound-1` | positive `corpus/practice/p/evidence/E3.txt`: `?sv=2022-11-02&ss=b&srt=sco&sp=rwdlac&se=…&sig=<51 base64 chars>` — four intervening parameters (the S127:605 ordering) | K4 `missing` (mutant loses the hit) | rc1/HIT vs rc0/none |
| #4 `param-name-max3` | positive `…/E3.txt`: `?sv=2022-11-02&skoid=<guid>&sig=<51 base64 chars>` (a 5-letter intervening name) | K4 `missing` | rc1/HIT vs rc0/none |
| #6 `sig-threshold-32` | **negative** `corpus/source-snapshots/round-1/S008.txt`: `?sv=2022-11-02&sig=<35 base64 chars>` expected to yield no hit | K4 `extra` (mutant invents a hit) | rc0/none vs rc1/HIT |
| #7 `sig-padding-drop` | none exists — equivalent mutant; see below | — | no separation on either padding form |
| #8 `sv-hardcoded-version` | positive `…/E3.txt`: `?sv=2024-11-04&sr=b&sig=<51 base64 chars>` | K4 `missing` | rc1/HIT vs rc0/none |
| #12 `lookbehind-drop` | **negative** `S008.txt`: `?mysv=2022-11-02&sig=<51 base64 chars>` (no Azure SAS: `sv` is not a parameter) | K4 `extra` | rc0/none vs rc1/HIT |
| #13 `lookbehind-allow-underscore` | **negative** `S008.txt`: `?_sv=2022-11-02&sig=<51 base64 chars>` | K4 `extra` | rc0/none vs rc1/HIT |
| #14 `gcs-threshold-128` | positive `S009.txt`: `X-Goog-Signature=<96 hex>` | K4 `missing` | rc1/HIT vs rc0/none |
| #15 `gcs-threshold-80` | positive `S009.txt`: `X-Goog-Signature=<72 hex>` | K4 `missing` | rc1/HIT vs rc0/none |
| #16 `gcs-nocase` | positive `S009.txt`: `x-goog-signature=<128 hex>` (lower-case name) | K4 `missing` | rc1/HIT vs rc0/none |
| #20 `scope-prefix-loose` | **negative** `corpus/practice2/p/evidence/F.txt` (a sibling corpus tree, out of scope) carrying a credential-shaped value | K4 `extra` | rc0/none vs rc1/one `credential` hit |
| #21 `scope-evidence-not-parts3` | **negative** `corpus/practice/p/sub/evidence/F.txt` (deeper than `<pkg>/evidence/`) | K4 `extra` | rc0/none vs rc1/one `credential` hit |
| #22 `selftest-drop-gcs-json-key` | no plant can kill it: behaviour is unchanged. Kill = K1 asserting the selftest case set (`SELFTEST gcs-json-key ok` present, or `cases=33`) | K1 (strengthened) | `cases=33` vs `cases=32`, both `pass` |
| #23 `selftest-drop-azure-html-amp` | same: K1 must pin case names/count. Compounding risk: `&amp;` has **no** K4 ground (mutant #1 was a K1-only kill), so deleting this case makes the `&amp;` limb unpinned twice over | K1 (strengthened) | `cases=33` vs `cases=32`, both `pass` |
| #24 `selftest-case-count-zero` | K1 asserting `SELFTEST-RESULT pass cases=33` | K1 (strengthened) | `cases=33` vs `cases=0`, both `pass` |

### #7 `sig-padding-drop` is an equivalent mutant, not a coverage gap

`(?:=|%3D){0,2}` can never *enable* a match that `[A-Za-z0-9%+/]{40,}` does not already make:
`%3D` is three characters inside the value class (`%`, `3`, `D`), so percent-encoded padding is
consumed by the `{40,}` run; a literal `=` is not required for a match, only consumed when present.
Both padding fixtures hit identically with and without the group. Recommendation for r89: drop the
dead group, or keep it and note in the docstring that it only widens the reported match — as written
it is unreachable weight.

## What this adds to ReviewC2Scanner

`ReviewC2Scanner` (F1/F2) showed from the *fix* direction that the counter cannot see a `\u0026`-position
lookbehind defect and that any GCS floor in 33..128 passes. This probe confirms it from the *mutant*
direction and pins the exact unpinned points:

* #12 `lookbehind-drop` passes K1-K6. It also **cures** ReviewC2Scanner F1: on the JSON-escaped SAS whose
  `sv=` follows a `\u0026` escape, the frozen instrument returns rc=0 (miss) and this mutant rc=1 (hit).
  So this survivor cannot be killed by any correct positive ground — only the negative plant in the table
  separates frozen from mutant. F1 is therefore invisible in both directions, which is exactly F2's claim.
* #14/#15: the GCS floor is not pinned where the claim puts it. K1's `gcs-short` negative is 32 hex, so a
  floor of 33 still passes K1; K4's doc-wrapped negative contributes only a 12-hex first segment, and its one
  positive is 128 hex, so a floor of 129 would fail K4 `missing` while 128 passes. The whole window
  **33..128 passes K1-K6** (empirical upper witnesses: `{80,}` and `{128,}` both survive), which is exactly
  the range `ReviewC2Scanner` F2 predicted; the frozen 64 is not a boundary either limb tests.
* #16: case-insensitivity is claimed behaviour (`(a)` survey: "in lower and upper case") but is unpinned —
  no selftest case and no K4 plant uses a lower-case `x-goog-signature`.
* #3/#4: K4's Azure plants exercise exactly **one** intervening parameter and only 2-3 letter parameter
  names (`sr`, `se`, `sp`, `spr`, `sv`, `st`, `sig`), so both bounds of `_PARAM` are unbound: the bound can
  collapse to 1 and the name alphabet to 2-3 letters and the counter still passes.
* #8: every Azure fixture (K1 and K4) uses `sv=2022-11-02`, so the year/month/day shape is not what K1-K6
  test — a literal version pin survives.
* #6: there is no 32-39 character `sig=` negative anywhere, so the 40-char floor can be lowered to 32
  (the 12-char `azure-short-sig` selftest case is the only short-sig negative).
* #20/#21: the practice-scope predicate is only pinned by its positive form; both relaxations
  (any `corpus/` prefix, evidence at any depth) pass all six limbs.
* #22-#24: the new selftest cases are the sole ground for `&amp;`, the GCS colon form and the GCS JSON-key
  form, and their presence is not checked — K1 asserts only the substring `SELFTEST-RESULT pass`.

## Hygiene, restoration and reproducibility

* No lane, fleet or sibling-lane write. No git mutation anywhere in the lane: every clone, commit and
  probe ran in `/fast/scratch/hyaku/kasegi-r88/MutC2Scanner/` and is deleted before yield.
* No fixture bytes and no matched value in any wave file: receipts contain `LIMB`/`HIT`/summary lines
  (shape names and paths only) and sha256 digests. No scanner, counter or `S<digits>.txt` snapshot copied.
  Self-check with the landing instrument, run over this report and every file in `MutC2Scanner-receipts/`:
  `mode=files scanned=30 hits=0 files=0 rc=0`.
* Restoration evidence (the frozen bytes were never mutated in place; these are the before/after checks):

```
before: sha256(corpus/instruments/capture-secret-scan.py) = d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417
        git show b43dc215:corpus/instruments/capture-secret-scan.py | sha256sum = d7349536…5417
after : sha256(corpus/instruments/capture-secret-scan.py) = d73495364f90f78fa5ee6ad28b83fce772a349a5339d240b21db4d5d04425417
        git -C <lane> status --porcelain --untracked-files=no  -> (empty)
```

`before` and `after` are byte-identical to each other and to the C2 landing blob; no tracked lane file
changed, so there was nothing to restore.

* Re-runnable: `MutC2Scanner-receipts/repro-mutants.py` rebuilds baseline, all 24 mutants and all survivor
  probes from pattern text only (fixtures generated at runtime; nothing credential-shaped is stored).

```
S=/fast/scratch/hyaku/kasegi-r88/MutC2Scanner; mkdir -p "$S"
python3 -B .ufo/waves/round-88/w1/MutC2Scanner-receipts/repro-mutants.py --work "$S" --all
```

The shipped script's own run is `MutC2Scanner-receipts/repro-output.txt` (script sha256
`fa40cd156c8a111d46dbb059207b4ed5dde61f84603f8ecaca36f64aa75e8a2a`, the file in this directory):
one baseline + 24 `MUTANT` lines with the same 9/15 split, 19 `PROBE` lines of which 17 separate and 2
are the expected non-separations of the equivalent mutant, ending `REPRO pass`.

## Files written

* `.ufo/waves/round-88/w1/MutC2Scanner.md` (this report)
* `.ufo/waves/round-88/w1/MutC2Scanner-receipts/` — 25 counter receipts (`<mutant>.txt`,
  `__baseline__.txt`), `repro-mutants.py`, `repro-output.txt` (that script's own `--all` run, `REPRO pass`),
  `sweep.json` (machine-readable verdicts), `probes.json` (survivor probe outputs)
