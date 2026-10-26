# ExecLimbSRoccurrencenotunique — falsify ledger limb `SR-occurrence-not-unique` (round 31, wave 2)

Seat: ExecLimbSRoccurrencenotunique (leaf). Lane repo `/home/vgpnk/Projects/shokunin/kasegi-shokunin`
(base `b374febbb33ccadade78a787279707fd5d2e6e1d`, claims freeze
`738a77999a00efbca129cfccb28a481037f6241f`, wave-1 landing HEAD
`eecad59db166e0626ca2472e96ea48bc28a35153`).

Files written: this receipt only. Every probe ran in `mktemp -d` scratch copies of `corpus/`, all
deleted at the end. No git/jj mutation (read-only `git rev-parse`), no delegation, no background job,
no network fetch, no credential material, no tool install/upgrade (nothing needed; pacman not
invoked). Answering model actually run on: `opencode-go/deepseek-v4.1-flash` (harness route; no model
passed).

Measured bytes — identical at seat start and seat end (no PRE-STATE label needed; the wave-2 writer
that owns these two files did not touch them during this seat):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/instruments/limb-mutation-check.py corpus/instruments/limb-ledger.json corpus/instruments/source-recheck.py
c660a95ff92ff1d578c6458faf868ac2c41c5d1854da3fe2a97f48ee71118a0f  corpus/instruments/limb-mutation-check.py
c042adf6b25c78b65e3f5c1e9898095f355599a188cfe08ba2547765d6ed03be  corpus/instruments/limb-ledger.json
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003  corpus/instruments/source-recheck.py
$ git rev-parse HEAD
eecad59db166e0626ca2472e96ea48bc28a35153
```

(Re-hashed after the last probe: same three hashes, same HEAD.)

## 0. The row under test (verbatim, `corpus/instruments/limb-ledger.json:104-113`)

```json
{
  "id": "SR-occurrence-not-unique",
  "instrument": "corpus/instruments/source-recheck.py",
  "find": "        if occurrences > 1 and anchor_verdict_result != \"ok\":\n",
  "replace": "        if occurrences > 1 and anchor_verdict_result != \"ok\" and anchor_verdict_result != \"missing\":  # SR-occurrence-not-unique mutant\n",
  "kill": "python3 {inst} --manifest {root}/corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json --source SFIX-REPEAT",
  "live_exit": 1,
  "signal": "reason=occurrence-not-unique",
  "note": "B2 (QUALITY Q9): a quote occurring more than once without a verified anchor is rejected. …"
}
```

`find` occurs exactly once in the landed instrument, at `corpus/instruments/source-recheck.py:192`
(the B2 gate; the map that supplies the reason strings is `:193-197`, the reject emit `:198`):

```
$ python3 -c "d=open('corpus/instruments/source-recheck.py','rb').read(); print('find_count=%d' % d.count(b'        if occurrences > 1 and anchor_verdict_result != \"ok\":\n'))"
find_count=1
```

The fixture is stem-correct (M30-1 closed): `manifest.json` records id `SFIX-REPEAT` with
`"path": "SFIX-REPEAT.txt"`, and the capture's pin matches the checked-in bytes:

```
$ sha256sum corpus/instruments/limb-fixtures/sr/occurrence-not-unique/SFIX-REPEAT.txt
a1a041334372a0539c928f0260999051dab3a04415c972174c21f0e4e7bbf723  corpus/instruments/limb-fixtures/sr/occurrence-not-unique/SFIX-REPEAT.txt
$ grep sha256 corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json
      "sha256": "a1a041334372a0539c928f0260999051dab3a04415c972174c21f0e4e7bbf723"
```

Capture body (5 lines; the quoted sentence is lines 1 and 4, i.e. exactly twice):

```
Repeated unanchored fixture quote.
Padding line one.
Padding line two.
Repeated unanchored fixture quote.
Padding line three.
```

## 1. Counter's line vs hand re-derivation

Counter, run in the lane (scratch-only by design; it writes nothing into the tree):

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && python3 corpus/instruments/limb-mutation-check.py --ledger corpus/instruments/limb-ledger.json; echo "counter_exit=$?"
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
counter_exit=0
```

(The 12 non-target limb lines belong to sibling seats; recorded only as the surrounding run.)

Hand re-derivation, own scratch copy, kill command expanded with `{inst}`/`{root}` as the row says:

```
$ S=$(mktemp -d /tmp/sr-occ-hand.XXXXXX); cp -a corpus "$S/corpus"; echo "$S" > /tmp/sr-occ-hand.path
$ sha256sum "$S/corpus/instruments/source-recheck.py"
fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003   # == the lane instrument
$ python3 "$S/corpus/instruments/source-recheck.py" --manifest "$S/corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json" --source SFIX-REPEAT; echo "live_exit=$?"
SFIX-REPEAT:sha256 OK
SFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique
live_exit=1
```

