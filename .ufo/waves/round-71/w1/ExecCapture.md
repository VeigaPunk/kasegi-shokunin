# ExecCapture — round-71 wave w1 — independent S106 capture verification

Seat: `ExecCapture-4` (executor, leaf). Lane: `kasegi-shokunin`.
Base rev: `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60` (= lane `HEAD` at run time,
confirmed `git rev-parse HEAD`). Frozen claims commit read first:
`0e260a54b0a670cee2915237ac403d37164c749d` → `.ufo/waves/round-71/claims.json`,
`.ufo/waves/round-71/controls/pins-r71.txt`.

Method: committed bytes materialized with
`git -C <lane> archive 4e33119e corpus | tar -x -C /fast/scratch/hyaku/kasegi-r71/ExecCapture-4/rev`
(no checkout, no mutating git anywhere). Scratch tree
`/fast/scratch/hyaku/kasegi-r71/ExecCapture-4` removed after this report was written.
No lane production file was touched; this report is the only write.
No tool installs were needed (python3, git, curl, tar already present).

## 0. Pinned digests re-verified against committed bytes

```
$ sha256sum rev/corpus/instruments/figure-audit.py rev/corpus/source-snapshots/round-71/S106.txt
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603  figure-audit.py   (matches goal pin)
291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db  S106.txt         (matches goal pin + manifest)
$ wc -l -c rev/corpus/source-snapshots/round-71/S106.txt
  148 15004                                                                     (matches manifest lines/bytes)
```

pins-r71.txt control hashes read (not re-run — other seats own the counters):
`c1-probe-run-r71.py 80020705…`, `c1-donothing-r71.txt eb24dd87…`,
`c1-base-r71.txt f553ddb4…`, `c2-base-counters-r71.txt 4adae3b6…`, `claims.json c530ec65…`.

## 1. Independent re-fetch digest comparison — VERIFIED, byte-identical

Ran the lane instrument from the extracted rev tree (cwd `…/ExecCapture-4/rev`):

```
$ TMPDIR=/fast/scratch/hyaku/kasegi-r71/ExecCapture-4 \
  python3 corpus/instruments/capture-source.py --id S106 \
  --url https://www.zerodayinitiative.com/about/ \
  --out /fast/scratch/hyaku/kasegi-r71/ExecCapture-4/S106-again.txt --kind html
S106 status=200 fetched_bytes=54328 snapshot_bytes=15004 \
  sha256=291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db \
  utc=2026-11-05T01:30:56Z out=…/S106-again.txt
exit=0
$ sha256sum S106-again.txt
291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db  S106-again.txt
$ wc -l -c S106-again.txt
  148 15004
```

Verdict: the live page re-fetch at 2026-11-05T01:30:56Z produced a snapshot
**byte-identical** to the committed `S106.txt`
(`291f36c2…59db`, 148 lines / 15004 bytes). No drift, no diff to explain —
the round-67 S100 nonce class did not fire here: the raw HTML carries a
per-response CSP nonce (`Content-Security-Policy-Report-Only: … 'nonce-5oR42RyjHf8DvOPT'`)
but nonces live in `<script>`/headers which `capture-source.py` strips before
hashing; two fetches ~4 min apart (manifest `fetched_utc` 01:27:03Z vs mine
01:30:56Z) yielded the same 54328-byte body and the same snapshot digest.

Supplementary raw fetch (same UA, curl, headers dumped): HTTP 200,
`Content-Length: 54328` — identical body size to the instrument's fetch.
Response headers: `Date: Thu, 05 Nov 2026 01:32:02 GMT`, `Server: Apache`,
`Cache-Control: no-store`, **no `Last-Modified`**.

## 2. Manifest quote audit — 15 quotes located in committed capture

Method: substring count of each manifest `quote` over the whole capture text,
plus line-level hits; `on_anchor` = quote present on manifest `anchor` line
(1-based). Script run over `rev/corpus/source-snapshots/round-71/{S106.txt,manifest.json}`.

