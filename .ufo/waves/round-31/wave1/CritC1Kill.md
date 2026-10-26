# CritC1Kill — C1 kill rule and counter: adversarial critique (round 31)

Seat `CritC1Kill`, leaf critic, round 31, lane `kasegi-shokunin`.
Base `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims freeze `738a7799`.
Write scope: this receipt and `.ufo/waves/round-31/wave1/CritC1Kill-scratch/` only.
Answering model: `devin/deepseek-v4-1-flash` (project-context route table; no model passed by this seat).
No delegation, no background jobs, no git/jj mutation, no tool installs, no network fetch.

**Bytes the figures below were measured on** (`sha256sum`, 2026-10-25T23:43:24Z; PRE-STATE —
`source-recheck.py` moved under this seat mid-round, see §5.4):

| file | sha256 |
|---|---|
| `corpus/instruments/recheck-audit.py` | `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` |
| `corpus/instruments/source-recheck.py` | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| `corpus/instruments/frontier-recheck-count.py` | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` |
| `corpus/instruments/limb-mutation-check.py` | `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` |
| `corpus/instruments/limb-ledger.json` | `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` |

The counter moved five times under this seat mid-review (`eb9b87ff…` → `cde7c2b6…` → `67db4a20…` →
`bd18c244…` → `c660a95f…`, the last stamped 2026-10-26T00:01Z). §2.1 keeps the states separate;
nothing is compared across them. The three instrument digests above are unchanged across all five
counter states.

## 0. Verdict

**The frozen C1 predicate is satisfiable without any of the 13 limbs being load-bearing.**
On the landed counter bytes, a contract-conform ledger of 13 non-load-bearing mutants prints the
target lines byte-exactly and exits 0 (§3.1):

