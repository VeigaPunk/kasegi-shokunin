# ConnTrends — round-35 trend→evidence map (kasegi)

Seat: `ConnTrends` (connector, L2 leaf, wave 1, round 35). Skill: godspeed (axes named per trend below).
Lane: `kasegi-shokunin`; lane base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims freeze
`617496b9c6e92bc671e7e78b83df69a04470d0e9`; wave-1 spec/dispatch `da2d3c687f82a9814ee71c91c930cb733050d37c`.

**Assignment.** Map the three learning trends to the round's evidence and produce the evidence table
the report's `## Trend verdicts` section will cite. Verdicts are the L1's; this seat decides nothing.
Axes named: expansion → `coverage`; quality → `depth:verifiability`; discernment → both
(lesson-backed criteria are quality surface; gate decisions are coverage surface).

**Method.** Read-only over the live working tree plus the frozen base `617496b9` (via `git show` /
`git archive` receipts of sibling seats). Every measurement below was taken by this seat at
2026-10-26T06:41–06:45Z unless a receipt is named. No product file was written; no subagents; no
`agent://all`; no git/jj mutation; no installs (pacman paused; nothing needed). No scratch tree was
created — every command ran read-only in the lane — so there is nothing to delete
(`test -e /fast/scratch/hyaku/kasegi-r35/ConnTrends` → absent, verified at exit).

---

## The evidence table (for `## Trend verdicts`)

Row status legend: **landed-wt** = present in the working tree at measurement time (uncommitted,
the L1 commits); **pending** = not yet in the tree, owner named; **committed** = in a landed commit.

### Trend 1 — expansion

| # | evidence item | measured value (2026-10-26 ~06:45Z) | named location | status |
|---|---|---|---|---|
| E1 | Frontier admission count | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **18** (base `617496b9` → 17; first read this seat 17, second read 18 — a sibling seat landed the amendment between reads) | `corpus/README.md:388` (F18 row), amendment § `Round-35 admission` at `:369` | landed-wt |
| E2 | F18 row shape | "CISA Known Exploited Vulnerabilities catalog — exploitation-status-based prioritization distinct from CVSS severity \| admitted \| knowledge/cisa-kev-catalog.md \| S052" | `corpus/README.md:388` | landed-wt |
| E3 | Coverage-map ground was uncovered | The appended round-35 coverage-map row is a **new area**: "Known-exploited-vulnerabilities prioritization (round 35)"; the mining sweep asked "does the lane already hold a known-exploited-vulnerabilities prioritization source … beyond the severity ground the registry already holds (S001, S015, S043–S047, S051)" and measured `known exploited 0 files / 0 hits` in the corpus (`KEV` only as a quoted CWE Top-25 cell, `corpus/lessons/round-22.md:91`) | `corpus/README.md:380-382` (map row); `.ufo/waves/round-35/wave1/ScribeSearchLog.md:149` (sweep question), `:78` (0/0 table) | landed-wt |
| E4 | Registry row S052 | `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|'` → **1**; row fields: kind `dataset`, tier `A`, status `mined`, opened `2026-10-26`, used-by `corpus/knowledge/cisa-kev-catalog.md`; registry total 51 → **52** | `corpus/SOURCES.md:58` | landed-wt |
| E5 | Entry citing mined S052 | `grep -lE '^source: S052 ' corpus/knowledge/*.md` → **1** file; header line: `source: S052 — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json — capture corpus/source-snapshots/round-35/S052.txt …`; `ground: F18`; `verified-at: 2026-10-26` | `corpus/knowledge/cisa-kev-catalog.md:3-5` (sha256 `09888666…`) | landed-wt |
| E6 | Harness | `python3 corpus/instruments/frontier-recheck-count.py` → `entries=21 pass=21 exit=0` incl. `PASS     F18  knowledge/cisa-kev-catalog.md … ids=S052           exit=0` (first read this seat: `entries=20 pass=20` — raced the README landing; final read 21/21) | harness output; entry per `corpus/instruments/knowledge-expected.txt` (+`cisa-kev-catalog.md`, git diff) | landed-wt |
| E7 | Source-recheck S052 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` → `sha256 OK`, Q1–Q5 each `occurrences=1` (Q3–Q5 `normalized=markup-whitespace` per Q8), **exit 0** | instrument output; manifest sha256 `06bfcc71…`; capture sha256 `d69349e8…` | landed-wt |
| E8 | Census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → `W04 S028`, `W04 S029`, `kasegi ok`, **exit 0** | output quoted; matches claims "W04 S028/S029 only" | landed-wt (read-only run) |
| E9 | Junk F18 twin rejected | twin's two fabricated sentences occur **0 / 0** times in the pinned capture (`grep -c` both → 0, exit 1); non-author reviewer rejected "proven independently" (`RevC2BeforeAfter.md` §3); twin not admitted — no `junk` file under `corpus/knowledge/` | `.ufo/waves/round-35/c2-controls/junk-f18.md` (sha256 `0abec359…`, committed at freeze); `.ufo/waves/round-35/wave1/RevC2BeforeAfter.md:89-107` | committed twin + landed-wt rejection evidence; do-nothing receipt `ExecDoNothingReject.md` **pending** (seat still running) |
| E10 | Capability rows | **none.** Master `## Capabilities` table last entry round 33; round-34 section records "Capabilities: no row enters this round"; no round-35 capability row is claimed anywhere in the frozen claims or the wave receipts | `SCORECARD.md:301` (table), `:1222` (round-34 sentence) | none (expected) |

