# Cloud signed-URL credentials in captured evidence — a Cloud Storage V4 signed URL, an Azure service SAS and an Amazon CloudFront signed URL are bearer credentials inside a captured page, HAR or JSON until expiry, the lane's scanner names all three shapes, and the redaction rule strips the query string while keeping the host and path

source: S126 — Google Cloud Storage documentation, Signed URLs — https://docs.cloud.google.com/storage/docs/access-control/signed-urls — anchor `corpus/source-snapshots/round-88/S126.txt:423-424` and `corpus/source-snapshots/round-88/S126.txt:487-488` (capture 584 lines, 18,245 bytes, sha256 b04de8a94c7905d8b768b8dcd7d7e354df3f972ef292bb3e1a1f36aea000b83d; manifest `corpus/source-snapshots/round-88/manifest.json` records Q01-possession at anchor 424 and Q02-signature-param at anchor 487, each `occurrences=1`); S127 — Azure Storage REST API reference, Create a service SAS — https://learn.microsoft.com/en-us/rest/api/storageservices/create-service-sas — anchor `corpus/source-snapshots/round-88/S127.txt:402-404`, `corpus/source-snapshots/round-88/S127.txt:599`, `corpus/source-snapshots/round-88/S127.txt:601`, `corpus/source-snapshots/round-88/S127.txt:605`, `corpus/source-snapshots/round-88/S127.txt:631-633`, `corpus/source-snapshots/round-88/S127.txt:638-639` (capture 663 lines, 38,072 bytes, sha256 66f8a35e9d598e5f5eecedd9003a7ba7f99c1eda24963e4cf1891245bdfb1312; manifest Q01-sig-hmac-base64 at anchor 404 and Q02-example-uri at anchor 605, each `occurrences=1`); S128 — Amazon CloudFront Developer Guide, Create a signed URL using a canned policy — https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html — anchor `corpus/source-snapshots/round-89/S128.txt:13`, `:56-57`, `:58-59`, `:62`, `:70`, `:77`, `:82-83`, `:94-96`, `:202`, `:206-211`, `:212` (capture 225 lines, 11,207 bytes, sha256 cd246e7debb4ea67cccf783ac6b16307b1d0febbda9de133df29a5ada5ea3331; manifest `corpus/source-snapshots/round-89/manifest.json` records Q01-signature-param at anchor 70, Q02-key-pair-id at anchor 77 and Q03-urlsafe-replacement at anchor 202, each `occurrences=1`); S130 — Amazon CloudFront Developer Guide, Create a signed URL using a custom policy — https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-custom-policy.html — anchor `corpus/source-snapshots/round-89/S130.txt:14`, `:66`, `:70-73`, `:75-84`, `:161-165` (capture 422 lines, 19,858 bytes, sha256 dcdaa1233df06b7304bc29c8af89371d81e7b0fa816251532ef9c52c8356ca39; manifest Q01-anyone-with-url at anchor 163 and Q02-policy-param at anchor 66, each `occurrences=1`)
verified-at: 2026-11-07 (re-opened at the pinned bytes: `sha256sum` prints S126 `b04de8a9…` and S127 `66f8a35e…`, equal to the manifest `sha256`; `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-88/manifest.json --source S126` prints `S126:sha256 OK` plus two `Q0n … OK occurrences=1 anchor=N-ok` lines, rc 0, and `--source S127` prints the same shape of output, rc 0; `python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-88/S126.txt corpus/source-snapshots/round-88/S127.txt` prints `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=17 rc=0`; the manifest records both captured 2026-11-07T03:30:10Z and a byte-identical second fetch; round-89 extension re-opened 2026-11-07: `sha256sum` prints S128 `cd246e7d…` and S130 `dcdaa123…`, equal to the round-89 manifest `sha256`; `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-89/manifest.json --source S128` prints `S128:sha256 OK` plus three `Q0n … OK occurrences=1 anchor=N-ok` lines, rc 0, and `--source S130` prints `S130:sha256 OK` plus two, rc 0; `python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-89/S128.txt corpus/source-snapshots/round-89/S130.txt` prints `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=2 unused_allow=17 rc=0` (the two documentation example signatures consumed the two round-89 allowlist rows); the round-89 manifest records them captured 2026-11-07T05:14:06Z and 2026-11-07T05:14:09Z)
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-88/manifest.json --source S126 && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-88/manifest.json --source S127 && python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-88/S126.txt corpus/source-snapshots/round-88/S127.txt && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-89/manifest.json --source S128 && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-89/manifest.json --source S130 && python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-89/S128.txt corpus/source-snapshots/round-89/S130.txt

## Attribution

S126 is Google Cloud's own Signed URLs page (`corpus/SOURCES.md:138`, tier A): every sentence here about a Cloud Storage signed URL being usable by whoever holds it, being limited in time, or being invalidated by key rotation is Google's statement about Cloud Storage, not a claim about any other provider's signed URL. S127 is Microsoft's own Create a service SAS reference (`corpus/SOURCES.md:139`, tier A): every sentence about `sig` being an HMAC-SHA256, about `sv=`, about `se=`, or about revocation by stored access policy or account-key regeneration is Microsoft's statement about the service SAS form, not a claim about the account SAS, the user-delegation SAS, or any other provider. S128 and S130 are AWS's own CloudFront Developer Guide pages (`corpus/SOURCES.md:140` and `:142`, tier A): every sentence here about a CloudFront signed URL's parameters, its URL-safe signature alphabet, or its bearer behavior is AWS's statement about CloudFront signed URLs, not about CloudFront signed cookies or S3 presigned URLs — the registry rows scope them that way.

The two captures do not overlap in provider. `grep -ciE 'azure|shared access signature|\bsas\b' corpus/source-snapshots/round-88/S126.txt` prints `0`, and `grep -ciE 'google|x-goog|cloud storage|gcs' corpus/source-snapshots/round-88/S127.txt` prints `0` (FC-5). The word "bearer" is this lane's reading, not either vendor's word: Google states possession is sufficient (Claim 1), Microsoft states the signature authorizes the request and names what revokes it (Claims 3-4) — the conjunction is why a captured URL is handled as a credential. The round-89 pair does not overlap another provider either: `grep -ciE 'azure|shared access signature|\bsas\b'` prints `0` on each of S128 and S130, `grep -ciE 'google|x-goog|cloud storage|gcs'` prints `0` on each, and `grep -ciE 'cloudfront'` prints `0` on both round-88 captures (FC-5).