```
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

Nine of those 13 mutants are behavior-equivalent comment patches: the instrument's own honest
`--selftest` stdout **and** stderr are byte-identical to the unmutated run (`d2adb51f86997c2c`, §3.2).
Four are module-level `NameError` imports that `py_compile` accepts (§3.2). Four rows are killed by a
kill command that produces a different result on the *same unmutated bytes* on its second invocation
(§3.2, `STATE` lines): no mutant is required for those "kills".

**The landed rows are honest, and that is exactly the problem.** All 13 real kills are
`python3 {inst} …` invocations, all three controls reuse a limb's kill, and the 13 triples are
distinct (measured, §3.5). So the lane's substance rests on author honesty plus the separate
mutation receipts (`MutRAExisting`, `MutSRExisting`, `MutFRExisting`), **not** on the counter: the
rule cannot tell an honest ledger from a degenerate one, so `killed=13` is not by itself evidence of
discrimination. With honest kills the counter *is* sensitive — downgrading one real row to a comment
patch turns it into `survivor` and reds the run (12/1, exit 1, §3.4) — so the missing clauses are
precisely the ones that bind a kill to the instrument's execution and bind the mutant to the limb.

Impacted axes: `depth:verifiability` (C1, held 4) — the claim's number does not carry its own proof
until A1.9, A2 and A3 land (§4); `coverage` (C2) unaffected.

### 0.1 State on the final counter (`c660a95f…`, §3.9)

ExecCounter hardened the counter against this review while it ran: per-row fresh scratch, double live
baseline, `python3 … {inst}` kill shape that must *end* at the instrument invocation, empty-string
signal rejection, control id→expect binding, an import gate with a completion sentinel
(`invalid:import`), and — after my last reproducer — a **separate fresh scratch and a double run for
the mutant side** (`invalid:mutant-baseline`). Selftest `cases=20 failures=0`.

Every route this seat found is closed on `c660a95f`, each by measurement (§3.9): the real ledger
prints `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` exit 0; the 13-row import-crash ledger
is `limbs=13 killed=0 survivors=0` exit 1; the `SystemExit(0)` row is `limbs=1 killed=0 survivors=0`
exit 1; the invocation-count kill is now `limbs=1 killed=0 survivors=1` exit 1 (it was `killed` at
`bd18c244`); the chained-grep row and both degenerate ledgers are refused at load (exit 2); the
one-degenerate-limb calibration is `limbs=13 killed=12 survivors=1` exit 1.

What remains is not counter-side: **A6** (a gutted module that imports cleanly and prints its own
summary), **A7** (C1's closure re-derivation checks the counter's arithmetic, not the limb) and **A11**
(`--root` scores any tree; the frozen stdout carries no root or digests) are claim-level and belong in
the L1's amendment, together with `reach` for exit-only kills.

The original finding stands as the reason those amendments exist: at `eb9b87ff` this counter accepted a
ledger of 13 non-load-bearing limbs and printed the target lines (§3.1). The lane's real ledger was
honest at every state; the rule could not tell.

## 1. Method

I wrote a contract-literal prototype counter (`contract-literal-counter.py`) that implements the
frozen INTERFACE CONTRACT and nothing else, then attacked it with a 13-row ledger carrying the exact
frozen ids (`RA-parse … FR-duplicate-entry`). Every attack was then replayed on the **landed**
counter, so each finding is a measurement of the shipped bytes, not of my reading of the contract.
Scratch lanes are `tempfile.mkdtemp` copies; the lane tree was never written except for this seat's
own receipt and scratch directory.

Contract clauses are referred to below as: **C-live** (live baseline must exit `live_exit` and match
`signal`, else `invalid:live-baseline`), **C-find** (`find` exactly once, else `invalid:find-count`),
**C-noop** (mutated bytes equal original, else `invalid:noop`), **C-compile** (`py_compile` of the
mutant, else `invalid:nocompile`), **C-killed** ("killed when the mutant's (exit != live_exit) or
(signal does not match); else survivor"), **C-ctl** (`rejected` counts controls whose verdict equals
`expect`), **C-exit** (exit 0 iff `n==k`, `s==0`, every limb valid, `rejected==controls`), and
**C-scratch** (one `mkdtemp` scratch lane; live run, then patch, then mutant run).

## 2. Attack table — caught or not, and the smallest fix

| # | attack | mechanism | contract clause | caught? | evidence | smallest safe correction |
|---|---|---|---|---|---|---|
| A1 | **Byte-inspection kill** | `kill` reads the instrument's source instead of executing it: `grep -cxF '<source line>' {inst}`. The mutation is a trailing `# crit-eq` comment, so the mutant is behavior-equivalent by construction. | none; C-killed fires on the exit difference | **NO** | 5 rows `RA-parse … RA-instrument`, §3.1; equivalence proven §3.2 (`identical=True`, digest `d2adb51f86997c2c` both sides) | require the kill command to invoke the instrument as a program (literal `python3 {inst}`) → `invalid:kill-shape`; plus A2 `reach` for the general case |
| A2 | **Stateful / order-dependent kill** | `if [ -e .crit-<id> ]; then echo CRIT-SECOND-RUN; exit 7; fi; touch .crit-<id>; echo CRIT-FIRST-RUN; exit 0`. C-scratch shares one scratch across the live and mutant runs, so the live run passes and the *second* invocation fails. | none; C-scratch as written *creates* the hole | **NO** | 4 rows `RA-own … RA-expect-unexpected`; on **unmutated** bytes run1=`0/CRIT-FIRST-RUN`, run2=`7/CRIT-SECOND-RUN` (§3.2 `STATE`) | fresh scratch copy **per run** (live and mutant never share a filesystem); run the live baseline twice and require the same `(exit, sig)`; run the mutant twice likewise |
| A3 | **Import-crash mutant** | module-level constant assigned an undefined name: compiles (`py_compile` clean), dies `NameError` at import, so every exercise command differs for a reason unrelated to the named limb. | C-compile passes it; C-killed fires | **NO** | 4 rows `SR-stem-mismatch … FR-duplicate-entry`, §3.2 `CRASH … py_compile=ok run_exit=1 traceback=NameError: name '_crit_undefined_limb' is not defined` | a mutant whose stdout+stderr carries `Traceback (most recent call last)` that the live run lacks is `invalid:crash`, never `killed`; plus A2 `reach` |
| A4 | **Vacuous signal** | `signal = "(?s).*"` matches every output, so the `sig` half of C-killed is dead and every kill is exit-only. | C-live passes (it matches), nothing forbids a total regex | **NO** | full 13/13 + `controls=3 rejected=3`, exit 0 with `(?s).*` (§3.3) | reject a `signal` that matches the empty string (`re.search(signal, "")`) → `invalid:signal-vacuous`; A2 `reach` then supplies the executed-instrument evidence the signal was pretending to give |
| A5 | **Id/expect unbound controls** | `CTL-equivalent` carries a **no-op** patch and `expect=invalid:noop`: three controls, `rejected=3`, and no equivalent-mutant control exists at all. | C-ctl compares verdict to `expect` only; the `id` enum carries no binding force. C1's kill rule also reads only the summary line. | **NO** | §3.3 run 2: `CONTROL CTL-equivalent verdict=invalid:noop expected=invalid:noop ok=y`, `controls=3 rejected=3`, exit 0 | bind ids to expects in the counter (`CTL-noop⇒invalid:noop`, `CTL-nocompile⇒invalid:nocompile`, `CTL-equivalent⇒survivor`) and require `CTL-equivalent` to reuse one limb's `instrument`+`kill`+`signal`+`live_exit` |
| A6 | **Whole-file gutting / oversized mutant** | `find` spans a whole module body, `replace` is a stub: C-find passes (occurs once), C-compile passes, C-killed fires. | none (no size or span bound) | **NO** | not separately run; structurally identical to A3 and closed by the same `reach` rule | `reach` (a gutted module never prints its own summary); optionally a bound on mutant line-delta |
| A7 | **Closure re-derivation is arithmetic only** | C1's kill rule says a closure "re-derives any one ledger patch by hand … and the result differs from the counter's LIMB line". For a degenerate row the hand re-derivation *reproduces* `killed`. | C1 kill rule, closure clause | **NO (partial)** | §3.2 hand run: live `grep -cxF` = `1` (exit 0), mutant = `0` (exit 1) ⇒ `killed` reproduced, while the mutant's `--selftest` stdout/stderr are byte-identical to live | the closure must also run the instrument's **own** report on the mutant and require the observable to move (amendment A3) |
| A8 | **Non-deterministic live baseline** | C-live runs the baseline once; if the instrument is nondeterministic the live/mutant comparison is noise. | none | **NO** (deterministic instance = A2) | A2 is the deterministic form: two identical invocations on identical bytes disagree | double-run both sides (part of A1's fix) |
| A9 | **Docstring / dead-branch / trailing-space mutant** | behavior-preserving patch, honest kill. | C-killed → `survivor`; C-exit reds the run | **YES** | §3.4: `LIMB RA-parse … verdict=survivor`, `limbs=13 killed=12 survivors=1`, exit 1 | none — this is the clause working |
| A10 | **Kill command reads the real lane, not the scratch** | absolute lane path inside `kill`; live and mutant then run the same real bytes. | none forbids it; result is `survivor` | **NO clause, but self-punishing** (survivor reds the run) | not run; the failure mode is a misleading `survivor`, not a false `killed` | reject a `kill` containing the resolved lane root → `invalid:kill-shape` |
| A11 | **`--root` at a doctored tree** | the counter scores any tree; the printed summary names neither root nor digests. | C1's frozen `counter_commands` run from the lane, so the published number is pinned; the receipt is not | **NO** | `--root` accepted, `limb-mutation-check.py:507` | additive `--json` receipt with root + per-row pre/post instrument sha256 and run digests (does not touch the frozen stdout grammar) |
| A12 | **13-id set unvalidated** | the counter validates ids only as strings; a ledger of 13 non-frozen ids would pass. | none | **NO** (but moot here) | my degenerate ledger carries the *exact* frozen ids, so id validation would not have helped | optional: assert the frozen 13-id set |

Two hardenings the landed counter already has and the contract does not require — both worth
freezing in the amendment rather than leaving as undocumented virtue: `PYTHONDONTWRITEBYTECODE=1` plus
`drop_bytecode_cache()` so a stale `.pyc` cannot stand in for the mutated bytes
(`limb-mutation-check.py:256-264`), and `invalid:timeout` instead of a kill
(`limb-mutation-check.py:68`, `:323`) — the second is an **extension of the frozen verdict enum**,
which C1's kill rule does not enumerate.

### 2.1 Where each attack stands across the four counter states

| attack | `eb9b87ff…` (§3.1–3.4) | `cde7c2b6…` (§3.6) | `67db4a20…` (§3.8) | `bd18c244…` (§3.9) | `c660a95f…` (§3.9) | what closed it |
|---|---|---|---|---|---|---|
| A1 byte-inspection kill | open — 5/5 killed | **closed** | closed | closed | closed | kill shape `python3 … {inst}` |
| A2 stateful kill (2-invocation) | open — 4/4 killed | **closed** | closed | closed | closed | double live baseline |
| A3 import-crash mutant | open — 4/4 killed | **open — 13/13 killed, exit 0** | **closed** | closed | closed | import gate (`invalid:import`) |
| A4 vacuous signal | open — 13/13 killed | **closed** | closed | closed | closed | empty-string signal rejection |
| A5 id/expect unbound controls | open — `rejected=3` with a no-op `CTL-equivalent` | **closed** | closed | closed | closed | `CONTROL_ID_EXPECTS` binding |
| A6 gutted mutant | open | open | open | open | **open** | nothing yet; a gutted module that imports cleanly and prints its own summary is not distinguishable — `reach` (A2) or a mutant-size bound |
| A7 closure is arithmetic | open | open | open | open | **open** (claim-level) | A3 |
| A9 equivalent mutant, honest kill | caught | caught | caught | caught | caught (§3.4) | C-killed working |
| A10 lane-path kill | not run | closed | closed | closed | closed | kill shape |
| A11 `--root` digest | open | open | open | open | **open** | additive `--json` receipt |
| A12 id set | open (moot) | open (moot) | open (moot) | open (moot) | **open** (moot) | optional |
| A13 `SystemExit(0)` at module level | — | — | **OPEN — killed, limb never ran** | **closed** | closed | import gate completion sentinel |
| A14 chained command after `{inst}` | — | — | **OPEN — killed by exit alone, signal survives** | **closed** | closed | kill must END at the instrument invocation |
| **A15 invocation-count kill** | — | — | — | **OPEN — killed, equivalent patch** | **closed — survivor** | mutant side gets its own fresh scratch and a double run |

A13/A14/A15 are holes in the counter's *added* hardening, not in the frozen contract (which knows no
import gate and no kill shape at all); all three are now closed; they are listed here because the claim's number is only as good
as the counter that prints it. `reach` cannot be bolted on as a decorative ledger field: the counter's
row validator drops unknown keys, so a `reach` nobody enforces would read as a guarantee while
changing no verdict (ExecLedgerMerge, `agent://ExecLedgerMerge`, this round). It only becomes a rule
when the counter *requires* it.

