# Round 71 attempt 2 — DraftScorecard seat report

Seat: `DraftScorecard` (leaf; no subagent dispatch). Judged on depth:verifiability and coverage.
Outputs: `.ufo/waves/round-71/w2/ScorecardDraft.md` (38 lines, 9351 bytes, sections: round heading, frozen-claims line, axis table, C1 scope, Capabilities, Saturation, non-author line, `### Round-71 move log`, `### Planned after round 71 (not frozen)` with 4 items), and this report.
Lane state read at start: HEAD `3cc8cd4` (`git -C <lane> rev-parse --short HEAD`). No lane mutation (no add/commit/checkout/reset/push; no jj). Scratch: `/fast/scratch/hyaku/kasegi-r71/DraftScorecard/`, removed before yield. Tool installs: none. Pacman: not used.

## Findings

1. **Base revision in the seat spec does not match the frozen claims.** The spec says base `4e33119e0167cac3fbfa15afb3f2f5b98a43cc60`. `claims.json` `base_revision` is `39cde8a086cf3bfa12aee6682904d194c574a7f0`, and `4e33119` is the measured implementation commit, a descendant of the freeze (`0e260a54…`). The draft uses `39cde8a` as base and `4e33119` as measured implementation. L1 should confirm before integrating.
2. **C1 receipts depend on the lane snapshot through R1 and R8's direct-run exit, not through the gate.** The frozen counter has no `--lane` in its counting command, and its default is the live lane path. Committed `c1-base-r71.txt` and `c1-candidate-trial-r71.txt` reproduce line-for-line only with the lane tree at `39cde8a`, where R8's `capture-binding-check | grep -c records=84` exits 0. At `4e33119` (S106 registry row absent) and at tip `3cc8cd4` (`records=85`), R1 and/or R8 direct exit is 1. The gate verdict (`admitted=1 value_ok=1`) stays green in every case, and `VERIFY failures=0` holds at both lane states I ran. The claim's counting command should name its lane.
3. **Round-71 commits are self-labelled "not a landed round".** `453275f` ("preserve in-flight work at hyaku run-15 wrap-up (L1 died on provider failure; not a landed round)"), `34faab9` and `3cc8cd4` ("late seat output … not a landed round"). The C2 landing commit is `453275f` (knowledge entry, F49 README row, S106 SOURCES row, knowledge-expected line); the S106 capture and manifest are in `4e33119`.
4. **Blanket-refusal forgery control.** `claims.json` lists it as "to be produced at the wave"; no round-71 committed receipt exists. I ran the committed round-70 forgery gate `.ufo/waves/round-70/controls/forgery-blanket-refusal-gate-r70.py` (sha256 `126de75d135f6399e5be19d121790f6cce4a275579fc6070200e214b1fd22502`) through the frozen counter. It fails (`VERIFY … failures=12`, exit 1), matching the lesson's own figure. L1 should decide whether to commit this as a round-71 receipt; I did not write one.
5. **Shell `sort` vs. `/usr/bin/sort`.** The seat shell resolves `sort` to a builtin that prints `sort 0.8.0`. The counter runs `/usr/bin/sort` through `subprocess`, which is GNU coreutils 9.12 (`pacman -Qo /usr/bin/sort`: `coreutils 9.12-2`; query only, no transaction). The counter's `HOST` line reads `sort (GNU coreutils) 9.12` and matches every committed receipt.
6. **Census inherits six W04 warnings** at both the live-root form and the committed-tip `--file` form (both exit 0). The live-root form is run against the live working tree, which has untracked round-71 files; the `--file` form is the committed tip.
7. **Coverage next ground.** `corpus/SOURCES.md` § Leads (tip lines 168–170) lists one unopened lead, the Fuzzilli primary documentation (`github.com/googleprojectzero/fuzzilli`). The round-70 scorecard's suggestion ("OSV schema's own field definitions beyond S080") is not a Leads entry, so the draft does not plan it as a lead.
8. **Not re-measured by this seat:** the one-limb mutant battery (lesson § C1: eight entries with no killing case, `--out` equivalent mutant). I did not run mutants, so V71-1..V71-3 are carried as the lesson states them, tagged [R], not re-verified.
9. **Density** is not measured by this seat; the draft says so ("not targeted; no density credit asserted").

