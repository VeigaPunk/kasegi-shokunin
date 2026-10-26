# Round 35 — kasegi

Lane: `kasegi-shokunin`. This lesson reports working-tree and receipt evidence, not a canonical
judge decision. Revisions: base `3266c9937b03062d9bbc2f436e20820115ed179c`; claims-freeze commit
`617496b9c6e92bc671e7e78b83df69a04470d0e9` (committer `2026-10-26T03:28:03-03:00` = `06:28:03Z`);
wave-1 dispatch commit `da2d3c687f82a9814ee71c91c930cb733050d37c`; C1 D4/D6/D7 integration commit
`aa6ad99bb90c4fe30dc5c326adf2f82d8ec84b1b`; wave integration commit
`0aee0ef` (lesson, SCORECARD section, SHONEN, LOG, wave receipts, assimilation artifacts); follow-ups
`8ce6fb4` (SCORECARD closing-commit wording) and `5a25337` (wave leftovers: S052 capture, SKILL
registry, controls, ready markers, receipts); closing lane-commit hash `INTEGRATION_HASH_PENDING`
(the L1 fills this in its final commit; this seat does not commit and deliberately plants no
angle-bracket lane-hash marker, because C1's own D1 clause counts that token).

Shape: **one v2 wave**. Wave 1 `kasegi-r35-build`, **64 seats**, one batched `task` call
(`.ufo/waves/round-35/wave1-dispatch.json`: `schema=ufo-swarm-wave-dispatch-v1`, `wave=kasegi-r35-build`,
`counts={spawn: 64, resume: 0, total: 64}`, `policy.maxLanes=128`, sha256 `aedd0320…`); `wave1-spec.json`
carries 64 `items` (sha256 `3fcf44e1…`); `wave1.ready` names `l1: KasegiR35`. Declared role counts:
executor 18, scribe 12, reviewer 10, scout 6, mutation-tester 5, critic 5, connector 4, sentinel 2,
simplifier 2 (= 64). Route: L1 inline spawn handoff, hyaku run 8
(`/home/vgpnk/Projects/shokunin/.ufo/watchdog.log:1490` — `2026-10-26T03:26:29-03:00 launch kasegi
round=35 pgid=2458141 driver=hyaku-inline attempt=1`). Axes owned: `depth:density`,
`depth:verifiability`, `coverage`; saturation line 9/10 per axis, window N=3; lowest non-retired axis
`depth:verifiability (4)`.

Receipt coverage at the last read: **61 of 64** spec names filed a `.ufo/waves/round-35/wave1/<seat>.md`,
plus one file under a name the spec does not carry (`ConnSibling-ruling-draft.md`, a ruling draft with
no `## Report`) — the name-vs-spec difference is non-empty on both sides
(`wave1/ScribeMistakesDraft.md:368-376`). Absent at the last count: `ExecCensusAfter`,
`ExecRegressionC1`, `SentScopeFinal`. Their numbers below are this
seat's own measurement at the digests stated inline, or are named absent; the SCORECARD round-35 record did land — a 19-line stub at `SCORECARD.md:1263-1281` carried by `0aee0ef`
(unclaimed by any receipt) and the receipt-grounded section `ScribeScorecard` appended at `:1284` — and
`SHONEN.md` was refreshed by `ScribeShonen`.

Answering model on seat receipts (by the name each receipt states for itself): **1 of 61** names one —
`anthropic/claude-sonnet-5-5` at `wave1/ScoutPackageThemes.md:3`. The other 60 name no model.
`wave1/ScribeIntegrationNotes.md:144` carries a `⟨FILL⟩` prompt for it. Two files carry a model-shaped
token that is **not** a seat self-identification: that prompt, and the rule at
`wave1/ScribeMistakesDraft.md:397` that model attribution is not a round criterion. No receipt names a
model outside these, so any model field in a report that is not read from a receipt is the report's own
route metadata, not seat evidence.

Frozen-control note: `c1-controls/before.txt` (`352d3da2…`), `c2-controls/before.txt` (`2835700332…`)
and `census-before.txt` (`74fc6a26…`) are three separate captures, and each was replayed independently
and matched line-for-line at the freeze commit by `wave1/ExecBeforeReceipts.md` §3–§5,
`wave1/RevC1BeforeAfter.md` §2 (12/12 MATCH) and `wave1/ScoutDatawalk.md` §2. This seat re-ran the same
replay from a `git archive 617496b9` export at `06:33Z` and matched all 18 stored values, including the
two that are easy to fake: `grep -c 'filled by the L1' SCORECARD.md` = 1 (`:1240` at the freeze) and
`grep -c '201\.7' SCORECARD.md` = 2 (`:1003` — the round-33 row, legitimately — and `:1145`).

## Frozen claims — before → after

Before column: the frozen controls at the freeze commit (claims-freeze evidence, not seat work).
After column: measured on the integrated tree at `2026-10-26T07:02Z`, after `aa6ad99` landed D4/D6/D7.

| Claim | Axis | Before (frozen controls, freeze `617496b9`) | After (integrated tree) | Verdict / boundary |
|---|---|---|---|---|
| **C1** | depth:verifiability (4) | `r35-defect-closure.sh` absent (`ls_exit=2`); `filled by the L1`=1; `c1c6a5f`=0; `201.7`=2 / `201.2`=0; SKILL registry greps 0/0; results tracked 0, provenance note 0; `claims-erratum-d5.md` absent; dead-seat sentence 1 / `Correction (round 35)` 0; `supersedes R22`=0 / `R23`=0 (`c1-controls/before.txt`) | suite `corpus/instruments/r35-defect-closure.sh` (sha256 `0ae4b484…`, 834 lines) prints `closed=7/7 exit=0` with `D1 placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3`, `D2 erratum-row=1,erratum-mean=3,row-bytes=1`, `D3 registry-r-defect-closure=4,registry-kill-rule=4`, `D4 tracked=1,provenance=1`, `D5 erratum-file=present,discriminating-invocation=5,per-id-occurrences=5`, `D6 dead-seat-sentence=0,correction-round-35=1`, `D7 supersedes-R22=1,supersedes-R23=1`; `--selftest` prints seven `selftest case=D<i> live=pass fixture=rejected mutants=n/n others=6/6 verdict=pass` lines and `selftest cases=7 failures=0`, with `control=clean closed=7/7`, `control=two-defect closed=5/7 failed=D1,D2`, four forgeries rejected and `judge=complete-report accepted=1` | **Held, and the frozen predicate is met.** Base-tree control `closed=0/7 exit=1` (`wave1/RevClosureSuite.md` §5, `wave1/CritC1Kill.md` §6); each defect's fix verified by a non-author (`wave1/RevD1D2.md:59` D1/D2 PASS; `wave1/RevD3D4.md` §1 D3; `wave1/ScribeErratumD5.md` §1 D5; D4/D6/D7 by the L1 at `aa6ad99`). **Boundary:** the counter is unbound to its own bytes (`wave1/CritC1Kill.md` §5 F-1) and three closure clauses are file-wide literals (F-2…F-5) — see § Open items 3–4 |
| **C2** | coverage (7) | frontier 17; registry rows 51; `S052` rows 0; entries citing S052 0; knowledge entries 46; harness `entries=20 pass=20 exit=0`; `source-recheck S052` → `manifest UNAVAILABLE reason=missing`, exit 2 (`c2-controls/before.txt`; base bytes re-run by `wave1/MutCounterBase.md` §2, `wave1/ExecRegressionC2.md` §2) | frontier **18**; registry **52** (`corpus/SOURCES.md:58`); `S052` row 1; entries citing `^source: S052 ` 1; knowledge entries **47**; harness `entries=21 pass=21 exit=0` incl. `PASS     F18  knowledge/cisa-kev-catalog.md … ids=S052`; `source-recheck --source S052` → `sha256 OK`, Q1–Q5 each `OK occurrences=1 anchor=N-ok`, exit 0; census exit 0 (W04 S028/S029 only); `recheck-audit.py` `lines=47 total=47 pass=47 fail-closed=24 parse_fail=0 cwd_fail=0 exit=0`, `expect=present expected=47 missing=0 unexpected=0` | **Counters reproduce** (`wave1/ExecRegressionC2.md` §4: seven counters + the entry count, `Mismatches: none`). **Boundary:** the entry needed one non-author repair round (Q2 on Claim 4b) and the declared junk-twin control does not discriminate (`wave1/CritC2Kill.md` § Verdict) — § Gate, § Mistakes M35-5 |

## Gate

### Admitted — F18 / S052 (CISA Known Exploited Vulnerabilities catalog)

- **Row:** `corpus/SOURCES.md:58` — `S052`, kind `dataset`, tier A scoped to CISA's own KEV statements,
  status `mined`, `opened 2026-10-26`, recheck `90d`, `used-by corpus/knowledge/cisa-kev-catalog.md`,
  anchor pinned to the round-35 capture (`wave1/ExecRegistryAppend.md` §1; `wave1/RevRowS052.md`
  § Verdict: **matches**, 11 cells / NF=13, no `|` inside a cell).
- **URL:** `https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json`
  — requested URL == effective URL, no redirect, HTTP 200, `application/json`, 1,807,090 served bytes →
  1,479,694 normalized bytes, 27,870 lines, sha256
  `d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826`
  (`corpus/source-snapshots/round-35/manifest.json`, `06bfcc71…`, 5,631 B).
- **Access date:** `2026-10-26T06:32:40Z` (manifest `fetched_utc`, strict UTC); the feed was re-fetched
  live at `06:36:23Z` with **0 differing lines** and the same sha256 (`wave1/ScoutKEVLive.md` A), and
  again by `wave1/CritC2Kill.md` (`IDENTICAL`).
- **Quote (≤25 words, located, exactly-once):** `"title": "CISA Catalog of Known Exploited
  Vulnerabilities",` — 7 words at `corpus/source-snapshots/round-35/S052.txt:2`, `occurrences=1`
  (manifest Q1). The exploitation-status limb rests on manifest Q4, 8 words at `S052.txt:15472`
  (`"dueDate": "2022-07-18", "knownRansomwareCampaignUse": "Known", …`), also `occurrences=1`.
- **Distinctness from CVSS:** measured as the absence of *fields*, not of tokens — `cvss` 0,
  `base score` 0, `risk rating` 0 across 12 keys × 1,756 records, while `severity` occurs twice and
  `score` once inside free text (`wave1/ExecC2Capture.md` §3, §7.3). The entry states it that way.
- **Currency boundary the round found:** BOD 22-01 is revoked and superseded by BOD 26-04 (directive
  page dated 2026-06-10, `wave1/ScoutKEVLive.md` verdict 4). The capture's own field text still names
  BOD 22-01 on 340 records and BOD 26-04 on 139 (`wave1/ExecC2Capture.md` §9); the entry states the
  split per record instead of promoting either directive.

### Admission history — the entry was refused once and repaired

`wave1/RevEntryF18.md:12` refused the intermediate bytes: `REFUSE — one criterion: Q2, for Claim 4b
only` — Claim 4b asserted directive force from a live page with no registry row and no capture, and
Q2 has no disclosed-live-read exemption. The author applied repair path 2 (demote the directive-force
content to a labelled Scope note, `:89`), and the reviewer's appended re-check reads
`Final verdict: ADMIT (digest e9de994d…)`, Q1–Q10 all PASS (`wave1/RevEntryF18.md:101-115`).
**Constraint this repair exposed:** registering a directive-page row instead would have moved the
registry to 53 and broken C2's frozen literal (`registry rows != 52`) — repair path 1 is a claim-level
change, not a wave-level one.

### Rejected — the declared junk-twin control does not discriminate

`c2-controls/junk-f18.md` carries the *same* `recheck:` line the real entry runs, so `source-recheck`
selects the real manifest and exits 0; the same bytes pass the harness as an admitted row
(`wave1/CritC2Kill.md` § Verdict: "no landed check rejects the junk twin"; this seat re-ran the twin's
command at `07:00Z` → exit 0). Per the frozen kill rule's literal ("junk twin passes source-recheck or
is admitted"), the control artifact triggers the clause. The executable form exists for the round-34
sentence in `.ufo/waves/round-35/claims-erratum-d5.md` (check *the twin's own fabricated quote* against
the capture: 0 occurrences) but was not restated for the round-35 claim. M35-5 carries it.

### Quarantine slice — 7 register rows, hand-checked, none adopted

Derivation is the frozen command over the read-only shokuknow register
(`absent-defect-register.md`, sha256 `5afe1810…`, 375 lines, unchanged since round 34). The slice is
417 B, sha256 `d02acb68…`, 7/7 lines carry an S-id and a second run is byte-identical
(`.ufo/waves/round-35/assimilation/quarantine-slice`; independently re-derived as
`quarantine-slice-rederived` `7696d76c…` — `wave1/ScoutQuarantine.md` §1, `wave1/ScribeGateAssimilation.md` §1).

| id | register class | live fetch (2026-10-26) | verdict | flip condition |
|---|---|---|---|---|
| S037 | `payload-absent` | 200, 24,189 B HTML | **prose-class-unverifiable** — four-cell composite; constituents located, no contiguous span | rewrite as cell-anchored fragments |
| S054 | `payload-absent` | 200, 513,648 B PDF | **prose-class-unverifiable** — drops an interpolated statutory parenthetical, crosses a line-wrap | restore the parenthetical (corrected span located) |
| S048 | never checked | **404**, 748 B (`HTTP状态 404 - 未找到`) | **unreachable** — dead record id, live host | a fresh register id for the same standard |
| S065 | never checked | 200, 7,465,472 B PDF | **present-and-located** (`刑法（7 件）` at `S065.txt:1182`) | — (not adopted: quarantine-first) |
| S068 | never checked | 301→301→200 to `sec.cloudapps.cisco.com`, 94,027 B | **present-and-located** (same document as lane row S040, already `mined`) | — |
| S069 | never checked | 302 → token URL; verifying client **fails (curl 60)**; `-k` fetch 200, 1,470,121 B PDF | **present-and-located** (`6.3.1 技术分级`, `S069.txt:1019`) — transport caveat | — |
| S070 | never checked | 302 → token URL; verifying client **fails**; `-k` fetch 200, 234,182 B PDF | **present-and-located** (`一、工作简况`, `S070.txt:8`) — transport caveat | — |

Totals: present-and-located 4 · prose-class-unverifiable 2 · unreachable 1 · absent 0, one fetch per
row in a 67.7 s window (`wave1/ExecQuarantineSlice.md` §2;
`.ufo/waves/round-35/assimilation/quarantine-verdicts.md`). Three things the Gate keeps from it:

1. **Four of the register's seven "absent"/never-checked rows are present when fetched.** For these ids
   the register's class records that nobody fetched, not that the text is gone. Nothing is adopted this
   round (quarantine-first), so no lane claim rests on them.
2. **The two derivations agree on the slice and the facts, and disagree on three labels** —
   `wave1/ScoutQuarantine.md` verdict line: "the executor's labels differ from mine on S037/S054 (label
   only), S065 (omitted three defects), S069/S070 (strict-TLS vs `-k`)". Recorded verbatim; Open item 8.
