# ExecLimbFRmissingentry — falsify ledger limb `FR-missing-entry` (round 31, wave 2)

Seat: ExecLimbFRmissingentry (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`, wave-1 landing HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`).

Files written: this receipt only. Every probe ran in a `mktemp -d` scratch copy of the lane `corpus/`;
all four scratch dirs were deleted at the end. No git/jj mutation (read-only `git rev-parse`,
`git status`), no delegation, no labrat used, no background job, no network fetch, no tool
install/upgrade (nothing needed; pacman not invoked). Answering model actually run on:
`opencode-go/deepseek-v4.1-flash` (harness route table; no model passed by this seat).

Measured bytes (identical at seat start and seat end; lane `corpus/` clean in `git status`):

```
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
$ sha256sum corpus/instruments/frontier-recheck-count.py corpus/instruments/limb-ledger.json \
            corpus/instruments/limb-mutation-check.py \
            corpus/instruments/limb-fixtures/fr/fr-missing-entry/corpus/README.md
aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893  corpus/instruments/frontier-recheck-count.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
9376e3316b0f61d1b37d5d049a926cf24443f838effa10db715b550bd05f1542  corpus/instruments/limb-fixtures/fr/fr-missing-entry/corpus/README.md
$ git status --porcelain corpus/ | wc -l
0
```

No PRE-STATE label: wave 1 is landed and quiescent, and the three hashes above did not move across
this seat. The landed `FR-` rows are byte-identical to the wave-1 fragment:

```
$ python3 -c "import json; f=json.load(open('.ufo/waves/round-31/wave1/ledger-fragments/fr.json')); \
l=json.load(open('corpus/instruments/limb-ledger.json')); \
print('identical', f['limbs']==[r for r in l['limbs'] if r['id'].startswith('FR-')])"
identical True
```

## 0. The row under test (`corpus/instruments/limb-ledger.json:115-122`, verbatim)

```json
{
  "id": "FR-missing-entry",
  "instrument": "corpus/instruments/frontier-recheck-count.py",
  "find": "    if not os.path.isfile(full):\n        return None\n",
  "replace": "",
  "kill": "python3 {inst} --root {root}/corpus/instruments/limb-fixtures/fr/fr-missing-entry",
  "live_exit": 1,
  "signal": "FAIL\\s+F98\\s+knowledge/zz-missing\\.md\\s+ids=-\\s+exit=-\\s+problems=missing-entry\\nentries=1 pass=0 exit=1\\n?",
  "note": "Drops the fail-closed missing-entry guard in entry_contract (E): … Measured r31: live 1/sig-y, mutant 1/sig-n."
}
```

`find` targets `corpus/instruments/frontier-recheck-count.py:78-79` — the second path resolution's
fail-closed `return None`. The first `if not os.path.isfile(full):` (`:75`) and the one in `evaluate`
(`:133`) are followed by a re-join, not `return None`, so the find text is unique:

```
$ python3 - <<'PY'
import json
inst=open('corpus/instruments/frontier-recheck-count.py',encoding='utf-8').read()
row=[r for r in json.load(open('corpus/instruments/limb-ledger.json'))['limbs'] if r['id']=='FR-missing-entry'][0]
print('find_count=%d' % inst.count(row['find'])); assert inst.count(row['find'])==1
PY
find_count=1
```

Instrument site before/after (`:74-80`), living run:

```
    full = os.path.join(root, entry_path)
    if not os.path.isfile(full):
        # README rows name entries relative to corpus/ (`knowledge/...`).
        full = os.path.join(root, "corpus", entry_path)
    if not os.path.isfile(full):
        return None
```

Fixture (`corpus/instruments/limb-fixtures/fr/fr-missing-entry/corpus/README.md`): exactly one admitted
row — `| F98 | ghost row naming an absent entry | admitted | knowledge/zz-missing.md | S099 | n/a |`
— and no `knowledge/` directory, so `missing-entry` is the only reachable problem class.

## 1. The counter's own line (lane run; the counter is scratch-only)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && \
  time python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json
...
LIMB FR-missing-entry live=1/y mutant=1/n verdict=killed
...
limbs=13 killed=13 survivors=0
controls=3 rejected=3

