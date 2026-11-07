# ScoutSources — independent re-open of C2 sources + leads (round 86, w1)

Seat: `ScoutSources` (scout, leaf, no delegation, no background jobs).
Fetched 2026-11-07T01:05–01:30Z. Plain `GET` only (`curl -sS -L --max-time 45`, browser UA).
**No login, no target probing, no submission.** Scratch `/fast/scratch/hyaku/kasegi-r86/ScoutSources`
(deleted on exit). Receipts: `.ufo/waves/round-86/w1/ScoutSources-receipts/`.
No file named `S<digits>.txt` was written into `w1/` (checked against the 15 repair-map key
basenames `S016,S020,S021,S023,S025,S071,S073,S075,S076,S078,S089,S090,S103,S105,S106`).

---

## 0. Headline

1. **All 9 manifest quotes for S122/S123 and all 12 reused round-85 quotes (S119/S120/S121)
   occur live**, each exactly once, at the declared anchor line. S120, S121, S123 are
   **byte-identical to their frozen snapshots** after `capture-source.py` normalization
   (sha256 `65d6b230…`, `9e346a4e…`, `22a7d5be…` — equal to the manifest values).
2. **S122 is NOT byte-reproducible**, for the same reason round-85 found for S119: the HackerOne
   JSON carries wall-clock-relative fields that drift (`allow_singular_disclosure_after`), plus
   two presigned S3 avatar URLs whose AWS STS query strings are freshly signed per request.
   A fresh re-capture today yields sha256 `d465ca87…`, not the manifest's `ceb01841…`.
   **All five quotes survive; the digest does not.**
3. **Lead (a) RESOLVED — the IBB split policy is official and quotable.** The Internet Bug
   Bounty's own program page states the award split explicitly: *"HackerOne will add all
   bounties for each eligible vulnerability, providing 80% to the finder and 20% to the
   open-source project, funding essential remediation efforts."* (archived 2024-08-13 and
   2024-10-22, `hackerone.com/internet-bug-bounty`; the live domain now redirects to
   HackerOne's Community Edition page). The policy first appears in archives from **2024-07-27**;
   the 2023-04-27 and 2024-01-25 captures of the same page do **not** contain it, so the
   split policy is **not** contemporaneous with the May-2023 disclosure of CVE-2023-28319.
   **It does not change any C2 pricing field** (see §4).
