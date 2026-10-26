# ExecC2Binding — capture-manifest binding verification (round 38)

Seat: ExecC2Binding (leaf, no spawns). Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; lane HEAD at seat start `700153593eb586c70a6499c8ca225ee4d673bc9b`
(wave1 spec/claims only; `git diff --name-only a173b0c HEAD` lists only `.ufo/waves/round-38/*`). Frozen claims read
(`.ufo/waves/round-38/claims.json`): C2 counting command `python3 corpus/instruments/capture-binding-check.py -> records=45 bound=45 unbound=0`.
Scratch: `/fast/scratch/hyaku/kasegi-r38/ExecC2Binding/` (removed before yield).

Verdict: the binding check passes `records=44 bound=44 unbound=0` at base and `records=45 bound=45 unbound=0` with a
round-38 S055 capture + manifest record + registry row. The check is a URL/provenance/file-accounting gate, **not** a
content gate: a wrong `sha256`, a missing capture file and a wrong `lines` value do **not** move it (measured below);
those pins belong to `source-recheck.py` (sha256/quotes) or to no instrument (`lines`). Binding-native mutations
(wrong url, pending `fetched_utc`, undeclared orphan, duplicate record) exit 1.

## 1. Baseline at base — expected records=44 bound=44 unbound=0

`git archive` of the base commit into a scratch mirror (read-only git), then the committed instrument:

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive a173b0c2b98c5ae39599fa9be76027fbbead0b9e | tar -x -C $S/mirror-base
$ python3 $S/mirror-base/corpus/instruments/capture-binding-check.py --root $S/mirror-base
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
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=44 with_url=44 with_fetched_utc=6 with_archival=38 snapshot_dirs=13 manifest_dirs=13 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=44 bound=44 unbound=0
EXIT=0
```

Same instrument run in-tree on the live lane HEAD produced the identical 44/44/0, exit 0 (corpus tree identical to base).

## 2. Instrument rules read (module docstring + code, `corpus/instruments/capture-binding-check.py`)

Four rules; exit 0 only with zero `FAIL` lines, 1 on any failure, 2 on read/shape errors:

- **A. Manifest presence + per-file binding.** Every snapshot dir (holds `manifest.json` or any capture file) must
  carry a manifest (`FAIL rule=missing-manifest`). Each direct capture file must be named by some record `path` (A1)
  or declared in top-level `orphans` as `{"path", "reason"}` (A2); otherwise `FAIL rule=orphan-capture`. A declared
  file that is absent is `FAIL rule=orphan-declared-missing`; a malformed orphans list is exit 2. Orphans never change
  `records=/bound=/unbound=`. Nested dirs are audited independently; a parent only checks its own direct files.
- **B. URL binding (id-scoped).** `id` must name a registry row (`no-row`), the id must be unique (`dup-id`), the row's
  status must not be `rejected` (`rejected-row-anchor`), the row's source cell must hold exactly one `https://` token
  (`url-ambiguous` / `double-https-row`), and the record `url` must equal that token byte-for-byte (`url-mismatch`,
  `detail=absent` when the field is missing).
- **C. Provenance.** `fetched_utc` must be strict UTC ISO-8601 (`Z` or `+00:00`, real calendar instant) or the record
  must carry `"archival": true`. Round-32+ (and non-`round-<N>` dirs) require `fetched_utc`; the archival exemption is
  closed there. Placeholder -> `detail=pending`; non-zero offset -> `detail=local-offset`; unparsable ->
  `detail=malformed`; absent -> `rule=provenance-missing`.
- **D. Integrity.** Duplicate `id` or `path` within one manifest -> `FAIL rule=dup-record field=<f> value=<v> count=<n>`.

`bound` = records passing B **and** C; `unbound = records - bound`. Rule-A and rule-D failures leave `unbound` at 0
while still exiting 1 (measured M7/M8) — **the exit status is the verdict**, not the summary line.

## 3. Mirror with round-38 S055 — expected records=45 bound=45 unbound=0

Mirror: `git archive HEAD` into `$S/mirror` (7297 files). Added three things, mirror only:

1. `corpus/source-snapshots/round-38/S055.txt` — a real CSAF v2.0 normalization:

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 \
    -o $S/S055.raw.html -w 'http_status=%{http_code} size_download=%{size_download} content_type=%{content_type} url_effective=%{url_effective} redirects=%{num_redirects}\n' \
    https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
fetch_utc=2026-10-26T18:27:51Z
http_status=200 size_download=414858 content_type=text/html url_effective=https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html redirects=0
curl_exit=0
fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b  $S/S055.raw.html

# normalized with the lane's own corpus/instruments/capture-source.py html_to_text()
snapshot_bytes=272441 lines=5146 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
$ sha256sum .../round-38/S055.txt ; wc -lc .../round-38/S055.txt
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  .../round-38/S055.txt
  5146 272441 .../round-38/S055.txt
