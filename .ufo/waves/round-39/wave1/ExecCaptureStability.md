# ExecCaptureStability — round 39 receipt

Seat: ExecCaptureStability (leaf). Item: stability probe for the S057 capture — fetch twice from different vantage (different UA), ~60 s apart, convert with `pdftotext -layout`, confirm normalized text bytes identical and record raw + normalized digests for the capture manifest's reproducibility note.

Axes: depth:verifiability (reproducibility evidence bound to fetched bytes). No change to C1/C2 claims; no lane file edited outside my write scope.

## What the URL actually serves

`https://www.cisa.gov/resources-tools/resources/when-issue-vex-information` serves `text/html; charset=utf-8` (54453 bytes), not a PDF. The page is the CISA landing page: title, publish date `November 06, 2023`, one abstract paragraph, and a Resource Materials row `When to Issue VEX Information / PDF, 229.76 KB` linking `https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf`. So the probe was run on both resources — the landing page (the registry URL, HTML capture leg) and its linked 508c PDF (the `pdftotext -layout` leg named in the item). Both legs are recorded in the deliverable so the manifest note binds whichever resource the S057 capture uses.

## Commands and actual output

First fetch (instrument UA), landing page:

```
$ curl -sS -L --max-time 90 -A "kasegi-shokunin/1.0" -D headers1.txt -o raw1.bin \
    -w 'status=%{http_code} bytes=%{size_download} url=%{url_effective} ct=%{content_type}\n' \
    "https://www.cisa.gov/resources-tools/resources/when-issue-vex-information"
status=200 bytes=54453 url=https://www.cisa.gov/resources-tools/resources/when-issue-vex-information ct=text/html; charset=utf-8
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T19:30:29Z
$ file raw1.bin
raw1.bin: HTML document, Unicode text, UTF-8 text, with very long lines (2764)
$ sha256sum raw1.bin
4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d  raw1.bin
$ grep -oE 'href="[^"]*\.pdf[^"]*"' raw1.bin | sort -u
href="/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf"
```

Landing page response headers (fetch A): `HTTP/2 200`, `cache-control: private, no-cache, must-revalidate`, `date: Mon, 26 Oct 2026 19:30:29 GMT`; no ETag, no Last-Modified, no Content-Length.

First fetch, linked PDF:

```
$ curl -sS -L --max-time 90 -A "kasegi-shokunin/1.0" -D pdfheaders1.txt -o pdf1.bin \
    -w 'pdf1 status=%{http_code} bytes=%{size_download} ct=%{content_type} url=%{url_effective}\n' \
    "https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf"
pdf1 status=200 bytes=235270 ct=application/pdf url=https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-26T19:30:44Z
$ file pdf1.bin
pdf1.bin: PDF document, version 1.7, 9 page(s)
$ sha256sum pdf1.bin
cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99  pdf1.bin
$ pdftotext -layout pdf1.bin pdf1.layout.txt && sha256sum pdf1.layout.txt && wc -c -l pdf1.layout.txt
d32b961ce530e97389e08db6e160bd98fa88db91f8620a1604ee50a81d5daa35  pdf1.layout.txt
  400 19718 pdf1.layout.txt
```

PDF response headers (fetch A): `HTTP/2 200`, `content-length: 235270`, `last-modified: Mon, 06 Nov 2023 15:43:40 GMT`, `etag: "39706-6097db7d52c78"`, `cache-control: max-age=186302`.
`pdfinfo pdf1.bin`: Title `When to Issue VEX Information`, Author `CISA`, CreationDate `Thu Nov 2 17:33:09 2023 -03`, ModDate `Thu Nov 2 17:34:47 2023 -03`, Pages 9, Encrypted no, PDF 1.7, 235270 bytes. 235270/1024 = 229.76 KiB, matching the landing page's stated file size.

Second fetch (recheck UA), both resources, 66 s / 57 s after the first:

```
2026-10-26T19:31:35Z
html2 status=200 bytes=54453 ct=text/html; charset=utf-8 url=https://www.cisa.gov/resources-tools/resources/when-issue-vex-information
2026-10-26T19:31:41Z
pdf2 status=200 bytes=235270 ct=application/pdf url=https://www.cisa.gov/sites/default/files/2023-11/When-to-Issue-a-VEX-508c.pdf
2026-10-26T19:31:41Z
4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d  raw1.bin
4e6aa483c20013bb84d43d166e3f20c91fba63ece7c35861f6d95c8b61af0e4d  raw2.bin
cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99  pdf1.bin
cbcbd77af32c589eaf85aef4e3911b133fd95ccdedd80b56b40e9c0909450d99  pdf2.bin
d32b961ce530e97389e08db6e160bd98fa88db91f8620a1604ee50a81d5daa35  pdf1.layout.txt
d32b961ce530e97389e08db6e160bd98fa88db91f8620a1604ee50a81d5daa35  pdf2.layout.txt
  400 19718 pdf2.layout.txt
```

Second fetch headers: landing page `HTTP/2 200`, same `cache-control: private, no-cache, must-revalidate`, `date: Mon, 26 Oct 2026 19:31:35 GMT`; PDF `HTTP/2 200`, `content-length: 235270`, same `last-modified` and `etag`, `date: Mon, 26 Oct 2026 19:31:41 GMT`.

