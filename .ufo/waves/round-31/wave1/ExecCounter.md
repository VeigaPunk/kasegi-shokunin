# ExecCounter — C1 limb-mutation counter (round 31, wave 1)

Seat: `ExecCounter` (leaf executor). Owned path: `corpus/instruments/limb-mutation-check.py` only.
Answering model: `devin/deepseek-v4-1-flash` (config route table; no model passed).
No tool installed or upgraded; no pacman transaction; no network fetch; no git/jj mutation by this
seat (read-only `git status` only). Nothing written outside the lane.

## 1. Deliverable identity

```
$ sha256sum corpus/instruments/limb-mutation-check.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
$ wc -lc corpus/instruments/limb-mutation-check.py
  747 30937 corpus/instruments/limb-mutation-check.py
$ python3 -c 'import ast,sys; ...'   # AST import scan
imports: argparse,json,os,py_compile,re,shutil,subprocess,sys,tempfile
stdlib_only: True
```

The file is untracked in the lane working tree (`?? corpus/instruments/limb-mutation-check.py`); the
L1 commits it through the lane helper. Digest `c660a95f…` is the digest `ExecLedgerMerge` ran its
quiescent pair on (their receipt cites only this digest).

## 2. Frozen interface → implementation map

| Contract clause | Implementation | Evidence |
|---|---|---|
| ledger `{"version":1,"limbs":[…],"controls":[…]}` | `load_ledger` validates version/lists, per-row keys, unique ids, lane-relative instrument, integer `live_exit`, compilable `signal`, `expect ∈ {invalid:noop, invalid:nocompile, survivor}` | §4, §6 |
| copy `<root>/corpus` (+ files a kill needs) into a fresh `tempfile.mkdtemp` scratch lane | `build_scratch` copytrees `corpus/` (skips `__pycache__`/`*.pyc`, `symlinks=True`); optional top-level `"copy"` list copies extra lane-relative files/dirs | §5 (fixtures travel), §8 (strace) |
| live baseline first, then mutant | `evaluate_row`: baseline side → gates → mutant side; the mutant side is a **second** fresh scratch copy | §6, §7 |
| `invalid:find-count` (not exactly once) | `text.count(row["find"]) != 1` | `invalid-find-count` (0×) and `invalid-find-twice` (2×) fixtures |
| `invalid:noop` (bytes identical) | `mutated == original` | `invalid-noop` fixture |
| `invalid:nocompile` (`py_compile` fails) | `py_compile.compile(path, cfile=<scratch>/.limb-compile-check.pyc, doraise=True)` | `invalid-nocompile` fixture |
| `killed` when mutant exit ≠ live_exit or signal lost; else `survivor` | `killed = mutant.exit != row.live_exit or not mutant.signal` | `killed` / `survivor` fixtures |
| `LIMB <id> live=<exit>/<sig:y|n> mutant=<exit>/<sig:y|n> verdict=…` | `limb_line` (single spaces, `-` when a run did not happen, `timeout` on the cap) | every transcript block |
| `CONTROL <id> verdict=<v> expected=<e> ok=y|n` | `control_line` | `green`, `controls`, `controls-mismatch` |
| `limbs=<n> killed=<k> survivors=<s>` / `controls=<n> rejected=<r>` | `aggregate` | all runs |
| exit 0 iff n==k, survivors==0, every limb killed, rejected==controls; 1 otherwise; 2 usage/ledger | `aggregate` + `main` | §4, §6 |
| 120 s per command, timeout ⇒ `invalid:timeout`, never killed | `TIMEOUT_SECONDS = 120`, `subprocess.run(..., timeout=…)` → `{"timed_out": True}` | §5 (2 m 0.19 s measured) |
| `bash -c` with `{inst}`/`{root}`, cwd = scratch root | `run_kill` substitutes then `subprocess.run(["bash","-c",expanded], cwd=scratch, env=PYTHONDONTWRITEBYTECODE=1)` | §5, §7 |
| `--root` defaults to the lane root derived from the script path | `lane_root_from_script()` = three dirs above the script | transcript last block (script copied into the fixture lane, no `--root`) |
| never writes the lane tree, deletes scratch, no git write | all writes under the mkdtemp scratch; `shutil.rmtree` in `finally`; no git invocation | §8 |
| stdlib only | import scan above | §1 |

