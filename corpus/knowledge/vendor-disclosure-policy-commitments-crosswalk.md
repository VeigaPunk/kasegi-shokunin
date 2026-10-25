# A vendor disclosure policy commits to a clock, not to a scope: Cisco's PSIRT crosswalked against three Japanese vendor policies
source: S040 — https://www.cisco.com/c/en/us/about/security-center/security-vulnerability-policy.html — sections "Cisco Product Security Incident Response" (L56, ISO/IEC alignment L57-L60, definition L66-L67, reservation L68), "Cisco Process for Product Security Incident Response" (L161, incl. "Incidents that may impact other vendors" L185-L193 with the four names at L187-L190), "Security Risk Assessment" (L244, CVSS v3.1 L245-L249, SIR L254-L259), "Disclosure of Security Vulnerabilities" (L299, default hold L300, four expedite bullets L301-L309), "Disclosure Schedule" (L318), "Security Software Updates" (L482), "Cisco Bug Bounty Programs" (L487-L489); Last Updated 2025 September 8 (L490)
source: S036 — https://cybozu.co.jp/company/security-policy/ — sections 脆弱性対応 → 対象範囲 (L13-L15) and 脆弱性対応フロー items 1-3 (L16-L25); 脆弱性情報の公開 → 対象範囲 (L27-L30) and 脆弱性情報の公開フロー item 2 JVNでの公開 (L43-L44)
source: S038 — https://pepabo.com/contact/vulnerability-reporting/ — sections 脆弱性報告制度 opening paragraphs (L16-L17), 脆弱性の評価について (L18-L20), 報告方法 (L21-L22), and the prohibited-acts list items 1-2 (L23-L25)
source: S039 — https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html — HIRT-PUB10008 §1 製品脆弱性情報の開示プロセス (L494), §1.1 概要 (L495-L501), §1.2 脆弱性情報の入手 (L503-L514), §1.3 調査ならびに対策 (L517-L520), §1.4 情報公開 (L522-L533), §1.5 CVE採番と公開プロセス (L535-L537), §2.6 ISO/IEC 脆弱性情報の開示と脆弱性対応手順 (L611-L623); 更新日 2026年10月14日 (L487)
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S040 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S038 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S039
ground: F10 (new frontier item: vendor-side disclosure policies as corpus objects; the lane's programme rows were platform- and statute-scoped, not vendor-policy-scoped)

## The claim

These four documents are not four versions of one form. Read as a crosswalk, they agree on almost
nothing except that a vendor should be told; what separates them is **who owns the disclosure clock
and how far the document binds itself in writing**. Cisco binds itself to a team, a slot and a
cut-off; Hitachi binds itself to a national simultaneous-publication principle and a coordinator;
Cybozu binds itself to one partner and one agreed date; GMO Pepabo binds itself to a legal posture
and leaves publication to case-by-case judgement.

## The crosswalk (each cell is checkable against the captures)

| dimension | S040 Cisco | S036 Cybozu | S038 GMO Pepabo | S039 Hitachi |
|---|---|---|---|---|
| explicit scope list | products and cloud-hosted services, plus third-party components with a "high profile" test (L200, L218-L233) | yes, twice: 対応 covers all of its own services and products plus third-party (L14-L15, `cybozu-scope`); 公開 covers package products only, cloud/mobile excluded (L28-L30) | no asset list; the object is "当社システム" in one sentence (L17) | products and control systems for the product-vendor IRT (L491), no per-asset list |
| process commitment | investigates all reports of product security vulnerabilities (L162, `cisco-investigates-all`) regardless of code version or lifecycle status until the Last Day of Support (L162-L163) | three steps: 情報収集 / 影響の確認 / 対策 (L16-L25) | all reports go to one internal security team (L16); no steps stated | three steps mapped to two ISO standards (L497-L499) |
| named standard + edition | ISO/IEC 29147:**2018** (L58) | none — `29147` occurs 0 times | none — `29147` occurs 0 times | ISO/IEC 29147:**2014** and ISO/IEC 30111:**2013** (L497-L499), with the 2018/2019 editions listed as links in §2.6 (L615, L621) |
| named coordination partner | CERT/CC, CERT-FI, JP-CERT, NPSA (names at L187, L188, L189, L190; paragraph L185-L193) | JPCERT/CC, for the publication date (L44) | none — `JPCERT` and `CERT/CC` occur 0 times | 情報セキュリティ早期警戒パートナーシップ (L510), CERT/CC (L512), CERT/CC and JPCERT/CC as 調整機関 (L520, L571), JVN and the CERT/CC Vulnerability Notes Database (L533) |
| severity instrument it says it uses | CVSS **v3.1**, Base plus sometimes Temporal (L245-L249), and a Security Impact Rating built on the Base score and included in every advisory (L254-L259) | CVSS as one indicator of 深刻度 (L22), with a CVSS v3 explainer (L49-L51) | none — `CVSS` occurs 0 times; 深刻度 and 実現可能性 are named but no instrument (L19) | none — `CVSS` occurs 0 times |
| stated conditions for going faster | default hold until patches/workarounds exist (L300), then **four** expedite bullets (L301, L302-L304, L305-L308, L309) | 公表日一致の原則, on the date agreed with JPCERT/CC (L44) | publication of the evaluation decided case by case, with no conditions given (L19, `pepabo-case-by-case`) | two principles: fixes ready at publication, and 公表日一致の原則 (L519) |
| published schedule | 1600 GMT on a Wednesday (L319-L320), plus twice-yearly bundles per product family (L321-L331) and an out-of-cycle list (L334-L341) | a JPCERT/CC-agreed publication date (L44), not a fixed time or cadence | none stated | none stated — the date is negotiated, not calendared |
| lifecycle boundary | FCS to LDoS; past LDoS reports are accepted but not analysed, fixed or disclosed (L480-L482) | none stated in the captured handling policy | none stated | none stated |
| lifecycle boundary | FCS to LDoS; past LDoS reports are accepted but not analysed, fixed or disclosed (L480-L482) | none stated | none stated | none stated |
| money | names bug bounty programmes, with the terms on a separate page and no amount here (L487-L489) | names 脆弱性報奨金制度 as one intake channel (L19); terms are on another page | states that no bounty scheme exists (L20) | `報奨金` occurs 0 times |
| reporter-facing duty | asks reporters to keep strict confidentiality until resolutions are published (L180-L181) | none stated | prohibits DoS testing and access beyond one's own account (L23-L25) | none stated |
| reserved definition | defines a vulnerability and reserves the right to deviate (L66-L68) | none stated | none stated | none stated |

## The quoted record (verbatim, per vendor, one quote per load-bearing cell)

Each row is the vendor's own words, attributed to that vendor only, with the capture line where it
sits. No quote crosses a U+FFFD line (see Limits). The `recheck:` line verifies these strings through
`corpus/source-snapshots/round-25/manifest.json`, whose per-source ids for the Japanese rows are
S036 Q2/Q4/Q5/Q7/Q8, S038 Q2/Q3/Q6/Q7 and S039 Q5/Q7/Q8/Q9 — the ids below are this entry's own
labels for the same strings, so a reader can bind row to manifest assertion without guessing.

| quote id | vendor | verbatim (≤25 words) | location |
|---|---|---|---|
| cisco-iso-29147-2018 | Cisco (S040) | "The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018" | L58, §Cisco Product Security Incident Response |
| cisco-investigates-all | Cisco (S040) | "The Cisco PSIRT investigates all reports of product security vulnerabilities" | L162, §Cisco Process for Product Security Incident Response |
| cisco-post-ldos | Cisco (S040) | "Once the LDoS has been reached, the Cisco PSIRT will continue to accept vulnerability reports" | L482, §Security Software Updates |
| cisco-jpcert-partner | Cisco (S040) | "Japan Computer Emergency Response Team (JP-CERT)" | L189, §Cisco Process for Product Security Incident Response, paragraph "Incidents that may impact other vendors" (wrapped L188-L189) |
| cisco-default-hold | Cisco (S040) | "Cisco generally does not publicly disclose security vulnerabilities in a Cisco product until the Cisco PSIRT has completed the incident response process" | L300, §Disclosure of Security Vulnerabilities |
| cisco-active-exploitation | Cisco (S040) | "The Cisco PSIRT has observed active exploitation of a vulnerability" | L302, §Disclosure of Security Vulnerabilities, expedite bullet 2 (L302-L304) |
| cisco-high-profile-bullet | Cisco (S040) | "The Cisco PSIRT has declared a third-party software vulnerability to be high profile." | L309, §Disclosure of Security Vulnerabilities, expedite bullet 4 |
| cisco-weekly-slot | Cisco (S040) | "Cisco generally discloses Cisco Security Advisories at 1600 Greenwich Mean Time (GMT)" | L319, §Disclosure Schedule |
| cisco-bounty-pointer | Cisco (S040) | "For information on Cisco Bug Bounty programs, see" | L487-L489, §Cisco Bug Bounty Programs |
| cybozu-scope | Cybozu (S036) | "当社が作成した全てのサービスおよび、製品" | L14, 脆弱性対応 → 対象範囲 |
| cybozu-cloud-mobile-excluded | Cybozu (S036) | "クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。" | L30, 脆弱性情報の公開 → 対象範囲 |
| cybozu-jpcert-date | Cybozu (S036) | "情報公開は公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します。" | L44, 脆弱性情報の公開フロー item 2 JVNでの公開 |
| cybozu-cvss | Cybozu (S036) | "当社では、深刻度の指標のひとつとしてCVSS(※1) を使用しています。" | L22, 脆弱性対応フロー item 2 影響の確認 |
| cybozu-bounty-intake | Cybozu (S036) | "脆弱性報奨金制度を含む外部からの報告" | L19, 脆弱性対応フロー item 1 情報収集 |
| pepabo-no-bounty | GMO Pepabo (S038) | "現在、報奨金制度は設けておりません。" | L20, 脆弱性の評価について |
| pepabo-safe-harbour | GMO Pepabo (S038) | "セキュリティ研究者に対して、法的措置をとらない方針です。" | L17, 脆弱性報告制度 opening |
| pepabo-case-by-case | GMO Pepabo (S038) | "評価結果の公表については都度判断といたします。" | L19, 脆弱性の評価について |
| pepabo-prohibited | GMO Pepabo (S038) | "DoS攻撃、DoS攻撃に該当する検証" | L24, prohibited-acts list item 1 |
| hitachi-29147-2014 | Hitachi (S039) | "ステップ１：脆弱性情報の入手 ... (1) ISO/IEC 29147:2014 脆弱性情報の開示" | L497, §1.1 概要 |
| hitachi-two-principles | Hitachi (S039) | "調査ならびに対策にあたっての基本的な考え方は、「対策情報を公表日に同時に公開する」「公表日一致の原則に従う」の２つです。" | L519, §1.3 調査ならびに対策 |
| hitachi-coordination | Hitachi (S039) | "脆弱性対策の調整機関であるCERT/CCやJPCERT/CCの協力を得て" | L520, §1.3 調査ならびに対策 |
| hitachi-cna | Hitachi (S039) | "2022年6月より、HIRTはCVE IDを日立製品の脆弱性に割り当て" | L557, §1.5 CVE採番と公開プロセス |

**The one sentence the sample supports.** A reader of these four policies learns the clock before
they learn the scope: S040 states when it will publish (L319) and when it will not (L482); S039
states that publication waits for a ready fix (L519); S036 states that publication waits for a date
agreed with a coordinator (L44); S038 states only that publication is decided per case (L19). A
finding's scope question — is this asset in bounds — is answered by S036 and by S040's product
sentence, but not by S038 or S039.

## Falsifiable rules

1. **Edition, not presence.** Exactly two of these four captures name ISO/IEC 29147, and they name
   different editions (2018 in S040, 2014 in S039). Check:
   `for f in S036 S038 S039 S040; do printf '%s %s\n' "$f" "$(grep -c 29147 corpus/source-snapshots/round-25/$f.txt)"; done`
   prints `S036 0 / S038 0 / S039 8 / S040 1`. An entry that says "the vendors follow ISO/IEC 29147"
   without the edition is falsified by the first line of that output.
2. **One coordinator is shared, one document names none.** JP-CERT appears in S040 (L189) and
   JPCERT/CC in S036 (L44) and S039 (L520, L533), while S038 names no coordinator at all
   (`grep -c JPCERT` = 0, `grep -c CERT/CC` = 0). A claim that a Japanese vendor policy necessarily
   names the national coordinator is falsified by S038.
3. **Money is a property of the page, not of the vendor.** Exactly one of the four pages says in its
   own words that no bounty scheme exists (S038 L20); exactly one names a bounty scheme as an intake
   channel (S036 L19); the Cisco page names its bug bounty programmes and puts the terms on a separate
   page (L487-L489); the Hitachi document never mentions one (`grep -c 報奨金` = 0).
4. **Four expedite bullets, not two.** Under "Disclosure of Security Vulnerabilities" the capture
   carries exactly four bullets after the default-hold sentence: high-severity with fixes planned
   (L301), observed active exploitation (L302-L304), potential for increased public awareness
   (L305-L308), and a declared high-profile third-party vulnerability (L309). A fifth bullet, or a
   "two conditions" reading, falsifies this entry — see the re-grounding note below.

## Rejected over-generalizations

- **Rejected: "Western vendors pay bounties and Japanese vendors do not."** S040 names its bug bounty
  programmes but publishes no amount, eligibility rule or scope on this page — only "For information
  on Cisco Bug Bounty programs, see" (L487-L489) — while S036 names its 脆弱性報奨金制度 as an
  intake channel (L19) and S038 states that no scheme exists (L20). Reason: the four pages carry
  three different money states, and the vendor's nationality does not predict which one a page
  carries. What can be asserted is the narrower, checkable statement in rule 3.
- **Rejected: "Cisco's policy is a process document while the Japanese pages are scope lists."**
  S036 carries an explicit 対象範囲 in both of its halves (L14-L15, L28-L30) *and* a three-step
  process flow (L16-L25); S039 is a process document (L497-L499) with no per-asset scope list.
  Reason: the scope-vs-process axis does not sort this sample — the sorting axis is who owns the
  disclosure clock and whether the document names it.

## Re-grounding note (why this entry is not the staged text)

The staged package of 2026-10-23 (its Cisco row is **staged S068**, not this lane's S040) described
Cisco's faster-disclosure conditions as "the two conditions under which it will go faster". The
round-25 capture lists **four** bullets (L301-L309), and the staged text was written against a page
that was unreachable that round. This entry states what the capture says; the four-bullet count is
itself a falsifiable rule (rule 4).

## Limits

- One capture per vendor, fetched 2026-10-25T08:14:25Z-08:14:28Z (`.ufo/waves/round-25/capture-log.txt`).
  S040 answers http 403 to a plain `curl -L` with a browser UA and http 200 to the capture
  instrument's UA; the capture is the bytes of record and proves availability on that date only.
- Japanese quotes are counted as whitespace-separated tokens, so each is one token; the JP-CERT quote
  is wrapped across two capture lines and matches under the declared whitespace normalization
  (QUALITY Q8), not as a raw byte substring.
- The "money" row is a statement about these four pages. The lane holds no Cisco bounty terms page,
  so nothing here says what Cisco pays or that Cybozu's scheme pays anything.
- Locations are capture line numbers in `corpus/source-snapshots/round-25/`, not upstream line
  numbers; the recheck line re-reads those bytes, not the live pages.
- Capture hazard: `S040.txt` carries U+FFFD replacement characters at L108, L193, L203, L222 and
  L479 (cp1252 bytes decoded with `errors=replace`). No quote in this entry crosses those lines, so
  no quote depends on a mangled byte; the coordination quote stops at the NPSA name (L190) and does
  not reach L193.
