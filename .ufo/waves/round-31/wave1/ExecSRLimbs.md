# ExecSRLimbs — round 31, C1 source-recheck limbs (SR-stem-mismatch, SR-occurrence-not-unique)

Seat: ExecSRLimbs (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope).
Round 31 / wave 1. Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze `738a77999a00efbca129cfccb28a481037f6241f`.
Answering model: `devin/deepseek-v4-1-flash` (runtime config route table decides; no model was passed).
Tools installed/upgraded: none. pacman transactions: none. Network fetches: none (local fixtures only). git/jj mutations: none (read-only `git log`, `git status` only).

Assigned subject: `corpus/instruments/source-recheck.py`, `corpus/instruments/limb-fixtures/sr/**`, `.ufo/waves/round-31/wave1/ledger-fragments/sr.json`.
Interface contract coded to (L1-frozen): LIMB rows `{id, instrument, find, replace, kill, live_exit, signal, note}`; kill command `python3 {inst} --manifest <fixture manifest> --source <id>` run from `{root}`; `live_exit 1`; signals `reason=stem-mismatch` / `reason=occurrence-not-unique`.

## 1. Pre-state (PRE-STATE — do not read as an after column)

```
$ git log --oneline -1
b374feb round-28: canonical wave results (kasegi-r28-build-results.json, 69 seats)
$ sha256sum corpus/instruments/source-recheck.py          # before this seat's edit
33602a9df53a4cadd7b7aa2b6ccea9b25235888799a3b71e87906de1fc622c6f  corpus/instruments/source-recheck.py
$ ls corpus/instruments/limb-fixtures
ls: cannot access 'corpus/instruments/limb-fixtures': No such file or directory
```

`33602a9d…` equals the C1 `do_nothing_control` prefix in `.ufo/waves/round-31/claims.json` and `.ufo/waves/round-31/c1-controls/base-instrument-digests.txt`. No fixture directory and no ledger fragment existed. Re-run for the after column: sections 3–9 below.

## 2. Files written (this seat)

| Path | sha256 |
|---|---|
| `corpus/instruments/source-recheck.py` | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| `corpus/instruments/limb-fixtures/sr/stem-mismatch/SFIX-STEM-capture.txt` | `856fc6bf9c9fb95d29aa7f28f413778ebc17744fa5ea088a4c54768082dfa620` |
| `corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json` | `151c64b193fc89972d0389082f4ed8e352be6160ab4cd8f70f58094ed76d7cf9` |
| `corpus/instruments/limb-fixtures/sr/occurrence-not-unique/SFIX-REPEAT.txt` | `a1a041334372a0539c928f0260999051dab3a04415c972174c21f0e4e7bbf723` |
| `corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json` | `923d63dde18cce2acdf626990063bdbed1147abf3487f51ff610feaab30cbe92` |
| `.ufo/waves/round-31/wave1/ledger-fragments/sr.json` | `4f7dc1e317d78a0f48814ec939cda4ee71a743e4f85c1932fa830334496d3e00` |
| `.ufo/waves/round-31/wave1/ExecSRLimbs-scratch/proof.txt` | `83d39f8b76067471433e78ce7f96c0b935e899311c4e9a40d26d8ec9fae14a57` |
| `.ufo/waves/round-31/wave1/ExecSRLimbs-scratch/rechecks.txt` | `afbe3ace6ca190d8b93984c61f316dee0d33c5c958f24ca7249f67b0cbddd93d` |
| `.ufo/waves/round-31/wave1/ExecSRLimbs-scratch/kill-sim.txt` | `a6ec98ed5f5bf958f6a26b95b7d91324b60717e5293cb7aa678570947eefe35c` |
| `.ufo/waves/round-31/wave1/ExecSRLimbs.md` (this receipt) | printed at the end of the seat run |

Scratch mutant copies (never lane instrument bytes): `pristine.py` `fd2e01e8…`, `mutant-SR-stem-mismatch.py` `6302635b…`, `mutant-SR-occurrence-not-unique.py` `8477c0cd…`, `mutant-accept-not-found.py` `ed61d817…`.

Instrument change: one added selftest case (`quote-absent`) plus its help-text word. No production-path code changed; the B1/B2 limbs are untouched and their find texts occur exactly once.

## 3. Fixtures — the isolating pair (closes M30-1)

