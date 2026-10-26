# RevEntryF21 — independent review of the F21 entry (S055, OASIS CSAF v2.0 VEX profile)

Round 38, wave 1, leaf reviewer seat. Item: independently verify the F21 entry's facts (own fetch + `capture-source.py` normalization + the five load-bearing claims), then review `ScribeEntryF21.entry.md` (quotes at declared lines, ≤25 words, attribution) and score it against QUALITY Q1–Q6. Receipt only; no deliverable file (item names none).

Reviewed artifact: `.ufo/waves/round-38/wave1/ScribeEntryF21.entry.md` — 137 lines, 22,887 bytes, sha256 `0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a`. The landed `corpus/knowledge/csaf-vex-product-status-and-justifications.md` is byte-identical (same sha256, 22,887 bytes), so this review covers the landed bytes.

## 1. Independent fact verification (my own fetch, not the scribe's)

Fetch (rules form): `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html` → HTTP 200, 414,858 bytes, 2026-10-26T18:32:35Z, raw sha256 `fad0c60d5857ac078e6c7b4f5fee5dc1aebd63645fbc61182b227e25420cd66b`. That raw sha256 and byte count are byte-identical to the manifest record's `raw_sha256`/`fetched_bytes` (its fetch 2026-10-26T18:25:51Z) — two independent curl fetches ~7 min apart served identical bytes.

Normalization with the lane instrument: `python3 corpus/instruments/capture-source.py --id S055 --url … --out $S/S055-review.txt --kind html` → `status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42 utc=2026-10-26T18:32:39Z`; `--selftest` → `selftest normalize=ok deterministic=ok`. My curl copy normalized through the same module gives the identical snapshot sha256 (272,441 bytes, 5,146 lines). Observation: the urllib fetch moved 367 raw bytes (415,225 vs 414,858) yet normalized identically — the normalized snapshot is the stable identity, which is exactly what the manifest pins (`sha256` for the snapshot, `raw_sha256` for its own fetch). No defect.

The landed `corpus/source-snapshots/round-38/S055.txt` is byte-identical to my capture (`63c8ad52…`, 5,146 lines, 272,441 bytes), and the landed `manifest.json` carries the S055 record (url, `fetched_utc 2026-10-26T18:25:51Z`, sha256, 4 quotes).

The five load-bearing claims an entry on the VEX profile must make — all verified at pinned lines of my own normalized capture:

1. **Purpose** — L2135 (§4.5 Profile 5: VEX, heading L2134): "The main purpose of the VEX format is to state that and why a certain product is, or is not, affected by a vulnerability." Terminology definition at L394 ("enables a supplier or other party to assert whether or not a particular product is affected by a specific vulnerability").
2. **Required product_status categories** — four, not eight: profile requirement list L2141–L2145 ("at least one of" fixed / known_affected / known_not_affected / under_investigation), mandatory test 6.1.27.7 L2843–L2844 ("at least one of the elements fixed, known_affected, known_not_affected, or under_investigation is present in product_status"), failing example L2852–L2861 (carries `first_fixed` + `recommended` only, verdict L2861). The eight defined properties are at L1855 (§3.2.3.9, heading L1854).
3. **Impact statement for known_not_affected** — L2151–L2152: machine-readable flag in `/vulnerabilities[]/flags` OR human-readable justification in `/vulnerabilities[]/threats` (category MUST be `impact`); test 6.1.27.9 L2876–L2877 repeats it.
4. **Action statement for known_affected** — L2153: "additional product specific information SHALL be provided in /vulnerabilities[]/remediations as an action statement"; test 6.1.27.10 L2932–L2933; `no_fix_planned`/`none_available` permitted (L2154).
5. **The five flags labels** — enum at L1757–L1761 (§3.2.3.5, heading L1729): `component_not_present`, `inline_mitigations_already_exist`, `vulnerable_code_cannot_be_controlled_by_adversary`, `vulnerable_code_not_in_execute_path`, `vulnerable_code_not_present`; per-label meanings L1763–L1769; "The given values reflect the VEX not affected justifications." L1762. Exactly five, no sixth.

