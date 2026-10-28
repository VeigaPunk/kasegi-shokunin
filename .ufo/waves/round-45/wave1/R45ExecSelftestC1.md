VERDICT: BROKEN

Seat R45ExecSelftestC1, round 45, C1 counter selftest (draft only). The frozen counter `corpus/instruments/r45-routed-defects.py` is not edited.

Draft: `.ufo/waves/round-45/wave1/R45ExecSelftestC1.draft/r45-counters-selftest-c1.py` (stdlib, ~640 lines).
Run: `python3 .ufo/waves/round-45/wave1/R45ExecSelftestC1.draft/r45-counters-selftest-c1.py` (about 66 s, exit 1 while false-greens exist).
Printed last line of the full run: `selftest cases=40 failures=9`.
Breakdown: 4 controls ok, 27 mutants rejected, 9 mutants FALSE-GREEN.

## What the harness builds
- Base: a hardlink clone (`cp -al`) of `/fast/scratch/hyaku/kasegi-r45/L1/pure`. Every write unlinks first, so the pure export and the shared inodes are never touched.
- GOOD tree, genuinely written:
  - **R1.** `corpus/source-snapshots/round-45/{S071.txt,S072.txt,manifest.json}` copied byte-for-byte from the lane. An 11-cell S072 row is inserted after the S070 row in `corpus/SOURCES.md`. Its anchor carries the S072.txt sha256. Its teaches cell starts `supersedes S070 —` and carries `flip:`, `readable` and `10029`. An appended `Correction (round 45): ... S072 ... 10029 readable characters ...` line goes into `corpus/lessons/round-44.md`.
  - **R2.** An appended `## Round-45 additions` block in `corpus/QUALITY.md` with R47/R48/R49 rows. Each is 3 cells, carries the counter's keywords, a grounded-in cell naming `corpus/lessons/round-44.md`, and one `enforced-by:` path that exists.
  - **R3.** `r44-frontier-count.py` is the frozen base source patched with a real `--selftest`: 8 fixture cases, each exercising the counting code through the CLI. The SKILL.md `## Round-45 Gates & probes registry addition` table has six 8-cell rows. The instruments README gets a table row for `r44-frontier-count.py`.
  - **R4.** A freeze-check.py written in the harness (my own minimal implementation). It replays `counter_cmd` with tree=base, matches `expect_before` as a whole line, rejects an `expect_after` match, and checks that the three fields exist. It has a real 8-case selftest. The real `claims.json` and the real r45 counters are copied in as the tool.
  - **R5.** The lane's own `final-attempt3-refiled.txt` (a recorded real run at tip c950fa3) is bound. See limitations for why it is not a fresh run in the fixture tree.
- Controls run through the frozen counter:
  - GOOD tree reads `fixed=5`.
  - Do-nothing base reads `fixed=0`.
  - Marker-only tree (base plus only the prose markers: heading, the Correction line, the R47/R48/R49 keywords, the registry heading with the names) reads `fixed=0`.
  - Null mutant (unchanged clone of GOOD) reads `fixed=5`. This shows the harness does not pass by flagging everything.

Printed:
```
GOOD counter output:
  limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1
  limb R2 fixed=1 read=criteria=3
  limb R3 fixed=1 read=selftest-cases=8
  limb R4 fixed=1 read=selftest-cases=8 replay=base_ok=2
  limb R5 fixed=1 read=refiled=ok original=unchanged
  routed-defects total=5 fixed=5 unresolved=0 exit=0
case control-good-tree total_fixed=5 verdict=ok expect fixed=5 R1=1 R2=1 R3=1 R4=1 R5=1
case control-do-nothing-base total_fixed=0 verdict=ok expect fixed=0
case control-null-mutant total_fixed=5 verdict=ok unchanged clone must stay fixed=5 (harness does not flag everything)
case control-marker-only total_fixed=0 verdict=ok prose markers only, no artifacts: expect fixed=0
```

## Mutants
Each is a hardlink clone of GOOD with one limb's bound artifact broken and the prose marker left in place. The harness records which watched files changed. REJECTED means:
- the target limb reads `fixed=0`,
- the total is exactly one lower (two lower for the one declared coupled case),
- no other limb changes,
- exactly one watched file changed.

### Rejected by the frozen counter (27)
Quoted `read=` token per mutant:
- R1:
  - `r1-snapshot-byte-flipped` → `recheck-rc=1-quotes=0`
  - `r1-manifest-quote-dropped` → `recheck-rc=0-quotes=1`
  - `r1-s070-row-edited` → `S070-row-changed-or-baseline-absent`
  - `r1-flip-clause-removed` → `flip-absent`
  - `r1-correction-wrong-size` → `lesson-correction-absent`
  - `r1-anchor-sha-wrong` → `snapshot-sha-not-in-anchor`
