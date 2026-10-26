# ExecRegressionC1 — round-33 final C1 counters on quiescent bytes

- Seat: `ExecRegressionC1` (executor, leaf). Role: final regression run for claim **C1** (`depth:verifiability`, held 4).
- Round 33 / wave 1, lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims-freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`.
- Answering model I actually ran on: `opencode-go/deepseek-v4.1-flash` (route table; no model passed by me).
- Measurement window: **2026-10-26T04:31Z–04:34Z** (local 01:31–01:34 -03), after all three subjects landed and after a 45 s quiescence probe.
- Writes made: this receipt + raw outputs in `wave1/ExecRegressionC1/` only. No lane/Git/jj mutation; no campaign tools in `shokuknow`; no tool installs or upgrades (nothing needed — stdlib Python 3 only). Scratch `$HYAKU_SCRATCH/kasegi-r33/ExecRegressionC1` removed at exit (§7).

## 0. Quiescence of the measured bytes (rule 6 / M30-3)

Waited for `wave1/ExecCaptureBinding.md`, `wave1/ExecManifestUpgrade.md`, `wave1/ExecManifest32.md`, then additionally for `ExecRegistryAppend.md`, `ScribeInstrReadme.md`, `ScribeSkillGate.md`, `ScribeProvince.md`, `ScribeReadmeF16.md`, `ExecEntryF16.md`, `ExecExpectedList.md` (the bytes my counters read), then `sha256sum` sampled twice 45 s apart: identical (`q1.txt` == `q2.txt`, `QUIESCENT`), and identical again after all counter runs (`q3.txt`, `LANE_UNCHANGED_BY_COUNTERS=YES` — the checker never writes into the lane).

Input digests at measurement time (`ExecRegressionC1/q2.txt`):

```
b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b  corpus/SOURCES.md                     (50 rows)
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84  SKILL.md
b57de5d9517d0ba67a7317d66f5ccc270b4e4a206ace8f27e20e9ec964abd679  PROVINCE.md
15dd603ec3cb47fa9dc181f2010790a858c437dedc2184ffcd1fe0eae40139ba  corpus/instruments/README.md
3f68b9a2ff7db654770bc11cb3b178b3d2920cc8e5ca0ba9761d85a65ab81ceb  corpus/instruments/knowledge-expected.txt
53c48b3b322aa4e5f90e1bae27ad0c1fb60c3452b2cff1e35a52e3276bb60a48  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774  corpus/source-snapshots/round-32/manifest.json
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py   (492 lines)
```

Legacy manifests (`sha256sum corpus/source-snapshots/*/manifest.json`) match the digests ExecManifestUpgrade and ExecManifest32 reported: round-23 `1f6d4fb5…`, round-24 `77b158ca…`, round-25 `251cb5b2…`, round-26 `1c913132…`, round-28 `89f51e05…`, round-29 `b24a485f…`, round-30 `8aacf77c…`, round-31 `5fa37fd7…`, round-32 `6e4e719a…`.

At measurement time `SCORECARD.md` (`6224ab87…`) and `corpus/lessons/round-33.md` had **not** landed (no `ScribeScorecard.md` / `ScribeLesson.md` receipt). Neither file is an input to any counter below; see §5 D-R33-2.

## 1. Gate results

| # | Gate (item wording) | Measured | Verdict |
|---|---|---|---|
| 1 | binding `records=40 bound=40 unbound=0`, exit 0, twice byte-identical | `records=40 bound=40 unbound=0`, `run1_exit=0 run2_exit=0`, `stdout_byte_identical=YES`, stdout sha256 `1861fec8…a3c5a9f1` on both runs | **PASS** |
| 2 | `--selftest` cases>=6 failures=0 exit 0 | `selftest cases=11 failures=0`, `selftest_exit=0` | **PASS** |
| 3 | fake checker must be rejected by the kill rule | fake prints `records=40 bound=40 unbound=0`, `fake_exit=0` on the FINAL manifests — rejected: on identical bytes where the summary is false (base tree) it prints `records=38 bound=38 unbound=0` exit 0 while the real checker prints `records=38 bound=0 unbound=38` exit 1; its `--selftest` prints `cases=0` | **REJECTED (as required)** |
| 4 | `recheck-audit.py --quiet` strict pass=45/45 | `strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0`; `lines=45 total=45 pass=45 fail-closed=24 … exit=0`; `expect=present expected=45 missing=0 unexpected=0 exit=0`; `recheck_exit=0` | **PASS** |
| 5 | `source-recheck.py --selftest` | `selftest cases=10 failures=0`, `sr_selftest_exit=0` | **PASS** |
| 6 | `frontier-recheck-count.py` entries=19 pass=19 | `entries=19 pass=19 exit=0`; `PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0` | **PASS** |
| 7 | `anchorcheck.py SKILL.md` verdict classes unchanged: 7 in-range / 0 bad / LOST-RECORDED=306 / PIN-BROKEN=0 / ORIGIN=0 / OUTSIDE-BASE=0 / BASE-ABSENT=0, exit 0 | `== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, `anchor_exit=0` | **DEVIATION** — in-range 7→12, every failure class identical (see D-R33-1) |
| 8 | `density.py SKILL.md --label r33-final`, mean not lower than r31's 191.5; report both | r31 (committed, `SHONEN.md:8`) **191.5**, base bytes re-measured **191.5** (689 cites / 24 blocks), r33 final **201.7** (710 cites / 25 blocks), `density_exit=0` | **PASS** |
| 9 | `git diff BASE -- SKILL.md PROVINCE.md` append-only, 0 deletions | `19  0  SKILL.md`, `2  0  PROVINCE.md`; `git diff … \| grep -c '^-[^-]'` = `0` | **PASS** |

## 2. Commands and outputs

### 2.1 Binding, two runs (raw: `ExecRegressionC1/bind-run1.txt`, `bind-run2.txt`)

```
$ python3 corpus/instruments/capture-binding-check.py > bind-run1.txt; echo run1_exit=$?
$ python3 corpus/instruments/capture-binding-check.py > bind-run2.txt; echo run2_exit=$?
run1_exit=0 run2_exit=0
stdout_byte_identical=YES
1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1  bind-run1.txt
1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1  bind-run2.txt
```

Output (identical in both runs; line set as the contract requires — `MANIFEST` per dir, then `AUDIT`, then failures, then the summary; zero `FAIL` lines here):

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
```

Rule coverage read off that output: rule A `snapshot_dirs=9 manifest_dirs=9 missing_manifest=0`; rule B `with_url=40`, `url_bound=40` (per-row, erratum-1 scoped); rule C `with_fetched_utc=2` (both round-32 records) + `with_archival=38` (all pre-round-32 records), and `round-32 fetched=2 archival=0` proves no archival exemption is being used for round-32.

### 2.2 Selftest (raw: `selftest.txt`)

```
$ python3 corpus/instruments/capture-binding-check.py --selftest
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=url-matching-two-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest cases=11 failures=0
selftest_exit=0
```

All six contract-named cases are present (`clean-all-pass`, `missing-manifest-dir`, `record-without-url`, `url-matching-two-rows`, `round-32-record-without-fetched_utc`, `pre-round-32-record-without-archival`); five further cases (`url-mismatch`, `no-row`, `shared-url-not-a-failure`, `round-32-record-with-fetched_utc-passes`, `pre-round-32-archival-passes`) make 11. The erratum-1 reading is implemented in the instrument as `case_duplicate_id_rows` (same id twice → `dup-id`) plus `case_shared_url_passes` (same URL on two different ids → not a failure), matching `claims-erratum-1.md` §Ruling items 3–4.

### 2.3 Fake-checker control (raw: `fake-final.txt`, `fake-base.txt`, `fake-selftest.txt`)

```
$ python3 .ufo/waves/round-33/c1-controls/fake-checker.py           # FINAL manifests
records=40 bound=40 unbound=0
fake_exit=0

$ python3 .ufo/waves/round-33/c1-controls/fake-checker.py --selftest
selftest cases=0 failures=0
fake_selftest_exit=0

$ python3 .ufo/waves/round-33/c1-controls/fake-checker.py --root <base-byte tree>   # same bytes as 2.4
records=38 bound=38 unbound=0
fake_base_exit=0
```

The fake is byte-for-byte indistinguishable from the target summary **on the final bytes** — which is exactly why the kill rule's clause is needed and why the discriminating control below matters: on the base-byte tree, where no manifest record carries a `url` and round-32 has no manifest, the fake still prints `bound=38 unbound=0` exit 0 while the real checker prints `bound=0 unbound=38` exit 1. Its `--selftest` also violates the `cases>=6` clause (`cases=0`). **Kill rule satisfied: a checker printing the summary without validating is not accepted as evidence.**

### 2.4 Kill-rule clause: real checker on base bytes (raw: `bind-base.txt`)

Fixture: read-only `git archive 690b69da corpus/SOURCES.md corpus/source-snapshots | tar -x` into `$HYAKU_SCRATCH/kasegi-r33/ExecRegressionC1/base-root` (8 manifests, `round-32/` with `S049.txt`/`S050.txt` and no manifest).

```
$ python3 corpus/instruments/capture-binding-check.py --root "$S/base-root"
MANIFEST round-23 records=4 url_bound=0 fetched=0 archival=0
…
FAIL rule=missing-manifest dir=round-32
FAIL rule=url-mismatch record=S041 detail=absent dir=round-30
FAIL rule=provenance-missing record=S041 dir=round-30
…
records=38 bound=0 unbound=38
bind_base_exit=1
```

Exit 1 with named records and the missing-manifest dir: the kill rule's "must exit 1 on the base bytes and name unbound records" holds. (This is base-byte evidence only; not an after-column comparison.)

### 2.5 `recheck-audit.py --quiet` (raw: `recheck.txt`)

```
strict pass=45/45 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=21 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=45 total=45 pass=45 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=45 missing=0 unexpected=0 exit=0
recheck_exit=0
```

(Pre-state at 04:16Z before the wave's scribes landed: `lines=44 total=44 pass=44 … expected=44`. Labelled PRE-STATE and not compared; the after-column is the block above.)

### 2.6 `source-recheck.py --selftest` (raw: `sr-selftest.txt`)

```
$ python3 corpus/instruments/source-recheck.py --selftest
SELFTEST double-occurrence-broken PASS expected-exit=1 observed-exit=1 …
SELFTEST quote-absent PASS expected-exit=1 observed-exit=1 …
selftest cases=10 failures=0
sr_selftest_exit=0
```

Extra manifest-bytes regression (`sr49.txt`, `sr50.txt`), run because C1 creates the round-32 manifest:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049   -> exit 0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050   -> exit 0
S049:Q8 OK occurrences=1 ; S050:Q6 OK occurrences=1   (last assertion lines)
```

### 2.7 `frontier-recheck-count.py` (raw: `frontier.txt`)

```
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
frontier_exit=0
```

### 2.8 `anchorcheck.py SKILL.md` (raw: `anchor.txt`)

```
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchor_exit=0
```

### 2.9 `density.py SKILL.md --label r33-final` (raw: `density-final.txt`, `density-base.txt`)

```
$ python3 corpus/instruments/density.py SKILL.md --label r33-final
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.
density_exit=0

$ python3 corpus/instruments/density.py <git 690b69da:SKILL.md copy> --label r31-base
| | **mean dens** | | | | | | | | **191.5** |
Total path-citation instances: 689 across 24 blocks.
density_base_exit=0
```

Both numbers: r31/base **191.5** (also the committed figure at `SHONEN.md:8`), r33 final **201.7** — not lower.

### 2.10 Append-only proof (raw: `git-diff-numstat.txt`, `git-diff-SKILL-PROVINCE.patch`)

```
$ git diff --numstat 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 -- SKILL.md PROVINCE.md
2       0       PROVINCE.md
19      0       SKILL.md
$ git diff 690b69da -- SKILL.md PROVINCE.md | grep -c '^-[^-]'
0
```

### 2.11 Independent manifest audit (raw: `independent-audit.txt`)

Second implementation (separate parsing of `corpus/SOURCES.md` rows and `https?://` tokens, `assert` per record) over the same final bytes:

```
round-23 .. round-31: records=N url_byte_exact=N fetched=0 archival=N
round-32: records=2 url_byte_exact=2 fetched=2 archival=0
TOTAL records=40 bound=40 fetched=2 archival=38
registry_rows=50 rows_without_url_token=[]
registry_urls_carried_by_two_ids=[('https://docs.hackerone.com/…safe-harbor-overview-faq', ['S006','S028']), ('https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng', ['S024','S029'])]
snapshot_dirs=9
```

So `multi_row_url=2` is exactly the two cross-id URL pairs erratum 1 §Finding names, not an unbound record. Round-32 records, byte-exact from the manifest:

```
S049 https://zc.cnvd.org.cn/news/helpList    2026-10-25T23:14:00-03:00  archival_key='<absent>'
S050 https://security.360.cn/Reward/rules    2026-10-25T23:14:00-03:00  archival_key='<absent>'
```

## 3. Claim-C1 gate set, mapped

All of C1's predicate clauses that these counters can settle are measured true: `records=40 bound=40 unbound=0` exit 0 (twice, identical); every snapshot dir has a manifest (9/9); every record's `url` is byte-exact to its own registry row (independent audit, `bound=40`); S049/S050 carry `fetched_utc`; all 38 pre-round-32 records carry `archival: true`; `--selftest` `cases=11 failures=0`. The one clause **not** observable at 04:33Z is the SCORECARD capabilities-row landing (D-R33-2).

## 4. Defects / deviations found by this seat

- **D-R33-1 (deviation from the item's literal expectation, no failure-class change).** `anchorcheck.py SKILL.md` reports **12** in-range / 12 distinct anchors, not the 7 the item wrote. Cause is visible in the diff: the round-33 append to `SKILL.md` adds exactly five resolvable anchors — `corpus/instruments/capture-binding-check.py:1-92`, `:166-181`, `:184-262`, `corpus/SOURCES.md:55-56`, `.ufo/waves/round-33/claims-erratum-1.md:1-36` — and the 12 `OK` lines are exactly the 7 pre-existing `corpus/knowledge/*` anchors plus those five. All failure classes are unchanged (`0 bad`, `LOST-RECORDED=306`, `PIN-BROKEN=0`, `ORIGIN=0`, `OUTSIDE-BASE=0`, `BASE-ABSENT=0`) and the exit is 0. Reported unrounded rather than restated as 7.
- **D-R33-2 (foreign-path observation, not my gate).** `SCORECARD.md` carries no `capture-binding-check` row at 04:33Z (`sha256 6224ab87…`, unchanged from base; no `ScribeScorecard.md` receipt). C1's predicate sentence includes "the capability `capture-binding-check` enters the SCORECARD capabilities table in the same round". The L1 must re-check this after ScribeScorecard lands; **no counter above depends on `SCORECARD.md`**, so no re-run of §2 is required for it.
- **D-R33-3 (rejected probe, disclosed so nobody cites it).** Running `anchorcheck.py` on a scratch copy of `git 690b69da:SKILL.md` yields `0 in-range, BASE-ABSENT=7, exit 1` because the instrument resolves lane-relative citations from the file's own location; an out-of-lane copy is **not** a base measurement. Raw kept as `anchor-base.txt` for auditability only; it is not evidence and is not compared to §2.8.

## 5. Risks and limits

- I read manifests, the registry and instrument output only; **no capture body was opened**, so nothing in this receipt asserts anything about capture content (QUALITY Q6 stays with ExecManifest32/ExecErratumCheck). The manifest's own `purpose` string is plain prose, not credential text.
- Erratum-1 semantics are in force: rule B binds a record to its **own** id row, and a URL shared by two ids is informational. Under the letter of the pre-erratum interface contract (global exactly-one-match), records S029 and S006 could never bind without editing frozen registry rows; the L1 filed the erratum before measurement (`claims-erratum-1.md`, 04:18Z local, no seat had scored). This receipt applies the erratum reading and discloses `multi_row_url=2`.
- The checker requires `fetched_utc` for any dir whose name does not parse as `round-N` (`round_no is None`). No such dir exists in the lane today; noted as a design property, not a defect.
- Bytes are quiescent **for the inputs above at 04:33Z**. If `corpus/SOURCES.md`, `corpus/README.md`, `SKILL.md`, `PROVINCE.md`, `corpus/instruments/README.md`, `knowledge-expected.txt`, any `source-snapshots/*/manifest.json`, or `capture-binding-check.py` changes before the commit, re-run: `python3 corpus/instruments/capture-binding-check.py && python3 corpus/instruments/capture-binding-check.py --selftest && python3 corpus/instruments/recheck-audit.py --quiet && python3 corpus/instruments/frontier-recheck-count.py && python3 corpus/instruments/anchorcheck.py SKILL.md && python3 corpus/instruments/density.py SKILL.md --label r33-final`.
- No blockers: every subject landed inside the 30-minute poll budget (`ExecRegistryAppend` at 04:29Z was the last of my inputs).

## 6. Scratch

All fixtures lived under `$HYAKU_SCRATCH/kasegi-r33/ExecRegressionC1/` (base-byte tree from `git archive`, base `SKILL.md` copy, outputs). Raw outputs were copied into `wave1/ExecRegressionC1/` first, then the scratch tree was removed — nothing of this seat's remains on the scratch disk and nothing was written to `/tmp`.

## 7. Files

- Written by this seat: `.ufo/waves/round-33/wave1/ExecRegressionC1.md` (this receipt) and the 22 raw files in `.ufo/waves/round-33/wave1/ExecRegressionC1/`.
- Read only: `corpus/instruments/{capture-binding-check,recheck-audit,source-recheck,frontier-recheck-count,anchorcheck,density}.py`, `corpus/SOURCES.md`, `corpus/README.md`, `corpus/instruments/README.md`, `corpus/instruments/knowledge-expected.txt`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, all `corpus/source-snapshots/*/manifest.json`, `.ufo/waves/round-33/{claims.json,claims-erratum-1.md,c1-controls/fake-checker.py}`, peer receipts.
