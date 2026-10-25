# ISO/IEC 29147:2014 as the JPCERT/CC P-guideline reads it, and where the two diverge

source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 (JPCERT/CC), 付録6「ソフトウエア製品の脆弱性の取扱いに関する国際標準への対応」 §2 (L1666-1678), §3 (L1679-1690), §4 (L1691-1993), 参考1 (L1996-2079), 参考2 (L2082-2100); capture `corpus/source-snapshots/round-26/S041.txt` (pdftotext, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`)
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041

## Ground

Adopts the staged entry `iso-29147-divergence-and-clause-crosswalk-2026-10-23.md` re-grounded on the fresh S041 capture of the JPCERT/CC 2026-10 guideline (2026-10-25).

## The claim

JPCERT/CC's 2026-10 P-guideline (情報セキュリティ早期警戒パートナーシップガイドライン) states its own account of where its early-warning framework differs from ISO/IEC 29147:2014. The divergence is one sentence, and it is a difference in **obligation**, not in practice: the guideline does not require a vendor to adopt a vulnerability disclosure policy, while ISO/IEC 29147:2014 does require the policy and the publication of part of it (`S041.txt:1868-1870`). Everything else in 付録6 §4 is the operational list that follows from that difference: what a vendor that chooses ISO conformance must add on top of guideline-aligned handling. The guideline is explicit that the two frameworks have no major contradiction (§3, `S041.txt:1680-1681`), so the difference is a gap in what is **required**, not a conflict in what is recommended.

The concrete additions the guideline names for a vendor taking on 29147:2014 conformance are: document and record applied remediation, and — for an online service — notify customers in advance of software updates that land in their environment (L1697-1704, L1778-1791); formulate a vulnerability disclosure policy and publish part of it, covering how to contact the vendor, secure communication options, expected interaction, information useful to a reporter, out-of-scope services, and how reports are tracked (L1706-1713, L1873-1884); stand up an external intake window aligned with the policy (L1717-1719) and **reply with an acknowledgement of receipt within seven days** (L1720-1721, L1913-1916); and treat intermediate-vendor triage and coordination as the vendor's own work, while applying one's own criteria to another vendor's components is usually impractical so a request is often the most that can be done (L1724-1732, L1984-1992).

## The quoted record (verbatim, per claim, with capture line)

The ids map to the manifest assertions in `corpus/source-snapshots/round-26/manifest.json` where one exists; the entry's labels below are the same strings.

| quote id | manifest | verbatim (≤25 words) | location |
|---|---|---|---|
| q-policy-not-required | Q3 | "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません" | S041.txt:1868 |
| q-policy-required | — | "ISO/IEC 29147:2014 では、脆弱性公開ポリシーを策定することや、その一部を公開することを求めています。" | S041.txt:1869-1870 (wraps across the line break at その一/部; matches under the declared markup-whitespace normalization, Q8) |
| q-seven-day-receipt | Q4 | "受信した旨を 7 日以内に返信することが必要となります。" | S041.txt:1916 |
| q-min-policy-aspects | Q5 | "6.2 Minimum policy aspects" | S041.txt:1813 |
| q-optional-policy-aspects | — | "6.3 Optional policy aspects" | S041.txt:1856 |
| q-secure-comm-option | Q2b | "b）セキュアな通信オプション" | S041.txt:1851 |

The pair `q-policy-not-required` + `q-policy-required` is the guideline's own contrast sentence (L1868-1870): the guideline does not ask for a policy; the standard asks for one and for publication of part of it. The 7-day sentence at L1916 is the guideline's **conformance-guidance** wording ("必要となります"), distinct from the standard's own 7.3 wording the guideline quotes as "recommended ... within seven calendar days" (L1901-1903) — the entry keeps the two voices separate (Q4).

## The 6.2/6.3 republication

付録6 §4(2) reproduces ISO/IEC 29147:2014 clause 6 in English with a Japanese rendering (`S041.txt:1792-1867`):

- **6.2 Minimum policy aspects** (L1813) — Japanese 6.2 最小限の要素 (L1838). The minimum list has six lettered elements: a) how the vendor would like to be contacted (L1819), b) secure communication options (L1830), c) setting communication expectations (L1831), d) information useful when submitting a possible vulnerability report (L1832-1834), e) out-of-scope services (L1835), f) how submitted reports are tracked (L1835). Japanese rendering at L1842-1855.
- **6.3 Optional policy aspects** (L1856) — Japanese 6.3 オプショナルなポリシーの要素 (L1862). The optional elements are a) credit to finder (L1859), b) synchronized public disclosure (L1860), c) distribution (L1861). Japanese at L1864-1866.

So a policy that is "at least" conformant carries the six minimum elements; credit-to-finder and synchronized disclosure are optional, not part of the minimum. The guideline's own checklist for what a published policy should include (L1874-1877) mirrors the six minimum elements — the same list, restated as the guidance for conforming vendors.

## The 参考1 clause cross-reference table (p.53-54)

参考1 (`S041.txt:1996-2079`, print pages 53-54) maps ISO/IEC 29147:2014's whole clause structure onto the P-guideline's sections: clause 1 適用範囲 → Ⅲ (L2001-2002), clause 3 用語および定義 → Ⅱ (L2005-2006), clause 5 概念 → Ⅰ/Ⅳ (L2009-2026), clause 7 脆弱性情報の受理 → Ⅳ 5 (L2032-2051), clause 9 アドバイザリの配布 → Ⅳ 5 (L2060-2073). Clause 6 (脆弱性公開ポリシーにおける考慮事項) and clause 8 (ベンダ間における脆弱性の報告) have **no counterpart** — the guideline's 対応箇所 column reads "－" for both (L2027-2028, L2054-2059). The table is therefore itself evidence of the divergence: the two clauses the guideline does not answer are clause 6 (the disclosure policy, exactly the obligation it does not impose) and clause 8 (inter-vendor reporting).

## Falsifiable rules

1. **The obligation contrast.** `grep -cF "P ガイドラインでは、ベンダに脆弱性公開ポリシーの策定を求めていません" corpus/source-snapshots/round-26/S041.txt` prints `1` (L1868), and the continuation at L1869-1870 states the standard requires formulation and partial publication. Any sentence claiming the P-guideline requires a disclosure policy is falsified by L1868.
2. **Seven-day receipt is the guideline's own guidance, not only the standard's.** The guideline's conformance guidance states the acknowledgement within 7 days as necessary (L1916); the standard text it quotes says "recommended ... within seven calendar days" (L1901-1903). A claim that the guideline drops the 7-day expectation is falsified by L1916.
3. **Minimum vs optional is a partition.** 6.2 lists six lettered minimum elements (L1819-1835), 6.3 lists three optional elements (L1859-1861). A claim that credit-to-finder or synchronized disclosure is among the six minimum elements is falsified by the separation of the two tables.
4. **参考1 row for clause 6 is "－".** The table row "6.脆弱性公開ポリシーにおける考慮事項" (L2027) has no P-guideline correspondent (L2028). A claim that every 29147:2014 clause maps to a guideline section is falsified by that row.

## Rejected over-generalizations

- **Rejected: "The P-guideline requires vendors to adopt a vulnerability disclosure policy."** The guideline states the opposite in its own words (`S041.txt:1868`). The guideline's difference from 29147:2014 is precisely the absence of that obligation; requiring it would erase the divergence this entry documents.
- **Rejected: "The P-guideline and ISO/IEC 29147:2014 are equivalent; conforming to one is conforming to the other."** The guideline claims no *major* contradiction (L1680-1681) but immediately itemizes fine-grained points to note when conforming (L1685-1688), and the additions are obligations, not suggestions. Equivalence-overstated fails on clause 6 (policy) and clause 8 (inter-vendor reporting), which have no guideline counterpart.
- **Rejected: "ISO/IEC 29147:2014 requires X" asserted as the lane's own reading of the standard.** The lane holds the standard only as reproduced inside the guideline (English excerpts + Japanese translation, L1739-1866); the paywalled ISO document is not independently held (SOURCES leads). Claims about the standard are attributed to the guideline's reproduction, not to a direct reading.

## The vendor example (S040, pointer only)

The guideline's own 参考2 (L2082-2100) lists existing public vulnerability disclosure policies as examples, and Cisco's "Security Vulnerability Policy" is the first (L2086-2088) — with the URL `https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html`, the same final URL recorded in this lane's S040 recheck cell (R25-5). The lane's round-25 F10 entry (`vendor-disclosure-policy-commitments-crosswalk.md`) already verified Cisco's claim "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018" (S040.txt:58, round-25 manifest) and crosswalked it against the Japanese vendor policies. This entry does not re-make that claim: S040 appears here only as the real-world example the guideline itself cites of a 29147:2018-aligned disclosure policy.

## Limits

- `S041.txt` is a pdftotext capture fetched 2026-10-25T12:34:17Z (capture log in `.ufo/waves/round-26/`); sha256 `e18acbf9…` binds the bytes. Availability is proven on that date only.
- Quotes that cross a PDF line wrap match under the declared markup-whitespace normalization (Q8); locations cite the capture line(s) where the quote sits.
- The ISO/IEC 29147:2014 text appears only as reproduced by the guideline (English excerpts plus its Japanese translation); the lane does not hold the standard itself.
- The capture contains no U+FFFD replacement characters (checked 2026-10-25), so no quote depends on a mangled byte.