## Measured command outputs (verbatim; this seat's runs)

Commands are run in scratch clones (`clone` = `4e33119`, `c39` = `39cde8a`, `c1bd` = `1bd01ee1`, `ctip` = `3cc8cd4`). Each clone is `git clone --shared` from the lane and `git -C <clone> rev-parse --show-toplevel` equals the clone dir. No commits were made in any clone.

### Revisions, ancestry and gate shas
```
0e260a5 => 0e260a54b0a670cee2915237ac403d37164c749d
4e33119 => 4e33119e0167cac3fbfa15afb3f2f5b98a43cc60
39cde8a => 39cde8a086cf3bfa12aee6682904d194c574a7f0
3cc8cd4 => 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
453275f => 453275f6f21b73a0db902f479527a65fbf7deae5
34faab9 => 34faab907f6c54ab8a5c15fdf2d12b9aca575358
1bd01ee1 => 1bd01ee1e6558925e23d3d27a4bb12b88f502656
0e260a5 ancestor-of 4e33119: yes
39cde8a ancestor-of 0e260a5: yes
4e33119 NOT ancestor of 0e260a5 (merge-base --is-ancestor 4e33119 0e260a5 failed; ancestor check printed the NOT branch)
gate sha256 at 39cde8a      7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5
gate sha256 at 0e260a5      7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5
gate sha256 at 4e33119      182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603
gate sha256 at 3cc8cd4      182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603
gate sha256 at 1bd01ee1     c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde
gate sha256 at c1051749     7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5
claims.json sha256 at 0e260a5 (`.ufo/waves/round-71/claims.json`): c530ec658cff551459a61b1dd3c8052cb089d806497c0e8a9f3ca0243238b3e6
lane status (read-only) at start: untracked .ufo/waves/round-71/{assimilation/attempt2/,build-spec-w2.py,w2-dispatch.err,w2-dispatch.json,w2-spec.json,w2.ready,w2.ready.dispatched,w2/}
```
Note: `4e33119 NOT ancestor of 0e260a5` is the `||` branch of my check; the command printed `NOT ancestor of 0e260a5`.

Sort identity: `type -a sort` in the seat shell → `sort is a shell builtin`; `/usr/bin/sort --version` → `sort (GNU coreutils) 9.12`; `pacman -Qo /usr/bin/sort` → `/usr/bin/sort is owned by coreutils 9.12-2`.

### C1 counter (frozen `c1-probe-run-r71.py`, sha256 `80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b`)

Candidate — `python3 -B <clone>/.ufo/waves/round-71/controls/c1-probe-run-r71.py --gate <4e33119>/corpus/instruments/figure-audit.py --work <scratch>/run-cand-base/work --lane <c39> --mode candidate` (exit 0):
```
HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
GATE sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
MEASURE N1-python-root-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N2-python-root-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N3-python-root-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N4-python-out-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N5-python-out-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N6-python-out-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N7-python-json-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N8-python-no-option-head ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N9-python-selftest ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N10-python-short-o ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N11-python-output-long ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N12-python-unknown-head ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE R1-capture-binding-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R2-kill-rule-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R3-frontier-count-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R4-claim-package-json ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R5-citation-ground-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R6-gate-quote-audit-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R7-routed-defects-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R8-capture-binding-pipeline ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest ok selftest cases=106 failures=0 rc=0 min=104
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
```
Diff against `controls/c1-candidate-trial-r71.txt` (MEASURE/VERIFY/GATE lines): identical.

Candidate at tip lane (`--lane <ctip>`, same gate bytes): R1 `direct_rc=0`, R8 `direct_rc=1 gate_rc=1 admitted=1 value_ok=1`, `VERIFY measurements=25 failures=0 … mode=candidate`, exit 0. Candidate at `4e33119` clone lane: R1 `direct_rc=1`, R8 `direct_rc=1`, `VERIFY … failures=0` exit 0 (first attempt, lane = clone at 4e33119, superseded by the `39cde8a`-lane run above).

