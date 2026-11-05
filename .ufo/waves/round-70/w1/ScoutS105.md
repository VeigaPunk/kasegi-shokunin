# ScoutS105 — round-70 C2 source-capture verification (S105 / S104)

Seat: ScoutS105 (scout, leaf). Scope: items 1–5 of the seat spec. Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, read-only except this file.
Scratch root `/fast/scratch/hyaku/kasegi-r70/ScoutS105/` (removed on exit).
Tools: no install; host `chromium 155.0.8059.84` (`/usr/bin/chromium`), `node v24.21.0`,
`python3 3.14.8`, `curl` were already present — nothing was installed, nothing upgraded.

## Verdict summary

| # | item | result |
|---|---|---|
| 1 | re-capture S105 vs committed | **PASS — byte-identical**, sha256 `9dd51a8e…e3350` (pinned digest reproduced) |
| 2 | `source-recheck.py --source S105` | **PASS — 19/19 OK, exit 0** (full output below) |
| 3 | manifest quotes ≤25 words, anchor contains quote | **PASS — max 24 words (Q15); every quote sits on its exact anchor line**; one non-manifest misquote found in the knowledge entry (§6) |
| 4 | F48 ground vs F47 (S103) and F36 (S087) | **PASS — genuinely different ground**, one line quoted from each below; both pages re-captured live and byte-identical to committed |
| 5 | EUVD apidoc re-open: S104 byte count + digest | **PASS — 3062 bytes, sha256 `6fb32b61…a38d5`, zero drift**; bundle and rendered text also reproduce the round-69 receipt byte-for-byte |

C2's frozen after-values additionally reproduce from the committed landing bytes (§7).

---

## 1. Re-capture of S105 — no drift

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/capture-source.py \
  --id S105 --url https://docs.github.com/en/code-security/security-advisories/global-security-advisories/about-the-github-advisory-database \
  --out /fast/scratch/hyaku/kasegi-r70/ScoutS105/S105-final.txt --kind html