## 3. `--selftest` — 20 internal cases

Internal fixtures run in a temp lane with a synthetic `probe.py`; the CLI uses the frozen 120 s, the
selftest uses a 1 s per-command cap so the timeout path is provable without a 2-minute wait.

```
$ python3 corpus/instruments/limb-mutation-check.py --selftest
selftest killed                 verdict=killed               want=killed               ok
selftest survivor               verdict=survivor             want=survivor             ok
selftest invalid-find-count     verdict=invalid:find-count   want=invalid:find-count   ok
selftest invalid-noop           verdict=invalid:noop         want=invalid:noop         ok
selftest invalid-nocompile      verdict=invalid:nocompile    want=invalid:nocompile    ok
selftest invalid-import         verdict=invalid:import       want=invalid:import       ok
selftest invalid-import-exit    verdict=invalid:import       want=invalid:import       ok
selftest invalid-live-baseline  verdict=invalid:live-baseline want=invalid:live-baseline ok
selftest invalid-timeout        verdict=invalid:timeout      want=invalid:timeout      ok
selftest invalid-nondeterministic verdict=invalid:live-baseline want=invalid:live-baseline ok
selftest invalid-mutant-baseline verdict=invalid:mutant-baseline want=invalid:mutant-baseline ok
selftest validate-vacuous-signal rejected=True  want=True  ok
selftest validate-kill-reads-bytes rejected=True  want=True  ok
selftest validate-kill-chained  rejected=True  want=True  ok
selftest validate-control-misbound rejected=True  want=True  ok
selftest validate-control-bound rejected=False want=False ok
selftest validate-valid-row     rejected=False want=False ok
selftest aggregate-green       ok
selftest aggregate-survivor    ok
selftest control-verdict-rule  ok
selftest cases=20 failures=0
selftest_exit=0
```

`invalid-nondeterministic` is a kill that writes `{root}/marker` on its first run and exits 7 on the
second: the two baseline runs disagree, so the row is `invalid:live-baseline` rather than killed.
`invalid-mutant-baseline` is a kill that counts its own invocations (state in the selftest temp dir):
baseline runs 1–2 agree, mutant runs 3–4 disagree, so the row is `invalid:mutant-baseline`.

## 4. One throwaway ledger per verdict path (CLI, full transcript)

Transcript of record: `.ufo/waves/round-31/wave1/ExecCounter-fixtures/transcript-fast.txt`
(subject digest `c660a95f…`). Fixture lane: `ExecCounter-fixtures/lane/` with a synthetic
`corpus/instruments/probe.py` (`MODE = "pass"` prints `probe ok`, exits 0; `MODE = "fail"` prints
`probe fail`, exits 1). Each block is the command and its exact output.

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger …/killed.json --root …/lane
LIMB FX-killed live=0/y mutant=1/n verdict=killed
limbs=1 killed=1 survivors=0
controls=0 rejected=0
exit=0

$ … --ledger …/survivor.json --root …/lane
LIMB FX-survivor live=0/y mutant=0/y verdict=survivor
limbs=1 killed=0 survivors=1
controls=0 rejected=0
exit=1

$ … --ledger …/invalid-find-count.json --root …/lane
LIMB FX-find-count live=0/y mutant=-/- verdict=invalid:find-count
limbs=1 killed=0 survivors=0
controls=0 rejected=0
exit=1

$ … --ledger …/invalid-find-twice.json --root …/lane
LIMB FX-find-twice live=0/y mutant=-/- verdict=invalid:find-count
limbs=1 killed=0 survivors=0
controls=0 rejected=0
exit=1

$ … --ledger …/invalid-noop.json --root …/lane
LIMB FX-noop live=0/y mutant=-/- verdict=invalid:noop
limbs=1 killed=0 survivors=0
controls=0 rejected=0
exit=1

$ … --ledger …/invalid-nocompile.json --root …/lane
LIMB FX-nocompile live=0/y mutant=-/- verdict=invalid:nocompile
limbs=1 killed=0 survivors=0
controls=0 rejected=0
exit=1

