# ExecHarness — round 62 predata

Axes: depth:verifiability; coverage. No production instrument changed. No commit, index, bookmark, deployment, global configuration or tool installation performed.

## Deliverable and usage

Draft: `.ufo/waves/round-62/w1/ExecHarness/c1-probe-run-r62.py`.

From any cwd (absolute paths):

```sh
python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-62/w1/ExecHarness/c1-probe-run-r62.py /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r62/verify/probes --mode baseline
```

For the integrated candidate, change only `--mode baseline` to `--mode candidate`. For a draft candidate, also change the instrument path. Baseline is round-62 base f7dcab84b104ccc03083fa1ad8c38e12830d25c9, instrument sha256 `051083a2dd3b76f96568dd2a18866975b71dd1578992546c671faf21e99418a9`; it is NOT round-61's before instrument.

Separate explicit baseline/candidate tables compare every named probe's `(exit, marker count, required diagnostic)`. A wrong instrument returning 2 cannot masquerade as a refusal without `reason=derive-not-read-only`. Ten probes cover quoted traversal, ./ prefix refusal, normalized instruments2 sibling refusal, inside/normalized-inside counters, quoted separator/plain count controls, and retained plain traversal/symlink refusals. Escape fixture scripts write a marker AND print 35, so an admitted escape has tuple `(0,1)` (unlike r61's nonprinting escape fixture).

No shell is interposed when invoking the instrument. Each literal derive enters a one-entry JSON ledger unchanged; receipts retain derive, exact instrument argv and full combined output. This tests the instrument's behavior, not a proof of all shell semantics. Required tools are Python stdlib and PATH-resolved bash/python3/cat/grep/wc; no GNU-only harness dependencies or find pipeline. Missing tools, fixture errors, collection errors and timeouts fail nonzero. Instrument beneath resolved scratch is refused before deletion, including symlinks resolving there. Scratch must be a disposable seat/subdirectory under the guarded r62 subtree.

## Retained evidence

All paths below are relative to this report's sibling `ExecHarness/` directory. Each run receipt retains the exact invoked command, output and exit status.

| receipt | observed result |
|---|---|
| `probes-baseline.txt` | baseline instrument: 10 probes, failures=0, exit=0 |
| `probes-candidate.txt` | same baseline instrument against candidate wants: 10 probes, failures=1, exit=1; quoted traversal executes instead of refusal |
| `probes-draft-candidate.txt` | sibling ExecArgv draft instrument: 10 probes, failures=0, exit=0; receipt pins its actual measured digest |
| `r61-defects.txt` | historical collector with exit99 instrument returns 0 despite eight execution failures; instrument-under-scratch is deleted and collector still returns 0; exact find-to-wc idiom reports pipeline statuses `1 0` and final exit0 |
| `r62-refusals.txt` | missing instrument exit2; syntactically valid `sys.exit(99)` instrument exit1 via ten mismatches; instrument-under-scratch exit2 with instrument preserved; empty PATH missing dependencies exit2; collection on nonexistent probe raises FileNotFoundError rather than returning zero |

Historical reproduction uses `r61-runner-relocated.sh`, copied from the retained r61 runner with ONLY its scratch guard changed from `kasegi-r61` to `kasegi-r62`. This confines the harmless reproduction to the assigned scratch subtree; it is not a claim that the historical frozen bytes were changed. Fixture instrument99 is exactly `import sys\nsys.exit(99)\n`. Missing-find demonstration uses the original collection idiom and prints bash PIPESTATUS; it does not assert a full-run find failure was induced. New collector failure was exercised directly through `collect_markers(nonexistent-path)`.

The candidate-side red-before run is intentionally nonzero; no exit0-only verdict is used. The draft-candidate pass is predata evidence, not L1's post-integration verification or predicate freeze. L1 should rerun the named candidate command after integration and freeze the runner digest with the instrument.

## Context, scope and limits

Read RULES first, round61 lesson/spotcheck, QUALITY (including R58/R72/R77/R79/R82), and SCORECARD's planned62 section. Base HEAD and instrument bytes matched the supplied base. S095 snapshot digest independently observed as `bed305896d46ef54f162b955585157e215f5082a27789ac71cfb9c045dddcac2`, 5802 bytes; no F43 admission work or source judgment belongs to this seat.

Scratch shared clone was created with `git clone --shared --no-checkout`; its toplevel printed `/fast/scratch/hyaku/kasegi-r62/ExecHarness/repo`. No checkout/index mutation followed. The entire exclusive scratch tree was removed before handoff. No giant fixtures retained. No full tests, formatter, lint or unrelated suites run. Python used: 3.14.8; installs: none. LSP unavailable: no mounted LSP definition/reference/refactor tool; this draft introduces no production symbol refactor.

These are named empirical controls, not sandboxing. Arbitrary allowed counters can write; racing filesystem changes or malicious instrument process behavior are not confined. Diagnostic matching pins current output wording. The runner timeout is 30 seconds per tiny probe, not the instrument's general execution budget. No broad mutation-kill claim is made here: explicit ./ and normalized-sibling tuples provide witnesses; mutation battery ownership remains ExecMutants.

Self-evaluation (not judgment): accuracy4 (retained receipts; integrated candidate unmeasured), completeness4 (all requested harness cases exercised; broader mutation battery separate), clarity4 (separate mode tables; diagnostic wording dependency stated), actionability4 (absolute usage and exact receipts; parent gate remains), conciseness4 (full raw outputs intentionally retained). Overall4.0. Highest-impact remaining integration action: run candidate tuples once on integrated frozen bytes. User agreement is not presumed.

## Post-review correction — exact result binding

HarnessAttack-2 found the initial diagnostic-substring draft admitted wrong-id/recorded output. The runner now requires the exact stdout FIG record (probe id, recorded value, derived value) plus exact one-figure summary for admitted probes, or exact stderr refusal record including probe id for refusals; the other stream must be empty. Prior receipts above describe the initial draft and remain preserved, not silently regenerated.

`ExecHarness/strict-record-binding.txt` retains amended-run commands/full outputs and the complete wrong-record adversary fixture: baseline 10/0 exit0; ExecArgv draft candidate 10/0 exit0; wrong-id/recorded adversary 10/10 failures exit1. This receipt supersedes initial substring-only result-binding evidence. Scratch was recreated only for this bounded amendment demonstration and removed again. No production edits or full-suite runs.

Report: .ufo/waves/round-62/w1/ExecHarness.md
