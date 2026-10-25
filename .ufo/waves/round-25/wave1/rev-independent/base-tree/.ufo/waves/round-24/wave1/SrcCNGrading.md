# SrcCNGrading — province-fit and reachability probe: three standards-body grading entries

Seat: scout (read-only). Item: probe `chinese-national-grading-model.md`,
`gb30279-2020-edition-provenance.md`, `cnnvd-grading-specification-primary.md` under
`/home/vgpnk/Projects/shokuknow/merge/kasegi/knowledge/corpus/knowledge/` for province fit,
primary reachability, and the QUALITY criterion each would most likely fail.
Lane base `d0a3f6a4643fc5f668e95d94fcdbe22830bb8f9a` (ancestor of `master` `c2480b1`).
Date: 2026-10-25. No production file, lane tree, git/jj state, fleet file or shokuknow byte was
written; no subagent dispatch. Probes were status-only `curl` reads of public documents.

## Findings first

1. **None of the three governs a surface PROVINCE.md claims.** All three sit on the
   *upstream standards layer* — a national standard (GB/T 30279—2020 and its 2026 revision), that
   standard's edition provenance, and CNNVD's own four-band specification — and none states a
   bounty-program rule, an asset scope, a triage gate, a claim-package rule, or a disclosure
   packaging rule. Advisory verdict: **adjacent, not core**; see §(a) per entry.
2. **One of the four cited primaries is dead as written.** `std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3`
   (S048, `chinese-national-grading-model.md:5`) answers **404 on HEAD and 404 on GET** (748-byte
   HTML error page, two attempts). The same plan record is live under a *different* id in the same
   package: S091's `gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3` answers GET **200, 98393 bytes**.
   The other three primaries (S047 PDF, S096 record, S099 PDF) are reachable; full table §(b).
3. **Two of the three entries have no H1 at all.** `gb30279-2020-edition-provenance.md` and
   `cnnvd-grading-specification-primary.md` begin, byte for byte, with an empty line 1 and
   `source:` on line 2 (`cat -A` verified). Both therefore fail QUALITY Q1's "opens, directly under
   its H1 title" clause as packaged, before any judgment about their content. The same two are the
   only ones whose `title` column in `MERGE-REPORT.md` is the file path itself — the title was lost
   in packaging, not written missing.
4. **All three `recheck:` fields are unexecutable in the Q7 sense.** `gb30279-…:4` and
   `cnnvd-…:4` are pure prose ("re-open the plan record and confirm … (ran 2026-10-24)") with no
   command at all; `chinese-national-grading-model.md:7` is a `curl` **without `-f`** followed by a
   human "then confirm" clause — on the now-404 URL curl writes the error page and does not fail
   (`curl --help all`: "`-f, --fail` Fail fast with no output on HTTP errors"), so the command half
   passes silently and only the human half could catch a dead source.
5. **The `ground:` fields are orphans in this lane.** `chinese-national-grading-model.md:8` cites
   `F14`; the lane's frontier table tops out at F08 admitted (F09 is this round's target) and
   `grep -rn '\bF14\b' corpus/` finds nothing. `gb30279-…:5` and `cnnvd-…:5` cite "round-8 ledger
   item 5/1"; `grep -rn 'ledger item' corpus/` returns **0 hits** — `corpus/lessons/round-8.md:19`
   mentions only `ledger/candidates.jsonl` run_ids, not item numbering. These `ground:` values
   belong to the package stager's rounds, not to the lane's round-8 lesson.
6. **The S-ids are staged, not registered.** Lane `corpus/SOURCES.md` holds 31 rows (S001–S031);
   `.ufo/waves/round-24/assimilation/staged-ids` holds 94 ids S031–S124 with only S031 colliding.
   So S047/S048/S096/S099 would append unchanged *if* the SOURCESRows append lands — but at base a
   `source: S###` citation resolves to no lane row, which is a hard Q1 miss until that append exists.
7. **Package arithmetic discrepancy, one line deep:** `MERGE-REPORT.md:9` says "lane registry
   currently holds **30** rows"; `.ufo/waves/round-24/assimilation/reg-ids` has **31** lines
   (S001–S031). The staged-id start (S031) collides with the lane's existing S031
   (`cna-assignment-and-vulnerability-rules.md`), which the package's own "first staged id is S031"
   line does not acknowledge.

## (a) Province fit, per entry

PROVINCE.md claims, at `PROVINCE.md:29`, that "the line-3 domain comprises program rules, scopes,
and claim packages; the core also covers triage and claim gates, and submission/disclosure
packaging", and at `PROVINCE.md:37` indexes under Frontier only "General practice that governs every
program". Test applied: does the entry state a rule that a bounty program, a scope decision, a
triage gate or a claim package must obey, or that governs every program?

