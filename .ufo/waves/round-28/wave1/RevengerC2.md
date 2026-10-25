# RevengerC2 — F12 claim traceability (round-28 wave 1, run 7)

Seat: `RevengerC2` (revenger, leaf). Date: 2026-10-25 (UTC). Lane base: `c9f8b115…`
(claims freeze commit). Scope: trace every claim in the landed
`corpus/knowledge/japanese-domestic-disclosure-workflow.md` (entry) to its origin in the staged
package bytes (`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`)
and its re-grounded anchor in the round-28 captures
(`corpus/source-snapshots/round-28/S041.txt`, `S042.txt`). Name silent drops and unsupported new
claims.

## State at check time

- The entry was NOT landed when this seat was spawned; it landed (untracked,
  `git status --porcelain` → `?? corpus/knowledge/japanese-domestic-disclosure-workflow.md`)
  while the seat ran. This receipt therefore covers the **landed** entry (complete, 103 lines),
  not a skeleton. No PRE-STATE label needed; the re-run command is `N/A`.
- Captures landed: `S041.txt` (2354 lines, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`),
  `S042.txt` (974 lines, sha256 `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`).
  Both digests match `corpus/source-snapshots/round-28/manifest.json` pins; S041 bytes are
  identical to the round-26 capture (`sha256sum ../round-26/S041.txt` same digest).
- No subagents spawned (leaf seat).

## Claim-traceability table (landed entry claim → staged origin → capture anchor → quote match)

Every quote in the entry's quoted record was re-located in the captures by this seat (grep +
region reads); all match verbatim at the cited line. "λ" = the claim is an interpretation/editorial
framing, not a verbatim quote requirement.

| # | Landed entry claim (line) | Staged origin (staged line) | Capture anchor | Quote match |
|---|---|---|---|---|
| H1 | `source: S041` header (L3) | staged L5 `source: S043` (JPCERT/CC guideline) | `S041.txt:340,648,658,430,1157,1281,1331` | yes — id remapped S043→S041 (lane id; staged S043 = lane S041, round-26). Header locations re-opened: L340 = 起算日 footnote 4 definition; L648 = 45日目安; L658 = 公表日決定後の対応; L430 = 11) 取下げ; L1157/L1281/L1331 = 付録2 図３/図４ captions. All verified present. |
| H2 | `source: S042` header (L4) | staged L4 `source: S042 – … step 5 起算日の連絡` | `S042.txt:123,144-145,133-159,162-182,184-200` | yes — 最終更新日 2017年5月30日 at :123; software steps 1.–10. at :133–159 (5.起算日の連絡 :144–145); web steps 1.–7. at :162–182; self steps 1.–8. at :184–200. Header expands anchors beyond staged (staged named only step 5). |
| H3 | `verified-at: 2026-10-25` | staged `verified-at: 2026-10-23` | — | n/a — date updated to today (capture date, manifest purpose says both captured 2026-10-25). |
| H4 | `recheck:` single executable cwd-independent line (L6) | staged L7 curl+`pdftotext` hybrid (prose+command, Q10-nonconforming) | — | n/a — staged recheck replaced with two chained `source-recheck.py --source S041/--source S042` invocations (Q10-conformant; `bash -n` parses; carries `cd <lane-root> &&`). |
| H5 | `ground: F12` (L7) | staged L8 `ground: F13 (new frontier item; extends F02)` | — | n/a — lane frontier row is F12 (staged package used its own F-numbering; adopted as F12 per claims.json C2, README F12 row). |
| M1 | adopt-staged/re-grounded statement (L7) | MERGE-REPORT.md adopt checklist items 3–4; staged entry | — | n/a — meta-claim. |
| C1 | state-coordinated pipeline; IPA = designated intake body; JPCERT/CC contacts developer, runs publication adjustment (L11) | staged L12–15 ("Japan runs a state-coordinated… flow … no marketplace, no bounty, no per-finding severity ratchet") | `S042.txt:130` ("2004年7月8日から経済産業省の告示に基づき…"), `S042.txt:131` (IPA は、届出受付機関として…) | yes for the coordination half (both quotes match). The **negative** half — "no marketplace, no bounty, no per-finding severity ratchet" — has NO capture anchor: `grep` for 報奨金/バウンティ returns 0 in both captures (S041 0, S042 0; S042's only 重要度 hit at :765 is unrelated page furniture). Retained as contrastive framing, not as a source-backed claim (Q4: a negative claim about "Western platforms" is not sourced). Flagged unsupported-as-cited (interpretive). |
| C2 | software-product path = ten numbered steps 1.–10. (L15–17) | staged L17–21 (9-step flow: 1 発見者はIPAに脆弱性関連情報を届け出る … 9 IPAは四半期ごとに統計情報を公表) | `S042.txt:133-159` (IPA numbering 1.–10.); `S041.txt:1281` (図３ caption), `S041.txt:1157` (付録2 scope line) | yes — S042 numbers the product path 1.–10. (steps at :133,136,138,140,144,146,152,154,157,159; verified 10. 統計情報の公表 at :159). **Staged origin conflated the guideline's 図1 9-step overview (S041.txt:212/249) with the IPA page's 10-step process; the landed entry corrected this by citing IPA's numbering + 図３ (S041.txt:1281).** Claim re-grounded; the staged "9-step" count is a corrected defect, not a drop. |
| C3 | 起算日 definition — first attempt at Ⅳ．４．2) contact, not receipt/acknowledgement (L21) | staged L23–29 (2026 guideline defines 起算日 precisely, footnote 4: the day the notification specified in Ⅳ．4.2) was first attempted; clock anchored on first attempted contact, not acknowledgement, not submission) | `S041.txt:340` (「本ガイドラインのⅣ．４．2)において規定された連絡を最初に試みた日を起算日とします。」) | yes — verbatim (manifest S041 Q1). S041.txt:305 carries the footnote marker "起算日4"; the footnote text is at :340. |
| C4 | IPA step 5 relays 起算日 both directions (L23) | staged L24–25 (JPCERT/CC tells IPA when it began contacting the developer; IPA tells the finder both the 起算日 and the date details were sent) | `S042.txt:145` (「JPCERT/CC は製品開発者への連絡を開始した旨（起算日）…IPAは起算日、および、詳細情報連絡日を発見者へ連絡します。」) | yes — verbatim (manifest S042 Q1). |
| C5 | one-year withdrawal rule; finder may ask IPA to withdraw non-disclosure request once 起算日 has passed (L27) | staged L37–38 (A finder who has filed an information non-disclosure request may ask IPA to withdraw it once one year has passed since 起算日) | `S041.txt:305-306` (「なお、起算日4から 1 年以上経過した届出については、発見者は IPA に対し、」「情報非開示依頼の取り下げを求めることができます。」) | yes — verbatim (manifest S041 Q6). Landed adds the operative repetition (S041.txt:430–431, 11) 情報非開示依頼の取下げ) and a precision note (withdrawn = the request, not the report). Semantic fix: staged said the finder "has filed" the request; the capture shows the request runs TO the finder (S041.txt:293, 903-904), and the finder asks for its withdrawal. |
| C6 | legal-points annex + evidence items (検証コード/画面キャプチャ/ログ), care re statutes (L93) | staged L40–43 (付録3 法的な論点について (p.36) gives finders, developers and site operators their own legal-points appendix; guideline tells finders to attach 検証コード, 画面キャプチャ or ログ while taking care not to touch related statutes) | `S041.txt:1333` (付録３ 法的な論点について), `S041.txt:1336` (１ 発見者が心得ておくべき法的な論点), `S041.txt:1338` (１－１．脆弱性関連情報の発見に際しての法的な問題), `S041.txt:344` (「画面キャプチャ」、) | yes — annex title verified at :1333; finder/developer/site-operator sub-headings verified at :1336 (finder), :38-40 ToC (developer :38, site operator :39); evidence items at :342/344 (検証コード/画面キャプチャ) and :927/929 (chapter Ⅴ counterpart); statute-caution at :275-276 ("関連法令に触れることがないよう留意してください") and :321-322. **Staged page ref "p.36" dropped; anchored to annex title + ss instead (PDF page numbers are not line-stable).** |
| C7 | web path lighter — seven steps, counterparty ウェブサイト運営者, ends 取扱い開始連絡/修正完了の連絡 (L29–33) | staged L45–48 (six-step flow; ends in 取扱い開始連絡 and 修正完了の連絡 rather than a negotiated publication date) | `S042.txt:162-182` (web steps 1.–7.: 1 :162, 2 :165, 3 :167, 4 :170, 5 :172, 6 :179, 7 :181) | yes for the seven-step count — **staged said six; the capture shows seven (verified `awk` count = 7), the entry follows the capture and says so at L102.** The staged "ends in 取扱い開始連絡 and 修正完了の連絡" is a partially-correct reading: those are steps 4 and 6, but the flow does not END there — step 7 is 統計情報の公表 (S042.txt:181-182). Landed entry states the actual ending (statistics with site-suppression at :182). No silent drop: the staged six-step claim is explicitly named as corrected (L102). |
| C8 | why-it-matters — 起算日 transferable artefact, clock start even if developer never answers, both sides see same date (L43) | staged L52–55 (起算日 is the single most transferable artefact; disclosure-clock start date both sides can see, survives a stalled negotiation; anchored on attempt not response) | `S042.txt:145` (IPA relays 起算日 to the finder) | partial — the "trigger is an attempt, so the clock starts even if the developer never answers" reading follows from S041.txt:340 (attempt-based definition) and is supported; "both sides can see the same date" is supported only for the finder side (IPA relays to the finder; the capture does not show the developer receiving the date back). Marked **partially supported / interpretive** (the developer-visibility half is not capture-backed). The F02 cross-reference (coordinator/trigger/interval/extension rule) is a lane-internal citation, not a capture. |
| N1 | "IPA dates the arrangement to a Ministry of Economy, Trade and Industry notification" (L11) | staged: no such sentence (staged mentions 経済産業省 only via IPA page context) | `S042.txt:130` | yes — new claim, capture-anchored (`2004年7月8日から経済産業省の告示に基づき`), supported. |
| N2 | 45-day 目安 target from 起算日 + four considerations + pubdate-change + five grounds (L25) | staged: absent (staged negotiated-schedule claim cited leak-risk/time-to-mitigate but not the 45-day number or the grounds) | `S041.txt:648` (「…から 45 日後を目安とします。ただし、」), `S041.txt:649` (「公表日の決定に際しては、以下の点も考慮します。」), `S041.txt:650-653` (① 対策方法の作成に要する期間…④ 当該脆弱性の悪用に関するリスク), `S041.txt:660` (「公表日を変更することがあります。」), `S041.txt:662-671` ((ア)–(オ) five grounds) | yes — new claim, capture-anchored, supported. |
| N3 | IPA explanation requirement when developer needs more time (L27) | staged: absent | `S041.txt:431-433` (「そのとき、製品開発者が正当な理由により対応に時間を要する場合、IPA はその状況を発見者に適切に説明し、…」) | yes — new claim, capture-anchored, supported. |
| N4 | web path lacks clock apparatus; JPCERT/CC absent from seven steps; chapter Ⅴ has no 起算日/no 45-day; 図３ has four 起算日の連絡 boxes, 図４ none; 図２ numbers five steps (L35) | staged: absent (staged only said "parallel, lighter path") | `S042.txt:162-182` (no 起算日/公表日 steps; no JPCERT/CC), `S041.txt:856-886` (chapter Ⅴ overview 図２ five steps), `S041.txt:1170,1171,1186,1211` (four 起算日の連絡 boxes in 図３), `S041.txt:1331` (図４ caption), 45日 occurrences at `S041.txt:648,786` (both chapter Ⅳ; `grep -c '45 日'` = 2) | yes — new claim, capture-anchored, supported (verified: chapter Ⅴ spans :856–1154 and contains no 起算日 line and no 45日 line; the only 45日 lines are 648/786 inside chapter Ⅳ). |
| N5 | self-report path — eight steps (L39) | staged: absent | `S042.txt:184-200` (self steps 1.–8.; 8.統計情報の公表 at :200) | yes — new claim, capture-anchored, supported. |
| N6 | quoted-record table + Limits: S041 bytes identical to round-26 capture (L97) | staged: absent | `sha256sum ../round-26/S041.txt` = e18acbf9… (same as round-28 S041) | yes — new meta-claim, verified by digest comparison. |
| N7 | `source-recheck.py` accepts one `--source` per invocation (L101) | staged: absent | `corpus/instruments/source-recheck.py:275` (`parser.add_argument("--source", help="check one source ID from the manifest")`; `--selftest` returns 2 if manifest/source given) | yes — new meta-claim, verified against instrument source. |

## Silent drops / unsupported claims

1. **Staged "developer may notify users before the publication date" (staged L34–35)** — ABSENT
   from the landed entry. `grep -n '公表日以前\|製品利用者' <landed entry>` → no hits. This
   claim WAS capture-supported (S041.txt:229–234 and :260–262: 「公表日以前に製品利用者に脆弱性検証の…通知することができる」).
   It is a **silent drop** of a staged claim that had a valid anchor. Not a defect in the
   re-grounded entry's accuracy (the entry does not contradict it — it simply omits it), but it
   violates the no-silent-drop rule. Flagged.
2. **Negative contrast "no marketplace, no bounty, no per-finding severity ratchet" (staged
   L12–14, retained at landed L11)** — retained in the landed entry but has NO capture anchor
   (see C1). The entry does not claim it as a quoted source; nonetheless as a "new/retained
   claim without a capture anchor" it is **unsupported-as-cited** and should either be labelled
   interpretive or dropped.
3. **C8 "both sides can see the same date"** — developer-visibility half has no capture anchor
   (only the finder-receipt half does). Partially supported as written; see C8.

## Verdicts

- All verbatim quotes in the entry's quoted record: **match** at the cited capture lines (each
  re-opened by grep/region read; manifest pins Q1–Q6 for S041 and S042 correspond to the entry's
  table rows and all verified).
- Staged claims → landed: fully re-grounded (C3, C4, C5, C6, C7, C8) or corrected with the
  correction named (C2 9→10-step, C7 six→seven-step, C5 request-direction, C6 p.36→annex
  anchor). No staged claim survived unsupported except the two flags above (C1 negative contrast,
  C8 half).
- New claims N1–N7: all capture-anchored and verified.
- **One defect named: silent drop of the staged pre-publication notify-users claim (S041.txt:229-234/260-262).**
- **One unsupported-as-cited claim named: the "no marketplace/no bounty/no severity ratchet" negative contrast (C1).**
- **One partially-supported claim: C8 developer-visibility half.**
- C2 anti-meta checks (entry's declared source ids = recheck `--source` ids; id present in
  manifest; quote assertions pinned): `source:` declares S041+S042; `recheck:` runs
  `--source S041` and `--source S042` against `corpus/source-snapshots/round-28/manifest.json` —
  ids equal, both present. (Run exit not re-executed by this seat: that is the executor's
  check; unit quote-match verification is this seat's.)

## Re-run commands for L1 (post-verify, at lane root)

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S042
```

(The landed entry was not present at seat spawn; it landed during the run. This receipt is
post-landing, so no PRE-STATE re-run is needed — the two commands above are the L1
paranoid re-verify.)
