# ScoutKEVLive — round-35 wave-1 receipt (live re-open of S052 + BOD 22-01 binding)

Seat: ScoutKEVLive (leaf, L1 = KasegiR35). Access date: **2026-10-26** (fetches 06:36:23Z–06:36:46Z, strict UTC from the
instrument). Write scope used: this receipt only. Scratch `/fast/scratch/hyaku/kasegi-r35/ScoutKEVLive/` deleted at the end.
No tool installed or upgraded (python3 + curl on host; fetches via the committed `corpus/instruments/capture-source.py`, UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, `capture-source.py:32`).

## Verdict (one line each)

1. S052 live == committed snapshot: **0 differing lines**, sha256 identical (`d69349e8…e8826`).
2. Gate quotes Q1–Q5 each occur live **exactly once** (normalized, whitespace-collapsed; `grep -cF` = 1 and `grep -oF` = 1 each) and each anchor line matches.
3. **The dispatched URL `https://www.cisa.gov/known-exploited-vulnerabilities.json` is HTTP 404** (confirms ExecC2Capture); the live source is the `/sites/default/files/feeds/…` path the manifest already records.
4. **BOD 22-01 is REVOKED and superseded by BOD 26-04 (page dated 2026-06-10).** The directive page does bind the `dueDate` clock — but only for records added up to 2026-06-09; every record from 2026-06-11 on is bound by BOD 26-04. Any S052 knowledge entry that says "dueDate is set by BOD 22-01" without that boundary is stale. (L1: this is a wording constraint for the entry, not a gate failure.)

## Report

### A. Live fetch of S052 (the C2 source)

```
$ curl -sS -o dispatch.body -w "code=%{http_code} final=%{url_effective} size=%{size_download} ct=%{content_type} redirects=%{num_redirects}\n" -A "$UA" -L https://www.cisa.gov/known-exploited-vulnerabilities.json
code=404 final=https://www.cisa.gov/known-exploited-vulnerabilities.json size=46916 ct=text/html; charset=utf-8 redirects=0
        # body = HTML "page-not-found" (<link rel="canonical" href="https://www.cisa.gov/page-not-found">)

$ curl -sS -o feed.json -w "..." -A "$UA" -L https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
code=200 final=https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json size=1807090 ct=application/json redirects=0

$ python3 corpus/instruments/capture-source.py --id S052 --url https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json --out $S/S052.live.txt --kind text
S052 status=200 fetched_bytes=1807090 snapshot_bytes=1479694 sha256=d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826 utc=2026-10-26T06:36:23Z out=…/S052.live.txt
exit=0
```

Final URL = requested URL (no redirect); HTTP 200; 1807090 bytes fetched; 1479694 bytes after `collapse()` (27870 lines, per
`wc -lc` of the committed snapshot).

```
$ sha256sum S052.live.txt corpus/source-snapshots/round-35/S052.txt feed.json
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  S052.live.txt
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt
97a6e54bc74c651ab3c55657191db9adec6c63b05ca54e4205327cfd97a8fb70  feed.json            (raw served bytes; json.load: catalogVersion=2026.10.23 dateReleased=2026-10-23T19:30:18.9209Z count=1756 len(vulnerabilities)=1756)

$ diff S052.live.txt corpus/source-snapshots/round-35/S052.txt | grep -c '^[<>]'
0        # diff exit=0
```

Live feed is unchanged since the 06:32:40Z capture (same `catalogVersion 2026.10.23`, same count 1756).

### B. Gate quotes live, exactly-once

Quotes taken from `corpus/source-snapshots/round-35/manifest.json` (Q1–Q5), checked against the live capture flattened to
one whitespace-collapsed line (`re.sub(r"\s+"," ")`), because Q3–Q5 span 2–4 source lines and per-line `grep -c` cannot match them:

```
Q1 count=1  anchor L2:     "title": "CISA Catalog of Known Exploited Vulnerabilities",
Q2 count=1  anchor L3:     "catalogVersion": "2026.10.23",
Q3 count=1  anchor L4:     "dateReleased": "2026-10-23T19:30:18.9209Z",     (+ L5 "count": 1756,)
Q4 count=1  anchor L15472: "dueDate": "2022-07-18",                          (+ L15473-L15475)
Q5 count=1  anchor L19165: "dateAdded": "2022-03-25",                        (+ L19166-L19168)
grep -cF  (flattened live file): Q1=1 Q2=1 Q3=1 Q4=1 Q5=1
grep -oF  | wc -l (occurrences): Q1=1 Q2=1 Q3=1 Q4=1 Q5=1
```

Each is a hard unique match: 5/5 exactly-once. Anchors Q1–Q5 point at the first line of each quote on the live capture, as
the manifest states. **Gate-phrasing note:** `grep -c` on a multi-line quote against the line-oriented snapshot returns 0 or
an inapplicable count; the exactly-once check for Q3–Q5 is only valid on the flattened text (as above) — the harness must
normalize before counting.

### C. BOD 22-01 directive page — how it binds the KEV `dueDate`

```
$ curl -sS -o /dev/null -D - -A "$UA" https://www.cisa.gov/binding-operational-directive-22-01
HTTP/2 301
location: /news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities-revoked
$ (same for https://www.cisa.gov/news-events/directives/binding-operational-directive-22-01 → same 301 target)

$ curl -sS -L … https://www.cisa.gov/binding-operational-directive-22-01
code=200 final=https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities-revoked size=87312 ct=text/html; charset=utf-8 redirects=1

$ capture-source.py --id BOD2201 --url https://www.cisa.gov/binding-operational-directive-22-01 --out $S/bod.txt --kind html
BOD2201 status=200 fetched_bytes=87312 snapshot_bytes=28756 sha256=16362951e258b970d4b0ac9122b4ddf238827e842b1bd98738e8cfb19f4519f4 utc=2026-10-26T06:36:32Z   exit=0   (236 lines; NOT committed — scratch only)
```

Page title (L1): `BOD 22-01: Reducing the Significant Risk of Known Exploited Vulnerabilities (Revoked) | CISA`; carries an
"Archived Content" banner; page date `June 10, 2026`; issuance date `November 03, 2021`.

