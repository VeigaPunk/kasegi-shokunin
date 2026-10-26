# ScribeEntryF21 — round-38 wave-1 receipt

seat: ScribeEntryF21 (scribe)
lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin at base a173b0c2b98c5ae39599fa9be76027fbbead0b9e (claims freeze 9a10b02fe411bb8d9d71aed3b1d3a5949d50d16b)
item: draft corpus/knowledge/csaf-vex-product-status-and-justifications.md (C2 / F21, source S055), delivered byte-exact beside this receipt
milestone: round-38 · judged on coverage · leaf seat, no subagent dispatch

## Behavior

Fetched the OASIS CSAF v2.0 OASIS Standard, normalized it with the lane's own `corpus/instruments/capture-source.py` (`html_to_text`), and wrote the complete knowledge entry against the normalized line numbers. The deliverable contains only landable bytes: H1, the three required header lines plus `ground:`, and the body (Attribution; what CSAF v2.0 is; seven claims; researcher use; overlap with F01/F18/F19/F20; falsifiable rule with FC-1..FC-6; eight rejected over-generalizations; honest limit). No validation blocks, notes or scaffolding sit inside it.

## Deliverable

- path this round: `.ufo/waves/round-38/wave1/ScribeEntryF21.entry.md`
- landing target (L1): `corpus/knowledge/csaf-vex-product-status-and-justifications.md`
- lines 137 · bytes 22887 · sha256 `0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a`
- header `source:` names `corpus/source-snapshots/round-38/S055.txt`, 5146 lines, 272,441 bytes, sha256 `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42`; header `recheck:` is one `cd`-prefixed command over the round-38 manifest with `--source S055`.

## Execution log (commands run, with their output)

Fetch (network rule: `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0`; status, bytes and UTC recorded):

```
$ S=/fast/scratch/hyaku/kasegi-r38/ScribeEntryF21; mkdir -p "$S" && cd "$S" && curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o S055.raw.html -w 'http_status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html; date -u +fetched_utc=%Y-%m-%dT%H:%M:%SZ
http_status=200 bytes=414858 url=https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
fetched_utc=2026-10-26T18:27:29Z
```

Normalization through the capture instrument's own function (no temporary files; every path under the seat scratch dir):

```
$ python3 -c "
import hashlib, importlib.util, sys
spec = importlib.util.spec_from_file_location('cap', '/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/capture-source.py')
cap = importlib.util.module_from_spec(spec); spec.loader.exec_module(cap)
raw = open('S055.raw.html','rb').read().decode('utf-8','replace')
text = cap.html_to_text(raw)
data = text.encode('utf-8')
open('S055.txt','wb').write(data)
print('snapshot_bytes=%d sha256=%s' % (len(data), hashlib.sha256(data).hexdigest()))
print('lines=%d' % text.count(chr(10)))
"
snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
lines=5146
$ wc -l S055.txt && sha256sum S055.txt
5146 S055.txt
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  S055.txt
```

Independent byte agreement with the capture seat (`ExecC2Capture`, fetched 2026-10-26T18:25:51Z from the same URL):

```
$ sha256sum <lane>/.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  ExecC2Capture.S055.txt
$ wc -l <lane>/.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt
5146
```

Quote verification over the delivered entry (every double-quoted string in the file must be a verbatim capture span, ≤25 words, with a resolving line anchor; the checker walks `anchor-2 .. anchor+4` on the normalized capture):

```
$ python3 verify.py <lane>/.ufo/waves/round-38/wave1/ScribeEntryF21.entry.md
spans 70 occ_all_1 False words_max 25 anchors_ok 70 of 70 bad 2
FAIL line 10 occ 2 words 13 anchor True refs [3, 4, 18, 1, 42, 44, 46, 53] | This specification is provided under the Non-Assertion Mode of the OASIS IPR Policy
FAIL line 87 occ 2 words 15 anchor True refs [1855, 1885, 1894, 2139] | which lists all products referenced later on in the CSAF document regardless of their state.
```

The two `FAIL` lines are the two non-unique spans and both anchors resolve (`anchor True`): the IPR-mode sentence occurs at L46 and L321, the `/product_tree` requirement at L2127 and L2139. QUALITY Q9 admits a non-unique quote when it carries a verified anchor, and the entry's FC-1 states both. Of the 68 distinct spans, 66 occur exactly once; the non-unique ones are `This specification is provided under the Non-Assertion Mode of the OASIS IPR Policy` at L46, `which lists all products referenced later on in the CSAF document regardless of their state.` at L2139.

