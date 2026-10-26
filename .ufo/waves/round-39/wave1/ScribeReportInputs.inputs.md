# Round-39 report input pack (drafting input only — the L1 writes the report)

Assembled by seat `ScribeReportInputs` at 2026-10-26T19:34Z from `.ufo/waves/round-39/claims.json`
(8942 B, sha256 `e427ab6a6ecec4b1f49ed5eed95860c468e0982af331a3a1ba135649d27e051c`) and the four
committed before-controls. Row tags: **[m]** measured by this seat at pack time; **[c]** verbatim from
a committed before-control; **[t]** frozen claim target — not measured, because the judged head J and
`.ufo/waves/round-39/final-gates/` do not exist yet (`ls` → `No such file or directory`).

## 1. C1 — depth:verifiability (frozen score 4, held 4)

Frozen counting commands, verbatim from `claims.json`:

```sh
C1.1  bash corpus/instruments/r39-closure.sh --export-ref <J> -> closed=8/8 exit=0
C1.2  bash corpus/instruments/r39-closure.sh --selftest --export-ref <J> -> selftest cases=8 failures=0 exit=0
C1.3  bash corpus/instruments/r39-closure.sh --export-ref 480b1a505a2dfc14a4f718d16d63808247214d0a -> closed<8/8 exit=1
C1.4  bash corpus/instruments/r39-closure.sh --export-ref 66703aca50529a35be49aa8759d04140720ad -> closed<8/8 exit=1
C1.5  bash corpus/instruments/r39-closure.sh -> exit 2 (plain run refused)
```

Before → after:

| # | Before | After (frozen target) |
|---|---|---|
| C1.1 | **[m]** no r39 instrument at base: `git cat-file -e 480b1a5…:corpus/instruments/r39-closure.sh` → `fatal: path 'corpus/instruments/r39-closure.sh' does not exist in '480b1a505a2dfc14a4f718d16d63808247214d0a'` (exit 128); `r37-closure.sh` and `r38-closure.sh` both present at base (`cat-file -e` exit 0). **[c]** `c1-controls/before.txt`: `ls: cannot access 'corpus/instruments/r39-closure.sh': No such file or directory` | **[t]** `closed=8/8 exit=0` on J |
| C1.2 | **[c]** no graded r39 selftest exists; r38 suite carries 25 surviving source mutants (`MutG1G2 19, MutG3G4 2, MutG5G8 4`) | **[t]** `selftest cases=8 failures=0` with eight graded `selftest case=G<n> … positive=pass … verdict=pass` lines |
| C1.3 | **[m]** instrument absent at base, so this red control has no prior result (not runnable) | **[t]** `closed<8/8 exit=1` |
| C1.4 | **[m]** instrument absent; the frozen revision string does not resolve in the lane repo — see §6 F1 | **[t]** `closed<8/8 exit=1` |
| C1.5 | **[m]** instrument absent at base (no plain-run behaviour to record) | **[t]** exit 2 |

C1 before-state detail carried by the same control (`c1-controls/before.txt`, sha256 `0363c8c0…`):
R1 frozen r38 predicate was self-referential (receipt required inside the export that names it); R2
overstatement corrections absent (`corpus/lessons/round-38.md:0 LOG.md:0 SCORECARD.md:0 SHONEN.md:0`);
R3 no committed positive-run transcript for the r38 tip run (`f06148c6`); R4 `M38-5`/`M38-7` lack
criteria (count `0`); R5 25 surviving mutants as above.

## 2. C2 — coverage (frozen score 7, held 7)

Frozen counting commands, verbatim from `claims.json`:

```sh
C2.1  grep -cE '^\| F[0-9]+ \|' corpus/README.md -> 22
C2.2  grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md -> 58
C2.3  grep -rlE '^source: S057' corpus/knowledge | wc -l -> 1
C2.4  python3 corpus/instruments/frontier-recheck-count.py -> entries=25 pass=25 exit=0
C2.5  python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-39/manifest.json --source S057 -> exit 0
C2.6  python3 corpus/instruments/capture-binding-check.py -> records=46 bound=46 unbound=0
C2.7  python3 corpus/instruments/recheck-audit.py --quiet -> expected=51 missing=0 unexpected=0 exit=0
C2.8  ls corpus/knowledge/*.md | wc -l -> 51
C2.9  bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi -> exit 0
```

Before (measured at base 480b1a5…) → after:

| # | Before | After (frozen target) |
|---|---|---|
| C2.1 | 21 — **[c]** `frontier rows: 21`; **[m]** base frontier-row grep → 21; **[m]** lane tip HEAD also 21 | 22 (F22 admitted, ids=S057) |
| C2.2 | 55 — **[c]** `registry rows: 55`; **[m]** base S-row grep → 55; ids `S001…S055` contiguous, no duplicate ids; 3 rows already carry status `rejected` (`S026`, `S027`, `S028`) | 58 per claim — but the four instructed appends give 59 on disk; see §6 F2 |
| C2.3 | 0 — **[c]** `S057 rows: 0`; **[m]** base SOURCES.md `S057` grep → 0; **[m]** knowledge files with `source: S057` → 0 at base and 0 at lane tip | 1 |
| C2.4 | **[c]** harness `PASS F21 knowledge/csaf-vex-product-status-and-justifications.md ids=S055 exit=0` then `entries=24 pass=24 exit=0` | `entries=25 pass=25 exit=0` incl. `PASS F22 ids=S057` |
| C2.5 | **[m]** no `corpus/source-snapshots/round-39/` at base or at lane tip (latest tracked round dir is `round-38`), so no capture/manifest exists to recheck | S057 recheck exit 0 |
| C2.6 | **[c]** `records=45 bound=45 unbound=0` (audit line: `snapshot_dirs=14 manifest_dirs=14 missing_manifest=0 multi_row_url=2 orphans=1 orphan=S040-live.txt`) | `records=46 bound=46 unbound=0` |
| C2.7 | **[c]** `expected=50 missing=0 unexpected=0 exit=0` | `expected=51 missing=0 unexpected=0 exit=0` |
| C2.8 | 50 — **[c]** `knowledge entries: 50`; **[m]** base `corpus/knowledge/*.md` → 50; **[m]** lane tip → 50 | 51 |
| C2.9 | **[c]** census exit 0 with only `W04 S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes` and `W04 S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes` (`census-before.txt`, sha256 `88a3c813…`) | exit 0, same two W04 codes, no new W/E |

C2 negative control: `.ufo/waves/round-39/c2-controls/junk-f22.md` (1620 B, sha256 `8a719e6a…`) —
fabricated CISA When-to-Issue claims; `source-recheck.py` over it must print one
`MISMATCH reason=quote-not-found` per claim and exit 1 (same shape as round-38 `c2-controls/junk-f21.md`).

## 3. Wave shape facts

- Wave `kasegi-r39-build`; milestone `round-39`; reportDir `.ufo/waves/round-39/wave1`; `maxLanes` 64.
- Spec axes `depth:verifiability`, `coverage`; claims `axes_owned` also carries `depth:density`.
- Seats 49 = **executor 27, scribe 11, reviewer 6, scout 2, critic 2, connector 1**.
  - executor: ExecFrontierCapture, ExecJunkRecheck, ExecHarnessProbe, ExecCorrectionsR2, ExecQualityCriteria, ExecWholeTailFixture, ExecGradedSelftestFixture, ExecPinnedG8Fixture, ExecG4ResultsFixture, ExecMistakesDraft, ExecConsiderthese, ExecAssimilationIds, ExecNoHarmFixture, ExecFrontierLeads, ExecScoreGap, ExecArchiveChecks, ExecSeatIdentitySpec, ExecRunbookChecks, ExecCensusAfterMirror, ExecConsidertheseLedger, ExecArchiveNoHarmMirror, ExecProofSuiteSelftest, ExecCaptureStability, ExecNoPlaceholderScan, ExecDiskGuardProbe, ExecContextGuardCheck, ExecSuiteBuild
  - scribe: ScribeRowS057, ScribeRowsRejected, ScribeEntryF22, ScribeFrontierF22, ScribeProvinceF22, ScribeSearchLog, ScribeLessonGate, ScribeShonen, ScribeReportInputs, ScribeWaveEvidence, ScribeSpotCheckList
  - reviewer: RevControls, RevCorrections, RevFrontierAmendments, RevAssimilationBlock, RevRowsCensus, RevScratchDiscipline
  - scout: ScoutSiblingF22, ScoutReopenS057 (the only 2-axis seats, with ConnRoleGround)
  - critic: CritFreezeAudit, CritDesignReview
  - connector: ConnRoleGround
