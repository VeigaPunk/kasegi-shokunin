# ExecFrontierLeads — round 39 next-frontier leads (read-only probes)

Seat: `ExecFrontierLeads` (leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Axes served: `coverage` (three unopened leads with measured access/scoping facts) and
`depth:verifiability` (every lead carries status, bytes, sha256 and the exact line numbers of
the sentence it rests on). No lane file other than this receipt and the deliverable was written.

Scratch: `S=/fast/scratch/hyaku/kasegi-r39/ExecFrontierLeads` (created `mkdir -p`, all work
copies under `$S`, removed at the end of this seat).

Disk guard before any fetch was green (`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`):

```
root                             use%     free
/tmp                               3%   125.2G
/var/tmp                          35%   585.6G
/fast/scratch/hyaku               25%   609.5G
```

## Deliverable

`.ufo/waves/round-39/wave1/ExecFrontierLeads.leads.md` — 3 lines, 4264 bytes,
sha256 `eefeeadf94a9b001d9d99292f2fae28a4b962cfdc9421efbffb990a0ca211b76`.
Landable bytes only (three `- ` bullets, no heading, no fence, no tables); appends under the
existing `## Leads (unopened)` section (`corpus/SOURCES.md` L87-L92, whose current last bullet
is L91). Each bullet is one line, matching the section's existing one-line shape.

## Probes and actual output

### Lead 1 — CISA VEX Status Justifications (June 2022)

```
URL=https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf
TLD=2026-10-26T19:30:41Z
curl=200 313386
fetched_utc=2026-10-26T19:30:41Z
9a4027c68674a99678bfd18d0897cdb213a2db59b568054b2b86439ff0cf513f  vex-justification.pdf
vex-justification.pdf: PDF document, version 1.7 (zip deflate encoded)
Title:           Vulnerability Exploitability eXchange (VEX) - Status Justifications
Author:          VEX Working Group
CreationDate:    Thu Jun 30 13:23:33 2022 -03
ModDate:         Tue Jul 12 18:09:12 2022 -03
Pages:           13
File size:       313386 bytes
```

Text extraction (`pdftotext -layout`), then label list and per-label sections:

```
  273 14678 vex-justification.txt
2b480ac832a62cf96bba44670dcdac8089f995d5cf6149b499cbcf00cf8df4e6  vex-justification.txt
3|Publication date: June 2022
50|Here is a list of the NOT AFFECTED status justifications:
51|   ● Component_not_present
52|   ● Vulnerable_code_not_present
53|   ● Vulnerable_code_cannot_be_controlled_by_adversary
54|   ● Vulnerable_code_not_in_execute_path
55|   ● Inline_mitigations_already_exist
101|3.3 Component_not_present
121|3.4 Vulnerable_code_not_present
138|3.5 Vulnerable_code_not_in_execute_path
160|3.6 Vulnerable_code_cannot_be_controlled_by_adversary
181|3.7 Inline_mitigations_already_exist
```

Five labels confirmed, and the PDF spells them Title_Case. The citing texts were checked so the
lead does not assert an unverified citation chain:

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o cisa-min-req.pdf -w 'status=%{http_code} bytes=%{size_download}\n' \
    https://www.cisa.gov/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf
status=200 bytes=1047967
1e73325c674aa55c5665e3d2b647201acc46ee1fa9c8ee8bf88e4ff044f975c8  cisa-min-req.pdf
435:[justification] MUST be one of the following values, described further in the previous publication,
436:Vulnerability Exploitability eXchange (VEX) - Status Justifications. 12
446:12 https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf
```

The PDF link was found on that page as `href="/sites/default/files/2023-04/minimum-requirements-for-vex-508c.pdf"`.

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o openvex-spec.md -w 'status=%{http_code} bytes=%{size_download}\n' \
    https://raw.githubusercontent.com/openvex/spec/main/OPENVEX-SPEC.md
status=200 bytes=30580
9375415ccb351260a998864cbeebbaff1808d1b09a306919b79cc75e5519f884  openvex-spec.md
368:... was defined by the VEX Working Group and published in the
369:... [Status Justifications] document on July 2022.
373:| `component_not_present` | ...
374:| `vulnerable_code_not_present` | ...
375:| `vulnerable_code_not_in_execute_path` | ...
376:| `vulnerable_code_cannot_be_controlled_by_adversary` | ...
377:| `inline_mitigations_already_exist` | ...
671:[Status Justifications]: https://www.cisa.gov/sites/default/files/publications/VEX_Status_Justification_Jun22.pdf
```

Line-number caveat recorded in the deliverable: L51-L55 are Title_Case display names; the wire
values are lower_snake_case (OpenVEX L373-L377; the CSAF S055 row already in the registry).

### Lead 2 — CSAF v2.1 standard status

```
URL=https://docs.oasis-open.org/csaf/csaf/v2.1/os/
status=404 bytes=41334 eff=https://docs.oasis-open.org/csaf/csaf/v2.1/os/
URL=https://docs.oasis-open.org/csaf/csaf/v2.1/
status=200 bytes=1097 eff=https://docs.oasis-open.org/csaf/csaf/v2.1/
fetched_utc=2026-10-26T19:30:41Z
e416b40032482d96f55c61e3ce3dd871e980c9ff5b4bfa2f89d1c2863fcfd731  csaf-12fa405e.out   (/v2.1/os/ body, <title>Not found &middot; docs.oasis-open.org</title>)
5e59949c479ca03097be81259cb5bf168a857562991c73be3c826e7822f03775  csaf-4747cc6d.out   (/v2.1/ body)
```

`/csaf/csaf/v2.1/` body:

```
<a href="csaf-v2.1.html">                                             21-Oct-2026 17:00        1M
<a href="csaf-v2.1.md">                                               21-Oct-2026 17:00      835K
<a href="csaf-v2.1.pdf">                                              21-Oct-2026 17:00        4M
<a href="csd01/">                                                     28-May-2025 17:00       -
<a href="csd02/">                                                     25-Feb-2026 17:00       -
<a href="csd03/">                                                     11-Sep-2026 17:00       -
<a href="csd04/">                                                     21-Oct-2026 17:00       -
<a href="schema/">                                                    21-Oct-2026 17:00       -
```

Root v2.1 document fetched and its status heading located:

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o csaf-v2.1.html -w 'status=%{http_code} bytes=%{size_download} ctype=%{content_type}\n' \
    https://docs.oasis-open.org/csaf/csaf/v2.1/csaf-v2.1.html
status=200 bytes=1231332 ctype=text/html
fdb4bf015c75f01269c1ba346912fd558e8a168b607279b951b1fe5335f366b0  csaf-v2.1.html
423:<h1 id="common-security-advisory-framework-version-2.1">Common Security Advisory Framework Version 2.1 ...
424:<h2 id="committee-specification-draft-04">Committee Specification Draft 04 ...
425:<h2 id="october-2026">21 October 2026 ...
```

`csd04/` listing (status 200, 1220 bytes, sha256 `749f9beef04b3a884f828fb7268859ceccf5c3418fd8f4cd0b2ae24d0046f161`)
holds `csaf-v2.1-csd04.html|.md|.pdf|.zip`, `csaf-v2.1-csd04-public-review-metadata.html` and
`manifest.json` — i.e. a draft under public review, not a standard. So there is no OASIS
Standard at v2.1, `/os/` is 404, and the flip condition written into the lead is
"`/csaf/csaf/v2.1/os/` resolves and lists `csaf-v2.1-os.html`". S055 (v2.0 OS) stays the
citable versioned standard.

### Lead 3 — CycloneDX v1.7 analysis-subtree scoping cost

Page measurement:

```
$ curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o cdx17.json.html -w 'status=%{http_code} bytes=%{size_download} ctype=%{content_type} eff=%{url_effective}\n' \
    https://cyclonedx.org/docs/1.7/json/
status=200 bytes=6419901 ctype=text/html; charset=utf-8 eff=https://cyclonedx.org/docs/1.7/json/
fetched_utc=2026-10-26T19:30:42Z
52e9fd86f14b84d11918fdca43ff092674f26d2a2f76ed87566cc786e7bd9b3c  cdx17.json.html
    897 6419901 cdx17.json.html
```

6.42 MB in 897 lines of minified HTML: a rendered accordion reference, not a schema file. The
`analysis` subtree exposes stable enum anchors:

```
id="vulnerabilities_items_analysis"
id="vulnerabilities_items_analysis_state_enum"
id="vulnerabilities_items_analysis_justification_enum"
id="vulnerabilities_items_analysis_response_items_enum"
```

Scoped extraction run on the scratch copy (script is 43 lines of stdlib only; `time python3
cdx-scope.py cdx17.json.html cdx-analysis-scope.json`):

```
input_bytes=6419901
state: 6 values -> resolved, resolved_with_pedigree, exploitable, in_triage, false_positive, not_affected
justification: 9 values -> code_not_present, code_not_reachable, requires_configuration, requires_dependency, requires_environment, protected_by_compiler, protected_at_runtime, protected_at_perimeter, protected_by_mitigating_control
response: 5 values -> can_not_fix, will_not_fix, update, rollback, workaround_available
output_bytes=2630 output_lines=91

real	0m0.021s
exit=0
c373862ac342828f725d9e680c81de5035f0cb9059e9360e0c00607641562592  cdx-analysis-scope.json
b8d8a5435d7860677c350c39d9b0b1eacf7ac3da433b974d026ab07e308dba9e  cdx-scope.py
```

Extractor, for reproduction (scratch copy is removed with the scratch dir):

```python
#!/usr/bin/env python3
"""Scoped extraction of the CycloneDX 1.7 JSON `vulnerabilities[].analysis` enums
from the rendered reference page, without loading a JSON-schema parser.

usage: cdx-scope.py <cdx17.json.html> <out.json>
"""
import html
import json
import re
import sys

SRC = sys.argv[1]
OUT = sys.argv[2]

doc = open(SRC, encoding="utf-8", errors="replace").read()
fields = {
    "state": "vulnerabilities_items_analysis_state_enum",
    "justification": "vulnerabilities_items_analysis_justification_enum",
    "response": "vulnerabilities_items_analysis_response_items_enum",
}
result = {"source_bytes": len(doc.encode()), "analysis": {}}
for name, anchor in fields.items():
    at = doc.find(f'id="{anchor}"')
    if at < 0:
        raise SystemExit(f"anchor not found: {anchor}")
    start = doc.index("<table", at)
    end = doc.index("</table>", start)
    table = doc[start:end]
    rows = re.findall(
        r'<td class="text-nowrap"><strong>"([^"]+)"</strong></td><td><p>(.*?)</p></td>',
        table,
        re.S,
    )
    result["analysis"][name] = [
        {"value": v, "description": html.unescape(re.sub(r"<[^>]+>", "", d))}
        for v, d in rows
    ]
blob = json.dumps(result, indent=1, ensure_ascii=False) + "\n"
open(OUT, "w", encoding="utf-8").write(blob)
print(f"input_bytes={result['source_bytes']}")
for k, v in result["analysis"].items():
    print(f"{k}: {len(v)} values -> " + ", ".join(x["value"] for x in v))
print(f"output_bytes={len(blob.encode())} output_lines={blob.count(chr(10))}")
```

Result: the whole 6.42 MB page need not be carried into a capture or parsed as JSON; the three
enums cost 2,630 bytes. The lead states this as method ground only — the extraction is
anchor-based and must be re-run and re-hashed if the rendered markup changes.

## Write scope and hygiene

- Writes: `$S` (fetch bodies, `pdftotext` output, extractor, extraction output) and the two lane
  paths — `.ufo/waves/round-39/wave1/ExecFrontierLeads.leads.md` and this receipt. No other file
  touched; no `git` mutation (read-only `git log`/`git status` only, to confirm the lane state).
- No tool installed or upgraded this seat (system `curl`, `pdftotext`, `pdfinfo`, `python3` were
  sufficient); no `pacman` transaction.
- `$S` removed after the deliverable and this receipt were written.

## Risks

- Lead 1: the PDF's label names are Title_Case; using them as wire values would be wrong. Flagged
  in the bullet. Per-label section text (L101-L205) was not mined, only located.
- Lead 2: the v2.1 root document is dated 21 October 2026 and is CSD04; that is a dated snapshot.
  Another csd may land before any `/os/` publication, and only the `/os/` check is the flip.
- Lead 3: the CycloneDX page is rendered HTML with positional accordion ids; the 43-line
  extractor depends on `id="vulnerabilities_items_analysis_*_enum"` anchors and the table markup,
  so a site build change silently breaks it (the script exits non-zero on a missing anchor, which
  is the intended failure mode).
- All three bullets cite measurements taken 2026-10-26 (UTC 19:30-19:31); the lane's existing
  leads style is prose-only, so these are longer than L89-L91. They remain single-line bullets.