```

2. `corpus/source-snapshots/round-38/manifest.json` — `schema_version: 1`, one `sources[]` record for S055 with
   `id/path/url/fetched_utc/fetched_bytes/snapshot_bytes/lines/sha256/normalized/raw_sha256/http/quotes`
   (5 quotes, all `occurrences=1`: product_status definition L1855, eight status categories L1855, VEX not-affected
   justification sentence L1762, `component_not_present` code L1763, known_not_affected impact-statement rule L2152).
3. `corpus/SOURCES.md` — appended row `| S055 | ... https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html ... | mined | 2026-10-26 | ... |`
   (rule B needs the registry row; the mirror's row count goes 54 -> 55).

Result:

```
$ python3 corpus/instruments/capture-binding-check.py --root $S/mirror
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
...
MANIFEST round-37 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=45 with_url=45 with_fetched_utc=7 with_archival=38 snapshot_dirs=14 manifest_dirs=14 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=45 bound=45 unbound=0
EXIT=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=1855-ok
S055:Q2 OK occurrences=1 anchor=1855-ok
S055:Q3 OK occurrences=1 anchor=1762-ok
S055:Q4 OK occurrences=1 anchor=1763-ok
S055:Q5 OK occurrences=1 anchor=2152-ok
EXIT=0
```

## 4. Mutation matrix (one `cp -a` copy of the mirror per mutation; actual output)

| # | mutation | binding exit | binding tail | source-recheck exit | catching instrument |
|---|---|---|---|---|---|
| M1 | `sha256` -> 64 zeros | **0** | `records=45 bound=45 unbound=0` | 1 | source-recheck: `S055:sha256 MISMATCH expected=000…000 actual=63c8ad52…` |
| M2 | delete `S055.txt` | **0** | `records=45 bound=45 unbound=0` | 2 | source-recheck: `S055:source UNAVAILABLE reason=missing` |
| M3 | `lines` 5146 -> 9999 | **0** | `records=45 bound=45 unbound=0` | 0 | **none** — `lines` is descriptive; both instruments pass |
| M4 | Q5 quote -> text from a different line | **0** | `records=45 bound=45 unbound=0` | 1 | source-recheck: `S055:Q5 MISMATCH reason=quote-not-found` |
| M5 | record `url` -> `https://example.invalid/csaf` | **1** | `FAIL rule=url-mismatch record=S055 row=S055 dir=round-38` / `records=45 bound=44 unbound=1` | — | binding check (rule B) |
| M6 | `fetched_utc` -> `pending` | **1** | `FAIL rule=fetched-utc record=S055 dir=round-38 detail=pending` / `records=45 bound=44 unbound=1` | — | binding check (rule C) |
| M7 | add undeclared `S055-extra.txt` | **1** | `FAIL rule=orphan-capture file=S055-extra.txt dir=round-38` / `records=45 bound=45 unbound=0` | — | binding check (rule A; exit 1, unbound unchanged) |
| M8 | duplicate the S055 record | **1** | `FAIL rule=dup-record field=id value=S055 count=2 dir=round-38` + same for `field=path` / `records=46 bound=46 unbound=0` | — | binding check (rule D; exit 1, unbound unchanged) |

Exact tails for M5–M8 (from the runs):

```
### M5 wrong url        binding exit=1  records=45 bound=44 unbound=1  FAIL rule=url-mismatch record=S055 row=S055 dir=round-38
### M6 pending stamp   binding exit=1  records=45 bound=44 unbound=1  FAIL rule=fetched-utc record=S055 dir=round-38 detail=pending
### M7 orphan capture   binding exit=1  records=45 bound=45 unbound=0  FAIL rule=orphan-capture file=S055-extra.txt dir=round-38
### M8 duplicate record binding exit=1  records=46 bound=46 unbound=0  FAIL rule=dup-record field=id value=S055 count=2 dir=round-38
                                       FAIL rule=dup-record field=path value=S055.txt count=2 dir=round-38
```

## 5. Findings for the C2 seat / L1

