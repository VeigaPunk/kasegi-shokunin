# K72ScoutCapture — S107 capture reproducibility (read-only scout)

Seat: K72ScoutCapture (leaf, no dispatch). Lane untouched: `git status` shows only the
integrator's edits; every command below is read-only or writes into
`/fast/scratch/hyaku/kasegi-r72/K72ScoutCapture/`.

Tools used (no installs): `curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0 OpenSSL/3.6.5`,
`Python 3.14.8`, `git version 2.56.0`. No tool was installed or upgraded.

## (1) Single fetch of the source URL

```
$ curl -sS -L -o $S/fetch.html -w '%{http_code} %{size_download}\n' \
    https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html
200 84557
```

- HTTP status **200**, **84557** bytes downloaded.
- sha256 of the fetched bytes:

```
$ sha256sum $S/fetch.html
d7ca4e440fc174094c08457c672aea27cdee9c73149d8d6924da49b64e6cf1ce  /fast/scratch/hyaku/kasegi-r72/K72ScoutCapture/fetch.html
```

- Raw bytes are stable across two independent fetches (curl default UA and the
  instrument's own UA) and across time:

```
$ curl -sS -L -o $S/fetch2.html -w 'http_code=%{http_code} size=%{size_download}\n' .../bug.html
http_code=200 size=84557
$ sha256sum $S/fetch2.html
d7ca4e440fc174094c08457c672aea27cdee9c73149d8d6924da49b64e6cf1ce  .../fetch2.html
$ cmp $S/fetch.html $S/fetch2.html   -> RAW BYTES STABLE across fetches
```

The instrument's UA fetch returns the identical raw digest
(`d7ca4e44…`, 84557 bytes) — the UA does not perturb the served bytes.

## (2) Re-run of the lane's capture instrument into scratch

```
$ TMPDIR=$S python3 .../corpus/instruments/capture-source.py --id S107 \
    --url https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html \
    --kind html --out $S/S107.txt
S107 status=200 fetched_bytes=84557 snapshot_bytes=31435 sha256=0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652 utc=2026-11-05T03:53:31Z out=/fast/scratch/hyaku/kasegi-r72/K72ScoutCapture/S107.txt
```

**Measured sha pair**

| side | sha256 | bytes | lines |
|---|---|---|---|
| my re-run `$S/S107.txt` | `0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652` | 31435 | 1176 |
| committed `corpus/source-snapshots/round-72/S107.txt` | `0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652` | 31435 | 1176 |

**Verdict: IDENTICAL** (`cmp` exit 0 — byte-identical, zero differing lines; the
`diff` line counts are therefore 0 and there are no first-three differing lines).

```
$ cmp $S/S107.txt .../corpus/source-snapshots/round-72/S107.txt
BYTE-IDENTICAL
```

A second instrument run reproduced the same digest (`S107_second.txt`, exit 0,
identical to both). The instrument's own selftest passes:

```
$ TMPDIR=$S python3 .../capture-source.py --selftest
selftest normalize=ok deterministic=ok      (exit=0)
```

**Normalization is independently reproducible from the fetched bytes alone** — I
re-ran the committed instrument's `html_to_text` over `$S/fetch.html` and got the
committed snapshot back byte-for-byte:

```
raw bytes         : 84557
raw sha256        : d7ca4e440fc174094c08457c672aea27cdee9c73149d8d6924da49b64e6cf1ce
normalized bytes  : 31435
normalized sha256 : 0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652
committed sha256  : 0b944ea123efa204f1c0539c7d9d8f0367c25741210290681099fb6429254652
normalize(fetch.html)==committed S107.txt : True
```

The capture instrument itself is the committed one, unmodified:
`git show a34ce4c:corpus/instruments/capture-source.py | sha256sum` and
`sha256sum corpus/instruments/capture-source.py` both give
`e1831888d7192a5b7d55636a89e4da4a705eabdae77b812d20e72eafb633dc18`.

## (3) Version line / "last updated"

**A version line exists; no "last updated" statement exists.**

- Capture **L1** `6.1.3. Bugs — Bugzilla 5.2+ documentation` — the page `<title>`;
  raw HTML: `<title>6.1.3. Bugs &mdash; Bugzilla 5.2+ documentation</title>`.
- Capture **L2** `5.2` — the Read the Docs sidebar version div
  (`<div class="version"> 5.2 </div>`), i.e. the doc set's own version marker.
- The capture contains **no** "last updated" / "last modified" / "updated on"
  line. `grep -niE 'last updated|page updated|document updated|updated on' S107.txt`
  returns nothing; the only "last modified" hit is unrelated prose about a bug
  flag timestamp (`S107.txt:364`). The raw HTML carries no `<meta>` date/time
  element and no `<time>` element; the footer (`<div role="contentinfo"><p></p>`)
  is empty of a date. The only dates in the raw HTML are JSON example payloads
  (`"creation_time": "2000-07-25T13:50:04Z"`, `"last_change_time":
  "2014-09-29T14:25:35Z"`, `"last_change_time": "2014-09-23T19:12:17Z"`).
- The build toolchain is stated at capture **L1174–L1176**:
  `Built with Sphinx using a` / `theme` / `provided by Read the Docs.`
- The version of the *docs* (5.2) is distinct from the `latest` track pointer:
  response header `x-rtd-version: latest`, `x-rtd-version-method: path`,
  `x-rtd-path: /proxito/html/bugzilla/latest/api/core/v1/bug.html`.

**Durability finding [INFERENCE from the headers + version div]:** the recorded URL
is the `latest` alias, so it is a moving pointer, not a version-pinned path; the
pinned sha256 (not the URL) is the durable authority. The served bytes were
identical across fetches on 2026-11-05, and `last-modified: Fri, 28 Aug 2026
05:52:15 GMT` / `etag: W/"2ae07139c2ff342a02969e99fb6b8f87"` were identical
across my two header fetches. Whether a version-pinned sibling path exists under
the same host was **not** measured — the item's URL allow-list covers only the
`latest` path, and the RTD version switcher is JS-driven
(`documentation_options.js`), so no version list is present in the fetched bytes.

## (4) Canonical URL and redirect chain

**No redirects.** The chain is a single hop.

```
$ curl -sSI -L https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html
HTTP/2 200
date: Thu, 05 Nov 2026 03:55:32 GMT
content-type: text/html; charset=utf-8
cache-control: max-age=1800, stale-if-error=86400, public
server: cloudflare
vary: Accept-Encoding
etag: W/"2ae07139c2ff342a02969e99fb6b8f87"
last-modified: Fri, 28 Aug 2026 05:52:15 GMT
x-rtd-domain: bugzilla.readthedocs.io
x-rtd-path: /proxito/html/bugzilla/latest/api/core/v1/bug.html
x-rtd-project: bugzilla
x-rtd-version: latest
x-rtd-version-method: path
```

- `grep -c '^HTTP/'` = **1** — one status line, no `3xx`.
- `grep -ci '^location:'` = **0** — no `Location` header is issued at all.
- `curl -sS -L -o /dev/null -w ...` → `final_url=https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html`,
  `num_redirects=0`, `http_code=200`.
- The instrument's own fetch likewise reports `status=200` with
  `final_url = https://bugzilla.readthedocs.io/en/latest/api/core/v1/bug.html`
  (identical to the requested URL).

**Confirmed:** the URL the capture records is the canonical one — requested URL ==
final URL, status 200, zero redirects. The manifest records the same pair
(`"url"` == `"capture_url"` == `http.final_url`, `http.status: 200`).

**Qualification [observed]:** the served HTML carries **no** `<link rel="canonical">`
element (`grep -ci 'rel="canonical"' fetch.html` → 0) and no `og:url`. So the
canonicality of this URL rests on the server's 200-without-redirect behaviour
plus the manifest's own record — not on an in-page canonical tag. A future
redirect inserted on this path would be caught by the pinned sha256, but the
`capture_url` string in the manifest is not independently attested by the page.

## (5) Attribution

This is the **Bugzilla project's own documentation of its own API**, hosted as the
`bugzilla` project on Read the Docs (`x-rtd-project: bugzilla`); it is **not** a
Mozilla policy document and **not** a Red Hat policy document — neither vendor
appears anywhere in the capture (`grep -niE 'mozilla|red hat|redhat|foundation'`
→ no hits), and the page states its own scope as the tracker's REST interface.

## Source-binding and round state (measured read-only)

The committed manifest `corpus/source-snapshots/round-72/manifest.json` names S107
with `sha256 0b944ea1…`, `bytes 31435`, `lines 1176`, `fetched_utc
2026-11-05T03:49:50Z`, `http.status 200`, `http.final_url` equal to the request
URL. Every manifest quote resolves to the quoted string at its anchor:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-72/manifest.json --source S107
S107:sha256 OK
S107:Q01-scope OK occurrences=1 anchor=33-ok
S107:Q02-token OK occurrences=1 anchor=297-ok
S107:Q03-undocumented OK occurrences=1 anchor=645-ok
S107:Q04-create OK occurrences=1 anchor=648-ok
S107:Q05-endpoint OK occurrences=1 anchor=649-ok
S107:Q06-required OK occurrences=1 anchor=660-ok
S107:Q07-defaulted OK occurrences=1 anchor=666-ok
S107:Q08-groups OK occurrences=1 anchor=726-ok
S107:Q09-groupdefault OK occurrences=1 anchor=731-ok
S107:Q10-assign OK occurrences=1 anchor=715-ok
S107:Q11-newbug OK occurrences=1 anchor=791-ok
S107:Q12-update OK occurrences=1 anchor=797-ok
S107:Q13-cc OK occurrences=1 anchor=881-ok
S107:Q14-comment OK occurrences=1 anchor=886-ok
S107:Q15-reporter OK occurrences=1 anchor=1002-ok
S107:Q16-access OK occurrences=2 anchor=1003-ok
S107:Q17-untracked OK occurrences=1 anchor=1166-ok
(exit=0)
```

I also checked the 24 quote+anchor pairs cited inside the F50 knowledge entry
`corpus/knowledge/bugzilla-rest-api-bug-endpoints.md`: **0 mismatches** — every
quoted string is present in the cited line range of the capture.

Live counters in the lane at the time of reading (the connector seat was editing
the lane concurrently — the manifest's quote set grew from 8 to 17 ids between my
first and second read, and the eight original quotes kept identical text and
anchors under the new ids):

```
$ python3 corpus/instruments/capture-binding-check.py --root .../kasegi-shokunin
MANIFEST round-72 records=1 url_bound=1 fetched=1 archival=0
AUDIT records=86 with_url=86 with_fetched_utc=48 with_archival=38 snapshot_dirs=45 manifest_dirs=45 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=86 bound=86 unbound=0     (exit=0)

$ python3 corpus/instruments/frontier-recheck-count.py
FRONTIER-CENSUS rows=50 admitted=50 closed=50 problem-rows=0 registry=107
FRONTIER-PASS F50 ids=S107
PASS     F50  knowledge/bugzilla-rest-api-bug-endpoints.md ids=S107   exit=0
entries=53 pass=53 exit=0        (exit=0)

$ ls corpus/knowledge/*.md | wc -l                    -> 88
$ wc -l corpus/instruments/knowledge-expected.txt     -> 90
$ grep -vc '^#' corpus/instruments/knowledge-expected.txt -> 88
$ grep -n -i 'bugzilla|F50' corpus/instruments/knowledge-expected.txt
8:corpus/knowledge/bugzilla-rest-api-bug-endpoints.md

$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi  ok  .../kasegi-shokunin/corpus/SOURCES.md      (exit=0)
```

C2 base receipt `.ufo/waves/round-72/controls/c2-base-counters-r72.txt` recorded
`registry=106`, `entries=52`, `records=85 bound=85 unbound=0`, `87 knowledge
files`, `89/87 knowledge-expected`; every one of those counters has moved by
exactly the C2 after-predicate's amount. The one pre-existing anomaly,
`orphans=1 orphan=S040-live.txt`, is **pre-existing at the freeze commit**
(`git ls-tree a34ce4c corpus/source-snapshots/round-26/` contains
`S040-live.txt`) and is unrelated to round 72.

## Coverage finding — two C2 target clauses are not grounded in S107

The frozen C2 target text names "**the api_key** and mandatory-field contract,
**the security-group restriction that keeps a report private**". Measured against
the committed capture:

```
$ grep -ci 'api_key' S107.txt   -> 0
$ grep -ci 'apikey'  S107.txt   -> 0
$ grep -ci 'api key' S107.txt   -> 0
$ grep -ci 'api-key' S107.txt   -> 0
$ grep -ci 'secur'   S107.txt   -> 0
$ grep -ci 'security' S107.txt  -> 0
$ grep -ci 'access group' S107.txt -> 0
```

The capture contains **no api_key clause and no security-group clause at all**;
it does contain the *mandatory-field* mechanism ("Some params must be set, or an
error will be thrown." `S107.txt:660`; the required/defaulted advice at
`S107.txt:666`), and its access sentences are per-field (`groups` at
`S107.txt:726`; "member of the groups the bug is restricted to" at
`S107.txt:238`; CC-list access at `S107.txt:881-883`; reporter access at
`S107.txt:1002-1003`), plus the only token statement, the per-bug `update_token`
(`S107.txt:297-298`), which is a web-form token, not an API credential.

The F50 knowledge entry already states this correctly in its **Limits** section
("an authentication or API-key requirement … is therefore not grounded in S107";
"a security-group rule that keeps a report private … The capture has no sentence
naming security"), so the entry is honest. **But the frozen C2 claim's target
sentence still asserts both clauses.** Two readings, both for the integrator:
(a) the claim wording is aspirational and should be narrowed to what S107 says,
or (b) the claim's stated target must be grounded by an additional source (the
Bugzilla core v1 *General* page is the conventional home of the api_key
parameter — **not fetched here**, outside this item's URL allow-list, so
unmeasured). The C2 *kill_rule* as written turns on quotes being located in the
capture, registry rows, and counters — all of which currently pass — so this is a
wording/grounding precision issue, not an automatic kill.

## Open / unresolved

1. Whether a version-pinned sibling path exists under the same host (so the
   source could be re-verified against an immutable path rather than the
   `latest` alias) — **not measured** (URL allow-list).
2. Whether the frozen C2 target's api_key and security-group clauses are to be
   narrowed or backed by another source — **decision for the integrator**.
3. `corpus/source-snapshots/round-72/` (both `S107.txt` and `manifest.json`) and
   `corpus/knowledge/bugzilla-rest-api-bug-endpoints.md` are still **untracked**
   in the lane at `HEAD=a34ce4c` — the integrator must `git add` them or C2's
   committed surface is not in the commit.

Scratch tree `/fast/scratch/hyaku/kasegi-r72/K72ScoutCapture/` was removed after
these measurements; every digest and quoted line above is reproduced in this
report.
