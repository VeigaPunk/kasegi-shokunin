VERDICT: HOLDS

Second live re-open at 2026-10-28T21:38:44Z. Attacked the export of lane commit `6662a4276b6f7bd61e23e12058414e09dd71b9e4` (archive extracted under this seat's scratch, then removed). The named worktree files are the same blobs as that commit. Capture pins in `corpus/source-snapshots/round-45/manifest.json`: S071 `capture_url` is the RST (`manifest.json:7`), sha256 `manifest.json:15`; S072 `capture_url` is the article API (`manifest.json:50`), sha256 `manifest.json:58`.

## Finding 1 — live RST equals export S071

Attacked: `https://docs.kernel.org/_sources/process/security-bugs.rst.txt` against export `corpus/source-snapshots/round-45/S071.txt` (claimed sha256 `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`).

Command: `curl -sS -L --max-time 60` of that URL, then `sha256sum`, `wc -l`, `wc -c`, and `cmp` against the export snapshot. Same hashes were printed for the worktree path and for `git archive 6662a4276b6f7bd61e23e12058414e09dd71b9e4`.

Output:

```
curl_http_code=200 curl_url_effective=https://docs.kernel.org/_sources/process/security-bugs.rst.txt curl_size_download=20152 curl_content_type=text/plain; charset=utf-8 curl_num_redirects=0
HTTP/2 200
content-type: text/plain; charset=utf-8
last-modified: Sun, 09 Aug 2026 21:57:49 GMT
age: 0
date: Wed, 28 Oct 2026 21:38:44 GMT
x-cache: MISS
content-length: 20152
sha256=0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40
rst_lines=372 s071_lines=372
rst_bytes=20152 s071_bytes=20152
RST_CMP_S071_EXIT=0 EQUAL
```

Worktree and export both printed `0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40`, 372 lines, 20152 bytes. `cmp` of worktree vs export printed `S071_WT_EQ_EXPORT`. Git blob `c7dfecc87764c05e437e9ecccf6605f31907f27c` is the same for the commit path and `git hash-object` of the worktree file.

The five manifest quotes sit on those same bytes. Snapshot lines (identical to the live RST by the cmp above):

- Q5 anchor 20, `S071.txt:20-21`: `with no version indication, your report` / `will not be processed.`
- Q3 anchor 39, `S071.txt:39-40`: `Binary-only executables are not` / `accepted.`
- Q4 anchor 41, `S071.txt:41-43`: line 41 ends `By`; lines 42-43 are `definition if an issue cannot be reproduced, it is not exploitable, thus it` / `is not a security bug.`
- Q2 anchor 95, `S071.txt:95-96`: `If you resorted to AI assistance to identify a bug, you must treat it as` / `public`.
- Q1 anchor 310, `S071.txt:310-311`: `for up to 7 calendar days from the start` / `of the release process, with an exceptional extension to 14 calendar days`.
- Contact, live RST line 281: `<security@kernel.org>`.

## Finding 2 — live HTML is a different byte string; the five quotes still locate in it

Attacked: `https://docs.kernel.org/process/security-bugs.html` against the same export S071.

Command: same curl form, then `sha256sum`, `wc`, `cmp`. A second command stripped tags, unescaped entities, collapsed whitespace, and tested the five quote strings plus `security@kernel.org`.

Output:

```
curl_http_code=200 curl_url_effective=https://docs.kernel.org/process/security-bugs.html curl_size_download=33621 curl_content_type=text/html; charset=utf-8 curl_num_redirects=0
HTTP/2 200
content-type: text/html; charset=utf-8
last-modified: Sun, 18 Oct 2026 23:32:42 GMT
age: 2916
date: Wed, 28 Oct 2026 21:38:44 GMT
via: 1.1 varnish
x-cache: HIT
content-length: 33621
sha256=174a89d065a58c462c5b398255969fbfdd1d300ddb30f95b27959ddbd2980cb2
html_lines=545 s071_lines=372
html_bytes=33621 s071_bytes=20152
HTML_CMP_S071_EXIT=1
differ: char 1, line 1
```

```
Q1 html=True rst=True
Q2 html=True rst=True
Q3 html=True rst=True
Q4 html=True rst=True
Q5 html=True rst=True
ADDR html=True rst=True
html_norm_chars 20512 rst_norm_chars 19701
```

Rendered contact at live HTML line 439: `mailto:security&#37;&#52;&#48;kernel&#46;org` with visible text `security&#64;` / `kernel&#46;org`. Embargo sentence at live HTML lines 464-465. HTML `Last-Modified` is Sun, 18 Oct 2026 23:32:42 GMT; the RST origin `Last-Modified` is Sun, 09 Aug 2026 21:57:49 GMT. The HTML response was a Varnish HIT, age 2916 seconds. Normalized HTML text is longer than normalized RST text (20512 vs 19701 characters).

## Finding 3 — jq -r .body equals export S072; the API response has no Last-Modified

Attacked: `https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section` field `.body`, against export `corpus/source-snapshots/round-45/S072.txt` (claimed sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`).

Command: curl of the API, then `jq -r '.body'` and `jq -j '.body'`, then `sha256sum`, `wc`, and `cmp`. `jq --version` printed `jaq 3.1.1` (`jq` is a shell builtin on this host). Python `json.loads` measured the raw field independently.

Output:

```
curl_http_code=200 curl_url_effective=https://bughunters.google.com/rest/v1/articles/about/rules/about-this-section curl_size_download=10588 curl_content_type=application/json curl_num_redirects=0
HTTP/2 200
cache-control: max-age=300
content-type: application/json
date: Wed, 28 Oct 2026 21:38:45 GMT
server: Google Frontend
content-length: 10588
gapi_has_last_modified=0
keys: body, categories, documentId, public, title
.body type=string character_length=10029
jq_r_sha=364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025
jq_r_lines=312 jq_r_bytes=10032 s072_lines=312 s072_bytes=10032
JQ_R_CMP_S072_EXIT=0
jq_j_sha=5e5a00b83340ab2cfd84b12e724c8991284db1001a437f89ab08662e5ad73f1a
jq_j_lines=311 jq_j_bytes=10031
JQ_J_CMP_S072_EXIT=1
```

Python on the same response body printed `body_utf8_bytes 10031`, `body_endswith_newline True`, `s072_equals_body False`, `s072_equals_body_plus_nl True`. Worktree S072 matched the export (`S072_WT_EQ_EXPORT`) at sha256 `364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025`, 312 lines, 10032 bytes. Git blob `789dc8e2f1cf40ada34f3de2feaed7f1e5c24442` matches the worktree hash-object. The raw JSON is one line (`wc -l` = 0) and its sha256 is `dccfcd4dd98b07bf0202c6271bc46fd4cfd4b3ddbf9d8390f4efc720eca8f6d7`, which is the envelope, not S072.

Header fact: this response has `date` and `cache-control: max-age=300`. It has no `last-modified` header.

## Finding 4 — do-nothing control vs a one-byte mutation

Attacked: the comparison procedure itself, using copies of the export snapshots in scratch (the snapshots were not modified).

Command: copy S071; `cmp` the copy to the export; append one `X` with `printf 'X' >>` on a second copy; `sha256sum`, `cmp`, `wc -l`. Repeat on S072 with `printf 'DRIFT-LINE\n' >>`.

Output:

```
0918dcfa7979f348c9004bf3ce6e183507367185fe69f4e0c7688521e9346f40  S071.identity
CONTROL_IDENTITY_S071_CMP_EXIT=0
c4e40bbf49c2f3a2a045a6c700f910cb63c9ab8a413c50d2f52bb5553c145a3f  S071.mutated
cmp: EOF on S071.txt after byte 20152
CONTROL_MUTATED_S071_CMP_EXIT=1
identity_lines=372 mutated_lines=372 snapshot_lines=372

364166c4a23e5071f6768a158253366db0e8d1ca6f1ce14a9a7384a60ba0a025  S072.identity
CONTROL_IDENTITY_S072_CMP_EXIT=0
e28b444f41298bac376bd40fb3a56a9202b140302be96e712c26c4931488b0ba  S072.mutated
cmp: EOF on S072.txt after byte 10032
CONTROL_MUTATED_S072_CMP_EXIT=1
identity_lines=312 mutated_lines=313 snapshot_lines=312
```

An unmodified copy matches. A changed copy does not. `wc -l` stayed 372 when the mutation was a trailing byte with no extra newline; sha256 and `cmp` still separated it. A newline-terminated extra line moved the S072 count from 312 to 313.

## Limitations

- One GET each, documentation only, at the Date headers above. No second sample, no other mirror.
- HTML was a Varnish HIT (age 2916). The RST was a MISS (age 0) and its bytes matched S071. The manifest records no prior HTML hash, so this re-open does not say whether the HTML bytes changed after `fetched_utc` `2026-10-28T20:52:44Z` (`manifest.json:13`).
- Normalized HTML text is 20512 characters and normalized RST text is 19701. This re-open locates the five cited quotes and `security@kernel.org` in the rendered page. It does not attribute the extra characters.
- The Google response can be cached for 300 seconds and carries no `Last-Modified`. Equality is to this response body.
- `jq` here is jaq 3.1.1. `jq -r '.body'` matches S072. `jq -j '.body'` is the raw UTF-8 field (10031 bytes) and does not match, because S072 is that field plus the extra newline `jq -r` writes. Python `json.loads` agrees with that split.
- `wc -l` alone misses a trailing non-newline byte. The equality calls above use sha256 and `cmp`.
- Scratch for this seat was removed after the commands above. The quoted output is the evidence.
