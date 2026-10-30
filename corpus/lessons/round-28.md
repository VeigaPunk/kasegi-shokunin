# Round 28 — kasegi

Lane: `kasegi-shokunin`. Three revisions matter and are named separately here, because the wave's
receipts use all three: **lane tip at round start** `261a6651b7e52c58e9ad0ceaef6f3bd0bf2d904f`
(the round-27 verifier spot-check; it is what `claims.json` names in its `base` field),
**claims-freeze commit** `c9f8b115a098c65356e4b3b6048af45a37ab8395` (contains `claims.json`,
the re-run round-27 controls and `census-before.txt`), and **dispatch commit**
`94f387cbee71a532a51ce075f01701a557231e85` (wave-1 spec + dispatch; lane HEAD while the wave ran).
`git merge-base --is-ancestor c9f8b11 HEAD` → exit 0, measured by several seats.

Shape: one v2-policy wave, `kasegi-r28-build`, **69 seats** (`wave1-dispatch.json`
`counts.spawn=69`, resume 0; `wave1.ready.dispatched` records `2026-10-25T14:22:08 spawned 69`, and
the wave's own UTC receipts begin at 17:21:57Z). Role split (LOG.md round-28 entry): executor 18,
scribe 16, reviewer 12, scout 5, critic 5, mutation-tester 5, connector 3, revenger 2, sentinel 2,
simplifier 1. The round re-declared the two claims round 27 froze and never dispatched (r27
carry-forward 1) and re-ran the committed round-27 fixtures instead of re-creating them.

> **Status: DRAFT — the L1 finalizes this file after close.** This lesson was assembled at
> 17:35Z against a wave still landing (60 of 69 seats had filed a wave-1 report, 33 a receipt; six
> had filed neither: `ScoutJpcertRecon`, `ScoutGateRegistry`, `RevDensityGuard`, `CritC2Kill`,
> `CritGlobal`, `SimplBloat`). Every
> value below carries the seat, digest and UTC stamp that produced it; nothing is projected. The
> two receipts my assignment names as the verdict source — `ExecC2Counters.txt` (17:21:57Z and
> 17:22:28Z) and `ExecFixtureRun.txt` (17:22Z) — are both **PRE-STATE**: they ran before
> `ExecImplC1` and `ScribeEntryC2` landed, so neither reaches an after value. The after values are
> recorded below from the seats that ran later at the landed digests, and the two close-out steps
> nobody has run yet (the canonical `c1-receipt-index.txt`, and a re-run at the commit that
> contains this file) are named as owed. No row here says "verified" for a check I did not see run.

## Frozen claims — before → after, with the state of every number

| Claim | Axis | Before (measured, committed) | After (measured at the landed digest) | Verdict at assembly |
|---|---|---|---|---|
| **C1** | depth:verifiability (4, lowest non-retired) | `anchorcheck.py` sha256 `c2a9e6c6…ef748`: bad-fixture **exit 0** (prints `BASE-ABSENT md:2 …`); bounties-fixture **0** `BOUNTIES-ABSENT` lines (cite invisible to `CITE`); `--selftest` absent (`FileNotFoundError: '--selftest'`, exit 1); `SKILL.md` exit 0, bad 0, LOST-RECORDED 306. Receipts `.ufo/waves/round-28/c1-controls/`, `receipts/ExecFixtureRun.txt` (PRE-STATE), `receipts/ExecInstrSelftest.txt` (PRE-STATE) | `anchorcheck.py` sha256 `95333e29…144514`, 523 lines (`receipts/ExecImplC1.txt`, 17:29:28Z): (a) bad-fixture **exit 1** with `BASE-ABSENT` still the printed class; (b) bounties-fixture **1** `BOUNTIES-ABSENT` line — `BOUNTIES-ABSENT md:3 ~/Projects/bounties/ops/claim-check.mjs:96 (base tree absent: …)`, runtime exit 1; (c) `--selftest` → `selftest cases=9 failures=0`, exit 0, 9 cases, mutants M1 (bounties arm removed) → `failures=4`, M2 (BOUNTIES-ABSENT removed from FAIL_CLASSES) → `failures=1`; (d) `SKILL.md` exit **0**, bad **0**, in-range 7, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0` — byte-equal to the before summary | **Predicate limbs (a)–(d) observed at `95333e29`; claim not closable yet.** `c1-receipt-index.txt` does not exist (verified absent 17:30:49Z), so frozen counter (c)'s index greps cannot run. Canonical index owed by the L1 |
| **C2** | coverage (7) | frontier admitted **11**; entries citing S042 **0**; registry **41** rows, census exit 0 (W04 ×2: S028/S029); harness `entries=14 pass=14 exit=0` (`.ufo/waves/round-28/census-before.txt`, `c2-controls/before.txt`) | frontier admitted **12** (`README.md:213`); entries citing S042 **1**; registry **42** rows with exactly one `S042` row, census **exit 0**, W04 ×2 only; harness `entries=15 pass=15 exit=0` (PASS line `F12 knowledge/japanese-domestic-disclosure-workflow.md ids=S041,S042`); manifest `e62ddad1…` pins both captures with 12 quote assertions, all `occurrences=1`, `source-recheck` exit 0 per id | **After values reached and measured** (`RevCounters2.md` 17:26:24Z; `receipts/ExecReceiptCanonC2.txt` 17:27:13Z POST-STATE; `receipts/RevCensusEnd.md`; my own census re-run at 17:30Z below). Still owed at close: the single canonical receipt and the L1's re-run |
| depth:density | 9 | `density.py SKILL.md` = mean **150.3**, **20** blocks, **652** path citations at the round base | same instrument after the SKILL.md append: the append adds citation-bearing text, so the block mean/instances must be re-measured at close; `anchorcheck.py SKILL.md` class counts did not move (row above) | **No-harm on verdict classes holds; density re-measure owed.** The comparand 154.0 / 19 blocks shipped in the dispatch was stale (M28-9) |

**Both states of the frozen counters, timestamped.** The counters themselves (`claims.json`
`counter_commands`) were executed at least three times by different seats. Only the runs at a
digest that stayed fixed count:

| UTC | seat | instrument digest | result |
|---|---|---|---|
| 17:21:57Z / 17:22:28Z | ExecC2Counters | n/a (C2) | 11 / 0 / 0 / exit 0 (41 rows) / 14-14 — PRE-STATE |
| 17:22Z | ExecFixtureRun, ExecInstrSelftest, ExecNoHarmC1, ScribeScorecard, RevCounters1 | `c2a9e6c6…` | every before value reproduced; no after value — PRE-STATE |
| 17:28:21Z | ExecGateLog §C | `c3629229…` | (a) 1, (b) 1, (c) `cases=9 failures=0` exit 0, (d) 0/0/306 |
| 17:29:16Z | ScribeSkillGate §8 | `95333e29…` | all four reproduced |
| 17:29:28Z | ExecImplC1 | `95333e29…` | all four + M1/M2 mutants + 44-file corpus sweep |
| 17:31:21Z | RevFixturesC1 | `95333e29…` | selftest run twice, identical, `cases=9 failures=0`, temp sandbox removed |

**Claims correction (appended, never in-place — R25-1/R9).** `.ufo/waves/round-28/claims-erratum-1.md`
supersedes the frozen C1 `corpus_disclosure` cell. The frozen text said the four marked
`[lost-tree]` `~/Projects/bounties/…` citations in `claim-gates.md`, `intake-and-finalize.md`,
`mission-control.md`, `source-tree-loss-2026-09-28.md` would "newly classify `LOST-RECORDED`".
They are plain-text `source:` trails with zero backticks, `TOK` extracts only backticked spans, and
the lane contains **0** backticked anchored `~/Projects/bounties/<path>:<NN>` tokens
(`ExecInstrReadme`, `ExecReceiptCanonC1` §F-B, `ExecImplC1`, `ScribeSkillGate` — four independent
measurements). Measured reclassification: **0 of 4** (`claim-gates` 0→0, `intake-and-finalize`
0→0, `mission-control` 0→0, `source-tree-loss…` 15→15). The correction is strictly stronger than
the frozen cell: the arm is invisible to every existing byte, so no verdict class moves anywhere —
`SKILL.md` included.

One intended consequence is disclosed rather than hidden: at the landed digest the fail-closed
exit moves five corpus files' **exit codes** 0 → 1 while their verdict classes stay put —
`corpus/QUALITY.md`, `corpus/knowledge/citation-bases.md`,
`cra-manufacturer-reporting-duties.md`, `iso-29147-divergence-and-clause-crosswalk.md`,
`root-loss-2026-10-12.md` (all BASE-ABSENT-driven; `ExecImplC1` O3). That is predicate (a) doing
its job on citations whose base has been absent since 2026-09-28/2026-10-12, not a regression.

## Gate — the assimilation set

*Drafted by `ScribeLessonGate` (`.ufo/waves/round-28/wave1/ScribeLessonGate.md`), pasted here and
reconciled against the landed tree at 17:30Z. Its assembly note is dropped; its drafting-time
qualifiers are kept only where the landed state still answers them, and the reconciliation line
below says what changed in between.*

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi` (read-only in this round; no campaign tool
was run there, nothing written into it). Round shape: ONE theme — the Japanese state-coordinated
disclosure workflow — with one entry re-grounded on two fresh captures (the IPA intake-process page
as the new row S042, the JPCERT/CC 2026 P-guideline re-captured under the existing row S041), plus
the quarantine slice and two standing reject candidates.

Package bytes read this round (all under that path): `MERGE-REPORT.md`; `SOURCES.append.md` rows
S042, S043, S044, S045, S046, S068, S080; the staged entries
`knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`,
`…/chinese-criminal-thresholds-and-authorisation.md`,
`…/vendor-third-party-finding-coordination-2026-10-23.md`. Register read (read-only):
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.

### Collision / adoption ids

Id-collision check ran in scratch (`.ufo/waves/round-28/assimilation/collision-check.txt`, taken
before the S042 append): registry `reg=41`, staged `staged=94`, collisions **11** (S031–S041). The
adopted id therefore continues the lane registry from **S042**. The guard was proved discriminating
against a 0-3-leading-space fixture (`assimilation/guard-proof.txt`): the tolerant pattern reports
the indented duplicate, `^\|` alone misses it. Lane result: no colliding row can be appended
silently.

The two staged rows this round touches are resolved **by document, never by arithmetic**:

| Staged id | Staged URL | Resolves to | Verdict |
|---|---|---|---|
| S042 | `https://www.ipa.go.jp/security/todokede/vuln/process.html` | lane **S042** (free at adoption: `grep -cE '^ {0,3}\| *S042 *\|' corpus/SOURCES.md` → 0 before the append; no lane row carried that URL: `grep -cF …todokede/vuln/process.html corpus/SOURCES.md` → 0) | **new row admitted** |
| S043 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | lane **S041** (registered round 26; `grep -cF` of the URL → 1, at `corpus/SOURCES.md:47`) | **cited, not re-registered** |

S043 is not an adoption candidate because the document is already registered: URL equality with
lane S041 (`assimilation/by-document-map.txt` §7 prints both URLs and they are the same string) and
S041's row is `mined`/tier A. Adopting it again would duplicate a document the registry already holds.

### Admitted

| Row | Admitted as | Document / capture | Opened | Evidence | Entry |
|---|---|---|---|---|---|
| S042 | tier **A**, status `mined` | IPA 脆弱性関連情報の届出受付業務における取扱いプロセス — `https://www.ipa.go.jp/security/todokede/vuln/process.html` | **2026-10-25** | `corpus/source-snapshots/round-28/S042.txt` (html capture via `capture-source.py --kind html`, status 200, fetched 229,982 B → 60,508 B, 974 lines, sha256 `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`, utc `2026-10-25T17:22:03Z`); `manifest.json` binds **6** quote assertions, every one `occurrences=1` | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (`used-by` names exactly this entry) |
| S041 | existing row, tier A / `mined`, **not re-registered** | JPCERT/CC 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 — `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | 2026-10-25 (unchanged) | **round-28 re-capture** `corpus/source-snapshots/round-28/S041.txt`: status 200, fetched 1,338,665 B → 147,267 B, 2354 lines, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`, utc `2026-10-25T17:22:12Z`; `cmp` against the round-26 capture → **IDENTICAL** (`cmp_exit=0`), so F11's round-26 line anchors still hold | the same F12 entry (`used-by` gained it, §Registry changes) |

**The new row, in the Gate's own words (round-26 routed defect 3 — quote inline, not by pointer).**

- S042 URL: `https://www.ipa.go.jp/security/todokede/vuln/process.html`; access date **2026-10-25**;
  located quote, `S042.txt:145`, `occurrences=1`, pinned by manifest assertion `S042:Q1`:
  「JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。」
  (63 chars, 2 whitespace-words — under the 25-word cap; the step-5 sentence `ScoutIpaRecon`
  located, pinned as manifest `S042:Q1`). The heading it answers to is `5.起算日の連絡`
  (`S042.txt:144`); the heading alone is **not** admissible as evidence (8 chars <
  `source-recheck.py` `MIN_QUOTE_CHARS=12`, measured `UNAVAILABLE reason=quote-too-short-to-be-evidence`
  on the manifest's first build — see §Defects caught).

**The admitted entry** (`corpus/knowledge/japanese-domestic-disclosure-workflow.md`, 103 lines,
18,544 B, sha256 `a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6`, created this
round):

| Property | Landed value |
|---|---|
| header | `source: S041` and `source: S042` (two lines, both capture-anchored), `verified-at: 2026-10-25`, `ground: F12` |
| recheck | one executable line, cwd-independent: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && … --source S042` |
| measured, foreign cwd (`/tmp`) | `bash -n` exit **0**; run exit **0**; both ids re-verified from the committed pins (`ExecHarnessC2` §C1) |
| `--source` id set = declared `source:` id set | S041, S042 — equal; the two invocations are chained because `source-recheck.py:275` accepts one `--source` per invocation (the entry discloses this in §Limits) |
| frontier binding | `frontier-recheck-count.py` → `PASS F12 knowledge/japanese-domestic-disclosure-workflow.md ids=S041,S042 exit=0`, `entries=15 pass=15 exit=0` |
| Q9 binding (`ExecHarnessC2` §A3) | `PASS S041 … assertions=7`, `PASS S042 … assertions=7`, `q9 ids=2 failures=0`; 12 quotes, every one exactly-once raw and normalized |
| corpus census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → **exit 0**, rows 42, only the pre-existing W04 S028/S029 |

**What the entry had to be re-grounded away from (staged → lane).** The staged package entry is
not adopted as written. Three measured deviations, recorded in the entry's §Limits and in
`ScribeRegistryC2`'s receipt:

1. **"six-step" web-application path is false on both captures.** Staged bytes
   (`japanese-domestic-disclosure-workflow.md:45-46`): "The IPA process page carries a second
   six-step flow for web applications". The capture numbers **seven** (`S042.txt:162-182`, step
   `7.` is the statistics step at `S042.txt:181-182`), and the guideline's 図４ agrees
   (`S041.txt:1331`). The landed entry states seven and cites the lines.
2. **The staged S043 id is not carried.** The entry cites the guideline under lane **S041** and
   says so in §Limits; no lane row was created for the document.
3. **The staged `opened` date moved 2026-10-23 → 2026-10-25** (today's access date), and the staged
   `anchor` cell's "ウェブアプリケーション … steps 1 to 6" was dropped from the registry row in
   favour of capture line numbers for the product flow and step 5.

### Refused (rejects carry flip conditions)

| Candidate (package path) | Failing gate | Reason (measured evidence) | Flip condition |
|---|---|---|---|
| `knowledge/corpus/knowledge/chinese-criminal-thresholds-and-authorisation.md` — standing refusal, **re-confirmed** | Q2, Q3, Q4, Q5, Q7/Q10; `ground` | (1) **Q2** — it rests on staged S044/S045/S046, none of which is a lane registry row (lane registry = S001–S042, 42 rows; `grep -cE '^ {0,3}\| *S04[3-9] *\|' corpus/SOURCES.md` → **0**), so "opened in the admitting round" cannot be satisfied. (2) **Q4** — it generalises three instruments into one jurisdiction-wide rule while its own §The claim describes 285(1) as covering state-affairs/defence/cutting-edge systems with no quantitative element. (3) **Q3** — the load-bearing sentence is a paraphrase with no located quote. (4) **Q7/Q10** — its `recheck:` is the package's prose form. | Register S044/S045/S046 as lane rows with today's access date; restate 285(1) as a conduct offence; quote the threshold items in full including 其他情节严重的情形; make the recheck a single executable command. |
| `knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` — **new refusal** | `ground` (no lane row), Q2, Q3, Q7/Q10 | (1) **The named gate** — `ground: F20` names no lane frontier row: `grep -cE '\| F20 ' corpus/README.md` → **0** (the frontier stops at F12). (2) **Q2** — its sole source is staged S080 (`SOURCES.append.md:21`, MSRC MSVR), not a lane registry row. (3) **Q3** — it restates the three routes from the fragment "MSVR learns about vulnerabilities in third-party products in three ways" with no located line, page or capture. (4) **Q7/Q10** — `recheck:` is "180d — `curl -sSL …` and confirm …", a prose hybrid. | Register the MSRC page as a lane row, capture it, locate a quote with `occurrences=1`, add a named lane frontier entry (or none), and make the recheck one command. |

No Q/R bar was relaxed for either reject. Neither staged entry file exists in the lane
(`test -e corpus/knowledge/…` → no for both), so nothing refused is half-landed.

**The refusals rest on these quoted bytes, inline (round-26 routed defect 3 — quote, not pointer):**

- `chinese-criminal-thresholds-and-authorisation.md:47-48` — "the Chinese criminal risk attaches to
  **scale and effect**, not to the mere act of unauthorised access." (18 words) — the jurisdiction-wide
  generalization Q4 refuses; its `ground: F12` (`:9`) is the package's F-space, whose lane counterpart
  is a different topic.
- `vendor-third-party-finding-coordination-2026-10-23.md:7` — "ground: F20" — a frontier id absent
  from the lane (`grep -cE '\| F20 ' corpus/README.md` → 0); and `:16` — "MSVR learns about
  vulnerabilities in third-party products in three ways:" (11 words) — the claim restated with no
  located quote in any captured source.

### Quarantine slice — seven rows hand-checked (2026-10-25, instrument UA)

Slice derived from the register itself (its header and `## By lane` totals are stale, as the round
prompt warns): `awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'`
→ 7 rows. **None adopted.** The gate seat ran the fetch/quote-locate itself because the assigned
scout receipt was not on disk at composition time; command and full output:
`.ufo/waves/round-28/wave1/ScribeLessonGate/quarantine-handcheck.sh|.out` (utc
`2026-10-25T17:24:29Z`). Normalization: tags stripped, whitespace collapsed (Q8).

| Staged row | Register class (verbatim) | Measured verdict (2026-10-25) | Meaning for adoption |
|---|---|---|---|
| S037 | `payload-absent` | **`fetched no-quote`** — 200 / 24,189 B; the staged anchor is a composite of separate table cells: the whole anchor string occurs **0×**, while `发布日期` occurs 1× and `GB/T 30279-2020` 2× | reachable + authentic metadata; quote-form defect — not appendable as staged (cell-anchored fragments would be needed) |
| S054 | `payload-absent` | **`fetched no-quote`** — 200 / 513,648 B; the PDF's own header is glyph-spaced (`府 サ 連 第 ７ 号`, `令和８年９月 17 日`), so the staged `府連第7号` occurs **0×** under whitespace collapse | source real, quote is a re-construction: not appendable as staged (a longer fragment or a spacing-normalized capture is needed) |
| S048 | the cited source could not be fetched, so no quote was checked | **`unfetchable`** — `gbDetailed?id=3B865A…` returns **404 / 748 B**; anchor `项目周期` 0× | dead as cited; refuse until an R8 `supersedes` row names a live id |
| S065 | the cited source could not be fetched, so no quote was checked | **`fetched quote-located`** — 200 / 7,465,472 B; `现行有效法律目录` 1×, `刑法（7 件）` 1× | reachable + quote located; **not adopted** — no admitted entry cites it, and registering it would be an unmotivated row |
| S068 | the cited source could not be fetched, so no quote was checked | **`already-mined-legacy`** — 200 / 94,027 B; `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018` 1× | the same document is lane **S040** (round 25; URL byte-equal to `SOURCES.md:46`) |
| S069 | the cited source could not be fetched, so no quote was checked | **`unfetchable`** — `gbPlan/download?path=…` → **302**, 0 B, redirect target fails TLS (`curl: (60)`) | unverifiable from these endpoints |
| S070 | the cited source could not be fetched, so no quote was checked | **`unfetchable`** — same 302/0 B + TLS failure | unverifiable from these endpoints |

The register's two unchecked families remain exactly that: a fetch today does not certify a quote,
and for S037/S054 the staged anchor fragment is not verbatim anywhere in the fetched bytes.
Reachability is reported, not upgraded into adoption.

### Registry changes — every change old → new, inline

- **S042 appended** (`corpus/SOURCES.md:48`): tier A, `mined`, `opened 2026-10-25`, `recheck 180d`,
  `used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md`. Against the staged row
  (`SOURCES.append.md:18`): `opened 2026-10-23 → 2026-10-25`; the anchor's "ウェブアプリケーション
  … steps 1 to 6" **dropped** (capture shows seven) → "ソフトウエア製品の取扱いプロセス steps 1
  to 10 (L132-L160), step 5 起算日の連絡 (L144-L145)" re-read from the capture; `teaches` rewritten
  to one grounded benefit; `status mined` and `recheck 180d` unchanged.
- **S041 `used-by` old → new** (R8, logged in `## Registry changes` and in `ScribeRegistryC2`'s
  receipt; recorded here because R8 requires the lesson to carry it):
  `iso-29147-and-30111-division-of-labour.md, iso-29147-divergence-and-clause-crosswalk.md`
  → `iso-29147-and-30111-division-of-labour.md, iso-29147-divergence-and-clause-crosswalk.md, japanese-domestic-disclosure-workflow.md`
  (paths under `corpus/knowledge/`). Cell-split diff: 13 cells both sides, only the `used-by` cell
  differs; `status mined`, `opened 2026-10-25`, `recheck 180d` unchanged.
- No status or recheck cell changed on any row this round; no row was superseded, retired or
  re-titled. The S042 row was placed as the last row of `## Registry` (a row after `## Paths` is
  census `E12`; measured on scratch in `ExecCensusDry` §4).

### considerthese item landed

`considerthese/2026-10-25.md` proposal 1 (wave-evidence economy) landed as `corpus/QUALITY.md`
**R14** (77 → 83 lines, `6 insertions(+), 0 deletions`; `before_sha256 319dc9eb…` →
`after_sha256 00d4b2a3…`, and `head -77` is byte-identical to the old file, so every existing
line keeps its number — `ScribeR14.txt`). Practised in-round: the captures are text snapshots with
sha256 pins, scratch trees live under `/tmp` or `wave1/<Seat>/`, and the largest committed control
tree is `.ufo/waves/round-28/c1-controls/` at **44 KiB** — below R14's "few hundred kilobytes"
threshold, so no tarball is required and none is claimed. Round-25's ~65 MB / ~3.77k files is the
comparand (`98261eb` +850,085 lines).

### Defects caught mid-wave (recorded because each was measured before landing)

1. **Manifest Q1 was a heading, not evidence.** First build (`fa1f366f…`) exited **2** with
   `S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`: the step-5 heading normalizes to
   8 chars, under `MIN_QUOTE_CHARS=12`. Fixed by replacing Q1 with the L145 body sentence; the
   landed manifest (`e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d`, 5038 B)
   exits 0 on both ids, all assertions `occurrences=1`. `ExecManifest` and `ExecHarnessC2` measured
   the same failure independently in the same window.
2. **`source-recheck.py` exits 0 for three of the C2 kill rule's own failure states.**
   `ExecHarnessC2` §D: stem≠id, an unanchored exactly-twice quote, and a broken anchor all exit
   **0**; only `quote-too-short` and `outside-manifest-directory` exit 2. The Q9 clause therefore
   cannot be read off `source-recheck`'s exit code or a harness `PASS` row — `check_q9.py` is the
   reader, and it fails each of the three states (controls A–D), so it is not always-PASS.
3. **A frontier row admitted before its entry existed crashes the harness.** With F12 `admitted`
   and the entry file absent, `frontier-recheck-count.py` raised an uncaught `FileNotFoundError`
   at `entry_contract()` (exit 1, no `entries=`/`pass=` line, no named problem). Not a false pass,
   but a mid-wave run of that harness is not a count. Landed state is clean
   (`entries=15 pass=15 exit=0`), so this is ordering evidence, not an open defect (M28-5).
4. **`source-recheck --source` is single-valued** (`:275`): a literal
   `--source S041 --source S042` re-derives only the last id. Measured by this seat on the landed
   manifest: that invocation printed **6** quote lines, not 12. The entry chains two invocations
   instead and says so in §Limits (M28-11).

### Spot-check result (LEARNING.md §Discernment)

- **Admit — agree.** `RevEntryC2` (non-author reviewer) bar-checked the landed entry against
  Q1–Q10 and records PASS on all ten, including the three assigned end-to-end checks (captures at
  cited anchors, recheck from a foreign cwd, source-id equality). `RevManifestC2` independently
  re-ran the Q9 table (12 quotes: `grep -c`/`grep -o`/normalized all 1, no anchor required) and
  `SentinelQuality` re-opened three randomly chosen load-bearing claims plus every numeric count —
  all verbatim. Three non-author seats agree with the admit.
- **Reject — agreement exists, the outside spot-check row is owed.** `ScoutAssimilation` reached
  the Chinese-thresholds refusal independently of `ScribeLessonGate` (§7 of its receipt), which is
  cross-seat agreement, not the fresh non-author spot-check LEARNING.md asks for. No reviewer seat
  filed a verdict on the two refusals at assembly time. **Named omission, not claimed:** the L1
  should have a non-author re-open one refused candidate's cited source and record agree/disagree
  here before this lesson is finalized.

## Mistakes

**M28-1 · counters ran before the thing they count existed (timing hazard, systemic).** Class:
wave-sequencing. Evidence: six seats produced PRE-STATE receipts for work that later landed —
`ExecC2Counters` (17:21:57Z / 17:22:28Z), `ExecFixtureRun` (17:22Z), `ExecInstrSelftest` (17:22:49Z),
`ExecNoHarmC1` (17:23Z), `RevCounters1` (17:22:55Z / 17:24:12Z), `ExecReceiptCanonC1` (17:25Z), and
`ScribeScorecard` whose C1 cells are `pending` for the same reason. Each labelled itself PRE-STATE
— the labelling worked — but seven receipts exist that cannot verify anything, and the round's
verdict had to be reconstructed from later seats. Captured-by: the seats themselves (their own state
labels), assembled here. Fix: a v2 wave dispatches counters in a second tranche after the owning
edit lands, or the spec gives each counter seat the landed digest to wait for. Until then, the rule
that worked is the one to keep: **label PRE-STATE, name the exact re-run, never compare a PRE-STATE
number to an after column.**

**M28-2 · a frozen disclosure asserted a reclassification without checking the token form.** Class:
stale premise. Evidence: the frozen C1 `corpus_disclosure` cell named four citations that would
"newly classify `LOST-RECORDED`"; all four are unbackticked `source:` trails (`claim-gates.md:123`,
`intake-and-finalize.md:109`, `mission-control.md:169`, `source-tree-loss-2026-09-28.md:353`), `TOK`
is backtick-only, and a lane-wide scan finds **0** backticked anchored bounties tokens. Measured
movement: 0 of 4. `ScribeScorecard`'s receipt had already written the expected post-change reading
"1 / 1 / 1 / 16" from the frozen cell before the erratum landed — a number nobody measured and
nobody can. Captured-by: `ExecInstrReadme` (first independent measurement, before the L1's
correction), then `ExecReceiptCanonC1` §F-B, `ExecImplC1`, `ScribeSkillGate`. Fix: appended
`.ufo/waves/round-28/claims-erratum-1.md` (R25-1 — never an in-place edit), and `ScribeSkillGate`'s
SKILL.md note records the erratum rather than the frozen cell. House rule forward: **a frozen
disclosure that names a class movement must name the lexical form the matcher reads**, and the
fixture that demonstrates it runs before the claims file freezes (the M27-1 rule, extended from
fixtures to disclosure prose).

**M28-3 · a frozen counter command that cannot produce its own output.** Class: unsatisfiable
instrument. Evidence: `claims.json` C1 counter-command 4's `bad=` limb,
`sed -n 's/^== .*bad; \([0-9]*\) bad.*/bad=\1/p'`, requires a second `bad` after `bad; `; the
summary grammar is `… , 0 bad; 7 distinct anchors; …`, so it prints **nothing** on the pre-change
bytes and nothing on the landed bytes. Measured three times independently: `ExecReceiptCanonC1` §F-A,
`ExecSkillGateSupport` §4, `ExecImplC1` O1. The `lost=` limb in the same command is correct
(`lost=306`). Captured-by: those three seats. Fix: the working extraction is
`sed -n 's/^== .* \([0-9]*\) bad;.*/bad=\1/p'` → `bad=0` (measured); it belongs in an appended
claims correction, not in a silent re-interpretation. The claim's after value (`bad=0`) is reachable
and was reached — through the corrected form.

**M28-4 · the instrument was non-stationary for six minutes, and receipts pinned intermediate
digests.** Class: measurement race. Evidence: `ExecGateLog` §B keeps the ledger —
`c2a9e6c6…` (freeze) → `0a24a173…` → `7adfc847…` → `982d7207…` → `3122643c…` → `21b59612…` →
`e14f75b8…` → `29aba084…` → `c3629229…` → landed `95333e29…`; `ScribeScorecard` observed its own
list (`… 5f5f725c…`), and this lesson observed `ad262eaa…`, `2f707046…`, `cab98bcc…`, `c3629229…`
between 17:25:55Z and 17:27:48Z. Intermediate states failed in instructive ways:
`NameError: name '_selftest' is not defined` (17:27:1x), and a bounties cite matched but resolved
under a mirror-prefix join as `BASE-ABSENT`. Consequence: `ExecRecheckAuditR28` pins `2f707046…`
in its identity block while its prose still says the file is `c2a9e6c6…`; `ExecInstrSelftest`'s
determinism result is measured on pre-change bytes and says so. Captured-by: `ExecGateLog`
(ledger), `ScribeScorecard`, `ScribeSkillGate`, `ExecSkillGateSupport`, and this lesson. Fix:
measure only at a digest that stays fixed across the whole block (the seats that closed did exactly
that at `95333e29…`); a receipt that pins an intermediate digest is stale by one edit and must say
so rather than be reconciled by prose.

**M28-5 · rows and entries landed in the wrong order, and two gates went transiently red.** Class:
landing order. Evidence: `ScribeLog`'s mid-wave measurement at `2026-10-25T17:23:53Z` — frontier
`admitted` 11 → 12 with the entry absent → `frontier-recheck-count.py` raised
`FileNotFoundError: …/corpus/knowledge/japanese-domestic-disclosure-workflow.md` (exit 1, no
`entries=` line) and `sources-census.sh validate` exited **1** with `E11` on **both** S041 and S042
for the same missing `used-by` path. Reproduced independently by `ExecHarnessC2` §B2/E1,
`ExecCensusDry` §B1, `RevRegistryC2` (open item), `RevCounters2` (three-snapshot timeline). Cleared
at 17:26Z when the entry landed. Captured-by: five seats. Fix: land the entry in the same commit as
(or before) the registry row and the frontier row — `ExecCensusDry` proved the identical registry
bytes validate exit 0 once the `used-by` file exists (§B2). Routed debt: `frontier-recheck-count.py`
should fail a named row instead of raising, so a half-landed tree reads as `pass=14 of 15` rather
than a traceback.

**M28-6 · R6's letter and the registry-table instruction cannot both be satisfied.**
Class: criterion/instruction conflict. Evidence: the dispatch said "append ONE row to the existing
gate|probe registry table … Append at the END of the table only (R6)" while R6 says an edit to a
line-cited file "keeps every existing line at its number (append at the end, or a same-line
suffix)". A table row at the end of a mid-file table necessarily shifts what follows:
`SKILL.md` 1032 → 1035 lines, 51 lines moved by +1, and `ExecSkillGateSupport` §2 names the
off-by-one referents — `corpus/instruments/resolve-dispatch-fixtures.json:159,161` pin
`SKILL.md:1000` (119 further `.ufo` copies cite `:1000`), plus frozen prior-round evidence at
`:993`, `:1014`, `:1019`, `:1021`. `ScribeSkillGate` disclosed the shift and argued "R6 satisfied
in substance, not in the letter"; `SentinelScope` §6 independently flagged it as "a strict R6
reading flags the line-number displacement"; `ExecSkillGateSupport` measured that the anchor
report itself changes only in one in-file `md:998 → md:999` position. Captured-by:
`ExecSkillGateSupport` and `SentinelScope` (both non-authors of the file). Fix: decide the rule
rather than the instance — either R6 gains an explicit carve-out ("a row appended to a table that
no cited line follows is a suffix, provided every shifted citation is re-anchored in the same
commit"), or gate rows move to an end-of-file table. This round did neither; the shift landed and
is disclosed. A pre-existing, separate drift (r26 inserted 9 lines at 976; the four-alternative set
is at 1007 before this edit, 1008 after, while the fixture still says 1000) is not this round's.

**M28-7 · the staged package's row/entry text was wrong in ways only the capture could show.**
Class: staged-source defect, caught by re-grounding. Evidence, each measured: staged S042 anchor
claimed the web flow has "steps 1 to 6" — the capture numbers **seven** (`S042.txt:162-182`;
`ExecCaptureS042` §5b, `ScoutIpaRecon` §4); the staged entry says "second six-step flow" and
"ending in 取扱い開始連絡 and 修正完了の連絡" — also wrong on the ending (`S042.txt:182`, the
statistics step, is last); staged `opened` was the package date 2026-10-23; staged `teaches` was a
three-clause prose sentence; staged `ground:` was `F13` while the lane row is F12; staged S043 is
the already-registered lane S041; and `MERGE-REPORT.md:9` claims "lane registry currently holds
**30** rows; first staged id is **S031**" while the lane held **41**, so staged S031–S041 all
collide by id and **0** of the 11 colliding URLs match (`ScribeSourcesGate` F-2). The package's
own F-space is different again (package F12 = Chinese statutory family). Captured-by:
`ExecCaptureS042`, `ScoutIpaRecon`, `ScribeSourcesGate`, `ScoutAssimilation`, `ScribeRegistryC2`,
`RevEntryC2`. Fix: rewrite by document, never append the package as its checklist instructs — the
landed row and entry carry capture line numbers, the lane ids, and today's access date. This is
the third round where the package's convenience framing would have written wrong rows.

**M28-8 · Q9 has a conjunct with no instrument behind it.** Class: criterion/implementation gap.
Evidence: `source-recheck.py` validates a record's relative `path`, its sha256 and its quote
assertions but never compares the path stem to the record `id`; the frontier harness's `PASS` row
does not test it either. `ExecReceiptCanonC2` F-3 measured the gap (and supplied
`manifest_path_stem_ok=True` from an independent `os.path.splitext` check), `ExecHarnessC2` §D
proved `source-recheck` exits 0 on a stem-mismatched record, and `RevManifestC2` re-derived the
stem check mechanically. Captured-by: those three seats. Fix: the canonical C2 receipt carries the
measured stem check, and Q9's executable limb is a named debt (candidate `check_q9.py` promotion).
Not repaired this round — the instrument belongs to a different owner than the claim's implementer.

**M28-9 · a stale comparand in the dispatch would have reported a false regression.** Class:
stale premise. Evidence: the dispatch's no-harm comparand was 154.0 mean / 19 blocks / 652 cites;
`ExecNoHarmC1` §2 measured the same instrument on the round base's `SKILL.md` at **150.3 / 20 /
652** and traced the delta to round 26's `## Gates & probes registry` block (9 lines, dens 80.0,
0 path cites) entering the unweighted mean. Using the shipped comparand unchanged would have
reported a −3.7 mean regression that does not exist. Captured-by: `ExecNoHarmC1` (and
`ScribeScorecard` §4, which re-derived it). Fix: re-base every same-byte guard at the round base
before dispatch, and attribute mean movement to block count when a block is added.

