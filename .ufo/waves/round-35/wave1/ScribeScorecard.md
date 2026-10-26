# ScribeScorecard — round 35, wave 1 (SCORECARD round-35 section)

Seat: `ScribeScorecard` (scribe, leaf of the round-35 L2 wave; this instance answered as
`ScribeScorecard-3`). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`3266c9937b03062d9bbc2f436e20820115ed179c`, claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`,
wave-1 spec/dispatch `da2d3c687f82a9814ee71c91c930cb733050d37c`. Wrote exactly two files:
`SCORECARD.md` (one append at EOF, 123 lines inserted / 1 replaced, the replaced line re-emitted at the
head of the insert) and this receipt. No git/jj mutation (read-only `log`/`diff`/`numstat`/`cat-file`
plumbing only), no subagent, no `agent://all`, no write outside the lane. No tool installed or upgraded
(nothing needed; no pacman/`uv tool`/`npx`/binary channel used, so the paused-pacman gate does not apply).

## Report

### 1. Pre-state and the integration stub (measured before the append)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && wc -l SCORECARD.md
1282 SCORECARD.md
$ sha256sum SCORECARD.md
085cffd60be1ad2fac07736e4bbe5c25fb06cace5bdda8707d75352e2575aaaa  SCORECARD.md
$ grep -n '^## Round 35' SCORECARD.md
1263:## Round 35 — frozen claims C1/C2 (2026-10-26)
$ git log --oneline -3
0aee0ef round-35: integration — lesson, scorecard, SHONEN, LOG, wave receipts, assimilation artifacts
aa6ad99 round-35: L1 integration — C1 D4/D6/D7 lands (results tracked + provenance, L1Integration correction, QUALITY supersessions)
da2d3c6 round-35: wave-1 spec + dispatch (64 seats, v2)
```

A 19-line `## Round 35` block already existed at `:1263-1281` (three table rows, a measurement-state line,
a move-log pair). It is **not this seat's text**: no wave receipt claims it (`grep -ln 'Round 35 — frozen
claims\|SCORECARD.md (append\|## Round 35' .ufo/waves/round-35/wave1/*.md` → only `ExecD2DensityRow.md`
and `ScribeIntegrationNotes.md`, both describing *their own* D2/LOG drafts), and it arrived with the L1's
integration commit `0aee0ef`. This seat appended the receipt-grounded section **after** it and stated the
reconciliation obligation in the section itself (§2 below), rather than editing another seat's committed
text.

Counters measured on that pre-append tree, exactly as the landed suite reads them:

```
$ grep -c 'filled by the L1' SCORECARD.md   → 1    (the stub's own closing sentence, :1271)
$ grep -c 'c1c6a5f' SCORECARD.md            → 3
$ grep -c '<LANE_HASH>' SCORECARD.md        → 0
$ bash corpus/instruments/r35-defect-closure.sh | tail -3
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=6/7 exit=1
```

So the integration commit had live-broken C1's marker clause (`claims.json` → C1
`counting_commands[2]`, literal must count 0; kill rule "… still present in SCORECARD.md"). I reported it
to `ExecD1Markers` (who was already on it) and did **not** edit the stub; the clause was reworded in place
by another seat before my append, and I re-measured: `placeholders=0`, suite `closed=7/7 exit=0`. The
episode is recorded in the section (§ "One C1 clause was broken and repaired inside this round") because
the repaired-only state hides the class.

### 2. What was appended (`SCORECARD.md:1284-1404`, 123 inserted lines, mirroring the round-34 section)

- `## Round 35 — frozen claims C1/C2 (2026-10-26)` preamble: `claims.json` digest + `frozen_at_utc`,
  base, claims-freeze, wave-1 spec/dispatch commit, 64-seat wave, the two committed do-nothing controls,
  the three frozen before-controls with digests, receipt inventory (60 seat receipts at read), the
  "last round heading at base is 34 ⇒ last-change column stays 34" sentence, and the subject sentence
  (D1–D7 closure; F18 / CISA KEV).
- **Stub-reconciliation paragraph** naming `0aee0ef…` and `SCORECARD.md:1263-1281`, stating that the stub
  is not this seat's text, that this section supersedes it, and that the stub's `depth:density` cell
  (`mean ≈ 201.2`) is contradicted by the landed 220.9 — the byte-bound split is in the guard row.
