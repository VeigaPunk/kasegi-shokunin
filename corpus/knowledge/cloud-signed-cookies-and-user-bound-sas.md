# CloudFront signed cookies and user-bound Azure SAS in captured evidence — a signed cookie is three name-value pairs a viewer presents until the policy's expiration, a user-bound user-delegation SAS is narrowed to one Entra identity and tenant, the lane's scanner names both forms, and the redaction rule replaces the value while keeping the cookie name and the parameter names

source: S133 — Microsoft Learn, Azure Storage REST API, Create a user delegation SAS — https://learn.microsoft.com/en-us/rest/api/storageservices/create-user-delegation-sas — anchor `corpus/source-snapshots/round-91/S133.txt:567` and `:571` (capture 954 lines, 60,089 bytes, sha256 56d858ac8c2988fdf95a045b5a75f13cc5a28a1f71b3786638522775b1786cd6; manifest `corpus/source-snapshots/round-91/manifest.json` records `Q02-skdutid-tenant` at anchor 567 and `Q01-skdutid-version` at anchor 571, each `occurrences=1`; row `corpus/SOURCES.md:145`, tier A, status `queued`); S134 — Amazon CloudFront Developer Guide, Set signed cookies using a custom policy — https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-setting-signed-cookie-custom-policy.html — anchor `corpus/source-snapshots/round-91/S134.txt:97` and `:17` (capture 441 lines, 21,243 bytes, sha256 ddf45b805c7f67f29cf15f60f805fd636968f14734f4e342c697760f8b49f1cc; manifest records `Q01-signature-cookie` at anchor 97 and `Q02-three-pairs` at anchor 17, each `occurrences=1`; row `corpus/SOURCES.md:146`, tier A, status `queued`).
verified-at: 2026-11-07 (re-opened at the pinned bytes: `sha256sum` prints S133 `56d858ac…` and S134 `ddf45b80…`, equal to the manifest `sha256`; `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-91/manifest.json --source S133` prints `S133:sha256 OK` plus two `Q0n … OK occurrences=1 anchor=N-ok` lines, rc 0, and `--source S134` prints the same shape, rc 0; `python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-91/S133.txt corpus/source-snapshots/round-91/S134.txt` prints `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0`; the manifest records S133 fetched 2026-11-07T07:48:19Z and S134 2026-11-07T07:48:20Z; the instrument read here is the landed scanner of `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`, sha256 `89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7`).
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-91/manifest.json --source S133 && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-91/manifest.json --source S134 && python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-91/S133.txt corpus/source-snapshots/round-91/S134.txt

## Attribution

S133 is Microsoft's own Create a user delegation SAS reference (`corpus/SOURCES.md:145`, tier A): every sentence here about what a user delegation SAS is, what signs it, what `sduoid` and `skdutid` require, and how it is revoked is Microsoft's statement about the Azure Storage user delegation SAS form, not about the service SAS, the account SAS, or any other provider. S134 is AWS's own CloudFront page for custom-policy signed cookies (`corpus/SOURCES.md:146`, tier A): every sentence about the three name-value pairs, what the signature is, what the policy contains, and how CloudFront validates it is AWS's statement about that form, not about signed URLs, canned-policy cookies, or any other provider. Both rows are `queued` with `used-by —` in the round-91 freeze (`corpus/SOURCES.md:318-319`); this entry is their first use.

The two captures do not overlap in provider or in carrier. `grep -ciE 'cloudfront|amazon' corpus/source-snapshots/round-91/S133.txt` prints `0`, and `grep -ciE 'azure|blob\.core\.windows\.net|shared access signature' corpus/source-snapshots/round-91/S134.txt` prints `0` (FC-5). S133 documents a query-string credential; S134 documents a cookie credential — the carrier differs, which is why the scanner carries two shapes.

The scanner is the lane's instrument, `corpus/instruments/capture-secret-scan.py` at `1dd0723` (capability row `SCORECARD.md:307`); its shape set, bounds, scope and output are a lane design choice, not a vendor statement, and every sentence in Claim 5 is about the instrument's own bytes.

## Claim 1 — a CloudFront signed cookie is three name-value pairs, and the signature pair is the authorizing value

