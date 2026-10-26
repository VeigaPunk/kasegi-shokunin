# ExecRDefectClosureSuite — R1–R9 instrument-soundness closure counter (round 34, C1)

Seat: executor (leaf), lane `kasegi-shokunin`, round 34, wave 1.
Write scope used: `corpus/instruments/r-defect-closure.sh` (new) and this receipt. Nothing else in the
lane was written; no git/jj mutation was run; no tool was installed.

## Report

### 1. Deliverable

`corpus/instruments/r-defect-closure.sh` — the C1 counter. Nine check functions, one per round-33
verifier-routed defect (`corpus/lessons/round-33-verifier-spotcheck.md` §5), bash 5, no `-e`, every
check `cd`s to the root under test before reading it (default root derived from the script's own
location: `<lane>/corpus/instruments/../..`).

```
$ sha256sum corpus/instruments/r-defect-closure.sh
809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d  corpus/instruments/r-defect-closure.sh
$ wc -l -c corpus/instruments/r-defect-closure.sh
832 35971 corpus/instruments/r-defect-closure.sh
$ bash -n corpus/instruments/r-defect-closure.sh ; echo bash-n_exit=$?
bash-n_exit=0
$ grep -cE '^check_r[1-9]\(\) \{' corpus/instruments/r-defect-closure.sh
9
$ grep -c '<LANE''_HASH>' corpus/instruments/r-defect-closure.sh      # the instrument carries no marker literal
0
```

Contract: a check exits **0 when its defect is closed** and **non-zero while it is open**; the plain
run prints one `R# check=... open=0|1` line per check and `closed=K/9 exit=0|1`, exit 0 only at
`K=9`; `--root DIR` points the same nine checks at another tree; `--selftest` runs each check twice
(live tree + a scratch fixture carrying that check's original defect) and counts a case as passing
only when the live run exits 0 **and** the broken fixture is rejected. Exit codes: 0 clean, 1
open/failure, 2 harness error (bad argument, missing root or scratch base).

### 2. The nine checks (predicate, surface read)

| id | surfaces read | closure predicate | descriptor printed on a closed tree |
|---|---|---|---|
| R1 | `SCORECARD.md` | literal marker count 0 AND an appended `Correction (round 34)` block naming `7963976e` and `014ee2d` | `SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d` |
| R2 | `SCORECARD.md`, `corpus/QUALITY.md` | `Erratum 2` block inside the round-33 section restating `"0 or 2+"` per id (`per id`/`own id scope`, `multi_row_url`, `dup-id`) AND an `R22` row stating satisfiability + pre-freeze | `SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step` |
| R3 | `corpus/QUALITY.md` | `Note (round 34)` below the R20 row, naming R20 + `exactly one` + `supersed` + per-id reading | `QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one')` |
| R4 | `corpus/QUALITY.md`, `SCORECARD.md`, `corpus/lessons/round-33.md` | the `R24` row (or one SCORECARD paragraph) carries `kill rule` + `selftest case=` + per-case wording AND the appended round-34 **R4** erratum carries the 3-of-4 figure, names the mutant obligation, corrects `all mutants killed`/`overstat` | `tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum` |
| R5 | `corpus/instruments/capture-binding-check.py` | `url-matching-two-rows` count 0 AND ≥11 case tuples still registered | `capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11)` |
| R6 | `corpus/source-snapshots/round-26/manifest.json` | `S040-live.txt` in `sources[].path` or in `orphan`/`orphans`, AND `purpose` names S040 and no longer says it was skipped | `round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected` |
| R7 | `corpus/lessons/round-33.md` | appended round-34 **R7** erratum: `19 → 31`, `23 → 22`, and `S050.txt:70` | `round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70)` |
| R8 | `corpus/source-snapshots/round-32/manifest.json` | every `fetched_utc` matches the frozen shape `^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$` or the frozen `+00:00` alternative, carries no non-zero `[+-]HH:MM` offset, **and** parses as a real calendar instant at UTC offset 0 — the accept set is capture-binding rule C's (`Z`, `+00:00`, fractional seconds), and the parse removes the loose regex's false positives | `round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset` |
| R9 | `capture-binding-check.py`, `frontier-recheck-count.py`, `c2-controls/` | the nine H4–H8 case names present AND rule A bidirectional **behaviourally** (mirror fixture passes, reverse fixture exits 1) AND the junk twin exists | `capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md` |

R4's limb 1 binds to the `| R24 |` row when it exists (so the three tokens cannot be spread across
the whole round-34 table) and falls back to one SCORECARD paragraph, which is the surface the frozen
claim allows.