- Claims table, 6 columns, three rows — C1 `depth:verifiability` (before / after with all seven
  per-check payloads / verdict + evidence), C2 `coverage` (before / after / verdict + evidence),
  `depth:density` guard row (201.2 base blob → 220.9 landed, mechanism, no score move). Last-change
  `34 (held 35)` for C1/C2 and `r15 (held r35)` for density.
- Five bolded paragraphs: the broken-and-repaired C1 clause disclosure; `C1 blind spots` (CritC1Kill's
  five findings, the prose-placeholder limit, D2's byte-survival limb, the two reviewer findings that are
  fixed in the landed bytes, the lane-root trap, the bounded-oracle note); `C2 reviewer posture`
  (REFUSE→ADMIT verbatim on `e9de994d…`, `RevRowS052` "matches", CritC2Kill G5, the mutant kills, the two
  scope limitations incl. the 404 dispatch URL); `Measurement state` (17 digests, four named
  supersessions, the two non-append-only files); `Capabilities: no row enters this round`; `Saturation
  unchanged`.
- `### Round-35 move-log rows` (two rows, 5 columns).
- Closing line naming `aa6ad99…` and `0aee0ef…` as the integration commits and stating that the closing
  lane commit is not known at this seat's read and is not asserted — **no placeholder token is printed**.

### 3. Validation of the append (this seat's own reads)

```
$ wc -l SCORECARD.md ; sha256sum SCORECARD.md
1404 SCORECARD.md
ed6e931f795c070eda0b996654fd5c1cf7d9b118432e1ee7fee49173946fcd94  SCORECARD.md
$ git diff --numstat 0aee0ef105395a2f1d6ace7eaeef13871bb26988 -- SCORECARD.md
123	1	SCORECARD.md
$ git diff --numstat 3266c9937b03062d9bbc2f436e20820115ed179c -- SCORECARD.md
176	15	SCORECARD.md
```

176/15 vs base = D1's 33/15 (its two assigned in-place rewrites) + the stub's 19/0 + this append 123/1.
The single deletion in my hunk is the file's former last line (the stub's saturation sentence), which I
re-emitted at the head of my insert so the stub's text is preserved word-for-word.

Frozen-counter re-verification on the final bytes (the suite's own predicates, read with the suite's own
`grep -F`/regex forms):

```
filled by the L1        = 0      (grep -c → 0, exit 1)
<LANE_HASH>             = 0      (grep -c → 0, exit 1)
the L1 fills this line  = 0
c1c6a5f lines           = 4      (≥1 required; 3 inherited + 1 in my supersession sentence)
201.2 lines             = 6      (≥1 required)
round-34 depth:density row lines = 1
stale-row regex ^\| depth:density \| 9 \| mean \*\*201\.7\*\*, 25 blocks, 710 … = 1
```

Table shape (columns per row, `\|` inside cells does not split):

```
L1310 cells=6  | Claim | Axis | Before | After | Verdict and evidence | Last change |
L1311 cells=6  |---|---|---|---|---|---|
L1312 cells=6  C1 row
L1313 cells=6  C2 row
L1314 cells=6  depth:density row
L1394 cells=5  | Round | Axis | Before | After | Evidence |
L1395 cells=5  |---|---|---|---|---|
L1396 cells=5  round-35 depth:verifiability row
L1397 cells=5  round-35 coverage row
```

**One self-inflicted violation, caught and fixed before this receipt.** My first draft of the disclosure
paragraph quoted the stub's sentence verbatim, which re-introduced the D1 literal
(`grep -c 'filled by the L1'` → 1 at 1404 lines). I reworded it to "carried a lane-commit sentence that
reprinted the D1 placeholder verbatim" and re-measured 0. Recorded because the same trap is what the
stub fell into; `ExecD1Markers` warned me about it before I wrote, and I still hit it on the first pass.

### 4. Counter runs this seat performed (read-only; each value in the section that is mine)

The wave's rule reserves the round gate for the parent; I ran four commands because the section's C1/C2
rows claim the *current* state and I would not quote a receipt value that the integration commit had
already changed. All are read-only (the suite's plain run writes nothing; `--selftest` writes only under
`$KASEGI_SCRATCH`, which I pointed into my scratch tree):

