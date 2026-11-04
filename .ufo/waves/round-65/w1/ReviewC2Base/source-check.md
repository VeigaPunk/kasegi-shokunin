# S098 candidate source check — FIRST PSIRT Services Framework v1.1

Seat ReviewC2Base (leaf), round 65 predata. Base commit `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`.
All work done from the export `/fast/scratch/hyaku/kasegi-r65/ReviewC2Base/base`
(`git archive <base> | tar -x`) and the read-only lane root
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`. No production file was edited
(`git status --porcelain` printed the same 5 untracked `.ufo/waves` lines before and
after every run, and `git rev-parse HEAD` still printed the base commit).

Subject: `https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1`
Candidate registry id: **S098** (registry today ends at `S097`; see §7).

---

## 1. Fetch evidence — two independent fetches, byte comparison

Both fetches used the lane's own instrument, the authoritative capture path
(`corpus/instruments/capture-source.py`, `--kind html`, instrument UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`).

```
$ cd /fast/scratch/hyaku/kasegi-r65/ReviewC2Base && URL=https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 && python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S098 --url "$URL" --out cap1/S098.txt --kind html
S098 status=200 fetched_bytes=229255 snapshot_bytes=170137 sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2 utc=2026-11-04T19:26:49Z out=cap1/S098.txt
EXIT1=0
$ sleep 3; python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py --id S098 --url "$URL" --out cap2/S098.txt --kind html
S098 status=200 fetched_bytes=229255 snapshot_bytes=170137 sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2 utc=2026-11-04T19:26:52Z out=cap2/S098.txt
EXIT2=0
```

```
$ sha256sum cap1/S098.txt cap2/S098.txt
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  cap1/S098.txt
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  cap2/S098.txt
$ wc -l cap1/S098.txt cap2/S098.txt
  1573 cap1/S098.txt
  1573 cap2/S098.txt
  3146 total
$ wc -c cap1/S098.txt cap2/S098.txt
170137 cap1/S098.txt
170137 cap2/S098.txt
340274 total
$ cmp cap1/S098.txt cap2/S098.txt && echo "IDENTICAL=yes"
IDENTICAL=yes
```

Raw (pre-transform) bytes, fetched twice with the same UA, `urllib` only:

```
$ python3 - (urllib.request; UA=kasegi-shokunin/1.0 ...)
RAW1 status=200 bytes=229255 sha256=3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11 ctype='text/html; charset=UTF-8' lastmod='Mon, 26 Jan 2026 14:43:46 GMT' etag=None clen='229255'
RAW2 status=200 bytes=229255 sha256=3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11 ctype='text/html; charset=UTF-8' lastmod='Mon, 26 Jan 2026 14:43:46 GMT' etag=None clen='229255'
$ cmp raw1.html raw2.html && echo RAW_IDENTICAL=yes
RAW_IDENTICAL=yes
```

**Measured values**

| item | value |
|---|---|
| HTTP status (both fetches) | 200 |
| raw bytes | 229255 (both fetches) |
| raw sha256 | `3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11` (both) |
| Content-Type | `text/html; charset=UTF-8` |
| Last-Modified | `Mon, 26 Jan 2026 14:43:46 GMT` (server-fixed, same in both) |
| ETag | absent |
| snapshot bytes | 170137 (both) |
| **snapshot sha256 (the digest a manifest record would pin)** | `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2` (both) |
| **parsed text line count** | **1573** (`wc -l`, both) |

Text stability: the two captures are byte-identical (`cmp` → `IDENTICAL=yes`), so the
*bound* artefact — the text snapshot — is stable across the fetch window. Re-measured
separately over a 25 s gap at the raw level:

```
T1 status=200 bytes=229255 sha256=3a1b5c1a... server_date=Wed, 04 Nov 2026 19:29:45 GMT lastmod=Mon, 26 Jan 2026 14:43:46 GMT nonce=1_R9iamV-HfsNu_Eo-Mk2w
T2 status=200 bytes=229255 sha256=3a1b5c1a... server_date=Wed, 04 Nov 2026 19:30:10 GMT lastmod=Mon, 26 Jan 2026 14:43:46 GMT nonce=1_R9iamV-HfsNu_Eo-Mk2w
```

The transform is also deterministic offline (no second fetch involved): re-running the
instrument's own `html_to_text()` on the saved `raw1.html` reproduces the pinned digest.

```
reparse_bytes=170137 lines=1573 sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2
matches_capture=True
```

---

## 2. URL-spelling hazard (measured, not inferred)

The trailing-slash spelling is a *different* URL that the server resolves to a
*different* page path (`v1-1`, hyphen) with different raw bytes but the same text:

```
URL=https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 status=200 final=https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 bytes=229255 sha256=3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11
URL=https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1/ status=200 final=https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1 bytes=229255 sha256=cf58a500607c1387ccf36ee497d2365f1f7d431fd89344bea5bf03d341c89dae
URL=http://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 status=200 final=https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 bytes=229255 sha256=3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11
```

Raw diff of the two HTTPS spellings is two lines — the `og:url` meta and a per-response
script nonce:

```
@@ -5 +5 @@
-<meta property="og:url" content="https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1" />
+<meta property="og:url" content="https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1-1" />
@@ -1704 +1704 @@
-...<script nonce="1_R9iamV-HfsNu_Eo-Mk2w" async="async" src="/_/web.js?20261104132345"></script>...
+...<script nonce="xwyiPBtsTbsiLIsVXltcHw" async="async" src="/_/web.js?20261104132345"></script>...
```

and the text snapshots are identical:

```
S098 status=200 fetched_bytes=229255 snapshot_bytes=170137 sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2 utc=2026-11-04T19:29:35Z out=cap3/S098-v1-1.txt
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  cap1/S098.txt
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  cap3/S098-v1-1.txt
TEXT_IDENTICAL=yes
```

Consequence for binding: `capture-binding-check.py` rule B5 requires the manifest
record's `url` to equal, byte-for-byte, the single `https://` token in the registry row.
The row must therefore carry the **dot** spelling
`.../psirt_services_framework_v1.1` (no trailing slash), and the record's `url` must be
that same string. A trailing-slash row would bind a URL that resolves to `v1-1`; the
snapshot digest would still match, so only the URL-byte equality rule separates them.

---

## 3. Capture method to bind

```
python3 corpus/instruments/capture-source.py \
  --id S098 \
  --url https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1 \
  --out corpus/source-snapshots/round-65/S098.txt --kind html
```

