# ScribeLessonGate — round-28 Gate section draft (for ScribeLesson to lift into `corpus/lessons/round-28.md`)

Seat: `ScribeLessonGate` (leaf, draft only; no production byte written by this seat).
Round 28 wave 1, lane base `c9f8b115a098c65356e4b3b6048af45a37ab8395`. Composed 2026-10-25
17:24Z–17:31Z (UTC) against the landed working tree. Every number below was produced by a
command this seat ran, or is attributed in-line to the seat that ran it. Nothing is copied
from a package byte as evidence.

> **Assembly note (drop before commit).** This file is the `## Gate` section only. Two facts
> belong to other seats and must be taken from their landed receipts, not from here: the
> kill-rule status table and the before→after counter rows (ScribeScorecard / ExecReceiptCanonC1 /
> ExecC2Counters). If ScoutAssimilation's slice receipt disagrees with §Quarantine below, its
> hand-check wins for the row it names; this seat's fetch table is the independent cross-check.

---

## Gate — the assimilation set

Package: `/home/vgpnk/Projects/shokuknow/merge/kasegi` (read-only in this round; no campaign
tool was run there, and nothing was written into it). Round shape: ONE theme — the Japanese
state-coordinated disclosure workflow — with one entry re-grounded on two fresh captures
(the IPA intake-process page as the new row S042, the JPCERT/CC 2026 P-guideline re-captured
under the existing row S041), plus the quarantine slice and two standing reject candidates.

Package bytes read this round (all under the path above): `MERGE-REPORT.md`;
`SOURCES.append.md` rows S042, S043, S044, S045, S046, S068, S080; the staged entries
`knowledge/corpus/knowledge/japanese-domestic-disclosure-workflow.md`,
`…/chinese-criminal-thresholds-and-authorisation.md`,
`…/vendor-third-party-finding-coordination-2026-10-23.md`. Register read (read-only):
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`.

### Collision / adoption ids

Id-collision check ran in scratch (`.ufo/waves/round-28/assimilation/collision-check.txt`,
taken before the S042 append): registry `reg=41`, staged `staged=94`, collisions **11**
(S031–S041). The adopted id therefore continues the lane registry from **S042**. The guard was
proved discriminating against a 0-3-leading-space fixture
(`.ufo/waves/round-28/assimilation/guard-proof.txt`): the tolerant pattern reports the indented
duplicate, `^\|` alone does not. Lane result: no colliding row can be appended silently.
Re-measured on the live worktree after the S042 append (ScoutAssimilation, same receipt):
`lane reg-ids = 42`, `staged = 94`, `collisions = 12` (S031–S042) — the count moved because the
lane now owns S042 too; `same-document=0 different-document=11` at the frozen base means every
collision is an id-space overlap, not a duplicate document.

The two staged rows this round touches are resolved **by document, never by arithmetic**:

| Staged id | Staged URL | Resolves to | Verdict |
|---|---|---|---|
| S042 | `https://www.ipa.go.jp/security/todokede/vuln/process.html` | lane **S042** (free at adoption: `grep -cE '^ {0,3}\| *S042 *\|' corpus/SOURCES.md` → 0 before the append; no lane row carried that URL: `grep -cF …todokede/vuln/process.html corpus/SOURCES.md` → 0) | **new row admitted** |
| S043 | `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | lane **S041** (registered round 26; `grep -cF` of the URL → 1, at `corpus/SOURCES.md:47`) | **cited, not re-registered** |

S043 is not an adoption candidate because the document is already registered: URL equality with
lane S041 (`.ufo/waves/round-28/assimilation/by-document-map.txt` §7 prints both URLs and they
are the same string), and S041's row is `mined`/tier A. The staged id therefore resolves to a
citation, not a row — adopting it again would duplicate a document the registry already holds.
ScoutAssimilation measured the consequence: appending staged S043 alongside live S041 makes the
census report `W04 S043 duplicate url www.jpcert.or.jp/vh/partnership_guideline2026.pdf across
scopes`. The census, not arithmetic, is the second witness here.

### Admitted

| Row | Admitted as | Document / capture | Opened | Evidence | Entry |
|---|---|---|---|---|---|
| S042 | tier **A**, status `mined` | IPA 脆弱性関連情報の届出受付業務における取扱いプロセス — `https://www.ipa.go.jp/security/todokede/vuln/process.html` | **2026-10-25** | `corpus/source-snapshots/round-28/S042.txt` (html capture via `capture-source.py --kind html`, status 200, fetched 229,982 B → 60,508 B, 974 lines, sha256 `b432ec165693d005fa5de326ffb40d60d0476b18a345a9fc6d631d10b9c96966`, utc `2026-10-25T17:22:03Z`); `manifest.json` binds **6** quote assertions, every one `occurrences=1` | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (`used-by` names exactly this entry) |
| S041 | existing row, tier A / `mined`, **not re-registered** | JPCERT/CC 情報セキュリティ早期警戒パートナーシップガイドライン 2026年10月 — `https://www.jpcert.or.jp/vh/partnership_guideline2026.pdf` | 2026-10-25 (unchanged) | **round-28 re-capture** `corpus/source-snapshots/round-28/S041.txt`: status 200, fetched 1,338,665 B → 147,267 B, 2354 lines, sha256 `e18acbf99d137c262c1f08c6f0f92887236641ec8abcccfc7470247242f5ab47`, utc `2026-10-25T17:22:12Z`; `cmp` against the round-26 capture → **IDENTICAL** (`cmp_exit=0`), so F11's round-26 line anchors still hold. Manifest binds 6 assertions, all `occurrences=1` | the same F12 entry (`used-by` gained it, §Registry changes) |

