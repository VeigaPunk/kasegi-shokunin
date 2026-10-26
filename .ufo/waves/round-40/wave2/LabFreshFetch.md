# LabFreshFetch receipt (kasegi round 40, falsify wave 2)

Seat: fetch-stability probe. Verification ref: lane HEAD 3074c76 (J5). Committed captures read via `git show HEAD:corpus/source-snapshots/round-40/<id>.txt`; the recheck instrument was run on a `git archive` copy in scratch.

## What I attacked
The claim that the committed round-40 captures (S016, S025 = mined sources; S060 = S060+ new row) are bound to bytes a stranger re-fetching from the live host gets, independent of User-Agent and of fetch time. Items: manifest records `raw_sha256` / `sha256` / `snapshot_sha256` / `full_text_sha256` / `fetched_bytes`, `quotes[]`, and the SOURCES.md S060 row. I picked S025 and S016 (both mined) and S060 (the S060+ source), plus the S025 landing page.

## Method (commands re-run)
- `curl -sS -L --max-time 90 -A <UA> -D hdr -o body` for 4 URLs x 6 UAs in parallel at 2026-10-26T22:07:03Z, about 51 min after the committed fetch (21:15:52Z to 21:16:18Z). A second round at 22:08:16Z used a Safari UA for S016/S025, and the committed UA twice for S060.
- UAs: ua1 `kasegi-shokunin/1.0`; ua2 Firefox 128 on Linux; ua3 `curl/8.9.1`; ua4 `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` (the string hard-coded in capture-source.py); ua5 `Python-urllib/3.12`; ua6 `LabFreshFetch-probe/2.0 (+hyaku r40 falsify)`; r2 Safari/macOS.
- URLs: S025 `https://arxiv.org/pdf/2503.17332` and `.../2503.17332v4`; S016 `https://www.anthropic.com/coordinated-vulnerability-disclosure`; S060 `https://cyclonedx.org/docs/1.7/json/`; S025 landing page `https://arxiv.org/abs/2503.17332`.
- Each body was normalised with the committed instrument (`corpus/instruments/capture-source.py` `html_to_text` / `pdf_to_text`, imported unchanged, pdftotext 26.08.0). For S060 I applied the manifest's declared slice (line 1 + lines 16060-16169 of the page text). I then compared the result with the committed bytes.
- `source-recheck.py --manifest corpus/source-snapshots/round-40/manifest.json --source {S016,S025,S060}` was run on the archive copy.
- Full transcript, with hashes, headers and normalisation results: `LabFreshFetch.transcript.txt` (beside this receipt, 100 lines).

## Results

### S025 (arXiv PDF): STABLE. Reproduced.
- All 6 UAs, both URL forms (`/pdf/2503.17332` and `/v4`), and the second-round Safari UA returned HTTP 200, 602933 bytes, 0 redirects, raw sha256 `334417c3...6cb1`. That equals the manifest `raw_sha256`.
- Normalised text: 71851 bytes, sha256 `faa1c1f8...f9b7b`, identical to the committed capture in every case.
- Headers: `last-modified: Wed, 25 Jun 2025 00:25:34 GMT`, etag `CKWc+92ni44DEAI=`, `age: 33535`. The content is a fixed, cache-served v4 PDF.
- The abs landing page returned 200, 44575 bytes, sha256 `28675fd2...d627`, equal to the manifest `landing_page.raw_sha256`.
- Recheck: sha256 OK; Q1 and Q2 OK with `normalized=markup-whitespace`, `occurrences=1`, anchors 32 and 507.
- Observation, not a defect: Q1 and Q2 do not occur verbatim on one line. The PDF wraps them across lines (Q1 L31-L34, Q2 L506-L510). They match only after whitespace normalisation, which the instrument applies and the manifest `location` fields disclose.

### S016 (Anthropic CVD page): STABLE for browser-like and curl UAs; hard-blocked for urllib.
- ua1, ua2, ua3, ua4, ua6 and the Safari second round returned HTTP 200, 164126 bytes, raw sha256 `fa4e70bc...2eac56d`. That equals the manifest `raw_sha256` and `fetched_bytes`. The raw bytes are byte-identical across 6 UAs and 2 times, with no per-request tokens.
- Normalised: 4481 bytes, sha256 `91cc996f...957a3b`, identical to the committed capture each time.
- Recheck: sha256 OK; Q1, Q2 and Q3 OK, occurrences=1, anchors 17, 16 and 12.
- Caveat: ua5 `Python-urllib/3.12` got HTTP 403, body `error code: 1010` (17 bytes), a Cloudflare browser-signature block. See finding F1.
- Headers: `cf-cache-status: DYNAMIC`, `cache-control: s-maxage=300, stale-while-revalidate=31535700`.

