# C2S037Quote — re-open S037 capture; verify quotes and absence of invitation-only claim

Seat: `L1Kasegi25.C2S037Quote` (UFO-FSD reviewer, wave 2 falsification, read-only).
Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Attacked items: `wave1/RevQuotesJP.md` §S037 + U3; `wave1/EntryJapanVendors.md` (Claim 5 /
rejection #5 / exactly-once table); `corpus/source-snapshots/round-25/manifest.json` S037
record; the live entry `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md`.

## Verdict

**Wave-1 result CONFIRMED — no correction needed.** All six manifest quotes are verbatim
substrings of the capture, each occurs exactly once and each lands on its declared line.
RevQuotesJP's six per-line S037 bindings are accurate. The capture contains no text
supporting an invitation-only / closed-programme reading, and the landed entry asserts
none — it states an account requirement plus an お申し込み (application) form and
explicitly *rejects* "invitation-only" as a staged-draft over-generalization.

## Evidence — commands, output, exits

### 1. Capture identity

```
$ sha256sum corpus/source-snapshots/round-25/S037.txt
b204aa7f60ec2e70713ecd8c605fb1adb6e39549f0ef09d32a297c10f473cb4c
```
Matches `manifest.json` S037.sha256 and `capture-log.txt` line 11 (fetched 2026-10-25T08:14:25Z,
status 200). `wc -l` = 294 lines.

### 2. Manifest quotes — exactly once, at declared lines

`grep -cF <quote>` over S037.txt (count | actual line | declared line):

| manifest id | count | line(s) | declared | verdict |
|---|---|---|---|---|
| Q1 `サイトによっては報奨金制度の対象外の可能性があります。` | 1 | 109 | :109 | OK |
| Q2 `報告にはアカウントが必要になります。` | 1 | 99 | :99 | OK |
| Q3 `お振込みまたは寄付のいずれかをお選びいただけます。` | 1 | 111 | :111 | OK |
| Q4 `いただいた報告が対応完了してから2ヶ月を経過した最終営業日にお支払いいたします。` | 1 | 115 | :115 | OK |
| Q5 `報告用サイトでは脆弱性検証を行わないでください。` | 1 | 123 | :123 | OK |
| Q6 `報告用サイトアカウントお申し込みフォームからお申込みください。` | 1 | 101 | :101 | OK |

End-to-end instrument confirmation:

```
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-25/manifest.json --source S037
S037:sha256 OK
S037:Q1 OK occurrences=1
S037:Q2 OK occurrences=1
S037:Q3 OK occurrences=1
S037:Q4 OK occurrences=1
S037:Q5 OK occurrences=1
S037:Q6 OK occurrences=1
exit=0
```

### 3. RevQuotesJP §S037 claim table — all six rows verified at the cited lines

```
$ grep -n '' S037.txt | sed -n '98,123p'
 99  A. …報告いただきます。報告にはアカウントが必要になります。   (account required — receipt L64)
 101 A. 報告用サイトアカウントお申し込みフォームからお申込みください。 (application form — L65)
 102 Q. 脆弱性報奨金制度に参加せずに報告したいのですが、どうしたら良いですか？ (explicit non-programme Q — L68)
 103 A. 脆弱性報告フォームからお申込みください。                    (non-programme route — L69)
 109 A. ご報告いただけます。ただし、…報奨金制度の対象製品をご確認ください。(pointer only — L66)
 115 A. いただいた報告が対応完了してから2ヶ月を経過した最終営業日にお支払いいたします。(payout timing — L67)
```
Each receipt sentence is a verbatim substring of its cited line. U3 upheld separately
below (§5).

### 4. Absence of invitation-only claim — capture sweep

```
$ for t in 招待 invitat invite 限定 クローズ closed 先着 抽選 審査 承認 許可 選ばれた 限られた 特定の のみが だけが 参加資格 登録制; do grep -cF "$t" S037.txt; done
→ 0 for every term
$ grep -c 招待 S036.txt S037.txt S038.txt S039.txt S040.txt → 0 0 0 0 0   (matches entry L196)
```
The only gating language in the capture is 報告にはアカウントが必要 (L99) +
お申し込みフォーム (L101) — an *application* regime, not an invitation regime.

### 5. U3 (target-product list) — receipt accurate

`報奨金制度の対象製品をご確認ください` at S037.txt:109 is a pointer; the list itself is
absent. Product names DO appear in the capture — S037.txt:192-194 and :266-268
(`kintone 全般 / Garoon 全般 / メールワイズ 全般`) — but both blocks are site navigation
under 制限事項 / サービスごとの連携ソリューション, not the bounty programme's scope list.
The receipt's bar ("may not name which products are in scope") stands.

### 6. Entry text — no invitation claim, quotes byte-identical

- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md:90-98` —
  "account-gated (S037:99) and account issuance runs through an application form (S037:101)";
  the negative assertion at :96-98 is reproduced and passes (`grep -c '招待'` = 0).
- Rejected over-generalization #5 at :195-199 — "Cybozu's bounty is invitation-only" is
  marked Rejected with the capture-based reason; accurate.
- Six entry blockquotes (:72,:75,:78,:81,:84,:87) each `grep -cF` = 1 in the capture at the
  annotated lines — matches EntryJapanVendors table rows S037 Q1–Q6.
- `grep -nEi '招待|invitat|invite'` on the entry → hits only at :96-98 and :195-198, all in
  the *negation*/rejection context; line 38's "only" is `package products only` (S036 scope).
- Staged-draft provenance confirmed: read-only source repo
  `/home/vgpnk/Projects/shokuknow/merge/kasegi/…/japanese-vendor-disclosure-policies-2026-10-23.md:37`
  reads "runs the programme **by invitation** with an account-gated reporting site" and :53
  "an invitation, a product list…" — exactly the over-claim the entry rejects.
- `source: S037` header (:4) cites :99-123; the four named topics (対象外 :109, 受け取り方法
  :111, 支払い時期 :115, 報告用サイト :119-123) all fall inside the range.

## Findings

None blocking. Two notes, not defects:

1. The capture's repeated product-name nav blocks (:192-194, :266-268) could tempt a future
   reader into treating `kintone/Garoon/メールワイズ 全般` as the bounty target list; U3's
   wording already forecloses this, and no wave-1 artifact made that error.
2. Claim 5's English gloss "the site is outside the programme" renders 報奨金制度の対象外
   (outside the *bounty* scope); the capture is ambiguous whether reporting still flows for
   non-eligible sites — L109's `ご報告いただけます` (you may report) supports the entry's
   "a report is welcome" reading. Supported as written; just don't extend it to "outside
   the disclosure policy".

## Residual risk / verification gaps

- Quote fidelity is to the pinned snapshot (sha-verified); freshness of the live cybozu.co.jp
  page was not re-fetched (same limit wave 1 stated — a captured-source comparison is not a
  fresh network check).
- "Invitation-only" absence is argued over the captured bytes only; the programme could be
  invitation-gated upstream on the linked application form page, which is not captured.
  The entry correctly scopes its claim to "these bytes".
- No installs or upgrades performed; no tool record to report.

Report: `.ufo/waves/round-25/wave2/C2S037Quote.md`
