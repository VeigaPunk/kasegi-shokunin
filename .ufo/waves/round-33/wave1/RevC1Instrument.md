# RevC1Instrument — review of `corpus/instruments/capture-binding-check.py`

Seat: RevC1Instrument (reviewer, leaf; no subagents, no background jobs). Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`; write scope = this receipt only.
Answering model: `zai/glm-5.3-flash` (workstation route; no model passed by this seat).
Tools installed/upgraded: none (stdlib Python 3 only; no pacman).

## 0. Digest trail (in-flight discipline, bound 6 / M30-3)

The instrument moved under me during review. Every citation below is at the final quiescent
digest unless labelled otherwise:

```
4bc7aed36308bec5… (491 lines)  first version, read fully (lines 1-491)
b4182665ba5cf544… (492 lines)  final version — all measurements below re-run at this digest
```

ExecCaptureBinding.md §digest-history says `4bc7aed3→b4182665` is docstring-only (two drift
statements: fixture count "ten"→eleven, `unbound` derivation prose). Corroborated independently:
the re-read docstring region (lines 40-100) shows exactly those two prose corrections and
byte-identical executable lines (`ROW_RE`/`URL_TOKEN`/`MODERN_ROUND`/`parse_round` unchanged at
lines 96-107), and the full battery re-run at `b4182665` returns the same 12/12 verdicts as at
`4bc7aed3`. Receipt quiescence probe: two consecutive sha samples 20 s apart identical.

## 1. Q1 — does rule B actually grep SOURCES.md and count matches? YES (erratum-1 scoped)

Code path read in full (`b4182665`, 492 lines):

- `load_registry` (L114-131): reads `corpus/SOURCES.md`, `ROW_RE = ^\|\s*(S\d{3,})\s*\|` (L96)
  matches every registry row; the source cell is column 2 of the pipe-split row (L121-124).
  Returns `rows_by_id` (id → list of cells; duplicate id visible as len>1) and all cells.
- `bind_record` (L167-183): resolves the record's **own** row by id (`rows_by_id.get(id)`);
  no row → `FAIL rule=no-row record=<id>`; len>1 → `FAIL rule=dup-id record=<id> rows=<n>`;
  then membership test `url not in row_tokens(own[0])` (L177) where `row_tokens` (L109-112)
  extracts the `https?://[^\s|]+` tokens of that cell. Mismatch → `FAIL rule=url-mismatch`.
- `url_row_count` (L134-136) counts rows carrying the URL text — used **only** for the
  informational `multi_row_url` aggregate (L221-223), never for binding. Erratum-1 §Ruling 4
  implemented as specified.

So rule B does grep SOURCES.md and count matches — per-id row binding (erratum 1), with the
cross-row occurrence count surfaced as `multi_row_url=N` on the AUDIT line, not as a failure.

## 2. Q2 — false-pass on a url matching one row but the WRONG row? NO — tested

Structural reason: binding never searches rows by URL; it looks up the record's own id row and
byte-compares against that row's tokens. A URL that exists in other rows cannot bind a record
whose own row carries a different URL. Behavioral proof — fixture T8 (record id `S029`, url =
the HackerOne FAQ URL that appears in rows S006+S028, while row S029 carries the EUR-Lex URL;
mirrors the real S024/S029 and S006/S028 duplicate-URL pairs my base census confirmed):

```
$ python3 capture-binding-check.py --root cases/T8/lane
MANIFEST round-23 records=1 url_bound=0 fetched=0 archival=1
AUDIT records=1 with_url=1 with_fetched_utc=0 with_archival=1 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0
FAIL rule=url-mismatch record=S029 row=S029 dir=round-23
records=1 bound=0 unbound=1
exit=1
```

No false pass (`url_bound=0`, `bound=0`, exit 1). Companion fixtures: T4 (shared URL across two
different ids, record bound to its own row) → exit 0 with `multi_row_url=1` and no FAIL line
(erratum §4 informational); T9 (two rows with the same id) → `FAIL rule=dup-id record=S006
rows=2`, exit 1; T10 (record url = row url + trailing `/`) → `FAIL rule=url-mismatch`, exit 1
(byte-exactness enforced on the record side).

Harness note (my own defect, corrected): the first battery run had two expectation bugs of mine
(T1/T12 expected 3 records where the trees hold 2; T8's must-not substring `bound=1` collides
with `unbound=1`). Checker behavior was correct in both; corrected expectations re-run clean.

## 3. Q3 — does `--selftest` cover every failure class? YES (11 cases ≥ contract's 6)

`CASES` (L349-411) at `b4182665`: `clean-all-pass`, `missing-manifest-dir` (rule A),
`record-without-url` (B3 `detail=absent`), `url-matching-two-rows` (rebuilt per erratum as
same-id rows → `dup-id`), `url-mismatch`, `no-row` (B1), `shared-url-not-a-failure` (erratum §4,
asserts `multi_row_url=1` present and no `FAIL ` line), `round-32-record-without-fetched_utc`
(C modern), `pre-round-32-record-without-archival` (C legacy), plus two pass-controls
(`round-32-record-with-fetched_utc-passes`, `pre-round-32-archival-passes`). Each case runs the
real file as a subprocess against a fixture tree and asserts exit status AND expected output
lines (L437-449); pass-expected cases additionally assert absence of any `FAIL ` line.

Measured at `b4182665` (twice — ambient env and TMPDIR-probe env):

