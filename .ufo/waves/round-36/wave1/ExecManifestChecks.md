# ExecManifestChecks — round 36 wave 1 — round-36 capture-manifest schema validation (S053 / F19)

Seat: `ExecManifestChecks` (executor, leaf — no subagents, no dispatches, no background jobs, no
`agent://all`). Lane: `kasegi-shokunin` (only write scope; this receipt is my only lane write).
Lane base `cc692008b0cfd58d18275aa6c4aed79620120799`; claims-freeze and HEAD at every read of mine
`b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`.

Assignment: validate the round-36 capture-manifest schema proposed by `ExecC2Capture` — fields
`url/fetched_utc/fetched_bytes/sha256/lines/normalized` on every record, `url` equal to the registry
row URL exactly, `fetched_utc` strict ISO8601 with `Z` — by running
`python3 corpus/instruments/capture-binding-check.py` logic over the scratch manifest, and report
bound/unbound counts with recorded outputs.

Method: two independent passes, both read-only against the lane.
(1) **End-to-end** — fixture lane roots (a byte copy of the real `corpus/SOURCES.md` plus one
drafted S053 row, plus `corpus/source-snapshots/round-36/` holding a manifest and a capture) run
through the committed instrument `capture-binding-check.py --root <fixture>`; the instrument has
**no `--manifest` flag** (its entry points are `--root`, `--selftest`, `--scratch`; `main()`
`:871-889`), so `--root` over a fixture root is the faithful equivalent.
(2) **Logic-level** — I imported the instrument's own `load_registry`, `bind_record`,
`provenance_ok`, `classify_fetched`, `row_tokens` from the committed file and evaluated each proposed
record against them directly. Source-recheck (which *does* take `--manifest`) was run over the same
scratch manifest. No git mutation, no network, no install.

Scratch: `/fast/scratch/hyaku/kasegi-r36/ExecManifestChecks/` (`validate.py`,
`validate_actual.py`, `validate.out`, `actual.out`, `fx/`, `actual/`), removed at yield after
copying every number into this receipt. Tooling: none installed; host `python3` is 3.14.8; no pacman.

## Report

### 0. Verdict

The schema is **sound and the landed `ExecC2Capture` manifest passes both gates**:

| object | gate | result |
|---|---|---|
| actual C2 manifest + a bare-URL S053 registry row | `capture-binding-check.py --root` | `records=1 bound=1 unbound=0` `exit=0` |
| actual C2 manifest | `source-recheck.py --manifest … --source S053` | `S053:sha256 OK`, `Q1..Q4 OK occurrences=1 anchor=N-ok`, `exit=0` |
| real lane HEAD `b47f2cd` (no regression baseline) | `capture-binding-check.py --root .` | `records=42 bound=42 unbound=0` `exit=0` |
| the instrument itself | `--selftest --scratch …` | `selftest cases=23 failures=0` `exit=0` |

Three schema-level gaps remain outside what any committed gate enforces (`fetched_bytes`/`lines`/
`normalized` unread; `+00:00` accepted where the contract says `Z`; a missing capture passes the
binding check). Details in §5-§8. Binding counts under every mutant are in §3.

### 1. Artifact facts I validated against

- Capture `S053.txt`: 8448 bytes, 244 lines (`splitlines()` = `wc -l` = 244), sha256
  `4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9`; UTF-8, final newline, no
  markup (`<[a-zA-Z/!]` → 0 matches), no double space/tab/NBSP (normalization holds).
- Served body `raw.html`: 26804 bytes = the `content-length` in `headers.txt`; `HTTP/2 200`,
  `content-type: text/html; charset=UTF-8`.
- Manifest: 3566 bytes, sha256 `f9590c2bbc26244af88dce8fa7c291d67e6138c293ba5198257789911c017da3`.
  `ExecC2Capture` removed its scratch dir before my later probes landed (`cp: …/manifest.json: No such
  file or directory`), so PASS 5-7 re-ran against my preserved byte copy at
  `actual/bare_url/corpus/source-snapshots/round-36/manifest.json` (same digest); PASS 0-4 and the
  direct `source-recheck` run used the original path while it existed.
