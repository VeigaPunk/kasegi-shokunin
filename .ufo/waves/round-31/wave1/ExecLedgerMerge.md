# ExecLedgerMerge — round 31, C1 one-limb mutation ledger (merge seat)

- **Seat:** `ExecLedgerMerge` (role: `executor`, leaf — no subagent dispatch, no background jobs)
- **Round/milestone:** kasegi-shokunin round 31, hyaku run 7, wave 1
- **Answering model:** devin/deepseek-v4-1-flash (route-table default; no model was passed by this seat)
- **Lane:** `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (only write scope)
- **Lane base:** `b374febbb33ccadade78a787279707fd5d2e6e1d`; claims-freeze commit `738a77999a00efbca129cfccb28a481037f6241f`; HEAD at run time `8a8916c7043bd873d191b30dd1744b241b91f4d9`
- **Written by this seat:** `corpus/instruments/limb-ledger.json` and this receipt only.

## 1. What the ledger is

`corpus/instruments/limb-ledger.json` is the C1 one-limb mutation ledger: the 13 named limbs of the
three recheck-family instruments (RA x9, SR x2, FR x2) in the frozen order, plus exactly 3 controls.
Rows are copied **verbatim** from the three owner fragments (no `find`/`replace`/`signal` was retyped);
the merge only concatenates and orders them, then adds the controls.

Fragment inputs (read, not edited):

| fragment | sha256 | rows taken |
|---|---|---|
| `.ufo/waves/round-31/wave1/ledger-fragments/ra.json` | `266cb024dafbba3c5cb780bebe9f45c7e8d1b7193abde032acf09b111cfb93ce` | 9 (`RA-*`) |
| `.ufo/waves/round-31/wave1/ledger-fragments/sr.json` | `4f7dc1e317d78a0f48814ec939cda4ee71a743e4f85c1932fa830334496d3e00` | 2 (`SR-*`) |
| `.ufo/waves/round-31/wave1/ledger-fragments/fr.json` | `ebda80f6a7c37138d37fe6c39045a97d5609efc08f15acfa10691ab7643cfc1b` | 2 (`FR-*`) |

Order assertion enforced at merge time: `[r['id'] for r in ra]` equals the 9 frozen RA ids in contract
order; `sr` is exactly `SR-stem-mismatch, SR-occurrence-not-unique`; `fr` is exactly `FR-missing-entry,
FR-duplicate-entry`. All 16 `find` texts were re-counted on the landed instrument bytes at merge time:
each occurs **exactly once**.

| artefact | sha256 |
|---|---|
| `corpus/instruments/limb-ledger.json` | `c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be` |
| `corpus/instruments/limb-mutation-check.py` (ExecCounter, FINAL) | `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` |
| `corpus/instruments/recheck-audit.py` (owner-landed bytes) | `5d4842da6103f17c7798ca2078a77288820bd8b90432348cd2cc012e1faf7f09` |
| `corpus/instruments/source-recheck.py` (owner-landed bytes) | `fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003` |
| `corpus/instruments/frontier-recheck-count.py` (owner-landed bytes) | `aa60b58126569a1c8ec04409011df5f6225a9c18f2a77ea6410cd1d0d5dc0893` |

## 2. Counter run on the landed bytes (twice, quiescent)

Command, run twice with the counter digest captured before and after both runs:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
```

Output (identical for both runs; `stderr` empty for both):

```text
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
```

| measurement | value |
|---|---|
| run 1 exit | `0` |
| run 2 exit | `0` |
| stdout+stderr byte-identical across the two runs | `true` |
| sha256 of the printed stdout (both runs) | `9b3864854a22644fda6ac6f3d8b34a56d8e9dec0173da75138662c8fb64ff838` |
| counter sha256 before / after the pair | `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` / `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f` (quiescent: `true`) |
| wall time for the pair | `29.3 s` |

Required lines are present byte-exactly: `limbs=13 killed=13 survivors=0`, `controls=3 rejected=3`,
13 lines beginning `LIMB `, and every LIMB line shows `live` != `mutant` in exit, signal, or both.