## 3. Transcripts

### 3.1 The landed counter at `eb9b87ff…` accepts the degenerate ledger (the target lines, exit 0)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ python3 corpus/instruments/limb-mutation-check.py \
    --ledger .ufo/waves/round-31/wave1/CritC1Kill-scratch/degenerate-ledger.json --root "$PWD"
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=7/n verdict=killed
LIMB RA-completeness live=0/y mutant=7/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=7/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=7/n verdict=killed
LIMB SR-stem-mismatch live=0/y mutant=1/n verdict=killed
LIMB SR-occurrence-not-unique live=0/y mutant=1/n verdict=killed
LIMB FR-missing-entry live=0/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=0/y mutant=1/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

The same output is produced by the prototype counter, i.e. by a literal implementation of the
contract, so the acceptance is the rule's, not one implementation's. Rows 1–5 are A1, 6–9 are A2,
10–13 are A3.

### 3.2 What each row actually measures

```
$ python3 .ufo/waves/round-31/wave1/CritC1Kill-scratch/prove-attacks.py
EQUIV RA-parse                   honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
EQUIV RA-cwd                     honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
EQUIV RA-paths                   honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
EQUIV RA-cdroot                  honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
EQUIV RA-instrument              honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
EQUIV RA-own                     honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
      STATE RA-own               unmutated-run1=0 CRIT-FIRST-RUN   unmutated-run2=7 CRIT-SECOND-RUN
EQUIV RA-completeness            honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
      STATE RA-completeness      unmutated-run1=0 CRIT-FIRST-RUN   unmutated-run2=7 CRIT-SECOND-RUN
EQUIV RA-expect-missing          honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
      STATE RA-expect-missing    unmutated-run1=0 CRIT-FIRST-RUN   unmutated-run2=7 CRIT-SECOND-RUN
EQUIV RA-expect-unexpected       honest_run original=0/d2adb51f86997c2c mutated=0/d2adb51f86997c2c identical=True
      STATE RA-expect-unexpected unmutated-run1=0 CRIT-FIRST-RUN   unmutated-run2=7 CRIT-SECOND-RUN
CRASH SR-stem-mismatch           py_compile=ok run_exit=1 traceback=NameError: name '_crit_undefined_limb' is not defined
CRASH SR-occurrence-not-unique   py_compile=ok run_exit=1 traceback=NameError: name '_crit_undefined_limb' is not defined
CRASH FR-missing-entry           py_compile=ok run_exit=1 traceback=NameError: name '_crit_undefined_limb' is not defined
CRASH FR-duplicate-entry         py_compile=ok run_exit=1 traceback=NameError: name '_crit_undefined_limb' is not defined
```

