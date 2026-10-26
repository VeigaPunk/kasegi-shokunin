# ScribeAssimilationGate — round 37 assimilation Gate block (draft)

Read-only seat. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` at HEAD
`b362068195d5489aa94b31e6ec8f880c367e0ba0` (round-37 claims-erratum-1). The shokuknow campaign
(`/home/vgpnk/Projects/shokuknow`) and the fleet root were read-only throughout; no campaign tool
was run there, no VCS mutation, no subagent, no install. Only this receipt was written in the lane;
all computation lives in scratch `/fast/scratch/hyaku/kasegi-r37/ScribeAssimilationGate/`, removed
before yielding.

Inputs (pinned, read-only):
- register `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
  — sha256 `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 375 lines, mtime
  `2026-10-24 08:37:00.746072780 -0300`.
- staged package `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` — sha256
  `4fe049cbe4bac6c7924392bc162d2792032e7e3780f7f6da316cb8c6d87e73eb`; package 70 files, every mtime
  `2026-10-24 23:33:20 -0300`; `find <pkg> -type f -newer .ufo/waves/round-37/claims.json` → 0 files.
- lane registry `corpus/SOURCES.md` (53 rows at this head), `corpus/README.md` frontier (F01–F19;
  `grep -cE '\| F2[0-9] '` → 0), `corpus/knowledge/` 48 files.

## 1. Id-collision rerun — 53 registry × 94 staged → 23 collisions

Commands, run verbatim in scratch (`$S` = scratch dir), exit 0:

```
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' lane/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u > $S/reg-ids
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' $S/../staged/SOURCES.append.md | grep -oE 'S[0-9]+' | sort -u > $S/staged-ids
comm -12 $S/reg-ids $S/staged-ids > $S/collisions
```

Counts and digests: `reg-ids` 53 (`5538790d…72ef7`), `staged-ids` 94 (`550a0129…8019f`),
`collisions` 23 (`56d979a0…7b50b`). The staged file read is the campaign package path above.

**Registry id list (53, contiguous S001–S053):**

```
S001 S002 S003 S004 S005 S006 S007 S008 S009 S010 S011 S012 S013 S014 S015 S016 S017 S018
S019 S020 S021 S022 S023 S024 S025 S026 S027 S028 S029 S030 S031 S032 S033 S034 S035 S036
S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048 S049 S050 S051 S052 S053
```

**Staged id list (94, contiguous S031–S124):**

```
S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044 S045 S046 S047 S048
S049 S050 S051 S052 S053 S054 S055 S056 S057 S058 S059 S060 S061 S062 S063 S064 S065 S066
S067 S068 S069 S070 S071 S072 S073 S074 S075 S076 S077 S078 S079 S080 S081 S082 S083 S084
S085 S086 S087 S088 S089 S090 S091 S092 S093 S094 S095 S096 S097 S098 S099 S100 S101 S102
S103 S104 S105 S106 S107 S108 S109 S110 S111 S112 S113 S114 S115 S116 S117 S118 S119 S120
S121 S122 S123 S124
```

**Collisions (23):** `S031 S032 S033 S034 S035 S036 S037 S038 S039 S040 S041 S042 S043 S044
S045 S046 S047 S048 S049 S050 S051 S052 S053`.

**Guard proof (indented-row scratch fixture).** Fixture registry: `| S001` (col 0), `  | S002`
(2 spaces), `    | S003` (4 spaces); fixture staged: `| S004` (col 0), `   | S002` (3 spaces),
`| S003` (col 0). With the real guard (`^ {0,3}\|…`): reg ids `{S001,S002}`, staged ids
`{S002,S003,S004}`, `comm -12` → `{S002}`, count 1 — non-empty, so the 0–3-space tolerance is
load-bearing. With a column-zero-only pattern on the same fixture: `comm -12` → empty, count 0.
Recorded limit: the 4-space-indented registry row `S003` is outside the pattern and is not caught
(the census format allows 0–3 spaces only).

**Renumber note — none adopted.** No staged row was adopted or renumbered this round; adoption is by
document identity, never by arithmetic on the staged number. The colliding block is contiguous
because the staged set starts at S031 and the lane has since grown through S053. Two forward
observations: (a) the frozen C2 row S054 (SSVC, `https://certcc.github.io/SSVC/`) will collide with
staged S054 (IPA 内閣府 request PDF) — different documents, so a future adoption of staged S054 would
need a renumber-by-document map; (b) register ids are package ids, not lane ids — e.g. register S037
is `openstd…GB/T 30279-2020` while lane S037 is the Cybozu bounty FAQ; register S048 is the
`std.samr.gov.cn` plan record while lane S048 is Microsoft MSVR.