## 3. Ledger JSON validity

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 -c 'import json;d=json.load(open("corpus/instruments/limb-ledger.json"));print("version=%r limbs=%d controls=%d" % (d["version"], len(d["limbs"]), len(d["controls"])))'
```

Output (exit `0`):

```text
version=1 limbs=13 controls=3
```

## 4. Counter self-test at the merged digest (its own verdict paths)

```sh
python3 corpus/instruments/limb-mutation-check.py --selftest | tail -3; echo "counter_selftest_exit=$?"
```

```text
selftest aggregate-survivor    ok
selftest control-verdict-rule  ok
selftest cases=20 failures=0
counter_selftest_exit=0
```

## 5. No-harm on the real corpus (C1's regression clause)

Run from the lane root on the same quiescent bytes; these are the three instruments the ledger judges:

```sh
python3 corpus/instruments/recheck-audit.py --quiet; echo "audit_exit=$?"
```
```text
strict pass=44/44 cdroot_fail=0 instrument_fail=0 own_fail=0
executes=20 gated=24 broken=0  (gated = the line runs and fails closed on an absent base; broken = it cannot run at all)
lines=44 total=44 pass=44 fail-closed=24 parse_fail=0 cwd_fail=0 paths_fail=0 exit=0
expect=present expected=44 missing=0 unexpected=0 exit=0
audit_exit=0
```

```sh
python3 corpus/instruments/source-recheck.py --selftest | tail -1; echo "sr_selftest_exit=$?"
```
```text
selftest cases=10 failures=0
sr_selftest_exit=0
```

```sh
python3 corpus/instruments/frontier-recheck-count.py | tail -2; echo "harness_exit=$?"
```
```text
PASS     F15  knowledge/vendor-third-party-finding-coordination.md ids=S048           exit=0   
entries=18 pass=18 exit=0
harness_exit=0
```

## 6. The counter writes nothing into the lane tree

Every file under `corpus/` was sha256-snapshotted immediately before the first counter run and
immediately after the second, across the same 29.3 s window as the pair above:

| check | result |
|---|---|
| files added under `corpus/` | `[]` |
| files removed under `corpus/` | `[]` |
| files changed under `corpus/` | `[]` |

The counter copies `corpus/` into `tempfile.mkdtemp` scratch per row (baseline and mutant each get
their own fresh copy), writes its compile/import probe inside that scratch, and deletes the scratch at
exit; no lane path moves. In-flight edits by other seats are visible in this snapshot (captured in the
same window) and are not attributable to this run:

```sh
git status --short corpus/ | head -30
```
```text
 M corpus/QUALITY.md
 M corpus/README.md
 M corpus/SOURCES.md
 M corpus/instruments/knowledge-expected.txt
 M corpus/instruments/recheck-audit.py
 M corpus/instruments/source-recheck.py
 M corpus/knowledge/considerthese-proposals-ledger.md
?? corpus/instruments/limb-fixtures/
?? corpus/instruments/limb-ledger.json
?? corpus/instruments/limb-mutation-check.py
?? corpus/instruments/score-gap.py
?? corpus/knowledge/vendor-third-party-finding-coordination.md
?? corpus/source-snapshots/round-31/
```

## 7. Independent re-derivation of every row (not the counter's code path)

A throwaway harness (copy `corpus/` to scratch, run the row's kill, apply the one find/replace,
`py_compile`, run the kill again, compare exit and signal) reproduces every LIMB verdict. The two
controls are where a naive harness without the counter's pre-mutant gates goes wrong, which is exactly
what they are for:

| row | find count | mutant compiles | live exit/sig | mutant exit/sig | byte-identical output | naive verdict | counter verdict |
|---|---|---|---|---|---|---|---|
| `RA-parse` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-cwd` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-paths` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-cdroot` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-instrument` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-own` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-completeness` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-expect-missing` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `RA-expect-unexpected` | 1 | yes | 0/y | 1/n | no | killed | killed |
| `SR-stem-mismatch` | 1 | yes | 1/y | 0/n | no | killed | killed |
| `SR-occurrence-not-unique` | 1 | yes | 1/y | 0/n | no | killed | killed |
| `FR-missing-entry` | 1 | yes | 1/y | 1/n | no | killed | killed |
| `FR-duplicate-entry` | 1 | yes | 1/y | 0/n | no | killed | killed |
| `CTL-noop` | 1 | n/a (noop) | 0/y | 0/y | yes | survivor | invalid:noop |
| `CTL-nocompile` | 1 | no | 0/y | 1/n | no | killed | invalid:nocompile |
| `CTL-equivalent` | 1 | yes | 1/y | 1/y | yes | survivor | survivor |

