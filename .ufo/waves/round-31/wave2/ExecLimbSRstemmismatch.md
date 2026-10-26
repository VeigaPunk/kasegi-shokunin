# ExecLimbSRstemmismatch — round 31 wave 2, falsify C1 limb `SR-stem-mismatch`

Seat: ExecLimbSRstemmismatch (executor, leaf). Write scope: lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin` only.
Lane base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze `738a77999a00efbca129cfccb28a481037f6241f`; landed wave-1 integration `eecad59`.
Answering model (recorded, route table decided, no model passed): `opencode-go/deepseek-v4.1-flash`.
Tools installed/upgraded: none. pacman transactions: none. Network fetches: none. git/jj mutations: none (read-only `git log`, `git status`). Lane writes: this receipt only; every attack ran in `mktemp -d` scratch.

## 0. Subject bytes (landed, read-only for this seat)

```
$ sha256sum corpus/instruments/source-recheck.py corpus/instruments/limb-ledger.json \
    corpus/instruments/limb-mutation-check.py \
    corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json \
    corpus/instruments/limb-fixtures/sr/stem-mismatch/SFIX-STEM-capture.txt
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
151c64b193fc89972d0389082f4ed8e352be6160ab4cd8f70f58094ed76d7cf9  corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json
856fc6bf9c9fb95d29aa7f28f413778ebc17744fa5ea088a4c54768082dfa620  corpus/instruments/limb-fixtures/sr/stem-mismatch/SFIX-STEM-capture.txt
$ git log --oneline -1
eecad59 round-31: wave-1 integration (C1 limb ledger+counter, C2 F15/S048, score-gap, erratum, LOG r30), wave-2 spec
$ git status --porcelain corpus/
(none)
```

`fd2e01e8…` for the instrument and `856fc6bf…` for the capture equal the digests wave 1 recorded in `.ufo/waves/round-31/wave1/ExecSRLimbs.md` §2, so the bytes falsified here are the landed bytes.

Ledger row under test (verbatim from `corpus/instruments/limb-ledger.json`, `limbs[9]`):

```json
{"id":"SR-stem-mismatch","instrument":"corpus/instruments/source-recheck.py",
 "find":"    if Path(path).stem != source_id:\n",
 "replace":"    if False:  # SR-stem-mismatch mutant: B1 stem check dropped\n",
 "kill":"python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json --source SFIX-STEM",
 "live_exit":1,"signal":"reason=stem-mismatch", "note":"B1 (QUALITY Q9): …"}
```

The `find` text occurs exactly once in the instrument (site: `source-recheck.py:124`, inside `check_source`, immediately after the `# B1:` comment at line 123).

## 1. Hand re-derivation (independent of the counter's machinery)

Fresh scratch lane, corpus copied by hand:

```
$ S=$(mktemp -d); cp -r corpus "$S/corpus"; I="$S/corpus/instruments/source-recheck.py"
$ sha256sum "$I"                       # pre-mutation, must equal the lane bytes
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  …/source-recheck.py
$ cd "$S" && python3 "$I" --manifest "$S/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json" --source SFIX-STEM; echo "exit=$?"
SFIX-STEM:manifest MISMATCH reason=stem-mismatch
exit=1
```

Live side: exit **1** (== `live_exit` 1), signal `reason=stem-mismatch` **matches** (stderr empty). The pristine verdict line printed is exactly one line, i.e. B1 fires before the pin gate.

Hand mutation (python bytes replace, then compile):

```
find count in instrument : 1
mutated bytes == original: False
mutant sha256            : 6302635bf94d9012746b6190851750a00b80ddd1473a56ba516ba67c3049c01b
py_compile(mutant)       : OK
$ cd "$S" && python3 "$I" --manifest "$S/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json" --source SFIX-STEM; echo "exit=$?"
SFIX-STEM:sha256 OK
SFIX-STEM:Q1 OK occurrences=1
exit=0
rerun identical (exit, stdout, stderr): True
```

