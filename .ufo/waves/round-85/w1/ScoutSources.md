# ScoutSources — live re-open of C2 sources + three leads (round 85, w1)

Seat: `ScoutSources` (scout, leaf). Read-only. Fetched 2026-11-07T00:33-00:37Z, plain `GET`,
no login, no target probing, no submission. Scratch `/fast/scratch/hyaku/kasegi-r85/ScoutSources`
(deleted on exit). Receipts: `.ufo/waves/round-85/w1/ScoutSources-receipts/`.

## 0. Headline

- **All 12 manifest quotes for S119/S120/S121 still occur live**, whitespace-collapsed, each
  exactly once. Zero drift on S120/S121.
- **S119 is NOT byte-reproducible**: the committed snapshot's `sha256` cannot be re-derived by
  re-capture today, because the HackerOne JSON carries a wall-clock-relative field
  `allow_singular_disclosure_after` that drifts by exactly the elapsed seconds since capture
  (-443.50001 s observed, 443 s elapsed). Snapshot *bytes* (5001) and *length* are stable; the
  digest is not. S120 and S121 **are** byte-reproducible (recomputed `sha256` == manifest
  `sha256` for both).
- Lead (a) resolved: the **2400 USD** recorded in the curl advisory was paid by the
  **Internet Bug Bounty**, through a *separate* HackerOne report on team `ibb`
  (**report 1997312**, `has_bounty?: true`) — not through the curl-team report 1913733
  (`has_bounty?: false`). This is the reconciliation the C2 pricing needs.
- Lead (b) resolved: curl's paid bug bounty ended **2026-01-31**, announced 2026-01-26.
  Reporting channel returned to HackerOne from 2026-03-01, still with no money.
- Lead (c) resolved: **CVE-2023-28319 is NOT in the CISA KEV catalog**, live feed
  `catalogVersion 2026.11.06`, `count 1769`, 0 occurrences.

## 1. Axis A — the three C2 sources re-opened live

Method: `curl -sS -L --max-time 45 -A <browser UA> <url>`; raw bodies kept as receipts; quotes
checked with `re.sub(r"\s+"," ",t)` collapse (and, for HTML, additionally with tags stripped +
`html.unescape`).

| id | URL | status | final URL | live bytes | manifest raw bytes | match |
|---|---|---|---|---|---|---|
| S119 | `https://hackerone.com/reports/1913733.json` | 200 | same (no redirect) | 5135 | 5135 | yes |
| S120 | `https://curl.se/docs/CVE-2023-28319.html` | 200 | same (no redirect) | 9732 | 9732 | yes |
| S121 | `https://curl.se/dev/vuln-disclosure.html` | 200 | same (no redirect) | 26500 | 26500 | yes |

Live raw `sha256` (recomputed here, receipt bytes are the proof):
S119 `82b11b5e56aa89571215f57283343a81a46efbef519e62f014f175d77d52d67d` ·
S120 `9b83a319c5a806e743c19fe1fbbe00b4cc31d51cbe6ab8099ebd3036681e8304` ·
S121 `91462d3511134e869e9afbe243d4dce564f5b373cd4a03066082702206df8a42`.
(The manifest's `sha256` binds the **snapshot**, not the raw body; the raw body sizes it records
in `fetch_method` all match live.)

### 1.1 Quote survival — all 12 present, occurrence count 1 each

`in_live_raw_collapsed` / `in_live_tags_stripped_collapsed` / `in_committed_snapshot_collapsed`,
plus occurrence counts. Full record: `ScoutSources-receipts/verification.json`.

| id | quote id | live raw | live tag-stripped | committed snapshot | live occurrences (raw / stripped) |
|---|---|---|---|---|---|
| S119 | Q01-severity-rating `"severity_rating":"medium"` | yes | yes | yes | 1 / 1 |
| S119 | Q02-has-bounty-flag `"has_bounty?":false` | yes | yes | yes | 1 / 1 |
| S119 | Q03-cve-id `"cve_ids":["CVE-2023-28319"]` | yes | yes | yes | 1 / 1 |
| S119 | Q04-team-handle `"handle":"curl"` | yes | yes | yes | 1 / 1 |
| S120 | Q01-cwe `CWE-416: Use After Free` | yes | yes | yes | 1 / 1 |
| S120 | Q02-severity `Severity: Medium` | yes | yes | yes | 1 / 1 |
| S120 | Q03-bug-bounty `Bug bounty: 2400 USD` | yes | yes | yes | 1 / 1 |
| S120 | Q04-original-report `Original report: https://hackerone.com/reports/1913733` | no¹ | yes | yes | 0 / 1 |
| S120 | Q05-affected `Affected versions: curl 7.81.0 to and including 8.0.1` | no¹ | yes | yes | 0 / 1 |
| S121 | Q01-no-bounty `There is no bug bounty and the curl project never offers rewards for reported vulnerabilities.` | yes | yes | yes | 1 / 1 |
| S121 | Q02-no-cvss `We do not support CVSS as a method to grade security vulnerabilities` | yes | yes | yes | 1 / 1 |
| S121 | Q03-medium-def `This is a security problem that is less hard than Low to exploit or trigger.` | no¹ | yes | yes | 0 / 1 |