- R2:
  - `r2-enforced-by-missing` → `R48-enforced-by-missing-corpus/instruments/does-not-exist.py`
  - `r2-quality-prefix-edited` → `quality-not-append-only-or-unchanged`
  - `r2-r49-ungrounded` → `R49-ungrounded`
  - `r2-duplicate-heading` → `round-45-heading!=1`
  - `r2-r47-lacks-before-data` → `R47-missing-before data`
- R3:
  - `r3-selftest-7-cases` → `selftest-rc=0-tokens=(7, 0)`
  - `r3-selftest-failure` → `selftest-rc=1-tokens=(8, 1)`
  - `r3-registry-row-7-cells` → `registry-row-wave-registry.py=1`
  - `r3-registry-row-duplicated` → rejected in the final run (its `read=` token was not displayed; the first run, whose mutation hit the SKILL.md baseline portion by mistake, read `SKILL-not-append-only`; the mutation was then fixed to duplicate the registry row and is counted among the 27 rejected)
  - `r3-registry-row-prose-only` → `registry-row-wave-registry.py=0`
  - `r3-readme-row-bullet` → `readme-row-absent`
  - `r3-skill-not-append-only` → `SKILL-not-append-only`
- R4:
  - `r4-freeze-selftest-5-cases` → `selftest-rc=0-tokens=(5, 0)`
  - `r4-freeze-selftest-failure` → `selftest-rc=1-tokens=(8, 1)`
  - `r4-claims-replay-short` → `replay-rc=1`
  - `r4-freeze-absent` → `freeze-check-absent`. This is a declared coupling: total drops by 2 because R2's R47 `enforced-by:` path is `freeze-check.py`.
- R5:
  - `r5-usage-line` → `usage-or-error-line-present`
  - `r5-error-line-only` (an `error:` line without `usage:`) → `usage-or-error-line-present`
  - `r5-original-changed` → `original-receipt-changed`
  - `r5-invocation-absent` → `invocation-absent`
  - `r5-cases-19` → `selftest-token-absent`

Token provenance: the `read=` tokens above come from the first full run (37 cases) and the final run's filtered output; the final run was filtered to non-rejected lines, and the count of 27 rejected comes from `grep -c "verdict=rejected"` on its output. Re-run the script to regenerate every line.

