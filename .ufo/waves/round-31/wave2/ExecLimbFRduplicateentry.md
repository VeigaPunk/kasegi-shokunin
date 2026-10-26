# ExecLimbFRduplicateentry — round 31 wave 2 receipt

Seat: `ExecLimbFRduplicateentry` (leaf executor). Target: falsify ledger limb
`FR-duplicate-entry` of the C1 ledger on the **landed** bytes.
Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, base `b374febbb33ccadade78a787279707fd5d2e6e1d`,
claims-freeze `738a77999a00efbca129cfccb28a481037f6241f`, read-only HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`. Python 3.14.8 (CPython), 2026-10-26T00:2xZ.
Answering model: `opencode-go/deepseek-v4.1-flash` (runtime route banner; no model
passed by this seat). Tool installs: **none** (stdlib only; no pacman transaction run).
Writes: this receipt only. All attack work in `mktemp`/`/tmp/frduphand-*` scratch copies.

**Verdict: `holds`.** Hand re-derivation reproduces the counter's line field for
field; four further distinct single-site mutant shapes are killed; one
behaviour-preserving refactor survives (no false kill); the kill is produced by
the duplicate case's own output lines, not by a crash.

## 0. Landed bytes pinned (read-only)

```
$ sha256sum corpus/instruments/frontier-recheck-count.py corpus/instruments/limb-ledger.json corpus/instruments/limb-mutation-check.py
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
```

`frontier-recheck-count.py` = 9418 bytes / 9416 chars / 1 non-ASCII char (`U+2014`
at char 647). Ledger row `FR-duplicate-entry` (`corpus/instruments/limb-ledger.json`)
is identical to the wave-1 fragment (`find`, `replace`, `signal`, `kill` all
`identical` under a field-by-field compare) — merge did not perturb this row.

Row under test (verbatim fields): `instrument` = `corpus/instruments/frontier-recheck-count.py`;
`find` = the `seen_realpath` / `DUPLICATE-ENTRY` / `fail_closed` block (494 chars);
`replace` = `    fail_closed = not records or passed != len(records)\n`;
`kill` = `python3 {inst} --root {root}/corpus/instruments/limb-fixtures/fr/fr-duplicate-entry`;
`live_exit` = 1; `signal` = the two `PASS` rows + `DUPLICATE-ENTRY F98,F97` + `entries=2 pass=2 exit=1`.

## 1. Hand re-derivation (independent of the counter)

Scratch lane = fresh `tempfile.mkdtemp` copy of the whole lane `corpus/` (pycache
excluded). Kill command expanded exactly as the counter expands it (`{inst}` and
`{root}` = scratch paths), `bash -c`, cwd = scratch root, `PYTHONDONTWRITEBYTECODE=1`.
Script: `/tmp/frduphand-1/hand.py` (re-implements the contract; imports nothing
from `limb-mutation-check.py`).

```
$ python3 /tmp/frduphand-1/hand.py
row id          : FR-duplicate-entry
instrument      : corpus/instruments/frontier-recheck-count.py
original sha256 : aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893 bytes 9418

expanded kill   : python3 /tmp/frdup-hand-fexs8km_/corpus/instruments/frontier-recheck-count.py --root /tmp/frdup-hand-fexs8km_/corpus/instruments/limb-fixtures/fr/fr-duplicate-entry
live_exit       : 1 (ledger live_exit: 1 )
live signal     : True
live stdout+stderr:
   |PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
   |PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
   |DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
   |entries=2 pass=2 exit=1
   |

find count      : 1
noop?           : False
mutant sha256   : 5028f09e2ee8cb9d46c615adc15c2b4f8d5c8fce96b0f31ddbcbaf45d287a7bb bytes 8980
py_compile      : True
mutant_exit     : 0
mutant signal   : False
mutant stdout+stderr:
   |PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
   |PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
   |entries=2 pass=2 exit=0
   |

