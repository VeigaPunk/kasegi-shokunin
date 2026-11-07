# Presigned-URL credentials in captured evidence — a disclosed bounty record can carry presigned avatar URLs, SigV4 names the field that holds a temporary-credential session token, the IAM prefix table separates a key id from a secret, and a token that expires is still a disclosure incident when the capture is pushed while it is live

source: S124 — AWS Identity and Access Management User Guide, Create a signed AWS API request (Signature Version 4) — https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-create-signed-request.html — anchor `corpus/source-snapshots/round-87/S124.txt:81-89` and `corpus/source-snapshots/round-87/S124.txt:409` (capture 437 lines, 20,439 bytes, sha256 88d4f703cef1b9d1cead11053dd9f02692bd4629a7110e42caecc74a2fc2f1cb; manifest `corpus/source-snapshots/round-87/manifest.json`, quotes Q01-Q03, all three exactly-once at anchors 84, 85, 409); S125 — AWS Identity and Access Management User Guide, IAM identifiers (unique ID prefixes) — https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html — anchor `corpus/source-snapshots/round-87/S125.txt:303-305`, `corpus/source-snapshots/round-87/S125.txt:318-319` and `corpus/source-snapshots/round-87/S125.txt:330-333` (capture 363 lines, 17,469 bytes, sha256 65c99351e731b743f18243e93613da7e05b4030d5fe2060a6cc484a320de55fe; same manifest, quotes Q01-Q03 at anchors 303, 331, 332); the record whose shape Claim 1 reads is S122 — HackerOne disclosed report 1997312, one-line JSON — https://hackerone.com/reports/1997312.json — capture `corpus/source-snapshots/round-86/S122.txt:1` (one line, 5,361 bytes, sha256 08cab370e7f153d051719bfe098cb140d0d68e9da99e27caacfa0b4228a72eb5), bound by `corpus/source-snapshots/round-86/manifest.json`, whose `redaction` block records the pre-redaction bytes
verified-at: 2026-11-07 (re-opened this day at the pinned bytes: `sha256sum` prints S124 `88d4f703…`, S125 `65c99351…`, S122 `08cab370…`, each equal to its manifest record; `python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-87/manifest.json --source S124` prints `S124:sha256 OK` plus three `Q0n … OK occurrences=1 anchor=N-ok` lines and the same for `--source S125`, both rc 0; the manifest records both round-87 captures fetched 2026-11-07T02:01:46Z with a byte-identical snapshot on a second fetch at 2026-11-07T01:54Z, and the S122 record's `redaction.pre_redaction_sha256` is `ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1` at 9,131 bytes)
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-87/manifest.json --source S124 && python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-87/manifest.json --source S125 && python3 -B -c "import json;m=json.load(open('corpus/source-snapshots/round-86/manifest.json'));r=[x for x in m['sources'] if x['id']=='S122'][0]['redaction'];raw=open('corpus/source-snapshots/round-86/S122.txt').read();print('S122:strings=%d pre_redaction_sha256=%s captured_xamz=%d' % (r['strings'],r['pre_redaction_sha256'],raw.count('X-Amz-')));assert r['strings']==2 and len(r['pre_redaction_sha256'])==64 and raw.count('X-Amz-')==0"  # prints S124 sha256 + 3 quote lines, S125 sha256 + 3 quote lines, then S122:strings=2 with the pre-redaction digest and a zero X-Amz- count; exits non-zero when a manifest, a capture or the redaction record is absent, so a lost base fails closed; a pinned-capture comparison, not a fresh network check

## Attribution

S124 and S125 are AWS's own IAM User Guide pages. Everything said here about where a SigV4 request carries a session token, and about what an `AKIA`/`ASIA` prefix classifies, is AWS's statement about AWS SigV4 signing and AWS IAM identifiers; neither capture mentions another provider's signing scheme (`grep -ciE 'azure|shared access signature|google cloud|gcs'` prints 0 on both, FC-3), so nothing here is a claim about signed URLs in general.

S122 is HackerOne's own machine record of one disclosed report (registry row S122, kind `dataset`, tier A). The two redacted strings inside the capture are the lane's own edit, not HackerOne's text: `.ufo/waves/round-86/l1/redact-presigned.py` rewrote them after the round-86 freeze. Lane reading, not a quote: the redaction is why this capture can be cited at all — the served body carried credential material and the committed body does not.

The scanner is the lane's instrument, `corpus/instruments/capture-secret-scan.py` (capability row `SCORECARD.md:307`). Its shape set is the claim-package gate's `SECRET_PATTERNS`, imported from `corpus/instruments/claim-package-check.py` beside it, plus two AWS shapes (instrument lines 25-31) and, from round 88, two cloud signed-URL shapes (lines 32-42; see `corpus/knowledge/cloud-signed-url-credentials-in-captured-evidence.md`) — a lane design choice, not an AWS statement.

## Claim 1 — a disclosed bounty record can carry presigned avatar URLs at three levels, and this capture's two signed strings were the team avatar's two sizes

> "Every JSON string value containing `X-Amz-` keeps its scheme/host/path and loses its query string, replaced by `?[presigned-query-redacted-r86]`." — `.ufo/waves/round-86/l1/redact-presigned.py:5-6`

`corpus/source-snapshots/round-86/S122.txt:1` is one 5,361-byte line holding a 51-key JSON object (FC-2). It carries a `profile_picture_urls` object in three places: `reporter.profile_picture_urls`, `team.profile_picture_urls` and `summaries[0].user.profile_picture_urls`, which is why the key occurs three times in the raw bytes (FC-2). The redaction marker occurs exactly twice, on `team.profile_picture_urls.small` and `team.profile_picture_urls.medium` — 211 characters each including the marker — so exactly two strings in this record were signed URLs, and both are the team avatar's two sizes.

What was removed from those two strings is named in the manifest's redaction record:

> "AWS STS X-Amz-Credential and X-Amz-Security-Token values" — `corpus/source-snapshots/round-86/manifest.json` (`sources[S122].redaction.removed`)

The other URL fields are unsigned in this record: `reporter.profile_picture_urls.small` is 92 characters and the three `summaries[0].user.profile_picture_urls` strings carry no `?` at all (FC-2). A presigned avatar is therefore a property of *some* URL fields in the record class, not of the record: a reader cannot infer from "this report is disclosed" that no URL inside it is signed, and cannot infer from one signed URL that every avatar URL is signed.

`attachments` is present as an array at the top level and again at `summaries[0].attachments`, and both hold 0 items in this record (FC-2). This capture demonstrates no attachment URL shape at all; the carrier exists in the record and is not exercised here.

## Claim 2 — SigV4 says a temporary-credential request carries the session token in `X-Amz-Security-Token`, in the header or the query string

> "Instead of using long-term credentials to sign a request, you can use temporary security credentials provided by AWS Security Token Service (AWS STS)" — `corpus/source-snapshots/round-87/S124.txt:81-82`

> "X-Amz-Security-Token to the Authorization header or include it in the query string to hold the session token." — `corpus/source-snapshots/round-87/S124.txt:84-85`

So the field is a container, and what it holds is the session token for a temporary credential: a captured request carrying it carries credential material for as long as the token is valid. The placement is not fixed — the page says some services require the field inside the canonical request and others only add it after the signature is calculated (`corpus/source-snapshots/round-87/S124.txt:86-89`) — so a scan that reads only a URL's query string sees one of at least two placements, and the instrument matches the header and JSON-key spellings as well as the query string (instrument lines 23-25).

## Claim 3 — the IAM prefix table separates an access-key id from the secret that makes it usable

> "IAM uses the following prefixes to indicate what type of resource each unique ID applies to." — `corpus/source-snapshots/round-87/S125.txt:304-305` (section heading "Understanding unique ID prefixes" at `:303`; the table has 12 prefix codes, FC-3)

The table renders one cell per line. `AKIA` (`:318`) is followed by `Access key` (`:319`), and `ASIA` (`:330`) by:

> "Temporary (AWS STS) access key" — `corpus/source-snapshots/round-87/S125.txt:331`

> "IDs use this prefix, but are unique only in combination with the secret access key and the session token." — `corpus/source-snapshots/round-87/S125.txt:332-333`

Lane reading of those three lines: the prefix classifies the *identifier*, and the id is not the credential — the sentence at `:332-333` makes the id unique only in combination with the secret access key and the session token, the two values an id never contains. An `ASIA` id in captured evidence is therefore evidence that temporary credentials were in use, and the material that made them usable is the companion `X-Amz-Security-Token` value of Claim 2, not the id. A scanner flagging both classes is reporting two different things: an identifier shape, and a token value.

## Claim 4 — the documented example key id is the one AWS key id a scanner must not flag

> "X-Amz-Credential=AKIAIOSFODNN7EXAMPLE/20220830/us-east-1/ec2/aws4_request&" — `corpus/source-snapshots/round-87/S124.txt:409`

The page's worked SigV4 examples use this key id in both spellings and both services — header form at `:385` and `:395`, query form at `:409` and `:422` — and all four `AKIA` occurrences in the capture are this one string (FC-4). The instrument carries it as the single built-in allowed value rather than as an allowlist row (`ALLOWED_VALUES`, instrument line 63), so the exception is one exact string and any other 20-character `AKIA`/`ASIA` id is a hit (its selftest case `real-shaped-akid` pins that). An allowlist row cannot substitute for it: a row binds one path, one shape and the sha256 of the matched bytes.

## Claim 5 — an expiring token is still a disclosure incident when the capture is pushed inside its lifetime

> "The JSON held two presigned profile-picture URLs with a HackerOne-issued AWS STS session token" — `corpus/lessons/round-86.md:61`

> "so the token was live when pushed" — `corpus/lessons/round-86.md:61`

The same line records `X-Amz-Date` 2026-11-07T00:58:29Z and `X-Amz-Expires` 3600 s (`corpus/lessons/round-86.md:61`), which puts the end of validity at 2026-11-07T01:58:29Z (FC-5); the manifest's `fetched_utc` for that capture is 2026-11-07T00:58:29Z — the same second — so the URL was signed at fetch time and the freeze commit `252df0c9` was pushed while an hour of validity remained. Expiry bounds the window in which the value is *usable*; it does not un-publish bytes. The redaction repaired the tip only and history was left unchanged ("History is unchanged (no force-push)" at `corpus/lessons/round-86.md:63`), so the pre-redaction bytes — `sha256 ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1`, 9,131 bytes — are still in that commit (`corpus/source-snapshots/round-86/manifest.json`, `redaction.pre_redaction_sha256` and `pre_redaction_bytes`). An expiring credential in a push is a disclosure incident with an end date, not a non-incident.

The class's fix was still open at the round-86 spot-check, which routed it as a defect: `corpus/lessons/round-86-verifier-spotcheck.md:124-127` says the M86-2 fix "is stated, not yet a committed check with a self-test" and asks for it as a pre-commit or pre-freeze step carrying a failing fixture. The round-87 capability `capture-secret-scan` is the instrument that closes it; whether a *commit-time* hook invokes it stays a lane process question, not something this entry measures.

## Claim 6 — the operating rule: scan every capture with `--files` before its first commit, redact the query string, keep the pre-redaction digest

> "run it on every capture before the commit that first adds it" — `corpus/instruments/capture-secret-scan.py:20-21`

The command is `python3 -B corpus/instruments/capture-secret-scan.py --files <path>...`. It scans exactly the named working-tree files, prints one `HIT shape=<s> path=<p> line=<n>` per file and shape, then a `CAPTURE-SECRET-SCAN mode=files scanned=… hits=… files=… allowed=… unused_allow=… rc=…` summary, and exits 0 when nothing matched, 1 when anything matched, 2 on a usage or read error (instrument lines 77-82; round-87 lines 41-46 before the round-88 docstring insertion). The summary never prints a matched value (line 77), so the receipt is safe to commit where the fixture is not.

Redaction is the second half of the rule, and it has two parts: strip the query string, and keep the digest. The capture keeps scheme/host/path (Claim 1's quote) so the record's shape stays readable, and the manifest then carries two digests — `sha256` for the committed bytes and `redaction.pre_redaction_sha256` for the served bytes. Both are load-bearing: the first binds the bytes a reader can open, the second is the surviving proof of what the commit history holds.

The allowlist is the third part, and it is narrow by design: a row is `path<TAB>shape<TAB>sha256-of-matched-bytes<TAB>reason`, one exact value at one path (instrument lines 33-36), and

> "Rows for aws-sts-session-token are refused (a session token is never a false positive)" — `corpus/instruments/capture-secret-scan.py:110-111`

so no row can quiet a session-token hit, and a refused or malformed row is a read error (exit 2) — an attempt to allow a token becomes a loud failure, not a silent pass. An unused row is reported (`unused_allow=` counts rows no scanned match consumed, "reported, not an error" at `corpus/instruments/capture-secret-scan.py:44-45`), so a stale row is visible without blocking a run.

## How a researcher uses this

1. **Scan the file, not the directory, before the first commit.** `--files` names exactly the working-tree paths about to be added (instrument lines 17-19); run it on each new capture and paste the `CAPTURE-SECRET-SCAN … rc=` line into the round receipt.
2. **Read a hit as one of two classes.** `aws-sts-session-token` is credential material (Claim 2); `aws-access-key-id` is an identifier that is unique only with its secret and session token (Claim 3). The first must be removed; the second must be checked against the documented example string before anything else.
3. **Redact the query string and keep the path.** The capture stays readable as a record (Claim 1) while the credential leaves the tip.
4. **Keep the pre-redaction digest.** Record `redaction.pre_redaction_sha256` and `pre_redaction_bytes` beside the post-redaction `sha256`; a reader checking the incident needs the served digest, a reader opening the file needs the committed one.
5. **Do not read `Expires` as a mitigation.** It bounds use, not publication (Claim 5); the window arithmetic is one subtraction.
6. **Do not infer safety from an empty `attachments` array.** The carrier exists in the record class and is simply empty in this one (Claim 1); a record with attachments is the case this capture does not show.

## Falsifiable rule and checks

**Falsifiable rule.** Any sentence asserting that a captured bounty-record JSON is credential-free is falsified by `python3 -B corpus/instruments/capture-secret-scan.py --files <capture>` exiting 1 with a `HIT` line, or by `grep -cE 'X-Amz-Security-Token|(AKIA|ASIA)[A-Z0-9]{16}' <capture>` printing a non-zero count. Any sentence asserting that an expiring presigned URL may be committed is falsified by Claim 5's window arithmetic. Any sentence asserting that an `AKIA`/`ASIA` id is itself a secret is falsified by `corpus/source-snapshots/round-87/S125.txt:332-333`.

**FC-1 — every quoted span is verbatim, exactly-once, on its declared line, and pinned to the capture.** `source-recheck.py` prints `S124:sha256 OK` then `S124:Q01-session-token OK occurrences=1 anchor=84-ok`, `Q02-hold-session-token OK occurrences=1 anchor=85-ok`, `Q03-example-key-id OK occurrences=1 anchor=409-ok`, and for S125 `Q01-prefix-intro OK occurrences=1 anchor=303-ok`, `Q02-sts-key OK occurrences=1 anchor=331-ok`, `Q03-sts-session OK occurrences=1 anchor=332-ok`; both invocations rc 0 (measured this day). The two quotes in this entry that are not S124/S125 text are lane own-work: the redaction tool's sentence and the lesson's two clauses, both cited by file and line.

**FC-2 — the S122 shape counts are measured, not remembered.** This prints counts and string lengths only, never a URL or a value:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B -c "import json;raw=open('corpus/source-snapshots/round-86/S122.txt').read();d=json.loads(raw);out=[]
def w(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items(): w(v,(p+'.'+k) if p else k)
    elif isinstance(o,list):
        for i,v in enumerate(o): w(v,p+'[%d]'%i)
    elif isinstance(o,str) and 'profile_picture_urls' in p: out.append((len(o),'?' in o))
w(d);print('ppu_fields=%d signed=%d lens=%s top_keys=%d summaries=%d attachments=%d/%d marker=%d ppu_key=%d xamz=%d' % (len(out),sum(1 for _,q in out if q),[l for l,_ in out],len(d),len(d['summaries']),len(d['attachments']),len(d['summaries'][0]['attachments']),raw.count('[presigned-query-redacted-r86]'),raw.count('profile_picture_urls'),raw.count('X-Amz-')))"
```

prints `ppu_fields=6 signed=2 lens=[92, 211, 211, 92, 92, 92] top_keys=51 summaries=2 attachments=0/0 marker=2 ppu_key=3 xamz=0` — six avatar-URL strings in the record, two of them signed (the two 211-character team sizes), the other four 92 characters and unsigned, both `attachments` arrays empty, and no `X-Amz-` string left in the capture.

**FC-3 — the quote set and the provider scope are counted.** `for q in "Temporary (AWS STS) access key" "IDs use this prefix, but are unique only in combination with the secret" "X-Amz-Security-Token to the Authorization header or include it in the"; do printf '%s => %s\n' "$q" "$(grep -oF "$q" corpus/source-snapshots/round-87/S12[45].txt | wc -l)"; done` prints `1` for each; `grep -ciE 'azure|shared access signature|google cloud|gcs'` on both captures prints `0`; `grep -cE '^(AKIA|ASIA|AIDA|AROA|ABIA|ACCA|AGPA|AIPA|ANPA|ANVA|APKA|ASCA)$' corpus/source-snapshots/round-87/S125.txt` prints `12`.

**FC-4 — the exception is one exact string.** `grep -n 'AKIA' corpus/source-snapshots/round-87/S124.txt` prints four lines (385, 395, 409, 422) and every one carries `AKIAIOSFODNN7EXAMPLE`; the scanner's selftest prints `SELFTEST aws-doc-example ok got=none` beside `SELFTEST real-shaped-akid ok got=aws-access-key-id`, and `python3 -B corpus/instruments/capture-secret-scan.py --selftest | tail -1` prints `SELFTEST-RESULT pass cases=33` at rc 0 (19 cases in round 87; round 88 added the cloud-shape and practice-scope cases).

**FC-5 — the window is arithmetic on two cited numbers.** `python3 -B -c "from datetime import datetime,timedelta;print('valid_until=%s' % (datetime.fromisoformat('2026-11-07T00:58:29')+timedelta(seconds=3600)).isoformat())"` prints `valid_until=2026-11-07T01:58:29`, from `X-Amz-Date` 2026-11-07T00:58:29Z and `X-Amz-Expires` 3600 s at `corpus/lessons/round-86.md:61`.

**FC-6 — the instrument reads the pinned captures clean and the allowlist is doing work.** `python3 -B corpus/instruments/capture-secret-scan.py --files corpus/source-snapshots/round-87/S124.txt corpus/source-snapshots/round-87/S125.txt` prints `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=2 unused_allow=15 rc=0` (the two allowed matches are the `authorization` allowlist rows pinned for the documented example header); the same command on `corpus/source-snapshots/round-86/S122.txt` prints `scanned=1 hits=0 files=0 allowed=0 unused_allow=17 rc=0` — the redacted capture reads clean without consuming any allowlist row.

## Rejected over-generalizations

1. **"A disclosed report record carries no credentials."** Rejected: S122 is a disclosed record and carried two presigned avatar URLs with a live STS session token (Claim 1, `corpus/lessons/round-86.md:61`).
2. **"A presigned URL is safe to publish because it expires."** Rejected: the token was live when the freeze was pushed, and expiry does not remove history (Claim 5).
3. **"An `AKIA`/`ASIA` id is the credential."** Rejected: the id is unique only in combination with the secret access key and the session token (`corpus/source-snapshots/round-87/S125.txt:332-333`); an id alone authenticates nothing.
4. **"Every signed URL carries these fields."** Rejected: S124 and S125 are AWS's SigV4 and IAM pages and neither mentions another provider's scheme (FC-3); the instrument's other shapes come from the lane's gate, not from these captures.
5. **"The documented example key id means the capture is a fixture."** Rejected: only that exact 20-character string is exempt, and any other `AKIA`/`ASIA` id is a hit (Claim 4, instrument line 63).
6. **"Scanning at freeze time covers the capture."** Rejected: the freeze commit is already in history; the scan must run before the commit that *first adds* the file (instrument lines 18-19, `corpus/lessons/round-86-verifier-spotcheck.md:124-127`).
7. **"An allowlist row can quiet a session token."** Rejected: rows for that shape are refused and a refused row is exit 2 (instrument lines 37-39).

## Honest limit

- **AWS shapes only.** S124/S125 describe AWS SigV4 and AWS IAM identifiers; a presigned URL from another provider is outside both captures, and the scanner's added shapes are exactly the two AWS ones. A non-AWS signed URL in a capture is screened only by whatever the gate's generic patterns catch.
- **The record shows avatar URLs, not attachment URLs.** Both `attachments` arrays are empty in S122 (FC-2), so the attachment carrier is named from the record's key set, not from a demonstrated value.
- **The pre-redaction bytes are not openable at the tip.** They live in the freeze commit `252df0c9`; the working-tree capture is the redacted one, and the only in-tree bindings to the served bytes are the manifest's digests.
- **The scan is a byte-pattern matcher.** It cannot tell a live token from a revoked one, and it reports `unused_allow` rather than failing on a stale row; a clean run means "no matching shape", not "no credential".
- **The incident's commit-time hook is not measured here.** The capability exists and its counter passes; whether a pre-commit hook invokes it on every capture is a process claim this entry does not make.
- **Dates are UTC.** The capture's `fetched_utc` and the presigned URL's `X-Amz-Date` are the same second (2026-11-07T00:58:29Z); the lane's own round labels differ by local-date convention and are not compared here.
- Documentation only: no live target was contacted for this entry — every value is read from pinned lane bytes — and the entry carries no credential material, session, private URL or vault reference. The one key id it quotes is AWS's documented example.