Field counters used in the entry (matcher named in FC-2/FC-6):

```
$ for w in score scoring severity CVSS product_status known_not_affected known_affected under_investigation csaf_vex VEX EPSS KEV SSVC; do printf '%s=%s ' "$w" "$(grep -oF -- "$w" S055.txt | wc -l)"; done
score=101 scoring=2 severity=15 CVSS=73 product_status=79 known_not_affected=18 known_affected=21 under_investigation=12 csaf_vex=10 VEX=21 EPSS=0 KEV=0 SSVC=0
$ sed -n '1757,1761p' S055.txt
component_not_present
inline_mitigations_already_exist
vulnerable_code_cannot_be_controlled_by_adversary
vulnerable_code_not_in_execute_path
vulnerable_code_not_present
$ grep -n 'at least one of the elements fixed, known_affected' S055.txt | cut -c1-40; sed -n '2852p' S055.txt
2844:For each item in /vulnerabilities it MUST be tested that at least one of th
Example 82 which fails the test:
$ grep -n 'known_not_affected an impact statement' S055.txt | cut -c1-30; grep -n 'known_affected additional product specific information' S055.txt | cut -c1-30
2152:/vulnerabilities[]/product_status/known_not_affected an
2153:/vulnerabilities[]/product_status/known_affected additi
```

Recheck line checks:

```
$ grep -n '^recheck:' entry.draft.md | sed 's/^[0-9]*:recheck: //' > recheck.cmd && bash -n recheck.cmd
bash_syntax=ok
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && bash -e -c "$(cat recheck.cmd)"
manifest UNAVAILABLE reason=missing
exit=2
```