3. `S069`/`S070` were fetched with certificate verification disabled after the verifying client failed
   on the `kass.sacinfo.org.cn` token URL. Nothing was adopted, so no claim rests on those bytes, but a
   later reader must not treat the fetch as clean.

### Id-collision check — re-run, guard shown load-bearing

`reg-ids` (registry ids) ∩ `staged-ids` (94 ids `S031`–`S124` from
`shokuknow/merge/kasegi/SOURCES.append.md`, `4fe049cb…`) = **21 collisions `S031…S051`** before the
S052 append, **22 `S031…S052`** after it (`wave1/ExecIdCollisions.md` §1,
`.ufo/waves/round-35/assimilation/{collisions,renumber-map-pre-c2.txt,renumber-map-post-c2.txt}`;
`wave1/ScoutPackageThemes.md` §2 reproduces 21→22). The guard was proved once on a fixture before any
append — `.ufo/waves/round-35/assimilation/guard-proof.txt`: 0-3-space pattern ids `S001 S031`,
column-0 pattern ids `S001`, `collisions (0-3-space) = 1 [S031]`, `collisions (col-0) = 0 []`,
negative control `S901` → 0, missing registry path → `exit=2` (fails closed), and the recorded limit
`indent boundary: 3sp caught=1 | 4sp caught=0 | tab caught=0`. Nothing was renumbered in the lane, and
adoption is by document, not by number (staged `S052` is a CNNVD weekly PDF; lane `S052` is the CISA
feed).