Hand re-derivation of one row exactly as C1's closure clause prescribes (A7), on a scratch copy:

```
--- before mutation ---
1                      # grep -cxF 'FROZEN_LIMBS = ("parse", "cwd", "paths")' → count
grep_exit=0
selftest_exit=0
d2adb51f86997c2c live.out
e3b0c44298fc1c14 live.err
--- apply the ledger patch by hand ---
find-count=1 patched
--- after mutation ---
0
grep_exit=1
selftest_exit=0
d2adb51f86997c2c mut.out
e3b0c44298fc1c14 mut.err
stdout IDENTICAL
stderr IDENTICAL
```

`killed` reproduced by hand, and the mutant is behaviorally indistinguishable. The closure clause
verifies the counter's arithmetic; it does not verify the limb.

### 3.3 Control hole (A5) and vacuous signal (A4) on the landed counter at `eb9b87ff…`

```
$ python3 corpus/instruments/limb-mutation-check.py \
    --ledger .ufo/waves/round-31/wave1/CritC1Kill-scratch/degenerate-ledger-controls.json --root "$PWD" | tail -5
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=invalid:noop expected=invalid:noop ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
exit=0
```

```
$ python3 corpus/instruments/limb-mutation-check.py \
    --ledger .ufo/waves/round-31/wave1/CritC1Kill-scratch/vacuous-signal-ledger.json --root "$PWD" | tail -4
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
exit=0
```