`signal` check on stdout+stderr for the unmutated run: `reason=occurrence-not-unique` present → `y`.

Mutation applied by hand with python — exactly-once assertion, byte-identity check, `py_compile`:

```python
find    = '        if occurrences > 1 and anchor_verdict_result != "ok":\n'
replace = '        if occurrences > 1 and anchor_verdict_result != "ok" and anchor_verdict_result != "missing":  # SR-occurrence-not-unique mutant\n'
data = open(inst, "rb").read()
n = data.count(find.encode()); print("find_count=%d" % n); assert n == 1
mut = data.replace(find.encode(), replace.encode(), 1); assert mut != data
open(inst, "wb").write(mut)
py_compile.compile(inst, doraise=True)
```

```
find_count=1
before_sha256=fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003
after_sha256=8477c0cdc46f1e4b9d51d4b5e902fc0166bea6247ae72fec675d8f597f7da636
bytes_changed=True
py_compile=ok
$ python3 "$S/corpus/instruments/source-recheck.py" --manifest "$S/corpus/instruments/limb-fixtures/sr/occurrence-not-unique/manifest.json" --source SFIX-REPEAT; echo "mutant_exit=$?"
SFIX-REPEAT:sha256 OK
SFIX-REPEAT:Q1 OK occurrences=2 anchor=MISSING
mutant_exit=0
```

Signal on the mutant run: `reason=occurrence-not-unique` absent → `n`.

Repeatability (the counter runs each side twice and requires a stable `(exit, signal)`):

```
$ for r in 1 2; do python3 .../source-recheck.py --manifest .../occurrence-not-unique/manifest.json --source SFIX-REPEAT > /tmp/live.$r.out 2>&1; echo "live_run$r exit=$?"; done
live_run1 exit=1
live_run2 exit=1
$ for r in 1 2; do python3 .../source-recheck.py --manifest .../occurrence-not-unique/manifest.json --source SFIX-REPEAT > /tmp/mut.$r.out 2>&1; echo "mut_run$r exit=$?"; done
mut_run1 exit=0
mut_run2 exit=0
$ diff /tmp/live.1.out /tmp/live.2.out && echo live_stable
live_stable
$ diff /tmp/mut.1.out /tmp/mut.2.out && echo mut_stable
mut_stable
```

Hand verdict: `live=1/y mutant=0/n verdict=killed` — **byte-for-byte the counter's line**
(`LIMB SR-occurrence-not-unique live=1/y mutant=0/n verdict=killed`). Step-(1) difference: **none**,
no defect.

## 2. Isolation: the kill is a limb-specific behavioural flip, not a crash

`diff` of the two unmutated-vs-mutated fixture runs (2 stdout lines each, both stderr empty):

```
2c2
< SFIX-REPEAT:Q1 MISMATCH reason=occurrence-not-unique
---
> SFIX-REPEAT:Q1 OK occurrences=2 anchor=MISSING
```

Exactly one line of two differs. The mutant still prints the instrument's normal pre-gate banner
(`SFIX-REPEAT:sha256 OK`, i.e. the record was accepted, the pin verified, B1 did not preempt), it does
not raise, and its exit is 0 — the difference is the B2 verdict on a twice-occurring unanchored quote
falling through to the `if assertion["quote"] in source_text:` success branch (`:201-203`) instead of
the fatal branch (`:192-199`).

Two scope checks confirm the mutation is confined to the non-unique-unanchored path — unmutated and
mutated copies print **identical** output on everything else I could reach:

```
--- LIVE / MUT: stem-mismatch fixture (B1 path) ---
SFIX-STEM:manifest MISMATCH reason=stem-mismatch      # both, exit=1 both
--- LIVE / MUT: real corpus, round-31 manifest --source S048 ---
S048:sha256 OK                                         # identical 9-line output, exit=0 both
S048:Q1..Q8 OK occurrences=1
--- LIVE selftest ---  selftest cases=10 failures=0    (exit 0)
--- MUT  selftest ---  selftest cases=10 failures=1    (exit 1)
  SELFTEST double-occurrence FAIL expected-exit=1 observed-exit=0 expected-ids=S900:sha256,S900:Q1 observed-ids=S900:sha256,S900:Q1
```

So the instrument's own suite also kills this mutant, on exactly the one case that names the limb
(`corpus/instruments/source-recheck.py:355-358`, `expected_substr="reason=occurrence-not-unique"`),
while the other nine cases stay green — the kill is attributable to the limb, not to collateral breakage.

