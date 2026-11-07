# ScoutSources — round 88, w1: S126/S127 live re-open, SOURCES.md row check, C1 map re-verification, round-89 leads

Seat: `ScoutSources` (scout, leaf — no delegation, no background jobs).
Fetch window: **2026-11-07 00:43Z – 01:0xZ** (all plain `GET`, no login, no probe, no submit — PROVINCE.md refuses
live-target testing). Scratch: `/fast/scratch/hyaku/kasegi-r88/ScoutSources` (deleted on exit).
Receipts: `.ufo/waves/round-88/w1/ScoutSources-receipts/`
(`live-refetch-r88.txt`, `lead-urls-status-r88.txt`, `scanner-gap-probe-r88.txt`, `raw-byte-variance-r88.txt`,
`c1-map-reverify-r88.txt`).

**No credential-shaped value was written into `w1/`.** No `S<digits>.txt` snapshot, no scanner bytes and no counter
bytes were copied in; the receipts carry sha256 digests, HTTP statuses, byte counts, located ≤25-word quotes and the
scanner's own `HIT`/summary lines (which never print a matched value). The five files in `w1/ScoutSources-receipts/`
and this report were re-scanned with the **landed** instrument before yielding:
`CAPTURE-SECRET-SCAN mode=files scanned=6 hits=0 files=0 allowed=0 unused_allow=17 rc=0`.

**These are routed defects and qualifiers, never re-scoring.** C1 and C2 are judged only on their frozen predicates at
their landing commits (`fd33e1bfe26ad9af13c138feb87c9f222be957cb`, `b43dc2154bc09470da2209fb626021da3af3593e`).

---

## 0. Headline

1. **Both round-88 sources re-open live today, HTTP 200, and reproduce their manifest sha256 byte-for-byte.** S126 →
   `b04de8a9…a000b83d` (manifest-equal), S127 → `66f8a35e…b1312` (manifest-equal). All **four** manifest quotes occur
   live, **exactly once each**, on their declared anchor lines (424, 487 / 404, 605).
2. **One verifiability qualifier on the manifest's `fetch_method` string (Q-V1):** the S126 *raw* body is not
   byte-reproducible today — 8 fetches returned 202 352 B (6×) or 202 356 B (2×), the difference being one
   `track-name="console"` attribute in the page's nav boilerplate — while the **normalized** snapshot is identical in
   every fetch. The manifest's stated "raw 202356 bytes" is therefore a one-sample observation, not a re-checkable
   invariant; the pinned `sha256`/`bytes`/`lines` of the snapshot are.
3. **Both SOURCES.md rows (S126, S127) are grounded in the live page text** — scope, anchor lines and `teaches` all
   re-located today (§2). No defect.
4. **C1's frozen 50-key map re-verifies cleanly on my own independent implementation** of the M8 content proxy: 50/50
   keys have a backticked site in the C1-landing tree, 94 sites, 0 missing targets, 0 out-of-range anchors, 0
   identifier-share failures. **But the L1's own non-author semantic pass labels 8 of the 50 keys WRONG** and the L1's
   `r140-check-r88.txt` prints `verdict=FAIL` for the frozen map on those labels — i.e. the lexical proxy passes where
   the semantics do not. This is the depth:verifiability hole the L1 has already encoded as QUALITY R140 (§3).
5. **Five first-party round-89 leads** with URL, HTTP status, a located ≤25-word quote and the shape taught (§4). The
   landed instrument misses **three** of them outright and catches the GitHub one only in its unencoded form.

---

## 1. S126 / S127 live re-open (this round's two new sources)

Method: `curl -sSL` (plain GET) → the same HTML→text normalization `corpus/instruments/capture-source.py` applies
(`<script|style>` dropped, block tags → newline, tags stripped, entities decoded, per-line whitespace collapsed);
digests taken over the normalized text. Receipt: `ScoutSources-receipts/live-refetch-r88.txt`.