> "and a CloudFront signed cookie requires three name-value pairs. The name-value pairs are: CloudFront-Policy, CloudFront-Signature, and CloudFront-Key-Pair-Id." — `corpus/source-snapshots/round-91/S134.txt:17-19`

> "A hashed, signed, and base64-encoded version of the JSON policy statement." — `corpus/source-snapshots/round-91/S134.txt:97-98`

Lane reading: the credential is a set, not a single string. The policy pair carries the statement, the signature pair carries the signature over it, and the key-pair pair names the public key CloudFront validates with. A capture that keeps all three keeps the grant; a capture that keeps only the signature keeps the value the scanner looks for.

> "The values must be present on the viewer before a user makes the first request for a file that you want to control access to." — `corpus/source-snapshots/round-91/S134.txt:22-23`

That is the carrier claim in AWS's words: the cookie set is what the viewer presents. Nothing else is presented — no account, no session, no header — which is why the lane treats the three pairs as one credential.

> "In general, we recommend that you exclude Expires and Max-Age attributes." — `corpus/source-snapshots/round-91/S134.txt:25-28`

The recommendation is about browser lifetime, not authority: AWS's stated reason is that closing the browser deletes the cookie, "which reduces the possibility of someone getting unauthorized access" (`corpus/source-snapshots/round-91/S134.txt:27-28`). Lane reading: a capture is not a browser. The bytes survive browser deletion, and the authority ends at the policy's own date (Claim 2), not at the cookie's `Expires`.

## Claim 2 — the policy bounds the cookie, and CloudFront validates the signature against it

> "The policy statement controls the access that a signed cookie grants to a user." — `corpus/source-snapshots/round-91/S134.txt:91-92`

> "It includes the files that the user can access, an expiration date and time" — `corpus/source-snapshots/round-91/S134.txt:92-95`

The same sentence continues at `corpus/source-snapshots/round-91/S134.txt:93-95` with "an optional date and time that the URL becomes valid, and an optional IP address or range of IP addresses that are allowed to access the file", so the policy names four bounds: which files, until when, from when, from where.

> "The expiration date and time for the URL in Unix time format (in seconds) and Coordinated Universal Time (UTC)." — `corpus/source-snapshots/round-91/S134.txt:255-258`

Lane reading: as with a signed URL, the record states its own end instant, so priority can be computed from the capture without contacting anything. The row's word "URL" is AWS's field description for `DateLessThan`; the same field bounds a cookie's policy (`corpus/source-snapshots/round-91/S134.txt:91-95`).

> "CloudFront compares the information in the signature with the information in the policy statement to verify that the URL has not been tampered with." — `corpus/source-snapshots/round-91/S134.txt:102-105`

That is the validation test: signature against policy. A captured cookie set passes it until the policy's date, because nothing in the check depends on who is presenting it.

> "Replace these invalid characters With these valid characters" — `corpus/source-snapshots/round-91/S134.txt:419-420`

The table rows at `corpus/source-snapshots/round-91/S134.txt:421-426` map `+` to `- (hyphen)`, `=` to `_ (underscore)` and `/` to `~ (tilde)`, so a cookie signature's alphabet is `A-Za-z0-9` plus `-`, `_` and `~` — the same URL-safe class as a CloudFront signed URL, and the alphabet the detector's class admits (`corpus/instruments/capture-secret-scan.py:139`). The table occurs twice in the capture, at `:196-197` and `:419-420`.

## Claim 3 — a user delegation SAS is signed with a user delegation key and travels as query parameters on the blob URL

> "A SAS secured with Microsoft Entra credentials is called a user delegation SAS." — `corpus/source-snapshots/round-91/S133.txt:30`

> "Every SAS is signed with a key. To create a user delegation SAS, you must first request a user delegation key" — `corpus/source-snapshots/round-91/S133.txt:31`

> "Shared access signatures are keys that grant permissions to storage resources, and you should protect them just as you would protect an account key." — `corpus/source-snapshots/round-91/S133.txt:34`

Lane reading: Microsoft states the credential property directly — a SAS is a key, protected like an account key. The signing key differs (a user delegation key instead of the account key); the credential property does not.

