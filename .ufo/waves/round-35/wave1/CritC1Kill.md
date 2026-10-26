# CritC1Kill — round 35, falsification of claim C1 (depth:verifiability)

Seat: critic `CritC1Kill`, leaf of round-35 wave 1. Assignment: attack C1's declared after-state by
constructing states that satisfy it while violating its kill rule, for five named attacks; state
caught (pass) or not (gap) per attack; verdict.

- Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`, working copy `qwsxkpzx 1de4007f`, parent
  `lprkqvpk da2d3c68` (dispatch). Lane base `3266c993`, claims freeze `617496b9`.
- Method: read the seven checks and the `--selftest` machinery in
  `corpus/instruments/r35-defect-closure.sh`; then build minimal trees in scratch
  (`/fast/scratch/hyaku/kasegi-r35/CritC1Kill/`) and run the suite's `--root` mode against them. No
  lane file was modified; the L1 commits.
- **Byte identity drift inside the review window.** First read (03:36 mtime) was 30284 B with a
  two-mutant D1; the tested bytes are 32148 B / 773 lines, mtime `2026-10-26 03:39:31 -0300`,
  sha256 `d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304`. Every result below is
  against a scratch copy of those bytes (`.../CritC1Kill/snap/r35-defect-closure.sh`), so it is
  pinned; the digest matters for attack 1.
- No tools installed; no packages needed (bash, git, python3 as present).

## Report

### 1. Tree state measured (2026-10-26T06:41:34Z)

```
$ sha256sum corpus/instruments/r35-defect-closure.sh
d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304  corpus/instruments/r35-defect-closure.sh
$ wc -l < corpus/instruments/r35-defect-closure.sh
773
$ bash corpus/instruments/r35-defect-closure.sh
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=3 open=0
D2 check=erratum-row=1,erratum-mean=2,row-bytes=1 open=0
D3 check=registry-r-defect-closure=4,registry-kill-rule=4 open=0
D4 check=tracked=0,provenance=1 open=1
D5 check=erratum-file=present,discriminating-invocation=5,per-id-occurrences=5 open=0
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=4/7 exit=1
exit=1
```

D4/D6/D7 are the limbs the L1's integration commit still owes (D4 needs the commit itself). **This
is a wave snapshot, not a verdict**: the claim's `closed=7/7` is currently unmet for the declared
reason, and nothing below treats that as a defect.

Fixture set landed during the review (`corpus/instruments/r35-fixtures/` now holds `D1`…`D7`,
`clean`, `two-defect`, `fixtures.json`, `b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113`).

### 2. Base-tree control (the claim's fail-closed limb)

`git archive 3266c993 | tar -x -C /fast/scratch/hyaku/kasegi-r35/CritC1Kill/base`, then:

```
$ bash corpus/instruments/r35-defect-closure.sh --root .../base
D1 check=placeholders=1,lane-hash-markers=0,correction-c1c6a5f=0 open=1
D2 check=erratum-row=0,erratum-mean=0,row-bytes=1 open=1
D3 check=registry-r-defect-closure=0,registry-kill-rule=0 open=1
D4 check=tracked=0,provenance=0 open=1
D5 check=erratum-file=absent,discriminating-invocation=0,per-id-occurrences=0 open=1
D6 check=dead-seat-sentence=1,correction-round-35=0 open=1
D7 check=supersedes-R22=0,supersedes-R23=0 open=1
closed=0/7 exit=1          exit=1
```

The claim's `closed=0/7 exit=1` at base reproduces. (D4's limb reads `git ls-files` in the root's
own repo; a git-free export therefore reads `tracked=0`, which is why the base control holds — the
fixture README states this construction, and it is what the `--selftest` uses.)

### 3. `--selftest` at tip

```
$ KASEGI_SCRATCH=... bash corpus/instruments/r35-defect-closure.sh --selftest
selftest case=D1 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D2 live=pass fixture=rejected mutants=3/3 others=6/6 verdict=pass
selftest case=D3 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D4 live=fail fixture=rejected mutants=2/2 others=6/6 verdict=fail
selftest case=D5 live=pass fixture=rejected mutants=2/2 others=6/6 verdict=pass
selftest case=D6 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest case=D7 live=fail fixture=rejected mutants=0/2 others=6/6 verdict=fail
selftest control=clean closed=7/7 verdict=pass
selftest control=two-defect closed=5/7 failed=D1,D2 verdict=pass
selftest cases=7 failures=3 control-failures=0
selftest judge=forged-summary rejected=1
selftest judge=forged-caselines rejected=1
selftest judge=short-report rejected=1
selftest judge=fake-suite rejected=1 path=.ufo/waves/round-35/c1-controls/fake-suite.sh output=cases=7 failures=0
selftest judge=fake-plain rejected=1 output=closed=7/7 exit=0
selftest problem=self-report status=1
exit=1
```

D6/D7 `mutants=0/2` is **attributable to the unlanded limbs** (mutants are built from the live tree;
with the live limb already open, a reopened clause cannot isolate — `verdict=unexpected rc=1`). It is
not a check defect.

### 4. The five attacks

Every attack tree was built in scratch and run with the pinned suite copy via `--root`.

| # | attack (as assigned) | landed check catches it? | measured |
|---|---|---|---|
| 1 | suite printing `closed=7/7` from seven vacuous checks | **PASS for vacuous check bodies; GAP for a substituted artifact** | see 4.1 |
| 2 | D5 erratum carrying both literals but not fixing the wording | **GAP** | `D5 … open=0` on a 63-byte headings-only file |
| 3 | D4 where results.json is tracked but is a placeholder | **GAP** (check); identity evidence exists in prose only | `D4 check=tracked=1,provenance=1 open=0` on `{}` + a two-line note |
| 4 | D1 prose gone but the correction names a wrong hash | **PASS in its literal form; GAP once the right literal appears anywhere in the file** | `D1 … correction-c1c6a5f=1 open=0` on a repudiation sentence that cites `deadbeef…` |
| 5 | D7 row mentioning supersedes-R22 without correcting the grounding | **GAP** | `D7 check=supersedes-R22=1,supersedes-R23=1 open=0` on a negation sentence |

#### 4.1 Attack 1 — vacuous checks vs a forged artifact (two branches, opposite answers)

Branch (a), vacuous check **bodies inside the real suite**: caught, twice.

```
# one check made vacuous (check_d7() { ( exit 0 ); } injected before the driver)
selftest detail=D7 fixture reason= verdict=unexpected rc=0
selftest detail=D7 mutant=supersedes-R22 reason= verdict=unexpected rc=0
selftest detail=D7 mutant=supersedes-R23 reason= verdict=unexpected rc=0
selftest case=D7 live=pass fixture=pass mutants=0/2 others=6/6 verdict=fail
selftest cases=7 failures=3 control-failures=0                       exit=1