- Dispatch/identity facts for G4: `.ufo/waves/round-39/wave1-dispatch.json` 433466 B, `taskCall.tasks` 49; `.ufo/waves/round-39/wave1/swarm-registry.json` members 49, distinct 49; task names distinct 49, none unnamed — **[m]**.
- Claims 2: C1 `depth:verifiability` 4 → held 4; C2 `coverage` 7 → held 7. Saturation line `9/10 per owned axis`, window `N=3`; `lowest_non_retired_axis` = `depth:verifiability (4)`.
- Judged-head rule: J = the `export-ref=` value in `.ufo/waves/round-39/final-gates/all-gates.txt`; lane tip Y = J + that receipt only. Lane files never name J by hash.
- The eight C1 checks (G1–G8): G1 whole-tail declared blocks (`<path> <lines> <sha256>` = `tail -n <lines>` digest and added-line count, backtick+tilde fence walk closed at EOF, corrections only outside fences, declared paths exist in the export); G2 all-gates v3 receipt (one `export-ref` whose `git diff --name-only <export-ref> REF` is the receipt only, `suite-sha256` = executing bytes, eight `G<n> payload=… closed=1`, eight graded selftest lines); G3 committed-run truth for every quoted `--export-ref …` result; G4 seat identity in results.json; G5 head-label drift (no commit-hash label lines in the round-39 sections, head named by reference only); G6 scratch quiescence; G7 considerthese ledger fill; G8 pinned r37 suite 14/14.
- Controls on disk: `c1-controls/before.txt` 1017 B `0363c8c0…`; `c2-controls/before.txt` 543 B `866ac757…`; `c2-controls/junk-f22.md` 1620 B `8a719e6a…`; `census-before.txt` 276 B `88a3c813…` (full digests: sha256, prefix shown).
- Precedent for a mid-round number correction: `.ufo/waves/{round-28,round-33,round-34,round-35,round-37}/claims-erratum-*.md`.

## 4. Evidence pointers, in order

1. Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only lane), branch `master`; tip at pack time `d65d823e7c84813c192b20ee757a8761f878a61f` (`round-39: wave1 spec/dispatch`); tracked tree clean (`git status --porcelain --untracked-files=no | wc -l` → 0); untracked `.ufo/waves/round-39/wave1/` receipts in flight (49 entries at pack time).
2. Base `480b1a505a2dfc14a4f718d16d63808247214d0a` — `round-38 verifier spot-check (integrator, hyaku): non-author admit/reject`; ancestor of the tip.
3. Claims freeze `dcd31701720a6a4929a32471a62011ed87103421` — `round-39: claims freeze C1/C2 + controls`; ancestor of the tip; `rev-list --count base..tip` = 2 (`dcd3170`, `d65d823`).
4. `.ufo/waves/round-39/claims.json` — the frozen predicates, kill rules, counting commands and the judged-head rule.
5. `.ufo/waves/round-39/c1-controls/before.txt`, `c2-controls/before.txt`, `c2-controls/junk-f22.md`, `census-before.txt` — the measured before state and the C2 negative twin.
6. `.ufo/waves/round-39/wave1-spec.json` (413733 B, 49 items) and `wave1-dispatch.json` (433466 B, 49 tasks) — wave shape and G4 identity source.
7. `.ufo/waves/round-39/wave1/` — seat receipts and byte-exact deliverables, including the row files `ScribeRowS057.row.md`, `ScribeRowsRejected.S056|S058|S059.row.md`, the README/F22 append, the r39 suite deliverable and the fixture receipts.
8. `.ufo/waves/round-39/final-gates/` — **absent at pack time**; will hold `all-gates.txt` (v3 receipt, `export-ref` = J) and any red-control transcripts.
9. `corpus/lessons/round-38-verifier-spotcheck.md` §5 — the routed defects R1–R4 that C1 closes.
10. `corpus/lessons/round-38.md` §Instrument attack findings — the 25 surviving mutants and the G4 identity / G8 export-ownership findings behind G1–G8.
11. `corpus/instruments/r39-closure.sh` — the new instrument (absent at base and at pack time; lands with C1).
12. Pinned r37 carry-over (G8): commit `2387dcf6ccfefcfb703783387b9aade8fc82abfa` (`round-37: F3 final head — bind final lane hash in SHONEN/SCORECARD`); `git show 2387dcf6:corpus/instruments/r37-closure.sh` = 73132 B / 1558 lines / sha256 `0da98e37b5a87e0ca7cb3d5f05ea05b992adbc4091095276848818a30342434d`.
13. Round-38 judged head, as recorded by the round-38 gate: `.ufo/waves/round-38/final-gates/all-gates.txt` line 2 `export-ref=66703acaaff50529a35be49aa8759d04140720ad`; that revision resolves locally (`round-38: integrate C1 r38-closure suite + D-A..D-F corrections, … (judged head)`). See §6 F1 for the frozen claim's variant.
14. C2 source trail: `corpus/SOURCES.md` rows `S056`/`S057`/`S058`/`S059` (to be appended; absent at base and tip) and the `## Registry changes` log; capture `corpus/source-snapshots/round-39/S057.txt` + `manifest.json`; entry `corpus/knowledge/cisa-when-to-issue-vex.md`; frontier row F22 and the count line in `corpus/README.md`.
15. C2 instruments: `corpus/instruments/frontier-recheck-count.py`, `source-recheck.py`, `capture-binding-check.py`, `recheck-audit.py`, plus the fleet-side `scripts/sources-census.sh` (fleet root read-only).
16. Ledger for G7: `corpus/knowledge/considerthese-proposals-ledger.md` — last heading at pack time `## Round-37 dispositions — filled (round 38)`; no round-39 section yet.
17. Report targets (lane files, each 0 `Round 39`/`round-39` mentions at pack time — **[m]**): `SCORECARD.md` 176890 B, `SHONEN.md` 17451 B, `LOG.md` 151862 B, `PROVINCE.md` 11794 B, `SKILL.md` 111619 B; `corpus/lessons/round-39.md` absent. Fleet root `/home/vgpnk/Projects/shokunin` holds only `SCORECARD.md` and `LOG.md` (0 round-39 mentions) — it has no `SHONEN.md`/`PROVINCE.md`/`SKILL.md`; those are lane files.

