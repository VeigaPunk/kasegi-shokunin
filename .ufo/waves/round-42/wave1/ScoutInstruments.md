# ScoutInstruments — receipt (kasegi-shokunin round 42, wave 1)

Seat: ScoutInstruments (leaf scout; write scope: this receipt + ScoutInstruments.txt
+ scratch only). Assignment: inventory the C2 instrument chain
(source-recheck.py, capture-binding-check.py, frontier-recheck-count.py,
recheck-audit.py, knowledge-expected.txt) — entry points, the CLI args the frozen
C2 counting commands use, where manifest/capture paths are bound, and map the two
r41 wave-2 findings (missing-path/URL-variant acceptances; status-flip blind spot)
to the exact function+line the J6/J7 repair must touch.

## Deliverable

- `.ufo/waves/round-42/wave1/ScoutInstruments.txt` — 312 lines, sha256
  `ece3d21ce5936c69fd5cf04f7d0e84b4b0a2bb88189643cb3554cc0648bf0ebe`.

## Method

- Read `.ufo/waves/round-42/claims.json` (C1/C2 predicates, kill rules, counting
  commands, before-controls) first; the C2 counting commands were copied verbatim.
- Read all five instruments fully (entry points, rule limbs, selftest plumbing);
  read the r41 wave-2 attack receipts MutBindingExistence.md, MutC2Chain.md,
  MutFrontierParser.md, MutFreshnessCensus.md, MutAuditUnexpected.md,
  RevCaptureNormalization.md and corpus/lessons/round-41-verifier-spotcheck.md §5.
- Empirical verification on a disposable fixture lane under scratch (no lane bytes
  touched): replayed the missing-path, url-case, url-trailing-slash and
  capture_url-only mutations against the real committed
  capture-binding-check.py bytes, and the admitted->explored/parked status flips
  against the real committed frontier-recheck-count.py bytes.
- Disk guard green before fixture runs (`disk-guard.sh status`: /tmp 5%, /var/tmp
  36%, /fast/scratch/hyaku 27%). No tools installed/upgraded. No network fetch.
  No mutating git/jj command anywhere; only writes were the two wave1 files and
  scratch, removed at yield.

## Live-lane baseline outputs (verbatim; match c2-controls/before.txt values)

```
$ python3 corpus/instruments/capture-binding-check.py | tail -4
MANIFEST round-41 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=55 with_url=55 with_fetched_utc=17 with_archival=38 snapshot_dirs=17 manifest_dirs=17 missing_manifest=0 multi_row_url=3 orphans=1 orphan=S040-live.txt
records=55 bound=55 unbound=0        exit=0
$ python3 corpus/instruments/frontier-recheck-count.py | tail -2
PASS     F24  knowledge/rfc-9116-security-txt.md                   ids=S063           exit=0
entries=27 pass=27 exit=0            exit=0
$ python3 corpus/instruments/recheck-audit.py --quiet | tail -4
strict pass=60/60 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=36 gated=24 broken=0 ...
lines=60 total=60 pass=60 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=60 missing=0 unexpected=0 exit=0      exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-41/manifest.json --source S063
S063:sha256 OK / Q1..Q3 OK anchors=330/270/235-ok      exit=0
```

All 24 `| F<n> |` README rows currently carry status `admitted` — so requiring
admitted rows to PASS is a safe J7 semantics.

Instrument sha256 prefixes (committed bytes): source-recheck fd2e01e88c8c45a9,
capture-binding-check 3d9e5e0ddbaaccf9, frontier-recheck-count 1be79af60cb5cb4c,
recheck-audit 5d4842da6103f17c, knowledge-expected.txt e030a8af914cadf2.

## Empirical mutation results (fixture lane, real instrument bytes)

Fixture: minimal lane (corpus/SOURCES.md with S001+S063 rows; round-41 snapshot
dir with manifest.json + S063.txt; instrument copied unmodified), plus a frontier
fixture (README F01/F02 admitted, two entries citing S001, stub source-recheck.py
exiting 0, schema-1 manifest).

| Mutation | Instrument output | Verdict |
|---|---|---|
| path=S063-missing.txt, real S063.txt left in place | `FAIL rule=orphan-capture file=S063.txt`, `records=1 bound=1 unbound=0`, exit 1 | killed (orphan direction fires; unbound still 0 — the FAIL not the tally carries the red) |
| path=S063.txt, file DELETED (no stray file) | `records=1 bound=1 unbound=0`, exit 0 | **SURVIVED — the live missing-path blind spot** |
| url+capture_url -> `…/RFC/rfc9116.txt` (case) | `FAIL rule=url-mismatch record=S063 row=S063`, unbound=1, exit 1 | killed by bind_record L303 |
| url+capture_url -> `…/rfc9116.txt/` (slash) | same url-mismatch, unbound=1, exit 1 | killed |
| capture_url -> `https://evil.invalid/…` (url intact) | `records=1 bound=1 unbound=0`, exit 0 | **SURVIVED — secondary URL field unbound** |
| F02 status `admitted` -> `explored` | `entries=1 pass=1 exit=0`, no FAIL line | **SURVIVED — F-FLIP denominator drop** |
| F02 status `admitted` -> `parked` | `entries=1 pass=1 exit=0` | SURVIVED |

## Finding-to-repair-site map (headline of the deliverable)

- **Missing-path (F-BIND):** `capture-binding-check.py` `check()` — record loop
  L394-428 / `bound_paths` L434-436. No line ever checks `record["path"]` exists;
  docstring L125-128 disclaims it. Silent variant = absent file with no stray
  capture (reproduced exit 0). Repair: `os.path.isfile(join(path, rec["path"]))`
  limb + FAIL; also decide absent/non-string path fields (excluded from
  bound_paths silently at L435-436) and `../` escape.
- **URL-variant (F-BIND):** `bind_record()` L297-304 — only `record.get("url")`
  is bound; `capture_url`/`http.final_url`/`files[]`/`used_by` never read
  anywhere in the file. url mutations already die (url-mismatch); capture_url
  divergence survives (reproduced exit 0). The r41 receipt's claim that
  both-fields mutation survived cannot reproduce on current bytes — J6 replay
  should bind secondary URL fields regardless; flag to suite author.
- **Status-flip (F-FLIP):** `frontier-recheck-count.py` `main()` L393 —
  `admitted = [r for r in rows if r[2] == "admitted"]` drops flipped rows before
  evaluate(); `_status` captured at L395 is discarded. Repair: evaluate every
  F-row (new problem e.g. row-status-not-admitted) or hard-fail non-admitted
  rows; fail_closed L419 propagates. Selftest template SELFTEST_README L252-256
  may need a parameterizable status cell (current template emits only admitted).
- **Replay-limb mechanics for the r42 suite:** both instruments take `--root`
  (capture-binding L873; frontier L377), so replay = exported instrument binary
  vs mutated scratch lane root. The r41 suite never invoked either instrument
  (`run_check` L1593-1596 dispatches only `check_i*` shell functions) — J6/J7
  are new limbs.

## Remaining unknowns / routed observations (not asked, recorded once)

- `record["files"]` array and `used_by`/`used-by` fields are unbound by every
  C2 instrument (MutC2Chain probe E was inconclusive; census E11 owns
  dangling-usedby). In-family or new family is the L1's call.
- r41 attack receipts named a `kasegi-r41-falsify-results.json`; the committed
  defeat *artifacts* for binding/frontier were not found as fixture trees —
  J6/J7 replay limbs will reconstruct the mutations from the receipts.
