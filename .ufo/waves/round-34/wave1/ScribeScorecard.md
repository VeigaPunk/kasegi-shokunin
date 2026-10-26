# ScribeScorecard — round 34, wave 1 (SCORECARD round-34 section)

Seat: `ScribeScorecard` (scribe, leaf of the round-34 L2 wave; this instance answered as
`ScribeScorecard-2`). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base
`014ee2d7aa8c3c095ff57ae51097606a9906228c`, claims-freeze `29f606dbdd28aff6fd4573ab4b90788bbb90af13`.
Wrote exactly two files: `SCORECARD.md` (one append at EOF, 124 lines) and this receipt. No git/jj
mutation (read-only `git diff`/`git show` plumbing at most), no subagent, no `agent://all`, no write
outside the lane, no counter run (values come from seat receipts; running the round gate is the L1's
step). No tool installed or upgraded.

## Report

### 1. Pre-state (measured before the append)

```
$ wc -l SCORECARD.md
1119 SCORECARD.md
$ sha256sum SCORECARD.md
b8fc8c66619cf4f3d390b133f97644e29fb8a0135e4c528952fbec70353389c0  SCORECARD.md
$ grep -c '<LANE_HASH>' SCORECARD.md
0
grep_exit=1
$ grep -n '^## Round' SCORECARD.md | tail -3
982:## Round 33 — frozen claims C1/C2 (2026-10-26)
1074:## Round-33 capabilities
   (no round-34 heading)
$ tail -3 SCORECARD.md
final hash `7963976e60b2564860553c6ab4838128d5ca06ea` (lane tip `014ee2d7aa8c3c095ff57ae51097606a9906228c`
after the verifier spot-check commit); the placeholder token no longer occurs in this file, and
the round-34 closure check R1 reads that count as 0.
```

The tail is `ExecScorecardMarkers`' R1 correction and `ExecErratum2`' block sits above it; the append
goes after both, so neither sibling's text moved.

### 2. What was appended (`SCORECARD.md:1121-1243`, 124 lines, mirroring the round-33 section)

- `## Round 34 — frozen claims C1/C2 (2026-10-26)` preamble: base, claims-freeze, wave-1 spec commit
  `206e5108…`, frozen controls, receipt inventory (`wave1/` 58 seat receipts at read), the
  "last round heading at base is 33 ⇒ last-change column stays 33" sentence (the round-33 section's
  own device), and the subject sentence (R1–R9 closure; F17).
- Claims table, 6 columns, three rows — C1 `depth:verifiability` (before/after/verdict), C2
  `coverage` (before/after/verdict), `depth:density` guard row (before/after/verdict, `r15 (held
  r34)`), last-change `33 (held 34)` for C1/C2.
- Five bolded paragraphs: `Erratum 1` disclosure (`records=41` + PRE-STATE labellings), `C2 predicate
  wording` disclosure (16×`occurrences=1` + Q9/Q17 `occurrences=2` anchored), `C1 blind spots`
  (recorded, not filed), `C2 reviewer posture` (verbatim ADMIT / holds / "gate is not
  provenance-sound"), `Measurement state` (digests + named supersessions + the fleet-root artefact
  reported by `RevNoHarm` §D).
- `Capabilities: no row enters this round` — the round-33 row's "11-case `--selftest`" literal is
  superseded by the landed **23 cases**, recorded as a note per the L1's integration message instead
  of editing the round-33 row; `Saturation unchanged` (9/10, N=3, window not restarted).
- `### Round-34 move-log rows` (two rows, 5 columns: Round/Axis/Before/After/Evidence).
- Closing line: final lane commit left to the L1 **without any placeholder token** (see §5.7).

### 3. Validation of the append (this seat's own reads)