**The new row, in the Gate's own words (round-26 routed defect 3 — quote inline, not by pointer).**

- S042 URL: `https://www.ipa.go.jp/security/todokede/vuln/process.html`; access date **2026-10-25**;
  located quote, `S042.txt:145`, `occurrences=1`, pinned by manifest assertion `S042:Q1`:
  「JPCERT/CC は製品開発者への連絡を開始した旨（起算日）、および、製品開発者へ詳細情報を連絡した旨をIPAへ連絡します。」
  (63 chars, 2 whitespace-words — under the 25-word cap; the step-5 sentence ScoutIpaRecon
  located, pinned as manifest `S042:Q1`). The heading it answers to is
  `5.起算日の連絡` (`S042.txt:144`); the heading alone is **not** admissible as evidence
  (8 chars < `source-recheck.py` `MIN_QUOTE_CHARS=12`, measured `UNAVAILABLE
  reason=quote-too-short-to-be-evidence` on the manifest's first build — see §Defects caught).

**The admitted entry** (`corpus/knowledge/japanese-domestic-disclosure-workflow.md`, 103 lines /
18,452 B, sha256 `a0f8e6172110c8419bdc1ea39823736b0b066e6155fc9a3f6f89cf7f4c260b59`, created this
round):

| Property | Landed value |
|---|---|
| header | `source: S041` and `source: S042` (two lines, both capture-anchored), `verified-at: 2026-10-25`, `ground: F12` |
| recheck | one executable line, cwd-independent: `cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-28/manifest.json --source S041 && … --source S042` |
| measured, foreign cwd (`/tmp`) | `bash -n` exit **0**; run exit **0**; both ids re-verified from the committed pins |
| `--source` id set = declared `source:` id set | S041, S042 — equal; the two invocations are chained because `source-recheck.py:275` accepts one `--source` per invocation (the entry discloses this in §Limits) |
| frontier binding | `frontier-recheck-count.py` → `PASS F12 knowledge/japanese-domestic-disclosure-workflow.md ids=S041,S042 exit=0`, `entries=15 pass=15 exit=0` |
| recheck-audit (entry granularity, Q10/R12) | `japanese-domestic-disclosure-workflow.md frozen=111 strict=111111 lane=0 foreign=0 executes  PASS` — all six strict limbs, from `/` and from the lane root (ScribeEntryC2 receipt check 3) |
| Q9 binding (ExecHarnessC2, `.ufo/waves/round-28/receipts/ExecHarnessC2.txt` §A3) | `PASS S041 … assertions=7`, `PASS S042 … assertions=7`, `q9 ids=2 failures=0`; 12 quotes, every one exactly-once raw and normalized |
| corpus census | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → **exit 0**, rows 42, only the pre-existing W04 S028/S029 |

**What the entry had to be re-grounded away from (staged → lane).** The staged package entry is
not adopted as written. Three measured deviations, all recorded in the entry's §Limits and in
`ScribeRegistryC2`'s receipt:

1. **"six-step" web-application path is false on both captures.** Staged bytes
   (`japanese-domestic-disclosure-workflow.md:45-46`): "The IPA process page carries a second
   six-step flow for web applications". The capture numbers **seven** (`S042.txt:162-182`, step
   `7.` is the statistics step at `S042.txt:181-182`), and the guideline's 図４ agrees
   (`S041.txt:1331`). The landed entry states seven and cites the lines.
