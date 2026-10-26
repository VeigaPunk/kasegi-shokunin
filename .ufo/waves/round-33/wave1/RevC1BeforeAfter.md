# RevC1BeforeAfter — independent before→after verification of the C1 counters

- Seat: `RevC1BeforeAfter` (reviewer, leaf). Round 33 / wave 1, lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
- Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims freeze `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; HEAD at review time `53bfa59` (dispatcher ready marker + `claims-erratum-1.md` + `l1-ref/sid-url.tsv`).
- Method: every C1 counter command from `.ufo/waves/round-33/claims.json` run **verbatim** from the lane; before-state re-derived on a base-byte tree extracted from `690b69da` in scratch; after-state re-derived independently of the instrument (second parser over `SOURCES.md` + manifests); byte-identity checked against `wave1/ExecRegressionC1.md` §0 digests. Model-independent verification: every cited value below is a command output; no model was passed and no number is quoted from a receipt without re-derivation.
- Writes made: this receipt only. No lane/Git/jj mutation (read-only `git status`/`log`/`diff`/`ls-files`/`archive` only); no campaign tools in `shokuknow`; no tool installs (stdlib Python 3 sufficed).

## 1. Before state, re-derived on base bytes (not copied from `before.txt`)

Fixture: `git -C <lane> archive 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 | tar -x -C $S/base` with `$S=$HYAKU_SCRATCH/kasegi-r33/RevC1BeforeAfter` (created `mkdir -p`, removed at exit §7).

```
$ ls $S/base/corpus/instruments/capture-binding-check.py
ls: cannot access ...: No such file or directory
ls_exit=2                                    # before.txt §instrument absent: ls_exit=2  MATCH

$ ls $S/base/corpus/source-snapshots/round-32/
S049.txt
S050.txt                                     # before.txt §round-32: S049.txt S050.txt, no manifest  MATCH

$ cd $S/base && for f in corpus/source-snapshots/*/manifest.json; do python3 -c "<counter-3 one-liner>" "$f"; done
round-23 records= 4 url= 0 fetched= 0 archival= 0
round-24 records= 19 url= 0 fetched= 0 archival= 0
round-25 records= 5 url= 0 fetched= 0 archival= 0
round-26 records= 1 url= 0 fetched= 0 archival= 0
round-28 records= 2 url= 0 fetched= 0 archival= 0
round-29 records= 3 url= 0 fetched= 0 archival= 0
round-30 records= 3 url= 0 fetched= 0 archival= 0
round-31 records= 1 url= 0 fetched= 0 archival= 0
(round-32 glob: FileNotFoundError — no manifest.json)   # before.txt: TOTAL records=38 with_url=0 with_fetched_utc=0  MATCH (4+19+5+1+2+3+3+1=38)

$ cd $S/base && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049
manifest UNAVAILABLE reason=missing
recheck49_exit=2                             # before.txt: manifest UNAVAILABLE reason=missing, recheck_exit=2  MATCH
```

Kill-rule clause, real checker on base bytes (current instrument, `--root $S/base`):

```
$ python3 corpus/instruments/capture-binding-check.py --root $S/base
MANIFEST round-23 records=4 url_bound=0 fetched=0 archival=0
... (8 manifest dirs, all url_bound=0)
AUDIT records=38 with_url=0 with_fetched_utc=0 with_archival=0 snapshot_dirs=9 manifest_dirs=8 missing_manifest=1 multi_row_url=0
FAIL rule=missing-manifest dir=round-32
FAIL rule=url-mismatch record=S018 detail=absent dir=round-23
FAIL rule=provenance-missing record=S018 dir=round-23
... (all 38 records named, url-mismatch detail=absent + provenance-missing)
records=38 bound=0 unbound=38
checker_on_base_exit=1
```

The real checker exits 1 on the base bytes, names every unbound record, and prints `bound=0` — it never prints `bound=N` while the records carry no `url`. The frozen fake (`c1-controls/fake-checker.py`, read: prints `records=N bound=N unbound=0` with no validation, `--selftest` prints `cases=0`) is rejected by this clause; its frozen receipt (`fake-checker-receipt.txt`: `records=38 bound=38 unbound=0`, `fake_exit=0`) matches the script's code.

## 2. After state, counters run verbatim on the lane (final bytes)

### 2.1 Counter 1 (binding)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"
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
binding_exit=0
```

vs claim `records=40 bound=40 unbound=0` exit 0: **MATCH**. Rule A: `snapshot_dirs=9 manifest_dirs=9 missing_manifest=0`. Rule C: `with_fetched_utc=2` (round-32 only, `fetched=2 archival=0` on that dir — no archival exemption used) + `with_archival=38` (all pre-round-32 records).

### 2.2 Counter 2 (selftest)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-binding-check.py --selftest; echo "selftest_exit=$?"
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

vs claim `--selftest` failures=0 exit 0: **MATCH**. 11 cases ≥ 6; all six contract-named cases present (`url-matching-two-rows` is rebuilt as the erratum-1 §3 `dup-id` case, disclosed in the instrument docstring and `corpus/instruments/README.md:537`).

### 2.3 Counter 3 (manifest audit)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && for f in corpus/source-snapshots/*/manifest.json; do python3 -c "<claims.json one-liner>" "$f"; done
round-23 records= 4 url= 4 fetched= 0 archival= 4
round-24 records= 19 url= 19 fetched= 0 archival= 19
round-25 records= 5 url= 5 fetched= 0 archival= 5
round-26 records= 1 url= 1 fetched= 0 archival= 1
round-28 records= 2 url= 2 fetched= 0 archival= 2
round-29 records= 3 url= 3 fetched= 0 archival= 3
round-30 records= 3 url= 3 fetched= 0 archival= 3
round-31 records= 1 url= 1 fetched= 0 archival= 1
round-32 records= 2 url= 2 fetched= 2 archival= 0
```

Totals: records=40, url=40, fetched=2, archival=38 — the 38 legacy records all carry `url`+`archival`, the 2 round-32 records carry `url`+`fetched_utc`. **MATCH** with the claim's rule-C clauses.

### 2.4 Independent re-derivation of rules B/C (second parser, not the instrument)

Separate Python pass over `corpus/SOURCES.md` (row id → `https://` tokens of the source cell) and every manifest record, asserting: own row exists, row id unique, `url` byte-equals one of the own row's tokens, provenance per rule C:

```
INDEPENDENT total=40 bound=40 unbound=0 multi_row_url=2
registry_rows=50
DUP-URL https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq ['S006', 'S028']
DUP-URL https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng ['S024', 'S029']
```

`bound=40 unbound=0` re-derived without the instrument. `multi_row_url=2` is exactly the two cross-id URL pairs `claims-erratum-1.md` §Finding names (S006/S028, S024/S029) — informational under the erratum, not unbound records. Round-32 record bytes read directly from the manifest:

```
S049 url=https://zc.cnvd.org.cn/news/helpList fetched_utc=2026-10-25T23:14:00-03:00 archival=<absent>
S050 url=https://security.360.cn/Reward/rules fetched_utc=2026-10-25T23:14:00-03:00 archival=<absent>
```

Both URLs byte-match the interface contract's named URLs; `fetched_utc` equals capture commit `288ea9ac17a78dce644388af35b89aa96b7994da` author time (`git show -s --format='%ai'` → `2026-10-25 23:14:00 -0300`).

### 2.5 Supplementary before→after arc for the manifest (C2 counters, run because C1 creates the manifest)

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S049  → recheck49_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050  → recheck50_exit=0
```

Before `recheck_exit=2` (absent manifest) → after `0` on both records.

## 3. Byte-identity of the after state (final-bytes check)

`sha256sum` of every C1 counter input at my final measurement window vs `wave1/ExecRegressionC1.md` §0 (`q2.txt`, window 04:31–04:34Z):

```
b22c7f01 corpus/SOURCES.md                        = ExecRegressionC1 b22c7f0173e75e0c…
b4182665 corpus/instruments/capture-binding-check.py = ExecRegressionC1 b4182665ba5cf544… (492 lines)
6e4e719a corpus/source-snapshots/round-32/manifest.json = ExecRegressionC1 6e4e719a76f1d18c…
1f6d4fb5 round-23  77b158ca round-24  251cb5b2 round-25  1c913132 round-26
89f51e05 round-28  b24a485f round-29  8aacf77c round-30  5fa37fd7 round-31   = all eight digests ExecRegressionC1 reports from ExecManifestUpgrade/ExecManifest32
```

All eleven C1 inputs byte-identical across the two measurement windows (~15 min apart). Counter-1 stdout in my final run hashes `1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1` — the same digest ExecRegressionC1 reports for `bind-run1.txt`/`bind-run2.txt`, so three independent runs on three windows produce byte-identical output.

Git state disclosure: at review time the wave's bytes are **worktree-final but not yet committed** (`git status --porcelain` shows the nine manifests `M`, the instrument / round-32 manifest / knowledge entry `??`, `SOURCES.md`/`SCORECARD.md`/`QUALITY.md`/`README`/`SKILL`/`PROVINCE`/`instruments/README`/`knowledge-expected.txt` `M`; HEAD `53bfa59`). The commit is the L1's closing act through the lane helper; no seat may commit (bound 4). The final-bytes condition is therefore evidenced by digest stability across three windows (ExecRegressionC1's 45 s-probed window, my two windows) rather than by a clean `git status`, which cannot exist before the L1's closing commit. If any C1 input digest changes before that commit, the after-column must be re-run (re-run line in ExecRegressionC1 §5 covers it).

## 4. SCORECARD capability row

```
$ grep -n "capture-binding-check" SCORECARD.md
1078:| capture-binding-check | Audit every committed capture snapshot in one pass: ... | 33 |
```

`SCORECARD.md:1074` opens `## Round-33 capabilities`; the row at `:1078` carries the full rule A/B/C description (erratum-1 reading disclosed), evidence pointers (`corpus/instruments/capture-binding-check.py` sha256 `b4182665…` 492 lines; `wave1/ExecRegressionC1.md`; `wave1/RevC1Instrument.md` §9 `lands`; `wave1/ExecDeterminism.md`; `wave1/CritC1Kill.md`) and **First-working round = 33**. The move-log row `:1084` records the 4→4-held C1 movement with the same numbers I re-derived. D-R33-2 (row absent at 04:33Z) is closed by this landing.

