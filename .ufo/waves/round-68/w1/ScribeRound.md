# ScribeRound — round 68 narrative drafts

**Verdict: DRAFTS DELIVERED + FINDINGS.** C1 frozen predicate reproduced by this seat (`VERIFY measurements=8 failures=0` exit 0 on the committed gate). C2 after-state equals the frozen target on the *uncommitted* worktree only; on committed bytes it is NOT MEASURED BY THIS SEAT. Three calibration findings (M68-2..M68-4), none of which defeats a claim.

Drafts (for L1 integration; nothing written to `corpus/lessons/`, `LOG.md` or `SCORECARD.md`):
- `.ufo/waves/round-68/w1/ScribeRound/lesson-draft.md`
- `.ufo/waves/round-68/w1/ScribeRound/log-entry-draft.md`
- `.ufo/waves/round-68/w1/ScribeRound/scorecard-row-draft.md`

Raw receipts are in the same directory: `c1-candidate-scribe.txt`, `c1-base-scribe.txt`, `c1-candidate-archive-lane-scribe.txt`, `c1-base-archive-lane-scribe.txt`, `c2-counters-scribe.txt`, `c2-base-d0f48405-scribe.txt`, `c2-live-worktree-scribe.txt`, `c2-census-live-scribe.txt`, `s102-fetch-scribe.txt`.

## What I ran (scratch `/fast/scratch/hyaku/kasegi-r68/ScribeRound`, removed before yield)

1. Pins. `sha256sum` on the lane files:
   `785e38fd…4b4b c1-probe-run-r68.py`, `8147350c…d247 base-gate-d0f48405.py`, `10c87100…fee8 corpus/instruments/figure-audit.py`, `6ebb8552…aa0 S102.txt`, `wc -l S102.txt` = 429. The `git archive 82b3b7d4` export has the same three instrument digests.
2. C1, frozen counter, default `--lane`:
   `python3 -B $S/cand/.ufo/waves/round-68/controls/c1-probe-run-r68.py --gate $S/cand/corpus/instruments/figure-audit.py --work $S/workc --mode candidate`
   ```
   MEASURE sort-compress-refused ok rc=2 marker_runs=0
   MEASURE git-textconv-refused ok rc=2 marker_runs=0
   MEASURE read-only-controls-admitted ok controls=5 failed=0
   MEASURE selftest ok selftest cases=77 failures=0 rc=0
   MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
   MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
   MEASURE red-fixture ok rc=1
   MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
   VERIFY measurements=8 failures=0 gate_sha256=10c8710080078fe07534eae8fcc1344ade9ae852be500e66a2804eb68b74fee8 mode=candidate
   EXIT=0
   ```
   Base: `--gate $S/cand/.ufo/waves/round-68/controls/base-gate-d0f48405.py --work $S/workb --mode base` printed `sort-compress-refused FAIL rc=1 marker_runs=18288`, `git-textconv-refused FAIL rc=1 marker_runs=1`, `selftest FAIL selftest cases=73 failures=0 rc=0`, `no-write-side-effect FAIL fixture_changed=0 marker_runs=18289`, `VERIFY measurements=8 failures=4 … mode=base`, `EXIT=1`. These match the committed receipts (`grep` of both control files gave the same MEASURE/VERIFY lines).
