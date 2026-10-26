# ExecFrontierCapture — S057 capture (C2, F22)

Seat: ExecFrontierCapture (leaf). Item: capture CISA, *When to Issue VEX Information* as the F22 source and write byte-exact
capture + manifest deliverables. Axes: coverage (F22 source), depth:verifiability (digest/line binding, instrument-normalized
bytes, reproducible quote anchors). Scratch: `/fast/scratch/hyaku/kasegi-r39/ExecFrontierCapture/` (removed after copy).
No lane file edited; only the two deliverables and this receipt were written.

## 1. Fetch ledger (network, `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`)

Both fetches started 2026-10-26T19:30:55Z (`date -u`), `curl_rc=0`, `redirects=0` (final URL == requested URL).

| # | URL | status | content-type | bytes | raw sha256 | UTC |
|---|---|---|---|---|---|---|
| 1 | https://www.cisa.gov/resources-tools/resources/when-issue-vex-information | 200 | `text/html; charset=utf-8` | 54453 | `4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d` | 2026-10-26T19:30:55Z |
| 2 | https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf | 200 | `application/pdf` | 235270 | `cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99` | 2026-10-26T19:30:55Z |

Both digests match the round-38 scout fetch ledger (`.ufo/waves/round-38/wave1/ScoutVexLeads.md` rows 4 and 5) byte-for-byte.
PDF response headers: `content-length: 235270`, `last-modified: Mon, 06 Nov 2023 15:43:40 GMT`, `etag: "39706-6097db7d52c78"`;
`file` reports `PDF document, version 1.7, 9 page(s)`. Page response headers: `content-language: en`, `date: Mon, 26 Oct 2026 19:30:55 GMT`.

Raw fetches are scratch-only; only the normalized text is committed, so the deliverables carry no fetched bytes.

## 2. Normalization and byte binding

```
$ python3 .../corpus/instruments/capture-source.py --id S057 --kind pdf \
    --url https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf --out $S/S057.cli.txt
S057 status=200 fetched_bytes=235270 snapshot_bytes=17971 sha256=11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f utc=2026-10-26T19:31:02Z out=.../S057.cli.txt
cli_rc=0
```

The committed capture is produced from **my curl raw bytes** through the same instrument path
(`capture_source.pdf_to_text` imported from the lane instrument) so the delivered bytes bind to digest
`cbcbd77a…0d99`, not to a second independent fetch:

```
raw_bytes=235270 raw_sha256=cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99
snapshot_bytes=17971 snapshot_sha256=11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f lines=275
$ cmp $S/S057.txt $S/S057.cli.txt
cmp: identical
```

Raw-text control (`cmp` demanded by the item): `pdftotext -enc UTF-8 pdf.raw raw-pdftotext.txt` gives 322 lines / 18027 bytes
/ sha256 `e351e922ca22fec9deb0011bc9e49b7cdf58224ba20333e74d67ea936fb3c9d2`; applying the instrument's `collapse()` to it
equals the deliverable byte-for-byte (`collapsed_equals_deliverable=True`). The 275-line count is exactly the collapse delta
(dropped blank lines + trimmed trailing spaces), not lost content: per-page extraction is non-empty on all 9 pages
(2441/2276/2281/1821/2346/1723/2588/1988/563 bytes).

Landing page (metadata only, `html_to_text`): 54453 raw bytes → 3497 snapshot bytes / 135 lines /
sha256 `c868f04a56c4fcc8dcfedc7354b2c65df5e47c8d55caf0f0502005e030360db2`. The page is a publication stub
(its body repeats the introduction at page.txt L82) — the document text lives in the PDF, which is why the PDF is the capture.

Instrument self-check: `capture-source.py --selftest` → `selftest normalize=ok deterministic=ok`, rc=0.

## 3. Quote verification (grep of the committed capture)

```
$ grep -n -i "business decision\|under_investigation\|inherit\|timestamp\|reaffirm\|update" S057.txt
13:and when, to issue VEX information is a business decision for most suppliers and possibly a
80:providing VEX information are primarily business decisions and are not determined by a strict
111:“under_investigation.” Other parties can also issue VEX information. For example, a researcher
133:new vulnerability is disclosed, an “under_investigation” status should be issued. When the
134:investigation has concluded, status should be updated, for example, noting that the product is
136:VEX information includes timestamps to indicate when the information was first issued and most
137:recently updated. By updating a timestamp but not changing status or other information, a VEX
138:issuer can reaffirm that the current status remains accurate at the present time.
181:how to use VEX information. Status inheritance
183:warning, VEX consumers should carefully evaluate if it is valid to inherit status from upstream
```

Occurrence and anchor check (same normalization `source-recheck.py` uses):

```
Q1 occurrences=1 anchor=12 window=12-15 anchor_ok=True len=165
Q2 occurrences=1 anchor=132 window=132-135 anchor_ok=True len=160
Q3 occurrences=1 anchor=136 window=136-139 anchor_ok=True len=270
Q4 occurrences=1 anchor=184 window=184-187 anchor_ok=True len=223
```