## 5. Observations (outside my counters, disclosed not judged)

- `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` digest moved after ExecRegressionC1's window (`53c48b3b…` → `1f7ac0a2…` at my check): a C2-side input, read by **no** C1 counter; C2 re-verification belongs to the C2 seats.
- Mid-flight PRE-STATE (bound 6, labelled, not compared): my first counter-1 run at ~01:2x local printed `records=40 bound=36 unbound=4` exit 1 (`url-ambiguous`/`url-unbound` rule names) — an earlier instrument revision plus the not-yet-appended S049/S050 registry rows. All after-column values above are from the post-landing quiescent bytes only.
- Governing contract: the frozen interface contract's rule B ("match EXACTLY ONE registry-row URL") is amended by `claims-erratum-1.md` (L1 ruling filed 2026-10-26 before any measurement, `bound`/`unbound`/counters/targets unchanged): rule B binds per record id. The instrument implements the erratum reading and discloses `multi_row_url=N`; under the pre-erratum global reading `unbound=0` would be unattainable without editing immutable registry rows, which no seat may do this round.

## 6. Verdict

**matches.** Every before value in `c1-controls/before.txt` re-derived independently on base bytes `690b69da` (instrument absent `ls_exit=2`; 38 records `url=0 fetched=0`; round-32 dir without manifest; recheck exit 2); every after value in `wave1/ExecRegressionC1.md` and the frozen claim re-derived verbatim on the final bytes (`records=40 bound=40 unbound=0` exit 0; `selftest cases=11 failures=0` exit 0; manifest audit 40/40/2/38; independent re-derivation `bound=40 unbound=0`; recheck 2→0 on both round-32 records); the kill-rule clause holds in both directions (real checker fails closed on base bytes naming all 38 records; fake rejected); the `capture-binding-check` capability row exists in `## Round-33 capabilities` with first-working round 33; all eleven C1 input digests are byte-identical across three measurement windows.

## 7. Scratch

`$HYAKU_SCRATCH/kasegi-r33/RevC1BeforeAfter/` (base-byte tree, final-bind.txt) removed before yield; nothing left on the scratch disk; nothing written to `/tmp`; no tool installs or upgrades (stdlib Python 3 only).