### 3.4 Calibration — the counter does discriminate when kill and mutant are honest (`eb9b87ff…`)

The **real** ledger with exactly one row downgraded to a behavior-equivalent comment patch, kill
unchanged (`python3 {inst} --selftest`):

```
LIMB RA-parse live=0/y mutant=0/y verdict=survivor
limbs=13 killed=12 survivors=1
controls=3 rejected=3
exit=1
```

So A9 is caught, and the gap in §0 is specifically the absence of any clause binding the kill to the
instrument's execution (A1/A4/A10) or the mutant to the limb (A2/A3/A6).

### 3.5 The landed real ledger (for the record, PRE-STATE, in-flight; reproduced on `c660a95f` in §3.9)

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed
…
LIMB SR-stem-mismatch live=1/y mutant=0/n verdict=killed
LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

Structural check of the same file: 13 limbs, 3 controls, 13 distinct `(instrument, find, replace)`
triples, 13 rows carrying `note`, and all three controls reuse a limb's
`(instrument, kill, signal, live_exit)` — i.e. the rows are honest. This is the lane's merit, not
the rule's.

### 3.6 The route that survived at `cde7c2b6…`: import-crash mutants

Thirteen mutants, one per frozen limb id, each assigning a module-level name to an undefined name so
the instrument compiles and dies at import; honest kills (`python3 {inst} --selftest`,
`python3 {inst} --root {root}`), the real ledger's own three controls. All 13 `find` counts asserted
== 1 before the run. On counter `cde7c2b6…`:

```
$ python3 corpus/instruments/limb-mutation-check.py \
    --ledger .ufo/waves/round-31/wave1/CritC1Kill-scratch/residual-crash-ledger.json --root "$PWD"
LIMB RA-parse live=0/y mutant=1/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/n verdict=killed
LIMB RA-paths live=0/y mutant=1/n verdict=killed
LIMB RA-cdroot live=0/y mutant=1/n verdict=killed
LIMB RA-instrument live=0/y mutant=1/n verdict=killed
LIMB RA-own live=0/y mutant=1/n verdict=killed
LIMB RA-completeness live=0/y mutant=1/n verdict=killed
LIMB RA-expect-missing live=0/y mutant=1/n verdict=killed
LIMB RA-expect-unexpected live=0/y mutant=1/n verdict=killed
LIMB SR-stem-mismatch live=0/y mutant=1/n verdict=killed
LIMB SR-occurrence-not-unique live=0/y mutant=1/n verdict=killed
LIMB FR-missing-entry live=0/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=0/y mutant=1/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
exit=0
```

Each mutant's failure mode is the same `NameError: name '_crit_undefined_limb' is not defined` at
import with `py_compile` clean (§3.2 `CRASH` lines), i.e. the limb named by the row never executes.

### 3.7 The import-time gate is non-breaking for all 13 landed rows

Each landed row's exact patch applied to a scratch copy, then the mutant **imported** (module level
executes, `main()` does not) and the row's own kill run:

```
$ python3 .ufo/waves/round-31/wave1/CritC1Kill-scratch/measure-import-gate.py
rows=13 controls=3
RA-parse                   import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-cwd                     import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-paths                   import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-cdroot                  import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-instrument              import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-own                     import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-completeness            import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-expect-missing          import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
RA-expect-unexpected       import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=False
SR-stem-mismatch           import=0   IMPORT-OK   mutant_exit=0   signal_survives=False traceback=False
SR-occurrence-not-unique   import=0   IMPORT-OK   mutant_exit=0   signal_survives=False traceback=False
FR-missing-entry           import=0   IMPORT-OK   mutant_exit=1   signal_survives=False traceback=True
FR-duplicate-entry         import=0   IMPORT-OK   mutant_exit=0   signal_survives=False traceback=False
```

Three facts the amendment rests on: every landed mutant **imports cleanly** (so an import gate moves
no landed verdict); every landed row is killed by **signal loss**, not by exit alone (so the stricter
exit-only branch is free); and exactly one landed row carries a traceback, `FR-missing-entry`, where
the crash *is* the limb — which is why a blanket traceback rule is the wrong correction.

### 3.8 Two routes that survive the import gate (`67db4a20…`)

A two-row ledger — one `SystemExit(0)` at module level, one behavior-equivalent comment patch behind a
kill that chains a source grep after a legitimate run — with the real ledger's own three controls:

```
$ python3 corpus/instruments/limb-mutation-check.py \
    --ledger .ufo/waves/round-31/wave1/CritC1Kill-scratch/post-gate-ledger.json --root "$PWD"
counter=67db4a2025d3 23:54:20Z
LIMB RA-parse live=0/y mutant=0/n verdict=killed
LIMB RA-cwd live=0/y mutant=1/y verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected:survivor ok=y
limbs=2 killed=2 survivors=0
controls=3 rejected=3
exit=0
```

`RA-parse`: `raise SystemExit(0)` in place of `FROZEN_LIMBS = ("parse", "cwd", "paths")` — the import
gate runs `python3 -c IMPORT_GATE <path>`, the module level terminates the interpreter with status 0,
the gate reads a clean exit as success, and the kill run then exits 0 printing nothing (signal lost).
The limb never ran. `RA-cwd`: `STRICT_LIMBS = (…)  # crit-eq` behind
`python3 {inst} --selftest && grep -cxF 'STRICT_LIMBS = (…)' {inst}` — the instrument runs normally
(`mutant=1/y`, signal survives) and only the chained grep flips the exit.

Both are non-breaking to close: zero landed kills chain anything after `{inst}` (measured across all 13
limbs + 3 controls; every landed kill shape is `python3 …`), and no instrument's module level raises
`SystemExit`. On the same bytes the import-crash ledger is fully refused and the real ledger still
passes:

```
$ … --ledger …/residual-crash-ledger.json        → limbs=13 killed=0 survivors=0, invalid:import ×13, exit 1
$ … --ledger corpus/instruments/limb-ledger.json → limbs=13 killed=13 survivors=0, controls=3 rejected=3, exit 0
$ … --ledger …/degenerate-ledger.json            → exit 2, "kill must run the instrument as a program … at a command boundary"
$ … --ledger …/one-degenerate-limb-ledger.json   → limbs=13 killed=12 survivors=1, exit 1
```

### 3.9 The last route: a kill that counts its own invocations (open at `bd18c244`, closed at `c660a95f`)

The live baseline and its confirmation run in the same scratch as the mutant run, so a kill can be
stateful at depth three. Over a behavior-equivalent comment patch (`FROZEN_LIMBS = (…)  # crit-eq`),
with the kill ending at the instrument invocation as the shape rule requires:

```
kill = n=$(cat .n 2>/dev/null || echo 0); n=$((n+1)); echo $n > .n; \
       if [ "$n" -ge 3 ]; then exec python3 {inst} --selftest >/dev/null; fi; \
       python3 {inst} --selftest

$ python3 corpus/instruments/limb-mutation-check.py \
    --ledger .ufo/waves/round-31/wave1/CritC1Kill-scratch/three-state-kill-ledger.json --root "$PWD"
LIMB RA-parse live=0/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected:invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected:survivor ok=y
limbs=1 killed=1 survivors=0
controls=3 rejected=3
exit=0
```

Three consecutive invocations on the same scratch, mutant bytes in place:

```
invocation (exit, stdout_bytes, signal_present): [(0, 3169, True), (0, 3169, True), (0, 0, False)]
```

Runs 1 and 2 are the live baseline and its confirmation, both honest; run 3 — the mutant run — is
silenced by the counter file, so the signal disappears and the row is `killed` although the patch is a
comment. The mutant's own selftest on a clean copy is unchanged (exit 0, identical output).

On the same bytes, the rest of the suite:

```
residual-crash-ledger.json      → limbs=13 killed=0 survivors=0, exit 1   (invalid:import ×13)
a13-ledger.json (SystemExit(0)) → limbs=1  killed=0 survivors=0, exit 1   (invalid:import)
post-gate-ledger.json           → exit 2, "limbs[1].kill must end at the instrument invocation"
corpus/instruments/limb-ledger.json → limbs=13 killed=13 survivors=0, controls=3 rejected=3, exit 0
degenerate-ledger.json          → exit 2, "kill must run the instrument as a program … at a command boundary"
one-degenerate-limb-ledger.json → limbs=13 killed=12 survivors=1, exit 1
```

**Closed at `c660a95f…` (2026-10-26T00:01Z).** The mutant side now gets its own fresh scratch copy and
runs the kill twice, with a disagreement reported as `invalid:mutant-baseline`. The same reproducer on
those bytes:

```
LIMB RA-parse live=0/y mutant=0/y verdict=survivor
limbs=1 killed=0 survivors=1
controls=3 rejected=3
exit=1
```

and the rest of the suite on `c660a95f`:

```
a13-ledger.json                 → limbs=1  killed=0 survivors=0, controls=3 rejected=3
residual-crash-ledger.json      → limbs=13 killed=0 survivors=0, controls=3 rejected=3
post-gate-ledger.json           → exit 2, "limbs[1].kill must end at the instrument invocation; '&' follows {inst}"
degenerate-ledger.json          → exit 2, "kill must run the instrument as a program … at a command boundary"
one-degenerate-limb-ledger.json → limbs=13 killed=12 survivors=1, controls=3 rejected=3
corpus/instruments/limb-ledger.json → limbs=13 killed=13 survivors=0, controls=3 rejected=3
```

