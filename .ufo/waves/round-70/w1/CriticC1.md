# CriticC1 — round 70, attack on C1 (python-head write/exec/ingress option refusal)

**Verdict: FINDINGS.** C1's frozen *predicate* reproduces exactly (candidate `measurements=12 failures=0`
exit 0; base `measurements=12 failures=9` exit 1), so no enumerated probe is defeated. C1's frozen
*declared sentence* is **refuted by measurement**: "while keeping every read-only derive admitted" is false
for 10 paired rows — the candidate refuses read-only derives the base admits and re-derives
(`ok.py --out x`, `claim-package-check.py … --json`, `capture-binding-check.py --root .`,
`kill-rule-check.py --root .`, `r44-frontier-count.py --root .`, and four more). Separately, the exec class
the round names is reachable **with no option at all**: `python3 corpus/instruments/frontier-recheck-count.py`
(no arguments) is admitted by both gates and runs the fixture entry's `recheck:` payload through `bash -c`
(marker 1, 51 `bash` invocations). The deny-list closes spellings, not the class.

Nothing in the lane was edited, staged, committed or pushed. Scratch: `/fast/scratch/hyaku/kasegi-r70/CriticC1/`
(removed at the end of this seat; every receipt below is pasted, not pointed at).

## Inputs (sha256 verified against `pins-r70.txt` before any run)

```
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  candidate = git show c1051749:corpus/instruments/figure-audit.py
c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde  base      = .ufo/waves/round-70/controls/base-gate-r70.py
aaee62290853791d0d0768fa7633f908e32ae5783c6c72a8cc354050f5276176  counter   = .ufo/waves/round-70/controls/c1-probe-run-r70.py
```
Host: Python 3.14.8, git 2.56.0, GNU sort 9.12. No tool installed or upgraded (pacman paused; nothing needed).

## Baseline, re-measured from committed bytes (paired, independent of the round's receipts)

```
python3 -B c1-probe-run-r70.py --gate <candidate> --work …/CAND --mode candidate
  VERIFY measurements=12 failures=0 gate_sha256=7a8d52eb… mode=candidate          exit 0
python3 -B c1-probe-run-r70.py --gate <base>      --work …/BASE --mode base
  MEASURE P1..P3 FAIL rc=1 refused=0 marker_runs=1
  MEASURE P4..P6 FAIL rc=1 refused=0 wrote=1
  MEASURE P7      FAIL rc=1 refused=0 marker_runs=1 wrote=1
  MEASURE selftest FAIL selftest cases=86 failures=0
  MEASURE no-write-side-effect FAIL marker_runs=4
  VERIFY measurements=12 failures=9 gate_sha256=c09b0fb1… mode=base             exit 1
```
The frozen facts hold on this host. My attack therefore aims at (i) spellings the predicate does not
enumerate and (ii) the declared universal, not at the twelve measurements.

## Method

Fixture `x` = full `git archive c1051749 | tar -x` (14 068 files) under scratch, plus `corpus/instruments/ok.py`
(`print(35)`) and one patched `recheck:` line (F01 `corpus/knowledge/cvss-v4-severity-and-vector.md`):
`printf 'ran\n' >> <marker.exec>; cd <x> && python3 corpus/instruments/source-recheck.py …` — the same
payload shape the committed counter uses. Fixture `repo` = `mktemp -d -p <scratch> && git -C "$D" init -q`,
`git -C "$D" rev-parse --show-toplevel` asserted equal to `$D`, one commit via `-c user.email=… -c user.name=…`.
Every row is run three ways with the same ledger (one figure, `want` = the value the derive really prints):
direct (`cwd=root`), base gate, candidate gate. `TMPDIR=HYAKU_SCRATCH=<scratch>/tmp`; the outside dir is
cleared before each measurement so a re-write is still a visible creation; a `PATH`-prepended `bash` shim
(`printf 'shim\n' >> marker.shim; exec /usr/bin/bash "$@"`) counts `bash` invocations that are invisible to a
file marker; `tree_sig(root)` = (path,size,mtime_ns) before/after every run catches write **and delete**.
"Admitted" = the gate did not print `reason=derive-not-read-only`; a stale figure verdict is not a refusal.

## Ranked table