### 3. Plain run on the landed tree — `closed=9/9 exit=0`

```
$ bash corpus/instruments/r-defect-closure.sh ; echo plain_exit=$?
R1 check=SCORECARD.md lane-hash-markers=0 + appended 'Correction (round 34)' naming 7963976e/014ee2d open=0
R2 check=SCORECARD.md round-33 'Erratum 2' per-id restatement + QUALITY.md R22 pre-freeze step open=0
R3 check=QUALITY.md appended round-34 note below R20 (per-id supersedes 'exactly one') open=0
R4 check=tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum open=0
R5 check=capture-binding-check.py url-matching-two-rows=0 cases=21 (>=11) open=0
R6 check=round-26 manifest binds S040-live.txt (record or orphan list) + purpose corrected open=0
R7 check=round-33 lesson appended R7 erratum (19->31, 23->22 characters, S050.txt:70) open=0
R8 check=round-32 manifest fetched_utc is a real strict-UTC instant (date-T time Z, zero offset), no '-' offset open=0
R9 check=capture-binding H4-H8 cases=9 + frontier rule A bidirectional (mirror=0 reverse=1) + junk=.ufo/waves/round-34/c2-controls/junk-f17.md open=0
closed=9/9 exit=0
plain_exit=0
```

### 4. `--selftest` — `cases=9 failures=0 exit=0` (the discriminator)

```
$ bash corpus/instruments/r-defect-closure.sh --selftest --scratch /fast/scratch/hyaku/kasegi-r34/ExecRDefectClosureSuite ; echo selftest_exit=$?
selftest case=R1 live=pass fixture=rejected control=absent verdict=pass
selftest case=R2 live=pass fixture=rejected control=absent verdict=pass
selftest case=R3 live=pass fixture=rejected control=absent verdict=pass
selftest case=R4 live=pass fixture=rejected control=absent verdict=pass
selftest case=R5 live=pass fixture=rejected control=absent verdict=pass
selftest case=R6 live=pass fixture=rejected control=absent verdict=pass
selftest case=R7 live=pass fixture=rejected control=absent verdict=pass
selftest case=R8 live=pass fixture=rejected control=pass verdict=pass
selftest case=R9 live=pass fixture=rejected control=absent verdict=pass
selftest cases=9 failures=0
selftest judge=forged-summary rejected=1
selftest judge=short-report rejected=1
selftest judge=complete-report accepted=1
selftest_exit=0
```

The three `selftest judge=` lines are the suite's judgement of its own report (§6), not additional
cases: the frozen predicate fixes the case count at nine.

Each broken fixture is a scratch tree holding only the files its check reads, with the check's
**round-33 defect** reintroduced (not an arbitrary mutation):

| case | fixture construction |
|---|---|
| R1 | `SCORECARD.md` copy + one appended line containing the marker literal |
| R2 | `SCORECARD.md` copy with every `Erratum 2` line dropped, `QUALITY.md` copy with the `R22` row dropped |
| R3 | `QUALITY.md` copy with the `Note (round 34)` line dropped |
| R4 | `QUALITY.md`/`SCORECARD.md` copies with the `selftest case=` record line dropped, lesson copy with the round-34 erratum lines dropped |
| R5 | instrument copy, the `case_duplicate_id_rows` tuple renamed back to `url-matching-two-rows` |
| R6 | round-26 manifest copy: S040 record/orphan key removed, `purpose` reset to the "skipped this round" text |
| R7 | lesson copy with the `S050.txt:70` and character-count correction lines dropped |
| R8 | round-32 manifest copy: every `fetched_utc` set to `2026-10-25Tgarbage-not-a-timeZ` — a value the frozen loose shape regex accepts and a real instant parse rejects (the original `-03:00` defect is covered by the base-tree run). **Positive control** (`control=pass`): the same manifest with `2026-10-26T04:16:06+00:00` and `2026-10-26T04:16:16.500Z`, which rule C accepts and R8 must not reject |
| R9 | instrument copies with the `nested-snapshot-dir` case line dropped (junk twin copied in) |