- Real registry at `b47f2cd`: 52 rows, `url_row_count(cells, "https://www.first.org/epss/") = 0`,
  `double_https_rows = []` — the URL is net-new, so `multi_row_url` stays 0 once S053 lands alone.

The validated record, verbatim (this is the object the count in §0 refers to):

```json
{
  "id": "S053",
  "path": "S053.txt",
  "url": "https://www.first.org/epss/",
  "fetched_utc": "2026-10-26T15:35:10Z",
  "fetched_bytes": 26804,
  "snapshot_bytes": 8448,
  "lines": 244,
  "sha256": "4ec61c59b0e9aedf89bb2cc3ba59f600e3b406599d1b2f8f89f43e03a16783e9",
  "normalized": "capture-source.py html_to_text(): <script>/<style> removed, block tags (p div li tr h1-h6 section article br) to newlines, remaining tags stripped, html.unescape() applied, runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8; final newline",
  "http": {"status": 200, "content_type": "text/html; charset=UTF-8",
           "final_url": "https://www.first.org/epss/", "redirects": 0,
           "user_agent": "kasegi-shokunin/1.0", "fetched_utc": "2026-10-26T15:35:10Z"},
  "quotes": [
    {"id": "Q1", "anchor": 216, "quote": "(EPSS) is a data-driven machine-learning model that estimates the probability that a published CVE will be exploited in the wild in the next 30 days."},
    {"id": "Q2", "anchor": 217, "quote": "EPSS publishes a 0–1 probability (with ranking percentiles)"},
    {"id": "Q3", "anchor": 217, "quote": "every day for every CVE and makes the data freely and openly accessible via CSV and API as well as a github repo"},
    {"id": "Q4", "anchor": 235, "quote": "EPSS is maintained by the EPSS Special Interest Group at FIRST. Scores are generated by Empirical Security and published freely to the community."}
  ]
}
```

(top level also carries `schema_version: 1` and a `purpose` prose block; both instruments ignore
`purpose` and both accept `schema_version` 1 — `source-recheck.py:29,64-70`.)

### 2. What the two gates actually require — schema acceptance set

Read from the committed bytes, not from prose:

| field | `capture-binding-check.py` | `source-recheck.py` | verdict |
|---|---|---|---|
| top-level key | `sources` list required, else `exit 2 UNAVAILABLE reason=manifest-shape` (`:383-385`) | `sources` non-empty required (`:67-70`) | **`sources`, not `records`** |
| `id` | row lookup, must be a single non-`rejected` row (`:283-305`) | `[A-Za-z0-9][A-Za-z0-9._-]*`, unique (`:31,48-50`) | required, `S053` |
| `path` | capture-coverage key (`:434-444`) | stem must equal `id` (B1, `:124-126`) | required, `S053.txt` |
| `url` | byte-equality with the row's single `https://` token, trailing `.,;:` stripped (`:182-185,283-305`) | not read | required |
| `fetched_utc` | strict UTC or `+00:00`, real calendar instant; mandatory at round ≥ 32 (`:162-175,249-281`) | not read | required |
| `sha256` | not read | 64 lowercase hex, must equal the capture's digest (`:128-131,171-173`) | required by recheck only |
| `quotes` | not read | non-empty list; ids unique+valid; each ≥ 12 normalized chars (`:132-154`) | required by recheck only |
| `fetched_bytes` | **not read** | **not read** | documentation only |
| `lines` | **not read** | **not read** | documentation only |
| `normalized` | **not read** | **not read** | documentation only |
| `archival` | round-32+ no longer exempts (`:167,268-281`) | not read | irrelevant at r36 |

So of the six fields the item names, `url` and `fetched_utc` are gated by the binding check,
`sha256` is gated by source-recheck, and **`fetched_bytes`/`lines`/`normalized` are gated by
nothing** (§5). `id` and `path` — absent from the item's field list — are load-bearing (§4, v0/v1).

### 3. End-to-end matrix (fixture roots, real `SOURCES.md` + one drafted S053 row)

Command shape, repeated per variant: `python3 corpus/instruments/capture-binding-check.py --root
fx/<tag>`; record = the §1 record with the noted mutation; registry cell = bare
`… — https://www.first.org/epss/` unless noted.

