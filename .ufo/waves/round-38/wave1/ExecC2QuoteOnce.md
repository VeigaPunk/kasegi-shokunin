# ExecC2QuoteOnce — round-38 wave-1 receipt (receipt only; no lane file lands from this seat)

Item: independently fetch the CSAF v2.0 OASIS Standard, normalize it with
`corpus/instruments/capture-source.py`, and pin 8–10 candidate quotes for the F21 knowledge
entry (`corpus/knowledge/csaf-vex-product-status-and-justifications.md`, `source: S055`) with
exact text, normalized-line number, occurrence count and word count; flag every quote that
occurs more than once and give the disambiguating anchor.

## 1. Fetch record (two clients, four fetches)

| # | client | command | HTTP | fetched bytes | raw sha256 | UTC |
|---|---|---|---|---|---|---|
| F1 | curl | `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o csaf-raw.html -w 'http_status=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` | 200 | 414858 | `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b` | 2026-10-26T18:27:16Z |
| F2 | capture-source.py (urllib) | `python3 corpus/instruments/capture-source.py --id S055 --url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html --out $S/S055.txt --kind html` | 200 | 415225 | `0fbc5857a66dabe57568c305c19d1bcf4e633c1872ac37f50405864d62d339ba` | 2026-10-26T18:27:31Z |
| F3 | capture-source.py, repeat | same as F2, `--out $S/S055.r2.txt` | 200 | 415225 | `0fbc5857…d339ba` | 2026-10-26T18:29:04Z |
| F4 | curl, repeat | same as F1, `-o csaf-raw2.html` | 200 | 414858 | `fad0c60d…20cd66b` | 2026-10-26T18:29:12Z |

F1 output verbatim:

```
2026-10-26T18:27:16Z
http_status=200 bytes=414858 url=https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html
2026-10-26T18:27:16Z
fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b  csaf-raw.html
csaf-raw.html: HTML document, Unicode text, UTF-8 text, with very long lines (1100), with CRLF line terminators
```

F2/F3 output verbatim:

```
S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:27:31Z out=/fast/scratch/hyaku/kasegi-r38/ExecC2QuoteOnce/S055.txt
S055 status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:29:04Z out=/fast/scratch/hyaku/kasegi-r38/ExecC2QuoteOnce/S055.r2.txt
```

Relevant response headers (F4, `curl -D -`): `HTTP/2 200`, `content-type: text/html`,
`last-modified: Sun, 05 Apr 2026 13:17:09 GMT`, `server: cloudflare`, `vary: Accept-Encoding`,
`content-length` absent. No redirect (requested URL == `%{url_effective}`).

### Client variance, and why it does not move the snapshot

The two clients return different raw bodies (414858 vs 415225 bytes, Δ=367) while producing
**byte-identical normalized text**. First differing byte, F1 vs F2:

```
len a 414858 len b 415225 cr a 6411 cr b 6411 lf a 6411 lf b 6412
first diff at byte 414841
a ctx: ...<li><code>/vulnerabilities[]/threats[]/date</code></li>\r\n</ul>\r\n</body>\r\n</html>\r\n
b ctx: ...<li><code>/vulnerabilities[]/threats[]/date</code></li>\r\n</ul>\r\n<script type="module" src="https://static.cloudflareinsights.com/beacon.min.js/...
```

The whole 367-byte delta is the Cloudflare insights `<script type="module" …beacon.min.js…>`
block, which `capture-source.py` removes with `SCRIPT_RE` before tag stripping. Cross-check that
the F1 (curl) body normalizes to the same snapshot:

```
python3 (import capture-source.py as module, html_to_text(open('csaf-raw.html').read()))
curl-raw normalized sha: 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
instrument snapshot sha: 63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
equal: True
```

Determinism (F2 vs F3): `cmp -s S055.txt S055.r2.txt` → `deterministic: identical`.

## 2. Normalized snapshot this receipt's line numbers refer to

| field | value |
|---|---|
| intended committed path | `corpus/source-snapshots/round-38/S055.txt` |
| lines / bytes | 5146 / 272441 |
| sha256 | `63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42` |
| normalized-by | `corpus/instruments/capture-source.py` → `html_to_text()` (script/style removed, block tags → newlines, remaining tags stripped, `html.unescape`, space/tab/NBSP runs collapsed, blank lines dropped, UTF-8, final newline) |
| sibling cross-check | `.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt` `sha256sum` = `63c8ad5271…e11cd42`, 5146 lines, 272441 bytes; `cmp` vs my independent capture → `IDENTICAL to my independent capture` |