`stem-mismatch` — record id `SFIX-STEM`, capture `SFIX-STEM-capture.txt` (stem ≠ id), sha256 pin **correct**, quote unique:

```
$ cat corpus/instruments/limb-fixtures/sr/stem-mismatch/SFIX-STEM-capture.txt
Fixture capture for the isolating stem-mismatch limb.
The pinned sentence appears here exactly once.
Isolating stem limb fixture quote.
Trailing filler line for line numbering.
$ cat corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json
{"note": "...", "schema_version": 1, "sources": [{"id": "SFIX-STEM", "path": "SFIX-STEM-capture.txt",
 "quotes": [{"id": "Q1", "location": "fixture line 3", "quote": "Isolating stem limb fixture quote."}],
 "sha256": "856fc6bf9c9fb95d29aa7f28f413778ebc17744fa5ea088a4c54768082dfa620"}]}
```

`occurrence-not-unique` — capture stem **equals** the record id (`SFIX-REPEAT.txt` / `SFIX-REPEAT`), quote occurs exactly twice, **no anchor**:

```
$ cat corpus/instruments/limb-fixtures/sr/occurrence-not-unique/SFIX-REPEAT.txt
Repeated unanchored fixture quote.
Padding line one.
Padding line two.
Repeated unanchored fixture quote.
Padding line three.
$ grep -c "Repeated unanchored fixture quote." corpus/instruments/limb-fixtures/sr/occurrence-not-unique/SFIX-REPEAT.txt
2
$ cat corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json
{"note": "...", "schema_version": 1, "sources": [{"id": "SFIX-REPEAT", "path": "SFIX-REPEAT.txt",
 "quotes": [{"id": "Q1", "location": "fixture lines 1 and 4", "quote": "Repeated unanchored fixture quote."}],
 "sha256": "a1a041334372a0539c928f0260999051dab3a04415c972174c21f0e4e7bbf723"}]}
```

Isolation argument: the round-30 frozen B2 fixture (`round-30/c1-controls/mutants/b2iso/manifest.json`, id `S045`, path `S045.txt`) is stem-correct, but the *committed* B2 record in the round-30 manifest was id `S045` with path `B2.txt`, so B1 exited first (M30-1). The new B2 fixture cannot route through B1 (stem equal, pin correct), and the new B1 fixture cannot route through B2 (quote occurs once). Both fixtures are inert to other instruments: no instrument globs `corpus/**/manifest.json` (`grep -rn "rglob\|glob(" corpus/instruments/*.py` shows only `corpus/knowledge/*.md` in `recheck-audit.py`), and the fleet census reads only `corpus/SOURCES.md`.

## 4. Live kill-command runs on landed bytes (after column)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json --source SFIX-STEM
SFIX-STEM:manifest MISMATCH reason=stem-mismatch
stem_live_exit=1
$ python3 corpus/instruments/source-recheck.py --manifest corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json --source SFIX-REPEAT
SFIX-REPEAT:sha256 OK
SFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique
repeat_live_exit=1
```

Both match their `live_exit` and `signal`. `SFIX-REPEAT:sha256 OK` shows the B2 run got past B1 and the byte pin.

## 5. One-limb mutant proofs (scratch copies only; `py_compile` ok on each)

Find/replace are the exact strings in `ledger-fragments/sr.json`; each find count asserted `== 1` before patching; every mutant was also cross-run on the *other* fixture to show it flips only its own limb (`proof.txt`):

```
live instrument corpus/instruments/source-recheck.py sha256=fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003
== live (lane bytes) ==
[stem] exit=1 stdout='SFIX-STEM:manifest MISMATCH reason=stem-mismatch' stderr=''
[repeat] exit=1 stdout='SFIX-REPEAT:sha256 OK\nSFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique' stderr=''
== one-limb mutants ==
mutant SR-stem-mismatch: sha256=6302635bf94d9012746b6190851750a00b80ddd1473a56ba516ba67c3049c01b py_compile=ok
  [stem OWN] exit=0 stdout='SFIX-STEM:sha256 OK\nSFIX-STEM:Q1 OK occurrences=1' stderr=''
  [repeat other] exit=1 stdout='SFIX-REPEAT:sha256 OK\nSFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique' stderr=''
