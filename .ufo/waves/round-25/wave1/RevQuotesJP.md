# RevQuotesJP — Japanese capture ↔ claim verification (round 25, wave 1)

Seat: `L1Kasegi25.RevQuotesJP` (read-only reviewer).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base revision `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`.
Scope: the five round-25 captures under `corpus/source-snapshots/round-25/` against the claim list in my item.
Method: `grep -n` anchor search, then `sed -n` line reads of the raw files; every quote below is a verbatim
substring of the named line. No file other than this report was written.

## Capture integrity (checked before quoting)

`sha256sum` of all five files matches `.ufo/waves/round-25/capture-log.txt` exactly, 5/5:

| id | sha256 (first 16) | capture-log | status |
|---|---|---|---|
| S036 | `022ca4f40b9e07a4` | same | match |
| S037 | `b204aa7f60ec2e70` | same | match |
| S038 | `09e077d31ce3b5e3` | same | match |
| S039 | `657e7b4c67e67d00` | same | match |
| S040 | `b7f7b55ff3fc723e` | same | match |

No line in any capture is truncated. The longest stored line is S039 line 524 at 527 characters / 1559 bytes,
and it ends in a complete sentence (`…情報公開を待機します（図2）。`); S039 line 506, the other long line, is
333 characters / 949 bytes and also ends complete (`…などがあります。`). Both exceed the 768-byte cut-off a
paged viewer applies, which proves the cut-off is display-only and the stored bytes are whole. Quotes below
therefore never depend on a truncated tail.

---

## Unsupported claims — these MUST NOT enter an entry

| # | source | claim fragment | why unsupported |
|---|---|---|---|
| U1 | S038 | "no-legal-action policy **and its conditions**" | Line 17 conditions the policy on `以下に示す条件` ("the conditions shown below"), but the capture never enumerates them: the following sections are 脆弱性の評価について / 報奨金制度 / 報告方法, and the only list (lines 23–25) is headed `以下の行為については禁止いたします` — prohibited acts for verification, not the safe-harbour conditions. The reference dangles. An entry may say the policy is conditioned on compliance with conditions stated on the page; it may **not** enumerate or characterise those conditions. |
| U2 | S040 | ISO/IEC alignment with **29147 and 30111** | `grep -c 30111 S040.txt` = **0**. The capture names only `ISO/IEC 29147:2018` (line 58). Any claim of 30111 alignment, or of "ISO/IEC standards" plural, is unsupported by this capture. |
| U3 | S037 | the **contents** of the target-product list | Line 109 only points at the list (`報奨金制度の対象製品をご確認ください`); the list itself is not in the capture. An entry may say a target-product list is referenced as the scope gate; it may **not** name which products are in scope. |
| U4 | S036 | the **third-party disclosure policy** content | Line 31 defers entirely to the CSIRT記述書 (`…CSIRT記述書の「…に関するポリシー」をご参照ください`), which is not captured. Only the deferral is supportable, not any term of that policy. |
| U5 | S036 | scope read as **one** sentence covering services+products+third-party | Lines 14 and 15 are two separate bullets under `脆弱性対応 / 対象範囲`, not one sentence. Supported only as two citations (14 and 15); must not be rendered as a single quoted clause. Also note this is the *handling* scope — the *disclosure* scope at line 28 is narrower (package products only). |

No other claim in the list failed. Everything else below is `yes`.

---

## S036 — 脆弱性情報ハンドリングポリシー (Cybozu)

| claim | capture line | verbatim sentence | supported |
|---|---|---|---|
| intake sources include the early-warning partnership and the bounty programme | 19 | 具体的には、情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。 | yes |
| scope = all services and products the company creates | 14 | 当社が作成した全てのサービスおよび、製品 | yes (bullet, see U5) |
| scope = third-party products it uses | 15 | 当社が利用しているサードパーティー製品 | yes |
| CVSS is one severity indicator | 22 | 当社では、深刻度の指標のひとつとしてCVSS(※1) を使用しています。 | yes |
| disclosure scope = package products, mobile excluded | 28 | 当社が作成したパッケージ製品（モバイル製品を除く） | yes |
| cloud and mobile are not disclosed in principle | 30 | クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。 | yes |
| third-party disclosure deferred to the CSIRT記述書 | 31 | また、当社が利用しているサードパーティー製品の情報開示については、CSIRT記述書の「利用しているサードパーティー製品の情報開示に関するポリシー」をご参照ください。 | yes (deferral only, see U4) |
| JVN publication under the 公表日一致 principle with JPCERT/CC | 44 | 製品の脆弱性対応に関する情報は、日本国内の脆弱性対策情報ポータルサイトであるJVNにて公開します。 なお、情報公開は公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します。 | yes |

