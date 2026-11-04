# Round-66 verifier spot-check — kasegi

author: hyaku closure (non-author integrator, @m_zfl)

Round: kasegi r66 · base `b6db9e818d322726e39cb441f2179d34d4170275` · final lane hash
`51a5cb0d9ac8bf58f355c433a33a9ccc44fa34c2` · measured implementation
`e8a865da49f3d1ff0e7222830006b3003d4577c0` · report `.ufo/reports/round-66/kasegi.md` (fleet commit
`acf6101b8eb8813c9ddaa8ebc2d130b0d200e580`, author date 17:43:23 -0300, commit date 17:44:16, by
`kasegi-shokunin`) · prompt `.ufo/prompts/kasegi-round-66.md` (818 lines, 17:04 dispatch).

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-11-04T17:04:56-03:00 launch kasegi round=66 pgid=2889804 driver=hyaku-inline attempt=1
2026-11-04T17:45:15-03:00 complete kasegi round=66; hyaku-inline attempt=1
```

## Conformance (step 1)

- **Attribution.** `git log --format='%an %H %ad' --date=iso -- .ufo/reports/round-66/kasegi.md` →
  `kasegi-shokunin acf6101b8eb8813c9ddaa8ebc2d130b0d200e580 2026-11-04 17:43:23 -0300`. Report lands
  after the lane's final commit (`51a5cb0d`, 17:41:28) and cites that hash as the final lane state.
- **SHONEN heading.** `grep -c '^## SHONEN'` = 1; four box lines (`[~]`, `[ ]`, `[~]`, `[~]`), one per
  box in `SHONEN.md` (4 boxes, `grep -c '^- \['` = 4). No `[x]` was written by this non-author.
- **Ancestry.** All seven cited commits plus the measured revision and the base exist, and
  `git -C kasegi-shokunin merge-base --is-ancestor <h> refs/heads/master` = yes for each (the repo is
  jj-colocated and git HEAD is detached, so ancestry was tested against the branch ref):
  `1957407e`, `6102c0e9`, `d94a9ecd`, `0d5aef2f`, `32a24002`, `e8a865da`, `51a5cb0d`, `b6db9e81`.
- **Lane state.** `scripts/hyaku/jj-lane.sh state kasegi-shokunin` →
  `branch=master local=51a5cb0d remote=51a5cb0d ahead=0 behind=0 head=detached tracked=0 untracked=0`;
  `git status --porcelain` empty; `git ls-remote origin refs/heads/master` prints
  `51a5cb0d9ac8bf58f355c433a33a9ccc44fa34c2`. No uncommitted round work.
- **Prompt fidelity.** `templates/round-prompt.md` lines 1–137 are byte-identical to the dispatch
  after four macro substitutions (working-dir form, axes value, lane, round); the 681-line tail
  (l.138–818: §6 hyaku addendum, §7 scratch discipline, run-15 notes) is appended, not substituted.
  The ten contract items are present: mission/axes binding (l.3–7), L2 ≥8 in one batched AgentSwarm
  call (l.82, matching `MISSION.md` l.65–66), commit-then-push (l.133), push scope (l.135–137), L0
  side channel (l.138–140), report path (l.101), commit-before-report (l.516–520), `## SHONEN` gate
  (l.521–522), commit-hash citation rule (l.472–473), lane write scope (l.448–455). §6 is present at
  l.141. One fleet-level defect, not a lane defect: addendum §2 (l.353–365) still states a 32–128
  seat shape while the binding run-15 line (l.145) is 8–16, and no supersede clause covers §2; the
  validator band (`ufo-wave-policy.json` min 8 / max 256) would let it execute. Routed below.
- **Marker check.** Substantive report: one declared claim, seven landed commits each tied to an
  existing `LOG.md` bullet (2682–2694, verified per commit), committed receipts. Status `ok`.

## Claim re-checks

