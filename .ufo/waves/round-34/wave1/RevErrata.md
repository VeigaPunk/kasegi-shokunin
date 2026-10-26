# RevErrata — round-34 wave-1 receipt (reviewer, leaf)

Seat: RevErrata · Round: kasegi-shokunin round 34, wave 1 (hyaku run 8, dispatched by KasegiR34) · Date: 2026-10-26
Scope: review the five appended errata (R1 correction + marker replacement; SCORECARD erratum 2 + pre-freeze satisfiability step; QUALITY R20 note; round-33 lesson R7 erratum; round-29 anchor-drift erratum), their append purity, and their factual claims. Lane base `014ee2d7aa8c3c095ff57ae51097606a9906228c`; claims freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`; working-copy parent `206e5108` (wave-1 spec).

## Report

### 0. Measurement state

- `jj log` (lane repo): `7963976e` = "round-33: remaining wave-1 receipts (final 12 seats)"; `014ee2d7` = "round-33 verifier spot-check (integrator, hyaku)" (lane base); `29f606db` = claims freeze; `206e5108` = wave-1 spec (working-copy parent).
- `git diff --stat 014ee2d7 206e5108` → 15 files, 3875 insertions(+), 0 deletions — all under `.ufo/waves/round-34/` (planner/spec files). The four errata files' blobs at `206e5108` are therefore byte-identical to the lane-base blobs; "pre-append" below = `git show 206e5108:<file>`.
- All diffs measured against `206e5108`. No git/jj mutation performed; no writes outside this receipt.

### 1. Verdict summary

| # | Item | Verdict | Key evidence |
|---|---|---|---|
| 1 | R1 correction + marker replacement | **PASS** | `grep -c '<LANE_HASH>' SCORECARD.md` → `0` (exit 1); correction paragraph `SCORECARD.md:1116-1119` names `7963976e60b2564860553c6ab4838128d5ca06ea` and `014ee2d7aa8c3c095ff57ae51097606a9906228c` |
| 2 | Erratum 2 + per-id restatement + pre-freeze step (R2) | **PASS** | `SCORECARD.md:1014` (erratum 2) and `:1028` (pre-freeze step), both inside the `## Round 33` section (`:982`–`:1096`); per-id reading matches erratum-1 ruling; QUALITY R22 row exists |
| 3 | QUALITY R20 note (R3) | **PASS** | R20 row at `corpus/QUALITY.md:169`; note at `:220-222` states the per-id reading supersedes "exactly one"; appended at file end per its own R6-form declaration |
| 4 | Round-33 lesson R7 erratum | **PASS** | `corpus/lessons/round-33.md:140`; both limbs verified against the captures (31/22 counts; `S050.txt:69` → `:70`) |
| 5 | Round-29 anchor-drift erratum | **PASS** | `corpus/lessons/round-29.md:265`; +7 drift table re-derived exactly against `0ab8929`/`690b69d`/`014ee2d` |
| 6 | All appends (no in-place edits) | **PASS** (one sanctioned exception) | numstat `14 0` / `74 0` / `109 0` on the three append-only files; `SCORECARD.md` is `31 3` and the 3 removed lines are exactly the two `<LANE_HASH>` marker-replacement sites (R1 itself) |

### 2. R1 — marker replacement + correction

```
$ grep -c '<LANE_HASH>' SCORECARD.md
0            (exit 1 — no matches)
```

Removed diff lines (`git diff 206e5108 -- SCORECARD.md | grep '^-' | grep -v '^---'`) — exactly 3, all at the two marker sites:

```
-`<LANE_HASH>`** — the L1 replaces this marker; the wave-1 value above is the commit the
-after-column seats measured, not the closing commit. Receipts land under
-**Round-33 final lane commit: `<LANE_HASH>`** — the L1 replaces this marker. Every value in
```

- `SCORECARD.md:1110` now reads: `**Round-33 final lane commit: `7963976e60b2564860553c6ab4838128d5ca06ea`** (filled in round 34, R1).` (first site, `:988` area, likewise).
- Correction paragraph `:1116-1119` (append): "Correction (round 34): the two lane-hash placeholders above (R1) were replaced with the round-33 final hash `7963976e60b2564860553c6ab4838128d5ca06ea` (lane tip `014ee2d7aa8c3c095ff57ae51097606a9906228c` after the verifier spot-check commit); the placeholder token no longer occurs in this file, and the round-34 closure check R1 reads that count as 0." — names both full hashes, as `round-33-verifier-spotcheck.md:165-166` (R1) requires ("the final lane commit is `7963976e60b2564860553c6ab4838128d5ca06ea`. Append a correction naming it.").
- The correction paraphrases "lane-hash placeholders" rather than printing the literal token — necessary so the grep count stays 0; rationale recorded in `wave1/ExecScorecardMarkers.md:71`.
- Hash identity: `7963976e` is the last round-33 content commit per `jj log`; `014ee2d7` is the spot-check commit/tip. Consistent with spotcheck R1's own statement.
- Repo-wide `<LANE_HASH>` occurrences remain only in historical round-31/32/33 wave specs/results/receipts and round-34 planner/control files (`build-spec.py`, `census-before.txt`, `c1-controls/before.txt`, `c2-controls/before.txt`, `claims.json` kill-rule text) — none in `SCORECARD.md` or any `corpus/` production file. The C1 claim scopes the count to `SCORECARD.md`; satisfied.

