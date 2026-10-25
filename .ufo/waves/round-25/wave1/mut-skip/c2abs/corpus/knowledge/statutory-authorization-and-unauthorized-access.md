# Statutory authorisation and unauthorised access (Japan)
source: S033 — https://laws.e-gov.go.jp/api/1/lawdata/411AC0000000128 — 法令 ID 411AC0000000128, 平成十一年法律第百二十八号; Article Num="2" Paragraph Num="4" Items 1–3, Article Num="3", Article Num="11", and the supplementary provisions; fetched 2026-10-25
source: S034 — https://www.soumu.go.jp/main_sosiki/cybersecurity/kokumin/basic/legal/09/ — the page's （罰則）第十一条 block; page footer © 2009 総務省
source: S035 — https://www.npa.go.jp/bureau/cyber/pdf/1_kaisetsu.pdf — §3 不正アクセス行為の禁止、処罰（第２条第４項、第３条、第11条関係）; PDF pages 2, 6 and 7; no publication date in the file metadata
verified-at: 2026-10-25
recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && true
ground: F09 — authorisation that exists outside a platform's safe-harbour text; extends F03, which attributes a safe-harbour statement to the party granting it

## Rule

Three checks a reviewer can run against a report or claim package:

1. **Consent-holder test.** For conduct shaped like 第二条第四項第二号 or 第三号 (evading an access-control restriction), the statutory exclusion requires the consent of the アクセス管理者 of the affected computer. The consent of the account or identification-symbol holder excludes only 第一号 conduct, and only the use of that symbol. Check: for each in-scope asset, does the package name the party that administers the affected computer, and is the recorded grant that party's? If the granting party is a different party, statutory consent is not established — record it unknown.
2. **Channel test.** The conduct must input a symbol, information or instruction *over a telecommunications line* into a networked computer and bring about a state in which the restricted use is possible. Console or offline use is outside the definition (S035, p.7), so a report describing direct console operation does not describe 不正アクセス行為.
3. **Penalty-quote test.** 第十一条 reads 三年以下の拘禁刑又は百万円以下の罰金 in the consolidated text (S033). A package that quotes 懲役 for 第十一条 is quoting a page that has not been updated (S034, S035), not the current statute.

## What the statute makes criminal

The prohibition is S033 第三条: “何人も、不正アクセス行為をしてはならない” (20字). The penalised act is therefore not “unauthorised access” in the abstract but the defined 不正アクセス行為, whose elements sit in 第二条第四項 as three items, each requiring input over a telecommunications line, operation of the affected computer, and the creation of a state in which the restricted 特定利用 can be performed:

- **第一号** — inputting *another person's* identification symbol;
- **第二号** — inputting information (other than an identification symbol) or an instruction that evades the restriction;
- **第三号** — inputting such information or an instruction into another connected computer whose access-control function restricts this computer's use.

S035 §3 (p.7) restates this as four cumulative conditions (a networked 特定電子計算機, access through the network, a symbol or evasion information/instruction input, and a restricted-use-capable state reached), and adds that the required element is the state in which the restricted use is possible — conduct that goes on to perform the use is included. S035 does not create these elements; it is the National Police Agency's official commentary on the statutory text and is cited here as interpretation.

## The consent carve-out

The carve-out is drafted inside the definition, not as a defence:

- 第一号 excludes acts by “the アクセス管理者 who added the access-control function” and acts done with the consent of the アクセス管理者 **or** of the identification-symbol holder: “アクセス管理者又は当該識別符号に係る利用権者の承諾” (25字), S033 第二条第四項第一号括弧書.
- 第二号 excludes the same manager acts and acts with the manager's consent only: “当該アクセス管理者の承諾を得てするものを除く” (22字), S033 第二条第四項第二号括弧書.
- 第三号 inherits 第二号's exclusion by reference: “次号において同じ” (8字), S033 第二条第四項第二号括弧書末尾.

So the two consent sources are not interchangeable. An account holder can consent to another party using *their* symbol (第一号); only the アクセス管理者 can consent to conduct that evades the access-control restriction itself (第二号, 第三号). S035 §3(1) (p.6) gives the reason for the exclusion — legitimate use such as “コンピュータのセキュリティ・チェックを実施する場合” (25字) — and S035 §3(2) (p.7) repeats the manager-only exclusion for the exploit-shaped items: “その承諾を得た者が行う場合は禁止の対象から除外” (23字).

