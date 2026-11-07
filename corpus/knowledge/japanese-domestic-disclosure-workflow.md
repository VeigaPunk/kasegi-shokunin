# The Japanese domestic disclosure workflow

source: S041 — https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf — 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月, 注釈4 起算日の定義 (L340), Ⅳ．3) 公表日 45日目安 (L648-653), Ⅳ．4) 公表日決定後の対応 (L658-660), Ⅳ．11) 取下げ (L430), 付録2 図３/図４ (L1157, L1281, L1331) — capture corpus/source-snapshots/round-28/S041.txt
source: S042 — https://www.ipa.go.jp/security/todokede/vuln/process.html — 脆弱性関連情報の届出受付業務における取扱いプロセス (IPA), 最終更新日 2017年5月30日 (L123); ソフトウエア製品 1.–10. (L133-159) with 5.起算日の連絡 (L144-145); ウェブアプリケーション 1.–7. (L162-182); 自社製品 1.–8. (L184-200) — capture corpus/source-snapshots/round-28/S042.txt
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
ground: F12 — adopts the staged package entry `japanese-domestic-disclosure-workflow.md` (`/home/vgpnk/Projects/shokuknow/merge/kasegi/`, read-only), re-grounded line by line on this round's captures; every quote below was re-located in `corpus/source-snapshots/round-28/`, none copied from the package bytes.

## The claim

Japan's vulnerability intake is a **state-coordinated** pipeline, not a marketplace: IPA receives the report as the designated intake body, and JPCERT/CC contacts the product developer and runs the publication adjustment. IPA dates the arrangement to a Ministry of Economy, Trade and Industry notification: "2004年7月8日から経済産業省の告示に基づき" (S042.txt:130), and states its own role as "IPA は、届出受付機関として届出された脆弱性関連情報を下記のとおり取扱います。" (S042.txt:131). There is no bounty and no per-finding severity ratchet; the finder's operative artefact is a **date**.

## The software-product path — ten numbered steps

IPA's page numbers the product path 1.–10. (S042.txt:133-159). JPCERT/CC's guideline carries the same flow as 図３, "図３ ソフトウエア製品における脆弱性情報取扱いの全体フロー" (S041.txt:1281), announced by "ソフトウエア製品、ウェブアプリケーションそれぞれの脆弱性情報取扱いに関" (S041.txt:1157, wrapping into L1158).

1. 届出の受付; 2. 受理／不受理の決定; 3. IPA → JPCERT/CC への連絡; 4. 製品開発者へ連絡 — an unreachable developer is named publicly rather than dropped: "製品開発者に連絡が取れない場合は、連絡不能開発者一覧に公表し、製品開発者からの連絡を呼びかけます。" (S042.txt:142), and a small-impact report can be closed at contact: "製品開発者に連絡することで取扱いを終了することがあります。" (S042.txt:143); 5. 起算日の連絡; 6. 製品開発者による対応 (a contact window, the verification result and a publication schedule, the mitigation, and status reports); 7. 対応状況の受付 — JPCERT/CC shares status with IPA and "発見者は、IPAへ進捗状況の問い合わせを行なう事ができます。" (S042.txt:153); 8. 公表日の調整; 9. 対応状況（対策方法）の公表 on the JVN portal; 10. "10. 統計情報の公表" (S042.txt:159).

## 起算日 is the clock anchor

The finder is told a date, and JPCERT/CC defines what that date is: "本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。" (S041.txt:340). The anchor is the **first attempt** at the contact required by Ⅳ．4．2) — not the day IPA received the report, and not the day the developer answered.

IPA's step 5 relays it in both directions: "JPCERT/CC は製品開発者への連絡を開始した旨（起算日）" (S042.txt:145) goes to IPA, and "IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。" (S042.txt:145) returns it to the finder.

JPCERT/CC sets a target publication date off that anchor: "みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、" (S041.txt:648). The ただし clause is load-bearing — the figure is 目安 (a guide), not a deadline — and four considerations follow: "公表日の決定に際しては、以下の点も考慮します。" (S041.txt:649), from "① 対策方法の作成に要する期間" (S041.txt:650) to "④ 当該脆弱性の悪用に関するリスク" (S041.txt:653). A date already set can still move: JPCERT/CC may change it on the developer's request, "公表日を変更することがあります。" (S041.txt:660), and the clause then lists five grounds on which publication may be called off entirely (S041.txt:662-671).