**`chinese-national-grading-model.md` — no (adjacent).**
It governs GB/T 30279—2020 as applied by JR/T 0276—2023 (a securities/futures *sector regulator's*
penetration-testing standard) plus revision plan 20260806-T-469. Every load-bearing sentence is a
standards fact: the three indicator classes and 1–9 scales, the two grading results, the revision's
change list, the drafting-unit list. Its own frame is comparative and forward-looking —
"the live signal to watch is the 修订计划 line on the project page" (`:52-53`) — i.e. a standard-revision
watch. A rule that binds Chinese regulated entities is not "general practice that governs every
program" (`PROVINCE.md:37`). The nearest *core* artifact is the package's
`chinese-program-severity-instrument.md` (round2), which is about a programme's instrument; this
entry is its upstream source material, not a topic in its own right. **Advisory: do not admit as an
independent Frontier topic; at most re-ground support inside a program-facing entry.**

**`gb30279-2020-edition-provenance.md` — no (adjacent).**
Content is standards-process history: plan 20190906-T-469, 24-month cycle, 2019-01-03..2019-01-18
comment window, the 2013+2017 merge scope. Its own "Kasegi use" (`:19-26`) is about *how the lane
should quote a 2020-era grading*, and its `### Limits` says the record carries no draft, no
disposition, no annex text. Zero program, scope, triage or claim content. **Advisory: refuse.**

**`cnnvd-grading-specification-primary.md` — no (adjacent).**
CNNVD is a national vulnerability database; the entry's rule is that database's 10-point/four-band
cut-point table. Its own use (`:30-37`) is notation discipline — which boundary notation the lane
should quote. No program rule, no scope, no claim rule. **Advisory: refuse** (at most upstream
vocabulary for a severity-vocabulary entry, and the entry itself concedes the source is a
third-party mirror of a retired page, tier B).

For all three the honest route to core would be an operator re-scope of PROVINCE.md, which the lane
has twice recorded it will not do itself (`PROVINCE.md:5-23`, "re-scope remains the operator's
decision"). None of the three appears in `claims.json` `assimilation.candidates_admit` (that list is
`authorised-testing-rules-of-engagement.md` and `statutory-authorization-in-three-traditions.md`),
so refusing them moves neither C2 counter.

## (b) Reachability, per cited primary

Status-only probes, 2026-10-25; per URL one HEAD then one GET (max 2 attempts), `--max-time 20`,
`-L`, browser UA on GET. No body was opened, so anchor presence is UNVERIFIED (§Remaining unknowns).

| entry | row | URL | attempt 1 (HEAD) | attempt 2 (GET) | verdict |
|---|---|---|---|---|---|
| chinese-national-grading-model.md:4 | S047 | `https://www.sse.com.cn/lawandrules/regulations/csrcannoun/c/10117011/files/028395e1b8364d3bb3fcb28d565de306.pdf` | 200, t=5.38s | 200, bytes=300207, `application/pdf`, t=10.51s | reachable |
| chinese-national-grading-model.md:5 | S048 | `https://std.samr.gov.cn/gb/search/gbDetailed?id=3B865A9398AA6160E06397BE0A0A52F3` | **404** | **404**, bytes=748, `text/html;charset=utf-8` | **NOT reachable as cited** |
| gb30279-2020-edition-provenance.md:2 | S096 | `https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=7236A1438F85571FE05397BE0A0A1552` | 200, t=1.07s | 200, bytes=31099, `text/html;UTF-8` | reachable |
| cnnvd-grading-specification-primary.md:2 | S099 | `https://raw.githubusercontent.com/y4ney/collect-cnnvd-vuln/main/doc/pdf/CNNVD%E6%BC%8F%E6%B4%9E%E5%88%86%E7%BA%A7%E8%A7%84%E8%8C%83.pdf` | 200 | 200, bytes=1293152, `application/octet-stream`, t=0.04s | reachable |

Control that localises the S048 failure to the id, not the host: S091's row in
`/home/vgpnk/Projects/shokuknow/merge/kasegi/SOURCES.append.md:67` points at
`https://std.samr.gov.cn/gb/search/gbDetailed?id=4C30E22D8B94BBB9E06397BE0A0A52F3` for the *same*
plan 20260806-T-469 and returns **GET 200, bytes=98393**. So the `gbDetailed` endpoint is alive and
the 3B865A… id is stale/incorrect. Consequence: `chinese-national-grading-model.md:7`'s recheck
target and the file's own stated watch signal ("the live signal to watch is the 修订计划 line on the
project page") both point at a dead URL. Fixing it is a *source-row* correction, not an entry edit —
QUALITY R8 makes a corrected anchor a new "supersedes S### —" row.

## (c) QUALITY criterion each would most likely fail

