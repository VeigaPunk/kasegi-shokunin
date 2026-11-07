# ScoutSources — round 91, attempt 1, wave w1

**Seat:** scout · **Axes judged:** `depth:verifiability`, `coverage`
**Scope:** re-open the round's sources and open round-92 leads.
**Receipt (full):** `.ufo/waves/round-91/w1/ScoutSources-receipts/round92-leads.txt`

Findings are routed defects and qualifiers. Nothing here re-scores either frozen claim, and
neither claim's predicate was touched.

---

## 1. Summary for the L1

| # | Finding | Kind | Verdict |
|---|---|---|---|
| A | Live re-fetch of S133/S134 is byte-identical to the committed snapshots and the manifest digests; all four pinned quotes re-verify at their anchors | verification | **clean — no defect in the round-91 sources** |
| B | S135's recorded rejection reason | verification | **AGREE** (all three clauses measured) |
| C | Lead A — GitHub Docs, *About authentication to GitHub* | round-92 lead | **OPEN** — a real uncovered class, sourceable today without an allowlist row |
| D | Lead B — Microsoft Learn, *Create an account SAS* | round-92 lead | **CLOSED** — already detected; both Azure limits unreachable with documented fields |
| E | Lead C — HTTP Archive (HAR) format, cookie object | round-92 lead | **OPEN, tier-limited** — the gap is real; the document declares itself non-authoritative |
| D1 | S133/S134 registry rows still `queued` / `—` at HEAD | routed qualifier | **not a defect** — the normal round-90 two-commit shape; the pending integration commit must carry the row change (see §5) |
| D2 | S135 scope cell omits the optional Hash-Algorithm pair | routed qualifier | scope is immutable — needs a superseding row, not an in-place edit |
| D3 | The GitHub pattern-catalogue page is intake-refused reproducibly | operational, for round-92 planning | needs a digest-bound allowlist row keyed to the **lane-relative** path |

**No C1 or C2 predicate was disturbed, and no defect was found in the round-91 sources
themselves.** The one substantive thing the L1 must act on is **D1**.

---

## 2. Re-opening the round's sources (task 1)

Every capture used the lane's own instrument (`corpus/instruments/capture-source.py`, default
instrument UA), so the intake gate ran on each. Access date for all of them: **2026-11-07**.

| id | URL | live sha256 | vs manifest | vs committed file |
|---|---|---|---|---|
| S133 | `learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas` | `56d858ac…cd6` | **equal** | **byte-identical** (`cmp` exit 0) |
| S134 | `docs.aws.amazon.com/…/private-content-setting-signed-cookie-custom-policy.html` | `ddf45b80…1cc` | **equal** | **byte-identical** (`cmp` exit 0) |

The manifest's own `bytes` and `lines` fields match the committed files (S133 60089 B / 954
lines; S134 21243 B / 441 lines), and both URLs appear exactly once in `corpus/SOURCES.md`
(R20's one-row-per-URL clause holds).

Recheck of the pinned quotes — `source-recheck.py --manifest corpus/source-snapshots/round-91/manifest.json`, **rc 0**:

```
S133:sha256 OK
S133:Q01-skdutid-version OK occurrences=1 anchor=571-ok
S133:Q02-skdutid-tenant OK occurrences=1 anchor=567-ok
S134:sha256 OK
S134:Q01-signature-cookie OK occurrences=1 anchor=97-ok
S134:Q02-three-pairs OK occurrences=1 anchor=17-ok
```

The pre-freeze capture-scan control also reproduces against the landed scanner: over the two
live captures plus the S135 re-fetch and the three lead captures, the run reads
`scanned=6 hits=0 files=0 allowed=0 unused_allow=19 rc=0`, matching
`.ufo/waves/round-91/controls/capture-scan-r91.txt`. The landed scanner at HEAD and at the C2
landing commit are the same bytes (`89e283c6…26d7`), which is the `--instrument-sha256` pin in
the frozen C2 command.

**Finding A: no defect.** No anchor drift, no digest drift, no intake refusal, no stale pin.

---

## 3. S135 — AGREE with the recorded rejection reason (task 2)

**Verdict: AGREE.**

`corpus/SOURCES.md` row S135 reads: *"REJECTED: its signature cookie has the same name and
value form as S134's, so it adds no detectable shape; the extra CloudFront-Expires pair is a
timestamp, not credential material."*

I re-opened the canned-policy page (HTTP 200, fetched 36439 B, snapshot 13229 B, 240 lines,
sha256 `d6fccb868f4a8367da95912ee818d2a00807575ed23419c7b2395c5aaff3994c`). The row's anchor
cell and the round-91 lesson both record that digest as `d6fccb86…`; the live re-fetch
reproduces it **exactly**, across two independent fetches, so it is a byte-stable normalized
snapshot digest, not a nonce-bound instance digest (R100 satisfied).

Each clause, measured:

1. **Same name.** S135 line 37 and S134 line 40 read the same string:
   `CloudFront-Signature=hashed and signed version of the policy statement;`
2. **Same value form.** The signature value on S135 line 110 and on S134 line 123 are each
   **28 characters** long — the documentation's short example value in both pages. The landed
   scanner's cookie shape has a 40-character floor, so *neither* page's example value is a hit.
   The two pages cannot differ in detectability on their own examples.
3. **The extra pair is a timestamp.** S135 line 109 shows the Expires pair carrying a Unix
   seconds value; S135 line 31 describes that field as *"date and time in Unix time format
   (in seconds)"*. No credential material.
4. **Same three-pair structure.** S135 lines 16-18 name the same three name-value pairs S134
   names at lines 17-19, with the Expires pair standing in place of the Policy pair.

I also measured companion-invariance on the landed scanner: the CloudFront-Signature cookie
detects identically whether the companion pair is the custom-policy Policy pair, the
canned-policy Expires pair, or absent. The row's flip clause — *"a round that binds the cookie
shape to its companion pairs cites it as the canned-policy form"* — is therefore still exactly
right, and the round-91 landing does not weaken the rejection.

The row's `status=rejected`, its reason, its flip, and its `used-by` cell (`—`, no path cites
it) are all consistent with the lane's conventions.

