# ScoutSources — round 90, wave 1

Scope: (1) re-open live S131 and S132 through the landed `capture-source.py`, compare with
`corpus/source-snapshots/round-90/manifest.json`, check both manifest quotes at their anchors, and
re-check S132's rejection reason against the live page; (2) open three round-91 leads and propose
SOURCES rows. Nothing in the lane tree was edited; all captures and fixtures lived in
`/fast/scratch/hyaku/kasegi-r90/ScoutSources`, which is **deleted** (the L1 scans every wave file with
`capture-secret-scan` before committing — this seat's three receipt files scan clean:
`CAPTURE-SECRET-SCAN mode=files scanned=3 hits=0 files=0 allowed=0 unused_allow=19 rc=0`).

Receipts: `.ufo/waves/round-90/w1/ScoutSources-receipts/s131-s132-recheck.txt`,
`…/gate-behaviour.txt`, `…/round91-leads.txt`.

Axis note. This seat was asked to work on `depth:verifiability` and `coverage`. Everything below is a
finding routed to the L1; no claim is re-scored here.

---

## 1. S131 — live re-open: manifest, digest and both quotes hold

| check | result |
|---|---|
| live capture through the **landed** instrument (gate active) | HTTP 200, fetched 637119 B, snapshot 20549 B, **sha256 `0c98d69a14b33d3995f0d7748112f191dcac391157a6cb093054c346ff71fcc9`**, exit 0 |
| manifest `sha256` for S131 | identical |
| committed `corpus/source-snapshots/round-90/S131.txt` | identical; `cmp` live vs committed → byte-identical (647 lines both) |
| `source-recheck.py --manifest corpus/source-snapshots/round-90/manifest.json` | exit 0 — `sha256 OK`, `Q01-block-before OK occurrences=1 anchor=570-ok`, `Q02-bypass-reason OK occurrences=1 anchor=610-ok` |
| quotes re-read at the anchors in the live snapshot | line 570 and line 610 each carry their quote verbatim, each occurring exactly once |

Two further checks the frozen predicate does not name, run because they cost nothing and bound the
claim's reach:

* **The pre-landing (base) instrument reproduces the same bytes.** `git show 6088c3eb:corpus/instruments/capture-source.py`
  re-captures S131 to the same sha256, byte-identical to the committed snapshot. The landed gate
  therefore changes nothing for a clean capture — independent corroboration of counter limb **G3** on a
  real first-party page, not only on the counter's own fixtures.
* **The manifest's "default UA" wording is not load-bearing.** Fetching S131 with urllib's stock UA and
  with the instrument UA yields the same 637119/20549/0c98d69a… triple. (The manifest note says the
  capture used the *pre-landing* instrument with the *default* UA; both readings land on the same bytes
  today, so the note is safe as written.)

**Finding S131-A (routed, no action needed for the claim):** nothing. S131 is fully re-verifiable from
the live page, the committed snapshot and the manifest, all three agreeing byte-for-byte.

## 2. S132 — the rejection reason holds against the live page

Re-captured (HTTP 200, 65723 B fetched, 16022 B snapshot, sha256 `78fe974000e435e06419e62e28b1f687156c7300d4aeb23bb9608866db86452d`,
335 lines). The S132 row's rejection rests on GitLab's *skip* conditions, and the live page carries them:

* line 90 — the blocking statement the row cites.
* lines 169–173 — skip conditions: too many changed paths / too many lines / scan timeout (GitLab
  **accepts** the push) / ruleset parse or compile error / invalid input.
* the row's own quoted sentence, at line 169, is verbatim in the live capture.

The rejection reason ("a fail-open path the intake gate refuses by design") is confirmed: the gate
fails closed where GitLab fails open. See §4 for the one discrepancy in the recorded word count.

**Finding S132-A (routed qualifier, one-line lesson erratum, not a claim defect).** Two mismatches
between the filed text and the live page, both about *where* the evidence sits rather than whether it
holds:

1. `corpus/SOURCES.md:144` cites the anchor as "scratch capture lines 90 and 168-173". On the live
   capture the skip-condition list runs 169–174, and **line 176 carries the numeric threshold**
   ("skipped when a push changes more than 3,150 paths or 350,000 lines") — the one concrete number the
   page gives. The cited range 168-173 excludes it and includes 168, which is the *blocking* audit event,
   not a skip condition. The range should read 90 and 169-176.
2. `corpus/lessons/round-90.md` records the line-169 quote as **12 words**; it is **13** by whitespace
   split. Still ≤25 words, so Q3 is met; the count is simply wrong.

Both live inside a `rejected` row whose `scope`/`anchor`/`teaches` cells are immutable under CORPUS
rule 2 (append-only; only `status`, `recheck`, `used-by` change in place). Per R8/R9 the correction
belongs in the round-91 lesson as an appended erratum, **not** as an in-place edit and **not** as a new
duplicate row. Routed to the L1 for the round-91 lesson.

**Finding S132-B (routed, informational).** S132's rejection cites a *scratch* capture that was never
committed ("not committed" in the anchor cell), so the rejected row is the one row in this round whose
evidence a reader cannot re-derive from the tree. The live page is stable and the sha256 above lets a
reader re-derive it, but the row itself carries no digest. Optional for round 91: record the digest in
the lesson so the rejected row's evidence is pinned.

## 3. What the landed intake gate actually does (observed, not asserted)

All observed through the landed instrument at HEAD `779062a` (sha256 `0630d32b…`, identical to the
frozen candidate). Full transcript: `ScoutSources-receipts/gate-behaviour.txt`.

| behaviour | observation |
|---|---|
| clean capture | passes, exit 0, byte-identical to the base instrument's output (§1) |
| credential-shaped bytes in a capture | `INTAKE-REFUSED <id> shape=private-key line=596 out=<path> written=no`, exit 3, **no file created** — shape and line only, no value on stdout |
| refusal with an existing file at `--out` | the existing file stays **byte-identical** (sha256 before == after) |
| scanner cannot be loaded (import raises) | `INTAKE-REFUSED … shape=gate-error:ImportError line=0 … written=no`, exit 3, nothing written → **fail closed** |
| allowlist row with the **correct** digest of the matched bytes | capture proceeds, exit 0, snapshot sha256 `77f388961f48b660e374701cd7667931f592bbfe215c7071c109d333cfda06eb` |
| allowlist row with a **wrong** digest | refused, exit 3 → the allowlist is digest-bound, not path-only |
| committed S131 snapshot re-scanned | `hits=0 rc=0`, reproducing the frozen control `controls/capture-scan-r90.txt` exactly |