**The one-year withdrawal rule.** A finder who has asked IPA not to disclose (情報非開示依頼) can have that request lifted once a year has run: "なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、" (S041.txt:305) "情報非開示依頼の取り下げを求めることができます。" (S041.txt:306). The operative clause repeats in the process list — "IPA は、起算日から 1 年以上経過した届出について、発見者から情報非開示依" (S041.txt:430, wrapping into "頼の取下げが求められた場合、これを取り下げます。", L431) — and adds that where the developer needs more time for a justified reason, IPA must explain the situation so the finder can judge the need to disclose. Precision: what is withdrawn is the non-disclosure request, not the report.

## The web-application path is lighter — seven steps

Here the counterparty is the ウェブサイト運営者 and IPA deals with it directly:

1. 届出の受付 (S042.txt:162); 2. 受理／不受理 (S042.txt:165); 3. "ウェブサイト運営者の連絡先を調査し、脆弱性関連情報を連絡します。" (S042.txt:168) — with closure available when no contact is found or no reply comes, and for small-impact reports (S042.txt:169); 4. "4.取扱い開始連絡" (S042.txt:170): "発見者へ、ウェブサイト運営者に脆弱性関連情報を連絡した旨(取扱い開始連絡)を連絡します。" (S042.txt:171); 5. 運営者による対応, where a suspected personal-data leak adds a public statement of the facts — "個人情報漏洩などの可能性がある場合は、二次被害の防止のため事実関係を公表" (S042.txt:178); 6. "6.修正完了の連絡" (S042.txt:179); 7. statistics, with the reported site kept unidentifiable: "その際、届出のウェブサイトが判別可能な情報は公表しません。" (S042.txt:182).

What this path lacks is the clock apparatus. There is no 起算日の連絡 step and no 公表日の調整 step, and JPCERT/CC does not appear anywhere in the seven steps (S042.txt:162-182). The guideline matches: its web chapter Ⅴ (S041.txt:856) carries no 起算日 and no 45-day figure — both occurrences of "45 日" in the capture sit in chapter Ⅳ (S041.txt:648, 786) — and the detailed flow 図４, "図４ ウェブアプリケーションにおける脆弱性情報取扱いの全体フロー" (S041.txt:1331), has no 起算日の連絡 box, while 図３ has four (S041.txt:1170, 1171, 1186, 1211). The chapter's overview 図２ numbers five steps (S041.txt:859-886) against 図４'s seven; that is a granularity difference between an overview and a detailed flow, not a second process.

## The self-report path — eight steps

A product developer reporting its own product gets an eight-step path (S042.txt:184-200): IPA forwards to JPCERT/CC, JPCERT/CC contacts the developer named in the report, the developer sets a window and writes the mitigation, the publication date is adjusted, IPA and JPCERT/CC publish on JVN, and the last step is "8.統計情報の公表" (S042.txt:200). No 起算日 step appears here either.

## Why it matters

起算日 is this round's transferable artefact. The lane's timeline rule (F02, `corpus/knowledge/coordinated-disclosure-timelines.md`) asks a disclosure record to name its coordinator, the event that starts the clock, the stated interval, and any documented extension. 起算日 answers the trigger question differently from the F02 sources, whose recorded triggers are the report or the availability of a fix (F02, S004 and S005): here the trigger is an **attempt**, so the clock starts even if the developer never answers, and both sides can see the same date because IPA relays it to the finder. Paired with the 45-day 目安 and the four considerations, it supplies a Japanese column for any coordinator-timeline comparison without importing another coordinator's policy. The interval number happens to coincide with CERT/CC's 45-day policy (F02, S004), but neither capture links the two: keep the records separate, since the trigger, the extension list and the withdrawal rule are this programme's own.

## The quoted record

All quotes are verbatim, contiguous substrings of the round-28 captures, each ≤70 characters. Locations are capture line numbers in `corpus/source-snapshots/round-28/`. The last column names the `manifest.json` assertion that pins the quote, where one does.

