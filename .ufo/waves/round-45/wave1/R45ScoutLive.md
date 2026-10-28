VERDICT: HOLDS

S071 live drift, measured 2026-10-28T21:03:18Z–21:03:55Z. The pinned capture is the RST at `corpus/source-snapshots/round-45/S071.txt` (manifest `capture_url` `https://docs.kernel.org/_sources/process/security-bugs.rst.txt`, `fetched_utc` `2026-10-28T20:52:44Z`). Two live GETs of that RST are byte-identical to the pin (sha256, 20152 bytes, 372 lines). The five manifest quotes are each present once in the live HTML text after whitespace collapse. No prose difference against the pin.

Tooling: no package installed. `curl 8.23.0`, `Python 3.14.8`, `sha256sum`/`cmp`/`diff`/`wc` from the host. User-Agent `kasegi-shokunin/1.0`. `TMPDIR=/fast/scratch/hyaku/kasegi-r45/R45ScoutLive`. Bodies saved with `curl --compressed` (decoded document, not the gzip wire bytes).

## 1. Do-nothing control: local pin, no network

Attacked: `corpus/source-snapshots/round-45/S071.txt` against `corpus/source-snapshots/round-45/manifest.json` S071 pin `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, 20152 bytes, 372 lines.

```
COMMAND: sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt
COMMAND: wc -lc /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt
  372 20152 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/source-snapshots/round-45/S071.txt
COMMAND: cmp <S071.txt> <S071.txt>
cmp_self_exit=0
```

```
PINFILE sha256=0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40 bytes=20152 newlines=372 splitlines=372 endswith_newline=1
PINFILE sha256_eq_manifest=1
PINFILE bytes_eq_manifest=1
PINFILE newlines_eq_manifest_lines=1
PINFILE splitlines_eq_manifest_lines=1
ANCHOR Q1 verdict=ok anchor=310 line=the reporter or an affected party for up to 7 calendar days from the start
ANCHOR Q2 verdict=ok anchor=95 line=**If you resorted to AI assistance to identify a bug, you must treat it as
ANCHOR Q3 verdict=ok anchor=39 line=    instructions, file-system image etc).  Binary-only executables are not
ANCHOR Q4 verdict=ok anchor=41 line=    without consent from the reporter, unless they are already public.  By
ANCHOR Q5 verdict=ok anchor=20 line=  * **affected kernel version range**: with no version indication, your report
PINTEXT SUMMARY hits=5/5
```

Each pin hit was `exact_raw=0 exact_text=0 normalized_count=1`. The manifest strings are not raw substrings; they wrap across lines. `corpus/instruments/source-recheck.py` agrees:

```
COMMAND: python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-45/manifest.json --source S071
S071:sha256 OK
S071:Q1 OK normalized=markup-whitespace occurrences=1 anchor=310-ok
S071:Q2 OK normalized=markup-whitespace occurrences=1 anchor=95-ok
S071:Q3 OK normalized=markup-whitespace occurrences=1 anchor=39-ok
S071:Q4 OK normalized=markup-whitespace occurrences=1 anchor=41-ok
S071:Q5 OK normalized=markup-whitespace occurrences=1 anchor=20-ok
source_recheck_exit=0
```

This control always matches the pin and prints no `Last-Modified` header. It cannot detect live drift.

## 2. Discriminators that must miss

Empty HTML body (locator default is not a hit):

```
LOCATOR label=EMPTY html_mode=1 raw_bytes=0 text_chars=0 norm_chars=0
EMPTY Q1 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
EMPTY Q2 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
EMPTY Q3 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
EMPTY Q4 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
EMPTY Q5 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
EMPTY SUMMARY hits=0/5
```

Same five S071 quotes searched in pinned S072 (`sha256sum` printed `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`):

```
LOCATOR label=NEGFILE html_mode=0 raw_bytes=10032 text_chars=10030 norm_chars=9428
NEGFILE Q1 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
NEGFILE Q2 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
NEGFILE Q3 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
NEGFILE Q4 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
NEGFILE Q5 MISS exact_raw=0 exact_text=0 normalized_count=0 prefix48_count=0
NEGFILE SUMMARY hits=0/5
```

Empty header file versus live header files:

```
COMMAND: grep -i '^last-modified:' empty.hdr
empty_hdr_grep_exit=1
COMMAND: grep -i '^last-modified:' rst1.hdr html1.hdr
rst1.hdr:last-modified: Sun, 09 Aug 2026 21:57:49 GMT
html1.hdr:last-modified: Sun, 18 Oct 2026 23:32:42 GMT
live_hdr_grep_exit=0
```

## 3. Live RST versus S071.txt — no byte difference

`curl -sS -L --compressed -A kasegi-shokunin/1.0 --max-time 60` of `https://docs.kernel.org/_sources/process/security-bugs.rst.txt`, twice.