C1 is the round's only claim. It is a **gate claim**, so per PROTOCOL §Gate standard ("Closure
consequence") the committed evidence was verified and the lane's gate was **never executed**: every
number below is either a byte measurement over committed objects or a receipt read as committed text.

### C1 — depth:verifiability, score 4→4, delta 0, nominal R58

Frozen predicate (`.ufo/waves/round-66/claims.json`): `VERIFY measurements=12 failures=0 and process
exit0 on the exact committed-input counter.`

```
$ git show <rev>:<path> | sha256sum            # committed bytes, not the worktree
.ufo/waves/round-66/w1/ExecCatDriver/verify.py    5962b7d6… (freeze 32a24002, measured e8a865da, final 51a5cb0d — identical)
.ufo/waves/round-66/w1/ExecCatGate/figure-audit.py 51f299af… (freeze, measured, final — identical)
.ufo/waves/round-66/controls/driver-pins.json      e6bb9032… (freeze and final — identical)
.ufo/waves/round-66/claims.json                    86bd78f4… (freeze and final — identical)
.ufo/waves/round-66/w1/ExecCatProbes/probes.py     d788bbc1… (final)
.ufo/waves/round-66/cat-mutbat.py                  8efa7d88… (final)
corpus/instruments/figure-audit.py                 51f299af… (measured and final = frozen candidate, byte-exact)
```

No postfreeze counter, candidate, pin or claims amendment: the freeze-time and final-time digests are
equal for all four frozen artifacts.

```
$ .ufo/waves/round-66/controls/final-verification-r66.txt
RESULT selftest PASS cases=67 failures=0 want=67 exit=0 kind=candidate
RESULT probes-base-paired PASS mode=base probes=8 rc=0
RESULT probes-measured PASS mode=candidate probes=8 rc=0
RESULT shape-identity PASS shapes=8 P1 stale derive-upstream-signal-13 | P2 stale derive-upstream-signal-13 |
  P3 ok | P4 ok | P5 stale derive-upstream-exit-1 | P6 ok | P7 ok | P8 stale derive-upstream-signal-13
RESULT real-ledger PASS want='FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0'
RESULT mutbat-existing PASS killed=5/5 survivors=0 invalid=0 controls=pass
RESULT cat-mutbat PASS killed=3/3 survivors=0 equivalents_held=1 invalid_rejected=1 failures=0
RESULT identity-guards PASS head=e8a865da gate=51f299af candidate=-(unpinned)
VERIFY measurements=12 failures=0 revision=e8a865da49f3… mode=final
exit=0
```

```
$ .ufo/waves/round-66/controls/driver-base-final-prefreeze.txt
RESULT probes-measured FAIL mode=candidate probes=8 rc=1 problems=P1,P2,P8 (want derive-upstream-signal-13)
RESULT shape-identity FAIL shapes=8 (P1/P2/P8 read ok at base)
RESULT selftest PASS cases=63 failures=0 want=63 exit=0 kind=base
RESULT cat-mutbat FAIL exit=2 (cat limb absent on base)
VERIFY measurements=12 failures=3 revision=b6db9e81… mode=base
exit=1
```

```
$ .ufo/waves/round-66/controls/driver-forgery-id-prefreeze.txt
RESULT probes-measured FAIL … instrument_sha256=2596baad…   (ID-keyed no-work oracle)
VERIFY measurements=12 failures=6 revision=b6db9e81… mode=candidate
exit=1
```

Supporting evidence re-read, not re-run: `driver-candidate-final-prefreeze.txt` = 12/0 exit0 with the
stand-in candidate; `w1/ReviewCat.md` states 43 cases at base and at candidate, 18 expected behavior
changes and 25 unchanged controls, and proves the doc-corrected v2 executable tail byte-identical;
`w1/CriticCat/opaque-final-summary.json` records id/path/text/always-green/always-stale controls each
`rc=1` (rejected) with the real candidate 8/0.

