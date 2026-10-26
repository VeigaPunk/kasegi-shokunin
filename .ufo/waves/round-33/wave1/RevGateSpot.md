# RevGateSpot — round-33 Gate discernment spot-check

Seat: RevGateSpot (leaf reviewer). Label per LEARNING.md: **lane-seat** — a seat this lane
dispatched re-opening the lane's own Gate; the non-author closure follows from the seat role,
not from independence. Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (write scope: this
receipt only). `/home/vgpnk/Projects/shokuknow` read-only (package `merge/kasegi/`, register
`absent-defect-register.md`; no campaign tool run, nothing written). Answering model actually
run on: `devin/glm-5-3-flash-1m` (workstation config; item does not hinge on a route choice).
No tool installs. Scratch `/fast/scratch/hyaku/kasegi-r33/RevGateSpot/`, removed before yield.

Gate read after `wave1/ScribeLesson.md` appeared (polled `until [ -s … ]`, sleep 20, ~26 min
wait; `corpus/lessons/round-33.md` `## Gate` landed). All landed-byte measurements below were
taken after that landing; the entry was **re-read on quiescent bytes** after M33-4's fix
(digest `1f7ac0a2…`, `提交漏洞时=2 漏洞提交时=0`) — my first read had been pre-fix.

## Verdicts

| Item | Verdict | Reason |
|---|---|---|
| (a) S049/S050 located quotes vs fresh fetch | **agree** | My own fresh fetch 2026-10-26T04:22Z (instrument UA, scratch): both HTTP 200; converted text **byte-identical** to the committed captures (sha256 `962a451a…1cb8` / `2f9c6406…6888`, `diff` empty both). All 14 manifest quotes sit at their stated lines; every line-ref in the two landed rows resolves (S049: L7/L10/L52/L71/L72/L131/L132/L134-135/L207-209/L210-212/L213-214/L409-410/L425; S050: L3/L5/L7/L69-71/L73/L86-87/L90-92/L98-100/L112/L118-125/L129/L418/L557-560/L595-598). The Gate's two quotes are present at `S049.txt:214` and `S050.txt:591`. Finding: the Gate's **character counts are wrong** (below). |
| (b) ADMIT staged S034/S035 → lane S049/S050 by document | **agree** | URL byte-equal at every hop: staged cell == manifest `url` == landed row cell, `https://zc.cnvd.org.cn/news/helpList` and `https://security.360.cn/Reward/rules`, 36 bytes each, no query/fragment/slash difference. Document identity confirmed: the lane capture IS the staged document's conversion (fresh fetch byte-identical). Collision guard re-derived: `reg_ids=48`, `staged_ids=94` (S031–S124 contiguous), `collisions=18` (S031–S048) — adoption by document is the only sound mapping. |
| (c) REFUSALs + quarantine verdicts | **agree** | Every stated criterion checked against the staged entry / register row (detail below). Quarantine slice re-derived byte-identically from register lines 99-100/322-326 (`diff` exit 0, all 7 rows `kasegi`); S037 refuse (spliced collage) and S054 refuse (elided parenthetical) consistent with the register rows and `wave1/ExecQuarantine.md` §4-§5; 5 unreachable rows never reported as fabrication; S065/S068 reachable-today note matches `wave1/ScoutPackageThemes.md` §3 (S068 URL byte-equal to lane `S040` — I re-verified that equality myself). |
| (d) R20/R21 row citations resolve | **agree** | `corpus/QUALITY.md` rows R20/R21 exist (lines 169-170; committed at `9f98488`, `git show 9f98488:corpus/QUALITY.md \| grep -cE '\| R2[01] \|'` → 2). R20 grounded-in → `corpus/lessons/round-33.md` § Mistakes M33-1 (present, line 91, cites both R20 and R21) + `round-32-verifier-spotcheck.md:93` D5 (verbatim: "are committed without a `round-32/manifest.json`", "so the 38-record target is not silently moved") + the base-measurement block (present, reproducible, matches the frozen control `dirs=9 manifest_records=38 with_url=0`). R21 grounded-in → `round-31.md:146` ("manifest `url`/`fetched_utc` fields and a census URL↔capture comparison") + `.ufo/waves/round-31/wave1/CritC2Kill.md:232` ("No URL↔capture binding anywhere") — both resolve to the quoted text. |