The consenting party is the **アクセス管理者**, defined in S033 第二条第一項 as “当該特定電子計算機の動作を管理する者” (18字) — the party that manages the operation of the computer for its networked use. S035 §2(1) (p.2) states that this may be a corporation as well as a natural person (“アクセス管理者は個人、法人の別を問いません”, 21字) and that one computer can have more than one アクセス管理者 (“２以上のアクセス管理者”, 11字). Which manager's consent counts therefore depends on which 特定利用 is at issue, not on who owns the hardware.

## Why a platform's safe-harbour text is not the legal definition

The statutory question is whether the アクセス管理者 of *that* computer consented to *that* conduct. A safe-harbour statement is a grantor's statement about its own posture and the scope it covers; it answers a different question and only bears on the statutory one through two conditions that must both hold:

1. the grantor is the アクセス管理者 of the affected computer for the affected 特定利用 (S035 p.2 records several managers for one computer, so which uses a grantor manages has to be established per asset); and
2. the statement actually consents to the conduct in question, rather than promising not to pursue a category of research.

Where the asset is operated by a third party (a customer, a supplier, a hosting tenant), the platform's text cannot supply that third party's consent, however broad its wording. Where the grantor is the manager but its scope list excludes the asset or method, condition 2 fails. Either failure leaves the statutory exclusion unestablished — and neither failure is visible from the badge or the safe-harbour paragraph alone, which is why F03's rule (check the asset scope separately) and this entry's consent-holder test are both needed. This section is this entry's reading of S033 with S035; S035 does not itself discuss safe-harbour text, and no court holding on the point was opened this round.

## Which text is authority for the penalty, and the divergence

**S033 is the authority**: it is the official 法令標準XML consolidated text served by the e-Gov lawdata endpoint under the law's own id, and its 第十一条 attaches the penalty to a breach of 第三条 (“第三条の規定に違反した者は”, 13字) as “三年以下の拘禁刑又は百万円以下の罰金に処する” (22字). The same document contains 拘禁刑 twice, in 第十一条 and 第十二条, and the string 懲役 zero times.

Both secondary documents diverge in the same direction:

- **S034 (MIC citizen page, tier B, footer © 2009)** prints “三年以下の懲役又は百万円以下の罰金に処する” (21字) in its （罰則）第十一条 block.
- **S035 (NPA commentary, p.6)** prints “３年以下の懲役又は100万円以下” (16字) in §3.

So the divergence is not a typo in one page: two government explainers still carry the pre-amendment 懲役 wording while the consolidated text carries 拘禁刑. The e-Gov document's own supplementary provisions are drafted against the Penal Code amendment (“刑法等一部改正法施行日から施行する”, 17字), which is consistent with the newer wording being the 拘禁刑 one, but **the amending act itself was not opened this round** (see Limits): the direction of the divergence is established by the consolidated text, not by reading the amendment.

## Evidence

- S033, 第二条第一項: “当該特定電子計算機の動作を管理する者” (18字) — the アクセス管理者 is defined by managing the computer's operation, not by owning it.
- S033, 第二条第四項第一号括弧書: “アクセス管理者又は当該識別符号に係る利用権者の承諾” (25字) — two possible consenting parties for symbol-based conduct.
- S033, 第二条第四項第二号括弧書: “当該アクセス管理者の承諾を得てするものを除く” (22字) — manager consent only for evasion conduct.
- S033, 第二条第四項第二号括弧書末尾: “次号において同じ” (8字) — 第三号 inherits that exclusion.
- S033, 第三条: “何人も、不正アクセス行為をしてはならない” (20字) — the prohibition the penalty attaches to.
- S033, 第十一条: “第三条の規定に違反した者は” (13字) and “三年以下の拘禁刑又は百万円以下の罰金に処する” (22字).
- S033, supplementary provisions: “刑法等一部改正法施行日から施行する” (17字) — the text is coordinated with the Penal Code amendment.
- S034, （罰則）第十一条: “三年以下の懲役又は百万円以下の罰金に処する” (21字) — the MIC page's stale wording.
- S035, §3, p.6: “３年以下の懲役又は100万円以下” (16字) — the NPA commentary's stale wording, writing the amount as 100万円 rather than 百万円.
- S035, §3(1), p.6: “コンピュータのセキュリティ・チェックを実施する場合” (25字) — the stated rationale for the consent exclusion.
- S035, §3(2), p.7: “その承諾を得た者が行う場合は禁止の対象から除外” (23字) — the manager-only exclusion for 第二号/第三号 conduct.
- S035, §2(1), p.2: “アクセス管理者は個人、法人の別を問いません” (21字) and “２以上のアクセス管理者” (11字) — corporate managers, and several managers per computer.