¹ These three span an HTML tag in the raw page (e.g. `Severity:` is inside a `<td>`,
`Original report:` precedes an `<a href>`). They occur in the raw body **after tag-stripping**,
which is exactly what the instrument's `html_to_text` does — and they occur verbatim in the
committed snapshot, which was produced by that same pipeline. **No quote is lost to markup.**

Anchor lines: every one of the 12 quotes is verbatim on its declared anchor line of the
committed snapshot (checked line-by-line, `in_committed_snapshot_collapsed` == true and the
anchor line itself contains the collapsed quote).

### 1.2 Capture-pipeline reproduction (new evidence)

Re-running the instrument's own pipeline (`corpus/instruments/capture-source.py`:
`collapse()` for `--kind text`, `html_to_text()` for `--kind html`) over today's live raw bodies:

| id | recomputed snapshot bytes | committed bytes | bytes equal | recomputed sha256 == manifest sha256 |
|---|---|---|---|---|
| S119 | 5001 | 5001 | **no** | **no** |
| S120 | 3053 | 3053 | yes | **yes** |
| S121 | 19670 | 19670 | yes | **yes** |

**S119 drift, isolated to one field.** The live and committed JSON differ in exactly two keys:

1. `allow_singular_disclosure_after` — live `-107102539.66721414`, committed
   `-107102096.16720407`, delta `-443.50001`. The capture is stamped
   `2026-11-07T00:26:28Z` and the live fetch `2026-11-07T00:33:51Z`: **443 s elapsed** — the
   field is a wall-clock-relative countdown, so it drifts by exactly the elapsed time.
