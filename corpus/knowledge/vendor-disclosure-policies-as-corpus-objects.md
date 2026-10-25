# Japanese vendor disclosure pages carry separable objects, not one programme

source: S036 — https://cybozu.co.jp/company/security-policy/ — 脆弱性情報ハンドリングポリシー, sections 脆弱性対応 対象範囲 / 脆弱性対応フロー 1. 情報収集 / 2. 影響の確認 / 脆弱性情報の公開 対象範囲 / 脆弱性情報の公開フロー 2. JVNでの公開 (capture corpus/source-snapshots/round-25/S036.txt:14-44)
source: S037 — https://cybozu.co.jp/products/bug-bounty/faq/ — FAQ（脆弱性報奨金制度）, the Q&A entries on 報告用サイト, 報奨金制度の対象外 sites, 受け取り方法 and 支払い時期 (capture corpus/source-snapshots/round-25/S037.txt:99-123)
source: S038 — https://pepabo.com/contact/vulnerability-reporting/ — 脆弱性報告制度, sections 脆弱性の評価について and 禁止行為 (capture corpus/source-snapshots/round-25/S038.txt:17-25)
source: S039 — https://www.hitachi.co.jp/hirt/publications/hirt-pub10008/index.html — HIRT-PUB10008 (更新日 2026年10月14日), 4 IRT model intro, §1.2 脆弱性情報の入手, §1.3 調査ならびに対策, §1.5/§1.6 CVE採番・活動トピックス, §2.6 ISO/IEC disclosure mapping (capture corpus/source-snapshots/round-25/S039.txt:491,503-520,535-557,611-623)
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S036 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S037 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S038 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S039
ground: F10 — vendor-side disclosure policies as corpus objects; admits the four round-25 captures S036–S039 (fetched 2026-10-25T08:14Z)

## Attribution

Every statement below is the named vendor's own position about its own handling: a
first-party self-description of published policy text, not an audit finding, and not a
rule about vendors in general. Four pages, three vendors — Cybozu (S036 policy page,
S037 bounty FAQ), GMO Pepabo (S038), Hitachi (S039). No claim here extends to a vendor
whose page was not captured.

## Claim 1 — intake is a policy-level list, and a bounty programme is one channel on it

Cybozu's policy names its collection channels rather than a single form:

> 情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。
> — 脆弱性対応フロー 1. 情報収集, capture S036.txt:19

Three channels are named on that line: the state-coordinated partnership
(情報セキュリティ早期警戒パートナーシップ), external reports including the bounty
programme, and internal detection. A report that models Cybozu's intake as "the bounty
programme" describes one of the three.

## Claim 2 — handling scope and disclosure scope are two different lists

Handling scope covers services and products Cybozu creates, plus third-party products it uses:

> 当社が利用しているサードパーティー製品
> — 脆弱性対応 対象範囲, capture S036.txt:15

> 当社が作成した全てのサービスおよび、製品
> — 脆弱性対応 対象範囲, capture S036.txt:14

Disclosure scope is package products only, mobile excluded:

> 当社が作成したパッケージ製品（モバイル製品を除く）
> — 脆弱性情報の公開 対象範囲, capture S036.txt:28

and cloud and mobile are, in principle, not published at all:

> クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。
> — 脆弱性情報の公開 対象範囲, capture S036.txt:30

So "the vendor handles this product" and "the vendor will publish this finding" are
separate predicates on this page, and the second is the narrower one.

## Claim 3 — severity is one indicator inside an internal decision

> 当社では、深刻度の指標のひとつとしてCVSS(※1) を使用しています。
> — 脆弱性対応フロー 2. 影響の確認, capture S036.txt:22

> 発見された情報の影響範囲と深刻度をPSIRTおよび関係部門で確認します。
> — 脆弱性対応フロー 2. 影響の確認, capture S036.txt:21

CVSS is ひとつ — one indicator — and the impact/severity confirmation is assigned to
PSIRT and related divisions, not to the reporter's scoring.

## Claim 4 — the publication date is an agreement, not a clock

> 情報公開は公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します。
> — 脆弱性情報の公開フロー 2. JVNでの公開, capture S036.txt:44