2. **The staged S043 id is not carried.** The entry cites the guideline under lane **S041** and
   says so in §Limits; no lane row was created for the document.
3. **The staged `opened` date moved 2026-10-23 → 2026-10-25** (today's access date), and the
   staged `anchor` cell's "ウェブアプリケーション … steps 1 to 6" was dropped from the registry
   row in favour of capture line numbers for the product flow and step 5.

### Refused (rejects carry flip conditions)

| Candidate (package path) | Failing gate | Reason (measured evidence) | Flip condition |
|---|---|---|---|
| `knowledge/corpus/knowledge/chinese-criminal-thresholds-and-authorisation.md` — standing refusal, **re-confirmed** | Q2, Q3, Q4, Q5, Q7/Q10; `ground` | (1) **Q2** — it rests on staged S044/S045/S046, none of which is a lane registry row (lane registry = S001–S042, 42 rows; `grep -cE '^ {0,3}\| *S04[3-9] *\|' corpus/SOURCES.md` → **0**), so "opened in the admitting round" cannot be satisfied. (2) **Q4** — it generalises three instruments into one jurisdiction-wide rule: "the Chinese criminal risk attaches to **scale and effect**, not to the mere act of unauthorised access" (`chinese-criminal-thresholds-and-authorisation.md:47-48`), while its own §The claim describes 285(1) as covering state-affairs/defence/cutting-edge systems with **no** quantitative element. (3) **Q3** — "and it is purely quantitative" (`:27`) is falsified by its own cited row: staged S044's anchor is "第一条 items （一）至（五）" (`SOURCES.append.md:20`), and item (五) is the catch-all 其他情节严重的情形 recorded in the round-26 lesson §Refused; five items cannot be "purely quantitative". (4) **Q5** — no `### Rejected` section: `grep -n '^### Rejected'` → exit 1 over both reject files. (5) **Q7/Q10** — its `recheck:` is a prose+command hybrid ending "(ran 2026-10-23)"; `bash -n` on the line → **exit 2**, `syntax error near unexpected token '('`. (6) **`ground: F12`** was written in the package's own F-space (ScoutAssimilation §5: package F12 = the Chinese statutory family, package F13 = this round's workflow), so read against the lane it resolves to `corpus/README.md:213` F12 = *Japanese state-coordinated disclosure workflow* — a subject mismatch — while the entry's own text names F03, which is the lane row that actually matches ("Authorization, safe harbor, and scope"). | Restate 285(1) as a conduct offence for the state-affairs limb and keep paragraphs 2–3 separate; quote 第一条 in full **including (五)** with a located page/line; delete "purely quantitative"; add a `### Rejected` block; make `recheck:` one executable command with its own `cd <lane-root> &&` prefix plus a control that fails; register the three documents under free lane ids **first** (S043+ are free); re-ground `F12` → `F03`. |
| `knowledge/corpus/knowledge/vendor-third-party-finding-coordination-2026-10-23.md` — **new refusal** | `ground` (no lane row), Q2, Q3, Q7/Q10, parent absent | (1) **The named gate** — `ground: F20` names no lane frontier row: `grep -cE '\| F20 ' corpus/README.md` → **0** (the frontier stops at F12). (2) **Q2** — its sole source is staged S080 (`SOURCES.append.md:21`, MSRC MSVR), not a lane registry row. (3) **Q3** — the claim is a paraphrase of the `source:` fragment "MSVR learns about vulnerabilities in third-party products in three ways" (`:4`, `:16`) with no located line or page and no capture; the three routes are restated, not quoted. (4) **Q7/Q10** — `recheck:` is "180d — \`curl -sSL https://www.microsoft.com/en-us/msrc/msvr\` and confirm the three routes are still listed (ran 2026-10-23)"; `bash -n` → **exit 2**, `syntax error near unexpected token '('`. (5) **Parent absent** — it says it "extends the round-4 entry vendor-cvd-policy-crosswalk", which the lane refused in round 26 and does not hold (`test -e corpus/knowledge/vendor-cvd-policy-crosswalk-2026-10-23.md` → **no**), so the stated parent cannot carry it. | Register S080 under a lane id, capture the MSVR page into a round snapshot and pin the three-route paragraph verbatim (Q3/Manifest), restate `recheck:` as one cwd-prefixed command with a failing control, re-ground on lane **F10** (vendor-side disclosure policies as corpus objects) instead of F20, and cite the two *admitted* F10 entries rather than the refused crosswalk. |

No Q/R bar was relaxed for either reject. Neither staged entry file exists in the lane
(`test -e corpus/knowledge/…` → no for both), so nothing refused is half-landed.

### Quarantine slice — seven rows hand-checked (2026-10-25, instrument UA)

Slice derived from the register itself (header and `## By lane` totals are stale, as the round
prompt warns): `awk -F'|' -v l='kasegi' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'`
→ 7 rows. **None adopted.** This seat ran the fetch/quote-locate itself because the assigned
scout receipt was not on disk at composition time; command and full output:
`.ufo/waves/round-28/wave1/ScribeLessonGate/quarantine-handcheck.sh|.out` (utc
`2026-10-25T17:24:29Z`). Normalization: tags stripped, whitespace collapsed (Q8).

| Staged row | Register class (verbatim) | Measured verdict (2026-10-25) | Meaning for adoption |
|---|---|---|---|
| S037 | `payload-absent` | **`fetched no-quote`** — 200 / 24,189 B; the staged anchor is a composite of separate table cells: the whole anchor string occurs **0×**, while `发布日期` occurs 1× and `GB/T 30279-2020` 2× | reachable + authentic metadata; quote-form defect — not appendable as staged (cell-anchored fragments would be needed) |
| S054 | `payload-absent` | **`fetched no-quote`** — 200 / 513,648 B; the PDF's own header is glyph-spaced (`府 サ 連 第 ７ 号`, `令和８年９月 17 日`), so the staged `府連第7号` occurs **0×** under whitespace collapse | source real, quote is a re-construction: not appendable as staged (a longer fragment or a spacing-normalized capture is needed) |
| S048 | the cited source could not be fetched, so no quote was checked | **`unfetchable`** — `gbDetailed?id=3B865A…` returns **404 / 748 B**; anchor `项目周期` 0× | dead as cited; refuse until an R8 `supersedes` row names a live id |
| S065 | the cited source could not be fetched, so no quote was checked | **`fetched quote-located`** — 200 / 7,465,472 B; `现行有效法律目录` 1×, `刑法（7 件）` 1× | reachable + quote located; **not adopted** — no admitted entry cites it, and registering it would be an unmotivated row |
| S068 | the cited source could not be fetched, so no quote was checked | **`already-mined-legacy`** — 200 / 94,027 B; `The Cisco PSIRT aligns its practices with ISO/IEC 29147:2018` 1× | the same document is lane **S040** (round 25; URL byte-equal to `SOURCES.md:46`); no new row |
| S069 | the cited source could not be fetched, so no quote was checked | **`unfetchable`** — `gbPlan/download?path=…` → **302**, 0 B, redirect target fails TLS (`curl: (60) … unable to get local issuer certificate`) | unverifiable from these endpoints |
| S070 | the cited source could not be fetched, so no quote was checked | **`unfetchable`** — same 302/0 B + TLS failure | unverifiable from these endpoints |

The register's two unchecked families remain exactly that: a fetch today does not certify a
quote, and for S037/S054 the staged anchor fragment is not verbatim anywhere in the fetched bytes.
Reachability is reported, not upgraded into adoption.

### considerthese item landed

`considerthese/2026-10-25.md` proposal 1 (wave-evidence economy) landed as `corpus/QUALITY.md`
**R14** (round-28 additions table): evidence is receipts and digests in git, a control/fixture
tree larger than a few hundred kilobytes is committed as one content-addressed tarball (sha256
in the receipt) or regenerated from `git archive <rev>` plus a named mutation script, never as a
full corpus copy. Practised in-round: the captures are text snapshots with sha256 pins and the
walk's fixtures stay small (`capture-source.py` → 60 KB / 147 KB; the collision guard's fixture
pair is 6 lines and 5 lines, `wc -l` on
`.ufo/waves/round-28/assimilation/fixture/fixture-{SOURCES,staged}.md`), so nothing in this
wave commits a corpus-sized fixture tree.

