# ScoutMSVR receipt — S048 recon (round 31, C2/F15)

Answering model: anthropic/claude-sonnet-5-5. Scratch: `.ufo/waves/round-31/wave1/ScoutMSVR-scratch/` (raw.html, S048.txt, S048b.txt). Nothing written to corpus/.

## Fetch (curl -sSL, instrument UA)
```
code=200 url=https://www.microsoft.com/en-us/msrc/msvr ctype=text/html; charset=utf-8 size=81802
raw.html sha256 e868fa4561d462a7cd8d19e2413b9e51e1568d968f8a29153447162d26e6f602 (81802 bytes)
```
No redirect (final URL = requested URL).

## capture-source.py (lane tool), exit 0
```
S048 status=200 fetched_bytes=81802 snapshot_bytes=3755 sha256=78dbb989f257db1f21dd6c8c5b67d20341d60bc8f8e71f52a9472b42259828f4 utc=2026-10-25T23:28:18Z
```
Snapshot: 97 lines, 3755 bytes, UTF-8.

### QUIRKS the capture must handle (observed)
1. **Line 2 is nondeterministic**: `This is the Trace Id: <32 hex>` — a per-request id. Second capture (S048b.txt) sha256 `43b3737a…481593` differs ONLY on line 2 (`diff` shows 2c2 only). So the snapshot sha is NOT reproducible by refetch; the manifest pins the committed bytes (source-recheck reads only local files, so exit 0 is unaffected). Never quote line 2; the receipt-bound sha is whichever snapshot ExecCapManifest commits (the S048.txt above is 78dbb989…; any recapture changes it). Raw HTML also carries one `Trace Id` occurrence (raw sha not stable either).
2. **Apostrophes differ by line**: line 30 uses a curly `’` ("Microsoft’s goal…", non-ASCII U+2019, the only non-ASCII line); line 35 uses ASCII `'` (raw HTML `Microsoft&#39;s`, decoded by html.unescape). Quotes spanning "Microsoft's Coordinated…" must use ASCII `'`.
3. Line 33 contains a source typo, "third-party product of affects both" (sic, "of" for "or") — quote verbatim, do not correct.
4. The three routes sit on separate lines (32,33,34), each prefixed by a bold lead-in that html_to_text puts on the same line as its sentence (`Internal Microsoft engineers: In the course…`). The three roles are all on ONE line (35). The normalized text has no "page last updated" date; page chrome (lines 3-27 nav, 36-97 footer incl. Surface/Copilot/ads) is volatile — avoid quoting there.
5. Page title/heading line 28: "Microsoft Security Vulnerability Research (MSVR)"; line 1 is just `msvr`.

## Locations
- L28 heading; L29 purpose sentence; L30 goal (curly apostrophe).
- L31 intro to the three ways (ends with colon).
- L32 route 1 internal engineers; L33 route 2 external reports to MSRC; L34 route 3 internal research projects.
- L35 CVD sentence = Microsoft's three roles (vendor affected / finder in third-party / coordinator of multi-vendor vulns), and the only statement that coordination happens "under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach". No finer-grained coordination process (timelines, contacts) is on this page — page-level evidence only; claims beyond L32-35 would need another source.

## Candidate quotes (each ≤25 words; counts via `grep -cF` on S048.txt; all counts = 1)
| # | Quote (verbatim) | Line | Words | Count | Status |
|---|---|---|---|---|---|
| Q-a | `MSVR learns about vulnerabilities in third-party products in three ways` | 31 | 10 | 1 | exactly-once |
| Q-b | `These vulnerabilities are reported to the MSVR team, which then works with the affected vendor to fix the issue.` | 32 | 19 | 1 | exactly-once (route 1) |
| Q-c | `These issues are coordinated by MSVR.` | 33 | 6 | 1 | exactly-once (route 2: external MSRC reports) |
| Q-d | `Any issues are reported to the affected vendor under accepted Coordinated Vulnerability Disclosure practices.` | 34 | 14 | 1 | exactly-once (route 3) |
| Q-e | `as a vendor affected by vulnerabilities in its products and services` | 35 | 11 | 1 | exactly-once (role 1) |
| Q-f | `as a finder of new vulnerabilities in third-party products and services` | 35 | 11 | 1 | exactly-once (role 2) |
| Q-g | `as a coordinator of vulnerabilities that affect multiple vendors` | 35 | 9 | 1 | exactly-once (role 3) |
| Q-h | `This coordination takes place under Microsoft's Coordinated Vulnerability Disclosure (CVD) approach.` | 35 | 11 | 1 | exactly-once (ASCII apostrophe) |
Also exactly-once: `External reports to the Microsoft Security Response Center (MSRC):` (L33, 9 words); `Internal Microsoft engineers:` (L32); `Internal research projects:` (L34); `MSVR is a program specifically designed to help improve the security ecosystem` (L29, 12 words); `either affects a third-party product of affects both the Microsoft product and external parties` (L33, sic typo, 15 words incl. "that" prefix variant counted =1).
None needs an anchor (no quote string occurs more than once). Short fragments like `MSVR` or `coordinated` are NOT unique — do not use. Q-e/f/g are mid-line fragments of L35: if the manifest checks whole-line matching it will need substring mode (source-recheck searches normalized text, B2 counts occurrences, so substring is fine).

Commands (reproduce): `grep -cF -- "<quote>" S048.txt` per row; `grep -nF` for line numbers; `diff S048.txt S048b.txt` for the Trace Id quirk.

Recommended pick for the F15 entry: Q-a (3-route intro), Q-c (coordination by MSVR of external findings affecting multiple parties), Q-g + Q-f (finder/coordinator roles), Q-h (CVD framing), plus L33's typo clause if the entry needs the "affects both Microsoft and external parties" condition.