## 4. Proposed frozen-rule amendment (for the L1 to append as an AMENDMENT file)

**A1 — counter, code only, no ledger-schema change** (`limb-mutation-check.py`):
1. Build a **fresh scratch copy per run**; the live and mutant runs never share a filesystem.
   *Landed in `cde7c2b6` as per-ROW, not per-run: the live run, its confirmation and the mutant run
   still share one copy — that is the surviving A15 (§3.9), fixed by item 9.*
2. Run the live baseline **twice** and require identical `(exit, signal-match)`. A `killed` verdict
   requires stable live ≠ mutant. *Landed in `cde7c2b6`; extending the double run to the mutant side
   is still worth having.* (Closes A2, A8.)
3. **Import gate (replaces the traceback rule).** After `py_compile`, execute the mutant's module
   level in the scratch (`importlib.util.spec_from_file_location` + `module_from_spec` +
   `exec_module`, `main()` not run); an exception there is `invalid:import`, never `killed`. This is
   the module-level-death class (A3, A6) and it is measured non-breaking for all 13 landed rows
   (§3.7). Do **not** add a blanket traceback rule: `FR-missing-entry` is killed by a runtime
   `FileNotFoundError`, and that crash is the limb. *Landed in `67db4a20`; the residual ledger is now
   `limbs=13 killed=0 survivors=0` and the real ledger still passes (§3.8).*
4. A `kill` that does not invoke the instrument as a program (`python3 [flags] {inst}`) is
   `invalid:kill-shape`; a `kill` containing the resolved lane root is `invalid:kill-shape`.
   *First half landed in `cde7c2b6`; the lane-root half is not.* (Closes A1, A10.)
5. A `signal` that matches the empty string is `invalid:signal-vacuous`. *Landed in `cde7c2b6`.*
   (Closes A4.)
6. Bind control ids to expects (`CTL-noop⇒invalid:noop`, `CTL-nocompile⇒invalid:nocompile`,
   `CTL-equivalent⇒survivor`). *Landed in `cde7c2b6`.* (Closes A5.)
7. **Import gate completion sentinel.** `IMPORT_GATE` must print a sentinel after `exec_module`, and
   `import_verdict` must require exit 0 **and** that sentinel in stdout. Without it a module level
   that raises `SystemExit(0)` is read as a clean import and the limb never runs (§3.8 A13). *Landed
   in `bd18c244` (`LIMB-IMPORT-OK`).*
8. **Kill must end at the instrument invocation.** After the `{inst}` token only redirections may
   follow: no `;`, `&&`, `||`, `|`. Otherwise a chained `grep` of the source manufactures an exit
   difference while the instrument's own output is unchanged (§3.8 A14). *Non-breaking: zero landed
   kills chain anything after `{inst}`. Landed in `bd18c244`.*
9. **Run the mutant in its own fresh scratch copy, twice.** The live baseline, its confirmation and
   the mutant run currently share one scratch, so a kill that counts its invocations passes runs 1–2
   and misbehaves on run 3 (§3.9 A15). Give the mutant its own copy (and its own repeat), so the
   double-run rule means the same thing on both sides. *One clause; no schema change.*

**A2 — ledger schema, needs the L1 because the interface is frozen, and needs the counter to enforce
it:** a row gains `reach`, a Python regex (`re.MULTILINE`) that must match **both** runs' output.
Required **only where the kill is exit-only** (the signal still matches and the exit differs): that is
the branch where a post-summary crash or an early `sys.exit` can masquerade as discrimination. On
signal-loss kills `reach` is optional, because a limb whose observable *is* a crash
(`FR-missing-entry`) has no post-crash marker to match. A decorative `reach` is worse than none — the
counter's row validator drops unknown keys, so an unenforced field reads as a guarantee while moving
no verdict (ExecLedgerMerge, `agent://ExecLedgerMerge`, this round).

**A3 — claim kill rule:** the closure re-derivation must run the instrument's **own** report on the
patched copy (its `--selftest`, or the harness on its fixture root) and require the observable to
move, not only the row's `kill`. Otherwise the closure re-checks the counter's arithmetic (proven
degenerate in §3.2). This aligns C1's closure with what `MutRAExisting` / `MutSRExisting` /
`MutFRExisting` already measure, and with the contract's own survivor rule ("strengthening IS the
work").

