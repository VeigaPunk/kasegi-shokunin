# kasegi — round 71 (attempt 2) — DRAFT report body

Drafted by seat DraftReport (leaf, no subagent dispatch). Lane `kasegi-shokunin`, axes depth + coverage.
Base `39cde8a086cf3bfa12aee6682904d194c574a7f0` (round-70 verifier spot-check). Lane tip measured:
`3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`. Frozen claims commit `0e260a54b0a670cee2915237ac403d37164c749d`
(`.ufo/waves/round-71/claims.json`, `.ufo/waves/round-71/controls/pins-r71.txt`).
Attempt-1 measured revision was `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60` (its L1 died on a provider failure).
Every value below is either a line I measured (scratch clones of the committed revisions, removed after drafting)
or a line copied from a committed receipt. Values I could not verify from a committed receipt are `L1 TO FILL`.

Scratch: `/fast/scratch/hyaku/kasegi-r71/DraftReport/` (clones `clone` at `3cc8cd4`, `clone-base` at `39cde8a`,
`work-*`, fleet shims). Deleted at seat end after copying the output lines below.

## Work performed

**Declared claims (2).**

1. **C1 — depth:verifiability** (score 4, lowest non-retired axis; nominal per R58). Per-script python-head census in
   the derive gate `corpus/instruments/figure-audit.py`: refuse the N1–N12 write/exec/ingress shapes, admit the R1–R8
   read-only derives, fail closed on a head absent from the census. Counter
   `.ufo/waves/round-71/controls/c1-probe-run-r71.py`, predicate `VERIFY measurements=25 failures=0` exit 0.