Do-nothing — gate `39cde8a` (`7a8d52eb…`), lane `39cde8a`, `--mode donothing` (exit 1):
```
HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
GATE sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
MEASURE N1-python-root-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N2-python-root-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N3-python-root-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N4-python-out-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N5-python-out-equals ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N6-python-out-abbrev ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N7-python-json-space ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N9-python-selftest FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N10-python-short-o ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N11-python-output-long ok rc=2 refused=1 marker_runs=0 wrote=0
MEASURE N12-python-unknown-head FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE R1-capture-binding-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R2-kill-rule-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R3-frontier-count-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R4-claim-package-json FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R5-citation-ground-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R6-gate-quote-audit-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R7-routed-defects-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R8-capture-binding-pipeline FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest FAIL selftest cases=96 failures=0 rc=0 min=104
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=1
VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
```
Diff against `controls/c1-donothing-r71.txt`: identical.

Base — gate `1bd01ee1` (`c09b0fb1…`), lane `39cde8a`, `--mode base` (exit 1). Final lines (full run diffed against `controls/c1-base-r71.txt`: identical):
```
GATE sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
MEASURE N1-python-root-space FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N2-python-root-equals FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N3-python-root-abbrev FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N4-python-out-space FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE N5-python-out-equals FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE N6-python-out-abbrev FAIL rc=1 refused=0 marker_runs=0 wrote=1
MEASURE N7-python-json-space FAIL rc=1 refused=0 marker_runs=1 wrote=1
MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0
MEASURE N9-python-selftest FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N10-python-short-o FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N11-python-output-long FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE N12-python-unknown-head FAIL rc=1 refused=0 marker_runs=0 wrote=0
MEASURE R1-R8 all ok admitted=1 (direct_rc as in committed receipt)
MEASURE selftest FAIL selftest cases=86 failures=0 rc=0 min=104
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=5
VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
```
(The `R1-R8 all ok` line abbreviates eight `MEASURE R… ok` lines, all `admitted=1 value_ok=1`; the diff covers them.)

Base run at the tip lane (`--lane <ctip>`) differs from the committed receipt only at `R8 direct_rc` (`1` vs `0`), the same lane-state effect as finding 2.