R8's fixture is the sharpest form of the round-33 defect, and it is the reason R8's parse limb exists:
`ExecCaptureBindingHarden` cross-checked (from `CritC1Kill`) that a Z-suffixed non-instant passes the
frozen shape regex while `capture-binding-check.py` rule C rejects it. Measured on the fixture value:

```
fixture values: ['2026-10-25Tgarbage-not-a-timeZ', '2026-10-25Tgarbage-not-a-timeZ']
frozen loose regex verdict: True
strict parse verdict: False
```

So a regex-only R8 would read this fixture `open=0`; the landed R8 rejects it.

The first version of the parse then over-rejected in the other direction: it demanded a literal `Z`
and its offset guard matched `+00:00`, so a stamp the frozen contract allows ("`+00:00` or `Z` only")
read `open=1` while rule C passed the same manifest. `ExecCaptureBindingHarden` measured that pair and
routed it. R8 now normalises a trailing `+00:00` to `Z` before the shape test, so its accept set is
rule C's (`Z`, `+00:00`, fractional seconds) and only non-zero offsets and non-instants fail. Measured
per value with `--root` on a one-file fixture:

```
value=2026-10-26T04:16:06+00:00        -> R8 … is a real strict-UTC instant … open=0
value=2026-10-26T04:16:16.500Z         -> R8 … is a real strict-UTC instant … open=0
value=2026-10-26T04:16:16-03:00        -> R8 … carries a fetched_utc that is not a strict-UTC instant open=1
value=2026-10-25Tgarbage-not-a-timeZ   -> R8 … carries a fetched_utc that is not a strict-UTC instant open=1
```

Both directions are now pinned in the selftest (defect fixture rejected, `+00:00`/fractional control
accepted), so neither divergence can return silently. On the landed bytes
`['2026-10-26T04:16:06Z', '2026-10-26T04:16:16Z']` the frozen regex and the parse agree.

### 5. Base-tree closure semantics — `closed=0/9 exit=1`

```
$ mkdir -p /fast/scratch/hyaku/kasegi-r34/ExecRDefectClosureSuite/base
$ git archive 014ee2d | tar -x -C /fast/scratch/hyaku/kasegi-r34/ExecRDefectClosureSuite/base
$ bash corpus/instruments/r-defect-closure.sh --root /fast/scratch/hyaku/kasegi-r34/ExecRDefectClosureSuite/base ; echo base_exit=$?
R1 check=SCORECARD.md lane-hash-markers=2 open=1
R2 check=no 'Erratum 2' block in SCORECARD.md open=1
R3 check=no appended 'Note (round 34)' below R20 open=1
R4 check=tightened kill-rule requirement not recorded (QUALITY R24 row or a SCORECARD paragraph: kill rule + one 'selftest case=' line per case) open=1
R5 check=misnamed selftest case 'url-matching-two-rows' still present (count=2) open=1
R6 check=round-26 manifest has no S040-live.txt record and no orphan list open=1
R7 check=round-33 lesson has no appended R7 erratum open=1
R8 check=round-32 manifest carries a fetched_utc that is not a strict-UTC instant open=1
R9 check=capture-binding H4-H8 cases missing: per-file-orphan-detected per-file-orphan-listed nested-snapshot-dir fetched-utc-pending-rejected fetched-utc-local-offset-rejected dup-record-in-manifest double-https-row rejected-row-anchor summary-only-selftest-rejected open=1
closed=0/9 exit=1
base_exit=1
```

Every check is therefore shown able to fail on the tree that carries its defect, and the suite fails
the frozen `closed=0/9` base-bytes clause. Harness error paths: `--root /nonexistent` ->
`suite UNAVAILABLE reason=root-missing root=/nonexistent`, exit 2; `--bogus` ->
`suite UNAVAILABLE reason=unknown-argument arg=--bogus`, exit 2.

### 6. The do-nothing control is rejected; the selftest is the discriminator

```
$ bash .ufo/waves/round-34/c1-controls/fake-suite.sh ; echo fake_plain_exit=$?
closed=9/9 exit=0
fake_plain_exit=0
$ bash .ufo/waves/round-34/c1-controls/fake-suite.sh --selftest ; echo fake_selftest_exit=$?
cases=9 failures=0
fake_selftest_exit=0
$ bash corpus/instruments/r-defect-closure.sh --selftest --scratch … | grep -c '^selftest case='
9
```