* kind `html` (the page's own body text; the site also links `FIRST_PSIRT_Services_Framework_v1.1.pdf`, which is a *different URL for the same document* — do not add it as a second row or put it in the same source cell, which would trip `double-https-row`).
* manifest record fields that `capture-binding-check.py` reads/prints: `id`, `url` (byte-equal to the row token), `capture_url`, `http.status`, `kind`, `fetch_method`, `fetched_utc`, `path`, `sha256`, `bytes`, `snapshot_bytes`, `lines`.
* values measured above and available for the record:
  `status=200`, `bytes=229255`, `sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`,
  `snapshot_bytes=170137`, `lines=1573`, `last_modified=Mon, 26 Jan 2026 14:43:46 GMT`.
* body scoping for `body_lines`: the document body is L216–L1535
  (`grep -n` measured: H1 `PSIRT Services Framework 1.1` = L1; title repeated in the
  content column = L216; `Also available in PDF.` = L217; `Purpose` = L218; last
  reference URL = L1535; site nav resumes at L1537). Body span = 1320 lines
  (`1535-216+1`).

---

## 4. Risks to record with the binding

1. **Nav/footer boilerplate is byte-identical across FIRST captures.** The nav block is
   the same bytes on every FIRST page, including the published ones:
   ```
   $ for f in round-24/S001.txt round-24/S002.txt round-36/S053.txt cap1/S098.txt; do printf '%s ' "$f"; sed -n '198,206p' "$f" | sha256sum; done
   corpus/source-snapshots/round-24/S001.txt bac145c2bf99e8cf8930f0e7649991dce48001ea76a61c5b5db43e8e9ec30ca4  -
   corpus/source-snapshots/round-24/S002.txt bac145c2bf99e8cf8930f0e7649991dce48001ea76a61c5b5db43e8e9ec30ca4  -
   corpus/source-snapshots/round-36/S053.txt bac145c2bf99e8cf8930f0e7649991dce48001ea76a61c5b5db43e8e9ec30ca4  -
   /fast/scratch/hyaku/kasegi-r65/ReviewC2Base/cap1/S098.txt bac145c2bf99e8cf8930f0e7649991dce48001ea76a61c5b5db43e8e9ec30ca4  -
   ```
   The string `PSIRT Services Framework` appears in the **nav of three other FIRST
   snapshots** (S001 L201, S002 L201, S053 L201 — `grep -rn ... | wc -l` → 3), so a title
   or nav-line anchor does not identify this document. All entry anchors must be taken
   from L216–L1535.
2. **Rolling copyright year.** L1573 is `Copyright © 2015—2026 by Forum of Incident
   Response and Security Teams, Inc. All Rights Reserved.` The year rolls at the next
   site rebuild, so the *snapshot* digest is stable only while the page is unchanged;
   pin the snapshot digest (as the manifest already does) and treat the live page as
   mutable, which is the lane's standing capture contract.
3. **Per-response nonce / `og:url` in raw HTML.** The raw digest is not a content
   digest (nonce and `og:url` vary by URL spelling and rebuild). Bind the text snapshot,
   never raw bytes.
4. **Version family.** The page cross-links `v1.1 HTML` (this page), `v1.1 PDF`,
   `v1.0 HTML`, `v1.0 PDF`, and Arabic/Spanish/French/Japanese `v1.1` PDFs. The URL
   contains the version (`..._v1.1`), so the pin is version-scoped; a future v1.2 would
   be a new URL and must not be silently substituted.
5. **ISO editions the framework cites are superseded, and the lane already holds the
   current editions.** In the capture: `ISO/IEC 30111:2013` at L1444, L1514, L1522,
   L1523 and `ISO/IEC 29147:2014` at L1445, L1513, L1515–L1517. Registry rows S089/S090 record
   `ISO/IEC 29147:2018` (`https://www.iso.org/standard/72311.html`) and
   `ISO/IEC 30111:2019` (`https://www.iso.org/standard/69725.html`). An F44 entry may
   quote the framework's ISO citations only as *the framework's* citations; it must not
   restate them as current ISO editions, or it contradicts F38/S089,S090.
6. **No revision date on the page.** The only date evidence is the `Last-Modified`
   header and the copyright year; the text itself carries no publication or revision
   date, so any dated claim must name the capture instant, not a document date.

---

## 5. Document content and its distinction from F43 / F06 (for the coverage axis)

Measured on the captured snapshot (`cap1/S098.txt`):

```
$ grep -c '^Service Area [0-9]' cap1/S098.txt   ->  6
$ grep -c '^Function ' cap1/S098.txt            ->  84
$ grep -c '^Sub-function ' cap1/S098.txt        ->  81
$ grep -c -iE 'coordinated disclosure' cap1/S098.txt -> 4
```

* Structure is a service taxonomy: `PSIRT Framework Structure` (L226) /
  `SERVICE AREAS – SERVICES – FUNCTIONS – SUB-FUNCTIONS` (L227), with six service areas
  (L402, L674, L843 `Vulnerability Triage and Analysis`, L941 `Remediation`, L1145
  `Vulnerability Disclosure`, L1309 `Training and Education`), 84 functions, 81
  sub-functions.
* It has an explicit PSIRT-vs-CSIRT differentiation section at L243 and PSIRT
  organisational models (`Distributed Model` L249, `Centralized Model` L259) —
  organisational design, not a disclosure process or a role matrix.
* `coordinated disclosure` occurs only 4 times (L477 sub-function title
  `1.2.2.2 Define Coordinated Disclosure Process`, L480 body, L731, L1197), i.e. the
  disclosure process is one sub-function here, not the document's subject.

Distinction from the existing frontier neighbours, from the registry rows themselves:

* **F43 / S095** — CERT/CC adapted CVD phase-to-five-role responsibility matrix
  (`corpus/SOURCES.md:104`: "CERT/CC's adapted phase-to-five-role responsibility matrix,
  especially Reporter fix confirmation versus Vendor/Coordinator incoming-report
  validation"). Its object is *phases × roles*. S098's object is *a PSIRT's own service
  catalogue*, with no phase×role matrix.
* **F06 / S018** — FIRST *multi-party vulnerability coordination* guidelines v1.1
  (`corpus/SOURCES.md:24`), whose object is coordination among multiple parties. S098
  references the same FIRST family but prescribes internal PSIRT capability areas
  (stakeholder management, triage, remediation, disclosure, training).

So the candidate is distinguishable on subject, not merely on publisher, and the
registry row's `scope` cell must say so (the reusable differentiator: *PSIRT service
areas / functions / sub-functions and organisational models*, explicitly not a phase
model and not multi-party coordination practice).

---

## 6. Duplicate checks

```
$ grep -c 'psirt_services_framework' corpus/SOURCES.md            -> 0
$ grep -rin 'psirt services framework' corpus/knowledge/ corpus/SOURCES.md corpus/README.md | wc -l  -> 0
$ grep -oE 'https://www\.first\.org[^ |]*' corpus/SOURCES.md | sort | uniq -c
      1 https://www.first.org/cvss/v4.0/specification-document
      1 https://www.first.org/cvss/v4.0/user-guide
      2 https://www.first.org/epss/
      1 https://www.first.org/global/sigs/vulnerability-coordination/multiparty/guidelines-v1.1
$ grep -rn 'first.org/standards' corpus/SOURCES.md                -> (no output)
```

* **URL duplicate:** none. The registry holds four distinct FIRST URLs (S001, S002,
  S018, S053); this document's path (`/standards/frameworks/psirts/`) appears nowhere in
  the registry, the frontier README, or `corpus/knowledge/`.
* **Title duplicate:** none in the registry or in `corpus/knowledge/`. The only committed
  occurrences of the title string are the three FIRST nav blocks quoted in §4.1, which
  are navigation, not a source.
* **Scope duplicate:** nearest rows are S040 (Cisco's *vendor* PSIRT policy — one
  vendor's disclosure policy) and S095/S018 above; none covers a PSIRT service
  taxonomy. `grep -ril 'psirt' corpus/knowledge/*.md | wc -l` → 4 files, all of which use
  "PSIRT" as an actor in ISO/vendor-policy discussions, not as a service model.
* **Id availability:** registry rows end at `S097` (`grep -oE '^\| S[0-9]{3} ' | sort -u
  | tail -3` → S095, S096, S097), so `S098` is free in the registry. It is **not**
  historically virgin: round-24 wave receipts used `S098` for a different staged source
  (`https://www.055110.com/xs/1/25120.html`, tier C;
  `.ufo/waves/round-24/wave1/ScoutCensus.md:65`, `ScoutMergeOther.md:53`,
  `.ufo/waves/round-28/wave1/ConnStagedCensus.md:131`). That row never reached
  `corpus/SOURCES.md` — `grep -n 'S098' LOG.md SKILL.md SCORECARD.md PROVINCE.md
  corpus/README.md` → no output, and `grep -rn '055110' LOG.md SKILL.md SCORECARD.md
  corpus/` → no output. Reusing the id is correct; the receipt should say the id is
  reused from an unlanded round-24 staging row so a later reader grepping `.ufo/waves`
  is not surprised by two different S098s.

---

## 7. Verdict for the C2 screen

The candidate is capturable, stable under the lane's own method, digest-pinned, and
distinct from F43 and F06 on the source's own text. Two binding requirements must be
honoured or the capture-binding counter will fail or silently mis-bind:

1. registry row must carry exactly one `https://` token and it must be the **dot**
   spelling `.../psirt_services_framework_v1.1` (no trailing slash) — rule B5 compares
   the record `url` byte-for-byte;
2. anchors must be taken from L216–L1535; L1–L215 and L1537–L1573 are FIRST site chrome
   that is byte-identical on three already-published captures.

Residual risk that cannot be closed from here: the page can be rebuilt at any time
(it carries a rolling year and a per-request nonce), so the only honest claim is
"snapshot `cfa42e23…` captured 2026-11-04T19:26:49Z", not "the page says X today".

---

## 8. Live addendum — a sibling seat captured S098 into the lane while I measured

After my base measurement, `corpus/source-snapshots/round-65/` appeared in the lane
(another seat's work, not mine; `git status --porcelain` then showed
`?? corpus/source-snapshots/round-65/`). I did not write it; I read it only. Its
`S098.txt` is byte-identical to my independent capture:

```
$ cmp corpus/source-snapshots/round-65/S098.txt /fast/scratch/hyaku/kasegi-r65/ReviewC2Base/cap1/S098.txt && echo CMP_WITH_MY_CAPTURE=identical
CMP_WITH_MY_CAPTURE=identical
$ sha256sum corpus/source-snapshots/round-65/S098.txt
cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2  corpus/source-snapshots/round-65/S098.txt
```

Two independent capture runs (the sibling's at `2026-11-04T19:26:27Z`, mine at
`19:26:49Z`) produced the same pinned digest — the stability claim in §1 is therefore
corroborated by a second runner, not just by my own repeat.

At that moment the registry row did **not** exist yet, and the counter says so:

```
$ python3 corpus/instruments/capture-binding-check.py
MANIFEST round-65 records=1 url_bound=0 fetched=1 archival=0
AUDIT records=79 with_url=79 with_fetched_utc=41 with_archival=38 snapshot_dirs=39 manifest_dirs=39 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
FAIL rule=no-row record=S098 dir=round-65
records=79 bound=78 unbound=1
[exit=1]
$ grep -c '^| S098 ' corpus/SOURCES.md
0
```

**Landing order matters and is measurable:** the manifest must not be committed before
its `corpus/SOURCES.md` row (rule B1 `no-row`), and the row must carry the dot-spelling
URL (rule B5) or the record becomes `unbound`. Base was `records=78 bound=78 unbound=0
exit=0`; the live tree is `records=79 bound=78 unbound=1 exit=1` until the row lands.