$ … --ledger …/invalid-import.json --root …/lane
LIMB FX-import live=0/y mutant=-/- verdict=invalid:import
limbs=1 killed=0 survivors=0
controls=0 rejected=0
exit=1

$ … --ledger …/invalid-live-baseline.json --root …/lane
LIMB FX-live-baseline live=0/n mutant=-/- verdict=invalid:live-baseline
limbs=1 killed=0 survivors=0
controls=0 rejected=0
exit=1

$ … --ledger …/green.json --root …/lane
LIMB FX-green-killed live=0/y mutant=1/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
limbs=1 killed=1 survivors=0
controls=1 rejected=1
exit=0

$ … --ledger …/controls.json --root …/lane
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=0 killed=0 survivors=0
controls=3 rejected=3
exit=0

$ … --ledger …/controls-mismatch.json --root …/lane
CONTROL CTL-probe-mismatch verdict=survivor expected=invalid:noop ok=n
limbs=0 killed=0 survivors=0
controls=1 rejected=0
exit=1

$ … --ledger …/validation-vacuous-signal.json --root …/lane
limb-mutation-check: limbs[0].signal matches the empty string and cannot discriminate a run
exit=2

$ … --ledger …/validation-kill-reads-bytes.json --root …/lane
limb-mutation-check: limbs[0].kill must run the instrument as a program: expected `python3 [flags] {inst}` at a command boundary
exit=2

$ … --ledger …/validation-kill-chained.json --root …/lane
limb-mutation-check: limbs[0].kill must end at the instrument invocation; '&' follows {inst}
exit=2

$ … --ledger …/validation-control-misbound.json --root …/lane
limb-mutation-check: controls[0].expect must be 'survivor' for control id CTL-equivalent
exit=2

$ (usage) python3 corpus/instruments/limb-mutation-check.py
usage: limb-mutation-check.py [-h] [--ledger LEDGER] [--root ROOT]
                              [--selftest]
limb-mutation-check: --ledger is required
exit=2

$ (missing ledger) python3 corpus/instruments/limb-mutation-check.py --ledger …/absent.json
limb-mutation-check: ledger not found: …/ExecCounter-fixtures/absent.json
exit=2

$ (default --root derived from script path; script copied into the fixture lane, no --root)
LIMB FX-killed live=0/y mutant=1/n verdict=killed
limbs=1 killed=1 survivors=0
controls=0 rejected=0
exit=0
```

Every verdict path in the contract (killed, survivor, `invalid:find-count`, `invalid:noop`,
`invalid:nocompile`, `invalid:live-baseline`, `invalid:timeout`) has its own fixture; `invalid:import`
and `invalid:mutant-baseline` are the two added gates (§7) and have their own fixtures too.

## 5. The frozen 120 s cap, measured at the CLI

`.ufo/waves/round-31/wave1/ExecCounter-fixtures/timeout-run.txt`, subject `c660a95f…`. The kill hangs
only on the mutated bytes (`if grep -q 'MODE = "fail"' {inst}; then sleep 130; fi; python3 {inst}`),
so the baseline is fast and the mutant run hits the cap.

```
$ time python3 corpus/instruments/limb-mutation-check.py --ledger …/invalid-timeout.json --root …/lane
LIMB FX-timeout live=0/y mutant=timeout/n verdict=invalid:timeout
limbs=1 killed=0 survivors=0
controls=0 rejected=0

real	2m0.189s
exit=1
```

## 6. Real-corpus integration over the three owner fragments (13 limbs)

The fragments are the owners' rows, read-only to me:
`.ufo/waves/round-31/wave1/ledger-fragments/ra.json` (`266cb024…`, 9 rows),
`sr.json` (`4f7dc1e3…`, 2 rows), `fr.json` (`ebda80f6…`, 2 rows). I assembled them into a throwaway
ledger `ExecCounter-fixtures/integration-13.json` (13 unique ids) and ran the counter on the lane
root. Subject bytes at run time (owner-declared landed/in-flight states, M30-3 label — this is an
interface integration run, not the claim's landed 13+3 run, which is `ExecLedgerMerge`'s):

```
recheck-audit.py          5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09
source-recheck.py         fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003
frontier-recheck-count.py aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893

