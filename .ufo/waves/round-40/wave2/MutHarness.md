# MutHarness — round-40 FALSIFY wave 2 — frontier-harness mutation probe

Seat: MutHarness (leaf member, no subagent dispatch). Run UTC 2026-10-26T22:19:22Z.
Lane repo: /home/vgpnk/Projects/shokunin/kasegi-shokunin (never written). Fleet root and
/home/vgpnk/Projects/shokuknow untouched. No tool installs, no network fetches.

## Item attacked

Claim C2 counting command and its predicate — frozen at
`.ufo/waves/round-40/claims.json`:

> `python3 corpus/instruments/frontier-recheck-count.py` → `entries=25 pass=25 exit=0` → `entries=26 pass=26 exit=0`
> predicate: "Harness entries=26 pass=26 incl. PASS F23 ids=S060..."

The instrument under attack is `corpus/instruments/frontier-recheck-count.py` (the gate
behind the C2 kill rule "harness not entries=26 pass=26 exit=0") together with its
expected list (`SELFTEST_CASES`, graded by `--selftest`). Probe question: does the
harness actually have teeth — does every listed mutation flip the verdict away from
`entries=26 pass=26 exit=0`? Any mutant that still returns `entries=26 pass=26` is a
defect per the seat kill rule.

## Method

- Mirror of committed bytes: `git -C <lane> archive 3074c7679d6f527ec3930d7748ccce1dbae4a58a`
  (lane HEAD) extracted to scratch `S=/fast/scratch/hyaku/kasegi-r40/MutHarness/base`.
  `git diff --name-only 4766b9d HEAD` = `.ufo/waves/round-40/declared-blocks.txt`,
  `LOG.md`, `SCORECARD.md`, `SHONEN.md` only — corpus bytes are identical to the wave-1
  integration commit 4766b9d, so the mirror is the integrated instrument regardless of
  which of those heads is taken as Y (the `all-gates.txt` receipt named by the claims is
  still untracked at run time; it is not corpus input to this harness).
- Pristine baseline run in the mirror (cwd = mirror root, `TMPDIR`/`HYAKU_SCRATCH` = S),
  then seven single-point mutants, each in its own fresh mirror copy; both detectors run
  per mutant: the plain lane run and `--selftest`. Every replacement was asserted unique
  (count==1) at generation; unified diffs recorded. Mutant copies deleted after each run.
- Lane repo never written; no mutating git/jj command run.

## Pristine baseline — REPRODUCED (green evidence)

- plain: `entries=26 pass=26 exit=0`, with the claimed line present:
  `PASS     F23  knowledge/cyclonedx-analysis-subtree.md              ids=S060           exit=0`
- selftest: `selftest cases=6 failures=0`, exit=0.

Claim C2's harness counting command reproduces exactly against committed bytes.

## Mutants and verdicts

| id | single-point mutation (target) | detector | observed output | verdict |
|---|---|---|---|---|
| M1 | remove pass-path case `bidirectional-holds` from `SELFTEST_CASES` (harness expected list) | `--selftest` | `selftest cases=5 failures=0`; graded `case=bidirectional-holds … verdict=pass` line gone; plain run unchanged 26/26/0 (lane path untouched by construction) | KILLED — graded output changed 6→5 |
| M1b | remove only the `"PASS"` expected substring from that case's want-list | `--selftest` | `selftest cases=6 failures=0` — identical to pristine | **SURVIVED** (coverage finding) |
| M2 | F23 row entry cell → F22's real entry `knowledge/cisa-when-to-issue-vex.md` (README) | plain run | `entries=26 pass=26 exit=1` + `DUPLICATE-ENTRY F22,F23 knowledge/cisa-when-to-issue-vex.md`; F23 line flips to `PASS F23 knowledge/cisa-when-to-issue-vex.md ids=S057 exit=0` | KILLED — exit 0→1, fail-closed duplicate limb; "incl. PASS F23 ids=S060…" visibly breaks |
| M2b | F23 row entry cell → `knowledge/nonexistent-f23.md` (README) | plain run | `entries=26 pass=25 exit=1`; `FAIL     F23  knowledge/nonexistent-f23.md  ids=-  exit=-  problems=missing-entry` | KILLED |
| M3 | pass-path expected count `entries=1 pass=1 exit=0` → `entries=1 pass=0 exit=0` (harness expected list) | `--selftest` | `case=bidirectional-holds … verdict=fail`, `problem=missing='entries=1 pass=0 exit=0'`, `cases=6 failures=1`, exit=1 | KILLED |
| M3b | admitted filter `r[2] == "admitted"` → `"Admitted"` (harness) | plain run | `entries=0 pass=0 exit=1`; selftest also `cases=6 failures=6` | KILLED — proves the 26 is genuinely counted from the committed frontier table |
| M4 | suppress per-entry PASS lines: `print(…)` → `record["status"] != "PASS" and print(…)` (harness) | plain run | `entries=26 pass=26 exit=0` with **no** per-entry lines (output = summary only) | **SURVIVED** on the plain-run detector (coverage finding); `--selftest` does flip (`cases=6 failures=2`: bidirectional-holds + evidence-list-declares-selection fail on missing `'PASS'`/`'ids=…'`) |