| # | variant | mutation | exit | summary | FAIL / UNAVAILABLE lines |
|---|---|---|---|---|---|
| v0 | `as_specified_key_records` | the six item fields under top-level `records` | **2** | — | `UNAVAILABLE reason=manifest-shape …/round-36/manifest.json` |
| v1 | `as_specified_key_sources` | the six item fields (no `id`, no `path`) under `sources` | **1** | `records=1 bound=0 unbound=1` | `FAIL rule=no-row record=<unnamed>`; `FAIL rule=orphan-capture file=S053.txt` |
| v2 | `recommended_full` | `id`+`path` added to the six | **0** | `records=1 bound=1 unbound=0` | — |
| v3 | `url_no_trailing_slash` | `url = https://www.first.org/epss` | 1 | `1/0/1` | `FAIL rule=url-mismatch record=S053` |
| v4 | `registry_markdown_link` | row cell `[EPSS](https://www.first.org/epss/)` | 1 | `1/0/1` | `FAIL rule=url-mismatch record=S053` |
| v5 | `registry_paren_url` | row cell `(https://www.first.org/epss/)` | 1 | `1/0/1` | `FAIL rule=url-mismatch record=S053` |
| v6 | `fetched_plus0000` | `2026-10-26T15:35:06+00:00` | **0** | `1/1/0` | — (gap, §5) |
| v7 | `fetched_naive` | `2026-10-26T15:35:06` | 1 | `1/0/1` | `FAIL rule=fetched-utc … detail=malformed` |
| v8 | `fetched_pending` | `pending` | 1 | `1/0/1` | `FAIL rule=fetched-utc … detail=pending` |
| v9 | `fetched_absent` | `fetched_utc` removed | 1 | `1/0/1` | `FAIL rule=provenance-missing record=S053` |
| v10 | `fetched_impossible` | `2026-02-30T15:35:06Z` | 1 | `1/0/1` | `FAIL rule=fetched-utc … detail=malformed` |
| v11 | `dup_records` | the record twice | 1 | `2/2/0` | `FAIL rule=dup-record field=id value=S053 count=2` + `field=path value=S053.txt count=2` |
| v12 | `orphan_capture` | extra file `S054.txt` | 1 | `1/1/0` | `FAIL rule=orphan-capture file=S054.txt` |
| v13 | `missing_integrity_fields` | only `id/path/url/fetched_utc` | **0** | `1/1/0` | — (blind, §5) |
| v14 | `wrong_sha256_and_lines` | `sha256="0"*64`, `lines=1` | **0** | `1/1/0` | — (blind, §5) |
| v15 | `registry_double_https` | row cell carrying two `https://` tokens | 1 | `1/0/1` | `FAIL rule=double-https-row row=S053 n=2`; `FAIL rule=url-ambiguous … tokens=2` |
| v16 | `registry_status_rejected` | status column = `rejected` | 1 | `1/0/1` | `FAIL rule=rejected-row-anchor record=S053 row=S053` |
| v17 | `url_case_drift` | `https://www.FIRST.org/epss/` | 1 | `1/0/1` | `FAIL rule=url-mismatch` |
| v18 | `url_query_drift` | `https://www.first.org/epss/?x=1` | 1 | `1/0/1` | `FAIL rule=url-mismatch` |

v11 is worth flagging to the integrator: `exit=1` with `records=2 bound=2 unbound=0` — the
`records/bound/unbound` invariant is **not** the verdict; the exit status is (`:104-115`). A duplicate
record raises bound without clearing the failure.

Registry-row forms against the **actual C2 manifest** (same `--root` command):

| row form | exit | summary |
|---|---|---|
| bare `… — https://www.first.org/epss/` | **0** | `records=1 bound=1 unbound=0` |
| bare + comma `…epss/, the documentation page` | **0** | `1/1/0` (trailing `,` stripped) |
| bare + period `…epss/. The documentation page` | **0** | `1/1/0` (trailing `.` stripped) |
| `[EPSS](https://www.first.org/epss/)` | 1 | `FAIL rule=url-mismatch` |
| `(https://www.first.org/epss/)` | 1 | `FAIL rule=url-mismatch` |
| `<https://www.first.org/epss/>` | 1 | `FAIL rule=url-mismatch` |
| `https://www.first.org/epss` (no slash) | 1 | `FAIL rule=url-mismatch` |

