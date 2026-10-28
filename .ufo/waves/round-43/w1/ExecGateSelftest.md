# ExecGateSelftest — claim-package-check.py `--selftest` (ten graded cases)

Round 43 · kasegi-shokunin · claim C2 (coverage) · axes: coverage, depth:verifiability
Seat role: executor (leaf). Parent: KasegiR43.

## Deliverables

| file | lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecGateSelftest.selftest.py` (lands pasted into `corpus/instruments/claim-package-check.py`) | 616 | `04951ca0e72050725fc01a16ba1e42d7a52bd29bb0ae653b164a39ed39b57b17` |
| `.ufo/waves/round-43/w1/ExecGateSelftest.transcript.txt` | 78 | `b4e8b2d4f70e57270ba4cbcef94a54db808462bfdbc91b68bbdf181d085363f9` |

Landing: paste the whole file byte-exactly above the gate's last comment line

```
# <!-- selftest-body-paste-anchor: paste run_selftest(...) ABOVE this guard -->
```

`selftest_dispatch()` resolves `globals()['run_selftest']` and calls
`run_selftest(os.path.abspath(__file__))`; fixtures default to
`<gate dir>/fixtures/claim-package`. The pasted body adds no `sys.exit` line and
its bottom guard is inert inside the gate (it checks
`not any(k in globals() for k in ("selftest_dispatch", "main"))`).

## Case grammar (stdout, one line per case, then the summary)

```
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=R-FILES verdict=pass
…
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=0
```

`detail=<one token>` is appended only to a failing case. Exit 0 only at
`failures=0`. A defect case passes only when the gate exits 1, prints exactly the
eight `RULE` lines, prints `verdict=DEFECT`, and the ONLY failing rule is the
fixture's expected rule — an extra or different failing rule is
`detail=wrong-rule` and a selftest failure, not a pass.

Expectation resolution, in order: `<fixture>/expected-rule` (one bare rule id),
then `<fixtures root>/index.txt` / `INDEX.txt` / `ExecGateFixtures.index.txt`
line `<fixture-name> <RULE>`, then the defect class token in the directory name
(missing-file/digest/negative/escape/redaction/custodian/reviewer/marker/secret).
All three sources agree in the delivered fixture set (9/9 dirs carry
`expected-rule`, the index repeats it, the names carry the class token); a
declaration that contradicts the name fails the case (`expected-mismatch`).

## Isolation: reads AND writes, per case

Each case is copied to `$TMPDIR/claim-pkg-selftest-*/case-<nn>-<fixture>/pkg`; the
gate child runs with `cwd` = that case dir and `PYTHONPATH` = an audit dir whose
`sitecustomize.py` appends every `open` / `os.scandir` / `os.listdir` target to
`$CLAIM_PKG_SELFTEST_AUDIT_LOG` as it happens, tagged `R` or `W` (write classified
from the `open` audit event's mode/flags). After each run the selftest asserts:

- every audited path under the work root resolves inside the case dir
  (`detail=sibling-read` / `sibling-write`);
- nothing at all is read or written under the canonical fixtures root
  (`detail=source-fixture-read` / `source-fixture-write`, with the tree-digest
  guard reporting `detail=fixtures-mutated` when bytes actually changed);
- every write resolves inside the case dir or the audit dir
  (`detail=external-write` otherwise, including a pinned `/tmp` path);
- a missing log is `detail=isolation-unverified` (fail closed).

Measured with `--work` retained, against the delivered gate + fixture set (the run
is green, so this is the read/write profile of a passing gate):

```
$ TMPDIR=$S/tmp python3 selftest.py --gate delivered/claim-package-check.py \
    --fixtures delivered/fixtures/claim-package --work $S/tmp/ev
selftest cases=10 failures=0