```
$ grep -c '<LANE_HASH>' SCORECARD.md ; echo "grep_exit=$?"
0
grep_exit=1
$ python3 -  # column count per appended table row
1141 6 ['Claim', 'Axis', 'Before', 'After', 'Verdict and evidence', 'Last change']
1142 6 ['---', '---', '---', '---', '---', '---']
1143 6 ['C1', 'depth:verifiability (lowest ', 'suite absent (`ls_exit=2`); ', '`bash corpus/instruments/r-d', '**Verified, score held 4.** ', '33 (held 34)']
1144 6 ['C2', 'coverage (7)', '`frontier_admitted=16`; regi', 'frontier admitted **17** (ap', '**Verified on every frozen C', '33 (held 34)']
1145 6 ['depth:density', '9', 'mean **201.7**, 25 blocks, 7', 'mean **201.7**, 25 blocks, 7', '**Unchanged (held 9), no har', 'r15 (held r34)']
move-log rows: 1235-1238 each 5 columns
$ wc -l SCORECARD.md ; sha256sum SCORECARD.md
1243 SCORECARD.md
efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91  SCORECARD.md
$ git diff --numstat 014ee2d7aa8c3c095ff57ae51097606a9906228c -- SCORECARD.md
155	3	SCORECARD.md
```

155 inserted / 3 deleted vs base = `ExecScorecardMarkers` 8/3 (two marker lines + correction) +
`ExecErratum2` 23/0 + this append 124/0. This seat deleted no line.

### 4. Value provenance (every number in the section, mapped to a receipt)

| Section value | Receipt / file of record |
|---|---|
| before-column C1 (suite absent `ls_exit=2`, `cases=11`, two survivors, markers 2, `-03:00` ×2, `records=1 paths=['S041.txt']`, R20 ×1, rule A one-directional, `c2-controls/` absent) | `.ufo/waves/round-34/c1-controls/before.txt`, `c2-controls/before.txt`; base audit `40/40/0` by `RevC1BeforeAfter` §1 B8; marker count 2 by `ExecScorecardMarkers` §1 |
| before-column C2 (frontier 16, rows 50, S051 0, citing 0, harness 19/19, recheck exit 2, knowledge 45, census exit 0 W04 S028/S029) | `.ufo/waves/round-34/c2-controls/before.txt`, `census-before.txt`; independently reproduced by `RevC2BeforeAfter` §0b |
| `closed=9/9 exit=0`, `selftest cases=9 failures=0`, base `closed=0/9 exit=1`, fake-suite control | `ExecRDefectClosureSuite` §3–§6 (final bytes `357a7e49…`, 688 lines — same digest this seat measured); `RevClaimsFreeze` §3 row 1/2; `RevRSuite`; `MutRSuiteChecks` "18/18 killed" |
| `selftest cases=23 failures=0`, nine new case names, `3d9e5e0d…` | `ExecCaptureBindingHarden` §2, §6; `MutSelftestSummary` §1; `CritC1Kill` |
| `records=41 bound=41 unbound=0 exit=0`, `orphans=1`, `multi_row_url=2`, `missing_manifest=0`, 10 dirs | `ExecCaptureBindingHarden` §Addendum; `ExecRegistryAppend` §5; `ExecCensusAfter` |
| erratum 1 ruling (`bound=records`, PRE-STATE labels) | `.ufo/waves/round-34/claims-erratum-1.md`; `RevClaimsFreeze` D-1 |
| `survivors=0`, `mutants=3 killed=3`, `gates=7 failed=0`, `controls=4 rejected=4`, `c279d952…` | `ExecKillRuleCheck` §3, §11; `MutKillRuleMutants` §11; `RevClaimsFreeze` §3 row 4 (an earlier `gates=6` generation, named in `ExecKillRuleCheck` §0) |
| markers 0 + `Correction (round 34)` naming `7963976e`/`014ee2d` | `ExecScorecardMarkers` §2–§4 |
| round-32 strict-UTC stamps, `72ab4e68…` | `ExecManifestR32Normalize` §2–§3; `MutManifestField` |
| round-26 `orphans` declaration, `33ac33c3…`, purpose corrected | `ExecS040Orphan`; `ExecCaptureBindingHarden` §3; `RevOrphan` |
| QUALITY R20 note + R22/R23/R24, `77d99df9…` | `ExecQualityAppends` §2; `ExecRDefectClosureSuite` §8 |
| R7 erratum (`:140`) and R4 erratum (`:215`), `f69472f3…` | `ExecLessonErrata` §0–§2; `RevErrata` |
| rule A bidirectional `1be79af6…`, both limbs killed | `ExecFrontierBidirectional` §3–§7; `MutFrontierRuleA` §5–§9 (`1be79af6…` FINAL) |
| junk twin `2752a994…`, committed at `29f606d`, rejected via reviewer-built manifest | `RevJunkTwin` §1–§4; `c1-controls/fake-controls-receipt.txt` |
| frontier 17, registry 51, S051 row 1, citing 1, harness 20/20 + `PASS F17`, knowledge 46 | `ExecHarnessAfter` §4, §6, §8; `ExecRegistryAppend` §4; `RevCensus` §2–§3; `RevC2BeforeAfter` counters 1–5; `ExecRegressionC2` |
| `source-recheck S051` 18 assertions OK, 16×`occurrences=1`, Q9/Q17 `occurrences=2` anchored, exit 0 | `ExecSnapshotR34` §4; `ExecRegistryAppend` §5; `RevClaimsFreeze` D-2; `RevC2BeforeAfter` counter 6 |
| census exit 0 (W04 S028/S029 only) + six-command battery | `ExecCensusAfter`; `RevCensus` §2–§3; `ExecRegistryAppend` §2, §4 |
| C1 blind spots (summary-line rewrite, provenance, all-orphan dir, R1 spelling, report-verifier limb, bounded probe set, presence tests) | `CritC1Kill` §3, §4, §5, §Additional states; `ExecRDefectClosureSuite` §11; `ExecCaptureBindingHarden` §Peer finding |
| C2 gaps G1–G5, verdict wording | `CritC2Kill` §8–§Verdict; `RevClaimsFreeze` §5 (G5/kill-rule clause) |
| ADMIT on `948b202e…` (earlier `e71fbcd9…` superseded) | `RevEntryF17` §Verdict, head |
| row/bullet/R8 review **matches** | `RevRowS051` verdict + §1 |
| depth:density `201.7 / 25 / 710`, 1090 lines, anchorcheck classes, `SKILL.md` byte-unchanged | `RevNoHarm` §A–§C (this seat re-read `SKILL.md` `b11b6085…`, 1090 lines, absent from `git diff --numstat 014ee2d7` — exit 0, no output) |
| fleet-root artefact `baseline-plain.txt` `56f08a92…` | `RevNoHarm` §D finding 1 |

### 5. Findings (for the L1; this seat does not judge the round)

1. **C2's frozen predicate literal is false on two of eighteen assertions.** 16 print
   `occurrences=1`, Q9/Q17 print `occurrences=2` under verified anchors, exit 0. The kill rule
   (`exit != 0`) is unaffected. Section reports the measured shape and names the recommended appended
   erratum (`RevClaimsFreeze` D-2). No claims file was edited.
2. **C2's junk-twin kill clause has no executable form as phrased.** The twin's own `recheck:` line
   exits 0 (it names the real manifest), and part of its quoted sentence is real text at
   `S051.txt:75` (`RevClaimsFreeze` §5, `CritC2Kill` G5, `ExecHarnessAfter` §7 F-B). Section states
   the rejection route (reviewer-built manifest `MISMATCH reason=quote-not-found`, exit 1, +
   non-admission) rather than the clause.
3. **C1 after-state uses erratum 1's invariant, not the frozen literal.** `records=41 bound=41
   unbound=0 exit=0`; the two intermediate `records=41 bound=40 unbound=1` and `cases=11` readings are
   labelled PRE-STATE in the section, per the L1's integration instruction.
4. **`ExecNoHarmFinal` had not landed at this seat's read** (`ls` → No such file). The depth:density
   guard row therefore cites `RevNoHarm` §A–§C, the independent reviewer, and says so in the cell.
   If `ExecNoHarmFinal` lands with conflicting density numbers, the L1 must reconcile before commit.
5. **Supersessions recorded, not compared:** `frontier-recheck-count.py` `87b14892…` → `8a79010d…` →
   `1be79af6…` (docstring/README-reference only; verdicts stable at both later digests);
   `QUALITY.md` `2bb724fb…` → `77d99df9…` at the same 228 lines inside its own appended block (R24's
   `grounded in` line cites `:174-176` now, `:173-175` in `ExecQualityAppends` §2);
   `r-defect-closure.sh` `7aca98b3…` (quoted by `RevClaimsFreeze`/`RevC1BeforeAfter`, whose R8
   descriptor is the pre-parse generation) → `357a7e49…` final, matching
   `ExecRDefectClosureSuite`'s run; `kill-rule-check.py` seven generations, final `c279d952…`;
   entry `e71fbcd9…` (PRE-STATE) → `948b202e…` (reviewed).
6. **Capability handling per the L1's message:** no new row; the round-33 row's "11-case" literal is
   superseded by `selftest cases=23 failures=0`, recorded as an appended note, master table untouched.
7. **No placeholder token was introduced for the final lane commit.** Round-33 R1's defect was a
   published placeholder and C1's counter reads that count as 0; the closing line therefore names the
   L1's obligation in prose and carries no token. `grep -c` for the token after the append is `0`
   (exit 1), i.e. the C1 marker clause is not re-opened by this section.
8. **Not adopted, reported:** `RevNoHarm` §D found `/home/vgpnk/Projects/shokunin/baseline-plain.txt`
   (850 B, untracked, `56f08a92…`) written at the read-only fleet root during the wave. It appears in
   § Measurement state as an observation about a foreign surface, not as a claim value; correcting the
   write is outside this seat's scope.
9. **`wave1/` held 58 seat receipts** at read; `ExecNoHarmFinal`, `ExecRegressionC1` (a
   `RevC1BeforeAfter`/`ExecRegressionC2` pair covers the same ground) and `SimplifierCleanup` output
   were absent. The section cites only receipts that existed.

### 6. Limits of this section

- Every counter value is quoted from a seat receipt; this seat ran no gate (suite, kill-rule, harness,
  census, `source-recheck`) and performed no re-review. Its own commands were `wc`, `sha256sum`,
  `grep`, `git diff --numstat` (read-only) and one Python structural read of the appended table.
- The `SCORECARD.md` digest recorded here (`efa646c8…`, 1243 lines) is a point-in-time value in a live
  working tree; no counter in the section reads it.
- The closing commit will change the file again (receipts, `LOG.md`, `SHONEN.md`, `corpus/lessons/round-34.md`),
  none of which any counter above reads.

### 7. Scratch and tooling

Scratch `/fast/scratch/hyaku/kasegi-r34/ScribeScorecard` was created empty, never written, and is
removed before yield (`rm -rf`, absence verified in the closing run). No tools installed or upgraded
(no `pacman`, `uv tool`, `npx`, no binary fetched); stdlib `python3`, `grep`, `sha256sum`, `wc`, `git`
read-only.

Report: .ufo/waves/round-34/wave1/ScribeScorecard.md
