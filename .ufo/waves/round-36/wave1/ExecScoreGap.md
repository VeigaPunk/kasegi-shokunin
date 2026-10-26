# ExecScoreGap — distance to the next score, both owned axes (round 36)

Read-only measurement for round 36, answering `considerthese/2026-10-26.md` proposal 1 ("Write the
concrete criteria for verifiability 5 and coverage 8 into `SCORECARD.md` §Saturation … Either the 4→5
and 7→8 thresholds are unreachable with the current kind of work, or they are undefined") and the
criterion `corpus/QUALITY.md` R26 (a round reports the distance to the next score, not only
"improved, held"). **This is not a claim and asserts no score move.** No lane file was edited; the
only lane file written is this receipt. Every figure below was printed by the command named beside it
and is not retyped from another document.

Measured lane head: `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6` (round-36 claims freeze). The live
tracked tree equals that commit: `git status --porcelain | grep -v '^?? \.ufo/waves/round-36/'`
prints nothing (only round-36 wave scratch is untracked). A second, race-free run was made on
`git archive b47f2cdf…` exported to scratch (§2).

## 1. The instrument the lane already owns: `score-gap.py`

`corpus/instruments/score-gap.py` (landed round 31, sha256 `57584fda…`) reports
**depth:verifiability only**. Run in-lane, exit 0:

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -B corpus/instruments/score-gap.py --root .
score-gap — depth:verifiability distance to score 5 (read-only; NOT a claim; asserts no score move)
source: corpus/instruments/recheck-audit.py sha256=5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source: SKILL.md sha256=daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc
source: corpus/instruments/citation-survival.md sha256=795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d
source: SCORECARD.md sha256=ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94
[1] rechecks
recheck: lines=47 executes=23 gated=24 broken=0 exit=0
[2] anchors
anchorcheck: in-range=16 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=0 exit=0
[3] citation-survival census (committed figures)
census-lane: 134/1480 = 9.05%
census-skill: 32/506 = 6.32%
[4] score-5 threshold
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
[5] gap
gap: 24 of 47 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
```

Soundness check of the instrument itself (`--selftest`, `TMPDIR` bound to scratch):
`selftest recheck-mode=real`, all case lines `ok`, `selftest fields=7 failures=0`, exit 0, and both
fixture lanes print `no-write-a/b ok tree digest unchanged=True`. It has no write path.

## 2. Export run, and the one field that is not export-invariant

Same instrument over `git archive b47f2cdf…` (7117 files) prints the **same** `[1]` counts, `[2]`,
`[3]`, `[4]` and `[5]` lines, but `recheck: … exit=1` instead of `exit=0`:

| root | `strict pass` | `lines=… pass=… fail-closed=` | recheck `exit` | gap line |
|---|---|---|---|---|
| live lane | `47/47 cdroot_fail=0` | `47 total=47 pass=47 fail-closed=24` | **0** | `24 of 47` |
| `git archive` export | `1/47 cdroot_fail=46` | `47 total=47 pass=47 fail-closed=24` | **1** | `24 of 47` |

Cause, measured in the instrument's own strict limbs: `recheck-audit.py`'s `cdroot` limb requires
each `recheck:` payload's `cd <path>` to equal the audited root (`recheck-audit.py:27,89,137`), and
46 of the 47 payloads `cd` to the lane path. **The gap line is invariant; the recheck exit is not.**
A reader who runs `score-gap.py` on an export and reports its `[1] exit` would report a red that is
a root-path artefact, not a lost-base fact. The in-lane run is the one to cite.

No-write proof for both instruments on the export: tree digest
`5550a6cbffa4411e29effdd5a6ef6608d50fa1586f7caa90ac488ed41d38b829` before **and** after running
`score-gap.py` and the coverage enumerator (`cmp` identical, 7117 files).

## 3. depth:verifiability — 4 → 5

| field | value |
|---|---|
| current score | **4** (`SCORECARD.md:1282`: "Lowest non-retired axis still depth:verifiability (4)") |
| next score | **5** |
| threshold recorded? | **yes** — `SCORECARD.md:331`, the only `Threshold for 5` line in the file (`grep -c 'Threshold for 5' SCORECARD.md` → `1`) |
| threshold text | `Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims.` |
| conjunct (A) source chains | today's analogue of `25/25` is **47/47** (`recheck:` lines = `corpus/knowledge/*.md` = 47) |
| conjunct (B) unsupported claims | **not defined** by the sentence; measured on both limbs the lane owns |
| measured (A) | **23/47 execute, 24 gated, 0 broken** (48.9 %) |
| measured (B) recheck limb | **24 gated** of 47 |
| measured (B) anchor limb | **5 of 51 swept files red, 9 failing instances** (8 `BASE-ABSENT`, 1 `PAST-EOF`) |
| **gap** | **24 gated chains + 9 failing anchor instances** |

Anchor sweep at this head (`for f in corpus/knowledge/*.md corpus/*.md SKILL.md; do python3 -B
corpus/instruments/anchorcheck.py "$f"; done` → `files=51 green=46 red=5`):

| file | instances | class |
|---|---|---|
| `corpus/knowledge/citation-bases.md` | 1 | `BASE-ABSENT` `~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` (true lost base) |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | 1 | `BASE-ABSENT` `S029.txt:20` (lane copy exists at `corpus/source-snapshots/round-23/S029.txt`) |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | 5 | `BASE-ABSENT` `S041.txt:…` (lane copy exists at `corpus/source-snapshots/round-26/S041.txt`) |
| `corpus/knowledge/root-loss-2026-10-12.md` | 1 | `BASE-ABSENT` `queue.json:11-12` (true lost base) |
| `corpus/QUALITY.md` | 1 | `PAST-EOF` `README.md:159` (the lane `README.md` has 14 lines) |

Reachability of the gap, stated so the L1 decides rather than infers: **7 of the 9 anchor instances
are lane-side fixes** (6 bare capture names to prefix, 1 ambiguous `README.md` to spell); **2 are true
lost-base cites**. The **24 gated chains cannot pass while `~/Projects/bounties` and
`~/Projects/the-bounty-hunter` are absent** — conjunct (A) is unreachable at these bytes without
operator restoration or a declared counter redefinition. That is the honest reading of "4 → 5 is
unreachable", and it is a property of the counter, not of this round's work.

Distance trend on the same bar: round 22 recorded 23 of 25 gated; round 25 23 of 37; round 35
`24 of 47`; today **24 of 47**. The passing set grew with capture-backed entries; the gated count
has not fallen. No score move is claimed or implied.

## 4. coverage — 7 → 8

There is **no committed instrument for the coverage axis**, so the computation was implemented
read-only in scratch (`$S/gap-coverage.py`, 100 lines, stdlib only, writes nothing) and enumerates
every recorded next-score threshold and bound from `SCORECARD.md` §Saturation, `corpus/QUALITY.md`
and `PROVINCE.md`. Output at this head, exit 0:

```
[1] recorded thresholds
threshold: SCORECARD.md:331 score 5 "a non-author audit passing 25/25 source chains and 0 unsupported current claims."

[2] saturation declaration (SCORECARD.md § Saturation)
saturation line: 9/10 on each owned axis
stagnation window: N = 3

[3] measured counters at this root
frontier_admitted: 18
frontier_last: F18
registry_rows: 52
knowledge_entries: 47
province_frontier_max: F17
province_names_F18: no

[4] gap per axis
depth:verifiability 4->5: threshold recorded at SCORECARD.md:331; run corpus/instruments/score-gap.py for the computed gap
coverage 7->8: threshold UNDEFINED (no 'Threshold for 8:' or coverage-bar sentence in SCORECARD.md, corpus/QUALITY.md or PROVINCE.md)
coverage nearest recorded bound: saturation line 9/10 = 2 points above the current 7
```

**Finding: the coverage 7 → 8 threshold is undefined.** `git grep -nE "coverage 8|score 8|coverage.*8/10|Threshold for 8" -- '*.md' ':!.ufo/'`
returns exactly two hits, neither a threshold: `considerthese/2026-10-26.md:29` (proposal 1, which
*asks* for the criterion to be written) and `corpus/lessons/round-24-verifier-spotcheck.md:206` — a
verifier row about an unrelated instrument mutant (`bound-64→8`). `grep -c 'Threshold for'
SCORECARD.md corpus/QUALITY.md PROVINCE.md` → `SCORECARD.md:1 corpus/QUALITY.md:0 PROVINCE.md:0`.

What *is* recorded, and why none of it yields a distance to 8:

| recorded item | location | relation to coverage 7 → 8 |
|---|---|---|
| coverage axis definition: "top-level surfaces of the domain root that have either (a) a corpus entry documenting a full census/full read, or (b) a recorded park disposition"; r15 denominator re-based onto "two surviving roots (2 items) + the attested 18" | `SCORECARD.md:43-46` | defines the axis; records **0 present / 18 corpus-attested** and 0/2 roots present → **0/20 present**; frozen by an operator-owned root loss |
| "The original domain-root map is exhausted: 0/18 surfaces are present … the public-practice frontier above is a separate denominator … and is not counted into the 0/18 figure" | `corpus/README.md:217-223` | **explicitly excludes frontier admissions from the axis**, so 18/18 admitted cannot be read as movement toward 8 |
| r22 proposed denominator "(20 Core + Frontier admitted)/total → (20+0)/25 before, (20+5)/25 after" | `SCORECARD.md:332` | **proposed only, never adopted**; arithmetically exhausted at 18 admissions ((20+18)/25 = 152 %), so it cannot express today's state |
| saturation line **9/10 per owned axis**, stagnation window **N = 3** | `SCORECARD.md:313-315` | the only live numeric bound on coverage; it is a **saturation** line, 2 points above 7, not the 7 → 8 threshold |
| `QUALITY.md` R26 | `corpus/QUALITY.md:249` | requires the gap to be reported; defines no coverage bar |

Current coverage counters at this head, for the record (none of them is a threshold): frontier
**18/18 admitted** (`corpus/README.md`), frontier recheck harness **`entries=21 pass=21 exit=0`**
(`frontier-recheck-count.py --root .`), registry **52** rows (`corpus/SOURCES.md`), knowledge
**47** entries.

**Distance statement for coverage:** not computable — the threshold is undefined. The two channels
that exist do not meet: the counted channel is **0/20 present** and cannot move without operator
restoration of the domain roots; the moving channel (frontier admissions, 18/18, harness 21/21) is
declared a *separate denominator* and is not counted into the axis. Any claim of "coverage distance
1 point" or "distance 0" at this head would be invented.

**Concrete gap that is measurable and is not the score:** the province record lags the frontier by
one admission — `PROVINCE.md` names F01–F17 (`province_frontier_max: F17`, `F18` occurrences **0**)
while `corpus/README.md` admits F18 and `SCORECARD.md:1397` records it. That is proposal 5 of
`considerthese/2026-10-26.md` ("land the owed F18 `PROVINCE.md` amendment"), still owed at this head.
Round-36 C2 adds F19 on top, so the lag becomes two unless the amendment lands.

**Nudge status (measured, not acted on):** every axis must sit at/above the saturation line for the
stagnation nudge to waive the lowest-axis obligation (`AXES.md:66-73`); depth:verifiability is 4
against a line of 9/10, so **the nudge does not apply**. The capability window is at 2 of N = 3
completed rounds without an entry (last entry round 33, `SCORECARD.md:1222,1385`; rounds 34 and 35
entered none; round 36 pending).

## 5. Summary table

| axis | current | next | threshold recorded | concrete gap |
|---|---:|---:|---|---|
| depth:verifiability | 4 | 5 | **yes**, `SCORECARD.md:331` (`25/25 source chains` + `0 unsupported current claims`) | **24 gated chains of 47** + **9 failing anchor instances** (8 `BASE-ABSENT`, 1 `PAST-EOF`); 24 gated + 2 lost-base instances unreachable without operator restoration |
| coverage | 7 | 8 | **UNDEFINED** — no `Threshold for 8`, no coverage-bar sentence in `SCORECARD.md`, `corpus/QUALITY.md` or `PROVINCE.md`; nearest recorded bound is the saturation line 9/10 (2 points) | **not computable**; counted channel 0/20 present (frozen), moving channel (frontier 18/18) explicitly outside the axis. Measurable adjacent debt: `PROVINCE.md` lags the frontier (max F17, F18 absent) |
| depth:density (context, not this seat's item) | 9 | 10 | **UNDEFINED** as well — no `Threshold for 10`; the only bound is the same saturation line 9/10, which density already meets | n/a |

## 6. What this does not say

- No claim that round-36 C1's closure suite (`r36-closure.sh`) moves either bar. It is a
  defect-closure counter; a green `closed=9/9` can coexist with 24 gated chains and an undefined
  coverage threshold. Nothing here depends on its landing.
- No claim that round-36 C2's F19 admission moves coverage. By `corpus/README.md:217-223` the
  frontier is a separate denominator; the admission adds a row and a harness entry, not a score.
- No score change, no `SCORECARD.md` edit, no `corpus/QUALITY.md` edit, no instrument edit. The two
  in-flight claims' files were opened read-only.

## Report

Seat: `ExecScoreGap` (leaf, round 36). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`cc692008b0cfd58d18275aa6c4aed79620120799`, claims freeze `b47f2cdf17d9f6021cbdb4db1add09a9dbf4f1d6`.
No git/jj mutation, no network, no subagent, no lane write except this receipt.

### Commands, output, exit codes

All from the lane root unless stated; scratch `S=/fast/scratch/hyaku/kasegi-r36/ExecScoreGap`.

| # | command | output (summary) | exit |
|---|---|---|---|
| 1 | `git rev-parse HEAD` / `git status --porcelain \| grep -v '^?? \.ufo/waves/round-36/'` | `b47f2cdf…` / empty (tracked tree clean) | 0 |
| 2 | `python3 -B corpus/instruments/score-gap.py --root .` | `lines=47 executes=23 gated=24 broken=0 exit=0`; anchors `in-range=16 bad=0 lost-recorded=306 base-absent=0 exit=0`; census `134/1480 = 9.05 %`, `32/506 = 6.32 %`; threshold `SCORECARD.md:331`; `gap: 24 of 47` | 0 |
| 3 | `TMPDIR=$S/tmp python3 -B corpus/instruments/score-gap.py --selftest` | `fields=7 failures=0`, `no-write-a/b … unchanged=True` | 0 |
| 4 | `git archive b47f2cdf… \| tar -x -C $S/head`; then `score-gap.py --root $S/head` | identical gap line; recheck `exit=1`, `strict pass=1/47 cdroot_fail=46` | 0 (instrument) / 1 (its recheck field) |
| 5 | `recheck-audit.py --root <export> --quiet` vs `--root .` | export `strict pass=1/47 cdroot_fail=46 exit=1`; lane `strict pass=47/47 cdroot_fail=0 exit=0`; both `lines=47 pass=47 fail-closed=24` | 1 / 0 |
| 6 | `for f in corpus/knowledge/*.md corpus/*.md SKILL.md; do anchorcheck.py "$f"; done` | `files=51 green=46 red=5`, 9 failing instances (table §3) | 5×(1) |
| 7 | `python3 -B $S/gap-coverage.py --root $S/head` | §4 output; `coverage 7->8: threshold UNDEFINED` | 0 |
| 8 | `python3 -B corpus/instruments/frontier-recheck-count.py --root .` | `entries=21 pass=21 exit=0` (and identical on the export) | 0 |
| 9 | `grep -c 'Threshold for' SCORECARD.md corpus/QUALITY.md PROVINCE.md` | `1 0 0` | 0 |
| 10 | `git grep -nE "coverage 8\|score 8\|coverage.*8/10\|Threshold for 8" -- '*.md' ':!.ufo/'` | 2 hits, neither a threshold: `considerthese/2026-10-26.md:29`, `corpus/lessons/round-24-verifier-spotcheck.md:206` | 0 |
| 11 | tree digest of the export before/after both instruments | `5550a6cb…` both sides, `cmp` identical | 0 |

### File digests (lane head `b47f2cdf`)

`SKILL.md` `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc`;
`SCORECARD.md` `ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94`;
`corpus/QUALITY.md` `d4f83bb1206f5084e998d9449c9bef5af06674c325fb66709fe5fbec9d6e2b69`;
`PROVINCE.md` `b4bb5fee0a37cb2a81e351ee837a3e23fc64fbe002dfb25e4688d0ed4782ff91`;
`corpus/README.md` `277f04cedfb06f493ae5da636d665b490ac0e78b26ea282b0d0ef3a469d3ffa2`;
`corpus/SOURCES.md` `0f95a132a69e2708c86e019b648cd67ff0af28c326d9c3929f4203ec2902f6ba`;
`corpus/instruments/citation-survival.md` `795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d`;
`corpus/instruments/score-gap.py` `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf`;
`corpus/instruments/recheck-audit.py` `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09`;
`corpus/instruments/anchorcheck.py` `d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912`.

### Scratch cleanup

`/fast/scratch/hyaku/kasegi-r36/ExecScoreGap` (export + `gap-coverage.py` + captured outputs) is
removed after this receipt lands; `test ! -e /fast/scratch/hyaku/kasegi-r36/ExecScoreGap` → exit 0.
No scratch tree remains on disk.

### Tooling

No installs or upgrades this seat.

### Findings for the L1 (measurement only; not acted on)

1. **Coverage 7 → 8 has no recorded threshold anywhere in the lane.** Proposal 1's second branch is
   the true one for coverage: undefined, not merely unreachable. If the L1 wants a distance line,
   the bar has to be written first — and the r22 denominator cannot be reused as written
   ((20+18)/25 exceeds 100 %).
2. **`score-gap.py` is not export-portable in its recheck exit field** (46 `cdroot_fail` on a
   `git archive` root, `exit=1` where the lane prints `exit=0`). Its gap line is invariant. Cite the
   in-lane run, or pass a root whose path matches the payloads' `cd`.
3. **`PROVINCE.md` lags the frontier by one admission** (max F17; `F18` absent; `corpus/README.md`
   and `SCORECARD.md:1397` both record F18). Owed per proposal 5; round-36 C2 makes it two (F19).
4. **The census of record is stale by scope** (`134/1480 = 9.05 %` committed; r35 measured the live
   tree at 18.17 % with the entire rise `INTERNAL`, which the lane does not credit). The gap line
   does not depend on it.
5. The stagnation nudge is **not** available this round: depth:verifiability 4 is far below the
   9/10 saturation line, whatever the capability window says.

Report: .ufo/waves/round-36/wave1/ExecScoreGap.md