# all seven made vacuous
selftest case=D1..D7 live=pass fixture=pass mutants=0/N verdict=fail   (7 lines)
selftest control=two-defect closed=7/7 failed=none verdict=fail
selftest cases=7 failures=7 control-failures=1                       exit=1
```

The mutant limb is the discriminator and it works: a check that does not read its clause cannot
reject the mutant that reopens it, and the two-fixture control also flips. Attack 1(a) is **caught**.

Branch (b), a **substituted artifact** that prints the summary without running anything: not caught.
The committed do-nothing control, copied under the suite's own name, prints exactly the strings the
frozen kill rule reads:

```
$ bash .../a1c-fake-as-suite/r35-defect-closure.sh --selftest
cases=7 failures=0 exit 0                     exit 0
$ bash .../a1c-fake-as-suite/r35-defect-closure.sh
closed=7/7 exit=0                             exit 0
# 361 bytes, sha256 292aaac048c9cacff081c24b54fd71fc67a86d3c6ab6845398e0e2856c5be121
# vs the real suite: 32148 bytes
```

The suite's own judge is **text-only**, so it also accepts a well-formed replica of its own report.
Sourcing the pre-`run_selftest()` half of the pinned suite and feeding it a fabricated report (seven
`selftest case=D<i> live=pass fixture=rejected mutants=1/1 others=6/6 verdict=pass` lines, seven
`fixture reason=` lines copied from the suite's own fixture output, seven mutant detail lines, the
`selftest cases=7 failures=0` line):

```
report_ok(verbatim-forgery) exit=0        # accepted; report sha256 6b52906d19aca46848366e6fbf0b5e37313d87cddeef6ab9ff9c4317a71f8fba
plain_report_ok(forged plain report) exit=0
```

The judge has no secret: its acceptance test is a function of the report text (`grep` shapes, per-id
`fix_re` match, mutant-count cross-check, `others=6/6`, final summary line). A forger who reads the
committed source reproduces all of it. And **no byte-identity binding exists**: grep over
`.ufo/waves/round-35/` for a sha256/digest of `r35-defect-closure.sh` finds none; `SKILL.md`
pins only the *round-34* instruments (`809aaf90…`, `c279d952…`); `corpus/instruments/r35-fixtures/fixtures.json`
is never read by the suite (`grep -n 'fixtures.json' corpus/instruments/r35-defect-closure.sh` → no
match), so fixture bytes are not pinned either. Attack 1(b) is a **GAP**: the kill rule's own proof
obligation ("proved by the suite's own --selftest") is discharged by the artifact under test.

#### 4.2 Attack 2 — D5 both literals, no fix

Built: `.ufo/waves/round-35/claims-erratum-d5.md` containing exactly

```
# erratum