Reading the controls: the naive harness reports `CTL-noop` as **survivor** (it cannot tell that the
mutant bytes are the original) and `CTL-nocompile` as **killed** (the broken file exits 1); the counter
reports `invalid:noop` and `invalid:nocompile` respectively, so both gates are load-bearing, and
`CTL-equivalent` — a real comment patch whose run is byte-identical to the live run — is an honest
`survivor`, not a fabricated kill.

## 8. The 3 controls (landed rows)

Each control reuses a **real limb's** instrument, kill command, signal and `live_exit`, so a `survivor`
means: the very kill that demonstrably kills that limb sees no difference from an equivalent patch.

### `CTL-noop` → expect `invalid:noop`

- instrument: `corpus/instruments/recheck-audit.py`; live_exit: `0`; kill/signal/live_exit reused from a landed limb
- find:
```python
def digest(data):
```
- replace:
```python
def digest(data):
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest parseonly\.md .*\bok$`
- note: control, bound to the RA-parse limb's own instrument/kill/signal/live_exit: find == replace on a real, exactly-once line (`def digest(data):` in recheck-audit.py). The mutated bytes ARE the original bytes, so the counter must stop at invalid:noop before compiling or running anything; a counter that calls this killed is rubber-stamping.

### `CTL-nocompile` → expect `invalid:nocompile`

- instrument: `corpus/instruments/recheck-audit.py`; live_exit: `0`; kill/signal/live_exit reused from a landed limb
- find:
```python
def digest(data):
```
- replace:
```python
def digest(data)
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest parseonly\.md .*\bok$`
- note: control, bound to the RA-parse limb's own instrument/kill/signal/live_exit: the same exactly-once line truncated to `def digest(data)` drops the colon, so the mutant cannot parse and py_compile must reject it as invalid:nocompile. The broken mutant also exits 1 and loses the selftest signal, so a counter without the compile gate would mislabel this row killed.

### `CTL-equivalent` → expect `survivor`

- instrument: `corpus/instruments/source-recheck.py`; live_exit: `1`; kill/signal/live_exit reused from a landed limb
- find:
```python
def normalize(text):
```
- replace:
```python
def normalize(text):  # equivalent control patch: comment only, no behavior change
```
- kill: `python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json --source SFIX-STEM`
- signal: `reason=stem-mismatch`
- note: control, bound to the SR-stem-mismatch limb's own instrument/kill/signal/live_exit: a comment appended to a real, exactly-once line (`def normalize(text):` in source-recheck.py). The patch compiles and the B1 fixture run keeps its exit and reason=stem-mismatch, so a kill that demonstrably sees SR-stem-mismatch sees no difference here: the honest verdict is survivor, and a counter reporting killed would be inflating kills with a patch that changes no behavior.

## 9. The 13 limbs (landed rows, verbatim from the owner fragments)

### `RA-parse` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
capture_output=True).returncode == 0
```
- replace:
```python
capture_output=True).returncode >= 0
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest parseonly\.md .*\bok$`
- note: frozen limb (a) parse: the bash -n gate is defeated, so every returncode (including the syntax-error 2) counts as parseable; isolated by parseonly.md, the only fixture whose frozen verdict depends on parse alone

### `RA-cwd` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
lane_rc == foreign_rc and lane_digest == foreign_digest
```
- replace:
```python
True
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest cwd\.md .*\bok$`
- note: frozen limb (b) cwd: lane-root vs foreign-cwd exit+digest equality collapsed to True; isolated by cwd.md (a relative corpus/instruments path runs from the lane root and fails from /)

