# MutC1Hunt — r84 C1: mutants the 33-case suite does not kill (beyond the frozen 79 rows)

Target (frozen, never edited): `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/c1/recheck-cwd-census.py`
sha256 `e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e` before and after
(`MutC1Hunt-receipts/hashes.txt`); selftest `cases=33 failures=0`.
Landed r83 instrument (not touched): `corpus/instruments/recheck-cwd-census.py`
sha256 `343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9`.
Frozen counter: `.ufo/waves/round-84/c1/mutbat.py` (r84_limbs). Landed table: 79 rows.

Deliverables
- Table: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/w1/MutC1Hunt-rows.json`
  — 25 rows: **18 behaviour-changing gaps, 4 equivalents, 2 killing controls, 1 neutral**.
- Receipts: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-84/w1/MutC1Hunt-receipts/`
  (`mutbat.out`, `witness.out`, `routechecks.out`, `build-rows.py`, `witness.py`, `imp.py`,
  `routecheck.py`, `hashes.txt`).

Battery result (verbatim final line, `mutbat.out`):
```
MUTBAT target_sha256=e5f2e4bdecfc18f80e823ec3bc0797e09b11761ad1b59ad99d488ca3c3cf179e baseline=ok rows=25 killed=2 survived=22 miskilled=0 dirty=0 notderived=0 neutral_ok=1/1 decoy=ok decoy_hidden=21/24
```
(exit 1 by design: survivors are the deliverable, not a battery defect. Baseline clean, keyed
D1/D2/D3 decoys green, both controls killed; no inconclusive rows — miskilled=dirty=notderived=0,
so every non-killed verdict is a clean exit-0 SURVIVED.)

Witness result (`witness.out`): every gap differs from pristine on a concrete command; every
equivalent is byte-identical (matrix stdout sha256 `569254f2…585ce`, or the 252-dict
`conform_ok` verdict vector).

## Verdict in one paragraph
The twelve r83 survivors H01-H12 are closed, but the six round-84 checks pin only the values
their fixtures happen to have: `summary-fields`' tree has `noprefix=exit2_foreign=restoration_only=0`,
so three summary slots can be rewritten and stay green (X09/X10/X18); `entry-set` pins exit-0/7
but not the commonest non-gating bucket exit-1 (X11) and bypasses the real timeout path (X12);
`argv-values`/`usage-guards` never execute the shipped CLI (X13) and never call `main()` with no
flags (X14). Outside the six checks: `conform_ok` couples two limbs and turns a two-defect tree
conformant (X21); `census` requires `TMPDIR` (X06); the timeout duration and sentinel are
unpinned (X15/X12); non-UTF-8 input crashes (X16); `has_restoration_recheck` and the prefix test
are weakened but latent (X07/X08); five `selftest()` restores are unasserted and leak module/process
state (X01-X05). The suite has no subprocess end-to-end test at all — that is the root cause of
X13/X14 and of the controls being the only rows killed by default-mode output assertions.

## Rows (battery verdict | class | witnessed difference | routed killing assertion)

