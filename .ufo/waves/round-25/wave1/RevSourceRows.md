# RevSourceRows — staged source rows S055, S056, S057, S060, S068 audited before append

Seat: `L1Kasegi25.RevSourceRows` (read-only). Lane: `kasegi-shokunin`, base
`b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Audited: 2026-10-25.
Staged file: `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` (94 rows, ids S031–S124).
Lane schema: `corpus/SOURCES.md` registry header, 11 columns
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

**Tool installs: none.** No pacman/uv/npx/cargo transaction was run for this item.

## 0. Which bytes are the record — the id mapping is not the staged id

The item names `corpus/source-snapshots/round-25/S0NN.txt` by the staged id. **No capture exists
under any of the five staged ids:**

```
$ for id in S055 S056 S057 S060 S068; do test -e corpus/source-snapshots/round-25/$id.txt \
    && echo "EXISTS $id" || echo "ABSENT $id"; done
ABSENT corpus/source-snapshots/round-25/S055.txt
ABSENT corpus/source-snapshots/round-25/S056.txt
ABSENT corpus/source-snapshots/round-25/S057.txt
ABSENT corpus/source-snapshots/round-25/S060.txt
ABSENT corpus/source-snapshots/round-25/S068.txt
```

The five documents **are** captured, under the lane ids `.ufo/waves/round-25/capture-log.txt` already
assigns them (log table, verbatim):

| lane id (capture stem) | document | staged id |
|---|---|---|
| S036 | 脆弱性情報ハンドリングポリシー (Cybozu) | S055 |
| S037 | FAQ（脆弱性報奨金制度） (Cybozu) | S056 |
| S038 | 脆弱性報告制度 (GMO Pepabo) | S057 |
| S039 | 日立グループにおける製品脆弱性情報の開示プロセス (HIRT-PUB10008) | S060 |
| S040 | Cisco Security Vulnerability Policy | S068 |

Every line citation below is to those five committed captures (S036.txt 87 lines, S037.txt 294,
S038.txt 77, S039.txt 696, S040.txt 503). Line numbers were produced with
`grep -n`/`sed -n` over the committed files; each quote below was counted exactly once in its
capture unless stated otherwise. My own live re-fetches (2026-10-25) corroborate but are **not**
the record and are labelled as such.

Consequence for the append: a row appended as `S055` would carry a `source:` id whose capture stem is
`S036.txt`, failing QUALITY Q9 ("the record's `path` stem equals its `id`"). The five rows must land
as **S036–S040**, which is also the only ordering the committed captures support.

## 1. Five-row normalization table

Legend: **VIOLATION** = must be corrected before append; **PRECISION** = claim is supported but
over-broad or under-qualified; **OK** = clean.

| staged id → lane id | columns | literal or escaped `\|` in a cell | `recheck` prose | `used-by` target missing | `anchor` locatable in capture | `teaches` supported by capture | verdict |
|---|---|---|---|---|---|---|---|
| S055 → **S036** | 11 ✔ | none (row splits to exactly 13 fields) | none (`180d`) | none (both targets are package files, both cite `S055`) | ✔ all named sections exist (S036.txt:12,13,16,17,20,24,26,27,43) | ✔ (19, 22, 44) — but see P1 | **PRECISION** + id fix |
| S056 → **S037** | 11 ✔ | none | none (`180d`) | none (both targets cite `S056`) | ✔ all four FAQ items verbatim (S037.txt:98,102,108,114) | **✘ "invitation-only" refuted** — no `招待` anywhere in 294 lines | **VIOLATION** + id fix |
| S057 → **S038** | 11 ✔ | none | none (`180d`) | none (all three targets cite `S057`) | ✔ (S038.txt:14,18,23) | ✔ (17) except "at all" — see P2 | **VIOLATION** (scope wording) + id fix |
| S060 → **S039** | 11 ✔ | none | none (`180d`) | none (target cites `S060`) | **✘ anchor is prose, names no section, page or line** | ✔ (S039.txt:506,510) | **VIOLATION** (anchor) + id fix |
| S068 → **S040** | 11 ✔ | none | none (`180d`) | none (both targets cite `S068`) | ✔ (S040.txt:56,185,299) | **✘ "the two conditions" refuted** — the page lists four, and says "may … expedite" | **VIOLATION** + id fix |

No row in this set has a column-count, pipe-escape, `recheck`-format or `used-by` defect. All five
`recheck` cells are the bare cadence `180d` (legal); all five `opened` cells are `2026-10-23` (ISO);
all five `status` cells are `mined`; all five `kind`/`tier` pairs are `docs`/`A`.

## 2. Claims the captures do NOT support — do not append as-is

### D1 (S056 → S037) `teaches`: "invitation-only and account-gated" — the invitation half is refuted

Capture S037.txt line 99–101:

```
 99  A. サイボウズではサイボウズが運営する専用サイト（報告用サイト）にアクセスし、報告いただきます。報告にはアカウントが必要になります。
