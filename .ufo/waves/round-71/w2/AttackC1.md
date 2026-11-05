# AttackC1 — round 71, attempt 2: attack seat on frozen claim C1

Seat: AttackC1 (leaf, no subagents). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
at tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`. The lane's working tree carries other
seats' in-flight edits (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`,
`corpus/README.md`, `corpus/SOURCES.md`, the ZDI entry, `corpus/lessons/round-71.md`,
`corpus/source-snapshots/round-71/manifest.json`), so every measurement below uses a
`--shared` clone of the committed tip, whose tree is clean
(`git -C $S/lane status --porcelain | wc -l` → `0`).
Scratch `/fast/scratch/hyaku/kasegi-r71/AttackC1` (created, deleted before yield; every
receipt below was produced there and is copied in verbatim). No tool installed or upgraded;
host stack is the frozen scope: `sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8`.
No pacman transaction attempted. No `git add/commit/checkout/reset/push` in the lane; the
clone below was made with `git clone --shared` and never checked out to another rev.

## Verdict

**C1: NOT VERIFIED — as written.** The numeric predicate reproduces exactly
(`VERIFY measurements=25 failures=0`, exit 0), but the sentence's positive clause
"admitting every read-only derive in the enumerated set R1-R8 ... **re-deriving each one's
own value**" is false for **four of the eight** R rows. Only R1-R4 re-derive and compare a
value; R5, R6, R7, R8 pass the counter on a stale-exit branch in which the gate stamps
`derived=UNAVAILABLE` and compares nothing. The attempt-2 peer VerifyC1 (`w2/VerifyC1.md` §4)
found this for R8 and asserted "the other 24 measurements ... retain their discriminating
form"; that assertion is falsified here: R5-R7 are the same vacuity, structurally at every
revision (§2.2). The sentence is repairable without touching the gate (§5) — the defect is
in the claim text and the counter's row design, not in the gate's behaviour on the twelve
negative rows.

Second, independent of the vacuity: "a python head not in the census is refused (fail
closed)" survives at the *parse* level (measured: unknown basename, symlinked basename,
`-m`, `-c`, leading env assignment all refused) but is **name-only**: a file that merely
carries a censused basename is admitted and executed against any `--root` (§3.1), and three
admitted census heads reach exec/write through un-denied options/positionals (§3.2-§3.4).
The claim's own `scope` field declares the positional/`--`/nested-python classes open, so
these are declared lessons, not sentence falsifiers — the name-only census is the one that
is not declared.

## 1. Pins and the frozen predicate (reproduced, not re-derived from a report)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD
3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
$ sha256sum corpus/instruments/figure-audit.py
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603
$ sha256sum .ufo/waves/round-71/controls/c1-probe-run-r71.py
80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b
```
Both equal the assignment's frozen shas and `controls/pins-r71.txt` line 1. Shared clone:

```
$ git clone --shared -q <lane> $S/lane && git -C $S/lane rev-parse HEAD
3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
$ git -C $S/lane status --porcelain | wc -l
0
```

Counter on the tip gate, `--lane $S/lane` (byte-identical clone of the live lane; the claim's
`counting_command` omits `--lane` and therefore reads the live lane, same bytes):

```
$ cd $S/lane && python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py \
    --gate corpus/instruments/figure-audit.py --work $S/FINAL --lane $S/lane --mode candidate
HOST sort (GNU coreutils) 9.12; git version 2.56.0; Python 3.14.8
GATE sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
MEASURE N1-python-root-space ok rc=2 refused=1 marker_runs=0 wrote=0
... (N2..N12 identical shape, all ok rc=2 refused=1)
MEASURE R1-capture-binding-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R2-kill-rule-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R3-frontier-count-root ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R4-claim-package-json ok direct_rc=0 gate_rc=0 admitted=1 value_ok=1
MEASURE R5-citation-ground-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R6-gate-quote-audit-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R7-routed-defects-root ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1
MEASURE read-only-controls-admitted ok controls=8 failed=0
MEASURE selftest ok selftest cases=106 failures=0 rc=0 min=104
MEASURE mutbat ok rc=0 mutbat killed=5/5 survivors=0 invalid=0 controls=pass
MEASURE real-ledger ok FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0 rc=0
MEASURE no-write-side-effect ok fixture_changed=0 marker_runs=0
VERIFY measurements=25 failures=0 gate_sha256=182f4...4603 mode=candidate
EXIT=0
```
The four positive rows whose `direct_rc=1` (R5-R8) are the attack surface. I did **not** re-run the
do-nothing and r69-base controls (they are VerifyC1's `w2` receipt at the same tip, and my
seat is the sentence, not the predicate); an unrun check has not passed here.

## 2. The falsification: four R rows compare no value

### 2.1 What the gate actually stamps for R5-R8

Each row measured alone through `figure-audit.py --ledger <one-figure JSON> --root $S/lane`
(ledger `recorded=want`, `want` = the direct arm's stripped stdout, exactly the frozen
counter's `probe()` shape):

```
$ python3 corpus/instruments/citation-ground-check.py --root .     # R5 direct
DIRECT rc=1 out='unresolved-class=1\nclass-lane-bare=1\n... verdict=failed'
GATE rc=1
  FIG R5 recorded=<multi-line> ... verdict=failed derived=UNAVAILABLE reason=derive-exit-1 stale
  FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1