### Standing refusals — seven staged entries, no flip cleared

`wave1/ScoutPackageThemes.md` § Verdict re-confirms all seven against the package (every digest
byte-identical to round 34; newest package mtime `2026-10-24 23:33:20 -0300`), with each entry's flip
condition:

| staged entry | reason it stays refused | flip condition (still unmet) |
|---|---|---|
| `program-scope-rules-and-asset-boundaries.md` | 0 located quotes, no executable recheck, `ground: F09` collides with admitted lane F09 | a located quote + executable recheck + a non-colliding frontier id |
| `claim-packaging-and-report-quality.md` | body cites S036 (BILISRC V1.7) in no lane row and no capture | an S036 row + capture |
| `cn-crowdsourced-testing-roles-and-conduct.md` | H1 count 0; S081/S082 in no row/capture | an entry shape + the two rows |
| `chinese-crowd-testing-national-standard-2026-10-23.md` | S077/S078/S079 unregistered; `ground: F24` is not a lane F-id | three rows + a real frontier id |
| `chinese-criminal-thresholds-and-authorisation.md` | three PRC legal sources in no row/capture; staged ids collide with different lane rows | three rows + a renumber map |
| `chinese-program-severity-instrument.md` | S047 (sse.com.cn) unregistered; anchor `newsType_6` → 0 in `round-32/S049.txt` | the row + a locatable anchor |
| `program-severity-ladders-and-reward-scales.md` | same-name lane file differs (`6c05c98f…` vs `35de5f8b…`); S036 half unregistered | byte-identity or a supersedes row |