100  Q. 報告用サイトのアカウントが欲しいです。
101  A. 報告用サイトアカウントお申し込みフォームからお申込みください。
```

`grep -c 招待 corpus/source-snapshots/round-25/S037.txt` → **0**. The gate is a self-service
*application form* (`お申し込みフォーム`), not an invitation; the page states no vetting step either
way. "account-gated" is supported; "invitation-only" is an unsupported addition, and it is the same
over-claim the staged entry repeats (`program-quirks-2026-10-23-amendment.md:16` "an invitation-only
one (S056)" and `:24` "reachable only by invitation"). The entry text needs the same correction or it
fails Q3/Q4 on this sentence.

**Corrected cell (`teaches`):**
`A Japanese bounty is account-gated rather than open submission: reporting runs through a dedicated reporting site whose account is obtained from an application form, non-programme reports go through a separate 脆弱性報告フォーム, scope is a published target-product list, and payment lands on the last business day after two months from remediation completion.`

(Last clause follows S037.txt:115 `対応完了してから2ヶ月を経過した最終営業日にお支払いいたします` — the
original `teaches` dropped "last business day"; restored here.)

### D2 (S068 → S040) `teaches`: "the two conditions under which it will accelerate disclosure" — refuted twice over

Capture S040.txt line 300, verbatim:

```
300  Cisco generally does not publicly disclose security vulnerabilities in a Cisco product until the Cisco PSIRT has completed the incident response process and determined that enough software patches or workarounds exist to address the vulnerability. Cisco may, however, expedite disclosure of a security vulnerability in the following situations:
```

The enumerated list that follows has **four** items, not two:

- line 301 — `The Cisco PSIRT has completed the incident response process for a high-severity vulnerability and public disclosure of code fixes is planned to address it.`
- lines 302–304 — observed active exploitation.
- lines 305–308 — potential for increased public awareness.
- line 309 — `The Cisco PSIRT has declared a third-party software vulnerability to be high profile.`

Modality is also wrong: the page says Cisco **may … expedite**, and the per-item wording is "will
accelerate the publication of a security announcement", not "will accelerate disclosure". A second,
separate list exists at lines 334–338 ("Conditions under which an out-of-cycle publication may occur
include, but are not limited to" — three items), so "the two conditions" matches neither list. The
staged entry inherits the same error (`vendor-cvd-policy-crosswalk-2026-10-23.md:31` "**It states the
two conditions under which it will go faster.**" and names only the first two).

**Corrected cell (`teaches`):**
`A vendor policy that names its ISO/IEC alignment and its coordination centres also states four situations in which it may expedite disclosure (a completed high-severity investigation with fixes planned, observed active exploitation, potential increased public awareness, or a third-party component declared high profile) and a separate, explicitly non-exhaustive list of three out-of-cycle publication triggers.`

### D3 (S060 → S039) `anchor`: prose, not a locatable anchor

Staged value: `body paragraphs describing the product-vendor IRT focus and the coordinated-report case for findings that affect another vendor's product`.
That names no section, page, paragraph number or revision, so nothing in it can be checked against a
capture without re-deriving the location — the failure mode QUALITY Q1/Q3 exist to prevent (and every
one of the lane's 35 existing rows names sections). The *content* is supportable; only the locator is
missing.

**Corrected cell (`anchor`):**
`1.2 脆弱性情報の入手 (製品開発工程においての問題発見 paragraph, capture S039.txt line 506), the 4つのIRT paragraphs under the HIRT-PUB10008 heading (capture lines 489-491), and 1.4 情報公開 (公表日一致の原則, capture lines 519-526); page 更新日 2026年10月14日 (capture line 487)`

Supporting capture lines for the `teaches` this anchor must bind: S039.txt:506
`(他社製品に影響することがわかった)場合には、情報セキュリティ早期警戒パートナーシップの脆弱性関連情報の届出窓口に報告することで、協調した脆弱性対策を開始します`
and S039.txt:510 `HIRTは、日立グループの窓口として、通知された脆弱性関連情報を製品開発部署に展開しています`.

### D4 (S057 → S038) `scope`: "legal safe-harbour for authorised testing" over-claims authorisation

Capture S038.txt:17 promises only that no legal action will be taken:

```
 17  また、当社システムへの侵入または侵入の試みが以下に示す条件を守る限りにおいて、セキュリティ研究者に対して、法的措置をとらない方針です。
```

The page authorises nothing — it grants no asset scope, no permission to test, and does not use a
safe-harbour term; it waives legal action for intrusion attempts that respect the stated conditions
(prohibited acts at lines 23–25). "safe-harbour for **authorised** testing" is the A7 over-claim class
in `corpus/QUALITY.md`. The `teaches` cell for this row is worded correctly ("no-legal-action policy
for researchers who respect stated conditions"), so only `scope` is wrong.

**Corrected cell (`scope`):**
`A Japanese vendor's published no-legal-action statement for researchers who respect its stated conditions, and its prohibited acts`

### P1 (S055 → S036) `teaches` is supported but under-qualified

Supported verbatim: S036.txt:19 `脆弱性報奨金制度を含む外部からの報告` (bounty as an intake source),
S036.txt:22 `当社では、深刻度の指標のひとつとしてCVSS(※1) を使用しています。` (CVSS as one severity
indicator), S036.txt:44 `情報公開は公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します。`
(JVN publication on a date agreed with JPCERT/CC). But the disclosure commitment is scoped to packaged
products: S036.txt:28 `当社が作成したパッケージ製品（モバイル製品を除く）` and S036.txt:30
`クラウド製品およびモバイル製品の脆弱性情報については、原則として公開しておりません。` The unqualified
sentence reads as company-wide JVN disclosure, which the page denies. Append with the limitation:

**Corrected cell (`teaches`):**
`A Japanese vendor's policy names its own bounty programme as an intake source, uses CVSS as one severity indicator, and publishes packaged-product vulnerabilities on JVN on a date agreed with JPCERT/CC; cloud and mobile products are not published by default.`

### P2 (S057 → S038) `teaches`: "at all" is stronger than the page

S038.txt:20 `現在、報奨金制度は設けておりません。` — "currently we do not run a bounty programme".
`現在` makes it a dated statement, not a standing one. Replace "and runs no bounty programme at all"
with `and states that it currently has no bounty programme`. (S038.txt:17 and :23 already support the
rest of the sentence verbatim.)

## 3. Claims the captures DO support — safe to append after the id fix

| lane id | claim | capture line and text |
|---|---|---|
| S036 | bounty named as an intake source | S036.txt:19 `脆弱性報奨金制度を含む外部からの報告` |
| S036 | CVSS as one severity indicator | S036.txt:22 `深刻度の指標のひとつとしてCVSS` |
| S036 | JVN, simultaneous-disclosure principle, JPCERT/CC | S036.txt:44 `公表日一致の原則に従い、JPCERT/CC と取り決めた日に合わせて公開します` |
| S036 | anchor sections all present | S036.txt:12 `脆弱性対応`, :13/:27 `対象範囲`, :16 `脆弱性対応フロー`, :17 `1. 情報収集`, :20 `2. 影響の確認`, :24 `3. 対策`, :26 `脆弱性情報の公開`, :43 `2. JVNでの公開`; policy sheet `（2018年4月9日版）` at :46 |
| S037 | account required; account by application form | S037.txt:99 `報告にはアカウントが必要になります`, :101 `報告用サイトアカウントお申し込みフォーム` |
| S037 | separate form for non-programme reports | S037.txt:102–103 `脆弱性報奨金制度に参加せずに報告したいのですが？` → `脆弱性報告フォームからお申込みください。` |
| S037 | scope by target-product list, exclusions possible | S037.txt:108–109 `報奨金制度の対象外の可能性があります。報奨金制度の対象製品をご確認ください。` |
| S037 | payout timing | S037.txt:114–115 `対応完了してから2ヶ月を経過した最終営業日にお支払いいたします。` |
| S038 | no legal action under stated conditions | S038.txt:17 (quoted in D4) |
| S038 | no bounty programme, currently | S038.txt:20 `現在、報奨金制度は設けておりません。` |
| S038 | prohibited acts 1 and 2 | S038.txt:23 `脆弱性の検証目的であっても、以下の行為については禁止いたします`, :24 DoS, :25 access beyond own account |
| S039 | product-vendor IRT focus | S039.txt:489–491 (`製品ベンダIRT` at :490–491) |
| S039 | escalate to the partnership when another vendor is affected | S039.txt:506 (quoted in D3) |
| S040 | ISO/IEC alignment | S040.txt:58 `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018` |
| S040 | coordination centres | S040.txt:185–190 CERT/CC, CERT-FI, JP-CERT, NPSA |
| S040 | anchor sections all present | S040.txt:56 `Cisco Product Security Incident Response`, :185 `Incidents that may impact other vendors`, :299 `Disclosure of Security Vulnerabilities` |

## 4. Normalization blockers outside the five rows (report, not fix — read-only seat)

These do not change the five rows' cells but they make a straight append of `SOURCES.append.md`
impossible; the L1 has to settle them in the same cutover.

**G1 — the staged id space collides with the lane's own S031–S035.**
`MERGE-REPORT.md` says "lane registry currently holds **30** rows; first staged id is **S031**"
(`MERGE-REPORT.json`: `"first_id": "S031"`, `"existing_rows": 30`). The lane now holds **35** rows,
`S001`–`S035` (`python3` count over `corpus/SOURCES.md`). Staged `S031`–`S035` therefore duplicate live
ids with different sources:

| id | lane row (committed) | staged row (SOURCES.append.md) |
|---|---|---|
| S031 | CVE Numbering Authority Operational Rules v4.2.6 | HackerOne standard program policy set |
| S032 | NIST SP 800-115 | Bugcrowd VRT repository README |
| S033 | 不正アクセス行為の禁止等に関する法律 (e-Gov lawdata XML) | Bugcrowd VRT CWE mapping dataset |
| S034 | 総務省, 不正アクセス…の解説 (citizen page) | 网络安全众测平台 帮助 |
| S035 | 警察庁, 不正アクセス…の解説 (commentary PDF) | 360SRC 外部漏洞处理和评分标准 V2.0 |

Duplicate ids also break capture binding, because `round-24/S032.txt`–`S035.txt` are already the NIST
and Japanese-statute captures (round-24 manifest) while a staged `S032` would name Bugcrowd.

Arithmetic for the fix: 35 existing + 94 staged = 129 ids, `S001`–`S129`. The five captured rows are
pinned to `S036`–`S040` by the committed capture stems, so the workable assignment is **hoist the five
captured rows to S036–S040 in capture-log order, then give the remaining 89 staged rows S041–S129 in
file order** (89 ids for 89 rows; `S129` is the last). A uniform `+5` shift of the staged file does
*not* work: it would move the cybozu policy row from S055 to S060 and orphan the S036 capture.

**G2 — entry headers must be rewritten with the rows.** Five staged entries cite the five staged ids
and must be rewritten to S036–S040: `program-quirks-2026-10-23-amendment.md`,
`japanese-vendor-disclosure-policies-2026-10-23.md`,
`authorization-safe-harbor-and-scope-2026-10-23-amendment.md`,
`iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`, `vendor-cvd-policy-crosswalk-2026-10-23.md`.
Four more entries cite the collision zone and must be rewritten with the S031–S035 shift:
`program-scope-rules-and-asset-boundaries.md`, `program-severity-ladders-and-reward-scales.md`,
`claim-packaging-and-report-quality.md`, `chinese-program-severity-instrument.md`. A row append without
this rewrite leaves every `source:` header pointing at the wrong authority (Q1, R12).

**G3 — one staged row is structurally broken.** `S120` splits into **12** cells, not 11, because a
literal `|` sits inside a cell (`… zdx` answers **200** …`): the split shifts `status` to a sentence
fragment and pushes `opened` to `mined`, so `opened`/`recheck`/`used-by` are all off by one. It is the
only row in the 94 with a column-count defect (`bad_col_count [('S120', 12)]`) and the only row whose
`used-by` target is not a path (`30d — re-run the five data endpoints …`). It must be repaired or
dropped before the table is pasted; as-is it corrupts every row after it in a naive paste.

**G4 — 43 of 94 staged rows carry prose in `recheck`.** Values are of the form
`90d — re-open the 公告 page and confirm … (ran 2026-10-24)` (ids S081–S119, S121–S124). The lane's 35
committed rows contain **zero** such values; every one is a bare cadence (`90d`, `180d`, `730d`,
`on-release`). For column homogeneity and for the C1 predicate, strip to the bare cadence and move the
prose into the entry's own `recheck:` line, where Q7 wants an executable command. The five rows in this
audit are already bare (`180d`) and need no change.

## 5. Capture provenance note for S040 (Cisco)

`capture-log.txt` records that "A plain `curl -L` with a browser UA returned http 403 for S040 while
the capture instrument's own UA returned 200". I reproduced both directions on 2026-10-25:

```
browser-UA curl  -> http=403 bytes=465   (Akamai "Access Denied", reference 18.4ac91002...)
default-UA curl -> http=200 bytes=94027
```

So the entry's stated recheck (`curl -sSL https://www.cisco.com/…`, no UA override) works, and a
browser-UA re-check must not be used as the fail-closed control — it would report 403 on a healthy
page. Note also that plain `curl -sSL` exits 0 on a 403 body, so any recheck built on it passes
vacuously when Cisco blocks; the capture comparison, not the curl exit code, is what binds.

## 6. Residual risk and verification gaps

- **Unverified by capture:** none of the five `teaches` cells was checked against a second capture; each
  rests on one snapshot taken 2026-10-25T08:14Z. Page drift after that date is unmeasured.
- **S037 "invitation-only":** my refutation is from absence (`招待` count 0 over 294 lines) plus the
  application-form path. Absence in a rendered capture cannot exclude a vetted-application step
  described off-page (e.g. in the ルールブック); the corrected cell deliberately says
  "account-gated rather than open submission" and claims nothing about vetting.
- **S040 second list:** the three out-of-cycle triggers (S040.txt:334–338) are inside the
  "Disclosure Schedule" section and are explicitly non-exhaustive; the corrected `teaches` says so
  rather than treating them as a closed set.
- **Not in scope, not measured here:** whether the 67 staged knowledge entries meet Q1–Q9, and whether
  the append changes the C2 counter. My only cross-check on entries was the `source:`-header binding
  described in G2 and the two inherited misstatements (D1, D2).

## 7. Re-run appendix

```bash
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
for id in S055 S056 S057 S060 S068; do test -e corpus/source-snapshots/round-25/$id.txt && echo "EXISTS $id" || echo "ABSENT $id"; done
grep -c 招待 corpus/source-snapshots/round-25/S037.txt                       # 0
sed -n '300,309p' corpus/source-snapshots/round-25/S040.txt                 # four expedite situations
sed -n '334,338p' corpus/source-snapshots/round-25/S040.txt                 # three out-of-cycle triggers
sed -n '17,20p'   corpus/source-snapshots/round-25/S038.txt                 # no-legal-action + 現在 no bounty
sed -n '19,22p;28,30p;43,44p' corpus/source-snapshots/round-25/S036.txt     # intake, CVSS, packaged-only, JVN
sed -n '489,491p;506,510p' corpus/source-snapshots/round-25/S039.txt        # IRT focus, partnership escalation
python3 - <<'PY'
import re
rows=[l for l in open('/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md',encoding='utf-8') if re.match(r'\| S\d{3} ',l)]
print('rows',len(rows))
print('bad cols',[(l.split('|')[1].strip(),len(l.split('|'))-2) for l in rows if len(l.split('|'))!=13])
print('prose recheck',len([l for l in rows if '—' in l.split('|')[10]]))
PY
```

**Verdict for the L1:** append none of the five as staged. Renumber to S036–S040, replace the four
cells named in D1–D4, apply P1 and P2, and settle G1–G4 in the same cutover. Two staged claims (D1
invitation-only, D2 two conditions) are refuted by the committed captures and must not enter the
registry in any form.