Implementation delta (`git diff 32a24002 e8a865da`): `upstream_stale(head, status)` becomes
`upstream_stale(head, stage_argv, status)` with per-stage decoded argv threaded from `run_derive`
(`stage_argvs`), a new `cat_sigpipe_exempt(argv)` (stdin-only or one operand, optional leading `--`,
any option token refused conservatively), other heads unchanged, `EXPECTED_CASES` 63→67, four new
public-path selftests, and a module-docstring correction. `git diff e8a865da 51a5cb0d` touches only
`LOG.md`, `SCORECARD.md`, `corpus/lessons/round-66.md` and `.ufo/waves/round-66/**` receipts — the
gate, counter, collector and pins are untouched after the measured revision.

Verdict: **claim verified** (predicate met on the frozen counter; before/after reproduced from
committed bytes and committed receipts; the measured production instrument equals the frozen
candidate digest).

### Registry re-derivation (my own count over committed bytes)

```
before rows=98 tiers={'A': 88, 'B': 5, 'C': 5} status={'mined': 80, 'rejected': 18}
after  rows=99 tiers={'A': 89, 'B': 5, 'C': 5} status={'mined': 81, 'rejected': 18}
added=['S099'] removed=[] old_rows_changed=0 malformed_rows_after=0
```

Matches the report exactly. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
kasegi` → `exit=0`, `ok …/corpus/SOURCES.md`, with the same six inherited `W04` URL warnings
(S028, S029, S072, S076, S080, S085) as `controls/census-before.txt`; none on S099.

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth:verifiability (lowest, 4) | **improved** | The finite predicate moved from 3 failures/exit1 to 0 failures/exit0 on the same frozen committed-input counter, with the same driver, pins and controls; the counter, probe collector, selftest (63→67), cat mutant battery (absent→3/3) and ID-forgery control (12/6 exit1) all discriminate. The nominal R58 score is held at 4 because the metric R58 scores (citation resolution / source availability) is not read by this gate — `delta 0` is reported, not hidden. |
| coverage (8) | **unchanged** | No knowledge/frontier admission, no new capability; `corpus/knowledge/` and `corpus/README.md` are byte-identical to base; registry 98→99 is S099 curation only. |
| depth:density (9) | **unchanged** | Not targeted, not remeasured; no density credit claimed and none taken. |

No owned axis is harmed: `SCORECARD.md` changes are a pure append (30 insertions, 0 deletions),
`PROVINCE.md` and `corpus/knowledge/` are unchanged, and the `SKILL.md` delta is the one gate row
plus one current-execution amendment. `corpus/QUALITY.md` gains only the R92 criterion row.

## Discernment spot-check (non-author)

| # | Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|---|
| 1 | S099 admit (own-work source) | admit, local diagnostic only | `corpus/instruments/figure-audit.py@b6db9e81:L83-L94`, quote `return status != -signal.SIGPIPE` at L91 | **agree** | Source exists at the pinned base, `upstream_stale` is exactly L83–L94, the quote is verbatim at L91 and 4 words (≤25). Tier A covers "the lane's own re-runnable gate output"; the anchor carries revision and lines, not a homepage. |
| 2 | Reject "SIGPIPE proves input completeness" | reject | `.ufo/waves/round-66/controls/red-before-mechanism.txt@1957407e:L4-L8` | **agree** | Re-opened receipt shows `native_statuses=141 0`, only `alpha` printed, `audit_rc=0` (green), while `untruncated_cat_rc=1` proves the later operand's error existed and was masked. A green pipeline therefore does not establish that all named inputs were read. |
| 3 | New `corpus/SOURCES.md` row S099 | row written as claimed | `corpus/SOURCES.md@51a5cb0d:L111` | **agree** | 11 columns, `kind=own-work`, `tier=A`, `status=mined`, `opened=2026-11-04`, `recheck=on-release`, `used-by=corpus/lessons/round-66.md` (path exists); quoted `teaches` is 22 words (≤25); anchor pins commit + lines; id is the next unused and unique. |
| 4 | Round-65 routed corrections (6 items) | corrected append-only | `corpus/lessons/round-65-verifier-spotcheck.md:132-155` vs `corpus/lessons/round-66.md:24-33` | **agree** | All six defects map one-to-one onto the six correction entries (invented "LOG bolts", two omitted commits, wrong driver label, non-tip revision, uncaptured base rc, sentinel per-run count); r65 filed bytes were not rewritten, and `R92` grounds the rule. |

Non-defect observed while re-opening: `corpus/instruments/figure-audit.py` is cited by both S096
(non-grep exit1 anchors L98–L109, L412–L424) and S099 (SIGPIPE anchors L83–L94). Anchors are
disjoint, contract v1 has no path-uniqueness rule, and the census `W04` check is URL-keyed, so this
is not a conformance defect; it is routed as a curation note below.

## Trend verdicts

- **Expansion — unchanged.** No new knowledge entry, frontier row, repertoire row or capability:
  `corpus/knowledge/` is unchanged, `corpus/README.md` is unchanged, and `capabilities_added` is
  empty. Registry 98→99 is own-work curation consumed by this round's lesson, which
  `LEARNING.md` counts as curation, not expansion. SHONEN box 2 stays `[ ]` and the round says so.
- **Quality — unchanged.** No knowledge entry was superseded, re-admitted or re-verified; the
  instrument repair is a gate correction, not a corpus entry. `QUALITY.md` gains the R92 criterion
  grounded in the outside r65 disagreement; a criterion is the discernment instrument, not a
  quality move by itself.
- **Discernment — improved.** The outside r65 record disagreements became six append-only
  corrections plus R92 (M66-5); the round's own prefreeze failures changed controls instead of being
  hidden (M66-4 ID-keyed oracle, M66-7 `rev:path` resolver peel, M66-8 path-keyed oracle, M66-9
  harness error not counted as a kill); ReviewCat's docstring contradiction was fixed before freeze
  (M66-6). This non-author spot-check agrees with both sampled decisions (admit and reject) and with
  the S099 row, so the gate's taste holds on the sample. Outside admission/promotion remains owed.

## Routed defects and notes

1. **V66-1 (lane, minor, curation).** S096 and S099 cite the same own-work path
   (`corpus/instruments/figure-audit.py`) with disjoint anchors. Not a contract defect, but the next
   lesson should name the split so a path-keyed lookup does not read the two rows as duplicates.
2. **V66-2 (lane, minor, report phrasing).** "Assigned attack3/9 (completed2/8)" in the report and
   `LOG.md` bullet 2683 is terse; it means 3 attack seats of 9, with 2 of the 8 evidence seats being
   attack seats (mutation-tester dead). State it that way if it recurs.
3. **V66-3 (fleet/operator, not the lane).** The hyaku addendum in the dispatched prompt keeps a
   32–128 seat shape at l.353–365 next to the binding 8–16 line at l.145, and no supersede clause
   covers §2; `ufo-wave-policy.json` (min 8, max 256) would let a 32–128 dispatch validate. Prompt
   text is operator/protocol-owned, so this is routed there, not to kasegi.
4. **V66-4 (operator-side observation).** `.ufo/state/kasegi.round` reads `17` while the hyaku
   driver's own state (`.scratch/run15-state.json`, `block_start 57`, `block_done 9`) puts this round
   at 66. The legacy watchdog state file is stale and is not lane-owned; recorded so a reader does
   not read it as a round mislabel (the report, lesson, LOG and SCORECARD all say 66).
5. **Operator note (promotion, operator-owned).** SHONEN boxes 1, 3 and 4 are `[~]`
   author-asserted but checkable by a non-author against committed bytes; box 2 stays `[ ]`. No box
   was marked here and promotion is operator-owned.
