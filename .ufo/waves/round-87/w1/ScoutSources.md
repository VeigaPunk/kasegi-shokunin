# ScoutSources — independent re-open of the round-87 sources + signed-URL frontier leads (round 87, w1)

Seat: `ScoutSources` (scout, leaf — no delegation, no background jobs).
Fetch window: **2026-11-07 02:50Z – 03:05Z** (all `GET`, instrument UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, `capture-source.py --kind html`).
**No login, no target probing, no scan, no submission** (PROVINCE.md refuses live-target testing).
Scratch: `/fast/scratch/hyaku/kasegi-r87/ScoutSources` (deleted on exit).
Receipts: `.ufo/waves/round-87/w1/ScoutSources-receipts/`
(`live-refetch-r87.txt`, `lead-urls-status-r87.txt`, `scanner-coverage-probe-r87.txt`).
**No `S<digits>.txt` file was written into `w1/`**; no snapshot bytes, no scanner bytes, no counter bytes, and no
credential-shaped value of any kind were written into `w1/` (the three receipts were re-scanned with the landed
instrument: `hits=0`, `rc=0`).

**These are routed defects and qualifiers, never re-scoring.** C1/C2 are judged only on their frozen predicates at
their landing commits.

---

## 0. Headline

1. **Both new sources re-open live and reproduce their manifest sha256 byte-for-byte.** S124 → `88d4f703…2fc2f1cb`
   (manifest-equal), S125 → `65c99351…0de55fe` (manifest-equal). Two independent fetch rounds today plus the two the
   freeze recorded agree byte-for-byte; the pages are stable today.
2. **All 6 manifest quotes occur live, exactly once each, and 5 of 6 sit on their declared anchor line.**
   S124 Q01/Q02/Q03 at lines 84/85/409 — exact. S125 Q02/Q03 at lines 331/332 — exact.
3. **ONE routed defect (D-1): S125 `Q01-prefix-intro` is anchored one line early.** The quote occurs at snapshot
   **line 304**; the manifest declares `anchor: 303`, where line 303 is the *section heading* `Understanding unique ID
   prefixes`. The instrument passes it (`anchor=303-ok`) only because `source-recheck.py`'s anchor window is
   `raw_lines[anchor-1 : anchor+3]` — a four-line window — so a quote one line below the anchor still verifies.
   This is the **4th such off-by-one in the corpus** (see §3), i.e. a live, recurring class, not a one-off.
4. **Four signed-URL credential shapes are documented by first parties and are NOT covered by the landed scanner.**
   GCS V4 (`X-Goog-Credential` / `X-Goog-Signature`), Azure SAS (`sig` / `se`), CloudFront signed URLs
   (`Signature` / `Key-Pair-Id` / `Policy`), and HackerOne's own `expiring_url` attachment field each have an
   official URL, HTTP 200, and a ≤25-word located quote naming the parameter (§4). A scratch-only planted probe shows
   the landed `capture-secret-scan` reports **`hits=0`** for all four while its AWS positive control reports
   `hits=3` (§5). **These are round-88 lead rows, not adoptions and not a C2 defect** — the C2 claim is scoped to the
   two AWS shapes S124/S125 name, and its frozen predicates say nothing about other providers.

---

## 1. S124 / S125 live re-open (the round's two new sources)

Method: `python3 -B corpus/instruments/capture-source.py --id S124 --url <url> --out $S/S124.txt --kind html`
(and the same for S125) into scratch, then digest + quote re-location measured against the **live** bytes.
Receipt: `ScoutSources-receipts/live-refetch-r87.txt`.

| id | URL | HTTP | live sha256 | manifest sha256 | byte-identical | snapshot lines (live `wc -l`) | manifest `lines` |
|---|---|---|---|---|---|---|---|
| S124 | `https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_sigv-create-signed-request.html` | 200 | `88d4f703cef1b9d1cead11053dd9f02692bd4629a7110e42caecc74a2fc2f1cb` | `88d4f703…2fc2f1cb` | **yes** | 437 | 437 |
| S125 | `https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html` | 200 | `65c99351e731b743f18243e93613da7e05b4030d5fe2060a6cc484a320de55fe` | `65c99351…0de55fe` | **yes** | 363 | 363 |

