# SentSecrets — round-38 credential / private-URL / vault-ref / mailbox sweep

Seat: `SentSecrets` (leaf sentinel, no subagent dispatch). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, claims freeze `9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b`. Lane HEAD
observed during the sweep: `700153593eb586c70a6499c8ca225ee4d673bc9b`, with 5 modified tracked files at the first check
(`PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`) and 22 porcelain entries at filing —
other seats' and the L1's landings, read-only to this seat, which wrote no lane path except this receipt. Those five paths are L1 landings in progress, not this seat's writes.
Nothing under `corpus/source-snapshots/round-38/` or `corpus/instruments/r38-closure.sh` existed when the sweep began;
both had landed by 18:40/18:46Z, so §4.1 audits the **landed bytes** as well as the wave-1 deliverables that carry
them (capture, manifest, instrument, knowledge entry, registry row, lesson and ledger blocks) and every other file in
the wave dir.

Answering model: `opencode-go/deepseek-v4.1-flash` (route from the spawn chain; the item does not depend on it).
**Tooling: nothing installed or upgraded** — no pacman (host-wide pause honoured), no `uv`/`npx` install, no binary
drop. **No network call was made by this seat**: the S055 capture was read as the wave-1 deliverable and its hash
compared to the manifest's own record, not re-fetched.

Scratch: `/fast/scratch/hyaku/kasegi-r38/SentSecrets/` (two scanners, positive/negative controls, mutation copies,
per-pass logs, tree snapshots). Removed at yield, after this receipt was copied into the wave dir.

---

## 0. Verdict

**0 credential values, 0 private-key blocks, 0 vault references, 0 session/signed-URL parameters, 0 loopback /
RFC1918 / `.internal` URLs, 0 tokens beyond public documentation, and 0 mailboxes beyond the four public OASIS TC
contacts the source itself publishes — in all 103 files of `.ufo/waves/round-38/wave1/` at the filing snapshot
(18:59:54Z), including the 22 landable-byte files (9,792 lines) and the hash-pinned S055 capture (5,146 lines).**

Redaction need: **none**. Nothing in this wave needs to be scrubbed before it lands, and nothing needs rotation. Three
categories produce non-zero counts and each is accounted for line by line in §3/§6: absolute **local paths** in
receipts (`/home/vgpnk/...`, 218 hits, no secret subtree), **digest-shaped hex** (hash records), and the words
*secret* / *credential* / *token* in prose — plus one lane fixture identity, `r38@local`, in the instrument's temp-repo
commits (§4). None of them is credential material.

The one thing a later run must keep green is the gate in §8; it is bound to the paths the L1 lands and returns `# expect 0`.

---

## 1. The rule as it applies to round 38

The frozen claims add: `corpus/knowledge/csaf-vex-product-status-and-justifications.md`, an `S055` row in
`corpus/SOURCES.md`, `corpus/source-snapshots/round-38/{S055.txt,manifest.json}`, `corpus/instruments/r38-closure.sh`,
`corpus/lessons/round-38.md`, the pending-marker resolutions section in `corpus/lessons/round-37.md`, the
`## Round-37 dispositions` table in `corpus/knowledge/considerthese-proposals-ledger.md`, a `Correction (round 38)` line
in `PROVINCE.md` / `corpus/README.md` / `SCORECARD.md`, the F21 row and `S055` row text in `corpus/README.md`, and the
`LOG.md` / `SHONEN.md` / `SKILL.md` updates. Every one of them lands in a public git history, so the rule is:

> Every round-38 addition carries no credential value, API key, private-key block, session token, cookie or signed-URL
> parameter, no loopback, private-network or internal-host URL, no vault-reference URI, and no mailbox that is not a
> public contact already published by the source. Where the source itself carries such material, the **location** is
> named and the **value** is never reproduced. The check is one command over the landed paths (§8) and it must print
> `0`; a non-zero count rejects the adding artifact.

The capture is the only artifact that could plausibly carry foreign PII, because it is a verbatim 5,146-line
transcription of a third-party page. §4 is that audit, and it is the answer to "does the entry's `Documentation only:`
claim hold for these bytes".

---

## 2. What was scanned, and when