That is the pre-landing state (the round-38 manifest and capture are wave deliverables, not yet in the lane) and is the documented fail-closed path. With the capture seat's manifest and capture in a scratch directory shaped like `corpus/source-snapshots/round-38/`, the same instrument prints:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-38/manifest.json --source S055
S055:sha256 OK
S055:Q1 OK occurrences=1 anchor=2135-ok
S055:Q2 OK occurrences=1 anchor=2844-ok
S055:Q3 OK normalized=markup-whitespace occurrences=1 anchor=2151-ok
S055:Q4 OK occurrences=1 anchor=1767-ok
exit=0
```

## Quote verification table (quote, entry anchor, occurrences, words)

68 distinct quoted spans. Occurrences are whitespace-collapsed substring counts on the normalized capture `S055.txt` (sha256 `63c8ad52…e11cd42`); each anchor was checked to hold its quote in the capture, with the exact line preferred over a window.

| # | quote (verbatim, from the normalized capture) | entry anchor | occurrences | words |
|---|---|---|---|---|
| 1 | OASIS Standard 18 November 2022 | L3-L4 | 1 | 5 |
| 2 | the definitive reference for the language which supports creation, update, and interoperable exchange of security advisories as structured information | L42 | 1 | 19 |
| 3 | This document was last revised or approved by the membership of OASIS on the above date. | L44 | 1 | 16 |
| 4 | This specification is provided under the Non-Assertion Mode of the OASIS IPR Policy | L46 | 2 | 13 |
| 5 | Copyright © OASIS Open 2022. All Rights Reserved. | L53 | 1 | 8 |
| 6 | All examples in this document are informative only. | L498 | 1 | 8 |
| 7 | Local or private profiles MAY exist and tools MAY choose to support them. | L2075 | 1 | 13 |
| 8 | The Common Security Advisory Framework (CSAF) is a language to exchange Security Advisories formulated in JSON. | L502 | 1 | 16 |
| 9 | This prose specification is one component of a Work Product that also includes: | L27 | 1 | 13 |
| 10 | This specification replaces or supersedes: | L35 | 1 | 5 |
| 11 | Each CSAF document MUST conform the CSAF Base profile. | L2070 | 1 | 9 |
| 12 | A profile can always add, but never subtract nor overwrite requirements defined in the profile it extends. | L2071 | 1 | 17 |
| 13 | To ensure a common understanding of which fields are required in a given use case the standard defines profiles. | L2069 | 1 | 19 |
| 14 | The value of /document/category SHALL be csaf_vex. | L2156 | 1 | 7 |
| 15 | Values of /document/category starting with csaf_ are reserved for existing, upcoming and future profiles defined in the CSAF standard. | L2073 | 1 | 19 |
| 16 | The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability. | L2135 | 1 | 24 |
| 17 | enables a supplier or other party to assert whether or not a particular product is affected by a specific vulnerability | L394 | 1 | 20 |
| 18 | For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status. | L2844 | 1 | 25 |
| 19 | contains different lists of product_ids which provide details on the status of the referenced product related to the current vulnerability. | L1855 | 1 | 20 |
| 20 | The eight defined properties are First affected (first_affected), First fixed (first_fixed), Fixed (fixed), Known affected (known_affected) | L1855 | 1 | 16 |
| 21 | None of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status. | L2861 | 1 | 13 |
| 22 | Fixed (fixed) of value type Products (products_t) represents that these versions contain a fix for the vulnerability but may not be the recommended fixed versions. | L1887 | 1 | 25 |
| 23 | Known affected (known_affected) of value type Products (products_t) represents that these versions are known to be affected by the vulnerability. | L1888 | 1 | 20 |
| 24 | Known not affected (known_not_affected) of value type Products (products_t) represents that these versions are known not to be affected by the vulnerability. | L1890 | 1 | 22 |
| 25 | Under investigation (under_investigation) of value type Products (products_t) represents that it is not known yet whether these versions are or are not affected | L1894 | 1 | 23 |
| 26 | No remediation is required regarding this vulnerability. | L1890 | 1 | 7 |
| 27 | For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats. | L2151-L2152 | 1 | 23 |
| 28 | the details field SHALL contain a a description why the vulnerability cannot be exploited. | L2152 | 1 | 14 |
| 29 | it MUST be tested that a corresponding impact statement exist in /vulnerabilities[]/flags or /vulnerabilities[]/threats | L2877 | 1 | 14 |
| 30 | The value impact indicates that the details field contains an assessment of the impact on the user or the target set | L2060 | 1 | 21 |
| 31 | or a description why it cannot be exploited. | L2060 | 1 | 8 |
| 32 | contains product specific information in regard to this vulnerability as a single machine readable flag. | L1737 | 1 | 15 |
| 33 | These flags enable the receiving party to automate the selection of actions to take. | L1738 | 1 | 14 |
| 34 | The given values reflect the VEX not affected justifications. | L1762 | 1 | 9 |
| 35 | additional product specific information SHALL be provided in /vulnerabilities[]/remediations as an action statement. | L2153 | 1 | 13 |
| 36 | it MUST be tested that a corresponding action statement exist in /vulnerabilities[]/remediations | L2933 | 1 | 12 |
| 37 | The use of the categories no_fix_planned and none_available for an action statement is permitted. | L2154 | 1 | 14 |
| 38 | Actions are recommended to remediate or address this vulnerability. | L1888 | 1 | 9 |
| 39 | The software is not affected because the vulnerable component is not in the product. | L1763 | 1 | 14 |
| 40 | The product is not affected because the code underlying the vulnerability is not present in the product. | L1764 | 1 | 17 |
| 41 | vulnerable code is used in such a way that an attacker cannot mount any anticipated attack. | L1766 | 1 | 16 |
| 42 | The affected code is not reachable through the execution of the code, including non-anticipated states of the product. | L1767 | 1 | 18 |
| 43 | Built-in inline controls or mitigations prevent an adversary from leveraging the vulnerability. | L1769 | 1 | 12 |
| 44 | the component in question is present, but for whatever reason (e.g. compiler options) the specific code causing the vulnerability is not present | L1765 | 1 | 22 |
| 45 | including non-anticipated states of the product | L1767 | 1 | 6 |
| 46 | Components that are neither used nor executed by the product. | L1768 | 1 | 10 |
| 47 | it MUST be tested that a Product is not member of more than one Flag item with a VEX justification code | L3096 | 1 | 21 |
| 48 | Additional flags with a different purpose might be provided in later versions of CSAF. | L3097 | 1 | 14 |
| 49 | for each Product ID the required information according to its product status as stated in the two points above is available | L2155 | 1 | 21 |
| 50 | all products with the status known_not_affected MUST have an impact statement | L2155 | 1 | 11 |
| 51 | the use of JSON schema allows validation and proof of model conformance | L510 | 1 | 12 |
| 52 | Consistency on the content level thus is in the responsibility of the producer of such documents | L515 | 1 | 16 |
| 53 | any deep validation on a semantic level (e.g. does the CWE match the described vulnerability) is to be ensured by the producer | L516 | 1 | 22 |
| 54 | It is out of scope for this specification. | L516 | 1 | 8 |
| 55 | which lists all products referenced later on in the CSAF document regardless of their state. | L2139 | 2 | 15 |
| 56 | especially helpful in efficiently consuming SBOM data | L394 | 1 | 7 |
| 57 | non-anticipated states of the product | L1767 | 1 | 5 |
| 58 | Delegation to industry best practices technologies | L518 | 1 | 6 |
| 59 | Common Vulnerability Scoring System (CVSS) Version 3.1 [CVSS31] | L522 | 1 | 8 |
| 60 | abiding by the schema at https://www.first.org/cvss/cvss-v2.0.json. | L2026 | 1 | 6 |
| 61 | A score object SHOULD reflect the associated product's status | L2028 | 1 | 9 |
| 62 | The range of values in this field is defined according to the document producer's policies and procedures. | L1233 | 1 | 17 |
| 63 | It is a document-level metric and applied to the document as a whole — not any specific vulnerability. | L1233 | 1 | 18 |
| 64 | provides a severity which is independent of - and in addition to - any other standard metric | L1246 | 1 | 17 |
| 65 | The value exploit_status indicates that the details field contains a description of the degree to which an exploit for the vulnerability is known. | L2059 | 1 | 23 |
| 66 | known not to be affected by the vulnerability | L1890 | 1 | 8 |
| 67 | contains different lists of product_ids which provide details on the status of the referenced product | L1855 | 1 | 15 |
| 68 | possible later revisions of this document | L44 | 1 | 6 |

## QUALITY Q1-Q6 self-check

| id | how this entry satisfies it |
|---|---|
| Q1 | Three header lines directly under the H1: `source:` (S055, the OASIS URL, the capture path with line/byte/sha256 and an exact line index), `verified-at: 2026-10-26` with the fetch instant, `recheck:` one runnable `cd`-prefixed command (plus `ground: F21`). |
| Q2 | Every claim rests on S055, a tier-A OASIS Standard opened this round (2026-10-26); no other row is sole support. |
| Q3 | Each load-bearing statement carries a verbatim quote ≤25 words with its line number; numbers (`73`, `0`, `15`, line ids) come from the commands above, not from memory. |
| Q4 | Attribution kept: the document is the OASIS CSAF TC's standard, cited by its own stage/date/IPR/copyright lines; a vendor's VEX is stated as that vendor's assertion (L394, L516), never generalized into a rule about vendors or programs. |
| Q5 | Seven-branch falsifiable rule plus eight rejected over-generalizations, each with its reason and line evidence. |
| Q6 | Documentation only: no probing/scanning/login/submission instruction, no credential, session or private URL, no vault-reference URI; the front matter's two personal e-mail addresses are not quoted. |

## Findings

1. The capture is reproducible from the public host on this date: two independent fetches (18:25:51Z and 18:27:29Z) normalized to identical bytes `63c8ad52…e11cd42`, so the entry's anchors and the manifest's pins sit on one normalization.
2. The VEX profile's requirement sentences split across normalized lines (`For each item in` on L2151, the status path on L2152/L2153). Any entry quoting them depends on the declared whitespace normalization — the peer manifest's Q3 records exactly `normalized=markup-whitespace`, and the entry discloses the split in its honest limit.
3. CSAF delegates scoring to CVSS (73 `CVSS` occurrences; schema references L521-L527) and never mentions EPSS, KEV or SSVC (0 each); its own `aggregate_severity` has a producer-defined value range (L1233). The entry states the neighbour-axis difference as that lexical fact plus lane analysis, not as a CSAF claim.
4. The standard checks presence, not truth: schema validation proves model conformance (L510) while semantic validation is "out of scope for this specification" (L516) — the sentence that governs how a `known_not_affected` flag may be used.

## Touched surfaces

- Written: `.ufo/waves/round-38/wave1/ScribeEntryF21.entry.md` (deliverable) and `.ufo/waves/round-38/wave1/ScribeEntryF21.md` (this receipt).
- Scratch: `/fast/scratch/hyaku/kasegi-r38/ScribeEntryF21/` — removed with `rm -rf` after both files were copied into the wave dir (no scratch survives).
- Read-only: `corpus/QUALITY.md`, `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md`, `corpus/knowledge/epss-exploit-prediction-scoring.md`, `corpus/knowledge/cisa-kev-catalog.md`, `corpus/README.md`, `corpus/instruments/capture-source.py`, `corpus/instruments/source-recheck.py`, `.ufo/waves/round-38/claims.json`, the peer capture/manifest in `wave1/`.
- Not edited: any lane source, the registry, the frontier table, the capture, the manifest, any other seat's deliverable.

## Out of scope (other seats own these)

- The `corpus/SOURCES.md` S055 row and the F21 frontier row; `corpus/source-snapshots/round-38/S055.txt` + `manifest.json`; harness, binding, recheck-audit, census and junk-twin checks; landing the entry.

## Known limits

- The entry is not landed by this seat. Until the L1 lands it at `corpus/knowledge/csaf-vex-product-status-and-justifications.md` and the capture/manifest land, the entry's own `recheck:` exits 2 (`manifest UNAVAILABLE reason=missing`, measured) and the registry census stays red for S055 — published fail-closed behavior, not a pass.
- Quote verification is a pinned-capture comparison against `63c8ad52…`; it is not a fresh network verification, and a later stage of the document is a new pin.
- The capture is the prose specification only; the three JSON schema artifacts (L28-L33) are not in it, so the entry quotes prose-level type/enum statements and says so.

## Tooling

None installed or upgraded this seat; pacman unused. Work used only `python3`, `curl`, `grep`, `sed`, `awk`, `cp`, `wc`, `sha256sum` already on the host.

## Appendix A — the quote verifier used above (replayable)

Run from a directory holding the normalized capture as `S055.txt`; it takes the entry path as `$1`. It extracts every double-quoted string in the entry, counts it on the whitespace-collapsed capture, counts its words, and checks that the declared `L<n>` (or `L<n>-L<m>`) reference, plus the two lines before and four after, contains the quote.

```
import re, sys
cap = open('S055.txt', encoding='utf-8').read()
lines = cap.split('\n')
if lines and lines[-1] == '': lines = lines[:-1]
norm = lambda t: ' '.join(t.split())
ncap = norm(cap)
entry = open(sys.argv[1] if len(sys.argv)>1 else 'entry.draft.md', encoding='utf-8').read().split('\n')
rows=[]; bad=0
for i, line in enumerate(entry, 1):
    quotes = re.findall(r'"([^"]+)"', line)
    if not quotes: continue
    refs = [int(x) for x in re.findall(r'L(\d+)', line)]
    for q in quotes:
        occ = ncap.count(norm(q))
        words = len(norm(q).split())
        anchor_ok = None
        if refs:
            anchor_ok = False
            for n in refs:
                if n < 1 or n > len(lines): continue
                win = norm(' '.join(lines[max(0,n-2):n+4]))
                if norm(q) in win: anchor_ok = True; break
            # blockquote spans e.g. L2151-L2152
            m = re.search(r'L(\d+)-L(\d+)', line)
            if m and not anchor_ok:
                a,b=int(m.group(1)),int(m.group(2))
                win = norm(' '.join(lines[max(0,a-1):b+4]))
                if norm(q) in win: anchor_ok = True
        rows.append((i, occ, words, anchor_ok, refs, q))
        if occ != 1 or words > 25 or anchor_ok is False: bad += 1
print('spans', len(rows), 'occ_all_1', all(r[1]==1 for r in rows), 'words_max', max(r[2] for r in rows),
      'anchors_ok', sum(1 for r in rows if r[3]), 'of', len(rows), 'bad', bad)
for r in rows:
    if r[1]!=1 or r[2]>25 or r[3] is False:
        print('FAIL line', r[0], 'occ', r[1], 'words', r[2], 'anchor', r[3], 'refs', r[4], '|', r[5][:120])
```