| id | URL | HTTP | raw bytes (today) | normalized bytes / lines | normalized sha256 | manifest sha256 | equal |
|---|---|---|---|---|---|---|---|
| S126 | `https://docs.cloud.google.com/storage/docs/access-control/signed-urls` | 200 | 202 352 or 202 356 (varies; see Q-V1) | 18 245 / 584 | `b04de8a94c7905d8b768b8dcd7d7e354df3f972ef292bb3e1a1f36aea000b83d` | `b04de8a9…a000b83d` | **yes** |
| S127 | `https://learn.microsoft.com/en-us/rest/api/storageservices/create-service-sas` | 200 | 87 659 (stable over 5 fetches) | 38 072 / 663 | `66f8a35e9d598e5f5eecedd9003a7ba7f99c1eda24963e4cf1891245bdfb1312` | `66f8a35e…b1312` | **yes** |

The manifest's `bytes` and `lines` fields (18 245 / 584 and 38 072 / 663) are also **exactly** today's normalized
figures. Ten independent fetches (5 per page) produced one normalized digest each.

### 1.1 Per-quote presence, live

| id | quote id | declared anchor | found at (live) | on anchor? | occurrences |
|---|---|---|---|---|---|
| S126 | Q01-possession | 424 | 424 | **yes** | 1 |
| S126 | Q02-signature-param | 487 | 487 | **yes** | 1 |
| S127 | Q01-sig-hmac-base64 | 404 | 404 | **yes** | 1 |
| S127 | Q02-example-uri | 605 | 605 | **yes** | 1 |

The lane's own instrument agrees:
`python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-88/manifest.json --source S126`
→ `S126:sha256 OK` + `Q01-possession OK occurrences=1 anchor=424-ok` + `Q02-signature-param OK occurrences=1
anchor=487-ok`, rc 0; identically for S127 (`anchor=404-ok`, `anchor=605-ok`), rc 0.

### 1.2 Q-V1 (routed qualifier, verifiability) — the S126 raw body is not byte-reproducible; the snapshot is

The manifest's S126 `fetch_method` string says *"raw 202356 bytes, snapshot 18245 bytes; a second fetch at
2026-11-07T03:30:05Z … gave byte-identical snapshot bytes"*. Measured today over 8 fetches of the same URL:

```
202352, 202356, 202352, 202356, 202352, 202352, 202352, 202352
```

A byte diff of two differing fetches localizes the difference to **one attribute in the page's nav boilerplate**
(`track-name="console"` present in one, absent in the other) — i.e. a rotating page element, not a content change.
After normalization every one of the ten fetches yields the identical 18 245-byte text with sha256 `b04de8a9…`.
S127 is stable at 87 659 raw bytes across 5 fetches.

**Consequence for round 89:** a re-check of S126 must compare the **normalized** digest, not the raw byte count.
The manifest's raw-byte figure is a one-sample observation and will fail a naive byte comparison on a different day.
Receipt: `ScoutSources-receipts/raw-byte-variance-r88.txt`.

---

## 2. `corpus/SOURCES.md` rows S126 / S127 against the live pages

Rows are at `corpus/SOURCES.md:138-139` in the working tree (the L1 has flipped `queued` → `mined` in the working
tree; at the C2 landing commit the rows still read `queued` / used-by `—`, which matches the freeze). Checked cell by
cell against today's live text:

| cell | S126 | S127 | verdict |
|---|---|---|---|
| scope | "an active Cloud Storage signed URL authorizes whoever holds it" + "its X-Goog-Signature query parameter is the authentication string"; "V4 signed URLs only, not V2 or other providers" | "definition of the service SAS sig query parameter (an HMAC-SHA256 over the string-to-sign, Base64-encoded)" + "its example URI carrying sv= and sig="; "service SAS on Azure Storage only, not account or user-delegation key formats" | **both true.** S126 live: 0 hits for `V2`, 0 hits for `azure|shared access signature|\bsas\b`, V4 named at line 461. S127 live: HMAC-SHA256+Base64 wording present at 402-404; the service-SAS example URI at 605 carries both `sv=` and `sig=` |
| anchor | "snapshot lines 423-424 and 487-488" | "snapshot lines 402-404, 601, 605 and 638-639" | **all cited lines re-located live, same content** (424/487 and 404/601/605/638-639). The named section headings exist too: S126 "Overview" (431) and "Signed URL example" (460); S127 "Specify the signature" (396) and "Service SAS example" (603) |
| teaches | "Treat an X-Goog-Signature value in a captured URL as bearer credential material for the URL's lifetime" | "Treat a sig= value beside an sv= storage version in a captured URL as an Azure SAS signature that grants access until expiry" | **both grounded**: S126 423-424 + 450-452 + 487-488; S127 594-601 (expiry/revocation) + 605 + 638-639 |

**One nuance on the S127 scope cell, for the L1 to weigh (not a defect).** The cell says *"service SAS on Azure Storage
only, not account or user-delegation key formats"*. That is true of what the **row teaches** — the anchor cites only
service-SAS material (396-404, 601, 605, 638-639). It is **not** true of the whole page: the live S127 also names the
other two SAS kinds in cross-reference prose (line 30 "Microsoft recommends using a user delegation SAS", 38-39 on
account SAS, and 642-643 link both) and the anchor cell's own "not account or user-delegation" exclusion is therefore
a *reader-scoping* statement rather than a page-content statement. The page's own recommendation (line 30) is also the
first-party pointer to the round-89 udsas lead in §4 (L3).

One minor qualifier, no defect: the **manifest** quote `Q01-sig-hmac-base64` is **29 words**, above the ≤25-word bar
QUALITY Q3 sets for load-bearing claim quotes. The manifest is a capture record rather than a claim, and the corpus
entry quotes the same passage at **22 words** (`corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md:39`),
so the entry complies. Precedent for >25-word manifest quotes exists (round-39 42 words, round-23 37, round-29 35,
round-50 32). Flagged only so the L1 can decide whether round-89 manifests should trim.

---

## 3. C1 — independent re-verification of the frozen 50-key repair map (depth:verifiability)

Method (independent of the frozen counter; read-only): `git archive fd33e1bf corpus/knowledge | tar -x` into scratch;
for each of the 50 keys in `.ufo/waves/round-88/c1/repair-map.json` find every **backticked** occurrence of the mapped
value in the C1-landing `corpus/knowledge/*.md`; check the cited anchor range is in range and that the citing line and
the cited range share ≥1 identifier of ≥4 characters (the M8 content proxy). Receipt:
`ScoutSources-receipts/c1-map-reverify-r88.txt`.

```
C1-REVERIFY map_keys=50 keys_with_a_backticked_site=50 total_backticked_sites=94
C1-REVERIFY missing_targets=0 out_of_range_anchors=0 identifier_share_failures=0
C1-REVERIFY verdict=pass
```

**The frozen predicate's own measure passes on my independent implementation.** But the L1's non-author semantic
labels (`.ufo/waves/round-88/l1/r88-semantic-labels.tsv`, transcribed from `w1/ReviewC1Semantics.md`) mark **8 of
the 50 keys WRONG** — `claim-gates.md:21-23`, `:34`, `:35-36`, `:63-66`, `:66-67`, `claim-package-contract.md:28-29`,
`japanese-domestic-disclosure-workflow.md`, `mission-control.md:43-46` — and the L1's own
`.ufo/waves/round-88/l1/r140-check-r88.txt` prints `map_keys=50 labelled=50 wrong=8 unclear=1 … verdict=FAIL exit=1`
for the frozen map, and `PASS` for the map with those 8 keys removed.