The scanner is the lane's instrument, `corpus/instruments/capture-secret-scan.py` (capability row `SCORECARD.md:307`); its shape set, path scope, output and limits are a lane design choice, not a vendor statement, and every sentence in Claim 5 is about the instrument's own bytes.

## Claim 1 — an active Cloud Storage V4 signed URL authorizes whoever holds it, and the authority sits in the query string

> "time-limited access to a specific Cloud Storage resource. Anyone in possession of the signed URL can use it while it's active, regardless of whether" — `corpus/source-snapshots/round-88/S126.txt:423-424`

The sentence continues at `corpus/source-snapshots/round-88/S126.txt:425` with "they have a valid account." Lane reading: possession of the URL is the whole test for the window — no account, no session, no header, no cookie. A capture that preserves this URL verbatim preserves the credential.

> "Signed URLs contain authentication information, including a signature, in their query string" — `corpus/source-snapshots/round-88/S126.txt:433-434`

So the carrier is the URL string itself: a rendered page that embeds it, a HAR that records a request URL, a JSON field that holds it. This lane's capture class — a snapshot of a served page under `corpus/source-snapshots/`, a practice package's copy under `corpus/practice/<pkg>/evidence/` — is exactly the class that keeps such a string byte-for-byte.

One scope note from the same page: "Signed URLs can only be used to access resources in Cloud Storage through XML API endpoints" (`corpus/source-snapshots/round-88/S126.txt:429-430`). A `storage.googleapis.com` bucket or object URL is the endpoint class involved; a URL from another Google API does not take this shape.

## Claim 2 — the parameter names the credential, and the window is `X-Goog-Expires` measured from `X-Goog-Date`

> "X-Goog-Expires: The length of time the signed URL remained valid, measured in seconds from the value in X-Goog-Date." — `corpus/source-snapshots/round-88/S126.txt:481-482`

> "X-Goog-Signature: The authentication string that allowed requests using this signed URL to access cat.jpeg." — `corpus/source-snapshots/round-88/S126.txt:487-488`

Lane reading: the window is arithmetic on two parameters inside the URL, and the page's own cap is "the longest expiration value is 604800 seconds (7 days)" (`corpus/source-snapshots/round-88/S126.txt:483-484`). The parameter list names six fields: `X-Goog-Algorithm` (`:476`), `X-Goog-Credential` (`:477`), `X-Goog-Date` (`:479`), `X-Goog-Expires` (`:481`), `X-Goog-SignedHeaders` (`:485`) and `X-Goog-Signature` (`:487`). The one that authorizes is the signature, which is why the lane's detector keys on that parameter name rather than on a bucket host.

Two consequences for a capture: the URL states its own end instant, so priority can be computed from the record without contacting anything; and the end instant is at most a week after the start, so an old capture is usually outside the window while a fresh one is inside it. The window bounds use, not publication: a capture pushed inside the window is a disclosure incident whatever its usability afterwards, and the bytes do not change when the clock passes.

## Claim 3 — an Azure service SAS puts the authorizing HMAC in `sig=`, beside the `sv=` version parameter

> "The signature is a hash-based message authentication code (HMAC) that you compute over the string-to-sign and key by using the SHA256 algorithm" — `corpus/source-snapshots/round-88/S127.txt:402-404`

> "&spr=https&sv=2022-11-02&sr=b&sig=<signature>" — `corpus/source-snapshots/round-88/S127.txt:605`

> "The signature is an HMAC that's computed over a string-to-sign and key by using the SHA256 algorithm" — `corpus/source-snapshots/round-88/S127.txt:639`

The table at `corpus/source-snapshots/round-88/S127.txt:402-404` puts the field name, the query parameter (`sig`, `:403`) and the meaning on consecutive lines; `corpus/source-snapshots/round-88/S127.txt:638` repeats the cell as `sig=<signature>` and `:639` says what it authorizes. The documented example URI at `:605` shows the SAS as query parameters appended to a blob URL — `sp=rw` permissions, `st=` start, `se=` expiration, `sip=` IP range, `spr=https` protocol, `sv=` version, `sr=b` resource, `sig=<signature>` signature — with the table at `:606-639` describing each one.

The literal `sig=<signature>` occurs twice in the capture, inside the example URI at `:605` and as the table cell at `:638`; FC-1 declares that expected count of 2. The rest of the entry's quotes are exactly-once.

Lane reading: the value is Base64 of an HMAC-SHA256, so its alphabet is `A-Za-z0-9+/` with `=` padding, and inside a URL it may be percent-encoded (`+` as `%2B`, `/` as `%2F`, `=` as `%3D`). A 32-byte HMAC in Base64 is 44 characters including one trailing `=`; that is the arithmetic behind the detector's 40-character floor and its `[A-Za-z0-9%+/]` alphabet with up to two trailing `=`/`%3D` (`corpus/instruments/capture-secret-scan.py:151`, `:162-163`).

## Claim 4 — expiry bounds use; revocation needs a policy or key action, so a captured SAS is a credential until then

> "Anyone who knows the URL can access the resource until the expiration time for the URL is reached" — `corpus/source-snapshots/round-88/S126.txt:450-451`

The same sentence ends at `corpus/source-snapshots/round-88/S126.txt:452` with "used to sign the URL is rotated": Google names two ways the authority ends — the clock and rotation of the signing key.

> "Regenerating the account key is the only way to immediately revoke an ad hoc SAS." — `corpus/source-snapshots/round-88/S127.txt:599`

> "A shared access signature URI is associated with the account key that's used to create the signature" — `corpus/source-snapshots/round-88/S127.txt:601`

Microsoft lists the ends of a SAS on the same page: the expiration time, reached by the interval elapsing or by editing the stored access policy to a past time (`corpus/source-snapshots/round-88/S127.txt:596`), deletion of the referenced stored access policy (`:597`), and regeneration of the account key (`:599`). With no stored access policy, `:601` says the only revocation is changing the account key. Lane reading: an ad hoc SAS in a capture cannot be selectively withdrawn by the party that published the capture — the available fixes are redacting the capture (Claim 6) or rotating the key, and only the first is available after publication.

## Claim 5 — what the lane's scanner detects, and where it looks

The docstring at `corpus/instruments/capture-secret-scan.py:1-132` is the specification this entry reads.