hand verdict    : killed
```

Literal `python3 -m py_compile` on the saved mutant (item's exact step):

```
$ python3 -c '... assert src.count(find)==1; write mutant.py'   # find_count=1, mutant_chars 8978
$ python3 -m py_compile /tmp/frduphand-1/mutant.py; echo $?
0
$ sha256sum /tmp/frduphand-1/mutant.py
5028f09e2ee8cb9d46c615adc15c2b4f8d5c8fce96b0f31ddbcbaf45d287a7bb  /tmp/frduphand-1/mutant.py
```

Counter line for the same row, from the landed counter on the landed ledger
(run in the lane; the counter itself is scratch-only):

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
LIMB RA-parse live=0/y mutant=1/n verdict=killed
... (11 further lines) ...
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
CONTROL CTL-noop verdict=invalid:noop expected=invalid:noop ok=y
CONTROL CTL-nocompile verdict=invalid:nocompile expected=invalid:nocompile ok=y
CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y
limbs=13 killed=13 survivors=0
controls=3 rejected=3
counter_exit=0
```

Determinism (second invocation, FR rows only, `/tmp/ledger-fr-only.json` = the two
`FR-*` rows copied out of the landed ledger, `controls: []`):

```
$ python3 corpus/instruments/limb-mutation-check.py --ledger /tmp/ledger-fr-only.json
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
LIMB FR-duplicate-entry live=1/y mutant=0/n verdict=killed
limbs=2 killed=2 survivors=0
controls=0 rejected=0
fr_only_exit=0
```

| field | hand | counter | agree |
|---|---|---|---|
| live exit / signal | `1` / `y` | `1` / `y` | yes |
| mutant exit / signal | `0` / `n` | `0` / `n` | yes |
| verdict | `killed` | `killed` | yes |
| find count / noop / compile | 1 / False / True | 1 / False / True | yes |
| mutant sha256 | `5028f09e…` | (same bytes under test) | yes |