The page names JVN as the publication portal and a date agreed with JPCERT/CC as the
timing. No duration appears on it.

## Claim 5 — money, programme membership and the reporting surface are their own objects

> サイトによっては報奨金制度の対象外の可能性があります。
> — FAQ, Q「Webサイトの脆弱性を見つけました。報告しても良いですか？」, capture S037.txt:109

> 報告にはアカウントが必要になります。
> — FAQ, Q「脆弱性を見つけたので報告したいのですが、どうしたら良いですか？」, capture S037.txt:99

> 報告用サイトアカウントお申し込みフォームからお申込みください。
> — FAQ, Q「報告用サイトのアカウントが欲しいです。」, capture S037.txt:101

> お振込みまたは寄付のいずれかをお選びいただけます。
> — FAQ, Q「報奨金の受け取り方法を教えてください。」, capture S037.txt:111

> いただいた報告が対応完了してから2ヶ月を経過した最終営業日にお支払いいたします。
> — FAQ, Q「報奨金はいつ支払われますか？」, capture S037.txt:115

> 報告用サイトでは脆弱性検証を行わないでください。
> — FAQ, Q「報告用サイトで脆弱性検証を行っても良いですか？」, capture S037.txt:123

Read together: a report is welcome even where the site is outside the programme
(S037:109); the reporting surface is account-gated (S037:99) and account issuance runs through an
application form (S037:101); payment has a form and a clock measured from resolution (S037:111,
S037:115); and the reporting site is described as not the place for verification, with the FAQ
pointing to a separately provided verification environment (S037:123). Membership, money and the
reporting surface are decided on different lines of the same FAQ. The gate the capture states is an
お申し込み form, not an invitation regime: `grep -c '招待' corpus/source-snapshots/round-25/S037.txt`
is 0 (as it is for S036, S038 and S039), so no page in this set supports an "invitation-only" or
"closed programme" reading.

## Claim 6 — Pepabo decides protection, publication and money separately

> また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。
> — 脆弱性報告制度, opening paragraph, capture S038.txt:17 (quoted whole: the fragment omits the subject, 当社システムへの侵入または侵入の試みが)

> 評価結果の公表については都度判断といたします。
> — 脆弱性の評価について, capture S038.txt:19

> 現在、報奨金制度は設けておりません。
> — 脆弱性の評価について, capture S038.txt:20

The protection is bounded by an explicit prohibition list:

> 1.DoS攻撃、DoS攻撃に該当する検証
> — 禁止行為 item 1, capture S038.txt:24

> 2.自分自身のアカウントや情報以外へのアクセス、改ざんを試みるなどの行為
> — 禁止行為 item 2, capture S038.txt:25

Pepabo's page is a reporting channel plus a conditional statement about legal action plus
a case-by-case publication decision, with no reward. The three are decided separately,
and the non-litigation statement refers to conditions the page does not enumerate; the two prohibition items above are a separate list, not those conditions.

## Claim 7 — Hitachi's product-vendor side routes a cross-vendor finding into the partnership and aligns the date

> 情報システム並びに制御システム関連製品を開発する側面(製品ベンダIRT)に焦点を絞り
> — intro (4つのIRT model), capture S039.txt:491

> 情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで
> — 1.2 脆弱性情報の入手, 製品開発工程においての問題発見, capture S039.txt:506

> 協調した脆弱性対策を開始します。
> — 1.2 脆弱性情報の入手, same paragraph, capture S039.txt:506

> 2004年7月から情報セキュリティ早期警戒パートナーシップに製品開発ベンダとして参画し
> — 1.2 脆弱性情報の入手, 情報セキュリティ早期警戒パートナーシップからの通知, capture S039.txt:510

> 調査ならびに対策にあたっての基本的な考え方は、「対策情報を公表日に同時に公開する」「公表日一致の原則に従う」の２つです。
> — 1.3 調査ならびに対策, capture S039.txt:519

> 関係者間で一定の足並みをそろえて公開することです。
> — 1.3 調査ならびに対策, capture S039.txt:519

