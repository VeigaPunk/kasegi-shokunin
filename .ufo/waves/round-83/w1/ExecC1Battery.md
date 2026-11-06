# ExecC1Battery — round-83 C1 scored receipt (frozen counter over frozen candidate)

Seat: `ExecC1Battery` (leaf, battery scorer). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze `0cd499dbdfc0bf9ce3095681af9bc76588d76f31`, base `834bf78eaca70a69294f2ecfefa89b73c3fa85b8`.
Wave: round-83 attempt 1, `w1`, dispatch `counts.spawn` = 13 seats. Scratch
`/fast/scratch/hyaku/kasegi-r83/ExecC1Battery` (removed at exit). No tool installed or upgraded; no lane file,
instrument, corpus file or git/jj state touched (read-only `git rev-parse`/`git status` only). All commands
run from the lane root with `TMPDIR` = scratch.

## Verdicts

| predicate | verdict | exact evidence |
|---|---|---|
| P1 candidate selftest | **holds** | `selftest cases=27 failures=0`, 27 `selftest case=` lines, exit **0** |
| P3 counter over candidate (3 nonces) | **holds** | three runs, each exit **0**, each ending `baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64` |
| P4 forgery controls F6–F11 | **holds** | 12 `FORGERY` lines, byte-identical to the frozen `controls/c1-forgeries-r83.txt` (diff empty) |
| P6 counter selftest | **holds** | `mutbat selftest ok … r83_forgeries={'count': (True, False), 'hashwl': (True, False), 'path': (True, False)}`, exit **0** |
| table rebuild (P3 precondition) | **holds** | `build-table rows=67 neutral=3 new=4`; rebuilt sha == frozen table sha; `cmp` rc **0** |

C1's scored limbs (P1, P3, P4, P6) all hold over the frozen bytes. No claim failure found in this seat's scope.

## 1 — Frozen bytes vs `claims.json`

```
recheck-cwd-census.py sha256=343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9 claims_contains_hash=MATCH
mutbat.py             sha256=2f7c49d44bb1f21e8286d1a8b54d4c57bccc0be990fd7946a57813db0d81cb7d claims_contains_hash=MATCH
mutant-table.json     sha256=5b1d99f59cede6cffa36d554ce7e8256bf1eba1cb84a9591bfbb9f7f386b6f44 claims_contains_hash=MATCH
build-table.py        sha256=890fff2c7fb2b99b6d954306a1f5132c8365d239f34da1da3eec1bbb0ffd0b69 claims_contains_hash=MATCH
```

The four C1 hash literals in `.ufo/waves/round-83/claims.json` are exactly these values (the file's remaining
two literals are the base instrument `81677e9d…` and the C2 snapshot `0a5fa51c…`). The lane tree still carries
the base instrument `corpus/instruments/recheck-cwd-census.py = 81677e9d…`, i.e. landing has not happened;
P3 scored the wave-dir candidate as specified. Receipt: `ExecC1Battery-receipts/hash-compare.txt`.

## 2 — P1: candidate selftest

```
$ TMPDIR=$S python3 -B .ufo/waves/round-83/c1/recheck-cwd-census.py --selftest
selftest case=gate-negpolarity ok neg_ok=False neg_ret_ok=False
selftest case=gate-checkids ok missing=[] extra=[] side_logs=[[True], [True], [True]]
selftest cases=27 failures=0
rc=0
```

27 `selftest case=` lines (== the declared `cases=27`), zero `FAIL` lines, exit 0.
Receipt: `ExecC1Battery-receipts/p1-selftest.log`.

## 3 — P3: frozen counter over frozen candidate, three nonces

Command shape (work dir fresh per run):
`python3 -B .ufo/waves/round-83/c1/mutbat.py --target .ufo/waves/round-83/c1/recheck-cwd-census.py --table .ufo/waves/round-83/c1/mutant-table.json --expect-cases 27 --work $S/m<n> [--seed <nonce>]`