**A4 — verdict-enum extension:** record `invalid:timeout` (already emitted at
`limb-mutation-check.py:68`, `:323`) in the frozen enum, since C1's kill rule enumerates neither it
nor the `invalid:import` / `invalid:unreached` / `invalid:kill-shape` / `invalid:signal-vacuous`
reasons proposed above.

## 5. Residuals this seat could not close

1. **`--root` at a doctored tree** (A11): the counter scores any tree and the frozen stdout carries
   no root or digest, so a receipt cannot prove which bytes were scored. Mitigated only by C1's
   frozen `counter_commands` (cwd = lane). Amendment: additive `--json` receipt with root + per-row
   pre/post instrument sha256 and run digests.
2. **Closure clause is arithmetic** (A7): proven above; needs A3.
3. **Frozen-13 id set unvalidated** (A12): moot for this ledger (the degenerate one uses the exact
   ids), so no rule change is required for the attack to work — worth recording as a known limit.
4. **In-flight bytes**: `source-recheck.py` moved `559e0442…` → `fd2e01e8…` and
   `limb-mutation-check.py` moved `eb9b87ff…` → `cde7c2b6…` → `67db4a20…` while this seat ran;
   `recheck-audit.py` was already `5d4842da…` (base `3fc0d751…`). Every figure in this receipt is at
   the §0 digests, and §2.1 keeps the counter states separate. Re-run after ExecRALimbs /
   ExecSRLimbs / ExecCounter quiesce:
   `python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json`,
   the §3.8 `post-gate-ledger.json` replay, and the §3.6 residual replay. Numbers here are PRE-STATE
   and are not compared to any after-column (M30-3).
5. **No counter-side route is open at `c660a95f`.** Every route this seat found is closed by
   measurement (§3.9). What remains is claim-level and belongs to the L1's amendment: A6 (gutted
   module), A7 (closure is arithmetic) and A11 (`--root` without digests), plus `reach` for exit-only
   kills. Until A7/A2 land, C1's `killed=13` should still be read together with §3.7's independent
   measurement (all 13 landed mutants import cleanly, all 13 are killed by signal loss) and with the
   three mutation receipts.

## 6. Peer messages sent

- `agent://ExecCounter` — (1) the §3.1 reproducer plus the code-only fixes (fresh scratch per run,
  `python3 {inst}` kill shape, vacuous-signal and control-binding notes); (2) after `cde7c2b6`, the
  surviving §3.6 reproducer and the corrected fix — an **import-time** gate, not the blanket
  traceback rule they rightly refused, with the §3.7 measurement that all 13 landed rows import
  cleanly and are killed by signal loss; (3) after `67db4a20`, the two post-gate routes (§3.8) and
  their one-line fixes: a completion sentinel in `IMPORT_GATE`, and a kill that ends at the
  instrument invocation; (4) after `bd18c244`, confirmation that both landed and the last surviving
  route (A15, the invocation-count kill) with its one-clause fix; (5) after `c660a95f`, confirmation
  that A15 is closed (reproducer now `limbs=1 killed=0 survivors=1`, exit 1) and that the real ledger
  is unchanged.
- `agent://ExecLedgerMerge` — the control-hole reproducer, the `reach` field, id→expect binding,
  `CTL-equivalent` reusing a limb kill, and the `invalid:timeout` enum gap for the amendment; and
  their correction that an unenforced `reach` is decoration, which scoped A2 to the exit-only branch.

## 7. Artifacts (this seat's scratch, critique-only — never merge into `corpus/`)

| file | role |
|---|---|
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/contract-literal-counter.py` | prototype implementing the frozen contract literally |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/build-ledgers.py` | emits the ledgers and asserts every `find` count == 1 |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/prove-attacks.py` | equivalence / crash / state proofs in §3.2 |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/measure-import-gate.py` | the §3.7 import-gate measurement on the 13 landed rows |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/degenerate-ledger.json` | 13 non-load-bearing limbs, exact frozen ids, honest control trio |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/degenerate-ledger-controls.json` | same limbs, `CTL-equivalent` downgraded to a no-op |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/vacuous-signal-ledger.json` | every `signal` = `(?s).*` |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/residual-crash-ledger.json` | 13 import-crash limbs, honest kills, the real ledger's controls (§3.6) |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/post-gate-ledger.json` | the two post-gate routes (§3.8) |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/a13-ledger.json` | the `SystemExit(0)` row alone (§3.9) |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/three-state-kill-ledger.json` | the invocation-count kill (§3.9) |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/honest-survivor-ledger.json` | one equivalent mutant under an honest kill → `survivor`, exit 1 |
| `.ufo/waves/round-31/wave1/CritC1Kill-scratch/one-degenerate-limb-ledger.json` | the real ledger with `RA-parse` downgraded (§3.4) |

Total 66 KB of file content (84 KB on disk); no corpus copy, no tarball needed (R14).
