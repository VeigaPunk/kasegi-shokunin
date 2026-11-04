# ScoutS098 — scoped findings (kasegi round 65, wave 1)

Seat: **ScoutS098** (leaf, read-only reconnaissance). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round evidence: `.ufo/waves/round-65`. Base master: `a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b`.
Claims are **not** frozen — nothing below is admitted by itself; L1 (KasegiR65) is the sole
production integrator.

Scope of this seat: **C2 source reconnaissance only**. I did not touch C1 (the figure-audit
signal-fail-closed gate); that is other seats' work.

## Deliverables (all under `.ufo/waves/round-65/w1/ScoutS098/`)

| file | what it is |
|---|---|
| `S098.candidate.txt` | candidate capture of the source, 170137 bytes, sha256 `cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2`, 1573 lines |
| `quotes.md` | 28 candidate pinned quotes, each with an `L<n>` anchor and a ≤25-word verbatim quote |
| `quotes_draft.txt` | the machine-checkable quote list the verifier reads (`id|line|quote`) |
| `scope-screen.txt` | scope-screen commands, per-term counts, and every file:line hit |
| `NOTES.md` | distinguishishment paragraph, capture method, fetch bytes/sha256/time, exact URL, weak-ground flags |

Nothing outside my own seat directory was created or modified. No commit, no push, no
mutating git/jj command, no task dispatch, no package install.

## The URL

```
https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1
```

HTTP 200, `text/html; charset=UTF-8`, **229255 fetched bytes**, raw sha256
`3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11`, fetched
**2026-11-04T19:26:42Z**, `Last-Modified: Mon, 26 Jan 2026 14:43:46 GMT`.

The candidate capture was made with **the lane's own instrument**, so its bytes are what
the L1's committed snapshot will contain:

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/capture-source.py --id S098 \
  --url "https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1" \
  --out .ufo/waves/round-65/w1/ScoutS098/S098.candidate.txt --kind html