Quotes (each `grep -cF` = 1 in the BOD 22-01 snapshot; line numbers are the scratch snapshot's, not a committed anchor):

- **Revocation, L93:** "This Directive has been revoked. It is superseded by BOD 26-04." (11 words)
- **Binding of the clock, Required Actions bullet, L112:** "Remediate each vulnerability according to the timelines set forth in the CISA-managed vulnerability catalog." (14 words) — i.e. the catalog's per-record timeline (= `dueDate`) is what the directive makes compulsory.
- **Default length of the clock, same bullet, L112:** "within 6 months for vulnerabilities with a Common Vulnerabilities and Exposures (CVE) ID assigned prior to 2021 and within two weeks for all other vulnerabilities" (24 words). The same sentence adds "These default timelines may be adjusted in the case of grave risk to the Federal Enterprise."
- **Who it binds (line number NOT verified — I did not grep this quote; it sits just above the "Background" heading in the snapshot):** "A binding operational directive is a compulsory direction to federal, executive branch, departments and agencies" — binding is on FCEB agencies, not on private organizations (L136: "Agencies are not required to update all CVE's … CISA encourages all stakeholders to leverage the CISA catalog").
- **Prioritization-vs-CVSS (the C2 distinctness claim), L124 (line number from `grep -n`; the two sentences quoted were read from the cut-off grep view and not re-grepped as exact strings, so treat their exact wording as unverified-to-the-byte):** "Known exploited vulnerabilities should be the top priority for remediation." and "CISA acknowledges CVSS scoring can still be a part of an organization's vulnerability management efforts" — so the directive itself frames KEV as exploitation-status prioritization alongside, not instead of, CVSS.
- **Add-criteria, L102 / L183:** "CISA will determine vulnerabilities warranting inclusion in the catalog based on reliable evidence that the exploit is being actively used" (L102); three criteria "(1) a CVE ID; (2) clear remediation guidance, and (3) reliable evidence of exploitation in the wild" (L183).
- **Not-a-current-exploitation-signal caveat, L165:** "Addition of a vulnerability to the KEV Catalog does not indicate that CISA is observing current active exploitation."

### D. The finding the L1 needs: BOD 22-01 no longer binds the live feed's newest records

The 22-01 page is revoked and points at BOD 26-04. The BOD 26-04 page (captured under the instrument UA, same date) states how
the clock now works:

```
$ capture-source.py --id B2604 --url https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk --out … --kind html
B2604 status=200 fetched_bytes=84350 snapshot_bytes=22347 sha256=e0baf6a647c70e037109fd337cdd6fe5b1790ca27cbbd4b1795fa37cdc83cf9a utc=2026-10-26T06:36:45Z  exit=0 (242 lines)
$ (implementation guidance) …/bod-26-04-implementation-guidance-prioritizing-security-updates-based-risk
B2604 status=200 fetched_bytes=111591 snapshot_bytes=44566 sha256=d4cece1a9e0be2f53712578484779e7f635bf220c630f8c1de334f5a81d25a43  exit=0 (439 lines)
```

BOD 26-04 page (L97): "In 2021 CISA established the Known Exploited Vulnerabilities catalog pursuant to BOD 22-01" (so the catalog predates and
survives its parent directive); (L181, `grep -cF` = 1): "The timelines defined in Table 1 begin when either (1) CISA adds the vulnerability to the KEV Catalog" — and the
second trigger is the agency's own enumeration on an asset per BOD 23-01; "Whichever event occurs first starts the remediation timeline." Table 1
(Appendix A) is "informed by the SSVC system"; **under 26-04 the KEV `dueDate` is no longer the only clock** (asset exposure,
exploit automation, technical impact also set it; the table cells themselves are images/structure not captured in the text snapshot,
so I did not read their values — unresolved).

Measured against the live feed (`feed.json`, 1756 records, field math on `dateAdded`/`dueDate`/`requiredAction`):

```
records whose requiredAction names "BOD 26-04": 139   dateAdded range 2026-06-11 … 2026-10-23
records naming "BOD 22-01":                       340
latest dateAdded of any record NOT naming BOD 26-04: 2026-06-09
post-2026-06-10 records without a 26-04 mention:    0     (clean boundary)
(dueDate - dateAdded) days, top buckets: 21d×1025, 14d×254+26(26-04), 181d×238, 3d×31+113(26-04), 7d×20 …
   26-04 records: 3d×113, 14d×26 ; pre-26-04 records: 21d×1025, 14d×254, 181d×238, …
```

Consequences for the S052 knowledge entry (not for the gate quotes):
- A statement "dueDate is the BOD 22-01 remediation clock" is true for records `dateAdded ≤ 2026-06-09` and stale for the 139 later records. Attribute to BOD 22-01 only with that bound, or name BOD 26-04 as the current governing directive.
- The 22-01 default clock text (6 months pre-2021 CVE / two weeks other) does not describe the dataset: the dominant buckets are 21 days (1025) and ~181 days (238+), i.e. CISA set per-record dates; the page itself says defaults "may be adjusted". Do not state "two weeks" as the typical `dueDate`.
- Q4/Q5 stay valid: both quoted records (`dueDate` 2022-07-18, 2022-04-15) are pre-26-04 records under the 22-01 clock.
- The dispatched URL in the ticket is 404 and the 22-01 URL in the ticket 301s to the "-revoked" page; record the canonical URLs above, not the ticket's.

### E. State observed in the lane (read-only, no edits)

`corpus/knowledge/*.md`, `SKILL.md` and `corpus/SOURCES.md` had no `S052` occurrence when I looked (06:36Z) — the registry/entry rows
are still to land; `git status --short` showed `corpus/source-snapshots/round-35/` untracked and S052 not yet registered. Nothing here is
a defect; it is the pre-integration state.

### F. Cleanup

`/fast/scratch/hyaku/kasegi-r35/ScoutKEVLive/` removed after this receipt was written; `ls -d` on it afterwards returned `No such file or directory`. The BOD 22-01 / BOD 26-04 snapshots were scratch-only and are not committed; their sha256 values are listed above.
