# ScribeAssimilationGate — round 34 assimilation Gate

Seat: `ScribeAssimilationGate` (scribe, wave 1, round 34). Role: draft the assimilation Gate block for the
round-34 lesson. This seat claims no axis score and judges no claim; it re-derives three measurements and
records verdicts for the L1 to integrate.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `014ee2d7aa8c3c095ff57ae51097606a9906228c`,
  claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.
- Lane tip at first read: `206e510` (round-34 wave-1 spec). Working tree at first read: `M SCORECARD.md`;
  untracked `.ufo/waves/round-34/{assimilation,wave1,wave1.ready}` and `corpus/source-snapshots/round-34/`.
- All measurements read-only. No git/jj mutation, no write outside this receipt path, no lane instrument run,
  no package tool run (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` never
  invoked), nothing written under `/home/vgpnk/Projects/shokuknow`.
- Measurement window: fetches `2026-10-26T05:31:52Z`–`05:32:45Z`; lane predicates and digests read
  `05:31Z` and re-read `05:39Z`. The wave landed its C2 row mid-seat: `corpus/SOURCES.md` held 50 rows
  (`b22c7f0173e7`) at `05:31Z` and 51 rows with `S051` (`4c85ff8608dd`) at `05:39Z`, README 16 → 17 frontier
  rows. Both moments are printed wherever the figure moves (Gate §2, § R1, § R4, Finding F2); nothing was
  restated as if the later bytes had been the first.

Inputs, digests read this seat (`@05:31Z` → `@05:39Z` where the file moved):

| path | sha256 (12 hex) | bytes |
|---|---|---|
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | `5afe1810a6c3` | 375 lines (unchanged across the seat) |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.json` | `8a42a9109c8c` | — |
| `corpus/SOURCES.md` | `b22c7f0173e7` @05:31Z → `4c85ff8608dd` @05:39Z | 50 rows → **51 rows** (`S051` at `:57`) |
| `corpus/README.md` | `3779e77f07a2` @05:31Z → `876be9cc7997` @05:39Z | 16 → **17** frontier rows (F01–F17) |
| `corpus/QUALITY.md` | `eb20eafc6aab` | 227 lines (Q1–Q10, R1–R23) |
| `corpus/lessons/round-33.md` | `f69472f38ea7` | refusal table at `:40-52` |
| `corpus/lessons/round-33-verifier-spotcheck.md` | `435e97b5929b` | R1–R9 at `§5` |
| `SCORECARD.md` | `b8fc8c66619c` | — |
| `.ufo/waves/round-34/claims.json` | `dedb9ea8063a` | assimilation item at `:89` |

Seven staged entries (read-only, digests unchanged from round 33's record — round-33 lesson
`§ Refused package candidates` prefixes in brackets):
`program-scope-rules-and-asset-boundaries.md` `120d8cd5d50b` [`120d8cd5`],
`claim-packaging-and-report-quality.md` `6ad64d785f8f` [`6ad64d78`],
`cn-crowdsourced-testing-roles-and-conduct.md` `a5302aaf0b9a` [`a5302aaf`],
`chinese-crowd-testing-national-standard-2026-10-23.md` `6c15d9411424` [`6c15d941`],
`chinese-criminal-thresholds-and-authorisation.md` `1660c00c1636…4e8a59ae` [`1660c00c…4e8a59ae`],
`chinese-program-severity-instrument.md` `442e0f2bfb08` [`442e0f2b`],
`program-severity-ladders-and-reward-scales.md` `35de5f8b19ed` [`35de5f8b`].

---

## Gate block for `corpus/lessons/round-34.md` (drop-in)

### Gate — assimilation: id-collision re-run, quarantine slice, standing refusals

Three components, all measured read-only at `2026-10-26T05:31Z`–`05:39Z` against register
`absent-defect-register.md` `sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`
and package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (`MERGE-REPORT.json 8a42a910…`, 67 knowledge
files, `accepted 94`, `existing_rows 30`, `first_id S031`, `renumbered 0`). Reproduce with
`.ufo/waves/round-34/wave1/ScribeAssimilationGate.md` § Report R4 (one `bash -n`-clean script,
`assim-check.sh`, embedded there, six runs).

#### 1. Quarantine slice — re-derived, 7 register rows, S-id on every line

Filter: lane cell `kasegi`, round cell, id cell, with the class taken from the register section
(`## Rows` → `payload-absent`; `## Rows whose quotes were NEVER CHECKED` → `unreachable`). Output, verbatim:

```
S037 | round1 | payload-absent
S054 | round3 | payload-absent
S048 | round2 | unreachable
S065 | round4 | unreachable
S068 | round4 | unreachable
S069 | round4 | unreachable
S070 | round4 | unreachable
```

`slice_rows=7 slice_malformed_lines=0`. Same seven ids, same order, as the committed
`.ufo/waves/round-34/assimilation/quarantine-slice` (`diff` on the S-id sequence empty); that committed
copy is a raw-cell dump whose five `unreachable` id cells carry the register's own stray trailing
backtick (`S048`` `), which this re-derivation normalizes.

Per-row verdicts. Live fetches at `2026-10-26T05:31Z`–`05:32Z`, one host each, `curl -L --max-time 60`
with a desktop UA; verdicts use the register's own two classes plus `reachable, no recorded span`:

| id | register class | live fetch (UTC) | body digest | verdict |
|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24209 B, `text/html`, `05:31:52Z` | `7159ea21ed61` | **payload-absent confirmed** — the registered span `信息安全技术 网络安全漏洞分类分级指南 标准状态：现行 发布日期：2020-11-19 实施日期：2021-06-01` is absent from the tag-stripped, whitespace-collapsed page (9119 chars: exact `False`, whitespace-folded `False`), while each of its 8 fragments occurs exactly once — a spliced field collage. **Refuse.** Flip: re-stage the contiguous field sequence, and add a lane row first (`grep -c openstd corpus/SOURCES.md` → 0). |
| S054 | `payload-absent` | 200, 513648 B, `application/pdf`, `05:31:53Z` | `0150c9d15dee` | **payload-absent confirmed for the registered span** — `pdftotext -layout` output 9780 B (UTF-8): `脆弱性の悪用が確認されたもの又は疑われるもの` exact 0, whitespace-folded 0; suffix `確認されたもの又は疑われるもの` 1 and `悪用が確認されたもの` 1, because the live clause reads `脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの` — the registered span elides the statutory parenthetical. **Refuse.** Flip: quote the full clause at §1（ア） verbatim, after a lane row exists (`grep -c 府連 corpus/SOURCES.md` → 0). |
| S048 | `unreachable` | **404**, 748 B, `text/html`, `05:31:54Z` | `95cd25d80d88` | **unreachable** — `std.samr.gov.cn` answers this URL with its 404 page (`HTTP状态 404 - 未找到`); whether the record was withdrawn or the id is stale is not observable from here. The register records no quote span, so there is nothing to test and this is never a fabrication. |
| S065 | `unreachable` | 200, 7465472 B, `application/pdf`, `05:32:42Z` | `e33b0f672934` | **reachable today, no recorded span** — the PDF is real (`现行有效法律目录（303 件）… 截至 2026 年 8 月 28 日`, `pdfinfo` CreationDate `2026-09-04`), so the class that describes today's fetch is `reachable`, not `unreachable` (the register's class was measured at census time and is not contradicted by today's read); but the register carried no quote, so `payload-present`/`payload-absent` cannot be adjudicated. Re-census with a located span before any admission. |
| S068 | `unreachable` | **403**, 465 B, `text/html`, `05:32:43Z` | `b2e56c7f4206` | **unreachable** — the body is an `Access Denied` page; the host refuses this instrument UA. Not a fabrication. |
| S069 | `unreachable` | 200, **0 B**, `05:32:44Z` | `e3b0c44298fc` | **unreachable in substance** — HTTP 200 with an empty body (`std.samr.gov.cn/dcpspTools/gbPlan/download…`); no payload exists to check. |
| S070 | `unreachable` | 200, **0 B**, `05:32:45Z` | `e3b0c44298fc` | same URL as S069, same empty body — the register holds two rows for one source. |

Net quarantine disposition: **0 adopted, 2 refused (S037, S054), 5 unreachable (S048, S068 outright; S069,
S070 empty; S065 reachable-but-unquoted)**. Blast radius inside the lane: **0** — all seven staged entries
that cite these ids (`chinese-vulnerability-taxonomy-and-grading.md`, `authorization-safe-harbor-and-scope-2026-10-23-amendment.md`,
`chinese-national-grading-model.md`, `chinese-statute-version-drift-2026-10-23-r4-amendment.md`,
`iso-29147-divergence-and-clause-crosswalk-2026-10-23.md`, `vendor-cvd-policy-crosswalk-2026-10-23.md`,
`chinese-grading-standard-draft-2026-10-23.md`) are absent from `corpus/knowledge/`, so no admitted lane entry
rests on a quarantined register row.

#### 2. Id-collision check — re-run, 21 collisions after the C2 row landed, guard shown load-bearing

```
reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
```

- Registry ids: `^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|` over `corpus/SOURCES.md`
  (`4c85ff8608dd`, 51 rows) → 51 unique (`S001`–`S051`); both the 0–3-space pattern and a column-0-only
  pattern return 51 here, so the guard is exercised on a fixture, not on the live file. Before the C2 row
  landed the same command read `reg_ids=50 … collisions=20 S031..S050` (`b22c7f0173e7`, `05:31Z`).
- Staged ids: `^[ ]{0,3}source:[[:space:]]*S[0-9]{3,}` over the package's 67 knowledge files → 94 unique
  (`S031`–`S124`).
- `comm -12` → `S031`…`S051` inclusive, 21 ids. At the 50-row moment the three derivation files were
  byte-identical to the committed `.ufo/waves/round-34/assimilation/{reg-ids,staged-ids,collisions}`
  (`ecc9c3b9…`, `550a0129…`, `dcfd73c7…`); those committed files are the pre-`S051` derivation, and the
  `+S051` control in § Report R4 reproduces the post-landing set exactly (`21`, `S031..S051`).
- Guard sensitivity (synthetic registry with one 2-space-indented `S031` row): 0–3-space pattern finds
  `S001 S031` and reports 1 collision; column-0-only pattern finds `S001` and reports 0 — the indented row
  is caught only by the wider pattern.
- Discrimination (each control moves exactly one figure, no other): registry `+S051` (fixture, run at the
  50-row moment) → `collisions=21 S031..S051` — which is what the landed row then produced; registry minus
  `S037` → `19`; register minus the `S054` row → `slice_rows=6`; absent register → `slice_rows=0 exit=1`;
  absent `SOURCES.md` → `reg_ids=0 exit=1`.
- The package still assumes a 30-row lane (`existing_rows 30`, `first_id S031`, `renumbered 0`), so every
  staged id in `S031`–`S051` names a different document than the lane row of the same id — e.g. staged
  `S044`/`S045`/`S046` are 最高人民法院 2011 解释 / 刑法 2023 修正 / 南京市检察院 指南, while lane `S044`/`S045`/`S046`
  are Bugcrowd VRT README / Bugcrowd VRT CWE mapping / IPA JVN activity report; staged `S047` is
  `sse.com.cn` JR/T 0276—2023, lane `S047` is the IPA JVN quarterly report. Adoption is therefore **by
  document, never by number**.

#### 3. Standing refusals re-confirmed, each with the flip condition still unmet

Digests unchanged (§ Inputs). One row per refused staged entry; "met?" is the measured flip predicate on
today's lane bytes, not an opinion. Every predicate in this table was run twice — at `05:31Z` on the 50-row
registry and again at `05:39Z` on the 51-row registry with `F17` admitted — and printed the same values both
times (§ Report R5), so the C2 landing moves none of them:

| staged entry | decision (round 33) | flip condition | met? |
|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | REFUSED (standing, round 30) | register+capture CNVD helpList and 360SRC rules (**met**, S049/S050 landed r33) **and** located quotes, per-platform attribution, executable recheck, re-ground on a lane frontier | **no** — `grep -cE 'txt:[0-9]+'` on the staged file → 0 located quotes; its `ground: F09` calls F09 "new frontier item" while lane `corpus/README.md:210` already holds an admitted F09 ("Authorisation outside the platform: the engagement document and the statute") |
| `claim-packaging-and-report-quality.md` | REFUSED (standing) | register+capture S034/S035/**S036** | **no** — `grep -c bilibili corpus/SOURCES.md` → 0; BILISRC in no lane row |
| `cn-crowdsourced-testing-roles-and-conduct.md` | REFUSED (standing) | H1 **and** register+capture S081/S082 **and** page/line quotes with exactly-once counts | **no** — `grep -c '^# '` → 0 (no H1); `std.samr.gov.cn/gb/search/gbDetailed?id=D0FE299A` → 0 rows in `SOURCES.md` |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | REFUSED (standing) | register+capture S077/S078/S079, quote the roles-and-duties sentence, re-ground on a lane F-id | **no** — `std.sacinfo.org.cn` → 0, `sac.gov.cn` → 0, `hcno=57CAF3B4` → 0 rows; `^| F24 |` → 0 (frontier is F01–F17); `「…」`-marked strings → 0 |
| `chinese-criminal-thresholds-and-authorisation.md` | REFUSED (standing, round 30) | register+capture S044/S045/S046 in non-colliding id space | **no** — `court.gov.cn` → 0, `czt.ln.gov.cn` → 0, `nj.jsjc.gov.cn` → 0 rows, **and** the staged ids `S044`–`S046` are occupied by Bugcrowd/IPA rows, so registration requires renumbering the package first |
| `chinese-program-severity-instrument.md` | REFUSED as an entry (round 33) | anchor present in the capture, second source registered | **no** — `grep -c newsType_6 corpus/source-snapshots/round-32/S049.txt` → 0 (`newsType_21` → 1); `grep -c sse.com.cn corpus/SOURCES.md` → 0 |
| `program-severity-ladders-and-reward-scales.md` | REFUSED / do-not-copy | — (overwrite hazard, not a flip) | **unchanged** — staged `35de5f8b19ed`/50 L vs lane `6c05c98f`/67 L |

No staged entry's flip set is fully met, and this round's new ground does not touch any of them:
`grep -rliE 'immunefi|vscs|web3'` over the package's 67 knowledge files → **0 files**, so F17/S051
(Immunefi VSCS v2.2) cannot unblock a refused entry and is not an assimilation candidate.

**Assimilation: none adopted this round.** Flips still unmet, named: `program-scope-rules-and-asset-boundaries`
(located quotes, per-platform attribution, executable recheck), `claim-packaging-and-report-quality`
(S036 BILISRC unregistered), `cn-crowdsourced-testing-roles-and-conduct` (S081/S082 unregistered, no H1),
`chinese-crowd-testing-national-standard-2026-10-23` (S077/S078/S079 unregistered, ground F24 absent),
`chinese-criminal-thresholds-and-authorisation` (S044/S045/S046 id-space collision), and
`chinese-program-severity-instrument` (anchor `newsType_6` absent from the capture, `sse.com.cn`
unregistered). No new refusal is opened and no prior refusal is lifted.

---

## Report

### R1 — Id-collision re-run (commands, exits, bytes)

Run at `05:31Z` against `corpus/SOURCES.md` `b22c7f0173e7` (50 rows):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -ohE '^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md \
    | grep -ohE 'S[0-9]{3,}' | sort -u > reg-ids            # 50 lines, exit 0
$ grep -ohE '^[ ]{0,3}source:[[:space:]]*S[0-9]{3,}' \
    /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/*.md \
    | grep -ohE 'S[0-9]{3,}' | sort -u > staged-ids         # 94 lines, exit 0
$ comm -12 reg-ids staged-ids > collisions                   # extern exit 0, 20 lines
reg_ids=50 staged_ids=94 collisions=20 collision_range=S031..S050
$ sha256sum reg-ids staged-ids collisions
ecc9c3b9f4dac2390cf2ba76bea084998fe2bad1c8b2c793547017da8aa59555  reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  staged-ids
dcfd73c75c0867e113fdd6470fcc7ccfb5129e7e1ee40661a18239e57fd5a99d  collisions
```

These three digests equal the committed `.ufo/waves/round-34/assimilation/{reg-ids,staged-ids,collisions}`
bit for bit (measured at `05:31Z`, 50-row registry); the re-derivation is independent and lands on the same
bytes. Re-run after the C2 row landed (`corpus/SOURCES.md` `4c85ff8608dd`, `05:39Z`, 51 rows):

```
reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
```

Independent count check in Python (same two patterns, `re.findall`, at `05:31Z`): `reg_0-3space 50 unique 50`,
`reg_col0 50 unique 50`, `pkg_files 67 staged_ids 94 S031 S124`, `collisions 20`.

Guard-sensitivity fixture (`.ufo/waves/round-33/assimilation/scratch-registry.md` rebuilt byte-equal here,
`sha256 ee8088e5208f…`):

```
0-3space pattern ids: S001 S031
col0-only ids: S001
collisions 0-3space=1 [S031]; col0=0 []
```

### R2 — Quarantine slice re-derivation

```
$ awk -F'|' '
    /^## Rows whose quotes were NEVER CHECKED/{sec="nc";next}
    /^## Rows$/{sec="pa";next}
    /^## /{sec=""}
    sec!="" && $2 ~ /kasegi/ { rnd=$3; id=$4
      gsub(/^[ `]+|[ `]+$/,"",rnd); gsub(/^[ `]+|[ `]+$/,"",id)
      if (id ~ /^S[0-9][0-9][0-9]$/) print id" | "rnd" | "(sec=="nc"?"unreachable":"payload-absent") }' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
S037 | round1 | payload-absent
S054 | round3 | payload-absent
S048 | round2 | unreachable
S065 | round4 | unreachable
S068 | round4 | unreachable
S069 | round4 | unreachable
S070 | round4 | unreachable
$ grep -cE '^S[0-9]{3} \| round[0-9]+ \| (payload-absent|unreachable)$' slice.txt   # 7 of 7, exit 0
$ sha256sum slice.txt
7696d76c4f17d1d9f41598e7c36def077e1f7429d947639726afdebf6e528f31
```

Completeness cross-checks on the register: `payload_absent_rows_total=194`; lane-cell
`kasegi` rows = **2** in `## Rows` and **5** in `## Rows whose quotes were NEVER CHECKED` (the class table
`## By lane` agrees: `| \`kasegi\` | 2 |`). A first-cut awk that let the never-checked header rematch
`^## Rows` counted 7 payload-absent rows; the section-state machine above fixes that — recorded because the
naive filter is the nearest wrong answer.

### R3 — Live fetch transcript (seven register sources)

```
$ curl -sS -L --max-time 60 -A "$UA" -o <name> -w "%{http_code} %{size_download} %{content_type}" <url>
s037  200 24209     text/html;charset=utf-8   05:31:52Z   sha256 7159ea21ed613f8d8058725299504271f905929bcfd152dd5e2f69df8987e508
s054  200 513648    application/pdf           05:31:53Z   sha256 0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88
s048  404 748       text/html;charset=utf-8   05:31:54Z   sha256 95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436
s065  200 7465472   application/pdf           05:32:42Z   sha256 e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83
s068  403 465       text/html                 05:32:43Z   sha256 b2e56c7f42060bdc65fc040dbab2a4cf4dc0a10f62fa6c669c12e1f7c054ad96
s069  200 0         (none)                    05:32:44Z   sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
s070  200 0         (none)                    05:32:45Z   sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Quote tests (the S054 body digest `0150c9d1…12b88` is the same digest round-33's quarantine seat recorded):

```
S037  tag-stripped+ws-collapsed page: 9119 chars
      full span present: False | ws-fold: False
      fragments, each exactly 1: 信息安全技术 / 网络安全漏洞分类分级指南 / 标准状态 / 现行 / 发布日期 /
                                 2020-11-19 / 实施日期 / 2021-06-01
S054  pdftotext -layout output: 9780 B (UTF-8)
      exact: False  ws-fold: False  count exact 0  flat 0
      '確認されたもの又は疑われるもの' 1 ; '悪用が確認されたもの' 1
      live clause: 脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの
S065  pdfinfo: CreationDate Fri Sep  4 05:00:02 2026 ; first page: 现行有效法律目录（303 件） …
S048  body: HTTP状态 404 - 未找到
S068  body: <TITLE>Access Denied</TITLE>
```

### R4 — Reproducible check with controls (`assim-check.sh`, `bash -n` clean)

One script prints the five figures the Gate block quotes and fails closed on missing inputs. Discrimination
per QUALITY R11/R13 — each control moves exactly one figure. Embedded verbatim (scratch is deleted, so this
copy is the durable one; `bash -n` exit 0; args are `[register] [SOURCES.md] [package knowledge dir]`):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
reg=${1:-/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md}
src=${2:-corpus/SOURCES.md}
pkg=${3:-/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge}
t=$(mktemp -d) || exit 9
grep -ohE '^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$src" | grep -ohE 'S[0-9]{3,}' | sort -u > "$t/reg"
grep -ohE '^[ ]{0,3}source:[[:space:]]*S[0-9]{3,}' "$pkg"/*.md | grep -ohE 'S[0-9]{3,}' | sort -u > "$t/staged"
comm -12 "$t/reg" "$t/staged" > "$t/coll"
awk -F'|' '
  /^## Rows whose quotes were NEVER CHECKED/{sec="nc";next}
  /^## Rows$/{sec="pa";next}
  /^## /{sec=""}
  sec!="" && $2 ~ /kasegi/ {
    rnd=$3; id=$4
    gsub(/^[ `]+|[ `]+$/,"",rnd); gsub(/^[ `]+|[ `]+$/,"",id)
    if (id ~ /^S[0-9][0-9][0-9]$/) print id" | "rnd" | "(sec=="nc"?"unreachable":"payload-absent")
  }' "$reg" > "$t/slice"
reg_ids=$(wc -l < "$t/reg"); staged_ids=$(wc -l < "$t/staged"); coll=$(wc -l < "$t/coll")
slice=$(wc -l < "$t/slice"); bad=$(grep -cvE '^S[0-9]{3} \| round[0-9]+ \| (payload-absent|unreachable)$' "$t/slice")
printf 'reg_ids=%s staged_ids=%s collisions=%s collision_range=%s..%s slice_rows=%s slice_malformed_lines=%s\n' \
  "$reg_ids" "$staged_ids" "$coll" "$(head -1 "$t/coll")" "$(tail -1 "$t/coll")" "$slice" "$bad"
rm -rf "$t"
[ "$reg_ids" -ge 1 ] && [ "$staged_ids" -ge 1 ] && [ "$bad" -eq 0 ] && [ "$slice" -ge 1 ]
```

| run | output | exit |
|---|---|---|
| baseline (`05:31Z`, lane `corpus/SOURCES.md` `b22c7f0173e7`, real register) | `reg_ids=50 staged_ids=94 collisions=20 collision_range=S031..S050 slice_rows=7 slice_malformed_lines=0` | 0 |
| baseline re-run (`05:39Z`, lane `corpus/SOURCES.md` `4c85ff8608dd` with `S051`) | `reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0` | 0 |
| control `+S051` row appended to a `SOURCES.md` copy (run pre-landing) | `reg_ids=51 … collisions=21 collision_range=S031..S051 slice_rows=7` | 0 |
| control `S037` row deleted from a `SOURCES.md` copy | `reg_ids=49 … collisions=19 … slice_rows=7` | 0 |
| control `S054` row deleted from a register copy | `… collisions=20 … slice_rows=6` | 0 |
| control register path absent | `… slice_rows=0` (awk fatal to stderr) | 1 |
| control registry path absent | `reg_ids=0 … collisions=0` | 1 |

The `+S051` control and the post-landing re-run agree exactly (`21`, `S031..S051`): the fixture predicted the
landed state before the row existed on disk, which is the discrimination R13 asks for.

First version of the script exited 0 when the **`SOURCES.md` path was absent** — `reg_ids=0 staged_ids=94
collisions=0 collision_range=.. slice_rows=7` — because `slice_rows=7` satisfied its only post-condition; it
was tightened to require `reg_ids>=1 && staged_ids>=1 && bad==0 && slice>=1`. That degenerate control is
recorded here rather than dropped (QUALITY R11/R13: a check that cannot fail on an absent input is not a
check).

### R5 — Lane-side predicates behind every flip verdict (exit codes)

First run at `05:31Z` (50-row registry, 16 frontier rows):

```
register sha256                 exit=0 :: 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833
registry row count              exit=0 :: 50
S051 rows                       exit=1 :: 0
frontier rows                   exit=0 :: 16      (F01..F16)
F24 present                     exit=1 :: 0
bilibili (staged S036)          exit=1 :: 0
sse.com.cn (staged S047)        exit=1 :: 0
openstd (S037 flip)             exit=1 :: 0
府連 (S054 flip)                 exit=1 :: 0
court.gov.cn (staged S044)      exit=1 :: 0
czt.ln.gov.cn (staged S045)     exit=1 :: 0
nj.jsjc.gov.cn (staged S046)    exit=1 :: 0
std.sacinfo.org.cn (S077)       exit=1 :: 0
sac.gov.cn (S078)               exit=1 :: 0
hcno=57CAF3B4 (S079)            exit=1 :: 0
id=D0FE299A (S082)              exit=1 :: 0
newsType_6 in S049.txt          exit=1 :: 0
newsType_21 in S049.txt         exit=0 :: 1
staged program-scope locators   exit=1 :: 0
staged cn-crowdsourced H1       exit=1 :: 0
immunefi|vscs|web3 in package   exit=1 :: (no file)
```

Second run at `05:39Z` on the post-landing bytes (`corpus/SOURCES.md` `4c85ff8608dd`, README
`876be9cc7997`). Only the two count lines move; every flip predicate prints the same value:

```
registry row count              exit=0 :: 51      (was 50)
frontier rows                   exit=0 :: 17      (was 16; F17 admitted)
F24 present                     exit=1 :: 0
bilibili / sse.com.cn / openstd / 府連  exit=1 :: 0 0 0 0
court.gov.cn / czt.ln.gov.cn / nj.jsjc.gov.cn  exit=1 :: 0 0 0
std.sacinfo.org.cn / sac.gov.cn / hcno=57CAF3B4  exit=1 :: 0 0 0
id=D0FE299A                     exit=1 :: 0
newsType_6 / newsType_21 in S049.txt  exit=1 :: 0 | exit=0 :: 1
staged program-scope locators   exit=1 :: 0
staged cn-crowdsourced H1       exit=1 :: 0
immunefi|vscs|web3 in package   exit=1 :: (no file)
```

`grep -c 'S051' corpus/SOURCES.md` moved `0 → 1` between the runs (row at `corpus/SOURCES.md:57`).

### R6 — Scope discipline

- At first read (`05:29Z`) `git status --porcelain` showed only `M SCORECARD.md` plus the untracked
  `.ufo/waves/round-34/{assimilation,wave1,wave1.ready}` and `corpus/source-snapshots/round-34/`. By `05:40Z`
  sibling seats had landed their own work — 12 modified paths (`SCORECARD.md`, `corpus/QUALITY.md`,
  `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/{README.md,capture-binding-check.py,frontier-recheck-count.py}`,
  `corpus/lessons/{round-29.md,round-33.md}`, `corpus/source-snapshots/round-{26,32}/manifest.json`,
  `.ufo/waves/round-33/wave1/ScribeReportDraft.md`) and new untracked paths
  (`corpus/instruments/kill-rule-check.py`, `corpus/instruments/r-defect-closure.sh`,
  `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md`, `selftest-baseline.txt`, `claims-erratum-1.md`).
  None of those is this seat's write; this seat wrote exactly one file, this receipt, inside the shared
  untracked `wave1/` directory. `selftest-baseline.txt` at the lane root is observed, unattributed, and left
  untouched — flagged for the L1 only because a lane-root file is unusual.
- No `git add/commit/push`, no `jj` invocation, no lane instrument executed, no package tool run.
- `/home/vgpnk/Projects/shokuknow` read only (`cat`/`grep`/`sha256sum`); the seven live fetches went to the
  register's cited public URLs, never to that tree, and no package tool ran there. Nothing under
  `/home/vgpnk/Projects/bounties`, the fleet repo, or sibling lanes touched.
- No tool installed, so no tool/version/channel line.

---

## Findings

1. **F1 — the committed round-34 quarantine slice is a cell dump, not a filtered slice.** It reproduces the
   register's own malformed `unreachable` id cells (`S048`` ` etc.) and carries no round/class field, so a
   reader cannot machine-check "S-id on every line" against it; the awk re-derivation (§ R2) is what makes
   that property checkable. The committed copy and this slice agree on all seven ids.
2. **F2 — the registry moved under the seat; both moments are recorded.** At `05:31Z` `corpus/SOURCES.md`
   `b22c7f0173e7` held 50 rows, zero `S051` tokens, and `corpus/README.md` printed 16 frontier rows; then
   `corpus/source-snapshots/round-34/{S051.txt,manifest.json}` (manifest: Immunefi VSCS v2.2, `captured
   2026-10-26T05:31:10Z`, HTTP 200, `sha256 4fd8ed98…`) landed with the C2 row, and at `05:39Z` the same
   files read 51 rows (`4c85ff8608dd`, `S051` at `:57`) and 17 frontier rows (`876be9cc7997`). The collision
   figure consequently reads **20 (`S031..S050`)** at the first moment and **21 (`S031..S051`)** at the
   second; the `+S051` fixture in § R4 predicted 21 before the row existed, so the move was measured, not
   inferred. Any lesson table quoting this figure should carry the moment it was read — the Gate block §2
   quotes the post-landing 21.
3. **F3 — the register's id column is malformed for every `unreachable` row, not just kasegi's.** All 109
   rows under `## Rows whose quotes were NEVER CHECKED` carry a trailing backtick in the id cell and no class
   column, so any naive `$4` read hands back `S048`` instead of `S048`. This seat's filter strips it; the
   register is read-only and no fix is proposed here (it belongs to the shokuknow generator).
4. **F4 — one register row's class no longer describes today's fetch.** `S065` (`npc.gov.cn`, `P020260904396146393500.pdf`) fetches
   cleanly today (200, 7,465,472 B, a real `现行有效法律目录（303 件）` PDF) but carried no quote, so it can be
   neither confirmed nor refused. It needs a re-census with a located span; calling it `unreachable` now
   overstates what the register measured.
5. **F5 — two register rows share one URL.** `S069` and `S070` cite the identical `std.samr.gov.cn/dcpspTools`
   URL and both return an empty 200. Any future count that treats these as two sources doubles a zero.
6. **F6 — the id-space hazard grows, not shrinks.** The package still declares `existing_rows 30` /
   `first_id S031` / `renumbered 0` against a lane registry of 51, so 21 of 94 staged ids currently name a
   different document than the lane row of that id (20 did at the 50-row moment), and each new lane row
   inside `S031`–`S124` adds one. `chinese-criminal-thresholds-and-authorisation` is the concrete casualty:
   its rows `S044`/`S045`/`S046` cannot be registered without renumbering.
7. **F7 — F17 does not enter the assimilation set.** No package knowledge file mentions Immunefi, VSCS or
   Web3, so the round's new ground is a coverage move, not an unblock for any standing refusal. This is the
   measured basis for "Assimilation: none adopted".
8. **F8 — no lane-side blast radius.** None of the seven staged entries that cite quarantined ids exists in
   `corpus/knowledge/`, so the quarantine slice touches package candidates only; no admitted entry needs a
   correction as a result of this slice.

## Limits

- **Fetch verdicts are one instant, one UA, one host each** (`05:31Z`–`05:32Z`, desktop UA). They say nothing
  about those pages before or after, and a 403/404/empty-200 is a statement about this instrument, not about
  the source's existence. Round-33's independent read found `S065`/`S068` reachable; my `S068` 403 agrees with
  the register's class and not with that observation, so the two moments disagree and neither is a verdict on
  the other.
- **S037/S054 quote tests are fold-dependent.** I tested exact and single-whitespace-fold only (the register's
  own class is defined over eleven folds, which this seat did not reproduce); a different fold could in
  principle match a span the register called absent. The negative result is stated for the two folds run.
- **The collision set is a set intersection, not a semantic diff.** 21 ids collide (20 at the 50-row moment);
  the document-level mismatch is illustrated with five examples (`S044`, `S045`, `S046`, `S047`, plus the
  staged `S034`/`S035` → lane `S049`/`S050` by-document mapping) and was not enumerated for all 21.
- **No C1/C2 measurement.** This seat read `SCORECARD.md`, `corpus/QUALITY.md` and the round-33 verifier file
  only for the Gate context it needed; nothing here verifies or disputes a claim score.

## Scratch

`/fast/scratch/hyaku/kasegi-r34/ScribeAssimilationGate/` held `fetch/` (seven bodies, metas, `s054.txt`,
`s037.txt`), `coll/`, `slice/`, `ctl/`, `assim-check.sh`. All figures and digests above were copied into this
receipt first; the tree is deleted at seat end (`rm -rf`, verified: the directory no longer exists). The
check script is embedded verbatim in § R4, so its logic survives the deletion; the only other durable
artifacts are this file and the committed `.ufo/waves/round-34/assimilation/` files that § R1 matched bit for
bit.

Report: `.ufo/waves/round-34/wave1/ScribeAssimilationGate.md`