mutant SR-occurrence-not-unique: sha256=8477c0cdc46f1e4b9d51d4b5e902fc0166bea6247ae72fec675d8f597f7da636 py_compile=ok
  [stem other] exit=1 stdout='SFIX-STEM:manifest MISMATCH reason=stem-mismatch' stderr=''
  [repeat OWN] exit=0 stdout='SFIX-REPEAT:sha256 OK\nSFIX-REPEAT:Q1 OK occurrences=2 anchor=MISSING' stderr=''
== verdict table ==
SR-occurrence-not-unique   repeat  exit=0
SR-occurrence-not-unique   stem    exit=1
SR-stem-mismatch           repeat  exit=1
SR-stem-mismatch           stem    exit=0
live                       repeat  exit=1
live                       stem    exit=1
== assertions ==
PASS live stem exit 1 with reason
PASS live repeat exit 1 with reason
PASS mutant SR-stem-mismatch own fixture flips to 0
PASS mutant SR-stem-mismatch leaves repeat at 1
PASS mutant SR-occurrence-not-unique own fixture flips to 0
PASS mutant SR-occurrence-not-unique leaves stem at 1
ALL_ASSERTIONS_OK=True
```

Mutant texts: B1 `    if Path(path).stem != source_id:` → `    if False:  # SR-stem-mismatch mutant: B1 stem check dropped`; B2 `        if occurrences > 1 and anchor_verdict_result != "ok":` → the same condition plus `and anchor_verdict_result != "missing"` (so out-of-range/broken anchors still fail and only the occurrence-not-unique limb is dropped).

## 6. Do-nothing control — limbs absent (round-30 freeze bytes)

```
$ sha256sum .ufo/waves/round-30/c1-controls/mutants/freeze-source-recheck.py
9fe6a4a07fdbbd83a9b64a588a14d02b154fd5de81e460b97519675d69a79b96  freeze-source-recheck.py
[stem]   exit=0 stdout='SFIX-STEM:sha256 OK\nSFIX-STEM:Q1 OK occurrences=1' stderr=''
[repeat] exit=0 stdout='SFIX-REPEAT:sha256 OK\nSFIX-REPEAT:Q1 OK occurrences=2 anchor=MISSING' stderr=''
PASS freeze bytes pass both fixtures (0,0) - limbs absent
```

The pre-limb bytes pass both fixtures (red-before), so each fixture's failure on landed bytes is attributable to the limb under test.

## 7. Counter-semantics simulation with `{inst}`/`{root}` (fresh scratch lane)

`corpus` (3.3 MB, 194 entries) copied to `mktemp -d`; kill command substituted and run with cwd = scratch root; scratch removed at the end:

```
scratch lane root=/tmp/sr-kill-sim-63s7_z3g (corpus copied, 194 entries)
SR-stem-mismatch live: exit=1 sig=y stdout='SFIX-STEM:manifest MISMATCH reason=stem-mismatch' stderr=''
  cmd=python3 /tmp/sr-kill-sim-63s7_z3g/corpus/instruments/source-recheck.py --manifest /tmp/sr-kill-sim-63s7_z3g/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json --source SFIX-STEM
  find-count=1
SR-stem-mismatch mutant: exit=0 sig=n stdout='SFIX-STEM:sha256 OK\nSFIX-STEM:Q1 OK occurrences=1' stderr=''
SR-stem-mismatch verdict=killed
SR-occurrence-not-unique live: exit=1 sig=y stdout='SFIX-REPEAT:sha256 OK\nSFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique' stderr=''
  find-count=1
SR-occurrence-not-unique mutant: exit=0 sig=n stdout='SFIX-REPEAT:sha256 OK\nSFIX-REPEAT:Q1 OK occurrences=2 anchor=MISSING' stderr=''
SR-occurrence-not-unique verdict=killed
scratch removed=True
SIM_ALL_OK=True
```

## 8. Selftest on landed bytes, and the M5 strengthening

