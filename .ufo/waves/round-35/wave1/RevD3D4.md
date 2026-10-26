# RevD3D4 — round 35 wave 1 — D3/D4 fix review

Seat: RevD3D4 (reviewer leaf). Item: review the D3/D4 fixes with a verdict and evidence —

- **D3** (`corpus/lessons/round-34-verifier-spotcheck.md:177-182`): SKILL.md Gates & probes
  registry rows for `r-defect-closure.sh` and `kill-rule-check.py` exist and carry all eight
  fields (name, gate|probe, entry command, verdict map, selftest spelling, pinned-value path,
  write scope, owner).
- **D4** (`round-34-verifier-spotcheck.md:183-187`): `.ufo/waves/round-34/wave1-results.json`
  is tracked (`git ls-files` → 1) and the provenance note exists beside it with the file's
  sha256.

## Report

Measured 2026-10-26 against the lane worktree at HEAD `da2d3c687f82a9814ee71c91c930cb733050d37c`
("round-35: wave-1 spec + dispatch (64 seats, v2)"); claims-freeze `617496b9c6e92bc671e7e78b83df69a04470d0e9`;
lane base `3266c9937b03062d9bbc2f436e20820115ed179c`. All commands run from
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless stated. No tool installs (none needed).

Tree state at measurement (`git status --porcelain`, excerpt): ` M SCORECARD.md`, ` M SKILL.md`,
`?? .ufo/waves/round-34/wave1-results.json`, `?? .ufo/waves/round-34/wave1-results.json.provenance.md`,
`?? corpus/instruments/r35-defect-closure.sh`, `?? .ufo/waves/round-35/wave1/` — the wave's
landings are worktree-only; the L1 has not committed since the dispatch commit.

### 1. D3 — SKILL.md Gates & probes registry rows

**1.1 Before-state (frozen).** `git show 617496b:SKILL.md | grep -c 'r-defect-closure'` → `0`;
`git show 617496b:SKILL.md | grep -c 'kill-rule-check'` → `0`. At HEAD `da2d3c6` both counts are
also `0`: the rows are uncommitted worktree changes (SKILL.md is ` M`), landing with the L1's
integration commit.

**1.2 Rows present.** SKILL.md:1093 `## Round-35 Gates & probes registry addition (appended
2026-10-26)`; header row SKILL.md:1095 is the same eight columns as the main registry
(SKILL.md:979): `| name | type | entry command | verdict map | self-test | pinned-value path |
write scope | owner |`. Rows: SKILL.md:1097 (`r-defect-closure.sh`), SKILL.md:1098
(`kill-rule-check.py`). Occurrence counts now: `grep -c 'r-defect-closure' SKILL.md` → 4,
`grep -c 'kill-rule-check' SKILL.md` → 4 (rows + prose).

**1.3 All eight fields populated in both rows** (read whole via `SKILL.md:raw:1097`, `:raw:1098`):