4. **Lead (b) RESOLVED — a curl-official page states the payer mechanism, and it is the
   strongest available evidence for the payer side.** curl's own `docs/BUG-BOUNTY.md`, as it
   stood on the disclosure date (commit `435acbd379`, 2022-05-19, the version in force on
   2023-05-17): *"The actual monetary reward amount is decided and paid by the Internet Bug
   Bounty.."* and *"once the vulnerability has been published by curl, the researcher can
   request their bounty from the Internet Bug Bounty (https://hackerone.com/ibb)."* The same
   file states the 2022-era Medium rate: *"In 2022, typical \"Medium\" rated vulnerabilities
   have been rewarded 2,400 USD each."* — consistent with `Bug bounty: 2400 USD`.
   **This corroborates `payer: internet-bug-bounty` and `reward-at-disclosure: 2400 USD`; it
   changes no field.**
5. **Lead (c) RESOLVED — CVE-2023-28319 is still absent from the live CISA KEV catalog**
   (`catalogVersion 2026.11.06`, `count 1769`, 0 occurrences) — same conclusion as round 85,
   now re-confirmed on a newer catalog.
6. **DEFECT (new, routed): the working tree's `S122.txt` and `manifest.json` no longer match
   the digests frozen in `claims.json`, and the candidate C2 package's `evidence/S122.txt`
   still carries the *un*redacted bytes.** C2's P2 and P3, and the E2 limb, are currently
   **FAIL** in the tree as it stands. See §5. This is not caused by this seat.

---

## 1. Live re-open of the three named sources

Method: `curl -sS -L --max-time 45 -A '<browser UA>' <url>`; raw bodies kept as receipts; quotes
matched verbatim in the raw body, and for HTML additionally after the `capture-source.py`
tag-strip + `html.unescape` + whitespace-collapse pipeline.

| id | URL | status | final URL | live raw bytes | manifest `bytes` | match |
|---|---|---|---|---|---|---|
| S122 | `https://hackerone.com/reports/1997312.json` | **200** | same (no redirect) | 9167 | 9131 | no (see §2) |
| S123 | `https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/` | **200** | same | 75270 | 75270 | yes |
| S120 (reused) | `https://curl.se/docs/CVE-2023-28319.html` | **200** | same | 9732 | 9732 | yes |

Additional live opens made for the leads: S121 `https://curl.se/dev/vuln-disclosure.html` **200**
(26500 raw → normalized 19670), S119 `https://hackerone.com/reports/1913733.json` **200** (5135),
live CISA KEV feed **200** (1832349 bytes).

### 1.1 Every round-86 manifest quote (S122, S123) present live

| id | quote id | anchor | present live | occurrence count | on declared anchor line |
|---|---|---|---|---|---|
| S122 | Q01-team-handle `"handle":"ibb"` | 1 | yes | 1 | yes |
| S122 | Q02-has-bounty-flag `"has_bounty?":true` | 1 | yes | 1 | yes |
| S122 | Q03-severity-rating `"severity_rating":"medium"` | 1 | yes | 1 | yes |
| S122 | Q04-cve-id `"cve_ids":["CVE-2023-28319"]` | 1 | yes | 1 | yes |
| S122 | Q05-original-report `The original submission can be found here: https://hackerone.com/reports/1913733` | 1 | yes | 1 | yes |
| S123 | Q01-end-date `It officially stops on January 31, 2026.` | 13 | yes | 1 | yes |
| S123 | Q02-payer `the awesome Internet Bug Bounty project, which has paid the bounties for us for many years` | 16 | yes | 1 | yes |
| S123 | Q03-totals `87 confirmed vulnerabilities and over 100,000 USD paid as rewards to researchers` | 15 | yes | 1 | yes |
| S123 | Q04-no-rewards `We no longer offer any monetary rewards for security reports` | 27 | yes | 1 | yes |

**S123 live-normalized sha256 `22a7d5bed4d4081db7e94e4c788a5aaf12ed8dc8f7607536ef4ad36828de4ab5`
— byte-identical to the frozen snapshot.** S120 live-normalized sha256
`65d6b230ad58e86517b1b0faddd800d6bcb111ed05e21e22752246f4b0913690` — byte-identical.

### 1.2 The two S120 lines named in the seat spec

| probe | live line | in frozen S120 |
|---|---|---|
| `Bug bounty: 2400 USD` | **81** | yes (anchor 81) |
| `Original report: https://hackerone.com/reports/1913733` | **83** | yes (anchor 83) |

### 1.3 Reused round-85 sources re-verified (all 12 quotes, all anchors)

S119 Q01–Q04 (anchor 1, team handle `curl`, `has_bounty?`:false, severity medium, CVE id),
S120 Q01–Q05 (anchors 79, 80, 81, 83, 85), S121 Q01–Q03 (anchors 43, 95, 103) —
**all present live, occurrence count 1, each on its declared anchor line.**
`python3 -B corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-86/manifest.json`
exits **0** in the current tree.

### 1.4 Live S122 field-level diff vs the frozen snapshot

Only **3** JSON leaves differ; every manifest-quoted value is byte-identical:

| field | frozen | live today |
|---|---|---|
| `allow_singular_disclosure_after` | `-106296111.6415311` | `-106296601.79957855` (wall-clock drift) |
| `team/profile_picture_urls/small` | presigned S3 URL | re-signed (new `X-Amz-Credential`/`X-Amz-Security-Token`) |
| `team/profile_picture_urls/medium` | presigned S3 URL | re-signed |

Unchanged and confirmed live: `team.handle="ibb"`, `team.offers_bounties=true`,
`team.default_currency="usd"`, `team.submission_state="paused"`,
`team.profile.about="The Internet Bug Bounty rewards security research into vulnerabilities
impacting Open Source Software Projects."`, `has_bounty?=true`, `severity_rating="medium"`,
`cve_ids=["CVE-2023-28319"]`, `state="Closed"`, `substate="resolved"`, `title="CVE-2023-28319:
UAF in SSH sha256 fingerprint check"`, and the `vulnerability_information` line carrying
`The original submission can be found here: https://hackerone.com/reports/1913733`.
Note `original_report_id` and `original_report_url` are `null` in **both** live and frozen —
the original-report link lives only inside `vulnerability_information`, which is exactly where
the frozen counter's `derive()` looks for it.

---

## 2. Reproducibility caveat (carried forward from round 85, now on S122)

Re-capturing S122 today and re-running the `capture-source.py` collapse yields
sha256 `d465ca8732685d302f6dc642b8a8e6e7e09f979067ca2aa2c4c12ad633cfc16d` (9168 bytes),
not the manifest's `ceb01841a5144d72fb744f733b99a3fac792bf4197038fe9ec686ef57b418ec1`
(9131 bytes). Root cause is the drifting `allow_singular_disclosure_after` value plus the
per-request presigned-URL signatures — **not** a content change. All five quotes verify.
This is the same class as round 85's S119 finding; the `source-recheck.py` instrument is
byte-local, so it cannot observe it.

---

## 3. Leads

### Lead (a) — the official IBB split policy (RESOLVED)

| field | value |
|---|---|
| URL | `https://www.hackerone.com/internet-bug-bounty` (via `https://arquivo.pt/wayback/20240813220502id_/…`) |
| HTTP status | **200** (archived replay; the live URL now 301s to `https://www.hackerone.com/company/open-source-community`, also 200) |
| Located quote (≤25 words) | *"HackerOne will add all bounties for each eligible vulnerability, providing 80% to the finder and 20% to the open-source project"* |
| Would it change a C2 pricing field? | **No.** |

Supporting lines from the same page: *"The IBB program operates in a pooled defense model,
where every participating program's bounty allocation is pooled to create the public bounty
table for the IBB."* and *"Contribute 10% (suggested) of your normal bounty budget, or any
amount that fits your program model, through your individual IBB Bounty Table."*

**Applicability caveat (important):** the 80/20 sentence is **absent** from the archived
`internetbugbounty.org` / `hackerone.com/internet-bug-bounty` captures of **2023-08-02,
2023-11-19, 2024-01-25** and **present** from **2024-07-27** onward. CVE-2023-28319 was
disclosed **2023-05-17**, i.e. *before* the split policy was published in that form. So the
80/20 split **must not** be asserted as the rule that applied to this 2023 award. The
page is a useful statement of the IBB's *structure*, not of the rule in force at disclosure.

Why it still matters: it explains the mechanism behind the round-85 reconciliation — the
`ibb` team is the **payer** of record (HackerOne hosts the program; IBB's pooled table sets
the amounts; curl's own doc says the amount is *"decided and paid by the Internet Bug
Bounty"*), while report **1913733** on team `curl` is the **original submission** and
report **1997312** on team `ibb` is the **bounty-bearing record** (`has_bounty?: true`).
That is the exact C2 subject distinction, and it is now attested from three independent
directions: S122 (HackerOne's own JSON), S123 (the maintainer's post), and curl's
contemporaneous `BUG-BOUNTY.md`.

### Lead (b) — a curl-official page on who pays, contemporaneous with the disclosure (RESOLVED)

| field | value |
|---|---|
| URL | `https://raw.githubusercontent.com/curl/curl/435acbd379730eab3beb5dbb6c5027001ece6e1d/docs/BUG-BOUNTY.md` (the commit in force on 2023-05-17; also live as `https://curl.se/docs/bugbounty.html` in the 2022-10-09 and 2024-05-14 arquivo.pt captures) |
| HTTP status | **200** (raw.githubusercontent 200; `curl.se/docs/bugbounty.html` now **301** → `https://curl.se/dev/vuln-disclosure.html`, **200**) |
| Located quote (≤25 words) | *"The actual monetary reward amount is decided and paid by the Internet Bug Bounty."* |
| Would it change a C2 pricing field? | **No — but it corroborates two of them.** |

Second located quote: *"once the vulnerability has been published by curl, the researcher can
request their bounty from the Internet Bug Bounty (https://hackerone.com/ibb)."* — the
`hackerone.com/ibb` URL is the **team URL recorded in S122** (`team.url`), so this links the
curl program to the `ibb` team mechanically.

Third quote (the 2022-era Medium rate): *"In 2022, typical \"Medium\" rated vulnerabilities
have been rewarded 2,400 USD each."* — consistent with the advisory's
`Bug bounty: 2400 USD` for a Medium-severity flaw.

Fourth quote (taxes/payout): *"The curl project or its security team never actually receive
any of this money, hold the money, or pay out the money."* — this is curl's own statement
that it is **not** the payer, i.e. the direct textual basis for `payer: internet-bug-bounty`.

**Caveat:** the current `master` `docs/BUG-BOUNTY.md` (commit `ed7bf43a08`, 2026-03-10) says
*"The curl project does not offer any rewards for reported bugs or vulnerabilities."* The
2026-01-22 commit `ca7ef4b817` ("we stop the bug-bounty end of Jan 2026") removed the
mentions. So the *historical* file must be cited, not `master`.

### Lead (c) — KEV re-check (RESOLVED, unchanged)

| field | value |
|---|---|
| URL | `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` |
| HTTP status | **200** |
| Located quote | n/a — structured feed; `catalogVersion 2026.11.06`, `count 1769`, **0** occurrences of `CVE-2023-28319` |
| Would it change a C2 pricing field? | **No.** `kev: not-listed` remains correct. |

### Leads sought but NOT available (recorded so the L1 does not re-chase them)

| lead tried | result |
|---|---|
| `https://internetbugbounty.org/` (live) | **301** → `https://www.hackerone.com/internet-bug-bounty` → **301** → `https://www.hackerone.com/company/open-source-community` (**200**). The apex domain is a redirector; `www.internetbugbounty.org` does not resolve (no A/AAAA). |
| `https://hackerone.com/ibb` (live) | **200**, but the page is a JS shell (7497 bytes; body text is only *"It looks like your JavaScript is disabled."*). The 80/20 policy is **not** in the served HTML — only the archived renders carry it. |
| `https://hackerone.com/ibb/policy` | **403** → `/users/sign_in` (login required; not attempted). |
| `https://api.hackerone.com/v1/hackers/reports/1997312` and `/v1/programs/ibb` | **401** (auth required). |
| `https://docs.hackerone.com/en/articles/8496298-internet-bug-bounty` (the page's own "Read the FAQs" link) | **404** live and **not archived** in arquivo.pt (0 results). Dead link. |
| `web.archive.org` (Wayback) | **unreachable from this host** — every request times out (000) after 15–90 s, including `archive.org/wayback/available` (which *did* answer) and the CDX API. `arquivo.pt` was used instead. |
| An IBB "public bounty table" listing CVE-2023-28319's award | **not found.** `hackerone.com/ibb?type=table` returns the JS shell (**200**, 7497 bytes); no public per-CVE award listing is reachable without login. |

---

## 4. Effect on C2's pricing fields — none

| C2 field | frozen value | effect of this seat's findings |
|---|---|---|
| `program` | `ibb` | unchanged — S122 `team.handle` live-confirmed |
| `payer` | `internet-bug-bounty` | unchanged — S123 Q02 live-confirmed; **corroborated** by curl's own `BUG-BOUNTY.md` ("decided and paid by the Internet Bug Bounty") |
| `severity` | `medium` | unchanged — S122 + S120 Q02 live-confirmed |
| `reward-at-disclosure` | `2400 USD` | unchanged — S120 `Bug bounty: 2400 USD` live at line 81; **corroborated** by curl's "2,400 USD" Medium rate |
| `platform-bounty-flag` | `true` | unchanged — S122 `has_bounty?` live-confirmed |
| `original-report` | `1913733` | unchanged — S122 Q05 live-confirmed; S120 `Original report:` live at line 83 |
| `reward-current-policy` | `ended 2026-01-31` | unchanged — S123 Q01 + S121 Q01 live-confirmed |
| `kev` | `not-listed` | unchanged — live KEV 2026.11.06 re-confirmed |
| `cve` | `CVE-2023-28319` | unchanged |

**No field changes.** The two substantive new facts (the 80/20 split; curl's "decided and paid
by the Internet Bug Bounty") are *context for the payer side*, and the 80/20 sentence is
**too late** to be applied to a May-2023 award. They are worth citing as corroboration but
must not be used to re-derive `reward-at-disclosure` (which is bound to the S120 advisory line
by the frozen counter's `derive()`).

---

## 5. ROUTED DEFECT — the working tree drifted from the frozen C2 digests (not caused by this seat)

Observed while re-verifying, at 2026-11-07 ~22:20 local. The L1 applied a presigned-URL
redaction (`.ufo/waves/round-86/l1/redact-presigned.py`, receipt
`.ufo/waves/round-86/l1/redact-presigned-r86.txt`) that rewrote **two tracked lane files**
*after* the freeze commit `252df0c9`:

```
 M corpus/source-snapshots/round-86/S122.txt
 M corpus/source-snapshots/round-86/manifest.json
```

Consequences, all measured:

| predicate / limb | state now | evidence |
|---|---|---|
| C2 P2 (`frozen instrument bytes at landing equal the sha256 values in claims.json`) | **FAIL** | `claims.json` still pins `S122.txt`=`ceb01841a5144d72…` and `manifest.json`=`8d3b7d35…`; the tree now holds `08cab370…` and `2de425ba…` |
| C2 P3 (`source-recheck.py --source S122\|S123` exit 0) | **pass** | re-run just now: all `S122:*` and `S123:*` lines `OK`, rc=0 — the manifest was updated in step with the redaction, so the local check is self-consistent |
| C2 E2 (evidence binding) | **FAIL** | `e2e-check.py` reports `LIMB E2 FAIL bound=S123` — the candidate package's `evidence/S122.txt` is still the **9131-byte unredacted** file, so it no longer byte-matches the lane's 5361-byte redacted snapshot |
| C2 E1 (r43 gate) | **FAIL** | `claim-package-check.py` on the candidate: `RULE R-NOSECRET verdict=fail detail=hits=1,first=evidence/S122.txt,shape=credential` → `verdict=DEFECT exit=1` |
| C1 M4 (basename uniqueness) | **unaffected** | the redaction changed bytes, not paths; `git ls-files` still yields exactly one tracked file with basename `S122.txt` |

Reproduce (read-only):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
git status --porcelain -- corpus/source-snapshots/round-86/
python3 - <<'PY'
import json,hashlib
c=json.load(open('.ufo/waves/round-86/claims.json'))
for rel in ('corpus/source-snapshots/round-86/manifest.json','corpus/source-snapshots/round-86/S122.txt'):
    got=hashlib.sha256(open(rel,'rb').read()).hexdigest()
    want=c['instruments'][rel]
    print(('OK  ' if got==want else 'DRIFT'), rel, 'want', want[:16], 'got', got[:16])
PY
python3 -B .ufo/waves/round-86/c2/e2e-check.py --lane . --pkg .ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312
python3 -B corpus/instruments/claim-package-check.py .ufo/waves/round-86/w1/ExecC2Package-candidate/curl-ibb-h1-1997312
```

**What I verified about the fix path** (in scratch, on a copy — the lane was not modified):
replacing the candidate's `evidence/S122.txt` with the **redacted** lane snapshot and updating
its `evidence/manifest.json` entry flips **E2 to pass** (`LIMB E2 pass bound=S122,S123`) and
clears **R-NOSECRET** (`verdict=pass detail=hits=0`). Two residual failures remain in that
construction and are the L1's to close: `R-REDACT detail=digest-mismatch=1` (a second digest
field elsewhere in the package still names the old `S122` digest) and
`R-STATUS detail=manifest_sha256=mismatch` / `R-REPORT detail=cited=4,unbound=1` (the
package's `provenance.json` / `status.json` / `report.md` digest references were not updated
in step). **All four must be updated together**, not just the evidence bytes.

**Also needed:** `claims.json` must record the post-redaction digests (or the freeze's
pre-redaction digests must be preserved as the binding and the redacted file moved out of the
frozen-instrument path). The `claims.json` `instruments` block is itself covered by C1's P2
("frozen instrument bytes at landing equal the sha256 values in this file's instruments
block") — so as things stand, **C1 P2 fails for the same reason**, since the L1's
`c1-landing-r86.txt` P2 block was measured at commit `fdb5f4a`, *before* the redaction.
Re-measure P2 at the actual landing commit.

**Note on the redaction itself:** it is a *security improvement* (removing live AWS STS
session-token material from a tracked file — those presigned URLs expired
2026-11-07T01:58:29Z but the token material was committed). It is correct to redact; the
defect is only that the redaction was not propagated to `claims.json`, the candidate
package's digests, and the P2 measurement. The pre-redaction bytes remain recoverable from
the pushed freeze commit `252df0c9`, so nothing is lost.

---

## 6. Bottom line for the L1

- **C2's pricing content is fully corroborated.** Every manifest quote is live-verified; every
  reused round-85 quote is live-verified; the KEV `not-listed` field is re-confirmed on a
  newer catalog. No pricing field changes.
- **Two new corroborating leads** (IBB 80/20 split policy; curl's own "decided and paid by
  the Internet Bug Bounty") — usable as context for the payer side, with the caveat that the
  80/20 sentence post-dates the May-2023 disclosure and must not be used to re-derive the
  2400 USD.
- **One routed defect** (§5): the working tree's redacted `S122.txt` / `manifest.json` no
  longer match `claims.json`, and the candidate package still holds the unredacted
  `evidence/S122.txt`. C1 P2 and C2 P2/E1/E2 are all currently FAIL. The fix is to propagate
  the redacted digests through `claims.json`, `evidence/manifest.json`, `provenance.json`,
  `status.json`, `report.md`, and to re-measure P2 at the real landing commit.
- **C1's own content is unaffected by my findings** (no knowledge-scope citation was touched;
  M4/M5 read file *paths* and *line counts*, and the redaction preserved S122's 1-line
  structure and the basename uniqueness).

## 7. Files written by this seat

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources.md` (this report)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/verification.json`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-H1-report-1997312.json` (redacted of presigned STS query strings)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-H1-report-1913733.json`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-daniel-end-of-curl-bug-bounty.html`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-curl-CVE-2023-28319.html`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-norm-S120-equivalent.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-norm-S121-equivalent.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-norm-S123-equivalent.txt`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/live-KEV-catalog.json`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/IBB-program-page-2024-08-13-archived.html`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-86/w1/ScoutSources-receipts/curl-BUG-BOUNTY-asof-2023-05-17.md`

No file named `S<digits>.txt` was written into `w1/` or `w1/ScoutSources-receipts/`.
No lane file outside `w1/` was modified. No git or jj write was performed.
Scratch `/fast/scratch/hyaku/kasegi-r86/ScoutSources` deleted on exit.
