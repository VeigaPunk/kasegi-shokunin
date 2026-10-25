# ScoutFetchCisco — independent re-fetch of the Cisco vulnerability policy

Seat: `L1Kasegi25.ScoutFetchCisco` (round 25, wave 1). READ-ONLY: this file is the only write.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41` (`git rev-parse HEAD` = same).
Fetched 2026-10-25 ~08:26–08:31 UTC.

## a) Fetch receipt

| field | value |
|---|---|
| URL | `https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html` |
| User-Agent | `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` — the exact `UA` constant at `corpus/instruments/capture-source.py:26` |
| HTTP status | **200** (HTTP/2) |
| bytes | **94 027** |
| body sha256 | **`098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807`** |
| redirects | 0 (`url_effective` = the URL above) |
| repeats | 3 consecutive GETs + 1 urllib GET → same status, same 94 027 bytes, same sha256 every time (deterministic, not a one-off) |
| page's own date | `Last Updated: 2025 September 8` (capture line 490) |

**Re-extraction matches S040.txt exactly.** `capture-source.py`'s own `html_to_text()` applied to the freshly
fetched body produces **33 463 bytes, sha256 `b7f7b55ff3fc723ec5f9ffb2da47f640f0cef12d2f969a5e35754eee0c4e286c`,
503 lines** — byte-identical to `corpus/source-snapshots/round-25/S040.txt` (same 33 463 bytes, same sha256,
same 503 lines). `difflib.unified_diff` over the two line lists → **0 diff lines**. The capture is reproducible
from the live page today, five days after the entry's 2026-10-23 verification.

### The UA matters — this is the sharp edge

The item names `kasegi-shokunin/1.0` as "the lane's capture UA". That truncated string is **blocked**; the
instrument's full UA is not. Measured:

| UA sent | status | bytes |
|---|---|---|
| `kasegi-shokunin/1.0` | **403** | 465 (Akamai `Access Denied`, `server: AkamaiGHost`) |
| `kasegi-shokunin/1.0 (documentation capture)` | **403** | 465 |
| `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` | 200 | 94 027 |
| `kasegi-shokunin/1.0 +https://shokunin.invalid/kasegi` | 200 | 94 027 |
| curl default (`curl/8.9.1`) | 200 | 94 027 |
| Chrome 126 desktop UA | **403** | 465 |

So Akamai's rule here is not "block bots" — it admits the curl default and a URL-bearing custom UA and rejects
both a bare token UA and a full browser UA. A recheck that writes `curl -A kasegi-shokunin/1.0 …` gets 403/465 B
and would read as "source died". The 403 body sha256 is `fe8f80d029ed089b2e47be41d059184056157117d9691142c24358bdb7841e56`.

## b) Four located sentences (line numbers in `corpus/source-snapshots/round-25/S040.txt`)

**1. ISO/IEC alignment — line 58 (sentence spans 58–60), 24 words verbatim:**

> The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018, which are guidelines for disclosure of potential vulnerabilities established by the International Organization for Standardization.

This is the page's *only* mention of 29147 (`grep -n '29147' S040.txt` → line 58 alone); no 2014 edition appears
anywhere in the capture, so the entry's "later than the 2014 edition" is a cross-document comparison, not a
capture claim.

**2. Coordination-partner list — lines 185–192; the four names sit at 186–190.** Verbatim, 20 words
(the CERT/CC acronym is expanded in the preceding words of line 187 as "Computer Emergency Response Team Coordination Center"):

> CERT/CC, Computer Emergency Response Team of Finland (CERT-FI), Japan Computer Emergency Response Team (JP-CERT), and National Protective Security Authority (NPSA)

Per-name line numbers: CERT/CC **187**, CERT-FI **188**, JP-CERT **189**, NPSA **190**. The sentence's tail
(192–193) also carries the "assist … or do so on the incident reporter's behalf" clause the entry paraphrases.

**3. The two acceleration conditions — lines 301 and 302–304** (section head `Disclosure of Security Vulnerabilities`, line 299; lead-in "may, however, expedite disclosure … in the following situations:" at line 300):

> (301) The Cisco PSIRT has completed the incident response process for a high-severity vulnerability and public disclosure of code fixes is planned to address it.  *(24 words)*

> (302–304) The Cisco PSIRT has observed active exploitation of a vulnerability that could lead to increased risk for Cisco customers.  *(19 words, complete sentence)*

**4. Vulnerability definition — lines 66–68.** Two ≤25-word verbatim fragments:

> (66–67) Cisco defines a security vulnerability as a weakness in the computational logic found in software and hardware components  *(18 words)*

> (68) Cisco reserves the right to deviate from this definition based on specific circumstances.  *(13 words)*

The elided middle of the definition (67–68) is "that, when exploited, results in a negative impact to
confidentiality, integrity, or availability." — present, just over the 25-word excerpt budget.

## c) What the staged package claims that the capture does not contain

Checked against `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/vendor-cvd-policy-crosswalk-2026-10-23.md` (read-only).