| id | committed lines | quote (trimmed) | why it matters |
|---|---|---|---|
| Q1 | L12-L14 | "Whether, and when, to issue VEX information is a business decision for most suppliers and possibly a more individual decision for independent open source developers." | issuance is discretionary, not protocol-mandated (restated L79-L83) |
| Q2 | L132-L134 (L134-L135 continues to `affected`/`not_affected`) | "Ideally, when a new vulnerability is disclosed, an “under_investigation” status should be issued. When the investigation has concluded, status should be updated" | the under_investigation lifecycle |
| Q3 | L136-L138 | "VEX information includes timestamps ... a VEX issuer can reaffirm that the current status remains accurate at the present time." | timestamp-only reaffirmation |
| Q4 | L184-L186 (exception L187-L191) | "Strictly speaking, consumers should not assume the status of an upstream component applies to a product that uses the component. Each component or product throughout a supply chain may require an independent VEX evaluation." | inheritance caution; exception = `component_not_present` / `vulnerable_code_not_present`, void if the code is re-introduced downstream |

## 4. Anchor drift reconciled (blocking for the row/entry, not for this capture)

The spec's estimated anchors (~L19-20, L205-213, L287-294) and the round-38 ledger anchors are **`pdftotext -layout`
line numbers, not committed-capture line numbers**. Measured here: `pdftotext -layout -enc UTF-8` gives 400 lines / 19718
bytes / sha256 `d32b961ce530e97389e08db6e160bd98fa88db91f8620a1604ee50a81d5daa35` — an independent fetch by ScribeEntryF22
produced the identical layout digest, so the drift is mode-only and reproducible, not a capture difference.

Map (layout → collapsed): business decision 19→13 (and 129→80); under_investigation 172→111, 206→133; reaffirm 165→137-138;
inheritance heading 220→181, inherit 222→183, caution 286→184, exception 292/294→188/190.

Consequence for landing: an anchor of `287` against the 275-line committed capture is `anchor=OUT-OF-RANGE` and fails
`source-recheck.py`. The S057 registry row / knowledge entry MUST cite committed-capture numbers (L12-L14, L131-L138,
L179-L191) or label layout numbers explicitly. Recomputed values were sent to ScribeEntryF22 (`agent://ScribeEntryF22`).

Also a binding constraint for the row author: `capture-binding-check.py` B4/B5 require the row's source cell to carry
**exactly one** `https://` token and the manifest `url` to equal it byte-for-byte. The planned row's https token is the page
URL, so the PDF may appear in the row only as a filename (`When-to-Issue-a-VEX-508c.pdf`), never as a second URL; the manifest
therefore keeps `url` = page URL and puts the PDF URL in `capture_url` / `http.final_url`.

## 5. Manifest validation against the lane instruments (scratch fixture, no lane edit)

Fixture root `$S/bindroot/corpus/` with the deliverable manifest + capture staged as `source-snapshots/round-39/{manifest.json,S057.txt}`
and a header-plus-one-row `SOURCES.md` mirroring the planned mined S057 row:

```
$ python3 .../corpus/instruments/capture-binding-check.py --root "$F"
MANIFEST round-39 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=1 bound=1 unbound=0
binding_rc=0

$ python3 .../corpus/instruments/source-recheck.py --manifest "$F/corpus/source-snapshots/round-39/manifest.json" --source S057
S057:sha256 OK
S057:Q1 OK normalized=markup-whitespace occurrences=1 anchor=12-ok
S057:Q2 OK normalized=markup-whitespace occurrences=1 anchor=132-ok
S057:Q3 OK normalized=markup-whitespace occurrences=1 anchor=136-ok
S057:Q4 OK normalized=markup-whitespace occurrences=1 anchor=184-ok
recheck_rc=0
```

Manifest shape: `schema_version: 1` (int), `sources[0]` = `{id S057, path S057.txt, url <page>, capture_url <pdf>,
fetched_utc 2026-10-26T19:30:55Z, fetched_bytes 235270, snapshot_bytes 17971, lines 275, sha256, snapshot_sha256,
raw_sha256, raw_bytes, tool, normalized, http{status,content_type,final_url,redirects,user_agent,fetched_utc,date,last_modified,content_length,etag},
landing_page{url,role,status,content_type,fetched_utc,redirects,raw_bytes,raw_sha256,snapshot_bytes,snapshot_sha256,lines,tool},
quotes[Q1..Q4 with anchor + location]}`. `path` stem == id (source-recheck B1); `fetched_utc` is strict-UTC (binding rule C,
round-39 ≥ 32 so no archival exemption).

## 6. Deliverables (byte-exact, in this directory)

| file | lines | bytes | sha256 |
|---|---|---|---|
| `ExecFrontierCapture.S057.txt` | 275 | 17971 | `11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f` |
| `ExecFrontierCapture.manifest.json` | 74 | 5488 | `432f2205b368acb39d620bb85fe81c0fd6ccb345dd0878661478085ac1ce6659` |

`cmp $S/S057.txt wave1/ExecFrontierCapture.S057.txt` → identical. L1 lands them as
`corpus/source-snapshots/round-39/S057.txt` and `corpus/source-snapshots/round-39/manifest.json` unchanged
(the manifest's `path` is `S057.txt`, matching the landed file name).

## 7. State, tooling, risks

- Lane tree: only `.ufo/waves/round-39/wave1/` is mine in the untracked set; no tracked file touched, no git mutation.
- Disk guard green before the pass (`use%` 3/35/24, rc=0). No tool installed or upgraded.
- Scratch `/fast/scratch/hyaku/kasegi-r39/ExecFrontierCapture/` removed; no kasegi-r39 residue from this seat.
- Risk (handled above): row/entry landing on layout line numbers would produce an out-of-range anchor — report-only fix is the
  collapsed map in §4; ScribeEntryF22 was told before landing.
- No half-open work: capture, manifest, digest binding, quote anchors and both instrument validations are complete.