real    0m21.147s
counter_exit=0
```

(The full 13-line block and all three `CONTROL` lines were printed; the C1 aggregate is
`limbs=13 killed=13 survivors=0` / `controls=3 rejected=3`, exit 0 — quoted here only as context for
this seat's single row.) Counter cleanliness: no `/tmp/limb-mutation-*` directory survived the run,
and the lane `corpus/` stayed `git status`-clean; `corpus/instruments/__pycache__/frontier-recheck-count.cpython-314.pyc`
still carries its pre-seat mtime `15:52` (no bytecode written by this seat's runs).

## 2. Hand re-derivation of `FR-missing-entry` on a scratch lane

Script (saved at `/tmp/fr_missing_hand.sh`, deleted after the run) — `S=$(mktemp -d)`, `cp -a` the lane
`corpus/` into `$S/corpus`, `ROOT=$S`, `INST=$S/corpus/instruments/frontier-recheck-count.py`,
`FIX=$ROOT/corpus/instruments/limb-fixtures/fr/fr-missing-entry`, kill command run as
`cd "$ROOT" && python3 "$INST" --root "$FIX"` (identical `{inst}`/`{root}` substitution and cwd to the
counter's `run_kill`).

```
SCRATCH=/tmp/fr-missing.V0iKBH
=== LIVE BASELINE: unmutated, kill command run twice ===
live_run1 exit=1
--- live_run1 output ---
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
live_run2 exit=1
--- live_run2 output ---
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
live_runs_identical=y
live_signal_match=y
live_signal_matched_text='FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry\nentries=1 pass=0 exit=1\n'
=== APPLY find/replace (python, exactly-once asserted) ===
orig_bytes=9416 mutated_bytes=9363 delta=-53
=== py_compile ===
py_compile_exit=0
=== MUTANT: kill command run twice ===
mutant_run1 exit=1
--- mutant_run1 output ---
Traceback (most recent call last):
  File "/tmp/fr-missing.V0iKBH/corpus/instruments/frontier-recheck-count.py", line 226, in <module>
    sys.exit(main())
  File ".../frontier-recheck-count.py", line 191, in main
    record = evaluate(root, entry)
  File ".../frontier-recheck-count.py", line 116, in evaluate
    contract = entry_contract(root, entry_path)
  File ".../frontier-recheck-count.py", line 79, in entry_contract
    with open(full, encoding="utf-8") as fh:
FileNotFoundError: [Errno 2] No such file or directory: '/tmp/fr-missing.V0iKBH/corpus/instruments/limb-fixtures/fr/fr-missing-entry/corpus/knowledge/zz-missing.md'
mutant_run2 exit=1
mutant_runs_identical=y
mutant_signal_match=n
mutant_signal_matched_text=None
```

(The `File ".../` lines are elided above for width only; the run printed the full absolute paths.)

Hand result vs counter line:

| quantity | hand (scratch, unmutated then patched) | counter `LIMB FR-missing-entry …` | agree |
|---|---|---|---|
| find count | 1 | accepted (no `invalid:find-count`) | yes |
| `py_compile` of mutant | exit 0 | accepted (no `invalid:nocompile`) | yes |
| live exit | 1 | `live=1` | yes |
| live signal match | y | `live=1/y` | yes |
| mutant exit | 1 | `mutant=1` | yes |
| mutant signal match | n | `mutant=1/n` | yes |
| verdict | killed (signal loss) | `verdict=killed` | yes |

**No difference.** The counter's arithmetic for this row reproduces by hand.

## 3. Isolation — the literal clause fails on the landed fixture

The item's clause 3 asks that the mutant still print "the instrument's normal banner/other cases", so
that the kill is not an unrelated crash. On the landed fixture the mutant's entire output is the
traceback above: there is no per-row line and no `entries=` summary, because the missing-entry fixture
admits exactly one row and the crash happens inside that row's `evaluate`. So this row is killed by
**signal only** (`live=1`, `mutant=1` — the exit codes are identical) and the mutant's distinguishing
output *is* a crash. The landed `note` states this openly, and `R51W2`-era wave-1 review
(`.ufo/waves/round-31/wave1/CritC1Kill.md:346-347`) already reads it the same way: "exactly one landed
row carries a traceback, `FR-missing-entry`, where the crash *is* the limb".

That reading is defensible — instrument contract E says the failure "never [is] an uncaught
FileNotFoundError traceback" — but it means the evidence does not satisfy clause 3 as written.

### 3a. The fixture is nonetheless limb-specific (so it is not an arbitrary crash)

Both cross-limb probes, done on the same scratch lane, show each FR fixture kills only its own limb:

```
=== A: FR-duplicate mutant under the MISSING-ENTRY kill command (fixture fr-missing-entry) ===
live_exit=1                       (unmutated: FAIL F98 … problems=missing-entry / entries=1 pass=0 exit=1)
patched FR-duplicate-entry find, count=1
py_compile_exit=0
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=1 pass=0 exit=1
mutant_exit=1
=== diff live vs FR-duplicate mutant (empty => survivor) ===
IDENTICAL => FR-duplicate mutant SURVIVES the missing-entry kill command

=== B: FR-missing mutant under the DUPLICATE-ENTRY kill command (fixture fr-duplicate-entry) ===
live_dup_exit=1
PASS     F98  knowledge/dup-entry.md                               ids=S003           exit=0
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
DUPLICATE-ENTRY F98,F97 knowledge/dup-entry.md
entries=2 pass=2 exit=1
patched FR-missing-entry find, count=1
py_compile_exit=0
mutant_on_dup_fixture_exit=1       (mutant output byte-identical to the live block above)
=== diff live vs missing-entry-mutant on the duplicate fixture ===
BYTE-IDENTICAL => survivor (duplicate fixture does not exercise the E limb)
```

So each FR fixture kills only its own limb: the duplicate-limb mutant survives the missing-entry kill
command and the missing-entry mutant survives the duplicate kill command (both byte-identical, exit
unchanged). The missing-entry fixture therefore exercises the E limb and nothing else, and the kill is
not a side effect of some other limb's case.

### 3b. Demonstrated strengthening (fixture gains a preceding passing row)

A one-row fixture cannot satisfy clause 3; a two-row fixture can, and the improvement is measurable.
Probe: copy the duplicate fixture to `fr-missing-plus-pass`, keep its valid `F97 → knowledge/dup-entry.md`
row, then append the ghost row, and run the *ledgered* mutant:

```
--- probe LIVE (pristine instrument) ---
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
entries=2 pass=1 exit=1
probe_live_exit=1
--- probe MUTANT (ledger FR-missing-entry find/replace) ---
PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
Traceback (most recent call last):
  ...
FileNotFoundError: [Errno 2] No such file or directory: '.../fr-missing-plus-pass/corpus/knowledge/zz-missing.md'
probe_mutant_exit=1
--- probe diff (live vs mutant) ---
 PASS     F97  knowledge/dup-entry.md                               ids=S003           exit=0
-FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=missing-entry
-entries=2 pass=1 exit=1
+Traceback (most recent call last): …
```

The mutant now keeps the instrument's normal per-row output (the `PASS F97` line prints before the
crash) and loses exactly the two diagnostic lines — a differential that survives clause 3. A signal of
the form `PASS\s+F97\s+knowledge/dup-entry\.md\s+ids=S003\s+exit=0[ \t]*\nFAIL\s+F98\s+…\nentries=2 pass=1 exit=1`
matches that live output and not the mutant. **Not applied**: the ledger and the counter are
single-writer to `ExecCounterFix` and the fixture tree is outside this seat's write scope, so this is
routed to the L1 rather than done here.

## 4. Discrimination — three independent one-limb mutants of the same limb

Each mutant is a single exact-once patch of the same instrument (find count asserted `1`), passing
`py_compile`, run with the ledgered kill command against the landed `fr-missing-entry` fixture:

| # | site (patch) | patch shape | live | mutant exit | mutant signal | killed? |
|---|---|---|---|---|---|---|
| landed | `:78-79` guard → `` (deleted) | crash, signal-loss | 1/y | 1 | n | killed |
| M2a | `:128-129` `"problems": ["missing-entry"], "status": "FAIL"` → `[], "PASS"` | **no crash**, exit + signal | 1/y | 0 | n | killed (exit and signal) |
| M2b | `:78-79` guard → `full = os.devnull` | **no crash**, signal-loss | 1/y | 1 | n | killed (signal only) |
| M2c | `:78-79` guard inverted to `if os.path.isfile(full):` | crash, signal-loss | 1/y | 1 | n | killed (signal only) |