3. C1 with `--lane $S/cand` (a git archive export, no `.git`): both modes printed `MEASURE real-ledger FAIL FIGURE-AUDIT figures=35 ok=11 stale=24 exit=1 rc=1`, which made candidate `failures=1` and base `failures=5`. `python3 -B corpus/instruments/figure-audit.py --root .` in the export printed `FIG frontier-rows recorded=34 derived=UNAVAILABLE reason=derive-exit-1 stale`. This was my harness choice, not the frozen command (M68-4).
4. Fresh source fetch: `curl -sS -o raw/swagger.json -w 'http=%{http_code} bytes=%{size_download}…' https://api.securityscorecards.dev/swagger.json` printed `http=200 bytes=11802` at 2026-11-04T21:53:35Z, raw sha256 `d526f327…c8af4`. Stripping per-line leading/trailing whitespace and adding the final newline gave sha256 `6ebb8552ac3e0c4085f4a9239e29551fa1be19cebbdf99ccabb96400d8c2caa0` over 429 lines, which is identical to the committed capture. `grep -n "published Scorecard result" S102.txt` printed `13:"description": "API to interact with a project's published Scorecard result",` (9 words; manifest Q01). The capture also has `11:"swagger": "2.0"`, `15:"version": "1.1.0"`, `17:"host": "api.scorecard.dev"`, routes at L19/L160/L234, and the aggregate-score description at L353.
5. Refused candidate: `curl … /projects/github.com/ossf/scorecard` printed `http=200 bytes=13259`, `wc -l` = 1, `date` 2026-11-03T06:28:58Z, `score` 8.8.
6. C2 counters on `git archive 82b3b7d4` and on the live worktree (first pass, 21:55Z): `FRONTIER-CENSUS rows=45 admitted=45 closed=45 problem-rows=0 registry=101`, `entries=48 pass=48 exit=0`, `records=82 bound=81 unbound=1`, capture exit 1, 85 lines / 83 entries. Census `validate` exit 0 with three W04 lines in the tail.
7. C2 on `git archive d0f48405`: `records=81 bound=81 unbound=0` exit 0, `rows=45 … registry=101`, `entries=48 pass=48`, 85 / 83. `git ls-tree -r --name-only d0f48405 corpus/source-snapshots/round-68` printed nothing.
8. C2 on the live worktree (second pass, 2026-11-04T21:58:53Z, HEAD `82b3b7d4`, ScribeF46 edits uncommitted): `FRONTIER-CENSUS rows=46 admitted=46 closed=46 problem-rows=0 registry=102`, `FRONTIER-PASS F46 ids=S102`, `entries=49 pass=49 exit=0`, `records=82 bound=82 unbound=0` capture exit 0, `86` lines, `84` entries, census exit 0.
9. Wave shape: `jq -r '.items[].role' w1-spec.json | sort | uniq -c` printed connector 1, critic 1, executor 2, mutation-tester 1, revenger 1, reviewer 2, scout 1, scribe 2, sentinel 1, for 12 items. `w1-dispatch.json` has `counts {"spawn":12,"resume":0,"total":12}` and minLanes 8 / maxLanes 16.
10. Re-read `.ufo/waves/round-67/w1/SentinelMultiHead.md` §3. It records "**68 217** (base) / **68 222** (candidate) compressor invocations" and "**1** driver run". This matches the `claims.json` residual text.

## Findings / disagreements (for L1 adjudication)

- **M68-2 (receipt labelling).** `controls/c2-base-counters-r68.txt` is headed `revision d0f48405…` but prints `records=82 bound=81 unbound=1`. At true d0f48405 the value is `records=81 bound=81 unbound=0` (step 7). `claims.json` C2 `do_nothing_control` quotes 81/81/0 and cites this receipt, which shows 82/81/1. The receipt's trailing note does disclose that the manifest was present. Suggested remedy: an erratum that labels the tree as base plus the round-68 capture input. The frozen file is not edited.
- **M68-3 (interim red).** At `82b3b7d4`, `capture-binding-check.py` exits 1 (`unbound=1`) until the S102 registry row is committed.
- **M68-4 (lane dependence).** The frozen counter's real-ledger measurement derives against the live lane repo. An archive-only "committed bytes" reproduction reads `figures=35 ok=11 stale=24`. This does not defeat C1, because the frozen command uses the default lane. It does mean that measurement 6 is not computed from committed bytes alone.
- C2 is **not verified by this seat on committed bytes**. The after-target holds only on the uncommitted worktree, so the L1 must re-run after committing.
- Not measured by this seat: the L1 FINAL receipt, wave settlement (dead seats, residual calls, `w1-results.json`), other seats' verdicts, and any further program-execution spellings (abbreviations, other heads), which are CriticC1/RevengerC1's ground.
- The untracked `corpus/lessons/round-68.md` (not mine, presumably the L1's) already exists. I did not touch it. My draft is separate for the L1 to merge.

## Bounds
Writes: only this report and `w1/ScribeRound/`. No lane commit, no mutating git, no `git add`, no edits to frozen files. Scratch fixture repos were created only by the frozen counter inside `--work`. No tool installs or upgrades. Scratch removed before yield.