## 2. Quarantine slice — seven kasegi rows, hand-checked, 0 adopted

Derivation (frozen command, exit 0, 7 rows; `slice.txt` sha256 `d02acb68…11b862`):

```
awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

Rows: register lines 99–100 (7-column table: S037, S054 `payload-absent`) and 322–326 (5-column
table: S048, S065, S068, S069, S070 "could not be fetched"). Each cited source was fetched fresh
today with a browser UA (`curl -sSL --max-time 90 -A '<Mozilla/5.0 … Chrome/130>' -o <file>
-w '%{http_code} %{size_download}'`), and each registered span was searched exact, whitespace-
normalized (collapse) and whitespace-squashed (remove all).

| id | register class | live fetch (2026-10-26) | quote location | verdict | flip condition |
|---|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24,209 B HTML (sha256 `8b92fa78…`) | assembled span exact **0**, normalized **0**; fragments each present once: `信息安全技术 网络安全漏洞分类分级指南` 1, `标准状态：` 1, `现行` 1, `发布日期` 1, `2020-11-19` 1, `实施日期` 1, `2021-06-01` 1 — but labels and values sit in separate table rows, and `标准状态：现行` occurs **0** in the raw HTML | **absent (composite quote-form)** — content true per field, span never contiguous; not a fabrication | re-stage as cell-anchored fragments (`标准状态：现行`; `发布日期2020-11-19实施日期2021-06-01`) and add a lane row first (`grep -c openstd corpus/SOURCES.md` → 0) |
| S054 | `payload-absent` | 200, 513,648 B PDF, 133 lines text (sha256 `0150c9d1…`) | registered span exact **0**, squash **0** — it drops the interpolated statutory parenthetical; the corrected full clause `脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` is contiguous under squash **1** at §1（ア）, text lines 46–47 | **absent (elided quote-form)** — source real, registered span a re-construction; not a fabrication | quote the full clause verbatim after a lane row exists (`grep -c 府連 corpus/SOURCES.md` → 0) |
| S048 | never checked | **404**, 748 B, body `HTTP状态 404 - 未找到` (sha256 `95cd25d8…`) | no payload, nothing quorable | **unreachable** | a fresh register id naming a live record for the same standard |
| S065 | never checked | 200, 7,465,472 B PDF, 1,295 lines text (sha256 `e33b0f67…`) | `刑法（7 件）` at text line 1182; entry 1 `1． 中华人民共和国刑法（1979 年通过，1997 年修订，` (line 1184) resumes `2009 年修正）` (line 1188) around a page footer `27`; staged phrase squash **1** with standalone footer lines removed; `现行有效法律目录（303 件）` line 1 | **prose-class** — anchor prose located; no verbatim registered span existed to check; page as-of line reads `（截至 2026 年 8 月 28 日 …` (line 2), not the staged "2026年9月" | — (not adopted: quarantine-first) |
| S068 | never checked | browser UA **403**, 465 B; plain client **301 → 200**, 94,027 B at `sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html` (sha256 `098f99a8…`) | `ISO/IEC 29147:2018` once; it is followed by `</a>,` + newline + `which`, so the register's `29147:2018 , which` is exact **0**/squash **1**; anchors `Cisco Product Security Incident Response` ×4, `Disclosure of Security Vulnerabilities` ×2; the "expedite" list opens with **four** `<li>` bullets, then a later list has three | **prose-class** — reachable via redirect, anchor located; access asymmetry (browser 403 / plain 200) reproduced; the staged row's "two conditions" is a four-bullet overclaim | — (same document as lane S040, already `mined`; nothing to adopt) |
| S069 | never checked | browser UA **302** → `https://kass.sacinfo.org.cn/kfs/token/download/pjzfynauwvlkxtwj`; verifying client fails (`curl` exit 60, incomplete TLS chain); plain `http://` token URL **200**, 1,470,121 B PDF 1.7, 58 pages (sha256 `b0c04697…`) | `6.3.1 技术分级` text line 1043; `6.3.2 综合分级` 1; `表A.1` 5, `表D.1` 2, `表E.1` 2; `GB/T 30279—202X` 56; bands `超危/高危/中危/低危` 11/24/21/20 | **prose-class** — anchor set located over http after the https leg failed; transport caveat stands | — (not adopted: quarantine-first; a later reader must not treat the fetch as clean) |
| S070 | never checked | browser UA **302** → `https://kass.sacinfo.org.cn/kfs/token/download/iolohzdoaclwhfzm`; verifying client fails (exit 60); plain `http://` token URL **200**, 234,182 B PDF 1.7, 8 pages (sha256 `2eff0a5b…`) | `一、工作简况` line 8, `1.1 任务来源` line 9; `20260806-T-469` 1, `中国信息安全测评中心` 5, `全国网络安全标准化技术委员会` 2; `1.2 制定背景`, `1.3 起草单位`; `CWE` 6, `CVSS` 5 | **prose-class** — anchor set located over http after the https leg failed; transport caveat stands | — (not adopted: quarantine-first) |