case-01-defect-1-missing-file read-in=20 read-out=1 write-in=0 write-out=0 R:audit
case-02-defect-2-digest      read-in=21 read-out=0 write-in=0 write-out=0
case-03-defect-3-negative    read-in=21 read-out=0 write-in=0 write-out=0
case-04-defect-4-escape      read-in=20 read-out=0 write-in=0 write-out=0
case-05-defect-5-redaction   read-in=21 read-out=0 write-in=0 write-out=0
case-06-defect-6-custodian   read-in=21 read-out=0 write-in=0 write-out=0
case-07-defect-7-reviewer    read-in=21 read-out=0 write-in=0 write-out=0
case-08-defect-8-marker      read-in=21 read-out=0 write-in=0 write-out=0
case-09-defect-9-secret      read-in=21 read-out=0 write-in=0 write-out=0
```

`audit` is the instrumentation's own `sitecustomize` dir, on the explicit
allowlist beside the gate file — not a sibling case dir. Case 1 opens one file
fewer because `claim_checklist.md` is absent by construction. The gate itself
performs zero writes.

## Evidence A — the gate's own `--selftest` (transcript block A, verbatim)

```
$ python3 claim-package-check.py --selftest
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=R-FILES verdict=pass
selftest case=2 class=defect fixture=defect-2-digest expected=R-MANIFEST observed=R-MANIFEST verdict=pass
selftest case=3 class=defect fixture=defect-3-negative expected=R-MANIFEST observed=R-MANIFEST verdict=pass
selftest case=4 class=defect fixture=defect-4-escape expected=R-MANIFEST observed=R-MANIFEST verdict=pass
selftest case=5 class=defect fixture=defect-5-redaction expected=R-REDACT observed=R-REDACT verdict=pass
selftest case=6 class=defect fixture=defect-6-custodian expected=R-CUSTODIAN observed=R-CUSTODIAN verdict=pass
selftest case=7 class=defect fixture=defect-7-reviewer expected=R-STATUS observed=R-STATUS verdict=pass
selftest case=8 class=defect fixture=defect-8-marker expected=R-REPORT observed=R-REPORT verdict=pass
selftest case=9 class=defect fixture=defect-9-secret expected=R-NOSECRET observed=R-NOSECRET verdict=pass
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=0
exit=0
```

Built from the delivered bytes: gate core
`.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py` (802 lines,
`8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6`; the owner
re-delivered it during the wave — `bdb50a82…` earlier — and the transcript runs
the current bytes) with this seat's body pasted at the anchor; fixtures
`ExecGateFixtures.defect-<k>` (nine dirs) + `ExecGateFixtures.index.txt` + the
`ExecExemplarPackage.*` exemplar, laid out under `fixtures/claim-package/`.
Per-fixture content digests are pinned in the transcript. Independently of the
selftest, each delivered fixture measures exactly one failing rule under the
delivered gate:

```
defect-1-missing-file  R-FILES      exit=1
defect-2-digest        R-MANIFEST   exit=1
defect-3-negative      R-MANIFEST   exit=1
defect-4-escape        R-MANIFEST   exit=1
defect-5-redaction     R-REDACT     exit=1
defect-6-custodian     R-CUSTODIAN  exit=1
defect-7-reviewer      R-STATUS     exit=1
defect-8-marker        R-REPORT     exit=1
defect-9-secret        R-NOSECRET   exit=1
```

and the assembled exemplar prints `rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0`.

## Evidence B — the degenerate always-pass control is rejected (transcript block B)

The control is a stub that prints eight `RULE … verdict=pass` lines and
`verdict=WELL-FORMED exit=0` unconditionally. Replaying the same grading against it:

```
$ python3 selftest.py --gate always-pass.py --fixtures fixtures/claim-package
selftest case=1 class=defect fixture=defect-1-missing-file expected=R-FILES observed=none verdict=fail detail=verdict=well-formed
selftest case=2 class=defect fixture=defect-2-digest expected=R-MANIFEST observed=none verdict=fail detail=verdict=well-formed
selftest case=3 class=defect fixture=defect-3-negative expected=R-MANIFEST observed=none verdict=fail detail=verdict=well-formed
selftest case=4 class=defect fixture=defect-4-escape expected=R-MANIFEST observed=none verdict=fail detail=verdict=well-formed
selftest case=5 class=defect fixture=defect-5-redaction expected=R-REDACT observed=none verdict=fail detail=verdict=well-formed
selftest case=6 class=defect fixture=defect-6-custodian expected=R-CUSTODIAN observed=none verdict=fail detail=verdict=well-formed
selftest case=7 class=defect fixture=defect-7-reviewer expected=R-STATUS observed=none verdict=fail detail=verdict=well-formed
selftest case=8 class=defect fixture=defect-8-marker expected=R-REPORT observed=none verdict=fail detail=verdict=well-formed
selftest case=9 class=defect fixture=defect-9-secret expected=R-NOSECRET observed=none verdict=fail detail=verdict=well-formed
selftest case=10 class=degenerate fixture=always-pass expected=reject observed=rejected-9/9 verdict=pass
selftest cases=10 failures=9
exit=1
```

Case 10 is the same replay run inside every real `--selftest` call; it passes only
when the stub is rejected on all nine (9 rejected / 9 replayed, 0 accepted, 9/9
runs short of `WELL-FORMED`).

## Discrimination controls (the selftest is not vacuous; all measured)

```
# fixture that fails for the wrong reason
selftest case=1 ... expected=R-FILES observed=R-MANIFEST verdict=fail detail=wrong-rule
selftest cases=10 failures=1