$ python3 corpus/instruments/gate-quote-audit.py --root .          # R6 direct
DIRECT rc=1 ... 'GATE-QUOTE-AUDIT annotated=10 ok=8 erratum-on-record=2 failures=2'
GATE rc=1
  ... failures=2 derived=UNAVAILABLE reason=derive-exit-1 stale
  FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1

$ python3 corpus/instruments/r44-routed-defects.py --root .        # R7 direct
DIRECT rc=1 ... 'routed-defects total=8 fixed=5 unresolved=3 exit=1'
GATE rc=1
  ... routed-defects total=8 fixed=5 unresolved=3 exit=1 derived=UNAVAILABLE reason=derive-exit-1 stale
  FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1

$ python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84   # R8 direct
DIRECT rc=1 out='0' err=''
GATE rc=1
  FIG R8 recorded=0 derived=UNAVAILABLE reason=derive-exit-1 stale
  FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1
```

`derived=UNAVAILABLE` is not a value: `run_derive` returns at
`corpus/instruments/figure-audit.py:337` (`return None, out, "derive-exit-%d" % status`) as
soon as the final pipeline stage exits nonzero, which is **before** the only value
comparison at `figure-audit.py:587` (`if derived == str(ent["want"])`). Nothing in the
`want` is consulted for these rows.

The counter accepts them on exit status alone —
`c1-probe-run-r71.py:275-282`:

```python
        admitted = not refused(rc, err)
        if direct_rc == 0:
            value_ok = rc == 0 and ("FIG %s " % name.split("-")[0].lower()) in out and " ok" in out
        else:
            value_ok = rc == 1 and ("FIG %s " % name.split("-")[0].lower()) in out