```
$ python3 corpus/instruments/source-recheck.py --selftest
SELFTEST clean PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST corrupt PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256 observed-ids=S900:sha256
SELFTEST missing-source PASS expected-exit=2 observed-exit=2 expected-ids=S900:source observed-ids=S900:source
SELFTEST missing-manifest PASS expected-exit=2 observed-exit=2 expected-ids=manifest observed-ids=manifest
SELFTEST stem-mismatch PASS expected-exit=1 observed-exit=1 expected-ids=S901:manifest observed-ids=S901:manifest
SELFTEST double-occurrence PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-anchored PASS expected-exit=0 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-out-of-range PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST double-occurrence-broken PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
SELFTEST quote-absent PASS expected-exit=1 observed-exit=1 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
selftest cases=10 failures=0
selftest_exit=0
$ python3 -c "import py_compile;py_compile.compile('corpus/instruments/source-recheck.py',doraise=True);print('compile_ok')"
compile_ok
```

`cases=9+` holds at 10. The new case is an adjacent strengthening requested by attack seat `MutSRExisting`, which measured a survivor (M5: the final `else` flipped to `OK`/`status=0` still passed all 9 cases because no case exercised `reason=quote-not-found`). The case asserts the whole line `S900:Q1 MISMATCH reason=quote-not-found`, so a status-label-only flip also dies:

```
== M5 strengthening (accept a not-found quote) ==
mutant M5: sha256=ed61d8175ca8f1e10d268c7e47c03cadaf6750681ad2db3a92f6142ec282e239 py_compile=ok
  pristine selftest exit=0 selftest cases=10 failures=0 fail_lines=[]
  M5 selftest exit=1 selftest cases=10 failures=1 fail_lines=['SELFTEST quote-absent FAIL expected-exit=1 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1']
```

This is instrument-selftest hardening, not one of the 13 frozen ledger limbs; no limb was relabelled.

## 9. Every recheck registered on manifests rounds 23–30 (each `--source`)

Enumerated from `corpus/source-snapshots/*/manifest.json` and run one `--source` at a time from the lane root (`rechecks.txt`):

```
round-23: records=4 pass=4 fail=0 ids=S018,S029,S030,S031
round-24: records=19 pass=19 fail=0 ids=S001,S002,S003,S004,S005,S006,S007,S008,S009,S010,S011,S012,S013,S014,S015,S032,S033,S034,S035
round-25: records=5 pass=5 fail=0 ids=S036,S037,S038,S039,S040
round-26: records=1 pass=1 fail=0 ids=S041
round-28: records=2 pass=2 fail=0 ids=S041,S042
round-29: records=3 pass=3 fail=0 ids=S043,S044,S045
round-30: records=3 pass=3 fail=0 ids=S041,S046,S047
TOTAL source runs=37 failures=0
ALL_PASS=True
```

(34 runs for rounds 23–29 plus 3 for round-30 — the same set the round-30 lesson counted as passing.) Round-31's manifest is `ExecCapManifest`/`ExecEntryF15`'s subject (S048) and is out of this seat's scope; it is not claimed here.

## 10. Ledger fragment (final)

`.ufo/waves/round-31/wave1/ledger-fragments/sr.json` — JSON array of the two LIMB rows, exactly the contract keys:

```json
[
  {"id": "SR-stem-mismatch", "instrument": "corpus/instruments/source-recheck.py",
   "find": "    if Path(path).stem != source_id:\n",
   "replace": "    if False:  # SR-stem-mismatch mutant: B1 stem check dropped\n",
   "kill": "python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json --source SFIX-STEM",
   "live_exit": 1, "signal": "reason=stem-mismatch", "note": "..."},
  {"id": "SR-occurrence-not-unique", "instrument": "corpus/instruments/source-recheck.py",
   "find": "        if occurrences > 1 and anchor_verdict_result != \"ok\":\n",
   "replace": "        if occurrences > 1 and anchor_verdict_result != \"ok\" and anchor_verdict_result != \"missing\":  # SR-occurrence-not-unique mutant\n",
   "kill": "python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json --source SFIX-REPEAT",
   "live_exit": 1, "signal": "reason=occurrence-not-unique", "note": "..."}
]
```

`find` counts on the landed bytes: 1 and 1. Told `ExecLedgerMerge` (shape, digest, both killed) and `ExecCounter` (subject digest, fixture paths inside `corpus`). Also notified `MutSRExisting` (M5 closure) and `ScribeInstrReadme` (append facts).

## 11. M30-1 disposition

Closed for this instrument: the ledger's B2 row runs on a **stem-correct** capture (`SFIX-REPEAT.txt` == record id `SFIX-REPEAT`), so B1 cannot preempt; the B1 row runs on a **unique-quote** fixture, so B2 cannot preempt; and each mutant was cross-run on the other fixture (section 5) to show the two limbs are independent. The round-30 frozen fixture bytes were not edited (they are freeze evidence).