```
name=rst1 http_code=200 size_download=8680 content_type=text/plain; charset=utf-8 num_redirects=0 url_effective=https://docs.kernel.org/_sources/process/security-bugs.rst.txt
curl_rst1_exit=0
  372 20152 rst1.body
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  rst1.body
name=rst2 http_code=200 size_download=8680 content_type=text/plain; charset=utf-8 num_redirects=0 url_effective=https://docs.kernel.org/_sources/process/security-bugs.rst.txt
curl_rst2_exit=0
  372 20152 rst2.body
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  rst2.body
cmp_snap_rst1_exit=0
cmp_rst1_rst2_exit=0
cmp_verbose_exit=0
0 rst1.diff
diffq_rst_pair_exit=0
```

`cmp` of S071.txt against the first body exited 0 and printed nothing. `diff -u` produced an empty diff (`0` lines). Both live bodies and the pin share sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, 20152 bytes, 372 newlines. `size_download=8680` is the gzip wire size (`content-length: 8680`, `content-encoding: gzip`). The hashed file starts `2e2e 205f 7365 6375 7269 7479 6275 6773` (`.. _securitybugs`), so the hash is the decoded RST.

rst1 response headers (rst2 repeated the same `last-modified`; its `date` was also `Wed, 28 Oct 2026 21:03:19 GMT`; `x-cache` was `HIT` / `x-cache-hits: 1` on rst2 versus `MISS` / `0` on rst1):

```
HTTP/2 200 
server: nginx
content-type: text/plain; charset=utf-8
last-modified: Sun, 09 Aug 2026 21:57:49 GMT
content-security-policy: default-src 'self' 'unsafe-inline'; img-src https: data:
content-encoding: gzip
accept-ranges: bytes
age: 0
date: Wed, 28 Oct 2026 21:03:19 GMT
via: 1.1 varnish
x-served-by: cache-gru-sbgr1930069-GRU
x-cache: MISS
x-cache-hits: 0
x-timer: S1793221399.577819,VS0,VE561
vary: Accept-Encoding
strict-transport-security: max-age=31557600
alt-svc: h3=":443";ma=86400,h3-29=":443";ma=86400,h3-27=":443";ma=86400
content-length: 8680
```

Last-Modified on the RST object: `Sun, 09 Aug 2026 21:57:49 GMT`.

## 4. Five manifest quotes in the live HTML

`https://docs.kernel.org/process/security-bugs.html`, two GETs. HTML is not the pinned capture, so its digest is not expected to equal S071.

```
name=html1 http_code=200 size_download=12016 content_type=text/html; charset=utf-8 num_redirects=0 url_effective=https://docs.kernel.org/process/security-bugs.html
curl_html1_exit=0
  545 33621 html1.body
174a89d065a58c462c5b398255969fbfdd1d300ddb30f95b27959ddbd2980cb2  html1.body
name=html2 http_code=200 size_download=12016 content_type=text/html; charset=utf-8 num_redirects=0 url_effective=https://docs.kernel.org/process/security-bugs.html
curl_html2_exit=0
174a89d065a58c462c5b398255969fbfdd1d300ddb30f95b27959ddbd2980cb2  html1.body
174a89d065a58c462c5b398255969fbfdd1d300ddb30f95b27959ddbd2980cb2  html2.body
cmp_html1_html2_exit=0
  545 33621 html2.body
```

html1 headers:

```
HTTP/2 200 
server: nginx
content-type: text/html; charset=utf-8
last-modified: Sun, 18 Oct 2026 23:32:42 GMT
content-security-policy: default-src 'self' 'unsafe-inline'; img-src https: data:
content-encoding: gzip
accept-ranges: bytes
age: 0
date: Wed, 28 Oct 2026 21:03:19 GMT
via: 1.1 varnish
x-served-by: cache-gru-sbgr1930061-GRU
x-cache: HIT
x-cache-hits: 0
x-timer: S1793221399.248321,VS0,VE538
vary: Accept-Encoding
strict-transport-security: max-age=31557600
alt-svc: h3=":443";ma=86400,h3-29=":443";ma=86400,h3-27=":443";ma=86400
content-length: 12016
```

html2 `last-modified` was the same line; its `date` was `Wed, 28 Oct 2026 21:03:55 GMT`. Last-Modified on the HTML object: `Sun, 18 Oct 2026 23:32:42 GMT`.

Decoded HTML begins `0a3c 2144 4f43 5459 5045 2068 746d 6c3e` (`.<!DOCTYPE html>`). Locator: strip `script`/`style`, take text nodes (`html.parser`, `convert_charrefs=True`), then the same whitespace collapse as `source-recheck.py` `normalize` (drop `</?u>`, then `" ".join(text.split())`).