| quote id | source | verbatim (≤70 chars) | location | manifest pin |
|---|---|---|---|---|
| ipa-statutory-basis | S042 | "2004年7月8日から経済産業省の告示に基づき" | S042.txt:130 | — |
| ipa-receipt-agency | S042 | "IPA は、届出受付機関として届出された脆弱性関連情報を下記のとおり取扱います。" | S042.txt:131 | Q2 |
| ipa-page-revision | S042 | "最終更新日：2017年5月30日" | S042.txt:123 | Q3 |
| ipa-product-step4-unreachable | S042 | "製品開発者に連絡が取れない場合は、連絡不能開発者一覧に公表し、製品開発者からの連絡を呼びかけます。" | S042.txt:142 | Q4 |
| ipa-product-step4-close | S042 | "製品開発者に連絡することで取扱いを終了することがあります。" | S042.txt:143 | — |
| ipa-product-step5-head | S042 | "5.起算日の連絡" | S042.txt:144 | Q1 (heading) |
| ipa-product-step5-relay-in | S042 | "JPCERT/CC は製品開発者への連絡を開始した旨（起算日）" | S042.txt:145 | Q1 (first half) |
| ipa-product-step5-relay-out | S042 | "IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。" | S042.txt:145 | Q1 (second sentence) |
| ipa-product-step7-progress | S042 | "発見者は、IPAへ進捗状況の問い合わせを行なう事ができます。" | S042.txt:153 | Q5 (second sentence) |
| ipa-product-step10 | S042 | "10. 統計情報の公表" | S042.txt:159 | — |
| ipa-web-step3-contact | S042 | "ウェブサイト運営者の連絡先を調査し、脆弱性関連情報を連絡します。" | S042.txt:168 | — |
| ipa-web-step4-head | S042 | "4.取扱い開始連絡" | S042.txt:170 | — |
| ipa-web-step4-body | S042 | "発見者へ、ウェブサイト運営者に脆弱性関連情報を連絡した旨(取扱い開始連絡)を連絡します。" | S042.txt:171 | Q6 |
| ipa-web-step5-personal-data | S042 | "個人情報漏洩などの可能性がある場合は、二次被害の防止のため事実関係を公表" | S042.txt:178 | — |
| ipa-web-step6-head | S042 | "6.修正完了の連絡" | S042.txt:179 | — |
| ipa-web-step7-suppression | S042 | "その際、届出のウェブサイトが判別可能な情報は公表しません。" | S042.txt:182 | — |
| ipa-self-step8 | S042 | "8.統計情報の公表" | S042.txt:200 | — |
| jpcert-kisoribi-definition | S041 | "本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。" | S041.txt:340 | Q1 |
| jpcert-45-day-target | S041 | "みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、" | S041.txt:648 | Q4 |
| jpcert-factors-head | S041 | "公表日の決定に際しては、以下の点も考慮します。" | S041.txt:649 | — |
| jpcert-factor-mitigation-time | S041 | "① 対策方法の作成に要する期間" | S041.txt:650 | — |
| jpcert-factor-abuse-risk | S041 | "④ 当該脆弱性の悪用に関するリスク" | S041.txt:653 | — |
| jpcert-pubdate-change | S041 | "公表日を変更することがあります。" | S041.txt:660 | — |
| jpcert-withdraw-1y | S041 | "なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、" | S041.txt:305 | Q6 |
| jpcert-withdraw-verb | S041 | "情報非開示依頼の取り下げを求めることができます。" | S041.txt:306 | Q6 (continuation) |
| jpcert-withdraw-process | S041 | "IPA は、起算日から 1 年以上経過した届出について、発見者から情報非開示依" | S041.txt:430 | — |
| jpcert-annex2-scope | S041 | "ソフトウエア製品、ウェブアプリケーションそれぞれの脆弱性情報取扱いに関" | S041.txt:1157 | — |
| jpcert-fig3-caption | S041 | "図３ ソフトウエア製品における脆弱性情報取扱いの全体フロー" | S041.txt:1281 | — |
| jpcert-fig4-caption | S041 | "図４ ウェブアプリケーションにおける脆弱性情報取扱いの全体フロー" | S041.txt:1331 | — |
| jpcert-finder-evidence | S041 | "「画面キャプチャ」、" | S041.txt:344 | — |

## Falsifiable rules