> "The following example shows a blob URI with a user delegation SAS token appended to it." — `corpus/source-snapshots/round-91/S133.txt:869`

> "The delimiter that precedes the query string. The delimiter is not part of the SAS token." — `corpus/source-snapshots/round-91/S133.txt:880`

So the carrier is the query string of the blob URL, and `sig=` is the authorizing parameter: "Used to authorize access to the blob. The signature is an HMAC that's computed over a string-to-sign and key by using the SHA256 algorithm" (`corpus/source-snapshots/round-91/S133.txt:922`).

> "You can specify that the key is valid for a period of up to seven days." — `corpus/source-snapshots/round-91/S133.txt:86`

Bounds: the key lives at most seven days, and `ske` states the end (`corpus/source-snapshots/round-91/S133.txt:540`). Revocation is a key action, not a per-token action: "You can revoke a user delegation SAS either by revoking the user delegation key, or by changing or removing RBAC role assignments" (`corpus/source-snapshots/round-91/S133.txt:924`), and "Stored access policies aren't supported for a user delegation SAS" (`corpus/source-snapshots/round-91/S133.txt:32`). Lane reading: there is no per-token withdrawal; the fixes after publication are redacting the capture (Claim 6) or revoking the key, and Microsoft warns that both the key and the role assignments are cached, so revocation is not instantaneous (`corpus/source-snapshots/round-91/S133.txt:926`).

## Claim 4 — a user-bound SAS is narrowed to one Entra identity and tenant, and its tenant field is the 7-letter `skdutid`

> "No one other than this user will be able to use the SAS token." — `corpus/source-snapshots/round-91/S133.txt:56`

> "When specified, the caller must also send a Bearer token; its oid claim must match sduoid." — `corpus/source-snapshots/round-91/S133.txt:565`

> "The skdutid field represents the tenant ID (tid) of the Microsoft Entra security principal that will use the SAS token." — `corpus/source-snapshots/round-91/S133.txt:567`

> "The sduoid and skdutid fields are supported with version 2025-07-05 and later." — `corpus/source-snapshots/round-91/S133.txt:571`

Lane reading: this form is **not** a universal bearer credential. It is a grant to one identity, and using it requires a bearer token whose `oid` — and, cross-tenant, whose `tid` — matches the fields in the token (`corpus/source-snapshots/round-91/S133.txt:565`, `:568`). Two consequences:

- the disclosure harm is narrower than a service SAS's but not zero: the captured token still authorizes that user, and it discloses the end-user object id and tenant id — identifiers about a person, in a record that may be published;
- the blast radius is the intersection of the key principal's permissions and `sp`: "The permissions granted to a client who possesses the SAS are the intersection of the permissions that were granted to the security principal" (`corpus/source-snapshots/round-91/S133.txt:49`).

The field names are the reason the detector missed it (Claim 5): `skdutid` is seven letters, and the round-90 window admitted two to six (`corpus/instruments/capture-secret-scan.py:100` at `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`).

## Claim 5 — what the landed scanner detects, and where it looks

The docstring at `corpus/instruments/capture-secret-scan.py:1-105` is the specification this entry reads; the instrument's sha256 at `1dd0723` is `89e283c6423216917c8ae31e1f72239f56ebcb842bda72f7bad4b2f36dc526d7`.

**Scope.** `--rev REV` reads a git tree without checkout and scans capture-class paths only: anything under `corpus/source-snapshots/`, anything under a practice package's `corpus/practice/<pkg>/evidence/`, any path with a directory segment ending in `-receipts`, and any file whose name starts with `live-` (`corpus/instruments/capture-secret-scan.py:14-21`, `is_capture_path` at `:176-181`). `--files PATH...` scans exactly the named working-tree files whatever their path, and the docstring's instruction is to run it "on every capture before the commit that first adds it" (`:19-21`).

**The cookie shape** — `cloudfront-signed-cookie-signature` (`corpus/instruments/capture-secret-scan.py:67-80`; left boundary `:130`, pattern `:138-139`): the cookie name followed by `=` and 40 or more characters of `[A-Za-z0-9_~-]`, name case-sensitive, in a `Set-Cookie:` or `Cookie:` header or in any text; the name may not be preceded by a letter, digit, `_` or `-` unless that character is the `n` of a JSON `\n` escape (several Set-Cookie values joined into one JSON string) or the end of a `\u0026`/`%26` separator.