### `RA-paths` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
limbs["paths"] = named and not missing
```
- replace:
```python
limbs["paths"] = True
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest ghost\.md .*\bok$`
- note: frozen limb (c) paths: the named-and-exists conjunction collapsed to True; isolated by ghost.md (names an absent corpus/knowledge path while parse and cwd still pass)

### `RA-cdroot` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
os.path.abspath(cd_target) == (cdroot or root)
```
- replace:
```python
True
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest elsewhere\.md .*\bok$`
- note: strict limb (d) cdroot: the 'cd <path> &&' target is no longer compared with the audited root; isolated by elsewhere.md (cd /tmp passes both frozen limbs, so only cdroot decides)

### `RA-instrument` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
strict["instrument"] = bool(instruments) or base_test
```
- replace:
```python
strict["instrument"] = True
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest instonly\.md .*\bok$`
- note: strict limb (e) instrument: the corpus/instruments-or-base-test requirement collapsed to True; isolated by instonly.md (own file named, cdroot ok, no instrument named)

### `RA-own` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
strict["own"] = own or sourced or base_state
```
- replace:
```python
strict["own"] = True
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest selftesty\.md .*\bok$`
- note: strict limb (f) own: the own/sourced/base-state disjunction collapsed to True; isolated by selftesty.md (instrument ok, the entry's own file not named)

### `RA-completeness` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
    complete = len(entries) == total and total > 0
    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)
```
- replace:
```python
    complete = True  # mutant: completeness limb disabled
    expect_ok = not expect_active or (not missing_entries and not unexpected_entries)
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest complete-empty\s+exit=1 want=1 lines=0/0 complete=False ok$[\s\S]*^selftest complete-missing-line\s+exit=1 want=1 lines=1/2 complete=False ok$`
- note: completeness: main()'s own 'complete' verdict collapsed to True. On the pre-round-31 bytes this was the one RA survivor (mutant compiled, find once, exit 0, stdout byte-identical to pristine). Round 31 added the two main()-level fixtures this signal keys on. Only 'total > 0' is observable alone, because strict_passed == total already implies len(entries) == total (strict_passed <= len(entries) <= total); complete-empty carries the exit flip, complete-missing-line carries the receipt complete=False flip

### `RA-expect-missing` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
sorted(wanted - actual)
```
- replace:
```python
[]
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest expect-missing .*\bok$`
- note: expected-list missing set collapsed to []: a committed entry deleted from the tree no longer reds the audit; isolated by the expect-missing tree fixture (rc must be 1 and missing_entries must name ghost-absent.md)

### `RA-expect-unexpected` — `corpus/instruments/recheck-audit.py`

- live_exit: `0`
- find:
```python
sorted(actual - wanted)
```
- replace:
```python
[]
```
- kill: `python3 {inst} --selftest`
- signal: `(?m)^selftest expect-unexpected .*\bok$`
- note: expected-list unexpected set collapsed to []: an extra tree entry no longer reds the audit; isolated by the expect-unexpected tree fixture (rc must be 1 and unexpected_entries must name extra.md)

### `SR-stem-mismatch` — `corpus/instruments/source-recheck.py`

- live_exit: `1`
- find:
```python
    if Path(path).stem != source_id:
```
- replace:
```python
    if False:  # SR-stem-mismatch mutant: B1 stem check dropped
```
- kill: `python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/stem-mismatch/manifest.json --source SFIX-STEM`
- signal: `reason=stem-mismatch`
- note: B1 (QUALITY Q9): a capture whose file stem differs from the record id is rejected before any byte pin. Fixture corpus/instruments/limb-fixtures/sr/stem-mismatch: record SFIX-STEM, capture SFIX-STEM-capture.txt with a correct sha256 pin and a quote that occurs exactly once, so B1 is the only failing limb; the B1-dropping mutant prints sha256 OK and exits 0.

### `SR-occurrence-not-unique` — `corpus/instruments/source-recheck.py`

- live_exit: `1`
- find:
```python
        if occurrences > 1 and anchor_verdict_result != "ok":
```
- replace:
```python
        if occurrences > 1 and anchor_verdict_result != "ok" and anchor_verdict_result != "missing":  # SR-occurrence-not-unique mutant
```
- kill: `python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json --source SFIX-REPEAT`
- signal: `reason=occurrence-not-unique`
- note: B2 (QUALITY Q9): a quote occurring more than once without a verified anchor is rejected. Fixture corpus/instruments/limb-fixtures/sr/occurrence-not-unique is stem-correct (capture SFIX-REPEAT.txt, id SFIX-REPEAT) so B1 cannot preempt, closing M30-1; the quote occurs exactly twice with no anchor and the mutant that lets missing anchors pass prints occurrences=2 anchor=MISSING and exits 0.

