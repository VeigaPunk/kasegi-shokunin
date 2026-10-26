# ScribeGateAssimilation — round-35 assimilation Gate

Seat: `ScribeGateAssimilation` (scribe, wave 1, round 35). Role: draft the assimilation Gate block for the
round-35 lesson. This seat claims no axis score and judges no claim; it re-derives three measurements, reads
the wave's own receipts, and records verdicts for the L1 to integrate.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `3266c9937b03062d9bbc2f436e20820115ed179c`,
  claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`; lane `HEAD` at composition `da2d3c6`
  (dispatch commit).
- All measurements read-only. No git/jj mutation, no lane instrument run, no package tool run
  (`renumber-staged.py`, `merge-plan.py`, `quote-lint.py`, `absent-defect-register.py` never invoked),
  nothing written under `/home/vgpnk/Projects/shokuknow`. Tools installed: **none**.
- Measurement window: arithmetic derivations `06:32Z`–`06:39Z`; fetches `06:33:53Z`–`06:41Z`; receipts
  read `06:40Z`–`06:44Z`. The C2 row (`S052`) had **not** landed during that window
  (`grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md` → 0; frontier rows 17; knowledge
  entries 46), so the collision figures were derived on the 51-row registry and the C2 value was carried as
  a **prediction**; the row landed at `06:41Z`–`06:42Z` while this receipt was being written and the
  prediction was then checked against the landed bytes (§ 2, § Report R2). Both moments are printed wherever
  the figure moves.
- Scratch: `/fast/scratch/hyaku/kasegi-r35/ScribeGateAssimilation/`, deleted after this receipt was
  written (§ Report R6).

Inputs (digests read this seat):

| path | sha256 (12 hex) | note |
|---|---|---|
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` | `5afe1810a6c3` | 375 lines; byte-identical to round 34 |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md` | `4fe049cbe4ba` | 94 staged ids `S031`–`S124` |
| `/home/vgpnk/Projects/shokuknow/merge/kasegi/MERGE-REPORT.json` | `8a42a9109c8c` | `accepted 94` |
| `corpus/SOURCES.md` | `4c85ff8608dd` @06:32Z → **`0f95a132a69e` @06:42Z** | 51 rows (`S001`–`S051`) → **52 rows** (`S052` at `:58`) |
| `corpus/README.md` | `876be9cc7997` @06:32Z → **`277f04cedfb0` @06:42Z** | 17 frontier rows → **18** (`F18` at `:388`) |
| `corpus/QUALITY.md` | `807cc714d015` | 229 lines; R1–R25, **no R26** at this read |
| `corpus/knowledge/` | — | 46 entries → **47** (one citing `source: S052 `, `cisa-kev-catalog.md`) |
| `.ufo/waves/round-35/assimilation/quarantine-slice-rederived` | `7696d76c4f17` | 7 rows |
| `.ufo/waves/round-35/assimilation/quarantine-verdicts.md` | `a795951da7e2` | 18,084 B — the wave's verdict file |
| `.ufo/waves/round-35/assimilation/collisions` / `reg-ids` / `staged-ids` / `guard-proof.txt` | `e7718d617b04` / `a262e5f46ca2` / `550a0129a446` / `714ccb879518` | executor artefacts |
| `corpus/instruments/capture-source.py` | UA at `:32` | `kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)` |

Wave receipts read (all in `.ufo/waves/round-35/wave1/`): `ExecQuarantineSlice.md`, `ScoutPackageThemes.md`,
and `ExecIdCollisions.md` (the last one landed at `06:41Z`, after this receipt's first draft; its committed
artefacts under `assimilation/` had already been read and are byte-identical to this seat's own derivation —
below and § Report R5).

Seven staged entries (digests unchanged from round 34, so the package did not move):
`program-scope-rules-and-asset-boundaries.md` `120d8cd5d50b`, `claim-packaging-and-report-quality.md`
`6ad64d785f8f`, `cn-crowdsourced-testing-roles-and-conduct.md` `a5302aaf0b9a`,
`chinese-crowd-testing-national-standard-2026-10-23.md` `6c15d9411424`,
`chinese-criminal-thresholds-and-authorisation.md` `1660c00c1636…4e8a59ae`,
`chinese-program-severity-instrument.md` `442e0f2bfb08`, `program-severity-ladders-and-reward-scales.md`
`35de5f8b19ed`.

---

## Gate block for `corpus/lessons/round-35.md` (drop-in)

### Gate — assimilation: quarantine slice, id-collision re-run, standing refusals

Three components, measured read-only at `2026-10-26T06:32Z`–`06:44Z` against register
`absent-defect-register.md` (`sha256 5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`,
375 lines) and package `/home/vgpnk/Projects/shokuknow/merge/kasegi/` (`MERGE-REPORT.json 8a42a910…`,
`SOURCES.append.md 4fe049cb…`, 67 knowledge files, `accepted 94`, `renumbered 0`). The Gate's
**≥1 admit** leg is met by the round's C2 admission (`F18` / `S052`), a live-capture admission and **not**
an assimilation adoption; the **≥1 reject** leg is met by seven standing refusals and two
`prose-class-unverifiable` quarantine rows. Four quarantine rows are **candidates** (payload present and
anchors located) and **none is adopted**. Reproduce with § Report R1 (one `bash -n`-clean script,
`assim-r35-check.sh`, six runs + five controls) and R2 (fetch transcript under both UA regimes).

#### 1. Quarantine slice — 7 register rows, S-id on every line, four-label verdicts

Filter: register lane cell `kasegi` + round cell + id cell, class taken from the register section
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

`slice_rows=7 slice_malformed_lines=0`; digest `7696d76c4f17d1d9f41598e7c36def077e1f7429d947639726afdebf6e528f31`,
identical to the committed `assimilation/quarantine-slice-rederived`. **7/7 lines carry an S-id; no line
lacks one.** Two register-format facts that are not slice defects: the five never-checked ids carry a stray
trailing backtick from the register's own cell (`absent-defect-register.md:322`–`:326`), and that section has
no quote column at all. `## By lane` (`:251`) counts kasegi **2** because it counts only the
`payload-absent` table; the five never-checked rows sit in the second section, so 2 + 5 = 7 is the whole
slice.