S105 status=200 fetched_bytes=616388 snapshot_bytes=22791 sha256=9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350 utc=2026-11-05T00:41:18Z
```

```
sha256sum S105-final.txt committed-S105.txt
9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350  S105-final.txt
9dd51a8ebd93268cd5f7a2fa626cfcb73767708df75777726535b28650be3350  committed-S105.txt
diff S105-final.txt committed-S105.txt   # → no output, exit 0
wc -c -l committed-S105.txt  → 656 lines, 22791 bytes
```

* Digest equals the frozen pin (`.ufo/waves/round-70/controls/pins-r70.txt`,
  `9dd51a8e…e3350`) and the manifest `sha256`. **No line differs, so no cited anchor moved.**
* Raw HTML is stable today: three consecutive fetches → `616388` bytes each, raw sha256
  `4d46d23199ae03f90f1dabcf7a8f8df8e048300478dc287508901bfe51b0aa80` (3/3 identical).
* Committed snapshot is byte-identical at every relevant revision
  (`b4afd8a` = `e74ba6b` = `c105174` = worktree; manifest sha `2f8b9844…` at all three).
* The manifest `bytes: 616388` is the **fetched**-HTML size (lane convention, same as
  S102 `11802`, S103 `329039`, S087 `937712`); `lines: 656` is the snapshot line count.
  `S105.txt` itself is 22791 bytes; the knowledge entry and the S105 registry row both
  state "656 lines, 22791 snapshot bytes over 616388 fetched" — consistent.

**Finding 1A (metadata, not content).** The live URL now **301-redirects**:

```
curl -sSI -A "kasegi-shokunin/1.0 …" <the recorded URL>
HTTP/2 301
location: /en/code-security/concepts/vulnerability-reporting-and-management/github-advisory-database
```

The manifest records `http.final_url` = the *pre-redirect* URL, so the recorded
`final_url` is no longer the URL actually served (the new canonical path is).
`capture-binding-check.py` rule E3 still passes (final_url == capture_url == url), and the
**snapshot bytes are identical from both URLs** (re-captured the redirect target:
sha256 `9dd51a8e…e3350`, diff empty). So this is stale URL metadata, not content drift.
Note the lane already carries the newer `…/concepts/vulnerability-reporting-and-management/`
path form for S076, so GitHub has moved these docs paths. No claim in `claims.json`
depends on `final_url`.

## 2. `source-recheck.py --source S105` — every line

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/source-recheck.py \
  --manifest corpus/source-snapshots/round-70/manifest.json --source S105
S105:sha256 OK
S105:Q01-purpose OK occurrences=1 anchor=558-ok
S105:Q02-osv OK occurrences=1 anchor=567-ok
S105:Q03-sources OK occurrences=1 anchor=573-ok
S105:Q04-reviewed-gate OK occurrences=1 anchor=584-ok
S105:Q05-registry-gate OK occurrences=1 anchor=585-ok
S105:Q06-swift OK occurrences=1 anchor=597-ok
S105:Q07-unreviewed-auto OK occurrences=1 anchor=601-ok
S105:Q08-unreviewed-noalert OK occurrences=1 anchor=602-ok
S105:Q09-malware-source OK occurrences=1 anchor=604-ok
S105:Q10-type-malware OK occurrences=1 anchor=606-ok
S105:Q11-substitution OK occurrences=1 anchor=607-ok
S105:Q12-scoped OK occurrences=1 anchor=607-ok
S105:Q13-ghsa-format OK occurrences=1 anchor=612-ok
S105:Q14-cvss-versions OK occurrences=1 anchor=621-ok
S105:Q15-cve-provenance OK occurrences=1 anchor=628-ok
S105:Q16-epss-sync OK occurrences=1 anchor=639-ok
S105:Q17-epss-first OK occurrences=1 anchor=640-ok
S105:Q18-community OK occurrences=1 anchor=642-ok
S105:Q19-credit OK occurrences=1 anchor=643-ok
EXIT=0
```

19 quotes, 19 `OK`, 0 failures, exit 0 — matches the round-70 claim's "19 located quotes".

## 3. Quote lengths and anchor containment (measured, not asserted)

Measured from the committed `corpus/source-snapshots/round-70/manifest.json` against the
committed `S105.txt`:

| quote | words | anchor | quote is ON the anchor line | occurrences in file |
|---|---|---|---|---|
| Q01-purpose | 10 | 558 | yes | 1 |
| Q02-osv | 14 | 567 | yes | 1 |
| Q03-sources | 12 | 573 | yes | 1 |
| Q04-reviewed-gate | 21 | 584 | yes | 1 |
| Q05-registry-gate | 18 | 585 | yes | 1 |
| Q06-swift | 3 | 597 | yes | 1 |
| Q07-unreviewed-auto | 17 | 601 | yes | 1 |
| Q08-unreviewed-noalert | 19 | 602 | yes | 1 |
| Q09-malware-source | 20 | 604 | yes | 1 |
| Q10-type-malware | 14 | 606 | yes | 1 |
| Q11-substitution | 8 | 607 | yes | 1 |
| Q12-scoped | 13 | 607 | yes | 1 |
| Q13-ghsa-format | 9 | 612 | yes | 1 |
| Q14-cvss-versions | 13 | 621 | yes | 1 |
| **Q15-cve-provenance** | **24** | 628 | yes | 1 |
| Q16-epss-sync | 18 | 639 | yes | 1 |
| Q17-epss-first | 12 | 640 | yes | 1 |
| Q18-community | 21 | 642 | yes | 1 |
| Q19-credit | 8 | 643 | yes | 1 |

