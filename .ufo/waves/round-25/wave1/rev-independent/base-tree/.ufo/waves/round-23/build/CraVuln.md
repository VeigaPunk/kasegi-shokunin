# CraVuln — CRA Article 14(1)–(2): 24 h / 72 h / final-report clocks against official bytes

- Seat: `KasegiR23.CraVuln-5` (scout, read-only lane)
- Round: 23 · observed base `922a4dde90b60b465e2b8b241d1fe363f1f27e98`
- Observed: 2026-10-20T21:44Z · axes: `depth:verifiability`, `coverage`
- Lane: open the official CRA text, verify Article 14(1)–(2) (actively exploited
  vulnerability: 24 h early warning, 72 h notification, final-report condition),
  supply exact ≤25-word located quotes with date/version, and check the existing
  S024 row. Production edits, admission and version rulings are L1's; this seat
  wrote only this file (`git status`: `corpus/SOURCES.md` and the
  `.ufo/waves/round-23/` tree were already modified/untracked before and after
  this seat's work — this seat changed neither).

## 1. Opened source identity (observed)

The assignment URL `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` is
**not directly fetchable by a plain HTTP client**: `curl` receives HTTP **202**
with `x-amzn-waf-action: challenge` and a 2035-byte diagnostic page (AWS WAF),
zero regulation bytes. Two retrievals were made instead:

| # | retrieval | result |
|---|---|---|
| A | Publications Office **Cellar**, `https://publications.europa.eu/resource/celex/32024R2847`, `Accept: application/xhtml+xml`, `Accept-Language: eng` | 303 → `http://publications.europa.eu/resource/cellar/21b7d4eb-a6e2-11ef-85f0-01aa75ed71a1.0006.03/DOC_1`; HTTP **200**, `application/xhtml+xml;charset=UTF-8`, **710 696 bytes**, 2026-10-20T21:44:30Z |
| B | Reader rendering of the *same* ELI URL (reader method `jina`), used only to cross-check A | full text, 1729 rendered lines |

Official-bytes identity (A):

| field | value |
|---|---|
| `ETag` | `"Con-20241125174506000"` |
| `Last-Modified` | `Mon, 25 Nov 2024 16:45:06 GMT` |
| embedded converter header | `CONVEX # converter_version:9.16.1 # generated_on:20241125-1721 # ELI version:0.2` |
| raw SHA-256 (A) | `fe0cca4a0caec50e7cf5a91432b94a19b211f86be8584fdba56372bdcea571ed` |
| re-fetch at 21:44:30Z | same 710 696 bytes, **same SHA-256** (byte-stable) |
| Article 14 plain text, whitespace-collapsed (after tag strip, entity unescape, U+00A0→space) | 8 932 chars, 1 373 words, SHA-256 `f350c18db5d7eb9c2caaa4f04f6e22ae76c9c414c5a7c2f5b01942b3686a8b73` |
| Article 14 whitespace-**stripped** stream | 7 560 chars |

Date/version (from the official XHTML title table and signature block):

- OJ **L series**, act number **2024/2847**, OJ date **20.11.2024**.
- Title: “REGULATION (EU) 2024/2847 OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL
  **of 23 October 2024** on horizontal cybersecurity requirements for products
  with digital elements … (Cyber Resilience Act)”.
- Signed: “Done at Strasbourg, 23 October 2024.”
- Version pinned by `ETag Con-20241125174506000` / generated 2024-11-25.
- This is the OJ first-publication (FMX) representation; no consolidated version
  was located (three guessed consolidated CELEX ids returned 404 —
  see §7; not proof of absence).

Rendering equivalence (A vs B): after collapsing whitespace, the Article 14
character stream of the reader rendering is **identical** to the official Cellar
stream — both 7 560 chars, first differing character: none. The only textual
difference between the two renderings is the reader gluing paragraph labels to
the following word (“1.A manufacturer”), which disappears when whitespace is
removed. This means the URL quoted by S024/S029 is authoritative, but its text
must be read through a renderer or Cellar; the pinned recheck must normalize tags
and U+00A0 before substring assertions (see §5).

## 2. Required located quote — Article 14(2)(a) early warning (17 words)

> “without undue delay and in any event within 24 hours of the manufacturer
> becoming aware of it”
> — Regulation (EU) 2024/2847, **Article 14(2)(a)**, OJ L 2024/2847 of
> 20.11.2024 (ETag `Con-20241125174506000`), fetched 2026-10-20.

- Whitespace word count: **17** (≤25). Exact substring of the official Article 14
  stream (`' '.join`-normalized).
- The full clause continues “…, indicating, where applicable, the Member States
  on the territory of which the manufacturer is aware that their product with
  digital elements has been made available”. The complete clause is 55 words, over
  budget; do not quote it whole.
- Note: the 10-word fragment “within 24 hours of the manufacturer becoming aware
  of it” is also verbatim but occurs **twice** in Article 14 (14(2)(a) and
  14(4)(a), vulnerability vs incident track). The 17-word form above is still not
  unique; uniqueness comes from the located clause label, not the string.

## 3. Article 14(1)–(2) findings (each falsifiable against the pinned bytes)

**F1 — Recipient, channel, trigger (no severity threshold).** Article 14(1)
requires a manufacturer to notify “any actively exploited vulnerability contained
in the product with digital elements that it becomes aware of”, simultaneously to
the CSIRT designated as coordinator (per 14(7)) and to ENISA, through the single
reporting platform of Article 16. Exact quotes:

| location | exact quote | words |
|---|---|---|
| Art. 14(1) | “The manufacturer shall notify that actively exploited vulnerability via the single reporting platform established pursuant to Article 16.” | 18 |
| Art. 14(1) | “any actively exploited vulnerability contained in the product with digital elements that it becomes aware of” | 16 |
| Art. 3, point (42) | “a vulnerability for which there is reliable evidence that a malicious actor has exploited it” | 15 |

Falsifier: Art. 14(3) says “any **severe** incident”; 14(1) contains no severity
qualifier. A summary that imposes a severity threshold on the vulnerability track
is false against 14(1)+(3).

**F2 — 24-hour early warning.** Art. 14(2)(a): early warning notification
“without undue delay and in any event within 24 hours of the manufacturer becoming
aware of it”; content is the Member States of availability where applicable.
Quote and count in §2.

**F3 — 72-hour vulnerability notification.** Art. 14(2)(b), exact quote (23 words):

> “a vulnerability notification, without undue delay and in any event within
> 72 hours of the manufacturer becoming aware of the actively exploited
> vulnerability”

Required content: general information as available on the product, the general
nature of the exploit and vulnerability, corrective/mitigating measures taken,
measures users can take, and the manufacturer's sensitivity marking. The clause
is prefixed “unless the relevant information has already been provided”.

**F4 — Final-report condition is measure availability, not awareness.**
Art. 14(2)(c), exact quote (16 words):

> “a final report, no later than 14 days after a corrective or mitigating measure
> is available”

- The clock start event is the **availability of a corrective or mitigating
  measure**; the text states no outer limit measured from awareness. “14 days”
  occurs **once** in the whole of Article 14 (verified `count('14 days') == 1`).
- Like (b), the clause is conditional: “unless the relevant information has
  already been provided”.
- Required content: (i) description incl. severity and impact; (ii) where
  available, information on the malicious actor exploiting it; (iii) details of
  the security update or other corrective measures made available.
- Contrast, same Article: for severe incidents the final report is “within one
  month after the submission of the incident notification under point (b)”
  (14(4)(c), 16 words) — a different start event and duration.

**F5 — Applicability dates.** Art. 71(2): “Article 14 shall apply from
11 September 2026” (8 words), earlier than the Regulation's general “This
Regulation shall apply from 11 December 2027.” (8 words). Art. 69(3) extends the
duty to legacy products: “the obligations laid down in Article 14 shall apply to
all products” (12 words) “… that have been placed on the market before
11 December 2027” (10 words). Consequence, falsifiable today (2026-10-20): the
Article 14 clocks are **already applicable**, not a 2027 duty. The two 69(3)
fragments are separated by “with digital elements that fall within the scope of
this Regulation”; do not join them into one quotation without the ellipsis.

**F6 — Optional intermediate report.** Art. 14(6): the receiving CSIRT “may
request manufacturers to provide an intermediate report on relevant status
updates” — a discretionary request, not a scheduled fourth stage.

## 4. Verification of the already-landed F08 material (observed defects)

At this seat's read time the working tree (uncommitted) already contained the
successor row and knowledge entry that this assignment was scoped to supply:

- `corpus/SOURCES.md:35` — `S029 | Regulation (EU) 2024/2847, CRA manufacturer
  reporting clocks | … | mined | 2026-10-20 | on-release |
  corpus/knowledge/cra-manufacturer-reporting-duties.md`; text says “supersedes
  S024”. `S024` itself (`corpus/SOURCES.md:30`) is unchanged, `queued`, with the
  caveat “Article 14 wording not yet verified against EUR-Lex”.
- `corpus/knowledge/cra-manufacturer-reporting-duties.md` exists with the Q1
  header (`source:`, `verified-at: 2026-10-20`, executable `recheck:` line 4).
- `corpus/README.md:202` F08 row is still `queued` with entry `—` (not yet
  integrated).

Independent checks against the official bytes:

- **5 of the entry's 6 quote-table rows verify exactly** (lines 45–49): the
  24 h, 72 h, 14-day-final, one-month-incident and 11-September-2026 strings are
  all verbatim substrings of the official Article 14/71 text; the S029 Gate quote
  “no later than 14 days after a corrective or mitigating measure is available”
  (13 words) also verifies.
- **D1 — one quote is not verbatim.** Entry line 50:
  `| Article 71 | “It shall apply from 11 December 2027.” |`. The string
  “It shall apply” occurs **0 times** in the official text and **0 times** in the
  entry's own pinned snapshot `corpus/source-snapshots/round-23/S029.txt`; the
  actual sentence is “This Regulation shall apply from 11 December 2027.”
  (8 words, verified). This fails QUALITY Q3 (verbatim quote). Fix: replace that
  row's quote with the actual sentence; locator should be `Article 71(2)` (first
  subparagraph), and line 49's quote likewise `Article 71(2)` (second
  subparagraph).