```
LOCATOR label=LIVEHTML html_mode=1 raw_bytes=33621 text_chars=21436 norm_chars=20510
LIVEHTML Q1 HIT exact_raw=0 exact_text=0 normalized_count=1 prefix48_count=1
LIVEHTML Q1 SNIPPET come available, this may be postponed at the request of the reporter or an affected party for up to 7 calendar days from the start of the release process, with an exceptional extension to 14 calendar days if it is agreed that the criticality of the bug requires more time. The only valid reason
LIVEHTML Q2 HIT exact_raw=0 exact_text=0 normalized_count=1 prefix48_count=1
LIVEHTML Q2 SNIPPET reporting, consider whether the issue actually crosses a trust boundary on such a system. If you resorted to AI assistance to identify a bug, you must treat it as public. While you may have valid reasons to believe it is not, the security team’s experience sh
LIVEHTML Q3 HIT exact_raw=0 exact_text=0 normalized_count=1 prefix48_count=1
LIVEHTML Q3 SNIPPET l be needed (source code, shell script, sequence of instructions, file-system image etc). Binary-only executables are not accepted. Working exploits are extremely helpful and will not be released without consent from the 
LIVEHTML Q4 HIT exact_raw=0 exact_text=0 normalized_count=1 prefix48_count=1
LIVEHTML Q4 SNIPPET d will not be released without consent from the reporter, unless they are already public. By definition if an issue cannot be reproduced, it is not exploitable, thus it is not a security bug. conditions: if the bug depends on certain configuration options, sysctls, permissions, ti
LIVEHTML Q5 HIT exact_raw=0 exact_text=0 normalized_count=1 prefix48_count=1
LIVEHTML Q5 SNIPPET ation are absolutely necessary in any security bug report: affected kernel version range: with no version indication, your report will not be processed. Note that a time-dependent version such as “latest mainline” is not acceptable. A stable
LIVEHTML SUMMARY hits=5/5
```

Raw windows (`str.find` on the HTML bytes decoded as UTF-8), showing the line wrap that makes `exact_raw=0`:

```
RAW Q1 find=29337 count=1
RAW Q1 REPR ' may be postponed at the request of\nthe reporter or an affected party for up to 7 calendar days from the start\nof the release process, with an exceptional extension to 14 cale'
RAW Q2 find=15168 count=1
RAW Q2 REPR 'ly crosses a trust boundary on such\na system.</p>\n<p><strong>If you resorted to AI assistance to identify a bug, you must treat it as\npublic</strong>. While you may have valid reasons to beli'
RAW Q3 full-sentence find=-1 count=0
HTML Binary-only find=11425 count=1
HTML REPR 'Binary-only executables are not\naccepted.  Working exploits are extremely helpful and will not be released\nwithout conse'
RAW Q4 find=11626 count=1
RAW Q4 REPR 't from the reporter, unless they are already public.  By\ndefinition if an issue cannot be reproduced, it is not exploitable, thus it\nis not a security bug.</p></li>\n<li><p><strong>conditions</strong>: if'
RAW Q5 find=10194 count=1
RAW Q5 REPR '<ul class="simple">\n<li><p><strong>affected kernel version range</strong>: with no version indication, your report\nwill not be processed.  Note that a time-dependent version such as “latest\nmain'
```

Q1–Q5 strings located, each `normalized_count=1`. The RST pin wraps the same way (`Binary-only executables are not\n    accepted.`).

## 5. Difference that is not pin drift

The HTML object’s `last-modified` (`Sun, 18 Oct 2026 23:32:42 GMT`) is later than the RST object’s (`Sun, 09 Aug 2026 21:57:49 GMT`). HTML sha256 `174a89d065a58c462c5b398255969fbfdd1d300ddb30f95b27959ddbd2980cb2`, 33621 bytes, 545 lines, versus S071 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, 20152 bytes, 372 lines. The manifest pins the RST, and that body did not change. There is no pinned HTML to diff. The five quote cores are still in the rendered text.

## Limitations

- One clock window. `date -u` started at `2026-10-28T21:03:18Z`; response `date` headers were `Wed, 28 Oct 2026 21:03:19 GMT` (rst1, rst2, html1) and `Wed, 28 Oct 2026 21:03:55 GMT` (html2). This does not say the page stays byte-stable after that.
- Hashes are decoded bodies. `content-length` / `size_download` are the gzip sizes (RST 8680, HTML 12016).
- Quote location is whitespace-normalized text, not a raw substring. `exact_raw=0` on the pin itself. HTML tags are removed before collapse; Q2 is split by `</strong>`’s surrounding markup and a newline (`as\npublic`).
- Served by nginx via Varnish (`age: 0`). rst1 was `x-cache: MISS`, rst2 `HIT`; the two bodies still matched. HTML was fetched twice and `cmp` exited 0.
- Public documentation GET only. No other host, no form post.
- Scratch under `/fast/scratch/hyaku/kasegi-r45/R45ScoutLive` held the bodies. Removed after the measurements above. The quoted command output is the evidence.

```
rm -rf /fast/scratch/hyaku/kasegi-r45/R45ScoutLive
if test ! -d /fast/scratch/hyaku/kasegi-r45/R45ScoutLive; then echo "scratch_absent=1"; else echo "scratch_absent=0"; fi
scratch_absent=1
```