| # | derive | base | candidate | evidence | class |
|---|---|---|---|---|---|
| 1 | `python3 corpus/instruments/frontier-recheck-count.py` | rc=0 **admitted** | rc=0 **admitted** | `marker.exec=1`, `shim=51`, gate line `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0` | **ADMITTED-EXEC, no option at all** — P1's payload with zero denied tokens |
| 2 | `python3 corpus/instruments/ok.py --out x` | rc=0, `derived=35 ok` | rc=2 **refused** | value should have been `35` | **OVER-REFUSAL**, read-only (`ok.py` is the committed counter's own fixture script, `print(35)`, which ignores argv) |
| 3 | `python3 corpus/instruments/claim-package-check.py corpus/instruments/fixtures/claim-package/exemplar --json` | rc=0 `FIG ok` | rc=2 **refused** | value: `{"exit": 0, "fail": 0, "package": "…/exemplar", "pass": 8, …}` | **OVER-REFUSAL** — `--json` is `action='store_true'` (stdout, no file; `claim-package-check.py:791`) |
| 4 | `python3 corpus/instruments/capture-binding-check.py --root .` | rc=0 `FIG ok` | rc=2 **refused** | value: `records=84 bound=84 unbound=0` | **OVER-REFUSAL**, read-only lane pointer |
| 5 | `python3 corpus/instruments/kill-rule-check.py --root .` | rc=0 `FIG ok` | rc=2 **refused** | value: `survivors=0` | **OVER-REFUSAL** |
| 6 | `python3 corpus/instruments/r44-frontier-count.py --root .` | rc=0 `FIG ok` | rc=2 **refused** | value: `frontier rows=48 admitted=48` | **OVER-REFUSAL** |
| 7 | `python3 corpus/instruments/r44-frontier-count.py --root . && cat corpus/README.md` | rc=0 `FIG ok` | rc=2 **refused** | value: the F48 row line | **OVER-REFUSAL** in a compound derive |
| 8 | `python3 corpus/instruments/capture-binding-check.py --root . \| head -n 1` | rc=1 admitted (stale) | rc=2 **refused** | direct value: `MANIFEST round-23 records=4 url_bound=4 fetched=0 archival=4` | **OVER-REFUSAL** in a pipeline |
| 9 | `python3 corpus/instruments/citation-ground-check.py --root .` | rc=1 admitted (stale) | rc=2 **refused** | value: `verdict=failed` | **OVER-REFUSAL** (diagnostic value) |
| 10 | `python3 corpus/instruments/gate-quote-audit.py --root .` | rc=1 admitted | rc=2 **refused** | value: `GATE-QUOTE-AUDIT annotated=9 ok=7 erratum-on-record=2 failures=2` | **OVER-REFUSAL** |
| 11 | `python3 corpus/instruments/r44-routed-defects.py --root .` | rc=1 admitted | rc=2 **refused** | value: `routed-defects total=8 fixed=5 unresolved=3 exit=1` | **OVER-REFUSAL** |
| 12 | `python3 corpus/instruments/frontier-recheck-count.py --selftest` | rc=0 admitted | rc=0 **admitted** | `shim=2` (2 `bash -c` runs), 6 fixture trees built+removed under `$HYAKU_SCRATCH` | **ADMITTED-EXEC** via a non-denied option |
| 13 | `python3 corpus/instruments/limb-mutation-check.py --selftest` | rc=0 admitted | rc=0 **admitted** | `shim=29`; source `limb-mutation-check.py:357` runs `[sys.executable,"-c",IMPORT_GATE,path]` | **ADMITTED-EXEC** |
| 14 | `python3 corpus/instruments/r46-landing-gate.py --selftest` | rc=0 admitted | rc=0 **admitted** | `shim=12`; builds git fixture lanes and commits inside them (`:301`, `:311`) | **ADMITTED-WRITE+EXEC** |
| 15 | `python3 corpus/instruments/kill-rule-check.py` (no args) | rc=0 admitted | rc=0 **admitted** | no on-disk receipt; source `:473-475` runs instruments with `--selftest --scratch` / `--root` | **ADMITTED-EXEC**, stage 2 |
| 16 | `python3 corpus/instruments/figure-audit.py --ledger <nested>` with inner `python3 corpus/instruments/frontier-recheck-count.py` | rc=1 admitted | rc=1 **admitted** | `marker.exec=1`, `shim=51` | **nested**: only stage 1 is validated |
| 17 | `python3 corpus/instruments/figure-audit.py --ledger <nested>` with inner `… --selftest` | rc=1 admitted | rc=1 **admitted** | `shim=2` | **nested**, same |
| 18 | `python3 corpus/instruments/capture-source.py --id x --url file://<src> --out <out>/p4.txt --kind text` | rc=1 **admitted**, created `p4.txt` 21 B | rc=2 **refused**, no file | outside file absent after the candidate run | P4 class **closed** (confirms the claim) |
| 19 | same with `--ur`/`--ou` (P6) | created `p6.txt` 21 B | refused, no file | | P6 class **closed** |
| 20 | same with `--url=… --out=…` (P5) | created `p5.txt` 21 B | refused, no file | | P5 class **closed** |
| 21 | `python3 corpus/instruments/wave-registry.py --results <r.json> --out <out>/wr.txt` | rc=0 `FIG ok`, created `wr.txt` 227 B | rc=2 **refused**, no file | `wave-registry.py:104` `open(args.out,"w")` | write class **closed** |
| 22 | `python3 corpus/instruments/limb-mutation-check.py --root . --ledger L` | rc=1 admitted | rc=2 refused | its `--root` copies the tree (`shutil`/`copytree`), so refusal is defensible | not an over-refusal |

Every base-admitted row measured with a tree signature (35/35 rows across the second, third and fourth
passes) left `root_delta_n=0` on the fixture tree (no write, edit or delete inside the root) — the only
writes in this table are the named outside files and transient scratch trees.

## Coverage of the assigned attack list

**(a) every denied long option and its argparse abbreviations — all refused by the candidate, all admitted
by the base** (base rc shown; `ref=0` = admitted):

| derive tail | base | cand |
|---|---|---|
| `--root .` / `--root=.` / `--ro .` / `--r .` / `--roo .` / `--ro= .` | rc=0, marker 1 | rc=2 refused |
| `'--root' .` / `"--root=."` / `--\root .` / `"--ro""ot" .` | rc=0, marker 1 | rc=2 refused |
| `--js ABS` (json) / `--scr ABS` (scratch) / `--wo ABS` (work) / `--o ABS` | rc=0 (2 marker) / rc=0 / rc=1 / rc=1 | rc=2 refused |
| `-o ABS` / `-oABS` / `-o ABS --root .` | rc=1 (argparse) | rc=2 refused |
| `--root . -- x` (denied before `--`) | rc=1 | rc=2 refused |
| `--roo` with no value | rc=1 | rc=2 refused |
| `--out`/`--ou`/`--out=`/`--url`/`--ur` on capture-source | wrote 21 B | rc=2 refused |

Quoted, `=`-joined, backslash-escaped and shlex-concatenated spellings all decode to the same token the gate
executes (`tokenize()` → `shlex.split(...)[0]`), so no spelling bypass exists. `--o` is not a unique
abbreviation (ambiguous `--out`/`--output`) and is refused conservatively; harmless.

**(b) flag after a positional** — `claim-package-check.py <package> --json` (row 3): refused. That is also
the cleanest over-refusal: `--json` there is a stdout flag.

**(c) short `-o`** — `-o`, `-oVALUE`, `-o VALUE` refused. **`-xo` is admitted** (D03) but inert: no
instrument declares a short option, argparse rejects it, `marker=0`, no file. Admitted-and-inert, not a defect.

**(d) `--` boundaries** — `python3 … -- --root .` admitted by both (D01), and the counter's argparse rejects
it (`rc=2` direct, gate `rc=1`), `marker=0`: the separator really disarms. A denied flag **before** `--` is
refused (row above). A second `--` (`ok.py -- -- --root`, D02) is admitted and re-derives `35`. Correct.

**(e) non-denied options that write or exec** — rows 12–15: `--selftest` (15 instruments declare it; every
one builds fixture trees, three execute programs) is not in `PY_DENIED_FLAGS`. `--results` on
`wave-registry.py` cannot write without `--out` (denied, row 21). `--keep`, `--jobs`, `--fixtures`,
`--ledger`, `--instrument`, `--lane`, `--manifest`, `--fake`, `--pure` are read/scratch options in the
instruments I read; none is a named write path in the rows measured. `r46-landing-gate --lane` is read-only
in the gate's own mode set (`--work` is denied; `--selftest` is row 14).

**(f) nested python** — rows 16–17: the outer gate validates only the first stage; the inner derive is
validated by the inner gate with the same rules, so nesting adds no *new* class — but `--selftest` in
`frontier-recheck-count.py` itself runs `[sys.executable, __file__, "--root", root]` (`:467`), i.e. a counter
hands `--root` to python after the gate has passed, and 12 instruments do the same
(`kill-rule-check.py:473-475`, `r44-frontier-count.py:247`, `capture-binding-check.py:1071`,
`r46-c1-gate.py:271,307,335`, …). The denial is a spelling filter on stage 1, not a property of the chain.

**(g) case/unicode/exactly-`--`-in-a-word** — `--Root` (D04), `--ｒoot` (U+FF52, D05) and `ok.py x--root`
(D06) are admitted and inert (argparse is case/byte sensitive; `x--root` is not an option token). No
instrument scans raw argv for a flag string (all 73 parse via `argparse`; the only `sys.argv` uses are
`main(sys.argv[1:])`), so `--`-disarming cannot be exploited by a counter's own parser.

**Read-only positive controls at the candidate** (both gates identical): `ok.py` → `35`;
`ok.py -- --root` → `35`; `cat … | head -n 1`; `grep -c S001 corpus/README.md` → `5`;
`git show HEAD:g.txt | head -n 1` → `35`; `git cat-file -t HEAD` → `commit`. Blanket refusal would fail
these, so the candidate is not a blanket refusal — it is a name-based filter.

## Why the predicate passes while the declared sentence fails

`PY_DENIED_FLAGS` (`figure-audit.py:122`) is a **global** name list applied to **every** counter
(`python_flags_ok`, `:364-388`). `--root` is the lane-root pointer of at least six read-only instruments and
`--json` is a stdout flag in one; both are denied by name. The frozen positive controls (8 derives) happen to
spell none of the seven denied names, so `measurements=12 failures=0` is a property of the control set, not
evidence for "every read-only derive admitted". The two refusals are not a tradeoff the Rust judge must
reject: a per-script list keeps all seven probes refused and restores all ten rows above.

The reverse direction is structural: `python_flags_ok` (`:374`) returns on the first `--`, skips tokens of
`len(name) <= 2`, and only inspects **options**. The exec primitive
(`frontier-recheck-count.py:269` `subprocess.run(["bash","-c",recheck], cwd=root)`) needs no option: the
default `root` (`:494`) is the counter's own directory, so the no-argument derive is the P1 payload with the
denial bypassed (row 1). The frozen scope concedes "the class of exec/write paths not named here stay open",
but it names positionals, `--` operands and non-denied options — **not** "no option at all", and that is the
cheapest exploit in the lane.

## Smallest safe correction

1. Per-script denial instead of a global list (keeps P1–P7 refused, restores rows 2–11):
   `PY_DENIED = {"frontier-recheck-count.py": ("--root","--json","--scratch","--selftest"),
   "capture-source.py": ("--url","--out","--selftest"), "wave-registry.py": ("--out",)}` plus
   `PY_DENIED_ANY = ("--out","--output")` for the path-writing names.
2. Add `--selftest` to the any-counter denial: it is a fixture-writing, program-running option in 15
   instruments and is not a derive.
3. Either refuse `frontier-recheck-count.py` as a python head outright (its `entries=51 pass=51` *is* 51
   committed shell payloads executed through `bash -c`, so it is not a read-only derive at all) or add the
   no-argument spelling to the frozen scope text and the lesson.
4. If (1) is not landed, change the declared sentence to "…while keeping every read-only derive that spells
   no denied name admitted". As frozen, the sentence is measurably false.

## Not measured / residual

- `census-freshness-check.py .` was admitted by both (positional root, no denial) and is read-only in my
  snapshot; its direct run took 320 s, so I did not repeat it under both gates.
- `capture-source.py --selftest`, `capture-binding-check.py --selftest`, `citation-ground-check.py --selftest`
  are admitted at rc=0 with no on-disk receipt (their scratch is removed inside the run).
- Network egress through `--url` (`capture-source.py:75` `urlopen`) was not exercised; the write is closed at
  the option, the egress is closed only because `--url` is denied.
- `limb-mutation-check.py --root . --ledger L` writes by copying the tree; the candidate's refusal is
  defensible and is not counted as an over-refusal.
