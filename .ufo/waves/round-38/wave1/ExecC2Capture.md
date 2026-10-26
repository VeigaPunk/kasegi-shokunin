# ExecC2Capture — S055 primary-source capture (round 38)

Seat: ExecC2Capture (leaf executor; no subagent dispatch, no labrat probe used).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` — the only repo I wrote into (this receipt and the two
deliverable files under `.ufo/waves/round-38/wave1/`).
Base commit `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`; claims-freeze commit `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`;
lane HEAD observed while working: `700153593eb586c70a6499c8ca225ee4d673bc9b` (`git status --porcelain` showed only
`?? .ufo/waves/round-38/wave1.ready`, `?? .ufo/waves/round-38/wave1.ready.partial`, `?? .ufo/waves/round-38/wave1/`).
Claim served: C2 coverage, frontier F21 (OASIS CSAF v2.0 — Common Security Advisory Framework; the VEX profile's
`product_status` categories and the machine-readable not-affected justification flags), capture leg only.

Deliverables (the L1 lands these byte-identically; nothing else in them):

| wave-dir file (written) | lands at (lane relative) | lines | bytes | sha256 |
|---|---|---|---|---|
| `ExecC2Capture.S055.txt` | `corpus/source-snapshots/round-38/S055.txt` | 5146 | 272441 | `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42` |
| `ExecC2Capture.manifest.json` | `corpus/source-snapshots/round-38/manifest.json` | 57 | 3841 | `95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f` |

Both wave-dir copies were re-verified against their scratch originals with `cmp -s` (identical).

## 1. Raw fetch metadata (S055 primary capture)

| field | value |
|---|---|
| request URL | `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` |
| curl argv | `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -D headers.txt -o raw.html -w '...' <url>` |
| HTTP status | 200 |
| effective URL | `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` |
| redirect count | 0 (requested == effective) |
| content-type | `text/html` (no charset parameter served) |
| served bytes | 414858 (`size_download=414858`; the response carried **no** `content-length` header) |
| server | `cloudflare` (`via: 1.1 a27ad8496269675a75f4ce79d5a1c352.cloudfront.net (CloudFront)`) |
| Date header | `Mon, 26 Oct 2026 18:25:51 GMT` |
| Last-Modified | `Sun, 05 Apr 2026 13:17:09 GMT` |
| canonical link | `<https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html>; rel="canonical"` (same URL) |
| cache | `x-cache: Hit from cloudfront`, `cf-cache-status: HIT`, `age: 769`, `cache-control: public, max-age=31536000, immutable` |
| fetched_utc | `2026-10-26T18:25:51Z` (UTC clock read immediately after the transfer; identical to the served Date second) |
| time_total | 0.061515 s |
| raw body sha256 | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |
| stability re-fetch | second full GET at `2026-10-26T18:29:36Z`: HTTP 200, no redirect, `size_download=414858`, same Last-Modified, `age: 994`, raw sha256 `fad0c60d…cd66b` — **identical bytes** |

Raw response headers as served (complete set; CRLF→LF for rendering, status line included):

```text
HTTP/2 200 
date: Mon, 26 Oct 2026 18:25:51 GMT
content-type: text/html
last-modified: Sun, 05 Apr 2026 13:17:09 GMT
server: cloudflare
x-amz-server-side-encryption: AES256
cache-control: public, max-age=31536000, immutable
x-amz-version-id: null
report-to: {"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=4qCXAtdEd9lvhSaB3%2BfdGVOYVjw656%2F172E5MCw3rnSxYyVs1OM7buZYabFmBEwzHqQK6ZLA9agl%2B9F%2Fx4MVKF%2FRy6b%2FyEibLAJreSXmFNjbPgqJqCIg%2FQoVztHtHan6mtFoUt2BTgWwlQB7kgjqiXdl"}]}
speculation-rules: "/cdn-cgi/speculation"
vary: Accept-Encoding
via: 1.1 a27ad8496269675a75f4ce79d5a1c352.cloudfront.net (CloudFront)
alt-svc: h3=":443"; ma=86400
age: 769
link: <https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html>; rel="canonical"
x-cache: Hit from cloudfront
x-amz-cf-pop: MIA50-P3
x-amz-cf-id: oqX9UbYiAfiyWm1SkOEZpC1rxg65nG7tIsEm_SG85GcE3fwbAc5VPw==
cf-cache-status: HIT
nel: {"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}
strict-transport-security: max-age=2592000
x-content-type-options: nosniff
cf-ray: a50b8189cfaae6c8-GIG
```

## 2. Normalization (lane instrument, read-only import)

- Instrument: `corpus/instruments/capture-source.py`, sha256
  `e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18` (read from the lane working tree; not modified).
- Function: `html_to_text(raw.decode("utf-8", "replace"))`, imported with
  `importlib.util.spec_from_file_location`; the module was never run as `__main__` and the instrument wrote no file.
- Behaviour as the instrument implements it: `<script>`/`<style>` removed; `</p|div|li|tr|h1-h6|section|article|br>`
  and `<br/>` to newlines; remaining tags stripped; `html.unescape()`; runs of space/tab/NBSP collapsed; blank lines
  dropped; UTF-8; one final newline.
- Output: 272441 bytes, 5146 lines, sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`;
  LF only (0 CR), ends with exactly one `\n`, 102 non-ASCII bytes (curly quotes/dashes in the document's front matter
  and body). Determinism checked by converting the same raw body twice: identical sha256.
- The 414858-byte raw HTML is **not** landed — the lane convention commits the normalized snapshot, so the raw body
  stays scratch-only with its sha256 recorded in §1.

## 3. Quote pins Q1–Q4

Chosen under ExecC2QuoteOnce's rule: ≤25 words, exactly one occurrence in the normalized text, declared anchor line.
Each anchor was verified through `source-recheck.py`'s own window rule (anchor line + 3 following lines).

| id | line(s) | words | occurrences (normalized) | literal substring | anchor verdict | quote |
|---|---|---|---|---|---|---|
| Q1 | L2135 | 24 | 1 | yes | `anchor=2135-ok` | The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability. |
| Q2 | L2844 | 25 | 1 | yes | `anchor=2844-ok` | For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status. |
| Q3 | L2151–L2152 | 23 | 1 | no (line wrap) | `anchor=2151-ok` | For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats. |
| Q4 | L1767 | 19 | 1 | yes | `anchor=1767-ok` | vulnerable_code_not_in_execute_path: The affected code is not reachable through the execution of the code, including non-anticipated states of the product. |

Location notes (as carried in each manifest `location`):

- **Q1 — VEX purpose.** L2135, second sentence of §4.5 "Profile 5: VEX" (heading L2134); the first sentence on the
  same line only names the format and points at `[VEX]`.
- **Q2 — `product_status` categories for VEX.** L2844, body of mandatory test §6.1.27.7 "VEX Product Status"
  (heading L2843): the four categories `fixed`, `known_affected`, `known_not_affected`, `under_investigation`, of
  which at least one must be present. 25 words — at the rule's limit, not over it.
- **Q3 — impact statement for `known_not_affected`.** L2151–L2152, required-element bullet of §4.5. The sentence
  is split across two normalized lines (L2151 is exactly `For each item in`), so the literal substring is absent
  while the whitespace-normalized occurrence is 1; `source-recheck.py` therefore reports
  `normalized=markup-whitespace occurrences=1` for this pin rather than a bare `occurrences=1`. Nothing is hidden:
  the four-line anchor window at L2151 contains the whole requirement, and `anchor=2151-ok` is reported.
- **Q4 — one flags label.** L1767, §3.2.3.5 "Vulnerabilities Property - Flags" (heading L1729), definition of
  `vulnerable_code_not_in_execute_path` in the VEX justification-code enum. The bare label also occurs at L1756 in
  the enum list; the pinned string with its definition occurs once.

## 4. Recheck (scratch copy of the lane instrument) — exit 0

`python3 source-recheck.py --manifest manifest.json --source S055` (binary copied from
`corpus/instruments/source-recheck.py`, sha256 `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`):

```text
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
exit=0
```

## 5. Binding check on a simulated registry row — exit 0

To prove the manifest's `url` binds under rule B5 (byte-exact against the registry's single `https://` token), a
scratch root was built from a copy of `corpus/SOURCES.md` with one appended S055 row (11 columns, one `https://`
token = the manifest URL) plus `corpus/source-snapshots/round-38/{S055.txt,manifest.json}`, then:

`python3 capture-binding-check.py --root "$S/bindroot"` (instrument sha256
`3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`):

```text
MANIFEST round-38 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=1 with_url=1 with_fetched_utc=1 with_archival=0 snapshot_dirs=1 manifest_dirs=1 missing_manifest=0 multi_row_url=0 orphans=0
records=1 bound=1 unbound=0
exit=0
```

The simulation exists only to prove the binding; the real registry row is ScribeRowS055's write.

## 6. manifest.json — byte-exact deliverable

57 lines, 3841 bytes, sha256 `95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f`
(written with `json.dumps(..., indent=1, ensure_ascii=False)` + trailing newline, the round-37 shape). Schema is
round-37's: `schema_version`, `purpose`, `sources[]` with `id`/`path`/`url`/`fetched_utc`/`fetched_bytes`/
`snapshot_bytes`/`lines`/`sha256`/`normalized`/`raw_sha256`/`http{}`/`quotes[]`. `http.content_length` is `null`
because the response carried no such header (the served byte count is `fetched_bytes` = 414858 from
`size_download`); no instrument reads that field.

```json
{
 "schema_version": 1,
 "purpose": "Round-38 F21 captured-source assertions for S055 (OASIS CSAF v2.0 - Common Security Advisory Framework, OASIS Standard dated 18 November 2022; the VEX profile's product_status categories and the machine-readable not-affected justification flags). Fetched 2026-10-26T18:25:51Z with curl -sS -L --max-time 90 under the instrument UA kasegi-shokunin/1.0: HTTP status=200, content-type=text/html, no redirect (requested URL == final URL), fetched_bytes=414858, snapshot_bytes=272441, 5146 lines, sha256 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42, raw_sha256 fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b. The normalized capture is the OASIS Standard HTML converted by corpus/instruments/capture-source.py html_to_text(); the four quotes are VEX purpose, the four VEX product_status categories, the known_not_affected impact-statement rule, and the vulnerable_code_not_in_execute_path flag definition.",
 "sources": [
  {
   "id": "S055",
   "path": "S055.txt",
   "url": "https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html",
   "fetched_utc": "2026-10-26T18:25:51Z",
   "fetched_bytes": 414858,
   "snapshot_bytes": 272441,
   "lines": 5146,
   "sha256": "63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42",
   "normalized": "capture-source.py html_to_text(): <script>/<style> removed, block tags (p div li tr h1-h6 section article br) to newlines, remaining tags stripped, html.unescape() applied, runs of space/tab/NBSP collapsed and blank lines dropped; UTF-8; final newline",
   "raw_sha256": "fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b",
   "http": {
    "status": 200,
    "content_type": "text/html",
    "final_url": "https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html",
    "redirects": 0,
    "user_agent": "kasegi-shokunin/1.0",
    "fetched_utc": "2026-10-26T18:25:51Z",
    "date": "Mon, 26 Oct 2026 18:25:51 GMT",
    "last_modified": "Sun, 05 Apr 2026 13:17:09 GMT",
    "content_length": null,
    "cache_age_seconds": 769,
    "server": "cloudflare"
   },
   "quotes": [
    {
     "id": "Q1",
     "quote": "The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability.",
     "anchor": 2135,
     "location": "L2135; second sentence of '4.5 Profile 5: VEX' (heading L2134), the profile's own statement of purpose."
    },
    {
     "id": "Q2",
     "quote": "For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status.",
     "anchor": 2844,
     "location": "L2844; body of mandatory test '6.1.27.7 VEX Product Status' (heading L2843), naming the four product_status categories a VEX document must use."
    },
    {
     "id": "Q3",
     "quote": "For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats.",
     "anchor": 2151,
     "location": "L2151-L2152; required-element bullet in '4.5 Profile 5: VEX'. The sentence is split across two normalized lines ('For each item in' ends L2151), so it matches the capture after whitespace normalization; anchor L2151 opens the four-line window that holds it."
    },
    {
     "id": "Q4",
     "quote": "vulnerable_code_not_in_execute_path: The affected code is not reachable through the execution of the code, including non-anticipated states of the product.",
     "anchor": 1767,
     "location": "L1767; '3.2.3.5 Vulnerabilities Property - Flags' (heading L1729), definition of the VEX justification code vulnerable_code_not_in_execute_path in the flag label enum."
    }
   ]
  }
 ]
}
```