Fetched bytes also match the manifest's `fetch_method` string exactly (S124 raw 57 201 B → snapshot 20 439 B;
S125 raw 47 977 B → snapshot 17 469 B). The manifest record's own `sha256`/`bytes`/`lines` fields are **all true at
the landing commit**.

### 1.1 Per-quote presence, live

| id | quote id | declared anchor | found at | on anchor? | occurrences |
|---|---|---|---|---|---|
| S124 | Q01-session-token | 84 | 84 | **yes** | 1 |
| S124 | Q02-hold-session-token | 85 | 85 | **yes** | 1 |
| S124 | Q03-example-key-id | 409 | 409 | **yes** | 1 |
| S125 | Q01-prefix-intro | 303 | **304** | **NO — see D-1** | 1 |
| S125 | Q02-sts-key | 331 | 331 | **yes** | 1 |
| S125 | Q03-sts-session | 332 | 332 | **yes** | 1 |

**No quote is absent.** The instrument's own verdict on the committed manifest is
`python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-87/manifest.json --source S124`
→ `sha256 OK` + three `OK occurrences=1 anchor=N-ok` lines, rc 0; identically for S125, rc 0.

---

## 2. D-1 (routed defect) — S125 `Q01-prefix-intro` anchor is one line early

**Claim.** The S125 manifest quote `Q01-prefix-intro` occurs at snapshot line **304**, not at its declared
`anchor: 303`.