# gate that lists its work-root sibling dir
selftest case=1 ... expected=R-FILES observed=R-FILES verdict=fail detail=sibling-read
selftest cases=10 failures=9

# gate that reads the canonical fixtures root instead of its copy
selftest case=1 ... expected=R-FILES observed=R-FILES verdict=fail detail=source-fixture-read
selftest cases=10 failures=9

# gate that prints only seven RULE lines
selftest case=1 ... expected=R-FILES observed=none verdict=fail detail=rules-printed=7
selftest cases=10 failures=9

# gate that writes a pinned /tmp path
selftest case=1 ... expected=R-FILES observed=R-FILES verdict=fail detail=external-write
selftest cases=10 failures=9

# gate that writes into the work root, outside its case dir
selftest case=1 ... expected=R-FILES observed=R-FILES verdict=fail detail=sibling-write
selftest cases=10 failures=9

# gate that opens a canonical fixture file for append (no bytes changed)
selftest case=1 ... expected=R-FILES observed=R-FILES verdict=fail detail=source-fixture-write
selftest cases=10 failures=9

# gate that actually mutates a canonical fixture
selftest case=1 ... expected=R-FILES observed=R-FILES verdict=fail detail=fixtures-mutated
selftest cases=10 failures=9
```

(Fixture tree verified restored afterwards: defect-1 digest
`acaa7b9346a6a021cc944c4a6da37ed5e51c1d33a01d5d084c08fb389926891d`, as pinned in the
transcript.)

Other fail-closed paths exercised: absent fixtures root (`fixtures-absent`,
`failures=10`, exit 1), absent gate (`gate-absent`, `failures=10`), crashing gate
(`rules-printed=0`), unknown argument (exit 2). With `TMPDIR` unset the work root
falls under `/tmp` and is removed on exit: `outside-tmpdirs before=0 after=0`.

## L1-routed items

1. **Collision with the gate's `RULES` dict** (mutant finding). Already fixed in
   the delivered bytes before the routing arrived: the file has no module-level
   `RULES`; its module-level names are `_SELFTEST_RULES`, `_SELFTEST_CLASSES`,
   `_SELFTEST_SUMMARY_RE`, `_SELFTEST_RULE_RE`, `_SELFTEST_AUDIT`,
   `_SELFTEST_DEGENERATE` (AST dump), plus `_selftest_*` helpers and the single
   seam `run_selftest`. The mutant composed an earlier body. Measured before the
   fix, then after: `RULE … detail=error:TypeError` ×8 → `selftest cases=10
   failures=0`.
2. **Silent acceptance of an out-of-dir write** (degenerate battery). Real gap:
   the audit hook recorded only paths, not access kind, so a write to a pinned
   `/tmp` path was invisible. Fixed: every `open` is classified read/write from
   `(mode, flags)`; writes are now failed as `external-write` / `sibling-write` /
   `source-fixture-write`, with the tree-digest guard still reporting
   `fixtures-mutated` for byte changes. Evidence in the control block above; the
   limit is stated in the deliverable's docstring ("writes anywhere outside its
   own dir").

## Scope discipline

- Lane writes: only `ExecGateSelftest.selftest.py`, `ExecGateSelftest.transcript.txt`
  and this receipt, all under `.ufo/waves/round-43/w1/`.
- No lane source tree, fleet root, `shokuknow`, sibling lane or PATH directory written.
- No mutating git/jj command (`git status`, `log`, `show`, `rev-parse` only).
- No tool installs needed; `pacman` not invoked.
- Scratch `/fast/scratch/hyaku/kasegi-r43/ExecGateSelftest/` removed before yield.

## Residual risk

- The transcript runs the *delivered* core + this body + the *delivered* fixtures,
  not the yet-unlanded `corpus/instruments/` paths; the preamble pins every input
  by sha256 and gives the exact splice/copy commands, so the landed run is one
  command away. If the core changes again before landing, re-run the one command;
  the pinned hashes are the check.
- Expectation authority is the fixture-side declaration cross-checked against the
  directory-name class token; disagreement fails the case rather than being accepted.