## discriminating invocation

## per-id occurrences
```

```
D5 check=erratum-file=present,discriminating-invocation=1,per-id-occurrences=1 open=0
```

63 bytes, sha256 `a5e61541280f9b960e6d072b86f4afcffa5fd85b23aa7cf161522f7174f1f85b`. The frozen
after-predicate says the file "carries the discriminating-invocation and per-id occurrences
**statements**"; headings are not statements, yet the check accepts them. **GAP** (check weaker than
its own claim text). The landed file is substantive (`grep -c 'source-recheck.py'` → 5,
`grep -c 'MISMATCH reason=quote-not-found'` → 3, sha256 `0d304b923d4953441d765f05d2b4ed55bd9b4b8b8112ca2387e6d69a05046c8a`),
so the live limb is fine; the check is what is not discriminating.

#### 4.3 Attack 3 — D4 tracked but placeholder

Built: `.ufo/waves/round-34/wave1-results.json` = `{}` (2 bytes, sha256
`44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`) plus a two-line provenance note,
`git init && git add -A`:

```
D4 check=tracked=1,provenance=1 open=0
```

**GAP in the check**: no size floor, no row count, no digest compare. The identity evidence *does*
exist and is one command — the landed note carries the right digest and a verifier line:

```
$ printf '%s  %s\n' 3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4 \
    .ufo/waves/round-34/wave1-results.json | sha256sum -c -
.ufo/waves/round-34/wave1-results.json: OK        exit=0
$ python3 -c 'import json;d=json.load(open(".ufo/waves/round-34/wave1-results.json"));print(d["seats"],len(d["results"]))'
65 65
$ git ls-files .ufo/waves/round-34/wave1-results.json | wc -l
0        # pre-integration, as expected
```

So the *record* survives attack 3; the *counter* does not test it. Note for any correction: the note's
**first** 64-hex string is `6b3604cb6d5aca94e68f2b2a66aaaaee5ed9c3e2856ba9f7c5c13cd32b06de83` — the digest
of `wave1/ExecRegressionC1.md`, not of the results file (line 59). A naive "first hex in the note"
parser would bind the wrong file; the field to read is the `| sha256 | `3afa3581…` |` identity row (line
67) or the `sha256sum -c` line.

#### 4.4 Attack 4 — D1 correction names a wrong hash

Literal form **is caught**: measured on a tree whose only citation is `deadbeef…` —

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=0 open=1     exit=1
```

But the check is `grep -c -F 'c1c6a5f' SCORECARD.md` — anywhere in
the file, any context. Built:

```
**Final lane commit: `deadbeefcafe0123456789abcdef0123456789ab`**

Note: the round-34 tip c1c6a5f could not be confirmed by this seat.
```

```
D1 check=placeholders=0,lane-hash-markers=0,correction-c1c6a5f=1 open=0
```