**Qualifier D2 (scope completeness, not a rejection defect).** The S135 page also documents an
optional **fourth** pair, the Hash-Algorithm pair (S135 lines 18-19, 48-50, 103-106), which
the row's scope cell does not name. CORPUS.md rule 2 freezes the scope cell, so a correction
would need a new superseding row, not an in-place edit. Flagged so the L1 does not read the
omission as an oversight and "fix" it in place.

---

## 4. Three round-92 leads for the capture scanner's known limits (task 3)

Each lead carries URL, access date, sha256, line anchors, one located quote (≤25 words), and
the **measured** landed-scanner behaviour on a scratch fixture of that form. All three pages
were captured with the lane instrument, so the intake gate ran on each.

### Lead A — GitHub Docs, *About authentication to GitHub* — **OPEN**

* URL `https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github`
* Accessed 2026-11-07 · fetched 202839 B · snapshot 13895 B · 178 lines
* sha256 `f0edd23c8d6d53a066a6bb90fe4f4f754746df418d833acfc48c44d13943cca0`
* **Captured with the default allowlist — the intake gate accepts this page with no allowlist row.**
  Two independent captures are byte-identical.
* Anchors: 157 heading *GitHub's token formats* · **158** the prefix rule · 160 the stateless
  JWT-format rollout note (a 2026-04-27 rollout — a token form that did not exist when the
  scanner's shapes were written) · 161 table header · 162-167 the six prefix rows
  (`ghp_`, `github_pat_`, `gho_`, `ghu_`, `ghs_`, `ghr_`).
* **Quote (line 158, 13 words):** *"GitHub issues tokens that begin with a prefix to indicate the token's type."*

**Measured.** The landed scanner has **no provider-prefix shape of its own**: a bare prefixed
value with no adjacent key name is not detected. Eight fixtures, each a syntactically valid
prefixed value of the documented length planted alone in a file:

| fixture | form | result |
|---|---|---|
| F-GH2 | classic-PAT-shaped, in prose | **NO HIT** |
| F-GH3 | OAuth-prefixed | **NO HIT** |
| F-GH4 | fine-grained-PAT-shaped | **NO HIT** |
| F-GH6 | JWT-shaped installation value | **NO HIT** |
| F-GH7 | fine-grained, documented separator and length | **NO HIT** |
| F-GH8 | GitLab-prefixed | **NO HIT** |
| F-GH9 | npm-prefixed | **NO HIT** |
| F-GH10 | Slack-prefixed | **NO HIT** |

Contrast — the same values are caught only when a *generic* gate shape happens to fire:
F-GH1 (value behind an Authorization header) → `HIT shape=bearer line=2` and
`HIT shape=authorization line=2`; F-GH5 (value behind a token-named key) →
`HIT shape=credential line=1`.

Batch sums: `scanned=6 hits=0 … rc=0` (F-GH2/3/4/6/7 + F-HAR1) and
`scanned=3 hits=0 … rc=0` (F-GH8/9/10). The mixed run reads
`scanned=9 hits=6 files=5 allowed=0 unused_allow=19 rc=1`.

So the class is genuinely uncovered, not merely rare, and a first-party page states the prefix
rule and enumerates the prefixes — **the class is sourceable**.

**Operational fact round 92 must plan for (D3).** The sibling GitHub *pattern-catalogue* page
(`…/secret-scanning/introduction/supported-secret-scanning-patterns`, sha256
`77f388961f48b660e374701cd7667931f592bbfe215c7071c109d333cfda06eb`, 688 lines — the digest
the round-90 ScoutSources seat recorded, reproducing byte-for-byte) is **refused** by the
intake gate:

```
INTAKE-REFUSED L1cat shape=private-key line=596 out=… written=no
```

This is a true positive on the *shape*, not on a secret: the matched bytes are the 27-byte
literal PEM private-key header **name** the page prints as a pattern description
(matched-bytes sha256 `3021d90e…f572d`, length 27, line 596 of the normalized snapshot). A
one-row, digest-bound allowlist row keyed to the **lane-relative** out path makes the same
capture succeed — verified both ways: with the row the bytes scan clean (`found=[]`), without
any row the same bytes report `[('private-key', 596)]`. Note the key must be
`corpus/source-snapshots/round-92/<id>.txt`, not an absolute path, because
`capture-source.py` keys the allowlist on `lane_rel(out)`.

**Lead A's own page needs no allowlist row**, so this class is reachable today without
touching the allowlist. The catalogue's line 616 states the push-protection scope rule and
line 675 carries a client-pagination marker, so a snapshot-anchored row may cite the rule but
not any whole-catalogue count.

### Lead B — Microsoft Learn, *Create an account SAS* — **CLOSED as a new shape**

* URL `https://learn.microsoft.com/en-us/rest/api/storageservices/create-account-sas`
* Accessed 2026-11-07 · fetched 69725 B · snapshot 24086 B · 645 lines
* sha256 `3c95457a4eba3b1cd99f7d32e2549232ef346fe61d2aa581d75588411d59f335`
* Default allowlist; two independent captures byte-identical.
* Anchors: **44** the account-SAS-URI definition · 51-52 the SignedVersion field (`sv`) ·
  **587** the documented account SAS URI example · 619 the signature parameter in it.
* **Quote (line 44, 23 words):** *"The account SAS URI consists of the URI to the resource for which the SAS will delegate access, followed by a SAS token."*

**Measured — the account SAS is already covered.** F-AZ1 (documented short field set) →
`HIT shape=azure-sas-signature line=1`; F-AZ5 (with the IP field added) → hit; F-AZ4 (with the
7-letter delegated-tenant field) → hit. Reverse parameter order also detects. Batch sum:
`scanned=4 hits=3 files=3 allowed=0 unused_allow=19 rc=1`.

**Round 92 should not open an Azure seat.** Both Azure limits are unreachable with any token
Microsoft documents, and I measured each boundary:

* **Parameter-name length.** 7 letters between the version and signature parameters still
  detects; **8 letters does not**. The longest parameter name documented anywhere in the
  Azure user-delegation and account-SAS pages is **7 letters**. Every documented Azure SAS
  field name is 2-7 lowercase letters, so the round-91 widening to 2-7 covers **100% of the
  documented names**.
* **Parameter count.** 20 intervening parameters still detect; **21 do not**. Clean sweep, each
  n being its own list of n distinct 3-letter names: n=15…20 → hit, n=21 → miss, n=22 → miss.
  The union of all 21 documented Azure SAS field names is 21, but that union is not a real token
  — several of those fields are mutually exclusive alternatives. The widest realistic token
  measured (a user-delegation SAS carrying 16 documented fields) detects.

So a name-length or count widening would be un-motivated by the sources.

**Ruled out, so it is not re-chased next round:** the hypothesis that a 9-letter Azure SAS
parameter exists (`sddistype`) is **not supported by Microsoft**. The string does not appear in
the create-user-delegation-sas, create-account-sas, create-service-sas, storage-sas-overview,
authorize-with-azure-active-directory or data-lake-storage-access-control-model pages, nor in
the `Azure.Storage.Sas` `DataLakeSasQueryParameters` / `DataLakeSasBuilder` reference pages
(measured count 0 on each). The real directory-depth parameter is the 3-letter `sdd`
(signedDirectoryDepth), present in the committed S133 capture at line 260 and in the field
table. **Nothing 8+ letters is documented.**

### Lead C — HTTP Archive (HAR) format, cookie object — **OPEN, tier-limited**

* URL `https://w3c.github.io/web-performance/specs/HAR/Overview.html` — this is the URL the
  document itself names as *This version* and *Latest version* (snapshot lines 5-10). The
  historical `httpwg.org/specs/HAR-1.2/` URL now returns **HTTP 404** and the `www` host fails
  certificate validation, so the self-named URL is the live one.
* Accessed 2026-11-07 · fetched 50878 B · snapshot 23064 B · 440 lines
* sha256 `88211ff4f5980591315a6a22e7ae659f1ab1e5a02021f818c18df51cfee80743` — the same bytes
  are served at `https://webperfwg.org/specs/HAR/Overview.html`, and the two captures are
  byte-identical.
* Default allowlist — the intake gate accepts this page with no allowlist row.
* Anchors: 4 the document's own date line · **29-31** its own status statement · 189 the
  request cookies array · 215 the response cookies array · **225** the cookies object heading ·
  **226** the sentence describing it · 227-238 a complete example cookie object · **239** the
  name member's definition · **240** the value member's definition.
* **Quote (line 226, 13 words):** *"This object contains list of all cookies (used in `<request>` and `<response>` objects)."*

**Measured.** The scanner detects the cookie only when the name and the value sit in one text
run. In the HAR object form they are **separate members**, so the cookie is not detected:

| fixture | form | result |
|---|---|---|
| F-HAR1 | HAR cookie object, name member and value member separate | **NO HIT** |
| F-HAR3 | the same object in a request's cookies array | **NO HIT** |
| F-HAR2 | the same value inside a headers-array member whose text holds the joined name and value | `HIT shape=cloudfront-signed-cookie-signature line=1` |
| F-HAR4 | the same, in the response's headers array | `HIT shape=cloudfront-signed-cookie-signature line=1` |
| F-HAR5 | the same value in a plain request `Cookie` header | `HIT shape=cloudfront-signed-cookie-signature line=1` |

Batch sum: `scanned=5 hits=3 files=3 allowed=0 unused_allow=19 rc=1`.

The split name/value object form is a genuine gap, and it is exactly the form the scanner's own
known-limits list names (HAR/JSON name/value objects). The first-party format document states
the object shape, so the gap is sourceable.

**Tier qualifier — load-bearing for the admission decision.** The document declares its own
non-status: snapshot lines 29-31 read, in its own words, that it is marked DO NOT USE, was
never published by the working group, and **has been abandoned**. It is therefore **not** a
first-party tier-A vendor specification, and it must not be admitted as tier A on the strength
of the shape being right. If a HAR-shaped row is opened, the honest tier is the one this lane
already gives non-normative community documents, and the row must record the abandonment. A
better-sourced route to the same object shape, if the L1 wants tier A, is the browser-vendor
or tool-vendor side; this seat did not open one, so **that search stays open**.

---

## 5. Routed findings for the L1

### D1 — the two round-91 source rows are still un-migrated in the committed registry *(integration obligation)*

At HEAD (`bcbfbde63b83c9336e845001323b5c92419e526a`), `corpus/SOURCES.md` rows S133 and S134
read `status=queued` and `used-by=—`. `corpus/SOURCES.md` has not changed since the freeze
commit `53ab692a7b544c35141e2b19f7413cbdb767c1ad`.

The round-91 lesson `corpus/lessons/round-91.md` lines 23 and 31 each record the row change as
*"status `queued` (freeze 53ab692a) → `mined` (integration); used-by `—` →
`corpus/instruments/capture-secret-scan.py`"*.

The instrument does cite both rows at the landed HEAD (`corpus/instruments/capture-secret-scan.py`
lines 50 and 77), and the cited path exists — so `mined` is the correct status under CORPUS.md's
own definition. Two factual observations:

* the lesson file is **not tracked** at HEAD (`git ls-files corpus/lessons/round-91.md` returns
  nothing; it exists only in the working tree), so the old→new change is currently recorded
  nowhere in the committed tree;
* the working-tree `corpus/SOURCES.md` is byte-identical to HEAD, so the migration has not
  happened in the tree either.

**This is not a failure of either frozen claim** — C1's predicate names only
`corpus/knowledge/triage-thresholds.md` and C2's only the scanner — and it is **not a defect
either**: the round-90 round used the same two-commit shape. Round-90's C2 landing (`643ddb4`)
landed the instrument, `corpus/instruments/README.md` and `SCORECARD.md` and did **not** touch
`corpus/SOURCES.md`; the S131 migration to `mined` and the lesson landed later, in the separate
integration commit `124e5b4`. Round 91 is at the same point in that sequence, with the
integration commit still to come. The obligation is simply that it must come, and must carry
the row change the lesson already states, or the round ends with a lesson describing a change
the registry does not carry. Verification after the integration commit:

```sh
git show <integration>:corpus/SOURCES.md \
  | awk -F'|' '/^\| S13[34] / {print $2, $9, $12}'
# must print:  S133  mined  corpus/instruments/capture-secret-scan.py
#              S134  mined  corpus/instruments/capture-secret-scan.py
```

The lane's own census rule then applies — a `mined` row's `used-by` paths must exist. The path
exists, so that check stays green.

### D2 — S135 scope cell omits the optional Hash-Algorithm pair *(qualifier)*

S135's scope cell names three cookie name-value pairs; the page also documents the optional
Hash-Algorithm pair (S135 lines 18-19, 48-50, 103-106). CORPUS.md rule 2 freezes the scope
cell, so a correction needs a new superseding row rather than an in-place edit. Recorded so the
L1 does not read the omission as an oversight and edit it in place.

### D3 — the GitHub pattern-catalogue page is intake-refused reproducibly *(operational, for round-92 planning)*

Details and the exact allowlist-row shape are in §4, Lead A. The key point for planning: the
allowlist row must be keyed to the **lane-relative** path (`corpus/source-snapshots/round-92/<id>.txt`),
because `capture-source.py` keys the allowlist on `lane_rel(out)`; the matched-bytes digest to
pin is `3021d90eb9437b2d8f30e8363695c4418b5e5f1870801b5c317e9398ee0f572d` (27 bytes). The
alternative first-party page for the same class — Lead A's authentication page — needs no
allowlist row at all.

### D4 — scope note on the round-91 sources *(no defect found)*

The committed S133/S134 snapshots and their manifest records re-fetch byte-identically, the
pinned quotes re-verify at their anchors, the intake gate accepts both pages, and S135's
rejection reason holds under measurement. On the round-91 sources this seat found **no defect**.

---

## 6. Method, hygiene, and what I did not do

* **Every capture** used `corpus/instruments/capture-source.py` with the default instrument UA,
  so the intake gate ran on each page; every access date is 2026-11-07.
* **Every lane script ran with `python3 -B`**; no `__pycache__` was written. The lane's own
  `resolve.py` census was not run (out of scope and expensive); the scope reading used was the
  scanner and `source-recheck.py`, both of which are seconds-scale.
* **Credential hygiene.** No credential-shaped value was written into this report or into the
  receipt. The planted fixtures (prefixed tokens, SAS URIs, HAR objects, cookie headers) lived
  only in the scratch tree and were deleted with it; the receipt carries sha256 digests, line
  anchors, ≤25-word quotes and the scanner's HIT/summary lines, which never print values. The
  scanner's summary lines and shape names only are quoted.
* **No writes outside my wave dir.** I created exactly two files:
  `.ufo/waves/round-91/w1/ScoutSources.md` and
  `.ufo/waves/round-91/w1/ScoutSources-receipts/round92-leads.txt`.
  No scanner, counter, or `S<digits>.txt` snapshot was copied into the wave dir. No corpus
  file, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, the frozen
  `c1/`/`c2/`/`controls/`/`l1/` bytes, or any instrument was modified. No git or jj write was
  performed anywhere — `git log`/`diff-tree`/`show`/`ls-files` were read-only.
* **Scratch.** Root `/fast/scratch/hyaku/kasegi-r91/ScoutSources`, `TMPDIR` pointed at it for
  every command that could write a temporary file. **Deleted before yield** — the directory was
  removed recursively and its absence verified. Nothing under it survives.
* **Network.** Only plain GETs on the public documentation pages named in this assignment. No
  probing, no login, no submission to any target.
* **Tooling.** No tool was installed or upgraded by this seat; none was needed.

---

## 7. Files written

1. `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-91/w1/ScoutSources.md`
   — this report.
2. `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-91/w1/ScoutSources-receipts/round92-leads.txt`
   — the full receipt: live-fetch digests and byte comparisons, the `source-recheck.py` and
   `capture-secret-scan.py` output lines, the S135 clause-by-clause measurements, the three
   leads with URL / access date / sha256 / line anchors / ≤25-word quote / measured behaviour,
   the routed findings, and the full command list.

Scratch root `/fast/scratch/hyaku/kasegi-r91/ScoutSources` — **deleted** before this yield.
