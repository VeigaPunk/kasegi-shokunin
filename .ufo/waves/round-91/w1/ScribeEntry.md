# ScribeEntry — round 91 wave 1: knowledge-entry candidate (CloudFront signed cookies + user-bound Azure SAS)

Seat: ScribeEntry (leaf; no delegation, no background jobs). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`; C2 landing `1dd0723fbd0bdc01d2244322f8df8c8c6f1adb70`; C1 landing `8a1a00c639ba808a701d1f186aac9ebd0045deaa`; landing receipts `bcbfbde`.

## What was produced

| path (relative to the lane) | what it is |
|---|---|
| `.ufo/waves/round-91/w1/candidate-knowledge-signed-cookies-and-user-bound-sas.md` | the candidate entry for `corpus/knowledge/` — 7 claims, 23 block quotes, 7 falsifiable checks (FC-1…FC-7), 7 rejected over-generalizations, 9 honest limits. Not admitted; the L1 decides. |
| `.ufo/waves/round-91/w1/ScribeEntry.md` | this report |
| `.ufo/waves/round-91/w1/ScribeEntry-receipts/fc-runs.txt` | raw measured output of FC-1…FC-7, one block per check |
| `.ufo/waves/round-91/w1/ScribeEntry-receipts/hygiene-scan.txt` | the landed scanner's run over the three wave files |

Nothing was written outside `.ufo/waves/round-91/w1/` and the scratch root. No lane file, instrument, counter, snapshot, `corpus/`, `SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`, `SHONEN.md`, or frozen `c1/ c2/ controls/ l1/` byte was modified. No git or jj write was issued anywhere; the only git calls were `git show <rev>:<path>` and `git log`.

## Citation table — the 23 quoted spans

Every quote is verbatim under `normalized=whitespace`, ≤25 words, anchored at the declared span, and occurs the declared number of times (FC-1, measured below).

| # | file:line | words | occ | quote (what it supports) |
|---|---|---|---|---|
| 1 | `corpus/source-snapshots/round-91/S133.txt:30` | 13 | 1 | "A SAS secured with Microsoft Entra credentials is called a user delegation SAS." — the form's definition |
| 2 | `S133.txt:31` | 21 | 1 | "Every SAS is signed with a key. To create a user delegation SAS, you must first request a user delegation key" — what signs it |
| 3 | `S133.txt:34` | 24 | 1 | "Shared access signatures are keys that grant permissions to storage resources, and you should protect them just as you would protect an account key." — the credential property |
| 4 | `S133.txt:32` | 10 | 1 | "Stored access policies aren't supported for a user delegation SAS." — no policy-based revocation |
| 5 | `S133.txt:49` | 23 | 1 | "The permissions granted to a client who possesses the SAS are the intersection of the permissions that were granted to the security principal" — blast radius |
| 6 | `S133.txt:56` | 14 | 1 | "No one other than this user will be able to use the SAS token." — user-bound narrowing |
| 7 | `S133.txt:565` | 16 | 1 | "When specified, the caller must also send a Bearer token; its oid claim must match sduoid." — use requires that identity |
| 8 | `S133.txt:567` | 20 | 1 | "The skdutid field represents the tenant ID (tid) of the Microsoft Entra security principal that will use the SAS token." — manifest `Q02-skdutid-tenant`, anchor 567 |
| 9 | `S133.txt:571` | 12 | 1 | "The sduoid and skdutid fields are supported with version 2025-07-05 and later." — manifest `Q01-skdutid-version`, anchor 571 |
| 10 | `S133.txt:869` | 16 | 1 | "The following example shows a blob URI with a user delegation SAS token appended to it." — the carrier is the URL |
| 11 | `S133.txt:880` | 16 | 1 | "The delimiter that precedes the query string. The delimiter is not part of the SAS token." — query-string carrier |
| 12 | `S133.txt:922` | 24 | 1 | "Used to authorize access to the blob. The signature is an HMAC that's computed over a string-to-sign and key by using the SHA256 algorithm" — `sig=` authorizes |
| 13 | `S133.txt:924` | 22 | 1 | "You can revoke a user delegation SAS either by revoking the user delegation key, or by changing or removing RBAC role assignments" — revocation is a key action |
| 14 | `S133.txt:86` | 16 | 1 | "You can specify that the key is valid for a period of up to seven days." — the window's outer bound |
| 15 | `corpus/source-snapshots/round-91/S134.txt:17-19` | 17 | 1 | "and a CloudFront signed cookie requires three name-value pairs. The name-value pairs are: CloudFront-Policy, CloudFront-Signature, and CloudFront-Key-Pair-Id." — manifest `Q02-three-pairs`, anchor 17 |
| 16 | `S134.txt:22-23` | 25 | 1 | "The values must be present on the viewer before a user makes the first request for a file that you want to control access to." — the viewer presents the set |
| 17 | `S134.txt:25-28` | 11 | 1 | "In general, we recommend that you exclude Expires and Max-Age attributes." — browser lifetime, not authority |
| 18 | `S134.txt:91` | 14 | 1 | "The policy statement controls the access that a signed cookie grants to a user." — the policy bounds the grant |
| 19 | `S134.txt:92-95` | 14 | 1 | "It includes the files that the user can access, an expiration date and time" — the bounds named |
| 20 | `S134.txt:97-98` | 11 | 1 | "A hashed, signed, and base64-encoded version of the JSON policy statement." — manifest `Q01-signature-cookie`, anchor 97 |
| 21 | `S134.txt:102-105` | 24 | 1 | "CloudFront compares the information in the signature with the information in the policy statement to verify that the URL has not been tampered with." — the validation test |
| 22 | `S134.txt:255-258` | 19 | 1 | "The expiration date and time for the URL in Unix time format (in seconds) and Coordinated Universal Time (UTC)." — the end instant is in the record |
| 23 | `S134.txt:419-420` | 8 | **2** | "Replace these invalid characters With these valid characters" — the URL-safe alphabet table; the same two-line header recurs at `:196-197` |

Two short inline quotations are additionally used and were checked by the same run (they are substrings of rows 3, 12, 13, 14, 21 and of the spans at `S134.txt:27-28`, `:93-95`, `:106-107`): "which reduces the possibility of someone getting unauthorized access" (`S134.txt:27-28`), "an optional date and time that the URL becomes valid, and an optional IP address or range of IP addresses that are allowed to access the file" (`S134.txt:93-95`, 26 words — prose, not a block quote), "This public key must belong to a key group that is a trusted signer in the distribution" (`S134.txt:106-107`), and "anyone with the signed URL can access" (`corpus/source-snapshots/round-89/S130.txt:163`, cited only as the sentence this entry refuses to transfer).

## Citation table — line references that are not block quotes

| file | lines | what each supports |
|---|---|---|
| `corpus/instruments/capture-secret-scan.py` (rev `1dd0723`) | `1-105` | the docstring read as the instrument's specification |
| | `14-21`, `176-181` | capture-class path scope; `is_capture_path` |
| | `19-21` | `--files` is for the file about to be committed |
| | `47-52` | the round-91 Azure widening: 2-7 letters, `skdutid`, 8-letter limit |
| | `53-80`, `67-80` | the two CloudFront shapes; the cookie shape's definition |
| | `81-87` | the named limits (HAR/JSON name-value, percent-encoded, 8+ letters, >20 params, soft-wrap, gzip/UTF-16/base64) |
| | `84-85` | 8+ letter Azure names end the window |
| | `90-97`, `192-199` | allowlist row form and its `(path, shape, sha256)` keying |
| | `95-97`, `157-159` | refused/malformed row is exit 2 |
| | `99-104`, `234-246`, `243`, `370-374` | output form, `report()`, `rc = 1 if hits else 0`, exit 2 |
| | `100` | the base revision's `{2,6}` window (`bb4309f`) |
| | `122` | the landed `{2,7}` `_PARAM` |
| | `130`, `138-139` | the cookie left boundary and pattern |
| | `139` | the URL-safe alphabet class |
| | `307-316` | the ten new selftest cases (2 Azure positive, 1 Azure negative, 3 cookie positive, 4 cookie negative) |
| | `309`, `312` | the 8-letter negative and the 28-character documentation-example negative |
| `corpus/source-snapshots/round-91/S133.txt` | `86`, `540` | key lifetime cap; `ske` states the end |
| | `926` | revocation is cached, not instantaneous |
| | `568` | the bearer token's `tid` claim must match `skdutid` |
| `corpus/source-snapshots/round-91/S134.txt` | `93-95` | the remaining policy bounds (start time, IP range) |
| | `106-107` | the key-pair id names a trusted-signer public key |
| | `123` | the 28-character documentation example (cited by line only, never by value) |
| | `196-197`, `421-426` | the alphabet table's second occurrence and its `+`/`=`/`/` mapping rows |
| `corpus/source-snapshots/round-89/S130.txt` | `163` | the signed-URL possession sentence this entry refuses to transfer to cookies |
| `corpus/SOURCES.md` | `145`, `146` | the tier-A rows for S133 and S134 |
| | `318-319`, `145-146` | both rows are `queued` with `used-by —` in the round-91 freeze |
| `SCORECARD.md` | `307` | the `capture-secret-scan` capability row |

## Self-check — every quote appears verbatim

FC-1 of the candidate (the block is in the entry, re-runnable as written) prints one line per span and a verdict. Measured 2026-11-07, rc 0:

```
S133:30-30 occurrences=1 expected=1 anchored=y words=13 OK
S133:31-31 occurrences=1 expected=1 anchored=y words=21 OK
S133:34-34 occurrences=1 expected=1 anchored=y words=24 OK
S133:32-32 occurrences=1 expected=1 anchored=y words=10 OK
S133:49-49 occurrences=1 expected=1 anchored=y words=23 OK
S133:56-56 occurrences=1 expected=1 anchored=y words=14 OK
S133:565-565 occurrences=1 expected=1 anchored=y words=16 OK
S133:567-567 occurrences=1 expected=1 anchored=y words=20 OK
S133:571-571 occurrences=1 expected=1 anchored=y words=12 OK
S133:869-869 occurrences=1 expected=1 anchored=y words=16 OK
S133:880-880 occurrences=1 expected=1 anchored=y words=16 OK
S133:922-922 occurrences=1 expected=1 anchored=y words=24 OK
S133:924-924 occurrences=1 expected=1 anchored=y words=22 OK
S133:86-86 occurrences=1 expected=1 anchored=y words=16 OK
S134:17-19 occurrences=1 expected=1 anchored=y words=17 OK
S134:22-23 occurrences=1 expected=1 anchored=y words=25 OK
S134:25-28 occurrences=1 expected=1 anchored=y words=11 OK
S134:91-91 occurrences=1 expected=1 anchored=y words=14 OK
S134:92-95 occurrences=1 expected=1 anchored=y words=14 OK
S134:97-98 occurrences=1 expected=1 anchored=y words=11 OK
S134:102-105 occurrences=1 expected=1 anchored=y words=24 OK
S134:255-258 occurrences=1 expected=1 anchored=y words=19 OK
S134:419-420 occurrences=2 expected=2 anchored=y words=8 OK
QUOTE-CHECK pass spans=23 bad=0
```

The check binds three things per span: the normalized count equals the declared count, the first 40 normalized characters fall inside the declared line span, and the word count is ≤25. The one span declared twice (`:419-420`) is disclosed in the entry with its second location (`:196-197`).

## Gates run (all rc 0, all measured, none re-run for decoration)

| check | measured result |
|---|---|
| FC-1 quote check | `QUOTE-CHECK pass spans=23 bad=0` |
| FC-2 digests + recheck + clean scan | S133 `56d858ac…6cd6`, S134 `ddf45b80…f1cc` (equal to the manifest); six `OK` lines from `source-recheck.py` (three per capture); `CAPTURE-SECRET-SCAN mode=files scanned=2 hits=0 files=0 allowed=0 unused_allow=19 rc=0` |
| FC-3 landed-vs-base discrimination | landed: `HIT shape=cloudfront-signed-cookie-signature` on the Set-Cookie and JSON-joined fixtures, `HIT shape=azure-sas-signature` on the `skdutid` fixture, each `hits=1 … rc=1`; base (`bb4309f`, sha256 `95f24a54…d20ec`): `hits=0 … rc=0` on all three |
| FC-4 selftest | ten `SELFTEST …` lines (5 shape, 5 `got=none`), then `SELFTEST-RESULT pass cases=53` |
| FC-5 named limits + provider disjointness | `S133 cloudfront=0`, `S134 azure=0`; lowercase name, 39-character value, 8-letter parameter name, HAR/JSON name-value object all `hits=0 … rc=0` |
| FC-6 redaction blocks | `r91_redaction_blocks=0` |
| FC-7 abbreviation window | histogram `8 2 / 15 3 / 6 4 / 4 5 / 1 6 / 1 7` (35 distinct abbreviations, max 7 letters); the single 7-letter line is `skdutid` |
| hygiene | the landed scanner over the entry, this report and the receipts dir: `hits=0 … rc=0` (receipt `ScribeEntry-receipts/hygiene-scan.txt`) |

## Findings — routed, not re-scoring

1. **The candidate is not admitted, and admission needs two `corpus/` edits this seat may not make.** `corpus/SOURCES.md:145` (S133) and `:146` (S134) are tier A and `queued` with `used-by —`. If the L1 admits the entry, those two rows should record the entry as their use. Confirm the current state with `grep -n '| S133 |\|| S134 |' corpus/SOURCES.md`. No knowledge index lists entries (`grep -rln 'cloud-signed-url-credentials-in-captured-evidence' corpus/` returns nothing), so no index row is missing.
2. **S134 states no possession rule for cookies, and the entry does not invent one.** `grep -ciE 'anyone|bearer|possession|whoever' corpus/source-snapshots/round-91/S134.txt` prints `0`; S133 prints `0` for `anyone|possession` and `5` for `bearer token`. The cookie reading therefore rests on `S134.txt:22-23`, `:91-95` and `:102-105`, and the entry's honest-limit section says so and names the sentence it refuses to transfer (`corpus/source-snapshots/round-89/S130.txt:163`). A round that wants a vendor-stated possession sentence for cookies has no source in this lane: S135 (canned-policy cookies) was rejected in the round-91 freeze.
3. **The 2-7 bound is the page's own maximum, not a guess.** FC-7 measures 35 distinct abbreviations on S133's field table, none longer than seven letters, with `skdutid` the only seven-letter one. A future widening to eight letters would be unsupported by S133 and would need a source whose field table carries such a name — route that as a sourcing requirement, not a scanner change.
4. **The HAR/JSON name-value form is a measured blind spot, not a hypothesis.** FC-5's `G-har-name-value` fixture (a cookie recorded as a JSON name/value object) reads `hits=0`, matching the docstring's named limit at `capture-secret-scan.py:81-83`. A capture that stores cookies as JSON objects is outside the shape; closing it needs a new shape and its own source.
5. **The cookie shape is a name-plus-value match, not a set match.** It fires on the signature pair alone, without `CloudFront-Policy` or `CloudFront-Key-Pair-Id` in the same text (`:67-80`; selftest `cf-cookie-set-cookie` at `:310` carries only the signature pair plus attributes). That is the right detector behaviour — a lone signature is still credential material — but a reader should not infer that a hit proves a *usable* set. The entry's Claim 1 says the credential is a set and Claim 5 says the shape matches one pair; the two are deliberately kept apart.
6. **Qualifier on FC-3/FC-5's scratch form.** Both checks create a `<1 KB` fixture under `mktemp -d -p "${TMPDIR:-/tmp}"`, following the admitted round-88 entry's FC form; the seat's own runs used `TMPDIR=/fast/scratch/hyaku/kasegi-r91/ScribeEntry`. A re-runner who cares about the scratch directive should export `TMPDIR` to a scratch dir first. The fixtures are deleted by each block's last line; the receipts carry only `HIT`/summary lines and one digest, never fixture bytes.

## Out of scope (deliberately not done)

- No admission decision, no `corpus/knowledge/` write, no `corpus/SOURCES.md` update, no `SCORECARD.md`/`LOG.md`/`SHONEN.md` edit — all L1 territory.
- No verification of C1 or C2: the claims are judged on their frozen predicates at the landing commits by the L1, and this seat ran no `knowledge-meter.py` and no `capability-check.py`. The scanner runs above are the entry's own evidence, not a claim verdict.
- No live target, no request, no cookie replay, no SAS use. Only the two pinned captures and the landed instrument's bytes were read.
- No tool was installed or upgraded; no package manager was invoked.

## Credential hygiene

- No credential-shaped value was written into any wave file. The entry uses `<signature>`, `<redacted>`, `<key-pair-id>`, `<object-id>` and `<tenant-id>` placeholders only; the 28-character documentation example at `S134.txt:123` is cited by line, never by value.
- Fixtures (seven in FC-3/FC-5, synthetic `FAKECF…`/`FAKEAZ…` values and an all-zero GUID) exist only in scratch and are deleted; the receipts carry `HIT`/summary lines and one instrument digest.
- No scanner, counter or `S<digits>.txt` snapshot was copied into the wave dir.
- The landed scanner over the three wave files reads `hits=0 … rc=0`.

## Scratch

Scratch root `/fast/scratch/hyaku/kasegi-r91/ScribeEntry/` held the seven fixtures, the base instrument extracted with `git show bb4309f:…` (plus `claim-package-check.py` beside it), the extracted FC scripts and the FC outputs. **It is deleted** (`trap 'rm -rf -- "$S"' EXIT` fired; the directory is gone).

## Artifacts

- `.ufo/waves/round-91/w1/candidate-knowledge-signed-cookies-and-user-bound-sas.md`
- `.ufo/waves/round-91/w1/ScribeEntry.md`
- `.ufo/waves/round-91/w1/ScribeEntry-receipts/fc-runs.txt`
- `.ufo/waves/round-91/w1/ScribeEntry-receipts/hygiene-scan.txt`