### S060 (CycloneDX 1.7 JSON reference): raw bytes UNSTABLE, normalised slice STABLE.
- ua1, ua2, ua3, ua4, ua6 and 2 same-UA refetches (ua1 string, 22:08:16Z) all returned HTTP 200 and 6419901 bytes, the committed `fetched_bytes`. The raw sha256 differed on every fetch (7 distinct values among my 7 successful fetches). Examples: ua1 `b1e38781...`, ua2 `fa9be79f...`, ua3 `c698b8b5...`, ua4 `95c93441...`, ua6 `2039b072...`, r2 `50be49ed...`, `f58eea4b...`. None equals the committed `raw_sha256` `4d9c10da...`.
- Cause, reproduced: 68 Cloudflare `data-cfemail` / `/cdn-cgi/l/email-protection#` tokens per fetch. Byte differences between two fetches were 3812 and 3998 positions. After stripping those tokens, three fetches (ua1, r2 same1, same2) were identical, sha256 `05397b8c...b4d2b1`.
- The normalised full page text was identical across all 7 successful fetches: 1041903 bytes, sha256 `ffe8c0b6...ba7f4`, the manifest `full_text_sha256`. The declared slice (4889 bytes, 111 lines) matched the committed `S060.txt` exactly, sha256 `d6862622...ce6779`, every time.
- Recheck: sha256 OK; Q1, Q2 and Q3 OK, occurrences=1, anchors 7, 15 and 50.
- ua5 `Python-urllib/3.12` got HTTP 403 / `error code: 1010`, as for S016.

### Verdict on UA and time stability
The committed text captures are stable under UA variation (6 UAs across 4 URLs, curl, Firefox, Safari and custom) and across about 52 min elapsed time. 3 of 3 captures were reproduced byte-for-byte after the instrument's normalisation. No freshness finding on content: nothing drifted, and the S025 and S016 raw bytes are stable too. Two surface defects and one hazard follow.

## Findings (disagreements)
- **F1 (hazard, low): urllib default UA is blocked.** `Python-urllib/3.12` gets Cloudflare 403 `error code: 1010` on both Cloudflare-fronted sources (S016, S060); arXiv does not block it. capture-source.py works only because it overrides the UA (`UA = "kasegi-shokunin/1.0 (documentation capture; ...)"`). Anyone who re-fetches with a bare `urllib` or a UA-less client gets 17 bytes of error text. If the instrument is changed to use the default UA, S016/S060 captures silently fail (they would exit non-zero or capture `error code: 1010`). The manifest does not record this constraint.
- **F2 (metadata defect, low): S060 `raw_sha256` is unverifiable.** Every fetch of that page returns different raw bytes (Cloudflare email-obfuscation tokens). The manifest `reproducibility` text discloses this, but the field is still presented as a hash. No instrument checks it: `grep raw_sha256 corpus/instruments/*.py` finds nothing, so it is documentation only. The `full_text_sha256` and the committed slice hash are the real bindings, and they reproduced. Also, the manifest's "3936 bytes differ" is a one-pair figure; I measured 3812 and 3998 for other pairs, so the number is not a constant.
- **F3 (metadata defect, trivial): S060 `full_text_lines: 22795` is off by one.** The normalised full text has 22794 lines. `wc -l` / `count("\n")` gives 22794 and `split("\n")[:-1]` has 22794 items; 22795 is the count including a trailing empty element. The slice mapping (capture line k>=2 is page-text line 16058+k) is correct: the hash matches. Only the line count is wrong. `git grep -n 22795 HEAD -- corpus/source-snapshots/round-40 corpus/SOURCES.md` shows one hit, `manifest.json:339`.
- **F4 (metadata defect, trivial): UA string mismatch.** The S016 and S060 `tool` and `http.user_agent` fields say `kasegi-shokunin/1.0`, while the instrument named in `tool` sends `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`. The manifest says S016 was obtained via the curl body with the short UA and then `html_to_text`. Both strings return identical bytes (ua1 and ua4 match), so there is no content effect. It is a provenance-precision gap.

## No defect found in
Sizes (S025 602933, S016 164126, S060 6419901), HTTP 200, 0 redirects, landing-page hash, normalised snapshot hashes (3 of 3), quote anchors and uniqueness (8 of 8 quotes OK under source-recheck), or the S060 slice mapping.

## Tools
None installed. Used curl, python3 and pdftotext 26.08.0 as already present.

## Cleanup
Scratch dir `/fast/scratch/hyaku/kasegi-r40/LabFreshFetch/` removed before yield (bodies, headers, probe.sh, norm.py, archive copy). Writes were limited to this receipt and `LabFreshFetch.transcript.txt`. No lane/fleet files were edited and no mutating git commands were run.