### `FR-missing-entry` — `corpus/instruments/frontier-recheck-count.py`

- live_exit: `1`
- find:
```python
    if not os.path.isfile(full):
        return None
```
- replace:
```python

```
- kill: `python3 {inst} --root {root}/corpus/instruments/limb-fixtures/fr/fr-missing-entry`
- signal: `FAIL\s+F98\s+knowledge/zz-missing\.md\s+ids=-\s+exit=-\s+problems=missing-entry\nentries=1 pass=0 exit=1\n?`
- note: Drops the fail-closed missing-entry guard in entry_contract (E): the mutant raises FileNotFoundError on the absent entry (traceback, still exit 1), so the kill is by signal, not exit. Fixture corpus/instruments/limb-fixtures/fr/fr-missing-entry holds one admitted row F98 naming knowledge/zz-missing.md and nothing else, so problems=missing-entry is the only failure marker. Measured r31: live 1/sig-y, mutant 1/sig-n.

### `FR-duplicate-entry` — `corpus/instruments/frontier-recheck-count.py`

- live_exit: `1`
- find:
```python
    seen_realpath = {}
    for record in records:
        rp = record.get("realpath")
        if rp is None:
            continue
        if rp in seen_realpath:
            duplicate = (seen_realpath[rp], record["frontier"], record["entry"])
            break
        seen_realpath[rp] = record["frontier"]
    if duplicate:
        print("DUPLICATE-ENTRY %s,%s %s" % (duplicate[0], duplicate[1], duplicate[2]))
    fail_closed = duplicate is not None or not records or passed != len(records)
```
- replace:
```python
    fail_closed = not records or passed != len(records)
```
- kill: `python3 {inst} --root {root}/corpus/instruments/limb-fixtures/fr/fr-duplicate-entry`
- signal: `PASS\s+F98\s+knowledge/dup-entry\.md\s+ids=S003\s+exit=0[ \t]*\nPASS\s+F97\s+knowledge/dup-entry\.md\s+ids=S003\s+exit=0[ \t]*\nDUPLICATE-ENTRY F98,F97 knowledge/dup-entry\.md\nentries=2 pass=2 exit=1\n?`
- note: Drops the duplicate-realpath fail-closed block (F) only: both admitted rows F98/F97 still PASS their own A-D contract on the same entry file, so the mutant flips exit 1 -> 0 with no DUPLICATE-ENTRY line (killed by exit and by signal). Fixture corpus/instruments/limb-fixtures/fr/fr-duplicate-entry carries a stem-correct S003 capture + schema-1 manifest and a relative source-recheck.py invocation, so no other problem class fires.

## 10. Known limits and routed recommendations (not implemented here)

1. **A limb id is a label, not a proof of the patched line.** The frozen row schema has no field binding
   `id` to a code location, so a ledger could name `RA-parse` while patching an unrelated line and still
   print `killed`. Mitigation in the landed file: every row's `note` names the implementing line and the
   isolating fixture, and the claim's closure clause re-derives rows by hand (section 7 does this for all
   16 rows). `CritC1Kill-5` proposed a per-limb `reach` regex (mutant must still reach the instrument's
   own summary). The landed counter already refuses signals that match the empty string, refuses kills
   that do not run `python3 … {inst}`, refuses commands chained after the last `python3 … {inst}`,
   confirms the live baseline twice, gates the mutant's module import with a sentinel, and runs the
   mutant twice on its own scratch; a full `reach` gate remains a counter-schema change outside this
   seat's file, so it is **routed to the L1** rather than faked with a field the counter would drop.
2. **`invalid:timeout` is emitted by the counter but is absent from the frozen verdict enum**
   (`invalid:live-baseline|find-count|noop|nocompile`). Observed in the counter's own docstring and
   `--selftest`. Routed to the L1 for the claims amendment; no row of this ledger hit that path.