Boundary: every line number and occurrence count below is valid only while the committed
snapshot keeps that sha256. If the capture seat commits different bytes, re-run §5 first.

## 3. DELIVERABLE — F21 quote pins

`## DELIVERABLE`

```text
F21 / S055 quote pins — OASIS CSAF v2.0 (OASIS Standard, 18 November 2022)
snapshot corpus/source-snapshots/round-38/S055.txt  lines=5146  bytes=272441  sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42
url https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html  http=200  fetched=2026-10-26T18:27:31Z
norm line = 1-based line in the normalized snapshot; occ = count of the exact text over the whole
snapshot; words = whitespace-separated tokens (a /vulnerabilities[]/… path is one token);
\n inside a quote is one newline byte (the quote spans normalized lines).

| id | pins | exact text | norm line | occ | words | anchor |
|---|---|---|---|---|---|---|
| Q1 | VEX profile purpose | `The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability.` | 2135 | 1 | 24 | `4.5 Profile 5: VEX` (heading L2134); second sentence of L2135 |
| Q2 | required product_status categories in VEX | `at least one of` ⏎ `/vulnerabilities[]/product_status/fixed` ⏎ `/vulnerabilities[]/product_status/known_affected` ⏎ `/vulnerabilities[]/product_status/known_not_affected` ⏎ `/vulnerabilities[]/product_status/under_investigation` | 2141–2145 | 1 | 8 | `4.5 Profile 5: VEX` (heading L2134), requirement list opened by L2137 `The following elements MUST exist and be valid:` |
| Q3 | impact statement requirement for known_not_affected | `For each item in` ⏎ `/vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats.` | 2151–2152 | 1 | 23 | `4.5 Profile 5: VEX` (heading L2134); the `For each item in` keyword closes L2151, its object opens L2152 |
| Q4 | action statement requirement for known_affected | `/vulnerabilities[]/product_status/known_affected additional product specific information SHALL be provided in /vulnerabilities[]/remediations as an action statement.` | 2153 | 1 | 14 | `4.5 Profile 5: VEX` (heading L2134); L2153 is the object of the shared `For each item in` keyword on L2151 |
| Q5 | product_status group names | `The eight defined properties are First affected (first_affected), First fixed (first_fixed), Fixed (fixed), Known affected (known_affected), Known not affected (known_not_affected)` | 1855 | 1 | 20 | `3.2.3.9 Vulnerabilities Property - Product Status` (heading L1854); window stops before `Last affected` — see remainder below |
| Q6 | flag definition: component_not_present | `component_not_present: The software is not affected because the vulnerable component is not in the product.` | 1763 | 1 | 15 | `3.2.3.5 Vulnerabilities Property - Flags` (heading L1729); definition list introduced by L1762 `… The values MUST be used as follows:` |
| Q7 | flag definition: vulnerable_code_not_present | `vulnerable_code_not_present: The product is not affected because the code underlying the vulnerability is not present in the product.` | 1764 | 1 | 18 | same; contrast sentence for this label is L1765 (`Unlike component_not_present, …`) |
| Q8 | flag definition: vulnerable_code_cannot_be_controlled_by_adversary | `vulnerable_code_cannot_be_controlled_by_adversary: The vulnerable component is present, and the component contains the vulnerable code.` | 1766 | 1 | 13 | same; second sentence of L1766 (`However, vulnerable code is used in such a way that an attacker cannot mount any anticipated attack.`) omitted to stay ≤25 words |
| Q9 | flag definition: vulnerable_code_not_in_execute_path | `vulnerable_code_not_in_execute_path: The affected code is not reachable through the execution of the code, including non-anticipated states of the product.` | 1767 | 1 | 19 | same; following note line is L1768 `Components that are neither used nor executed by the product.` |
| Q10 | flag definition: inline_mitigations_already_exist | `inline_mitigations_already_exist: Built-in inline controls or mitigations prevent an adversary from leveraging the vulnerability.` | 1769 | 1 | 13 | same; last item of the definition list (L1763–L1769) |

Multi-line quotes, verbatim (exact bytes, one normalized line per row; ⏎ above = one newline):

Q2, lines 2141–2145, occ=1:
at least one of
/vulnerabilities[]/product_status/fixed
/vulnerabilities[]/product_status/known_affected
/vulnerabilities[]/product_status/known_not_affected
/vulnerabilities[]/product_status/under_investigation

Q3, lines 2151–2152, occ=1:
For each item in
/vulnerabilities[]/product_status/known_not_affected an impact statement SHALL exist as machine readable flag in /vulnerabilities[]/flags or as human readable justification in /vulnerabilities[]/threats.

Q5 remainder, same normalized line 1855 (does not occur anywhere else as a line substring):
Last affected (last_affected), Recommended (recommended), and Under investigation (under_investigation) are all of value type Products (products_t).

Duplicate / near-duplicate map (nothing in the table above occurs more than once; these are the
forms that DO collide, with the anchor that disambiguates):

| colliding form | occ | normalized lines | disambiguating anchor |
|---|---|---|---|
| `component_not_present` | 5 | 1757, 1763, 1765, 3091, 3127 | definition is the occurrence followed by `: The software is not affected because the vulnerable component is not in the product.` (L1763); 1757 is the enum list, 1765 the `Unlike component_not_present, …` contrast, 3091/3127 are JSON example `label` values |
| `inline_mitigations_already_exist` | 2 | 1758, 1769 | definition is L1769 (followed by `: Built-in inline controls…`); 1758 is the enum list |
| `vulnerable_code_cannot_be_controlled_by_adversary` | 3 | 1759, 1766, 3133 | definition is L1766; 1759 enum, 3133 JSON example |
| `vulnerable_code_not_in_execute_path` | 2 | 1760, 1767 | definition is L1767; 1760 enum |
| `vulnerable_code_not_present` | 2 | 1761, 1764 | definition is L1764; 1761 enum |
| `at least one of` (lead-in alone) | 7 | — | not usable alone; Q2 is unique only as the whole five-line block (verified occ=1) |
| four product_status paths without the lead-in | 2 | 2142–2145, 2848–2851 | keep the L2141 `at least one of` lead-in (Q2); L2848 sits in the `6.1.27.7 VEX Product Status` test list |
| VEX product-status requirement, prose restatement | 1 | 2844 | `For each item in /vulnerabilities it MUST be tested that at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status.` (25 words, occ=1, §`6.1.27.7 VEX Product Status` heading L2843) — cite this only as the test form, never as the VEX-profile requirement |
| impact-statement requirement, test form | 1 | 2877 | `For each item in /vulnerabilities[]/product_status/known_not_affected it MUST be tested that a corresponding impact statement exist in /vulnerabilities[]/flags or /vulnerabilities[]/threats.` (33 words, occ=1) — quote its §4.5 form Q3 for the entry text, this one only as the machine-checkable test |
| action-statement requirement, test form | 1 | 2933 | `For each item in /vulnerabilities[]/product_status/known_affected it MUST be tested that a corresponding action statement exist in /vulnerabilities[]/remediations.` (17 words, occ=1) |
```