**Routed finding (D-C1-1, already known to the L1, restated with my independent measurement):** the M8 lexical proxy
that C1 is frozen against passes on all 50 keys, and the same 50 keys contain 8 that a non-author semantic reviewer
calls wrong. A proxy pass is not a semantic pass. The L1 has already written QUALITY R140 (working tree,
`corpus/QUALITY.md`) requiring a hand-labelled sample of ≥15 keys with no WRONG verdict before a proxy-selected map is
frozen. **The 8 keys are already applied in the C1 landing** — so if R140 is to bind this map, the landing needs the
8-key correction; if it is to bind only future maps, the landing keeps them and round 89 must not repeat the
proxy-only selection. This is a decision for the L1; I do not re-score C1, whose frozen predicates (P1/P2/P3) are
judged at `fd33e1bf` and are unaffected by this observation.

---

## 4. Round-89 leads — credential material in captured evidence the scanner does not yet detect

Each lead is a **first-party page I opened today** with URL, HTTP status, a **located ≤25-word quote** and the shape it
teaches. Full measurements (raw bytes, normalized bytes/lines/sha256, located line numbers) are in
`ScoutSources-receipts/lead-urls-status-r88.txt`. None is written into the lane; none is a corpus row yet.

The gap measurements come from the **landed** instrument at the C2 landing commit (sha256 `d7349536…4417`), run over
scratch-only synthetic fixtures; the receipt carries the scanner's `HIT`/summary lines and each fixture's sha256, never
a value (`ScoutSources-receipts/scanner-gap-probe-r88.txt`). The positive control fires three shapes, so the probe is
live.

### L1 — Amazon CloudFront signed URLs (`Signature=` + `Key-Pair-Id=`)

- **URL:** `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html` — **HTTP 200** (34 341 B raw → 11 207 B normalized, 225 lines).
- **Quote (11 words, normalized line 72):** *"A hashed, signed, and base64-encoded version of the JSON policy statement."*
- **Quote (7 words, normalized line 70):** *"&Signature=hashed and signed version of the policy"*
- **Shape taught:** CloudFront carries the policy hash in a **`Signature=`** parameter and the signing public key in
  **`Key-Pair-Id=`** — neither is an `X-Goog-Signature` nor an `sig=` parameter.
- **Gap (measured):** the landed instrument reports **`hits=0`** on a CloudFront-style signed URL (fixture G1,
  sha256 `932fd5fc…`). Custom-policy page (`…signed-url-custom-policy.html`, HTTP 200, 50 387 B raw) teaches the same
  two parameters plus `Policy=`; quote (7 words, line 60): *"Your query string parameters can't be named"*.
- **Design note for the L1:** `Key-Pair-Id` is a **public key id**, not a secret — AWS's own example is
  `K2JCJMDEHXQW5F`. A scanner matching on it would false-positive on the vendor's documentation example, so a
  round-89 shape should target the `Signature=` value only (as the r87 lead L3 already warned).

### L2 — Google Cloud Storage **V2** signing (`GoogleAccessId=` + `Signature=`)

- **URL:** `https://docs.cloud.google.com/storage/docs/access-control/signed-urls-v2` — **HTTP 200** (121 500 B raw → 10 063 B normalized, 262 lines). Note `https://developers.google.com/storage/docs/signed-urls-v2` now **404s** and redirects to the docs.cloud.google.com form.
- **Quote (12 words, normalized line 159):** *"to retrieve a service account name, which is the GoogleAccessId you need"*
- **Quote (11 words, normalized line 105):** *"This page covers legacy material related to the V2 signing process."*
- **Shape taught:** the V2 scheme puts a **service-account email in `GoogleAccessId=`** and the signature in
  **`Signature=`** — different parameter names *and* a different encoding from V4's hex `X-Goog-Signature`.
- **Gap (measured):** **`hits=0`** (fixture G2, sha256 `6675e0ec…`).
- **Scope note:** the page is explicitly marked legacy/caution (quote above), so a round-89 row should say so in its
  scope cell rather than presenting V2 as current practice.

### L3 — Azure **user-delegation** SAS (`skoid=` + `sktid=` + `skv=`)