The fake reproduces both summary lines with no work. The discriminator is per-case evidence: the real
`--selftest` emits nine `selftest case=R# live=... fixture=... control=... verdict=...` lines, each
derived from real executions, and a case passes only if the live run is 0, the defect-bearing fixture
is non-zero and the control is accepted. The fake has no case table, so it can emit none; and because
it cannot exhibit a check that fails on a defect-bearing tree, its `closed=9/9` also reads `9/9` on
base bytes, where the real suite reads `0/9`.

`CritC1Kill-2` then attacked the remaining hole: an external reader can see the case lines, but the
suite itself never checked that they were there, so a mutant that replaces the top of `run_selftest()`
with `printf 'selftest cases=9 failures=0'; return 0` would print the claim's strings at exit 0 with
zero checks. The suite now judges its own report (`report_ok`, `plain_report_ok`,
`judge_selftest_report` in the instrument): the captured output must carry exactly nine case lines
with distinct ids R1..R9 and the matching summary, and `--selftest` proves that judgement on two
forged reports before trusting the real one. Replayed on copies of the landed bytes:

```
--- mutant: summary-only --selftest (critic's patch verbatim) ---
selftest cases=9 failures=0
selftest judge=forged-summary rejected=1
selftest judge=short-report rejected=1
selftest problem=self-report cases=0 expected=9
mutant_selftest_exit=1
--- mutant: summary-only plain run (same patch on run_plain) ---
closed=9/9 exit=0
suite problem=self-report plain-lines=0 expected=9
mutant_plain_exit=1
```

Bound, stated rather than implied: the judge binds *shape and consistency* of the report, not
provenance. A mutant that fabricates a complete nine-line report without running the checks would
still pass the self-judgement; what catches that class is the tree the run is pointed at (the
`--root` base run must read `closed=0/9`) and the external readers (the kill-rule matrix and the
review seats). The judge closes summary-only, short-report, duplicate-id and inconsistent-summary
forgeries — the routes that print the claim's strings with no work.

### 7. R9's reverse limb is load-bearing (base tool vs landed tool)

Same two fixture trees, run against the base instrument and the landed one (`S=/fast/scratch/hyaku/kasegi-r34/ExecRDefectClosureSuite`):

```
--- live frontier tool, mirror fixture ---
PASS     F99  knowledge/r9-fixture.md                              ids=S001           exit=0   
entries=1 pass=1 exit=0
mirror_exit=0
--- live frontier tool, reverse fixture ---
FAIL     F99  knowledge/r9-fixture.md                              ids=S001           exit=-    problems=selection-not-declared-by-entry
entries=1 pass=0 exit=1
reverse_exit=1
--- base (014ee2d) frontier tool, mirror fixture ---
PASS     F99  knowledge/r9-fixture.md                              ids=S001           exit=0   
entries=1 pass=1 exit=0
base_mirror_exit=0
--- base (014ee2d) frontier tool, reverse fixture ---
PASS     F99  knowledge/r9-fixture.md                              ids=S001           exit=0   
entries=1 pass=1 exit=0
base_reverse_exit=0
```

The reverse fixture's body cites both S001 and S002 in prose and its header declares S001 only, so
the only rule that can fire is the reverse limb; the base tool passes it (`exit=0`), the landed tool
fails it with exactly `selection-not-declared-by-entry` (`exit=1`). My first version of this fixture
was **not** discriminative (it also tripped `selection-not-cited-by-entry`, which the base tool
already catches); that is why the fixture now cites both ids in prose.

### 8. Subject state observed at the final run (bytes the checks read)

