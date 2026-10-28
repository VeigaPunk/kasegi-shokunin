VERDICT: HOLDS

# R46ScoutLive — S073 live drift check

Scope: S073 = https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately
Read-only. Scratch only (`/fast/scratch/hyaku/kasegi-r46/R46ScoutLive/`, removed on exit). No commits, no git mutation, no shared files touched.

## 1. Live capture vs frozen snapshot — no drift

Command:
```
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S073 --url https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately --out "$SCRATCH/S073.live.txt" --kind html
```
Output:
```
S073 status=200 fetched_bytes=577188 snapshot_bytes=15568 sha256=66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930 utc=2026-10-28T23:09:42Z out=/fast/scratch/hyaku/kasegi-r46/R46ScoutLive/S073.live.txt
```

Frozen baseline, `sha256sum` + `wc -c -l` on `corpus/source-snapshots/round-46/S073.txt`:
```
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  .../round-46/S073.txt
  589 15568 .../round-46/S073.txt
```
Live, same measures:
```
  589 15568 /fast/scratch/hyaku/kasegi-r46/R46ScoutLive/S073.live.txt
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  /fast/scratch/hyaku/kasegi-r46/R46ScoutLive/S073.live.txt
```
Byte comparison: `cmp .../round-46/S073.txt S073.live.txt` printed `CMP: files identical`.
Line-level: a python zip over the 589 frozen and 589 live lines printed `line-diff count 0`.

Result: sha256, byte count (15568) and line count (589) all match. The page did not change in the captured text, so no changed lines to report.

Manifest-side figures for reference: `manifest.json` S073 entry records `fetched_utc: 2026-10-28T22:56:49Z`, `bytes: 577188`, `snapshot_bytes: 15568`, `lines: 589`. The live fetch's raw HTML is also 577188 bytes (`wc -c raw.html`), matching the manifest's `bytes`.

## 2. The eight manifest quotes located in the live text

Locator: for each `quotes[]` entry in `round-46/manifest.json`, exact substring test (`quote in line`) against the live 589-line capture. Each printed `FOUND` with live line equal to the manifest anchor:

```
Q1 anchor=560 FOUND live_lines=[560]   L560: Anyone can privately report a security vulnerability to repository maintainers.
Q2 anchor=563 FOUND live_lines=[563]   L563: If you have admin or security permissions for a public repository, you don’t need to submit a vulnerability report. Inst...
Q3 anchor=564 FOUND live_lines=[564]   L564: Private vulnerability reporting is separate from a repository’s SECURITY.md file. You can only report vulnerabilities pr...
Q4 anchor=566 FOUND live_lines=[566]   L566: If the repository doesn't have private vulnerability reporting enabled, you need to initiate the reporting process by fo...
Q5 anchor=573 FOUND live_lines=[573]   L573: By default, you must provide a summary, details, proof of concept, and impact statement. Maintainers can customize the f...
Q6 anchor=574 FOUND live_lines=[574]   L574: Optionally, select I used AI assistance to find or write up this report.
Q7 anchor=577 FOUND live_lines=[577]   L577: When the report is submitted, GitHub automatically adds the reporter of the vulnerability as a collaborator and as a cre...
Q8 anchor=578 FOUND live_lines=[578]   L578: Optionally, click Start a temporary private fork if you want to start to fix the issue. Note that only the repository ma...
```
(The `...` marks where my print truncated at 120 characters; the match test itself was the full quote string.)

Result: 8/8 quotes present at their manifest anchor lines. Because the live text is byte-identical to the frozen snapshot, this is expected; the locator is what discriminates.

## 3. Do-nothing control

Same locator, controls that must NOT match:
```
CTRL-perturbed-Q1 hits=[] -> MISS (expected)     # Q1 with "repository owners" instead of "repository maintainers"
CTRL-absent-phrase hits=[] -> MISS (expected)    # "last updated on"
```
A `grep -c -i "last updated" S073.live.txt` returned `0`. The locator is therefore not a match-everything check: it rejects a one-word perturbation of a real quote and a phrase the page does not contain.

## 4. Revision / "last updated" marker

Searched the live text: `grep -n -i -E "last updated|last-updated|revision|updated|version" S073.live.txt` printed only:
```
75:Dependabot version updates
204:Configure version updates
437:version
```
None is a page-revision marker. The search also found no "last updated" phrase.

Searched the raw HTML (`raw.html`, 577188 bytes) for date/revision metadata:
```
last updated     0
lastmod          0
dateModified     0
datePublished    0
datetime=        0
<time            0
last-modified    0
updated          2
zzqq-absent-term 0     # control term
```
The two `updated` hits are navigation slugs, not revision markers:
`...in/manage-your-dependency-security/controlling-dependencies-updated"...` and `...controlling-dependencies-updated","title":"Control dependency update"...`

Result: the page carries NO `last updated` / revision / datePublished / dateModified marker in either the captured text or the raw HTML. The `date` value in the HTTP response header (below) is the only date the page exposes.

## 5. HTTP headers of the final URL

Command: `curl -sS -L -D headers.txt -o /dev/null https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately` (exit 0). Only one header block was emitted, so there was no redirect: the URL is its own final URL, matching `manifest.json` `http.final_url`.

Relevant printed headers (from the single `HTTP/2 200` block):
```
HTTP/2 200
cache-control: public, max-age=60
x-powered-by: Next.js
content-type: text/html; charset=utf-8
x-github-backend: Kubernetes
x-github-edge-region: iad
via: 1.1 varnish, 1.1 varnish
accept-ranges: bytes
date: Wed, 28 Oct 2026 23:10:52 GMT
age: 85
x-served-by: cache-iad-kiad7000087-IAD, cache-gig2250038-GIG
x-cache: MISS, HIT
x-cache-hits: 0, 1
vary: x-user-version, accept, Accept-Encoding
strict-transport-security: max-age=31557600
content-length: 577188
```
(The CSP and other security headers were also present; the CSP line was truncated by the tool and is not quoted.)

## Limitations

- The live capture and the curl request were served through a Varnish cache (`age: 85`, `x-cache: MISS, HIT`, `cache-control: public, max-age=60`). The bytes are therefore a cached copy at most about a minute old, not a guaranteed origin render. The snapshot-level identity is still an observed fact.
- The sha256 match is observed for the captured text (the instrument's output), not for the browser-rendered DOM. Dynamic content injected after load would not appear in either.
- My `curl` raw-HTML request and the capture both happened at 2026-10-28 ~23:09–23:11 UTC. A later re-check could differ if GitHub edits the page; this check does not establish stability over time.
- The manifest's `fetched_utc` (22:56:49Z) predates this check by about 13 minutes; the page was unchanged across that window in the bytes observed.
- Quote matching is exact-substring; it does not check typography (e.g. `’` vs `'`). Q4 and Q2 contain apostrophes in the live text; matching used the manifest strings as stored, and all eight matched.
- Not done (outside this scout's single item): the F28 entry, the C1 re-grounds, and the counter/control falsification belong to other seats.

## Install / tool record

None. Only `python3`, `curl`, `sha256sum`, `cmp`, `wc`, `grep` were used (all pre-installed).