Passes over `.ufo/waves/round-38/wave1/` while sibling seats were still landing: three spaced passes (8m33s and 9m44s
apart, the item's 3×5-minute window), three interim passes as the tree grew, and a filing pass after the receipt bytes
were final:

| # | UTC | files | bytes | value classes P01-P16,P18 / Q01-Q06,Q09 | P17 local paths | Q07 hex+ | Q08 word |
|---|---|---|---|---|---|---|---|
| 1 | 2026-10-26T18:36:42Z | 60 | 945,955 | **0 / 0** | 135 | 231 | 65 |
| — | 2026-10-26T18:39:13Z | 74 | 1,114,290 | **0 / 0** | 156 | 265 | 81 |
| — | 2026-10-26T18:42:06Z | 87 | 1,384,180 | **0 / 0** | 184 | 329 | 117 |
| 2 | 2026-10-26T18:45:15Z | 94 | 1,553,302 | **0 / 0** | 203 | 354 | 156 |
| — | 2026-10-26T18:49:07Z | 101 | 1,672,463 | **0 / 0** | 210 | 377 | 175 |
| 3 | 2026-10-26T18:54:59Z | 103 | 1,746,342 | **0 / 0** | 218 | 397 | 187 |
| filing | 2026-10-26T18:59:54Z | 103 | 1,752,053 | **0 / 0** | 218 | 397 | 194 |

Own-write disclosure: one control file (`q.txt`, 2 lines of synthetic `password=` / `passwd=` values, written by a
shell step whose `cd` left it in the wave dir instead of scratch) existed in this directory for 9 seconds around
18:59:45Z and is visible in that interim pass as `P11 = 2`. It was deleted before the filing pass; `ls q.txt` → absent,
and the filing snapshot above is the scanned tree. No other write by this seat touched the wave dir before its receipt.

Spacing 8m33s and 9m44s between the numbered passes. The tree grew by 43 files and 800,387 bytes across the window,
and every file added between passes was scanned in the next pass. Exact added set (`comm -13` over the pass-1 and
closing tree snapshots, `LC_ALL=C`, 43 names):

```
ConnC1C2.md ConnPatterns.md ConnSibling.md CritBoundary.md CritC1Export.md CritC1Kill.md
CritC2Ground.md CritC2Kill.md CritJudgedHead.md CritMotivation.md ExecQuarantine.md
ExecQuarantine.quarantine-slice ExecRefChecker.md ExecSchemaCross.md ExecSuiteBuild.md
ExecSuiteBuild.r38-closure.sh MutC2Entry.md MutC2Row.md MutG5G8.md MutJunkTwin.md RevClaimsFreeze.md
RevDARanges.md RevEntryF21.md RevNoHarm.md RevPendingResolutions.md RevSelftestBar.md
RevSourceRecheck.md RevSpotCheckReadiness.md RevSuiteDesign.md ScoutCaptureAvailability.md
ScoutF21Open.md ScoutR37Evidence.md ScoutStandingRefusals.md ScoutVexLeads.md
ScribeGateLesson.block.md ScribeGateLesson.md ScribeLedgerFill.block.md ScribeLedgerFill.md
ScribeShonen.block.md ScribeShonen.md SentScope.md SimplHygiene.md SimplReport.md
```

Three files were rewritten mid-flight and re-scanned on their new bytes: `ScribeEntryF21.entry.md` and
`ScribeEntryF21.md` (between pass 1 and pass 2) and `ExecSuiteBuild.r38-closure.sh`, which the instrument's seat revised
at least three times during the window (observed: 1,473 lines/61,159 B at 18:36 → 1,716 lines/74,707 B →
**1,767 lines / 77,726 B / sha256 09d46673…** at filing). Each revision was scanned in the pass that followed it; the filing-pass gate over the final
bytes is `0` (§4.1). The capture (`63c8ad52…`) and manifest (`95b3f46d…`) were byte-stable across all seven passes —
the tree snapshot at pass 1 and at filing carry the same two hashes:

```console
$ grep -hE 'ExecC2Capture\.(S055\.txt|manifest\.json)$' $S/tree1.sha256 $S/tree3.sha256 | sort -u
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  ExecC2Capture.S055.txt
95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f  ExecC2Capture.manifest.json
```

The **zero-tolerance subset** is the set of files whose bytes the L1 lands verbatim, exactly as the round's
deliverable discipline defines them (`*.block.md`, `*.row.md`, `*.entry.md`, `*.sh`, `*.py`, the capture and the
manifest, plus the `.collisions` / `.reg-ids` / `.staged-ids` data files):

```console
$ set -- *.block.md *.row.md *.entry.md *.sh *.py *.collisions *.reg-ids *.staged-ids \
         ExecC2Capture.manifest.json ExecC2Capture.S055.txt
$ echo "files=$# lines=$(cat "$@" | wc -l)"
files=22 lines=9792      # 9,741 at pass 3; the instrument grew to its filing revision (§2)
$ grep -rInE -- "$PAT_BROAD" "$@" | wc -l
0
$ grep -rInE -- "$PAT_GATE" "$@" | wc -l
0
```

---

## 3. Results by class

`PAT_BROAD` is the P01-P18 value set reproduced in §7 (one ERE, applied line-wise); the Q01-Q09 rows are separate
probes over the same bytes. `PAT_GATE` is the compact landed gate of §8. Counts are `grep -c` line hits over the
filing snapshot (18:59:54Z, 103 files) — the numbers in the table are that snapshot's.

| class | what it detects | hits |
|---|---|---|
| P01 | vault / 1Password reference URIs | **0** |
| P02 | PEM private-key headers (`BEGIN … PRIVATE KEY`) | **0** |
| P03 | AWS access-key ids (`AKIA`/`ASIA` + 16) | **0** |
| P04 | GitHub tokens (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`, `github_pat_`) | **0** |
| P05 | Slack tokens (`xox[baprs]-`) | **0** |
| P06 | `sk-` style API keys (Stripe/OpenAI/…) | **0** |
| P07 | Google API keys (`AIza` + 35) | **0** |
| P08 | JWTs (`eyJ….eyJ…`) | **0** |
| P09 | GitLab PAT / npm / PyPI tokens | **0** |
| P10 | generic secret assignments (`api_key=`, `client_secret:`, …) | **0** |
| P11 | password assignments | **0** |
| P12 | `Authorization: Bearer …` headers | **0** |
| P13 | signed / credentialed URL parameters (`X-Amz-Signature`, `?token=`, `?session=`, …) | **0** |
| P14 | URL userinfo credentials (`scheme://user:pass@`) | **0** |
| P15 | loopback / RFC1918 hosts in URLs | **0** |
| P16 | `.internal` / `.local` / `.lan` / `.corp` hostnames | **0** |
| P17 | absolute local paths (`file:///`, `/home/…`, `/Users/…`) | 218 — informational, §6 O1 |
| P18 | env dumps of secret-bearing variables (`AWS_SECRET_ACCESS_KEY=`, `GITHUB_TOKEN=`, …) | **0** |
| Q01 | SSH key material (`ssh-rsa AAAA…`, `BEGIN OPENSSH`) | **0** |
| Q02 | session / cookie headers and ids (`Set-Cookie:`, `JSESSIONID=`, `PHPSESSID=`) | **0** |
| Q03 | secret-manager CLI invocations (`op read`, `pass show`, `security find-generic-password`, `bw get`) | **0** |
| Q04 | credential file names (`.netrc`, `.git-credentials`, `id_rsa`, `.aws/credentials`, `.npmrc`) | **0** |
| Q05 | base64 of `password`/`secret`/`token` | **0** |
| Q06 | `Basic <base64>` blobs | **0** |
| Q07 | ≥64-char alphanumeric blobs (entropy proxy) | 397 — all digests/SHAs, §3.1 |
| Q08 | the words *secret* / *credential* / *token* | 187 — all prose or identifiers, §3.1 |
| Q09 | private git remotes with inline credentials | **0** |

### 3.1 The three non-zero classes, resolved

**Q07 = 397 lines, 0 surprises.** Excluding the 64-hex digests/SHAs that every receipt and manifest records, the
*unique* residual set is four strings, all benign:

```console
$ grep -rhoIE '\b[A-Za-z0-9_-]{64,}\b' . | grep -vE '^[0-9a-f]{64}$' | sort -u
0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF   # synthetic test hex in the declared-blocks fixture (ExecDeclaredBlocks.gen.sh + .md)
37df33cb…d0fcb3                                                    # spec Example 12 crypto hash (capture L876)
9ea4c820…fa697c                                                    # spec Example 12 crypto hash (capture L878)
when-issue-vulnerability-exploitability-exchange-vex-information   # public FIRST VEX page slug
```

The two long values are the CSAF spec's own example digests (`Examples 12`, capture L876 and L878) inside section
`3.1.3.3.2 Full Product Name Type - Product Identification Helper - Hashes` (heading L820), under the `value` property
description at L872 — a standard's worked example, not anyone's secret.

**Q08 = 194 lines at filing, all the word in prose.** Word-sense breakdown: `token` in *"reference token"* (a CSAF
`product_id_t` type description), *"URL token"* / *"the row's single `https://` token"* (the C2 binding rule text),
*"whitespace-separated tokens"* (quote-matching rules), *"word tokens"* (the pending-marker instrument), and
`WORD_TOKENS = re.compile(...)` / `added_word_tokens=` (Python identifiers). Assignment-shaped occurrences — the only
shape that would be a value — are 3, and all three are those Python identifiers:

```console
$ grep -rnIiE '(secret|credential|token)s?[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/+_.-]{8,}' .
./ExecRefChecker.py:170:WORD_TOKENS = re.compile(r'\b(?:TBD|TODO)\b')
./ExecRefChecker.py:506:        added_fixed_tokens=fixed_hits,
./ExecRefChecker.py:507:        added_word_tokens=word_hits,
```

**P17 = 218 local paths.** Prefix census (all within the two permitted trees, no sensitive home subtree):

```console
$ grep -rhoIE '/home/vgpnk/[^ "'"'"'`),;|]*' . | awk -F/ '{print "/"$3"/"$4"/"$5"/"$6}' | sort | uniq -c | sort -rn
    149 /vgpnk/Projects/shokunin/kasegi-shokunin
     21 /vgpnk/Projects/shokunin/scripts
     19 /vgpnk/Projects/shokunin/
     13 /vgpnk/Projects/shokunin/.ufo
      9 /vgpnk/Projects/shokuknow/merge
      6 /vgpnk/…/kasegi-shokunin/corpus
      4 /vgpnk/Projects/shokuknow/.ufo
      2 /vgpnk/Projects/shokunin/kasegi-shokunin}
      1 /vgpnk/Projects/{shokunin/
      1 /vgpnk/Projects/shokunin/kasegi-shokunin:
$ grep -rhoIE '/(home|root)/[A-Za-z0-9._-]+/(\.ssh|\.aws|\.gnupg|\.config|\.password-store|\.netrc)[^[:space:]`"'"'"']*' . | sort -u
(no output)
```

Zero paths into `.ssh`, `.aws`, `.gnupg`, `.config`, `.password-store`, `.netrc`; zero `/etc`, `/root`, `/proc` paths.
The 9 `shokuknow/merge` and 4 `shokuknow/.ufo` references are read-only *provenance citations* in scribe receipts
(what was grepped and where), not content that lands.

### 3.2 URL census — every host referenced anywhere in the wave

All hosts are public documentation, standards bodies, vendor press/PSIRT pages or RFC 2606 reserved domains. No
single-line hit is a private-network URL (P15/P16 = 0). The non-obvious ones and their nature:

- `static.cloudflareinsights.com`, `a.nel.cloudflare.com` — beacons captured inside the OASIS HTML while the manifest
  recorded the fetch; public, unauthenticated.
- `psirt.domain.tld`, `domain.tld`, `keys.example.net`, `example.invalid`, `cert.example`, `psirt.example.com`,
  `lister.example`, `aggregator.example`, `example.com` — RFC 2606/6761 reserved example domains quoted from the spec.
- `csaf.io`, `securitytxt.org`, `certcc.github.io`, `githubengineering.com`, `swinslow.net`, `cybozu.co.jp`,
  `ipa.go.jp`, `bsi.bund.de`, `std.samr.gov.cn`, `openstd.samr.gov.cn`, `ntia.gov`, `us-cert.gov`, `icasi.org`,
  `openssl.org`, `iana.org` — public standards/vendor/citation pages.
- `api.github.com`, `raw.githubusercontent.com`, `spdx.github.io` — public raw/api endpoints cited by the mapping
  examples in the spec text, no token-bearing access.

---

## 4. The planned capture, audited on the bytes that will land

The capture is not committed at sweep time, so the audit is of the wave-1 deliverable that carries the exact bytes,
and that hash is the one the manifest itself declares:

```console
$ wc -lc ExecC2Capture.S055.txt ExecC2Capture.manifest.json
  5146 272441 ExecC2Capture.S055.txt
    57   3841 ExecC2Capture.manifest.json
$ sha256sum ExecC2Capture.S055.txt ExecC2Capture.manifest.json
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  ExecC2Capture.S055.txt
95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f  ExecC2Capture.manifest.json
$ grep -m1 '"sha256"' ExecC2Capture.manifest.json | sed 's/^ *//'
"sha256": "63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42",
```

Capture-bytes hash == manifest-declared hash, so the audited bytes are the bound bytes.

Shape probes over the 5,146 lines — the counts a documentation page should produce:

```console
$ bash $S/scan.sh <capture dir>   # P01-P18 then Q01-Q09 over the two capture files
op:// 0 | PEM 0 | AKIA/ASIA 0 | gh*_ 0 | xox* 0 | sk- 0 | AIza 0 | JWT 0 | glpat/npm/pypi 0
api_key=/client_secret= 0 | password= 0 | Authorization: Bearer 0 | signed-URL params 0
://user:pass@ 0 | loopback/RFC1918 0 | .internal/.local/.lan 0 | env-dump 0
ssh key material 0 | Set-Cookie/JSESSIONID 0 | op read/pass show 0 | base64(password) 0 | Basic b64 0
$ for w in password passwd credential login session cookie bearer authorization secret 'private key'; do
    printf '%-14s %s\n' "$w" "$(grep -oiE "$w" ExecC2Capture.S055.txt | wc -l)"; done
password       0
passwd         0
credential     0
login          0
session        0
cookie         0
bearer         0
authorization  0
secret         0
private key    0
token          5      # "reference token" — product_id_t / product_group_id_t type definitions
```

The one security-adjacent construct in the page is normative prose, not protected content: `7.1.5 Requirement 5:
TLP:AMBER and TLP:RED` (capture L3802-L3803) *states the marking rule* — "CSAF documents labeled TLP:AMBER or TLP:RED
MUST be access protected" — and the capture is a TLP:WHITE OASIS Standard page. No marked-up material was transcribed.

**Mailbox census: 9 token shapes, 0 private.** Eight live in the capture (table below). The only `@`-token in the
22 landable files is `r38@local` (10 occurrences, all `git -c user.email=r38@local` inside the instrument's
temp-repo fixtures at `ExecSuiteBuild.r38-closure.sh:1286,1290,1293,1306,1313,1331,1338,1346,1350,1403`) — a
lane-internal fixture identity on the non-routable `.local` TLD, carrying no personal data:

```console
$ grep -hoE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+' *.block.md *.row.md *.entry.md *.sh | sort | uniq -c
     10 r38@local
```

| token | classification | basis |
|---|---|---|
| `osantos@cisco.com` | public contact | OASIS CSAF TC **Chair**, named on the standard's title page (capture L20) |
| `lrock@redhat.com` | public contact | TC **Editor** (L22) |
| `stefan@hagen.link` | public contact | TC **Editor** (L23) |
| `thomas.schmidt@bsi.bund.de` | public contact | TC **Editor** (L24) |
| `contact_us@example.com` | not a mailbox | `example.com` is RFC 2606 reserved; spec Example 33 (L1356) |
| `contact_us@lister.example` | not a mailbox | RFC 2606 reserved `.example` TLD; Example CSAF lister (L4052) |
| `contact_us@aggregator.example` | not a mailbox | RFC 2606 reserved `.example` TLD; Example CSAF aggregator (L4095) |
| `jboss-logging@3.4.1.Final` | false positive | a Maven coordinate `group@version`, not an address (L971) |
| `r38@local` (landable instrument) | not a mailbox | temp-repo `user.email` in a `git` fixture; `.local` is non-routable, no personal data |

So the entry's `Documentation only:` claim is true of these bytes, and ordinary quoting practice needs no carve-out:
line numbers may be cited freely; no line needs a value withheld.

### 4.1 The bytes that actually landed

While this sweep ran, the L1 landed the capture, the manifest and the instrument into the lane. Re-scanned at filing
(`grep -rInE -f $S/patb.txt`, both pattern sets):

```console
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/r38-closure.sh \
    corpus/source-snapshots/round-38/S055.txt corpus/source-snapshots/round-38/manifest.json
85d33ea9d386926e88f9818bbdae5c49ef9cf951363ea09de641cb22a26979a6  corpus/instruments/r38-closure.sh
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  corpus/source-snapshots/round-38/S055.txt
95b3f46d9c502573f299ed565325a0db27009c2a5eb50205c1ca27b3556f9a9f  corpus/source-snapshots/round-38/manifest.json
$ grep -rInE --exclude=SentSecrets.md "$PAT" corpus/source-snapshots/round-38 corpus/instruments/r38-closure.sh | wc -l
0
$ grep -rInE -f $S/patb.txt corpus/source-snapshots/round-38 corpus/instruments/r38-closure.sh | wc -l
0
```

The landed capture and manifest are **byte-identical** to the audited wave-1 deliverables (`63c8ad52…`, `95b3f46d…`),
so §4's capture verdict carries to the committed bytes without re-derivation. The landed instrument is the first
revision (1,473 lines / 61,159 B / `85d33ea9…`); the wave-1 deliverable at filing is the seat's fourth (1,767 lines /
77,726 B / `09d46673…`). Both are credential-clean — the gate over the landed copy is `0` and over the wave-1 revision
`0`. If a later revision is the one that lands, re-run the §8 gate on it; the delta is a revision question, not a
credential one (O5).

---

## 5. Controls — the scan is not vacuous

**5.1 Synthetic positive / negative pair.** One line per class, then the same shapes with every value replaced by a
placeholder:

```console
$ bash $S/scan.sh $S/pos | grep '^-- P' | awk -F' : ' '{gsub(/ hit\(s\)/,"",$2); s+=$2; n++} END{printf "positive classes fired: %d hits: %d\n", n, s}'
positive classes fired: 18 hits: 19        # P02 fires twice (RSA + OPENSSH headers); 18/18 classes fire
$ bash $S/scan.sh $S/neg | grep '^-- P' | awk -F' : ' '{gsub(/ hit\(s\)/,"",$2)} $2>0{c++} END{printf "classes still firing: %d\n", c+0}'
classes still firing: 0                    # every class returns to 0 once the value is a placeholder
```

**5.2 Real-artifact injection.** Append one synthetic value to scratch copies of three landable artifacts:

```console
$ cp $W/ExecC2Capture.S055.txt mut2/cap.txt; cp $W/ScribeEntryF21.entry.md mut2/entry.md
$ cp $W/ScribeRowS055.row.md mut2/row.md
$ grep -cE -- "$PAT" mut2/cap.txt mut2/entry.md mut2/row.md
mut2/cap.txt:0
mut2/entry.md:0
mut2/row.md:0
$ echo 'api_key=CONTROLAAAAAAAA0000' >> mut2/cap.txt; echo 'see op://controlvault/controlitem' >> mut2/entry.md
$ echo 'mirror at http://127.0.0.1:8080/admin?session=CONTROL' >> mut2/row.md
$ grep -cE -- "$PAT" mut2/cap.txt mut2/entry.md mut2/row.md
mut2/cap.txt:1
mut2/entry.md:1
mut2/row.md:1
```

3/3 pristine artifacts green, 3/3 injected copies red — a hit on the landed artifact would have been visible.

**5.3 The gate does not red on its own documentation.** The §8 pattern is written so that its own source text cannot
match it (`op:[/][/]` instead of the literal scheme; `https?://` never satisfies its own `http://` alternative):

```console
$ grep -cE "$PAT_GATE" $S/deliverable-block.txt   -> 0     # the gate pasted anywhere stays green
$ cp deliverable-block.txt $S/mut-block.txt && echo 'api_key=CONTROL000000000000' >> $S/mut-block.txt
$ grep -cE "$PAT_GATE" $S/mut-block.txt           -> 1
```

---

## 6. Findings register

| id | severity | finding | impact | smallest remediation |
|---|---|---|---|---|
| N1 | none | 0 credential values in 103 wave files at the filing snapshot and in the 22 landable-byte files (9,792 lines) under an 18-class value set (§3). | none reachable | none |
| N2 | none | 0 vault refs, 0 session/signed-URL parameters, 0 loopback/RFC1918/`.internal` URLs, 0 cookie/session ids (§3, §3.2). | none | none |
| N3 | none | The S055 capture (5,146 lines, sha `63c8ad52…`) carries no credential, no form/login, no cookie, no marked-TLP content, and only 4 public TC contacts + 3 RFC 2606 example addresses + 1 Maven coordinate (§4). The entry's `Documentation only:` claim is true of these bytes. | none | cite §4 in the entry's Q6 line, or weaken the sentence |
| O1 | informational | 218 absolute local-path hits in wave receipts (`/home/vgpnk/Projects/{shokunin,kasegi-shokunin,shokuknow}`). These are provenance citations in receipts, which never land; no `.ssh`/`.aws`/`.gnupg`/`.config`/`.password-store`/`.netrc` path and no `/etc`/`/root`/`/proc` path appears (§3.1). | host layout disclosed in an uncommitted receipt; none in landed content | none required; if the L1 wants stricter hygiene, keep the receipts out of the export path (round-37's head-red transcript already diffs with `':!.ufo'`, `ExecR37HeadRed.transcript.txt:732`) |
| O2 | informational | One receipt (`ExecQuiescence.md:126-127`) pastes `df -h` output and therefore names the host block devices `/dev/nvme1n1p1` (128G, `/tmp`) and `/dev/nvme1n1p2` (804G, `/fast`) with free-space figures. | host topology/capacity in an uncommitted receipt; not a credential | none; if desired, quote only the mount point and the `24%` / `3%` utilisation |
| O3 | informational | The landable instrument carries a default `LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin` with a `--lane` override — a path default, not a secret. | portability only | none |
| O4 | informational | `/dev/null`, `/dev/fd/63` hits are shell redirection and process-substitution syntax inside quoted command transcripts, not device access. | none | none |
| O5 | informational | The landed `corpus/instruments/r38-closure.sh` is the first revision (`85d33ea9…`, 61,159 B) while the wave-1 deliverable at filing is the fourth (`09d46673…`, 77,726 B); the seat revised it four times during the sweep. Both are credential-clean (§4.1). | the L1 may land bytes that differ from the seat's final revision | land the intended revision at J; no redaction implied either way |

**Redaction need across the wave: none.** No value was reproduced in this receipt; where a token had to be identified
(§4's mailbox table) it is a public contact a reader can already see on the OASIS page.

---

## 7. The pattern set (durable copy — scratch is deleted at yield)

`PAT_BROAD`, one ERE for `grep -E` (18 value classes; class labels in §3):

```
op://[A-Za-z0-9]|-----BEGIN [A-Z ]*PRIVATE KEY-----|(AKIA|ASIA)[0-9A-Z]{16}|(ghp_|gho_|ghu_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{16,}|xox[baprs]-[A-Za-z0-9-]{10,}|sk-(live|test|proj)?[-_]?[A-Za-z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}|(glpat-[A-Za-z0-9_-]{20,}|npm_[A-Za-z0-9]{36}|pypi-[A-Za-z0-9_-]{30,})|(api[_-]?key|apikey|access[_-]?token|auth[_-]?token|client[_-]?secret|secret[_-]?key|private[_-]?token)[[:space:]]*[:=][[:space:]]*["']?[A-Za-z0-9/+_-]{12,}|(password|passwd|pwd)[[:space:]]*[:=][[:space:]]*["']?[A-Za-z0-9][^ "']{5,}|[Aa]uthorization:[[:space:]]*[Bb]earer[[:space:]]+[A-Za-z0-9._~+/-]{10,}|(X-Amz-(Signature|Credential|Security-Token)|[?&](token|access_token|api_key|apikey|key|sig|signature|session|sessionid|sso|auth|code)=[A-Za-z0-9%._~-]{6,})|://[^/@[:space:]]+:[^/@[:space:]]+@|(https?|ssh|ftp)://(10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|192\.168\.[0-9]{1,3}\.[0-9]{1,3}|172\.(1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3}|127\.0\.0\.1|localhost)(:[0-9]+)?|(https?|ssh)://[A-Za-z0-9.-]+\.(internal|local|lan|corp|intranet)([:/]|$)|(^|[^A-Za-z])(AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|GITHUB_TOKEN|GH_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|ELEVENLABS_API_KEY|OP_SERVICE_ACCOUNT_TOKEN|SSH_AUTH_SOCK)[=:][[:space:]]*[^[:space:]]{4,}
```

Sanity of this exact line as a file pattern: `grep -cE -f patb.txt` scores the positive control 18 lines and the
all-redacted control 0, so the copy above is faithful to the set that produced §3. The Q01-Q09 shapes (SSH blobs,
cookie/session ids, secret-manager CLIs, encoded credentials) are separate probes over the same bytes, not part of
this alternation.

Two calibration notes that cost a false result if dropped, both measured this round:

- **`ghp_` (and friends) must require 16+ `[A-Za-z0-9_]`** and a redaction fixture must therefore be written
  `ghp_<REDACTED>`; `ghp__________________` still matches, because `_` is inside the token alphabet. The negative
  control in §5.1 failed this way on its first wording and was fixed.
- **Password-assignment patterns must require an alphanumeric first value char** (`["']?[A-Za-z0-9]…`), otherwise a
  redaction like `password=<REDACTED>` re-trips the detector and the "review this line" class never returns to zero.
  With that anchor, the all-redacted fixture is 0/18 while the value-bearing fixture is 19 hits.

---

## 8. The gate to land (receipt-only item)

Landed text, nothing else. 8 lines, 954 bytes, `sha256 5d579b40a78d6effc91c235701cf49e87e85b111330d283d27771ab13eb6f51b`.

## DELIVERABLE

```
# Round-38 credential gate (QUALITY Q6): expect 0 on the judged head J.
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
PAT="(AKIA|ASIA)[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{16,}|glpat-[A-Za-z0-9_-]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----|(op|sops):[/][/][A-Za-z0-9]|api[_-]?key[[:space:]]*[:=]|client[_-]?secret[[:space:]]*[:=]|(password|passwd)[[:space:]]*[:=][[:space:]]*[\"']?[A-Za-z0-9]|[?&](X-Amz-Signature|token|sessionid|sig)=[A-Za-z0-9]|https?://(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[01])\.|127\.0\.0\.1|localhost)"
grep -rInE --exclude=SentSecrets.md "$PAT" \
  corpus/source-snapshots/round-38 corpus/knowledge/csaf-vex-product-status-and-justifications.md \
  corpus/instruments/r38-closure.sh corpus/lessons/round-38.md \
  corpus/knowledge/considerthese-proposals-ledger.md corpus/QUALITY.md \
  SCORECARD.md SHONEN.md PROVINCE.md README.md LOG.md SKILL.md | wc -l    # expect 0
```

Dry-run today against the wave-1 stand-in bytes for those same paths (the 22 landable files) and against the whole
wave tree: `0` and `0`; `bash -n` parses it, the expanded `PAT` is 447 characters, it still catches the quoted forms
`password="CONTROL123"` / `passwd='CONTROL123'` (2/2), and it does not match its own source text (0). This receipt
itself trips it on **7 lines** as filed — the P10 row of §3, the §4 probe summary line, the two §5.2 mutation-result
lines, the §5.3 injection command, the §7 calibration note that prints the `ghp_____` counter-example, and this
sentence's own quoted-form example. The number moves by one whenever the file names another shape, so reproduce it
rather than trust it: `grep -cE "$PAT" .ufo/waves/round-38/wave1/SentSecrets.md`. `--exclude=SentSecrets.md` is therefore part of the gate,
and it is inert for the landed paths, which never include `.ufo/`.

---

## 9. Limits

- This is a scan of **bytes**, not a history audit: it says nothing about what earlier rounds committed, and a later
  re-fetch of S055 is a new pin against the same review.
- The gate is a detector of *shapes*; it cannot prove the absence of a secret written in a shape nobody encodes (an
  opaque prose sentence, a value split across lines). §4's prose counts and §3's structural absence are the evidence
  for the capture, which is the only artifact with foreign origin.
- Wave receipts are excluded by construction from the "lands verbatim" claim: they carry the synthetic control values
  of §5 and the pattern text of §7, which is exactly why they are not content.
