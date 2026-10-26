# ScribeSkillGate — `SKILL.md` round-33 registry row (append-only, R6)

Seat: ScribeSkillGate, kasegi-shokunin round 33, wave 1, leaf. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`. Answering model: `opencode-go/deepseek-v4.1-flash`
(config route; no model passed by this seat). Tools installed/upgraded: none.

Write scope exercised: `SKILL.md` only (append). No other lane file written; no git/jj mutation
(read-only `git diff`/`sha256sum` only); no subagent dispatch; no live fetch.

## 1. Wait discipline

| waited for | first seen | how |
|---|---|---|
| `.ufo/waves/round-33/wave1/ExecManifest32.md` | 2026-10-26T01:20 | `until [ -s … ]` poll, 15 s interval |
| `.ufo/waves/round-33/wave1/ExecCaptureBinding.md` | 01:21 (receipt re-written 01:23 at the final digest) | same poll |
| `corpus/SOURCES.md` at 50 registry rows (S049/S050 appended) | 01:25 | same poll — required because rule B binds each record to its own row, so the 40/40/0 target is unmeasurable before the append |

The only run I took before the append is labelled PRE-STATE and is not compared to anything:

```
$ python3 corpus/instruments/capture-binding-check.py            # PRE-STATE: 48 rows, S049/S050 absent
…
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
FAIL rule=no-row record=S049 dir=round-32
FAIL rule=no-row record=S050 dir=round-32
records=40 bound=38 unbound=2
binding_exit=1
```

## 2. Gates before the append (same commands, same cwd)

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md; echo "ANCHOR_EXIT=$?"
== SKILL.md: 7 in-range cite instances, 0 bad; 7 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
ANCHOR_EXIT=0

$ python3 corpus/instruments/density.py SKILL.md --label r33
| 24 | Round-31 Gates & probes registry addition (appended 2026-10-25) | 13 | 8 | 27 | 2 | 18 | 6 | 53 | 662.5 |
| | **mean dens** | | | | | | | | **191.5** |
Total path-citation instances: 689 across 24 blocks.
```

Pre-append file state: 1071 lines, sha256 `817636048968caf9801f3bdd22c8b8970f1014fc5a8192c49010e8328c4088b7`.

## 3. Measured subject bytes (quiescent, after the registry append)

```
$ sha256sum corpus/instruments/capture-binding-check.py
b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9  corpus/instruments/capture-binding-check.py
$ wc -l corpus/instruments/capture-binding-check.py
492 corpus/instruments/capture-binding-check.py
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
50
```

Three audit runs, byte-identical stdout (`diff -q run1.txt run2.txt`, `diff -q run1.txt run3.txt` → `IDENTICAL`
/ `STILL_IDENTICAL`), exit 0 each:

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
run1_exit=0
```

Selftest at the same digest (`--scratch` pointed at my scratch dir, not an inherited `TMPDIR`):

```
$ python3 corpus/instruments/capture-binding-check.py --selftest --scratch /fast/scratch/hyaku/kasegi-r33/ScribeSkillGate
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

## 4. What was appended (19 insertions, 0 deletions)

```
$ git diff --stat -- SKILL.md
 SKILL.md | 19 +++++++++++++++++++
 1 file changed, 19 insertions(+)
$ git diff -U0 -- SKILL.md | grep -E '^@@|^-[^-]'
@@ -1071,0 +1072,19 @@ …
```

No deletion hunk exists, so R6 holds: the block starts at line 1072 and every earlier line is untouched.
Post-append file: 1090 lines, sha256 `b11b60857986c3d735876da168042fe150b8c80fbdf2792263a29cf2a8e3ed84`.

Section `## Round-33 Gates & probes registry addition (appended 2026-10-26)` carries one 8-column registry
row for `corpus/instruments/capture-binding-check.py`:

| documented | content |
|---|---|
| type | `gate\|probe` |
| entry command | `cd <lane> && python3 corpus/instruments/capture-binding-check.py [--root DIR]` |
| verdict map | exit 0 iff no `FAIL` line; 1 on any `FAIL`; 2 on `UNAVAILABLE reason=no-snapshot-tree\|read-error\|manifest-JSONDecodeError\|manifest-shape\|record-shape`; rule lines A `missing-manifest`, B1 `no-row`, B2 `dup-id`, B3 `url-mismatch` (`detail=absent` form included), C `provenance-missing` with the `round-32`+ archival exemption closed (unparsable dir name = fail-closed modern) |
| self-test | `--selftest` → 11 `selftest case=… verdict=pass` lines then `selftest cases=11 failures=0`, exit 0 |
| pinned-value path | `.ufo/waves/round-33/wave1/ExecCaptureBinding.md` |
| write scope | inputs read-only, nothing written; fixtures under `--scratch` else `$HYAKU_SCRATCH` else `$TMPDIR`, removed in `finally` |
| owner | `kasegi` |