**Evidence (re-runnable, read-only):**

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
import json
m = json.load(open("corpus/source-snapshots/round-87/manifest.json"))
src = [s for s in m["sources"] if s["id"] == "S125"][0]
q = [q for q in src["quotes"] if q["id"] == "Q01-prefix-intro"][0]
lines = open("corpus/source-snapshots/round-87/S125.txt", encoding="utf-8").read().split("\n")
hits = [i + 1 for i, l in enumerate(lines) if q["quote"] in l]
print("declared_anchor=%d found_at=%s exact=%s" % (q["anchor"], hits, hits[:1] == [q["anchor"]]))
print("line303=%r" % lines[302]); print("line304=%r" % lines[303])
PY
```

Measured output: `declared_anchor=303 found_at=[304] exact=False`; line 303 = `Understanding unique ID prefixes`
(the section heading), line 304 = the quote.

**Why the landed counter does not see it.** `source-recheck.py` verifies a declared anchor against the *four-line
window* `raw_lines[max(0, anchor-1) : anchor+3]` joined, so a quote sitting on line 304 verifies against an anchor of
303. The instrument prints `anchor=303-ok` and rc 0. The manifest's own `note_anchor` explains the neighbouring
choices ("the prefix table renders one cell per line: AKIA (line 318) is followed by 'Access key' (319), ASIA (330) by
'Temporary (AWS STS) access key' (331)") — the manifest author was already tracking exact line numbers for the
table cells, and the same discipline applied to `Q01-prefix-intro` would give **304**.

**Census — this is a recurring class, not a one-off.** Scanning every anchored quote in every
`corpus/source-snapshots/round-*/manifest.json` (577 anchored quotes whose text occurs at least once in its snapshot),
four have an anchor that is not the quote's own line:

| snapshot dir | id | quote id | declared anchor | actual line |
|---|---|---|---|---|
| round-54 | S086 | Q1 | 1 | 2 |
| round-77 | S112 | Q04-params-same | 30 | 31 |
| round-77 | S112 | Q05-pagination-instructions | 31 | 32 |
| **round-87** | **S125** | **Q01-prefix-intro** | **303** | **304** |

The three precedents show the same shape: the anchor names the line *before* the quote (a heading or the first line
of a paragraph), and the instrument's four-line window absorbs the difference. So the class is
"anchor names the anchor-section, not the quote's line", and it has now appeared four times without a corpus-level
check.

**Routing (for the L1 / round 88 — not a re-score of C2).** Options, in the lane's own append-only idiom:
(a) leave S125 as it is and record the class as a known-accepted idiom; or (b) treat the anchor as a *section* anchor
and say so in the manifest record, so the next reader is not misled; or (c) correct the S125 anchor to 304 in a
round-88 superseding record (`supersedes S125 —`, per QUALITY R8) and add a corpus-level check that flags an anchor
whose quote is not on its own line.

**Does this touch a frozen predicate?** **No.** C2's P1 (counter prints `CAPABILITY-CHECK-RESULT pass rc=0`) and P2
(byte-equality of the two instrument files with the frozen candidates) are unaffected: the manifest bytes are pinned
at `9648c7646fa9e569433a5751cd8e7c5b04542b967892aa68b2b9ac7473082d85` in `.ufo/waves/round-87/claims.json`, and my
measurement confirms the committed manifest still hashes to exactly that value. Changing the manifest would break P2's
pin, so **this is a round-88 item, never an in-round edit.**

---

## 3. C1 cross-check (read-only, no re-scoring)

Cheap structural check of the frozen tranche-2 map (no counter run, no census): all **83** map targets resolve to an
existing tracked file once the `:N` / `:N-M` anchor is stripped, and **every declared anchor is inside its target's
line range** (`anchors_out_of_range=0`). The map carries **no** `S124`/`S125` key, and no `corpus/knowledge/*.md`
file cites S124 or S125 yet — consistent with both sources being round-87 additions used only by the instrument.

Re-runnable:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
python3 -B - <<'PY'
import json, re, os
m = json.load(open(".ufo/waves/round-87/c1/repair-map.json"))
missing = out = 0
for k, v in m.items():
    path = re.sub(r":\d+(-\d+)?$", "", v)
    if not os.path.exists(path):
        missing += 1; continue
    mm = re.search(r":(\d+)(?:-(\d+))?$", v)
    if not mm: continue
    a, b = int(mm.group(1)), int(mm.group(2) or mm.group(1))
    n = sum(1 for _ in open(path, encoding="utf-8", errors="replace"))
    if not (1 <= a <= b <= n): out += 1
print("map_keys=%d missing_targets=%d anchors_out_of_range=%d" % (len(m), missing, out))
PY
```

Measured: `map_keys=83 missing_targets=0 anchors_out_of_range=0`.

---

## 4. Frontier leads for round 88 — other signed-URL credential shapes (unopened rows)

These are **leads, not adoptions**. Each has a first-party official URL, an HTTP status, and a **≤25-word located
quote that names the parameter**. Full measurements (status, final URL, raw bytes, capture digest, occurrence count,
snapshot line span) are in `ScoutSources-receipts/lead-urls-status-r87.txt`. Every capture below was fetched **twice**
today and is byte-reproducible; none is written into the lane.

**Why this class.** Round 86's incident (lesson M86-2) was a bounty-platform capture that carried a live AWS STS
session token inside a presigned URL. The landed scanner now covers the AWS shapes S124/S125 name. The adjacent risk is
the same *kind* of material in a *different provider's* signed-URL vocabulary — a shape the scanner currently does not
match.

### L1 — Google Cloud Storage V4 signed URLs (`X-Goog-Credential`, `X-Goog-Signature`)

- **Official URL:** `https://docs.cloud.google.com/storage/docs/xml-api/reference-headers` — **HTTP 200**, final URL unchanged.
- **Located quote (11 words, snapshot lines 2325–2338, occurs once):** *"X-Goog-Credential A query string parameter to determine the credential type used."*
- **Located quote (14 words, snapshot lines 2382–2395, occurs once):** *"X-Goog-Signature A query string parameter with the value of a V4 signed URL signature."*
- Corroborating first-party page: `https://cloud.google.com/storage/docs/access-control/signed-urls` — **HTTP 200**;
  *"X-Goog-Signature: The authentication string that allowed requests using this signed URL to access cat.jpeg."*
  (14 words, lines 475–488).
- Credential scope per Google: `X-Goog-Credential` carries `AUTHORIZER/CREDENTIAL_SCOPE` (service-account email **or**
  an HMAC key access ID) — so the parameter can carry a *key identifier*, not only a signature.
- **Note for the round-88 designer:** the `X-Goog-Credential` value is a service-account email or an HMAC access key
  ID (`GOOG1…`-style), **not** an `AKIA`/`ASIA` id — so the landed `aws-access-key-id` pattern cannot match it.

### L2 — Azure shared access signatures (`sig`, `se`)

- **Official URL:** `https://learn.microsoft.com/en-us/rest/api/storageservices/create-service-sas` — **HTTP 200**.
- **Located quote (22 words, snapshot lines 391–404, occurs once):** *"signature sig The string-to-sign is a unique string that's constructed from the fields and that must be verified to authorize the request."*
- **Located quote (12 words, snapshot lines 120–133, occurs once):** *"signedExpiry se Required. The time when the shared access signature becomes invalid,"*
- Corroborating first-party page: `https://learn.microsoft.com/en-us/azure/storage/common/storage-sas-overview` —
  **HTTP 200**; *"One of the query parameters, the signature, is constructed from the SAS parameters and signed with the key that was used to create the SAS."*
  (25 words, lines 43–56).
- The `sig` value is a base64 HMAC-SHA256 of the string-to-sign — a bearer-equivalent secret in the URL.

### L3 — Amazon CloudFront signed URLs (`Signature`, `Key-Pair-Id`, `Policy`)

- **Official URL (canned policy):** `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-canned-policy.html` — **HTTP 200**.
- **Located quote (23 words, snapshot lines 82–95, occurs once):** *"When you create a signed URL using a canned policy, the Signature parameter is a hashed and signed version of a policy statement."*
- **Official URL (custom policy):** `https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-creating-signed-url-custom-policy.html` — **HTTP 200**.
- **Located quote (12 words, snapshot lines 50–63, occurs once):** *"Your query string parameters can't be named Policy, Signature, Key-Pair-Id, or Hash-Algorithm."*
- **Capture hazard for round 88 (measured, worth routing):** the CloudFront Developer Guide serves a **2 410-byte
  JavaScript meta-refresh shell** for several plausible URLs, and `capture-source.py` collapses it to an **18-byte**
  snapshot (`Amazon CloudFront`) — HTTP 200 but no capturable text. Measured shells (all 18 B): the plural-`urls`
  forms `private-content-creating-signed-urls-canned-policy.html`,
  `private-content-creating-signed-urls-custom-policy.html`, `private-content-creating-signed-urls.html`,
  `private-content-signed-urls-canned-policy.html`, `private-content-setting-signed-url-custom-policy.html`,
  `private-content-setting-signed-urls-canned-policy.html`. Measured working captures: the **singular-`url`** forms
  `private-content-creating-signed-url-canned-policy.html` (11 207 B),
  `private-content-creating-signed-url-custom-policy.html` (19 858 B),
  `private-content-signed-urls.html` (8 385 B) and
  `private-content-setting-signed-cookie-custom-policy.html` (21 243 B). This is the same wall round 87 already
  recorded for the S3 SigV4 query-string page (lesson `round-87.md` § Rejected): **the HTTP 200 is not proof of text.**
  A round-88 capture must check the snapshot byte count, not the status.
- Also note `Key-Pair-Id` (`K2JCJMDEHXQW5F` in the docs example) is a **public key id**, not a secret — a scanner
  matching on it would false-positive on the docs' own example.

### L4 — HackerOne's own attachment URL field (`expiring_url`)

- **Official URL:** `https://api.hackerone.com/hacker-reference/` — **HTTP 200**.
- **Located quote (10 words, snapshot lines 236–249, occurs once):** *"A temporary, pre-signed URL to download the attachment file directly."*
- The field is HackerOne's own `expiring_url` on an attachment object; the reference states it expires after 60 minutes
  and that *"there is no separate endpoint to retrieve a single attachment"*. The same field appears in
  `https://api.hackerone.com/customer-reference/` and `https://api.hackerone.com/customer-resources/` (both HTTP 200).
- **Round-86 tie-in (measured):** the *redacted* S122 snapshot in the lane still carries the incident's shape — a
  `profile_picture_urls` entry whose presigned query is replaced by the literal marker `[presigned-query-redacted-r86]`.
  The r86 incident was a **profile-picture** URL, while HackerOne's reference documents `expiring_url` on
  **attachments** — a sibling field, same vocabulary. Worth a round-88 look at whether the scanner's scope should
  cover the HackerOne attachment URL shape, not only AWS SigV4.
- **Documentation gap (measured):** `docs.hackerone.com` serves only a 1 194-byte client-side shell to this lane's
  instrument, and its search endpoints return HTTP 404; `support.hackerone.com` article URLs tried (2) return 404.
  The capturable first-party surface is `api.hackerone.com` — the API reference — not the help centre.

---

## 5. Coverage probe — the landed scanner does not match the other providers' shapes

Scratch-only planted repository (`git init` in a `mktemp -d` under scratch; `git rev-parse --show-toplevel` asserted to
equal the fixture dir; every later call named `-C "$D"`). **The planted bytes stay in scratch and are deleted on exit;
the receipt carries only the scanner's HIT/summary lines, which never print values.**
Receipt: `ScoutSources-receipts/scanner-coverage-probe-r87.txt`.

| planted shape | scanner result |
|---|---|
| AWS STS query + `X-Amz-Security-Token` + `ASIA…` key id (positive control) | `hits=3` — `credential`, `aws-sts-session-token`, `aws-access-key-id`; rc 1 |
| GCS V4 signed URL (`X-Goog-Credential`, `X-Goog-Signature`) | **`hits=0`**, rc 0 |
| Azure SAS URL (`se=`, `sig=`) | **`hits=0`**, rc 0 |
| CloudFront signed URL (`Expires`, `Signature`, `Key-Pair-Id`) | **`hits=0`**, rc 0 |
| HackerOne-style `attachments.s3.amazonaws.com` URL with `X-Amz-Signature` | **`hits=0`**, rc 0 |

**What this is.** A **coverage lead for round 88** (the `coverage` axis is the one C2 sits on). The landed scanner's
two new patterns are `X-Amz-Security-Token` and `\b(?:AKIA|ASIA)[A-Z0-9]{16}\b`; the other providers use
`X-Goog-Signature`, `sig=`, and `Signature=`, and their key identifiers are *not* `AKIA`/`ASIA`-shaped, so nothing in
the current pattern set matches them.

**What this is NOT.** Not a C2 defect, and not a re-score. C2's statement is explicitly scoped to the two AWS shapes
S124/S125 name; the frozen predicates (P1 counter pass, P2 byte-equality) say nothing about other providers, and the
counter's K-limb P3-style checks do not range over them. The r87 scanner is a **capability acquisition for AWS**; the
other providers are an **extension the round did not claim**. Per the C2 kill rule — "the scanner, allowlist and counter
are never changed after the freeze (a seat finding becomes a routed defect for round 88)" — this is routed, not fixed.

**Lane precedent worth citing to round 88:** the r39 wave-2 secret scan already classed
`presigned URLs (X-Amz-Signature|X-Goog-Signature)` as a scan class (`.ufo/waves/round-39/wave2/SentinelSecretsScan.secrets.txt:102`,
count 0 in the corpus at that time). The round-87 instrument narrowed to the AWS shapes; a round-88 extension can pick
that class back up, and the corpus still shows **0** occurrences of the other providers' shapes in the current tree —
so extending the patterns would not produce allowlist churn.

---

## 6. Summary of routed items

| id | kind | one-line | routed to |
|---|---|---|---|
| D-1 | defect (source record) | S125 `Q01-prefix-intro` anchor 303, quote on line 304; passes only via the instrument's 4-line anchor window; 4th instance corpus-wide | round 88 (manifest bytes are pinned in `claims.json` → **not** an in-round edit) |
| L1 | lead (unopened row) | GCS V4 signed-URL parameters `X-Goog-Credential` / `X-Goog-Signature` — official URL, HTTP 200, two located quotes | round 88 |
| L2 | lead (unopened row) | Azure SAS `sig` / `se` — official URL, HTTP 200, two located quotes | round 88 |
| L3 | lead (unopened row) | CloudFront signed URLs `Signature` / `Key-Pair-Id` / `Policy` — two official URLs, HTTP 200, two located quotes; plus the 2 410 B JS-shell capture hazard | round 88 |
| L4 | lead (unopened row) | HackerOne attachment `expiring_url` — official URL, HTTP 200, one located quote; the r86 incident shape lives in the sibling `profile_picture_urls` field | round 88 |
| Q-1 | qualifier | The landed scanner matches **none** of L1–L4's shapes (`hits=0` on a scratch planted set) while its AWS control gives `hits=3` — an extension the r87 claim did not make | round 88 (coverage axis) |

**No finding here changes the frozen predicates of C1 or C2.** C1's map targets all resolve and all anchors are in
range; C2's manifest and both source snapshots are byte-identical to their pins at the landing commit.

---

## 7. Method, hygiene and limits

- **Tools:** `python3 -B` for every script (no `__pycache__` written); the lane's own
  `corpus/instruments/capture-source.py` for every fetch; `corpus/instruments/source-recheck.py` for the manifest
  quote verdict; `corpus/instruments/capture-secret-scan.py` for the coverage probe. No new tool was installed, so no
  tool/version/channel entry is owed.
- **Read-only to the lane:** the only writes are this file and the three receipt files under
  `.ufo/waves/round-87/w1/ScoutSources-receipts/`. Nothing under `corpus/`, no instrument, no `SKILL.md` /
  `PROVINCE.md` / `SCORECARD.md` / `LOG.md` / `SHONEN.md`, no frozen `c1/` / `c2/` / `controls/` byte, and no
  `.ufo/state/` was touched. No git or jj write was performed anywhere.
- **Credential hygiene:** no planted or real `X-Amz-Security-Token`, no `AKIA`/`ASIA` id other than the AWS
  documentation example, no private-key header and no `token=`/`secret:` value was written into `w1/` — the three
  receipts were re-scanned with the landed instrument (`hits=0`, rc 0) and the fixture bytes never left scratch.
- **Scratch:** `/fast/scratch/hyaku/kasegi-r87/ScoutSources`, `TMPDIR` passed explicitly on every capture call, and the
  directory is removed before this seat yields.
- **Limits / unresolved.** (a) The CloudFront Developer Guide's JS-shell wall (§4 L3) means several plausible CloudFront
  URLs yield no text; the two signed-URL pages quoted above are the ones that capture, and I did not exhaustively
  enumerate the guide's file list. (b) `docs.hackerone.com` and `support.hackerone.com` yield no article text to this
  instrument, so the HackerOne attachment-URL lead rests on `api.hackerone.com` only. (c) The §5 probe used
  representative synthetic shapes; a real-world CloudFront or GCS URL may carry additional or differently-formed
  credential parameters that my synthetic set does not exercise — a round-88 extension should be driven from captured
  real examples rather than from my probe. (d) I did not run the knowledge-meter or the C2 counter; the C1/C2 statements
  above are read-only structural checks, and C1/C2 are judged by the L1 on their frozen predicates.