Totals: **absent 2 · unreachable 1 · prose-class 4 · adopted 0**. No row is a confirmed fabrication;
the two `payload-absent` rows are quote-form defects (composite / elided) with authentic sources.

## 3. Standing refusals — seven staged entries unchanged, 0/7 flips cleared

Package byte-identity (re-measured): 70 files, every mtime `2026-10-24 23:33:20 -0300`,
`find -newer .ufo/waves/round-37/claims.json` → 0, `SOURCES.append.md` `4fe049cb…73eb` — identical to
rounds 35/36. All seven entry digests equal their round-36 values:

| staged entry | sha256 (now = round 36) | flip condition | met? | fresh evidence |
|---|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | `120d8cd5…9abc8` | located quote + executable recheck + non-colliding frontier id | **No** | body `txt:N` locators **0**; its single `recheck:` is a prose `curl` snippet, not an executable lane recheck; `ground: F09` names lane F09 "Authorisation outside the platform" (different admitted item, `README.md:210`) |
| `claim-packaging-and-report-quality.md` | `6ad64d78…8dbc` | S036 row + capture | **No** | cites S034/S035/S036; lane S036 is the Cybozu handling policy (`SOURCES.md:42`), different document from BILISRC V1.7; `BILISRC` in non-lesson `corpus/` only as do-not-adopt prose in `knowledge/program-severity-ladders-and-reward-scales.md` |
| `cn-crowdsourced-testing-roles-and-conduct.md` | `a5302aaf…e813` | entry shape + S081/S082 rows | **No** | H1 (`^# `) count **0**; registry ends S053, so S081/S082 rows absent |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | `6c15d941…ef83f` | three rows + a real frontier id | **No** | S077/S078/S079 registry rows absent (registry ends S053); `ground: F24` while lane frontier ends F19 (`README.md:389`; no F20–F29 row) |
| `chinese-criminal-thresholds-and-authorisation.md` | `1660c00c…a59ae` | three rows + renumber map | **No** | `court.gov.cn` / `czt.ln.gov.cn` / `nj.jsjc.gov.cn` → 0 non-lesson hits in `corpus/`; staged S044/S045/S046 collide with lane S044/S045/S046 (Bugcrowd VRT README, Bugcrowd CWE dataset, IPA JVN report — different documents) |
| `chinese-program-severity-instrument.md` | `442e0f2b…257c` | row + locatable anchor | **No** | `sse.com.cn` → 0 non-lesson hits; `newsType_6` → 0 in `corpus/source-snapshots/round-32/S049.txt` (20,272 B), `newsType_21` → 1 |
| `program-severity-ladders-and-reward-scales.md` | `35de5f8b…c87` | byte-identity or supersedes row | **No** | lane same-name `6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6` ≠ staged `35de5f8b…`; S036 half still unregistered |

The new round-37 lane material does not touch any refusal: none of the seven cites S052/S053/S054, and
`grep -ilE 'ssvc|epss|stakeholder-specific'` over the seven → 0 files.

## 4. Gate block draft (paste-ready for the round-37 lesson)