| id | verdict | witness (pristine → mutant) | route |
|---|---|---|---|
| X01-LK-runforeign | SURVIVED | `run_foreign` restored true → false (stub `-1` left installed) | `entry-set` += `globals()["run_foreign"] is real_run` |
| X02-LK-selftest | SURVIVED | `selftest` global restored true → false (`lambda:77` left) | `argv-values` += `globals()["selftest"] is real_selftest` |
| X03-LK-chdir | SURVIVED | cwd restored true → false (left in deleted case-29 dir) | `argv-values` += `os.getcwd() == here29` |
| X04-LK-timeout | SURVIVED | `TIMEOUT` 120 → 1 after selftest | `timeout-bucket` += `TIMEOUT == saved_timeout17` |
| X05-LK-mkdtemp | SURVIVED | `tempfile.mkdtemp` restored true → false (recording wrapper left) | `scratch-cleanup` += `tempfile.mkdtemp is real_mkdtemp` |
| X06-ENV-tmp-unset | SURVIVED | TMPDIR unset: `entries=1 … exit0_foreign=1`, rc 0 → `KeyError: 'TMPDIR'`, rc 1 | `tmpdir-unset`: run `census(root1, lane1)` and assert `got18 == got1` |
| X07-REST-substr | SURVIVED | mid-line mention: `NORECHECK`/`norecheck=1` → `RESTORATION-ONLY`/`restoration_only=1` | case-8 `n-neither.md` += prose line containing the header |
| X08-NOPREFIX-in | SURVIVED | `true && cd <LANE> && true`: `noprefix=1`, rc 1 → `noprefix=0`, rc 0 | case 14 += `d-mid.md`, `noprefix=3`, `exit0_foreign=3` |
| X09-SUM-noprefix-slot | SURVIVED | summary `noprefix=1` → `noprefix=0` (prints `norecheck`) | case-1 exact summary line |
| X10-SUM-exit2-zero | SURVIVED | summary `exit2_foreign=1` → `0` | case-1 exact summary line |
| X11-ENTRY-exit1 | SURVIVED | prefixed exit-1: no ENTRY → `ENTRY q-exit1.md noprefix=0 foreign_exit=1` | `bucket-sum` += `"ENTRY osv-b.md" not in out21` |
| X12-TIMEOUT-sentinel | SURVIVED | timeout ENTRY `foreign_exit=-1` → `-2` (same bucket) | `timeout-bucket`: capture case 17 with `verbose=True`, assert `ENTRY h-hang.md noprefix=0 foreign_exit=-1` |
| X13-MAIN-argv-slice | SURVIVED | CLI `--root D --lane D`: rc 0 + RESULT conformant → rc 2 + `usage:`, no RESULT | `usage-guards`: one `subprocess.run([sys.executable, "-B", abspath(__file__), "--root", root19a, "--lane", lane19])`, assert rc 0 + RESULT |
| X14-MAIN-defroot | SURVIVED | bare run in empty fixture: `entries=0`, rc 0 → `no corpus/knowledge under <parent>`, rc 1 | `usage-guards`: chdir into an empty fixture, `main([prog])`, assert rc 0 + `entries=0` |
| X15-TIMEOUT-default | SURVIVED | 2 s recheck: `exit0_foreign=1` (~2 s) → `foreign_exit=-1`, `exit_other=1` (1 s) | `timeout-bucket` += `TIMEOUT == 120` (policy pin; behaviour test costs ~2 s/run) |
| X16-FIRST-errors | SURVIVED | one 0xE9 byte: `entries=1 … exit0_foreign=1`, rc 0 → `UnicodeDecodeError`, rc 1 | `first-line`: bytes fixture with `0xE9`, assert no exception and `entries=1/exit0_foreign=1` |
| X18-SUM-restoration-adds-noprefix | SURVIVED | summary `restoration_only=1` → `2` (adds noprefix) | case-1 exact summary line (its `noprefix=5`, `restoration_only=0`) |
| X21-CONFORM-couple-norecheck-restoration | SURVIVED | tree with `norecheck=1`+`restoration_only=1`: RESULT nonconformant rc 1 → **conformant rc 0** | `conform-limbs` += hand-built `conform_ok({...norecheck:1, restoration_only:1}) is False` |
| X17-STRIP-space | SURVIVED | **equivalent**: matrix stdout sha identical | — |
| X22-CONFORM-exit2-le-noprefix | SURVIVED | **equivalent**: 252-dict verdict vector identical | — |
| X24-CONFORM-sum-add-noprefix | SURVIVED | **equivalent**: 252-dict verdict vector identical | — |
| X25-USAGE-except-breadth | SURVIVED | **equivalent on frozen bytes**: matrix stdout identical; guard unreachable | note as latent (r80-F4 shape) |
| X19-SUM-entries-slot | KILLED (summary-fields) | control: summary `entries=2` → `1` | — |
| X20-ENTRY-drop-exit2 | KILLED (output-lines) | control: `ENTRY e-exit2.md …` disappears | — |
| X23-NEUTRAL-comment | NEUTRAL-OK | control: trailing comment, no change | — |

## Exact routed fixes (cheapest assertion; attack seat does not edit)

**X09/X10/X18 — one assertion kills all three.** In `prefix-census` (case 1; `_t1` already
holds the default output; the fixture has entries=6, noprefix=5, exit2=1, exit0=3, exit1=1,
other=1, norecheck=0, restoration=0):
```python
        want1s = ("RECHECK-CWD entries=6 noprefix=5 exit2_foreign=1 exit0_foreign=3 "
                  "exit1_foreign=1 exit_other=1 norecheck=0 restoration_only=0")
        check("prefix-census",
              all(got1[k] == v for k, v in want1.items())
              and [ln for ln in _t1.splitlines()
                   if ln.startswith("RECHECK-CWD entries=")] == [want1s],
              "got=%s want=%s" % (counts_str(got1, want1), counts_str(want1, want1)))
```
X09 prints `norecheck=0`≠5, X10 prints `0`≠1, X18 prints `0+5=5`≠0.

**X11.** In `bucket-sum` (case 21): `and "ENTRY osv-b.md" not in out21`. `osv-b` is the
prefixed exit-1 entry; `out21` is already captured and emitted no ENTRY line at
`e5f2e4bd`, so the conjunct is true on pristine and false on the mutant
(`routechecks.out` PASS X11). Do **not** use case 1: its `d-exit1` is prefix-less
(`recheck: exit 1`) and prints an ENTRY line in both versions — verified, that route would
have failed on pristine.