### Trend 2 — quality

| # | evidence item | measured value (2026-10-26 ~06:45Z) | named location | status |
|---|---|---|---|---|
| Q1 | Closure suite existence | `corpus/instruments/r35-defect-closure.sh` present (832-line class instrument; sha256 `a4f80067…`); fixtures `corpus/instruments/r35-fixtures/` | instrument + fixtures dir | landed-wt |
| Q2 | Suite live run | `closed=4/7 exit=1` — D1 `placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0`; D2 `erratum-row=1,erratum-mean=2,row-bytes=1 open=0`; D3 `registry-r-defect-closure=4,registry-kill-rule=4 open=0`; D5 `erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0`; **D4 `tracked=0,provenance=1 open=1`; D6 `dead-seat-sentence=1,correction-round-35=0 open=1`; D7 `supersedes-R22=0,supersedes-R23=0 open=1`** | suite stdout, run twice by this seat (identical) | partial — 4/7 closed in wt |
| Q3 | Suite selftest | `--selftest` → `cases=7 failures=3` (the 3 failures are exactly D4/D6/D7 live-open cases, consistent with Q2); forgery judges: `forged-summary`, `forged-caselines`, `short-report`, `fake-suite` (path `.ufo/waves/round-35/c1-controls/fake-suite.sh`), `fake-plain` → **all `rejected=1`** | suite stdout; do-nothing control committed at freeze (`292aaac0…`) | landed-wt; `cases=7 failures=0` is **pending** on D4/D6/D7 landing |
| Q4 | Fail-closed direction | every D-check's selftest fixture prints its defect-open payload (e.g. `D1 fixture reason=placeholders=1,…`); per-defect mutants flip back to open (e.g. `D5 mutant=discriminating-invocation reason=…discriminating-invocation=0…`); base-tree values are the claims' `before` list (suite absent `ls_exit=2`, D1 1/0, D2 2/0, D3 0, D4 0/0, D5 0, D6 1, D7 0 0) | suite `--selftest` detail lines; `.ufo/waves/round-35/wave1/ExecBeforeReceipts.md`; `.ufo/waves/round-35/wave1/MutCounterBase.md` (C2 probes on `git archive 617496b9`: every AFTER value unreachable on base bytes) | landed-wt |
| Q5 | recheck-audit | `python3 corpus/instruments/recheck-audit.py --quiet` → `strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0`; `lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0` | instrument output, run by this seat | landed (read-only instrument over current tree) |
| Q6 | No admitted entry failed re-check | harness `entries=21 pass=21` — zero FAIL lines, F18 included (E6) | harness output | landed-wt |
| Q7 | D1 landing | `grep -c 'filled by the L1' SCORECARD.md` → **0**; correction names `c1c6a5f826d2425446347173de527c42991b78b0` ×3 | `SCORECARD.md:1130`, `:1241`, `:1259` | landed-wt |
| Q8 | D2 landing | appended erratum names mean **201.2** with byte-bound measurement state (`git show 206e510:SKILL.md` … vs `git show 3266c99…:SKILL.md …`) | `SCORECARD.md:1246-1257` | landed-wt |
| Q9 | D3 landing | `SKILL.md` Gates & probes registry rows name both instruments (grep hits at `:1097-1098` region, "Round-34 Gates & probes registry addition" block) | `SKILL.md:1097-1104` | landed-wt |
| Q10 | D4 in flight | `.ufo/waves/round-34/wave1-results.json` (312874 B class) + `.ufo/waves/round-34/wave1-results.json.provenance.md` written; suite reads `tracked=0` because the file is untracked — closes only when the L1 commits it (per D4's own fix text and the M35-1 candidate: quiesce before the final commit) | provenance note head (filed by `ExecD4ResultsTrack` ~06:32Z); suite D4 payload | pending — L1 commit |
| Q11 | D5 landing | `.ufo/waves/round-35/claims-erratum-d5.md` present (sha256 `eee0bb57…`); suite reads `discriminating-invocation=5,per-id-occurrences=5`; the erratum restates the round-34 frozen clauses with invocations run against committed bytes | `.ufo/waves/round-35/claims-erratum-d5.md:1-30`; `.ufo/waves/round-35/wave1/ScribeErratumD5.md` | landed-wt |
| Q12 | D6 pending | stale sentence still present: "The round-33 summary `ExecRegressionC1` did not file a receipt (dead seat, 1 of 65)" in round-34's `L1Integration.md`; suite `correction-round-35=0` | `.ufo/waves/round-34/wave1/L1Integration.md:30` (Notes bullet) | pending — no seat owns it yet in wave1 |
| Q13 | D7 ready, unapplied | `ScribeQualityDraft.md` §1 block (21 lines / 2842 bytes, sha256 `e3aa99a1…`) flips D7 on a copy: `supersedes-R22=1,supersedes-R23=1 open=0`; filtering the two row lines flips back — measured by that seat, values quoted verbatim | `.ufo/waves/round-35/wave1/ScribeQualityDraft.md:1-45` | pending — L1 applies |

### Trend 3 — discernment

| # | evidence item | measured value | named location | status |
|---|---|---|---|---|
| D1 | Round-34 precedent: gate vs non-author spot-check | spot-check §4 re-opened all 5 gate decisions: 1 admit (F17/S051) + 4 rejects/refusals → **agree ×5**; the one dispute (junk-twin wording vs fact) was ruled "wording is a defect (D5). It does not falsify C2" — disagreement became an erratum, not a silent waiver | `corpus/lessons/round-34-verifier-spotcheck.md:130-136` (§4), `:96-108` (§2 D5 ruling) | committed |
| D2 | Disagreement → lesson-backed criterion (lineage) | M34-1 ("all mutants killed" overstatement) → **R24**; M34-3 (`records=40` freeze-satisfiability) → **R25**; both criteria rows present in the bar | `corpus/QUALITY.md:226-229`; `.ufo/waves/round-34/mistakes-erratum-1.md:9-29` (M34-3 minted); `corpus/lessons/round-34.md:238-310` (M34 rows) | committed |
| D3 | Round-35 gate decisions on record | assimilation Gate: quarantine slice re-derived (7 register rows, four-label verdicts), standing refusals re-confirmed (no staged entry with fully-met flips), admit leg met by the C2 F18/S052 admission — **"Assimilation: none adopted"** (0 adopted of the slice) | `.ufo/waves/round-35/wave1/ScribeGateAssimilation.md:207` (§4), `:96-108` (verdict table) | landed-wt (receipt) |
| D4 | F18 admission gate discrimination | junk twin (E9) rejected independently by a non-author reviewer; the admission gate is exercised against a same-shape fabrication, not just welcomed | `.ufo/waves/round-35/wave1/RevC2BeforeAfter.md:89-107` | landed-wt (receipt) |
| D5 | Live disagreement candidate #1 → lesson path | `ScoutDatawalk` F-4: the round-35 C2 junk-twin kill clause repeats the D5 class — the twin's `recheck:` line is byte-identical in form to the real entry's, so "source-recheck exit != 0" is non-discriminating **as written** once the real manifest lands (same finding class as round-34 D5, `round-34-verifier-spotcheck.md:103-107`). Whether it becomes an erratum/criterion is the L1's call; the receipt names the exact clause | `.ufo/waves/round-35/wave1/ScoutDatawalk.md:73` | landed-wt (receipt) — round-35 lesson not yet written |
| D6 | Live disagreement candidate #2 → erratum-class correction | `ScribeGateAssimilation` §1a/2: correction to round-34's Gate table **verdict classes** (UA-vs-fetch verdicts; `present-and-located` for S068/S069/S070) recorded "as an erratum-class note, not a rewrite" — R8/R9 discipline on a filed gate table; the round-34 disposition (0 adopted) stands | `.ufo/waves/round-35/wave1/ScribeGateAssimilation.md:120-132`, `:469` | landed-wt (receipt) |
| D7 | Distance-to-next-score criterion mined (R26) | `considerthese/2026-10-25.md:53-57` proposal 2 ("Track 'distance to the next score', not just 'improved, held'") → drafted bar row **R26** (with the D7 supersedes-R22 correction in the same block per the dispatch's allowance); live figure measured: `python3 corpus/instruments/score-gap.py` exit 0 → `gap: 24 of 46 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims` (threshold `SCORECARD.md:331`) | `considerthese/2026-10-25.md:53-57`; `.ufo/waves/round-35/wave1/ScribeQualityDraft.md` §1 (R26 row), F7; `.ufo/waves/round-35/wave1/ExecScoreGap.md:215-216` | landed-wt (receipts); QUALITY row pending L1 apply |
| D8 | Mistake mint pending (M35-1+) | claims name M35-1 candidate: round-34 D4 class "landing/closure-order" — wave writes landed after the `complete` line; fix = commit results with provenance + quiesce before final commit; "Further M35 rows minted from wave receipts in the lesson" — the round-35 lesson does not exist yet (`ls corpus/lessons/ | grep round-35` → absent) | `.ufo/waves/round-35/claims.json` → `non_claim_frontier_items.mistake` | pending — L1 lesson |

**Cross-trend contradictions to keep visible for the verdict writer (not smoothed):**
- C1's frozen after-state says `closed=7/7` / `cases=7 failures=0`; the tree at measurement holds
  `closed=4/7` / `failures=3` with D4/D6/D7 open and named owners (Q10/Q12/Q13). The quality trend
  evidence is **directionally complete but numerically pending** — the verdict line must read the
  suite at integration time, not this snapshot.
- C2's frozen harness count `entries=21 pass=21` raced this seat's first read (`20/20`) and held on
  the second (`21/21` incl. `PASS F18 ids=S052`). The README amendment is the load-bearing landing
  for both the frontier counter and the harness's F18 discovery.
- E9's twin-rejection receipt (`ExecDoNothingReject.md`) is still being written by a live seat; the
  rejection fact itself is already independently evidenced (`RevC2BeforeAfter.md` §3 + 0/0 capture
  occurrences measured by this seat).

---

## Report

### Commands and outcomes (all read-only; run 2026-10-26T06:41–06:45Z, cwd = lane root)

1. `bash corpus/instruments/r35-defect-closure.sh` → exit **1**;
   `D1 … open=0 / D2 … open=0 / D3 … open=0 / D4 … open=1 / D5 … open=0 / D6 … open=1 / D7 … open=1`,
   `closed=4/7 exit=1` (payloads in table row Q2; run twice, identical).
2. `bash corpus/instruments/r35-defect-closure.sh --selftest` → exit **1**;
   `selftest cases=7 failures=3` (live fails = D4/D6/D7), controls `clean closed=7/7 verdict=pass`,
   `two-defect closed=5/7 failed=D1,D2 verdict=pass`, and five judge lines
   `judge=forged-summary|forged-caselines|short-report|fake-suite|fake-plain rejected=1`.
3. `python3 corpus/instruments/frontier-recheck-count.py` → first run exit 0 `entries=20 pass=20`;
   second run (after the README amendment landed) exit 0 `entries=21 pass=21 exit=0` with
   `PASS     F18  knowledge/cisa-kev-catalog.md … ids=S052           exit=0`.
4. `python3 corpus/instruments/recheck-audit.py --quiet` → exit **0**;
   `strict pass=47/47 cdroot_fail=0 instrument_fail=0 own_fail=0`;
   `lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0`.
5. `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052` → exit **0**; `S052:sha256 OK`; Q1–Q5 `OK occurrences=1` (Q3–Q5 `normalized=markup-whitespace`), anchors `2-ok, 3-ok, 4-ok, 15472-ok, 19165-ok`.
6. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → exit **0**; `W04 S028 …`, `W04 S029 …`, `kasegi ok …/corpus/SOURCES.md`.
7. `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **18** (and `git show 617496b9:corpus/README.md | grep -cE …` → **17**).
8. `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **52**; `grep -cE '^\|[[:space:]]*S052[[:space:]]*\|` → **1** (row at `:58`: kind `dataset`, tier `A`, status `mined`, opened `2026-10-26`).
9. `grep -lE '^source: S052 ' corpus/knowledge/*.md | wc -l` → **1** (`corpus/knowledge/cisa-kev-catalog.md`); `ls corpus/knowledge/*.md | wc -l` → **47**.
10. `grep -c 'filled by the L1' SCORECARD.md` → **0**; `grep -n 'c1c6a5f' SCORECARD.md` → `:1130, :1241, :1259`; `grep -n '201\.2' SCORECARD.md` → `:1246, :1250` (erratum + byte-bound measurement state `:1247-1257`).
11. `grep -c 'five exploited vulnerabilities to the catalog every Tuesday' corpus/source-snapshots/round-35/S052.txt` → **0** (exit 1); `grep -c 'scores each entry with a CVSS v4 vector' …` → **0** (exit 1) — the twin's fabricated strings are absent from the pinned capture.
12. `grep -nE '^\| R2[2-6] \|' corpus/QUALITY.md` (via `ScribeQualityDraft.md:3` command echo) — R22–R25 present, no R26/R27 yet; D7 payload `supersedes-R22=0,supersedes-R23=0 open=1` (command 1).
13. `sed -n '25,35p' .ufo/waves/round-34/wave1/L1Integration.md` — stale sentence "did not file a receipt (dead seat, 1 of 65)" present (D6 open, correction-round-35=0).
14. `git status --porcelain` → modified: `SCORECARD.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/instruments/knowledge-expected.txt`, `.ufo/waves/round-35/build-spec.py`; untracked incl. `.ufo/waves/round-34/wave1-results.json{,.provenance.md}`, `corpus/knowledge/cisa-kev-catalog.md`, `corpus/instruments/r35-defect-closure.sh`, `corpus/source-snapshots/round-35/`, `.ufo/waves/round-35/wave1/`. No git/jj mutation by this seat.
15. `test -e /fast/scratch/hyaku/kasegi-r35/ConnTrends` → absent (no scratch created; nothing to delete).

### File digests (sha256, at read time)

| path | sha256 |
|---|---|
| `corpus/README.md` (wt, +28) | `277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2` |
| `corpus/SOURCES.md` (wt) | `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba` |
| `SCORECARD.md` (wt) | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` |
| `corpus/knowledge/cisa-kev-catalog.md` | `0988866608c4a1818219e02bbb23cd1d7aeffb5768a73c411216a4cf821f5e74` |
| `corpus/instruments/r35-defect-closure.sh` | `a4f80067183e8512d5e7f39a789c7b51437f357acb05cd77d481a4d9c7cc35ad` |
| `corpus/source-snapshots/round-35/manifest.json` | `06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee` |
| `corpus/source-snapshots/round-35/S052.txt` | `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826` |
| `.ufo/waves/round-35/claims-erratum-d5.md` | `eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6` |
| `.ufo/waves/round-35/wave1/ScribeGateAssimilation.md` | `63c39a38b88e327b2646381f37d9ecd0b1164f129fa85882c8497add90e23a3a` |
| `.ufo/waves/round-35/wave1/ScribeQualityDraft.md` | `ffe46ad853e70cc47464bb7df266ceaef713cc47104aeadd4635d453b4130e8e` |
| `.ufo/waves/round-35/wave1/ExecScoreGap.md` | `fe795dd3b4eedd252aece34c5bbde11d3d1c83cd9ba7f5a583f2841d1f2a20c4` |
| `.ufo/waves/round-35/wave1/RevC2BeforeAfter.md` | `0a78d8528ec12717a033e76595a887b662810dc688f1069fe8ed93c9ecb01d88` |
| `.ufo/waves/round-35/wave1/ScoutDatawalk.md` | `e692140fc7a9e84e19191252453b9c9eb7d4783c0d6cd280a5b74692c393dc6e` |
| `.ufo/waves/round-35/wave1/MutCounterBase.md` | `d9ad2df2740ef3c43758aa61e4cc58dd2e6ee7337bb9cf9b5263d006ad61da39` |
| `.ufo/waves/round-35/wave1/ExecBeforeReceipts.md` | `167902c7f29fbb3daeaffea07e703973031e4283d1c6d183c252571e8cfc0a34` |
| `.ufo/waves/round-35/c2-controls/junk-f18.md` | `0abec3591e4a2dc5195b23b1c2c920f66052327b7f971aa578af76c3459dc176` |

### Tooling

No installs or upgrades. Tools used: `bash`, `grep`, `sed`, `awk`, `sha256sum`, `git` (read-only
`status/log/show`), `python3` (stdlib), `scripts/sources-census.sh` (fleet read-only validator).
No package transaction ran (pacman paused host-wide; nothing needed).

### Scratch

None. This seat created no work tree under `/fast/scratch/hyaku/kasegi-r35/ConnTrends` — every
command above is read-only in the lane. `test -e /fast/scratch/hyaku/kasegi-r35/ConnTrends` →
absent at exit (command 15). No defect to report on this surface.

### Findings for the L1

- **F1 (race, recorded):** this seat's first frontier-harness read printed `entries=20 pass=20`;
  between reads a sibling landed the README F18 amendment (+28 lines) and the second read printed
  `entries=21 pass=21` with `PASS F18 ids=S052`. Both values are quoted above with their order; the
  frozen counting commands must be re-run at integration.
- **F2 (pending owners):** D4 closes only at the L1's commit of `wave1-results.json` +
  provenance note (Q10); D6 has no authored correction yet (Q12); D7's exact apply-bytes sit in
  `ScribeQualityDraft.md` §1 (Q13). Until all three land, the suite prints `closed=4/7` and the
  selftest prints `failures=3` — that is the expected mid-wave state, not a suite defect.
- **F3 (discernment feed):** `ScoutDatawalk` F-4 is the round's live disagreement candidate (the C2
  junk-twin kill clause repeats the D5 class as written); it should reach the round-35 lesson
  alongside M35-1. The round-35 lesson file does not exist yet.
- **F4:** `ExecDoNothingReject.md` receipt was still being written by its seat at yield time; the
  twin-rejection fact is independently evidenced in the table (E9).

**Verdict for the L1:** the evidence table above is complete for all three trends with named
locations, measured values, and pending owners; trend verdicts remain the L1's. Expansion evidence
is landed in the working tree (18/18 counters green except the pending do-nothing receipt); quality
evidence is 4/7 closed with the remaining three named and ready; discernment evidence shows the
agree-pattern holding (5/5 round-34, gate decisions on record round-35) with two live disagreement
candidates routed to the lesson path.

Report: `.ufo/waves/round-35/wave1/ConnTrends.md`