Mutant side: exit **0** (≠ 1), signal **absent**. ⇒ hand verdict `killed`. Mutated region as read back from the scratch file:

```
 123     # B1: the capture file stem must equal the record id (QUALITY Q9).
 124     if False:  # SR-stem-mismatch mutant: B1 stem check dropped
 125         emit(out, f"{source_id}:manifest", "MISMATCH", "reason=stem-mismatch")
 126         return 1
```

Counter line, same landed bytes, run in the lane (scratch-only tool):

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
limbs=13 killed=13 survivors=0
controls=3 rejected=3
EXIT=0
```

**Hand result == counter line, field by field** (`live=1/y`, `mutant=0/n`, `verdict=killed`). No defect on the re-derivation axis. `mutant=0/n` also confirms the ledger note's prediction "the B1-dropping mutant prints sha256 OK and exits 0" — measured, not assumed.

## 2. Isolation — the kill is limb-specific, not a crash

| Observation | Pristine | Ledger mutant |
|---|---|---|
| stem-mismatch fixture run | `exit=1` — `SFIX-STEM:manifest MISMATCH reason=stem-mismatch` (1 line) | `exit=0` — `SFIX-STEM:sha256 OK` / `SFIX-STEM:Q1 OK occurrences=1` (2 lines) |
| stderr / traceback | empty | empty |
| sibling fixture `sr/occurrence-not-unique` (stem-correct) | `exit=1` — `SFIX-REPEAT:sha256 OK` / `SFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique` | byte-identical (`sibling identical: True`) |

Differing output line list: the mutant drops exactly one line, `SFIX-STEM:manifest MISMATCH reason=stem-mismatch`, and continues into the instrument's normal downstream reporting (`sha256 OK`, `Q1 OK occurrences=1`). It still parses the same manifest, still pins the bytes and still evaluates the quote — the run is a complete normal recheck, not an aborted or crashed one, and the unaffected sibling fixture proves the mutant did not break unrelated behaviour. The `sha256 OK` + `occurrences=1` lines also independently confirm the fixture's isolating preconditions (correct pin, unique quote) so B1 is the only gate that can fail on it.

Signal-bearing semantics worth recording: the row's `signal` (`reason=stem-mismatch`) is emitted only at `source-recheck.py:125`; a mutant that keeps the exit but renames the reason is caught by signal alone (mutant M6 below, exit 1 / sig n ⇒ killed), and a mutant that keeps the reason but continues is caught by exit alone (M5, exit 0 / sig y ⇒ killed). The row therefore discriminates on both axes, not by exit only.

## 3. Discrimination — six further one-limb mutants of the same limb

Each mutant ran on its own fresh scratch lane; `find` count asserted == 1; `py_compile` done; same kill command as the row.

| # | Mutant (site/shape) | kill exit/sig | killed? | instrument `--selftest` |
|---|---|---|---|---|
| M2 | inversion: `if Path(path).stem == source_id:` (line 124) | 0 / n | **killed** | exit 1, `cases=10 failures=9` |
| M3 | leniency by case folding: `if Path(path).stem.lower() != source_id.lower():` | 1 / y | **survivor** | exit 0, `cases=10 failures=0` |
| M4 | leniency by prefix: `if not Path(path).stem.startswith(source_id):` | 0 / n | **killed** | exit 0, `cases=10 failures=0` |
| M5 | drop only the `return 1` (emit kept) | 0 / y | **killed** (exit axis) | exit 1, `failures=1` |
| M6 | rewrite the reason: `reason=stem-diff` | 1 / n | **killed** (signal axis) | exit 1, `failures=1` |
| M7 | different code site: `source_id` derived from `Path(path).stem` ⇒ self-comparison | 0 / n | **killed** | exit 1, `failures=1` |
| M8 | over-rejection: line 124 collapses to `if True:` (always MISMATCH) | 1 / y | **survivor** | exit 1, `failures=8` |

M3 is **not equivalent** — proved by behaviour, not argument. A case-only-stem-different capture (`id SFIX-CASE`, file `sfix-case.txt`, correct pin `22381531cf4fb225e1008decb1b96faf70b1d780568cbff3655eee7b6e8fa163`, unique quote) on pristine vs M3:

```
pristine exit=1  SFIX-CASE:manifest MISMATCH reason=stem-mismatch
M3       exit=0  SFIX-CASE:sha256 OK | SFIX-CASE:Q1 OK occurrences=1
```

So M3 accepts a capture whose stem matches only under case folding — a real B1 hole (the record id `S048` would accept `s048.txt`) — while the row's kill command and the instrument's own selftest both leave it alive. M8 (unconditional rejection) is likewise killed by the selftest (`failures=8`) but survives the row's kill command, because that command exercises only the reject path: it contains no accepting (stem-correct) run.

Shape summary: the fixture kills *absence* of B1 (M2/M7), *reason tampering* (M6) and *suffix-sharing leniency* (M4 — the fixture stem `SFIX-STEM-capture` still shares the id prefix), but not *case-folding leniency* (M3) and not *over-rejection* (M8). That is a shape-specific, one-sided fixture, not a defect in the limb's stated claim.

## 4. Repeatability / non-flake

`python3 corpus/instruments/limb-mutation-check.py --ledger /tmp/sr-only-ledger.json` (the two SR rows, same `--root` = lane) three times in a row: three identical outputs, `EXIT=0` each, first line every time `LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed`. Hand mutant rerun reproduced byte-identical stdout. No timing, path or cwd sensitivity observed; the row's `{root}` expansion resolves to the scratch lane root (`$S/corpus/...` in §1 is the same shape the counter builds).

## 5. Verdict

**Verdict: `holds`.** The limb is genuinely load-bearing on the landed bytes: the B1 stem check at `source-recheck.py:124` is the sole gate that rejects the isolating fixture, and dropping it flips the row from `exit=1 + reason=stem-mismatch` to `exit=0` with the normal downstream report. Hand re-derivation equals the counter's line exactly (`live=1/y mutant=0/n verdict=killed`), the kill is isolated (one dropped output line, no traceback, sibling fixture byte-identical), and the row is stable across repeats.

**Discrimination: `weak` (recorded limit, not a claim failure).** Two non-equivalent mutants of the same limb survive this row's kill command — case-folding leniency (M3, also invisible to the instrument's own `--selftest`) and unconditional rejection (M8, which the selftest does catch). Nothing was relabelled: the row is correctly `killed`.

Defect report for the L1 (this seat is read-only on instruments, entries, registry, README, SKILL.md, PROVINCE.md — not fixed here):
1. `SR-stem-mismatch` kill command has no accepting-side case, so it cannot kill over-rejection (M8). Route: append a stem-correct run to the row's `kill` (e.g. `… && python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/stem-correct/manifest.json --source SFIX-OK`) — a ledger/contract decision, since the row currently carries one command and one `live_exit`.
2. Neither the fixture nor `source-recheck.py --selftest` (`cases=10`, new case `stem-mismatch` at lines 342-351 compares `S901` against `S900.txt`) kills case-folding leniency. Route: one extra SR fixture whose stem differs only in case (`id SFIX-CASE`, capture `sfix-case.txt`) plus, if the instrument selftest is to stay the generic guard, one case of the same shape. Both are lane-tree edits outside this seat's write scope.
3. No defect found in the counter, ledger schema use, digests, `{inst}`/`{root}` expansion, or the row's signal regex.

Evidence retained in this receipt: all commands with their captured output; scratch lanes are `mktemp`-only and were not cleaned by the seat (paths quoted above are dead after reboot). Nothing in the lane tree was modified except this report file.