| run | DECOY line | MUTBAT line | rc |
|---|---|---|---|
| `--seed 1` | `DECOY keyed=yes nonce=1 d3_row=K-M2` | `MUTBAT target_sha256=343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9 baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64` | 0 |
| `--seed beef` | `DECOY keyed=yes nonce=beef d3_row=K-CL` | same MUTBAT line (identical bytes, sha `343b21e4…`) | 0 |
| no `--seed` (os.urandom) | `DECOY keyed=yes nonce=ee7c1d186224c2d1 d3_row=G3` | same MUTBAT line (identical bytes, sha `343b21e4…`) | 0 |

Each run printed exactly 67 `MUTANT` lines; verdict tally per run: `KILLED=63 EXCEPTION-KILL=1 NEUTRAL-OK=3`.
All 67 `MUTANT` lines are identical to the frozen candidate receipt `controls/c1-candidate-r83.txt` in all
three runs (sorted diff empty). Non-`verdict=KILLED` lines, all legitimate and counted per the counter's
classifier (no SURVIVED, MISKILLED, DIRTY or NOT-DERIVED row):

```
MUTANT K-M3 verdict=EXCEPTION-KILL rc=1 fails=2 failed_cases=gate-consume,gate-negpolarity counted=yes
MUTANT NT1 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT2 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
MUTANT NT3 verdict=NEUTRAL-OK rc=0 fails=0 failed_cases=- counted=yes
```

The four r82 MutC1Hunt rows are killed by their declared cases on all three nonces (G1 also by `bucket-over`):

```
MUTANT G1 verdict=KILLED rc=1 fails=2 failed_cases=bucket-other,bucket-over counted=yes
MUTANT G2 verdict=KILLED rc=1 fails=1 failed_cases=bucket-over counted=yes
MUTANT G3 verdict=KILLED rc=1 fails=1 failed_cases=main-verbose counted=yes
MUTANT G4 verdict=KILLED rc=1 fails=1 failed_cases=main-verbose counted=yes
```

Receipts: `ExecC1Battery-receipts/p3-seed1.log`, `p3-seedbeef.log`, `p3-noseed.log`.

## 4 — P4: forgery controls (12 FORGERY lines, six drivers, one work dir each)

```
FORGERY F6-selfdiff counter=r82 forgery_sha256=facf90d634511506ab8801ed5148a4dd0a347fdb0c5d4237a7dda1a09595945a rc=1 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=facf90d634511506ab8801ed5148a4dd0a347fdb0c5d4237a7dda1a09595945a baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=63/64
FORGERY F6-selfdiff counter=r83 forgery_sha256=facf90d634511506ab8801ed5148a4dd0a347fdb0c5d4237a7dda1a09595945a rc=1 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=facf90d634511506ab8801ed5148a4dd0a347fdb0c5d4237a7dda1a09595945a baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=63/64
FORGERY F7-wsnorm counter=r82 forgery_sha256=9f344d94b647d60887d12f6f86e1384312dfb5ad42f2e912e89724c734724a4d rc=1 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=9f344d94b647d60887d12f6f86e1384312dfb5ad42f2e912e89724c734724a4d baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=63/64
FORGERY F7-wsnorm counter=r83 forgery_sha256=9f344d94b647d60887d12f6f86e1384312dfb5ad42f2e912e89724c734724a4d rc=1 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=9f344d94b647d60887d12f6f86e1384312dfb5ad42f2e912e89724c734724a4d baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=63/64
FORGERY F8-astembed counter=r82 forgery_sha256=0bc61c9673a4fb41c159a463922bf8b73c5b314be3561d3d572f82a035032271 rc=1 verdicts={"KILLED": 63, "NEUTRAL-OK": 3, "SURVIVED": 1} MUTBAT target_sha256=0bc61c9673a4fb41c159a463922bf8b73c5b314be3561d3d572f82a035032271 baseline=ok rows=67 killed=63 survived=1 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64
FORGERY F8-astembed counter=r83 forgery_sha256=0bc61c9673a4fb41c159a463922bf8b73c5b314be3561d3d572f82a035032271 rc=0 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=0bc61c9673a4fb41c159a463922bf8b73c5b314be3561d3d572f82a035032271 baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64
FORGERY F9-pathlabel counter=r82 forgery_sha256=a071b57b5e5b1d80a7cc6cc57e07a8cd10b7b4cc8dcd7e2d0387a76a81ecf71a rc=0 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=a071b57b5e5b1d80a7cc6cc57e07a8cd10b7b4cc8dcd7e2d0387a76a81ecf71a baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64
FORGERY F9-pathlabel counter=r83 forgery_sha256=a071b57b5e5b1d80a7cc6cc57e07a8cd10b7b4cc8dcd7e2d0387a76a81ecf71a rc=1 verdicts={"NEUTRAL-OK": 3, "SURVIVED": 64} MUTBAT target_sha256=a071b57b5e5b1d80a7cc6cc57e07a8cd10b7b4cc8dcd7e2d0387a76a81ecf71a baseline=ok rows=67 killed=0 survived=64 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64
FORGERY F10-hashwl counter=r82 forgery_sha256=c08bf9a79a84277f022d368e0377471e5342d6865a9fafdef67cf593ed747442 rc=0 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=c08bf9a79a84277f022d368e0377471e5342d6865a9fafdef67cf593ed747442 baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64
FORGERY F10-hashwl counter=r83 forgery_sha256=c08bf9a79a84277f022d368e0377471e5342d6865a9fafdef67cf593ed747442 rc=1 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=c08bf9a79a84277f022d368e0377471e5342d6865a9fafdef67cf593ed747442 baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=63/64
FORGERY F11-count counter=r82 forgery_sha256=646588a233ba05d5c9c41d1df091dc3d6ced3d0c98abe8398066db1aec18ea87 rc=0 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=646588a233ba05d5c9c41d1df091dc3d6ced3d0c98abe8398066db1aec18ea87 baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64
FORGERY F11-count counter=r83 forgery_sha256=646588a233ba05d5c9c41d1df091dc3d6ced3d0c98abe8398066db1aec18ea87 rc=1 verdicts={"KILLED": 64, "NEUTRAL-OK": 3} MUTBAT target_sha256=646588a233ba05d5c9c41d1df091dc3d6ced3d0c98abe8398066db1aec18ea87 baseline=ok rows=67 killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=broken decoy_hidden=63/64
```

