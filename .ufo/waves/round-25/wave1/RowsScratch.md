# RowsScratch — round 25 wave 1: normalized append block for S036–S040 (C2)

Seat: `L1Kasegi25.RowsScratch`. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Nothing was appended to `corpus/SOURCES.md` by this seat:
`git status --porcelain corpus/SOURCES.md` is empty after all work.

## Axes

- **coverage (C2, score 7)** — the surface this item serves: five registry rows the L1 appends so the
  frontier F10 ground has admitted, citable rows.
- **depth:verifiability (4, no-harm)** — every `anchor`/`teaches` claim in the block carries a capture line
  pointer, and each was checked against the committed capture bytes, not against the staged text.
- **depth:density (9, no-harm)** — no `SKILL.md` or entry byte touched.

## Files written (only my scope)

| path | what |
|---|---|
| `.ufo/waves/round-25/assimilation/rows/SOURCES.append.block.md` | the five normalized rows, nothing else (3 comment lines + 5 rows) |
| `.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md` | scratch mirror: lane `corpus/SOURCES.md` + the same five rows at the end of the Registry table |
| `.ufo/waves/round-25/assimilation/rows/validate/corpus/knowledge` | symlink → `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/knowledge` (the mirror's `used-by` resolver; see Risks) |
| `.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.mutant-dup-id.md` | discrimination mutant (E03) |
| `.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.mutant-dup-url.md` | discrimination mutant (E04) |
| `.ufo/waves/round-25/wave1/RowsScratch.md` | this report |

No tool install or upgrade was needed (bash, coreutils, gawk, the fleet census script were already present).

## Id mapping (followed the document, not arithmetic)

From `.ufo/waves/round-25/capture-log.txt`: staged S055→**S036**, S056→**S037**, S057→**S038**,
S060→**S039**, S068→**S040**. Staged rows read read-only from
`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md`.

## Normalization applied to all five rows

`status` = `mined`; `opened` = `2026-10-25`; `recheck` = `180d` (cadence, never prose); `kind` = `docs`,
`tier` = `A` for all five; no cell carries a literal or escaped `|` (Japanese quotes, `...` and `to` replace
the staged em-dash pipes-free forms); `used-by` names exactly the entries whose headers cite the row.

`used-by` was set from the two landed entries, read directly, not from the staged text:

- `corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md` — `source:` lines for S036, S037, S038, S039 (`grep -c 'S040'` = 0, so it does not cite S040).
- `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md` — four `source:` lines: S040, S036, S038, S039 (`^source: S037` count = 0).

Result: S036, S038, S039 → both entries; S037 → JP entry only; S040 → crosswalk only.

## Corrections against the capture (staged claim → what the capture says)

1. **S037 anchor.** Staged quoted `脆弱性報奨金制度に参加せずに報告したいのですが？` — 0 literal hits in
   `S037.txt`. Replaced with the wording that exists, `脆弱性報奨金制度に参加せずに報告したいのですが、どうしたら良いですか？`.
2. **S039 anchor + teaches.** Staged anchor named no heading ("body paragraphs describing the product-vendor
   IRT focus and the coordinated-report case"), so it could not be checked. Retargeted to `1.2 脆弱性情報の入手 ... (1)`
   (L503) with the 他社製品 sentence at L506, plus the four-IRT intro (L490, L491) and `1.4 情報公開` (L522); the
   teaches cell now states the ISO/IEC mapping the capture actually prints (L497–L499) and the L510 partnership
   participation instead of an unsourced "escalates" phrasing.
3. **S040 teaches.** Staged said Cisco "states the two conditions" for accelerated disclosure. `S040.txt`
   L301–L309 lists **four** bullets under "Cisco may, however, expedite disclosure … in the following
   situations". Cell corrected to four, with the four bullet line numbers.
4. **S036 and S038** were checked and kept (anchor targets all resolve; L13/L16/L17/L20/L24/L27/L43 and
   L14/L18/L23/L24/L25 respectively). S036's scope cell was narrowed to "its one severity indicator" because
   the capture says CVSS is *one of* its indicators (L22) and names no ISO alignment (`grep -c ISO` = 0).

## Acceptance

**a) Five rows, 11 cells each**

```
$ awk -F'|' '/^\| S0/ {print NF-2}' .ufo/waves/round-25/assimilation/rows/SOURCES.append.block.md
11
11
11
11
11
```

**b) Pipe audit** — 5 lines carry pipes, 60 pipes total = 5 × 12, no escaped pipe:

```
$ grep -c '|' .ufo/waves/round-25/assimilation/rows/SOURCES.append.block.md
5
$ grep -o '|' .ufo/waves/round-25/assimilation/rows/SOURCES.append.block.md | wc -l
60
$ grep -c '\\|' .ufo/waves/round-25/assimilation/rows/SOURCES.append.block.md
0
```

(`grep -c` counts lines; `grep -o | wc -l` counts pipes. The block is 3 pipe-free HTML comment lines plus the
5 rows, so no header/separator row inflates the count.) The block's rows and the mirror's rows are byte-identical:

```
$ diff <(grep '^| S0' …/rows/SOURCES.append.block.md) <(grep -E '^\| S0(3[6-9]|40) ' …/rows/validate/corpus/SOURCES.md)
IDENTICAL
```

**c) Census validate on the scratch mirror — exit 0**

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file .ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md
exit=0
```

No E-code fires. The two W04 lines are the pre-existing S028/S029 warnings the round's frozen before-state
already records (`claims.json` `census_before`: "W04 x2 (S028,S029 pre-existing)"), not introduced here.

Row accounting on the same file (`census` mode): `rows 40` (= 35 + 5), `tier.A 37` (32 + 5), `tier.B 1`,
`tier.C 2`, `status.mined 28` (23 + 5), `queued 9`, `rejected 3`, `missing 0`, exit 0.

**Discrimination (R11 spirit)** — the exit 0 above is not vacuous; two mutants of the same mirror are killed:

```
$ … sources-census.sh validate --file …/validate/corpus/SOURCES.mutant-dup-id.md
file	E03	S038 duplicate id
exit=1
$ … sources-census.sh validate --file …/validate/corpus/SOURCES.mutant-dup-url.md
file	E04	S037 duplicate url cybozu.co.jp/company/security-policy within scope A Japanese vendor's own vulnerability-handling policy: its intake routes, its one severity indicator, and the split between what it publishes and what it withholds
exit=1
```

The first mutant renames S039's id to S038; the second gives S037 S036's URL and scope. Both are mine, in my
scope, and are kept as the controls for this receipt.

**d) `used-by` existence** — both named paths exist on disk (checked after both entry seats landed):

```
$ for p in <cells>; do test -e "$p" && echo "EXISTS $p"; done
EXISTS corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
EXISTS corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
```

Ownership: `vendor-disclosure-policies-as-corpus-objects.md` is the `EntryJapanVendors` seat's file
(header `source:` lines S036–S039); `vendor-disclosure-policy-commitments-crosswalk.md` is the
`EntryCiscoCrosswalk` seat's file (header `source:` lines S040, S036, S038, S039, confirmed by message and by
reading the file's L2–L5).

**e) Capture line pointers for every kept `anchor`/`teaches` claim**

```
### S036 (anchor: 対象範囲 L13, フロー L16, 1. 情報収集 L17, 2. 影響の確認 L20, 3. 対策 L24, 公開 L26, 対象範囲 L27, 2. JVNでの公開 L43)
12:脆弱性対応   13:対象範囲   16:脆弱性対応フロー   17:1. 情報収集   20:2. 影響の確認   24:3. 対策   26:脆弱性情報の公開   27:対象範囲   43:2. JVNでの公開
19:具体的には、情報セキュリティ早期警戒パートナーシップや、脆弱性報奨金制度を含む外部からの報告、社内での検出などです。
22:当社では、深刻度の指標のひとつとしてCVSS(※1) を使用しています。…
28:当社が作成したパッケージ製品（モバイル製品を除く）
30:クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。
44:製品の脆弱性対応に関する情報は、…JVNにて公開します。 なお、情報公開は公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します。