M2a (different code site, `evaluate`'s None branch) output:

```
PASS     F98  knowledge/zz-missing.md                              ids=-              exit=-
entries=1 pass=1 exit=0
M2a exit=0   M2a signal_match=n
```

M2b (no crash — the fallback parses `/dev/null` as an empty entry body):

```
FAIL     F98  knowledge/zz-missing.md                              ids=-              exit=-    problems=no-source-line,no-recheck-line,no-source-selection,no-manifest
entries=1 pass=0 exit=1
M2b exit=1   M2b signal_match=n
```

(Trailing alignment spaces at the end of the per-row lines are trimmed in the quotes above; the run
prints them. The landed `FR-missing-entry` signal absorbs that padding with `\s+` between fields, the
`FR-duplicate-entry` signal with explicit `[ \t]*` at each line end.)

M2c (guard inverted; the absent path then falls through to `open`):

```
Traceback (most recent call last): … FileNotFoundError: [Errno 2] No such file or directory: '…/corpus/knowledge/zz-missing.md'
M2c exit=1   M2c signal_match=n
```

So the instrument's cases are **not** tuned to one mutant shape: the fixture kills the crash shape, a
non-crashing silent-fallback shape, and a mislabelled-diagnostic shape. What is shape-specific is only
the *nature of the observable* for the landed row (crash vs. nothing), not which rewrite of the guard
survives.

## 5. Verdict — `weak`

| clause | result |
|---|---|
| 1. hand re-derivation equals the counter's line | **pass** — exact agreement on find count, compile, live 1/y, mutant 1/n, verdict (no defect) |
| 2. a second, different mutant is killed | **pass** — 3 of 3 alternative one-limb mutants killed, two of them without any crash |
| 3. the mutant is killed by a limb-specific case, not an unrelated crash; it still prints normal output | **fail as written** — the mutant prints a bare `FileNotFoundError` traceback and none of the harness's per-row output; the kill is signal-only (`live=1`, `mutant=1`) |

`weak`, not `defect`: the counter and hand disagree on nothing, the row's `note` discloses the crash
honestly, the fixture is provably limb-specific (§3a), and under the frozen C1 predicate — killed when
`exit != live_exit` **or** the signal no longer matches — `verdict=killed` is correct. The weakness is
evidential, not arithmetic: the row's entire discrimination rests on one regex, and a reader cannot see
"the harness still ran" in the mutant output.

Routed (L1 to decide; both files are single-writer to `ExecCounterFix` and the fixture tree is not a
wave-2 write path):

1. Preferred: give `fr-missing-entry` a preceding passing row (§3b), re-signal to
   `PASS F97 … / FAIL F98 … problems=missing-entry / entries=2 pass=1 exit=1`. Cost: one fixture README
   plus one ledger field; it makes clause 3 hold without touching the instrument.
2. Alternative: keep the row and add M2a (the `evaluate` None-branch relabel, `:128-129`) as an
   additional `FR-…` limb — it is killed by exit *and* signal with no crash, so the pair covers both
   observables. This changes the frozen 13-limb count, so it is the L1's call, not this seat's.
3. Do **not** add a traceback-based rule to the counter: the crash is the documented limb here, and
   wave-1 review (`CritC1Kill.md:465-466`) reached the same conclusion for a different reason.

## 6. Reproducibility and non-findings

Everything above is reproducible with the frozen ledger alone:

```
S=$(mktemp -d); cp -a corpus "$S/corpus"; ROOT=$S
INST=$S/corpus/instruments/frontier-recheck-count.py
FIX=$ROOT/corpus/instruments/limb-fixtures/fr/fr-missing-entry
cd "$ROOT" && python3 "$INST" --root "$FIX"; echo "live_exit=$?"          # 1, FAIL F98 … problems=missing-entry
python3 - "$INST" corpus/instruments/limb-ledger.json <<'PY'
import json,sys
o=open(sys.argv[1],encoding="utf-8").read()
r=[x for x in json.load(open(sys.argv[2]))["limbs"] if x["id"]=="FR-missing-entry"][0]
assert o.count(r["find"])==1
open(sys.argv[1],"w",encoding="utf-8").write(o.replace(r["find"],r["replace"],1))
PY
python3 -m py_compile "$INST" && cd "$ROOT" && python3 "$INST" --root "$FIX"; echo "mutant_exit=$?"   # 1, traceback
```

Cleanup proof:

```
$ rm -rf /tmp/fr-missing.V0iKBH /tmp/fr-disc.27x01I /tmp/fr-cross.JDXLdc /tmp/fr-crossA.LslD5m /tmp/fr_missing_hand.sh /tmp/fr_disc.sh
$ ls -d /tmp/fr-* /tmp/fr_* 2>&1 | head -5
ls: cannot access '/tmp/fr_*': No such file or directory
/tmp/fr-audit.json
/tmp/fr-prefixture.json
```

(`/tmp/fr-audit.json` and `/tmp/fr-prefixture.json` are other seats' files, untouched; no
`/tmp/limb-mutation-*` remained after the counter run.)

Non-findings recorded so they are not re-opened: the ledger row is byte-identical to the wave-1
fragment (no landing drift); the counter's `{inst}`/`{root}` substitution and cwd match this seat's
hand run; the counter leaves the lane and `/tmp` clean; the fixture's `S099` source cell is inert (the
harness never reads the `sources` column); and no state material, credential or network contact was
involved.