Deliverable is receipt-only: it is the fenced block above; 0 lane files change from this seat.
No `.suffix` deliverable file exists for this item, so the block body itself is the deliverable:

| deliverable | lines | bytes | sha256 |
|---|---|---|---|
| body of the `text` fence under `## DELIVERABLE` (fences excluded, trailing newline included) | 51 | 7292 | `46fc5a56d0b2dcc97e9cd1eafea0a44308d2dfb89884904c8116eec358b45954` |

Extraction rule used to compute that digest, reproducible as-is:

```
python3 - <<'PY'
import hashlib
t = open('.ufo/waves/round-38/wave1/ExecC2QuoteOnce.md', encoding='utf-8').read().split('\n')
start = t.index('```text') + 1
end = t.index('```', start)
block = '\n'.join(t[start:end]) + '\n'
print(len(t[start:end]), len(block.encode()), hashlib.sha256(block.encode()).hexdigest())
PY
```

observed: `51 7292 46fc5a56d0b2dcc97e9cd1eafea0a44308d2dfb89884904c8116eec358b45954`

## 4. What each pin is for (entry mapping, not landed text)

| pin | fact the F21 entry can assert from it |
|---|---|
| Q1 | the VEX profile's stated purpose: state *that and why* a product is or is not affected — the entry's opening definition |
| Q2 | a VEX document needs at least one of fixed / known_affected / known_not_affected / under_investigation in `product_status` |
| Q3 | **known_not_affected requires an impact statement** — machine-readable flag in `/flags` or human-readable justification in `/threats` (`category` MUST be `impact`) |
| Q4 | **known_affected requires an action statement** in `/remediations` |
| Q5 | the eight `product_status` group names, each a `products_t` |
| Q6–Q10 | the five flag labels that carry the not-affected justification, with the spec's own definitions (Q7's contrast rule with Q6 is on L1765) |

Q3's L2152 continues, after the quoted sentence: `For the latter one, the category value for such a statement MUST be impact and the details field SHALL contain a a description why the vulnerability cannot be exploited.`
(the doubled `a a` is in the source bytes; do not silently fix it if that clause is ever quoted).

## 5. Recheck (run after the snapshot lands)

```
python3 - <<'PY'
import hashlib
p = "corpus/source-snapshots/round-38/S055.txt"
raw = open(p, encoding="utf-8").read(); L = raw.split("\n")
def seg(n, a=None, b=None):
    s = L[n-1]; i = 0 if a is None else s.index(a)
    j = len(s) if b is None else s.index(b)+len(b)
    return s[i:j]
