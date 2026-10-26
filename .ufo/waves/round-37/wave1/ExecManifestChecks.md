# ExecManifestChecks — round-37 capture-manifest binding checks (R20/R21)

Seat: ExecManifestChecks (leaf). Scope: run the committed `corpus/instruments/capture-binding-check.py`
at base, read its rule A/B/C definitions, then construct the planned round-37 S054 manifest record in
scratch and validate it against those rules on a mirror of the base export. Receipt only; no lane file
written, no git mutation, scratch removed at exit.

## Instrument under test (version binding)

| field | value |
|---|---|
| path | `corpus/instruments/capture-binding-check.py` |
| sha256 (base `b56a41680cefd391868c1c370dc063c69d827e7d` export) | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` |
| sha256 (live lane working tree, head `b362068195d5489aa94b31e6ec8f880c367e0ba0`) | `3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa` (identical — base export == head) |
| last commits touching it | `4b0a9f2` (round-34), `9f98488` (round-33) |
| interpreter | Python 3.14.8; curl 8.23.0 (used only for the URL-form probe) |
| tooling installed/upgraded | none (nothing needed; no pacman, no network install) |

## Base run (as assigned)

```
$ cd <base export b56a416> && python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
MANIFEST round-24 records=19 url_bound=19 fetched=0 archival=19
MANIFEST round-25 records=5 url_bound=5 fetched=0 archival=5
MANIFEST round-26 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-28 records=2 url_bound=2 fetched=0 archival=2
MANIFEST round-29 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-30 records=3 url_bound=3 fetched=0 archival=3
MANIFEST round-31 records=1 url_bound=1 fetched=0 archival=1
MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
MANIFEST round-34 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-35 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-36 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=43 with_url=43 with_fetched_utc=5 with_archival=38 snapshot_dirs=12 manifest_dirs=12 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=43 bound=43 unbound=0
EXIT=0
```

Expected `records=43 bound=43 unbound=0 exit=0` — **matched exactly**. The single orphan is the
pre-existing declared orphan `round-*/S040-live.txt` (declared in its manifest, printed on the AUDIT
line, exits 0 by rule A2).

The same command read against the live lane tree (no round-37 capture landed yet; `git status
--porcelain` shows only untracked `.ufo/waves/round-37/…`) also printed `records=43 bound=43
unbound=0` exit 0 — so the PRE-STATE in the frozen claim's `before` list is confirmed against the
live tree, not just the export.

`--selftest` at base: `selftest cases=23 failures=0`, exit 0 (23 fixture verdict lines, all
`verdict=pass`; transcript reproduced below in the control section since the selftest is the
authority for which rule shapes are distinguished).

```
selftest case=clean-all-pass exit=0 want=0 verdict=pass
selftest case=missing-manifest-dir exit=1 want=1 verdict=pass
selftest case=record-without-url exit=1 want=1 verdict=pass
selftest case=shared-url-between-two-records exit=0 want=0 verdict=pass
selftest case=duplicate-id-rows exit=1 want=1 verdict=pass
selftest case=url-mismatch exit=1 want=1 verdict=pass
selftest case=no-row exit=1 want=1 verdict=pass
selftest case=shared-url-not-a-failure exit=0 want=0 verdict=pass
selftest case=round-32-record-without-fetched_utc exit=1 want=1 verdict=pass
selftest case=pre-round-32-record-without-archival exit=1 want=1 verdict=pass
selftest case=round-32-record-with-fetched_utc-passes exit=0 want=0 verdict=pass
selftest case=pre-round-32-archival-passes exit=0 want=0 verdict=pass
selftest case=fetched-utc-pending-rejected exit=1 want=1 verdict=pass
selftest case=fetched-utc-local-offset-rejected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-detected exit=1 want=1 verdict=pass
selftest case=per-file-orphan-listed exit=0 want=0 verdict=pass
selftest case=nested-snapshot-dir exit=0 want=0 verdict=pass
selftest case=nested-snapshot-missing-manifest exit=1 want=1 verdict=pass
selftest case=dup-record-in-manifest exit=1 want=1 verdict=pass
selftest case=double-https-row exit=1 want=1 verdict=pass
selftest case=rejected-row-anchor exit=1 want=1 verdict=pass
selftest case=summary-only-selftest-rejected exit=1 want=1 verdict=pass
selftest case=complete-selftest-report-accepted exit=0 want=0 verdict=pass
selftest cases=23 failures=0
EXIT=0
```

## Rule definitions read (instrument docstring, verbatim substance)

- **A — manifest presence and per-file binding.** Every snapshot directory (one holding
  `manifest.json` or any capture file of its own) must carry a `manifest.json`
  (`FAIL rule=missing-manifest dir=<dir>`), and every capture file in it must be either named by some
  `sources[].path` (A1) or declared in the top-level `orphans` list as
  `{"path": "<name>", "reason": "<non-empty>"}` (A2). An undeclared capture is
  `FAIL rule=orphan-capture`; a declaration with no file is `FAIL rule=orphan-declared-missing`; a
  malformed `orphans` value is a shape error (exit 2). Orphans never move `records=`/`bound=`/`unbound=`.
  Nested snapshot directories are audited in their own right.
- **B — URL binding (id-scoped).** B1 row `| <id> | … |` must exist (`rule=no-row`); B2 row id unique
  (`rule=dup-id`); B3 a `status` cell of `rejected` cannot anchor a record
  (`rule=rejected-row-anchor`); B4 the row's source cell must carry exactly **one** `https://` token
  (`rule=double-https-row row=<id> n=<n>` plus `rule=url-ambiguous record=<id>`), and B5 the record's
  `url` must equal that token **byte-for-byte** after stripping trailing `.,;:` (`rule=url-mismatch`;
  missing `url` is `detail=absent`). A URL repeated across *different* ids is informational
  (`multi_row_url=` on AUDIT), not a failure.