**The widened Azure window.** Between `sv=YYYY-MM-DD` and `sig=`, the intervening parameter names are now two to seven letters (`_PARAM` at `corpus/instruments/capture-secret-scan.py:122`, previously `{2,6}` at `:100` of the base revision), so a query carrying `skdutid` between them is spanned (`:47-52`); an eight-letter name still ends the window (`:84-85`), and the selftest pins that case (`:309`). FC-7 measures the page's own field table: thirty-five distinct abbreviations, none longer than seven letters, and `skdutid` is the only seven-letter one — the bound is exactly what this page needs and no wider.

**Output.** Never the matched value: `HIT shape=<s> path=<p> line=<n>` per file and shape, first non-allowed match, then `CAPTURE-SECRET-SCAN mode=<m> scanned=<n> hits=<h> files=<f> allowed=<a> unused_allow=<u> rc=<rc>` (`corpus/instruments/capture-secret-scan.py:99-104`, `report()` at `:234-246`); `rc = 1 if hits else 0` (`:243`); exit 2 on a usage or read error (`:370-374`). A receipt carrying those lines is safe to commit where the fixture is not.

**Allowlist.** `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason` — one exact matched value at one path, so a different value at the same path and shape is still a hit (`corpus/instruments/capture-secret-scan.py:90-97`, keying at `:192-199`); rows for `aws-sts-session-token` are refused and a refused or malformed row is exit 2 (`:95-97`, `:157-159`). No row binds either round-91 shape, so both captures read clean by absence, not by exemption (`allowed=0` in FC-2).

**Selftest.** The new cases are pinned at `corpus/instruments/capture-secret-scan.py:307-316`: two Azure positives (`azure-skdutid-user-bound`, `azure-skdutid-sig-first`), one Azure negative (`azure-eight-letter-name`), three cookie positives (`cf-cookie-set-cookie`, `cf-cookie-request-header`, `cf-cookie-json-joined`) and four cookie negatives (`cf-cookie-doc-example`, `cf-cookie-doc-placeholder`, `cf-cookie-lowercase-name`, `cf-cookie-prefixed-name`). Measured 2026-11-07: `SELFTEST-RESULT pass cases=53` (FC-4).

**Named limits**, verbatim from `corpus/instruments/capture-secret-scan.py:81-87`: CloudFront signed cookies held as HAR/JSON name/value objects, percent-encoded parameter names or `=`, Azure SAS parameter names of 8+ letters between `sv` and `sig`, more than 20 other parameters between the two matched ones, values soft-wrapped across lines, and gzip/UTF-16/base64-wrapped captures are not detected. Three of those are measured in FC-5.

## Claim 6 — the operating rule: scan before the first commit, then replace the value and keep the names

For a cookie, redaction is not "strip the query string" — there is no query string. The rule is: replace the value, keep the name. A redacted record reads `CloudFront-Signature=<redacted>` beside `CloudFront-Policy=<redacted>` and `CloudFront-Key-Pair-Id=<key-pair-id>`, which keeps the record readable (which distribution, which pair, which policy shape) and drops the authorizing bytes. The key-pair id is not the credential — it names the public key, and "This public key must belong to a key group that is a trusted signer in the distribution" (`corpus/source-snapshots/round-91/S134.txt:106-107`) — so it is an identifier worth keeping, not a secret worth dropping.

For a SAS, the round-88 rule still applies: strip the query and keep `scheme://host/path`; the residue names the account, container and blob. If the record must keep the parameter names, replace every value: `sig=<redacted>` and `skdutid=<redacted>` — Claim 4's identifiers are personal data.