The page frames the whole process in three steps mapped onto the two ISO/IEC documents, and names
the coordination bodies it works with:

> ステップ１：脆弱性情報の入手 ... (1) ISO/IEC 29147:2014 脆弱性情報の開示
> — 1.1 概要, capture S039.txt:497

> 脆弱性対策の調整機関であるCERT/CCやJPCERT/CCの協力を得て
> — 1.3 調査ならびに対策, capture S039.txt:520

> 2022年6月より、HIRTはCVE IDを日立製品の脆弱性に割り当て
> — 1.5 CVE採番と公開プロセス, capture S039.txt:557

Hitachi states its own process: a finding from its development flow whose impact reaches
another vendor's product is reported to the partnership's 届出窓口, coordinated
remediation starts on that basis, and multi-vendor publication is aligned across the
parties. Since June 2022 the same team states it assigns CVE IDs to Hitachi product
vulnerabilities. This is Hitachi describing Hitachi, not a claim about what other vendors do.

## Falsifiable rules — checkable against a report or package

- FR-1: A package asserting that a vendor publishes everything it handles is falsified for
  Cybozu by S036.txt:14 (handling scope: all its services and products) read against
  S036.txt:30 (cloud and mobile, in principle, not published).
- FR-2: A package treating "the vendor runs a vulnerability-report route" as "the vendor
  pays" is falsified by S038.txt:20.
- FR-3: A package quoting a published non-litigation statement as unconditional
  authorisation is falsified by the condition clause at S038.txt:17 and the two
  prohibited acts at S038.txt:24-25.
- FR-4: A package stating a fixed embargo length for a JVN publication is unsupported by
  these captures: S036.txt:44 and S039.txt:519 name an agreed date and an alignment,
  not a duration.

## Rejected over-generalizations

1. **"A Japanese vendor's disclosure policy is a programme."** Rejected. A bounty programme
   carries a reward ladder and a submission form; neither is a component of these policy pages.
   Pepabo publishes a 脆弱性報告制度 with no reward at all (S038.txt:20) and routes reports to an
   email address rather than a submission form; Cybozu keeps the handling policy (S036) apart from
   the bounty FAQ (S037), and the reward terms and the reporting-site application live only in the
   FAQ. Mapping policy onto programme would make Pepabo's page a programme with no reward and
   Cybozu's policy a programme with no reward terms — both pages say they are something else.
2. **"公表日一致 is a fixed embargo period."** Rejected. Cybozu names a date agreed with
   JPCERT/CC (S036.txt:44) and Hitachi names alignment across vendors (S039.txt:519);
   neither page states a duration, so an "N-day embargo" reading adds a fact the captures
   do not carry.
3. **"A published non-litigation policy grants safe harbour for testing."** Rejected.
   Pepabo's statement is conditional (S038.txt:17) and its prohibition list bars access
   beyond one's own account and information (S038.txt:25), so the page cannot be read as
   authorisation. This is the lane's A7 anti-pattern applied to a Japanese page.
4. **"HIRT-PUB10008 is a disclosure policy for Japanese vendors at large."** Rejected.
   The page states it narrows the focus to the 製品ベンダIRT side (S039.txt:491) and
   describes 日立グループ's own process; it is one vendor's process description.
5. **"Cybozu's bounty is invitation-only."** Rejected. No page in this set contains 招待
   (`grep -c '招待'` over the four captures is 0,0,0,0); what S037.txt:99-101 states is an
   account requirement plus an お申し込み form. An invitation regime is a claim these bytes do not
   carry — a staged draft's "invitation-only" wording is unsupported, and "application-gated" is
   what the capture says.

## Scope and limits

- Four pages, three vendors, read as the pinned captures of 2026-10-25T08:14Z; this is
  not a survey and carries no frequency claim about Japanese vendors.
- The recheck verifies the pinned captures' bytes and the exactly-once presence of each
  quote in them. It does not verify that the upstream pages still carry this text — that
  is source-recheck.py's own stated limit (a captured-source comparison is not a fresh
  network verification).
- Documentation only: this entry records published policy text. It instructs no probing,
  scanning, login or submission against any target, and carries no credential material,
  session or private URL.