**`chinese-national-grading-model.md` → Q7** (`QUALITY.md:48`).
`:7` = `180d — `curl -sSL '<url>'` then confirm the 修订计划 line still reads 20260806-T-469
正在征求意见 (ran 2026-10-23)`. Four ways it fails Q7: (i) the executable half is a bare
`curl -sSL` with no `-f` and no output assertion, so a 404 page (observed: 748 bytes) is written and
the command still exits 0; (ii) the assertion lives in a human "then confirm" clause, so no output
"names what was checked"; (iii) its one URL is the S048 id that now 404s; (iv) S047 — the entry's
first source — carries no recheck at all, so half the entry is unrechecked. Co-failing:
**Q5** (`QUALITY.md:18`) — the file has only `## The claim` (`:10`) and `## Why it matters` (`:47`),
i.e. no rejected over-generalization and no explicit rejection with a reason; and its "rule" is a
standards fact, not a rule a reader can check against a report or claim package.
Partial: **Q1** — four header lines of which two are `source:` and only one is `recheck:`.

**`gb30279-2020-edition-provenance.md` → Q1** (`QUALITY.md:14`).
Byte-verified: line 1 empty, line 2 `source: S096 …`; the first heading in the file is `### Rule`
at `:7`. There is no H1, so the entry cannot "open directly under its H1 title, with three header
lines"; its title exists only in `MERGE-REPORT.md:58` (and there as the path, not a title).
Second Q1 defect: `:5` `ground: round-8 ledger item 5` names an artifact the lane does not hold
(§Findings 5). Third: S096 is staged, not registered at base (§Findings 6). Co-failing: **Q7** —
`:4` is prose with no command.

**`cnnvd-grading-specification-primary.md` → Q1** (`QUALITY.md:14`).
Same missing-H1 defect (line 1 empty, line 2 `source: S099`, first heading `### Rule` at `:7`).
Additionally its tier claim has no row to live on: `:43` says "this row's tier is B rather than
A", but S099 is staged and `corpus/SOURCES.md` has no S099 row, so the tier is asserted in the entry
instead of carried by the row (R8 keeps immutable fields in the row). Co-failing: **Q7** — `:4` is
prose with no command. Q2 itself would pass *if* the row existed with tier B, since B is permitted
as sole support and C is the only barred tier.

## (d) What this changes for the lane

- Nothing in this report asks for a production edit. All three verdicts are advisory; L1 decides.
- If L1 admits any of them, the ordering that costs least is: (1) register the staged rows (SOURCESRows
  append, which also has to resolve the S031 collision); (2) restore the H1 for the two title-lost
  files (packaging defect, no claim changes); (3) replace the two prose rechecks and the broken
  `curl` with a `corpus/instruments/source-recheck.py` invocation in the house form
  (`corpus/knowledge/authorization-safe-harbor-and-scope.md:4`); (4) re-point S048 at the live id via
  a supersedes row, not an in-place edit. Step (4) alone is the difference between a recheck that
  can pass and one that cannot, and it is not decidable by an entry edit.
- Refusing all three leaves C2 untouched (§(a)) and costs nothing on either axis; admitting them as
  Frontier topics would require an operator re-scope of `PROVINCE.md:29-37` and would inflate the
  frontier denominator with standards-watch material rather than program practice.

## Confidence

High on: province fit (§(a)) — read from the entries' own framing sentences and PROVINCE's own
claim text; the four HTTP outcomes (§(b)) — each reproduced on a second attempt; the missing H1
(byte-level `cat -A`); the recheck prose (§(c)); the orphan `ground:` values (0-hit greps in the lane);
the staged-vs-registered id split (registry row count and `staged-ids`).
Medium on: the Q7-over-Q5 ordering for `chinese-national-grading-model.md` — both fail on their face;
I rank Q7 first because it is the criterion the round's own routed defect class names, and Q5 second.
Medium on: the S048 404 being permanent rather than a session/geo artefact — argued only by the live
S091 sibling id on the same endpoint.

## Remaining unknowns

- **UNVERIFIED:** anchor presence inside the three reachable bodies. Probes were status-only, so I did
  not confirm that the S047 PDF still contains 附录A A.1–A.7 at the cited location, that S096's page
  still prints "计划号 20190906-T-469" and the 公示 dates, or that S099's archive still contains
  "CNNVD将漏洞的危害级别划分为四个等级". Blocked by the item's status-only instruction, not by the source.
- **UNVERIFIED:** whether the S048 id ever resolved, or was mistyped at package build. Not answerable
  from bytes I may read.
- **UNVERIFIED:** whether any bounty program in the lost tree ever adopted GB/T 30279 or CNNVD banding
  as its own severity rule — which is the only route by which these entries could become core. The tree
  is absent (`corpus/knowledge/root-loss-2026-10-12.md`), so the question is not answerable this round.
- Not probed beyond one browser UA and `-L`: no cookie/session, no Referer, no retry loop after 404
  (the per-URL attempt cap was 2 and was used).

## Tooling

No installs, no upgrades; no package manager was touched (pacman paused host-wide).