## Commands and output

### (a) fresh fetch + quote/line verification

```
python3 corpus/instruments/capture-source.py --id S049 --url https://zc.cnvd.org.cn/news/helpList --kind html --out $S/S049-fresh.txt
S049 status=200 fetched_bytes=56674 snapshot_bytes=20272 sha256=962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8 utc=2026-10-26T04:22:17Z
python3 corpus/instruments/capture-source.py --id S050 --url https://security.360.cn/Reward/rules --kind pdf --out $S/S050-fresh.txt
S050 status=200 fetched_bytes=427391 snapshot_bytes=31016 sha256=2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888 utc=2026-10-26T04:22:26Z
sha256sum committed vs fresh: identical both ids; diff -u rc=0, 0 bytes, both
```

Manifest quotes at stated lines (whitespace-normalized containment, committed capture ≡ fresh):
`S049 Q1 L211 ok, Q2 L214 ok, Q3 L410 ok, Q4 L208 ok, Q5 L419 ok, Q6 L408 ok, Q7 L132 ok,
Q8 L212 ok; S050 Q1 L70 ok, Q2 L591 ok, Q3 L595 ok, Q4 L597 ok, Q5 L112 ok, Q6 L418 ok;
quote_line_misses=0`. Provenance: `git show -s 288ea9ac --format=%aI` →
`2026-10-25T23:14:00-03:00` = both records' `fetched_utc`. Entry hand-measured strings:
22/22 line checks PASS (footer L425-426, settlement L359, intro L72 with opener len 27,
worked example L134-140, trusted-testing L408, L414, L200, credential block L202-205 present
and **not echoed**, S050 L62/L68/L71/L113/L119-124/L99/L558/L591-593/L597-598/L601/L607/L611,
peg label repeats L159/189/219/249/274/304). FC-1…FC-6 all PASS under `grep -c` line semantics
(`安全币` S049=0/S050=32 lines, `奖金` S049=12, `不予收录`=6, `授权`=2, `免责|安全港`=0/0,
`授权测试` S050=0). Credential material: counted only, never printed (bound 8/Q6).

### (b) byte-compare (staged → manifest → landed row)

```
row49 url == manifest url (byte): True | row50 == manifest: True   (36 bytes each)
staged34 == row49: True | staged35 == row50: True
registry_rows=50; L55 is S049 row: True; L56 is S050 row: True
git diff 690b69d -- corpus/SOURCES.md: appended lines=6 deleted=0 (2 rows :55/:56, 1 Search-log bullet :75, 3 R8 lines :98-:100)
tier histogram A=47 B=1 C=2; status histogram mined=38 queued=9 rejected=3
SOURCES.md sha256 b22c7f01…944d13b (base 5a03c696…f6f5)
```

### (c) refusal criteria (staged entries opened; digests verified)

```
program-scope-rules-and-asset-boundaries.md  120d8cd5 lines=39  — S031/S034/S035 cited, ground: F09,
  prose curl recheck, universal sentence present: "360SRC's published standard bounds its own scope by asset
  class (Web, server-side, mobile, PC client, smart hardware, privacy, threat intelligence) and by named
  exclusions" + "every platform's scope list is a restatement of that ownership"; Gate's new criterion
  (mixes 适用范围 with grading) supported: S050.txt:69-71 scopes by 360 group product/business
claim-packaging-and-report-quality.md  6ad64d78 lines=45 — S034/S035/S036 cited; recheck `curl … && pdftotext …`
  fails `bash -n` (rc=2 syntax error); 4 `"`-marked strings without page/line
cn-crowdsourced-testing-roles-and-conduct.md  a5302aaf — no H1 (file opens with `source:`), S081/S082
  unregistered, S082 drafting-stage per its own Limits; captures score 0 for
  您不得因为漏洞信息私自联系厂商 / 众测需求方 / 授权测试方 (0/0/0 both captures)
chinese-crowd-testing-national-standard-2026-10-23.md  6c15d941 — ground: F24, S077/S078/S079,
  quote-marked strings=0; `43741`/`国家标准` = 0 in both captures