Q = {
 "Q1":  seg(2135, "The main purpose of the VEX format", "vulnerability."),
 "Q2":  "\n".join(L[2140:2145]),
 "Q3":  "\n".join([L[2150], seg(2152, None, "in /vulnerabilities[]/threats.")]),
 "Q4":  seg(2153, None, "as an action statement."),
 "Q5":  seg(1855, "The eight defined properties are", "(known_not_affected)"),
 "Q6":  L[1762], "Q7": L[1763],
 "Q8":  seg(1766, None, "contains the vulnerable code."),
 "Q9":  L[1766], "Q10": L[1768],
}
print("sha256=%s lines=%d" % (hashlib.sha256(raw.encode()).hexdigest(), len(L)-1))
for k, t in Q.items():
    i = raw.find(t); print("%-3s line=%4d occ=%d words=%2d %s" % (
        k, raw.count("\n", 0, i)+1, raw.count(t), len(t.split()),
        "OK" if len(t.split()) <= 25 else "OVER"))
PY
```

Output actually observed (run against my scratch copy, path rewritten to `S055.txt`; the sha256
line proves it is the same bytes the committed snapshot must hold):

```
sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 lines=5146
Q1  line=2135 occ=1 words=24 OK
Q2  line=2141 occ=1 words= 8 OK
Q3  line=2151 occ=1 words=23 OK
Q4  line=2153 occ=1 words=14 OK
Q5  line=1855 occ=1 words=20 OK
Q6  line=1763 occ=1 words=15 OK
Q7  line=1764 occ=1 words=18 OK
Q8  line=1766 occ=1 words=13 OK
Q9  line=1767 occ=1 words=19 OK
Q10 line=1769 occ=1 words=13 OK
```

## 6. Evidence notes and risks

- **Zero duplicates.** All ten pinned quotes occur exactly once in the full snapshot (`occ=1`),
  so no quote needs a location suffix. Every collision the item asked about is in the
  near-duplicate map instead: the *bare labels* occur 2–5 times (enum list at L1757–L1761,
  definition list at L1763–L1769, JSON example `label` values at L3091/L3127/L3133), and the
  four-path `product_status` list occurs twice (L2142, L2848). A quote of a bare label or of the
  bare path list would be ambiguous; the label-plus-definition sentence and the five-line block
  with its `at least one of` lead-in are not.
- **Sibling cross-check.** `.ufo/waves/round-38/wave1/ExecC2Capture.S055.txt` (the capture seat's
  deliverable) is byte-identical to my independent capture — `cmp` reported
  `IDENTICAL to my independent capture`, same sha256, same 5146 lines. Two seats, two clients,
  two fetch times: same normalized text.
- **Quote form difference worth knowing.** The capture seat's manifest pins its Q3 as one line
  (`For each item in /vulnerabilities[]/product_status/known_not_affected an impact statement …`).
  That string has `occ=0` in the snapshot: L2151 ends with `For each item in` and L2152 opens with
  the path, so the joined-with-space form is a whitespace-normalized reading, not a substring.
  Pin Q3 as the two-line quote above (or quote only L2152's sentence, `occ=1`, 18 words).
- **Line numbers are snapshot-bound.** They are 1-based normalized lines of the sha256
  `63c8ad5271…e11cd42` capture; a re-capture with different bytes invalidates all of them
  (the recheck script in §5 fails loudly rather than silently re-pinning).
- **Source-byte quirks preserved, not fixed.** L2152 contains `contain a a description` in the
  source (second sentence, outside Q3). L2135 has nested straight double quotes around
  `"Vulnerability Exploitability eXchange"` — Q1 deliberately starts after them.
- **No writes outside scope.** Nothing installed (no pacman, no `uv tool install`; the task needed
  only `python3`, `curl`, `cmp`, `sha256sum`). Read-only git only (`rev-parse HEAD`,
  `status --porcelain`). Scratch `/fast/scratch/hyaku/kasegi-r38/ExecC2QuoteOnce/` removed before
  yield.