```
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=3,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=1,provenance=1 open=0
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=0,correction-round-35=1 open=0
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
closed=7/7 exit=0                                          suite_exit=0

$ KASEGI_SCRATCH=$S bash corpus/instruments/r35-defect-closure.sh --selftest
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest judge=complete-report accepted=1
selftest_exit=0

$ python3 corpus/instruments/frontier-recheck-count.py | tail -4
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
PASS     F17  knowledge/immunefi-vscs-v2-2-smart-contract-severity.md ids=S051           exit=0
PASS     F18  knowledge/cisa-kev-catalog.md                        ids=S052           exit=0
entries=21 pass=21 exit=0

$ python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-35/manifest.json --source S052
S052:sha256 OK
S052:Q1 OK occurrences=1 anchor=2-ok
S052:Q2 OK occurrences=1 anchor=3-ok
S052:Q3 OK normalized=markup-whitespace occurrences=1 anchor=4-ok
S052:Q4 OK normalized=markup-whitespace occurrences=1 anchor=15472-ok
S052:Q5 OK normalized=markup-whitespace occurrences=1 anchor=19165-ok
recheck_exit=0
```

Every other number in the section is quoted from the named seat receipt (§5). I ran **no** census, no
mutation battery, no base-export run and no re-review; those remain the cited receipts' evidence.

### 5. Value provenance (every number in the section, mapped to its source)