## 5. Current lane state of every landed artefact the report will cite

Measured at the lane tip / working tree at pack time: frontier rows 21; registry rows 55; knowledge
entries 50; knowledge files citing `source: S057` 0; `corpus/source-snapshots/round-39/` absent;
`corpus/instruments/r39-closure.sh` absent; `corpus/knowledge/cisa-when-to-issue-vex.md` absent;
`corpus/lessons/round-39.md` absent; `final-gates/` absent. Tracked tree clean. So every "after"
value in §1–§2 is still **[t]**, and the report must take it from the gates at Y, not from this pack.

## 6. Conflicts to resolve before the report lands

**F1 — the frozen r38-head revision does not resolve (37-character string).**
`claims.json` C1 `kill_rule` and counting command C1.4 both carry
`66703aca50529a35be49aa8759d04140720ad` (37 chars). Measurements:
`git cat-file -t 66703aca50529a35be49aa8759d04140720ad` → MISSING in the lane repo, the fleet root repo
and shokuknow; `git log -1 66703aca50529a35be49aa8759d04140720ad` → `fatal: ambiguous argument …:
unknown revision or path not in the working tree.`; `git ls-remote origin` → `master` only, no such
ref; GitHub API `GET /repos/VeigaPunk/kasegi-shokunin/commits/66703aca50529a35be49aa8759d04140720ad`
→ `http=422 bytes=171`, body `No commit found for SHA: 66703aca50529a35be49aa8759d04140720ad`
(fetched 2026-10-26T19:31:51Z). The round-38 gate records the real 40-character head
`66703acaaff50529a35be49aa8759d04140720ad` (`.ufo/waves/round-38/final-gates/all-gates.txt` line 2),
which does resolve. The 37-character variant appears 51× in `wave1-spec.json`, 51× in
`wave1-dispatch.json`, 2× in `claims.json`, and the 40-character variant appears 0× in any of them —
so seats were dispatched with the unresolvable string. Two consequences for the report: (a) the r38
red control must be restated (erratum precedent `.ufo/waves/round-37/claims-erratum-1.md`) or run
against `66703acaaff50529a35be49aa8759d04140720ad` with the erratum named; (b) any gate that consumes
a red export must first assert `git rev-parse --verify` success, otherwise a `git archive` failure
reads as `closed<8/8` and the red control passes for the wrong reason.

**F2 — C2 registry arithmetic: 55 + 4 = 59, frozen target 58.**
`claims.json` C2 predicate/kill rule/counting command C2.2 all say 58; `ScribeRowsRejected`'s item
spec says "old→new: registry 55 → 58" while instructing three rejected row files (`S056`, `S058`,
`S059`) and `ScribeRowS057` instructs one mined row (`S057`) — four appended rows on a measured
55-row registry (`S001…S055`, contiguous, no duplicate ids, rejected rows `S026`/`S027`/`S028` already
counted by the same grep). On-disk result of the plan is 59. Either the target/erratum is 59, or one of
the four rows must not land as a registry row; the frozen counting command cannot be satisfied as
written by the instructed plan.

**F3 — nothing to measure for "after" at pack time.** `final-gates/` absent, J unnamed anywhere in
the lane (by rule), so all after-values here are targets. Do not promote them.