**Scope.** `--rev REV` reads a git tree without checkout and scans capture-class paths only: anything under `corpus/source-snapshots/`, anything under a practice package's `corpus/practice/<pkg>/evidence/` (added round 88), any path with a directory segment ending in `-receipts`, and any file whose name starts with `live-` (`corpus/instruments/capture-secret-scan.py:14-21`). `--files PATH...` scans exactly the named working-tree files whatever their path, and the docstring's instruction is to run it "on every capture before the commit that first adds it" (`:20-21`).

**Shapes.** The claim-package gate's `SECRET_PATTERNS`, imported from `claim-package-check.py` beside the instrument so the two never drift, plus the two AWS shapes, the two round-88 cloud shapes and the round-89 CloudFront shape (`corpus/instruments/capture-secret-scan.py:23-66`):

- `gcs-signed-url-signature` — `X-Goog-Signature=<hex>` (query string) or `X-Goog-Signature: <hex>` (header, JSON key) with 64 or more hex digits: a Cloud Storage V4 signed URL's signature (`:32-36`; pattern `:132-133`).
- `azure-sas-signature` — a `sig=` query parameter of 40 or more base64/percent-encoded characters in the same query as an `sv=YYYY-MM-DD` storage-version parameter, either order, separated by `&`, `&amp;` or JSON `\u0026` (`:37-46`; pattern `:134-135`, with up to 20 intervening parameters); round 89 admits a match that starts right after a `\u0026` or `%26` separator, and the selftest pins S127's documented parameter order (`sv=` sixth) as detected (`:297`).
- `cloudfront-signed-url-signature` — a `Signature=` query parameter of 40 or more CloudFront URL-safe base64 characters in the same query as a `Key-Pair-Id=` of 8-32 upper-case letters or digits, either order, separated by `&`, `&amp;` or JSON `\u0026`, parameter names case-sensitive, up to 20 other parameters between (`:53-66`; pattern `:126-137`); a `Signature=` preceded by `-` (`X-Amz-Signature=`) never starts a match (`:126`).

**Output.** Never the matched value: `HIT shape=<s> path=<p> line=<n>` per file and shape, first non-allowed match, then `CAPTURE-SECRET-SCAN mode=<m> scanned=<n> hits=<h> files=<f> allowed=<a> unused_allow=<u> rc=<rc>` (`:99-103`; `report()` at `:234-246`). `rc = 1 if hits else 0` (`:243`); exit 2 on a usage or read error (`:104`). A receipt carrying those lines is safe to commit where the fixture is not.

**Allowlist.** `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason` — one exact matched value at one path, so a different value at the same path and shape is still a hit (`:90-97`); rows for `aws-sts-session-token` are refused and a refused or malformed row is exit 2 (`:95-97`; `NEVER_ALLOWED` at `:142`); the documented AWS example key id is the single built-in allowed value (`:88`; `ALLOWED_VALUES` at `:141`). A cloud signature can be bound by such a row — that is the mechanism for a vendor's own documented example, not for a live URL — while a session token cannot be bound at all. Round 89 adds two rows binding AWS's CloudFront documentation example signature at the two round-89 snapshot paths (`corpus/instruments/capture-secret-allow.tsv:21-22`); the two captures read clean only under those rows (FC-9).