| Section value | Receipt / file of record |
|---|---|
| `claims.json` `fe0dae89…`, `frozen_at_utc`, attempt 1; before-controls `352d3da2…` / `28357003…` / `74fc6a26…`; fake suite `292aaac0…`; junk twin `0abec359…` | this seat's `sha256sum` on `.ufo/waves/round-35/`; `ExecBeforeReceipts` §2; `ScribeIntegrationNotes` Report 1 |
| C1 before-column (suite absent `ls_exit=2`, placeholder 1 + second spelling 1, `c1c6a5f` 0, `201.7` 2 / `201.2` 0, D3 0/0, tracked 0, note 0, D5 absent, D6 1/0, D7 0 0) | `.ufo/waves/round-35/c1-controls/before.txt`; independently reproduced 12/12 by `RevC1BeforeAfter` §2 |
| C2 before-column (17 / 51 / 0 / 0 / `entries=20 pass=20` / `manifest UNAVAILABLE` exit 2 / 46) | `.ufo/waves/round-35/c2-controls/before.txt`; reproduced cell-for-cell on a do-nothing export by `MutCounterBase` and `ExecDoNothingReject` §2a |
| suite `0ae4b484…`, 834 lines, 7 checks, 17 clause mutants, base `closed=0/7 exit=1`, all-fixed tree `7/7` + `cases=7 failures=0`, fake rejected, `judge=complete-report accepted=1`, digest chain `c748dd70…`→`cba8c95b…`→`d7ad8438…`→`a4f80067…`→`0ae4b484…` | `ExecClosureSuite` §1–§11; `RevClosureSuite`; `RevSelftestFixtures`; `MutClosureSuite` (14/14 vacuous+delete killed); `MutFixturesLimbs` |
| the seven landed payloads + `closed=7/7 exit=0` + `--selftest cases=7 failures=0` | **this seat's own runs** (§4), on the final bytes |
| D1 markers 0/0, `c1c6a5f` ×3, appended `Correction (round 35)`; the stub episode (`placeholders=1` → `closed=6/7 exit=1` → repaired) | `ExecD1Markers` §2–§4; this seat's pre-append and post-repair runs (§1, §4); `RevD1D2` (its own churn read: 2 mid-edit, 0 after) |
| D2 erratum + measurement-state paragraph, `201.7`=`git show 206e510:SKILL.md` (`b11b6085…`, 1090 lines), `201.2`=`3266c99:SKILL.md` (`ba5ebe5d…`, 1091 lines), `row-bytes=1` byte survival | `ExecD2DensityRow` §2–§4; `RevD1D2`; `ExecClosureSuite` §2 |
| D3 rows `SKILL.md:1097-1098`, greps 4/4, `13 0`, section heading | `ExecD3SkillRegistry` §2–§5; `RevD3D4`; `RevC1BeforeAfter` §4 |
| D4 `tracked=1,provenance=1`, results `3afa3581…` 312874 B, note `e1c44301…` 5639 B, the 3 min 48 s after-`complete` offset | `ExecD4ResultsTrack` §1–§4; `ScribeIntegrationNotes` Draft B; `RevD3D4`; `RevC1BeforeAfter` §6 |
| D5 erratum `discriminating invocation` ×5, `per-id occurrences` ×5; digests `e2e7202d…` → `0d304b92…` → `eee0bb57…`; C2→`C1.after[10]` attribution correction | `ScribeErratumD5` §3–§5, §8; `RevD5D6D7` F5; `CritC1Kill` §7 (its own read `0d304b92…`); this seat's `sha256sum` (`eee0bb57…`) |
| D6 dead-seat sentence 0 / `Correction (round 35)` 1; in-place shape with 3 deletions, forced by the `== 0` clause | `RevD5D6D7` §shape nuance; suite D6 payload; this seat's read |
| D7 `supersedes R22` 1 / `supersedes R23` 1, QUALITY 250 lines `d4f83bb1…`, R26/R27 rows | `ScribeQualityDraft` §1–§3; `ExecClosureSuite` §3; this seat's `grep -c` + `sha256sum` |
| C2 after (frontier 18 `28 0`, registry 52 `5→7`, S052 row `:58`, entry `e9de994d…` 91 lines, capture `d69349e8…` 1479694 B / 27870 lines, manifest `06bfcc71…` 5631 B, knowledge 47, `knowledge-expected.txt` `d2e99ca6…`, census exit 0 W04 S028/S029) | `ExecC2Capture` §2–§6; `ExecRegistryAppend` post-append block; `ScribeEntryF18` R1–R5; `ExecExpectedListSync` §3–§4; `ExecDoNothingReject` §2b; `RevC2BeforeAfter`; `RevRowS052`; this seat's `grep`/`wc`/`sha256sum` |
| harness `entries=21 pass=21` incl. `PASS F18 … ids=S052`; recheck exit 0, five assertions `occurrences=1` | **this seat's own runs** (§4); `ExecExpectedListSync` §4; `ExecDoNothingReject` §2b/§3a |
| junk twin: 0/0 occurrences, `MISMATCH reason=quote-not-found` exit 1, no row / no entry / refusal on record | `ScribeErratumD5` §3 (E1, N1), §6 item 4; `ExecDoNothingReject` §3; `MutJunkTwin`; `RevEntryF18` |
| REFUSE (Q2, Claim 4b only) → **ADMIT** Q1–Q10 on `e9de994d…`; `RevRowS052` "matches"; CritC2Kill G5 | `RevEntryF18` §1, §3, final-verdict line; `RevRowS052` verdict; `CritC2Kill` §Verdict, G5 |
| MutC2Entry M1/M2a/M4 killed | `MutC2Entry` §table (M1 harness `no-source-line` exit 1; M2a `quote-not-found` exit 1; M4 exit 1) |
| CritC1Kill verdict (survives 1(a)/base/4-literal; not 1(b)/2/3/4-with-mention/5), F-1…F-5 | `CritC1Kill` §5, §Verdict |
| density 201.2 / 25 / 711 (`ba5ebe5d…`, 1091 lines) vs 220.9 / 26 / 742 (`daeff71b…`, 1104 lines), block 26 dens 712.5, `anchorcheck` 16 in-range / 0 bad / LOST-RECORDED=306 / other classes 0 exit 0, `density.py` `ee803726…`, `anchorcheck.py` `d0f35f8c…`, the `BASE-ABSENT=11` copy trap | `ExecNoHarmFinal` §1–§3, F6; `RevNoHarm` §B, §item 2; `ExecD2DensityRow` §5 |
| numstat table (`SKILL.md 13 0`, `PROVINCE.md`/`LOG.md` unchanged, `README 28 0`, `SOURCES 7 0`, `knowledge-expected 1 0`, `SCORECARD 33 15`) and the 15-deletion attribution | `RevNoHarm` §A, §A.1; `ExecNoHarmFinal` §3 |
| 60 seat receipts | this seat's `ls .ufo/waves/round-35/wave1/*.md \| wc -l` |

### 6. Findings for the L1 (this seat does not judge the round)