- **URL:** `https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas` — **HTTP 200** (118 382 B raw → 60 089 B normalized, 954 lines).
- **Quote (11 words, normalized line 534):** *"The signedObjectId (skoid) field is required for a user delegation SAS."*
- **Quote (11 words, normalized line 536):** *"The signedTenantId (sktid) field is required for a user delegation SAS."*
- **Shape taught:** a user-delegation SAS binds the request to a **Microsoft Entra principal** through `skoid=` (object
  id) and `sktid=` (tenant id), with its own version parameter `skv=` — and the page's own example URI (normalized
  line 870) carries `skoid=`, `sktid=`, `skv=2022-11-02` **and** `sv=2022-11-02` **and** `sig=`.
- **Gap (measured):** a udsas-style token that carries `skv=` but **no `sv=`** is **not** detected (`hits=0`, fixture
  G3, sha256 `5834a43c…`), because the landed azure shape requires `sv=YYYY-MM-DD` in the same query; the identical
  token **with** `sv=` *is* detected (`HIT shape=azure-sas-signature`, fixture G4, sha256 `8fc5a948…`). So the precise
  round-89 gap is the **UDSAS version parameter**, not the udsas signature.

### L4 — HackerOne attachment `expiring_url` (pre-signed download URL in a first-party field)

- **URL:** `https://api.hackerone.com/hacker-reference/` — **HTTP 200** (155 762 B raw → 50 170 B normalized, 2 568 lines).
- **Quote (10 words, normalized line 249):** *"A temporary, pre-signed URL to download the attachment file directly."*
- **Quote (5 words, normalized line 251):** *"The URL will automatically expire"*
- **Shape taught:** HackerOne's own attachment object carries `expiring_url` — a **pre-signed S3 URL that expires after
  60 minutes**, i.e. bearer material inside a report JSON, the same field family as the round-86 incident
  (`profile_picture_urls`) but on attachments.
- **Gap (measured):** **`hits=0`** on a realistic `expiring_url` fixture (G5, sha256 `5fd1eb44…`): its
  `X-Amz-Signature` parameter name is not the GCS one, and the only key id in it is the AWS documentation example
  (allow-listed), so nothing matches. Note the shape is *time-boxed* — 60 minutes — so a scan window matters.

### L5 — GitHub raw download `?token=` (bearer URL parameter)

- **URL (first-party, tier A):** `https://docs.github.com/en/rest/repos/contents` — **HTTP 200** (436 444 B raw → 30 097 B normalized, 824 lines).
  **Quote (11 words, normalized line 294):** *"Download URLs expire and are meant to be used just once."*
  **Quote (12 words, normalized lines 738 and 779):** *"For private repositories, these links are temporary and expire after five minutes."*