## 12. Bounds compliance

- Writes only under the lane: the five owned production paths, the fragment, seat scratch `wave1/ExecSRLimbs-scratch/`, and this receipt. No write to the fleet root, sibling lanes, `shokuknow`, `templates/`, `scripts/`, `.ufo/state/`, `MANIFEST.json`, or `.scratch/`.
- No git/jj mutation in the lane (read-only `git log` / `git status`); mutants and kill-simulations ran in `mktemp -d` scratch trees and lane-local scratch, both outside the lane instrument bytes; the kill-sim scratch tree was deleted.
- No pacman transaction, no tool install, no background job, no delegation, no `agent://all` message, no live bounty-target contact, no credentials read or written.
- Counter never writes into the lane on this seat's side: my kill commands are read-only `--manifest/--source` runs; the fixture files are inputs.

## 13. Risks and boundaries (for the L1 / merge seat)

1. **Instrument digest moved** `33602a9d…` → `fd2e01e8…` (selftest case only). Any seat or control that treats `33602a9d…` as "landed after" must re-measure on `fd2e01e8…` (M30-2 discipline). `.ufo/waves/round-31/c1-controls/base-instrument-digests.txt` is a pre-state record and was not touched.
2. **Selftest count is 10, not 9.** Receipts citing `source-recheck.py --selftest cases=9 failures=0` as the *current* state are stale; the claim's clause is `failures=0`, which holds.
3. **Family counters not run here.** `recheck-audit.py --quiet` (ExecRALimbs) and `frontier-recheck-count.py` (ExecFRLimbs) were being edited by their owners during this seat's run; their outputs would be non-comparative (M30-3) and are the parent's closure commands. I did not cite them.
4. **Fixture ids are synthetic** (`SFIX-*`), outside the `S0xx` registry namespace, and live under `corpus/instruments/limb-fixtures/`, not `corpus/source-snapshots/`; the census reads only `corpus/SOURCES.md`, so no registry/census effect is expected. This seat did not run the census (C2's counter).
5. **Counter contract dependence:** the rows assume the counter substitutes `{inst}` and `{root}` and runs the kill command with cwd = scratch lane root. The simulation in section 7 used exactly that form; if `ExecCounter` substitutes differently (e.g. relative `{root}`), the fixture manifest path must still resolve inside the copied `corpus`.
6. No claim is made here about C1/C2 scores or the merged ledger summary lines (`limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`); those are `ExecLedgerMerge`/`ExecCounter` outputs on the merged ledger.

## 14. Independent post-fix confirmation (other seat's measurement, reported not rerun)

`MutSRExisting` re-ran its 5-mutant probe on this receipt's landed bytes, verifying `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` before and after with the lane untouched: **5/5 mutants killed, survivors=0**. M5 dies on the new `quote-absent` case alone (`SELFTEST quote-absent FAIL expected-exit=1 observed-exit=0`); M1–M4 killer sets unchanged; `quote-absent` kills neither M1 nor M2, so the B1/B2 independence verdict is unchanged on the 10-case selftest. All six of its find strings (including the 3-line B1 block and the 9-line B2 block) still occur exactly once on the new bytes. Post-fix section: `.ufo/waves/round-31/wave1/MutSRExisting.md` (pre-fix `33602a9d…` vs post-fix `fd2e01e8…` labeled). This seat did not rerun that probe.

## 15. Counter integration confirmation (ExecCounter's measurement, reported not rerun)

`ExecCounter` assembled `ra.json` + `sr.json` + `fr.json` into a throwaway ledger and ran the counter on the lane bytes (counter sha256 `cde7c2b6f74888dd2a841179002ad8583c3f57b4407db94b489063ce2747f275`, subject `source-recheck.py` `fd2e01e8…`): `SR-stem-mismatch live=1/y mutant=0/n verdict=killed`, `SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed`, overall `limbs=13 killed=13 survivors=0`, exit 0, 8.9 s. It confirms the `--manifest {root}/...` form is what the scratch substitution supports and that the fixtures travel with the corpus copytree. The landed 13+3 run remains `ExecLedgerMerge`'s output; this seat did not rerun the merged counter.