Verdicts use the four labels defined in `assimilation/quarantine-verdicts.md` §1 —
`present-and-located`, `absent` (fabrication class), `unreachable`, `prose-class-unverifiable` (payload
retrieved, quoted text not a verbatim span: field composite, elision or paraphrase; the constituent facts
locatable). Fetch leg measured by `wave1/ExecQuarantineSlice.md` §R2–§R4 with the lane's instrument UA; every
figure below was re-measured independently by this receipt's author (§ Report R2) and matches:

| id (register line) | register class | live fetch 2026-10-26 | located anchor | verdict | adopted? |
|---|---|---|---|---|---|
| S037 openstd GB/T 30279-2020 (`:99`) | `payload-absent` | 200, 24,189 B, `text/html`, sha256 `9cba2e96e343…`, 0 redirects | fragments only: `标准状态： 现行` … `发布日期 2020-11-19 实施日期 2021-06-01`, each once, in register order | **prose-class-unverifiable** — the quoted string concatenates four page cells, drops the intervening 在线预览/CCS/ICS block and adds colons the page does not render (`发布日期 2020-11-19`, not `发布日期：2020-11-19`); exact `False`, whitespace-folded `False`, whitespace-removed `False` | **no** |
| S054 内閣府 request PDF (`:100`) | `payload-absent` | 200, 513,648 B, `application/pdf`, sha256 `0150c9d15dee…` | `S054.txt:46-47`: `（ア） 脆弱性（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認` / `されたもの又は疑われるもの` | **prose-class-unverifiable** — the span deletes the interpolated statutory parenthetical and crosses a line wrap; exact 0, folded 0; with the parenthetical restored the span is present under the no-space fold | **no** |
| S048 GB plan record (`:322`) | never checked | **404**, 748 B, `text/html` (Tomcat `HTTP状态 404 - 未找到`), sha256 `95cd25d80d88…` | — | **unreachable** — the record id is dead as cited while the host is alive (it answers S069/S070 with `302`); the register recorded no quote, so nothing is testable and this is never a fabrication | **no** |
| S065 法律目录 PDF (`:323`) | never checked | 200, 7,465,472 B, `application/pdf` (31,710 B text per `ExecQuarantineSlice.md` §R2), sha256 `e33b0f672934…` (re-measured here) | `刑法（7 件）` at `S065.txt:1182`; `现行有效法律目录（303 件）` at `:1` | **present-and-located** — the PDF is real and quotable; the register carries no quote, so "located" is against the staged catalogue anchors, not against a register claim | **no** (candidate) |
| S068 Cisco policy (`:324`) | never checked | `301`→`301`→`200` at `sec.cloudapps.cisco.com`, 94,027 B, sha256 `098f99a89df3…` | sentence contiguous **once** in tag-stripped/whitespace-collapsed text (offset depends on the collapse: 2,621 here, 22,472 in the executor's normalisation); `raw_html=0` — inline markup splits it | **present-and-located**, and the document is **already lane row `S040`** (`corpus/SOURCES.md:46`, `mined`, captures `round-25/S040.txt` `b7f7b55ff3fc…` + `round-26/S040-live.txt`, cited by `corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md:2`) — nothing new to adopt | **no** (duplicate of S040) |
| S069 consultation draft (`:325`) | never checked | `302` → attachment host; verifying client fails (`curl` 60); `-k`: **200, 1,470,121 B**, PDF 1.7 **58 pp** (size, page count and the anchor re-measured here; full digest `b0c046970f9c…` per `ExecQuarantineSlice.md` §R2) | `6.3.1 技术分级` at `S069.txt:1019` (under `6.3 漏洞分级方法`, `:1017`) | **present-and-located** with a transport caveat (§ 1a) | **no** (candidate) |
| S070 drafting note (`:326`) | never checked | same transport; `-k`: **200, 234,182 B**, PDF 1.7 **8 pp** (size, page count and the anchors re-measured here; full digest `2eff0a5b10e2…` per `ExecQuarantineSlice.md` §R2) | `一、工作简况` at `S070.txt:8`, `1.1 任务来源` at `:9`, plan no `20260806-T-469` at `:13` | **present-and-located** with the same caveat | **no** (candidate) |

Totals: **present-and-located 4** (S065, S068, S069, S070) · **prose-class-unverifiable 2** (S037, S054) ·
**unreachable 1** (S048) · **absent 0** · **adopted 0**. Note that `absent 0` is a real result and not a
grid: the two rows whose register class was `payload-absent` are **quote-form** defects (a collage and an
elision), which is why they are refused as quoted without being called fabrications — the register's own
preamble says an unmatched quote is a candidate, not a verdict.

##### 1a. A fetch verdict is a property of the invocation, not of the source

Measured this round by running the same seven URLs under two regimes; three rows move, four do not:

| row | browser-UA `curl -L` (this seat, `06:33Z`) | instrument-UA `curl -L` (`capture-source.py:32`) | what decided it |
|---|---|---|---|
| S068 | **403**, 465 B `Access Denied` | **301→301→200**, 94,027 B, sentence located | **UA** (the host gates browser strings) |
| S069 / S070 | **200, 0 B** | **302** → TLS-incomplete host → `curl` 60; with `-k`, 1,470,121 B / 234,182 B | **URL cell truncation + TLS chain** (the register's cell ends at `…%E8%8D%89%2F`, a directory path that answers 200/0 B; the real PDFs need the full `20_WD_…` / `20_DI_…` path, and the attachment host omits its intermediate — `verify error:num=21`, corroborated independently by staged row `SOURCES.append.md:95` `S119` recording the same DI attachment at **234,182 B** over plain `http`) |
| S037 | 200, 24,209 B, sha `b98b1342…` | 200, 24,189 B, sha `9cba2e96…` | **UA** (page rotates content); verdict identical both ways: span absent, every fragment once, in order |
| S054, S048, S065 | byte-identical across regimes (`0150c9d1`, `95cd25d8`, `e33b0f67`) | same | nothing |

Consequences that belong in the lesson and in any future check:

1. A quarantine closure check **must pin the UA** to `corpus/instruments/capture-source.py:32`, follow
   redirects, and **state its TLS policy**. A verifying-only client manufactures `unreachable` verdicts for
   S069/S070 whose payload exists; a browser UA manufactures a 403 for S068 whose sentence exists.
2. **Correction to round-34's Gate table** (stated as an erratum-class note, not a rewrite): its rows
   "S068 **403** (465 B `Access Denied`)" and "S069/S070 200, **0 B** … unreachable in substance" were true
   of that invocation (desktop UA, register cell verbatim) and are not true of the sources. Round 34's
   *disposition* (0 adopted) stands; its two verdict classes do not.
3. The slice's numbers are UA-stable; only reachability labels move. So a reader can trust
   `slice_rows=7` from any UA and must not trust `unreachable` from any UA.

#### 2. Id-collision check — 21 collisions before the C2 row, 22 after, guard load-bearing

```
# at the measurement window (51-row registry, 4c85ff8608dd)
reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
# re-run after the C2 row landed (52-row registry, 0f95a132a69e, 06:42Z)
reg_ids=52 staged_ids=94 collisions=22 collision_range=S031..S052 slice_rows=7 slice_malformed_lines=0
```

- Registry ids: `^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}` over `corpus/SOURCES.md` (`4c85ff8608dd`) → 51 unique
  (`S001`–`S051`), digest `a262e5f46ca2`. Staged ids: 94 unique (`S031`–`S124`), digest `550a0129a446`,
  from **two independent routes that agree byte for byte** — the 67 package knowledge files
  (`^[ ]{0,3}source:[[:space:]]*S[0-9]{3,}`) and the `SOURCES.append.md` rows (94 ids over 96 `|` lines):
  same 94 ids, same digest, `diff` empty.
- `comm -12` → `S031`…`S051` inclusive, 21 ids, digest `e7718d617b04` — equal to the committed
  `assimilation/collisions` (`e7718d617b04`), to the executor's `reg-ids`/`staged-ids`, and to the scout's
  independent python3 pass (`wave1/ScoutPackageThemes.md` §2: `lane_rows 51 S001 S051`, `collisions 21`).
  **Three independent derivations, identical bytes.**
- Guard sensitivity, proved on a fixture (`assimilation/guard-proof.txt` `714ccb87`, re-proved here): a
  synthetic registry with one 2-space-indented `S031` row → 0–3-space pattern finds `S001 S031` and reports
  **1** collision; column-0-only finds `S001` and reports **0**. Boundary limits, measured: 3-space indent
  **caught** (reg_ids 51), 4-space indent **missed** (reg_ids 50, collisions 20 `S032..S051`), tab indent
  missed. Missing registry → `reg_ids=0`, exit 1; missing register → `awk: fatal`, exit 2: the guard fails
  closed both ways.
- Discrimination (each control moves exactly one figure):

| run | output | exit |
|---|---|---|
| baseline, append route | `reg_ids=51 staged_ids=94 collisions=21 S031..S051 slice_rows=7 malformed=0` | 0 |
| baseline re-run (determinism) | identical | 0 |
| baseline, knowledge route | identical | 0 |
| registry `+S052` fixture (C2 prediction) | `reg_ids=52 … collisions=22 S031..S052 slice_rows=7` | 0 |
| registry `-S037` fixture | `reg_ids=50 … collisions=20 …` | 0 |
| register `-S054` row fixture | `… collisions=21 … slice_rows=6` | 0 |
| missing register | `awk: fatal …` (no figures printed) | 2 |
| missing `SOURCES.md` | `reg_ids=0 … collisions=0 … slice_rows=7` | 1 |

- **C2 prediction, stated before the row landed and then confirmed:** with `S052` appended the check must
  read `reg_ids=52 staged_ids=94 collisions=22 collision_range=S031..S052`. The scout reproduces that value
  through `assimilation/collide-check.sh` (`kind=wide reg_ids=52 collisions=22 … S052`, exit 0) as a
  fixture, and the **landed tree now reads exactly it** (`corpus/SOURCES.md 0f95a132a69e`, 52 rows, `06:42Z`;
  § Report R2). A landing that had read 21 collisions with 52 rows would have meant a malformed `S052` row —
  it did not.
- **Adopt by document, never by number.** Staged `S044`/`S045`/`S046` are 最高人民法院 2011 解释 / 刑法 2023
  修正 / 南京市检察院 指南; lane `S044`/`S045`/`S046` are Bugcrowd VRT README / Bugcrowd VRT CWE mapping /
  IPA JVN activity report. Fresh this round: **staged `S052` is CNNVD's weekly advisory
  (`信息安全漏洞周报（2026 年第 40 期，总第 853 期）`, `SOURCES.append.md:28`) while lane `S052` is the CISA
  KEV JSON feed** (`corpus/source-snapshots/round-35/manifest.json`) — the collision count rises 21 → 22
  without a single document coming into conflict. Two of the quarantine ids are worse than arithmetic: lane
  `S037` (`:43`) is the Cybozu bounty FAQ and lane `S048` (`:54`) is Microsoft MSVR, both already cited by
  knowledge entries (`vendor-disclosure-policies-as-corpus-objects.md:4`,
  `vendor-third-party-finding-coordination.md:2`), so adopting register `S037`/`S048` by number would bind a
  live id to a different document. The executor's renumber maps show the arithmetic (`renumber-map-pre-c2`:
  `S031 → S052`; `post-c2`: `S031 → S053`; the seven quarantined rows carried `HOLD(quarantine)` in both).

#### 3. Standing refusals re-confirmed, each with the flip condition still unmet

Package digests unchanged (§ Inputs), so no refusal can have been lifted by package movement; the lane side
was re-measured today by this seat and re-measured independently by `wave1/ScoutPackageThemes.md` §3 with the
same counts:

| staged entry | decision (standing) | measured today | flip condition | met? |
|---|---|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | REFUSED (round 30) | `grep -cE 'txt:[0-9]+'` → 0 located quotes; `ground: F09` names a different lane item | register+capture CNVD helpList and 360SRC rules (**met**, S049/S050) **and** located quotes, per-platform attribution, executable recheck, re-ground on a lane frontier | **no** |
| `claim-packaging-and-report-quality.md` | REFUSED (standing) | `grep -ci 'bilibili\|BILISRC' corpus/SOURCES.md` → 0 | register+capture S034/S035/**S036** | **no** — BILISRC still in no lane row and no capture |
| `cn-crowdsourced-testing-roles-and-conduct.md` | REFUSED (standing) | `grep -c '^# '` on the staged file → 0 (no H1); `grep -c 'newsTypeCode=100100' corpus/SOURCES.md` → 0 | H1, register+capture S081/S082, page/line quotes with exactly-once counts | **no** |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | REFUSED (standing) | `std.sacinfo` → 0, `sac.gov.cn` → 0, `57CAF3B4` → 0 rows; `grep -cE '^\| F24 \|' corpus/README.md` → 0 (frontier is F01–F17) | register+capture S077/S078/S079, quote the roles-and-duties sentence with a location, re-ground on a lane F-id | **no** |
| `chinese-criminal-thresholds-and-authorisation.md` | REFUSED (round 30) | `court.gov.cn` → 0, `czt.ln.gov.cn` → 0, `nj.jsjc.gov.cn` → 0 rows; its staged ids `S044`–`S046` are occupied | register+capture S044/S045/S046 in a non-colliding id space, bound the conclusion to located text | **no** |
| `chinese-program-severity-instrument.md` | REFUSED as an entry (round 33) | `sse.com.cn` → 0; anchor `newsType_6` → 0 in `round-32/S049.txt` (`newsType_21` → 1) | anchor present in a capture, second source registered | **no** |
| `program-severity-ladders-and-reward-scales.md` | REFUSED / do-not-copy | same-name lane entry differs: staged `35de5f8b`/50 L vs lane `6c05c98f`/67 L | overwrite hazard, not a flip | **unchanged** |

#### 4. Assimilation: none adopted

`grep -ci 'immunefi\|cisa\|known exploited' SOURCES.append.md` → **0** and
`grep -rliE 'cisa|known.exploited|kev'` over the package's 67 knowledge files → **0 files** (the scout's
whole-package pass agrees), so this round's new ground (F18 / S052, CISA KEV) cannot unblock any refused
entry. No staged entry's flip set is fully met (table above). **No new refusal is opened and no prior
refusal is lifted.**

Per-row reasons for the quarantine slice (from `assimilation/quarantine-verdicts.md` §6, reproduced here so
the lesson needs one file):

- **S037, S054** — not adoptable **as quoted** (`prose-class-unverifiable`): a corrected, cell- /
  parenthetical-anchored quote must be written and re-checked first. **Reject.**
- **S048** — `unreachable`: the record id is dead; adoption blocked until a `supersedes` row re-points at a
  live id. **Reject.**
- **S065** — quotable, but the register carries no quote for it and the staged entry that cites it was never
  adopted; a hand-written quote would be new work, not an adoption. **Candidate for a later round, not
  adopted.**
- **S068** — the document is already lane row `S040`; adopting it again would duplicate a source under a
  colliding id. **Nothing to adopt.**
- **S069, S070** — payload and anchors located, but re-checking depends on a TLS-bypass or plain-`http`
  fetch; a row whose verification path needs a transport exception may be adopted only with that exception
  recorded in the row itself. **Candidates for a later round, not adopted.**

The Gate's admit leg is therefore met by the C2 admission (`F18` / `S052`, live capture, `fetched_utc
2026-10-26T06:32:40Z`), which is a new source, not an adoption of package bytes; recording it as an
assimilation adopt would overclaim. Confirmed on the landed tree at `06:42Z`: registry row `S052` at
`corpus/SOURCES.md:58` (`CISA Catalog of Known Exploited Vulnerabilities (KEV catalog JSON feed)`, tier `A`,
`dataset`), frontier row `F18` at `corpus/README.md:388` (`admitted`), and one knowledge entry carrying
`source: S052 ` (`corpus/knowledge/cisa-kev-catalog.md`; 47 entries).

##### 4a. Closure spot-check list for the non-author

Two rejects and three candidates, each with a command whose value is fixed:

| leg | item | command | expected |
|---|---|---|---|
| reject A | S037 | `curl -sSL -A "$UA" <openstd hcno=458BACCE…>` then tag-strip/ws-collapse and test the register span | `200 24189`, exact `False`, folded `False`, each of the 8 fragments ×1, in order |
| reject B | S054 | `curl -sSL -A "$UA" <ipa request_to_ipa.pdf> \| pdftotext -layout - -` then count the span | `200 513648`, exact `0`, folded `0`; `悪用が確認されたもの` ×1; parenthetical present |
| reject C | S048 | `curl -sSL -A "$UA" <std.samr gbDetailed?id=3B865A93…>` | `404 748`, body `HTTP状态 404 - 未找到` |
| candidate | S069 | `curl -sSLk -A "$UA" <full 20_WD_… path>` + `pdftotext -layout` + `grep -n '6.3.1 技术分级'` | `200 1470121`, 58 pp, hit at `:1019` |
| candidate | S070 | same with `<full 20_DI_… path>` + `grep -n '一、工作简况'` | `200 234182`, 8 pp, hit at `:8` |
| candidate | S065 | `curl -sSL -A "$UA" <npc.gov.cn P020260904396146393500.pdf>` + `pdftotext -layout` + `grep -n '刑法（7 件）'` | `200 7465472`, hit at `:1182` |

Any spot-check that fetches with a verifying-only client or a browser UA will see `unreachable`/`403` on
S068–S070 and should read § 1a before recording a defect.

#### 5. Contested scope — pointer only, not absorbed here

The sibling-overlap ruling for this round lives in `wave1/ConnSibling-ruling-draft.md` (connector seat,
`wave1/ConnSibling.md` for its commands) and belongs to the lesson's **contested-scope record**, which the
L1 / `ScribeLesson` splices; this Gate block claims no part of it. Two facts tie it to the block above and
were measured here:

- **No intersection with any assimilation figure.** `grep -ci 'immunefi\|cisa\|known exploited'
  SOURCES.append.md` → 0 and `grep -rliE 'cisa|known.exploited|kev'` over the package's 67 knowledge files
  → 0 files: no staged entry, and therefore no refusal or candidate in § 1–§ 4, touches the CISA/KEV ground
  the ruling protects. The ruling's subject is the C2 admit leg (`F18` / `S052`), named in § 4.
- **A count quoted by the ruling needs its pattern.** Against `corpus/SOURCES.md` at `06:46Z`:
  `grep -ciE '\bCISA\b|\bKEV\b'` → **11** lines (`:9 :14 :27 :29 :32 :58 :70 :71 :79 :108 :112`), so the
  scout's `10` was stale by the `:112` search-log scope-correction line, while the scout's own wider pattern
  (`+ known exploited | BOD 22-01 | exploited vulnerabilit | remediation deadline`) reads **12** lines here.
  Both are correct for their pattern; a lesson that prints one number without the pattern repeats the
  class of defect C1 is closing.

---

## Report

### R1 — Reproducible check with controls (`assim-r35-check.sh`, `bash -n` clean)

`bash -n` exit 0; script digest `8278e328daa41d4ae81ffa6abaada6e00066adf1bdef3584a298608e1007f627`. Embedded
verbatim (scratch is deleted, so this copy is the durable one; args are
`[register] [SOURCES.md] [route: append|knowledge]`):

```sh
#!/usr/bin/env bash
# assim-r35-check.sh [register] [SOURCES.md] [staged-source: append|knowledge]
set -u
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin || exit 9
reg=${1:-/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md}
src=${2:-corpus/SOURCES.md}
route=${3:-append}
t=$(mktemp -d) || exit 9
if [ "$route" = knowledge ]; then
  grep -ohE '^[ ]{0,3}source:[[:space:]]*S[0-9]{3,}' \
    /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/*.md \
    | grep -ohE 'S[0-9]{3,}' | sort -u > "$t/staged"
else
  grep -ohE '^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}' \
    /home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md \
    | grep -ohE 'S[0-9]{3,}' | sort -u > "$t/staged"
fi
grep -ohE '^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}' "$src" | grep -ohE 'S[0-9]{3,}' | sort -u > "$t/reg"
comm -12 "$t/reg" "$t/staged" > "$t/coll"
awk -F'|' '
  /^## Rows whose quotes were NEVER CHECKED/{sec="nc";next}
  /^## Rows$/{sec="pa";next}
  /^## /{sec=""}
  sec!="" && $2 ~ /kasegi/ {
    rnd=$3; id=$4
    gsub(/^[ `]+|[ `]+$/,"",rnd); gsub(/^[ `]+|[ `]+$/,"",id)
    if (id ~ /^S[0-9][0-9][0-9]$/) print id" | "rnd" | "(sec=="nc"?"unreachable":"payload-absent")
  }' "$reg" > "$t/slice" || { echo "awk_fatal exit=$?"; rm -rf "$t"; exit 2; }
reg_ids=$(wc -l < "$t/reg"); staged_ids=$(wc -l < "$t/staged"); coll=$(wc -l < "$t/coll")
slice=$(wc -l < "$t/slice")
bad=$(grep -cvE '^S[0-9]{3} \| round[0-9]+ \| (payload-absent|unreachable)$' "$t/slice")
printf 'route=%s reg_ids=%s staged_ids=%s collisions=%s collision_range=%s..%s slice_rows=%s slice_malformed_lines=%s\n' \
  "$route" "$reg_ids" "$staged_ids" "$coll" "$(head -1 "$t/coll")" "$(tail -1 "$t/coll")" "$slice" "$bad"
rm -rf "$t"
[ "$reg_ids" -ge 1 ] && [ "$slice" -ge 1 ] && [ "$bad" -eq 0 ]
```

Runs (all `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin`; `$S` = this seat's scratch dir):

```
$ bash $S/assim-r35-check.sh
route=append reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
exit=0
$ bash $S/assim-r35-check.sh                      # determinism, second run
route=append reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
exit=0
$ bash $S/assim-r35-check.sh "" "" knowledge      # second staged-id route
route=knowledge reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
exit=0
$ bash $S/assim-r35-check.sh "" $S/src-plus-S052.md
route=append reg_ids=52 staged_ids=94 collisions=22 collision_range=S031..S052 slice_rows=7 slice_malformed_lines=0
exit=0
$ bash $S/assim-r35-check.sh "" $S/src-minus-S037.md
route=append reg_ids=50 staged_ids=94 collisions=20 collision_range=S031..S051 slice_rows=7 slice_malformed_lines=0
exit=0
$ bash $S/assim-r35-check.sh $S/reg-minus-S054.md
route=append reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 slice_rows=6 slice_malformed_lines=0
exit=0
$ bash $S/assim-r35-check.sh $S/nonexistent.md
awk: fatal: cannot open file `…/nonexistent.md' for reading: No such file or directory
awk_fatal exit=2
exit=2
$ bash $S/assim-r35-check.sh "" $S/nope.md
grep: …/nope.md: No such file or directory
route=append reg_ids=0 staged_ids=94 collisions=0 collision_range=.. slice_rows=7 slice_malformed_lines=0
exit=1
$ bash $S/assim-r35-check.sh "" $S/guard-SOURCES.md   # 2-space-indented S031
route=append reg_ids=51 staged_ids=94 collisions=21 collision_range=S031..S051 …
$ bash $S/assim-r35-check.sh "" $S/src-4sp.md         # 4-space-indented S031
route=append reg_ids=50 staged_ids=94 collisions=20 collision_range=S032..S051 …
```

Scratch digests (deleted at exit): `assim-r35-check.sh` `8278e328…`, `reg-ids` `a262e5f4…`,
`staged-ids` `550a0129…`, `staged-ids-append` `550a0129…` (routes agree), `collisions` `e7718d61…`,
`coll-append` `e7718d61…`, `slice` `7696d76c…`, plus the four fixtures.

Independent completeness cross-checks on the register: `## By lane` holds `| \`kasegi\` | 2 |` (`:251`);
`## Totals` holds `rows with at least one ABSENT quote: 194`, `ABSENT quotes: 324`; the never-checked
section supplies the other 5 kasegi rows (`:322`–`:326`), so 2 + 5 = 7. The naive `awk` printed in the
seat's own dispatch (`$2 ~ "\`kasegi\`" && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/`) also yields 7 lines but
prints the *reason* column, not a class; the section-state machine above is what produces the two register
classes. This is the trap round 34 recorded: a filter that lets the never-checked header rematch `^## Rows`
folds five `unreachable` rows into `payload-absent`. Both projections are on disk
(`assimilation/quarantine-slice` `d02acb68cb40` = the raw-cell dump; `quarantine-slice-rederived`
`7696d76c…` = the classified slice) and agree on the seven ids and their order.

### R2 — Live fetch transcript, two regimes (this seat's own measurement)

Regime A, browser UA (`Chrome/131.0`), register cells verbatim — the regime that produces round-34's
numbers:

```
s037 200 24209    text/html;charset=utf-8  06:33:53Z  sha256 b98b1342b4b288b464eb0493086083971170fe54f1d1c1996bc745ead657c169
s054 200 513648   application/pdf          06:33:55Z  sha256 0150c9d15dee603f55573f4692f306ba8ff46f70454b032f813b95fbdbb12b88
s048 404 748      text/html;charset=utf-8  06:33:56Z  sha256 95cd25d80d88cce1e08528c03d5eb488f56bf9991f820bc31569b001eb2e2436
s065 200 7465472  application/pdf          06:34:43Z  sha256 e33b0f67293441f19ee519b2ed1619121da84867aa8396a3a16facd572586d83
s068 403 465      text/html                06:34:43Z  sha256 4ca9acac36657a950b7895693d976dcd145041e7811cc6f52603025dc070155e
s069 200 0        (none)                   06:34:44Z  sha256 e3b0c44298fc…b7852b855   (register cell = directory path)
s070 200 0        (none)                   06:34:45Z  sha256 e3b0c44298fc…b7852b855   (same URL twice)
```

Regime B, instrument UA (`corpus/instruments/capture-source.py:32`), full paths:

```
$ UA='kasegi-shokunin/1.0 (documentation capture; +https://shokunin.invalid/kasegi)'
s037 200 24189     text/html;charset=utf-8  sha256 9cba2e96e343e1d0c95d23fb50454fa1321cb2d01af6ae318653290a1d20f204
s068 200 94027     text/html;charset=ISO-8859-1  sha256 098f99a89df3a8018ab6eff7529fd8482af70dde6406472b88d526c773ded807
     effective https://sec.cloudapps.cisco.com/security/center/resources/security_vulnerability_policy.html   (301→301→200)
s069 200 0         (register cell, unchanged — the truncation is in the register, not the UA)
s070 200 0         (same)
$ curl -sSLk -A "$UA" 'https://kass.sacinfo.org.cn/kfs/token/download/mirciskbdmzdvuov'
s069 200 1470121   application/octet-stream;charset=UTF-8     PDF 1.7, 58 pages, pdftotext 146961 B
$ curl -sSLk -A "$UA" 'https://kass.sacinfo.org.cn/kfs/token/download/iwpbpsmwxkkibqpk'
s070 200 234182    application/octet-stream;charset=UTF-8     PDF 1.7, 8 pages,  pdftotext 19747 B
```

Anchor and fold tests (this seat's runs):

```
S037  instrument-UA body, tag-stripped + ws-collapsed: 824 chars
      exact False | folded False | fragments each 1 | positions [238,245,377,383,440,445,456,461] ordered True
      live field run: 标准状态： 现行 在线预览 下载标准 实施信息反馈 中国标准分类号（CCS） L80
                      国际标准分类号（ICS） 35.040 发布日期 2020-11-19 实施日期 2021-06-01
S054  pdftotext -layout: 9780 B (UTF-8); exact 0 | folded 0
      確認されたもの又は疑われるもの 1 ; 悪用が確認されたもの 1 ; 法第42条第１項に規定する脆弱性をいう 1
      live clause: 脆弱性（（法第42条第１項に規定する脆弱性をいう。以下同じ。）の悪用が確認されたもの又は疑われるもの
S068  tag-stripped + ws-collapsed: 33752 chars; sentence count 1 (offset 2621); raw_html count 0
      context: …responsible for responding to Cisco product security incidents. The Cisco PSIRT aligns its
               practices with ISO/IEC 29147:2018 , which are guidelines for disclosure of potential …
S065  pdftotext -layout: 刑法（7 件） at line 1182 ; 现行有效法律目录（303 件） at page 1
S069  pdftotext -layout: 6.3.1 技术分级 at line 1019
S070  pdftotext -layout: 一、工作简况 at line 8
S048  body: HTTP状态 404 - 未找到
```

Reproducibility caveats, stated rather than smoothed: (a) the S068 sentence offset depends on the
whitespace normalisation (2,621 with `\s+`→single-space here, 22,472 in the executor's pass) while the
count is 1 either way; (b) the S037 page rotates per request (24,209 B vs 24,189 B, different digests under
the two UAs; 824 collapsed chars here vs 9,119 in round 34), and its verdict is unchanged because the test
is span-absence plus fragment-count; (c) the S068 `403` body carries a rotating `Reference #`, so its
digest is not a stable identifier — the `200` payload digest is.

Post-landing re-read (`06:42:41Z`, after the C2 row appeared; scratch already deleted, so this is a direct
lane read):

```
$ grep -cE '^\|[[:space:]]*S052[[:space:]]*\|' corpus/SOURCES.md          -> 1     (row at :58, tier A, dataset)
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md    -> 52
$ grep -cE '^\| F[0-9]+ \|' corpus/README.md                              -> 18    (F18 at :388)
$ grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l                 -> 1     (cisa-kev-catalog.md)
$ ls corpus/knowledge/*.md | wc -l                                        -> 47
$ grep -ohE '^[ ]{0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md | grep -ohE 'S[0-9]{3,}' | sort -u \
  | comm -12 - <(grep -ohE '^[ ]{0,3}source:[[:space:]]*S[0-9]{3,}' \
      /home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/*.md \
      | grep -ohE 'S[0-9]{3,}' | sort -u) | wc -l                         -> 22    (S031..S052)
sha256sum corpus/SOURCES.md corpus/README.md
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md
```

The landed collision count is the predicted 22, computed by the same two greps used in R1 — no instrument
was written to make the prediction come true.

### R3 — Lane blast radius, same-number precision, candidate rows

```
$ for f in chinese-vulnerability-taxonomy-and-grading.md chinese-national-grading-model.md \
    chinese-statute-version-drift-2026-10-23-r4-amendment.md iso-29147-divergence-and-clause-crosswalk-2026-10-23.md \
    vendor-cvd-policy-crosswalk-2026-10-23.md chinese-grading-standard-draft-2026-10-23.md \
    authorization-safe-harbor-and-scope-2026-10-23-amendment.md; do [ -f corpus/knowledge/$f ] …; done
absent ×7                                                    # none of the seven staged citers is in the lane
$ grep -rn 'source: S037\|source: S048' corpus/knowledge/*.md
vendor-disclosure-policies-as-corpus-objects.md:4:source: S037 — https://cybozu.co.jp/products/bug-bounty/faq/ …
vendor-third-party-finding-coordination.md:2:source: S048 — https://www.microsoft.com/en-us/msrc/msvr …
$ grep -nE '^\|[[:space:]]*S0(37|48)[[:space:]]*\|' corpus/SOURCES.md
43:| S037 | FAQ（脆弱性報奨金制度） (サイボウズ) — https://cybozu.co.jp/products/bug-bounty/faq/ | …
54:| S048 | Microsoft Security Vulnerability Research (MSVR) — https://www.microsoft.com/en-us/msrc/msvr | …
$ grep -c -F 'std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3' corpus/SOURCES.md   # 0
$ grep -c -F 'request_to_ipa.pdf' corpus/SOURCES.md                                                          # 0
$ grep -c -F 'security-vulnerability-policy.html' corpus/SOURCES.md                                          # 1  (lane S040)
```

Blast radius is **0 in document terms**: the seven staged entries citing the quarantined ids are absent from
`corpus/knowledge/`, and no admitted lane entry rests on a refused row. The same-number citations are
different documents (§ 2). The single document that *is* registered — S068/Cisco → lane `S040` — is the only
join between the register slice and the registry, and it yields nothing adoptable
(`corpus/source-snapshots/round-25/manifest.json` records three located quotes for it; the sentence
`The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018` occurs exactly once in both
`round-25/S040.txt` and `round-26/S040-live.txt`).

### R4 — Refusal predicates (commands and counts)

```
grep -ci 'bilibili\|BILISRC' corpus/SOURCES.md              -> 0
grep -c 'newsTypeCode=100100' corpus/SOURCES.md             -> 0
grep -c 'D0FE299A' corpus/SOURCES.md                        -> 0
grep -c 'std.sacinfo' corpus/SOURCES.md                     -> 0
grep -c 'sac.gov.cn' corpus/SOURCES.md                      -> 0
grep -c '57CAF3B4' corpus/SOURCES.md                        -> 0
grep -c 'court.gov.cn' corpus/SOURCES.md                    -> 0
grep -c 'czt.ln.gov.cn' corpus/SOURCES.md                   -> 0
grep -c 'nj.jsjc.gov.cn' corpus/SOURCES.md                  -> 0
grep -c 'sse.com.cn' corpus/SOURCES.md                      -> 0
grep -c '府連' corpus/SOURCES.md                            -> 0
grep -c 'openstd' corpus/SOURCES.md                         -> 0
grep -cE '^\| F24 \|' corpus/README.md                      -> 0
grep -cE '^\| F18 \|' corpus/README.md                      -> 0     (C2 not landed at read)
grep -c '^# ' <staged cn-crowdsourced…>                     -> 0
grep -cE 'txt:[0-9]+' <staged program-scope…>               -> 0
grep -ci 'immunefi\|cisa\|known exploited' SOURCES.append.md -> 0
grep -rliE 'cisa|known.exploited|kev' <pkg knowledge>/*.md | wc -l -> 0
sha256sum <pkg knowledge>/program-severity-ladders-and-reward-scales.md -> 35de5f8b19ed… (50 L)
sha256sum corpus/knowledge/program-severity-ladders-and-reward-scales.md -> 6c05c98f3c68… (67 L)
```

Every predicate is a count-zero or a byte comparison; no refusal rests on an opinion of the text. The scout
re-measured the same set (`wave1/ScoutPackageThemes.md` §3) and prints the same values.

### R5 — Receipt cross-check, and the one divergence found and closed

Landed and read: `wave1/ExecQuarantineSlice.md` (fetch leg + `assimilation/quarantine-verdicts.md`
`a795951da7e2`), `wave1/ScoutPackageThemes.md` (refusal leg), and — landing at `06:41Z`, after this receipt's
first draft — `wave1/ExecIdCollisions.md` (collision leg). The collision seat's §1 runs the assignment's
block verbatim (`exit codes 0 0 0`, `reg-ids=51`, `staged-ids=94`, `collisions=21`, range `S031..S051`), adds
a `uniq -d` duplicate check on both sides (empty) and a `comm -3` between its two staged-id routes (0 lines),
and its committed artefacts `reg-ids a262e5f4…` / `staged-ids 550a0129…` / `collisions e7718d61…` are
byte-identical to this seat's independent derivation (§ Inputs, § R1).

- **Agreements** (independent seats, same numbers): slice 7 ids/order; collisions 21 `S031..S051`;
  `+S052` → 22 `S031..S052`; guard load-bearing with the 3-space caught / 4-space missed boundary; all seven
  refusal predicates unmet; package digests unchanged; staged `S052` ≠ lane `S052` by document.
- **Divergence, found and closed.** This seat's first fetch pass (browser UA, register cells verbatim)
  produced `S068 403` and `S069/S070 200 0 B`, and an earlier draft of this receipt carried those as
  `unreachable`. `wave1/ExecQuarantineSlice.md` §8 flagged that divergence and diagnosed its cause; this seat
  re-fetched under the instrument UA with full paths and reproduced the executor's payloads exactly
  (§ R2 regime B). The corrected verdicts are the ones in § 1 (`present-and-located` for S068/S069/S070).
  The lesson must carry **task-level**, not source-level, reachability labels — § 1a is that finding.
- **Seat coverage per leg**: the four fetch verdicts rest on two seats (this one and `ExecQuarantineSlice`),
  the seven refusal predicates on two (this one and `ScoutPackageThemes`), and the collision arithmetic on
  three (this seat, `ExecIdCollisions`' artefacts and receipt, and the scout's python3 pass). No number in
  the Gate block comes from a single seat that never filed evidence.

### R6 — Files written, scratch, tools

- Written in the lane: this file only (`.ufo/waves/round-35/wave1/ScribeGateAssimilation.md`). No git/jj
  command of any kind was run; no lane instrument, no package tool, nothing under
  `/home/vgpnk/Projects/shokuknow` or the fleet root.
- Scratch `/fast/scratch/hyaku/kasegi-r35/ScribeGateAssimilation/` (derivation outputs, the check script,
  seven bodies under two UA regimes, the two TLS-bypassed PDFs and their text renders, five fixtures) copied
  into this receipt first, then deleted; `tree_gone=yes`.
- Tools installed or upgraded: **none** (`pacman` untouched, no `uv`/`npm`/`cargo` transaction). Toolchain
  used: `curl`, `awk`, `comm`, `grep`, `sha256sum`, `python3`, `pdftotext`/`pdfinfo` (poppler) — all
  pre-installed.

Report: `.ufo/waves/round-35/wave1/ScribeGateAssimilation.md`