$ time python3 corpus/instruments/limb-mutation-check.py --ledger …/integration-13.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
limbs=13 killed=13 survivors=0
controls=0 rejected=0

real	0m13.698s
exit=0
```

`ExecLedgerMerge`'s independent quiescent pair on the same digest `c660a95f…` (their message, not my
run) reported pre==post digest, both exit 0, byte-identical stdout
`sha256 9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838`,
`limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`, 29.3 s, `--selftest cases=20 failures=0`,
and zero added/removed/changed files under `corpus/` across the run. Their receipt cites
`c660a95f…` only.

### 6b. Landed ledger — independent confirmation (ledger owned by `ExecLedgerMerge`)

After the landed ledger appeared (`corpus/instruments/limb-ledger.json` sha256
`c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be`), I ran the counter on it
read-only from the lane root, on the final counter digest `c660a95f…`:

```
$ time python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3

real	0m28.223s
counter_exit=0
```

The ledger artifact is not mine and its receipt is authoritative; this run is the counter-side
confirmation that the landed bytes and the landed ledger produce the claim's two summary lines at
exit 0.

## 7. Hardening beyond the frozen procedure (declared, verdict-neutral on the landed rows)

`CritC1Kill-5` attacked the counter across five digests; each route below was closed by a change that
moves **no** landed verdict (all 13 landed rows re-measured killed after each change). Transcripts:
`ExecCounter-fixtures/critic-replay.txt`, `.ufo/waves/round-31/wave1/CritC1Kill.md` §2.1/§3.

| Route (critic id) | Counter rule now | Landed effect |
|---|---|---|
| one scratch shared by all rows (contamination) | fresh scratch copy per side per row | none |
| kill that counts its own invocations (three-state, A15) | baseline side and mutant side never share a scratch; each side runs the kill twice and must reproduce itself (`invalid:live-baseline` / `invalid:mutant-baseline`) | none |
| vacuous `signal` (`(?s).*`) | ledger error: a signal that matches the empty string cannot discriminate | none |
| kill that only reads the patched bytes (`grep`) | ledger error: the kill must run `python3 [flags] {inst}` at a command boundary | none |
| kill chained after the invocation (A14) | ledger error: nothing but arguments/redirections may follow the last invocation | none |
| mutant that raises at import (A13/residual) | after `py_compile`, the mutant's module level is exec'd in a subprocess; it must exit 0 **and** print the `LIMB-IMPORT-OK` sentinel, else `invalid:import` (a `SystemExit(0)` module level prints no sentinel) | none — all 13 mutants import with the sentinel |
| `CTL-equivalent` used as a no-op patch | control ids `CTL-noop`/`CTL-nocompile`/`CTL-equivalent` are bound to their frozen expects | none |

Critic reproducers replayed on `c660a95f…` (full text in `critic-replay.txt`):

```
degenerate-ledger.json          exit 2  kill must run the instrument as a program
degenerate-ledger-controls.json exit 2  kill must run the instrument as a program
vacuous-signal-ledger.json      exit 2  signal matches the empty string
post-gate-ledger.json           exit 2  limbs[1].kill must end at the instrument invocation; '&' follows {inst}
residual-crash-ledger.json      limbs=13 killed=0 survivors=0 (invalid:import ×13), controls=3 rejected=3, exit 1
honest-survivor-ledger.json     limbs=1 killed=0 survivors=1, controls=3 rejected=3, exit 1
one-degenerate-limb-ledger.json limbs=13 killed=12 survivors=1, exit 1 (survivor = RA-parse with an `== 0  # crit-eq` equivalent patch, live=0/y mutant=0/y)
three-state-kill-ledger.json    limbs=1 killed=0 survivors=1, controls=3 rejected=3, exit 1
```

The critic's closing message on this digest: "No counter-side route remains from this seat". Their
remaining items are claim-level and stay with the L1: (A6) a gutted module that imports cleanly and
prints the summary the ledger's signal keys on; (A7) the closure re-derivation; (A11) `--root` scores
any tree and the frozen stdout carries no root/digest (the stdout grammar is frozen, so a root line
cannot be added without breaking it) plus the exit-only `reach` marker.

## 8. No lane writes, scratch hygiene, no git

`strace -f` over a full 13-limb run (writes/mutations = `O_WRONLY|O_RDWR|O_CREAT|unlink|rename|mkdir`):

```
lane_write_or_mutation_syscalls=0
scratch_write_or_mutation_syscalls=5044
git_execve=0
leftover_scratch_dirs=0
```

Also measured: `find . -newer <marker> -type f` over the lane after a counter run printed nothing
outside `.ufo/waves/round-31/wave1/`; every `limb-mutation-*` scratch dir is removed by
`shutil.rmtree` in `finally` (0 left after each run); no git command is executed by the counter.
Disclosure: one manual `python3 -m py_compile corpus/instruments/limb-mutation-check.py` during
development wrote `corpus/instruments/__pycache__/limb-mutation-check.cpython-314.pyc`; it was removed
with `rm` (gitignored bytecode cache, no source bytes). The counter itself writes no bytecode into the
lane: the compile gate writes its `cfile` inside the scratch root and child processes run with
`PYTHONDONTWRITEBYTECODE=1`.

## 9. Exit-code map (measured)

| Exit | Condition | Evidence |
|---|---|---|
| 0 | every limb `killed`, no survivor/invalid, `rejected==controls` | `killed`, `green`, `controls`, integration-13, ExecLedgerMerge pair |
| 1 | a survivor, any `invalid:*`, or a control mismatch | `survivor`, all invalid fixtures, `controls-mismatch`, critic reproducers |
| 2 | usage (no `--ledger`, `--selftest` with `--ledger`/`--root`), missing ledger, missing lane `corpus/`, missing instrument, malformed ledger | transcript §4, `validation-*` fixtures |

Boundary, measured and disclosed: an **empty** ledger (`limbs: []`, `controls: []`) prints
`limbs=0 killed=0 survivors=0` / `controls=0 rejected=0` and exits 0 — that is the frozen iff applied
literally (`n==k`, `survivors==0`, `all()` vacuously true, `rejected==controls==0`). The transcript
records it (`ExecCounter-fixtures/empty.json`). It is not reachable for the artifact: the landed
ledger has 13 limbs and the L1's kill rule requires 13 `LIMB ` lines, which an empty ledger cannot
print. I did not add a non-empty requirement because the contract states the exit rule as a
biconditional and the landed ledger is the artifact under test.

## 10. Ownership, messages, and what this seat did not do

- Single writer of `corpus/instruments/limb-mutation-check.py`; I did not touch `recheck-audit.py`,
  `source-recheck.py`, `frontier-recheck-count.py`, `limb-fixtures/**`, `limb-ledger.json`,
  `corpus/README.md`, `corpus/SOURCES.md`, `QUALITY.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md`,
  `PROVINCE.md`, the knowledge entry, the snapshots, or the report.
- Messages: `ExecLedgerMerge` (five digests, each supersede with a one-line change note; final
  `c660a95f…`), `ExecSRLimbs` (their two rows killed in the 13-limb integration run), `CritC1Kill-5`
  (each hardening step and the measurements on their reproducers).
- Not mine / left to the L1: the landed `13+3` ledger run (`ExecLedgerMerge`), the ledger's own
  content quality, the A6/A7/A11/`reach` claim-level questions, and the commit.
- Fixtures under `.ufo/waves/round-31/wave1/ExecCounter-fixtures/` are throwaway evidence, not the
  landed ledger.

## 11. Re-run commands for the parent gate

```
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/instruments/limb-mutation-check.py
python3 corpus/instruments/limb-mutation-check.py --selftest; echo "selftest_exit=$?"
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
```

Targets on the landed ledger: `selftest cases=20 failures=0` exit 0; `limbs=13 killed=13 survivors=0`
and `controls=3 rejected=3` with exit 0. A survivor, any `invalid:*`, or a control mismatch makes the
counter exit 1; a malformed ledger exits 2.