1. **The binding check does not read capture bytes.** `sha256`, `quotes`, `lines` are never opened by it (rule A binds
   by file name only; the docstring's "Known limits" says the reverse direction and content pinning are
   `source-recheck.py`'s job). Therefore M1 (wrong sha256) and M2 (missing file) leave `records=45 bound=45 unbound=0`,
   exit 0; `source-recheck.py` fails them (exit 1 / exit 2). The C2 claim's kill rule already pairs
   `binding 45/45` with `source-recheck S055 exit 0`, so the pair is sound — but a green binding run alone does not
   prove the capture bytes.
2. **`lines` is bound by nothing.** M3 shows both instruments exit 0 with `lines=9999`. Treat `lines` as a human
   convenience field, not evidence.
3. **`unbound=0` is not the verdict.** Rule-A (orphan) and rule-D (dup-record) failures exit 1 while `unbound` stays 0
   (M7, M8). Only rule-B/rule-C failures move `unbound`. The claim's counting command must be read as
   "`records=45 bound=45 unbound=0` **and** exit 0".
4. **Rule B needs the registry row.** A manifest record alone cannot reach 45/45: without the `| S055 |` row the record
   is `FAIL rule=no-row`. The mirror therefore appended the row (URL byte-equal to the record `url`, status `mined`).
   The landed C2 change must land `corpus/SOURCES.md` row S055 and the manifest record in the same commit.
5. **Byte-equality is exact.** The record `url` must be the row's single `https://` token with trailing `.,;:` stripped;
   a row with two tokens fails as `url-ambiguous` before the record is compared.

## DELIVERABLE

```text
Manifest shape required by corpus/instruments/capture-binding-check.py (round 38, schema_version 1).

Top-level JSON object:
  sources   list, REQUIRED. One record object per captured source. Absent or non-list -> UNAVAILABLE, exit 2.
  orphans   list, OPTIONAL. Each entry is an object {"path": "<file name in this snapshot dir>", "reason": "<non-empty>"}.
            Malformed list/entry -> UNAVAILABLE, exit 2. A declared path with no matching file ->
            FAIL rule=orphan-declared-missing. Orphans never change records=/bound=/unbound=.

Each sources[] record (all four fields are enforced by the binding check):
  id           non-empty string naming exactly one corpus/SOURCES.md row `| S0xx | ... |` (rule B1/B2:
               missing row -> no-row; duplicate id -> dup-id). That row's status cell (column 8) MUST NOT be
               "rejected" (B3), or FAIL rule=rejected-row-anchor.
  url          non-empty string equal byte-for-byte to the single https:// token in that row's source cell
               (column 2; trailing . , ; : stripped). A row with two or more tokens -> url-ambiguous;
               any difference, or an absent url -> url-mismatch (B4/B5).
  fetched_utc  strict-UTC ISO-8601 string ("YYYY-MM-DDTHH:MM:SS[.frac]Z" or "...+00:00", real calendar
               instant). REQUIRED for round-32 and later snapshot dirs (round-38 included). Placeholder ->
               detail=pending; non-zero offset -> detail=local-offset; unparsable -> detail=malformed;
               absent -> FAIL rule=provenance-missing (rule C). `"archival": true` (boolean) substitutes
               only for round-<N> dirs with N < 32.
  path         string naming a file directly inside the same snapshot directory (rule A1). Every direct
               file must be named by some record's path or declared in orphans (A2), else FAIL
               rule=orphan-capture. Two records naming the same path/id -> FAIL rule=dup-record (rule D).

Fields the binding check never reads (other instruments / prose own them):
  sha256, quotes, anchor, fetched_bytes, snapshot_bytes, lines, normalized, raw_sha256, http, schema_version.
  sha256 and quotes are enforced by source-recheck.py; `lines` is descriptive metadata that no instrument
  verifies (a wrong value passes both instruments: measured mutation M3).

Verdict line: `records=<N> bound=<M> unbound=<N-M>`; exit 0 only when no FAIL line exists. A rule-A
orphan failure or a rule-D duplicate failure leaves unbound=0 and still exits 1.
```

Deliverable block (exact fenced bytes, final newline included): 31 lines, 2509 bytes,
sha256 `b9a2cc9eb8e98d90daaeaeebcf08dfe6bf4ce86a6d4118b11d7a90a041460635`.

## 6. Tooling, scratch and hygiene

- Python 3.14.8 (preinstalled, `/usr/bin/python3`). No installs, no upgrades, no pacman invocation, no host service
  touched. No network fetch beyond the single CSAF GET recorded above (HTTP 200, 414858 bytes, 2026-10-26T18:27:51Z).
- All work under `/fast/scratch/hyaku/kasegi-r38/ExecC2Binding/` (`mirror`, `mirror-base`, `mut-*`, raw HTML); the
  directory is removed before yield. No write touched the lane tree, the fleet root, or shokuknow: `git status` in the
  lane showed only the pre-existing untracked `.ufo/waves/round-38/wave1*` entries.
- No mutating git: only `git archive`/`rev-parse`/`diff`/`log`/`status` against the lane repo.

## 7. Risks / blockers

- None blocking. The only divergence from the item's phrasing is factual, not a gap: the three named mutations
  (wrong sha256, missing file, wrong lines) are not binding-check rules — measured exits are 0/0/0 for the binding
  check, with source-recheck catching the first two and no instrument catching `lines`. Binding-native mutations
  (M5–M8) demonstrate `unbound`/exit 1. If the round-38 C2 receipt cites `binding 45/45` as evidence of capture
  integrity, it must cite `source-recheck S055 exit 0` alongside it.
