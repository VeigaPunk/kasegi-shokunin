# ScoutSources — round-89 wave 1 (attempt 1)

Seat: source verification and round-90 lead opening.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Lane HEAD at the time of the run:
`50e2632ea891bb080425f359d6a6115874cee61f` (round-89 landing receipts).
Scope: `depth:verifiability`, `coverage`.

Everything below was executed read-only against the lane and the four public URLs the item
names. No lane file was modified. No commit was made. The seat scratch root
`/fast/scratch/hyaku/kasegi-r89/ScoutSources` was deleted before yield (`rm -rf -- "$S"`).

## 1. Frozen-claim source verification (S128, S130, S129)

### 1.1 S128 and S130 re-opened live, recaptured, digest compared — MATCH

Both manifest URLs were re-fetched with `corpus/instruments/capture-source.py --kind html`
(default instrument UA) into scratch and the snapshot sha256 compared against the committed
`corpus/source-snapshots/round-89/` bytes and against the manifest's `sha256` field.

| id | HTTP | raw bytes | snapshot bytes | live sha256 | manifest sha256 | match |
|----|------|-----------|----------------|-------------|------------------|-------|
| S128 | 200 | 34341 | 11207 (225 lines) | `cd246e7debb4ea67cccf783ac6b16307b1d0febbda9de133df29a5ada5ea3331` | same | YES |
| S130 | 200 | 50387 | 19858 (422 lines) | `dcdaa1233df06b7304bc29c8af89371d81e7b0fa816251532ef9c52c8356ca39` | same | YES |

The live digests also equal the digests recorded in the round-88 lead receipt
(`.ufo/waves/round-88/w1/ScoutSources-receipts/lead-urls-status-r88.txt`), which is exactly what
the manifest's `fetch_method` field asserts. Neither source has drifted since the freeze.
Receipt: `ScoutSources-receipts/live-recapture-r89.txt`.

### 1.2 Every manifest quote present once at its anchor — CONFIRMED

`python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-89/manifest.json`
→ exit 0, no MISMATCH / UNAVAILABLE line:

```
S128:sha256 OK
S128:Q01-signature-param OK occurrences=1 anchor=70-ok
S128:Q02-key-pair-id OK occurrences=1 anchor=77-ok
S128:Q03-urlsafe-replacement OK occurrences=1 anchor=202-ok
S130:sha256 OK
S130:Q01-anyone-with-url OK occurrences=1 anchor=163-ok
S130:Q02-policy-param OK occurrences=1 anchor=66-ok
```

Each of the five quotes was additionally re-located by literal `grep -F -c` in the file the
manifest pins it to: exactly one hit each. (One non-defect note: the Q03 sentence also occurs
raw twice in S130, lines 138 and 399, but the manifest pins that quote to S128 only, where it
occurs once; `source-recheck` normalizes whitespace and reports `occurrences=1 anchor=202-ok`.)
Receipt: `ScoutSources-receipts/manifest-quote-recheck-r89.txt`.

### 1.3 The S129 rejection still holds — CONFIRMED

`corpus/SOURCES.md` row S129 rejects the GCS V2 signing page
(`https://docs.cloud.google.com/storage/docs/access-control/signed-urls-v2`) with the recorded
reason: the page names `Signature` and `GoogleAccessId` as values a program supplies but shows
no query-string form or example URL. The page was re-fetched live (HTTP 200; normalized snapshot
10063 bytes; sha256 `517f22a3669fb2e8b803637684476dc70f3e49451a03125e75c0cef4ef87de07`, byte-identical
to the round-88 lead capture) and re-checked:

- strict parameter-form search `GoogleAccessId=|Expires=|Signature=|&amp;Expires` → **0 hits**;
- no `?`-prefixed URL appears anywhere on the page;
- the five bare-name mentions are the string-to-sign component `Expires` (lines 120, 136, 138) and
  prose about the values the program supplies (lines 156, 159) — never `Name=value`;