### FALSE-GREEN: the frozen counter does not reject (9) — the finding
Verbatim from the final run:
```
FALSE-GREEN mutant=r1-row-outside-table limb=R1 recipe: PROBE: the S072 row is moved into a ``` fence at the end of SOURCES.md (not in the registry table) | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r1-forged-snapshot-self-consistent limb=R1 recipe: PROBE: S072.txt replaced by a 2-line forgery holding only the two quotes; manifest sha/bytes/lines/anchors and the row anchor sha re-pinned to it | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r1-correction-content-free limb=R1 recipe: PROBE: lesson correction reduced to 'Correction (round 45): S072 10029' (cites tokens, corrects nothing) | counter read: limb R1 fixed=1 read=S072=supersedes recheck-quotes=2 corrections=1 total=5
FALSE-GREEN mutant=r2-enforced-by-directory limb=R2 recipe: PROBE: R47 `enforced-by: `corpus`` (a directory; only os.path.exists is tested) | counter read: limb R2 fixed=1 read=criteria=3 total=5
FALSE-GREEN mutant=r2-vacuous-criterion limb=R2 recipe: PROBE: R48 criterion reduced to 'presence-only enforced-by: `LOG.md`' (keywords + any existing file) | counter read: limb R2 fixed=1 read=criteria=3 total=5
FALSE-GREEN mutant=r3-stub-selftest limb=R3 recipe: PROBE: r44-frontier-count.py replaced by a 5-line stub that prints `selftest cases=8 failures=0` | counter read: limb R3 fixed=1 read=selftest-cases=8 total=5
FALSE-GREEN mutant=r4-stub-freeze-check limb=R4 recipe: PROBE: freeze-check.py replaced by a 5-line stub printing both tokens | counter read: limb R4 fixed=1 read=selftest-cases=8 replay=base_ok=2 total=5
FALSE-GREEN mutant=r4-claims-weakened limb=R4 recipe: PROBE: tree claims.json counter_cmd of both claims replaced by `echo '<expect_before>'` | counter read: limb R4 fixed=1 read=selftest-cases=8 replay=base_ok=2 total=5
FALSE-GREEN mutant=r5-fabricated-receipt limb=R5 recipe: PROBE: refiled receipt is a 3-line hand-written text (comment carrying the invocation, the token, exit=0); nothing was run | counter read: limb R5 fixed=1 read=refiled=ok original=unchanged total=5
selftest cases=40 failures=9
```
Recipes (tree = GOOD, one change each; limb code in the counter):
- **r1-row-outside-table** (`limb_r1`, `sources_rows`, line 81). `sources_rows` matches any `^ {0,3}\|\s*S\d{3,}\s*\|` line, with no table or fence awareness. Delete the S072 row from the registry table and append it inside a fenced block. The counter reads S072.
- **r1-forged-snapshot-self-consistent**. The counter checks the snapshot's sha, the manifest sha, quote location, and the row anchor sha. It never checks that the snapshot is the page, or that its length matches the `10029` token the row asserts. Replace `S072.txt` with the two quote strings (2 lines) and re-pin manifest sha/bytes/lines/anchors and the row anchor sha. It reads fixed=1 with `recheck-quotes=2`. This is a limit of offline verification; the counter should at least pin the manifest sha, `bytes` and `lines` to the frozen capture values (20 152 / 10 032 / 312 for S071/S072 in the committed manifest).
- **r1-correction-content-free**. The Correction line is matched on the prefix `Correction (round 45`, `S072` and `10029` only. `Correction (round 45): S072 10029` passes.
- **r2-enforced-by-directory**. `os.path.exists` is the only test. `enforced-by: \`corpus\`` (a directory) passes.
- **r2-vacuous-criterion**. R48's criterion `presence-only enforced-by: \`LOG.md\`` passes. Keywords plus any existing file are the whole predicate, so R2 is itself a presence-only limb.
- **r3-stub-selftest**. `r44-frontier-count.py` as a 5-line script printing `selftest cases=8 failures=0` (and exiting 0) passes. The counter reads only the tokens and rc.
- **r4-stub-freeze-check**. The same shape for `freeze-check.py`; it also prints `freeze-check claims=2 base_ok=2 exit=0` for any args. It passes both the selftest check and the replay check.
- **r4-claims-weakened**. `limb_r4` replays `<tree>/.ufo/waves/round-45/claims.json`, the graded tree's own copy, not the frozen file at 8cf62c8. Replace both `counter_cmd` values with `echo '<expect_before>'`. Replay reads `base_ok=2`.
- **r5-fabricated-receipt**. A three-line hand-written file `# --root X --selftest --work Y` / `selftest cases=20 failures=0` / `exit=0` passes `limb_r5`. The invocation regex matches inside a comment, and nothing binds the receipt to a real run.

## Side findings (verified by commands)
1. `corpus/instruments/r44-routed-defects.py --selftest --work DIR` crashes with `FileNotFoundError` when DIR does not exist (`tempfile.mkdtemp ... r44-routed-defects.py line 715`). After `mkdir -p`, a run in an export of tip `c950fa3` printed `selftest cases=20 failures=0`.
2. The same selftest run against the pure base (`--root .` inside `/fast/scratch/hyaku/kasegi-r45/L1/pure`, `--work` pre-created) prints `selftest case=POSITIVE verdict=fail fixed=7 unresolved=1` and ends `selftest cases=20 failures=1`. `r44-routed-defects.py --root . --baseline .` at the pure base reads `R44-D4 status=unresolved detail=the round-44 LOG section does not record the affirmative planner=L1 mapping` and `fixed=7 unresolved=1`. So a base-derived tree cannot mint a fresh `cases=20 failures=0` receipt for R5; the harness binds the lane's recorded refiled receipt (tip c950fa3) and says so.
3. My freeze-check, from the kept GOOD tree: `selftest cases=8 failures=0` and, on the real claims file against the pure base:
```
claim C1 base_read=routed-defects total=5 fixed=0 unresolved=5 exit=1 verdict=ok finding=ok
claim C2 base_read=c2-gate fixed=1/7 exit=1 verdict=ok finding=ok
freeze-check claims=2 base_ok=2 exit=0
```
   This confirms the frozen expect_before strings are reproducible on the base.
4. My r44-frontier-count with `--selftest`: `selftest cases=8 failures=0`. `--root <pure>` printed `frontier rows=26 admitted=26`.
5. Coupling to note for the L1: removing `freeze-check.py` breaks both R4 and R2, because R47's `enforced-by:` path is `corpus/instruments/freeze-check.py`.
6. A control for the harness itself: the do-nothing/marker-only/null cases are in the run. The null mutant stays `fixed=5`, so the 27 rejections are real discrimination.

## Limitations
- The synthetic freeze-check.py and r44-frontier-count selftest are my own implementations, not the siblings' drafts. The false-greens do not depend on them (the stubs bypass the real ones), but R3/R4 "good" are my own. The sibling builders' drafts were not read, not run and not graded.
- S071 SOURCES row and the C2 artifacts are not built; this selftest covers C1 only. The replayed C2 at base reads `c2-gate fixed=1/7`.
- `r1-forged-snapshot` is a limit of any offline check; I report it as a finding, not as a counter bug that can be fully closed. The size-token (10029) is also unbound to the snapshot: the lane's S072.txt decodes to 10 030 characters / 10 032 bytes, and the counter does not compare any of these with the token.
- 9 "FALSE-GREEN" cases are probes I chose; they are not proof of an actual cheat in the current lane. The kill rule in claims.json ("predicate sentence changed after a seat has scored" is a violation) means fixes for them would be counter errata at best.
- Scratch (`/fast/scratch/hyaku/kasegi-r45/R45ExecSelftestC1*`) was removed before yield; only the draft script and this report remain.
- No git mutation, no edit to the counter, SKILL, QUALITY or any shared file.