```

For `direct_rc != 0` (line 279) the row passes for **any** gate that exits 1 and prints a
`FIG r8 ` line — including the `derived=UNAVAILABLE` stamp above, and including a gate whose
re-derivation produced nothing. That is the definition of vacuous on both sides: the
"recorded" side is never compared, and the "derived" side is literally absent.

R1-R4 are not in this class: `direct_rc=0`, and their records read
`FIG R1 ... derived=<...> ok` / `FIG R3 recorded=frontier rows=49 admitted=49
derived=frontier rows=49 admitted=49 ok` — a nonempty, exact string comparison.

### 2.2 R5-R7 are structurally vacuous at every revision; R8 only at the tip

The three counters exit 1 for tree-content reasons, at the frozen base and at the tip alike,
so the gate's `derive-exit-1` short-circuit fires at every revision:

```
$ git -C $S/lane archive 39cde8a corpus | tar -x -C $S/base39
$ cd $S/base39 && for c in citation-ground-check gate-quote-audit r44-routed-defects; do ...
citation-ground-check.py --root . rc=1 out_first=unresolved-class=2
gate-quote-audit.py --root . rc=1 out_first=corpus/lessons/round-48.md:18 claimed=14 measured=14 OK quote=marks ar
r44-routed-defects.py --root . rc=1 out_first=R44-D1 status=unresolved detail=...
# identical rc=1 / same first lines at 4e33119 ($S/base4e)
```

R8 is the one row whose *semantics changed inside this round*, because the counter's lane is
not pinned (`--lane` defaults to the live lane, and C2 landed a record):

```
$ cd $S/base39 && python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84
2                      # grep_rc=0  (AUDIT records=84 ... / records=84 bound=84 unbound=0)
$ cd $S/base4e && ... | grep -c records=84
0                      # grep_rc=1
$ cd $S/lane   && ... | grep -c records=84
0                      # grep_rc=1 ; tip prints AUDIT records=85 ... / records=85 bound=85 unbound=0
```

So at `39cde8a` R8 took the counter's `direct_rc == 0` branch and genuinely compared `2`;
from `4e33119` onward it takes the stale branch and compares nothing. The frozen receipt
does not pin the tree, so the *meaning* of the same row differs between the round's base and
tip with no counter change. A positive control that silently degrades to an exit-status
check when the lane's record count changes is not a control.

### 2.3 Two more frozen-instrument mismatches found while reading the row set

- `c1-probe-run-r71.py:37` documents R8 as `... | head -n 1 (pipeline, admitted)`; the row
  the counter actually runs is `:266-267 ... | grep -c records=84`. The docstring is stale
  against its own code.
- `claims.json` `probe_set.positives[3]` (R4) is
  `claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar --json`, and
  that matches the counter's **code** (`:260-262`). But the counter's own **docstring**
  (`:33`) enumerates the same row as
  `claim-package-check.py corpus/knowledge/cve-json-record-format.md --json`. So the frozen
  counter's prose enumerates a different R4 and a different R8 from the rows it runs; the
  claim sentence "the enumerated set R1-R8" therefore names rows that disagree across the
  two frozen documents and their own code.
- The docstring is explicit that R5-R7 are admission-only: `:34-36`
  `R5/R6/R7 ... --root .   (counter exits 1 -> stale, admitted)`. That is the counter author
  declaring the rows do not bind a value, while `claims.json`'s `declared` sentence says the
  counter re-derives "each one's own value". The two frozen texts contradict each other on
  exactly the four rows measured vacuous above.

## 3. Over-refusal and reachability table (measured; gate = `figure-audit.py` at `182f4ef7`)

Method: `DIRECT` = `/bin/sh -c '<derive>'` in the root with `TMPDIR` in scratch; gate = the
same derive as a one-figure ledger. "verdict" = what the gate's `--ledger` path returned
(`reason=derive-not-read-only` + rc 2 = refused; a `FIG .../FIGURE-AUDIT` line = admitted).
"load-bearing" = the refusal prevents an effect that the direct arm demonstrably has.

| # | derive (root) | direct observed | gate verdict | judgement |
|---|---|---|---|---|
| 1 | `frontier-recheck-count.py --root .` (probe fixture) | rc=0, prints `FRONTIER-CENSUS rows=1 ... PASS F01`; appended 1 line to the fixture's exec marker | refused rc=2 | **load-bearing** — the head runs the entry's `recheck:` line through `bash -c`; marker went 0→1 |
| 2 | `score-gap.py --root .` | rc=0, `score-gap — ... (read-only; NOT a claim ...)` | admitted, rc=0 `ok` | not refused — no over-refusal |
| 3 | `shonen-form.py --root .` | rc=0, `shonen-form canonical=1 finding=SF-CLEAN exit=0` | admitted, `... derived=... ok` | not refused — no over-refusal |
| 4 | `limb-mutation-check.py --root .` | not run (copies the root and executes mutants) | refused rc=2 | load-bearing, but `--ledger` is the real hole (#17) |
| 5 | `citation-ground-check.py --json` (bare) | rc=2, `error: argument --json: expected one argument` | refused rc=2 | **inert** — that spelling cannot write |
| 6 | `citation-ground-check.py --json $S/out/cite.json` | rc=0, file **written** | refused rc=2 | **load-bearing** |
| 7 | `gate-quote-audit.py --json` (bare) | rc=2, `error: argument --json: expected one argument` | refused rc=2 | **inert** |
| 8 | `gate-quote-audit.py --json $S/out/gq.json` | rc=1, file **written** | refused rc=2 | **load-bearing** |
| 9 | `mirror-containment-check.py --json $S/out/mirror.json` | rc=0, file **written** | refused rc=2 | **load-bearing** |
| 10 | `kill-rule-check.py --json $S/out/kr.json` | rc=0, file **written** | refused rc=2 | **load-bearing** |
| 11 | `resolve.py .` | rc=0; **wrote** `citation-survival.tsv` + `.md` | **admitted, rc=0 ok** | under-refusal (declared carve-out: positional write) |
| 12 | `claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar --json` | rc=0, JSON to stdout (store_true) | admitted, `ok` | correct admission |
| 13 | `capture-source.py --id x --url file://... --kind text` | rc=2, `--id, --url and --out are required` | refused rc=2 | zero-cost refusal: the script cannot capture without `--out` |
| 14 | `recheck-audit.py --root .` | rc=1, per-entry table with an `executes` column | refused rc=2 | **load-bearing** — `recheck-audit.py:103` runs `bash -c <cmd>` |
| 15 | `kill-rule-check.py --scratch $S/kscratch` | rc=0; created `$S/kscratch` (cleaned after) | **admitted, rc=0 ok** | minor write class (mkdir outside root) |
| 16 | `figure-audit-mutbat.py --instrument $S/evilinst.py` | rc=1; evil file **executed** (`mutbat.exec` written) | **admitted** (gate rc=1 is the derive's own exit) | **exec class reachable** |
| 17 | `limb-mutation-check.py --ledger $S/evil-ledger2.json` | rc=1; ledger's `kill` prefix ran (`limb2.exec` = `limb-ledger-exec`) | **admitted** | **exec+write class reachable** |
| 18 | `capture-source.py -- --out $S/out/after.txt --id x --url file://... --kind text` | rc=2, `error: unrecognized arguments` | admitted (stale `derive-exit-2`, no refusal) | **inert** — argparse end-of-options |
| 19 | `capture-source.py --out $S/out/before.txt -- id x` | rc=2 | refused rc=2 | correct, no file written |
| 20 | `python3 -m corpus.instruments.score-gap --root .` | rc=0 (works) | refused rc=2 | over-refusal, but load-bearing as a class (any module on `sys.path`) |
| 21 | `python3 -c 'import pathlib; ...write_text(...)'` | rc=0, `dashc.exec` **written** | refused rc=2 | **load-bearing**, effective |
| 22 | `TMPDIR=$S python3 corpus/instruments/score-gap.py --root .` | rc=0 | refused rc=2 | over-refusal of a shell form; not a ledger-reachable bypass (env is the gate caller's) |
| 23 | head reached through a symlink (`$S/symroot/corpus/instruments/score-gap.py -> $S/evil.py`) | rc=0, evil file **executed** | refused rc=2 (`realpath` check, `figure-audit.py:505`) | **load-bearing** |
| 24 | same basename, plain attacker file in `$S/evilroot/corpus/instruments/score-gap.py` | rc=0, `evil ran`, `evil.exec` written | **admitted rc=0** `FIG ... derived=evil ran ok` | **census is name-only** (§3.1) |
| 25 | `capture-source.py -o <path> ...` (N10's shape) | rc=2, `unrecognized arguments: -o ...`, no file | refused rc=2 | **N10's write hazard is unreachable**: `grep -n 'add_argument("-o"' corpus/instruments/*.py` → no instrument takes `-o` |
| 26 | `test_resolve.py` | rc=0 (unittest output on stderr; stdout empty) | admitted, `derived=UNAVAILABLE reason=derive-empty` | admitted test runner; derives no value |

Sum of #1-#26: of the plausible read-only derives, the only genuinely over-refused ones are
`-m <module>` (#20) and a leading `VAR=value` assignment (#22); both are shell/module classes
the gate cannot scope by script, so both are load-bearing or harmless rather than defects.
`score-gap.py --root`, `shonen-form.py --root`, `resolve.py`, `claim-package-check.py --json`
are admitted, so the round-70 over-refusal class is in fact closed for `--root`/stdout-`--json`.

### 3.1 "Fail closed" is name-only, not content

`python_head_ok` (`figure-audit.py:490-505`) checks a literal `corpus/instruments/` prefix, a
`realpath` inside `<root>/corpus/instruments`, a basename in `PY_SCRIPT_CENSUS`, and the
per-script option set. It never checks the file's bytes, so with any `--root` whose
`corpus/instruments/<censused-name>.py` is attacker code, the gate **itself** runs it and
reports `ok` (#24). The symlink variant is correctly refused (#23), which shows the
`realpath` limb is load-bearing; the content is not. The counter's own fixtures do pass a
fixture root (`build_fixture` copies three instruments in), so "run the gate against a
fixture root" is an established use, not a hypothetical.

### 3.2-3.4 Exec/write through admitted heads (declared-open classes, now measured)

- `figure-audit-mutbat.py --instrument ABS` (#16): un-denied `--instrument`; `mutbat` reads
  that path and runs `[sys.executable, path, "--selftest"]`
  (`figure-audit-mutbat.py:44-47`). Marker file written by the "instrument".
- `limb-mutation-check.py --ledger ABS` (#17): only `--root` is denied. The ledger's `kill`
  is executed with `["bash", "-c", expanded]` (`limb-mutation-check.py:294-295`); validation
  constrains only the text **after** the last `{inst}` invocation, so a prefix such as
  `printf 'limb-ledger-exec\n' > FILE;` is accepted. Measured: `limb2.exec` = `limb-ledger-exec`.
- `resolve.py <positional>` (#11): writes `citation-survival.tsv`/`.md` next to the script.
  Fixture measurement (root `$S/rroot`, its own `resolve.py` copy):
  `DIRECT rc=0 'distinct=2 ...' 'wrote .../citation-survival.tsv'`, gate `rc=0 ok`, and
  `ls $S/rroot/corpus/instruments` went `resolve.py` → `citation-survival.md citation-survival.tsv resolve.py`.
- `kill-rule-check.py --scratch` (#15) creates a directory outside the root; `--instrument`
  and `--row-file` are also un-denied.
- Systematic scan (AST over `corpus/instruments/*.py`, names in `PY_SCRIPT_CENSUS`):
  **49 un-denied options** matching out/json/scratch/work/instrument/ledger/root/url/file/dest/write
  across the 44 censused heads, of which the ones proven to write or execute are #15-#17.

## 4. The one-line answer on the vacuous row

- R8: measured vacuous at the tip (`FIG R8 recorded=0 derived=UNAVAILABLE reason=derive-exit-1
  stale`; counter line 279 `value_ok = rc == 1 and ("FIG %s " % ...) in out`; gate line 337
  precedes line 587).
- Other vacuous rows: **R5, R6, R7**, same measured stamp and same code path. VerifyC1's
  "24 of 25 measurements re-derive a value" undercounts the debt by three.
- No R row passes on an *empty* value on both sides; the four rows pass with no comparison at
  all, which is weaker.

## 5. Smallest safe correction set for round 72 (gate not edited here)

1. **Re-word C1's positive clause** to what the counter measures: "R1-R4 are admitted and
   their own recorded value is re-derived and compared exactly; R5-R7 are admitted and the
   gate reports them stale on the counter's own nonzero exit (`derive-exit-1`), comparing no
   value; R8's row is tree-dependent and is re-anchored per (3)." This is the minimal change
   that makes the sentence true at the tip; the numeric predicate is unaffected.
2. **Re-anchor the four vacuous rows so they bind a value**: point R5-R7 at a *clean fixture
   root* (a fixture lane where the counter exits 0) so the gate takes the `derived == want`
   path, or make the row assert the exact stamp (`derived=UNAVAILABLE reason=derive-exit-1`
   plus `want=<direct value>` present in the FIG line) instead of `rc==1 and "FIG id" in out`.
   For R8, replace `grep -c records=84` with `grep -c '^records='` (returns `1` non-vacuously
   at any record count) or with a fixture-owned literal.
3. **Pin the tree**: pass an explicit `--lane` (or a fixture root) in the counting command.
   The default `--lane` is the live lane and C2's landing changed R8's branch mid-round
   (2/exit 0 at `39cde8a` → 0/exit 1 at `4e33119`/tip).
4. **Fix the frozen self-descriptions**: `c1-probe-run-r71.py`'s docstring must match its own
   code — `:37` says R8 is `| head -n 1` (code: `| grep -c records=84`) and `:33` says R4 is
   `.../corpus/knowledge/cve-json-record-format.md` (code, and `claims.json`: 
   `.../fixtures/claim-package/exemplar`). As frozen, the counter's prose enumerates a
   different R1-R8 than the rows it runs.
5. **Gate movement for round 72** (new capability, not this round's claim): deny
   `--ledger` for `limb-mutation-check.py` and `--instrument` for `figure-audit-mutbat.py` /
   `kill-rule-check.py`; deny `--scratch`/`--row-file`/`--fake` for `kill-rule-check.py`;
   add a per-script positional rule for `resolve.py` (or state the write in the lesson as a
   named exemption); and pin **content** for censused basenames (a per-basename digest check,
   or refuse when `<root>/corpus/instruments/<name>.py` is not the committed bytes), which is
   the only change that makes "fail closed" mean code rather than names.
6. **Trim the inert members** of the refusal list so the list's load-bearing members are
   visible: N10 (`-o`) is unreachable (no instrument accepts `-o`); the bare `--json`
   spellings of `citation-ground-check.py`/`gate-quote-audit.py` cannot write either.

## 6. Not run / limits of this seat

- Do-nothing (round-70 bytes) and r69-base control runs: not re-run here (VerifyC1 `w2` §2 is
  the receipt at this tip). The candidate predicate was re-run and reproduced.
- `limb-mutation-check.py --root .` direct run: not run (it copies the root and executes
  mutants); the weaker statement is in #4, and the exec class is proven by #17 instead.
- `resolve.py` against the full lane: launched, then cancelled after it had not finished
  (the mirror stat pass is long); the write is proven by the fixture measurement in §3.2,
  which is the same code path (`here`-relative `open(..., "w")`, `resolve.py:369` and
  `:609`) and shows the file appearing under the root's `corpus/instruments/`.
- `VerifyC1` §4 is used only as a prior peer finding to compare against; no verdict of mine
  rests on it.