- both anchors SOURCES.md cites (scratch lines 105–111 and 150–160) hold on the live capture, and
  the page still carries its own "Caution: This page covers legacy material related to the V2
  signing process." marking.

The rejection is correct at 2026-11-07 and its recorded flip condition stands.
Receipt: `ScoutSources-receipts/s129-rejection-r89.txt`.

### 1.4 The landed scanner still behaves as the frozen control claims — CONFIRMED

Re-running the landed `capture-secret-scan.py` on the two committed snapshots:
with `--allow /dev/null` → 2 hits (`cloudfront-signed-url-signature` at S128:13, S130:14), rc=1;
with `corpus/instruments/capture-secret-allow.tsv` → `allowed=2`, `hits=0`, rc=0. That matches
the frozen control `.ufo/waves/round-89/controls/capture-scan-r89.txt` exactly. The two
allowlist rows (rows 21–22 of the allowlist) bind the AWS documentation example signature.

## 2. Coverage probes on the landed scanner (round-90 material, falsifiable)

Each shape was probed in its **own** single-line fixture, because the scanner reports only the
first non-allowed match per shape per file (`scan_bytes` breaks after the first hit of a shape) —
a multi-line fixture masks later shapes of the same kind. All probes used `--allow /dev/null`.

| probe shape (values are shapes, not secrets) | landed scanner |
|---|---|
| `<cf-url>?Expires=…&Signature=<40+>&Key-Pair-Id=<8..32>` | **HIT** (the round-89 pinned shape) |
| `Signature=<40+>&Key-Pair-Id=<8..32>` (bare, no host) | **HIT** |
| `X-Signature=<40+>&Key-Pair-Id=<8..32>` | no hit |
| `a-Signature=<40+>&Key-Pair-Id=<8..32>` | no hit |
| `Signature=<40+>;Key-Pair-Id=<8..32>` (`;` separator) | no hit |
| `Set-Cookie: CloudFront-Signature=<40+>` | no hit |
| `Set-Cookie: CloudFront-Key-Pair-Id=<8..32>` | no hit |
| `Set-Cookie: CloudFront-Signature=<40+>&CloudFront-Key-Pair-Id=<8..32>` | no hit |
| `<gcs-url>?GoogleAccessId=<email>&Expires=<epoch>&Signature=<40+>` | no hit |

Two coverage gaps follow, each with a stated cause:

**(a) CloudFront signed cookies are not covered.** The landed `cloudfront-signed-url-signature`
rule anchors on the bare token `Signature=` and requires the pair to be joined by `&`/`&amp;`/
`\u0026`. In the cookie form the names are `CloudFront-Signature` and `CloudFront-Key-Pair-Id`
and they travel in `Set-Cookie` headers separated by `;`. The rule's left boundary
`(?:(?<![A-Za-z0-9_-])|(?<=\u0026)|(?<=%26))` rejects the hyphen inside `CloudFront-Signature`
(proved by the `X-Signature=`/`a-Signature=` probes), and the separator requirement rejects the
cookie layout. **Length caveat for the round-90 designer:** AWS's own documentation example
cookie signature value is **28 characters**, below the landed rule's `{40,}` floor, so a cookie
rule needs its own length floor — the long S128/S130 URL example is a padded artefact and would
otherwise mislead a threshold choice.

**(b) GCS V2 signed URLs are not covered.** The landed `gcs-signed-url-signature` rule is
anchored on the V4 parameter `X-Goog-Signature`; a V2 URL carries `GoogleAccessId=`/`Expires=`/
`Signature=`, which fires nothing.

Neither gap disturbs the round-89 frozen claim (which covers the CloudFront signed-URL shape
only) nor the landed controls. Both are round-90 coverage candidates.
Receipt: `ScoutSources-receipts/scanner-gap-probe-r89.txt`.

## 3. Round-90 source leads (URL, HTTP status, located quote ≤25 words)

