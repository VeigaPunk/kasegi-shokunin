# ScoutCaptureAvailability — S055 capture plan: executable and stable (round 38)

Seat: leaf scout, read-only; no repo writes except this receipt; no tool installs. Scratch `/fast/scratch/hyaku/kasegi-r38/ScoutCaptureAvailability/` removed before yield.
URL: `https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` (S055). Verdict: **capture plan executable and stable; no blocker.**

## 1. Two raw fetches 60 s apart (`curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`)
| fetch | UTC | HTTP | bytes | redirects | effective URL | raw sha256 |
|---|---|---|---|---|---|---|
| 1 | 2026-10-26T18:35:52Z | 200 | 414858 | 0 | same as requested | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |
| 2 | 2026-10-26T18:36:53Z (sleep 60 between) | 200 | 414858 | 0 | same as requested | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` |

`cmp raw1.html raw2.html` -> IDENTICAL. Same hash as ExecC2Capture's two fetches (18:25:51Z and 18:29:36Z): four fetches over ~11 min, one hash. Stable.

## 2. HEAD / headers (HEAD at 2026-10-26T18:36:53Z: HTTP/2 200, `num_redirects=0`)
- ETag: **none served** (HEAD, GET 1, GET 2 carry no `etag`). Content-Length: none served (chunked). Validation therefore rests on `Last-Modified` + raw sha256, not ETag.
- Last-Modified: `Sun, 05 Apr 2026 13:17:09 GMT` on HEAD and both GETs (unchanged).
- `cache-control: public, max-age=31536000, immutable`; `x-cache: Hit from cloudfront`; `age` 1370 (GET 1) -> 1431 (GET 2/HEAD), consistent with 61 s elapsed — a single cached object, not re-generated per request.
- `link: <https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html>; rel="canonical"` (self).
- Redirect: none. `curl -I` without `-L`: `200 redirect_url=[]`.
- `Accept-Encoding` handling: `--compressed` served `content-encoding: zstd`; decoded body sha256 equals the plain fetch (`fad0c60d…cd66b`). Range request `-r 0-99` returned HTTP 200 (no `accept-ranges`), so partial fetch is unavailable; full GET is the only mode (0.06 s, no issue).

## 3. Client-dependent raw bytes (note for the manifest, not a blocker)
`capture-source.py` (python urllib, HTTP/1.1 chunked) receives **415225 bytes, raw sha256 `0fbc5857…d339ba`**, not the 414858 bytes curl (HTTP/2) receives: Cloudflare injects one `<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/…" data-cf-beacon=…>` line (first difference at byte 414842) for the urllib client. `capture-source.py` strips `<script>` blocks, so the normalized text is unaffected. A different UA string (`kasegi-shokunin/1.0 (documentation capture; …)`, curl) still gave 414858 / `fad0c60d…`. Consequence: the manifest's raw-body hash and `fetched_bytes` depend on which client captured; the snapshot hash does not. Executors should state which client's raw hash they record (ExecC2Capture recorded the curl one, 414858/`fad0c60d…`; `capture-source.py` prints 415225).

## 4. Normalized text and large-file rules
Reproduction (scratch only): `python3 corpus/instruments/capture-source.py --id S055 --url <URL> --out $S/S055-repro.txt --kind html` printed
`S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:37:07Z`; 5146 lines; `cmp` against `.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt` -> identical (sha256 `63c8ad52…cd11cd42`, matches ExecC2Capture's deliverable table).
- Normalized size 272441 B = 0.26 MiB. Limits: `jj config get snapshot.max-new-file-size` in the lane = `1MiB` (1048576 B); jj-lane.sh `commit` refuses a *named file* >10485760 B without `--allow-large` (jj-lane.sh lines 638-639) and its comments (lines 654-657) say named files are tracked with `--include-ignored` (bypassing the 1 MiB cap) whereas named directories are tracked like `git add <dir>` and honour the cap.
- 272441 < 1048576 < 10485760: S055.txt (and manifest.json, 3841 B) pass even when committed through a directory path; no `--allow-large` needed. Even the raw HTML (414858 B) is under 1 MiB.
- Precedent: `corpus/source-snapshots/round-35/S052.txt` is tracked at 1479694 B (>1 MiB) via commit 5a25337 "(named >1MiB)"; the next largest tracked snapshots are 249789 B (round-24 S032) and 147267 B (S041). S055 at 272441 B becomes the second-largest committed snapshot, well within limits.
- Recommendation: name `corpus/source-snapshots/round-38/S055.txt` and `…/manifest.json` as files in the landing commit anyway (house habit from round 35); no flag required.

## 5. Lane state observed
`git status --porcelain` showed only untracked `.ufo/waves/round-38/wave1.ready`, `wave1.ready.dispatched`, `wave1/`; `corpus/source-snapshots/round-38/` does not exist yet (to be created by the L1 landing).
Nothing else touched; no mutating git/jj commands run.