chinese-criminal-thresholds-and-authorisation.md  1660c00c…4e8a59ae — cites "row S034" (dangling: lane S034
  is the 総務省 soumu page, a different document), S044/S045/S046 cited
chinese-program-severity-instrument.md  442e0f2b — ground: F10, colliding S034, second source S047
  sse.com.cn + "JR/T 0276—2023" present and unregistered (`grep -c` → 0 in lane registry);
  anchor newsType_6 in staged entry, `newsType_6`=0 / `newsType_21`=1 in S049 capture
program-severity-ladders-and-reward-scales.md  staged 35de5f8b/50 lines vs lane 6c05c98f/67 — overwrite hazard real
```

Quarantine slice re-derivation (my own, from the read-only register):

```
sed -n '99,100p;322,326p' absent-defect-register.md | awk -F'|' … > my-slice.txt
diff my-slice.txt .ufo/waves/round-33/assimilation/quarantine-slice ; echo "slice_diff_exit=$?"  → 0
… | awk lane column | sort | uniq -c  → 7 `kasegi`
```

S037/S054 verdicts confirmed against register rows (S037 quote = 4-field splice with inserted
`：`; S054 quote elides `（（法第 42 条第１項に規定する脆弱性をいう。以下同じ。））`) and
`wave1/ExecQuarantine.md` §4 fold table (absent F1-F4 / F1-F3; flip strings
`发布日期2020-11-19实施日期2021-06-01` F3=True; full clause contiguous). I fetched neither
quarantine URL (bounds: my item names only the S049/S050 URLs).

### (d) R20/R21 resolution

```
git show 9f98488:corpus/QUALITY.md | grep -cE '\| R2[01] \|'  → 2
round-31.md:146 → "4. **Gate caveat 1 fixes not landed** — manifest `url`/`fetched_utc` fields and a census URL↔capture comparison …"
CritC2Kill.md:232 → "2. **No URL↔capture binding anywhere** (§4). Minimal: manifest `url` + `fetched_utc` per record and …"
round-32-verifier-spotcheck.md:93 → "**D5** … are committed without a `round-32/manifest.json` … so the 38-record target is not silently moved."
round-33.md:91 (M33-1) cites R20 and R21; QUALITY R20/R21 grounded-in cells point back at it — round trip closes.
```

### Corroborating C1 run (landed bytes, quiescent)

```
python3 corpus/instruments/capture-binding-check.py
AUDIT records=40 with_url=40 with_fetched_utc=2 with_archival=38 snapshot_dirs=9 manifest_dirs=9 missing_manifest=0 multi_row_url=2
records=40 bound=40 unbound=0 ; binding_exit=0
--selftest → cases=11 failures=0, selftest_exit=0   (contract floor: ≥6 cases)
instrument sha256 b4182665…d0b7f9 / 492 lines; manifest sha256 6e4e719a…c774; watchdog digest 7bf40db6…63ed85 — all match the Gate's citations
```

## Findings

1. **Minor — Gate quote character counts misstated** (`corpus/lessons/round-33.md` § Gate,
   Admitted table). Gate says the S049 quote is "19 characters"; the quoted string
   「众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。」 is **31** characters
   (`len()` in python3). Gate says the S050 quote is "23 characters"; the quoted string
   「未纳入安全服务的资产一般情况下不收录相关漏洞」 is **22**. The quotes themselves, their
   locations (`S049.txt:214`, `S050.txt:591`) and access dates are correct, so the admits
   stand; the counts are the M33-2/M33-4 class (a number in report prose not taken from the
   bytes). Suggested fix: recompute or drop the two counts (ScribeLesson's file; I did not edit it).
2. No other disagreement. Gate caveats I confirmed as accurately stated: the C1
   metadata-not-bytes binding limit, the plain-run url-missing survivor covered by the
   selftest clause, the junk-construction-passes-counters caveat, and the two header
   placeholders being the L1's edit.

## Cleanup

Scratch `/fast/scratch/hyaku/kasegi-r33/RevGateSpot/` removed before yield (fresh fetches
byte-identical to committed captures; diffs empty; nothing needed preserving beyond this
receipt). No git/jj mutation anywhere; no writes outside this receipt.
