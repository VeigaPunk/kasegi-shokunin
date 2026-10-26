# ExecCaptureBinding — C1 instrument `corpus/instruments/capture-binding-check.py`

Seat: ExecCaptureBinding (round 33, wave 1, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
write scope = that one path only. Answering model: `opencode-go/deepseek-v4.1-flash` (session route from
the harness context; no model was passed by this seat). Tools installed/upgraded: none.

Landed bytes (working tree, untracked — the L1 commits):

```
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
492 corpus/instruments/capture-binding-check.py
py_compile=ok
```

Digest history in this wave: `bcabe76a…` (first erratum-compliant write, before the selftest expectation
fix) → `4bc7aed3…` (selftest green, 11 cases) → **`b4182665…`** (docstring-only correction of two
drift statements CritC1Kill measured: the fixture count said "ten" while `CASES` has 11, and the summary
field prose implied a different `unbound` derivation; behaviour identical, `selftest cases=11 failures=0`
re-run at the final digest). Peers were re-notified at `b4182665…`. The §3–§7 runs below were executed at
`4bc7aed3…`; the only difference at `b4182665…` is docstring prose (no executable line), and the selftest
was re-run at the final digest with the same `cases=11 failures=0`, so those measurements stand.

Raw evidence files for every block below live in
`.ufo/waves/round-33/wave1/ExecCaptureBinding/` (`selftest.txt`, `prestate.txt`, `prestate-run2.txt`,
`live-inflight.txt`, `live-run2.txt`, `simulated-registry-append.txt`, `mutants.txt`,
`exit2-and-noharm.txt`, `final-bytes.txt`). Scratch tree
`$HYAKU_SCRATCH/kasegi-r33/ExecCaptureBinding/` (base extraction, simulation root, mutant copies, exit-2
roots) was removed before this receipt was finalised; only the copies under the wave dir remain.

## 1. What the landed bytes implement

Frozen contract + `claims-erratum-1` (L1 ruling, commit `53bfa59`), in the instrument's own order:

| rule | behaviour | failure line |
|---|---|---|
| A | every directory under `corpus/source-snapshots/` that holds `manifest.json` **or** any captured file must hold `manifest.json` | `FAIL rule=missing-manifest dir=<dir>` |
| B1 | the registry row `\| <record id> \| … \|` must exist | `FAIL rule=no-row record=<id> dir=<dir>` |
| B2 | two rows with that id are a failure | `FAIL rule=dup-id record=<id> rows=<n> dir=<dir>` |
| B3 | the record `url` must be byte-identical to the `https://` token of **its own** row's source cell; an absent url is the `detail=absent` form | `FAIL rule=url-mismatch record=<id> [row=<id>|detail=absent] dir=<dir>` |
| C | `fetched_utc` non-empty **or** `archival is True`; a `round-32`+ dir (or an unparsable dir name, fail-closed) requires `fetched_utc` and refuses the archival exemption | `FAIL rule=provenance-missing record=<id> dir=<dir>` |

Output grammar: `AUDIT` header (records / with_url / with_fetched_utc / with_archival / snapshot_dirs /
manifest_dirs / missing_manifest / `multi_row_url`), one `MANIFEST <dirname> records=N url_bound=M
fetched=K archival=L` line per manifest dir, the `FAIL` lines, then exactly one summary
`records=<total> bound=<total> unbound=<total>`. Exit 0 iff no failure line, 1 on any failure, 2 on a
usage/read error (`UNAVAILABLE …`). `multi_row_url` is the erratum's informational count: records whose
URL text also occurs in another registry row — never a failure.

## 2. `--selftest` — 11 fixture cases, two byte-identical runs, exit 0

`python3 corpus/instruments/capture-binding-check.py --selftest` (each case is a subprocess of this same
file against a fresh fixture lane tree in `tempfile.mkdtemp(dir=$HYAKU_SCRATCH)`; the scratch tree is
removed in a `finally`):

```
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

Case mapping to the contract's six required cases: `clean-all-pass`, `missing-manifest-dir`,
`record-without-url`, `url-matching-two-rows` (**rebuilt** per the L1's erratum instruction as a same-id
row pair — two rows `S001`/`S001`, verdict `dup-id`), `round-32-record-without-fetched_utc`,
`pre-round-32-record-without-archival`; the other five are controls or defects the contract's mutant list
names (`url-mismatch`, `no-row`, `shared-url-not-a-failure` = erratum §4, and two pass controls). Every
pass-expected case also asserts the absence of any `FAIL ` line. Second run byte-identical
(`selftest-run2.txt`, exit 0).

## 3. Red-before on the base bytes (PRE-STATE, base commit `690b69da`)

The working tree's manifests were already upgraded by ExecManifestUpgrade when this seat ran, so the
base state was rebuilt read-only and measured on real bytes of the lane base:

```
git archive 690b69dae23ab9f4ccf056ba2d619cadc2abb3c4 corpus/SOURCES.md corpus/source-snapshots \
  | tar -x -C "$HYAKU_SCRATCH/kasegi-r33/ExecCaptureBinding/base"
python3 corpus/instruments/capture-binding-check.py --root "$S/base"
```

```
MANIFEST round-23 records=4 url_bound=0 fetched=0 archival=0
MANIFEST round-24 records=19 url_bound=0 fetched=0 archival=0
MANIFEST round-25 records=5 url_bound=0 fetched=0 archival=0
MANIFEST round-26 records=1 url_bound=0 fetched=0 archival=0
MANIFEST round-28 records=2 url_bound=0 fetched=0 archival=0
MANIFEST round-29 records=3 url_bound=0 fetched=0 archival=0
MANIFEST round-30 records=3 url_bound=0 fetched=0 archival=0
MANIFEST round-31 records=1 url_bound=0 fetched=0 archival=0
AUDIT records=38 with_url=0 with_fetched_utc=0 with_archival=0 snapshot_dirs=9 manifest_dirs=8 missing_manifest=1 multi_row_url=0
FAIL rule=missing-manifest dir=round-32
FAIL rule=url-mismatch record=S018 detail=absent dir=round-23
… (38 records × url-mismatch + 38 × provenance-missing; full list in prestate.txt)
records=38 bound=0 unbound=38
pre_exit=1
```

Two runs, `diff` of stdout empty (`IDENTICAL`) — the instrument is deterministic. The `with_url=0` figure
the seat item expects is on the `AUDIT` line; the summary line keeps the contract's three fields exactly.

## 4. Live tree — PRE-STATE for the registry append (non-comparative, M30-3)

Label: this is **not** the after column. `corpus/SOURCES.md` still carried 48 registry rows while the
wave ran (ExecRegistryAppend had not landed S049/S050 at measurement time), so rows are absent, not
wrong. Two runs, byte-identical.

```
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=0 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=no-row record=S049 dir=round-32
FAIL rule=no-row record=S050 dir=round-32
records=40 bound=38 unbound=2
live_exit=1
```

Facts this establishes on landed data: **40** records over **9** snapshot dirs, every dir has a manifest
(`missing_manifest=0`, closes D5's shape), all **38** legacy records carry `archival: true` and a
byte-exact own-row `url`, both round-32 records carry `fetched_utc` and no `archival`, and
`multi_row_url=2` — exactly the two erratum-declared records (S029 in round-23, S006 in round-24) whose
URL text also sits in the rows S024 / S028. The two failures are the two missing registry rows.

## 4b. Live tree AFTER the registry append — the claim's predicate, on landed bytes

ExecRegistryAppend landed rows S049/S050 (`corpus/SOURCES.md` sha256
`24738a86753edc13d66e40790305f785cdecced1dae4143159708627c382099b`, 50 registry rows; round-32 manifest
sha256 `6e4e719a76f1d18c36792f0c012d3ba3bd8cfb57aab25655f77c7a47343c8774`), and the same instrument at
`b4182665…` was re-run twice on quiescent bytes, 2026-10-26T04:25Z:

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
after_exit=0
```

Two runs byte-identical (`live-postappend-run1.txt` / `live-postappend-run2.txt`, stdout sha256
`1861fec846ca9a5c0e1a7a54591888896fb2c4f2ab89255c640e46eda3c5a9f1`), exit 0 both. This is the AFTER
column: every count in it was recomputed from the two files hashed above, and the pre-append block in §4
is labelled PRE-STATE and is not comparable to it (M30-3). The §5 simulation predicted exactly this
output, which is why it is kept as a reachability proof and not as a figure.

**Registry churn.** `corpus/SOURCES.md` moved again while the wave ran. Re-run at SOURCES.md sha256
`b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b` (50 rows, 2026-10-26T04:29Z; instrument
`b4182665…` and round-32 manifest `6e4e719a…` unchanged): `records=40 bound=40 unbound=0`, AUDIT
`multi_row_url=2`, exit 0, two runs byte-identical (`live-recheck-current.txt` /
`live-recheck-current2.txt`, log `live-recheck-current.log`). The verdict is invariant across both registry
digests this seat measured; cite the registry digest the lane holds at verification time, not the one in
this sentence.

## 5. Target reachability — SIMULATED, not landed bytes

The `records=40 bound=40 unbound=0` target was checked against a scratch **copy** of the live tree with
the two rows appended (ids + the two contract URLs, nothing else):

```
python3 corpus/instruments/capture-binding-check.py --root "$S/sim"
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
sim_exit=0
```

This is a reachability proof on real manifest bytes, **not** a measurement of landed bytes. The citable
figure must come from a post-append run on the lane itself (ExecRegressionC1 / the L1), at the digest in
the header.

## 6. Counter mutants (the four the frozen claim names) — 4/4 killed

Each mutant is a one-`str.replace` copy of the landed file under scratch (the repo file is untouched),
run as a subprocess; "killed" = its `--selftest` no longer prints `selftest cases=11 failures=0` with
exit 0.

```
live selftest: exit=0 summary=['selftest cases=11 failures=0']
MUTANT M1-accept-record-without-url     selftest_exit=1 selftest_summary=['selftest cases=11 failures=1']
   sim_tree : exit=0 summary=['records=40 bound=40 unbound=0']
   verdict=killed
MUTANT M2-accept-url-not-in-registry    selftest_exit=1 selftest_summary=['selftest cases=11 failures=1']
   sim_tree : exit=0 summary=['records=40 bound=40 unbound=0']
   verdict=killed
MUTANT M3-skip-fetched-requirement      selftest_exit=1 selftest_summary=['selftest cases=11 failures=1']
   sim_tree : exit=0 summary=['records=40 bound=40 unbound=0']
   verdict=killed
MUTANT M4-skip-selftest                 selftest_exit=0 selftest_summary=[]
   verdict=killed
```

M1–M3 are killed by the case that isolates the limb (`record-without-url`, `url-mismatch`,
`round-32-record-without-fetched_utc`). M4 (`--selftest` returns 0 without running anything) is killed by
the counter command's own expected output: it prints no `selftest cases=` line at all. Each mutant's
`sim_tree` run shows it *would* print the 40/40/0 target — i.e. the selftest, not the happy-path summary,
is the discriminator.

## 7. Exit-2 paths and no-write behaviour

```
--- root without corpus/source-snapshots
UNAVAILABLE reason=no-snapshot-tree …/e2/nothing
exit=2
--- snapshot tree present, SOURCES.md absent
UNAVAILABLE reason=read-error [Errno 2] No such file or directory: '…/e2/nosources/corpus/SOURCES.md'
exit=2
--- unparsable manifest JSON
… MANIFEST lines for the earlier dirs …
UNAVAILABLE reason=manifest-JSONDecodeError …/e2/badjson/corpus/source-snapshots/round-31/manifest.json
exit=2
```

`--root` relocates both inputs: the same file scores 38 on the extracted base tree, 40 on the live tree
and 40 on the simulated tree, and every count is recomputed (no 38/40 constant exists in the file). The
checker opens files read-only and writes nothing; `git status --short corpus/instruments
corpus/source-snapshots` after all runs shows only the peers' manifest edits, `round-32/manifest.json`
and this instrument as untracked — no file created or modified by a checker run. (Disclosure: this seat
also removed the pre-existing untracked `corpus/instruments/__pycache__/` directory after its own
`py_compile`; nothing tracked was touched.)

## 8. Proposed but NOT landed (outside the frozen contract — the L1's call, not mine)

Received from attack seats during the wave; each would widen or tighten Rule A–C beyond erratum 1, so it
is recorded here rather than implemented:

1. **Rule D (bytes)** — `CritC1Kill`: a record's `path` must be a basename inside its manifest dir, exist,
   be non-empty, and its sha256 must equal `record.sha256`. Measured on current bytes, all 40 records
   satisfy this (`records=40 path_missing=0 sha_or_empty_fail=0`), so it would not change 40/40 — but it
   is a fourth rule the frozen contract does not define, and it changes the meaning of `bound`.
2. **Strict RFC3339 `fetched_utc`** (presence alone passes `pending`) and **round-32+ must not carry
   `archival: true`** — a tighter reading of Rule C; the contract says "carries" and only closes the
   exemption, and both round-32 records carry no `archival` today, so this is also a no-op on landed data.
3. **Non-`round-<N>` directory name = Rule-A failure** — landed bytes treat it as a modern round
   (fail-closed on provenance) instead; no such directory exists.
4. **Row must carry exactly one `https://` token** — measured: all 48 pre-append rows carry exactly one and
   no row token ends in punctuation (S049/S050, read at the after-state, likewise carry one each and bind);
   landed bytes bind on exact token membership and would accept a two-token row whose token equals the
   record url.

If the L1 wants any of 1–4 in the frozen contract, it needs an erratum like erratum 1 and a one-line
change here; this seat did not widen the claim.

**Holes the attack seat measured against these bytes (`CritC1Kill`, at digest `4bc7aed3…`), recorded as
limits of the frozen A–C surface, not implemented:** (a) a truncated (`0`-byte) `S050.txt` and a deleted
`S049.txt` still score 40/40 — no capture-bytes rule; (b) a record `path` of `../round-32/S050.txt` binds;
(c) `fetched_utc: "pending"` binds; (d) a duplicate record appended to one manifest yields
`records=41 bound=41` (no per-manifest id/path uniqueness); (e) a `round-32` directory moved to
`source-snapshots/nested/round-32` disappears (the walk is one level, as the contract's
`source-snapshots/*/manifest.json` says) and the run scores `38/38` exit 0; (f) a row carrying two
`https://` tokens binds either; (g) a record binds to a `rejected` row (no status filter). Items (a)–(b)
are what `source-recheck.py` covers by design (its sha256 + exact-quote pins are the byte check); (c)–(g)
are strictness and enumeration changes that would redefine `bound`, so they belong in an erratum, not in
this file. Measured facts on the landed data for the record: all 40 records' `path` exists, is non-empty
and matches its `sha256` (`records=40 path_missing=0 sha_or_empty_fail=0`), all 48 registry rows carry
exactly one `https://` token, and all 38 bound legacy rows have status `mined`.

## 9. Handoff

Peers notified by id at the final digest: ExecManifestUpgrade, ExecManifest32, ExecRegressionC1 (re-run
their receipts against `b4182665…`; ExecRegressionC1 also got the §4b after-state), plus ScribeLesson
(landed rule-B reading + digest) and CritC1Kill / the L1 (erratum compliance + the four unlanded
proposals). Re-run after any edit to this file:

```
sha256sum corpus/instruments/capture-binding-check.py      # b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9
python3 corpus/instruments/capture-binding-check.py --selftest; echo "selftest_exit=$?"   # cases=11 failures=0, exit 0
python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"               # landed AFTER (§4b): records=40 bound=40 unbound=0, exit 0
```
