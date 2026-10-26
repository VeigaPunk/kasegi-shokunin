# ScoutCaptureAvailability — S054 capture availability receipt (round 37, C2)

Verdict: the S054 capture plan is executable. `https://certcc.github.io/SSVC/` answers HTTP 200 with no redirect under the instrument UA, and it is the canonical docs host, not a redirect trap.

Probed 2026-10-26T17:12:24Z (HEAD/GET, `curl -sS`, 60 s timeout). Lane HEAD at probe time: `b362068195d5489aa94b31e6ec8f880c367e0ba0`. Nothing in the lane repo was written. The scratch dir `/fast/scratch/hyaku/kasegi-r37/ScoutCaptureAvailability/` was removed on exit.

## Facts observed

| Check | Result |
|---|---|
| Instrument UA (`corpus/instruments/capture-source.py` line 32) | `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` |
| HEAD, no-follow, instrument UA | `HTTP/2 200`, `server: GitHub.com` (GitHub Pages behind Fastly/varnish) |
| GET, no-follow, instrument UA | `http_code=200 num_redirects=0 url_effective=https://certcc.github.io/SSVC/` |
| content-type | `text/html; charset=utf-8` |
| size | `content-length: 105807` bytes; `size_download=105807` |
| body sha256 | `60c00968563c688e4ffafb7a5b9fcedf097db8459114b92185c37cd4482112ed` |
| `curl -L` result | byte-identical to the no-follow body (same sha256), 0 redirects, so the requested URL is the final URL |
| Python `urllib` with the instrument script's `fetch()` request shape | status 200, `geturl()` == requested URL, 105807 bytes, same sha256 |
| Default curl UA (no UA override) | also 200, 105807 bytes, so there is no UA-based gating or block |
| Cache headers | `last-modified: Fri, 23 Oct 2026 16:21:47 GMT`, `etag: "6adb899b-19d4f"`, `cache-control: max-age=600`, `access-control-allow-origin: *` |
| Block evidence | No 403/429/captcha/challenge response. A grep for `captcha`, `access denied`, `403 forbidden`, `just a moment` returned 0 hits. The one `cloudflare` hit is a `<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js">` asset tag, which is benign. |
| robots | `certcc.github.io/robots.txt` and `/SSVC/robots.txt` both return 404, so there is no robots file and no crawl restriction. `/SSVC/sitemap.xml` returns 200, `application/xml`, 24202 bytes. |
| Timing | Total fetch time about 0.08 s. The raw fetch is far under the instrument's `MAX_FETCH_BYTES` (32 MiB) and 60 s timeout. |

## Canonical-host / redirect-trap check

- The page's own `<link rel="canonical" href="https://certcc.github.io/SSVC/">` equals the requested URL exactly.
- The `<title>` is `SSVC: Stakeholder-Specific Vulnerability Categorization`. The meta description is "SSVC is a framework for prioritizing vulnerabilities based on stakeholder needs."
- The page links to the upstream repo `https://github.com/CERTCC/SSVC` (plus Discussions and Q&A). The footer text reads "Carnegie Mellon University", with the CERT®/Carnegie Mellon®/CERT Coordination Center® registered-mark notice.
- The TLS cert is a GitHub wildcard (`CN=*.github.io`, SAN includes `github.io`), issued by Let's Encrypt, valid 2026-09-30 to 2026-12-29.
- DNS resolves to GitHub Pages anycast addresses (`2606:50c0:800{0..3}::153`).
- Variants:
  - `https://certcc.github.io/SSVC` (no trailing slash) returns 301 to `https://certcc.github.io/SSVC/`.
  - `http://certcc.github.io/SSVC/` returns 301 to the same https URL.
  - The trailing-slash https URL, the one in the frozen claim, is the terminal canonical URL. Use it as `url` in the manifest.
- No `<meta http-equiv="refresh">` and no JS-only shell. The body is server-rendered HTML.

## Dry normalization (nothing written to the lane)

I ran the lane's `capture-source.py` `html_to_text()` on the fetched body in scratch:

- The page normalizes to snapshot_bytes=7730, 286 lines, sha256 `a66133152a5bb8b760e6aef1c316b46777abc5dda2c1d957410ceccbce58bb56`, as seen at 17:12Z.
- The page cites the name and defines the method:
  - L1/L3/L16: `SSVC: Stakeholder-Specific Vulnerability Categorization`.
  - L203: `SSVC stands for A Stakeholder-Specific Vulnerability Categorization.`
  - L204: `It is a methodology for prioritizing vulnerabilities based on the needs of the stakeholders involved in the vulnerability management process.`
  - L273: `Carnegie Mellon University`.
- These are line numbers in my normalized scratch text only. The executor's real capture decides the anchors.
- The page is served from GitHub Pages with `max-age=600`. The ETag and last-modified are from the Fri 23 Oct deploy. The snapshot sha256 will change if the site redeploys, so the manifest must bind the executor's own captured bytes, not the digests above.

## Remaining unknowns / cautions

- The numbers above are a single probe. The executor's capture should record its own `fetched_utc`, `fetched_bytes` and `sha256` in `manifest.json` (S053's manifest shape, `http.user_agent` field included).
- Do not copy the 105807 or 7730 byte counts from this receipt as binding values.
- The Pages deployment can change before or after capture. The content quote the knowledge entry uses must be a substring of the executor's committed `S054.txt`.

Confidence: high on 200 / content-type / no redirect / UA accepted / canonical host. Medium on any specific line anchor, because the deploy can change.