| id            | anchor | count | line_hits     | on_anchor | verdict |
|---------------|-------:|------:|---------------|:---------:|---------|
| Q01-scope     |     28 |     2 | [28, 102]     |    yes    | **NOT exactly-once** |
| Q02-acquisition |   31 |     1 | [31]          |    yes    | ok |
| Q03-guarantee |     47 |     1 | [47]          |    yes    | ok |
| Q04-validation|     49 |     1 | [49]          |    yes    | ok |
| Q05-window    |     70 |     1 | [70]          |    yes    | ok |
| Q06-shortened |     70 |     1 | [70]          |    yes    | ok |
| Q07-escalation|     70 |     1 | [70]          |    yes    | ok |
| Q08-limited   |     52 |     1 | [52]          |    yes    | ok |
| Q09-full      |     51 |     1 | [51]          |    yes    | ok |
| Q10-offer     |     60 |     1 | [60]          |    yes    | ok |
| Q11-nobacklog |     62 |     1 | [62]          |    yes    | ok |
| Q12-credit    |     61 |     1 | [61]          |    yes    | ok |
| Q13-dossier   |     69 |     1 | [69]          |    yes    | ok |
| Q14-refusal   |     72 |     1 | [72]          |    yes    | ok |
| Q15-nolimit   |     60 |     1 | [60]          |    yes    | ok |

Deviation found — **Q01-scope is not exactly-once**:
quote `the world's largest vendor-agnostic vulnerability disclosure program`
occurs twice in the capture:
- line 28 (the anchor): `…ZDI) is the world's largest vendor-agnostic vulnerability disclosure program. Built on…`
- line 102 (researcher CTA): `Earn rewards and contribute to the world's largest vendor-agnostic vulnerability disclosure program.`

It does occur on its anchored line (28), so anchor placement is correct; only
the uniqueness property fails. All other 14 quotes occur exactly once, each on
its anchored line. Anchors 60/61/62/70 each correctly host their quotes
(Q10+Q15 share anchor 60; Q05+Q06+Q07 share anchor 70 — all verified on-line).

## 3. Page date / version signals — none stated

The page states **no publication or revision date**. Evidence:

- Capture line 127: `©2026 TrendAI™ Zero Day Initiative™ (ZDI).` — copyright
  year only (footer, raw HTML line 583 inside `<p class="copyright …">`).
- Body-year references are content, not page dates: line 29 `established in
  2005`; line 34 `…in 2024 than all other participating programs combined`;
  line 95 `since 2007`; line 97 `…in 2024`; line 99 `since 2007`.
- Raw HTML head carries only `<meta charset="UTF-8">` and
  `<meta name="viewport" …>`; no `article:published_time`, `datePublished`,
  `dateModified`, `og:*`, JSON-LD, or `<time datetime>` anywhere (grep over the
  54328-byte body). No `Last-Modified` response header.
- `fetched_utc` 2026-11-05T01:27:03Z in manifest.json is capture provenance,
  not a page-stated date.

## 4. capture-binding-check.py on committed corpus — expected FAIL reproduced

```
$ cd rev && python3 corpus/instruments/capture-binding-check.py
MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4
… (round-24 … round-70 lines omitted here; all url_bound=records, exit-clean)
MANIFEST round-70 records=1 url_bound=1 fetched=1 archival=0
MANIFEST round-71 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=85 with_url=85 with_fetched_utc=47 with_archival=38 snapshot_dirs=44 manifest_dirs=44 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S106 dir=round-71
records=85 bound=84 unbound=1
exit=1
```

The one expected FAIL is present: `FAIL rule=no-row record=S106 dir=round-71`
— the round-71 manifest record exists but no `| S106 |` registry row is
committed at base rev `4e33119e` yet (`url_bound=0`, `unbound=1`). Round-71
itself contributes no orphan (`S106.txt` is manifest-declared); the single
`orphans=1 orphan=S040-live.txt` is pre-existing from an earlier round.
`records=85` already counts S106's manifest record; `bound=84` awaits the
registry row.

## 5. Scope / hygiene

- Files changed by this seat: this report only
  (`.ufo/waves/round-71/w1/ExecCapture.md`). No production file written.
- No git/jj mutation run anywhere; all committed bytes read via
  `git show`/`git archive`.
- Scratch `/fast/scratch/hyaku/kasegi-r71/ExecCapture-4` (rev tree,
  S106-again.txt, S106-raw.html, S106-headers.txt) removed before yield.
- Verification performed: digest re-fetch (live network), quote census,
  date-signal scan of capture + raw HTML + response headers, binding check.
  Nothing skipped; no claim left unrun.