Match against P4, clause by clause:

| forgery | P4 requires | measured | matches |
|---|---|---|---|
| F6-selfdiff | rc=1 under both counters | r82 rc=1, r83 rc=1 | yes |
| F7-wsnorm | rc=1 under both counters | r82 rc=1, r83 rc=1 | yes |
| F8-astembed | rc=0 under r83 (recorded limit, not a pass condition) | r83 rc=0; r82 rc=1 (`survived=1`) | yes |
| F9-pathlabel | r82 rc=0, r83 rc=1 with `killed=0` | r82 rc=0 (`killed=64 decoy=ok`), r83 rc=1 (`killed=0 survived=64`) | yes |
| F10-hashwl | r82 rc=0, r83 rc=1 with `decoy=broken` | r82 rc=0 (`decoy=ok`), r83 rc=1 (`decoy=broken`) | yes |
| F11-count | r82 rc=0, r83 rc=1 with `decoy=broken` | r82 rc=0 (`decoy=ok`), r83 rc=1 (`decoy=broken`) | yes |

The 12 lines are byte-identical to the frozen pre-freeze receipt `.ufo/waves/round-83/controls/c1-forgeries-r83.txt`
(`diff` empty). Driver exit code was 0 for every one-name invocation.
Receipt: `ExecC1Battery-receipts/forgeries-execbattery.txt`.

## 5 — P6: counter selftest

```
$ python3 -B .ufo/waves/round-83/c1/mutbat.py --selftest --work $S/st
mutbat selftest ok got={'T-KILL': 'KILLED', 'T-MIS': 'MISKILLED', 'T-SURV': 'SURVIVED', 'T-ABSENT': 'NOT-DERIVED', 'T-EXC': 'EXCEPTION-KILL', 'T-EXCA': 'EXCEPTION-KILL', 'T-NEU': 'NEUTRAL-OK', 'T-NEUBAD': 'NEUTRAL-BROKEN'} counted={'T-KILL': 'yes', 'T-MIS': 'no', 'T-SURV': 'no', 'T-ABSENT': 'no', 'T-EXC': 'yes', 'T-EXCA': 'no', 'T-NEU': 'yes', 'T-NEUBAD': 'no'} all_killed_exit=True location_forgery_exit=False baseline_forgery_exit=False selfdiff_forgery_exit=False r83_forgeries={'count': (True, False), 'hashwl': (True, False), 'path': (True, False)} bad_tables=[True, True, True, True]
rc=0
```