Caution on the CVSS row: line 22 says `指標のひとつ` (one of the indicators), and line 50 adds that Cybozu
evaluates vulnerabilities using CVSS. "One indicator among others" is supported; "the sole indicator" is not,
and the capture does not say which other indicators are used.

## S037 — FAQ（脆弱性報奨金制度） (Cybozu)

| claim | capture line | verbatim sentence | supported |
|---|---|---|---|
| invitation/account gating: a report-site account is required | 99 | A. サイボウズではサイボウズが運営する専用サイト（報告用サイト）にアクセスし、報告いただきます。報告にはアカウントが必要になります。 | yes |
| the account is obtained through an application form | 101 | A. 報告用サイトアカウントお申し込みフォームからお申込みください。 | yes |
| target-product list gates eligibility | 109 | A. ご報告いただけます。ただし、サイトによっては報奨金制度の対象外の可能性があります。報奨金制度の対象製品をご確認ください。 | yes (pointer only, see U3) |
| payout timing: last business day two months after remediation completes | 115 | A. いただいた報告が対応完了してから2ヶ月を経過した最終営業日にお支払いいたします。 | yes |
| the "not in the programme" case is asked explicitly | 102 | Q. 脆弱性報奨金制度に参加せずに報告したいのですが、どうしたら良いですか？ | yes |
| what to do if not in the programme | 103 | A. 脆弱性報告フォームからお申込みください。 | yes |

## S038 — 脆弱性報告制度 (GMO Pepabo)

| claim | capture line | verbatim sentence | supported |
|---|---|---|---|
| no-legal-action policy towards security researchers | 17 | また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。 | yes (policy only) |
| the conditions of that policy | — | (no enumerated list in the capture; `以下に示す条件` is never expanded) | **no — U1** |
| no bounty programme | 20 | 現在、報奨金制度は設けておりません。 | yes |
| prohibited acts, even for verification purposes | 23 | 脆弱性の検証目的であっても、以下の行為については禁止いたします | yes |
| prohibited act 1: DoS and DoS-equivalent testing | 24 | 1.DoS攻撃、DoS攻撃に該当する検証 | yes |
| prohibited act 2: accessing or altering anything beyond one's own account/information | 25 | 2.自分自身のアカウントや情報以外へのアクセス、改ざんを試みるなどの行為 | yes |

## S039 — 日立グループにおける製品脆弱性情報の開示プロセス (HIRT-PUB10008)

| claim | capture line | verbatim sentence | supported |
|---|---|---|---|
| product-vendor IRT focus | 491 | HIRT-PUB10008では、情報システム並びに制御システム関連製品を開発する側面(製品ベンダIRT)に焦点を絞り、日立グループにおける製品脆弱性情報の開示プロセスについて紹介したいと思います。 | yes |
| coordinated route when another vendor's product is affected | 506 | なお、発見された脆弱性の影響が日立グループ製品に留まらない(他社製品に影響することがわかった)場合には、情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで、協調した脆弱性対策を開始します。 | yes |

Context confirming the focus claim: line 490 lists the four IRTs and names `製品ベンダIRT` as the product-development side; line 491 then narrows the document to it. The coordinated route is via the 情報セキュリティ早期警戒パートナーシップ reporting desk — not via JVN directly, and not via a named external coordinator, so an entry must not substitute CERT/CC or JPCERT/CC for that route on the strength of this capture (line 520 mentions CERT/CC・JPCERT/CC only for specification-dependent vulnerabilities).

## S040 — Cisco Security Vulnerability Policy