# S098 status=200 fetched_bytes=229255 snapshot_bytes=170137
# sha256=cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2 utc=2026-11-04T19:26:42Z
```

`--out` pointed at my seat directory; no lane file was written. **Determinism was
re-checked**: a second run two seconds later produced the identical digest, and a third
fetch under a different User-Agent returned byte-identical raw HTML (`cmp` identical).
Strict UTF-8 in, **zero** U+FFFD out.

## Title / version / date

- `<title>` and `og:title` = `PSIRT Services Framework 1.1`; `<h1>` = `PSIRT Services Framework`.
- **The HTML page carries no publication date, no revision date, no version-history table
  and no `<table>` element at all.** `grep` for `April` / `Spring 2020` / `2020` / `2021`
  in the body: **0 hits**. The version survives in-body only as the Downloads list
  (`v1.1 HTML`, `v1.0 HTML`, …) at L1550-1573.
- The only date in the capture is the copyright footer **L1573**:
  `Copyright © 2015—2026 by Forum of Incident Response and Security Teams, Inc. All Rights Reserved.`
- The only date outside the capture is the HTTP `Last-Modified` header.
- Cross-check (different artifact, different URL): the canonical PDF
  `FIRST_PSIRT_Services_Framework_v1.1.pdf` (2712956 bytes, sha256
  `be85371ba2bcadbd2243005b610c4652e2e31842ee396cc2117119f8626cba5a`, 91 pages, PDF
  CreationDate 2021-01-19) prints **`Version 1.1`** and **`Spring 2020`** on its cover.
  I rendered page 1 to PNG and read it to confirm. **Do not cite the PDF's `Spring 2020`
  date as part of the S098 HTML capture** — different URL, different capture.
  Also: `pdftotext` emits a stray `Version 2 (April 202` first line on PDF page 1 that
  is **not visible in the rendered page** — an off-page text artefact, not content.

## What the document actually is

FIRST's **product-side service taxonomy**: the services a vendor PSIRT *may provide*.
Its structural spine (L227) is `SERVICE AREAS – SERVICES – FUNCTIONS – SUB-FUNCTIONS`,
with a written definition per level (L229/L231/L235/L239) and a
Description + Purpose/Outcome template per service/function.

Counts measured in the capture: **6 service areas, 28 services, 84 functions, 159
sub-functions.**

- **SA1** Stakeholder Ecosystem Management (1.1-1.7)
- **SA2** Vulnerability Discovery (2.1-2.5)
- **SA3** Vulnerability Triage and Analysis (3.1-3.3)
- **SA4** Remediation (4.1-4.4)
- **SA5** Vulnerability Disclosure (5.1-5.4)
- **SA6** Training and Education (6.1-6.5)

Plus: Organizational Structure (Distributed / Centralized / Hybrid, L248), Operational
Foundations tiered **Strategic / Tactical / Operational** (L309-401), Annexes 1-5,
Glossary (L1498+), Downloads (L1550+).

Caveat for the L1: **Service Area 1 and Service Area 2 headings carry no title text in
the HTML** (L402 is literally `Service Area 1`, L674 is literally `Service Area 2`); SA3/
SA4/SA5 carry their names inline. SA1's name exists only in prose (L331) and in the PDF
TOC. Quote SA1/SA2 titles from prose, never from the heading line.

## Maturity — the decisive negative finding

**This page defines NO maturity levels.** Measured on the capture:
`grep -iE "level [0-9]"` over the body → **0 hits**; `Maturity Level|Level [0-9]|maturity
model` → **0 hits** in the body.

All body "maturity" mentions: L274, L403, L433, L439, L675 ("Maturity of a PSIRT may be
measured via the availability and efficiency of the difference services prescribed in
this service area" — the source's own "difference" typo), L863, L875, L1499 (glossary
"Actions"), **L1510** (glossary "Maturity — how effectively an organization executes a
particular capability within the mission and authorities of the organization. It is a level
of proficiency attained either in actions or tasks or in an aggregate of functions or
services."), and the Downloads links L1553-1554/L1567-1568.

The **actual level ladder (Level 1 Basic / Level 2 Intermediate / Level 3 Advanced, plus
"Beyond Level 3", 2019, 29 pages) is in a different FIRST document** —
`FIRST_PSIRT_Maturity_Document.pdf` / `psirt_maturity_document` — linked from this
page's Downloads section. It is a separate candidate source, not part of S098.

**Consequence:** if F44 is admitted as "PSIRT Services Framework v1.1", any maturity-level
claim would be unsupportable from this capture. The Strategic/Tactical/Operational tiers
(L309-401) are a *different axis* and are not levels.

## Distinguishishment (suggested F44 ground)

> **F44 — FIRST PSIRT Services Framework v1.1: the product-side service taxonomy a vendor
> PSIRT is measured against.** FIRST's own description of the services a **product**
> incident response team may provide, organised as service areas → services → functions →
> sub-functions (L227) over six service areas, with 28 services, 84 functions and 159
> sub-functions. Its subject is the **vendor's own PSIRT operation**: the
> Distributed/Centralized/Hybrid organisational models, the Operational Foundations tiered
> Strategic/Tactical/Operational, and the per-service Purpose/Outcome templates. Its
> differentiator from every other FIRST document the lane holds is stated by the document
> itself: "The focus on products is the key differentiator between the PSIRT of an
> organization and other incident response teams represented in the same organization"
> (L244).

- **Not F43 (CERT/CC CVD phases/roles, S095).** F43's unit is a *phase → five-role*
  matrix with a Validation/Remediation/Deployment row assignment. S098 has **no phases
  and no role matrix**; it has a service catalogue, and L844 says outright that the order
  of operations varies ("there are variations, such as the exact point when a 'case' is
  created"). F43 adapts ISO/IEC 30111:2019; S098 cites 30111 only as a glossary footnote
  (L1522-1523; 29147 at L1513-1517).
- **Not F06/S018 (FIRST multi-party coordination guidelines).** S018 is *guidelines for
  parties* (role/relationship recording, negotiated timelines, upstream/downstream web;
  "an upstream fix is not downstream evidence"). S098's Service Area 5 covers the same
  territory **from the vendor-PSIRT's side** — notification to intermediate
  vendor/coordinator/finder (L1145-1146), bi-lateral and multi-vendor coordination
  (L1195, L1210), disclosure artefacts (L1236, L1248) — but as *services the PSIRT
  performs*, in a Service/Function/Sub-Function taxonomy with Purpose/Outcome metrics,
  not as guidelines for how parties should relate. Different URL tree
  (`/standards/frameworks/psirts/` vs `/global/sigs/vulnerability-coordination/multiparty/`),
  different artifact type (HTML rendering vs PDF guidelines). S018 is not cited by name on
  the S098 page; the only FIRST cross-reference in S098's footnotes is the multiparty
  **v1.0** PDF URL at L1531.
- **Not S053/F19 (EPSS) nor S054/F20 (SSVC).** EPSS is a published 0-1
  exploitation-likelihood score (S053.txt:216-217); SSVC is a decision-point
  prioritisation method. S098 defines **no score and no prioritisation method**. "EPSS"
  appears in the capture only as site-navigation chrome (L153, L1547). S098 names CVSS
  twice — once in Service 3.1 (L853) and once in the glossary (L1503) — i.e. it
  *references* the severity scale the lane already holds (F01/S001/S002) without
  restating it. SSVC/EPSS are scoring *inputs* a PSIRT consumes; S098 is the *service
  structure* around them.
- **Not the maturity document** — see above.

### Every held row that could overlap, and why it does not

| held row | overlap | why not |
|---|---|---|
| **F43** (S095) | **highest** | phase/role matrix vs service catalogue; L844 states operational variation; no phases, no role matrix in S098 |
| **F06** (S018) | **high** | guidelines-for-parties vs vendor's-own-service-catalogue; different URL tree, different artifact type; S018 not cited by S098 |
| **S053/F19** | medium | 0-1 score vs no score; EPSS appears only as nav chrome (L153, L1547) |
| **S054/F20** | medium | decision points vs none; SA3's Quality Gate/Bug Bars (L852, L298) is a *threshold* for what counts as a vulnerability, not a priority category |
| **F01** (S001/S002) | medium | CVSS referenced at L593/L853/L1503; no metric/vector/score semantics defined — all CVSS ground stays F01 |
| **F02** (S003-S005) | medium | F02 holds stated clocks; S098 states **no** numeric timeline (asks teams to negotiate, L1160/L1190) |
| **F10** (S036-S040) | low-med | F10 = specific vendor policies (Cisco, Hitachi, JPCERT/CC); S098 is the generic framework, names no vendor and no clock |
| **F11/F38** (S041) | low | 29147/30111 cited only as glossary footnotes (L1513-1517, L1522-1523); no division of labour assigned |
| **F15** (S048) | low-med | F15 = one named programme (MSVR) as an intake route; S098 2.1 "Intake of Vulnerability Reporting" (L680) is a generic service (Ensure Reachability L686, Handle Vulnerability Reports L704) |
| **F21/F22** (S055, S043) | low-med | L1259 *recommends* CSAF; S098 defines no product_status / VEX justification flags; CSAF is a URL footnote (L1525) |
| **F25/F30** (S032, S076) | low | no CVE-record schema, no API; CVE only in the glossary (L1502) |
| **F18** (S052) | low | KEV only in nav chrome; no KEV content |
| **F07** (S031) | low | no CNA/CVE-assignment rules |
| **F08/F09/F03** (S029, S032-S035, S006-S008) | low | grants no authority, sets no statutory duty, no safe harbour |
| **F24** (S063) | low | no security.txt / machine-readable discovery for intake |

**Cleared by keyword sweep** (no subject-matter contact): F04, F05, F13, F14, F16, F17,
F23, F26, F27, F28, F29, F31, F32, F33, F34, F35, F36, F37, F39, F40, F41, F42.

## Scope screen (full output in `scope-screen.txt`)

Over `PROVINCE.md`, `corpus/README.md` (frontier rows), `corpus/SOURCES.md`,
`corpus/knowledge/*.md` (81 files), as counting **matching lines**:

| term | cs | ci | | term | cs | ci |
|---|---|---|---|---|---|---|
| PSIRT | **12** | 12 | | services framework | **0** | **0** |
| FIRST | 37 | 204 | | multi-party | 11 | 14 |
| maturity | **0** | **0** | | multiparty | 6 | 6 |
| intake | 91 | 93 | | SSVC | 75 | 87 |
| triage | 59 | 73 | | EPSS | 70 | 72 |
| remediation | 43 | 49 | | CVD | 40 | 45 |
| disclosure | 283 | 315 | | CERT/CC | 86 | 86 |

Two decisive zeros: **`maturity` 0/0** and **`services framework` 0/0**. The lane holds no
services-framework document and uses the word "maturity" nowhere.

The 12 PSIRT hits are all a PSIRT as an **organisation**: `corpus/SOURCES.md:46` (S040
Cisco), `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:1,46,47,48,50,51,52`,
`corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:59,63`,
`corpus/knowledge/iso-29147-and-30111-division-of-labour.md:19`,
`corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:60`. **Not one** names
FIRST's framework, a service area, a service, a function, a sub-function or a level.

The 37 FIRST hits are exactly F19/EPSS (`PROVINCE.md:78`, `corpus/README.md:389`),
F06/S018 (`corpus/README.md:207`, `corpus/SOURCES.md:24`), CVSS rows
(`corpus/SOURCES.md:7,8`), S053 (`corpus/SOURCES.md:59`), source-table prose
(`corpus/SOURCES.md:117,122,123,128,134`), and the knowledge entries citing them
(`cisa-cvd-program-stages.md:5,54,95,114`; `csaf-vex-product-status-and-justifications.md:125`;
`cvss-v4-severity-and-vector.md:38,43`; `epss-exploit-prediction-scoring.md:1,10,11,14,83,99,102,110,132,186,196,247`;
`multiparty-vulnerability-coordination.md:15,44,51,52`; `ufo-archive-2026.md:80`;
`vendor-third-party-finding-coordination.md:63`). The 167-line ci inflation is the English
word "first". **`first.org/standards/frameworks` occurs 0 times in the lane**;
`psirt_services_framework` occurs 0 times. So the source is **not already held** and
neither F44 nor S098 is taken — S097 is the highest source id, F43 the highest frontier id.

The high-count generics (intake 91, triage 59, remediation 43, disclosure 283) are the
shared English of the whole disclosure domain; the discriminator is the **unit of
analysis**, not the vocabulary.

## Flags — how good a first-party ground is this?

**Good:** first-party `www.first.org`; HTTP 200; no paywall, login, cookie wall or bot
challenge; whole body server-rendered in the initial 229255-byte response; 1 `<script>`
tag and 0 `<noscript>` blocks, so **not** JavaScript-dependent; deterministic (two
captures → identical digest; two UAs → identical raw bytes); strict UTF-8, zero U+FFFD;
stable `id` anchors on every heading; a downloadable-PDF counterpart exists.

**Cautions the L1 must carry:**

1. **No in-page version or date** — version only in `<title>`/`og:title`/Downloads;
   date only outside the capture. Weakest version ground among the held sources.
2. **Mutable + a site-wide `Last-Modified`** — identical for the framework page and the
   maturity page (`Mon, 26 Jan 2026 14:43:46 GMT`), so it is a site publish, not a
   document revision. Only the sha256 pin defends against silent prose edits.
3. **No maturity levels in it** (§ above).
4. **Rendering, not the artifact** — no page numbers; the 20 figure artworks are separate
   PNGs (`psfw_media/v1.1/image1..20.png`, HTTP 200 verified) so the text capture holds
   only the 40 caption lines; SA1/SA2 heading titles lost.
5. **Site chrome dominates the head** — L1-216 are FIRST's global nav; pin quotes inside
   the body range and use the lane's `body_lines` manifest mechanism (cf.
   `corpus/source-snapshots/round-62/manifest.json`, `body_lines: [56,157]`).
6. **Not a normative standard** — the PDF's own Notice (page 2) says it states FIRST's
   best-practice beliefs, "for informational purposes only", with no liability. The HTML
   page omits that Notice. Describe S098 as a **framework/catalogue**, never a
   requirement.
7. **Source typo to preserve** — L675 "the difference services"; quote verbatim.

## Commands actually run (receipts)

```
# capture (twice; identical digest) — lane instrument, --out into my seat dir
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/capture-source.py --id S098 \
  --url "https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1" \
  --out .ufo/waves/round-65/w1/ScoutS098/S098.candidate.txt --kind html
python3 corpus/instruments/capture-source.py --id S098b --url "<same>" \
  --out /fast/scratch/hyaku/kasegi-r65/ScoutS098/S098b.txt --kind html
sha256sum <both>   # identical: cfa42e2306546c5f418ccfc62db86f3c340ce31694028666abb46f2803b7a3c2

# raw-byte determinism across UAs
curl -sSL -A "kasegi-shokunin/1.0 ..." -o raw_ua.txt "<url>"      # 229255 bytes
curl -sSL -A "Mozilla/5.0 ..."        -o psirt_v11.html "<url>"   # 229255 bytes
cmp raw_ua.txt psirt_v11.html        # identical
sha256sum raw_ua.txt psirt_v11.html  # 3a1b5c1ac0583ff94ffdc82a8e25ce547d3c074255c5f3908944d5197a7aea11

# headers
curl -sSI "<url>"   # 200, text/html; charset=UTF-8, Last-Modified Mon, 26 Jan 2026 14:43:46 GMT,
                     # content-length 229255, Cache-Control public, max-age=3600

# cross-check PDFs
curl -sSL -o psirt_v11.pdf ".../FIRST_PSIRT_Services_Framework_v1.1.pdf"   # 2712956 bytes
pdfinfo psirt_v11.pdf    # 91 pages, CreationDate Tue Jan 19 16:56:29 2021 -03
pdftotext -layout psirt_v11.pdf psirt_v11_pdf.txt
pdftoppm -r 80 -f 1 -l 1 -png psirt_v11.pdf p1   # rendered the cover to confirm "Spring 2020"
curl -sSL -o mat.pdf ".../FIRST_PSIRT_Maturity_Document.pdf"  # 644190 bytes — the SEPARATE levels doc
pdftotext -layout mat.pdf mat.txt   # confirms Level 1/2/3 + "Beyond Level 3"

# quote verification (run from the seat directory)
cd .ufo/waves/round-65/w1/ScoutS098 && python3 - <<'PY'
import re
C='S098.candidate.txt'
lines=open(C,encoding='utf-8').read().split('\n')
def norm(s): return re.sub(r'\s+',' ',s).strip()
for rec in open('quotes_draft.txt',encoding='utf-8'):
    qid,ln,q=rec.rstrip('\n').split('|',2); ln=int(ln)
    t=norm(lines[ln-1]); qn=norm(q)
    assert qn in t and len(qn.split())<=25, qid
print('all quotes verify')
PY
# → all quotes verify: 28   (0 failures)

# scope screen
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for t in PSIRT FIRST maturity intake triage remediation disclosure "services framework" \
         "multi-party" multiparty SSVC EPSS CVD "CERT/CC"; do
  grep -rn --binary-files=without-match "$t" PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/knowledge/
  grep -rni --binary-files=without-match "$t" PROVINCE.md corpus/README.md corpus/SOURCES.md corpus/knowledge/
done
```

## Remaining unknowns for L1

1. Whether F44 should be admitted against the **HTML rendering** (no date) or whether the
   L1 wants a **separate PDF source** for the `Spring 2020` date and the printed
   `Version 1.1`. My recommendation: admit the HTML as S098 and describe its version
   evidence as `<title>` + Downloads list + HTTP `Last-Modified`; do not import the PDF's
   date. If the L1 wants the date, that is a second candidate source (S099?) at the PDF
   URL — **not** F44's scope.
2. Whether the maturity levels document should be admitted as its own row (it is a
   different FIRST artifact with a real level ladder) — out of my scope, but the scope
   screen shows `maturity` = 0 hits in the lane, so it would be new ground if wanted.
3. Whether SA1/SA2 titles should be quoted from the prose (L331) or the PDF TOC — my
   recommendation is prose-only, so the claim survives on this capture alone.
4. The figure PNGs are not pinned by the text capture; any claim about figure *content*
   needs the images captured as their own artifacts.

## Lane discipline

- Wrote only under `.ufo/waves/round-65/w1/ScoutS098/` and this report path.
- Read-only on `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`,
  `corpus/knowledge/*`. `corpus/instruments/capture-source.py` was **executed** (not
  modified) with `--out` inside my seat dir.
- No commit / push / mutating git or jj. No task or subagent dispatch (leaf seat).
- No package installed: `python3` 3.14.8 with `beautifulsoup4` 4.15.0, `pdftotext`,
  `pdftoppm` (poppler), `curl` were already present.
- Scratch `/fast/scratch/hyaku/kasegi-r65/ScoutS098/` held the raw HTML, the PDF
  cross-checks and the second capture; receipts were copied into the seat dir and the
  scratch was removed on exit.