Blanket-refusal forgery — gate `.ufo/waves/round-70/controls/forgery-blanket-refusal-gate-r70.py` (`126de75d…`), lane `4e33119` clone, `--mode forgery` (exit 1):
```
GATE sha256=126de75d135f6399e5be19d121790f6cce4a275579fc6070200e214b1fd22502 mode=forgery
MEASURE N1..N12 ok rc=2 refused=1 marker_runs=0 wrote=0 (all twelve)
MEASURE R1-capture-binding-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R2-kill-rule-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R3-frontier-count-root FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R4-claim-package-json FAIL direct_rc=0 gate_rc=2 admitted=0 value_ok=0
MEASURE R5-citation-ground-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R6-gate-quote-audit-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R7-routed-defects-root FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE R8-capture-binding-pipeline FAIL direct_rc=1 gate_rc=2 admitted=0 value_ok=0
MEASURE read-only-controls-admitted FAIL controls=8 failed=8
MEASURE selftest FAIL selftest cases=86 failures=47 rc=1 min=104
MEASURE mutbat FAIL rc=1 mutbat killed=5/5 survivors=0 invalid=0 controls=fail
MEASURE real-ledger FAIL no-audit-line rc=2
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=25 failures=12 gate_sha256=126de75d135f6399e5be19d121790f6cce4a275579fc6070200e214b1fd22502 mode=forgery
```
(The forgery run's `N1..N12` line abbreviates twelve `ok rc=2 refused=1` lines.)

### C2 counters

At `39cde8a` (clone `c39`), commands from `claims.json` `counting_command` run in the clone root:
```
frontier-recheck-count exit=0
FRONTIER-CENSUS rows=48 admitted=48 closed=48 problem-rows=0 registry=105
entries=51 pass=51 exit=0
capture-binding-check exit=0
AUDIT records=84 with_url=84 with_fetched_utc=46 with_archival=38 snapshot_dirs=43 manifest_dirs=43 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=84 bound=84 unbound=0
knowledge-expected lines: 88
knowledge-expected entries: 86
sort -c exit=0
knowledge files: 86
frontier rows (README ^| F[0-9]+ |): 48
registry rows (SOURCES ^|S###|): 105
```
(The frontier `FRONTIER-PASS` and `PASS` lines — 48 FRONTIER-PASS rows, `entries=51 pass=51` — are elided from this excerpt; the count line is the observed value.)

At `3cc8cd4` (clone `ctip`), same commands:
```
frontier-recheck-count exit=0
FRONTIER-CENSUS rows=49 admitted=49 closed=49 problem-rows=0 registry=106
FRONTIER-PASS F49 ids=S106
PASS     F49  knowledge/zdi-disclosure-process-and-vendor-coordination.md ids=S106 exit=0
entries=52 pass=52 exit=0
capture-binding-check exit=0
AUDIT records=85 with_url=85 with_fetched_utc=47 with_archival=38 snapshot_dirs=44 manifest_dirs=44 missing_manifest=0 multi_row_url=7 digest_unpinned=0 orphans=1 orphan=S040-live.txt
records=85 bound=85 unbound=0
knowledge-expected lines: 89
knowledge-expected entries: 87
sort -c exit=0
knowledge files: 87
frontier rows (README ^| F[0-9]+ |): 49
registry rows (SOURCES ^|S###|): 106
```

Census (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, documented read-only in its header):
```
validate --root /home/vgpnk/Projects/shokunin kasegi          exit=0 ; grep -c W04 over output = 6  (live tree)
validate --file <ctip>/corpus/SOURCES.md                       exit=0 ; W04 lines: S028, S029, S072, S076, … (committed tip)
```

S106 capture and manifest (`ctip`):
```
S106 sha=291f36c27b5ccddcd57067ceb5e67182d1a2382e5b7545180070fe3ea6cf59db lines=148
manifest.json quotes: 15
Q01-scope hits=[28,102] words=7   Q02-acquisition hits=[31] words=13   Q03-guarantee hits=[47] words=19
Q04-validation hits=[49] words=5  Q05-window hits=[70] words=15        Q06-shortened hits=[70] words=15
Q07-escalation hits=[70] words=25 Q08-limited hits=[52] words=19       Q09-full hits=[51] words=12
Q10-offer hits=[60] words=19      Q11-nobacklog hits=[62] words=19     Q12-credit hits=[61] words=16
Q13-dossier hits=[69] words=19    Q14-refusal hits=[72] words=18       Q15-nolimit hits=[60] words=13
exact-substring-found: 15 of 15
```
Counting-form check (both forms run by this seat at `39cde8a` and `3cc8cd4`; `[|]` is the claim's `\|` as a character class): README claim-form `grep -cE '^\| F[0-9]+ \|'` = 48 at `39cde8a` and 49 at `3cc8cd4`; README bracket-form `grep -cE '^[|] F[0-9]+ [|]'` = 48 and 49; SOURCES claim-form `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` = 105 and 106; SOURCES bracket-form `grep -cE '^[|][[:space:]]*S[0-9]{3,}[[:space:]]*[|]'` = 105 and 106; `sources-census.sh validate --file corpus/SOURCES.md` at `3cc8cd4` exit 0. The F49 row at `corpus/README.md:1114` names `S106` and `zdi-disclosure-process-and-vendor-coordination.md`. `corpus/SOURCES.md:118` carries the S106 row; § Leads at `:168–170` lists the Fuzzilli lead. The knowledge file is 256 lines (`wc -l`).

## RECEIPTS (number → source)

Committed receipts (read from the lane tree):
- `.ufo/waves/round-71/claims.json` — freeze/base_revision (`39cde8a`), axis_score_before (C1 4, C2 8), predicate text, counting/before/after commands and before/after value strings for C2.
- `.ufo/waves/round-71/controls/pins-r71.txt` — counter sha `80020705…`.
- `.ufo/waves/round-71/controls/c1-donothing-r71.txt` — do-nothing 25/13 exit 1 (reproduced, identical).
- `.ufo/waves/round-71/controls/c1-base-r71.txt` — base 25/14 exit 1 (reproduced at lane `39cde8a`, identical).
- `.ufo/waves/round-71/controls/c1-candidate-trial-r71.txt` — candidate 25/0 exit 0, selftest 106/0, mutbat 5/5, ledger 35/35 (reproduced, identical at lane `39cde8a`).
- `.ufo/waves/round-71/controls/c2-base-counters-r71.txt` — before values rows=48/registry=105/entries=51/records=84/knowledge 88/86/86 files/48 rows/105 registry (reproduced at `39cde8a`).
- `.ufo/waves/round-71/controls/c1-probe-run-r71.py` — counter source (sha `80020705…`, read lines 1–60 and 182–337).
- `.ufo/waves/round-70/controls/forgery-blanket-refusal-gate-r70.py` — forgery gate (sha `126de75d…`).
- `corpus/lessons/round-71.md` — C1 residuals, V71-1..V71-3, M71-1, the eight unkilled per-script entries (§ C1), the lesson's own run figures (cited as [R]).
- `corpus/source-snapshots/round-71/S106.txt`, `manifest.json` — capture sha `291f36c2…`, 148 lines, 15 quotes.
- `corpus/knowledge/zdi-disclosure-process-and-vendor-coordination.md` — 256 lines.
- `corpus/README.md:1114` — F49 row; `corpus/SOURCES.md:118` (S106 row), `:168–170` (Leads).
- `SCORECARD.md` — round-69/70 shape (`## Round 69` at line 2717, `## Round 70` at line 2748, `### Round-70 move log` at 2764, `derive-gate-chain-refusal` row at line 2474, saturation phrasing at 2762 "line 9/10 per owned axis").
- `.ufo/waves/round-71/w1/` — ten seat reports present (ConnectorScope, ExecCapture, ExecRerun, ExecSelftest, ReviewC2, ReviewerC1, ScoutF49, ScribeF49, ScribeLesson, ScribeRegistry); attempt-1 dead seats: CriticC1, CriticC2, MutationC1, SentinelGate.
- Commit subjects from `git log` at the lane: `4e33119`, `0e260a5`, `453275f`, `34faab9`, `3cc8cd4`, `39cde8a`.

Seat-run measurements (outputs above):
- C1 counter: candidate (4e33119 gate, lane 39cde8a; and tip lane), do-nothing (39cde8a gate), base (1bd01ee1 gate), forgery (round-70 gate) → all VERIFY lines quoted above.
- C2 counters at `39cde8a` and `3cc8cd4`; census both forms; S106 manifest quote check (15/15); F49 row and Leads lines (read from `ctip`).
- Revision, ancestry and gate-sha checks (`git rev-parse`, `merge-base --is-ancestor`, `git show <rev>:corpus/instruments/figure-audit.py | sha256sum`).

Numbers in the draft tagged `[R]`: the three C1 VERIFY lines, c2-base-counters, the 15 quotes' anchors where not re-derived, the lesson's per-entry unkilled-mutant facts (not re-run by this seat). Tagged `[M]`: every tip count (49/49/49, 106, 52, 85, 89/87, 87, 49, 106), census exits, sha256 checks, quote substring checks, the tip-lane candidate verdict. `[R+M]`: base counts and both C1 controls, reproduced identically.

## Scratch and cleanup

`/fast/scratch/hyaku/kasegi-r71/DraftScorecard/` holds the clones (`clone`, `c39`, `c1bd`, `ctip`), run work dirs, and output files. Its contents were copied into this report and it is deleted before the seat yields (`rm -rf -- /fast/scratch/hyaku/kasegi-r71/DraftScorecard`).