**Finding GATE-A (routed, round-91 instrument work — outside this round's P3 scope, not a claim defect).**
The gate refuses a first-party documentation page whose text quotes a credential *shape* as an example.
GitHub's own "Supported secret scanning patterns" page is refused (`shape=private-key line=596`) because
the generic-private-key pattern description contains a PEM header as an example. Opening such a page
needs a one-row `--allow` file whose sha256 column is the digest of the matched bytes. The lane's default
allowlist has 19 rows and none for this page. This is the intended fail-closed behaviour plus the
documented bypass, so it does **not** touch the C2 predicate — but a round that wants to mine that page
must ship the allowlist row with the page, or the page stays unminable.

**Finding GATE-B (routed, round-91 instrument work).** Two capture-side defects observed while opening
the leads; neither affects the landed claim, both are cheap:

1. `capture-source.py` lets an HTTP error escape as a **traceback** (`urllib.error.HTTPError: HTTP Error
   404`, exit 1) instead of a short refusal line. The lane already recorded the sibling defect class in
   round 90 (M90-2: `file://` responses carry `status=None` → the instrument's `%d` print raises *after*
   the file is written); both are "the instrument's error path is a traceback rather than a refusal".
2. A **moved** AWS doc URL captures **successfully** as an 18-byte title-only snapshot
   (`fetched_bytes=2410 snapshot_bytes=18 sha256=5f741c4a…`, exit 0). The manifest digest then pins an
   18-byte title instead of the document, and nothing in the pipeline notices. A one-line emptiness check
   (refuse a snapshot below a floor, or flag it) would close it.

**Finding GATE-C (routed, informational).** The scanner's documented known limits are unchanged by the
C2 landing, and the gate inherits them exactly: bare provider-prefixed tokens are **not** detected
without a key name in front of them; the Azure SAS with the documented 7-letter parameter is not
detected; a CloudFront signature delivered as a cookie is not detected; gzip/UTF-16/base64-wrapped and
soft-wrapped values are not detected. The intake gate is therefore a *fail-closed wrapper around a
detector with known blind spots*, and a capture whose secret is in one of those shapes passes the gate.
Wording for the round-91 lesson.

## 4. Round-91 leads — opened, quoted, digested

All three opened with the lane's own instrument (so the C2 gate ran on each); access date **2026-11-07**.
Full receipts: `ScoutSources-receipts/round91-leads.txt`.

### Lead 1 — Microsoft Learn, *Create a user delegation SAS* (the `skdutid` parameter)

URL <https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas>
HTTP 200 · fetched 118382 B · snapshot 60089 B · **sha256 `56d858ac8c2988fdf95a045b5a75f13cc5a28a1f71b3786638522775b1786cd6`** · 954 lines.

* line 177 — the parameter token on its own, in the SAS-parameter table
* line 566 — prose: when the field is required
* line 571 — prose: version support
* Quote (line 571, 12 words): *"The sduoid and skdutid fields are supported with version 2025-07-05 and later."*
* Quote (line 177): *"skdutid"*

**Lead 1 caveat that matters for any new row.** Round-89's `ReviewWindow` cited the same URL with a
*different normalisation* (its own text sha256 `184d191b…`, doc lines 1472-1483 / 3471 / 3513). Under
`capture-source.py`'s normalisation the same facts sit at **177** and **566-571**. Line numbers do not
port between the two normalisers. A round-91 row must anchor to a `capture-source.py` snapshot and pin
its digest, or the anchor will not re-derive.

Measured on the landed scanner: a SAS carrying this 7-letter parameter between `sv=` and `sig=` is
**not** detected; the same URL without it is. Recounting the documented Azure SAS parameter tokens from
this capture gives 35, of which exactly one (`skdutid`) falls outside the scanner's `[A-Za-z]{2,6}`
parameter-name class. This is the round-91 C2 work item the round-90 claims file already routed.

### Lead 2 — GitHub Docs, *Supported secret scanning patterns*

URL <https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns>
HTTP 200 · fetched 827097 B · snapshot 19263 B · **sha256 `77f388961f48b660e374701cd7667931f592bbfe215c7071c109d333cfda06eb`** · 688 lines.
*(Gate refuses this page by default — Finding GATE-A. Captured in scratch with a one-row, digest-bound
`--allow` file.)*

* line 582 — pattern-category table, provider row
* line 587 — table caption, push-protection column
* line 614 — the sentence introducing the pattern table
* line 616 — the push-protection scope rule
* line 624 — table header row
* line 675 — pagination marker
* Quote (line 616, 16 words): *"Push protection only supports the most recent token versions that secret scanning can identify with confidence."*
* Quote (line 614, 12 words): *"Use the table below to search, filter, and browse all supported patterns."*

**Which token shapes push protection covers that `capture-secret-scan` lacks** — the question this lead
was opened to answer, answered with two measurements:

1. **The page's own table is client-paginated.** The snapshot holds only the first alphabetical slice
   of providers (1Password … Apify, 25 pattern rows) plus the marker `Previous123456…22Next` at line
   675 — the full set is 22 pages. The complete set lives in the page's embedded JSON payload
   (**531** entries across **207** providers), which the instrument's HTML conversion strips, so it is
   **not** in the snapshot. Counting `hasPushProtection: true` over that embedded payload gives
   **465 of 531** patterns push-protected, per-pattern and per-provider. A round-91 row that anchors to
   the *snapshot* can cite the rule at line 616 and the categories at 582/587, but **not** the 465/531
   count — that number is only re-derivable from the raw HTML, and a snapshot-anchored row must say so.
2. **The scanner detects no provider-prefixed token on its own.** Bare values shaped `ghp_`, `gho_`,
   `github_pat_`, `npm_`, `xoxb-`, `sk-ant-api03-`, `sk-proj-`, `dd_api_`, `sk_live_` produce **no hit**;
   each is caught only when a key name (`token=`, `api_key=`, `secret=`) precedes it, via the generic
   `credential` shape. Push protection matches those prefixes directly, and by partner rule. Line 616
   also bounds push protection to the *most recent* token versions, so any prefix rule taken from this
   page is version-sensitive and must carry that qualifier.

### Lead 3 — Amazon CloudFront Developer Guide, *Setting signed cookies with a custom policy*

URL <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-custom-policy.html>
HTTP 200 · fetched 51673 B · snapshot 21243 B · **sha256 `ddf45b805c7f67f29cf15f60f805fd636968f14734f4e342c697760f8b49f1cc`** · 441 lines.

* line 19 — the two cookie names
* line 40 — what the signature cookie holds
* line 96 — the cookie-parameter table
* Quote (line 40, 8 words): *"CloudFront-Signature=hashed and signed version of the policy statement;"*
* Quote (line 19, 3 words): *"CloudFront-Signature, and CloudFront-Key-Pair-Id."*

**Why this is the right third lead.** The scanner's own docstring lists *"CloudFront signed cookies
(`CloudFront-Signature`)"* as a known limit, and this is the first-party document that defines the
cookie-borne form — so it converts a stated limit into a sourceable one. Measured on the landed scanner:
a `Set-Cookie` header carrying that signature is **not** detected, and the same value in a signed-URL
query is **not** detected either at 32 characters (the cloudfront shape needs 40+ characters *and* a
`Key-Pair-Id` parameter in the same query). A GCS V2 signed-URL page was opened as the runner-up
(`cloud.google.com/storage/docs/access-control/signed-urls-v2`, sha256 `517f22a3…`, 262 lines; names
`GoogleAccessId` at line 159) and set aside: the scanner already lists that GCS V2 shape as a known
limit, so it would restate a limit rather than open ground, and the page carries no example of the query
form to quote.

## 5. Proposed SOURCES rows (11 columns, `corpus/SOURCES.md` header)

**Not applied** — `corpus/SOURCES.md` is not edited by this seat; the L1 integrates. Next free ids are
**S133, S134, S135** (registry currently ends at S132). Each row is quoted from a capture made by the
lane's instrument on 2026-11-07; each carries its capture digest so the anchor re-derives. Status is
`queued` at the freeze and becomes `mined` only if a path cites it (CORPUS rule 2).

```
| S133 | Microsoft Learn, Create a user delegation SAS — https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas | docs | A | Microsoft's own definition of the user-delegation SAS parameter set (skdutid, sduoid) and the version that supports them; Azure user-delegation SAS only, not service or account SAS | SAS-parameter table line 177 and delegated-user prose lines 566-571, capture corpus/source-snapshots/round-91/S133.txt sha256 56d858ac…cd6 (954 lines) | A documented Azure SAS parameter name can be seven letters, so a matcher's parameter-name class must be derived from the documented parameter list, not assumed from the short names | queued | 2026-11-07 | 180d | — |

| S134 | GitHub Docs, Supported secret scanning patterns — https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns | docs | A | GitHub's own catalogue of provider secret patterns and the rule bounding push protection to the most recent token versions; the rendered pattern table is client-paginated and the full pattern set is embedded page JSON, so a snapshot anchors the rule and the categories, not the pattern count | push-protection scope rule line 616, pattern-category table lines 582 and 587, pagination marker line 675, capture corpus/source-snapshots/round-91/S134.txt sha256 77f38896…06eb (688 lines; capture requires a one-row digest-bound allowlist entry, the page quotes a PEM header as a pattern example) | Push protection matches a provider token by prefix and partner rule, so a detector that only recognises one provider's key-id prefix misses those tokens; the scope rule also makes any prefix rule version-sensitive | queued | 2026-11-07 | 180d | — |

| S135 | Amazon CloudFront Developer Guide, Setting signed cookies with a custom policy — https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-custom-policy.html | docs | A | AWS's own definition of the CloudFront-Signature and CloudFront-Key-Pair-Id cookies carrying a signed policy; signed cookies only, not the signed-URL forms of S128 and S130 | cookie-parameter table line 96, cookie names line 19, signature-cookie definition line 40, capture corpus/source-snapshots/round-91/S135.txt sha256 ddf45b80…f1cc (441 lines) | The same cloud signature travels as a cookie header value as well as a URL query parameter, so a detector that reads only query strings misses the cookie-borne form | queued | 2026-11-07 | 180d | — |
```

Notes on the three rows:

* All three are `docs`, tier **A** (first-party vendor documentation for their own scope), `recheck 180d`,
  `used-by —` at `queued`.
* S134 and S135 would be **new** ids, not corrections: S128/S130 cover CloudFront *signed URLs*; the
  cookie form is a different document and a different shape. S129 (GCS V2) stays rejected — its rejection
  is not disturbed by anything here.
* S133 is the first-party backing for the Azure `skdutid` gap the round-89 `ReviewWindow` seat found and
  the round-90 claims file routed to round 91. It is **not** a correction of S127 (that row is the
  *service* SAS document; the user-delegation document is a different source).
* If the L1 prefers one row rather than three, S133 is the load-bearing one: it is the source for a
  routed, reproducible gap.

## 6. Summary for the L1

| # | finding | severity | where it lands |
|---|---|---|---|
| S131-A | S131 fully re-verified: live == manifest == committed, both quotes at anchors, `source-recheck` exit 0 | none — claim holds | note in the round-91 lesson's verification paragraph |
| S132-A | S132 anchor range should read 90 and 169-176 (the numeric threshold is on 176 and is currently outside the cited range); the filed word count says 12, the quote is 13 | qualifier | round-91 lesson erratum (R8/R9 — not an in-place SOURCES edit) |
| S132-B | S132's evidence is an uncommitted scratch capture with no digest in the row | minor | optional digest in the round-91 lesson |
| GATE-A | the gate refuses a first-party doc page that quotes a credential *shape* as an example; mining it needs a shipped digest-bound allowlist row | minor, expected behaviour | round-91 instrument/allowlist work |
| GATE-B | (1) HTTP errors escape as tracebacks, not refusals; (2) a moved doc URL captures as an 18-byte title-only snapshot and the manifest pins that | minor, real | round-91 instrument work (the sibling of M90-2) |
| GATE-C | the gate is fail-closed around a detector with unchanged known blind spots (bare provider tokens, `skdutid`, cookie-borne CloudFront signatures, wrapped/encoded values) | qualifier | wording in the round-91 lesson |
| L1-L3 | three round-91 leads opened and quoted; proposed S133/S134/S135 rows above | — | L1 integrates the rows it accepts |

**Files written by this seat** (all under
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-90/w1/`):

* `ScoutSources.md` — this report
* `ScoutSources-receipts/s131-s132-recheck.txt`
* `ScoutSources-receipts/gate-behaviour.txt`
* `ScoutSources-receipts/round91-leads.txt`

No lane file outside that directory was created or modified. No instrument, control, fixture or frozen
byte was touched. No git or jj write was performed anywhere. The scratch root
`/fast/scratch/hyaku/kasegi-r90/ScoutSources` was deleted at the end of this seat and no longer exists.
