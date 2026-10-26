# RevRowS050 — S050 registry-row review against SOURCES contract v1 (round 33, wave 1)

- **Seat:** `RevRowS050` (reviewer, leaf; no subagent dispatch, no background jobs kept).
- **Answering model:** not asserted — this item is **not model-dependent**; every verdict below is a command output measured on landed bytes (bound 10: the config route table decides; no model passed).
- **Tooling installed/upgraded:** none. `pacman` paused host-wide (orchestrator ruling 2026-10-20); no package transaction, no binary fetched. `pdftotext` 26.08.0 (pre-installed, `/usr/bin/pdftotext`) used read-only for the PDF-page cross-check.
- **Subject:** landed row `S050` at `corpus/SOURCES.md:56` (1,095 B), mapped by DOCUMENT from staged `S035` at `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:11` (read-only).
- **Contract:** `/home/vgpnk/Projects/shokunin/CORPUS.md` § "SOURCES.md — where a shokunin learns", Contract v1 (kaika 2026-10-19, frozen), rules 1–6 + Shape + the frozen census block. (`corpus/CORPUS.md` does not exist in the lane; the contract lives at the fleet root — measured, not assumed.)
- **Lane write scope:** this receipt only. Scratch `/fast/scratch/hyaku/kasegi-r33/RevRowS050/` (bound 12), removed before yield; no lane file other than this receipt written; no git/jj mutation (read-only `git show`/`diff`/`log` only).
- **State label:** all §2 counters are **POST-STATE** — run after `ExecEntryF16.md` and `ExecRegistryAppend.md` landed (both present 01:29), on quiescent bytes (`git diff -U0 corpus/SOURCES.md` stable across two runs 10 min apart). The one PRE-STATE observation (URL absence pre-append) is labelled inline.
- **Verdict: ADMIT-ROW.** All six contract rules CONFORMANT at row level; every dispatched check passes on landed bytes. One LOW finding (rule-1 lesson half pending on `corpus/lessons/round-33.md`, owner `ScribeLesson`) and three notes. No medium or high finding.

---

## 1. Independent re-open of the source (non-author verification)

### 1.1 Live re-fetch — instrument UA, scratch only, my own instant

```text
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/capture-source.py \
    --id S050 --url https://security.360.cn/Reward/rules --kind pdf --out "$S/S050-now.txt"
S050 status=200 fetched_bytes=427391 snapshot_bytes=31016 \
  sha256=2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888 utc=2026-10-26T04:18:48Z
capture_exit=0
$ sha256sum "$S/S050-now.txt" corpus/source-snapshots/round-32/S050.txt
2f9c6406…6888  /fast/scratch/hyaku/kasegi-r33/RevRowS050/S050-now.txt
2f9c6406…6888  corpus/source-snapshots/round-32/S050.txt
$ diff -u corpus/source-snapshots/round-32/S050.txt "$S/S050-now.txt"; echo "diff_exit=$?"
diff_exit=0          # zero differing lines over all 630
```

The committed capture is byte-identical to a fresh conversion at `2026-10-26T04:18:48Z` — my own fetch, independent of `wave1/ScoutLiveDrift.md` (which measured the same equality at 04:16:16Z). The manifest's `sha256` pin (`2f9c6406…6888`) equals both.

### 1.2 URL shape — canonical, no redirect, no session artefact in the URL

```text
$ curl -sS -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' \
    -o /dev/null -D - -w 'http=%{http_code} redirects=%{num_redirects} final=%{url_effective}\n' \
    https://security.360.cn/Reward/rules
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: inline; filename=360SRC外部漏洞处理和评分标准V2.0（试行）
http=200 redirects=0 final=https://security.360.cn/Reward/rules
```

`redirects=0`, final URL byte-equal to the requested URL, no query string. The response sets a `PHPSESSID` cookie (server-issued to the fetcher, not corpus content); the committed text capture carries no cookie or session artefact. The `Content-Disposition` filename is the standard's own title — the row's `source` cell title matches the document, not just the URL.