## 3. Discrimination: other one-limb mutants of the same limb

Each row is a fresh scratch copy of the landed `corpus/`, one find/replace asserted exactly once,
`py_compile` ok in all cases, then the scale's kill command under test (the row's fixture command)
and, separately, the instrument's own `--selftest`.

| mutant | site | fixture kill run | row verdict | selftest FAIL cases |
|---|---|---|---|---|
| M1 = ledger row (add `and != "missing"`) | `:192` gate | exit 0, signal n, prints `OK occurrences=2 anchor=MISSING` | killed | `double-occurrence` |
| M2 = anchor-verdict flip (`"missing"` → `"unique"`) | `:107` verdict | exit 1, signal n, **`KeyError: 'unique'` traceback** after `sha256 OK` | killed (by crash) | `double-occurrence` |
| M3 = gate threshold (`> 1` → `> 2`) | `:192` gate | exit 0, signal n, `OK occurrences=2 anchor=MISSING` | killed | `double-occurrence`, `double-occurrence-out-of-range`, `double-occurrence-broken` |
| M4 = gate broadened (`> 1` → `>= 1`) | `:192` gate | exit 1, signal **y**, output byte-identical to live | **survivor** | `clean` (`expected-exit=0 observed-exit=1`) |
| M5 = reason string (`reason=occurrence-not-unique` → `reason=anchor-missing`) | `:194` reason map | exit 1, signal n | killed (signal only) | `double-occurrence` |

Reading:

- The row is **not** a single-shape special case: three distinct mutant shapes on the gate itself
  (M1 add-a-conjunct, M3 threshold, M4/M5 at neighbouring sites) are seen by the instrument, and M3
  is additionally killed by three selftest cases.
- **M4 is a real coverage boundary of the row's kill command, not of the limb.** Broadening the gate
  to `occurrences >= 1` is observationally identical on this fixture (the quote occurs twice, so both
  `> 1` and `>= 1` enter the gate); the row's fixture command therefore reports `survivor` for it. The
  instrument's selftest does kill it — the `clean` case (a unique, unanchored quote) turns from
  `expected-exit=0` to `observed-exit=1` because `"unique"` is not a key in `anchor_reasons`
  (`:193-197`). So the limb is load-bearing beyond the fixture command; only the fixture is narrow.
  This does not weaken the row: the row's own mutant is killed, as measured.
- **M2 exposes a criterion property of the counter for the L1 to route (counter file is not this
  seat's write scope):** M2 exits 1 (equal to `live_exit`) and is killed only because its signal is
  absent — the kill is an uncaught `KeyError`, not a graceful rejection. The contract's kill rule
  (`exit != live_exit` **or** `signal` mismatch) accepts such crash-only kills. The landed row is not
  affected (its mutant exits 0 with a clean banner), but a future ledger row whose live baseline
  exits non-zero could be "killed" by a mutant that merely crashes. Available hardening, for the
  owning executor: require the mutant run to contain no `Traceback` line, or require the mutant's
  emitted record lines to be the expected ones. Not applied here.

## 4. Verdict

**holds** for the ledger row `SR-occurrence-not-unique`.

- (1) hand re-derivation == counter line == `live=1/y mutant=0/n verdict=killed`; `find` occurs
  exactly once (`:192`), mutated bytes differ (`8477c0cd…` vs `fd2e01e8…`), the mutant compiles, the
  unmutated run matches the row's `signal`, and both runs are stable across repeats. No defect.
- (2) discrimination: the row's shape is not lone (M3, M5 also killed on this limb, M3 by three
  selftest cases); the row's fixture command is blind to M4 (`>= 1`), which the instrument's own
  `clean` case kills — recorded above as a boundary of the kill command, not of the limb.
- (3) isolation: one differing line of two, empty stderr, normal `sha256 OK` banner, exit 0; the
  stem-mismatch fixture and the real S048 round-31 manifest are byte-identical between live and
  mutant; the selftest differs on exactly the `double-occurrence` case. Not a crash, not collateral.

Blockers: none. Scratch removed after measurement — every prefix this seat created is gone
(`ls -d /tmp/sr-occ-hand.* /tmp/sr-live*.* /tmp/sr-disc-* /tmp/sr-st-* /tmp/sr-fl-*` → all five
"no such file or directory"). One foreign file remains at `/tmp/sr-only-ledger.json` (mtime
21:22, older than this seat's first probe; not created here) and was left untouched. Lane tree
unchanged: the three hashes above are identical to the seat-start values and `git status --porcelain`
lists no modified tracked file (only untracked wave artifacts the L1 owns).