A **repudiation** of the hash satisfies a clause whose claim text says "an appended **correction
naming** c1c6a5f". **GAP** in the discriminating sense (it cannot separate citation from mention).
Slot-bound probe (smallest correction shape, measured): restricting the search to the slot keeps the
live tree passing and rejects the attack tree —

```
$ sed -n '/^## Round 34 /,$p' SCORECARD.md | grep -A1 'Final lane commit:' | grep -c c1c6a5f
1        # live: the slot's next line is `c1c6a5f826d…` (line 1129–1130; also 1241)
$ sed -n '/^## Round 34 /,$p' .../a4-d1-wronghash/SCORECARD.md | grep -A1 'Final lane commit:' | grep -c c1c6a5f
0
```

(The live slot spans two lines: `**Final lane commit:` then `` `c1c6a5f…`** ``, so the bind must allow
one line of continuation; a single-line regex over the slot returns 0 on the landed bytes.)

#### 4.5 Attack 5 — D7 mention without correcting the grounding

Built: `corpus/QUALITY.md` holding the R22/R23 rows verbatim plus

```
Round-35 note: nothing here supersedes R22 and nothing supersedes R23; both keep their
original grounding and neither row is corrected.
```

```
D7 check=supersedes-R22=1,supersedes-R23=1 open=0
```

