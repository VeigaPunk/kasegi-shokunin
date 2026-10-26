# RevRSuite — review of `corpus/instruments/r-defect-closure.sh` (kasegi round 34, wave 1)

- Seat: RevRSuite (reviewer, L2 leaf). Reviewed artefact: `corpus/instruments/r-defect-closure.sh`
- Reviewed digest (sha256): `0beafed2c2ead41e66b8248893448954a3ddadd7dade7451579f49a480d460d1` (665 lines, 28512 B) — re-measured unchanged after every battery phase; matches the writer seat ExecRDefectClosureSuite's FINAL ping.
- Byte history observed during review: 608 → 655 → 663 → 665 lines while the writer iterated; all dynamic evidence below was produced at the final 665-line digest only. The syntax audit (function extraction) also ran at this digest.
- Method: independent — base tree extracted by me via `git archive 014ee2d7aa8c3c095ff57ae51097606a9906228c | tar -x -C <scratch>`; tip tree via `rsync -a --exclude .git --exclude .jj` of the working tree; read-only property proven by sorted sha256 manifests of the whole tree before/after each run (`diff -q` empty). Scratch root `/fast/scratch/hyaku/kasegi-r34/RevRSuite`; `TMPDIR` pointed into it; no writes to /tmp observed (TMPDIR listing empty after runs).

## Report

### 1. Static audit — exactly nine checks, parseable, cd-prefixed, read-only

- Function inventory: `grep -cE '^check_r[0-9]+\(\) \{'` → `9`; names `check_r1 … check_r9`, no tenth check; `CHECK_IDS=(R1 R2 R3 R4 R5 R6 R7 R8 R9)` aligned 1:1 with `CHECK_FNS`.
- `bash -n corpus/instruments/r-defect-closure.sh` → exit 0.
- Per-function parse: all 17 defined functions (`block_from build_broken_fixture check_r1..check_r9 copy_into filter_out para_grep run_plain run_selftest usage`) extracted and individually `bash -n` → all rc=0 (extraction script printed `parse: ALL-OK`).
- cd-prefix: the first command of every `check_rN` is
  `cd -- "${RD_ROOT:-$LANE_ROOT}" 2>/dev/null || { DESC="root unreadable"; return 1; }` — verified programmatically for all nine (`cd-prefix: all 9 OK`).
- Read-only: automated scan of the nine check bodies for write constructs (`>`/`>>` redirects, `sed -i`, `tee`, `mktemp`, `mkdir`, `rm`, `mv`, `cp`, python `open(...,"w")`). R1–R4, R6–R8: none (scan hits were `<<<` heredoc strings, DESC text and `->` in regexes — false positives, manually inspected). R5: reads only (`grep -c`). R9: writes only inside its own `mktemp -d "${TMPDIR:-/tmp}/rdc-r9.XXXXXX"` fixture (removed via `rm -rf -- "$tmp"` in the same check); `>/dev/null` redirects only. Empirical proof: full-tree sha256 manifests before/after — `diff -q` empty for both the base-tree run and the tip-copy run (`base-tree-unmodified=YES`, `tip-copy-unmodified=YES`). No git command in the script.

### 2. Dynamic — open on base, closed on tip

Base tree (all nine defects open, `git archive 014ee2d`):

```
$ bash corpus/instruments/r-defect-closure.sh --root <base>
R1 check=SCORECARD.md lane-hash-markers=2 open=1
R2 check=no 'Erratum 2' block in SCORECARD.md open=1
R3 check=no appended 'Note (round 34)' below R20 open=1
R4 check=tightened kill-rule requirement not recorded (QUALITY R24 row or a SCORECARD paragraph: kill rule + one 'selftest case=' line per case) open=1
R5 check=misnamed selftest case 'url-matching-two-rows' still present (count=2) open=1
R6 check=round-26 manifest has no S040-live.txt record and no orphan list open=1
R7 check=round-33 lesson has no appended R7 erratum open=1
R8 check=round-32 manifest carries a non-UTC fetched_utc open=1
R9 check=capture-binding H4-H8 cases missing: per-file-orphan-detected … summary-only-selftest-rejected open=1
closed=0/9 exit=1        base-rc=1
```

Base ground truth spot-checked: `grep -c 'LANE_HASH' SCORECARD.md` → 2; round-32 manifest `fetched_utc` = `2026-10-25T23:14:00-03:00` — the descriptors name real open defects, not harness noise.

Tip working-tree copy and the live lane tree:

```
$ bash corpus/instruments/r-defect-closure.sh --root <tip-copy>
… all nine lines open=0 … closed=9/9 exit=0        tipcopy-rc=0
$ bash corpus/instruments/r-defect-closure.sh      # in-repo plain run
… all nine lines open=0 … closed=9/9 exit=0        live-rc=0
```

Mid-flight observation: at an earlier byte state (R4's QUALITY R24 prose not yet landed by its writer seat) the same suite printed `closed=8/9 exit=1` with R4 open — the suite tracks the actual defect surface, not a canned verdict. R4 closed to `open=0` once the sibling seat's prose landed (descriptor: `tightened kill rule recorded (R24 row: kill rule + one 'selftest case=' line per case) + round-33 lesson R4 3-of-4 erratum`).

Edge paths: unknown arg → `suite UNAVAILABLE reason=unknown-argument arg=--bogus`, rc=2; missing root → `suite UNAVAILABLE reason=root-missing`, rc=2; `--help` rc=0 (prints the file header).

### 3. `--selftest` — nine genuine two-sided cases

```
$ bash corpus/instruments/r-defect-closure.sh --selftest --scratch <scratch>
selftest case=R1 live=pass fixture=rejected verdict=pass
selftest case=R2 live=pass fixture=rejected verdict=pass
selftest case=R3 live=pass fixture=rejected verdict=pass
selftest case=R4 live=pass fixture=rejected verdict=pass
selftest case=R5 live=pass fixture=rejected verdict=pass
selftest case=R6 live=pass fixture=rejected verdict=pass
selftest case=R7 live=pass fixture=rejected verdict=pass
selftest case=R8 live=pass fixture=rejected verdict=pass
selftest case=R9 live=pass fixture=rejected verdict=pass
selftest cases=9 failures=0        selftest-rc=0
```

Fixture construction audited (`build_broken_fixture`, frozen bytes): each case copies only the files that check reads into the scratch tree and reintroduces that check's defect — R1 re-appends a literal `<LANE_HASH>` placeholder; R2 strips `[Ee]rratum 2` lines and the `| R22 |` row; R3 strips the `[Nn]ote \(round 34\)` lines; R4 strips `selftest case=` lines and the lesson erratum/3-of-4 markers; R5 seds a case tuple back to `url-matching-two-rows` (with a fallback pattern and a hard failure if neither sed lands); R6 removes S040-live.txt records/orphan keys and resets `purpose` to "skipped this round"; R7 strips the erratum and miscount lines; R8 rewrites every `fetched_utc` to the `-03:00` offset form; R9 deletes the `nested-snapshot-dir` case name. `verdict=pass` requires live run exit 0 AND fixture run exit non-zero; the summary line prints `cases=9 failures=0` and the exit is the verdict.

Vacuous-check resistance — mutation evidence (mutants installed into a lane-shaped scratch copy so `$LANE_ROOT` fixture sourcing works; both mutants `bash -n` clean):

- Mutant A — `check_r8` replaced by `echo "R8 vacuous-ok"; return 0`: selftest prints `selftest case=R8 live=pass fixture=passed verdict=fail problems=fixture-not-rejected`, `selftest cases=9 failures=1`, rc=1. A vacuous echo check cannot pass the selftest.
- Mutant B — `check_r5` replaced by `return 1`: `selftest case=R5 live=open fixture=rejected verdict=fail problems=live-open(always-open R5)`, `failures=1`, rc=1.
- Control — unmutated copy run from inside the same tree: `cases=9 failures=0`, rc=0.
- Designed quirk (fail-closed, documented here): the selftest sources fixture bytes from `$LANE_ROOT` (the script's own lane), not `$RD_ROOT`; a suite copy outside a lane-shaped tree fails all nine cases with `problems=fixture-build` (`fixture-source-missing`) rather than silently passing. Observed; acceptable.

### 4. Depth probes of the two least-self-evident checks

- R9 rule-A bidirectionality, exact frozen fixture text, live tool (`corpus/instruments/frontier-recheck-count.py`): mirror fixture → `entries=1 pass=1 exit=0`; reverse fixture → `FAIL … problems=selection-not-declared-by-entry`, `entries=1 pass=0 exit=1`. Base tool (round-33 bytes from the base tree) on the same two fixtures: exit 0 and exit 0 — i.e. the fixture discriminates a one-directional rule A from a bidirectional one; check_r9's `[ "$rc_reverse" -eq 1 ]` genuinely tests the new direction, not any failure.
- R5 case-count bound: independent count of case tuples `^\s*\("[a-z0-9-]+",` in the landed `capture-binding-check.py` → 21, equal to the check's `cases=21`; the 21 names enumerate the CASES table (R24 set incl. `per-file-orphan-detected … complete-selftest-report-accepted`); `url-matching-two-rows` absent from the landed file. The `>=11` bound alone would be weak, but the selftest's R5 fixture reintroduces the banned name, so the pair of clauses is non-vacuous.

### 5. Findings

1. (observation, non-blocking) R9's junk-twin limb accepts either `c2-controls/junk-f17.md` or `.ufo/waves/round-34/c2-controls/junk-f17.md`; at review time only the wave-dir copy exists (`PRESENT .ufo/waves/round-34/c2-controls/junk-f17.md`; `corpus/c2-controls/…` absent). The DESC line names which path satisfied it (`junk=.ufo/waves/round-34/c2-controls/junk-f17.md`), so the choice is visible in output. Whether the claim's "committed under c2-controls/" requires the corpus-level path is an L1 adjudication; the suite itself is honest about which it found.
2. (observation, non-blocking) `$LANE_ROOT`-based fixture sourcing in selftest (§3 quirk) is fail-closed but undocumented in the header; a one-line usage note would prevent misreads.
3. (process note) The artefact changed four times during this review before the writer's FINAL pin; every figure above is measured at the pinned digest `0beafed2…`. Any later edit invalidates this receipt.

No defect found that would block the suite's claims: nine checks, parseable, cd-prefixed, read-only over the tree under test, open-on-base / closed-on-tip, selftest two-sided and mutation-hard.

### Environment

No tooling installed or upgraded (pacman untouched): used preinstalled bash, coreutils, awk, sed, grep, git (read-only archive/status only), rsync, python3. Scratch `/fast/scratch/hyaku/kasegi-r34/RevRSuite` deleted after receipt write; no seat tree left on disk.

---

## Addendum — re-verification at the final digest (2026-10-26, post-yield)

The writer seat landed two further R8 corrections after the digest pinned above. This addendum re-runs the full battery and supersedes the digest of record.

- **Digest of record (final): `2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc`** (742 lines, 31887 B, `bash -n` 0). Intermediate digests observed and superseded: `0beafed2…` (§1–§5 above), `357a7e49…` (garbage-Z fixture added; battery re-run green, then superseded within the same session). Byte churn was sole-writer (ExecRDefectClosureSuite), confirmed by the writer after I probed; no second-writer coordination defect.
- Static re-audit at `2a635bf5…`: 18 functions extracted, all `bash -n` rc=0; `CHECK_IDS` = exactly R1–R9; all nine checks cd-prefixed (same first command as §1).
- Dynamic re-run at `2a635bf5…`: base (`git archive 014ee2d`) → `closed=0/9 exit=1` (R8 descriptor now `…not a strict-UTC instant`), tree snapshot diff empty; tip working-tree copy → `closed=9/9 exit=0`, snapshot diff empty; live plain run → `closed=9/9 exit=0`.
- `--selftest` at `2a635bf5…`: nine `selftest case=R# live=pass fixture=rejected control=… verdict=pass` lines — R8 now carries a positive control (`control=pass`), the other eight print `control=absent` — plus `selftest cases=9 failures=0`, exit 0. The case-line shape gained the `control=` field; the frozen claim's `cases=9 failures=0` is unchanged and holds.
- R8 boundary probes (suite run on manifest variants in a scratch copy): `2026-10-25T23:14:00+00:00` → open=0; `2026-10-25T23:14:16.500Z` → open=0; `2026-10-25T23:14:00-03:00` → open=1; `2026-10-25Tgarbage-not-a-timeZ` → open=1. Independent probe of the frozen regex floor alone: it accepts the garbage-Z value (`regex-floor-accepts-garbage: True`) while `datetime.fromisoformat` rejects it (`ValueError`) — the check adds real discrimination beyond the frozen predicate, and its accept set now matches capture-binding rule C (Z, +00:00, fractional seconds).
- Vacuous-check resistance re-proven at `2a635bf5…`: mutant `check_r8` = echo + `return 0` → `selftest case=R8 live=pass fixture=passed control=pass verdict=fail problems=fixture-not-rejected`, `cases=9 failures=1`, rc=1.
- R9 probe re-run at final bytes with the exact frozen fixture texts: live tool mirror rc=0, reverse rc=1 with `problems=selection-not-declared-by-entry` only; base (round-33) tool rc=0 on both — the bidirectionality discrimination holds at the final digest. R5 recount: 21 case tuples, `url-matching-two-rows` count 0.
- Findings §5 items 1–3 stand unchanged at the final digest (junk-twin dual path still resolves to the wave-dir copy: `junk=.ufo/waves/round-34/c2-controls/junk-f17.md`; `$LANE_ROOT` fixture-sourcing quirk unchanged; churn note now closed — sole writer confirmed).
- Scratch `/fast/scratch/hyaku/kasegi-r34/RevRSuite` deleted again after this addendum; no seat tree on disk.

**Final verdict: PASS** — all mandated properties verified at digest `2a635bf575c38e04b028dd26ecbeff73c3b909add892ab727c2ab6b1c821dcfc`.

---

## Addendum 2 — re-verification at the self-report-judge digest (final, 2026-10-26)

The writer landed one more substantive hardening after Addendum 1: `CritC1Kill-2`'s forged-summary mutant (replace `run_selftest()` with `printf 'selftest cases=9 failures=0'; return 0`) used to print the claim's strings at exit 0 with no checks. The suite now judges its own report in both modes.

- **Digest of record (final): `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d`** (832 lines, 35971 B, `bash -n` 0). Supersedes `2a635bf5…` (Addendum 1) and `0beafed2…` (§1–§5). Churn remained sole-writer throughout.
- New functions: `report_ok` (selftest-mode report judge: exactly nine case lines of the full shape `selftest case=R[1-9] live=pass fixture=rejected control=(pass|absent) verdict=pass`, ids exactly R1–R9 distinct, summary exactly `selftest cases=9 failures=0`), `plain_report_ok` (plain-mode: nine `R# check=… open=[01]` lines, ids R1–R9, summary consistent with the counted open=0 lines), `judge_selftest_report` (proves the judge on two forged reports — bare summary and an 8-case short report — before trusting the real one), `build_control_fixture` (R8 positive control). Call sites: top-level driver wraps both modes (`RD_REPORT=$(run_selftest|run_plain)` → judge → exit), so a forged driver cannot print an unjudged summary.
- Static re-audit at `809aaf90…`: 21 functions, all `bash -n` rc=0 individually and whole-file; `CHECK_IDS` exactly R1–R9; all nine checks cd-prefixed.
- Dynamic re-run at `809aaf90…`: base (`git archive 014ee2d`) → `closed=0/9 exit=1`, tree snapshot diff empty; tip working-tree copy → `closed=9/9 exit=0`, snapshot diff empty; live plain run → `closed=9/9 exit=0`.
- `--selftest` at `809aaf90…`: nine case lines (R8 `control=pass`, others `control=absent`) + `selftest cases=9 failures=0` + `selftest judge=forged-summary rejected=1` + `selftest judge=short-report rejected=1` + `selftest judge=complete-report accepted=1`, exit 0. The frozen counting command `--selftest → cases=9 failures=0` is still satisfied verbatim; `grep -c '^selftest case='` = 9 (the three `judge=` lines are not cases).
- Independent judge attacks (my mutants, installed in the lane-shaped scratch copy): forged-summary `run_selftest` → exit 1 with `selftest judge=forged-summary rejected=1`, `judge=short-report rejected=1`, `selftest problem=self-report cases=0 expected=9`; forged-summary `run_plain` → exit 1 with `suite problem=self-report plain-lines=0 expected=9`. Vacuous `check_r8` (echo + return 0) still caught: `fixture-not-rejected`, `cases=9 failures=1`, rc=1.
- Disclosed bound verified accurate: a fabricated *complete* nine-case report (perfect shape, no checks run) passes the judge (my mutant `run_selftest` printing a hand-built report → exit 0). This matches the writer's stated limitation — the self-report judge binds shape, not provenance; the base-tree run (`closed=0/9` on `git archive 014ee2d`, re-measured here) and external readers remain the provenance counter.
- R8 boundary probes re-run at `809aaf90…`: `+00:00` open=0, fractional `.500Z` open=0, `-03:00` open=1, garbage-Z open=1 (accept set = capture-binding rule C). R9 probe re-run: live tool mirror rc=0 / reverse rc=1 (`problems=selection-not-declared-by-entry` only), base round-33 tool 0/0 — bidirectionality discrimination holds. R5 recount: 21 tuples.
- Scratch `/fast/scratch/hyaku/kasegi-r34/RevRSuite` deleted after this addendum; no seat tree on disk.

**Final verdict: PASS** — all mandated properties verified at digest `809aaf9078a2c788c2aec29afd23db251f46c4c0c7e0be5caa7a381ac34d567d`; the forged-summary hole that CritC1Kill-2 found is closed and independently re-attacked here.