* **Longest quote: Q15-cve-provenance, 24 words** — "If GitHub obtains a CVE, the GitHub
  Advisory Database uses the CVSS version assigned by the maintainer, which can be version
  3.1 or 4.0." (cross-checked with `wc -w` on the quote alone → 24). Within the ≤25 bound;
  agrees with the registry row's "max 24 words".
* All 19 quotes occur exactly **once** in the snapshot, so each anchor is a *disambiguator*,
  not a locator — see Finding 6A.

## 4. Is F48's ground genuinely different from F47 (S103) and F36 (S087)?

Both comparison pages were re-opened live and re-captured with the lane instrument; both
snapshots are **byte-identical** to the committed ones:

```
capture-source.py --id S103-live --url https://docs.github.com/en/rest/security-advisories/global-advisories
  → sha256 c531c1e9b3eb9b4443e9851edc479e137eff772fb41dca3db16d697ac514344f   (= committed round-69/S103.txt; diff empty)
capture-source.py --id S087-live --url https://docs.github.com/en/rest/security-advisories/repository-advisories
  → sha256 3eebdf476fbfe5040ad3367edfe3961fbda1bff412bb74ee43bb08ab2f754b93   (= committed round-55/S087.txt; diff empty)
```

One line each, showing each page's own subject matter:

* **F47's REST reference (S103)** — `S103.txt:275`:
  > "Lists all global security advisories that match the specified parameters. If no other
  > parameters are defined, the request will return only GitHub-reviewed advisories that are
  > not malware."
* **F36's repository-advisories entry (S087)** — `S087.txt:283`:
  > "Use the REST API to view and manage repository security advisories."

Separation is not merely asserted — it is measurable, by string presence in each committed
snapshot (`0` = absent):

| marker (a curation-semantics marker) | S105 | S103 | S087 |
|---|---|---|---|
| "National Vulnerability Database feed" | 601 | 0 | 0 |
| "OpenSSF Malicious Packages" | 604 | 0 | 0 |
| "GHSA-xxxx-xxxx-xxxx" | 612 | 0 | 0 |
| "supported registry" | 585 | 0 | 0 |
| "source it from FIRST" | 640 | 0 | 0 |
| `credit type of "Analyst"` | 643 | 0 | 0 |
| "Open Source Vulnerability" | 567 | 0 | 0 |
| "CVSS version 4.0" | 621 | 0 | 0 |

and symmetrically, REST-interface markers (`per_page`, `cursor`, `X-GitHub-Api-Version`,
`api.github.com/advisories`) occur in S103 (lines 335/328-330/356/487) and **0 times** in S105.
S105 has 40 "Dependabot" hits and 4 "malware alerts"; S103 has 1 and 0.

The two are also **cross-referenced, not overlapping**: `S103.txt:276` itself defers the
class semantics to the page S105 captures — "For more information about the different types
of security advisories, see \"About the GitHub Advisory database.\"" That is exactly the
"curation semantics F47 left unopened" the F48 row claims. **F48's ground is genuinely
distinct from both neighbours.**