### 3. Erratum 2 + pre-freeze satisfiability step (R2)

- Location: `SCORECARD.md:1014` "**Erratum 2, disclosed (round-34 append, round-25 form).**" and `:1028` "**Pre-freeze satisfiability step, recorded (QUALITY R22).**" — both inside `## Round 33` (`:982`), before the next heading `## Round-33 capabilities` (`:1097`). Section placement confirmed.
- Per-id restatement (quoted from `:1014-1027`): the kill-rule parenthetical "is scoped **per id**, not globally … a URL shared by two *different* rows is informational (`multi_row_url=N`) and does not fail rule B; two rows carrying the same id **do** fail, and the instrument names that `dup-id`." This matches the erratum-1 ruling of record (`.ufo/waves/round-33/claims-erratum-1.md:31-34`: point 4 names S024/S029 and S006/S028 as informational, `multi_row_url=N`; point 3 `dup-id`).
- Factual claims re-verified:
  - Registry rows sharing URLs (python cross-check over `corpus/SOURCES.md`): `https://docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq` → rows S006, S028; `https://eur-lex.europa.eu/eli/reg/2024/2847/oj/eng` → rows S024, S029.
  - Manifest records carrying those URLs: round-23 manifest record `S029` → eur-lex…; round-24 manifest record `S006` → docs.hackerone.com… — exactly the two records the block names ("their URLs are also the S024 and S028 rows' URLs").
  - Instrument output confirms `multi_row_url=2` (see §8 for the full run).
  - Selftest pins both directions: `case_duplicate_id_rows` (`corpus/instruments/capture-binding-check.py:563`, registered `("duplicate-id-rows", …, 1)` at `:679`) and `case_shared_url_passes` (`:580`, `("shared-url-not-a-failure", …, 0)` at `:688`).
- Pre-freeze step (`:1028-1036`): records that each literal constant/regex in a predicate and kill rule is evaluated against base bytes for satisfiability before freeze, names the two round-33 unsatisfiable literals, and grounds the criterion in `corpus/QUALITY.md` R22 — which exists in the appended QUALITY block (`| R22 |` row; `grep -cE '^\| R22 \|' corpus/QUALITY.md` → 1 per `wave1/ExecQualityAppends.md:135`, row read directly).
- Spotcheck R2 (`round-33-verifier-spotcheck.md:167-169`) required exactly these two parts. Both present.

### 4. QUALITY R20 note (R3)

- R20 row at `corpus/QUALITY.md:169` (`grep -n '^| R20'` → `169:`), carrying the "exactly one `corpus/SOURCES.md` registry-row URL" reading — the frozen text R3 flags.
- Note at `:220-222` (append): "Note (round 34): R20's 'exactly one registry-row URL' reading is superseded by the C1 erratum-2 per-id reading — a URL shared by two different registry rows is informational `multi_row_url=N`, not a failure (SCORECARD round-33 section, erratum 2)." — states the per-id supersession, as claims.json C1 after-value requires.
- Placement: the note is appended at file end (`:214-227`) together with the R22/R23 rows, per the block's own declaration (`:215-216`): "R20's row (line 169) and every earlier line stay byte-identical; the R20 note and the two rows below are appended at the end of the file." It is below the R20 row in document order; the append-only form is what keeps lines 1–213 byte-identical (verified: `head -213 corpus/QUALITY.md | sha256sum` = `00781e09…` = pre blob). Spotcheck R3 asked for an "appended note" — satisfied in the lane's append-only form.

### 5. Round-33 lesson R7 erratum

Location: `corpus/lessons/round-33.md:140` `## Erratum (round 34) — R7: the S049/S050 quote counts and the S050 sentence line` (appended after the pre-append file end at `:138`; a second appended block, the R4 erratum, starts at `:215` — outside this item, noted as observed).

(a) Quote counts — erratum says 19→31 and 23→22 with producing commands; re-run:

```
$ printf '%s' '众测平台仅接收客户授权测试范围内的安全漏洞，不接受互联网漏洞。' | wc -m
31
$ printf '%s' '未纳入安全服务的资产一般情况下不收录相关漏洞' | wc -m
22
$ grep -cF '<S049 string>' corpus/source-snapshots/round-32/S049.txt   → 1
$ grep -cF '<S050 string>' corpus/source-snapshots/round-32/S050.txt   → 1
```

Line hits: `S049.txt:214`, `S050.txt:591` (the S050 hit follows the `10、` enumerator, as stated). Capture facts: S049 = 20272 B / 426 lines / `sha256 962a451a3b1cd9ff7ae128a0c2bf0d4abb859cb86bf370a1673884199d1e9cb8`; S050 = 31016 B / 630 lines / `sha256 2f9c6406ed381ee74556e9b31dd16550310de3daf45a2a6a646914fc6f378888` — match the erratum's `962a451a…1cb8` / `2f9c6406…6888`. The filed lines `:38`/`:41` still read 19/23 and are byte-identical (`head -138` digest equality, §7) — the erratum leaves the filed assertion in place and appends the correction, as it declares.

(b) Sentence line — erratum says the applicability sentence is at `S050.txt:70`, not `:69`; re-run:

```
$ sed -n '69,71p' corpus/source-snapshots/round-32/S050.txt
69: 一、适用范围
70: 本标准适用于 360 集团发布的产品和业务，此外 360 集团所投资的公司、子公司、合资公
71: 司等也在收录范围内，具体范围可参考 https://security.360.cn/Product/product。
$ grep -nF '一、适用范围' corpus/source-snapshots/round-32/S050.txt
25:…(TOC copy)   69:一、适用范围
```

Heading at L69 (plus TOC copy at L25 — the "occurs twice" claim holds), sentence begins L70, wraps into L71 with `合资公`/`司` split — all as the erratum states.

Sweep re-run (`grep -rn 'S050\.txt:69\|(L69\|适用范围 L69' --include=*.md corpus/ SCORECARD.md LOG.md SKILL.md`, exit 0): 8 matches in 4 files, every one classifiable per the erratum's own table — range citations (`corpus/SOURCES.md:56` S050 row cell and `:99` row-added change cell, both "L69-71" spans; `corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md:4`), the defect record itself (`round-33-verifier-spotcheck.md:181`), and the erratum's own table/sweep lines (`round-33.md:190,192,193,204`). **No lane production file cites `:69` for the sentence** — claim holds.