**Supported, no defect.** ISO sentence, partner list, "assist … or on the reporter's behalf", the
"regardless of … product lifecycle status, until … Last Day of Support (LDoS)" quote (capture 162–163),
"Past the LDoS … continues to accept … but will not analyze, fix, or disclose" (482–483), the
"generally does not publicly disclose … until enough software patches or workarounds exist" lead-in (300),
both acceleration conditions quoted, the definition and the deviation reservation. Every one is an exact
substring of the capture (verified as a whitespace-flattened substring test).

**D-1 (material) — "the two conditions" understates the page.** The entry says "It states the two conditions
under which it will go faster". The capture's `<ul>` at line 300 has **four** `<li>` conditions:
301 (high-severity, code fixes planned), 302–304 (observed active exploitation), **305–308** (potential for
increased public awareness — "Cisco will accelerate the publication of a security announcement …"), and
**309** ("has declared a third-party software vulnerability to be high profile"). Raw HTML confirms exactly
4 `<li>` elements in that list. The entry's "two conditions" is a narrowing the page does not support.

**D-2 (material) — "no bounty" is contradicted by the page itself.** The entry lists Cisco's shape as
"no bounty, no severity ladder for reporters, no submission form". Capture lines **487–489** carry a
"Cisco Bug Bounty Programs" section ("For information on Cisco Bug Bounty programs, see Bug Bounty Programs
at Cisco."). The page defers the bounty to another page; it does not say there is none.

**D-3 (adjacent) — "no severity ladder for reporters".** The page publishes a severity ladder, just not a
reporter-facing reward ladder: CVSS v3.1 Base/Temporal/Environmental at **245–253**, the Security Impact Rating
and the advisory-type table at **254–262** ("Security Advisories for Critical, High, and Medium SIRs include
fixed software information"). "No severity ladder" is defensible only if read as "no payout tiers".

**D-4 (adjacent) — "no submission form".** Literally true (no form), but the page names a reporting channel:
`Email psirt@cisco.com` / "This is the most effective method." at **74–75**, with the encryption note at 77–78.
Read as "no way in", the phrase is wrong.

**Nothing the entry quotes as page text is absent from the capture.** The defects are all framing/count claims
around accurate quotes.

## Provenance and registry hazards (observed, for the L1)

1. **S040.txt is not committed.** `git status --porcelain corpus/source-snapshots/round-25/S040.txt` →
   `?? corpus/source-snapshots/round-25/S040.txt`; `git cat-file -e <base>:corpus/source-snapshots/round-25/S040.txt`
   → `fatal: path … exists on disk, but not in '<base>'` (rc 128). The whole `round-25/` directory is untracked
   working-tree evidence, so "the committed capture" is only true after the L1 lands it. The diff above is against
   the on-disk bytes (sha256 pinned).
2. **`S040` is overloaded and does not mean the Cisco page in the staged id space.** Round-24's renumber map
   (`corpus/lessons/round-24.md:43`) assigns **staged S040 → lane S034**, the 総務省 不正アクセス page.
   The round-25 snapshot file numbering is round-local (S036 Cybozu policy, S037 Cybozu bounty FAQ,
   S038 GMO Pepabo, S039 Hitachi HIRT, S040 Cisco). The crosswalk entry cites **S068**. Any note that equates
   "S040" with the Cisco capture without saying "round-25 file" will be misread against the staged map.
3. **`source: S068` is not a lane registry id.** `corpus/SOURCES.md` has 35 rows, S001–S035; `grep -rn S068`
   across the lane finds only `corpus/lessons/round-24.md:97`. If this entry is admitted it needs a lane id, and
   the capture it cites must be the round-25 file, not S068.
4. **The capture has 5 lines with U+FFFD where the page uses cp1252 right single quotes** (lines 108, 193, 203,
   222, 479). The HTML is served with `content-type: text/html;charset=utf-8` but contains byte `\x92`
   (e.g. `…incident reporter\x92s behalf.`), which `capture-source.py:89` decodes with `errors="replace"`.
   Consequence for the entry's recheck: "confirm the JP-CERT coordination sentence is still present" cannot be a
   literal-substring test if the sentence crosses "reporter's" — the apostrophe is `\ufffd`, not `'` and not `’`.
   Quote to line 190 (NPSA), not 193.
5. **The entry's `recheck:` line is a prose+command hybrid**, not one shell command
   (`recheck: 180d — \`curl …\` then confirm … (ran 2026-10-23)`), which is one of C1's 23 `bash -n` failures;
   and the bare `curl` it shows works only because curl's *default* UA is admitted — adding `-A kasegi-shokunin/1.0`
   (as the instrument's own header comment would suggest) turns it into a 403.

## Method (reproduction)

```
UA='kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)'
curl -sSL -A "$UA" -o body.html -w 'code=%{http_code} bytes=%{size_download}\n' \
  'https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html'
sha256sum body.html
python3 -c "import importlib.util;spec=importlib.util.spec_from_file_location('c','corpus/instruments/capture-source.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);print(m.html_to_text(open('body.html','rb').read().decode('utf-8','replace')),end='')" > re-extract.txt
cmp re-extract.txt corpus/source-snapshots/round-25/S040.txt
```

Tooling: nothing installed or upgraded; no pacman, no uv, no npx. Only `curl`, `python3` (stdlib) and the lane's
own `capture-source.py` (imported, not modified). No file outside this report was written; the fetches and the
re-extraction live in `/tmp/ciscofetch/`.
