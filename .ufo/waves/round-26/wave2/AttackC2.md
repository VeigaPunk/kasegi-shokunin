# Attack C2 — crosswalk quality audit

**Verdict: PASS with defects.** Coverage is genuinely additive to F10 (F10 compares vendor policies; this entry explains the JPCERT/CC guideline’s 2014-standard comparison, clause 6 policy gap, and clause mapping). However, the crosswalk has material quote/line-reference defects and one overstatement in its S040 comparison.

## Findings

- **High — q-policy-required quote is not verbatim at the cited capture lines.** Entry line 24 gives `ISO/IEC 29147:2014 では、脆弱性公開ポリシーを策定することや、その一部を公開することを求めています。` as a single quote attributed to S041:1869-1870. Capture lines 1869-1870 instead read `が、ISO/IEC 29147:2014 では、脆弱性公開ポリシーを策定することや、その一` and `部を公開することを求めています。` The quote omits the initial continuation `が、` and reconstructs the wrap as `一部` (declared whitespace normalization can justify wrap normalization, not omission of source text). Quote as the complete sentence spanning L1868-1870 or accurately quote only the relevant clauses; keep the normalization explicit.

- **Medium — q-seven-day-receipt conflates quoted wording and location.** Entry line 25 quotes `受信した旨を 7 日以内に返信することが必要となります。` and cites only S041:1916. Capture L1916 is `た際には、受信した旨を 7 日以内に返信することが必要となります。` The quote is a substring, but the prose at line 30 calls it the sentence at L1916; clarify it is an excerpt or include the complete sentence. The source separately says its ISO 7.3 text recommends acknowledgement within seven calendar days at L1901-1907; the entry correctly distinguishes that recommendation from the guideline’s necessary wording at L1916.

- **Medium — 6.2/6.3 heading quotes are not exact.** Entry lines 26-27 quote `6.2 Minimum policy aspects` and `6.3 Optional policy aspects`, citing S041:1813 and :1856. Capture has `6.2 Minimum policy aspects` at L1813 and `6.3 Optional policy aspects` at L1856 (these appear exact). But the entry’s explanatory claim that the Japanese rendering and all six/three elements are captured is supported by L1838-1855 and L1862-1866; no defect there. No finding.

- **Low — 参考1 citation is to a broad table range, not precise rows.** Entry line 43 correctly identifies no counterpart for clause 6 and clause 8; capture shows clause 6 and `－` at L2027-2028, clause 8 and `－` at L2054-2059. References are appropriate and checkable.

- **Medium — Cisco edition statement needs strict attribution.** Entry line 60 describes Cisco as a real-world example “of a 29147:2018-aligned disclosure policy”; S040 L58 says only that “The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018”. This supports Cisco’s own statement about PSIRT practices, not an independently verified conclusion that the policy itself is aligned or conforms. F10 correctly quotes and attributes the claim at its lines 46 and 78-82. Rephrase the crosswalk pointer as Cisco’s stated alignment claim, and cite S040.txt:58 directly.

## Coverage / duplication

No actionable duplication with F10: F10 covers cross-vendor policy commitments, including the Cisco 2018 claim; this entry adds a distinct standards-divergence and clause-crosswalk analysis grounded in S041. The Cisco example is a useful bridge, but must preserve attribution and not imply independent conformance verification.

## Residual risk and verification gaps

This is a document-level comparison against the guideline’s reproduced ISO excerpts, not an independent reading of ISO/IEC 29147:2014; the entry itself discloses that limit at lines 56 and 66. No LSP device was available in this session; checks were made against the supplied S041/S040 captures and F10 text. No production files changed. No tools installed.