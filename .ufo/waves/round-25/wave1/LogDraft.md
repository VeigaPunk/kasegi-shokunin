# LogDraft — round-25 LOG entry draft (scribe report)

Seat: `L1Kasegi25.LogDraft` (scribe, leaf). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`,
base `b49948f1164ef65106b2c4cbee3f53e8a44b8c41`. Draft written at
`.ufo/waves/round-25/wave1/log-entry.md` (7.5 KB, 11 bullets). No production edit, no VCS write, no
spawn, no background job, no tool install or upgrade. This report is the only other file I wrote.

Drafting happened while wave 1 was still landing (first seat report 05:27, my last measurement 05:41),
so every figure below is either a command I ran in this session or a lane receipt I read; anything
still moving is named as such.

## 1. Acceptance

| # | Requirement | Where in the draft | Status |
|---|---|---|---|
| a | Both frozen claims named, each with a before value and a counter command | C1 bullet (lines 7-18): counter `python3 corpus/instruments/recheck-audit.py --json .ufo/waves/round-25/c1-after.json`, before `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`. C2 bullet (30-43): the three `claims.json` counters (frontier `awk`, `grep -l '^source: S03…'`, `sources-census.sh validate`), before `frontier 9, entries 0, census exit 0` | pass |
| b | No invented commit hash; `{{LANE_HEAD}}` left for the L1 | Preamble: "base `b49948f1`, lane HEAD at this entry `{{LANE_HEAD}}`"; D24-1 line cites `{{LANE_HEAD}}` | pass — the only hash written is the base revision, read from `claims.json` |
| c | D24-1..D24-5, one line each, with what closed it | Bullet "Routed defects D24-1…D24-5 — all five closed", five sub-bullets | pass |
| — | `{{WAVES}}` for wave shape/seat counts | Waves bullet, with the measured dispatch counts beside it | pass |
| — | `{{CENSUS}}` for census before/after | Census bullet (before measured, after placeholder) | pass |

## 2. Numbers I measured this session

| Fact | Command | Observed |
|---|---|---|
| C1 before | `cat .ufo/waves/round-25/c1-before.txt` (frozen receipt) | `lines=35 pass=6 fail-closed=23 parse_fail=23 cwd_fail=6 paths_fail=0 exit=1`, `BEFORE_EXIT=1` |
| C1 frozen instrument / receipt digests | `cat .ufo/waves/round-25/c1-instrument-digest.txt` | instrument `d07af435…`, `c1-before.json` `3e3eeb4e…` |
| C1 after (final) | `python3 corpus/instruments/recheck-audit.py --quiet`; `c1-after.json` summary | `lines=37 total=37 complete=True pass=37 pass_strict=37 fail-closed=23 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` |
| Fail-closed exit code before → after | per-entry `class == fail-closed` over both receipts | before 23 entries at `(lane_exit 2, foreign_exit 2)`; after 23 at `(1, 1)` |
| Files rewritten by C1 | `git diff --numstat -- corpus/knowledge` | 29 files, each `1 1` |
| `cd`-prefix coverage | `grep -h '^recheck: ' corpus/knowledge/*.md \| grep -c '^recheck: cd /home/vgpnk/Projects/shokunin/kasegi-shokunin &&'` / total | 36 of 37; the exception is `root-loss-2026-10-12.md` (already cwd-independent, `test ! -e ~/Projects/...`) |
| Knowledge files | `ls corpus/knowledge/*.md \| wc -l` | 37 |
| C2 before: frontier | `awk -F'\|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md` | **9** at 05:33 (F10 row not yet appended); **10** at 05:41 after the L1's append |
| C2 before: entries citing S036+ | `grep -lE '^source: S0(3[6-9]\|[4-9][0-9])' corpus/knowledge/*.md \| wc -l` | 0 before, 2 after |
| Registry rows | `grep -cE '^\| *S[0-9]{3} ' corpus/SOURCES.md` | **35** before the append, **40** after (05:41) |
| Census after | `sources-census.sh census` / `validate` | `rows 40, tier.A 37, tier.B 1, tier.C 2, status.mined 28, queued 9, rejected 3`; validate exit 0, file `ok`, only W04 ×2 |
| Capture digests | `sha256sum corpus/source-snapshots/round-25/S0{36,37,38,39,40}.txt` | `022ca4f4…`, `b204aa7f…`, `09e077d3…`, `657e7b4c…`, `b7f7b55f…` — all five match `.ufo/waves/round-25/capture-log.txt` |
| Round-25 manifest | `python3 -c "…len(m['sources']), sum(len(s['quotes']))…"` | 5 records, 42 quote assertions |
| D24-2 count | `sum(len(s['quotes']))` over `corpus/source-snapshots/round-24/manifest.json` | 76 |
| D24-4 receipt | `sed -n '5,6p' .ufo/waves/round-24/c1-control-baseline.txt` | `L4 liveness expect=INTERNAL actual=INTERNAL FAIL` then `also expect=MIRROR-EQUIVALENT actual=GONE FAIL path_check=missing-path` |
| Assimilation id sets | `cat .ufo/waves/round-25/assimilation/ids/{reg-ids,staged-ids,collisions}` | reg 35 ids (S001–S035), staged 94 (S031–S124), collisions 5 (S031–S035) |
| Staged rows mirror | `scripts/sources-census.sh validate --file .ufo/waves/round-25/assimilation/rows/validate/corpus/SOURCES.md` | exit 0, only the two pre-existing W04s (S028, S029) |
| Wave dispatch | `wave1-spec.json` / `wave1-dispatch.json` | 38 items, `counts.spawn=38`; reviewer 12, scout 7, executor 5, scribe 5, critic 4, mutation-tester 2, connector 1, sentinel 1, simplifier 1 |
| Census before | `claims.json` `frontier_step` + scout receipt | exit 0, rows 35, malformed 0, A=32 B=1 C=2, mined=23 queued=9 rejected=3, W04 ×2 |

## 3. Numbers I could NOT verify (and how the draft handles them)

- **C1 "exit=0" is a moving target.** The instrument and the after-receipt changed four times while I
  drafted: `c1-after.json` at 05:28 (`lines=35 pass=35 exit=0`), 05:33:43 (`lines=36 pass=35
  paths_fail=1`), 05:37:59 (`lines=37 pass=37`), 05:39:19 (`lines=37 pass=37 pass_strict=37`); the
  instrument digest `d07af435…` → `4475d2e6…` (05:34:28) → `1ccee066…` (05:39). The draft states the
  final measured line **and** publishes the drift as a limit. If the instrument or the receipt moves
  again, that bullet needs the last numbers, not mine.
- **D24-3's fresh measurement is not committed.** `RevBound8.md` §3 measured the mutant on the landed
  bytes (`88122e10…`: dispatch 8/8 exit 0, containment 24/24 exit 0, `many10` INTERNAL→GONE), but its
  receipts live in `/tmp/kasegi-r25-bound8/`. The draft cites the seat report, not a committed receipt.
- **D24-2 residuals are still 77.** `SCORECARD.md:510` ("19 records, 77 assertions") and
  `corpus/lessons/round-24.md:77` ("19 records / 77 assertions") still read 77 at 05:39. The draft says
  the same figure replaces them (list: `InstrumentsCounts.md` §d) — the L1 must land that edit or soften
  the sentence.
- **D24-3 residuals.** `SCORECARD.md:499-501` still prints the old "8/8 … 24/24 … (`ResolverAttack`
  receipt, wave 1)" sentence; `corpus/QUALITY.md:65` (R11) has been corrected but now says an `8/8` on
  the landed bytes "is an inference, not a lane measurement", which `RevBound8`'s run has since
  overtaken. Two artefacts, two different truths — L1's call, with `RevBound8.md` §5 as the list.
- **D24-4's sentence has no home yet.** `corpus/lessons/round-25.md` does not exist (05:40); the draft
  says the sentence lands there and cites the receipt I read plus `RevL4Reconcile.md` §3.
- **C2's after-state is now landed (measured 05:41).** Frontier is 10, the registry 40 rows, both
  entries cite S036+, and the census validates exit 0. The draft still carries `{{CENSUS}}` for the
  L1's own append, per the task; the measured substitute string is
  `exit 0, rows 40, malformed 0, tier A=37 B=1 C=2, status mined=28 queued=9 rejected=3, W04 ×2
  (S028, S029 pre-existing)` — `sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi`
  prints `rows 40 / tier.A 37 / tier.B 1 / tier.C 2 / status.mined 28 / status.queued 9 /
  status.rejected 3`, and `validate` prints the file `ok` plus the two W04 lines, exit 0. If any further
  row lands, re-run both.
- **Seat-reported, not re-measured by me:** the `git diff` shape per file beyond the `1 1` counts (the
  counts I did measure), the collision-guard fixture proof, and every quote/line anchor inside the two
  new entries (the two files exist, their headers name S036–S039 and S040; I did not audit the quotes).

## 4. Conflicts and findings for the canonical judge

1. **`claims.json` planned reject is falsified by the capture log.**
   `assimilation.planned_reject` = "vendor-cvd-policy-crosswalk-2026-10-23.md (S068 Cisco policy
   unreachable this round)", while `.ufo/waves/round-25/capture-log.txt` records
   `S040 status=200 fetched_bytes=94027 … sha256=b7f7b55f… utc=2026-10-25T08:14:28Z`. The draft files
   the Q3 refusal instead (`the two conditions` vs four bullets at S040 `L301`, `L302`, `L305`, `L308`)
   and says the reachability reason is not filed.
2. **Frozen counter instrument moved after the freeze.** Digest `d07af435…` (the value
   `c1-instrument-digest.txt` pins, and the bytes that produced the before-receipt) is no longer on
   disk; the file is `1ccee066…` (13037 → current bytes, mtime 05:39). The before-receipt cannot be
   re-derived from the current instrument; before and after are therefore two instruments' verdicts on
   one predicate, and the frozen limbs (a)–(c) are unchanged only in their source form.
3. **Two entries share three sources under one frontier row.** `lesson-mistakes.md` measures overlap
   S036/S038/S039 under F10 and asks for a decision (one object per document set, or a declared division
   of labour). The draft's C2 bullet lists both entries and does not decide; the L1 must, before F10's
   entry column is written.
4. **Manifest quote count disagreement.** `lesson-mistakes.md` says the round-25 manifest holds "5
   records, 33 quotes"; the manifest on disk holds 5 records, **42** quotes (`sum(len(s['quotes']))`,
   measured 05:40). The draft carries 42.
5. **The staged package vanished mid-session.** `/home/vgpnk/Projects/shukuknow/merge/kasegi` was
   listable at 05:26 (I read `MERGE-REPORT.md`/`SOURCES.append.md` metadata) and returned "No such file
   or directory" at 05:33 and after; the seats that read it (`CritC2Scope`, `CollisionGuard`,
   `RowsScratch`) did so earlier. I wrote nothing there — `shukuknow` is read-only to this seat. The
   draft cites the package path as `claims.json` records it.
6. **D24-1 is closed by construction, not by measurement.** The draft's D24-1 line asserts only that
   this entry and the report cite `{{LANE_HEAD}}`; the L1 must actually fill it with the HEAD at write
   time and name the paths each cited commit carries, or D24-1 reopens.

## 5. Shape notes (why the draft reads the way it does)

- Heading form follows the task (`## Round 25 — …`), with the date kept inside it as the three most
  recent entries do (`## 2026-10-25 — round 24 …`).
- Bullets are bold-led like the round-23/24 entries; each claim bullet carries its counter command
  verbatim from `claims.json`, so the L1 can re-run rather than trust.
- The two C1 limits are one bullet, not a second claim: they are the honest boundary of the C1 figure,
  in the same register as the round-24 "known blind spot (R11, published not hidden)" text.
- No `##` sub-headings were added inside the entry; the lane's recent entries use bullets only.

## 6. Files

- Written: `.ufo/waves/round-25/wave1/log-entry.md` (the draft).
- Written: `.ufo/waves/round-25/wave1/LogDraft.md` (this report).
- Read only, elsewhere: `LOG.md:1114-1244`, `.ufo/waves/round-25/{claims.json,c1-before.txt,c1-before.json,c1-after.json,c1-instrument-digest.txt,capture-log.txt,wave1-spec.json,wave1-dispatch.json}`, `.ufo/waves/round-25/wave1/*.md` (16 seat reports at read time), `.ufo/waves/round-25/assimilation/ids/*`, `assimilation/rows/*`, `corpus/lessons/round-24-verifier-spotcheck.md`, `corpus/knowledge/*.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/instruments/README.md`, `SCORECARD.md`, `PROVINCE.md`, `.ufo/waves/round-24/c1-control-baseline.txt`.