```
$ sha256sum SCORECARD.md corpus/QUALITY.md corpus/lessons/round-33.md \
    corpus/source-snapshots/round-{26,32}/manifest.json \
    corpus/instruments/{capture-binding-check.py,frontier-recheck-count.py,r-defect-closure.sh} \
    .ufo/waves/round-34/c2-controls/junk-f17.md
efa646c83baead97e41d9ccad65fac9a4d8468f6bb8af956446d347d68237e91  SCORECARD.md
77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8  corpus/QUALITY.md
f69472f38ea71039192592803f4d6f11b0f01d872ea46b0758da19c42f388807  corpus/lessons/round-33.md
33ac33c3caa6d43f3772b8cf8532b37cdb50f48db8ba667b5dd90645e8eacefa  corpus/source-snapshots/round-26/manifest.json
72ab4e6834b98cf7237cf8bb0f1ec6e667b55c3d9a153634d22771c238528eb6  corpus/source-snapshots/round-32/manifest.json
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249  corpus/instruments/frontier-recheck-count.py
357a7e4923bf784cd513dfaa94258d4cb6d5dfc1cbb677b36accbab86a05bc2d  (superseded) corpus/instruments/r-defect-closure.sh
2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc  (superseded) corpus/instruments/r-defect-closure.sh
809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d  corpus/instruments/r-defect-closure.sh (final)
2752a994265a1e284ebd236730d169d677e1923cfb7073cf79ad874d19bc4026  .ufo/waves/round-34/c2-controls/junk-f17.md
```

Re-measured on these bytes: `closed=9/9 exit=0`, `selftest cases=9 failures=0` plus the three
`selftest judge=` lines, `QUALITY.md` `^| R24 |` count 1, `Note (round 34)` count 1,
`frontier-recheck-count.py` `entries=20 pass=20 exit=0`. Several subject files moved while this seat
worked (`SCORECARD.md` `b8fc8c66…` -> `efa646c8…` as the round-34 section landed; the frontier tool
`8a79010d…` -> `1be79af6…`); every output above was re-taken on the digests in this block. No check
reads a digest of its own subject, so a later append re-opens a check only if it changes the named
evidence.

Named values the passing checks read, quoted:

- R6 — the round-26 manifest keeps `sources` = `['S041.txt']` and declares the orphan instead:
  `orphans` = one entry `{path: 'S040-live.txt', sha256: 'b7f7b55f…4e286c', row: 'S040',
  row_url: 'https://www.cisco.com/…/security_vulnerability_policy.html', captured_url:
  'https://sec.cloudapps.cisco.com/…', fetched_utc: '2026-10-25T12:34:27Z'}`; its `purpose` now opens
  "This manifest accounts for exactly the two files committed in this directory." and no longer
  contains "skipped this round".
- R8 — `[('S049', '2026-10-26T04:16:06Z'), ('S050', '2026-10-26T04:16:16Z')]`.
- R4 — `corpus/QUALITY.md` carries `| R24 | A counter's pass is its per-case evidence, not its summary
  line: … one `selftest case=<name> …` line per case … a kill rule that reads only the summary line is
  not a kill rule.`; `corpus/lessons/round-33.md:215` carries
  `## Erratum (round 34) — R4: "all mutants killed" overstated; the frozen kill rule caught 3 of 4`.
- R7 — `corpus/lessons/round-33.md:140` carries
  `## Erratum (round 34) — R7: the S049/S050 quote counts and the S050 sentence line`, with
  `— 19 → 31 and 23 → 22` and the `S050.txt:70` section.
- R5 — the instrument's case table has no `url-matching-two-rows`; `shared-url-between-two-records`
  is the renamed informational case and `duplicate-id-rows` keeps the dup-id coverage. My descriptor
  reads `cases=21` (the tuples matched by the shape regex) while the instrument's own `--selftest`
  prints `selftest cases=23` (two further cases are registered in a different list shape); the check
  only requires ≥11, so the reading is a floor, not an equality.
- R9 — capture-binding `--selftest` `selftest cases=23 failures=0`; frontier `entries=20 pass=20
  exit=0`; the nine required case names all present in the CASES list.

### 9. Read-only and scratch discipline

`grep -nE 'sed -E -i|>>"|mv "\$f|mkdir -p "\$dest|cp -p "\$LANE_ROOT|mktemp -d'` lists every write
site: they all target `$dest` (a fixture tree under the scratch root) or a `mktemp -d` directory, and
nothing else:

```
420:  tmp=$(mktemp -d "${TMPDIR:-/tmp}/rdc-r9.XXXXXX") …
492:    mkdir -p "$dest/$(dirname -- "$rel")"
493:    cp -p "$LANE_ROOT/$rel" "$dest/$rel"
502:  mv "$f.tmp" "$f"                       # $f is always a fixture path
509:  mkdir -p "$dest"
515:        '<LANE''_HASH>' >>"$dest/SCORECARD.md"
533:      sed -E -i '…' "$dest/corpus/instruments/capture-binding-check.py"
536:        sed -E -i '…' "$dest/corpus/instruments/capture-binding-check.py"
592:          mkdir -p "$dest/$(dirname -- "$j")"
593:          cp -p "$LANE_ROOT/$j" "$dest/$j"
613:  scratch=$(mktemp -d "$base/r-defect-closure-selftest.XXXXXX") …
```

