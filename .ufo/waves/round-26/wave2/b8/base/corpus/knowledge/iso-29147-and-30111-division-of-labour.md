# Division of labour between ISO/IEC 29147:2014 and ISO/IEC 30111:2013
source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 付録6 §2 p.45, division paragraph L1667-1672 and 図1 L1676-1678 (capture corpus/source-snapshots/round-26/S041.txt)
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-26/manifest.json --source S041
ground: F11 — this entry adopts the staged entry iso-29147-and-30111-division-of-labour-2026-10-23.md, re-grounded on the round-26 capture of the JPCERT/CC 2026 P-guideline (S041, 付録6 §2)

## The claim

The JPCERT/CC 2026 partnership guideline's annex 付録6 §2 (国際標準の概要) presents two ISO standards that split a vendor's vulnerability handling into an outward-facing half and an in-house half:

- **ISO/IEC 29147:2014** covers the vendor's dealings with parties outside the company ("社外とのやりとり", S041.txt:1669): the guideline enumerates these as receiving vulnerability information from outside and distributing advisories of countermeasures to users (S041.txt:1669-1670). Its subjects are the businesses that handle software products — product developers, online-service providers and intermediate vendors (S041.txt:1667-1668).
- **ISO/IEC 30111:2013** provides guidance for the vendor's in-house vulnerability handling process — verification of vulnerabilities and development of countermeasures (S041.txt:1671-1672).

Figure 1 shows the correspondence between the two standards, drawn based on ISO/IEC 29147:2014 (S041.txt:1676-1678).

Two already-mined vendor rows corroborate the same split from the vendor side:

- Hitachi's HIRT publication (S039) maps its three-step product-vulnerability disclosure process onto the two standards: step 1 (情報の入手, acquiring the vulnerability information) and step 3 (情報公開, public disclosure) map to ISO/IEC 29147:2014, while step 2 (調査ならびに対策, investigation and mitigation) maps to ISO/IEC 30111:2013 (S039.txt:497-499). The internal investigation phase — not the receipt or the announcement — is the 30111 piece.
- Cisco's PSIRT (S040) states alignment with ISO/IEC 29147:**2018** (S040.txt:58) — the 2018 edition, whereas the JPCERT/CC guideline and Hitachi compare against 29147:2014 / 30111:2013.

## The quoted record

All quotes are verbatim, contiguous substrings of their captures, each ≤70 characters. Locations are capture line numbers (`corpus/source-snapshots/round-26/S041.txt`, `corpus/source-snapshots/round-25/S039.txt`, `corpus/source-snapshots/round-25/S040.txt`).

| quote id | source | verbatim (≤70 chars) | location |
|---|---|---|---|
| jpcert-29147-subject | S041 | "ISO/IEC 29147:2014 はソフトウエア製品に係る事業者" | S041.txt:1667 |
| jpcert-outward-exchanges | S041 | "社外とのやりとり" | S041.txt:1669 |
| jpcert-outward-enum | S041 | "弱性に関する情報の受領、ユーザに対する脆弱性対策のアドバイザリ配布等）" | S041.txt:1670 — continuation of the enumeration that begins on L1669 (the PDF line wrap splits 脆弱性 into 脆/L1669 + 弱性/L1670) |
| jpcert-30111-half1 | S041 | "ISO/IEC 30111:2013 はベンダの社内での脆弱性取扱" | S041.txt:1671 (manifest Q1a) |
| jpcert-30111-half2 | S041 | "いのプロセス（脆弱性の検証、脆弱性対策の開発等）の指針を提供します。" | S041.txt:1672 (manifest Q1b) |
| jpcert-fig1-title | S041 | "ISO/IEC 29147 と ISO/IEC 30111 の対応" | S041.txt:1677 |
| jpcert-fig1-caption | S041 | "（出所：ISO/IEC 29147:2014 を元に作成）" | S041.txt:1678 (anchor; the string repeats at L1777/L1867/L1908/L1974 for later figures in 付録6) |
| hitachi-step1-29147 | S039 | "ステップ１：脆弱性情報の入手 ... (1) ISO/IEC 29147:2014 脆弱性情報の開示" | S039.txt:497 |
| hitachi-step2-30111 | S039 | "ステップ2：調査ならびに対策 ... (2) ISO/IEC 30111:2013 脆弱性対応手順" | S039.txt:498 |
| hitachi-step3-29147 | S039 | "ステップ3：情報公開 ... (3)(4) ISO/IEC 29147:2014 脆弱性情報の開示" | S039.txt:499 |
| cisco-iso-29147-2018 | S040 | "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018" | S040.txt:58 |

## Falsifiable rules

1. **Classification rule.** Given a vendor vulnerability-handling step, decide the standard by direction: report receipt and advisory/publication are 29147; verification and mitigation development are 30111. Check against S041.txt:1667-1672 (definition and division) and the Hitachi mapping S039.txt:497-499 — in particular, step 3 (情報公開) maps to 29147, not 30111, which falsifies any "29147 = intake only" reading.
2. **Edition rule.** Each source names its own edition: JPCERT/CC and Hitachi compare against ISO/IEC 29147:2014 / 30111:2013 (S041.txt:1656-1658; S039.txt:497-499), while Cisco names 29147:2018 (S040.txt:58). A claim about "ISO/IEC 29147" that drops the edition cannot be checked: `grep -c '29147:2018' corpus/source-snapshots/round-25/S040.txt` prints `1`, while `grep -c '29147:2014' corpus/source-snapshots/round-26/S041.txt` prints `24`.

## Rejected over-generalizations

- **Rejected: "ISO/IEC 29147 is only about receiving vulnerability reports."** S041 puts both directions under 29147's 社外とのやりとり: receiving vulnerability information from outside **and** distributing advisories of countermeasures to users (S041.txt:1669-1670), and Hitachi maps its public-disclosure step to 29147 as well (S039.txt:499).
- **Rejected: "Vendors follow ISO/IEC 29147:2014."** Cisco's own policy states alignment with 29147:**2018** (S040.txt:58); the JPCERT/CC guideline and Hitachi compare against the 2014/2013 editions. State the edition a source names rather than assuming one.

## Limits

- One capture per source: S041 was fetched 2026-10-25T12:34:17Z by capture-source.py (`pdftotext` of the JPCERT/CC 2026 P-guideline PDF; sha256 e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47); S039/S040 are round-25 captures rechecked by their own entries.
- The 30111 sentence wraps across S041.txt lines 1671-1672; it is quoted as the two manifest-pinned fragments Q1a/Q1b, not as one raw substring. The outward enumeration likewise wraps (L1669→L1670), and the quoted fragment starts at the wrapped word.
- The 図1 caption string appears five times in 付録6 (L1678, L1777, L1867, L1908, L1974); L1678 is the 図1 caption per the capture record; the figure image itself is not reproduced.
- Documentation-only: nothing here instructs contacting, probing, scanning, or submitting against any system; all sources were read as public documents on 2026-10-25.