`row_tokens` strips only trailing `.,;:` (`:182-185`); a wrapping `)`, `>`, `]` or any host-case,
path or query difference breaks the binding. **The S053 row must carry the URL bare.**

### 4. Landing-order failure modes

| lane state | `capture-binding-check` | consequence |
|---|---|---|
| manifest + capture present, **no S053 row** | `exit 1`, `records=1 bound=0 unbound=1`, `FAIL rule=no-row record=S053` | manifest must not land before the row |
| `S053.txt` present, **no manifest** | `exit 1`, `records=0 bound=0 unbound=0`, `missing_manifest=1`, `FAIL rule=missing-manifest dir=round-36` | capture must not land without the manifest in the same commit |
| manifest present, **capture absent** (row present) | **`exit 0`, `records=1 bound=1 unbound=0`** | binding check is blind; `source-recheck --manifest` on the same fixture prints `S053:source UNAVAILABLE reason=missing`, `exit=2` — both gates must run |

### 5. The three unread fields — measured, not assumed

`grep` over every manifest reader in the lane (`capture-binding-check.py`,
`source-recheck.py`, `frontier-recheck-count.py`, `recheck-audit.py`, `kill-rule-check.py`) finds
no read of `fetched_bytes`, `lines` or `normalized`; `sha256` is read only by `source-recheck.py`
(`:128-159`). Empirically:

- v13 (fields deleted) → `exit 0`; v14 (`sha256="0"*64`, `lines=1`) → `exit 0`.
- v14 with the same wrong `sha256` but handed to source-recheck → `MISMATCH` (that gate does read it).

Values in the actual manifest are nevertheless **internally consistent**, hand-checked:
`sha256` = `hashlib.sha256(S053.txt)`; `lines` 244 = `len(splitlines())`; `fetched_bytes` 26804 =
`len(raw.html)` = `content-length`; `snapshot_bytes` 8448 = file size; `normalized` is a 251-char
prose description (string, not bool) and the capture satisfies every clause of it.

`fetched_bytes` semantics are pinned by the producer, not guessed: `capture-source.py capture()`
prints `fetched_bytes=len(raw)` (served bytes) and `snapshot_bytes=len(data)` (normalized bytes).
The manifest's 26804/8448 pair matches that accounting exactly.

### 6. Strict-`Z` gap

`classify_fetched` (`:162-166,249-266`) accepts `Z` **or** `+00:00`, with optional fractional
seconds. Measured verdicts:

| value | instrument | assignment contract (`strict ISO8601 with Z`) |
|---|---|---|
| `2026-10-26T15:35:06Z` | pass | pass |
| `2026-10-26T15:35:06.123Z` | pass | pass (fractional) |
| `2026-10-26T15:35:06+00:00` | **pass** | **violates** |
| `2026-10-26T15:35:06` | fail (`malformed`) | violates |
| `2026-02-30T15:35:06Z` | fail (`malformed`, calendar check) | violates |

The actual manifest uses `2026-10-26T15:35:10Z` — conforming. But nothing prevents a future record
from using `+00:00` and still passing. A one-line strict-Z predicate
(`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,9})?Z$`) is the hidden rule this round's contract
adds; it is currently enforced only by the author's discipline.

### 7. Quotes — the item's illustrative wording is not verbatim; the landed pin is

Against the normalized capture:

| probe | occurrences | line |
|---|---|---|
| item-spec Q1 wording `EPSS is a data-driven …` | **0** | — |
| verbatim `The Exploit Prediction Scoring System (EPSS) is a data-driven … 30 days.` | 1 | L216 |
| item-spec Q2 wording `0-1 probability` (hyphen) | **0** | — |
| verbatim `EPSS publishes a 0–1 probability (with ranking percentiles)` (U+2013) | 1 | L217 |
| Q3 `every day for every CVE … github repo` | 1 | L217 |
| Q4 `EPSS is maintained by the EPSS Special Interest Group at FIRST. …` | 1 | L235 |