Each Japanese quote above is a contiguous substring of its document under whitespace-collapsing normalization and occurs once in that document; character counts are the author's own.

## Kasegi use

Apply the consent-holder test at the same step as SKILL.md's “Program-rule checklist (step 1 of any mission)”: the checklist already records the verbatim testing grant and the exact assets. Add one field to that record — the party that administers each in-scope computer — because the statutory exclusion turns on that party's consent, not on the platform's wording alone.

Use the channel test when a report describes how the finding was reached: if the steps are console or offline operations, the described conduct is outside 第二条第四項 and the report should not borrow the statute's vocabulary for it.

Use the penalty-quote test before citing the offence in a package: quote S033's wording, or label the MIC or NPA page as carrying pre-amendment wording rather than silently mixing the two.

## Rejected

- **Rejected: “A safe-harbour statement makes the described research authorised in law.”** The statutory exclusion requires the アクセス管理者's consent (第二号, 第三号) and, for 第一号, the manager's or the symbol holder's consent; a safe-harbour paragraph promises the grantor's own posture and may be issued by a party that does not administer the affected computer. F03 already shows a platform's safe harbour does not change program scope; the statutory point is separate and narrower — the badge is neither the definition nor, by itself, the consent.
- **Rejected: “The account holder's consent authorises exploit testing of that account's service.”** 第一号's two-party consent does not extend to 第二号/第三号; those items exclude only the manager's consent, and 第三号 inherits that by “次号において同じ” (8字).
- **Rejected: “懲役 and 拘禁刑 are interchangeable, so any government page can be quoted.”** The consolidated text contains 拘禁刑 twice and 懲役 zero times while both explainers print 懲役; a citation mixing them misstates at least one document's current wording.
- **Rejected: “The MIC page is the safer citation because it is written for citizens.”** It is the least current of the three on the penalty (footer © 2009, tier B); it remains useful as a plain-language reproduction of the definition, and its reproduction of 第二条第四項 agrees with S033.

## Limits — what this entry does not cover

- **The Chinese half is not covered.** The package entry this one derives from (`statutory-authorization-in-three-traditions.md`) records that the official text of 刑法 第285条 (非法侵入计算机信息系统罪) could not be opened in its round and points to its own `CANNOT-ANSWER.md`; no substitute was admitted here, so this entry documents one tradition and names the other as an open item rather than generalising across “three traditions”. The package's separate Chinese-thresholds entry is outside this seat and was not adopted.
- **No case law.** No court decision interpreting the scope of 承諾, the identity of the アクセス管理者 for hosted assets, or the boundary between 第一号 and 第二号 was opened; the consent-holder test is a reading of the statutory text and the NPA commentary.
- **No amending act.** 刑法等の一部を改正する法律 was not opened; the 拘禁刑/懲役 divergence is disclosed from the consolidated text and the two explainers, not from the amendment's own commencement provision.
- **Only 第三条 and 第十一条 are treated.** 第四条 (符号の不正取得), 第五条 (助長行為), 第六条 (不正保管) and 第七条 (入力の不正要求), and their penalties in 第十二条, are outside this entry, as are civil liability, provider liability and evidentiary questions.
- **It does not decide whether a particular platform is the アクセス管理者 of a particular asset.** That is a per-asset finding; where it is unknown, the entry's rule requires it to stay unknown.
- **Documentation-only.** This entry instructs no testing, scanning, login or submission against any system; all three sources were read as public documents on 2026-10-25.