1. **The integration commit broke C1's marker clause and it was repaired inside the round.** At
   `0aee0ef…` the stub's closing sentence reprinted the D1 placeholder, `grep -c` = 1, suite
   `closed=6/7 exit=1`. Repaired in place by a peer seat; measured 0 and `closed=7/7 exit=0` at my
   append. **Two artefacts must not ship:** the repaired state is what the counters see, but the class
   (a lane-commit sentence quoting the placeholder) is the same one D1/R1 filed, and the section says so.
2. **Two `## Round 35` headings now exist** (`:1263` the stub, `:1284` this section). The closing commit
   is the reconciliation point: deleting the stub also removes its stale density cell
   (`mean ≈ 201.2` for a landed 220.9) and its move-log rows, which my rows supersede. If the L1 keeps
   the stub instead, its density cell needs the 220.9-landed / 201.2-base-blob split — reported by
   `ExecD1Markers` too, and neither of us edited it.
3. **`SCORECARD.md` is not append-only this round** (33/15 vs base before my append; 176/15 after). The
   15 deletions are D1's two assigned in-place placeholder rewrites; the section records the deviation
   and its attribution rather than hiding it behind `numstat`.
4. **D2's "no deletion" limb is a byte-survival test, not a git check** (`ExecClosureSuite` §2, finding
   4): a judge that insists on a literal `git diff --numstat` deletion count would lose one of D2's three
   clauses in a git-free export or a fixture tree. Named in the blind-spots paragraph, not filed as a
   failure.
5. **CritC1Kill's F-1 is the one live gap C1's predicate does not close:** nothing binds the counter's
   own bytes, so "proved by the suite's own `--selftest`" is discharged by the artifact under test. A
   one-command digest pin is the smallest safe correction; whether it lands this round is the L1's call.
   The other four findings are check-level literal-grep limits, recorded.
6. **The C2 dispatch URL 404s.** `https://www.cisa.gov/known-exploited-vulnerabilities.json` returns a
   46916-byte HTML error page under three user agents; the captured feed is
   `…/sites/default/files/feeds/known_exploited_vulnerabilities.json` (200, `application/json`), and every
   landed byte (row, manifest, entry) carries that path. The section states it as a scope limitation.
7. **`RevEntryF18`'s ADMIT binds `e9de994d…`, not the digest any earlier receipt quotes** (`da81204b…` →
   `e3f233c0…` → `e9de994d…`). The section cites the ADMIT digest; the entry's own scribe receipt quotes
   the first, which is PRE-STATE and is not used as a value.
8. **No placeholder token was introduced.** The closing line names the two integration commits and says
   the closing lane commit is not known at this seat's read and is not asserted; the file's
   `filled by the L1` and `<LANE_HASH>` counts are both 0 on the final bytes.

### 7. Limits of this section

- Every value is either quoted from a named seat receipt (§5) or produced by one of the four read-only
  commands in §4. This seat ran no census, no base-export suite run, no mutation battery and no
  re-review.
- The `SCORECARD.md` digest `ed6e931f…` (1404 lines) is a point-in-time value in a live working tree that
  moved twice during this seat's run (1282 → 1290-class reads by peers → my 1404); no counter in the
  section reads it.
- The closing commit will change the file again (receipts, `LOG.md`, `SHONEN.md`,
  `corpus/lessons/round-35.md`, stub reconciliation), none of which any counter above reads.
- Line numbers in the section's citations are as-of-write; the frozen counters it names are
  line-number-independent (`grep -c`, `git ls-files`, file presence).

### 8. Scratch and tooling

Scratch `/fast/scratch/hyaku/kasegi-r35/ScribeScorecard/` was created (`mkdir -p`) to hold the
`--selftest` scratch root and one captured run log (`st.txt`, 3240 B); the suite removes its own tree on
return, and the whole directory was deleted before this receipt was finalised:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r35/ScribeScorecard; echo "rm_exit=$?"
rm_exit=0
$ test -e /fast/scratch/hyaku/kasegi-r35/ScribeScorecard && echo PRESENT || echo scratch-absent
scratch-absent
```

No tool installed or upgraded. Tools used: `bash`, `coreutils` (`sha256sum`, `wc`), `grep`, `git`
(read-only), `python3` (stdlib only). No pacman transaction attempted (host-wide pause).

Report: .ufo/waves/round-35/wave1/ScribeScorecard.md