Matches P6 exactly, including the `r83_forgeries` mapping with `(True, False)` for each of `count`, `hashwl`,
`path`. Receipt: `ExecC1Battery-receipts/p6-mutbat-selftest.log`.

## 6 — Table reconstruction

`python3 .ufo/waves/round-83/c1/build-table.py .ufo/waves/round-83/c1/recheck-cwd-census.py $S/t.json`
printed `build-table rows=67 neutral=3 new=4` (the four new rows are `G1 G2 G3 G4`; table classes:
63 assertion + 3 neutral + 1 exception = 67; `extra` sites only on `G4`; `kill_cases` G1 `[bucket-other]`,
G2 `[bucket-over]`, G3/G4 `[main-verbose]`). `cmp $S/t.json .ufo/waves/round-83/c1/mutant-table.json`
exited **0**; both files hash to `5b1d99f5…`. So P3's table is exactly the table the builder derives from the
candidate — the 67-row battery is candidate-derived, not hand-maintained. Receipts:
`ExecC1Battery-receipts/rebuild-table.log`, `rebuild-cmp.txt`, `rebuilt-mutant-table.json`.

## 7 — Observations and residual risk (not claim failures, not routed defects)

1. **F8 remains the open class.** A self-AST-comparing forgery still exits 0 under the r83 counter
   (`F8-astembed counter=r83 rc=0`). C1's P4 declares this a recorded limit rather than a pass condition, so
   it does not falsify the predicate; it is the one live forgery class the nonce-keyed decoys cannot reject.
   Any future round claiming forgery-completeness must not cite P4 as covering AST-identity forgeries.
2. **F6/F7 are rejected by the decoy limb, not by check-row kills.** Both show `decoy=broken` under both
   counters, so their rc=1 says the decoy nonce-keying catches self-source forgeries; it is not independent
   evidence that the 27 selftest cases alone would.
3. **F9's r83 signal is `killed=0`, not a mis-kill.** The path-label forgery reports all 64 rows SURVIVED
   under r83 (rc=1), exactly P4's `killed=0` clause. `decoy=ok` there confirms the rejection is the kill
   tally, not the decoy.
4. **Seed stability.** All three nonces (1, beef, urandom `ee7c1d186224c2d1`) produce the identical MUTBAT
   line and identical 67 MUTANT lines; only `d3_row` varies (`K-M2`, `K-CL`, `G3`). The D3 row selection is
   therefore nonce-dependent as designed, and in all three draws D3 stays `decoy=ok`, so no selected row
   destabilises the counter.
5. **`decoy_hidden=63/64` is constant** across the candidate, the stub and the base under both counters; the
   limb needs `h >= 1` only, so this is a property of the candidate's anchor set under D1 unparse, not a
   weakness signal.
6. **Landing not yet done:** the lane instrument is still `81677e9d…` (base), so P1/P3/P4/P6 here verify the
   wave-dir candidate bytes; the landing-commit re-run remains the L1/integrator's step (the frozen
   `c1-candidate-r83.txt` receipt carries the same lines this seat reproduced).

## 8 — Files written

Only inside this seat's wave dir:
- `.ufo/waves/round-83/w1/ExecC1Battery.md` (this report)
- `.ufo/waves/round-83/w1/ExecC1Battery-receipts/`:
  `hash-compare.txt`, `commands-and-rcs.txt`, `p1-selftest.log`, `p3-seed1.log`, `p3-seedbeef.log`,
  `p3-noseed.log`, `p6-mutbat-selftest.log`, `forgeries-execbattery.txt`, `rebuild-table.log`,
  `rebuild-cmp.txt`, `rebuilt-mutant-table.json`.

No lane tree, corpus, instrument, SKILL/PROVINCE/SCORECARD/LOG, `.ufo/state`, git/jj state, or fleet-repo
file was modified. Scratch dir removed at exit.