**M28-10 · a seat labelled the round-27 spot-check commit as the claims freeze.** Class:
bookkeeping. Evidence: `ScribeFrontierNote` §A reads "Base (claims freeze): `261a6651…`", while
`claims.json`'s `base` field is `261a6651…` and the actual freeze commit — the one containing
`claims.json` — is `c9f8b11`. Both hashes are legitimate; the label conflates "revision the claims
were written against" with "commit that froze them". Captured-by: this lesson (cross-checked against
`git log` and `claims.json`). Fix: name all three revisions explicitly at the top of a round's
lesson and in `LOG.md` (this lesson does), and treat `claims.json.base` as "lane tip at round
start", never as "the freeze commit".

**M28-11 · a single-valued CLI flag was cited as covering two ids.** Class: instrument
mis-citation. Evidence: `source-recheck.py:275` is `add_argument("--source", …)` with no
`action="append"`, so `--source S041 --source S042` checks only S042; run on the landed manifest it
printed **6** `OK occurrences` lines, not 12 (this seat, 17:31Z). The entry's §Limits says so
correctly; `SCORECARD.md`'s round-28 C2 cell cites the two-flag form as "6 quotes per source".
Captured-by: `ScribeEntryC2` (entry §Limits) and this seat's run. Fix: cite two chained invocations
(the entry's own `recheck:` line) or a single `--source` per invocation; the SCORECARD cell's
wording is its owner's to correct at close.

**M28-12 · receipt digests and labels drifted behind the bytes they describe.** Class:
bookkeeping. Evidence: `ScribeReadmeC2`'s receipt records `after sha256 e38ba567…`, 243 lines, but
the landed `corpus/README.md` at 17:30:49Z is `5f458a7a…`, **245** lines — it received a second edit
after its receipt (the F12 `next` cell was rewritten; `ScribeFrontierNote` had already observed "two
F12 `next` texts"). `ExecGateLog` §A records `95333e29…` as the digest read while §B calls
`c3629229…` "LANDED" and §C's runs were executed at `c3629229…`. A third instance: `ExecInstrReadme`
issued two receipt revisions for the same file — 289 lines / 93 insertions, then 327 lines /
131 insertions (`cf35a643…`) — so for a window a reader citing the first revision would have pinned a
stale size and digest. Captured-by: this lesson's cross-checks at 17:30:49Z, 17:34:31Z and 17:35:26Z.
Fix: the L1 re-hashes every landed production file immediately before the
commit and records the digests in `LOG.md`; a receipt's `after_sha256` is evidence about a moment,
not about the tree.


**M28-13 · selftest inherited the caller's Git repository selection.** Class: survivor. Evidence:
`CritC1Kill.md` and the L1 reproduction: with `GIT_DIR=<temp-repo>/.git`,
`anchorcheck.py --selftest` printed `selftest FAIL pin-broken: PIN-BROKEN: want 1, got 0;
IN-RANGE: want 0, got 1; exit: want 1, got 0`, then `selftest cases=9 failures=1`, exit 1.
The pin fixture created a fresh repository but inherited Git's environment overrides, so
`git show deadbeef:pinned.md` could read a caller-supplied blob and bypass PIN-BROKEN.
Captured-by: the C1 selftest's isolating-fixture criterion (round-28 claims.json C1 kill rule);
the test did not vary Git environment despite claiming fresh temp isolation.
Fix (shown able to fail): selftest child environments now remove inherited `GIT_*` variables
before setting the isolated KASEGI roots. The same perturbation now prints
`selftest cases=9 failures=0`, exit 0; code is at `anchorcheck.py:311-317`, correction at
`.ufo/waves/round-28/claims-erratum-1.md` §Erratum 2.

**M28-14 · a second stale premise lived in the claim's disclosure, not its fixture.** Class:
stale-premise. Evidence: `.ufo/waves/round-28/claims-erratum-1.md` — the frozen disclosure
predicted four corpus cites would newly become LOST-RECORDED, but the four are plain-text
`source:` trailers and `TOK` only extracts backticks; observed movement was 0/4.
Captured-by: none before freeze (r27 M27-1 only required executing fixtures; it did not require
checking the lexer's token grammar against the prose disclosure).
Fix: freeze lexical form as part of the claim's counter premise, and run one representative
source token through the actual matcher before freezing any matcher-dependent disclosure.

**M28-15 · wave prompts omitted the bound Godspeed directive bytes.** Class: landing. Evidence:
the committed `.ufo/waves/round-28/wave1-spec.json` tasks lead with `/skill:godspeed` and then
the assignment, but do not include the verbatim bytes from
`/home/vgpnk/.agents/skills/godspeed/directive.md` (opened at close; lines 1-8).
Captured-by: the prompt's §3 Godspeed lead; no validator enforced the required prefix bytes.
Fix: include the exact directive bytes after `/skill:godspeed` in every future fresh task,
and add a pre-dispatch byte check over every `prompt` field before validating the wave.
## Compliance

**Freeze discipline (R25-1, R9).** `claims.json` committed at `c9f8b11` before dispatch and never
edited in place; one correction landed as an appended file, `.ufo/waves/round-28/claims-erratum-1.md`
(M28-2). The freeze's own `frozen_at_utc` is `2026-10-25T00:00:00Z` while the file's real creation
time preceded dispatch — the round-24 erratum pattern; no measurement in this lesson precedes the
freeze commit. Round-27 fixtures were re-run, not re-created
(`.ufo/waves/round-28/c1-controls/`, `c2-controls/`, `census-before.txt`).

**Ownership.** Every production path had exactly one writer, and the tree shows exactly those
files: `corpus/instruments/anchorcheck.py` (`ExecImplC1`, `95333e29…`), `corpus/instruments/README.md`
(`ExecInstrReadme`, 196 → **327** lines, `131 insertions / 0 deletions`, sha256 `cf35a643…`; the seat's
receipt carries two successive states — 289 lines / 93 insertions before its second, erratum-driven
append, 327 / 131 after — same owner, still one writer),
`SKILL.md` (`ScribeSkillGate`, `125be37d…`, 1032 → 1035),
`corpus/knowledge/japanese-domestic-disclosure-workflow.md` (`ScribeEntryC2`, `a22d2321…`, 103 lines),
`corpus/SOURCES.md` (`ScribeRegistryC2`, `e59240f8…`, 41 → 42 rows),
`corpus/README.md` (`ScribeReadmeC2`, `5f458a7a…`), `corpus/QUALITY.md` (`ScribeR14`, `00d4b2a3…`,
77 → 83), `LOG.md` (`ScribeLog`, `c30b7608…`), `SCORECARD.md` (`ScribeScorecard`, `95a0ec5b…`).
`git status --porcelain` shows no other tracked modification and no untracked file outside
`.ufo/waves/round-28/`, `receipts/` and `corpus/source-snapshots/round-28/` (`SentinelScope` §1).
Cross-write check: `ExecScopeSweep` (`scope-check.sh` sha256 `0f30d2c8…`, self-proved with
`selftest cases=13 failures=0` including five off-map VIOLATION cases) reports
`lane_prod_paths=12 lane_wave_paths=238 lane_violations=0`; `SentinelScope` finds **0 hard-rule
violations**. The one substantive flag is the R6 line displacement (M28-6), recorded by both.

**Census, before / mid / after.** Before, at the freeze: exit 0, **41 rows** (tier A 38 / B 1 / C 2;
mined 29, queued 9, rejected 3), with only the two pre-existing W04 warnings
(`S028` duplicating S006's HackerOne URL, `S029` superseding S024 on the EUR-Lex CRA URL) and no
E-codes (`.ufo/waves/round-28/census-before.txt`). Mid-wave, 17:24Z–17:26:17Z: exit **1** with
`E11 S041` and `E11 S042` — both naming the same then-absent `used-by` file; a transient ordering
state, discharged when the entry landed (ScribeLog, RevRegistryC2, ExecCensusDry, RevCounters2).
After, at `corpus/SOURCES.md` sha256 `e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d`
(this seat's run at 17:30Z, independently corroborated by `RevCensusEnd` and `ScribeCensusNote` §7):
**exit 0, 42 rows** (tier A **39** / B 1 / C 2; mined **30**, queued 9, rejected 3), exactly one
`| S042 |` row, W04 still only S028/S029 — so the round adds one tier-A mined row and no warning.
The ordering constraint is discharged, not waived: `E11` makes a registry row whose `used-by` file
is absent a hard failure, which is why the transient red is evidence the gate works.

**Scope and safety.** No write to the fleet root, any sibling lane, `/home/vgpnk/Projects/shokuknow`
(read-only; `merge/kasegi/` max mtime 2026-10-24T23:33Z, 0 files newer than the wave — ExecScopeSweep
limb 3, SentinelScope §3), `/home/vgpnk/Projects/shokunin/.ufo/state`, `.scratch`, `MANIFEST.json`, `/home/vgpnk/Projects/shokunin/templates/` or fleet
`/home/vgpnk/Projects/shokunin/scripts/`. No credential material, session or private URL in any artifact written this round
(SentinelScope §2 scans production diffs, the entry, the snapshots and the scratch tree; the only
lookalikes are prose uses of "token" and page-content strings inside a captured policy document).
Live network use: 2 dispatched captures plus 11 verification probes, all GETs with the instrument UA
(`kasegi-shokunin/1.0 …`) on public URLs, none credentialed; two quarantine probes failed TLS
verification and captured nothing. No fixture in this wave contacted a live target — `--selftest`
builds its 9 cases under `tempfile.mkdtemp` and removes them (post-run `ls /tmp/anchorcheck-selftest-*`
→ none).

**Tooling.** No `pacman` transaction was attempted by any seat (host-wide pause respected; every
receipt says so). One ephemeral use: `uv run --with markdown-it-py` (uv 0.13.0, markdown-it-py
4.2.0, CPython 3.14.8) to render the SKILL.md table for `ExecSkillGateSupport`'s GFM check — no
persistent install. `pdftotext` 26.08.0 was already present. This seat installed and upgraded
nothing.

**Close-out ledger — what is still owed, with the command that closes it.**

1. `python3 .ufo/waves/round-28/assemble-receipts.py` → `.ufo/waves/round-28/c1-receipt-index.txt`
   (absent at assembly). Then the two greps `grep -cE 'selftest cases='` → 1 and
   `grep -oE 'instrument_sha256=[0-9a-f]{64}'` → the landed digest. Two defects must be corrected in
   the assembler or by hand first: it takes the SKILL.md line as `stdout.split('\n')[-1]`, which is a
   verdict line, not the `== …` summary (`ExecImplC1` O2); and it emits none of C2's manifest-quote
   or capture-sha lines although the C2 kill rule turns on exactly-once quotes (`ConnClaims` §3).
2. The four frozen C1 counters at the landed digest (already measured twice at `95333e29…`, must be
   re-measured at the commit that contains this lesson). Block:
   `sha256sum corpus/instruments/anchorcheck.py`; bad-fixture `echo $?` → 1; bounties-fixture
   `grep -c BOUNTIES-ABSENT` → 1; `--selftest` → `selftest cases=9 failures=0`, exit 0;
   `SKILL.md` → exit 0 with the summary above.
3. The five frozen C2 counters — all currently green (`RevCounters2`, `ExecReceiptCanonC2`): 12 /
   1 / 1 / census exit 0 at 42 rows / `entries=15 pass=15 exit=0`.
4. Non-author spot-check of one refusal (Gate §Spot-check) — owed.
5. `density.py` re-measure after the SKILL.md append, attributed to the added block.


## Close-out addendum (L1; supersedes the drafting-time DRAFT/PENDING labels above)

The 69-seat wave completed; `wave1-results.json` contains 69 final outputs and the role
histogram recorded at the top of this lesson. No seat is reported dead; the last seat report
was `ScoutGateRegistry.md`. The wave's attack receipts are not a universal proof: CritC2Kill
demonstrated counterexamples against the counters when used without the admitted-entry and
manifest-path binding, and MutSelftestC1 showed that the string counter alone accepts
skip-fixtures mutants. Those are recorded as instrument limits; the actual frozen predicates
were checked on the landed content, and the independent adversarial results remain in the wave
evidence.

L1 close-out actions:

- Recheck-audit expected list regenerated from the working-tree glob after F12 entry landing:
  `knowledge-expected.txt` now has 40 entry lines / 42 physical lines; live audit exits 0,
  `lines=40 total=40 pass=40`, `expected=40 missing=0 unexpected=0`.
- C1 selftest isolation defect from CritC1Kill was independently reproduced with `GIT_DIR`:
  before fix `selftest cases=9 failures=1`, exit 1; after clearing inherited `GIT_*` for the
  isolated child process, same perturbation gives `cases=9 failures=0`, exit 0. See M28-13,
  claims erratum 2, and `anchorcheck.py:311-317`.
- Canonical C1 receipt index assembled at the final instrument bytes:
  `.ufo/waves/round-28/c1-receipt-index.txt`, sha256
  `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`. It records the
  instrument sha256 `23818c1204c38ee8d1bb0c6d449dd0ffb3c9181271f14fb3d7aab25a73ee7396`,
  one `selftest cases=9 failures=0` line, and the C1/C2 counter outputs. Post-commit re-runs
  are recorded in the report.
- Counter (d)'s frozen `sed` extractor is defective: its pattern expects `bad; N bad`, while
  the summary prints `N bad; ...`; it returns no value for both before and after. The actual
  summary field was parsed directly and remained bad=0. Claims remain frozen; this instrument
  defect is reported honestly (CritGlobal F5) and is not silently substituted as a frozen
  counter.
- C2 final gates: F12 12 admitted; one entry cites S042; registry 42 rows; census exit 0;
  frontier harness 15/15; separate `source-recheck.py --source S041` and `--source S042`
  both exit 0 (the CLI flag is single-valued). The Gate records an admitted F12/S042 and
  rejected candidates with located inline quotes; the captures were opened this round.
- Density guard after SKILL.md's append: `density.py` mean 160.2, 20 blocks, 656 path cites,
  versus round-base 150.3, 20, 652. This is disclosed as changed measurement, not a claimed
  axis score move.
- The non-author refusal spot-check remains an independent closure duty; this lesson does not
  claim a reviewer outside the round performed it.
## Carry-forward for round 29

1. **Dispatch counters after their subject lands**, or give them the landed digest; keep the
   PRE-STATE label rule (M28-1). Seven PRE-STATE receipts are the round's largest evidence tax.
2. **Every frozen disclosure names the lexical form the matcher reads**, and its fixture runs
   before the freeze (M28-2, extending M27-1 from fixtures to prose).
3. **Every frozen counter command is executed once against its frozen before bytes before the file
   commits.** M28-3's `bad=` limb printed nothing for the whole round; that is a two-minute check.
4. **Decide R6 for table rows** (M28-6): amend the criterion with the carve-out, or move registry
   rows to an end-of-file table. The round's `SKILL.md` ships a disclosed +1 shift and a stale
   `resolve-dispatch-fixtures.json:159,161` pointer to `SKILL.md:1000`.
5. **Promote Q9's stem check into an instrument** (M28-8) and register the `check_q9.py` reader
   beside `source-recheck.py`; today C2's Q9 clause rests on hand-run receipts.
6. **Fix `frontier-recheck-count.py`'s crash on an absent entry** (M28-5) so a half-landed tree
   yields `pass=14 of 15`, and re-point `resolve-dispatch-fixtures.json` at the current SKILL.md
   line for the four-alternative set.
7. **Re-base the density guard at each round's base** (M28-9) — the same-byte comparand is
   150.3 / 20 blocks / 652 at `c9f8b11`, not the 154.0 / 19 shipped in the dispatch.
8. **Carried debt, unchanged:** 23 of 40 recheck lines stay gated on lost bases (the 2026-09-28 and
   2026-10-12 losses); `anchorcheck.py`'s fail-closed rule now makes five corpus files exit 1 by
   design — that is the intended cost of the gate and should stay disclosed wherever the corpus is
   quoted.