The landed manifest avoids both traps: Q1 is pinned from `(EPSS)` onward (25 words, the pin budget),
Q2 uses the en dash. Recheck confirmation:

```
S053:sha256 OK
S053:Q1 OK occurrences=1 anchor=216-ok
S053:Q2 OK occurrences=1 anchor=217-ok
S053:Q3 OK occurrences=1 anchor=217-ok
S053:Q4 OK occurrences=1 anchor=235-ok        exit=0
```

Q1=25 words, Q2=8, Q3=23, Q4=23 (≤25 each); anchors 216/217/217/235 equal the measured first line
of each quote; Q2 and Q3 sharing L217 is fine (each is unique, so the anchor is confirmatory only —
`source-recheck.py:85-115`).

### 8. Flags for integration (ordered by blast radius)

1. **`sources` key, `id`, `path` are load-bearing and absent from the item's field list.** v0/v1
   show the failure: `exit 2 manifest-shape` or `bound=0 + orphan-capture`. The landed manifest has
   all three, so no action is needed on the C2 side — only on the *schema statement* for future
   rounds.
2. **Registry row form.** S053's source cell must carry `https://www.first.org/epss/` bare, exactly
   one `https` token, status `mined` (not `rejected`). If ScribeRowS053 writes a markdown link, a
   parenthesised URL or a no-slash URL, the whole binding check fails with `url-mismatch` even
   though the manifest is correct.
3. **`fetched_bytes`/`lines`/`normalized` are documentation, not evidence.** If this round wants
   them to be evidence, they need a check (cheapest: a capture-binding rule-D limb asserting
   `sha256 == digest(path)`, `lines == len(path.splitlines())`, `fetched_bytes >= snapshot_bytes`;
   the fixtures v13/v14 are ready-made negative cases). I did not add it — instrument edits belong to
   the C1 suite seat, and this seat is report-only.
4. **Missing-capture is invisible to the binding check** (landing-order row 3). Keep
   `source-recheck --manifest` in the integration gate alongside `capture-binding-check --root`.
5. **Strict-Z** (§6): satisfied by the landed record, unenforced by any gate.
6. `normalized` is a free-form string here and nothing type-checks it; if the schema is to be
   normative, declare string-or-bool rather than leaving it implicit.

### 9. Baseline and non-regression evidence

```
$ python3 corpus/instruments/capture-binding-check.py --root .
MANIFEST round-23 … round-35 (11 manifests)
AUDIT records=42 with_url=42 with_fetched_utc=4 with_archival=38 snapshot_dirs=11
      manifest_dirs=11 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt
records=42 bound=42 unbound=0                                   EXIT=0

$ python3 corpus/instruments/capture-binding-check.py --selftest \
      --scratch /fast/scratch/hyaku/kasegi-r36/ExecManifestChecks
selftest cases=23 failures=0                                    EXIT=0
```

Round 36 adds exactly one manifest dir (`round-36`, 1 record) and one registry row; the expected
post-integration line is `records=43 bound=43 unbound=0` with `multi_row_url` unchanged at 2
(the EPSS URL is currently present in 0 registry cells).

### 10. Retained evidence and cleanup

Every number above came from `validate.out` (sha256 `d8d6b6307fe5fe89047b5349930b7efe6ec72c5e0db393aba3f17ed606dbe0c4`,
harness `validate.py` `45d0e2bac427236adb081da462732f62d5566e0b8032c98f75bfcdfa46d657df`) and
`actual.out` (sha256 `5631f90f0d49fb80c39b7bd2509100f2ca1d921db4e672be1377a3307ceb5b1c`,
harness `validate_actual.py` `d3667db94ad4d06238b4e89fdfefb3ead4368424186a90e28aa709b5a668ad5e`);
both produced at lane HEAD `b47f2cd` with `python3` 3.14.8. All fixture roots, harnesses and outputs
lived only under `/fast/scratch/hyaku/kasegi-r36/ExecManifestChecks/`, which I remove at yield; no
lane file other than this receipt was written; no git/jj mutation, no install, no network, no
subagent. Per the seat rules I ran no build, lint, test or formatter — the counts above are gate
runs, not a verification loop.

Report: .ufo/waves/round-36/wave1/ExecManifestChecks.md