### Registry changes — every change old → new, inline

- **S042 appended** (new row, `corpus/SOURCES.md:48`): tier A, `mined`, `opened 2026-10-25`,
  `recheck 180d`, `used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md`.
  Against the staged row (`SOURCES.append.md:18`): `opened 2026-10-23 → 2026-10-25`; anchor's
  "ウェブアプリケーションの取扱いプロセス steps 1 to 6" **dropped** (capture shows seven) →
  "ソフトウエア製品の取扱いプロセス steps 1 to 10 (L132-L160), step 5 起算日の連絡 (L144-L145)"
  re-read from the capture; `teaches` rewritten to one grounded benefit; `status mined` and
  `recheck 180d` unchanged.
- **S041 `used-by` old → new** (R8, logged in `## Registry changes` and in
  `ScribeRegistryC2`'s receipt):
  `corpus/knowledge/iso-29147-and-30111-division-of-labour.md, corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md`
  → `corpus/knowledge/iso-29147-and-30111-division-of-labour.md, corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md, corpus/knowledge/japanese-domestic-disclosure-workflow.md`.
  Every other S041 cell is byte-identical (cell-split diff: 13 cells both sides, only the
  used-by cell differs) — `status mined`, `opened 2026-10-25`, `recheck 180d` **unchanged**.
- No status or recheck cell changed on any row this round; no row was superseded, retired or
  re-titled.

### Defects caught mid-wave (recorded, because each was measured before landing)

1. **Manifest Q1 was a heading, not evidence.** First build (`fa1f366f…`) exited **2** with
   `S042:Q1 UNAVAILABLE reason=quote-too-short-to-be-evidence`: the step-5 heading normalizes to
   8 chars, under `MIN_QUOTE_CHARS=12`. Fixed by replacing Q1 with the L145 body sentence; the
   landed manifest (`e62ddad133ffc19ebc66822c0fcb3b48ed4993c101f05262302acc58714f291d`, 5038 B)
   exits 0 on both ids, all assertions `occurrences=1`. ExecManifest and ExecHarnessC2 measured
   the same failure independently in the same window.
2. **`source-recheck.py` exits 0 for three of the C2 kill rule's own failure states.**
   ExecHarnessC2 §D: stem≠id, an unanchored exactly-twice quote, and a broken anchor all exit
   **0**; only `quote-too-short` and `outside-manifest-directory` exit 2. The Q9 clause therefore
   cannot be read off `source-recheck`'s exit code or a harness `PASS` row — `check_q9.py` is the
   reader, and it fails each of the three states (controls A–D).
3. **A frontier row admitted before its entry existed crashes the harness.** With F12 `admitted`
   and the entry file absent, `frontier-recheck-count.py` raised an uncaught `FileNotFoundError`
   at `entry_contract()` (exit 1, no `entries=`/`pass=` line, no named problem). It is not a
   false pass, but a mid-wave run of that harness is not a count. Landed state is clean
   (`entries=15 pass=15 exit=0`), so this is ordering evidence, not an open defect.
4. **`source-recheck --source` is single-valued** (`:275`): a literal `--source S041 --source S042`
   re-derives only the last id. The entry chains two invocations instead, and says so in §Limits.
5. **The staged package cannot be appended wholesale.** ScoutAssimilation §5 measured **43 of 94**
   staged rows (S081–S124) carrying prose `recheck` cells, i.e. the census `E09` class. Neither
   row adopted this round is in that set (both are `180d`), which is why S042 could be normalised
   and appended; the other 43 would have to be rewritten first. This is a lane-wide admission
   boundary, not a defect of this round's two rows.

### What this Gate does not claim

- It does not report counter before→after values; those belong to ScribeScorecard and the
  canonical receipt index at the landed instrument digest.
- It does not claim any re-fetch reproduces the S042 digest: the captured page carries a live
  news feed below `S042.txt:209`, so only the committed pins bind, not upstream bytes.
- It does not claim the staged package's own F-space maps onto the lane's frontier numbering.
  Measured by ScoutAssimilation §5: **package F12 = the Chinese statutory family** and **package
  F13 = this round's workflow**, while the lane's F12 is that workflow and its F10 is the
  vendor-policy row. So a staged `ground:` id is never a lane id: the rejected Chinese entry's
  `F12` now points at an unrelated lane row, the rejected vendor entry's `F20` points at no row
  at all, and the admitted entry had to be grounded on the lane id F12 explicitly.
- It does not claim the quarantine rows are false. S037/S054/S065 are reachable; their *quotes*
  are what fails, and S048/S069/S070 are unreachable from the cited endpoints.
- It does not claim the lane's expected-list gate is green at compose. Measured 2026-10-25T17:31Z:
  `python3 corpus/instruments/recheck-audit.py` prints `lines=40 total=40 pass=40 fail-closed=24
  parse_fail=0 cwd_fail=0 paths_fail=0` and then `expect=present expected=39 missing=0
  unexpected=1 exit=1` (`unexpected=corpus/knowledge/japanese-domestic-disclosure-workflow.md`).
  `corpus/instruments/knowledge-expected.txt` is outside this seat's write scope; ExecExpectedList
  owns the regeneration and its receipt carries the exact command. The entry is not at fault — the
  list is one entry short of the tree — but until the list is regenerated the C1(d) surface is red,
  and this Gate must not be read as saying otherwise.
