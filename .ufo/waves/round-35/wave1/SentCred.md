# SentCred — round-35 credential/secret scan (wave 1, leaf seat)

Seat `SentCred`, leaf of the L2 wave of kasegi-shokunin round 35. Lane
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `3266c9937b03062d9bbc2f436e20820115ed179c`,
claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`. Judged axes: `depth:verifiability`,
`coverage`. No subagents, no commits, no writes outside the lane.

## Report

### Scope

Every artifact new this round, enumerated by the lane itself rather than by a hand list:
`git diff --name-only <base>` (modified vs the frozen base) plus `git ls-files --others
--exclude-standard` (untracked). At the pinned instant that is **160 files / 4,429,153 bytes**:
the S052 capture (1,479,694 B), `corpus/source-snapshots/round-35/manifest.json`, the F18 entry
`corpus/knowledge/cisa-kev-catalog.md`, the round-35 SOURCES/README/SKILL/SCORECARD edits,
`corpus/instruments/r35-defect-closure.sh` with `corpus/instruments/r35-fixtures/**` (56 fixture
files), `.ufo/waves/round-35/**` (claims, spec/dispatch/plan, `assimilation/`, `c1-controls/`,
`c2-controls/`, `claims-erratum-d5.md`, and every landed `wave1/*.md` receipt with its logs), and
the newly tracked `.ufo/waves/round-34/wave1-results.json` with its provenance note.

### Verdict

**CLEAN — no credential material, no session/auth value, and no private URL in any new artifact.**

`blocking_findings: 0`. The refuse clause ("if the KEV capture contains credential material,
refuse it and report the location") is **not triggered**: `refused: false`.

The capture is **pure JSON**: `json.loads` over the raw bytes succeeds with five top-level keys
(`title`, `catalogVersion`, `dateReleased`, `count`, `vulnerabilities`), 1,756 records each with
the same 12 keys, first bytes `7b0a` (`{\n`), last bytes `0a7d0a` (`\n}\n`), no BOM, no HTML
wrapper, no NUL (`cmp_exit=0`), no ESC/ANSI (`0`), no non-ASCII byte (`LC_ALL=C grep -c '[^ -~]'`
→ `0`). Nothing in the feed's bytes is a secret.

### Method (commands, output, exit codes)

Two independent implementations, so a single regex mistake cannot produce the verdict:

**1. Seat scanner** (committed attachment, re-runnable):

```
$ python3 .ufo/waves/round-35/wave1/SentCred/credscan.py --root . --show-s3
scan root=/home/vgpnk/Projects/shokunin/kasegi-shokunin base=3266c9937b03062d9bbc2f436e20820115ed179c
files=160 bytes=4429153 excluded_self=1
S1 … / S2 …                     (none printed)
S3 cleartext_http_url … (4) / S3 email_address … (2) / S3 tracking_param … (2) / S3 private_ip_literal … (1)
s1=0 s2=0 s3=9 exit=0
                                                                              # shell EXIT=0
```

Classes: **S1 credential material** — AWS access-key ids, GitHub/Slack/Stripe/OpenAI(op-anchored)/
Google keys, JWT triples, PEM private-key blocks, SSH public keys, `op://` vault references,
AGE secret keys, GitLab PATs, SendGrid keys, Docker PATs, PyPI tokens, `_authToken=`.
**S2 session/auth values** — `Authorization:`/`Cookie:`/`Set-Cookie:` with a bearer/basic/digest/
token/session value, `Bearer <value>`, `Basic <value>`, `password|passwd|pwd|api_key|access_key|
secret_key|client_secret|session_id|csrf_token = value`, userinfo URLs (`https://user:pass@`),
`?token=|?key=|?sig=|?signature=` parameters, `.netrc`/`id_rsa`/`.ssh/`/`.aws/credentials`/
`.config/gh`, `x-api-key:`. **S3 triage** (printed, never counted as a hit) — addresses,
tracking parameters, cleartext `http://` URLs, private-IP literals.

**2. POSIX-ERE cross-check** (grep, no Python), over the same file list:

```
$ grep -rInE -f <p-cs2: token formats> -- <160 paths>      →  (no output)
$ echo $?                                                   →  CS_EXIT=1
$ grep -rIniE -f <p-ci2: header/assignment/userinfo/query> -- <160 paths>  →  (no output)
$ echo $?                                                   →  CI_EXIT=1
```

`grep` exit 1 = no match, i.e. zero hits. A superset scan with looser patterns was run first and
returned exactly 10 lines, every one a false positive — catalogued in §C6 so they are not re-filed
as findings: the unanchored `sk-` form matched hyphenated URL slugs (`…significant-risk-known-
exploited-…`, `ask-using-ai-models-…`), and `authorization:` matched the prose "read neither as
scope or authorization: 360SRC's…" at `corpus/README.md:335`.

**3. Capture structure and hygiene:**

```
$ python3 -c 'import json;d=json.load(open("corpus/source-snapshots/round-35/S052.txt"));…'
toplevel_keys 5 records 1756 count 1756                                   # exit 0
$ head -c 2 S052.txt | xxd -p ; tail -c 3 S052.txt | xxd -p
7b0a / 0a7d0a                                                             # exit 0
$ LC_ALL=C grep -c '[^ -~]' S052.txt ; LC_ALL=C grep -c $'\x1b' S052.txt
0 / 0                                                                     # exit 1 (no match)
$ tr -d '\000' < S052.txt | cmp -s - S052.txt ; echo cmp_exit=$?
cmp_exit=0                                                                # exit 0
$ stat -c '%a %n' S052.txt manifest.json cisa-kev-catalog.md r35-defect-closure.sh
644 / 644 / 644 / 755
$ wc -l < S052.txt                        → 27870
```

### Findings

**C1 — no credential material anywhere (blocking class S1 = 0).** Zero hits for every provider
key shape, private-key block, `op://` reference with a payload, AGE key, GitLab PAT, SendGrid key,
Docker PAT, PyPI token and npm auth line across all 160 artifacts. The capture's 12-key record
schema contains no key that could hold a secret: `cveID, vendorProject, product, vulnerabilityName,
dateAdded, shortDescription, requiredAction, dueDate, knownRansomwareCampaignUse, forensicTriage,
notes, cwes` (one key set across all 1,756 records).

**C2 — no session/auth value (blocking class S2 = 0).** The words appear only as vulnerability
prose: `password` 47×, `authorization` 62×, `session` 34×, `token` 21×, `credential` 52×,
`login` 25×, `cookie` 4×, `secret` 5×, `bearer` 1×, and every one is a description of a *class*
of bug, never a value — e.g. `S052.txt:15422` "Atlassian Questions For Confluence App has
hard-coded credentials, exposing the username and password in plaintext" (no value),
`S052.txt:24630` "uses the same API key by default" (no value), `S052.txt:1011` "an arbitrary
Bearer token" (no value). `op://` occurs **0** times in the capture.

**C3 — closest item: one published account *name*, no password value.** `S052.txt:27859`
(CVE-2020-29583, Zyxel): `contains a use of hard-coded credentials vulnerability in an undocumented
account ("zyfwp") with an unchangeable password.` This is the only literal credential identifier
in the capture. Classification: **publicly published vulnerability data** (the account name is in
the vendor's own advisory and in NVD), **not credential material** — no password, hash, token or
URI accompanies it, and nothing here is usable from the capture alone. No redaction is required;
recorded so the L1 knows the string exists before any artifact describes the capture as carrying
"no credential".

**C4 — personal data: two public mailing-list addresses, five message-id slugs, no other PII.**
All eight `@` occurrences in the capture are accounted for:
`S052.txt:355` `updates@lists.opensuse.org` (inside an `https://lists.opensuse.org/archives/list/…`
URL), `S052.txt:9800` `…20240610090330.1347021-2-lee@kernel.org` (inside a `lore.kernel.org/linux-
cve-announce/…` URL), and five lore.kernel.org message-id slugs ending `@gregkh` at `L2725, L6982,
L6998, L7510, L7958` (no domain — message ids, not addresses); `L3397` is the CSS token `@import`
in prose. Both addresses are published archive addresses inside the URL that carries them, already
public in CISA's and NVD's feed; the lane introduces no new exposure. Zero hits for phone, SSN,
passport, wallet, SSH/PGP key, or `Mr./Mrs./Ms./Dr.` forms; no structured PII field exists in the
schema. Vendor strings such as `Dassault Systèmes` (9 `è`) are companies, not people.

**C5 — private URLs: zero. Two vendor tracking parameters and one cleartext link set.** No
private-IP, loopback, `.internal/.corp/.lan/.local`, userinfo-embedded or signed URL anywhere;
all 288 distinct hosts in the capture match a public-domain shape (3399 `https` + 7 `http` URLs).
Two URLs carry third-party marketing identifiers, both vendor-published in the feed and neither a
credential nor a session value: `S052.txt:2316` Check Point `?_gl=1*1wqeqhc*_gcl_au*MTI1…`
(Google linker/Ads id) and `S052.txt:13892` IBM X-Force `?_ga=2.189195179.1800390251…`
(GA client id); a PaperCut vendor tracking id sits at `S052.txt:1133` (`?lid=2oneu2wt0ct4`).
Seven quoted advisories are cleartext `http://` at `L355, L2567, L5267, L12069, L12255, L13860,
L25651` — quoted publisher links, never fetch targets of this round. In this round's own artifacts
the only cleartext links are findings *about* probes, not credentials:
`.ufo/waves/round-35/assimilation/quarantine-verdicts.md:62,214` (npc.gov.cn PDF) and `:162` plus
`.ufo/waves/round-35/wave1/ScoutQuarantine.md:107` (`http://kass.sacinfo.org.cn/kfs/token/download/`
— `token` is a path segment of the site, no token value, and the probe returned `curl_rc=60`).

**C6 — false positives, catalogued so they are not re-filed.**
(a) `S052.txt:19370` `10.0.0.50` is **not a private IP**: the record reads "NETGEAR DGN2200 devices
with firmware through 10.0.0.50" — a firmware version. Any private-IP scan over this capture must
treat that line as a false positive.
(b) The unanchored `sk-` key form matches hyphenated URL slugs in 6 artifacts (three wave
prompts/specs and `SOURCES.md:15`, `ScoutKEVLive.md:72,76`, `ScribeSearchLog.md:31`).
(c) `corpus/README.md:335` "read neither as scope or authorization: 360SRC's …" is prose, not a
header.
(d) The literal `op://` appears in exactly four wave files as **task text with no payload**
(`build-spec.py:691`, `wave1-dispatch.json:1046`, `wave1-plan.out:1051`, `wave1-spec.json:621`);
it is the scan instruction, not a vault reference.

**C7 — provenance of the capture (trust boundary).** The capture came over HTTPS from
`https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
(`manifest.json`), fetched by `corpus/instruments/capture-source.py --id S052 --kind text` with a
`User-Agent` only — no `Cookie`, no `Authorization`, no credential of any kind (instrument UA
`kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)`, where
`shokunin.invalid` is RFC-2606 reserved and not resolvable). The body is public federal data.
Two fetches 40 s apart produced the identical sha256 (manifest `purpose`), and the committed bytes
hash to the manifest's pinned digest (§Digests). One data-fidelity note, not a credential issue:
the feed itself carries U+FFFD in two records (`CVE-2021-41773`, `CVE-2020-4428`
`shortDescription`) and a full-width `＿` in one URL (`CVE-2022-23227` `notes`); the capture
preserves the corruption rather than repairing it.

**C8 — the entry's credential claim is true; its `(Q6)` is the entry bar, not a manifest
assertion.** `corpus/knowledge/cisa-kev-catalog.md:117` states "the capture carries no credential,
session or private URL, and this entry quotes no such line (Q6)". Independently confirmed by this
seat (C1–C5). `(Q6)` resolves to `corpus/QUALITY.md:19` (entry bar Q6, the documentation-only
criterion naming "credential material, session or private URL, or vault-reference URI"), **not** to
the round-35 manifest, whose quote ids are only `Q1…Q5` (`manifest.json`; `grep -c 'Q6'
cisa-kev-catalog.md` → 1). It is therefore not a dangling reference — but it *reads* like one,
because the neighbouring bullets cite manifest Q3/Q4/Q5 by the same notation. Observation only,
no defect filed: the claim is verified, and a reader who checks it against the manifest will look
for an id that is not there. If the L1 wants it unambiguous, the smallest edit is to spell the
citation as `QUALITY Q6` in that bullet, not to add a manifest assertion — `source-recheck.py`
fails an `occurrences=0` assertion (`corpus/instruments/source-recheck.py:203-210`,
`reason=quote-not-found`), so an absence claim cannot be expressed in the manifest schema at all.

**C9 — operator path, pre-existing.** `/home/vgpnk/…` appears throughout the new artifacts, as it
does in the repo already: `git grep -c '/home/vgpnk' <base> | wc -l` → **3222 files** carry it at
the frozen base. Not a new exposure and not a secret; recorded as INFO because the handoff's
absolute-path convention puts it in every receipt.

### Digests (pinned at 2026-10-26T06:46:25Z)

```
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt        (1479694 B, 27870 lines)
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json   (5631 B)
0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74  corpus/knowledge/cisa-kev-catalog.md     (06:46:25Z pin; observed chain, all scanned clean: da81204b… → 7429811c… → 09888666… → e3f233c0… at 06:47:26Z)
a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad  corpus/instruments/r35-defect-closure.sh (06:46:25Z pin; observed chain d7ad8438… → 8b8c2420… → a4f80067… → 0ae4b484… at 06:47:26Z)
b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113  corpus/instruments/r35-fixtures/fixtures.json
0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176  .ufo/waves/round-35/c2-controls/junk-f18.md
292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121  .ufo/waves/round-35/c1-controls/fake-suite.sh
07dbcba3fe8430ad1364ec2564a3df58d1537019dd94fb378f62fbc4a4cc0896  .ufo/waves/round-35/wave1/SentCred/credscan.py
7e598c6e45d5aca6dcb2d4b22a592e2b7b1817523a44947591cee8d5748077c3  .ufo/waves/round-35/wave1/SentCred/scan-hits.txt (1259 B)
7578699b2e0af0a7c258def45b8bb892191d9e900c2f9157f7e30a11541ddf81  .ufo/waves/round-35/wave1/SentCred/artifacts.sha256 (160 lines, one per scanned path)
```

### Limits

- **Point-in-time, on a tree in flight.** Peers were still landing receipts while this seat ran.
  The F18 entry moved `da81204b…` → `7429811c…` → `09888666…` and the closure suite
  `d7ad8438…` → `8b8c2420…` → `a4f80067…`; every state was scanned and every state was clean.
  The verdict binds the digests above, not later ones: re-run §Re-run after closure.
- The scan reads bytes; it cannot prove a secret is *absent from a source the capture does not
  contain*. It says nothing about the feed after 2026-10-26T06:32:40Z.
- The capture is 1.41 MiB of a public feed; scanning it as bytes means the S3 triage classes
  (addresses, tracking parameters, cleartext links) will always carry legacy vendor noise. That
  noise is vendor-published, not lane-introduced, and is enumerated above by line.

### Re-run

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  python3 .ufo/waves/round-35/wave1/SentCred/credscan.py --root . --show-s3 ; echo exit=$?
# expected: files=<n> s1=0 s2=0 exit=0 ; exit=3 means a blocking class hit ; exit=2 means a path vanished
```

### Structured summary

```json
{
  "seat": "SentCred",
  "wave": "round-35/wave1",
  "scope": "credential/secret scan of every new round-35 lane artifact",
  "verdict": "CLEAN",
  "blocking_findings": 0,
  "refused": false,
  "flag": [
    {"severity": "INFO", "item": "published account name 'zyfwp' in the KEV capture (CVE-2020-29583); public CVE text, no password value", "location": "corpus/source-snapshots/round-35/S052.txt:27859"},
    {"severity": "INFO", "item": "two public mailing-list addresses and five @gregkh message-id slugs, all inside published archive URLs", "location": "S052.txt:355, 9800; L2725, L6982, L6998, L7510, L7958"},
    {"severity": "INFO", "item": "two vendor tracking parameters (_gl, _ga) and one vendor tracking id (lid), vendor-published in the feed", "location": "S052.txt:2316, 1133, 13892"},
    {"severity": "INFO", "item": "(Q6) at entry line 117 cites QUALITY.md:19 entry-bar Q6, not a manifest assertion; claim independently verified true", "location": "corpus/knowledge/cisa-kev-catalog.md:117"},
    {"severity": "INFO", "item": "operator path /home/vgpnk present but pre-existing at base in 3222 files", "location": "lane-wide"}
  ],
  "coverage": {
    "scan_of_record_utc": "2026-10-26T06:46:25Z",
    "artifacts": 160,
    "bytes": 4429153,
    "missing": 0,
    "composition": "modified-tracked + untracked at base 3266c993",
    "blocking_classes": {"S1_credential_material": 0, "S2_session_auth_values": 0},
    "triage_counts": {"S3_cleartext_http_url": 4, "S3_email_address": 2, "S3_tracking_param": 2, "S3_private_ip_literal": 1},
    "scanner_exit": 0,
    "cross_check_grep_exit": 1
  },
  "key_results": {
    "capture_S052_sha256": "d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826",
    "capture_bytes": 1479694,
    "capture_lines": 27870,
    "capture_pure_json": true,
    "capture_toplevel_keys": 5,
    "capture_records": 1756,
    "manifest_sha256": "06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee",
    "f18_entry_sha256": "0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74",
    "f18_q6_independently_confirmed": true,
    "op_uri_references": 0,
    "emails": 2,
    "private_urls": 0,
    "pii_fields": 0,
    "capture_producer_headers": "User-Agent only (capture-source.py); no Cookie/Authorization",
    "instruments_clean": ["r35-defect-closure.sh", "credscan.py", "r35-fixtures/**"],
    "env_handling": "no ENV read or printed; no network code in any scanned instrument"
  },
  "attachments": {
    "credscan.py": {"path": ".ufo/waves/round-35/wave1/SentCred/credscan.py", "sha256": "07dbcba3fe8430ad1364ec2564a3df58d1537019dd94fb378f62fbc4a4cc0896"},
    "scan-hits.txt": {"path": ".ufo/waves/round-35/wave1/SentCred/scan-hits.txt", "sha256": "7e598c6e45d5aca6dcb2d4b22a592e2b7b1817523a44947591cee8d5748077c3"},
    "artifacts.sha256": {"path": ".ufo/waves/round-35/wave1/SentCred/artifacts.sha256", "sha256": "7578699b2e0af0a7c258def45b8bb892191d9e900c2f9157f7e30a11541ddf81", "lines": 160}
  }
}
```

### Liveness re-run (after this receipt landed)

```
$ python3 .ufo/waves/round-35/wave1/SentCred/credscan.py --root . --show-s3
files=162 bytes=4484434 excluded_self=4
s1=0 s2=0 s3=9 exit=0                                    # 2026-10-26T06:47:26Z, EXIT=0
```

Two further artifacts landed between the scan of record (160) and this re-run (162); the receipt
and its three attachments are now in the enumeration and excluded from their own scan by path
prefix (`.ufo/waves/round-35/wave1/SentCred`), so `excluded_self` counts them. Blocking classes
stayed at zero, as they did at every intermediate state.

The last run before this seat yielded (`2026-10-26T06:47:54Z`) reports
`files=164 bytes=4521982 s1=0 s2=0 s3=9 exit=0` — four artifacts landed after the scan of record,
still zero blocking hits. The tree is still moving; the re-run above is the authoritative check
after closure.

### Scratch

All work lived in `/fast/scratch/hyaku/kasegi-r35/SentCred/` (pattern files, the two scan
outputs, the digest list) and was copied into `.ufo/waves/round-35/wave1/SentCred/` before
removal; the directory is deleted before this seat yields, and `ls -d` on it afterwards is
expected to fail. Tooling: none installed or upgraded (python3, grep, xxd, cmp, sha256sum from the
base system); no package transaction attempted.