The prose records the measured 40/40/0 at digest `b4182665…` with all nine per-dir counts, the id-scoped
rule-B reading from `.ufo/waves/round-33/claims-erratum-1.md:1-36` (`multi_row_url=2` informational only),
and the known limits: registry-text identity only, never page content — that is
`corpus/instruments/source-recheck.py`'s sha256+quote job; a 0-byte or deleted capture still scores
`bound=40`; `fetched_utc` is presence, not RFC3339 (`"pending"` binds); the walk is one level, so a nested
snapshot dir is invisible; two records with one id print `records=41 bound=41`; a record binds to a
`rejected` row.

## 5. Gates after the append

```
$ python3 corpus/instruments/anchorcheck.py SKILL.md; echo "anchor_exit=$?"
== SKILL.md: 12 in-range cite instances, 0 bad; 12 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0
anchor_exit=0
```

Same verdict classes as §2 (0 bad, PIN-BROKEN/ORIGIN/OUTSIDE-BASE/BASE-ABSENT all 0). `LOST-RECORDED` stayed
`306` — the new block cites only live lane paths, so no `[lost-tree]`/`[lost-base]` line was added.

```
$ python3 corpus/instruments/density.py SKILL.md --label r33
| 25 | Round-33 Gates & probes registry addition (appended 2026-10-26) | 18 | 11 | 21 | 1 | 21 | 6 | 49 | 445.5 |
| | **mean dens** | | | | | | | | **201.7** |
Total path-citation instances: 710 across 25 blocks.
```

Mean density 191.5 → **201.7** (not lower); the new block itself is 445.5. Two intermediate drafts measured
113.5 and 148.6 and were reflowed rather than left to pull the mean down — the numbers above are the final
bytes.

## 6. Conflicts and caveats (for the canonical judge)

1. **Contract vs erratum on rule B.** The frozen interface contract says a record's `url` must match
   *exactly one* registry-row URL (0 or 2+ = failure). The L1's `.ufo/waves/round-33/claims-erratum-1.md`
   supersedes that reading with id-scoped binding: the record must match the URL token of **its own** row,
   and a URL also carried by S024/S029 or S006/S028 only raises `multi_row_url=N`. The landed instrument
   implements the erratum (docstring `corpus/instruments/capture-binding-check.py:1-92`, `bind_record` at
   `corpus/instruments/capture-binding-check.py:166-181`), and my row documents the erratum, not the
   superseded literal text. Under the literal reading the 40/40/0 predicate would be unattainable without
   editing immutable registry rows.
2. **The checker moved three times inside the wave** (`bcabe76a…` → `4bc7aed3…` → `b4182665…`, the last a
   docstring-only correction). `ExecCaptureBinding.md` §3-§7 runs were taken at `4bc7aed3…`; my 40/40/0 and
   `selftest cases=11 failures=0` are measured at `b4182665…` and the row pins that digest.
3. **Selftest case count.** The contract required at least 6 cases; 11 landed (the 6 named plus
   `url-mismatch`, `no-row`, `shared-url-not-a-failure`, and two pass controls). The contract's
   `url-matching-two-rows` case is landed as a same-id row pair (`dup-id`), per the erratum.
4. **`MANIFEST` line field.** The contract writes `<round>`; the instrument prints the directory name
   (`MANIFEST round-23 …`). Identical on this tree (every dir is `round-<N>`), recorded rather than smoothed.

## 7. Out of scope (not touched)

`SCORECARD.md` (capability row is ScribeScorecard's), `corpus/instruments/README.md` (ScribeInstrReadme),
`corpus/QUALITY.md` (ScribeQuality), `PROVINCE.md` (ScribeProvince), `SHONEN.md` (ScribeShonen),
`corpus/lessons/round-33.md` (ScribeLesson), `LOG.md` (the L1), `corpus/SOURCES.md`, all manifests, the
checker itself, and every other round-33 control directory. No score claim is made here.

## 8. Artifacts

- Receipt evidence: `.ufo/waves/round-33/wave1/ScribeSkillGate/` — `digests.txt` (checker + 9 manifests),
  `run1.txt` / `run2.txt` / `run3.txt` (identical audit runs), `selftest-final.txt`, `anchor-after3.txt`,
  `anchor-final.txt`, `density-final.txt`.
- Scratch `/fast/scratch/hyaku/kasegi-r33/ScribeSkillGate/` removed before yield (`rm -rf`; the directory
  no longer exists), after the copies above; no `/tmp` path is cited anywhere in this receipt or in the
  appended row.
- `anchor-final.txt` and `density-final.txt` in that directory are the post-cleanup re-runs on the final
  bytes (exit 0 each, same figures as §5). One cosmetic artifact to discount: an `anchorcheck.py … | head -1`
  pipeline raised `BrokenPipeError` from the instrument's own `print` (it writes ~38 KB of LOST-RECORDED
  lines); that is the pipe, not a verdict — the unpiped runs exit 0.