## 7. Landing instructions for the L1

1. Write `ExecC2Capture.S055.txt` byte-for-byte to `corpus/source-snapshots/round-38/S055.txt` (272441 bytes,
   5146 lines, sha256 `63c8ad52…cd42`).
2. Write `ExecC2Capture.manifest.json` byte-for-byte to `corpus/source-snapshots/round-38/manifest.json`
   (3841 bytes, 57 lines, sha256 `95b3f46d…a9f`).
3. S055's registry source cell must carry exactly one `https://` token and it must be, byte-for-byte,
   `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` — the manifest `url`; a second `https://`
   token in the cell fails B4, and any other URL fails B5.
4. With those three in place, `python3 corpus/instruments/source-recheck.py --manifest
   corpus/source-snapshots/round-38/manifest.json --source S055` exits 0; that is also the entry's `recheck:` line.

## 8. Risks and limits

- **No `content-length`.** The HTTP/2 response carried none; the manifest records `null` rather than inventing a
  value, and `fetched_bytes` holds curl's `size_download` (414858).
- **Cache-served bytes.** `age: 769` with `cache-control: immutable` means the representation was assembled ~13 min
  before my request. The second GET four minutes later returned identical bytes, which shows the served
  representation was stable across two instants, not that OASIS will serve the same bytes later.