- **D2 — the declared recheck is currently red.** Running line 4 verbatim:
  `python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-23/manifest.json --source S029` prints
  `manifest UNAVAILABLE reason=missing` and exits **2**. The snapshot directory
  contains `S018.txt`, `S029.txt`, `S030.txt` but **no `manifest.json`** (observed
  21:44Z). Per Q7 a red recheck is not admission evidence; if a manifest with these
  six quotes is added, the instrument (after a SHA-256 match) checks each quote as
  a substring and would report D1 as `MISMATCH reason=quote-not-found`.
- **D3 (provenance note, not a defect).** `S029.txt` is a 19 900-byte excerpt
  (SHA-256 `82514478b6c5fb8f81c0a51391da91bd35f1f0d3f35bc008b0f5afdf4ce32b8c`)
  in reader (markdown/URL) form, explicitly “Article 14” through at least
  Article 71. Its Article 14 whitespace-stripped stream is **character-identical**
  to the official Cellar stream (7 560 chars). Recording that provenance (official
  CELEX raw digest `fe0cca4a…` vs excerpt digest) would make the pin auditable;
  the file presently has no provenance header.

No edit was made by this seat to either production file.

## 5. Reproduction (fresh network verification, corrupt and missing controls)

Fresh official fetch with digest pin and four quote assertions:

```bash
set -eu
f=$(mktemp /tmp/cra.XXXXXX.xhtml)
curl -fsSL -H 'Accept: application/xhtml+xml' -H 'Accept-Language: eng' \
  https://publications.europa.eu/resource/celex/32024R2847 -o "$f"
[ "$(sha256sum "$f" | cut -d' ' -f1)" = \
  fe0cca4a0caec50e7cf5a91432b94a19b211f86be8584fdba56372bdcea571ed ]
python3 - "$f" <<'PY'
import sys,re,html
t=re.sub(r'<[^>]+>','',open(sys.argv[1],encoding='utf-8').read())
t=html.unescape(t).replace('\xa0',' '); t=re.sub(r'\s+',' ',t)
for q in [
 "without undue delay and in any event within 24 hours of the manufacturer becoming aware of it",
 "a vulnerability notification, without undue delay and in any event within 72 hours of the manufacturer becoming aware of the actively exploited vulnerability",
 "a final report, no later than 14 days after a corrective or mitigating measure is available",
 "Article 14 shall apply from 11 September 2026"]:
    assert q in t, "MISSING: "+q
print("OK 4/4 quotes in CELEX 32024R2847")
PY
rm -f "$f"
```

Article 14 extraction and cross-check against the pinned excerpt (both local):