No git command is executed; no file outside the scratch root is created or modified. The selftest
scratch tree is removed by an `EXIT` trap (verified: after a run, the scratch base held only this
seat's own files, no `r-defect-closure-selftest.*` directory).

One property the reviewer flagged as undocumented: the selftest sources its fixture bytes from
`$LANE_ROOT` (derived from the script's own location), not from `$RD_ROOT`. That is deliberate — the
fixtures are built from the bytes this instrument ships with, so `--selftest --root <other tree>` still
replays the *same* fixture copies — and it is fail-closed: a fixture whose source file is missing from
the lane prints `selftest problem=fixture-source-missing path=…` and the case fails rather than
passing.

### 10. Tooling

No install or upgrade was needed. Versions used: GNU bash 5.3.20, Python 3.14.8, GNU Awk 5.4.1,
`grep` 0.2.0 (pi-uu-grep). `shellcheck` is present at `/usr/bin/shellcheck` but was **not run**: this
seat's role directive defers lint/format gates to the parent after integration.

### 11. Findings and notes for the L1 (not verdicts)

1. **R4's first limb had no writer** when I first ran the suite (`closed=8/9`). The gap: the tightened
   kill-rule requirement is a *record*, and the only surfaces the frozen claim names are QUALITY
   R22/R24 or the SCORECARD section; R22 is R2's satisfiability row and carries no per-case clause,
   and R24 did not exist. I reported the exact matcher needed to `KasegiR34`; `ExecQualityAppends`
   then landed R24 and the limb closed. My check binds to that row rather than to the whole round-34
   table, following `ScribeQualityDraft`'s F6 note that paragraph-level matching would stay green if
   the tokens drifted apart.
2. **Two instrument defects of my own, found and fixed before freezing**, disclosed because they are
   exactly the class this counter exists to catch: (a) the selftest's live run reused `$RD_ROOT`
   after the fixture run had reassigned it, so cases 2–9 were measuring the previous fixture tree
   (live results then disagreed with the plain run); fixed by capturing `live_root` once before the
   loop. (b) My first R9 reverse fixture tripped `selection-not-cited-by-entry`, a limb the base
   instrument already enforces, so it would have read "bidirectional" against the base tool; the
   fixture now cites both ids in prose and only `selection-not-declared-by-entry` separates the two
   instruments (§7).
3. **R9's junk limb resolves to `.ufo/waves/round-34/c2-controls/junk-f17.md`** (the frozen control,
   untracked at my read; the check also accepts a repo-root `c2-controls/junk-f17.md`). Commit
   membership is outside this suite — it reads bytes; the C1 kill rule's "committed" clause is the
   L1's/regression seat's check.
4. **R1's predicate depends on the correction prose not containing the literal marker**;
   `ExecScorecardMarkers` wrote "the two lane-hash placeholders above" instead of quoting the token,
   which is what makes count 0 and the correction co-exist. A later edit that quotes the token in
   that paragraph re-opens R1, correctly. The instrument itself avoids the contiguous token (its
   pattern is `'<LANE''_HASH>'`), so a repo-wide grep for the marker finds none in this file.
5. **R4/R7 lesson limbs key on the heading text** `Erratum (round 34)` plus `R4`/`R7` and an
   append-order test against `## Touched surfaces and provenance`. `ExecLessonErrata` is the
   sole writer of `corpus/lessons/round-33.md`; if that heading wording changes, the checks must be
   updated with it.
6. **R8 was corrected twice by peer cross-checks, both inside the frozen predicate.** (a)
   `ExecCaptureBindingHarden` reported (from `CritC1Kill`) that `fetched_utc = "2026-10-25Tgarbage-not-a-timeZ"`
   passes the frozen shape regex `^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*Z$` while `capture-binding-check.py`
   rule C rejects it as `detail=malformed` — a regex-only R8 could score the round-32 manifest closed
   on a value the instrument it closes over refuses. R8 gained a real `datetime.fromisoformat` instant
   parse at UTC offset 0, fixture switched to the garbage value. (b) The same seat then measured the
   opposite divergence: the new parse required a literal `Z` and its offset guard matched `+00:00`, so
   a stamp the frozen contract allows (`+00:00` or `Z` only) read `open=1` while rule C passed it.
   R8 now normalises a trailing `+00:00` to `Z`, giving rule C's accept set; a positive-control
   fixture (`control=pass`) pins the boundary in the selftest, and per-value probes are recorded in
   §4. I kept a self-contained parse rather than delegating to rule C because delegating on the
   instrument's exit couples R8 to the whole-corpus run (which read `binding_exit=1` on an unrelated
   unappended registry row).