No difference between the hand result and the counter's line → **no defect**.
Note the hand replay deliberately re-uses ONE scratch (live, then mutate in place,
then mutant run — the contract's literal order), while the counter runs each side
on its own fresh scratch; both give the identical verdict, so the row has no
cross-side state dependence (the kill command writes nothing).

## 2. Discrimination — a SECOND, different one-site mutant

Script `/tmp/frduphand-1/alts.py`: each mutant is applied alone to a fresh scratch
copy, `py_compile`d, then run through the row's own kill command.

```
$ python3 /tmp/frduphand-1/alts.py
M2a-key-confusion  find-count=1
  site: '        rp = record.get("realpath")\n'
  compiles=True mutant_exit=0 signal_matches=False -> killed
    |PASS     F98 ... |PASS     F97 ... |entries=2 pass=2 exit=0
M2b-detection-off  find-count=1
  site: '        if rp in seen_realpath:\n'  ->  '        if False:\n'
  compiles=True mutant_exit=0 signal_matches=False -> killed
    |PASS     F98 ... |PASS     F97 ... |entries=2 pass=2 exit=0
M2c-report-inversion  find-count=1
  site: '            duplicate = (seen_realpath[rp], record["frontier"], record["entry"])\n'
  compiles=True mutant_exit=1 signal_matches=False -> killed
    |PASS     F98 ... |PASS     F97 ... |DUPLICATE-ENTRY F97,F98 knowledge/dup-entry.md |entries=2 pass=2 exit=1
M2d-report-dropped  find-count=1
  site: '        print("DUPLICATE-ENTRY %s,%s %s" % (duplicate[0], duplicate[1], duplicate[2]))\n' -> '        pass\n'
  compiles=True mutant_exit=1 signal_matches=False -> killed
    |PASS     F98 ... |PASS     F97 ... |entries=2 pass=2 exit=1
M2e-equivalent-test  find-count=1
  site: '    if duplicate:\n'  ->  '    if duplicate is not None:\n'
  compiles=True mutant_exit=1 signal_matches=True -> survivor
    |PASS     F98 ... |PASS     F97 ... |DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md |entries=2 pass=2 exit=1
```

(`...` elides the unchanged `PASS` lines; full transcript lines are byte-identical
to section 1's.)

Reading:

- **Not shape-specific.** Four structurally different single-site mutants of the
  same limb are all killed: (i) keying the map by `frontier` instead of entry
  `realpath`, (ii) disabling only the duplicate test while leaving the print and
  `fail_closed` wiring, (iii) inverting the reported pair, (iv) dropping only the
  `DUPLICATE-ENTRY` note. The instrument's case therefore kills the *limb*, not a
  spelling of it.
- **Two kill channels, both exercised.** M2a/M2b flip exit 1→0 *and* lose the
  signal; M2c/M2d keep exit 1 and are killed **by signal only** — so the signal is
  load-bearing independently of the exit code, and the row's `signal` genuinely
  discriminates report shape.
- **No rubber stamp.** M2e (a behaviour-preserving refactor of the same test) is
  correctly a `survivor`, so the kill does not fire on arbitrary edits near the limb.
- The frozen mutant is not behaviour-equivalent anywhere either: under `--json` it
  silently writes `"duplicate_entry": null` for a duplicate-bearing root (measured,
  live `"knowledge/dup-entry.md"`), a second observable the kill command does not
  exercise (see risk 2).

## 3. Isolation — killed by this limb's own case, not a crash

`difflib` diff of the frozen mutant against live, same fixture, fresh scratches:

```
--- live
+++ mutant
@@ -1,5 +1,4 @@
 PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0   
 PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0   
-DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
-entries=2 pass=2 exit=1
+entries=2 pass=2 exit=0
```

Exactly **two** lines differ. The mutant still prints the harness' normal per-row
lines (`PASS F98`, `PASS F97` — i.e. both admitted rows still pass their own A–D
contract, including the real `source-recheck.py` invocation) and its normal summary
line; stderr is empty and contains no `Traceback` on either side. The kill is the
disappeared `DUPLICATE-ENTRY` line plus the `exit=` field flip inside the summary —
not an unrelated crash (contrast `FR-missing-entry`, whose mutant still exits 1 via
an uncaught `FileNotFoundError` and is killed by signal alone).

Cross-root isolation (same frozen mutant, fresh scratch lane per side):

```
fr-duplicate-entry fixture      live exit=1  stdout_sha16=c07ae86ed5666891
                                mutant exit=0 stdout_sha16=8bf008cb7d197052  differ
fr-missing-entry fixture        live exit=1  stdout_sha16=4e8e44d3f4cfd5c9
                                mutant exit=1 stdout_sha16=4e8e44d3f4cfd5c9  IDENTICAL
whole scratch lane corpus/      live exit=0  stdout_sha16=fe8170ec16e6c349  (entries=18 pass=18)
                                mutant exit=0 stdout_sha16=fe8170ec16e6c349  IDENTICAL
```

The mutant is invisible on the other FR fixture and on the real 18-row corpus
(18/18 PASS, exit 0 — matches C2's after-state), and changes only the
duplicate-bearing root. Each side ran in its own scratch copy; no `--json` file, no
pycache residue left in the lane.

## Risks / notes (advisory; no fix attempted — lane is read-only for this seat)

1. **Signal couples to column padding.** The row's `signal` encodes the harness'
   `%-13s`/`%-4s` spacing (tolerated via `\s+` / `[ \t]*`). A print-format change
   makes the row `invalid:live-baseline` (fail-closed) rather than silently passing,
   but any format edit must re-measure both FR rows.
2. **Kill covers stdout + exit only.** The frozen mutant also changes the `--json`
   receipt (`duplicate_entry: null`, measured in a scratch root). That second
   observable is not part of the kill, so a future mutant that keeps stdout and the
   exit identical but corrupts only the receipt would survive this row. Out of the
   frozen 13-limb contract; reported, not widened.
3. **Wave-1 receipt unit nit (evidence only, not a lane defect).**
   `.ufo/waves/round-31/wave1/ExecFRLimbs.md` labels mutant `5028f09e…` as
   `bytes 8978`; the same digest measured here is 8978 *chars* / 8980 UTF-8 *bytes*
   (one `U+2014` in the source). Identical digest ⇒ identical bytes; the ledger and
   fixtures are unaffected.
4. **Concurrent-lane churn observed, not caused here.** `corpus/instruments/__pycache__/`
   is gitignored and its members' mtimes move while sibling seats run instruments in
   the lane (e.g. `source-recheck.cpython-314.pyc` at 21:24:15 -0300, header
   mtime/size = the current lane source, so a live import, not a mutant).
   `git status --porcelain -- corpus/instruments` is clean; every run of this seat
   was scratch-only (`/tmp/frduphand-*`, `/tmp/ledger-fr-only.json`), and the
   counter leaves no `limb-mutation-*` scratch behind (one transient directory seen
   during a sibling's concurrent invocation was gone on the next check).
5. **No blockers**, no peer receipt waited on, no message sent to `agent://all`.