**X12.** In case 17 change `_t17, got17 = capture(census, root17, root17)` to
`capture(census, root17, root17, True)` (same run, TIMEOUT already patched to 1) and add to
`timeout-bucket`: `and "ENTRY h-hang.md noprefix=0 foreign_exit=-1" in _t17`.

**X13.** In `usage-guards` (after `ret19l`):
```python
        e2e = subprocess.run([sys.executable, "-B", os.path.abspath(__file__),
                              "--root", root19a, "--lane", lane19],
                             stdin=subprocess.DEVNULL, capture_output=True,
                             text=True, timeout=60)
        # check(...): and e2e.returncode == 0
        #             and "RECHECK-CWD-RESULT conformant" in e2e.stdout
```
This is the only test that exercises `if __name__ == "__main__"`.

**X14.** In `usage-guards`:
```python
        root19d, _k19d = fixture("case19-default-root")     # empty corpus/knowledge
        here19 = os.getcwd()
        os.chdir(root19d)
        try:
            try:
                out19d, ret19d = capture(main, ["recheck-cwd-census.py"])
                exit19d = None
            except SystemExit as exc19d:
                out19d, ret19d, exit19d = "", None, str(exc19d)
        finally:
            os.chdir(here19)
        # check(...): and exit19d is None and ret19d == 0
        #             and "RECHECK-CWD entries=0" in out19d
```

**X15.** In `timeout-bucket`: `and TIMEOUT == 120`. (A behaviour test — a fixture running
`sleep 2` under the shipped TIMEOUT and expecting `exit0_foreign=1` — costs ~2 s on every suite
run; the pin is free and `exit_other` is non-gating, so the failure mode is silent.)

**X16.** In `first-line`:
```python
        root5b, kdir5b = fixture("case5-bytes")
        with open(os.path.join(kdir5b, "z-latin1.md"), "wb") as fh5b:
            fh5b.write(b"# caf\xe9\nrecheck: cd " + root5b.encode() + b" && true\n")
        try:
            _t5b, got5b = capture(census, root5b, root5b)
            exc5b = None
        except Exception as exc5b_:
            got5b, exc5b = {}, repr(exc5b_)
        # check(...): and exc5b is None and got5b.get("entries") == 1
        #             and got5b.get("exit0_foreign") == 1
```

**X21.** In `conform-limbs`:
```python
        coupled = {"entries": 2, "noprefix": 0, "exit2_foreign": 0, "exit0_foreign": 0,
                   "exit1_foreign": 0, "exit_other": 0, "norecheck": 1,
                   "restoration_only": 1}
        # check(...): and conform_ok(coupled) is False
```

**X06.** In `tmpdir-unset`, inside the existing try after `refused18, raised18 = …`:
`_t18, got18 = capture(census, root1, lane1)` and in the check `and got18 == got1`.
(The existing `except Exception` turns the mutant into a FAIL, not a traceback.)

**X07.** In case 8:
```python
        write_entry(kdir8, "n-neither.md",
                    "body only, no recheck header\n"
                    "- documents `restoration-recheck:` mid-line\n")
```
`want8u` stays `norecheck=1`, so the substring mutant relabels to `restoration_only` and fails.

**X08.** In case 14:
```python
        write_entry(kdir14, "d-mid.md", "recheck: true && cd %s && true\n" % root14)
        want14 = {"entries": 4, "noprefix": 3, "exit2_foreign": 0, "exit0_foreign": 3,
                  "exit1_foreign": 1, "exit_other": 0, "norecheck": 0}
```

**X01-X05 (harness state).** One identity conjunct each, appended to the check that owns the
swap; all referenced locals are in scope at that point:
`entry-set` → `globals()["run_foreign"] is real_run`;
`argv-values` → `globals()["selftest"] is real_selftest and os.getcwd() == here29`;
`timeout-bucket` → `TIMEOUT == saved_timeout17`;
`scratch-cleanup` → `tempfile.mkdtemp is real_mkdtemp`.
These are low-severity (in-process reuse only) but exactly the class the seat was asked to probe,
and each is unasserted today while `has_restoration_recheck`'s analogous restore **is** load-bearing
(conform-limbs kills it — see the frozen S37 row).

## Equivalents (survive, not coverage findings)
- **X17 `strip()` → `strip(" ")`**: the retained trailing newline is inert — the prefix test only
  reads leading bytes and `bash -c` ignores trailing whitespace. Witness: 8-entry matrix stdout
  sha256 identical (`569254f2…585ce`).