### 1.3 URL byte-equality — row cell vs the dispatched URL vs the manifest record

```text
$ sed -n '56p' corpus/SOURCES.md | grep -oE 'https://security[^ |]+' | tr -d '\n' | sha256sum
642ebcc3378386df8ad786eea99b00dc7831b0bfd77a5acb199f2692a228acee  -
$ printf 'https://security.360.cn/Reward/rules' | sha256sum
642ebcc3378386df8ad786eea99b00dc7831b0bfd77a5acb199f2692a228acee  -
$ od -c <(sed -n '56p' corpus/SOURCES.md | grep -oE 'https://security[^ |]+') | sed -n '1,4p'
h t t p s : / / s e c u r i t y . 3 6 0 . c n / R e w a r d / r u l e s \n   # trailing \n is grep's
$ grep -c "security.360.cn/Reward/rules" corpus/SOURCES.md
1                      # exactly one occurrence in the whole file: the S050 row's source cell
```

Byte-equal, no trailing slash, no fragment, no case drift. Manifest record `url` (`corpus/source-snapshots/round-32/manifest.json`, S050) is the same string; `capture-binding-check.py` rule B binds it (`url_bound=2` for round-32, §2). PRE-STATE label: before the append, `grep -c "security.360.cn"` over `git show 6e55c8d:corpus/SOURCES.md` → `0` — the URL is new to the registry, so rule B's "exactly one row" holds with no duplicate (E04-negative-control logic in `wave1/ExecCensusDry.md`).

### 1.4 Anchor re-opened line by line (landed anchor → capture lines)

The landed `anchor` cell (verbatim, `SOURCES.md:56` field 7):

> capture corpus/source-snapshots/round-32/S050.txt: 编写人 360 安全应急响应中心 L3, 版本号 V2.0 L5, 实施日期 2023 年 3 月 1 日 L7, 一、适用范围 L69-71 (the sentence wraps across L70-L71), 二、威胁反馈与处理流程 1. 漏洞报告模板 L73 with the 仅从理论层面说明漏洞的存在而无利用和复现过程将不予收录 sentence L86-L87, 2. 漏洞审核 L90-92, 4. 漏洞定级 L98-100, 三、漏洞奖励标准 漏洞奖励=业务系数*基础安全币 L112 with the 业务系数 table L118-125 and the 安全币 RMB ratio line L129, 七、漏洞定级标准 five grades L418-L419, 八、漏洞审核原则 item 1 L557-560, 九、通用规定 items 1-2 L595-598

Every cite measured against the committed capture:

| anchor cite | capture line(s) | observed |
|---|---|---|
| 编写人 360 安全应急响应中心 L3 | L2=`编写人`, L3=`360 安全应急响应中心` | ✔ value line cited (label one line up — consistent pattern, see N2) |
| 版本号 V2.0 L5 | L4=`版本号`, L5=`V2.0` | ✔ |
| 实施日期 2023 年 3 月 1 日 L7 | L6=`实施日期`, L7=`2023 年 3 月 1 日` | ✔ |
| 一、适用范围 L69-71 | L69 heading; L70-71 the applicability sentence (wraps) | ✔ |
| 1. 漏洞报告模板 L73 | L73 = `1. 漏洞报告模板` | ✔ |
| 仅从理论层面…不予收录 sentence L86-L87 | L86 ends `…将不`, L87 = `予收录。（例如扫描报告、请求头配置等）` | ✔ (sentence spans L85-87; the quoted clause sits in L86-87) |
| 2. 漏洞审核 L90-92 | L90 heading; L91-92 the three-working-days review clock | ✔ |
| 4. 漏洞定级 L98-100 | L98 heading; L99-100 the seven-working-days final-grading clock | ✔ |
| 漏洞奖励=业务系数*基础安全币 L112 | L112 exact | ✔ |
| 业务系数 table L118-125 | L118 `【业务系数】` … L125 `0.1~0.5` | ✔ |
| 安全币 RMB ratio line L129 | L129 `漏洞安全币（安全币 ：RMB=1 : 5）` | ✔ |
| 七、漏洞定级标准 five grades L418-L419 | L418 `…分为严重、高危、中危、低危、忽略五个等级。收录的基本原`, L419 `则是有实际应用危害。` | ✔ |
| 八、漏洞审核原则 item 1 L557-560 | L557 heading; L558-560 item 1 (only 360 products/businesses; unlisted holding businesses not collected) | ✔ |
| 九、通用规定 items 1-2 L595-598 | L595 item 1 (no open-cloud report storage), L597 item 2 (no pre-fix disclosure) | ✔ |