- **C — provenance.** Every record needs a strict-UTC `fetched_utc` (ISO-8601 whose suffix is `Z` or
  `+00:00` and whose fields are a real calendar instant) or `"archival": true`. Placeholder → `pending`;
  non-zero offset → `local-offset`; anything unparsable → `malformed`; absent → `provenance-missing`.
  **The archival exemption is closed for `round-32` and later** (`MODERN_ROUND = 32`), and a directory
  name that does not parse as `round-<N>` counts as modern.
- **D — manifest integrity.** Duplicate `id` or duplicate `path` inside one manifest fails
  (`rule=dup-record field=id|path`).
- Output contract: one `MANIFEST <dir> records=N url_bound=M fetched=K archival=L` per manifest
  directory, one `AUDIT …` line, one `FAIL` line per failure, exactly one
  `records=<total> bound=<total> unbound=<U>` summary; `bound` = records passing **B and C**;
  exit 0 only when no `FAIL` line was emitted, 1 on failure, 2 on usage/read/shape error.

## Planned record (as constructed in scratch for F20 / S054)

Fetch made with the lane's own instrument (`capture-source.py --id S054 --url
https://certcc.github.io/SSVC/ --kind html`, instrument UA `kasegi-shokunin/1.0 (documentation
capture; …)`), output written only under my scratch dir:

```
S054 status=200 fetched_bytes=105807 snapshot_bytes=7730 sha256=a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56 utc=2026-10-26T17:02:58Z
```

Probe snapshot: 7730 bytes, 286 lines (file ends with a newline; matches the round-36 convention where
`lines` == `wc -l`). Record as validated:

```json
{
  "id": "S054",
  "path": "S054.txt",
  "url": "https://certcc.github.io/SSVC/",
  "fetched_utc": "2026-10-26T17:02:58Z",
  "fetched_bytes": 105807,
  "snapshot_bytes": 7730,
  "lines": 286,
  "sha256": "a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56",
  "normalized": "capture-source.py html_to_text(): <script>/<style> removed, block tags (p div li tr h1-h6 section article br) to newlines, remaining tags stripped, html.unescape() applied, runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8; final newline",
  "quotes": []
}
```

The registry row used in the mirror kept the *shape* of `S053` (`| id | <name> — <bare URL> | docs | A |
scope | anchor | teaches | mined | 2026-10-26 | 90d | <used-by> |`); its scope/anchor/teaches text was
labelled "scratch mirror row, binding validation only" because authoring those cells is not this
seat's scope (R20/R21 is the binding, not the row prose).

**Validate result: PASS.** Mirror (base export + one appended S054 row + `corpus/source-snapshots/
round-37/{S054.txt,manifest.json}`) run end-to-end:

```
MANIFEST … round-36 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=44 with_url=44 with_fetched_utc=6 with_archival=38 snapshot_dirs=13 manifest_dirs=13 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=44 bound=44 unbound=0
EXIT=0
```

This reproduces the frozen claim's counting command `python3 corpus/instruments/capture-binding-check.py
-> records=44 bound=44 unbound=0 exit 0` byte-for-byte, on a tree whose only delta from base is the S054
row + capture directory. Direct rule probes against the same mirror (imported functions, no shell
guessing):

| check | observed |
|---|---|
| `load_registry` row count base → mirror | 53 → 54, `S054` present exactly once |
| S054 source cell parsed | `SSVC — … — https://certcc.github.io/SSVC/` |
| `row_tokens(cell)` | `['https://certcc.github.io/SSVC/']` — one token, `== [record url]` |
| `url_row_count(cells, 'https://certcc.github.io/SSVC/')` | base 0 → mirror **1** (unique row) |
| `double_https_rows(rows)` | `[]` (no two-token row anywhere) |
| duplicate row ids | none |
| `classify_fetched('2026-10-26T17:02:58Z')` | `(True, None)` — strict UTC |
| `classify_fetched('…+00:00')` | `(True, None)` — also accepted by the instrument |
| `classify_fetched('…+02:00')` | `(False, 'local-offset')` — rejected |
| `parse_round('round-37')` | `37`; `provenance_ok(record, 37)` → `(True, True, False, None)` |
| `multi_row_url` before/after | 2 → 2 (the pre-existing S024/S029 and S006/S028 duplicates; S054's URL collides with nothing) |

## Discriminating controls (the validation is not vacuous)

Each control is a separate copy of the same mirror with one field perturbed; all exited as predicted.

| control | perturbation | observed | verdict |
|---|---|---|---|
| C1 registry markdown link | cell carries `[SSVC](https://certcc.github.io/SSVC/)` (token keeps `)`) | `exit=1`, `FAIL rule=url-mismatch record=S054 row=S054 dir=round-37`, `records=44 bound=43 unbound=1` | rejected — registry cell **must** carry the bare URL, not a Markdown link |
| C2 no trailing slash | record `url=https://certcc.github.io/SSVC` | `exit=1`, `FAIL rule=url-mismatch record=S054 row=S054` | rejected — byte equality is exact |
| C3 archival in a modern round | round-37 record with `"archival": true`, no `fetched_utc` | `exit=1`, `FAIL rule=provenance-missing record=S054 dir=round-37`, `MANIFEST … fetched=0 archival=1` | rejected — archival exemption closed at round-32+, so a round-37 record **must** carry `fetched_utc` |
| C4 extra file in the capture dir | `S054.headers.txt` added next to `S054.txt` | `exit=1`, `FAIL rule=orphan-capture file=S054.headers.txt dir=round-37`, `orphans=2 orphan=S040-live.txt orphan=S054.headers.txt` | rejected unless declared; with `orphans:[{path,reason}]` the same tree exits 0 and the file is printed on AUDIT (`records=44 bound=44 unbound=0` unchanged) |
| C5 two https tokens in the row cell | `https://certcc.github.io/SSVC/ and https://certcc.github.io/SSVC/howto/` | `exit=1`, `FAIL rule=double-https-row row=S054 n=2` + `FAIL rule=url-ambiguous record=S054 row=S054 tokens=2` | rejected — the S054 row's source cell must name exactly one URL |
| C6 id/path stem mismatch | record `path=S054-ssvc.txt`, `id=S054` | capture-binding-check `exit=0` (**does not judge stems**); `source-recheck.py --source S054` `exit=1`, `S054:manifest MISMATCH reason=stem-mismatch` | stem equality is enforced by `source-recheck.py` rule B1, not by the binding checker |

## Cross-instrument findings for the seat that lands the real capture

1. **`quotes` are required downstream, not by this checker.** With `"quotes": []` the binding checker
   passes (it never reads quotes), but `source-recheck.py` exits **2** with
   `S054:manifest UNAVAILABLE reason=missing-quotes`. Adding one genuine quote from the same capture
   makes both green:
   ```
   $ python3 corpus/instruments/source-recheck.py --manifest …/round-37/manifest.json --source S054
   S054:sha256 OK
   S054:Q1 OK occurrences=1 anchor=203-ok
   EXIT=0
   ```
   (quote `SSVC stands for A Stakeholder-Specific Vulnerability Categorization.`, anchor L203 of my
   probe snapshot, single occurrence). The frozen claim's counting command
   `source-recheck.py … --source S054 -> exit 0` therefore depends on a non-empty `quotes[]` list.
2. **Field enforcement split.** `capture-binding-check.py` reads only `id`, `path`, `url`,
   `fetched_utc`, `archival`. `source-recheck.py` reads `path` (stem == id), `sha256` (must equal the
   capture's digest) and `quotes[]`. `fetched_bytes`, `snapshot_bytes`, `lines` and `normalized` are
   **documentation-only — no instrument verifies them**; keep them accurate by hand.
3. **URL form is load-bearing, measured 2026-10-26T17:03Z with the instrument UA:**
   `https://certcc.github.io/SSVC/` → `200`, no redirect; `https://certcc.github.io/SSVC` → `301`,
   `location: https://certcc.github.io/SSVC/`; `https://certcc.github.io/ssvc/` → `404`. The record and
   the registry token must both be the 200 form `https://certcc.github.io/SSVC/` (trailing slash,
   upper-case path), or rule B5 fails.
4. **The existing CERT/CC row does not collide.** `S004` carries
   `https://certcc.github.io/certcc_disclosure_policy/`; the substring test in `url_row_count` counts
   zero rows for the SSVC URL at base and exactly one after the S054 row, so `multi_row_url` stays 2 and
   the W04 census remains S028/S029-only.
5. **The staged campaign id `S054` carries no payload** (`.ufo/waves/round-37/assimilation/
   quarantine-slice` marks it `payload-absent`). The lane row must therefore be authored against the
   round-37 live capture; if the row is copied from the staged text without the capture, the record
   fails rules B/A rather than passing silently — the id alone is not evidence.

## Risks / notes

- My fetch instant `2026-10-26T17:02:58Z`, `sha256 a6613315…bb56`, 7730 snapshot bytes / 105807 fetched
  bytes / 286 lines are **probe measurements**, not claims about the bytes the landing seat commits.
  If that seat fetches later, its `fetched_utc`/`sha256`/`snapshot_bytes`/`lines` will differ and must
  be copied from its own `capture-source.py` line; my binding verdict holds for any strict-UTC stamp
  and any digest, because the checker compares neither to a fixed expectation — only `source-recheck`
  compares the digest to the file, and it passed on my probe bytes.
- The mirror registry row's scope/anchor/taught cells are scratch prose by construction; a real row
  whose *source cell* is not `<name> — <bare URL>` (e.g. Markdown link, two URLs, trailing `)`) breaks
  binding exactly as controls C1/C5 show.
- Nothing outside my scratch dir was written; no git mutation; no pacman/network install; the lane tree
  is byte-identical to how I found it (`git status --porcelain` unchanged: only the pre-existing
  untracked `.ufo/waves/round-37/…` paths). Scratch `/fast/scratch/hyaku/kasegi-r37/ExecManifestChecks`
  removed after this receipt was written; no `capture-binding-selftest-*` leftover dirs remain under
  `/fast/scratch/hyaku`.