7. **Degenerate-orphan route is NOT covered here.** `ExecCaptureBindingHarden` also relayed
   `CritC1Kill`'s finding that a manifest dir with captures and `"sources": []`, every capture
   declared as an orphan, prints `records=0` at exit 0; the guard is not landed. That is an
   instrument-rule gap routed to the L1, not one of R1–R9, and neither R6 nor R9 claims to catch it:
   R6 requires S040-live.txt to be bound or declared in the specific round-26 manifest, and R9 checks
   case names, bidirectionality and the junk twin. A suite reading `closed=9/9` is not evidence
   against that route.
8. **A summary-only forgery of this suite was a live route until `CritC1Kill-2` measured it.** The
   attack: replace the top of `run_selftest()` with `printf 'selftest cases=9 failures=0'; return 0`
   (or the same on `run_plain` with `closed=9/9 exit=0`) and the claim's strings print at exit 0 with
   no check performed. The suite now judges its own report — nine named case lines with distinct ids
   R1..R9 plus a consistent summary for `--selftest`, nine named check lines plus a consistent
   `closed=K/9` for the plain run — and proves that judgement on two forged reports
   (`selftest judge=forged-summary rejected=1`, `selftest judge=short-report rejected=1`,
   `selftest judge=complete-report accepted=1`). Both mutants replayed on copies of the landed bytes
   now exit 1 (§6). The frozen case count stays nine: the judge lines are not cases.
9. **`kill-rule-check.py`'s digest is deliberately not pinned here.** `CritC1Kill-2` notes the
   counter's `counter_sha256=c279d952…` is unpinned in-tree and offers a one-line sha256 comparison
   in this suite. I declined: R1–R9 do not include the mutant matrix (R4 is the tightened-rule
   *record* and the lesson erratum), the file is another seat's in-flight artifact in this same wave
   (`kill-rule-check.py` did not exist at my last read), and a digest pin would make this suite's
   exit status depend on that file's churn rather than on the nine defects it counts. The C1 clause
   `kill-rule-check.py -> survivors=0` belongs to the seat that owns the instrument and to the
   do-nothing-reject seat; if the L1 wants the pin, it belongs in `claims.json` (frozen literal) or in
   that instrument's own selftest, not in the closure suite.
10. **Measurement moment**: the digests in §8 were taken after the wave's fixes landed and before the
    L1's integration commit. Values in §4–§5 depend only on committed-plus-untracked bytes at that
    moment; the suite reads no git state.

### 12. Risks

- **Self-report binds shape, not provenance.** A mutant that fabricates a complete nine-line report
  without running the checks passes the suite's own judgement. What catches that class is the tree
  the run is pointed at (`--root` of base bytes must read `closed=0/9`) and the external readers
  (kill-rule matrix, review seats). Summary-only, short, duplicate-id and inconsistent-summary
  forgeries are closed.
- R8 checks only the round-32 manifest (as the frozen predicate states); a non-UTC `fetched_utc`
  introduced into a different manifest is caught by `capture-binding-check.py` rule C, not by this
  suite. R8's accept set is rule C's (`Z`, `+00:00`, fractional seconds) and its parse rejects
  non-instants and non-zero offsets, so it cannot disagree with a real-value reading of either the
  frozen regex or the instrument.
- R6 accepts a record *or* an orphan declaration; it does not re-derive the capture's sha256. The
  instrument's own per-file binding (`orphan=`/`rule=orphan-capture`) is where the bytes are checked.
- R5's ≥11 floor is a case-table size guard, not a semantic check that each case asserts what its name
  says; that depth belongs to the instrument's own 23-case selftest and to the kill-rule counter.

### 13. Blockers

None.