3. **Control-id binding is enforced by the counter** (`CONTROL_ID_EXPECTS`: `CTL-noop` ⇒ `invalid:noop`,
   `CTL-nocompile` ⇒ `invalid:nocompile`, `CTL-equivalent` ⇒ `survivor`), and this ledger additionally
   binds each control to a real limb's instrument/kill/signal/live_exit.
4. **PRE-STATE note.** The counter digest changed nine times while this seat waited
   (`9e729daf…` → `eb9b87ff…` → `b4223ed9…` → `cde7c2b6…` → `f926bf75…` → `e1195722…` → `67db4a20…` →
   `bd18c244…` → `c660a95f…`; prefixes as observed, final digest full below). Every supersede was a
   critic-route closure, not a schema change, and no supersede moved a verdict. Runs against earlier
   digests are non-comparative and are **not** cited; every figure in this receipt is from the FINAL
   digest `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f`, captured before and after the pair in section 2.
   ExecCounter's one-line description of the last step: "bd18c244 -> c660a95f: the mutant side now runs
   on its OWN fresh scratch copy and is run twice like the baseline; a disagreement between the two
   mutant runs is invalid:mutant-baseline."
5. **The import-crash route is closed on the final counter, and I measured it myself.** `CritC1Kill-5`
   showed that on `cde7c2b6` thirteen module-level `NameError` patches, unrelated to the limbs their ids
   named, still printed `limbs=13 killed=13 survivors=0` / `controls=3 rejected=3` exit 0, because a
   crash loses the signal exactly as a load-bearing mutant does. On the landed counter the same patch
   shape is refused before the mutant run. Measured with a throwaway ledger (not the landed file; the
   landed file has no such row, since all 13 landed mutants import cleanly):

```text
find    = FROZEN_LIMBS = ("parse", "cwd", "paths")
replace = FROZEN_LIMBS = ("parse", "cwd", "paths") + a new module-level line  _undefined_probe_name_   # valid syntax, NameError at import
kill    = python3 {inst} --selftest;  live_exit 0;  signal = (?m)^selftest parseonly\.md .*\bok$
```

```text
LIMB GATE-import-nameerror live=0/y mutant=-/- verdict=invalid:import
limbs=1 killed=0 survivors=0
controls=0 rejected=0
```

   `mutant=-/-` and `verdict=invalid:import`: the probe never reaches the mutant run, so it cannot be
   counted as a kill. A blanket "any traceback is invalid" rule is explicitly **not** proposed, because
   it would break `FR-missing-entry`, whose mutant raises inside the run and whose raise IS the limb.

## 11. Bounds compliance

- Writes: only `corpus/instruments/limb-ledger.json` and this receipt, both under the lane. Nothing in
  the fleet root, `shokuknow`, `templates/`, `scripts/`, `.ufo/state/`, `MANIFEST.json` or `.scratch/`.
- No git/jj mutation (read-only `git status` / `git rev-parse` only); no commit, stash, checkout, reset.
- No tool install or upgrade (none needed); no network fetch; no pacman transaction.
- Leaf role: no subagent dispatch, no delegation. Read-only poll commands were auto-backgrounded by the
  tool harness when they exceeded the foreground window; no work was started in the background.
- Scratch used for measurement lives under `tempfile.mkdtemp` and was deleted per row.

## 12. Notifications and one digest correction

- `ScribeInstrReadme`: messaged with the landed ledger/counter facts. The first message cited the
  then-final counter `bd18c244…`; it was **corrected to `c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f`** after
  ExecCounter's last supersede. The ledger digest (`c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be`) did not change.
- `ScribeSkillGate`: the id resolves to a **closed round-28** seat (it replied out of scope, deliverable
  untouched at its committed state). `R51DraftSkillGates` also replied out of scope — it is a round-51
  Gates-row scribe in another lane. No live round-31 skill-gate consumer answered under either id, so
  the R6 evidence for this wave is recorded here (sections 1-9) and needs no lane file from me.
- `ExecCounter`: informed of the merge result and of each digest change I observed, so the final digest
  in this receipt is the one its owner declared last.

## 13. Files changed by this seat

- `corpus/instruments/limb-ledger.json` (new, 13 limbs + 3 controls)
- `.ufo/waves/round-31/wave1/ExecLedgerMerge.md` (this receipt)