**Anchor form:** standard title + publisher provenance (编写人/版本号/实施日期) + named sections and subsections + capture line numbers + the wrap note. Not a bare homepage; the revision identifier the contract demands is present (V2.0, effective 2023-03-01 — L5/L7), so unlike S048 no no-date caveat is needed.

### 1.5 PDF-page cross-check of the staged anchor (scratch, read-only)

```text
$ curl -sS -A 'kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)' \
    -o "$S/rules.pdf" https://security.360.cn/Reward/rules      # 427391 B
$ for p in 5 6 7; do pdftotext -enc UTF-8 -f $p -l $p "$S/rules.pdf" - | sed -n '1,3p'; done
page 5: 360SRC 外部漏洞处理和评分标准 V2.0 / (2023.03.01) / 前言 …
page 6: … 2. 漏洞审核 / 在漏洞审核过程中我们可能与报告者沟通确认 …
page 7: 三、漏洞奖励标准 / 1. 基础奖励标准 / 漏洞奖励=业务系数*基础安全币。
```

The staged anchor's "PDF pages 5 to 6, section 二 威胁反馈与处理流程, subsections 1 漏洞报告模板, 2 漏洞审核, 4 漏洞定级" is accurate against the live PDF; the landed anchor re-expresses the same ground as byte-pinned capture lines (L69-105 region), which is the stronger form.

### 1.6 `teaches` grounding re-measured (exactly-once under declared normalization)

```text
$ python3 (source-recheck.py normalize over the capture)
occurrences=1  漏洞奖励=业务系数*基础安全币          # L112
occurrences=1  分为严重、高危、中危、低危、忽略五个等级  # L418
occurrences=1  本标准适用于 360 集团发布的产品和业务    # L70 clause
```

The landed `teaches` cell — "360SRC states its own two-sided boundary — the standard applies to the products and businesses 360 publishes (L70-L71) with unlisted assets generally not collected (L591-L593), and a report that only asserts a theoretical vulnerability with no exploitation or reproduction is not collected (L86-L87)" — resolves clause by clause: L70-71 (applicability, ✔ §1.4), L591-593 (rule 10: assets outside security-service coverage generally not collected, ✔), L86-87 (theoretical-only reports not collected, ✔). Attributed to 360SRC as the stating party — the staged cell's generic "A Chinese vendor SRC refuses…" universalization is gone (Q4 trade, logged in the R8 note, §3).

### 1.7 Credential sweep (rule 6 / bound 8 / Q6)

```text
$ sed -n '56p' corpus/SOURCES.md | grep -nEi 'op://|password|token|secret|cookie|session=|bearer|vault|帐号|密码'
(no output)  → row cells clean
$ grep -nEi 'password|passwd|账号密码|密码|token|secret|cookie|session|vpn|op://' corpus/source-snapshots/round-32/S050.txt
434/517/518/522 — generic vulnerability-class prose (weak-password SSRF example, router-password scenario in the grading tables)
```

