# C2 admission attack — F12 (2026-10-25)

## Verdict
**Admission survives the four tested grounds; one fixable silent-drop defect remains.** The strongest objection is (d): the staged entry’s pre-publication user-notification claim was silently omitted from the re-grounded entry. This is a completeness/re-grounding defect, not evidence that the F12 core is unsupported or duplicate. Smallest correction: restore the bounded notification claim with its S041 anchor, or explicitly disclose its omission in Limits/round notes. No admission-kill evidence found on (a)–(c).

## (a) Is 起算日 supported by both captures?
Yes, but the two captures support complementary halves; neither should be credited with the other's wording.

- **IPA capture S042, lines 144–145:** `5.起算日の連絡` and `JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。` This directly supports the coordinator-to-IPA-to-finder relay.
- **Guideline capture S041, line 340:** `本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。` This defines the anchor as first attempted developer contact.
- **Clock consequence, S041 lines 647–653:** `...連絡を最初に試みた日（起算日、２．注釈 4 を参照）から 45 日後を目安とします。ただし、` followed by the publication-date factors, including mitigation time, overseas coordination time, leak risk, and exploitation risk. Thus S041 supplies the clock/interval and S042 supplies the relay. The landed entry correctly attributes each.
- **Manifest:** round-28 SHA-256 pins matched both captures; all 12 declared manifest quote assertions were exactly-once in their respective capture (S041 Q1–Q6, S042 Q1–Q6). The entry’s recheck line invokes `source-recheck.py` for S041 and S042.

Therefore, an attack that demands each capture independently state the whole composite claim fails; the entry expressly uses both. Do not say S042 independently establishes a 45-day clock: it does not.

## (b) Duplicate F11 ground?
No. F11’s two entries use S041’s 付録6 to compare ISO/IEC 29147/30111 division of labour and clause/conformance divergence. F12 uses S041’s Ⅳ handling chapter / 付録2 flow figures and S042’s IPA process page to record the Japanese intake path, 起算日 and differentiated product/web/self-report flows. Shared document S041 is not shared claim ground. README F12 also explicitly relates the entry to F02’s timeline rule: F02 sources are CISA/CERT/CC/Project Zero policies; F12 adds the Japanese first-attempt trigger, contrasted with S004’s report-date trigger. The landed F02 entry’s rule asks for coordinator, clock event, interval, patch/publication relation, and exceptions; F12 fills the distinct Japanese example rather than restating F02.

I could not obtain ScribeStagedCompare’s map before this receipt; the comparison above is independently grounded in the live F02/F11 entries and S041 section anchors. No waiting/polling performed.

## (c) Is S042 tier A justified?
Yes for this narrow claim. S042 is IPA’s own process page, explicitly labels IPA the `届出受付機関` (L131), and gives the institution’s own numbered procedures, including the JPCERT/CC-to-IPA-to-finder date relay (L144–145). The page’s revision stamp is 2017-05-30 (L123), which the landed entry records as the page revision date; age alone does not make this primary statement a secondary explainer. Registry now records S042 as `docs | A`, mined, opened 2026-10-25, recheck 180d, used-by exactly the F12 entry. The staged row’s inaccurate web-app “steps 1 to 6” was corrected to seven steps in the lane row/entry. A tier-B downgrade would weaken provenance without evidence that IPA is not speaking for its own process.

## (d) Staged skeleton claim silently dropped?
**Yes: pre-publication user notification.** The staged entry says in its 9-step flow: `製品開発者は、製品利用者に生じるリスクを低減できると判断した場合、JPCERT/CCと調整した上で、公表日以前に製品利用者に脆弱性検証の結果及び対応状況について通知することができる` (staged package entry under `/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`, “flow” section). It separately says the developer may notify users before publication. The landed entry’s 10-step IPA path at lines 15–17 omits this claim, and its Why-it-matters / Rejected / Limits sections do not disclose that omission.

This was not an unsupported staged assertion: S041 round-28 capture lines 229–234 says `製品開発者は、製品利用者に生じるリスクを低減できると判断した場合、JPCERT/CCと調整した上で、公表日以前に製品利用者に脆弱性検証の結果及び対応状況について通知することができる`. The adjacent note at L245–248 explains when full user notification can count as equivalent to public disclosure. This is a substantive, source-supported option, distinct from priority pre-release information provision to critical-infrastructure operators at S041 L434–440 and from IPA’s S042 L156 statement. Restore the bounded claim with S041 L229–234 (and note the conditions), or explicitly record its exclusion; do not silently conflate it with priority disclosure.

Other staged claims checked: the 起算日 definition, coordinator relay, 45-day *目安*, one-year withdrawal of the non-disclosure request (not the report), legal appendix/evidence/care about related laws, and web-application path are retained in the re-grounded entry. The staged “Figure 1” attribution was corrected: S041 L212–249 is the software-product overview (図1), while the detailed product/web flows are 付録2 図3/図4 (landed entry L15, L35). The staged web-path step count (six) was also corrected to seven. The landed entry adds the self-report path. These are corrections/additions, not silent claim loss.

## Evidence timing / rerun
The lane entry, S042 registry row, F12 README row, and round-28 manifest were present when inspected. Re-run after final landing: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042 && python3 corpus/instruments/frontier-recheck-count.py`.