2. `vulnerability_information` — **whitespace-only** difference (the reporter's embedded `git
   blame` block is re-indented upstream: `667     char *fingerprint_b64 = NULL;` vs
   `667 char *fingerprint_b64 = NULL;`). Whitespace-collapsed the two strings are **equal**.

Normalizing exactly those two (drop the drifting field, collapse whitespace) makes live and
committed JSON **equal** — every other field, including `severity_rating`, `has_bounty?`,
`cve_ids`, `team.handle`, `disclosed_at`, `vulnerability_information` text, is identical.

Consequence for C2 (falsifiable, and it does **not** break E2): the C2 counter's E2 limb
compares the package's evidence artifact bytes against the **committed** `S119.txt` and
`S120.txt` and their manifest digests. That holds. But S119's manifest `sha256` is **not
re-derivable by re-capture** on any later day — a verifier who re-runs `capture-source.py`
against `https://hackerone.com/reports/1913733.json` will get a *different* digest for the same
logical record and must not report that as a corrupted capture. S120/S121 have no such defect.

Re-runnable command (this seat's finding; run from the lane root):

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B - <<'PY'
import importlib.util, json, os, re, html, hashlib
spec=importlib.util.spec_from_file_location('cs','corpus/instruments/capture-source.py')
cs=importlib.util.module_from_spec(spec); spec.loader.exec_module(cs)
raw=open('/tmp/s119-live.json',encoding='utf-8').read()
out=cs.collapse(raw).encode('utf-8')
print('recomputed sha256', hashlib.sha256(out).hexdigest())
print('manifest  sha256', json.load(open('corpus/source-snapshots/round-85/manifest.json'))['sources'][0]['sha256'])
PY
```

## 2. Lead (a) — who paid the 2400 USD, given S119 `has_bounty?` is false

**Resolved. The payer was the Internet Bug Bounty, on a second HackerOne report.**

`https://hackerone.com/reports/1997312.json` — status **200**, final URL unchanged,
**9203 bytes** (receipt `live-LEAD-hackerone-ibb-1997312.json`).

Observed fields (JSON record, one line):

| field | value |
|---|---|
| `id` | `1997312` |
| `title` | `CVE-2023-28319: UAF in SSH sha256 fingerprint check` |
| `team.handle` / `team.profile.name` | `ibb` / `Internet Bug Bounty` |
| `team.url` | `https://hackerone.com/ibb` |
| `team.profile.about` | `The Internet Bug Bounty rewards security research into vulnerabilities impacting Open Source Software Projects.` |
| `has_bounty?` | **true** |
| `team.offers_bounties` | `true` |
| `reporter.username` | `wct` (same reporter as 1913733) |
| `cve_ids` | `["CVE-2023-28319"]` |
| `severity_rating` | `medium` |
| `created_at` / `submitted_at` | `2023-05-23T08:38:55Z` |
| `disclosed_at` | `2023-06-25T18:16:40Z` |
| `original_report_id` / `original_report_url` | `null` / `null` |
| `state` / `substate` | `Closed` / `resolved` |

One-line quote (≤25 words), located in `vulnerability_information` of the same record:

> "The original submission can be found here: https://hackerone.com/reports/1913733"

and from `team.profile.about`:

> "The Internet Bug Bounty rewards security research into vulnerabilities impacting Open Source Software Projects."

The IBB record contains **no payout amount** (no `amount`/`reward`/`award`/`payout` key exists in
its JSON — searched all 43 top-level keys). The 2400 USD figure exists only in curl's own
records: the advisory (`S120`, `Bug bounty: 2400 USD`) and curl's machine-readable CVE JSON
`https://curl.se/docs/CVE-2023-28319.json` (status 200, 1892 bytes), whose
`database_specific.award` is `{"amount": "2400", "currency": "USD"}`. **That JSON is not in the
round-85 manifest and is not in `SOURCES.md`** — it is a new, machine-checkable corroboration
of the price, worth registering as a lead (see §5).

Corroborating statement from the curl maintainer himself, `https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/`
(status 200, 75270 bytes, post dated **January 26, 2026**), body paragraph 5:

> "I would like to especially highlight the awesome Internet Bug Bounty project, which has paid the bounties for us for many years."

and paragraph 4 (body, after the "87 confirmed vulnerabilities" line):

> "87 confirmed vulnerabilities and over 100,000 USD paid as rewards to researchers."

Reading of the tension the task named: `S119` `has_bounty?: false` describes the **curl-team
report's** platform state (the curl team offers no bounties — `team.offers_bounties: false`,
`team.profile.name: "curl"`). The reward was routed through IBB's own HackerOne program under
report 1997312, where `has_bounty?: true` and `offers_bounties: true`. The two records are
consistent once the payer is identified; the curl advisory records the *amount*, not the payer.

**[INFERENCE]** — The IBB report was created 2023-05-23, five days after the curl advisory
published (2023-05-17), and disclosed 2023-06-25, 39 days after 1913733 was disclosed
(2023-05-24). That ordering is consistent with IBB being the payment channel opened around
publication, but the IBB record states no causal link; the only explicit causal statement found
is Stenberg's "which has paid the bounties for us for many years". Confidence: high on the
identity of the payer (two independent sources: IBB's own program record with `has_bounty?:
true`, and Stenberg's explicit statement), medium on the 2400-USD-to-1997312 linkage
(the amount and the report are connected by CVE id, reporter, title and program, not by any
statement in either record).

## 3. Lead (b) — curl's dated statement ending its paid bug bounty

**Resolved: announced 2026-01-26, effective 2026-01-31.**

`https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/` — status **200**,
final URL unchanged, **75270 bytes** (receipt `live-LEAD-daniel-2026-01-26-end-of-bug-bounty.html`).

Title line: `The end of the curl bug-bounty` — byline `Daniel Stenberg`, dateline
`January 26, 2026`.

One-line quote (tldr paragraph, body lines 2-3 of the post):

> "There is no longer a curl bug-bounty program. It officially stops on January 31, 2026."

Second quote, "Actions" section:

> "We no longer offer any monetary rewards for security reports – no matter which severity."

Corroborating launch post (the bounty era's start), `https://daniel.haxx.se/blog/2019/04/22/curl-hackerone-true/`
— status 200, 56705 bytes:

> "Now we are back with a new and refreshed bug bounty program! The curl bug bounty program reborn."

with the award table in the same post: `Critical: 2,000 USD` / `High: 1,500 USD` /
`Medium: 1,000 USD` / `Low: 500 USD`, and the funding line naming the HackerOne Internet Bug
Bounty program.

First-year accounting, `https://daniel.haxx.se/blog/2020/04/23/report-curls-bug-bounty-one-year-in/`
— status 200, 61887 bytes:

> "We've handed out 1,400 USD so far, which makes it an average of 233 USD per confirmed report."

**Follow-up that matters for pricing** (the naive reading of "the bounty ended" is wrong on the
channel), `https://daniel.haxx.se/blog/2026/02/25/curl-security-moves-again/` — status 200,
69186 bytes, dateline `February 25, 2026`:

> "The reward money is still gone, there is no bug-bounty, no money for vulnerability reports, but we return to accepting"

and

> "Starting March 1st 2026, this is now (again) the official place to report security problems to the curl project."

So the dated sequence is: bounty programme 2019-04-22 → reward programme ended 2026-01-31 →
reporting channel returned to HackerOne 2026-03-01, with **no** money either way. The
`S121` policy page (live, unchanged) states the current position:
"There is no bug bounty and the curl project never offers rewards for reported vulnerabilities."

Note for the package: `S121` says the project "never offers rewards", which is the *current*
policy statement and the one the frozen counter keys on
(`reward-current-policy: none` iff `"There is no bug bounty" in S121`). Stenberg's own 2026-01-26
post is the dated historical counter-statement (over 100,000 USD paid 2019-2026, paid by IBB).
Both are true of their own scope: no rewards *now*, vs a real paid programme that has ended.
The pricing must keep `reward-at-disclosure: 2400 USD` (what S120 records) separate from
`reward-current-policy: none` (what S121 records) — which is exactly the two-field split the
frozen counter derives.

## 4. Lead (c) — is CVE-2023-28319 in the current CISA KEV feed?

**No.** `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` —
status **200**, final URL unchanged, **1832349 bytes** (receipt
`live-KEV-known_exploited_vulnerabilities.json`).

- `catalogVersion` = **2026.11.06**
- `dateReleased` = `2026-11-06T19:44:45.1797Z`
- `count` = **1769** (and `len(vulnerabilities)` = 1769, unique cveIDs = 1769)
- `grep -c 'CVE-2023-28319'` over the raw feed = **0**
- No entry in the feed has `vendorProject` or `product` mentioning curl (0 matches).
- Lane capture `corpus/source-snapshots/round-35/S052.txt`: `catalogVersion` **2026.10.23**,
  `count` 1756, `CVE-2023-28319` occurrences **0** — same answer, older catalog.

So the frozen counter's `kev` derivation (`"not-listed" if kev.count(cve) == 0 else "listed"`)
yields `not-listed`, and the live feed independently confirms it today. The catalogVersion
drifts (2026.10.23 in the capture vs 2026.11.06 live); the package should cite the capture's
value for the frozen derivation and may note the live value separately.

## 5. Other live findings (leads, not registered)

- `https://curl.se/docs/CVE-2023-28319.json` — status 200, 1892 bytes. curl's own CVE 5.5.0
  JSON. Carries `database_specific.award = {"amount":"2400","currency":"USD"}`,
  `database_specific.severity: "Medium"`, `database_specific.issue:
  https://hackerone.com/reports/1913733`, `published: 2023-05-17T08:00:00Z`,
  `credits: [{Wei Chong Tan, FINDER}, {Daniel Stenberg, REMEDIATION_DEVELOPER}]`. **A
  machine-readable second source for the 2400 USD amount**, currently unregistered.
- `https://curl.se/docs/vuln.json` — status 200, 650967 bytes, a 239-entry list of curl CVEs in
  the same schema; the 2023-28319 entry carries the identical `award` block. 0 of the 239
  entries mention "bounty" in any other field.
- `https://cveawg.mitre.org/api/cve/CVE-2023-28319` — status 200, 3917 bytes. The CVE record's
  `assignerShortName` is **`hackerone`** (not curl), and its references list
  `https://hackerone.com/reports/1913733` — the curl advisory is not among the CNA references.
- `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2023-28319` — status 200,
  8136 bytes. NVD scores it CVSS 3.1 **7.5 HIGH** (`AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`),
  sourced to HackerOne. Directly contrasts with curl's own `Severity: Medium` and S121's
  "We do not support CVSS" — the counter's `cvss: not-set-by-vendor` is the vendor-scoped
  statement, and the 7.5 HIGH figure is a third party's.
- `https://curl.se/docs/security.html` — status 200, 110025 bytes. curl's advisory index; lists
  CVE-2023-28319 in its table but carries **no** "bounty" string anywhere. There is no
  curl-hosted bounty page: `https://curl.se/docs/bounty.html` → 404, `https://curl.se/security`
  → 404, `https://curl.se/docs/vulnerability-table.html` → 404.
- `https://hackerone.com/ibb` — status 200 but the HTML is a JavaScript-required shell
  ("It looks like your JavaScript is disabled"); the `ibb` team's textual identity must be taken
  from the report JSON (`team.profile.about`), not from the team page.
- `https://www.hackerone.com/company/open-source-community` — status 200, 341420 bytes; the
  current landing page for the Internet Bug Bounty program (`hackerone.com/internet-bug-bounty`
  redirects here).
- `https://hackerone.com/reports/1997312/bounties.json` → **404**. The per-report bounty
  endpoint does not exist publicly; there is no public endpoint exposing the 2400 amount on
  HackerOne. The amount is knowable only from curl's own records.

## 6. C2 package inputs confirmed against the frozen counter

Re-deriving the frozen counter's pricing expectations by importing
`.ufo/waves/round-85/c2/e2e-check.py` and calling its own `derive()` on the committed lane bytes
(read-only; no lane file written):

```
severity              = medium
reward-at-disclosure  = 2400 USD
platform-bounty-flag  = false
reward-current-policy = none
cvss                  = not-set-by-vendor
kev                   = not-listed
cve                   = CVE-2023-28319
```

Cross-checks against this seat's live re-open:

- `severity` — S120 `Severity: Medium` and S119 `severity_rating: medium` agree; live both
  present. OK.
- `reward-at-disclosure` — S120 `Bug bounty: 2400 USD`; live present, occurrence 1. **And
  independently corroborated live by curl's CVE JSON `award.amount = "2400"`** (new evidence,
  §5). OK.
- `platform-bounty-flag` — S119 `"has_bounty?":false`; live present, occurrence 1. The flag is
  about the **curl-team** record; the money moved on IBB report 1997312 (§2). The package must
  state `false` here and must **not** read it as "unpaid" — that is exactly the SOURCES.md
  S119 caveat ("do not read has_bounty? false as unpaid"). OK, with the §2 caveat available as
  the surrounding prose.
- `reward-current-policy` — S121 "There is no bug bounty"; live present. OK, and consistent with
  the dated 2026-01-26 / 2026-02-25 posts in §3.
- `cvss` — S121 "We do not support CVSS"; live present. OK. Note NVD's 7.5 HIGH (§5) is a
  third-party score, not a curl score.
- `kev` — 0 occurrences in S052 and 0 in the live feed. OK.
- `cve` — S119 `cve_ids[0]`. OK.

E4 quote pool note: the counter pools the **committed snapshots** (`S119`/`S120`/`S121`) for
the `> ` quote lines, so the three tag-wrapped quotes (S120 Q04/Q05, S121 Q03) are usable —
they are verbatim in the snapshots. Verified above.

## 7. What I did not do

- Did not register any lead in `corpus/SOURCES.md`, `corpus/README.md` or any knowledge entry
  (registration is the integrator's job; my seat produces leads with URLs, status and quotes).
- Did not edit the lane tree, the frozen `c1/`, `c2/`, `controls/` bytes, any instrument, or
  any corpus file. Only `.ufo/waves/round-85/w1/ScoutSources.md` and
  `.ufo/waves/round-85/w1/ScoutSources-receipts/` were written.
- Did not run `resolve.py` (the skill-meter counter is the SKILL-scope reading).
- No network activity beyond plain `GET` on the public pages named above; no login, no
  submission, no probing of any target.

## 8. Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ScoutSources.md`
  (this file)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ScoutSources-receipts/verification.json`
  — machine-readable status/final-URL/bytes/digest + per-quote survival table for the three
  manifest sources.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ScoutSources-receipts/live-S119-hackerone-1913733.json`
- `.../live-S120-curl-CVE-2023-28319.html`
- `.../live-S121-curl-vuln-disclosure.html`
- `.../live-LEAD-hackerone-ibb-1997312.json`
- `.../live-LEAD-daniel-2026-01-26-end-of-bug-bounty.html`
- `.../live-LEAD-daniel-2026-02-25-curl-security-moves-again.html`
- `.../live-LEAD-daniel-2019-04-22-curl-hackerone-true.html`
- `.../live-LEAD-daniel-2020-04-23-bug-bounty-one-year-in.html`
- `.../live-LEAD-curl-CVE-2023-28319.json`
- `.../live-LEAD-cveawg-CVE-2023-28319.json`
- `.../live-LEAD-nvd-CVE-2023-28319.json`
- `.../live-KEV-known_exploited_vulnerabilities.json`

(All under `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-85/w1/ScoutSources-receipts/`.)
No tools were installed or upgraded for this seat; no pacman transaction was made.