The second half of the rule is the digest pair: record the pre-redaction `sha256` beside the committed one (the round-86 manifest's `redaction` block is the model, `corpus/source-snapshots/round-86/manifest.json`). Neither round-91 capture needed redaction: both read clean (FC-2) and neither manifest record carries a `redaction` block (FC-6).

## How a researcher uses this

1. **Scan the file, not the directory, before the first commit** (`corpus/instruments/capture-secret-scan.py:19-21`). Run `--files` on each new capture and paste the `CAPTURE-SECRET-SCAN … rc=` line into the round receipt.
2. **Read a cookie hit as the signature pair.** `cloudfront-signed-cookie-signature` is the `CloudFront-Signature` pair of Claim 1; its policy and key-pair pairs sit in the same header block and are what makes the set usable.
3. **Read an Azure hit as the signature parameter.** `azure-sas-signature` is `sig=` beside `sv=` (Claim 3); if `sduoid` or `skdutid` is in the same query, the token is user-bound (Claim 4) and the disclosure includes those identifiers.
4. **Redact the value, keep the names** (Claim 6).
5. **Read the window from the record before deciding urgency.** Cookie: the policy's `DateLessThan` (`corpus/source-snapshots/round-91/S134.txt:255-258`). SAS: `se=` for a service SAS, `ske` for a user delegation SAS (`corpus/source-snapshots/round-91/S133.txt:540`), with revocation by key action (`:924`). Expiry bounds use, not publication.
6. **Treat a clean run as "no matching shape", not "no credential"** (Claim 5's limits, FC-5).

## Falsifiable rule and checks

**Falsifiable rule.** Any sentence asserting that a capture holding a CloudFront signed cookie set or a user-bound user-delegation SAS is credential-free is falsified by `python3 -B corpus/instruments/capture-secret-scan.py --files <capture>` exiting 1 with a `HIT shape=cloudfront-signed-cookie-signature` or `HIT shape=azure-sas-signature` line. Any sentence asserting that a user-bound SAS is usable by anyone who holds it is falsified by `corpus/source-snapshots/round-91/S133.txt:56` and `:565`. Any sentence asserting that the round-90 instrument detected either form is falsified by FC-3's base run, which prints `hits=0` on both fixtures.

**FC-1 — every quoted span is verbatim, anchored, within 25 words, and occurs the declared number of times (`normalized=whitespace`).**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
def norm(s): return ' '.join(s.split())
Q = [
 ('S133','corpus/source-snapshots/round-91/S133.txt',30,30,1,"A SAS secured with Microsoft Entra credentials is called a user delegation SAS."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',31,31,1,"Every SAS is signed with a key. To create a user delegation SAS, you must first request a user delegation key"),
 ('S133','corpus/source-snapshots/round-91/S133.txt',34,34,1,"Shared access signatures are keys that grant permissions to storage resources, and you should protect them just as you would protect an account key."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',32,32,1,"Stored access policies aren't supported for a user delegation SAS."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',49,49,1,"The permissions granted to a client who possesses the SAS are the intersection of the permissions that were granted to the security principal"),
 ('S133','corpus/source-snapshots/round-91/S133.txt',56,56,1,"No one other than this user will be able to use the SAS token."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',565,565,1,"When specified, the caller must also send a Bearer token; its oid claim must match sduoid."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',567,567,1,"The skdutid field represents the tenant ID (tid) of the Microsoft Entra security principal that will use the SAS token."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',571,571,1,"The sduoid and skdutid fields are supported with version 2025-07-05 and later."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',869,869,1,"The following example shows a blob URI with a user delegation SAS token appended to it."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',880,880,1,"The delimiter that precedes the query string. The delimiter is not part of the SAS token."),
 ('S133','corpus/source-snapshots/round-91/S133.txt',922,922,1,"Used to authorize access to the blob. The signature is an HMAC that's computed over a string-to-sign and key by using the SHA256 algorithm"),
 ('S133','corpus/source-snapshots/round-91/S133.txt',924,924,1,"You can revoke a user delegation SAS either by revoking the user delegation key, or by changing or removing RBAC role assignments"),
 ('S133','corpus/source-snapshots/round-91/S133.txt',86,86,1,"You can specify that the key is valid for a period of up to seven days."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',17,19,1,"and a CloudFront signed cookie requires three name-value pairs. The name-value pairs are: CloudFront-Policy, CloudFront-Signature, and CloudFront-Key-Pair-Id."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',22,23,1,"The values must be present on the viewer before a user makes the first request for a file that you want to control access to."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',25,28,1,"In general, we recommend that you exclude Expires and Max-Age attributes."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',91,91,1,"The policy statement controls the access that a signed cookie grants to a user."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',92,95,1,"It includes the files that the user can access, an expiration date and time"),
 ('S134','corpus/source-snapshots/round-91/S134.txt',97,98,1,"A hashed, signed, and base64-encoded version of the JSON policy statement."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',102,105,1,"CloudFront compares the information in the signature with the information in the policy statement to verify that the URL has not been tampered with."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',255,258,1,"The expiration date and time for the URL in Unix time format (in seconds) and Coordinated Universal Time (UTC)."),
 ('S134','corpus/source-snapshots/round-91/S134.txt',419,420,2,"Replace these invalid characters With these valid characters"),
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

Measured 2026-11-07: twenty-three `OK` lines and `QUOTE-CHECK pass spans=23 bad=0`, rc 0. The `:419-420` span is declared twice because the same two-line table header recurs at `:196-197`.

**FC-2 — the pinned captures read clean and their digests match the manifest.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
sha256sum corpus/source-snapshots/round-91/S133.txt corpus/source-snapshots/round-91/S134.txt
python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-91/manifest.json --source S133
python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-91/manifest.json --source S134
python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-91/S133.txt corpus/source-snapshots/round-91/S134.txt
```

Measured 2026-11-07: `56d858ac8c2988fdf95a045b5a75f13cc5a28a1f71b3786638522775b1786cd6` for S133 and `ddf45b805c7f67f29cf15f60f805fd636968f14734f4e342c697760f8b49f1cc` for S134, six `OK` lines across the two runs (three per capture: `sha256 OK` plus `Q01-skdutid-version OK occurrences=1 anchor=571-ok` and `Q02-skdutid-tenant OK occurrences=1 anchor=567-ok`; then `Q01-signature-cookie OK occurrences=1 anchor=97-ok` and `Q02-three-pairs OK occurrences=1 anchor=17-ok`), and `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0`, rc 0.

**FC-3 — both shapes are load-bearing: the landed instrument fires where the base instrument does not.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9   # set TMPDIR to a scratch dir; the fixture is under 1 KB
mkdir -p "$T/base"
git show bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1:corpus/instruments/capture-secret-scan.py > "$T/base/capture-secret-scan.py"
git show bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1:corpus/instruments/claim-package-check.py > "$T/base/claim-package-check.py"
python3 -B - "$T" <<'PY'
import sys
T = sys.argv[1]
cf = 'FAKECF' + 'a' * 40
az = 'FAKEAZ' + 'b' * 40
g  = '00000000-0000-0000-0000-000000000000'
open(T + '/A-set-cookie.txt', 'w').write('Set-Cookie: CloudFront-Signature=%s; Path=/\n' % cf)
open(T + '/D-json-joined.txt', 'w').write('{"set-cookie":"CloudFront-Key-Pair-Id=K2JCJMDEHXQW5F; Path=/\\nCloudFront-Signature=%s; Path=/"}\n' % cf)
open(T + '/E-skdutid.txt', 'w').write('https://a.blob.core.windows.net/c/b.txt?sp=rw&skv=2025-07-05&sv=2025-07-05&sr=b&skdutid=%s&sig=%s\n' % (g, az))
PY
for f in A-set-cookie D-json-joined E-skdutid; do
  printf '%s landed: ' "$f"; python3 -B corpus/instruments/capture-secret-scan.py --files "$T/$f.txt" | grep -E '^(HIT|CAPTURE)' | tr '\n' '|'; echo
  printf '%s base:   ' "$f"; python3 -B "$T/base/capture-secret-scan.py" --files "$T/$f.txt" | grep -E '^(HIT|CAPTURE)' | tr '\n' '|'; echo
done
sha256sum "$T/base/capture-secret-scan.py" | cut -c1-64
rm -rf -- "$T"
```

Measured 2026-11-07: landed `HIT shape=cloudfront-signed-cookie-signature` on `A-set-cookie` and `D-json-joined` and `HIT shape=azure-sas-signature` on `E-skdutid`, each with `hits=1 … rc=1`; base `hits=0 … rc=0` on all three; the base instrument's digest is `95f24a541db8b3d6693315a03de28d0b6de0fb0b6e53a68471265382114d20ec` — the round-89 pinned instrument (`.ufo/waves/round-89/l1/c2-landing-r89.txt`). The receipt of this check is the printed `HIT`/summary lines and the digest, never the fixture bytes.

**FC-4 — the selftest pins the new cases.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B corpus/instruments/capture-secret-scan.py --selftest | grep -E '^(SELFTEST (cf-cookie|azure-skdutid|azure-eight)|SELFTEST-RESULT)'
```

Measured 2026-11-07: ten `SELFTEST …` lines — five with `got=cloudfront-signed-cookie-signature` or `got=azure-sas-signature` (`cf-cookie-set-cookie`, `cf-cookie-request-header`, `cf-cookie-json-joined`, `azure-skdutid-user-bound`, `azure-skdutid-sig-first`) and five with `got=none` (`cf-cookie-doc-example`, `cf-cookie-doc-placeholder`, `cf-cookie-lowercase-name`, `cf-cookie-prefixed-name`, `azure-eight-letter-name`) — then `SELFTEST-RESULT pass cases=53`, rc 0.

**FC-5 — the named limits are real, and the two captures do not overlap in provider.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
printf 'S133 cloudfront=%s\n' "$(grep -ciE 'cloudfront|amazon' corpus/source-snapshots/round-91/S133.txt)"
printf 'S134 azure=%s\n' "$(grep -ciE 'azure|blob\.core\.windows\.net|shared access signature' corpus/source-snapshots/round-91/S134.txt)"
T=$(mktemp -d -p "${TMPDIR:-/tmp}") || exit 9   # set TMPDIR to a scratch dir; the fixtures are under 1 KB
python3 -B - "$T" <<'PY'
import sys
T = sys.argv[1]
cf = 'FAKECF' + 'a' * 40
az = 'FAKEAZ' + 'b' * 40
open(T + '/B-lowercase.txt', 'w').write('Set-Cookie: cloudfront-signature=%s; Path=/\n' % cf)
open(T + '/C-short.txt', 'w').write('Set-Cookie: CloudFront-Signature=%s; Path=/\n' % cf[:39])
open(T + '/F-eight.txt', 'w').write('https://a.blob.core.windows.net/c/b.txt?sv=2025-07-05&abcdefgh=1&sig=%s\n' % az)
open(T + '/G-har-name-value.txt', 'w').write('{"name":"CloudFront-Signature","value":"%s"}\n' % cf)
PY
for f in B-lowercase C-short F-eight G-har-name-value; do
  printf '%s ' "$f"; python3 -B corpus/instruments/capture-secret-scan.py --files "$T/$f.txt" | grep -E '^(HIT|CAPTURE)' | tr '\n' '|'; echo
done
rm -rf -- "$T"
```

Measured 2026-11-07: `S133 cloudfront=0`, `S134 azure=0`, and four `CAPTURE-SECRET-SCAN … hits=0 files=0 … rc=0` lines — a lowercase cookie name, a 39-character value, an eight-letter parameter name, and a HAR/JSON name-value object all read clean while carrying the value.

**FC-6 — neither round-91 capture carries a redaction block.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B -c "import json;m=json.load(open('corpus/source-snapshots/round-91/manifest.json'));print('r91_redaction_blocks=%d' % sum('redaction' in x for x in m['sources']))"
```

Measured 2026-11-07: `r91_redaction_blocks=0`.

**FC-7 — the 2-7 window covers every parameter abbreviation on S133's field table, and `skdutid` is the only 7-letter one.**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
awk 'NR>=88 && NR<=559' corpus/source-snapshots/round-91/S133.txt | grep -E '^[a-z]{2,8}$' | sort -u | awk '{print length($0)}' | sort -n | uniq -c
awk 'NR>=88 && NR<=559' corpus/source-snapshots/round-91/S133.txt | grep -E '^[a-z]{7}$' | sort -u
```

Measured 2026-11-07: the histogram `8 2`, `15 3`, `6 4`, `4 5`, `1 6`, `1 7` — thirty-five distinct abbreviations, none longer than seven letters — and the single seven-letter line is `skdutid`. Lane reading: the widened bound is exactly what this page's table needs, and no wider; an eight-letter bound would be unsupported by S133.

## Rejected over-generalizations

1. **"A CloudFront signed cookie is the same shape as a CloudFront signed URL."** Rejected: the URL form is query parameters (`Signature=` beside `Key-Pair-Id=`), the cookie form is three name-value pairs in a header; the scanner carries two shapes for that reason (`corpus/instruments/capture-secret-scan.py:53-80`).
2. **"A captured cookie is harmless because the browser deletes it."** Rejected: `corpus/source-snapshots/round-91/S134.txt:25-28` is about browser lifetime; the bytes survive it, and authority ends at the policy's date (`:91-95`, `:255-258`).
3. **"A user-bound SAS is a bearer credential like any other SAS."** Rejected: `corpus/source-snapshots/round-91/S133.txt:56` and `:565` require the named identity's bearer token; what the capture discloses is the signature plus the end-user identifiers.
4. **"The skdutid widening made the detector permissive."** Rejected: the window is still bounded (`corpus/instruments/capture-secret-scan.py:84-85`), the eight-letter case is pinned as not detected (`:309`), and the shape still requires `sv=` and a 40+ character `sig=` (`:122-124`).
5. **"A clean scan means the capture is credential-free."** Rejected: the shapes are byte patterns over a named scope (`corpus/instruments/capture-secret-scan.py:176-181`); FC-5 measures four forms that read clean while carrying the value.
6. **"The documentation's example cookie value is a live credential."** Rejected: it is AWS's 28-character example (`corpus/source-snapshots/round-91/S134.txt:123`), below the 40-character floor, and the selftest pins it as not detected (`corpus/instruments/capture-secret-scan.py:312`).
7. **"A cookie hit and a SAS hit mean the same thing for the reader."** Rejected: the cookie set is usable by whoever presents it until the policy's date (Claim 2), while a user-bound SAS requires the named identity's bearer token (Claim 4) — the remediation urgency differs even though both are hits.

## Honest limit

- **Two forms, one page each.** S133 covers the user delegation SAS, including the user-bound fields; the service SAS, the account SAS, stored access policies and the `srh`/`srq` fields are outside this entry. S134 covers custom-policy signed cookies; canned-policy cookies (`CloudFront-Expires`) are a different page and are not covered.
- **No live credential is exercised.** Every sentence about a credential's behavior is the vendor's documented statement; no request is made, no cookie is replayed, no SAS is used. The example values in both captures are documentation examples.
- **S134 does not state a possession rule for cookies in the words S130 uses for signed URLs.** AWS's "anyone with the signed URL can access" sentence is about signed URLs (`corpus/source-snapshots/round-89/S130.txt:163`); this entry does not transfer it. The cookie reading rests on `corpus/source-snapshots/round-91/S134.txt:22-23` (the values must be present on the viewer), `:91-95` (the policy controls access) and `:102-105` (CloudFront validates signature against policy).
- **The HAR case is a named limit, not a covered case.** A HAR that records the cookie as a name/value object reads clean (FC-5's `G-har-name-value` fixture); the shape matches header text, not JSON objects (`corpus/instruments/capture-secret-scan.py:81-83`).
- **The captures read clean by absence.** No allowlist row binds either shape (`allowed=0` in FC-2), so a clean run here is the shapes' absence, not an exemption.
- **The SOURCES.md rows are `queued`.** `corpus/SOURCES.md:145-146` record both as tier A with `used-by —`; this entry is their first use, and the registry update is the L1's integration step, not this file's.
- **The scanner's thresholds are the instrument's.** 40 characters is a lane choice sized to the documented encodings; a shorter or reformatted signature falls outside the shape and a clean run says nothing about it.
- **One fixture family, not a corpus.** FC-3 and FC-5 exercise seven synthetic fixtures in a scratch directory; they show the shapes fire and the named limits hold, and they say nothing about any real capture's bytes.
- Documentation only: no live target was contacted for this entry — every value is read from pinned lane bytes — and the entry carries no credential material, session, private URL or vault reference. Every example is a `<placeholder>`.