## Per the seat kill rule — surviving mutants

Two mutants still return `entries=26 pass=26` and are recorded as coverage findings
(not contract changes, per my role):

- **M1b** — the PASS-line assertion in the graded selftest is single-point: it lives only
  in the `"PASS"` expected substrings of the two pass-path cases. Removing it leaves
  `cases=6 failures=0` untouched, so the selftest verdict does not certify that a PASS
  line is asserted at all.
- **M4** — the lane gate's machine verdict (`entries=N pass=M exit=X`) is computed
  independently of the per-entry PASS lines. The claim's "incl. PASS F23 ids=S060…"
  predicate is therefore transcript-level: enforced by reviewer inspection of the run
  output, not by the gate itself. A harness regression suppressing PASS lines keeps the
  C2 counting command green (the `--selftest` limb of the suite does catch it, but no
  frozen C2 counting command runs `--selftest` for this harness).

No disagreement with the frozen claims: the pristine re-run reproduces the C2 predicate
exactly (`entries=26 pass=26 exit=0` incl. `PASS F23 … ids=S060`).

## Byte-exact mutants

Mutant files lived only in the scratch mirror (tasking: scratch mirror, disposable);
each is reconstructable byte-exactly from the committed blob by applying the recorded
replacement (uniqueness asserted, count==1). sha256 of each mutated file:

| id | target file | mutant sha256 |
|---|---|---|
| M1-pass-case-removed | corpus/instruments/frontier-recheck-count.py | `262d225d7ac59f062df9bb1114bf914dff92b1ffa4d68382f1978c6ac95cd210` |
| M1b-pass-expectation-removed | corpus/instruments/frontier-recheck-count.py | `aa72d3f1c7677cb891d1499276467ac42c5aa5477349533aee001be96e3c1039` |
| M2-f23-cross-entry | corpus/README.md | `68fd5a4cd9cbfb33cf65833a2de9b17c3a2822ee0bf14774cb738e2fa32631aa` |
| M2b-f23-missing-entry | corpus/README.md | (README mutant, same recipe as M2 with new cell `knowledge/nonexistent-f23.md`) |
| M3-selftest-count-flipped | corpus/instruments/frontier-recheck-count.py | (same recipe as M1b with `entries=1 pass=0 exit=0`) |
| M3b-count-basis-broken | corpus/instruments/frontier-recheck-count.py | (single-line filter change recorded above) |
| M4-pass-output-suppressed | corpus/instruments/frontier-recheck-count.py | (single-line print guard recorded above) |

Exact replacements (old → new, each asserted unique):

- M1: delete the two-line tuple
  `    ("bidirectional-holds", ("S001", "S002"), ("S001", "S002"), (), (), 0,\n     ["PASS", "ids=S001,S002", "entries=1 pass=1 exit=0"]),\n`
- M1b: `["PASS", "ids=S001,S002", "entries=1 pass=1 exit=0"]` → `["ids=S001,S002", "entries=1 pass=1 exit=0"]`
- M2: `admitted | knowledge/cyclonedx-analysis-subtree.md | S060` → `admitted | knowledge/cisa-when-to-issue-vex.md | S060`
- M2b: `admitted | knowledge/cyclonedx-analysis-subtree.md | S060` → `admitted | knowledge/nonexistent-f23.md | S060`
- M3: `["PASS", "ids=S001,S002", "entries=1 pass=1 exit=0"]` → `["PASS", "ids=S001,S002", "entries=1 pass=0 exit=0"]`
- M3b: `admitted = [r for r in rows if r[2] == "admitted"]` → `admitted = [r for r in rows if r[2] == "Admitted"]`
- M4: `            print("%-8s %-4s %-52s ids=%-14s exit=%-4s%s" % (` → `            record["status"] != "PASS" and print("%-8s %-4s %-52s ids=%-14s exit=%-4s%s" % (`

## Restoration evidence

- Lane `corpus/instruments/frontier-recheck-count.py` sha256 before and after all runs:
  `1be79af60cb5cb4c1662e4f0e14201a4f372df01513608481297fd564cd48249` (unchanged; equals
  the committed blob at 3074c76).
- Lane `corpus/README.md` sha256 before and after:
  `7e59a0d85b34c193b243f65d1ed3c6ced91c656af165fd40b08d111ab61bcbd1` (unchanged).
- `git status --porcelain` before/after identical (only the four pre-existing untracked
  wave-2 entries: `final-gates/`, the two `kasegi-r40-falsify.ready*` flags, `wave2/`);
  HEAD unchanged `3074c7679d6f527ec3930d7748ccce1dbae4a58a`.
- No mutating git/jj command was run anywhere; the only writes were this receipt and
  scratch under S (removed before yielding; the harness selftest removes its own
  fixture dirs, which were placed under S via `HYAKU_SCRATCH`).
- Disk guard checked before the pass: healthy (`/fast/scratch/hyaku` 24% use, 616.1G free).