Full detail, with digests and anchor lines, in
`ScoutSources-receipts/round90-leads-r89.txt`.

**L1 — GCS V2 signed-URL query (`GoogleAccessId`/`Expires`/`Signature`) as text.**
This is the flip condition SOURCES.md row S129 records. The GCS docs page itself cannot supply it
(§1.3), so the shape was located in Google's **own client-library sources**, which set the three
query parameters together. Three independent first-party Google repositories carry it:

- `https://raw.githubusercontent.com/googleapis/google-cloud-go/main/storage/storage.go` — HTTP 200,
  raw 105181 bytes, snapshot sha256 `9edf54caa87b4b38d84896ea7ec76f231ec3f395ddf77dcf540710ad51bf9f15`;
  capture lines 887–889: `q.Set("GoogleAccessId", opts.GoogleAccessID)` /
  `q.Set("Expires", fmt.Sprintf("%d", opts.Expires.Unix()))` / `q.Set("Signature", string(encoded))`.
  Located quote (11 words): **`q.Set("GoogleAccessId", opts.GoogleAccessID)`**
- `https://raw.githubusercontent.com/googleapis/nodejs-storage/main/src/signer.ts` — HTTP 200,
  raw 14026 bytes, snapshot sha256 `62a7fce59477def8c32504eac71bdca8958682b7451b5fdae378f92fc33a9ad3`;
  capture lines 70–73: `interface V2SignedUrlQuery extends SignedUrlQuery {` / `GoogleAccessId: string;` /
  `Expires: number;` / `Signature: string;`.
  Located quote (4 words): **`interface V2SignedUrlQuery extends SignedUrlQuery`**
- `https://raw.githubusercontent.com/googleapis/python-storage/main/google/cloud/storage/_signing.py`
  — HTTP 200, raw 26144 bytes, snapshot sha256
  `62386fab8cc0e0ca6fe09d94db6226bb7dfa6e16c9766943a2cb382a8f543ebb`; capture lines 72–74:
  `"GoogleAccessId": service_account_name,` / `"Expires": expiration,` / `"Signature": signature,`.
  Located quote (3 words): **`"GoogleAccessId": service_account_name,`**

**L2 — CloudFront signed cookies (`CloudFront-Signature`, `CloudFront-Key-Pair-Id`).**
- `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-custom-policy.html`
  — HTTP 200, raw 51673 bytes, snapshot sha256 `ddf45b805c7f67f29cf15f60f805fd636968f14734f4e342c697760f8b49f1cc`;
  capture lines 17–19. Located quote (9 words): **`CloudFront-Signature, and CloudFront-Key-Pair-Id.`**
- `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-canned-policy.html`
  — HTTP 200, raw 36439 bytes, snapshot sha256 `d6fccb868f4a8367da95912ee818d2a00807575ed23419c7b2395c5aaff3994c`;
  capture lines 17–18. Located quote (5 words): **`CloudFront-Expires, CloudFront-Signature, and`**
- `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-signed-cookies.html`
  — HTTP 200, raw 24668 bytes, snapshot sha256 `a78303e45bda077ffe9f310860589546ab29d67b4221c8e032c06ea08404dd43`;
  capture line 102. Located quote (5 words): **`In the CloudFront-Expires attribute, specify the shortest`**

**L3 — Azure user-delegation SAS example URI (`skoid`/`sktid`/`skv` beside `sig`).**
`https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas` — HTTP 200,
raw 118382 bytes, snapshot sha256 `56d858ac8c2988fdf95a045b5a75f13cc5a28a1f71b3786638522775b1786cd6`;
capture line 870 carries the whole query, and the table that follows names each part
(`skoid=` at 891, `sktid=` at 894, `skv=` at 906, `sig=` at 921). Located quote (one URL, 6 words):
**`myaccount.blob.core.windows.net/sascontainer/blob1.txt?sp=rw&st=…&skoid=<object-id>&sktid=<tenant-id>&…&skv=2022-11-02&…&sig=<signature>`**
— all values are the page's own placeholders; no credential value is present.