Also verified: `/document/category` SHALL be `csaf_vex` (L2156); contradicting-status groups pairwise disjoint (6.1.6, L2328–L2341, `recommended` exempt L2338); per-status definitions L1885–L1894 (known_not_affected L1890–L1891).

## 2. Entry review — quotes, word counts, attribution

Quote binding, checked programmatically against my own capture (identical sha256, so line numbers coincide). The entry carries **70 anchored quoted spans** (65 inline/blockquote `"…" (L<n>)`/`"…" — L<n>` spans + 5 table rows whose anchor sits in the next cell), **68 distinct** — matching the entry's own FC-1 claim `spans 70 distinct 68 words_max 25 anchors_ok 70 of 70`.

- **Present at declared line:** all 70. 68 exactly-once; the 2 double-occurrence spans are exactly the ones FC-1 discloses — the IPR-mode sentence (L46 and L321, entry anchors L46) and the `/product_tree` requirement (L2127 and L2139, entry anchors L2139, the VEX-profile occurrence, which I confirmed contains the text).
- **Split sentence:** the Claim 3 blockquote spans L2151–L2152 ("For each item in" ends L2151); it matches only after whitespace normalization — present in the declared two-line window, exactly-once in the whole capture under that normalization (`normalized=markup-whitespace`, the Q8-declared form). The entry's Honest limit discloses this.
- **≤25 words:** all 70; maximum is exactly 25 (the 6.1.27.7 test quote and the L1887 `fixed` definition).
- **Table rows (Claim 5):** all five label-meaning quotes verbatim at L1763/L1764/L1766/L1767/L1769, exactly-once, 14/17/16/19/12 words.
- **Numbers copied from the source:** header's 5,146 lines / 272,441 bytes / sha256 reproduced; FC-2 counts reproduced exactly (`score=101 scoring=2 severity=15 CVSS=73 product_status=79 known_not_affected=18 known_affected=21 under_investigation=12 csaf_vex=10 VEX=21 EPSS=0 KEV=0 SSVC=0`); all 15 `severity` hits are `aggregate_severity`-related or the L381 terminology example, as claimed. FC-3 (five labels, no sixth), FC-4 (Example 82 at L2852, `first_fixed`+`recommended` only, verdict L2861), FC-5 (L2152/L2153 + tests L2877/L2933), FC-6 (EPSS/KEV/SSVC = 0, CVSS only as delegated schema L517–L527) all reproduced.
- **Header anchors:** every `L<n>` pointer in the `source:` line re-opened against my capture — L1, L3–L4, L18, L27–L33, L35–L36, L42, L44, L46, L53, L381, L498, L502, L510, L515–L516, L518, L521–L527, L394, L1233/L1246, L1729/L1737–L1739/L1757–L1769, L1855/L1887–L1894, L2069–L2078, L2134–L2156, L2843–L2861, L2876–L2877, L2932–L2933, L3095–L3097 — all correct.
- **Attribution (Q4):** standard's text attributed to the TC throughout; examples marked informative (L498, including the L2931 group-coverage note, which sits inside an example); the CVSS/KEV/EPSS/SSVC comparison is labelled "Lane analysis, not a quote" and its one-line characterizations of F01/F18/F19/F20 match the frontier rows (corpus/README.md L202, L388, L389, L416); the single lane-reading sentence ("a program's scope call or duplicate decision stays with the program") is explicitly labelled as the lane's reading; rejected over-generalization 7 explicitly refuses any adoption claim. No universal rule is manufactured from the standard's own words.
- **Recheck line:** `bash -n` OK; `cd <lane-root> &&`-prefixed; human note after `#`; fail-closed behavior described (exit 2 missing capture/manifest, exit 1 moved quote). Ran it: `S055:sha256 OK` + `Q1..Q4 OK` with `occurrences=1` and anchors `2135-ok/2844-ok/2151-ok/1767-ok`, exit 0 (Q3 line prints `normalized=markup-whitespace`).

## 3. QUALITY Q1–Q6 scoring

