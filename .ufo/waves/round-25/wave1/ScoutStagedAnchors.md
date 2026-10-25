# Scout: staged `anchor` cells vs committed captures (round 25, wave 1)

Question: do the `anchor` cells of staged rows S055, S056, S057, S060, S068 in
`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` resolve to real headings/content in the
matching committed captures? READ-ONLY seat; nothing outside this file was written.

## Method

- Staged rows read from `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (lines 31, 32, 33,
  36, 44).
- Staged id → lane capture mapping is authoritative from
  `kasegi-shokunin/.ufo/waves/round-25/capture-log.txt` (document table): S055→S036, S056→S037,
  S057→S038, S060→S039, S068→S040.
- Captures read at `kasegi-shokunin/corpus/source-snapshots/round-25/{S036..S040}.txt` (all five present,
  sha256 recorded in capture-log.txt). Line numbers below are lines of those capture files.
- Each anchor fragment was matched literally (`grep -n`, anchored to heading position where the capture has
  one heading per line) and then confirmed by reading the surrounding lines. No re-fetch, no re-capture.

## Result table

| staged id | anchor cell (as staged) | capture | found / NOT FOUND |
|---|---|---|---|
| S055 | `sections 脆弱性対応 → 対象範囲 / 脆弱性対応フロー 1 情報収集・2 影響の確認・3 対策, and 脆弱性情報の公開 → 対象範囲 / 2 JVNでの公開` | S036.txt (Cybozu 脆弱性情報ハンドリングポリシー) | ALL FOUND — `脆弱性対応` L12; `対象範囲` L13 (under 脆弱性対応) and L27 (under 脆弱性情報の公開); `脆弱性対応フロー` L16; `1. 情報収集` L17; `2. 影響の確認` L20; `3. 対策` L24; `脆弱性情報の公開` L26; `2. JVNでの公開` L43 |
| S056 | `FAQ items 「脆弱性を見つけたので報告したいのですが、どうしたら良いですか？」, 「脆弱性報奨金制度に参加せずに報告したいのですが？」, 「Webサイトの脆弱性を見つけました。報告しても良いですか？」, 「報奨金はいつ支払われますか？」` | S037.txt (Cybozu FAQ 脆弱性報奨金制度) | 3 of 4 FOUND, 1 NOT FOUND — L98 `Q. 脆弱性を見つけたので報告したいのですが、どうしたら良いですか？`; **NOT FOUND** `脆弱性報奨金制度に参加せずに報告したいのですが？` (0 literal hits; the capture's item is L102 `Q. 脆弱性報奨金制度に参加せずに報告したいのですが、どうしたら良いですか？`); L108 `Q. Webサイトの脆弱性を見つけました。報告しても良いですか？`; L114 `Q. 報奨金はいつ支払われますか？` |
| S057 | `sections 脆弱性報告制度 / 脆弱性の評価について / 脆弱性の検証目的であっても、以下の行為については禁止いたします 1・2` | S038.txt (GMO Pepabo 脆弱性報告制度) | ALL FOUND — `脆弱性報告制度` L12 (page title) and L14 (section heading); `脆弱性の評価について` L18; `脆弱性の検証目的であっても、以下の行為については禁止いたします` L23, with items `1.DoS攻撃、DoS攻撃に該当する検証` L24 and `2.自分自身のアカウントや情報以外へのアクセス、改ざんを試みるなどの行為` L25 |
| S060 | `body paragraphs describing the product-vendor IRT focus and the coordinated-report case for findings that affect another vendor's product` | S039.txt (日立 HIRT-PUB10008) | TOO VAGUE TO CHECK as a heading — names no section/heading. Content does exist: `製品ベンダIRT` focus at L490–L491 (intro, before `1. 製品脆弱性情報の開示プロセス` L494) and the coordinated-report case at L506 (`…他社製品に影響することがわかった)場合には、情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで、協調した脆弱性対策を開始します。`) under `1.2 脆弱性情報の入手 ... (1)` L503 |
| S068 | `sections "Cisco Product Security Incident Response", the third-party coordination paragraph, and "Disclosure of Security Vulnerabilities"` | S040.txt (Cisco Security Vulnerability Policy) | ALL FOUND — `Cisco Product Security Incident Response` L56 (body heading; L17 is the same text in the TOC); third-party coordination paragraph `Incidents that may impact other vendors:` L184–L190 (CERT/CC, CERT-FI, JP-CERT, NPSA); `Disclosure of Security Vulnerabilities` L299 (body heading; L28 TOC) |

## Verdict per row (rewrite before append?)

| staged id | verdict |
|---|---|
| S055 | **No rewrite required.** All four named targets are real headings at the cited structural positions; only cosmetic difference is the anchor writing `1 情報収集` without the capture's `1. ` period. |
| S056 | **MUST rewrite.** The second quoted FAQ item is a truncated paraphrase that does not occur in the capture; replace with the verbatim `脆弱性報奨金制度に参加せずに報告したいのですが、どうしたら良いですか？` (L102). The other three items are verbatim. |
| S057 | **No rewrite required.** All three named targets, including the prohibition heading and its items 1 and 2, are verbatim headings. |
| S060 | **SHOULD rewrite.** The anchor names no heading, so it cannot be checked as a heading; point it at `1.2 脆弱性情報の入手 ... (1)` (L503) plus the L506 sentence, or at the intro paragraphs L490–L491. Substantively supported either way. |
| S068 | **No rewrite required.** All three named targets resolve (L56, L184–L190, L299). |

## Side note (not an anchor defect, flagged for the row owner)

S068's summary column asserts the policy "states the two conditions under which it will accelerate
disclosure", while S040's `Disclosure of Security Vulnerabilities` section lists **four** bullets
(L301–L309: high-severity fix planned; observed active exploitation; potential increased public awareness;
third-party vulnerability declared high profile). The anchors are fine; the summary count is not. Same for
S055/S060 accuracy only if the row owners rely on ISO alignment — S036 contains no `ISO` token at all
(`grep -c ISO` = 0), which is consistent with S055's anchor not claiming one.

## Confidence

High for all five rows: every verdict is a literal-string match against the committed capture bytes with a
printed line number, plus a read of the surrounding context. No inference used. Remaining unknown: none for
the assigned question. Captures are of record as committed under `corpus/source-snapshots/round-25/`
(hashes in `capture-log.txt`); no live re-fetch was attempted or needed.