**L4 — HackerOne attachment `expiring_url` format.**
`https://api.hackerone.com/hacker-reference/` — HTTP 200, raw 155762 bytes, snapshot sha256
`ee5d92ed5a36287bb07f7367cb46901c8caf5da2c0a2021b5c198b699eba97f4`; the field is `» expiring_url`
(type string, required true) at capture lines 246–251. Located quote (13 words):
**`A temporary, pre-signed URL to download the attachment file directly.`**
The JSON example at lines 90 and 205 shows the same field on the `attachments.s3.amazonaws.com`
host; the path segment of that example is an opaque HackerOne attachment id, not a credential, and
is not reproduced in the receipts.

**Bonus L5 — Google Cloud CDN signed URL (`Expires` + `KeyName` + `Signature`).**
`https://cloud.google.com/cdn/docs/using-signed-urls` — HTTP 200, raw 284631 bytes, snapshot
sha256 `76aac52e38e5f9f5c96c2b0ec24b98e76ab259bb63ac8630a86f06cf16a32010`; capture lines 884 and
891 show complete placeholder query strings. Located quote (1 URL, 6 words):
**`https://example.com/PATH?Expires=EXPIRATION&KeyName=KEY_NAME&Signature=SIGNATURE`**
Not requested, but it is the one first-party page found that renders a complete signed-URL query
for a Google signing scheme. Note the shape uses `KeyName=`, not `Key-Pair-Id=`, so the round-89
CloudFront rule would not fire on it either.

## 4. Credential hygiene

- No credential-shaped value was written into anything under
  `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/`. No planted or real
  session-token, object-signature, Azure SAS, or CloudFront signature value; no AWS access-key id
  of any kind; no private-key header; no `token=`/`secret:` value. The AWS example signature
  values and the Azure example URI were read in scratch only and never transcribed; the receipts
  carry parameter names, shapes, digests and placeholder values.
- The landed scanner was run over this report and all five receipts:
  `CAPTURE-SECRET-SCAN mode=files scanned=6 hits=0 files=0 allowed=0 unused_allow=0 rc=0`.
- No scanner, counter, or `S<digits>.txt` snapshot was copied into the wave dir; no snapshot bytes
  are reproduced in the receipts.
- The scratch root was removed at yield (`rm -rf -- /fast/scratch/hyaku/kasegi-r89/ScoutSources`);
  it is gone. The lane tree outside the wave dir was not touched; `git status` shows the wave dir
  as the only addition under `.ufo/waves/round-89/w1/`.

## 5. Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/ScoutSources.md` (this report)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/ScoutSources-receipts/live-recapture-r89.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/ScoutSources-receipts/manifest-quote-recheck-r89.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/ScoutSources-receipts/s129-rejection-r89.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/ScoutSources-receipts/round90-leads-r89.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-89/w1/ScoutSources-receipts/scanner-gap-probe-r89.txt`

## 6. Open items for the L1

1. The S129 flip condition ("a first-party capture that shows a V2 signed URL's query parameters
   as text") is now satisfiable from Google's own client-library sources (L1a/L1b/L1c). A docs
   page still does not show it; a round-90 source row would have to be scoped as library source,
   not documentation, and would carry the `GoogleAccessId`/`Expires`/`Signature` triple.
2. Two coverage candidates, each falsifiable by the commands in the probe receipt:
   cloudfront-signed-cookie (needs its own name pattern, its own separator handling and its own
   length floor — AWS's own example value is 28 characters) and gcs-v2-signed-url (needs the V2
   parameter names, not `X-Goog-Signature`).
3. No findings were routed as defects against the round-89 frozen claims: every frozen predicate
   re-verified at the landing commits.

No tooling was installed or upgraded for this seat (no pacman, no uv tool, no npm).