| claim | capture line | verbatim sentence | supported |
|---|---|---|---|
| ISO/IEC alignment | 58–60 | The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018, which are guidelines for disclosure of potential vulnerabilities established by the International Organization for Standardization. | yes (29147:2018 only, see U2) |
| named coordination partners | 185–190 | The Cisco PSIRT works with third-party coordination centers such as … (CERT/CC), … (CERT-FI), … (JP-CERT), and … (NPSA) to manage a coordinated industry disclosure | yes |
| faster disclosure is exceptional, not the default | 300 | Cisco may, however, expedite disclosure of a security vulnerability in the following situations: | yes |
| condition 1: high-severity, fixes planned | 301 | The Cisco PSIRT has completed the incident response process for a high-severity vulnerability and public disclosure of code fixes is planned to address it. | yes |
| condition 2: observed active exploitation | 302–304 | The Cisco PSIRT has observed active exploitation of a vulnerability that could lead to increased risk for Cisco customers. | yes |
| condition 3: potential for increased public awareness | 305–308 | There is the potential for increased public awareness of a vulnerability affecting Cisco products and/or cloud-hosted services… increased risk for Cisco customers. | yes |
| condition 4: third-party vulnerability declared high profile | 309 | The Cisco PSIRT has declared a third-party software vulnerability to be high profile. | yes |
| definition of a security vulnerability (first clause) | 66–67 | Cisco defines a security vulnerability as a weakness in the computational logic found in software and hardware components | yes |
| definition (consequence clause) | 67–68 | that, when exploited, results in a negative impact to confidentiality, integrity, or availability. | yes |
| definition reservation | 68 | Cisco reserves the right to deviate from this definition based on specific circumstances. | yes |

The four conditions are the complete list at 301/302–304/305–308/309; line 310 (`All Cisco security
publications are disclosed to customers and the public simultaneously.`) is the next section, not a fifth
condition. The `…` in the partners row elides only the spelled-out expansions of the four acronyms, which
appear verbatim across lines 186–190 (Computer Emergency Response Team Coordination Center; Computer
Emergency Response Team of Finland; Japan Computer Emergency Response Team; National Protective Security
Authority).

**Two typographic facts an entry must respect.** (a) S040 is hard-wrapped, so every multi-line quote above
joins stored line ends with a single space; the line spans are cited so each join is checkable. (b) The
partner block uses **U+202F NARROW NO-BREAK SPACE**, not U+0020, between each spelled-out body name and its
acronym — eight occurrences across lines 186–190 (`…Center\u202f(CERT/CC)`, `…of Finland\u202f(CERT-FI)`,
`…Team\u202f(JP-CERT)`, `…Authority\u202f(NPSA)`), including the one before `Computer` after `such as the`.
The quote in the table above reproduces exactly the narrow no-break spaces it retains (seven of the eight; the
eighth, the one before `Computer`, falls inside the first elision); `cat -A` shows them as `M-bM-^@M-/`. An
entry that normalises them to ordinary spaces is making a typographic change, not a content change — allowed,
but it must not present the normalised string as a byte-exact quote. No other quoted line in any of the five
captures contains a non-ASCII space.

---

## Residual risk / verification gaps

- **Word-limit compliance.** Every English quote is ≤25 words (verified by token count; the widest is the
  S040 partners row at exactly 25). Where the source sentence is longer, the elision is marked with `…`
  (partners row, condition 3) and the full line span is cited so the elision is checkable. Japanese quotes are
  single sentences, longest 110 characters (S039 line 506); the ≤25-word bound has no clean Japanese
  tokenisation, so each is kept to one sentence and no two lines were merged into one quote.
- **S040 fetch asymmetry.** The capture log records `curl -L` returning 403 while the instrument's UA returned
  200. I verified the bytes of record (hash match) but did not re-fetch, so the capture's fidelity to the live
  page rests on the log's own claim, which is the ScoutFetchCisco seat's item, not mine.
- **S039 is a moving document.** Line 487 reads `更新日：2026年10月14日`; the quotes are valid for this snapshot
  only.
- **No entry drafts existed at review time** (`grep -rl "S03[6-9]\|S040"` over `corpus/knowledge/` and the
  wave-1 tree returned no draft), so verification is against the claim list in my item, not against drafted
  prose. If a scribe later phrases a claim differently from the list, the U1–U5 table is the binding limit.
- Nothing was installed or upgraded for this item; no tool version changes to record.

Report: .ufo/waves/round-25/wave1/RevQuotesJP.md