1. **Trigger rule.** Take a record's stated start date and compare it with the report date and the developer's first reply. If the record anchors the Japanese clock on either of those, it misstates 起算日: the definition is "…連絡を最初に試みた日を起算日とします。" (S041.txt:340), and IPA's step 5 relays that same date outward (S042.txt:145).
2. **Scope rule.** The 45-day figure belongs to the software-product track. `grep -c '45 日' corpus/source-snapshots/round-28/S041.txt` prints `2`, both inside chapter Ⅳ (S041.txt:648, 786); a record that applies a 45-day target to a web application contradicts the captures, whose web path has neither 起算日の連絡 nor 公表日の調整 (S042.txt:162-182) and whose guideline chapter has no 45-day figure (S041.txt:856-1150).
3. **Withdrawal rule.** A record claiming the non-disclosure request can be withdrawn before one year from 起算日 is falsified by "なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、" (S041.txt:305).

## Rejected over-generalizations

- **Rejected: "起算日 is the date IPA received the report."** It is the date JPCERT/CC first attempted the developer contact (S041.txt:340), which IPA then relays to the finder (S042.txt:145); the report date and the contact date are different steps — 1 and 5 of the product path.
- **Rejected: "Japan runs a fixed 45-day disclosure deadline."** The 45 days are 目安, subject to four stated considerations (S041.txt:648-653), changeable on the developer's request (S041.txt:660), and the publication can be called off on five grounds (S041.txt:662-671). A record that states 45 days as a deadline has dropped the capture's qualifier.
- **Rejected: "The web-application flow shares the product clock."** The web path has no 起算日 step and no publication-date adjustment (S042.txt:162-182), and 図４ contains no 起算日の連絡 box (S041.txt:1331) while 図３ contains four (S041.txt:1170, 1171, 1186, 1211).
- **Rejected: "This is the Japanese standard for coordinated disclosure."** It is IPA's and JPCERT/CC's operation of the 早期警戒パートナーシップ under a METI notification (S042.txt:130), and the guideline's advice is addressed to the finders, developers and site operators inside that partnership — for example its legal-points annex opens its finder section with "１－１．脆弱性関連情報の発見に際しての法的な問題" (S041.txt:1338) and asks finders for evidence such as "「画面キャプチャ」、" (S041.txt:344). It binds those parties, not coordinators elsewhere.

## Limits

- One capture per source, both taken 2026-10-25 with `corpus/instruments/capture-source.py`: S042 `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966` (HTML, 974 lines), S041 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47` (PDF via `pdftotext`, 2354 lines). The S041 bytes are identical to the round-26 capture, so the line anchors in `corpus/knowledge/iso-29147-and-30111-division-of-labour.md` still hold.
- The IPA page carries its own revision stamp, "最終更新日：2017年5月30日" (S042.txt:123); that is the page's revision date, not the programme's, and the guideline is the 2026年10月 edition.
- PDF figure text is extraction-ordered, not reading-ordered; 図２/図３/図４ are cited by caption and by the step headings the extractor separated, never quoted as continuous prose. The 起算日 definition is extracted as a footnote (S041.txt:340, note 4), separated from its body text, so it is quoted as that footnote.
- One quoted string is not unique: "「画面キャプチャ」、" occurs twice (S041.txt:344 in chapter Ⅳ's evidence footnote, S041.txt:929 in chapter Ⅴ's). L344 is the occurrence cited here; no `manifest.json` assertion pins this string, so its binding is the line number, not an exactly-once count.
- `source-recheck.py` accepts one `--source` per invocation (`corpus/instruments/source-recheck.py:275`), so the `recheck:` line chains two invocations instead of repeating the flag; `--source S041 --source S042` on a single invocation would silently re-derive only S042.
- The staged draft this entry adopts described the web path as "six-step". Both captures number seven — S042.txt:162-182 and 図４ at S041.txt:1331 — and the entry follows the captures. The staged draft also carried a `source:` line for the JPCERT/CC guideline under a package-local S043 id; that source is the lane's S041 (registered round 26), cited here under its lane id, not re-registered.
- Documentation-only: nothing here instructs contacting, probing, scanning, logging in to, or submitting against any system; both sources were read as public documents on 2026-10-25.