No credential material, session URL, or vault reference in the row or the capture (the S049 capture's VPN tester instructions are S049's hazard; none of it is in S050's bytes).

---

## 2. POST-STATE counters (run on landed, quiescent bytes)

### 2.1 The six contract census commands, verbatim from CORPUS.md § Census

```text
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
50
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
$ awk -F'|' '…{t=$5; …} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=47 B=1 C=2
$ awk -F'|' '…{s=$9; …} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=38 queued=9 rejected=3
$ awk -F'|' '…{i=$2; …}' corpus/SOURCES.md | sort | uniq -d
(no output)
$ awk -F'|' '…NF==13 {…if (t !~ /^[ABC]$/) …; if (s !~ /^(queued|mined|rejected)$/) …; if (k !~ /^(spec|docs|…|own-work)$/) …; if (t=="A" && k=="community") …}' corpus/SOURCES.md
(no output)
$ awk -F'|' '…NF==13 {…if (s=="mined") {…print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
```

Totals: 47+1+2 = 38+9+3 = 50 rows (48 → 50, C2 predicate); malformed 0; duplicate ids none; enum/tier-inflation none; every `mined` `used-by` path resolves — including S050's (`corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` exists, 24,492 B). All six clean.

### 2.2 Maintained census CLI

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Exit 0; only the two **base** W04 warnings frozen in `census-before.txt`; **no new E/W naming S050** (no duplicate URL — §1.3 — no unused mined row).

### 2.3 Binding checker and source-recheck (the row's record side)

```text
$ python3 corpus/instruments/capture-binding-check.py; echo "binding_exit=$?"
… MANIFEST round-32 records=2 url_bound=2 fetched=2 archival=0
… AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0
binding_exit=0
$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-32/manifest.json --source S050; echo "recheck50_exit=$?"
S050:sha256 OK
S050:Q1…Q6 OK occurrences=1   (six lines)
recheck50_exit=0
```

The S050 manifest record binds to its row (rule B) and carries `fetched_utc` (rule C); all six of its quote assertions are exactly-once under the declared normalization. I additionally verified each assertion's `location` line by `sed -n Np` (L70, L591, L595, L597, L112, L418 — all match, §1.4 table).

### 2.4 Harness interlock (used-by side)

```text
$ python3 corpus/instruments/frontier-recheck-count.py; echo "harness_exit=$?"
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
harness_exit=0
$ grep -lE '^source: S050 ' corpus/knowledge/*.md | wc -l
1
```

Exactly one entry cites S050 on a `source:` line; its anchor line (`entry:4`) names the standard title + version + sections + capture lines (`…in capture corpus/source-snapshots/round-32/S050.txt:69-71, 112, 113, 129, 418, 558, 591-593, 595-598, 601, 607, 611`) — every cited line re-verified against the capture (L110 `三、漏洞奖励标准`, L113 business classes, L594 `九、通用规定`, L601 item 3, L607 item 6, L611 item 8 — all ✔). The entry's `recheck:` line is `cd`-prefixed, parses under `bash -n`, human note after `#` (Q10 shape).

### 2.5 Append-only / byte-identity of pre-existing rows

```text
$ git diff -U0 -- corpus/SOURCES.md | grep -cE '^-[^-]'
0          # zero deletions
$ git diff --numstat -- corpus/SOURCES.md
6	0	corpus/SOURCES.md
# the 6 additions: row S049 (L55), row S050 (L56), Search-log note (L75),
# R8 notes S049 (L98) / S050 (L99), no-changes note (L100)
$ grep -E '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md \
    | grep -vE 'S049|S050' | sha256sum
b837d23e938388e2cafcf5cb1924fa0e680e6832284849d1cf522bfa5e96b25e
$ git show 6e55c8d:corpus/SOURCES.md | grep -E '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' | sha256sum
b837d23e938388e2cafcf5cb1924fa0e680e6832284849d1cf522bfa5e96b25e   # identical
```

The 48 pre-existing rows are byte-identical to the freeze commit; additions only. The R8 note (`SOURCES.md:99`) logs every staged→landed cell change old→new (§3 table), and `SOURCES.md:100` states no pre-existing cell changed — both verified here.

---

## 3. Verdict per rule + dispatched checklist

| rule | requirement | verdict | evidence |
|---|---|---|---|
| **1** | Row written after opening the source; round lesson `## Gate` records URL, access date, ≤25-word located quote grounding `teaches` | **CONFORMANT (row level); lesson half PENDING — LOW-1** | Capture opened twice this round by non-author seats (ScoutLiveDrift 04:16Z, this seat 04:18:48Z, §1.1); `opened 2026-10-26` = the round date. `corpus/lessons/round-33.md` **ABSENT** at 01:35 (`ls` exit 2) — owner `ScribeLesson`; no `ScribeGateDraft.md` receipt yet either. Closure check: `test -s corpus/lessons/round-33.md && grep -c 'S050' corpus/lessons/round-33.md`. |
| **2** | Append-only; only status/recheck/used-by change in place, logged old→new; corrections are new rows | **CONFORMANT** | §2.5: 6 additions, 0 deletions; 48-row block sha equal to base; R8 note logs kind/opened/anchor/teaches/used-by old→new for the NEW row (a new row's staged→landed mapping, not an in-place edit of a landed row). |
| **3** | No second method | **CONFORMANT** | Row + R8 note + Search log carry no admission criterion and no research method; the Search log cites standing refusals and peer receipts only. |
| **4** | Expansion is knowledge, not rows; no quota | **CONFORMANT** | One row for one document; exactly 1 entry cites S050 (§2.4); no second row minted for the same URL (grep count 1, §1.3). |
| **5** | Search log: question/where/date/identified/screened/included/excluded + reasons + stop rationale | **CONFORMANT** | `SOURCES.md:75` (2,879 B): question, where (package + 12-term sweep + two URLs), date 2026-10-26, identified 9 / screened 9 / included 2 / excluded 7 with seven named exclusion reasons, stop rationale. Counts match `wave1/ScoutPackageThemes.md`'s 9-row verdict table and `wave1/ScoutF16Sweep.md`'s sweep. |
| **6** | No credential material, session/private URL, `op://` | **CONFORMANT** | §1.7: row cells clean; capture's 密码 hits are generic vuln-class prose; URL public, query-free, `redirects=0`. |

Dispatched checklist:

| ask | verdict | measurement |
|---|---|---|
| URL byte-equality with `https://security.360.cn/Reward/rules` | **PASS** | sha256 `642ebcc3…acee` equal across row cell / dispatched literal / manifest record; 1 occurrence in the file (§1.3) |
| 11 columns (NF=13 under the census awk), no `\|` in cells | **PASS** | `awk -F'\|' '/^\| S050 \|/ {print NF}'` → `13`; malformed census 0 (§2.1) |
| tier scoped, not global | **PASS** | tier `A`, scope = "360SRC's own handling and scoring standard: its applicability clause, report-template requirement, review and grading clocks, reward formula and intake rules" — scoped to this standard; kind `docs` ≠ `community`, enum sweep silent (§2.1) |
| anchor = standard title + capture lines, exact, not a bare homepage | **PASS** | §1.4: all 15 cites verified on the capture; version + effective date present (L5/L7); URL canonical (§1.2) |
| `teaches` one grounded benefit | **PASS (note N1)** | every clause resolves at its cited lines (§1.6); attributed to 360SRC (Q4); 43 words — lane-accepted cells run to 53 (S040), the ≤25-word cap binds the Gate quote, not the cell |
| status `mined` with a resolving used-by path | **PASS** | used-by = the F16 entry; exists (24,492 B); carries `source: S050 …` at `entry:4`; missing-used-by census empty (§2.1, §2.4) |
| `opened 2026-10-26` (not staged 2026-10-23) | **PASS** | `opened` cell `2026-10-26`; `sed -n 56p \| grep -c 2026-10-23` → `0` |
| `recheck` a valid cadence | **PASS** | `180d` — a contract-named cadence form, bare (no inline prose for E09 to fire on) |
| used-by the F16 entry | **PASS** | §2.4: harness `PASS F16 ids=S049,S050`, entries=19 pass=19 exit=0 |
| six census commands clean | **PASS** | §2.1: rows=50, malformed=0, A=47 B=1 C=2, mined=38 queued=9 rejected=3, dups none, enum none, missing none |
| census CLI exit 0, W04 S028/S029 only | **PASS** | §2.2 |
| pre-existing rows byte-identical to base | **PASS** | §2.5: block sha `b837d23e…` equal to `6e55c8d`; 6 additions 0 deletions |

Staged `S035` → landed `S050`, cell by cell:

| cell | staged `SOURCES.append.md:11` | landed `SOURCES.md:56` | verdict |
|---|---|---|---|
| id | `S035` | `S050` | mapped by DOCUMENT (URL byte-equal, §1.3). Staged `S035` is a different document (NPA 解釈線 PDF, per `wave1/ExecCensusDry.md` collision trap: live S035 = `npa.go.jp/.../1_kaisetsu.pdf`); the package's own `S049`/`S050` numbers are the JVN docs already landed as lane S046/S047 — following package ids would have duplicated landed rows. `S050` was free (48 rows, max S048). Correct. |
| source | `360SRC 外部漏洞处理和评分标准 V2.0 — https://security.360.cn/Reward/rules` | identical | unchanged, byte-equal. |
| kind | `spec` | `docs` | deliberate, logged in the R8 note with its reason (the capture is the PDF's converted text, read as its publisher's documentation). Both are contract enum values; census silent. |
| tier / status | `A` / `mined` | identical | unchanged. |
| scope | "360SRC's published report template, triage SLA, two-stage grading and 安全币 reward scale" | "360SRC's own handling and scoring standard: its applicability clause, report-template requirement, review and grading clocks, reward formula and intake rules" | broadened to the ground the entry's Claims 3-6 actually cite (applicability + intake rules), still scoped to 360SRC's own standard. |
| anchor | PDF pages 5-6, section 二, subsections 1/2/4; version V2.0, 实施日期 2023-03-01, 编写人 360 安全应急响应中心 (no capture lines) | capture-pinned: provenance lines L3/L5/L7 + section/subsection lines L69-71/L73/L86-87/L90-92/L98-100/L112/L118-125/L129/L418-419/L557-560/L595-598 | staged form had no byte-pinned lines; landed form fixes it and every line verifies (§1.4). PDF-page accuracy of the staged form cross-checked §1.5. |
| teaches | "A Chinese vendor SRC refuses reports that show no exploitation and reproduction, so the claim package must carry proof of impact" | "360SRC states its own two-sided boundary — … (L70-L71) … (L591-L593) … (L86-L87)" | staged cell universalized one vendor's rule onto "A Chinese vendor SRC" (Q4 hazard); landed cell attributes to 360SRC and adds the applicability half. Correct trade, logged. |
| opened | `2026-10-23` | `2026-10-26` | staged date not inherited (dispatched requirement); capture instant 2026-10-25T23:14:00-03:00 = 2026-10-26T02:14Z. |
| recheck | `180d` | `180d` | unchanged. |
| used-by | `program-scope-rules-and-asset-boundaries.md`, `claim-packaging-and-report-quality.md` (both refused, outside the lane) | `chinese-crowdsourced-testing-scope-and-rewards.md` | staged paths do not exist in the lane; landed path resolves and is the single citing entry. |

---

## 4. Findings by severity

**HIGH / MEDIUM — none.** No cell of the landed row is false against the fresh bytes; no pre-existing row changed; every dispatched check passes.

- **LOW-1 — rule 1's lesson half is unlanded.** `test -e corpus/lessons/round-33.md` → ABSENT (2026-10-26T01:35Z); no `ScribeGateDraft.md` receipt either. The `## Gate` record for S050 (URL, access date, ≤25-word located quote grounding `teaches`) must land in `ScribeLesson`'s file; until then rule 1 is conformant only at row level. Owner: `ScribeLesson` (not my write path). Closure check: `test -s corpus/lessons/round-33.md && grep -q 'S050' corpus/lessons/round-33.md`. Same shape as round-31's LOW-1 (`wave2/RevRowS048.md` §4); if the Gate lands with a quote spanning the L86→L87 wrap it must carry the normalized single-space form (`…将不 予收录…`) or pick a within-line span — `normalize()` inserts a space at the wrap, so the unspaced string has 0 normalized occurrences (measured this seat).
- **NOTE N1 — `teaches` is 43 words / three clauses.** Contract's ≤25-word cap binds the Gate quote, not the cell; lane-accepted cells run to 53 words (S040). The cell is a two-sided boundary statement (what is collected / what is refused) — one coherent learner benefit, not two unrelated ones. Taste note only.
- **NOTE N2 — provenance cites name value lines, not label lines.** `编写人 … L3` (label L2), `版本号 V2.0 L5` (label L4), `实施日期 … L7` (label L6). Consistent within the anchor and every cited line says what the anchor claims; no false location. No repair available in place (anchor immutable under R8); not warranted as a `supersedes` row.
- **NOTE N3 — teaches paraphrase "unlisted assets" compresses "未纳入安全服务的资产" (assets outside security-service coverage).** The cited lines (L591-L593) carry the precise rule and its examples, and the entry's Claim 4 states the precise reading ("collection exclusions keyed to security-service coverage, not to a scope list"). Compression, not error; bound by the cited lines.
- **INFO-1 (pre-existing, not caused by this append) — the stale `SOURCES.md:83` citations drift further.** `round-29.md:214` and `round-29-verifier-spotcheck.md:74` cite `SOURCES.md:83` for the S043 old→new note; that citation was already wrong at the round-33 base (base L83 = the S040 recheck note; known M31-3, routed). This round's inserts (rows L55-56, Search log L75, R8 notes L98-100) move the S043 note to L90. No **correct** citation was newly broken: every correctly-located citation into SOURCES.md (`round-25.md:90`→L22, `round-28.md:203`→L48, `round-31.md:29`→L54, `round-31-verifier-spotcheck.md:92`→L54) sits at or above L54, and the inserts all sit at L55+. Routed to the L1 with round-31's open erratum item; not repaired here (append-only file, not my write path).

---

## 5. Residual risk and verification gaps

1. **Currency is a short-interval observation.** Two independent re-fetches (04:16:16Z Scout, 04:18:48Z this seat) both byte-identical to the capture, ~2 h after capture. Says nothing about later drift; `source-recheck.py` re-reads committed bytes, not the network. The row's `recheck 180d` is the standing control [INFERENCE: published V2.0 standard dated 2023-03-01, low-churn institutional document — unmeasured].
2. **Raw-PDF byte equality is unproven** (fetched_bytes 427,391 both times, but the repo records no round-32 raw-body digest); what is pinned and re-verified is the converted text the anchors and assertions bind to. Sufficient for the row's claims, which are all line-anchored.
3. **Rule 1's Gate half cannot be verified from committed bytes until `corpus/lessons/round-33.md` lands** (LOW-1). If it lands omitting the URL, access date, or located quote for S050, rule 1 fails retroactively and needs a lesson erratum, not a row edit.
4. **Entry-level Q1-Q10 is another seat's assignment** (`RevEntryF16`); this receipt verifies only the row↔entry interlock (used-by resolution, `source: S050` line, anchor-line accuracy, recheck-line shape). I did not judge the entry's internal claims beyond what the row check required.
5. **`fetched_utc` provenance is the commit instant, not a measured HTTP instant** (no round-32 fetch log exists; `wave1/ExecManifest32.md` §8 states this). The drift runs bound content equality from 04:16Z onward only.
6. **Tier A is a curation claim about this standard only** (its own scope cell says so); nothing here endorses generalizing 360SRC's boundary to other SRCs — the entry's rejected-overgeneralizations section (Q5) is the guard, reviewed by `RevEntryF16`.

## Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r33/RevRowS050/` (fresh fetch, PDF, diffs, extracted row/log lines) removed before yield; the receipt (this file) is the only artifact kept, in the wave dir. No lane file other than this receipt was written; no git/jj mutation; no installs.