### S037 (anchor: the four FAQ items)
98:Q. 脆弱性を見つけたので報告したいのですが、どうしたら良いですか？
101:A. 報告用サイトアカウントお申し込みフォームからお申込みください。
102:Q. 脆弱性報奨金制度に参加せずに報告したいのですが、どうしたら良いですか？
108:Q. Webサイトの脆弱性を見つけました。報告しても良いですか？
109:A. ご報告いただけます。ただし、サイトによっては報奨金制度の対象外の可能性があります。報奨金制度の対象製品をご確認ください。
114:Q. 報奨金はいつ支払われますか？
115:A. いただいた報告が対応完了してから2ヶ月を経過した最終営業日にお支払いいたします。
(account gate: 99:A. …報告にはアカウントが必要になります。  非参加の報告路: 103:A. 脆弱性報告フォームからお申込みください。)

### S038
14:脆弱性報告制度   18:脆弱性の評価について   23:脆弱性の検証目的であっても、以下の行為については禁止いたします
24:1.DoS攻撃、DoS攻撃に該当する検証
25:2.自分自身のアカウントや情報以外へのアクセス、改ざんを試みるなどの行為
17:また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。
20:現在、報奨金制度は設けておりません。

### S039
490/491: 4つのIRT model と「製品ベンダIRT」への焦点 (HIRT-PUB10008では…製品ベンダIRT)に焦点を絞り…)
497:ステップ１：脆弱性情報の入手 ... (1) ISO/IEC 29147:2014 脆弱性情報の開示
498:ステップ2：調査ならびに対策 ... (2) ISO/IEC 30111:2013 脆弱性対応手順
499:ステップ3：情報公開 ... (3)(4) ISO/IEC 29147:2014 脆弱性情報の開示
503:1.2 脆弱性情報の入手 ... (1)
506:…発見された脆弱性の影響が日立グループ製品に留まらない(他社製品に影響することがわかった)場合には、情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで、協調した脆弱性対策を開始します。
510:日立グループは、2004年7月から情報セキュリティ早期警戒パートナーシップに製品開発ベンダとして参画し…
522:1.4 情報公開 ... (3)(4)
533:…JVN(Japan Vulnerability Notes) や CERT/CC Vulnerability Notes Database に対応状況を掲載することで、対策の展開活動を進めています。

### S040
56:Cisco Product Security Incident Response   58:security incidents. The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018,
185:Incidents that may impact other vendors: The Cisco PSIRT works
299:Disclosure of Security Vulnerabilities
300:…Cisco may, however, expedite disclosure of a security vulnerability in the following situations:
301:The Cisco PSIRT has completed the incident response process for a high-severity vulnerability…   (bullet 1)
302–304:The Cisco PSIRT has observed active exploitation…   (bullet 2)
305–308:There is the potential for increased public awareness…   (bullet 3)
309:The Cisco PSIRT has declared a third-party software vulnerability to be high profile.   (bullet 4)
310:All Cisco security publications are disclosed to customers and the public simultaneously.
```

(TOC duplicates at `S040.txt:17` and `:28` are why the anchor cites the body headings at 56/299.)

## Risks and open dependencies (not mine to close)

1. **The crosswalk's `recheck:` line names four sources.** `vendor-disclosure-policy-commitments-crosswalk.md`
   L7 chains `--source S040 … S036 … S038 … S039` against `corpus/source-snapshots/round-25/manifest.json`.
   That manifest does not exist yet; for that line to exit 0 the manifest must carry quote records for all four
   ids. Whoever builds the round-25 manifest must include the crosswalk's S036/S038/S039 quotes, not only S040's.
   My rows do not depend on it; the census checks `used-by` existence only.
2. **Mirror `used-by` resolution.** With `--file`, the census resolves `used-by` against `dirname(file)/..`, i.e.
   the `validate/` directory, so the mirror carries a `corpus/knowledge` symlink to the lane's real knowledge
   directory. Nothing under `corpus/knowledge` was copied or modified by me (`git status` shows peer-owned
   modifications there, not mine).
3. **The C2 counter the L1 should run after appending** is the fleet form
   `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` (not `--file`), which reads
   the real `corpus/SOURCES.md`. Expected: `rows 40`, `tier A=37`, `status.mined=28`, the same two W04 lines,
   exit 0. If that run reports E03/E04, the append introduced a duplicate — report it, do not paper over it.
4. **Frontier row is not mine.** C2's first conjunct (frontier admitted rows = 10) lives in `corpus/README.md`
   and is another seat's file; this receipt covers only the five rows, the block and the mirror.
5. Pre-existing, unchanged: W04 on S028 and S029 (`claims.json` records them as pre-existing).