- **X24 `conform_ok` bucket sum += noprefix**: `noprefix>0` already fails the noprefix limb, so the
  verdict is False either way; `noprefix=0` adds zero. Witness: 252-dict grid verdict vector
  identical. (The same edit at the *summary print* is X18, which is a real gap.)
- **X22 `exit2_foreign == 0` → `<= noprefix`**: the same predicate pins `noprefix == 0`, so the
  two forms agree for non-negative counts. Witness: same 252-dict vector.
- **X25 `except Exception` → `except SystemExit` in `usage_run`**: main() returns ints on every
  `usage_run` input, so the breadth is unobservable; the redundant `r[2] is None` conjunct is
  likewise implied by `r[1] == 2`. Latent harness weakness only (a future main() raising would
  crash the suite instead of printing a FAIL, the r80-F4 shape).

## Controls
- **X19** (summary entries slot ← noprefix) is **KILLED by summary-fields**: it proves the battery
  does catch summary-slot defects, so X09/X10/X18 survive *only* because case 27's fixture leaves
  those slots zero.
- **X20** (drop the exit-2 ENTRY arm) is **KILLED by output-lines**, proving the exit-2 arm is
  pinned while X11's exit-1 arm is not.
- **X23** (neutral comment) is NEUTRAL-OK; D3 picked one non-neutral row's anchor (this run
  `d3_row=X15-TIMEOUT-default`) and the decoy limb is green with `decoy_hidden=21/24`.

## Route verification (proposed assertions fire on their mutants)
`MutC1Hunt-receipts/routecheck.py` builds each inserted fixture, evaluates the proposed conjunct
on pristine and on the mutant bytes, and prints PASS iff pristine holds and the mutant fails:
```
ROUTECHECK pass=13 fail=0
```
Covers X06, X07, X08, X09, X10, X11, X12, X13, X14, X15, X16, X18, X21; X01-X05 are identity
conjuncts on state the leak witness already shows missing (no dynamic route needed). Notable
findings while validating the routes: case 1's `d-exit1` is prefix-less so it cannot pin the
exit-1 ENTRY arm (X11 must use case 21's `osv-b`), and the summary assertion must be the exact
line because X18's mutant prints `restoration_only=5` on case 1.

## Reproduce
```sh
S=/fast/scratch/hyaku/kasegi-r84/MutC1Hunt   # any scratch; TMPDIR is passed explicitly
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
TMPDIR=$S python3 -B .ufo/waves/round-84/c1/mutbat.py \
  --target .ufo/waves/round-84/c1/recheck-cwd-census.py \
  --table .ufo/waves/round-84/w1/MutC1Hunt-rows.json \
  --expect-cases 33 --work $S/h                      # ~40 s, exit 1 (2 killed / 22 survived)
TMPDIR=$S python3 -B .ufo/waves/round-84/w1/MutC1Hunt-receipts/witness.py \
  --target .ufo/waves/round-84/c1/recheck-cwd-census.py \
  --rows .ufo/waves/round-84/w1/MutC1Hunt-rows.json --outdir $S/wit  # ~20 s, 25 rows
TMPDIR=$S python3 -B .ufo/waves/round-84/w1/MutC1Hunt-receipts/routecheck.py \
  --target .ufo/waves/round-84/c1/recheck-cwd-census.py \
  --rows .ufo/waves/round-84/w1/MutC1Hunt-rows.json \
  --mutbat .ufo/waves/round-84/c1/mutbat.py --outdir $S/route  # ~4 s, 13/13 PASS
```
`MutC1Hunt-rows.json` is generated (and every anchor's uniqueness asserted) by
`MutC1Hunt-receipts/build-rows.py`; `witness.py` imports `mutbat.apply_row` so the receivers
re-materialise the exact mutant bytes. Witness command per row (single row):
`… witness.py --only X13-MAIN-argv-slice --outdir $S/wit`.

## Scope / hygiene
- No lane file was edited; only `.ufo/waves/round-84/w1/` was written (rows, report, receipts).
  Frozen c1 bytes, landed corpus instrument, corpus/, SKILL/PROVINCE/SCORECARD/LOG untouched.
- Target sha256 before/after: `e5f2e4bd…179e` (unchanged); landed r83 instrument `343b21e4…08c9`.
- No git/jj writes; no pacman; no tool installs (nothing to install).
- Scratch `/fast/scratch/hyaku/kasegi-r84/MutC1Hunt` removed after the receipts were copied.

## Files written
- `.ufo/waves/round-84/w1/MutC1Hunt-rows.json`
- `.ufo/waves/round-84/w1/MutC1Hunt.md`
- `.ufo/waves/round-84/w1/MutC1Hunt-receipts/{mutbat.out,witness.out,routechecks.out,build-rows.py,witness.py,imp.py,routecheck.py,hashes.txt}`