```
$ python3 corpus/instruments/capture-binding-check.py --selftest
selftest cases=11 failures=0
selftest_exit=0
```

Not covered (none contract-required; residual, §8): no exit-2 (read-error) case, no
missing-record-id case, no trailing-punctuation row-token case.

## 4. Q4 — does `bound=N` count exactly B+C satisfiers? YES

`check` L249-250: `if url_ok and prov_ok: totals["bound"] += 1` — the conjunction, nothing
else. Summary L263-264: `records=<total> bound=<total> unbound=<total-bound>`. Fixture T11
(3 records: B+C ok / B ok C missing / B fail) measured:

```
$ python3 capture-binding-check.py --root cases/T11/lane   (tail)
records=3 bound=2 unbound=1
exit=1
```

Exactly the B+C satisfiers are counted; the C-only-passing record (S098, no row) is unbound.

## 5. Q5 — does it write anywhere? NO

Code inspection: `check` only opens files read-only and prints to stdout; the only writers are
the selftest fixture builders, confined to `tempfile.mkdtemp(dir=scratch_base())`, removed in a
`finally` (L433-469). Behavioral proof at `b4182665` — SHA-256 of every lane file (excluding
`.jj`/`.git`) snapshotted before and after a selftest run plus a live run:

```
LANE-WRITES: NONE
```

## 6. Q6 — does it honour TMPDIR/scratch? YES

`scratch_base` (L425-431): explicit `--scratch` arg → `$HYAKU_SCRATCH` → `$TMPDIR` →
(`/fast/scratch/hyaku` if `/fast/scratch` exists, else `tempfile.gettempdir()`); `mkdtemp(dir=…)`
then honours the chosen base. No hardcoded `/tmp` anywhere in the file. Behavioral proof with
`HYAKU_SCRATCH` unset and `TMPDIR` pointed at a dedicated probe dir:

```
$ env -u HYAKU_SCRATCH TMPDIR=<probe> python3 capture-binding-check.py --selftest
selftest cases=11 failures=0   exit=0
strace -f -e trace=mkdirat,mkdir: 46 mkdir calls with the selftest prefix, 46 under TMPDIR
SCRATCH-LEFTOVER: []            (fixtures removed at exit)
```

## 7. Independent after-column on live bytes (supplements, not replaces, the claim counters)

PRE-STATE (labelled; ExecRegistryAppend had not landed S049/S050 rows, registry rows=48):
`records=40 bound=38 unbound=2`, `FAIL rule=no-row record=S049 dir=round-32` + S050, exit 1 —
failures are the missing rows, not wrong bytes. AFTER (registry rows=50, instrument
`b4182665`, SOURCES.md `b22c7f0173e75e0c…` — the digest ExecRegressionC1 measured quiescent):

```
$ python3 corpus/instruments/capture-binding-check.py   (tail)
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
binding_exit=0
```

`multi_row_url=2` is exactly the two erratum-declared cross-id URL pairs (S029/S024 EUR-Lex,
S006/S028 HackerOne) — matches my base census and ExecRegressionC1 §2.11's independent audit.
Registry token shapes measured independently at rows=50: `rows_with_token_count!=1=0`,
`rows_with_trailing_punct=0` — the two docstring-disclosed loosenings (two-token rows bind
either token; row-token trailing `.,;:` stripped) are unreachable on current bytes.

## 8. Cross-checks and residual risk

Receipts cross-checked: ExecCaptureBinding.md (digest history, selftest 11/0, mutants 4/4,
exit-2 paths, base-byte kill-rule clause) and ExecRegressionC1.md (40/40/0 twice
byte-identical, selftest 11/0, fake-checker rejection, independent audit) — both consistent
with my own measurements; no contradiction found.

Residual risks (disclosed, none contract-violating, none reachable on current bytes):

1. Binding is id-scoped and trusts the manifest `id` field; a record whose capture bytes came
   from another document still binds (the instrument's own docstring limit; byte/quote truth is
   `source-recheck.py`'s job — its round-32 run exits 0 per ExecRegressionC1 §2.6).
2. `ROW_RE` matches `| S0xx |` lines anywhere in SOURCES.md, not only inside the Registry
   section; a future non-registry table reusing S-ids would false-fail `dup-id`. Today all 50
   matching lines are registry rows (census).
3. `snapshot_dirs` counts only top-level files, so a snapshot dir whose captures sit in a
   subdirectory would not be flagged `missing-manifest`; the contract's own glob
   `corpus/source-snapshots/*/manifest.json` is one-level, so this matches the frozen surface
   (CritC1Kill hole (e) in ExecCaptureBinding §8 is the same observation).
4. Row-token trailing-`.,;:` strip and multi-token-row membership are one-directional
   loosenings vs strict byte-match; measured unreachable today (§7).
5. Selftest has no exit-2 / unnamed-id / punctuation case (not in the contract's six).

## 9. Verdict

**lands** — all six review questions answered yes with code-line and behavioral evidence at
the quiescent digest `b4182665ba5cf5441d6495d7de3d59a4c6f8d679d5e9d85c38d16abfb6d0b7f9`; the
frozen predicate's `records=40 bound=40 unbound=0` exit 0 and `selftest cases=11 failures=0`
exit 0 both reproduced independently on live bytes.

Scratch: `$HYAKU_SCRATCH/kasegi-r33/RevC1Instrument` (12 fixture trees + harness + trace) is
removed after this receipt is written; nothing of this seat remains on the scratch disk.