| id | verdict | evidence |
|---|---|---|
| Q1 | PASS | Three header lines directly under the H1: `source:` S055 + URL + capture path + exact anchors; `verified-at: 2026-10-26`; `recheck:` runnable cd-prefixed command (`bash -n` OK), fail-closed. Shape matches the admitted F17/F18 entries' headers (incl. the `ground:` line). |
| Q2 | PASS | Every load-bearing claim rests on S055 — tier A, kind spec, opened 2026-10-26 (the admitting round); no tier-C support; comparative sentences labelled lane analysis and cross-referenced to F01/F18/F19/F20 rows that exist as stated. |
| Q3 | PASS | 70/70 anchored spans verbatim at their declared normalized lines, all ≤25 words, exactly-once except the two disclosed double occurrences each anchored to the occurrence meant; numbers copied from the source. One non-quoted-span pointer defect is filed as F1 below (it is a backtick literal in the Honest limit, not a load-bearing claim's quote). |
| Q4 | PASS | Attribution kept everywhere (TC's text, informative examples, lane analysis labelled, lane reading labelled, no vendor-adoption inference). |
| Q5 | PASS | Falsifiable rule with seven anchored falsifiers (a)–(g); eight rejected over-generalizations, each with reason and anchor. |
| Q6 | PASS | Documentation-only closing statement; the usage section only reads published vendor VEX documents; no probing/scanning/login/submission instruction, no credential or private-URL material. |

## 4. Findings

- **F1 (minor, one-token fix):** Honest-limit bullet asserts "`L2155` reads `MAY also be provide`" — the text is on **L2153** (`…as an action statement. Optional, additional information MAY also be provide through…`); L2155 is the Product-Group-ID coverage sentence and contains no such text. The bullet's other two pointers are correct (L2152 `contain a a description` ✓; L2071 `indirect through` ✓ — the typo sits in L2071's first sentence, the quoted sentence is its second). Not a `"…" (L<n>)` span, so FC-1's `anchors_ok 70 of 70` is unaffected and no load-bearing claim moves; but as landed it is a wrong location assertion (R9 erratum class). Recommend correcting L2155 → L2153 in that bullet before/at commit; with the fix the entry is clean.
- No other defect: every checked quote, count, anchor and attribution held; the five load-bearing claims are correct and correctly anchored.

## 5. Verdict

**Entry passes Q1–Q6 — admissible.** One minor pointer defect (F1) recommended for a one-token correction; it does not touch any load-bearing claim or quoted span.

## 6. Commands run (evidence)

- `curl -sS -L --max-time 90 -A kasegi-shokunin/1.0 -o csaf-raw.html -w …` → `http=200 bytes=414858`, `utc=2026-10-26T18:32:35Z`, raw sha256 `fad0c60d…` (matches manifest `raw_sha256`).
- `python3 corpus/instruments/capture-source.py --selftest` → `selftest normalize=ok deterministic=ok`.
- `python3 corpus/instruments/capture-source.py --id S055 --url … --out $S/S055-review.txt --kind html` → `status=200 fetched_bytes=415225 snapshot_bytes=272441 sha256=63c8ad52… utc=2026-10-26T18:32:39Z`.
- Module-level re-normalization of my curl copy → identical snapshot sha256 `63c8ad52…` (272,441 bytes).
- Programmatic span check over the entry: 65 regex spans + 5 table rows = 70; all present at declared lines; max words 25; Q3 quote exactly-once under whitespace normalization in the L2151–L2152 window.
- `grep -oF` vocabulary counts → FC-2 numbers reproduced exactly; severity-hit line list = L381 + aggregate_severity lines only.
- `bash -n` on the entry's recheck command → OK; then ran it → 5 OK lines, exit 0.
- `sha256sum` wave1 entry vs landed `corpus/knowledge/csaf-vex-product-status-and-justifications.md` → identical `0343ef45…`; landed `corpus/source-snapshots/round-38/S055.txt` → identical `63c8ad52…`.
- Frontier rows F01/F18/F19/F20/F21 read at corpus/README.md L202/L388/L389/L416/L417.

## 7. Seat notes

- Tooling: nothing installed or upgraded (python3/curl/git already sufficient); no pacman run.
- Scratch: `/fast/scratch/hyaku/kasegi-r38/RevEntryF21/` removed before yield (trap); no writes outside the wave1 receipt and scratch.
- Entry file appeared on check 2 of 3 (18:38:46Z; check 1 at 18:33:28Z found none).