2. **C2 — coverage** (score 8). Frontier F49 admitted on S106 (TrendAI Zero Day Initiative's About page), with a
   knowledge entry, a 15-quote capture manifest and one mined registry row. Frozen counters: `FRONTIER-CENSUS`,
   `entries`, `records`, knowledge-expected, sort, file counts, `sources-census.sh validate`.

**Work items (attempt 2, this seat) and evidence.**

- **Frozen-claim pins re-hashed at the tip.** Each pin line of `pins-r71.txt` hashed from `git show 3cc8cd4:<path>`:
  ```
  PIN ok controls/c1-probe-run-r71.py
  PIN ok controls/c1-base-r71.txt
  PIN ok controls/c1-donothing-r71.txt
  PIN ok controls/c2-base-counters-r71.txt
  PIN ok claims.json
  ```
- **Gate hashes at the measured revisions** (`git show <rev>:corpus/instruments/figure-audit.py | sha256sum`):
  `39cde8a` → `7a8d52eb…` (round-70 gate, the do-nothing bytes); `e7c02bd` → `c09b0fb1…` (round-69 base);
  `4e33119` and `3cc8cd4` → `182f4ef7…` (candidate). `git show 39cde8a:… | grep -cE '^\s+run_case\('` = 96 (base),
  `4e33119:…` = 105, `3cc8cd4:…` = 105 (see "C1 selftest pin" below).
- **C1 candidate counter at the tip** (`python3 -B .../c1-probe-run-r71.py --gate <clone>/corpus/instruments/figure-audit.py
  --work <scratch>/work-candidate --lane <clone> --mode candidate`, clone at `3cc8cd4`; exit 0, wall 53.19 s). Full output
  in §Before → after. Measured rows: all N1–N12 `ok rc=2 refused=1 marker_runs=0 wrote=0`; R1–R8 `ok … admitted=1 value_ok=1`;
  `selftest ok selftest cases=106 failures=0 rc=0 min=104`; `mutbat ok rc=0 mutbat killed=5/5 survivors=0`;
  `real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0`; `no-write-side-effect ok fixture_changed=0 marker_runs=0`.
- **C1 do-nothing control at the tip** (round-70 bytes `7a8d52eb…` through the same counter, `--mode donothing`; exit 1). Reproduces the frozen receipt `controls/c1-donothing-r71.txt`: `VERIFY measurements=25 failures=13`.
  The N8 row is `FAIL rc=1 refused=0 marker_runs=1 wrote=0`; R1–R8 all `FAIL … gate_rc=2 admitted=0 value_ok=0`.
- **C1 base control at the tip** (round-69 base gate `c09b0fb1…`, `--mode base`; exit 1). Reproduces
  `controls/c1-base-r71.txt`: `VERIFY measurements=25 failures=14`; all twelve N rows `FAIL … refused=0`.
- **C1 blanket-refusal forgery at the tip** (`--mode forgery`, gate `.ufo/waves/round-70/controls/forgery-blanket-refusal-gate-r70.py`
  sha `126de75d…`; exit 1): `VERIFY measurements=25 failures=12 gate_sha256=126de75d… mode=forgery`; R1–R8 `FAIL … admitted=0`;
  `read-only-controls-admitted FAIL controls=8 failed=8`; `selftest FAIL selftest cases=86 failures=47`;
  `real-ledger FAIL no-audit-line rc=2`. **Deviation:** the claim's `controls.blanket_refusal_forgery` reads
  "to be produced at the wave"; no round-71 forgery gate is committed. This is the round-70 artifact, measured here.
- **C1 selftest pin.** Runtime `python3 corpus/instruments/figure-audit.py --selftest` at the clone: `selftest cases=106
  failures=0`. `EXPECTED_CASES = 106` (`figure-audit.py:221` at `3cc8cd4`). The `^\s+run_case\(` literal count is 105
  at the tip while the runtime case count is 106, so one case is registered outside that literal; the round-70 method
  (grep count = pin) does not reproduce the round-71 pin.
- **C1 attempt-1 reviewer, reproduced by its seat** (committed): `.ufo/waves/round-71/w1/ReviewerC1.md:3` `C1: VERIFIED`
  at base `4e33119`; its §5 discloses two R1/R8 `direct_rc` differences tied to the S106 row not yet landed.
- **C1 attempt-1 isolation audit** (committed): `.ufo/waves/round-71/w1/ExecSelftest.md:149-155`
  `ISOLATED=9/10`; the missing case `python-out-only-refused` is redundant with the `--out` element of `PY_DENIED_ANY`.
- **C1 attempt-1 residuals and routed defects** (committed): `.ufo/waves/round-71/w1/ScribeLesson.md`, section
  "Findings for the L1": eight per-script denial entries unpinned by selftest (`cases=106 failures=0` while the gate's
  verdict changes; routed V71-1); `frontier-recheck-count.py --json` inert under `PY_HEAD_REFUSED` (V71-3); residual
  probes admitted: positional `claim-package-check.py <exemplar>`, `resolve.py .` (timed out at 90 s), `--results`,
  `--manifest`, `--fleet-root`, `ok.py -- --root`, `capture-source.py -- --out x`; these stay open in the claim scope.
- **C1 frozen-counter defect I measured: R8 literal is stale.** The frozen R8 probe is
  `python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84` (counter line 267). At the tip the
  instrument prints `records=85 bound=85 unbound=0` (exit 0), so `grep -c records=84` matches nothing and exits 1:
  `R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1` (committed trial at `4e33119` recorded
  `direct_rc=0`). The probe still passes because `value_ok` compares the gate's output with the direct output of the
  same literal pipeline; it does not compare to an expected value. The R8 row therefore does not detect a change of
  record count. (The counter's docstring line 37 names `| head -n 1` for R8; the executed command is `| grep -c records=84`.)
- **C2 capture, re-measured.** `git show 3cc8cd4:corpus/source-snapshots/round-71/S106.txt | sha256sum` →
  `291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db`; `wc -l` → `148`. Manifest `sources[0]`:
  `id S106`, `fetched_utc 2026-11-05T01:27:03Z`, `bytes 15004`, `lines 148`, 15 quotes (`quotes` list length 15).
- **C2 source-recheck over the 15 pinned quotes, at the tip** (`python3 corpus/instruments/source-recheck.py --manifest
  corpus/source-snapshots/round-71/manifest.json`; exit 0):
  ```
  S106:sha256 OK
  S106:Q01-scope OK occurrences=2 anchor=28-ok
  S106:Q02-acquisition OK occurrences=1 anchor=31-ok
  S106:Q03-guarantee OK occurrences=1 anchor=47-ok
  S106:Q04-validation OK occurrences=1 anchor=49-ok
  S106:Q05-window OK occurrences=1 anchor=70-ok
  S106:Q06-shortened OK occurrences=1 anchor=70-ok
  S106:Q07-escalation OK occurrences=1 anchor=70-ok
  S106:Q08-limited OK occurrences=1 anchor=52-ok
  S106:Q09-full OK occurrences=1 anchor=51-ok
  S106:Q10-offer OK occurrences=1 anchor=60-ok
  S106:Q11-nobacklog OK occurrences=1 anchor=62-ok
  S106:Q12-credit OK occurrences=1 anchor=61-ok
  S106:Q13-dossier OK occurrences=1 anchor=69-ok
  S106:Q14-refusal OK occurrences=1 anchor=72-ok
  S106:Q15-nolimit OK occurrences=1 anchor=60-ok
  ```
- **C2 gate quote.** `S106.txt` line 70 contains "Vendors are given a standard coordination window of 120 days under
  TrendAI™ ZDI's disclosure policy." `printf '%s' "<quote>" | wc -w` → `15` (≤25 words).
- **C2 attempt-1 reviewer, and its resolution at the tip.** `.ufo/waves/round-71/w1/ReviewC2.md:3` `Verdict: C2: NOT
  VERIFIED` at `4e33119`: the corpus half (registry row S106, knowledge entry, README F49 row, knowledge-expected
  additions) was absent from that commit. The corpus half landed in `453275f`; `34faab9` added the registry-changes bullet. My measurements
  at the tip (below) reproduce every frozen after-value. This is a measurement at the tip by this seat, not a non-author
  verdict on the tip.
- **C2 attempt-1 capture re-fetch** (committed): `.ufo/waves/round-71/w1/ExecCapture.md:49-56` — a live re-fetch at
  `2026-11-05T01:30:56Z` produced a snapshot byte-identical to the committed `S106.txt` (`291f36c2…59db`, 148 lines).
- **C2 counters at the tip and at the base** (clones of `3cc8cd4` and `39cde8a`; exact outputs in §Before → after).
  The frozen counting commands were run unchanged; `knowledge-expected` counted with `wc -l` and `grep -vc '^#'`.
- **C2 census** (`scripts/sources-census.sh validate --root <root> kasegi`): exit 0 at the live lane, at a base-shim root
  and at a tip-shim root; six inherited W04 duplicate-url warnings (S028, S029, S072, S076, S080, S085) at each.
- **Assimilation collision count, re-derived** (see Sources & frontier).
- **Attempt-1 seats that died (no verdict).** The attempt-2 assignment records `CriticC1`, `CriticC2`,
  `MutationC1` and `SentinelGate` as dead; no verdict from them exists in `w1/`. The attack-seat verdicts for this
  attempt are `L1 TO FILL`.
- **Live lane state at measurement time (not mine).** `git -C <lane> status --porcelain -- .ufo/waves/round-71/controls corpus`
  printed ` M corpus/QUALITY.md`, ` M corpus/README.md`, ` M corpus/lessons/round-71.md`, and three untracked
  `.ufo/waves/round-71/controls/` files (`c1-forgery-r71.txt`, `census-attempt2-start.txt`, `census-attempt2-end.txt`).
  `corpus/SOURCES.md` and the frozen `controls/` pins were not among the modified paths. My measurements use committed
  bytes in clones, so the live modifications do not enter the numbers above.

## Landed changes

Commits from `git log --oneline 39cde8a..3cc8cd4` (five commits), with what each contains (`git show --stat`):

| commit | content (measured by `git show --stat`) | LOG.md entry |
|---|---|---|
| `0e260a5` | freeze: `claims.json` (81 lines), `pins-r71.txt`, `controls/c1-probe-run-r71.py` (341 lines), `controls/c1-base-r71.txt`, `controls/c1-donothing-r71.txt`, `controls/c2-base-counters-r71.txt` (6 files, 494 insertions) | L1 TO FILL |
| `4e33119` | C1: `corpus/instruments/figure-audit.py` (167 lines changed; the commit's total is 13 deletions; selftest 106), `controls/c1-candidate-trial-r71.txt`; S106 capture `corpus/source-snapshots/round-71/S106.txt` (148 lines) and `manifest.json` (99 lines) | L1 TO FILL |
| `453275f` | attempt-1 seat outputs (`.ufo/waves/round-71/w1/*`, 10 reports), `build-spec.py`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1.ready.dispatched`, `assimilation/{reg-ids,staged-ids,collisions,quarantine-slice,guard/*}`; corpus: `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` (256 lines), S106 registry row in `corpus/SOURCES.md`, F49 row in `corpus/README.md`, `corpus/instruments/knowledge-expected.txt` (+1), `corpus/QUALITY.md` R110 (+1), `PROVINCE.md` (+2). Commit subject: "preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)" | L1 TO FILL |
| `34faab9` | `corpus/SOURCES.md` (+1: the `Round-71 S106 added …` registry-changes bullet, not a row), `.ufo/waves/round-71/w1/ScribeRegistry.md` (255 lines). Subject: "late seat output … after wrap-up; not a landed round" | L1 TO FILL |
| `3cc8cd4` | `corpus/lessons/round-71.md` (199 lines), `.ufo/waves/round-71/w1/ScribeLesson.md` (135 lines). Subject: "late seat output … after wrap-up; not a landed round" | L1 TO FILL |

Corrections to the seat's commit map: the S106 **row** is in `453275f` (`git log -S'| S106 |' -- corpus/SOURCES.md` returns
only `453275f`), and `34faab9` carries the registry-changes bullet. `QUALITY.md` R110 and the F49 README row are also in
`453275f`.

**No `LOG.md` or `SCORECARD.md` change exists for round 71.** `git log --oneline 39cde8a..3cc8cd4 -- LOG.md SCORECARD.md`
prints nothing, and `grep '^## '` on `LOG.md` at the tip ends at `## Round 70`. Each change's LOG pointer and the per-claim
SCORECARD row (score delta, evidence, counting command, measured commit) are therefore `L1 TO FILL`.

Lesson-level findings (in `corpus/lessons/round-71.md`, not re-measured here): the M71-1 mistake (one global deny
list applied where flags are per-script) cites criteria `R103` and `R110`. `R110` at the tip is the quiescence
criterion ("a round signals done only after the lane's quiescence gate passes"), not the per-script denial class.
Only `R103` names the selftest-limb class. This mapping is `L1 TO FILL` for the L1 to confirm or correct.

## Before → after measurements

Frozen counting command for C1 (`claims.json` `counting_command`), run at the tip with `--lane` set to the clone so the
fixture is built from the measured revision:

```
python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate <clone>/corpus/instruments/figure-audit.py \
  --work <scratch>/work-candidate --lane <clone> --mode candidate
```

**C1 (depth:verifiability).**

| state | gate (sha256) | measured commit | observed VERIFY line | exit | source |
|---|---|---|---|---|---|
| before — do-nothing (round-70 bytes) | `7a8d52eb…` | `39cde8a` bytes at the tip run | `VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb… mode=donothing` | 1 | re-run this seat; equals `controls/c1-donothing-r71.txt` (sha `eb24dd87…`) |
| before — base (round-69 gate) | `c09b0fb1…` | `e7c02bd` bytes at the tip run | `VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1… mode=base` | 1 | re-run; equals `controls/c1-base-r71.txt` (sha `f553ddb4…`) |
| after — candidate | `182f4ef7…` | `3cc8cd4` (clone) | `VERIFY measurements=25 failures=0 gate_sha256=182f4ef7… mode=candidate` | 0 | re-run this seat; committed trial at `4e33119` `c1-candidate-trial-r71.txt` (sha `2231c8c8…`) says the same |
| forgery (r70 artifact) | `126de75d…` | round-70 controls | `VERIFY measurements=25 failures=12 gate_sha256=126de75d… mode=forgery` | 1 | re-run this seat |

Before/after per row, candidate at the tip (this seat's run, `c1-candidate-tip.txt`):
`N1…N12 ok rc=2 refused=1 marker_runs=0 wrote=0` (twelve lines); base at the tip: `N1…N12 FAIL rc=1 refused=0`, with
`marker_runs=1` on N1, N2, N3, N7, N8 and `wrote=1` on N4, N5, N6, N7. Do-nothing at the tip: N8 `FAIL rc=1 refused=0
marker_runs=1 wrote=0`; N9 `FAIL … refused=0`; N12 `FAIL … refused=0`; R1–R8 `FAIL direct_rc=… gate_rc=2 admitted=0 value_ok=0`.

**C2 (coverage).** Frozen counting commands. Before = `39cde8a` (re-run this seat; equals `controls/c2-base-counters-r71.txt`).
After = `3cc8cd4` (re-run this seat).

| counter (frozen command) | before `39cde8a` | after `3cc8cd4` |
|---|---|---|
| `python3 corpus/instruments/frontier-recheck-count.py` → `FRONTIER-CENSUS …` | `rows=48 admitted=48 closed=48 problem-rows=0 registry=105` | `rows=49 admitted=49 closed=49 problem-rows=0 registry=106` |
| same command → `entries=… pass=… exit=…` | `entries=51 pass=51 exit=0` | `entries=52 pass=52 exit=0` |
| `python3 corpus/instruments/capture-binding-check.py` → `records=…` | `records=84 bound=84 unbound=0` (exit 0) | `records=85 bound=85 unbound=0` (exit 0) |
| `wc -l < corpus/instruments/knowledge-expected.txt` | 88 | 89 |
| `grep -vc '^#' corpus/instruments/knowledge-expected.txt` | 86 | 87 |
| `LC_ALL=C sort -c corpus/instruments/knowledge-expected.txt` exit | 0 | 0 |
| `ls corpus/knowledge/*.md \| wc -l` | 86 | 87 |
| `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 48 | 49 |
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` | 105 | 106 |
| `sources-census.sh validate --root <root> kasegi` exit | 0 (six W04) | 0 (six W04) |

Frontier census lines are the exact output: `FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106`
and `entries=52 pass=52 exit=0` (tip); `FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105`
and `entries=51 pass=51 exit=0` (base).

Frozen-value check: every frozen `after_values` item in `claims.json` (rows=49 admitted=49 registry=106; entries=52 pass=52;
records=85 bound=85; knowledge-expected 89/87 sort-clean; 87 knowledge files; frontier rows 49; registry rows 106;
census exit 0 with six inherited W04) reproduced at `3cc8cd4`. The frozen `before_values` (48/48/105; 51/51; 84/84;
88/86; 86 files; 48; 105; census exit 0) reproduced at `39cde8a`.

## Sources & frontier

**`corpus/SOURCES.md` census before → after** (`scripts/sources-census.sh`, lane `kasegi`, `--root` on shims whose
`kasegi-shokunin` link points at the base or tip clone; the fleet `shokunin.conf` copied in):

- `validate` at base (`39cde8a`): exit **0**, six W04 duplicate-url warnings (S028, S029, S072, S076, S080, S085) and
  `kasegi ok …/corpus/SOURCES.md`.
- `validate` at tip (`3cc8cd4`): exit **0**, the same six W04 warnings.
- `validate` against the live lane path `/home/vgpnk/Projects/shokunin/kasegi-shokunin`: exit **0**, six W04 (the SOURCES.md
  file is not among the live modifications).
- `census` (mode census), base → tip diff: `kasegi rows 105 → 106`, `kasegi tier.A 94 → 95`, `kasegi status.mined 86 → 87`;
  `FLEET rows 105 → 106`, `FLEET tier.A 94 → 95`, `FLEET status.mined 86 → 87`; no other census line differs.

**Rows.** Before 105 → after **106**. Added by tier: **A 1** (S106, `docs`, tier A, `mined`, opened 2026-11-05, recheck 180d,
used-by `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md`). Tier C 0 added. Rows touched old → new: **none**
(the `git diff 39cde8a 3cc8cd4 -- corpus/SOURCES.md` hunks are one row insert at line 118 and one appended bullet at line 262).

**Frontier.** F49 admitted on S106 (`corpus/README.md`, row F49 `admitted`, entry `knowledge/zdi-disclosure-process-and-vendor-coordination.md`,
source S106). Frontier rows advanced: **48 → 49**. Knowledge entries 86 → 87 (the entry is 256 lines). Capture records 84 → 85.
`corpus/instruments/knowledge-expected.txt` 88/86 → 89/87 with the entry name added in sort order.

**Assimilation: none.** Collision count (re-derived this seat from the committed slices `453275f:.ufo/waves/round-71/assimilation/{reg-ids,staged-ids}`):
`staged unique 94`, `reg unique 105`, `staged ∩ reg = 75`; `collisions` (committed, 75 lines) equals that intersection exactly
(`diff` empty). Against the tip registry (106 ids) the intersection is 76. Adoption stays closed; the staged package is
not adopted, and the quarantine verdicts are not part of this draft (`L1 TO FILL` if the L1 cites them).

## Trend verdicts

Proposed for the L1 to rule. Verdict vocabulary: improved / harmed / unchanged / unprovable-but-better. No scalar.

- **expansion — improved.** Evidence: frontier 48 → 49 (F49 admitted on S106, measured above); registry 105 → 106 (one tier-A
  mined row, measured); knowledge 86 → 87; capture records 84 → 85; census exit 0 at base, tip and the live path.
- **quality — improved (on the enumerated C1 set only).** Evidence: the frozen counter on the candidate gate `182f4ef7…` at the
  tip: `VERIFY measurements=25 failures=0` exit 0; the do-nothing control `failures=13` exit 1 and the base `failures=14` exit 1
  reproduce; the forgery fails R1–R8 and exits 1. Limits named in the evidence above and in the claim's own scope: positional
  arguments, a counter's own writes on a positional path, options after `--`, nested python, and exec classes not named stay
  open (ScribeLesson residual probes); the R8 probe literal is stale (`records=84` against 85 records) and does not detect a
  record-count change; eight per-script denial entries are unpinned by selftest (routed V71-1).
- **discernment — unchanged.** Evidence: the four attack seats (`CriticC1`, `CriticC2`, `MutationC1`, `SentinelGate`) died in
  attempt 1 and produced no verdict; this attempt's attack-seat outcomes are `L1 TO FILL`. Findings this attempt came from
  reviewer, executor and scribe seats: the attempt-1 reviewer's `NOT VERIFIED` for C2 at `4e33119` (`w1/ReviewC2.md:3`),
  the stale R8 literal and the forgery artifact deviation measured here. No critic or mutation verdict was added.

## Stale-lane

Respawn-per-round driver; no other mission of this lane is open.

## Tooling

No tool was installed or upgraded this round. The six attempt-1 `w1/` seat files that address tooling each state that nothing
was installed or upgraded, and this seat installed nothing (no pacman, uv or npm activity, no fixture outside `/fast/scratch`).

## SHONEN

L1 TO FILL — left for the L1 per the seat spec.

---

GAPS (each `L1 TO FILL` marker, and the open items the L1 must resolve; open items without a marker are not placeholders):

1. **Landed changes → LOG.md pointer** (five rows of the table): `LOG.md` has no round-71 block at the tip
   (`grep '^## ' LOG.md` ends at `## Round 70`; `git log 39cde8a..3cc8cd4 -- LOG.md` empty). The L1 writes the entry; this seat may not touch the fleet-tracked lane file.
2. **SCORECARD.md** per-claim score delta, evidence and measured-commit row: `SCORECARD.md` untouched in `39cde8a..3cc8cd4`.
   Verdicts and deltas are the L1's to assign after the non-author verification.
3. **Attack-seat outcomes for attempt 2** (CriticC1, CriticC2, MutationC1, SentinelGate): no committed report at the time of drafting.
4. **Knowledge-entry depth check** (R108, source-outrun list for `zdi-disclosure-process-and-vendor-coordination.md`): no critic
   verdict exists for this entry; this seat only checked that the 15 pinned quotes are present and located.
5. **Round-71 forgery artifact**: the claim's `blanket_refusal_forgery` says "to be produced at the wave"; none is committed. The
   measured forgery here uses the round-70 artifact. The L1 must decide whether that satisfies the frozen control.
6. **M71-1 criteria mapping** (`R103`, `R110`): the lesson cites R110 for the per-script denial class; R110 at the tip is the
   quiescence criterion. Needs the L1's correction, not this seat's.
7. **Landed status**: the five commit subjects say "not a landed round" for `453275f`, `34faab9`, `3cc8cd4`; whether this round
   lands is the L1's decision.
8. **Quarantine verdicts** (`assimilation/attempt2/quarantine-verdicts.md`, uncommitted, a sibling's file): not cited here.
9. **Trend verdicts**: drafted as proposals; the L1 rules them.
10. **SHONEN**: left for the L1 per the seat spec.

Ordering note for the L1: the frozen C1 counting command omits `--lane`; this draft passes `--lane <clone>` so the
fixture is built from the measured revision. The default is the live lane, whose working tree had uncommitted corpus edits
when measured.