### Assimilation: none adopted

No staged entry has its flip conditions fully met, and no quarantine row was hand-checked present *and*
adoptable as quoted. The ≤1-reject leg of the gate is met by 1 unreachable + 2 prose-class-unverifiable
quarantine rows and seven standing refusals; the admit leg is met by the round's **C2 admission
(F18/S052)**, a live-capture admission, **not** an assimilation adoption.
`wave1/ScribeGateAssimilation.md` § Gate block and `wave1/ScoutPackageThemes.md` § Verdict both read
"Assimilation: none".

### Contested scope — none, ruled rather than left silent

`wave1/ConnSibling-ruling-draft.md` (drafted for this lesson; its re-runnable evidence is in
`wave1/ConnSibling.md`, which this seat did not open — the draft's own verdict line is what is quoted)
rules on every CISA/KEV-ground hit in the sibling lanes under `PROTOCOL.md:457-461` and kasegi's
`PROVINCE.md` Adjacent ("Sibling lanes are reported, not absorbed"):

- **19 of 20 sibling lanes hold zero hits.** The only tokens are `kake-shokunin`'s *rejection record*
  of the CISA **BOD 20-01** VDP template (`kake …/corpus/lessons/round-35.md:58-60`,
  `kake …/corpus/SOURCES.md:255`) — a different directive from BOD 22-01/KEV and a different topic
  (VDP publication path, already held here as S008/S021) — plus incidental NVD/CVSS/"in the wild" hits
  in `kagi`, `mori`, `kotoba`, `kotodama`, `tabi` that are quote sources, raw evidence blobs, or
  unrelated senses.
- **Ratification, not contest:** `shokuknow/doctrine/channel-recurrence.md:62` assigns the `cisa.gov`
  host to kasegi.
- **Ruling:** F18/S052 is uncontested; no report-to-lane item arises and no `PROVINCE.md` refinement is
  required.

## Mistakes

Numbering follows `claims.json` `non_claim_frontier_items.mistake`, which pre-numbers M35-1.
**Rows M35-2…M35-11 are provisional**: under the minting contract they may not be cited as ids until the
L1 files them in a separate appended erratum (`.ufo/waves/round-35/mistakes-erratum-1.md`, the
`.ufo/waves/round-34/mistakes-erratum-1.md` form). Field schema is round 33/34's plus this round's
six-point contract at `wave1/CritMistakes.md` § "Minting contract": class · evidence pointer with a
re-runnable command · captured-by (seat, or `none`, with `Criterion missed:` separate) · fix (a landed
artefact with digest, or *not landed* plus owner) · fix shown able to fail (a red value and a green
value, reachable without editing production files).

- **M35-1 — the round-34 wave wrote `wave1-results.json` 3 min 48 s after the lane was declared
  `complete`, so the file never entered a commit.** Class: landing / closure-order. **Evidence:**
  `.ufo/waves/round-34/wave1/ExecD4ResultsTrack.md:57` (watchdog `1488:… complete kasegi round=34`),
  `:61` ("written 3 min 48 s after the closure line"), `:188-190` (mtime `06:23:19Z`);
  `corpus/lessons/round-34-verifier-spotcheck.md:30,183-187` route it as D4, including its second limb
  (a transient rewrite of the committed `ExecRegressionC1.md`). **Captured by:** `none` as a live
  defect; **Criterion missed:** R4 ("a rendered wave is not execution") — every seat read the lane
  commit, nobody read the dispatcher's own output. (Writing `captured-by: R4` would repeat M34-1's
  criterion-as-seat error; `wave1/CritMistakes.md` F1.) **Fix:** landed — the file and its provenance
  note (`e1c44301…`) are committed at `aa6ad99`. **Able to fail:** `git ls-files
  .ufo/waves/round-34/wave1-results.json | wc -l` → `0` before that commit and `1` after (the suite's
  D4 payload separates the halves: `tracked` vs `provenance`).