```bash
python3 - <<'PY'
import re,html
raw=open('/tmp/cra.xhtml',encoding='utf-8').read()          # from the command above
i=raw.find('id="art_14"'); j=raw.find('id="art_15"')
seg=re.sub(r'^id="art_14">\s*','',raw[i:j])
t=re.sub(r'<[^>]+>','',seg); t=html.unescape(t).replace('\xa0',' ')
t=re.sub(r'\s+',' ',t).strip(); t=re.sub(r'\s*<div[^>]*$','',t).strip()
s=open('corpus/source-snapshots/round-23/S029.txt',encoding='utf-8').read()
a=s.find("Article 14\n\nReporting obligations of manufacturers")
b=s.find("\nArticle 15\n\nVoluntary reporting",a)
print("article14 chars",len(re.sub(r'\s+','',t)),
      "snapshot-match",re.sub(r'\s+','',t)==re.sub(r'\s+','',s[a:b]))
PY
```

Observed today: `OK 4/4 quotes in CELEX 32024R2847`; `article14 chars 7560
snapshot-match True`. Controls observed: mutating one copy with
`sed 's/within 24 hours/within 23 hours/'` makes the assertion fail; requesting a
non-existent CELEX (`99999R9999`) returns 404 and `curl -f` exits non-zero. Raw
`grep` on the XHTML must **not** be used for quote rechecks: the official bytes
encode several spaces as U+00A0 and split “no later than 14 days …” away from
plain-string matches (raw grep count 0 for that quote).

## 6. Falsifiers / rejected over-generalizations

1. **“The final report is due 14 days after awareness.”** False: 14(2)(c) starts
   the clock at availability of a corrective or mitigating measure; Article 14
   gives no outer limit from awareness.
2. **“All CRA obligations start 11 December 2027.”** False for Article 14:
   Art. 71(2) applies it from 11 September 2026 (live on the observation date).
3. **“Vulnerability and incident reporting share one clock.”** False: incident
   final report is one month after the incident notification (14(4)(c)); the
   vulnerability final report is keyed to measure availability (14(2)(c)).
4. **“The 24 h/72 h clocks apply to any vulnerability, or are a researcher
   publication deadline.”** False: 14(1)–(2) bind manufacturers to *actively
   exploited* vulnerabilities (Art. 3(42) definition) and are notification duties,
   not disclosure authorizations; Art. 15 is the separate voluntary channel.

## 7. Scope limits

- Claims cover the **English OJ first-publication FMX** whose raw digest is pinned
  above, fetched 2026-10-20; not later consolidated/amended text, other language
  versions, or national implementation.
- Not checked: delegated acts under 14(9) (due by 11 December 2025), implementing
  acts under 14(10), national CSIRT end-point operation, whether the Article 16
  single reporting platform is operational, penalties/Art. 64, or the full
  Articles 15–16 inventory despite S029's broader scope text.
- Three guessed consolidated CELEX ids (`02024R2847`, `02024R2847-20260911`,
  `32024R2847R(01)`) returned 404 on Cellar; that is inconclusive about whether a
  consolidated text exists elsewhere.
- The eur-lex ELI URL itself is WAF-challenged to `curl`; availability of the
  reader path is not guaranteed, so the durable recheck uses Cellar bytes.
- The landed entry's defect list (D1–D3) is a point-in-time observation of an
  uncommitted working tree; another seat may correct it concurrently.
- Admission of F08, README/SOURCES integration, and any version ruling are L1's,
  not this seat's. No admission is claimed here.

## 8. Tooling record

No installs or upgrades; no package transactions. Used host `curl`, `sha256sum`,
`python3` (stdlib) and the repo's existing `source-recheck.py`. Scratch confined
to `/tmp` (`cra-cellar.xhtml`, `art14-clean.txt`, `cra-full-clean.txt`). This seat
is read-only: the only file written is this report.
