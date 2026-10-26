# ExecScoreGap — distance to score 5 for `depth:verifiability` (round 35)

Read-only measurement mined from `considerthese/2026-10-25.md` proposal 2 ("track distance to the
next score, not just 'improved, held'"). **This is not a claim and asserts no score move.** No axis
score is changed here, `corpus/QUALITY.md` was not edited, and the only lane file written is this
receipt. Every figure below was produced by the command printed beside it; nothing is retyped from
another document.

## 1. The score-5 threshold, as recorded

| item | value |
|---|---|
| location | `SCORECARD.md:331` (the only line in the file containing `Threshold for 5`; `grep -c 'Threshold for 5' SCORECARD.md` → `1`) |
| verbatim | `Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims.` |
| context | the round-22 `depth:verifiability (C1, lowest axis)` row: `4` before, `**4**` after, "Improved, score held" |
| origin of the request | `considerthese/2026-10-25.md` proposal 2 quotes the same sentence as `SCORECARD.md:327`; the line has moved to 331 since that file was written (later round rows were appended above it) |

Reading of the bar (two conjuncts):

- **(A) every source chain passes** — at round 22 the audited set was the 25 legacy knowledge
  entries ("25/25"). Today every one of the **46** `corpus/knowledge/*.md` entries carries a
  `recheck:` line and `corpus/instruments/knowledge-expected.txt` pins that set
  (`expected=46`, `missing=0`, `unexpected=0`), so the analogue of `25/25` today is **46/46**.
- **(B) 0 unsupported current claims** — the bar sentence does not define "unsupported". The lane's
  own r22 application measured it as the fail-closed `recheck:` count (23 of 25 closed in r22). I
  therefore measure it on **both** limbs the lane owns: the `recheck:` limb (chains that cannot
  pass) and the anchor limb (`anchorcheck.py` fail classes, which since round 28 drive the exit
  code). Where the two disagree, §2d says so rather than picking the cheaper one.

## 2. Measured current facts

Snapshot of the lane bytes these numbers belong to — taken at **2026-10-26T06:35:28Z**:

| file | sha256 |
|---|---|
| `SKILL.md` | `0cc9563824328a762b3acf168fe719101a9164cf64e51fcc6cccb8a8a23b5190` |
| `SCORECARD.md` | `a0898ebe3eef09edfcf3afcafaef037bfc246484e7ce51548010cb7cbf195e05` |
| `corpus/QUALITY.md` | `807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8` |
| `corpus/instruments/citation-survival.md` | `795ba4f2801f6868b9e759ec82d2dcfb80cbee46af96380873506d744ca8036d` |
| `corpus/instruments/recheck-audit.py` | `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` |
| `corpus/instruments/anchorcheck.py` | `d0f35f8ccdcf995b78ea1403732fa90e12708b79bda21793002f7315b0e2a912` |
| `corpus/instruments/score-gap.py` | `57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf` |

`corpus/knowledge/*.md` count at snapshot: **46**.

**Concurrency disclosure (the tree moved while this seat measured).** `SKILL.md` was
`54137b6afd8b7403c3e07e3d33619dc7f646c6ad5fb967b953daae6a1f032053` at 06:33 and
`0cc95638…` at 06:35 (the D3 registry seat is editing it; `git status --porcelain SKILL.md` → ` M
SKILL.md`). `SCORECARD.md` likewise moved `31ebb1ea…` → `a0898ebe…` during the seat. All figures
below are from a single re-run at the digests above. The knowledge count is 46, not the 47 that
claim C2 declares for its after-state: `corpus/knowledge/cisa-kev-catalog.md` had not landed at
snapshot time. That is a wave-timing fact, not a finding against C2.

### 2a `anchorcheck.py SKILL.md` — the instrument of record for the anchor limb

```
$ python3 -B corpus/instruments/anchorcheck.py SKILL.md
== SKILL.md: 15 in-range cite instances, 0 bad; 15 distinct anchors; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1
BASE-ABSENT md:1097 S050.txt:70 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/S050.txt)
exit=1
```

- `bad=0` still holds (no `MISSING-FILE`/`PAST-EOF`/`OUTSIDE-BASE`), but the round-28 fail-closed
  rule makes `BASE-ABSENT=1` an exit-1 verdict, and **SKILL.md exits 1 today**. Round 28's landed
  record for this file was `BASE-ABSENT=0`, exit 0, so this is a **new red since round 28**.
- The failing token is a **spelling**, not a lost source: the capture exists in the lane at
  `corpus/source-snapshots/round-32/S050.txt` (31016 bytes; `sed -n '70p'` prints its line 70, so
  the anchor is in range — the content is Chinese-language policy text, and S050 is not this
  round's CISA row S052), and line 1084
  of the same file already cites it with the correct lane-relative prefix. The bare `S050.txt:70`
  sits inside the `r-defect-closure.sh` Gates & probes row at `SKILL.md:1097`; at the lane base
  `3266c99`, `git show 3266c99:SKILL.md | grep -cE 'r-defect-closure\.sh|kill-rule-check\.py'` →
  `0`, i.e. that row is new in this wave (D3's subject). Attribution to D3 is
  `[INFERENCE]` from those two facts; the red verdict itself is measured.
- `LOST-RECORDED=306` is the recorded-not-checked bucket: it never flips the exit code and is not
  counted as "unsupported" below, but it is named because a reader who equates "unsupported" with
  "not verifiable today" would get 306, not 1. The lane's own instrument does not count it.

### 2b Anchor sweep — `corpus/knowledge/*.md` + `corpus/*.md` + `SKILL.md`

```
$ for f in corpus/knowledge/*.md corpus/*.md SKILL.md; do python3 -B corpus/instruments/anchorcheck.py "$f"; echo "$f rc=$?"; done
files=50   exit_0=44   exit_1=6
```

The six red files, verbatim summary lines:

| file | summary line (verbatim) | exit |
|---|---|---|
| `SKILL.md` | 15 in-range, 0 bad; 15 distinct; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1 | 1 |
| `corpus/QUALITY.md` | 9 in-range, **1 bad**; 9 distinct; LOST-RECORDED=0 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=0 | 1 |
| `corpus/knowledge/citation-bases.md` | 10 in-range, 0 bad; 8 distinct; LOST-RECORDED=1 … BASE-ABSENT=1 | 1 |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | 0 in-range, 0 bad; 0 distinct; … BASE-ABSENT=1 | 1 |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | 0 in-range, 0 bad; 0 distinct; … BASE-ABSENT=5 | 1 |
| `corpus/knowledge/root-loss-2026-10-12.md` | 1 in-range, 0 bad; 1 distinct; … BASE-ABSENT=1 | 1 |

All ten failing instances, each classified by whether a lane copy of the cited base exists
(`find corpus/source-snapshots -name <basename>`):

| file | class | token as written | lane copy |
|---|---|---|---|
| `SKILL.md:1097` | BASE-ABSENT | `S050.txt:70` | `corpus/source-snapshots/round-32/S050.txt` |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md:55` | BASE-ABSENT | `S029.txt:20` | `corpus/source-snapshots/round-23/S029.txt` |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md:13` (×3), `:34`, `:43`, `:54` | BASE-ABSENT ×5 | `S041.txt:1868-1870`, `:1680-1681`, `:1792-1867`, `:1996-2079`, `:1868` | `corpus/source-snapshots/round-26/S041.txt` |
| `corpus/knowledge/citation-bases.md` | BASE-ABSENT | `~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` | none — true lost-base cite |
| `corpus/knowledge/root-loss-2026-10-12.md:61` | BASE-ABSENT | `queue.json:11-12` | none — true lost-base cite |
| `corpus/QUALITY.md:77` | PAST-EOF | `README.md:159` | resolves to lane-root `README.md` (14 lines) |

So of **10** failing anchor instances across **6** files: **7** are mechanically fixable today by
writing the lane-relative capture path (`S050`/`S029`/5×`S041` all exist in the lane), **2** are
genuine lost-base cites, and **1** is a `PAST-EOF` bare-name collision (`QUALITY.md`'s R13 row
quotes `README.md:159`; the bare token resolves to the 14-line lane `README.md`, not to
`corpus/README.md` or `corpus/instruments/README.md`). The `QUALITY.md` line is byte-identical at
base `3266c99`, i.e. the bad anchor predates this wave and only became exit-relevant when round 28
made the exit a verdict.

### 2c The `recheck:` limb — source chains that cannot pass

```
$ python3 -B corpus/instruments/recheck-audit.py --root "$LANE" --quiet
strict pass=46/46 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=22 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=46 total=46 pass=46 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=46 missing=0 unexpected=0 exit=0
exit=0
```

Independent check, not relying on the instrument's classification — every `recheck:` line extracted
and executed directly (`bash -c` on the line's own payload, lane-root cwd):

```
$ for f in corpus/knowledge/*.md; do line=$(grep -m1 '^recheck:' "$f" | sed 's/^recheck:[[:space:]]*//'); bash -c "$line" >/dev/null 2>&1; echo "$? $f"; done
entries=46   exit_0=22   exit_1=24   (no NO-LINE)
```

The two counters agree exactly: **22 of 46 chains pass; 24 cannot pass today; 0 are unparseable.**
All 24 are lost-base gated: 23 carry an inline `test -d ~/Projects/bounties` gate (some also
`test -d ~/Projects/the-bounty-hunter` / `~/Projects/origin-work`; `repo-git-state.md` gates on
`~/Projects/bounties/.git`), and 1 (`citation-bases.md`) has no `test` gate but runs
`anchorcheck.py` on itself, which exits 1 on its `~/Projects/the-bounty-hunter/ops/rank.mjs:55-58`
cite.

The 24 gated entries:

```
citation-bases.md claim-anatomy-sample.md claim-gates.md claim-package-contract.md
evidence-dir.md ev-model.md intake-and-finalize.md intake-surface.md mission-control.md
mission-ledger.md operator-queue.md ops-invariants.md policy-access-playbook.md
program-quirks.md repo-git-state.md retirement-autopsies.md source-tree-loss-2026-09-28.md
submitted-registry.md target-checkouts.md terminal-classes.md triage-thresholds.md
ufo-archive-2026.md ufo-workspaces.md vdp-disclosure-packages.md
```

The 22 that pass are the capture-backed entries (`ai-assisted-finding-validation`,
`authorised-testing-rules-of-engagement`, `authorization-safe-harbor-and-scope`,
`chinese-crowdsourced-testing-scope-and-rewards`, `cna-assignment-and-vulnerability-rules`,
`considerthese-proposals-ledger`, `coordinated-disclosure-timelines`,
`cra-manufacturer-reporting-duties`, `cvss-v4-severity-and-vector`, `cwe-top25-2025-methodology`,
`immunefi-vscs-v2-2-smart-contract-severity`, `iso-29147-and-30111-division-of-labour`,
`iso-29147-divergence-and-clause-crosswalk`, `japanese-domestic-disclosure-workflow`,
`japanese-severity-vocabulary-and-impact-model`, `multiparty-vulnerability-coordination`,
`program-severity-ladders-and-reward-scales`, `root-loss-2026-10-12`,
`statutory-authorization-and-unauthorized-access`, `vendor-disclosure-policies-as-corpus-objects`,
`vendor-disclosure-policy-commitments-crosswalk`, `vendor-third-party-finding-coordination`).

### 2d The two limbs disagree on three entries

Three entries **pass their own `recheck:`** and **still fail their own anchor gate**:

| entry | own recheck exit | failing anchors |
|---|---|---|
| `cra-manufacturer-reporting-duties.md` | 0 (`source-recheck.py … --source S029`) | `S029.txt:20` → BASE-ABSENT |
| `iso-29147-divergence-and-clause-crosswalk.md` | 0 (`source-recheck.py … --source S041`) | 5× `S041.txt:…` → BASE-ABSENT |
| `root-loss-2026-10-12.md` | 0 (four `test` clauses on the absent/present roots) | `queue.json:11-12` → BASE-ABSENT |

That matters for conjunct (B): a passing `recheck:` line does **not** imply the entry's prose
anchors are resolvable. The recheck limb's 22/46 counts chains, not claims. Measuring "0 unsupported
current claims" from `recheck-audit.py` alone therefore understates the anchor limb by these 3
entries (and misses `QUALITY.md`, which has no `recheck:` line at all).

### 2e `resolve.py` — live resolvability vs the committed census of record

`resolve.py <lane>` writes `citation-survival.md`/`.tsv` next to the script, so it was run from a
scratch copy to keep the lane read-only (`cp corpus/instruments/resolve.py $SCRATCH/lib/resolve.py;
python3 -B $SCRATCH/lib/resolve.py "$LANE"`). The lane census digest was `795ba4f2…` before and
after the run.

```
live (94 files scanned):  SKILL.md alone: 82/589 = 13.92%
                          corpus alone:   493/2521 = 19.56%
                          lane total:     523/2878 = 18.17%
                          classes: RESOLVES=32  MIRROR-EQUIVALENT=0  INTERNAL=491  GONE=2355
committed census (50 files scanned): SKILL.md alone 32/506 = 6.32%
                          corpus alone    118/1153 = 10.23%
                          lane total      134/1480 = 9.05%
```

Two measured facts, neither credited:

1. **The committed census is stale by scope**: it scanned 50 files/1480 distinct citations; the
   live tree has 94 files/2878. The lane rate moved 9.05 % → 18.17 %, but the entire numerator move
   is `INTERNAL` (491 vs 102 by subtraction); `RESOLVES` is **32 in both** runs and
   `MIRROR-EQUIVALENT` is 0 in both. Under the lane's own standing rule that internal-citation rise
   is not credited (r22 row: "resolver rise is all INTERNAL and **not credited**"), this is not
   score progress.
2. The definition travels with the number: numerator = `RESOLVES + MIRROR-EQUIVALENT + INTERNAL`,
   quoted from the census file itself.

### 2f The lane's own gap instrument (`score-gap.py`, landed r31)

```
$ python3 -B corpus/instruments/score-gap.py --root "$LANE"
recheck: lines=46 executes=22 gated=24 broken=0 exit=0
anchorcheck: in-range=15 bad=0 lost-recorded=306 origin=0 outside-base=0 base-absent=1 exit=1
threshold: SCORECARD.md:331 "Threshold for 5: a non-author audit passing 25/25 source chains and 0 unsupported current claims."
gap: 24 of 46 rechecks still gated on a lost base; score 5 needs 0 gated unsupported claims
exit=0
```

Its computed gap line equals this seat's independent counts (24 gated / 46 lines). Its gap line
covers conjunct (A) only; it does not read the anchor limb, which is red today (§2a–2b).

## 3. Gap statement

> **The score-relevant number today is X = 22 of 46 source chains passing (47.8 %; 24 gated, 0
> broken), with 6 of 50 swept files red on the anchor limb (10 failing instances: 9 BASE-ABSENT, 1
> PAST-EOF). The score-5 bar is Y = all source chains passing (46/46; the r22 analogue of `25/25`)
> plus 0 unsupported current claims. Gap = Z = 24 gated chains + 10 failing anchor instances across
> 6 files. No axis score changes; this is a measurement.**

Composition of Z, and what is reachable without operator action:

| component | count | reachable by a lane edit? |
|---|---|---|
| gated source chains | 24 | no — 23 gate on `~/Projects/bounties` (absent since 2026-09-28) and/or `~/Projects/the-bounty-hunter` (2026-10-12), 1 on the mirror cite in `citation-bases.md` |
| BASE-ABSENT anchor instances with a lane copy of the capture | 7 | yes, mechanically — write `corpus/source-snapshots/<round>/<Sxxx>.txt:LINE` instead of the bare name |
| BASE-ABSENT anchor instances with no lane copy | 2 | no — true lost-base cites (`ops/rank.mjs:55-58`, `queue.json:11-12`) |
| PAST-EOF anchor instance | 1 | yes — the bare `README.md:159` token needs its intended file spelled (`corpus/README.md`, 368 lines, or `corpus/instruments/README.md`, 960 lines) |

Distance trend, measured against the same bar: round 22 recorded **23 of 25** chains gated; today
**24 of 46**. The passing set grew 2 → 22 because the audited set grew with capture-backed entries,
while the gated count grew by 1. On the bar's own terms the distance was **not** closed: the
conjunct that matters (0 gated) is unchanged, and the anchor limb is red where round 28 left it
green for `SKILL.md`.

Structural ceiling, stated so the L1 can decide rather than infer: with both domain bases absent,
the 24 gated chains **cannot** pass, and no lane-side edit can flip them. Conjunct (A) is therefore
unreachable at this round's bytes by construction; only the operator restoring the roots, or a
declared redefinition of the counter, changes it. Conjunct (B) is reachable in part — 8 of the 10
anchor instances are lane-side fixes (7 prefixes + 1 spelled `README.md` path). Any such redefinition
or fix is a scoring/implementation decision above this seat; none was taken.

## 4. What this does not say

- No claim that C1's D1–D7 closure suite moves this bar. The suite is a **defect-closure** counter
  (`closed=7/7`); a green closure run can coexist with 24 gated chains — the two measure different
  things, and this report's numbers are independent of the suite's landing.
- No claim that the live resolver rate is progress (§2e: all `INTERNAL`).
- No edit to `corpus/QUALITY.md`, `SKILL.md`, `SCORECARD.md`, or any instrument. The r35 in-flight
  files were opened read-only; `corpus/instruments/citation-survival.md` and `.tsv` were not
  rewritten.

## Report

Seat: `ExecScoreGap` (leaf, round 35). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`.
No git/jj mutation, no network, no subagent.

### Commands, output, exit codes

All run from the lane root; scratch `S=/fast/scratch/hyaku/kasegi-r35/ExecScoreGap` (removed after
the receipt was written — see cleanup below).

| # | command | output (summary) | exit |
|---|---|---|---|
| 1 | `sha256sum SKILL.md SCORECARD.md corpus/QUALITY.md corpus/instruments/citation-survival.md corpus/instruments/recheck-audit.py corpus/instruments/anchorcheck.py corpus/instruments/score-gap.py` | digests in §2 | 0 |
| 2 | `ls corpus/knowledge/*.md \| wc -l` | `46` | 0 |
| 3 | `python3 -B corpus/instruments/anchorcheck.py SKILL.md` | `15 in-range, 0 bad; 15 distinct; LOST-RECORDED=306 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1` + `BASE-ABSENT md:1097 S050.txt:70` | **1** |
| 4 | `for f in corpus/knowledge/*.md corpus/*.md SKILL.md; do python3 -B corpus/instruments/anchorcheck.py "$f"; done` | `files=50 exit_0=44 exit_1=6`; the 6 listed in §2b | 6×(1) |
| 5 | `python3 -B corpus/instruments/recheck-audit.py --root "$LANE" --quiet` | `strict pass=46/46 … executes=22 gated=24 broken=0 … lines=46 total=46 pass=46 fail-closed=24 … expect=present expected=46 missing=0 unexpected=0` | 0 |
| 6 | per-entry `bash -c "<recheck payload>"` over 46 entries | `exit_0=22 exit_1=24` | 0 (loop) |
| 7 | `cp corpus/instruments/resolve.py $S/lib/resolve.py && python3 -B $S/lib/resolve.py "$LANE"` | `SKILL 82/589 = 13.92 %`, `corpus 493/2521 = 19.56 %`, `lane 523/2878 = 18.17 %`, classes `RESOLVES=32 MIRROR-EQUIVALENT=0 INTERNAL=491 GONE=2355` | 0 |
| 8 | `grep -nE '^- (lane total\|SKILL\.md alone\|corpus alone)' corpus/instruments/citation-survival.md` | `32/506 = 6.32 %`, `118/1153 = 10.23 %`, `134/1480 = 9.05 %` | 0 |
| 9 | `python3 -B corpus/instruments/score-gap.py --root "$LANE"` | gap line quoted in §2f | 0 |
| 10 | `grep -c 'Threshold for 5' SCORECARD.md` | `1` (line 331) | 0 |
| 11 | `git show 3266c9937b03062d9bbc2f436e20820115ed179c:SKILL.md \| grep -cE 'r-defect-closure\.sh\|kill-rule-check\.py'` | `0` (registry rows absent at base) | 0 |
| 12 | `git status --porcelain SKILL.md SCORECARD.md corpus/QUALITY.md corpus/instruments` | ` M SCORECARD.md`, ` M SKILL.md`, `?? corpus/instruments/r35-defect-closure.sh` | 0 |
| 13 | `grep -cE '^\| R26 ' corpus/QUALITY.md` | `0` (R26 row not yet landed at snapshot; the proposal-2 mining row is another seat's) | 1 |

### File digests

Inputs (see §2 table) plus the two files this seat wrote nothing to, checked unchanged across the
`resolve.py` run: `corpus/instruments/citation-survival.md` = `795ba4f2…` before **and** after.
This receipt: `.ufo/waves/round-35/wave1/ExecScoreGap.md`.

### Scratch cleanup

`/fast/scratch/hyaku/kasegi-r35/ExecScoreGap` (432 K, including `lib.QTvk/` written by the copied
resolver) was removed after this receipt landed; `test ! -e /fast/scratch/hyaku/kasegi-r35/ExecScoreGap`
→ exit 0. No scratch tree remains on disk.

### Tooling

No installs or upgrades this seat.

### Findings for the L1 (measurement only; not acted on)

1. `SKILL.md` anchor gate exits 1 at the wave snapshot because of a bare `S050.txt:70` token inside
   the new `r-defect-closure.sh` registry row (`SKILL.md:1097`, D3's file). The correct lane copy
   exists (`corpus/source-snapshots/round-32/S050.txt`); the owner can clear it by prefixing.
   Messaged to `ExecD3SkillRegistry`.
2. `corpus/QUALITY.md:77` (`R13` row, byte-identical at base) carries `README.md:159`, which the
   gate resolves to the 14-line lane `README.md` → `PAST-EOF`. Pre-existing; surfaced now because
   the exit is a verdict. Not edited (out of scope by instruction).
3. Conjunct (B) is not currently measured by the recheck limb alone: 3 entries pass their own
   `recheck:` while their prose anchors fail closed (§2d), and `QUALITY.md` carries no `recheck:`.
4. If the L1 wants a distance line in `SCORECARD.md`, the committed `score-gap.py` already prints
   one for conjunct (A); it would need an anchor-limb field to cover (B). Not changed this round.

## Addendum — re-measured after the D3 fix and the C2 entry landing (2026-10-26T06:38:56Z)

§2 above is kept **as measured at 06:35:28Z** and is not rewritten (append-only, the lane's R9/R18
convention). Two in-flight landings changed the tree during this seat, so the same commands were
re-run against the new bytes:

- **D3 prefixed the failing token** in the `r-defect-closure.sh` row: `S050.txt:70` →
  `corpus/source-snapshots/round-32/S050.txt:70`. New `SKILL.md` digest
  `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc`, 1104 lines (peer
  `ExecD3SkillRegistry`, message received after this seat's first yield: "Confirmed and fixed on
  SKILL.md … diff still append-only 13/0").
- **C2 landed** `corpus/knowledge/cisa-kev-catalog.md` (one `source: S052` line) and the expected
  list gained it: `corpus/instruments/knowledge-expected.txt` now has 47 entries,
  sha256 `d2e99ca60bc5acf109a60a26452379bc8d428ea0cb382f1e513696a7873347a8`.

| field | 06:35:28Z (§2) | 06:38:56Z (addendum) |
|---|---|---|
| `SKILL.md` | `0cc95638…` | `daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc` |
| `SCORECARD.md` | `a0898ebe…` | `51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7` (threshold still `SCORECARD.md:331`, same sentence) |
| `anchorcheck.py SKILL.md` | 15 in-range, `BASE-ABSENT=1`, exit **1** | **16 in-range, 0 bad, LOST-RECORDED=306, BASE-ABSENT=0, exit 0** |
| anchor sweep | 50 files: 44 green / 6 red, 10 instances | **51 files: 46 green / 5 red, 9 instances** |
| knowledge entries | 46 | 47 |
| recheck limb | 22 executes / 24 gated of 46 | **23 executes / 24 gated of 47**, `strict pass=47/47`, `expect=present expected=47 missing=0 unexpected=0 exit=0` |
| `score-gap.py` gap line | `24 of 46` | `24 of 47` |
| census of record | `795ba4f2…` | `795ba4f2…` (unchanged; not regenerated) |

**Transient, resolved, recorded:** at 06:38:11Z `recheck-audit.py` exited **1** with
`expected=46 missing=0 unexpected=1` (`unexpected=corpus/knowledge/cisa-kev-catalog.md`) because the
new entry landed before `knowledge-expected.txt` did; by 06:38:46Z the run prints
`expected=47 missing=0 unexpected=0 exit=0`. The completeness gate working is the point; this is not
a standing defect.

Remaining anchor reds at the addendum snapshot — 9 instances across 5 files (per-file instance
counts from `grep -cE '^(BASE-ABSENT|MISSING-FILE|PAST-EOF|OUTSIDE-BASE)'`):

| file | instances | class | lane-side fixable? |
|---|---|---|---|
| `corpus/knowledge/citation-bases.md` | 1 | BASE-ABSENT `~/Projects/the-bounty-hunter/ops/rank.mjs:55-58` | no — true lost-base |
| `corpus/knowledge/cra-manufacturer-reporting-duties.md` | 1 | BASE-ABSENT `S029.txt:20` | yes — prefix to `corpus/source-snapshots/round-23/S029.txt` |
| `corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md` | 5 | BASE-ABSENT `S041.txt:…` | yes — prefix to `corpus/source-snapshots/round-26/S041.txt` |
| `corpus/knowledge/root-loss-2026-10-12.md` | 1 | BASE-ABSENT `queue.json:11-12` | no — true lost-base |
| `corpus/QUALITY.md` | 1 | PAST-EOF `README.md:159` (14-line lane `README.md`) | yes — spell the intended file |

**Restated gap statement (supersedes §3's numerals; same method):**

> The score-relevant number today is **X = 23 of 47 source chains passing (48.9 %; 24 gated, 0
> broken)** with **5 of 51 swept files red on the anchor limb (9 failing instances: 8 BASE-ABSENT, 1
> PAST-EOF)**. The score-5 bar is **Y = all source chains passing (47/47) plus 0 unsupported current
> claims**. Gap = **Z = 24 gated chains + 9 failing anchor instances**, of which 6 anchor instances
> are lane-side fixes (S029 + 5×S041 prefixes), 2 are true lost-base cites, 1 is a PAST-EOF
> bare-name collision. No axis score changes; this is a measurement.

The §2a red is therefore **closed inside this wave** by its owner, not by this seat; the measured
finding and the fix are both on record. The structural ceiling is unchanged: the 24 gated chains
still cannot pass while `~/Projects/bounties` and `~/Projects/the-bounty-hunter` are absent, so
conjunct (A) remains unreachable without operator restoration or a declared counter redefinition —
a decision above this seat.

Report: .ufo/waves/round-35/wave1/ExecScoreGap.md

Receipt self-digest: `head -n -1 .ufo/waves/round-35/wave1/ExecScoreGap.md | sha256sum` = `7ec6c4d895251cbc25f624d4cd7bd8ca7ed0dbad4185cf33110dac7588f80af7` (only this final line is excluded; the digest covers §1–§4, the Report section and the addendum).