| field | r-defect-closure.sh (SKILL.md:1097) | kill-rule-check.py (SKILL.md:1098) |
|---|---|---|
| name | `r-defect-closure.sh` | `kill-rule-check.py` |
| gate\|probe (type col) | `gate\|probe` | `gate\|probe` |
| entry command | `bash corpus/instruments/r-defect-closure.sh [--root DIR]` + base-tree control `--root <base-extraction>` | `cd <lane> && python3 corpus/instruments/kill-rule-check.py [--instrument PATH] [--fake PATH] [--root DIR] [--scratch DIR] [--row-file PATH] [--json PATH]`, default instrument `capture-binding-check.py` |
| verdict map | per-check `R# check=<desc> open=0\|1` ×R1–R9, `closed=K/9 exit=0\|1`; exit 0 only K=9; exit 1 open/self-report-judgement; exit 2 `suite UNAVAILABLE reason=root-argument-missing\|root-missing\|scratch-argument-missing\|unknown-argument` | header `KILL-RULE instrument=... sha256=... bytes=... lines=... floor=19 counter_sha256=...`; `probe <name> pristine=pass\|fail exit=...` ×9; `mutant-patch/-bytes/-probe/mutant=/mutant-invalid`; `control=CTL-{noop,nocompile,equivalent,fake-killrule}`; `controls=4 rejected=K`; `GATE ok\|fail name=<7 names>`; `mutants=3 killed=K survivors=K invalid=K`; `gates=7 failed=K`; final `survivors=K`; exit 0 iff survivors=0 ∧ invalid=0 ∧ failed=0; exit 1 otherwise; exit 2 `UNAVAILABLE reason=instrument\|row-file`; six `invalid:` reasons enumerated |
| self-test | `--selftest [--scratch DIR]` → per-check `selftest case=R# live=pass fixture=rejected control=pass\|absent verdict=pass`, three `selftest judge=` lines, `selftest cases=9 failures=0`; exit 0/1/2 semantics | `--selftest` → three arithmetic scenarios `selftest case=<name> got=<...> want=<...> verdict=pass\|fail`, `selftest cases=3 failures=0`; exit 0 iff failures=0; runs no instrument and no subprocess |
| pinned-value path | check literals inside `corpus/instruments/r-defect-closure.sh` (R1 `7963976e`/`014ee2d`; R2–R9 literals enumerated); measured against the committed files they read; frozen before-state `.ufo/waves/round-34/c1-controls/before.txt` | the script itself: three `MUTANTS` patches, `ROW_PINS` find/find\0replace sha256 literals, `CASE_FLOOR = 19`, CTL patch anchors; fake control = newest `.ufo/waves/round-*/c1-controls/fake-killrule.py` (round 35 carries none → round-34's binds; `--fake PATH` overrides) |
| write scope | read-only on the lane; only `--selftest` scratch fixtures (`--scratch`, else `$HYAKU_SCRATCH`, else `$TMPDIR`, else `/tmp`), removed on exit; no git command | read-only on the lane; scratch fixture lanes + mutant copies + `pyc` under its scratch root, removed on exit; `--json PATH` writes only that path |
| owner | `kasegi-shokunin` | `kasegi-shokunin` |

**1.4 Append-only (R6, `corpus/QUALITY.md:40`).** `git diff --numstat 617496b -- SKILL.md` →
`13	0	SKILL.md`; single hunk `@@ -1089,3 +1089,16 @@` at EOF; file 1091 → 1104 lines. No
existing line moved.

**1.5 Pinned values vs bytes (all match).**

```
sha256sum corpus/instruments/r-defect-closure.sh
  → 809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d   (row: same)   exit 0
sha256sum corpus/instruments/kill-rule-check.py
  → c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61   (row: same)   exit 0
sha256sum corpus/instruments/capture-binding-check.py
  → 3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa   (row: same)   exit 0
wc -l → 832 / 881        (row: "832 lines" / "881 lines")              ✓
grep -n CHECK_IDS corpus/instruments/r-defect-closure.sh
  → 491:CHECK_IDS=(R1 R2 R3 R4 R5 R6 R7 R8 R9)                        (row: R1–R9)  ✓
grep -c '7963976e' / '014ee2d' in the suite → 3 / 4                    (row: R1 pins) ✓
grep -n CASE_FLOOR corpus/instruments/kill-rule-check.py
  → 143:CASE_FLOOR = 19                                               (row: floor=19) ✓
grep -n ROW_PINS → 54, 110                                            (row: ROW_PINS) ✓
```

Fake-control binding verified: `.ufo/waves/round-35/c1-controls/` holds only `before.txt` and
`fake-suite.sh` (no `fake-killrule.py`), and the live plain run printed
`fake=/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-34/c1-controls/fake-killrule.py`
— exactly the row's "round 35 carries none, so round-34's file binds". The frozen before-state
`.ufo/waves/round-34/c1-controls/before.txt` exists (1552 B, base `014ee2d7…` header).

**1.6 Registered invocations executed live (worktree bytes).** Full logs preserved at
`.ufo/waves/round-35/wave1/RevD3D4/{r-suite-plain,r-suite-selftest,killrule-plain,killrule-selftest}.log`
(digests in §4).

- `bash corpus/instruments/r-defect-closure.sh` → nine `R# check=… open=0` lines (R1–R9), then
  `closed=9/9 exit=0`; **exit 0**. Matches the registered verdict map line-for-line.
- `bash corpus/instruments/r-defect-closure.sh --selftest --scratch <dir>` → nine
  `selftest case=R# live=pass fixture=rejected control=absent|pass verdict=pass` lines (R8 is
  the `control=pass` case), `selftest cases=9 failures=0`, then `selftest judge=forged-summary
  rejected=1`, `selftest judge=short-report rejected=1`, `selftest judge=complete-report
  accepted=1`; **exit 0**. All registered spellings present and exact.
- Missing-scratch arm: `--scratch <nonexistent>` → `selftest UNAVAILABLE reason=scratch-missing
  base=…`; **exit 2** — matches the registered exit-2 semantics.
- `bash corpus/instruments/r-defect-closure.sh --root /nonexistent/xyz` → `suite UNAVAILABLE
  reason=root-missing root=/nonexistent/xyz`; **exit 2** — matches (`--root` is honoured).
- `python3 corpus/instruments/kill-rule-check.py --selftest` → `selftest case=all-killed
  got=(3, 0, 0, 0) want=(3, 0, 0, 0) verdict=pass`, `one-survivor` and `one-invalid` likewise,
  `selftest cases=3 failures=0`; **exit 0**. Matches the registered selftest spelling exactly.
- `python3 corpus/instruments/kill-rule-check.py --scratch <dir>` → header `KILL-RULE
  instrument=corpus/instruments/capture-binding-check.py sha256=3d9e5e0d… bytes=40556 lines=892
  floor=19 counter_sha256=c279d952…` (counter digest = the checker's own pinned digest), nine
  `probe <name> pristine=pass exit=…` lines (`selftest-shape` + the eight fixture lanes), three
  mutants each `status=ok` / `killed=1` (10 `mutant-probe` lines per mutant),
  `control=CTL-noop verdict=invalid:noop ok=1`, `CTL-nocompile invalid:nocompile ok=1`,
  `CTL-equivalent verdict=survivor ok=1 witness_survivors=1 witness_exit=1` (the registered
  deliberate witness), `CTL-fake-killrule verdict=opaque ok=1`, `controls=4 rejected=4`, seven
  `GATE ok` lines, `mutants=3 killed=3 survivors=0 invalid=0`, `gates=7 failed=0`,
  `survivors=0`; **exit 0**. Matches the registered verdict map in full.
- Instrument-missing arm: `--instrument /nonexistent/xyz.py` → `UNAVAILABLE reason=instrument
  [Errno 2] …`; **exit 2** — matches.
- `cd`-not-required claim: plain run from a foreign cwd (`/fast/scratch/hyaku/kasegi-r35/RevD3D4`)
  with the absolute script path still derived the lane root and printed `survivors=0`, **exit 0**.

**1.7 Finding F1 (minor, row SKILL.md:1097 self-test field).** The row describes the selftest
line order as "… then `selftest judge=forged-summary rejected=1`, `selftest judge=short-report
rejected=1`, `selftest judge=complete-report accepted=1`, then `selftest cases=9 failures=0`".
Measured output prints `selftest cases=9 failures=0` **before** the three judge lines
(`r-suite-selftest.log`). Every line and spelling is present and exact, and the exit semantics
are correct; only the sequence is misdescribed. Per the row's own rule ("if the case set or gate
list changed, append a correction (R6)") this warrants an appended correction at the L1's
discretion; it does not affect field presence, pinned values, or any exit code.

**1.8 Finding F2 (minor, both rows, owner field).** Owner value is `kasegi-shokunin`, while all
eight earlier registry rows (SKILL.md:981, 982, 1041, 1054, 1055, 1064, 1065, 1077) use `kasegi`.
Cosmetic convention deviation; the field is present and unambiguous.

### 2. D4 — wave1-results.json tracking + provenance note

**2.1 File and note on disk, identity verified.**

```
wc -c  .ufo/waves/round-34/wave1-results.json                 → 312874          (note §3: 312874) ✓
sha256sum .ufo/waves/round-34/wave1-results.json
  → 3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4             (note §3: same)   ✓
```

The verifier's abbreviated digest in the spotcheck (`3afa3581afb14aba…`) is a prefix of this
full digest. The note `.ufo/waves/round-34/wave1-results.json.provenance.md` (sha256
`e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98`) exists beside the file and
carries the file's sha256, size, parse check, the D4 narrative, and the frozen counting command.

**2.2 Note content spot-checks.** The quoted closure line exists verbatim:
`sed -n '1488p' /home/vgpnk/Projects/shokunin/.ufo/watchdog.log` →
`2026-10-26T03:19:31-03:00 complete kasegi round=34; hyaku-inline attempt=2` (= 06:19:31Z; note
§2's "3 min 48 s after" offset vs mtime 06:23:19Z). The round-33 counterpart asymmetry holds:
`git ls-files .ufo/waves/round-33/wave1-results.json | wc -l` → `1`.

**2.3 Tracking measured — NOT yet satisfied.**

```
git ls-files .ufo/waves/round-34/wave1-results.json | wc -l   → 0      (frozen C1 counting command wants 1)
git ls-files .ufo/waves/round-34/wave1-results.json.provenance.md | wc -l → 0
git status --porcelain .ufo/waves/round-34/
  → ?? .ufo/waves/round-34/wave1-results.json
  → ?? .ufo/waves/round-34/wave1-results.json.provenance.md
git check-ignore -v <both files> → (no output), exit 1        → not git-ignored
git rev-parse HEAD → da2d3c687f82a9814ee71c91c930cb733050d37c (dispatch commit; no integration commit yet)
```

**2.4 Finding F3 (closure-pending, D4).** The fix's content is complete on disk (file + note,
digest match, not ignored), but the tracked condition is unmet at measurement time because the
L1's integration commit has not happened yet — the same landing/closure-order class D4 itself
records. The frozen counting command prints `1` if and only if the L1's closing commit includes
**both** `.ufo/waves/round-34/wave1-results.json` **and**
`.ufo/waves/round-34/wave1-results.json.provenance.md` (the note is also currently untracked;
C1's kill rule names the results file, but D4's fix text is "commit `wave1-results.json` with a
provenance note" — an untracked note would leave the provenance unverifiable from the committed
tree). If either file is omitted from the closing commit, D4 reopens and the C1 kill rule
("wave1-results.json untracked") fires.

### 3. Verdict

- **D3: CLOSED in the working tree.** Both rows exist (SKILL.md:1097, SKILL.md:1098) under the
  appended section (SKILL.md:1093), all eight fields populated in each, append-only vs
  `617496b` (13 insertions, 0 deletions, single EOF hunk), every pinned digest / line count /
  structural claim verified against the instrument bytes, and all registered invocation forms
  executed live with outputs and exit codes matching the registered verdict maps (including both
  exit-2 UNAVAILABLE arms on both instruments). Rows are uncommitted; they land with the L1's
  integration commit. Two minor prose findings (F1 selftest line order, F2 owner value) — neither
  blocks closure.
- **D4: fix content COMPLETE; tracked condition PENDING the L1 integration commit.** Measured
  `git ls-files` → 0 now (frozen command wants 1); both files untracked and not git-ignored;
  file digest matches the note exactly. Closure completes at the L1's closing commit provided
  both files are included (F3).

### 4. Evidence artifacts and digests

Run logs preserved at `.ufo/waves/round-35/wave1/RevD3D4/` (identical bytes to the scratch
originals):

```
85d80cb2c8c6cbf237bba0941617b7ad9904db6fbaabac0d5e7066b9f3bb9027  killrule-plain.log
eb83937c44aef715cbe84a28f9fbe72425451107afb38f48e6a4a25688a20ec1  killrule-selftest.log
0823a08c544444788672a11009254951ac985fb66702594ad96f0e80555dfa15  r-suite-plain.log
9955ce658978a51bf307af52c595aae50f3cf4d6a4fea33cac5adc3fa2905026  r-suite-selftest.log
```

Other digests measured this session: SKILL.md (worktree)
`0cc9563824328a762b3acf168fe719101a9164cf64e51fcc6cccb8a8a23b5190`;
`.ufo/waves/round-34/wave1-results.json`
`3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4` (312874 B);
`.ufo/waves/round-34/wave1-results.json.provenance.md`
`e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98`;
`corpus/instruments/r-defect-closure.sh`
`809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d`;
`corpus/instruments/kill-rule-check.py`
`c279d952cba54f3f7d502a7a5e056be640146adc5b21a88b1d8dd65bfcdb5d61`;
`corpus/instruments/capture-binding-check.py`
`3d9e5e0ddbaaccf91db255b4a978d49a1d44a2c54cd7cc1fef22c78330da99fa`.

### 5. Scratch and scope

Scratch `/fast/scratch/hyaku/kasegi-r35/RevD3D4/` removed before yielding (logs first copied to
`.ufo/waves/round-35/wave1/RevD3D4/`, digests above). No writes outside the lane repo; no git/jj
mutations (read-only `git show`/`ls-files`/`status`/`diff`/`check-ignore`/`rev-parse` only); no
subagents dispatched; no tool installs.

Report: .ufo/waves/round-35/wave1/RevD3D4.md