**Named limits**, verbatim from `corpus/instruments/capture-secret-scan.py:106-115` (round-91 text; round 92 prepends fine-grained `github_pat_` tokens at `:106-107`): GCS V2 `GoogleAccessId=`/`Signature=` URLs, CloudFront signed cookies held as HAR/JSON name/value objects (`"name":"CloudFront-Signature"`), percent-encoded parameter names or `=` (a whole URL percent-encoded inside another URL's query), Azure SAS parameter names of 8+ letters between `sv` and `sig`, more than 20 other parameters between the two matched ones, values soft-wrapped across lines, and gzip/UTF-16/base64-wrapped captures are not detected. Until round 91 the list named CloudFront signed cookies outright; round 91 added the `cloudfront-signed-cookie-signature` shape (`corpus/instruments/capture-secret-scan.py:67-80`, sourced on S134) and kept only the HAR/JSON object form as a limit.

Six further limits follow from the frozen patterns and the instrument's own selftest, and are named here so a clean run is not over-read:

- the Azure shape requires `sv=YYYY-MM-DD` in the same query; the page dates that parameter from storage service version 2012-02-12 ("For Azure Storage version 2012-02-12 and later, this parameter indicates the version to use", `corpus/source-snapshots/round-88/S127.txt:631-633`), and the selftest pins `azure-sig-without-sv` as not detected (`corpus/instruments/capture-secret-scan.py:337`);
- the GCS shape requires 64 or more **contiguous** hex digits after the parameter name. The page's own example signature is wrapped at 80-character lines (`corpus/source-snapshots/round-88/S126.txt:466-473`, 512 hex digits over 8 lines), and the selftest pins exactly that wrapped case as not detected (`corpus/instruments/capture-secret-scan.py:330`, case `gcs-doc-wrapped`, expected evidence set empty). A capture that hard-wraps a signed URL therefore reads clean while carrying the signature — measured in FC-7;
- the thresholds are shape-sized, not credential-sized: `gcs-short` (32 hex, `:289`), `azure-short-sig` (12 characters, `:296`), `cf-short-sig` (`:305`) and `cf-lowercase-names` (`:306`) are pinned as not detected, and `azure-doc-placeholder` (the vendor's `<signature>` placeholder, `:294`) and `cf-doc-placeholder` (`:302`) are pinned as clean, so a HIT reports a matching shape and never proves liveness;
- the GCS shape matches the parameter name literally, so a percent-encoded parameter name is the docstring's percent-encoded-name limit restated for this shape.
- the round-88 `\u0026` limit is closed: the left boundary `_LB` (`corpus/instruments/capture-secret-scan.py:153`) admits a match that starts right after `\u0026` or `%26`, so a JSON-escaped copy of the documented example URI (`corpus/source-snapshots/round-88/S127.txt:605`, `sv=` sixth) is detected and the selftest pins that order (`corpus/instruments/capture-secret-scan.py:339`, case `azure-json-escaped-s127-order`). What remains: `%26` is a left boundary only, not a separator inside the span (`_SEP` at `corpus/instruments/capture-secret-scan.py:149` is `&`, `&amp;`, `\u0026`), so a query whose parameters are joined by `%26` is not spanned; and at most 20 intervening parameters with 2-7 letter names are spanned (`:150`; 2-6 until round 91, widened for the user-delegation field `skdutid`, S133).
- the CloudFront URL shape needs `Key-Pair-Id=` in the same query and 40 or more signature characters: `cf-sig-without-kpi` (`:303`), `cf-amz-signature-beside-kpi` (`:304`), `cf-short-sig` (`:305`) and `cf-lowercase-names` (`:306`) are pinned as not detected, `cf-doc-placeholder` (`:302`) as clean; CloudFront signed cookies (`CloudFront-Signature=`) are outside this shape and, since round 91, matched by the separate `cloudfront-signed-cookie-signature` shape (`:67-80`, `:138-139`); a `%26`-separated CloudFront query is not spanned for the same reason as the Azure shape (`:126`).

## Claim 6 — the operating rule: scan every capture before its first commit, strip the query string, keep host/path and both digests

> "Every JSON string value containing `X-Amz-` keeps its scheme/host/path and loses its query string" — `.ufo/waves/round-86/l1/redact-presigned.py:5-6`

That line is the lane's round-86 redaction tool, written for the AWS shape; the rule it implements is provider-neutral. All three vendors put the authorizing value in the query string (Claims 1, 3 and 7), and scheme/host/path is what keeps the record readable — which bucket, which object, which blob, which distribution path. Stripping the query of a Cloud Storage URL removes `X-Goog-Signature`; stripping the query of an Azure URI removes `sig=`; stripping the query of a CloudFront URL removes `Signature=` (and `Policy=`/`Expires=` with it). In every case the residue is a locator, not a credential.

The second half of the rule is the digest pair. The round-86 manifest records the committed `sha256` beside `redaction.pre_redaction_sha256`, `pre_redaction_bytes`, `strings`, `tool` and `applied_utc` (`corpus/source-snapshots/round-86/manifest.json`, `sources[S122].redaction`). The round-88 captures needed no redaction: the scanner reads both clean (FC-3) and neither manifest record carries a `redaction` block (FC-6), so their `sha256` is the served digest as well as the committed one. The round-89 captures also needed none: the scanner reads both clean under the two digest rows (FC-9), neither round-89 manifest record carries a `redaction` block (FC-6), and the only signature-shaped bytes in them are AWS's documentation example, which the two rows bind at those two paths.

## Claim 7 — an Amazon CloudFront signed URL puts its authorizing `Signature` in the query string beside `Key-Pair-Id`, in one of two parameter sets (round 89)

> "When you create a signed URL using a canned policy, the Signature parameter is a hashed and signed version of a policy statement." — `corpus/source-snapshots/round-89/S128.txt:94-95`

> "A hashed, signed, and base64-encoded version of the JSON policy statement." — `corpus/source-snapshots/round-89/S130.txt:77-78`

Lane reading: the authorizing value is the `Signature` query parameter, and it is a signature over a policy statement. The canned form signs a policy the URL does not carry; the custom form carries that policy in `Policy=`. Either way the credential travels inside the URL, so a capture that keeps the URL verbatim keeps the credential.

**The two parameter sets.** Canned policy: `Expires=`, `Signature=`, `Key-Pair-Id=`, optional `Hash-Algorithm=` (`corpus/source-snapshots/round-89/S128.txt:56-57`, `:70`, `:74`, `:84`). Custom policy: `Policy=`, `Signature=`, `Key-Pair-Id=`, optional `Hash-Algorithm=` (`corpus/source-snapshots/round-89/S130.txt:66`, `:75`, `:79`, `:90`). The difference is where the policy lives, not whether the signature authorizes: AWS's canned-policy page says the canned `Signature` is a signed policy statement and that the statement is not included in the URL, while the custom-policy page's `Policy=` is that statement (`corpus/source-snapshots/round-89/S128.txt:94-96`, `corpus/source-snapshots/round-89/S130.txt:66-69`).

> "Expires=date and time in Unix time format (in seconds) and Coordinated Universal Time (UTC)" — `corpus/source-snapshots/round-89/S128.txt:56-57`

> "The date and time that you want the URL to stop allowing access to the file." — `corpus/source-snapshots/round-89/S128.txt:58-59`

> "Policy=base64 encoded version of" — `corpus/source-snapshots/round-89/S130.txt:66`

> "The policy statement controls the access that a signed URL grants to a user." — `corpus/source-snapshots/round-89/S130.txt:70-71`

Lane reading of the window: the canned form states its own end instant in `Expires=` as Unix seconds in UTC, and the page's own arithmetic dates the example's instant — "January 1, 2026 10:00 am UTC converts to 1767290400" (`corpus/source-snapshots/round-89/S128.txt:62`; the same sentence recurs at `:154-155`), which is before this round's 2026-11-07 capture, so the documented example URL is outside its own window. The custom form states the end inside the base64 `Policy=` JSON, whose description names "an expiration date and time" (`corpus/source-snapshots/round-89/S130.txt:70-73`), so the URL still carries the end instant, encoded rather than plain.

**The URL-safe alphabet.** AWS's own replacement rule:

> "Replace characters that are invalid in a URL query string with characters that are valid." — `corpus/source-snapshots/round-89/S128.txt:202`

> "+ - (hyphen) = _ (underscore) / ~ (tilde)" — `corpus/source-snapshots/round-89/S128.txt:206-211`

The table maps `+` to `-`, `=` to `_` and `/` to `~`, so a CloudFront signature's alphabet is `A-Za-z0-9` plus `-`, `_` and `~`. The `~` is the distinguishing byte — a value carrying it is neither plain base64 nor the common base64url spelling — and the detector's class admits all three substitutions (`corpus/instruments/capture-secret-scan.py:156`).

> "Append the resulting value to your signed URL after &Signature=, and return to" — `corpus/source-snapshots/round-89/S128.txt:212`

**The bearer statement.** AWS states the possession property as the consequence of a broad policy, not as a universal rule:

> "anyone with the signed URL can access all of the files in any distribution that is associated" — `corpus/source-snapshots/round-89/S130.txt:163`

The sentence is the caution attached to omitting `Resource` from the policy (`corpus/source-snapshots/round-89/S130.txt:161-165`): with `Resource` present the URL covers the named file or wildcard pattern, and with it omitted the URL covers every file in every distribution of the key pair. Lane reading: the URL is a bearer credential for whatever the policy covers; the policy's breadth is the blast radius, not the credential's kind. The trust anchor is the key pair — `Key-Pair-Id` names the public key CloudFront validates with, and "This public key must belong to a key group that is a trusted signer in the distribution" (`corpus/source-snapshots/round-89/S128.txt:82-83`).

**Scanner shape.** `cloudfront-signed-url-signature` (`corpus/instruments/capture-secret-scan.py:53-66`; pattern `:154-165`): a `Signature=` of 40 or more URL-safe characters in the same query as a `Key-Pair-Id=` of 8-32 upper-case letters or digits, either order, separated by `&`, `&amp;` or JSON `\u0026`, parameter names case-sensitive, up to 20 other parameters between, and a `Signature=` preceded by `-` never starts a match — so an S3 `X-Amz-Signature=` is not read as a CloudFront signature. The selftest pins four detected cases (`cf-canned`, `cf-custom`, `cf-kpi-first-json`, `cf-html-amp`, `:340-343`) and five clean ones (`cf-doc-placeholder`, `cf-sig-without-kpi`, `cf-amz-signature-beside-kpi`, `cf-short-sig`, `cf-lowercase-names`, `:344-348`).

**Limits of this shape**, so a clean run is not over-read:

- a `Signature=` with no `Key-Pair-Id=` in the same query is not detected (`cf-sig-without-kpi`, `corpus/instruments/capture-secret-scan.py:345`);
- the bounds are 40 signature characters and 8 key-id characters (`:128-129`), so a shorter value is outside the shape (`cf-short-sig`, `:305`);
- parameter names are case-sensitive, so lowercase names are not detected (`cf-lowercase-names`, `:306`);
- CloudFront **signed cookies** are outside the URL shape: a cookie is not a query parameter, and `-` before `Signature=` keeps `CloudFront-Signature=` from starting a URL-shape match; since round 91 the separate `cloudfront-signed-cookie-signature` shape matches the cookie pair (`:67-80`), and only its HAR/JSON name/value object form stays a named limit (`:81-87`);
- `%26` is a left boundary only (`:126`), so a match may start after it but the separator set inside the span is `&`, `&amp;`, `\u0026` (`:121`) — a `%26`-joined query is not spanned;
- more than 20 intervening parameters, percent-encoded parameter names, soft-wrapped values, and gzip/UTF-16/base64-wrapped captures are outside the shape (`:81-87`);
- the two round-89 captures read clean only because AWS's documentation example signature is bound by two digest rows (`corpus/instruments/capture-secret-allow.tsv:21-22`); the same bytes at another path, or a different signature at the same path, is a hit (Claim 5's allowlist rule).

## How a researcher uses this

1. **Scan the file, not the directory, before the first commit.** `--files` names exactly the working-tree paths about to be added (`corpus/instruments/capture-secret-scan.py:20-21`); run it on each new capture and paste the `CAPTURE-SECRET-SCAN … rc=` line into the round receipt.
2. **Read a cloud hit as the authorizing field.** `gcs-signed-url-signature` is the `X-Goog-Signature` query parameter of Claim 2; `azure-sas-signature` is the `sig=` parameter beside `sv=` of Claim 3; `cloudfront-signed-url-signature` is the `Signature=` parameter beside `Key-Pair-Id=` of Claim 7. None is a false-positive class by default; a digest-bound allowlist row can name a vendor's documented example, and no row can name a session token (`:95-97`).
3. **Redact the query and keep the locator.** Strip `?…`, keep `scheme://host/path` (Claim 6), and record the pre-redaction digest beside the committed one.
4. **Read the window from the URL before deciding urgency.** GCS: `X-Goog-Date` + `X-Goog-Expires` (Claim 2). Azure: `se=` (`corpus/source-snapshots/round-88/S127.txt:623`) with revocation by stored access policy or account key (Claim 4). CloudFront: `Expires=` for a canned policy or the `Policy=` JSON's expiration for a custom one (`corpus/source-snapshots/round-89/S128.txt:56-59`, `corpus/source-snapshots/round-89/S130.txt:70-73`), with no lane-side revocation at all — only expiry or rotating the key pair. Expiry bounds use, not publication.
5. **Treat a clean run as "no matching shape", not "no credential".** The shapes are the three cloud ones plus the gate's and AWS sets (`:23-66`); the scope is path-based (`:14-21`); the limits are `:81-87`.
6. **Practice packages are in scope by design.** A package that copies a capture under `corpus/practice/<pkg>/evidence/` is scanned on the same terms as `corpus/source-snapshots/` (`:16-17`), so a capture moved into a practice package does not leave the covered set.

## Falsifiable rule and checks

**Falsifiable rule.** Any sentence asserting that a capture holding an active Cloud Storage V4 signed URL, an Azure service SAS or an Amazon CloudFront signed URL is credential-free is falsified by `python3 -B corpus/instruments/capture-secret-scan.py --files <capture>` exiting 1 with a `HIT shape=gcs-signed-url-signature`, `HIT shape=azure-sas-signature` or `HIT shape=cloudfront-signed-url-signature` line. Any sentence asserting that an Azure ad hoc SAS can be revoked without a policy or key action is falsified by `corpus/source-snapshots/round-88/S127.txt:599` and `:601`. Any sentence asserting that a Cloud Storage signed URL grants nothing to its holder is falsified by `corpus/source-snapshots/round-88/S126.txt:423-424`. Any sentence asserting that a CloudFront signed URL grants nothing to whoever holds it is falsified by `corpus/source-snapshots/round-89/S130.txt:163`. Any sentence asserting the scanner catches every signed-URL form is falsified by `corpus/instruments/capture-secret-scan.py:106-115`.

**FC-1 — every quoted span is verbatim, anchored, within 25 words, and occurs the declared number of times (`normalized=whitespace`).**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
def norm(s): return ' '.join(s.split())
Q = [
 ('S126','corpus/source-snapshots/round-88/S126.txt',423,424,1,"time-limited access to a specific Cloud Storage resource. Anyone in possession of the signed URL can use it while it's active, regardless of whether"),
 ('S126','corpus/source-snapshots/round-88/S126.txt',433,434,1,"Signed URLs contain authentication information, including a signature, in their query string"),
 ('S126','corpus/source-snapshots/round-88/S126.txt',450,451,1,"Anyone who knows the URL can access the resource until the expiration time for the URL is reached"),
 ('S126','corpus/source-snapshots/round-88/S126.txt',481,482,1,"X-Goog-Expires: The length of time the signed URL remained valid, measured in seconds from the value in X-Goog-Date."),
 ('S126','corpus/source-snapshots/round-88/S126.txt',487,488,1,"X-Goog-Signature: The authentication string that allowed requests using this signed URL to access cat.jpeg."),
 ('S127','corpus/source-snapshots/round-88/S127.txt',402,404,1,"The signature is a hash-based message authentication code (HMAC) that you compute over the string-to-sign and key by using the SHA256 algorithm"),
 ('S127','corpus/source-snapshots/round-88/S127.txt',599,599,1,"Regenerating the account key is the only way to immediately revoke an ad hoc SAS."),
 ('S127','corpus/source-snapshots/round-88/S127.txt',601,601,1,"A shared access signature URI is associated with the account key that's used to create the signature"),
 ('S127','corpus/source-snapshots/round-88/S127.txt',605,605,1,"&spr=https&sv=2022-11-02&sr=b&sig=<signature>"),
 ('S127','corpus/source-snapshots/round-88/S127.txt',638,638,2,"sig=<signature>"),
 ('S127','corpus/source-snapshots/round-88/S127.txt',639,639,1,"The signature is an HMAC that's computed over a string-to-sign and key by using the SHA256 algorithm"),
]
bad = 0
for sid, p, a, b, want, q in Q:
    raw = open(p, encoding='utf-8').read().split('\n')
    n = norm('\n'.join(raw)); nq = norm(q)
    got = n.count(nq)
    span = norm('\n'.join(raw[a-1:b]))
    ok = got == want and nq[:40] in span and len(nq.split()) <= 25
    bad += not ok
    print('%s:%d-%d occurrences=%d expected=%d anchored=%s words=%d %s'
          % (sid, a, b, got, want, 'y' if nq[:40] in span else 'n', len(nq.split()), 'OK' if ok else 'FAIL'))
print('QUOTE-CHECK %s spans=%d bad=%d' % ('pass' if not bad else 'fail', len(Q), bad))
raise SystemExit(1 if bad else 0)
PY
```

Measured 2026-11-07: eleven `OK` lines and `QUOTE-CHECK pass spans=11 bad=0`, rc 0.

**FC-2 — the missing-source and corrupted-source controls fail closed.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-88/manifest.json --source S999; echo "missing_rc=$?"
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9
cp corpus/source-snapshots/round-88/S126.txt corpus/source-snapshots/round-88/manifest.json "$T"/ \
  && python3 -B -c "import sys;p=sys.argv[1]+'/S126.txt';b=bytearray(open(p,'rb').read());b[100]^=0x20;open(p,'wb').write(b)" "$T" \
  && python3 -B corpus/instruments/source-recheck.py --manifest "$T/manifest.json" --source S126; echo "corrupt_rc=$?"
rm -rf -- "$T"
```

Measured 2026-11-07: `S999:source UNAVAILABLE reason=not-listed` with `missing_rc=2`, and `S126:sha256 MISMATCH expected=b04de8a9… actual=b5b7c4a3…` with `corrupt_rc=1`.

**FC-3 — the pinned captures read clean and their digests match the manifest.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
sha256sum corpus/source-snapshots/round-88/S126.txt corpus/source-snapshots/round-88/S127.txt
python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-88/S126.txt corpus/source-snapshots/round-88/S127.txt
```

Measured 2026-11-07: the two digests above and `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0`, rc 0. (The `unused_allow` count is the allowlist's row count when nothing is consumed; it rose from 17 to 19 with the two round-89 rows.)

**FC-4 — the two round-88 shapes are load-bearing, not decorative.** The frozen counter's do-nothing control (base revision as landing) fails K1, K4 and K5, and the K4 miss list names both new shapes (`.ufo/waves/round-88/controls/c2-controls-r88.txt:2-9`, including `missing=…|azure-sas-signature,…|gcs-signed-url-signature,…`). Limb K6 reads `base_rc=1 base_hits=6 new_caught_by_base=none` in both that control and the landing receipt — the base instrument's six hits on the planted repository contain none of the new shapes' hits. At the C2 landing the same limbs pass: `LIMB K1 pass selftest_rc=0 instrument_sha256=d7349536…`, `LIMB K4 pass rc=1 missing=none extra=none … files_ok=True`, `LIMB K6 pass …`, `CAPABILITY-CHECK-RESULT pass rc=0` (`.ufo/waves/round-88/l1/c2-landing-r88.txt`).

**FC-5 — provider scope is counted and the instrument is pinned.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
printf 'S126 azure_sas=%s\n' "$(grep -ciE 'azure|shared access signature|\bsas\b' corpus/source-snapshots/round-88/S126.txt)"
printf 'S127 google=%s\n' "$(grep -ciE 'google|x-goog|cloud storage|gcs' corpus/source-snapshots/round-88/S127.txt)"
printf 'S128 azure_sas=%s google=%s\n' "$(grep -ciE 'azure|shared access signature|\bsas\b' corpus/source-snapshots/round-89/S128.txt)" "$(grep -ciE 'google|x-goog|cloud storage|gcs' corpus/source-snapshots/round-89/S128.txt)"
printf 'S130 azure_sas=%s google=%s\n' "$(grep -ciE 'azure|shared access signature|\bsas\b' corpus/source-snapshots/round-89/S130.txt)" "$(grep -ciE 'google|x-goog|cloud storage|gcs' corpus/source-snapshots/round-89/S130.txt)"
printf 'r88_cloudfront=%s\n' "$(grep -ciE 'cloudfront' corpus/source-snapshots/round-88/S126.txt corpus/source-snapshots/round-88/S127.txt | awk -F: '{s+=$2} END{print s+0}')"
sha256sum corpus/instruments/capture-secret-scan.py | cut -c1-64
```

Measured 2026-11-07: `S126 azure_sas=0`, `S127 google=0`, `S128 azure_sas=0 google=0`, `S130 azure_sas=0 google=0`, `r88_cloudfront=0`, and `95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` — the pinned instrument of the round-89 C2 landing receipt (`.ufo/waves/round-89/l1/c2-landing-r89.txt:4`).

**FC-6 — the redaction rule's line exists and the round-88 captures carry no redaction block.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
sed -n '5,6p' .ufo/waves/round-86/l1/redact-presigned.py
python3 -B -c "import json;m=json.load(open('corpus/source-snapshots/round-88/manifest.json'));print('r88_redaction_blocks=%d' % sum('redaction' in x for x in m['sources']))"
python3 -B -c "import json;m=json.load(open('corpus/source-snapshots/round-89/manifest.json'));print('r89_redaction_blocks=%d' % sum('redaction' in x for x in m['sources']))"
python3 -B -c "import json;r=[x for x in json.load(open('corpus/source-snapshots/round-86/manifest.json'))['sources'] if x['id']=='S122'][0]['redaction'];print('r86_pre_digest_len=%d keys=%s' % (len(r['pre_redaction_sha256']), ','.join(sorted(r))))"
```

Measured 2026-11-07: the two tool lines of Claim 6, `r88_redaction_blocks=0`, `r89_redaction_blocks=0`, and `r86_pre_digest_len=64 keys=applied_utc,note,pre_redaction_bytes,pre_redaction_sha256,removed,strings,tool`.

**FC-7 — the wrapped-signature miss is the wrap, not the absence of a shape.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9
python3 -B -c "
import sys
L = open('corpus/source-snapshots/round-88/S126.txt', encoding='utf-8').read().split(chr(10))
open(sys.argv[1] + '/S126-joined.txt', 'w', encoding='utf-8').write(chr(10).join(L[:465] + [''.join(L[465:473])] + L[473:]))
" "$T"
python3 -B corpus/instruments/capture-secret-scan.py --files "$T/S126-joined.txt"; echo "joined_rc=$?"
rm -rf -- "$T"
```

Measured 2026-11-07: `HIT shape=gcs-signed-url-signature path=…/S126-joined.txt line=466`, `CAPTURE-SECRET-SCAN mode=files scanned=1 hits=1 files=1 allowed=0 unused_allow=19 rc=1`, `joined_rc=1`; the unjoined capture is the `scanned=2 hits=0` run of FC-3. The scratch copy holds the vendor's documented example signature and is deleted by the last line; the receipt of this check is the two printed lines, never the fixture.

**FC-8 — every CloudFront quoted span is verbatim, anchored, within 25 words, and occurs the declared number of times (`normalized=whitespace`).**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
def norm(s): return ' '.join(s.split())
Q = [
 ('S128','corpus/source-snapshots/round-89/S128.txt',56,57,1,"Expires=date and time in Unix time format (in seconds) and Coordinated Universal Time (UTC)"),
 ('S128','corpus/source-snapshots/round-89/S128.txt',58,59,1,"The date and time that you want the URL to stop allowing access to the file."),
 ('S128','corpus/source-snapshots/round-89/S128.txt',62,62,2,"January 1, 2026 10:00 am UTC converts to 1767290400"),
 ('S128','corpus/source-snapshots/round-89/S128.txt',70,70,1,"&Signature=hashed and signed version of the policy"),
 ('S128','corpus/source-snapshots/round-89/S128.txt',77,77,1,"The ID for a CloudFront public key, for example, K2JCJMDEHXQW5F."),
 ('S128','corpus/source-snapshots/round-89/S128.txt',82,83,1,"This public key must belong to a key group that is a trusted signer in the distribution"),
 ('S128','corpus/source-snapshots/round-89/S128.txt',94,95,1,"When you create a signed URL using a canned policy, the Signature parameter is a hashed and signed version of a policy statement."),
 ('S128','corpus/source-snapshots/round-89/S128.txt',202,202,1,"Replace characters that are invalid in a URL query string with characters that are valid."),
 ('S128','corpus/source-snapshots/round-89/S128.txt',206,211,1,"+ - (hyphen) = _ (underscore) / ~ (tilde)"),
 ('S128','corpus/source-snapshots/round-89/S128.txt',212,212,1,"Append the resulting value to your signed URL after &Signature=, and return to"),
 ('S130','corpus/source-snapshots/round-89/S130.txt',66,66,1,"Policy=base64 encoded version of"),
 ('S130','corpus/source-snapshots/round-89/S130.txt',70,71,1,"The policy statement controls the access that a signed URL grants to a user."),
 ('S130','corpus/source-snapshots/round-89/S130.txt',77,78,1,"A hashed, signed, and base64-encoded version of the JSON policy statement."),
 ('S130','corpus/source-snapshots/round-89/S130.txt',79,81,1,"&Key-Pair-Id=public key ID for the CloudFront public key whose corresponding private key you're using to generate the signature"),
 ('S130','corpus/source-snapshots/round-89/S130.txt',163,163,1,"anyone with the signed URL can access all of the files in any distribution that is associated"),
]
bad = 0
for sid, p, a, b, want, q in Q:
    raw = open(p, encoding='utf-8').read().split('\n')
    n = norm('\n'.join(raw)); nq = norm(q)
    got = n.count(nq)
    span = norm('\n'.join(raw[a-1:b]))
    ok = got == want and nq[:40] in span and len(nq.split()) <= 25
    bad += not ok
    print('%s:%d-%d occurrences=%d expected=%d anchored=%s words=%d %s'
          % (sid, a, b, got, want, 'y' if nq[:40] in span else 'n', len(nq.split()), 'OK' if ok else 'FAIL'))
print('QUOTE-CHECK %s spans=%d bad=%d' % ('pass' if not bad else 'fail', len(Q), bad))
raise SystemExit(1 if bad else 0)
PY
```

Measured 2026-11-07: fifteen `OK` lines and `QUOTE-CHECK pass spans=15 bad=0`, rc 0. The `:62` span is declared twice because the same sentence recurs at `:154-155`; the entry cites that recurrence.

**FC-9 — the CloudFront shape is load-bearing and the two round-89 captures read clean under their two allowlist rows.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B corpus/instruments/capture-secret-scan.py --selftest | grep -E '^SELFTEST cf-|^SELFTEST-RESULT'
python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-89/S128.txt corpus/source-snapshots/round-89/S130.txt
```

Measured 2026-11-07: nine `SELFTEST cf-… ok` lines — four with `got=cloudfront-signed-url-signature` (`cf-canned`, `cf-custom`, `cf-kpi-first-json`, `cf-html-amp`) and five with `got=none` (`cf-doc-placeholder`, `cf-sig-without-kpi`, `cf-amz-signature-beside-kpi`, `cf-short-sig`, `cf-lowercase-names`) — then `SELFTEST-RESULT pass cases=43`; and `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=2 unused_allow=17 rc=0`, rc 0. The frozen counter's base control reads `LIMB K6 pass base_rc=1 base_hits=11 new_caught_by_base=none` at the round-89 C2 landing (`.ufo/waves/round-89/l1/c2-landing-r89.txt:8`), so the base instrument catches none of the round-89 shapes' hits on the planted repository.

## Rejected over-generalizations

1. **"A signed URL is safe in a capture because it expires."** Rejected: expiry ends the URL's authority, not the capture's bytes (Claim 2); a capture pushed inside the window is a disclosure incident whatever its later usability.
2. **"A Cloud Storage signed URL, an Azure SAS and a CloudFront signed URL are the same shape."** Rejected: different parameter names (`X-Goog-Signature` versus `sig` versus `Signature` beside `Key-Pair-Id`), different encodings (hex V4, Base64 HMAC-SHA256, URL-safe base64 with `~`), different revocation stories (key rotation, policy deletion or key regeneration, expiry or key-pair rotation); the instrument carries three separate shapes for that reason (`corpus/instruments/capture-secret-scan.py:160-165`).
3. **"The scanner catches every signed-URL form."** Rejected: the named limits at `corpus/instruments/capture-secret-scan.py:106-115` exclude GCS V2, CloudFront signed cookies held as HAR/JSON name/value objects, percent-encoded parameter names, Azure names of 8+ letters, more than 20 intervening parameters and soft-wrapped values; the Azure shape needs `sv=` in the same query and the CloudFront URL shape needs `Key-Pair-Id=` (Claim 5, Claim 7).
4. **"An Azure ad hoc SAS can be revoked without touching the key."** Rejected: `corpus/source-snapshots/round-88/S127.txt:599` and `:601` say the opposite for an ad hoc SAS with no stored access policy.
5. **"A clean scan means the capture is credential-free."** Rejected: it is a byte-pattern matcher over a named shape set and a path scope; a clean run means "no matching shape" (Claim 5).
6. **"Every capture in the repository is scanned by `--rev`."** Rejected: the scope is path-based (`corpus/instruments/capture-secret-scan.py:14-21`); a capture at another path is covered only by `--files`, which is why the docstring says to run that on each capture before its first commit (`:20-21`).
7. **"An allowlist row is a general exemption."** Rejected: a row binds one exact matched value at one path (`:94-95`); the same shape with a different value is still a hit.
8. **"A CloudFront signed URL and a CloudFront signed cookie are the same shape."** Rejected: the URL shape matches query parameters of a signed URL (`Signature=` beside `Key-Pair-Id=`); signed cookies carry `CloudFront-Signature` and `CloudFront-Key-Pair-Id` cookie names, and a cookie is not a query parameter (Claim 7). Since round 91 a separate shape, `cloudfront-signed-cookie-signature`, matches the cookie pair (`corpus/instruments/capture-secret-scan.py:67-80`, `:166-167`).
9. **"The CloudFront documentation example is a live credential."** Rejected: it is AWS's example bytes, bound by two digest rows at the two snapshot paths only (`corpus/instruments/capture-secret-allow.tsv:21-22`), and its own `Expires` value is the page's 2026-01-01 example instant (`corpus/source-snapshots/round-89/S128.txt:13`, `:62`), before the 2026-11-07 capture.

## Honest limit

- **Three providers, one form each.** S126 covers Cloud Storage V4 signed URLs; S127 covers the Azure service SAS; S128 and S130 cover the CloudFront signed URL, whose canned and custom policies are two parameter sets of one form. Account SAS, user-delegation SAS, GCS V2 and CloudFront signed cookies are outside this entry. Round 91 extended the detector to CloudFront signed cookies and to user-delegation SAS carrying `skdutid` (`corpus/instruments/capture-secret-scan.py:47-52`, `:67-80`; S133, S134); `corpus/knowledge/cloud-signed-cookies-and-user-bound-sas.md` is the entry for those forms. GCS V2 stays outside the shape set (`corpus/instruments/capture-secret-scan.py:106-115`).
- **No HAR is exercised.** None of the four captures is a HAR; the HAR case is the same query string preserved in a request URL, and the instrument's selftest exercises the shapes in a URL query string, a JSON key, an HTML-escaped query and a JSON `\u0026` escape (`corpus/instruments/capture-secret-scan.py:328-348`), not in a real HAR. This entry measures no HAR bytes.
- **A clean run on these captures is not a clean page.** S126 reads clean only because its example signature is hard-wrapped: rejoining the eight wrapped lines makes the same bytes produce `HIT shape=gcs-signed-url-signature` (FC-7). The detector sees a contiguous shape, and a wrapped signature is outside it.
- **No live URL is exercised.** Every sentence about a signed URL's behavior is the vendor's documented statement, not a request made by this lane; the documented example carries a 2018 date (`X-Goog-Date` at `corpus/source-snapshots/round-88/S126.txt:465-466`), so no window arithmetic here is run against a live URL.
- **The thresholds are the instrument's.** 64+ hex digits, 40+ base64/percent characters and 40+ URL-safe characters are lane choices sized to the documented encodings (`corpus/instruments/capture-secret-scan.py:156-165`); a shorter or reformatted signature falls outside the shape and a clean run says nothing about it.
- **The CloudFront captures are clean by allowlist, not by absence.** Both round-89 captures contain AWS's documentation example signature, and the scanner reads them clean only because two rows bind that exact value at those two paths (`corpus/instruments/capture-secret-allow.tsv:21-22`; `allowed=2` in FC-9). A capture of a real signed URL has no such row and reads as a hit.
- **The documented CloudFront example is expired.** Its `Expires` value is the page's own 2026-01-01 10:00 UTC example (`corpus/source-snapshots/round-89/S128.txt:13`, `:62`), before the 2026-11-07 capture, so the example URL is outside its own window; no live CloudFront URL is exercised and no request is made.
- **Revocation is Microsoft's statement for the SAS forms that page covers.** The same page also documents account SAS and user-delegation SAS, which this entry does not.
- **The commit-time hook is not measured here.** The capability and its counter exist (`.ufo/waves/round-88/l1/c2-landing-r88.txt`); whether a pre-commit hook invokes the scanner on every capture is a process claim this entry does not make.
- Documentation only: no live target was contacted for this entry — every value is read from pinned lane bytes — and the entry carries no credential material, session, private URL or vault reference. It quotes one vendor's `<signature>` placeholder and cites the other vendors' example signatures only by line span, never by value.