*Side observation (pre-existing, out of C2's scope, one line):* the round-55 manifest records
S087 `bytes: 937712`; today's raw fetch is 937479 bytes (raw digest changed) while the
normalized snapshot still reproduces exactly. So `bytes` (raw fetched size) is not stable
across time for GitHub Docs pages — only the snapshot digest is. S105's raw fetch *is*
stable today (3/3, 616388).

## 5. EUVD apidoc re-opened — S104 row's byte count and digest, no drift

```
curl -sSL -o euvd-apidoc.html https://euvd.enisa.europa.eu/apidoc
http=200 size=3062
sha256 = 6fb32b61a3f44c7aa137699de08cf3a240aab7315f0d68ec7012e69d0a0a38d5
```

Exactly the S104 row's claim ("HTTP 200, 3062 bytes, sha256 `6fb32b61…a38d5`") and exactly
the round-69 receipt's `static_html_bytes=3062 / sha256 6fb32b61…a38d5`. The static body's
"zero occurrences" claim also reproduces: `grep -c endpoint` → 0, `grep -c "/api/"` → 0,
`wc -l` → 0 (single line, no trailing newline).

The two other byte facts in the round-69 receipt also reproduce **byte-for-byte**:

* bundle `/static/js/main.61fcf30f.js` → 544337 bytes, sha256
  `b824a45aae9afea9abbeb402b101e3070b8207a19712f72990259f85b8554ecd` (receipt: same bytes, same digest);
* rendered text (headless Chromium, `document.body.innerText`) → **4216 bytes**, sha256
  `25fd52889d8f0cd812be8d6cbb6c273c35dc23f0daab950f63b3d4d116f8c87c` — the receipt's
  `rendered_text` digest exactly; and the receipt's "rendered first heading: 8:EUVD API
  Documentation" reproduces (line 8 of the re-rendered innerText is exactly that string).

**Finding 5A (receipt method ambiguity, not drift).** The receipt records
`bundle … endpoint_mentions=3`. On the *byte-identical* bundle (same sha256) I measure
`'endpoint'`/`'endpoints'` substring = **5**, `endpoints:[{` groups = **4**, `url:"/api/` = **8**,
distinct `/api/` URLs = **8**, `/api/` = **16**, word-boundary `endpoint` = **0**. The value
**3** is reproducible only by counting `title:"…",endpoints` adjacencies (3 of the 4 groups
carry an explicit `title:` key; the "Query Vulnerabilities with Flexible Filter" group does
not) — an unstated method. The figure is therefore not re-derivable from the receipt text
alone. Nothing in C2's predicate depends on it, and the S104 **row** states the checkable
"zero occurrences in the static body", which does reproduce (0 and 0).

**Flip condition check.** The flip is "a statically served or line-anchorable rendering of
the same API reference appears at this URL or a documented successor". The static body is
byte-identical to round 69 (still an SPA shell, still 0 `endpoint` / 0 `/api/`), so **the
flip has NOT triggered** and the rejection stands as written. (The rendered page does carry
the API documentation — 9 endpoint URLs under `https://euvdservices.enisa.europa.eu` — but
that is JS-rendered text this lane's capture instrument cannot pin to a line, exactly as the
row says.) The static-HTML refusal remains honest.

## 6. Defects found (none of them falsify C2's predicate)

**6A (depth:verifiability, strongest finding) — the 19 anchors are not load-bearing.**
`source-recheck.py` fails an anchor only when the quote is *non-unique* (`B2`: the fatal
branch is `occurrences > 1 and verdict != "ok"`). Every S105 quote occurs exactly once, so a
wholly wrong anchor set still exits 0. Measured on a scratch copy (manifest sha256 re-based
so the digest check passes):

* M4 — every one of the 19 anchors set to line 1:
  `S105:Q01-purpose OK occurrences=1 anchor=1-BROKEN` … ×19, **exit 0**;
* M3 — Q04's quote physically moved 10 lines away: `S105:Q04-reviewed-gate OK occurrences=1
  anchor=584-BROKEN` — note it still prints **OK** and the run exits **0**;
* M2 — inserting 1/2/3 lines ahead of the quoted block still yields `anchor=N-ok` (the
  verdict window is `raw_lines[anchor-1 : anchor+3]`); 4 inserted lines break it.

So the instrument's `anchor=N-ok` note is not a proof that a quote sits at line N for this
source, and the claim "each located at its anchor" is **not enforced by the cited gate**.
I re-derived it independently: all 19 quotes *are* on their exact declared line in the
committed snapshot (19/19, checked line-by-line, not window-wise). The claim is true as
filed; the gate does not carry it. Any future S-record whose quotes are all unique inherits
the same hole.

**6B (depth:verifiability) — a hand-typed word count is off by one and the audit is
blind to it.** `corpus/lessons/round-70.md:78` states the S105 Gate quote is "18 words";
`wc -w` on that exact quoted text → **17** (and the manifest's identical Q07 quote measures
17 as well). This is precisely the R56/M48-3 drift class. It escaped
`gate-quote-audit.py` because that instrument's `ANNOTATION_RE` requires the shape
`<N> words by `wc -w`` — the lesson says only "18 words". Coverage of that shape across the
lesson tree: **13** annotations match "N words by `wc -w`" (the audit sees 9) versus **262**
occurrences of a bare "N words" string, so the audit inspects ~5% of the class it was built
for. (The audit's 2 failures, round-55:46 and round-64:15, are inherited at base `e7c02bd`
— verified by running the instrument on a `git archive e7c02bd` export — not round-70 debt.)

**6C (coverage) — a non-verbatim quoted fragment in the new knowledge entry.**
`corpus/knowledge/github-advisory-database-curation-semantics.md:80` quotes
`"always fully synchronized"` and cites `S105.txt:639`, but line 639 reads
"…will **always be** fully synchronized, score percentiles will only be updated when
significantly different." — the quoted span is not a substring of the anchored line (the
word "be" intervenes). I checked every quoted span in that entry that carries an inline
`S105.txt:N` citation: **17 ok / 1 fail** (this one). The manifest's Q16 quote of the same
sentence is verbatim and correct, so the defect is in the entry, not the manifest. For
comparison the F47 entry is clean (11 ok / 0 fail).

**6D (coverage) — a stale sibling cross-reference left by the round-70 landing.**
The landing updated the F47 row in `corpus/README.md` ("database curation semantics … are
held by F48/S105") but did **not** update the F47 knowledge entry, whose Limits bullet
still reads (corpus/knowledge/github-global-security-advisories-rest-api.md:77):

> "advisories enter are deferred to \"About the GitHub Advisory database\" (`S103.txt:276`),
> **which was not opened**."

That file's digest is unchanged across the whole round (`4624d242…` at `9811156` = `b4afd8a`
= `c105174` = HEAD), so the corpus now simultaneously asserts (README) that the curation
ground is held by F48/S105 and (F47 entry) that the page "was not opened". Under R9 the fix
is an **appended erratum** in the F47 entry, not a rewrite of the filed bullet.

## 7. C2's frozen after-values reproduce from the committed landing bytes

Exported `b4afd8a` read-only (`git archive b4afd8a | tar -x -C <scratch>`) and measured there:

```
FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105
FRONTIER-PASS F48 ids=S105
entries=51 pass=51 exit=0
capture-binding-check: MANIFEST round-70 records=1 url_bound=1 fetched=1 archival=0
                        records=84 bound=84 unbound=0
knowledge-expected.txt: 88 lines / 86 entries ; LC_ALL=C /usr/bin/sort -c → rc 0
corpus/knowledge/*.md: 86 files ; README frontier rows: 48 ; SOURCES rows: 105 (S104 and S105 both present)
sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi → exit 0, six W04 warnings
  (S028, S029, S072, S076, S080, S085 — all inherited, none from round 70)
```

Every value in `claims.json`'s C2 `after_values` reproduces from the landed commit, and the
`capture-binding-check.py` orphan `S040-live.txt` is a pre-existing round-26 file (present at
base `e7c02bd`), not round-70 debt.

## 8. Unresolved / not measured

* `http.final_url` for S105 (Finding 1A) is stale metadata; whether the lane wants the
  canonical `…/concepts/vulnerability-reporting-and-management/github-advisory-database`
  recorded instead is a maintainer decision, not mine to make.
* The round-69 receipt's `endpoint_mentions=3` counting method (Finding 5A) is unrecoverable
  from the receipt text; I could not ask its author (read-only seat).
* I did not evaluate whether the ≤25-word bound or the "19 quotes" count is machine-enforced
  for *other* round-70 records — out of my scope.