```markdown
### Assimilation: none adopted

Id-collision rerun at the round-37 head: registry **53** ids (S001–S053) × staged **94** ids
(S031–S124, `SOURCES.append.md` sha256 `4fe049cb…73eb`) → **23 collisions S031–S053**. The
0–3-space guard was proved once on an indented-row fixture (2-space registry row + 3-space staged
row → collision detected, count 1; column-zero-only pattern on the same fixture → 0; 4-space rows
fall outside the pattern by design). No row was adopted or renumbered; adoption remains by
document, and the frozen C2 row S054 (SSVC) will collide with staged S054 (IPA request PDF), a
different document — a future adoption needs a renumber-by-document map, not arithmetic.

Quarantine slice: 7 kasegi rows hand-checked against fresh fetches — **absent 2** (S037 composite
span, S054 elided parenthetical; both sources authentic, neither a fabrication), **unreachable 1**
(S048, 404/748 B), **prose-class 4** (S065 anchor at line 1182 with the page's `截至 2026 年 8 月
28 日`; S068 anchor located but browser-UA 403 vs plain-client 200 and the staged "two conditions"
is really four bullets; S069/S070 anchors located only over plain http after the https token leg
failed TLS verification). **0 adopted.**

Standing refusals: 7 staged entries byte-identical to round 36 (all seven digests equal; package
70 files, newest mtime `2026-10-24 23:33:20 -0300`), **0 of 7 flip conditions cleared** — and none
of the seven cites S052/S053/S054.
```

## 5. Findings and limits

1. **Prospective collision.** Today's 23 collisions are S031–S053. When the frozen C2 row S054
   lands, staged S054 (IPA 内閣府 request PDF) collides with it; count becomes 24. Nothing was
   adopted, so no renumber map was minted.
2. **S065 staged date is contradicted by the page.** The staged row says "catalogue dated 2026年9月";
   the fetched page line 2 reads `（截至 2026 年 8 月 28 日 …`. The row is prose-class and not
   adopted, but a later adopter must correct the date.
3. **S037/S054 are quote-form defects, not fabrications.** Every constituent fragment of S037 is
   present once; S054's corrected full clause is contiguous; the register's "absent" class records
   that the assembled/elided span does not occur, which is true.
4. **S068 access asymmetry reproduced.** Browser UA 403/465 B at the canonical URL; plain client
   301 → 200/94,027 B at the redirect destination. Same mechanism as rounds 25/35, opposite UA side.
5. **S069/S070 transport caveat.** The `https://kass.sacinfo.org.cn` token host fails certificate
   verification (curl 60); the bytes were fetched over its `http://` form. Nothing rests on them.
6. **Register ids ≠ lane ids.** The seven ids are package ids at census time (register S037 =
   openstd GB/T 30279-2020 vs lane S037 = Cybozu FAQ; register S048 = std.samr.gov.cn plan vs lane
   S048 = Microsoft MSVR). Any adoption must re-derive by document.
7. **No file outside this receipt was written**; scratch `/fast/scratch/hyaku/kasegi-r37/ScribeAssimilationGate/`
   was removed after the receipt was written.

## Commands / outputs / exits (selected)

- Register pin: `sha256sum` → `5afe1810…bad833`, `wc -l` → 375, `stat -c %y` → `2026-10-24 08:37:00.746072780 -0300` (exit 0).
- Guard: `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' … | grep -oE 'S[0-9]+' | sort -u` — registry 53, staged 94 (exit 0); `comm -12` → 23 lines (exit 0).
- Fixture: 0–3-space pattern → `S002`, count 1; column-zero pattern → count 0.
- Slice: `awk -F'|' …` → 7 lines (exit 0); sha256 `d02acb68…11b862`.
- Fetches (status/bytes): S037 200/24,209; S048 404/748; S054 200/513,648; S065 200/7,465,472;
  S068 browser 403/465 and plain 301→200/94,027; S069 302→https (curl exit 60) then http 200/1,470,121;
  S070 302→https (exit 60) then http 200/234,182. All curl commands exit 0 except the two TLS legs (60).
- Lattice checks: registry rows `grep -cE '^ {0,3}\|…'` → 53; `ls corpus/knowledge/*.md | wc -l` → 48;
  `grep -cE '\| F2[0-9] ' corpus/README.md` → 0; `grep -cE '\| S054 ' corpus/SOURCES.md` → 0;
  `find <pkg> -type f -newer .ufo/waves/round-37/claims.json | wc -l` → 0.

## Tooling

No installs, no upgrades, no removals. Pre-existing `curl`, `pdftotext`/`pdfinfo` (poppler),
`python3`, `awk`, `grep`, `comm`, `sha256sum`, `stat`, `find`, `sort`, `wc` only. `RULES.md` read
before tool use; no `pacman`, no `uv`, no `npx`.