- **M35-2 (provisional) — C1's D1 clause cannot see the placeholder spelling that actually occurred,
  and a repudiation of the hash satisfies its correction clause.** Class: counter discrimination.
  **Evidence:** `grep -c 'the L1 fills this line' SCORECARD.md` → 1 at the freeze (`:1129`) and 0 now,
  but `check_d1` matches only `filled by the L1` + the angle-bracket marker; the suite documents the
  choice rather than fixing it (`corpus/instruments/r35-defect-closure.sh:50-52`: "a literal matcher
  cannot cover prose placeholders without matching legitimate prose that quotes them"). Repudiation
  fixture: `wave1/CritC1Kill.md` §5 F-2 — a tree whose only `c1c6a5f` mention reads "**could not be
  confirmed** by this seat" scores `correction-c1c6a5f=1 open=0`. **Captured by:** `ExecBeforeReceipts`
  finding 3 (before the suite existed) and `CritC1Kill`. **Criterion missed:** R22 (freeze
  satisfiability). **Fix:** *not landed* — slot-bind the hash clause (the `Final lane commit:` line
  range) and add either a prose clause or a fixture that pins the documented limit. **Able to fail:**
  the repudiation fixture reads `open=0` and must read `open=1` under a slot-bound clause.

- **M35-3 (provisional) — the D1 landing deleted 15 lines from an append-only file and shifted the
  round-34 depth:density row from 1145 to 1146, orphaning a verifier citation.** Class: line-number
  drift against R6. **Evidence:** `git diff --numstat 3266c993 -- SCORECARD.md` → `54 15`;
  `git show 3266c993:SCORECARD.md | grep -n 'mean \*\*201\.7\*\*, 25 blocks, 710 path-citation'` → `1145`,
  the same grep on the worktree → `1146`; the orphaned citation is
  `corpus/lessons/round-34-verifier-spotcheck.md:173` ("Where: `SCORECARD.md:1145`").
  **Captured by:** `ExecD1Markers` (disclosed the reflow at `:82`). **Criterion missed:** R6.
  **Fix:** *not landed* — keep base line numbers or re-pin citations to a blob+line. **Able to fail:**
  `diff <(git show 3266c993:SCORECARD.md | sed -n 1145p) <(sed -n 1145p SCORECARD.md)` differs today
  and is empty when every base line keeps its number.

- **M35-4 (provisional) — the round's own closure gate is unregistered, and D3's clause cannot see it
  because a near-name sibling satisfies the literal.** Class: gate registration (D3 recurring on the
  round's own counter). **Evidence:** `grep -c -F 'r35-defect-closure' SKILL.md` → **0** while
  `grep -c -F 'r-defect-closure' SKILL.md` → 4 (rows `SKILL.md:1097-1098`), and the suite prints
  `D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0` — green while the new gate has no
  row. D3's own reason applies verbatim: "not graded conformant until registered" (`SKILL.md:1100`).
  **Captured by:** `ExecD3SkillRegistry` finding 1, `ExecScoreGap` § — and `wave1/CritMistakes.md` F2
  calls it the strongest row of the round. **Fix:** *not landed* — append the eight-field row for
  `r35-defect-closure.sh` and widen `check_d3` to the exact basename with its own mutant.
  **Able to fail:** the live tree is the red fixture (`0` vs `open=0`); after the row a
  `filter_out 'r35-defect-closure.sh'` mutant must print `open=1`.

- **M35-5 (provisional) — C2's frozen junk-twin rejection limb has no discriminating invocation,
  repeating the defect D5's erratum was filed to repair.** Class: frozen predicate without an executable
  form. **Evidence:** `claims.json` C2 `after[6]`; `c2-controls/junk-f18.md`'s `recheck:` line is the
  *real* selection (`--manifest …/round-35/manifest.json --source S052`) and exits **0** (measured by
  this seat at `07:00Z`); `wave1/CritC2Kill.md` § Verdict; `wave1/ScoutDatawalk.md` F-4 names it
  "exactly the round-34 D5 finding". **Captured by:** `ScoutDatawalk`, `CritC2Kill`. **Criterion
  missed:** the D5 erratum's restated rule, applied to this claim at freeze. **Fix:** *not landed for
  C2* — state the twin's rejection as the capture check (`grep -c` of its sentence in `S052.txt` → 0)
  and append the erratum form. **Able to fail:** the twin's sentence count is `0` while the frozen
  command exits `0`; the two outputs differ.

- **M35-6 (provisional) — the landed S052 search-log bullet carries an invalid digest abbreviation and
  a row count that does not match the registry.** Class: unverified literal in landed bytes.
  **Evidence:** `corpus/SOURCES.md:79` prints `sha256 d69349e8…77e8826`; the capture digest ends
  `779e8826`, and `'77e8826' in <digest>` is `False` (measured). The same line says "7 SOURCES rows":
  the base registry holds **5** rows mentioning CISA (`S003 S008 S021 S023 S026`), and 7 is only what a
  whole-file line grep returns once two `## Search log` bullets are counted. **Captured by:**
  `wave1/ScribeSearchLog.md` §5a (abbreviation) and `wave1/ScribeSOURCESRow.md` (count) — **Captured by
  a criterion:** `none`; the census validates row shape and URL binding, not prose counts or
  abbreviated digests. **Fix:** *not landed* — an R9-style appended correction naming both facts (never
  a rewrite of `:79`). **Able to fail:** the abbreviation check prints
  `abbrev=1 invalid=1 [(79, 'd69349e8…77e8826')]` today and `invalid=0` after;
  `grep -ci cisa` restricted to `^| S` rows prints `5` at base and `6` at tip, never `7`.

- **M35-7 (provisional) — a receipt asserted its scratch tree was absent while a later write re-created
  it, making the durable record a prediction.** Class: landing/closure-order (M35-1's class, on
  cleanup). **Evidence:** `wave1/CritBoundary.md:45-60` — `wave1/ExecClosureSuite.md` (mtime `03:41:35`,
  sha256 `f8f99970…`) printed `scratch-absent` while `live-selftest.txt` (`03:42:59`),
  `.git/objects/…` (`03:43:36`) and `green.txt` (`03:43:43`) were written after it; `ls -d` at
  `03:44:26` returned PRESENT. **Captured by:** `CritBoundary`; the seat then appended its own
  correction (`wave1/ExecClosureSuite.md:381-386`). **Fix:** landed in the receipt (cleanup stated last,
  as executed output) plus an L1 close gate listing leftover scratch dirs. **Able to fail:** the red
  value is receipt-pinned; the re-runnable form is
  `find /fast/scratch/hyaku/kasegi-r35 -mindepth 1 -maxdepth 1 -type d` listing only seats with no
  receipt.

- **M35-8 (provisional) — an uncommitted edit to the wave generator states a C2 premise the capture
  seat measured as false.** Class: plan-vs-capture drift with no attribution. **Evidence:**
  `git diff -- .ufo/waves/round-35/build-spec.py` (mtime `03:32:50`, sha256 `a56179ca…`) rewrites the
  `ExecC2Capture` item to "the JSON endpoint … returns HTTP 404 …, so the official CSV distribution is
  the primary data source"; that 404 is the **short** path only — the feed exists one path over (200,
  `application/json`, 1,807,090 B) and the CSV shares all 1,756 records with 12 header fields, not 9
  (`wave1/ExecC2Capture.md` §1, §6). **Captured by:** `CritBoundary` F2 and the capture seat itself
  ("that steer's premise is false one path over"). **Fix:** *not landed* — a committed spec erratum
  naming the accepted URL; the editor's identity is not determinable from the bytes, and the lesson
  must say so (`wave1/CritBoundary.md` F2). **Able to fail:** `curl -o /dev/null -w '%{http_code}'` →
  `404` on the short path, `200` on the feed; `grep -c 'known-exploited-vulnerabilities.json'
  wave1-spec.json` → 1.

- **M35-9 (provisional) — the frozen claims declare a freeze instant 62 minutes after the freeze commit,
  and it is still in the future.** Class: unbound provenance literal (R22/R25's class on a timestamp).
  **Evidence:** `.ufo/waves/round-35/claims.json:6` `"frozen_at_utc": "2026-10-26T07:30:00Z"`;
  `git log -1 --format='%cI' 617496b9` → `2026-10-26T03:28:03-03:00` (= `06:28:03Z`); `date -u` at
  teaching time `07:03Z`. Sign anomaly: round 34's field sat *before* its commit. **Captured by:**
  `none`. **Fix:** *not landed* — bind the field to the freeze commit's committer date. **Able to
  fail:** `declared <= now` is false today and true once bound.

- **M35-10 (provisional) — a live prior-round seat answered for a round-35 item because the id is
  reused across rounds, and the landed row's author is recorded as "an unnamed round-35 seat".**
  Class: dispatch/identity collision. **Evidence:** `wave1/ExecRegistryAppend.md:3` names itself
  `ExecRegistryAppend-3` and claims authorship of `corpus/SOURCES.md:58/:79/:108-110`, while
  `wave1/ScribeSOURCESRow.md:7-15` records that the agent it addressed as that executor "replied that
  it holds only the round-33 item and disclaims the round-35 write". **Captured by:**
  `ScribeSOURCESRow`. **Fix:** *not landed* — round-prefix seat ids; require a substitute to quote the
  authorizing message id. **Able to fail:** a pre-spawn check that every spec name is unused in the live
  registry is red on this wave; the two receipts contradict each other on disk.

- **M35-11 (provisional) — the round-35 SCORECARD depth:density guard row repeats D2 on this round: it
  prints the base mean as if it were the guard reading.** Class: stale density row (D2 class).
  **Evidence:** `SCORECARD.md:1269` — `| depth:density | 9 | unchanged (no density claim; no-harm guard
  mean ≈ 201.2) | wave1/ExecNoHarmFinal.md |`; the landed tree measures **220.9** over **26 blocks /
  742 cites** (`wave1/ExecNoHarmFinal.md` §1, this seat at `07:02Z`), against 201.2 over 25 blocks /
  711 cites at the freeze. The number in the row is the *base* value, the word "unchanged" is false for
  the mean, and the cited receipt reports both values. **Captured by:** `ExecNoHarmFinal` (its two T
  samples carry both numbers) and `ScribeScorecard`, whose appended section at `SCORECARD.md:1284`
  restates the guard as 220.9 with byte binding and flags the stub as superseded.
  **Criterion missed:** D2's own fix (append the after-value beside the before-value).
  **Fix:** *partially landed* — the receipt-grounded restatement exists at `:1284`; the stub row at
  `:1269` is reconciled only at the closing commit, and the file still carries **two** `## Round 35`
  headings (`:1263`, `:1284`). **Able to fail:** `python3 corpus/instruments/density.py SKILL.md | grep mean`
  prints `220.9` today; the row says `≈ 201.2`.

Cleared on re-check (not minted): the dispatch URL 404 itself (external drift; the artefact choice is
in the committed manifest — `wave1/CritMistakes.md` F7), the ~35 s `unexpected=cisa-kev-catalog.md`
transient from `recheck-audit.py` (the completeness gate firing correctly — same F7), and model
attribution (`wave1/ScribeMistakesDraft.md:397`).

Word sweep this section rests on — over the 62 `.md` files in `wave1/` at teaching time:
`for w in FAIL REFUSE REJECT SURVIVOR traceback; do printf '%-9s files=%s\n' "$w" "$(grep -l -F -- "$w" *.md | wc -l)"; done`
→ `FAIL files=8`, `REFUSE files=15`, `REJECT files=2`, `SURVIVOR files=1`, `traceback files=1`. The
`FAIL` files are fixture and gate output, the `REFUSE` count includes every receipt quoting the entry
review, and the single `SURVIVOR` file is `MutC2Entry`. Pointer, not review: § Mistakes lists the events
this seat opened and re-verified.

## considerthese

`considerthese/2026-10-25.md:53-57` proposal 2 ("Track 'distance to the next score', not just 'improved,
held'") is **mined → landed** as **R26** at `corpus/QUALITY.md:249`, in the append-only block that also
lands **R27** (`:250`, supersedes R23's grounded-in column). The block was drafted as 21 lines / 2842 B
/ sha256 `e3aa99a1…` appended after line 229, whose prefix hash is `807cc714…`
(`wave1/ScribeQualityDraft.md` §1); the landed file's digest is `d4f83bb1…`. The read-only gap
computation the criterion asks for is `corpus/instruments/score-gap.py` (this seat ran it,
`07:03Z`, exit 0):

```
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

So the score-relevant number moved from 23/37 gated (round 25's reading) to **24/47** while the entry
set grew — coverage improved and the score-5 gap did not narrow. This is a measurement, not a score
move: no axis score changes.

Dispositions of the other five proposals (from the lane's own ledger, not assumed):

1. *Cap wave-evidence bloat* — **mined round 28 → R14**, re-measured at `07:02Z`:
   `.ufo/waves/round-35` is 2,532,336 B, `wave1/` (62 `.md`, 17,636 lines) is 1,354,155 B at the last read, the planner
   artifacts are text-only (`wave1-spec.json` 654 + `wave1-dispatch.json` 1,067 + `wave1-plan.out`
   1,069 = 2,789 lines), the 1.41 MiB S052 capture is required source data outside the wave directory,
   and **0** scratch trees sit in the committed set.
2. *Distance to the next score* — **mined this round → R26** (above).
3. *Bounty craft / SHONEN box 2* — `unchanged`: the KEV capture plus `source-recheck` is a measurement,
   not a hunt-to-claim pipeline; `ScribeShonen` filed no receipt, so no box moved (`SHONEN.md` was
   updated by the L1).
4. *Proposal status ledger* — `unchanged` (`corpus/knowledge/considerthese-proposals-ledger.md`); this
   section is the disposition line the ledger would carry.
5. *Open-defects ledger with runnable closure checks* — **mined round 29 → R15**, and this round is its
   largest application: D1–D7 each carry a runnable check inside `corpus/instruments/r35-defect-closure.sh`,
   and `closed=7/7` is the ledger's read.
6. *Event-driven reflections* — **mined round 34 → R23**, citation superseded by R27.

## Census before → after

- **Before** (`.ufo/waves/round-35/census-before.txt`, `74fc6a26…`; replayed by
  `wave1/ExecBeforeReceipts.md` §5 against the live fleet root and, with `--file`, against the freeze
  export):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

- **After** (this seat at `2026-10-26T07:02Z`; `wave1/ExecRegressionC2.md` §4 counter 7 re-ran the same
  command with the same three lines and exit 0):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Same three lines, same exit, no new `W`, no `E`, with registry rows 51 → 52 and the S052 URL carried
once (no duplicate-URL warning). `ExecCensusAfter` filed no receipt, so the after-state is this seat's
measurement plus the seat named.

## No-harm

Measured by this seat at `2026-10-26T07:00–07:03Z` on the integrated tree; `RevNoHarm` and
`ExecRegressionC1` filed no receipt, so this table is the lesson's own measurement, with
`wave1/ExecNoHarmFinal.md` (its two T samples carry the same figures) and `wave1/CritBoundary.md`
(scope axes) beside it.

| Instrument | Before (freeze `617496b9`) | After (integrated tip) | Verdict |
|---|---|---|---|
| `density.py SKILL.md` | mean **201.2**, 25 blocks, 711 cites, 1091 lines (re-measured on the freeze export) | mean **220.9**, 26 blocks, 742 cites, 1104 lines | **Improved, not "unchanged".** The added block is the round-35 registry section (`SKILL.md:1093-1104`). The SCORECARD guard row's `≈ 201.2` is the base value — M35-11 |
| `anchorcheck.py SKILL.md` | 12 in-range, **0 bad**, `LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0`, exit 0 | 16 in-range, **0 bad**, same failure-class values (`BASE-ABSENT=0`), exit 0 | No class moved. One transient red is recorded, not hidden: `wave1/ExecScoreGap.md` §2a read `BASE-ABSENT=1` / exit 1 at `SKILL.md:1097` while the D3 row carried a bare `S050.txt:70`; the token is now `corpus/source-snapshots/round-32/S050.txt:70` and both the seat's addendum and this seat's run read clean. Caused by measuring in-flight bytes, not by a landing defect |
| `anchorcheck.py PROVINCE.md` | 0 in-range, 0 bad, exit 0 | identical; `PROVINCE.md` is byte-identical to base | No harm |
| `git diff --numstat 3266c993` | — | `SCORECARD.md 176 15`; `SHONEN.md 78 0`; `SKILL.md 13 0`; `corpus/README.md 28 0`; `corpus/SOURCES.md 7 0`; `corpus/QUALITY.md 21 0`; `LOG.md 10 0`; `knowledge-expected.txt 1 0`; `PROVINCE.md` **absent (0)** | Append-only except the D1-mandated in-place placeholder replacements (the 15 deletions — M35-3) |
| unowned writes | — | fleet root: no untracked `kasegi`/`round-35` path; `shokuknow`, `bounties`, `the-bounty-hunter`: zero round-window writes; lane git/jj: no stage/commit/bookmark mutation by a seat (`wave1/CritBoundary.md` §2) | **PASS with two recorded defects** (M35-7 scratch ordering, M35-8 plan-vs-capture) and three hygiene notes. Scratch: every seat that names a path records deletion; the exceptions are M35-7's window and this seat's own tree, deleted at exit |

Continuity of the counter: the suite digest moved six times inside the wave (`c748dd70…` 643 lines,
`cba8c95b…` 760, `5fb0da5e…`, `d7ad8438…` 773, `a4f80067…` 834, `0ae4b484…` 834) and then held at
`0ae4b484…` through the integration commits. Every C1 figure above is bound to `0ae4b484…`; the L1 must
record that digest in the closing receipt (round-28 convention), since C1's suite carries no byte pin of
its own (M35-2 / Open item 3).

## Open items / unverified

1. **C1's kill rule is met, its certification is not bound.** The suite prints `closed=7/7 exit=0` and
   `--selftest cases=7 failures=0`, but nothing binds the counter's own bytes: `wave1/CritC1Kill.md` §5
   F-1 shows a 361-byte replica printing the kill rule's strings, and `report_ok` accepting a report
   replica. The one-command fix is to record the suite + `fixtures.json` digests in the integration
   receipt; it is not landed.
2. **CritC1Kill F-2…F-5 are check-vs-own-text gaps, none landed:** D1's file-wide literal (M35-2), D5's
   heading-satisfiable statement clause, D4's identity-blind `{}` clause, D7's negation-satisfiable row
   clause, and D2/D3's shared shape. Each has a one-line append-only correction in that receipt.
3. **Three seats filed no receipt:** `ExecCensusAfter`, `ExecRegressionC1`, `SentScopeFinal`. Their numbers here are this seat's measurement or the L1's landed
   section; `ConnSibling-ruling-draft.md` is a draft under a non-spec name and carries no `## Report`.
4. **The entry's final ADMIT depends on a demoted claim.** Q2 is satisfied because Claim 4b became a
   labelled Scope note; the directive-force statement remains unregistered by design, and the
   reviewer notes a later round can admit it via a row + capture (`wave1/RevEntryF18.md:115`). That
   repair would move registry 52 → 53 and therefore needs a claim erratum, not a wave edit.
5. **C2's junk-twin control is false as built** and the frozen kill-rule clause is triggered by the
   control artifact (M35-5). The executable restatement exists only for the round-34 sentence.
6. **Two C2 mutants survive** (`wave1/MutC2Entry.md` § Verdict summary): M2b (an entry-side paraphrase
   is invisible to `source-recheck`, which reads the manifest) and M3 (a wrong anchor on a unique quote
   prints `anchor=N-BROKEN` on an `OK` line and exits 0, because `source-recheck.py` makes a broken
   anchor fatal only when `occurrences > 1`). All five S052 assertions are `occurrences=1`, so the
   anchor limb is unexercised by this round's manifest.
7. **The two quarantine derivations disagree on three labels** (`S037`/`S054` label only; `S065`
   "omitted three defects"; `S069`/`S070` strict-TLS vs `-k`). Recorded verbatim; the L1 or the
   canonical judge resolves. `S069`/`S070` bytes were obtained with certificate verification disabled
   and nothing was adopted from them.
8. **The wave generator is edited in the working tree** (`build-spec.py`, `a56179ca…`, uncommitted,
   author not determinable from bytes) and its C2 premise contradicts the capture (M35-8). The
   committed `wave1-spec.json` still names the 404 URL in the `ExecC2Capture` item.
9. **`claims.json`'s `frozen_at_utc` is future-dated** relative to its own commit and to the wall clock
   (M35-9). Nothing downstream reads it, so no counter is affected.
10. **`ExecExpectedListSync` left a stale header stamp** in `corpus/instruments/knowledge-expected.txt`
    ("— round 30") while the list is the 47-row round-35 set, by instruction
    (`wave1/ExecExpectedListSync.md` §7.3).
11. **The F18 entry was revised twice after receipts pinned it.** `wave1/ScribeEntryF18.md:7` pins
    `da81204b…`, `wave1/ExecExpectedListSync.md` §7.2 correlates its audit with that digest, and the
    final bytes (post-repair, ADMIT) are `e9de994d…`. The expectation limb is name-based so it still
    holds; any reader citing the 47/47 audit must use the final digest.
12. **The `S052` capture is 1.41 MiB** (above the round brief's 1 MiB note, far below the 10 MiB
    ceiling) and committed in full. It version-pins itself (`catalogVersion 2026.10.23`, `count` 1756);
    `source-recheck` is a local byte check and does not assert upstream freshness.
13. **This lesson's § Mistakes is a sweep plus opened receipts, not a completeness claim**, and rows
    M35-2…M35-11 are provisional until the L1 files the erratum (minting contract item 6). Two
    candidate rows were deliberately not minted (§ Mistakes "Cleared on re-check").
14. **`ScribeMistakesDraft`'s CISA-row figure is right for rows and wrong for lines** (5 registry rows
    vs 7 whole-file lines); this lesson prints both and adopts neither as a single figure (M35-6).
15. **`SCORECARD.md` carries two `## Round 35` headings** — a 19-line stub at `:1263-1281` (unclaimed by
    any receipt, carried by `0aee0ef`) and the receipt-grounded section at `:1284` (`ScribeScorecard`).
    The second names the first as superseded, and one stub cell (density `≈ 201.2`) is contradicted
    there and restated as 220.9 (M35-11). Merging the two is the closing commit's job; `grep -c
    '^## Round 35' SCORECARD.md` → 2 today.
16. **No statement in this lesson certifies the closing commit.** Six of the seven after-values were
    measured on worktree bytes after `aa6ad99`; the L1's closing commit, and a post-commit re-run of
    both C1 counters, remain owed.

## Touched surfaces and provenance

This lesson's only production path is `corpus/lessons/round-35.md`; the scoped seat report is
`.ufo/waves/round-35/wave1/ScribeLesson.md`, which holds the commands, their output, exit codes and file
digests. Evidence paths are named inline, principally
`.ufo/waves/round-35/{claims.json,claims-erratum-d5.md,census-before.txt,c1-controls/*,c2-controls/*,assimilation/*,wave1-spec.json,wave1-dispatch.json,wave1.ready}`
and the `wave1/` receipts this seat opened: `ExecBeforeReceipts`, `ExecC2Capture`, `ExecClosureSuite`,
`ExecD1Markers`, `ExecD2DensityRow`, `ExecD3SkillRegistry`, `ExecD4ResultsTrack`,
`ExecExpectedListSync`, `ExecIdCollisions`, `ExecNoHarmFinal`,
`ExecQuarantineSlice`, `ExecRegistryAppend`, `ExecRegressionC2`, `ExecScoreGap`,
`ExecSelftestFixtures`, `MutC2Entry`, `MutCounterBase`, `RevC1BeforeAfter`, `RevC2BeforeAfter`,
`RevD1D2`, `RevD3D4`, `RevD5D6D7`, `RevEntryF18`, `RevClosureSuite`, `RevRowS052`,
`RevSelftestFixtures`, `CritC1Kill`, `CritC2Kill`, `CritMistakes`, `CritBoundary`, `ScoutKEVLive`,
`ScoutDatawalk`, `ScoutQuarantine`, `ScoutPackageThemes`, `ScoutSiblingSweep`,
`ConnSibling-ruling-draft`, `ScribeEntryF18`, `ScribeErratumD5`, `ScribeGateAssimilation`,
`ScribeIntegrationNotes`, `ScribeQualityDraft`, `ScribeSearchLog`, `ScribeSOURCESRow`,
`ScribeMistakesDraft`, `ScribeScorecard`, `ScribeShonen`, `SentCred`. Every receipt this file cites, this seat opened; the three seats that
filed nothing are named where their numbers would otherwise have been cited.

Digests of the bytes this lesson's numbers belong to (`2026-10-26T07:03Z`, worktree; the L1 must
re-measure after the closing commit):

```
0ae4b4848b109ccc2cc5635725a4f58f172ab58ea294a3506bf5d3fec09ae27f  corpus/instruments/r35-defect-closure.sh (834 lines)
b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113  corpus/instruments/r35-fixtures/fixtures.json
e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761  corpus/knowledge/cisa-kev-catalog.md (final, ADMIT)
d69349e86c5cce17146ccb4a4d514272d5ef47cb9586d06085113cf6779e8826  corpus/source-snapshots/round-35/S052.txt (1479694 B, 27870 lines)
06bfcc71e6df494b0b54f489077b6bf747aeb4294f412e4deae64a2ac747f6ee  corpus/source-snapshots/round-35/manifest.json
ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94  SCORECARD.md             (D1+D2; round-35 stub :1263, section :1284)
daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md                 (D3 registry, 13/0)
0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba  corpus/SOURCES.md        (52 rows, S052 at :58)
277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2  corpus/README.md         (18 frontier rows)
d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69  corpus/QUALITY.md        (R26 :249, R27 :250)
a576d58c347300b7d4517515397ae7bb541d87fbc837139b22b8612280885200  LOG.md                   (round-35 entry)
eee0bb579844ad9d02777fb4cd241e726d0bb0630679bc41aa534d7f5d0951e6  .ufo/waves/round-35/claims-erratum-d5.md
e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98  .ufo/waves/round-34/wave1-results.json.provenance.md
```