Fleet report (read-only): `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md` sha256 `0a2c6758705df4bf28b018b0a1c00974f528d7811951ec3fa3333e3c41b3e7c6` (matches the erratum's `0a2c6758…41b3e7c6`); `:61` cites 「本标准适用于 360 集团发布的产品和业务」 `(S050.txt:69)` — the slip R7 flags; the erratum is its correction of record, the fleet path being outside lane write scope.

### 6. Round-29 anchor-drift erratum

Location: `corpus/lessons/round-29.md:265` `## Erratum (round 34) — M33-3: the `SOURCES.md` line anchors cited from this lesson are stale by +7` (appended after the pre-append file end at `:263`).

- Anchor table re-derived with the erratum's own producing command (revs `0ab8929`, `690b69d`, `014ee2d`):

```
0ab8929 lines=86 3 53 60 70 76 83
690b69d lines=94 3 56 63 74 80 87
014ee2d lines=100 3 58 65 77 83 90
```

— matches the erratum's table line-for-line (86/94/100 lines; `## Registry changes` at 76/80/83; S043 change cell at 83/87/90; drift +7).
- `corpus/SOURCES.md:83` today = `## Registry changes` heading; `:90` = `Change cell old → new: the S043 anchor …` — the stale `:83` pointer now names the heading, exactly as the erratum says.
- Both stale citations confirmed in place: `corpus/lessons/round-29.md:214` ("ExecManifestC2 appended the R8 old→new change cell at `corpus/SOURCES.md:83`") and `corpus/lessons/round-29-verifier-spotcheck.md:74` ("the R8 change cell at `SOURCES.md:83`").
- "S043 row cell (line 49) still line 49" verified: `corpus/SOURCES.md:49` = `| S043 | HackerOne standard program policy set — https://hackerone.com/security/policy_versions | …`.
- `corpus/SOURCES.md` at `014ee2d`: sha256 `b22c7f0173e75e0c8c49cbf4b6e7f307fc2b1d9299ce282c1f78aadfc944d13b`, 100 lines — matches the erratum's measurement claim; the file is unmodified in the working copy.

### 7. Append purity and file digests

`git diff --numstat 206e5108 -- <files>`:

```
31	3	SCORECARD.md
14	0	corpus/QUALITY.md
74	0	corpus/lessons/round-29.md
109	0	corpus/lessons/round-33.md
```

| file | pre-append sha256 (= `206e5108` blob = base bytes) | lines | post-append sha256 (now) | lines |
|---|---|---|---|---|
| `SCORECARD.md` | `e03fbefa3eb2382a637313a98e74f4b0dd644d1fa3b351cc18a5f1038712aff3` | 1091 | `b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0` | 1119 |
| `corpus/QUALITY.md` | `00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087` | 213 | `eb20eafc6aabc312ba46fe7214860590098aef4f7664064de4a7c888653dc8cb` | 227 |
| `corpus/lessons/round-29.md` | `78ae8080fc3653b2f7291df7fd229ff4aeccc9965db2042c1825ca1f5aa52f5b` | 263 | `4afb96be18355cd958f9ddccc4f9687c2c2afa4b2747d49f687add956484ecce` | 337 |
| `corpus/lessons/round-33.md` | `ca17591d4a36e1a6623adb9acb7ac2bc0a3dbd87c24f3913229fe0b4b781feb2` | 138 | `f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807` | 247 |

- Pre-append digests match the values the errata blocks themselves declare (round-29 `78ae8080…`/263; round-33 `ca17591d…`/138) — self-consistent.
- Prefix-byte equality for the three append-only files: `head -263 round-29.md`, `head -138 round-33.md`, `head -213 QUALITY.md` each sha256 to the pre blob (outputs in §5/§4/§7 commands) — nothing above any erratum block was touched.
- `SCORECARD.md` −3 lines are exactly the two marker-replacement sites (quoted in §2); every erratum block in it (erratum 2 `:1014-1027`, pre-freeze step `:1028-1036`, correction `:1116-1119`) is a pure append. The marker replacement is the R1 fix itself, which the item and spotcheck R1 sanction; no other in-place edit exists in the errata set.
- Executor receipts cross-checked, digests identical to my independent measurements: `wave1/ExecLessonErrata.md:18-27` (round-33/round-29 pre/post), `wave1/ExecScorecardMarkers.md:21,113` (SCORECARD pre/post + grep counts), `wave1/ExecQualityAppends.md:19,95,107` (QUALITY pre/post + prefix check), `wave1/ExecErratum2.md:21,55,91` (SCORECARD/QUALITY digests).

### 8. Residual observations (not errata defects)

- Mid-wave C1 baseline: `python3 corpus/instruments/capture-binding-check.py` at review time exits **1**:
  ```
  MANIFEST round-34 records=1 url_bound=0 fetched=1 archival=0
  FAIL rule=no-row record=S051 dir=round-34
  records=41 bound=40 unbound=1
  ```
  The round-34 S051 manifest record is landed but its registry row is not yet (`corpus/SOURCES.md` unmodified in the working copy; C2 seat in flight). Erratum 2's `records=40 bound=40 unbound=0` describes the round-33 landed bytes (correct for that state); `multi_row_url=2` is confirmed in the current output. The C1 counting command will read `records=40 bound=40 unbound=0 exit=0` only once the S051 row lands — sequencing note for the L1, not a defect in the errata.
- `<LANE_HASH>` persists in historical round-31/32/33 wave specs/results/receipts and round-34 planner/control files — outside the C1 claim's `SCORECARD.md` scope and outside this item's errata scope; noted so no later reader mistakes those for live markers.

### 9. Scratch, tooling, bounds

- No scratch created: `/fast/scratch/hyaku/kasegi-r34/` contains no `RevErrata` directory (verified by `ls`); nothing to delete, no scratch-on-disk defect.
- No tools installed or upgraded; no pacman transaction; no network fetch; no git/jj mutation; no subagents; no writes outside this receipt path.
- Fleet-root read-only accesses: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kasegi.md` (sha256 + line 61 only). shokuknow untouched; no campaign tool run.

### Verdict

**All five errata items PASS.** R1: marker count 0 with the correction naming both hashes; erratum 2 + pre-freeze step present in the round-33 section with the per-id restatement matching the erratum-1 ruling and its URL-sharing facts verified; QUALITY R20 note present below the R20 row in append-only form; round-33 R7 erratum present with both limbs re-verified against the captures (31/22; `:69`→`:70`); round-29 anchor-drift erratum present with the +7 table re-derived exactly. Append purity holds: the only in-place edits in the set are the two R1 marker replacements themselves; every erratum block is a pure append with pre-append bytes proven byte-identical by digest.