Normalization with the lane's own instrument (`corpus/instruments/capture-source.py`, imported read-only), then byte comparison:

```
html1 normalized bytes=3497 lines=135 sha256=c868f04a56c4fcc8dcfedc7354b2c65df5e47c8d55caf0f0502005e030360db2
pdf1 layout-normalized bytes=17977 lines=278 sha256=03dd22dcd761ed1e39f7c35fa074d3d9bb3f6e9b498746c6432ff60098e9480a
pdf1 instrument(pdf_to_text) bytes=17971 lines=275 sha256=11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
html2 normalized bytes=3497 lines=135 sha256=c868f04a56c4fcc8dcfedc7354b2c65df5e47c8d55caf0f0502005e030360db2
pdf2 layout-normalized bytes=17977 lines=278 sha256=03dd22dcd761ed1e39f7c35fa074d3d9bb3f6e9b498746c6432ff60098e9480a
pdf2 instrument(pdf_to_text) bytes=17971 lines=275 sha256=11c8d6d684448a1ae049ecf4881cd98172fad7333a9fd7829e6b12c9b5d64f2f
--- byte equality ---
raw equal
html norm equal
layout equal
pdf layout-norm equal
pdf instrument-norm equal
```

(`normalized` above = `html_to_text()` for the landing page; `pdf_to_text()` uses `pdftotext -enc UTF-8` without `-layout` and then `collapse()`. The `-layout` leg is additionally collapsed to whitespace-normalized form so the comparison is against text, not column padding.)

Instrument determinism cross-check on the bytes I fetched (same instrument, `--kind html`, second invocation over `raw1.bin`):

```
S057 status=200 fetched_bytes=54453 snapshot_bytes=3497 sha256=c868f04a56c4fcc8dcfedc7354b2c65df5e47c8d55caf0f0502005e030360db2 utc=2026-10-26T19:30:36Z
```

## Deliverable

- Path: `.ufo/waves/round-39/wave1/ExecCaptureStability.stability.txt`
- 18 lines, 3689 bytes, sha256 `87fce57e1e16330dade20ac54a55312331930b7a2d90f59dcfaa23b333df1ffc`, trailing newline present.
- Content is the reproducibility note only (resource identification, per-fetch UTC/UA/status/bytes, raw and normalized digests, byte-equality results, and the scope-of-claim caveat). No scaffolding, no tables, no headings that are not part of the note itself.

## Scratch and host discipline

- Scratch `S=/fast/scratch/hyaku/kasegi-r39/ExecCaptureStability/` held `raw{1,2}.bin`, `pdf{1,2}.bin`, `pdf{1,2}.layout.txt`, the normalized copies and headers. All curl fetches and conversions wrote there. One exception disclosed: the `capture-source.py --kind html` cross-check wrote its 3497-byte snapshot and a 54453-byte input copy into `/tmp/tmp.X4sDfXMVlC` (a `mktemp -d` I passed as `--out`), well under the 50 MB `/tmp` allowance; that directory was removed (`ls -d /tmp/tmp.X4sDfXMVlC` → `No such file or directory`). No inherited `TMPDIR` was relied on.
- Disk guard checked before any fetch: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → `/fast/scratch/hyaku 24% 610.7G free` (green).
- Scratch removed before yielding; absence verified with `ls -d /fast/scratch/hyaku/kasegi-r39/ExecCaptureStability` → `No such file or directory`.
- No tool installed or upgraded: `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0`, `pdftotext version 26.08.0`, `sha256sum`/`cmp` from coreutils were already present. No pacman, no config edit.
- No git/jj mutation: only `git status --porcelain`, `git log --oneline` in the lane. No file written outside the deliverable path and my scratch. Fetches were `GET` only; 5 HTTP requests total (3 landing page — including one inside `capture-source.py` — and 2 PDF), all HTTP 200.
- The `capture-source.py --kind html` run was itself a third independent landing-page fetch at 2026-10-26T19:30:36Z and printed the same snapshot digest `c868f04a…60db2`, so the landing-page normalization reproduced across three fetches, not two.

## Risks / notes

1. The frozen claim names `https://www.cisa.gov/resources-tools/resources/when-issue-vex-information` as the S057 source, but that URL is a no-cache HTML landing page whose normalized text is only 3497 bytes (title, date, abstract, Resource Materials row, nav/footer). The document body — the issuance/lifecycle/reaffirmation/inheritance material the F22 frontier describes — lives in the linked 508c PDF (`.../2023-11/When-to-Issue-a-VEX-508c.pdf`, 9 pages). Whether the S057 capture is the landing page or the PDF is the C2 seat's call; both legs are probed and stable, so the manifest note can bind either without re-fetching.
2. Stability is claimed only over the measured window (66 s landing page, 57 s PDF, same host, different UA). The landing page is explicitly `no-cache` and dynamically assembled, so byte-identity is an observation, not a server guarantee; the PDF is immutable in practice (Last-Modified 2023-11-06, ETag stable across fetches).
3. The instrument UA (`kasegi-shokunin/1.0 (documentation capture; ...)`) differs from the probe UA (`kasegi-shokunin/1.0`); the landing page returned identical bytes under both probe UAs, so UA is not a byte-affecting vantage here.