sha256 `6af497c0ed7cc303e7ee00d5d3d39ec325a9dfe70ce66179dfffa1f6a509ae65`. A **negation** satisfies
"carries appended supersession rows". **GAP**. (The L1's build spec already routes the content test to
`RevD5D6D7` — "grounding text is correct (M34-3 for R22; round-34 lesson for R23)" — so the content
authority exists; it is a reviewer instruction, not a runnable invocation, which is exactly the
distinction D5's erratum draws for frozen clauses.)

#### 4.6 Two same-class instances found while probing (not in the assigned five)

- **D2**: a SCORECARD carrying the stale row plus `the string \`round-34 depth:density row\` and the
  figure 201.2 in this sentence are not a measurement … no erratum is filed` →
  `D2 check=erratum-row=1,erratum-mean=1,row-bytes=1 open=0` (sha256
  `17df3d8f133cabc627c169c0517e76717f5efa89343c3c46871709e44a4d6687`). Same presence-only class.
- **D3**: an `SKILL.md` reading `Prose: r-defect-closure and kill-rule-check are deliberately NOT in
  the Gates & probes registry.` → `D3 check=registry-r-defect-closure=1,registry-kill-rule=1 open=0`
  (sha256 `1c831c53a6cdd421857f69313047a3a77f2a8f9a0bc83820054e56ee62ca0ebe`). The clause is
  "registered at the Gates & probes registry home"; the check reads the whole file, so the base-open
  fact (base has 0 occurrences) is what carries it, not the registry location.

### 5. Findings and the smallest safe correction for each

| id | finding | smallest safe correction (append-only; nothing here edits frozen claims) |
|---|---|---|
| F-1 | C1's suite has no byte identity. `--selftest` is a text-shaped judge; a 361-byte replica prints the kill rule's strings, and `report_ok` accepts a report replica (`exit=0`). | L1 records, in the integration receipt and in one landed command, `sha256sum corpus/instruments/r35-defect-closure.sh corpus/instruments/r35-fixtures/fixtures.json` taken **after the last edit** (the suite moved 30284→32148 B inside this wave), and the C1 after-state names that digest; the plain run is read only alongside a passing `sha256sum -c`. One line, no suite change. |
| F-2 | D1's clause is a file-wide literal, so a repudiation passes. | Bind the hash to the slot: within `^## Round 34 ` to EOF, `grep -A1 'Final lane commit:' | grep -c c1c6a5f` ≥ 1 (measured 1 on live, 0 on the attack tree), plus one mutant. |
| F-3 | D5's clause accepts headings; the predicate's noun is "statements". | Require one executable artefact per statement already present in the landed erratum: `grep -c 'MISMATCH reason=quote-not-found'` ≥ 1 **and** `grep -c 'source-recheck.py'` ≥ 1 (live 3 / 5). Mutant: delete the invocation block. |
| F-4 | D4's clause ignores identity; `{}` passes. | Compare `sha256sum` of the results file against the digest in the note's `| sha256 |` identity row (not the note's first 64-hex — line 59 is `ExecRegressionC1.md`'s digest), and require `seats == len(results)` ≥ 65 from the parsed JSON. Mutant: flip one byte. |
| F-5 | D7's clause accepts a negation; D2/D3 have the same shape. | D7: require the corrected grounding token the reviewer already tests (`M34-3` on the R22 row, `round-34` lesson on the R23 row) inside a row that begins `\| R2`. D2/D3: same slot/noun binding (D2's erratum inside `^## Round 34`; D3's rows inside the registry table region). |

Proportionality: F-2…F-5 are **check-vs-own-text** gaps, not new defects — the live landings for
D1, D2, D5 are substantive and the D4 record is digest-verifiable (measured above); D6's clause is
already a conjunction with a deletion count (`dead-seat-sentence=0`), which is why it does not have
this shape. F-1 is the only finding that can defeat the claim outright, and it is one command away
from closed.

### 6. What I did **not** find

- The mutant limb is real work, not a summary: 16 clause mutants, one per clause, each built from the
  live tree with exactly one clause reopened, `isolate_ok` requiring the other clauses closed, and two
  non-case controls (`clean` 7/7; `two-defect` exact D1,D2). A vacuous check cannot survive it
  (4.1a).
- The base control is not vacuous: `closed=0/7 exit=1` reproduces on a `git archive` of `3266c993`
  (2).
- The `filled by the L1` count is 0 and `c1c6a5f826d2425446347173de527c42991b78b0` is genuinely the
  round-34 lane tip (`jj log`: `vnxmnxml c1c6a5f8 "round-34: late ExecRegressionC1 receipt + lesson/LOG
  post-commit errata"`), so D1's pin is not false provenance.
- No `<LANE_HASH>` marker in `SCORECARD.md` (`grep -c` → 0).

### 7. File digests measured (tip, 2026-10-26T06:41Z)

```
d7ad84384eb4b3fa2f5737e0597cbc9cdf3ded1eac867f6131886b790d38a304  corpus/instruments/r35-defect-closure.sh (32148 B, 773 lines)
b9a07afa1bed7b15b1754e7defee87cdb6233806d0b94b80d8a0acb4529da113  corpus/instruments/r35-fixtures/fixtures.json
51337bf1fd5da7a5aebb626fe8c5fd520cce40209d79537324cf9d08a990efc7  SCORECARD.md
807cc714d01587e03fb3025ad04aa8434980b3e5804bc3f639d0f4935f8b74a8  corpus/QUALITY.md
0d304b923d4953441d765f05d2b4ed55bd9b4b8b8112ca2387e6d69a05046c8a  .ufo/waves/round-35/claims-erratum-d5.md
3afa3581afb14abaf49297b08b66aaac48ddc7f450a983616fc3444047d981d4  .ufo/waves/round-34/wave1-results.json (312874 B, 65 rows)
e1c4430133adeb58b8d3b3af9edcb49739eacd3f40536dca529105c609e86c98  .ufo/waves/round-34/wave1-results.json.provenance.md
```

Scratch (`/fast/scratch/hyaku/kasegi-r35/CritC1Kill/`, including the pinned suite copy, the base
export and the eight attack trees) — deleted after this receipt was written; nothing of it remains on
disk.

## Verdict (seat-level, C1 only)

**C1 survives attack 1(a), the base control and attack 4's literal form; it does not survive attack
1(b), 2, 3 (check-level), 4 (with a mention present) or 5.** Concretely: the closure suite is a real
fail-closed counter with a genuine 18-mutant selftest, but (i) nothing binds the counter's own bytes,
so the frozen kill rule's "proved by the suite's own --selftest" is discharged by the artifact under
test, and (ii) three of the seven closure clauses are file-wide literal greps that a negation or a
heading satisfies, which is the same "no discriminating invocation" class D5's erratum was filed to
correct. The live tree at read time is `closed=4/7` with D4/D6/D7 pending the L1's integration
commit; the depth:verifiability after-state as declared is therefore not yet measurable, and on
F-1 it would not be measurable even at 7/7 unless the suite digest is pinned. Corrections F-1…F-5 are
one command each and are append-only; the L1 decides whether they land this round or the next.
