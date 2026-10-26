# ExecD3SkillRegistry — D3: register `r-defect-closure.sh` + `kill-rule-check.py` at the Gates & probes registry home

Seat: leaf of round-35 wave 1 (L1 = KasegiR35). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scope: `SKILL.md` registry append only. No git/jj mutation run (L1 commits). No scratch tree created; no tool install.

## Report

### 1. Defect state before the append (D3)

Source text: `corpus/lessons/round-34-verifier-spotcheck.md:177` — "**D3 — gates unregistered at the registry
home.**"; lines 178-180 name both instruments and require name, gate|probe, entry command, verdict map,
selftest spelling, pinned-value path, write scope, owner.

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -c 'r-defect-closure' SKILL.md
0
$ grep -c 'kill-rule-check' SKILL.md
0
```
Both exit 0 with count 0 — the two instruments had no registry row. The commit history agrees: the
round-34 frozen before-control `.ufo/waves/round-34/c1-controls/before.txt:5-6` reads
`ls: cannot access 'corpus/instruments/r-defect-closure.sh': No such file or directory` / `ls_exit=2`,
and `.ufo/waves/round-34/wave1/ScribeSkillGate/pins-and-instruments.txt:11-12` reads
`ABSENT corpus/instruments/r-defect-closure.sh` / `ABSENT corpus/instruments/kill-rule-check.py`.

Both files are committed and clean at the lane base (read-only checks):
```
$ git ls-files corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py
corpus/instruments/kill-rule-check.py
corpus/instruments/r-defect-closure.sh
$ git status --porcelain -- corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py SKILL.md
(empty; exit 0)
```

### 2. Placement decision (R6)

The registry home table is `SKILL.md:977-982` ("## Gates & probes registry"), mid-file. R6 forbids mid-table
insertion, and rounds 29/30/31/33 all append a fresh per-round section at end of file. I therefore appended
one new section at EOF rather than touching the mid-file table. Appended rows only; zero existing lines moved.

```
$ git diff --numstat -- SKILL.md
13	0	SKILL.md
$ git diff -U0 -- SKILL.md | grep -c '^-[^-]'   # removed non-header lines
0
```

Before/after digests:
```
before: 1091 lines  ba5ebe5d9417b1801d48bbdb8fa533eb9df586f588bbad398eacd062e408163e  SKILL.md
after:  1104 lines  daeff71be4d0ee991599abfba16721d878ab957f6e047da07b171b60a0b67dbc  SKILL.md  (corrected from the first append digest 0cc95638… — see §4b)
```

### 3. Appended section (verbatim, `SKILL.md:1093-1104`)

Heading: `## Round-35 Gates & probes registry addition (appended 2026-10-26)` at `SKILL.md:1093`, then the
eight-column header/separator as in the earlier registry additions, then these two rows:

| name | type | entry command | verdict map | self-test | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|---|
| r-defect-closure.sh | gate\|probe | `bash corpus/instruments/r-defect-closure.sh [--root DIR]`; the root defaults to this script's lane and every check honours `--root`, so the base-tree control is `bash corpus/instruments/r-defect-closure.sh --root <base-extraction>` | plain run: one `R# check=<desc> open=0\|1` line per check R1–R9, then `closed=K/9 exit=0\|1`; exit 0 only for K=9, exit 1 while any check is open or when the suite's self-report judgement fails (`suite problem=self-report plain-lines=N expected=9`), exit 2 on harness error (`suite UNAVAILABLE reason=root-argument-missing\|root-missing\|scratch-argument-missing\|unknown-argument`). Each check exits 0 when its round-33 defect is CLOSED and non-zero while it is still OPEN, so a summary-only printer cannot read `closed=9/9` on defect-bearing bytes | `bash corpus/instruments/r-defect-closure.sh --selftest [--scratch DIR]` -> per check one `selftest case=R# live=pass fixture=rejected control=pass\|absent verdict=pass` line (or `verdict=fail problems=...`), then `selftest judge=forged-summary rejected=1`, `selftest judge=short-report rejected=1`, `selftest judge=complete-report accepted=1`, then `selftest cases=9 failures=0`; exit 0 only when all nine live runs pass, every defect fixture is rejected and the complete report is accepted, exit 1 on any case failure or `selftest problem=self-report ...`, exit 2 on `selftest UNAVAILABLE reason=scratch-missing\|scratch-create-failed` | the pinned expected values are the check literals inside `corpus/instruments/r-defect-closure.sh` (R1 `7963976e`/`014ee2d`; R2 `0 or 2+`, `multi_row_url`, `dup-id`, R22 satisfiability; R3 `R20`/`exactly one`/superseded; R4 kill-rule prose plus one `selftest case=` line; R5 no `url-matching-two-rows`; R6 `S040-live.txt`; R7 `19->31`, `23->22`, `corpus/source-snapshots/round-32/S050.txt:70`; R8 the `Z`/`+00:00`/fractional accept set; R9 the nine capture-binding case names plus frontier rule A mirror/reverse), measured against the committed files they read (`SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-33.md`, `corpus/source-snapshots/round-26/manifest.json`, `corpus/source-snapshots/round-32/manifest.json`); the frozen before-state they discriminate is `.ufo/waves/round-34/c1-controls/before.txt` | read-only on the lane: every check only reads files under the root; the only writes are its own scratch fixtures under `--selftest` (scratch base = `--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`, else `/tmp`), removed on exit; no git command is run and nothing outside the scratch directory is written | kasegi-shokunin |
| kill-rule-check.py | gate\|probe | `cd <lane> && python3 corpus/instruments/kill-rule-check.py [--instrument PATH] [--fake PATH] [--root DIR] [--scratch DIR] [--row-file PATH] [--json PATH]` (the default root derives from the script path, so the `cd` is canonical rather than required; default instrument `corpus/instruments/capture-binding-check.py`) | header `KILL-RULE instrument=... sha256=... bytes=... lines=... floor=19 counter_sha256=...`; one `probe <name> pristine=pass\|fail exit=...` per probe (`selftest-shape` plus the eight fixture lanes); per row `mutant-patch ... status=ok\|invalid:<reason>`, `mutant-bytes`, one `mutant-probe ... pristine=pass mutant=pass\|fail`, `mutant=<name> killed=0\|1`, `mutant-invalid`; `control=CTL-{noop,nocompile,equivalent,fake-killrule} verdict=... expect=... ok=0\|1`; `controls=4 rejected=K`; `GATE ok\|fail name=<named-rows\|pristine-selftest\|pristine-fixtures\|pristine-determinism\|rows-valid\|controls\|survivors-zero>`; `mutants=3 killed=K survivors=K invalid=K`; `gates=7 failed=K`; final `survivors=K`. Exit 0 iff `survivors=0` AND `invalid=0` AND `failed=0`; exit 1 on any survivor, any invalid row, or any failed gate (the CTL-equivalent witness deliberately prints `survivors=1`, exit 1); exit 2 on `UNAVAILABLE reason=instrument\|row-file`. `invalid:` reasons are `find-count`, `noop`, `nocompile`, `anchor-mismatch`, `nondeterministic`, `inconsistent-kill` — an invalid row is never relabelled killed and never counted as a survivor | `python3 corpus/instruments/kill-rule-check.py --selftest` -> three arithmetic scenarios, each `selftest case=<name> got=<(killed,survivors,invalid,exit)> want=<...> verdict=pass\|fail`, then `selftest cases=3 failures=0`; exit 0 iff `failures=0`, else 1; it runs no instrument and no subprocess | `corpus/instruments/kill-rule-check.py` itself: the three `MUTANTS` patches, their `ROW_PINS` `find` and `find\0replace` sha256 literals, `CASE_FLOOR = 19`, and the CTL patch anchors; the do-nothing fake control is the newest `.ufo/waves/round-*/c1-controls/fake-killrule.py` (round 35 carries none, so round-34's file binds; `--fake PATH` overrides) | read-only on the lane: reads the instrument under test and writes only scratch fixture lanes, mutant copies and their `pyc` under its scratch root (`--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`), removed on exit; `--json PATH` writes only that path | kasegi-shokunin |

Followed by three short paragraphs at `SKILL.md:1101-1104` (D3 close-out with the before-counts; measured
digests; re-verify commands), including the explicit statement that the plain-run values are the contract
read from the committed source plus the round-34 receipts, not a round-35 run.

### 4. Field-count verification (eight fields per row)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 - <<'PY'
import re
lines=open('SKILL.md',encoding='utf-8').read().splitlines()
st=next(i for i,l in enumerate(lines) if l.startswith('## Round-35 Gates'))
rows=[l for l in lines[st:] if l.startswith('|')]
for r in rows:
    c=re.split(r'(?<!\\)\|', r)[1:-1]
    print("fields=%d first=%r" % (len(c), c[0]))
PY
fields=8 first=' name '
fields=8 first='---'
fields=8 first=' r-defect-closure.sh '
fields=8 first=' kill-rule-check.py '
```
(exit 0; header, separator and both data rows carry exactly eight cells, `\|` inside cells does not split them)

```
$ grep -c 'r-defect-closure' SKILL.md
4
$ grep -c 'kill-rule-check' SKILL.md
4
$ grep -n 'Round-35 Gates' SKILL.md
1093:## Round-35 Gates & probes registry addition (appended 2026-10-26)
```
All exit 0; both acceptance counts are >= 1 (4 each: two table mentions plus two prose mentions).

### 4b. Correction after the append: bare `S050.txt:70` cite cleared

`ExecScoreGap` reported at 2026-10-26T06:35Z that `python3 -B corpus/instruments/anchorcheck.py SKILL.md`
read `15 in-range cite instances, 0 bad; … BASE-ABSENT=1`, exit 1, on the failing instance
`BASE-ABSENT md:1097 S050.txt:70 (base tree absent: /home/vgpnk/Projects/the-bounty-hunter/S050.txt)` —
the bare token I put inside the new `r-defect-closure.sh` row (their context: `.ufo/waves/round-35/wave1/ExecScoreGap.md` §2a).

Fix: the row now spells the cite the way `SKILL.md:1084` already spells the same capture,
`corpus/source-snapshots/round-32/S050.txt:70`, so it resolves in-lane instead of arming the absent
bounty-base arm. The erratum it describes (round-33 lesson R7) still cites line 70, and the line exists:
```
$ wc -l corpus/source-snapshots/round-32/S050.txt
630 corpus/source-snapshots/round-32/S050.txt
$ sed -n '70p' corpus/source-snapshots/round-32/S050.txt | cut -c1-40
本标准适用于 360 集团发布的产品和业务，此外 360 集团所投资的公司…
$ grep -c 'S050.txt:70' SKILL.md
1
```
(exit 0; one occurrence, and it is the prefixed spelling at `SKILL.md:1097`). I did not re-run `anchorcheck.py`
— the parent's post-integration gate owns that re-measurement per this wave's rule; the report above is
`ExecScoreGap`'s, not mine. No other bare relative `file:line` token was introduced: the rest of the section
uses `corpus/…`, `.ufo/…` or `.md:NNN` prefixed spellings.

### 5. Instrument digests and the facts each row states

```
$ sha256sum corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py corpus/instruments/capture-binding-check.py
809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d  corpus/instruments/r-defect-closure.sh
c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61  corpus/instruments/kill-rule-check.py
3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa  corpus/instruments/capture-binding-check.py
$ wc -l corpus/instruments/r-defect-closure.sh corpus/instruments/kill-rule-check.py
832 corpus/instruments/r-defect-closure.sh
881 corpus/instruments/kill-rule-check.py
```
All exit 0. Row facts were read from the committed source, not inferred:
- `r-defect-closure.sh:90-91` — `Exit codes: 0 closed / selftest clean, 1 open defect(s) / selftest failure,
  2 harness error`; `:491` — `CHECK_IDS=(R1 … R9)`; `:502-521` `run_plain` prints
  `R# check=… open=0|1` then `closed=K/9 exit=0|1`; `:108-119` the four `suite UNAVAILABLE` reasons;
  `:528-586` `report_ok`/`plain_report_ok`/`judge_selftest_report` (forged-summary, short-report,
  complete-report); `:748-810` `run_selftest` prints the nine per-case lines then
  `selftest cases=%d failures=%d`; `:752-756` the two `selftest UNAVAILABLE` reasons.
- `kill-rule-check.py:387-392` scratch order `--scratch`/`$HYAKU_SCRATCH`/`$TMPDIR`; `:346-366` nine
  `PROBES` (1 `selftest-shape` + 8 fixture lanes); `:208-221` three `control_rows()` plus the fake
  (`controls=len+1` at `:838`); `:831-846` seven `GATE` names; `:847-851` the three summary lines;
  `:875` `return 0 if (survivors == 0 and invalid == 0 and failed == 0) else 1`; `:503-563` the
  `invalid:` reason set; `:653-666` the `--selftest` three-scenario printer and `selftest cases=3` shape.

Round-34 receipts on the same behaviours (quoted, not summarised): `.ufo/waves/round-34/wave1/ExecCaptureBindingHarden.md:505-507`
"Live suite: `closed=9/9 exit=0`; `--selftest` prints `selftest case=R8 live=pass fixture=rejected control=pass verdict=pass` and
`selftest cases=9 failures=0`, exit 0."; `.ufo/waves/round-34/wave1/MutSelftestSummary.md:332-333`
"Full counter re-run on the same current bytes: `mutants=3 killed=3 survivors=0 invalid=0`, `gates=6 failed=0`, `survivors=0`, exit 0".
The `gates=6`→`gates=7` drift is stated in the appended prose: the committed source lists seven gates now.

### 6. Scope, no-harm and retained state

- Files written by this seat: `SKILL.md` (append only) and this receipt. Nothing else in the lane, the
  fleet root, bounties or shokuknow was opened for write.
- No `git add/commit/push`, no jj command, no lane-external tool run. No scratch directory was created
  (`/fast/scratch/hyaku/kasegi-r35/ExecD3SkillRegistry/` does not exist), so nothing to clean up.
- No tool install or upgrade.
- I did not run either instrument's plain or `--selftest` run: this wave's rule reserves gate execution
  for the parent post-integration. The rows therefore document the contract from the committed source and
  cite round-34's measured receipts; the appended prose says so in those words.

## Findings / risks

1. **Name split inside claim C1.** Frozen C1's predicate and counting commands name `corpus/instruments/r35-defect-closure.sh`
   with seven D1–D7 checks (`closed=7/7`, `cases=7`), while D3 and my assignment name
   `corpus/instruments/r-defect-closure.sh`, which is the committed nine-check R1–R9 suite
   (`closed=K/9`, `cases=9`). The two rows I appended register the latter pair exactly as D3 words it. If C1
   lands a separate `r35-defect-closure.sh`, that file still has no registry row and D3's "registry registers
   the round-34-discovered gates" wording is satisfied only for the two instruments named in D3. Integration
   decision for the L1; I did not widen scope to a name I was not assigned.
2. **Registry rows are contract-level.** They are registration (D3's "not graded conformant until
   registered"), not a fresh green verdict. The parent's post-integration run is the measurement.
3. **Digest-pinned prose.** `r-defect-closure.sh:153-154` itself pins the round-34 hashes `7963976e`/`014ee2d`
   in `SCORECARD.md`, and its R1–R9 checks read `SCORECARD.md`, `corpus/QUALITY.md` and `corpus/lessons/round-33.md`.
   Sibling seats appending to those files (D1/D2/D7 work) change what the suite reads; both instruments read
   files that other wave-1 seats may touch, so the parent should run the closure suite after all appends land.
4. **No blockers.** The append needed no external input; the eight fields are all backed by the committed
   source lines quoted in §5.