- **URL (the parameter's own spelling, community tier):** `https://github.com/orgs/community/discussions/78633` — **HTTP 200** (192 080 B raw → 4 093 B normalized, 185 lines).
  **Quote (9 words, normalized line 98):** *"it generates the URL with the ?token=... part in"*
- **Shape taught:** GitHub's raw-content URLs for private repositories carry a **`?token=`** parameter that authorizes
  that one file; the first-party API reference states the download URL is single-use and the private-repo variant
  expires after five minutes.
- **Gap (measured):** **partial.** The unencoded form is caught only *incidentally*, by the claim-package gate's
  generic `credential` shape (`HIT shape=credential`, fixture G6, sha256 `eaab3d8a…`); the **percent-encoded** form
  evades every pattern (`hits=0`, fixture G7, sha256 `b53e86a0…`).
- **Tier note for the L1:** CORPUS.md fixes `community` at tier C and never A. The *expiry* fact is tier A
  (docs.github.com); the *`?token=` spelling* is only attested by a GitHub community discussion. A round-89 row should
  therefore be anchored on the first-party expiry statement, with the discussion named only as corroboration — or the
  row should be scoped to the first-party claim alone.

### 4.1 Coverage summary (landed instrument, C2 landing commit)

| lead | shape | landed scanner |
|---|---|---|
| L1 CloudFront | `Signature=` + `Key-Pair-Id=` | **`hits=0`** (G1) |
| L2 GCS V2 | `GoogleAccessId=` + `Signature=` | **`hits=0`** (G2) |
| L3 Azure udsas w/o `sv=` | `skoid=`/`sktid=`/`skv=` + `sig=` | **`hits=0`** (G3); **detected** once `sv=` is present (G4) |
| L4 HackerOne `expiring_url` | pre-signed S3 URL in a JSON field | **`hits=0`** (G5) |
| L5 GitHub raw `?token=` | `?token=` bearer parameter | caught **only unencoded**, by the generic gate shape (G6); **`hits=0`** percent-encoded (G7) |
| — AWS SigV4 query-string `X-Amz-Signature=` | 64-hex query signature | **`hits=0`** (G8) — the *only* AWS signature form the corpus's own S124 documents (`corpus/source-snapshots/round-87/S124.txt:412, 426`) and the landed scanner still misses |
| positive control | AWS STS token + key id | `hits=3` — `credential`, `aws-sts-session-token`, `aws-access-key-id` (G9) |

**This is a coverage lead for round 89, not a C2 defect.** C2's frozen statement is scoped to the two shapes S126/S127
name; the killed-rule text freezes the instrument after the freeze, so every row above is a routed lead. The landed
instrument's own docstring already names GCS V2 and CloudFront as known limits
(`corpus/instruments/capture-secret-scan.py:43-45`), which my measurements confirm are still open.

---

## 5. Summary of routed items

| id | kind | routed to | re-runnable command | evidence |
|---|---|---|---|---|
| Q-V1 | qualifier | L1 / round-89 capture discipline | `curl -sSL -o /dev/null -w '%{size_download}\n' https://docs.cloud.google.com/storage/docs/access-control/signed-urls` (repeat) | `ScoutSources-receipts/raw-byte-variance-r88.txt` — 8 fetches: 202 352 ×6, 202 356 ×2; normalized digest identical in 10/10 |
| Q-M1 | qualifier | L1 (manifest authoring) | `python3 -B -c "import json;m=json.load(open('corpus/source-snapshots/round-88/manifest.json'));print([(s['id'],q['id'],len(q['quote'].split())) for s in m['sources'] for q in s['quotes']])"` | manifest `Q01-sig-hmac-base64` = 29 words; the corpus entry's own quote is 22 words |
| D-C1-1 | routed defect (semantic, already encoded as QUALITY R140 by the L1) | L1 | `python3 -B .ufo/waves/round-88/l1/r140-check.py --map .ufo/waves/round-88/c1/repair-map.json --labels .ufo/waves/round-88/l1/r88-semantic-labels.tsv` | `.ufo/waves/round-88/l1/r140-check-r88.txt` — `wrong=8 … verdict=FAIL`; my independent proxy re-verification: 50/50 keys, 94 sites, 0 failures |
| L1–L5 | round-89 leads (unopened rows) | round-89 designer | `python3 -B corpus/instruments/capture-secret-scan.py --files <capture>` | `ScoutSources-receipts/lead-urls-status-r88.txt`, `scanner-gap-probe-r88.txt` |

**Files written by this seat** (all under
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-88/w1/`):

- `ScoutSources.md` (this report)
- `ScoutSources-receipts/live-refetch-r88.txt`
- `ScoutSources-receipts/lead-urls-status-r88.txt`
- `ScoutSources-receipts/scanner-gap-probe-r88.txt`
- `ScoutSources-receipts/raw-byte-variance-r88.txt`
- `ScoutSources-receipts/c1-map-reverify-r88.txt`

Nothing outside `w1/` was created or modified; scratch removed on exit. No lane, corpus, fleet or sibling-lane file was
written; no git/jj mutation was performed in the lane (read-only `git show` / `git archive` / `git ls-tree` only, plus
`git archive` into scratch).