- **Front-matter date vs `Last-Modified`.** The document says "OASIS Standard, 18 November 2022"; the CDN's
  `Last-Modified` is 2026-04-05 (file mtime, not a revision claim). The capture supports the first date as the
  standard's date and makes no recency claim beyond `fetched_utc`. I did not investigate whether a v2.1 exists —
  that is ExecCsafStatus's item, not mine.
- **Q3 normalization.** Stated in §3: the impact-statement sentence is split by a line break, so the pin is a
  normalized match (`normalized=markup-whitespace`) with a verified anchor, not a literal substring.
- **Whole page, not an excerpt.** The snapshot includes the document's table of contents, references and OASIS
  boilerplate as served; that is what the capture instrument produces and what `source-recheck.py` hashes.
- **Binding was proven on a simulated row.** The real row's wording is another seat's deliverable; if it carries a
  second URL token, binding fails by design. The row's scope must also avoid claiming a recency the capture cannot
  support.

## 9. Tooling and scratch

- No tools installed or upgraded; no pacman invocation (transactions paused host-wide). Host `curl` 8.23.0 and
  `python3` 3.14.8 sufficed — nothing to record under the 2026-10-19 tooling authorization.
- Scratch root `/fast/scratch/hyaku/kasegi-r38/ExecC2Capture/` held the raw bodies (two fetches), headers, the
  normalizer run, the manifest build, the recheck and binding instruments and the fixture root; the directory was
  removed after the receipt and deliverables were copied into the wave dir.
- No file in the lane repo outside `.ufo/waves/round-38/wave1/ExecC2Capture.*` and this receipt was written; the
  fleet root, sibling lanes, shokuknow and source trees were not touched; no mutating git/jj command was run.
