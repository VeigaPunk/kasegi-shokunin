# ExecJ8Receipt — round-42 J8 receipt-integrity limb (family F-RCPT)

Seat: `ExecJ8Receipt`, round-42 wave 1, lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `5053a7f46de35784cff4b56756906e9014a38276`; frozen claims read from
`.ufo/waves/round-42/claims.json`. No mutating git/jj command was run anywhere; no tool was
installed; no network fetch was made; nothing outside the paths below was written.

## Deliverables

| file | lines | bytes | sha256 |
|---|---|---|---|
| `.ufo/waves/round-42/wave1/ExecJ8Receipt.sh` | 825 | 36383 | `011cc914661e32af75d90548fa712cfe4b170eee5492ec9da686307fb8cdd86e` |
| `.ufo/waves/round-42/wave1/ExecJ8Receipt.spec.txt` | 177 | 9200 | `1005bfb4876d5d6a4a7c3c2d5ae02d33dfb665fdf6ab2e6789f82489faddc686` |

`ExecJ8Receipt.sh` is sourceable (defines 29 `j8_*` functions plus the two entry points; it runs
its CLI only when executed directly) and provides:

* `check_j8 TREE REF` — the suite check. Prints the J8 payload on stdout; exit 0 green / 1 red.
* `make_receipt [--out PATH]` — writes the canonical receipt transcript (the bytes the run tees).
* `j8_verify FILE`, `j8_flags FILE`, `j8_forge_fixtures DIR` — the grader, the per-class verdict
  table and the committed fixture generator (honest control + one fixture per forgery class).

`ExecJ8Receipt.spec.txt` is the normative contract: the receipt's exact 33-line grammar, the
canonical bundle, the seven forgery classes with their loci, the producer rules and the host
contract (ordering + invariance).

## The receipt contract this seat fixes

```
all-gates v1
export-ref=<40 hex>                    the commit the transcript was teed at (J at Y = J + receipt)
suite-sha256=<64 hex>                  sha256 of corpus/instruments/r42-closure.sh as exported
time-basis=ref-commit                  there is no other time basis
run-utc=<YYYY-MM-DDTHH:MM:SSZ>         the committer instant (%ct) of the ref on line 2
J1 payload=<k=v,...> closed=<0|1>      lines 6..18, J1..J13 ascending
...
selftest case=J1 mutants=<ok>/<n> positive=pass payload-match=1 verdict=pass     lines 19..31
...
selftest cases=13 failures=0           line 32
closed=13/13 exit=0                    line 33
```

Payload values are **re-derived, never trusted**: for every id except J8 the recorded payload is
split on `,` and compared token-for-token (in order) against the value the suite recomputed for
that id at receipt time; a prefix, substring or superset is a mismatch. A receipt carrying a
value the suite did not print is red.

The self-reference is **closed, not trusted**: the J8 payload is the fact bundle of the *canonical
transcript this run would write now* (built from the re-derived values, the freshly re-executed
graded selftest lines and the ref-scoped facts) plus `control=<0|1>`. It never reads the recorded
J8 payload, so the fixed point exists and is reached in one rewrite. The resulting bundle for the
honest run here is:

```
receipt=1,sentinel=1,ref=1,digest=1,time-basis=1,run-utc=1,not-future=1,ancestor=1,diff-clean=1,diff-read=ok,tree-bind=1,header-lines=5,run-lines=13,selftest-lines=12,selftest-verdicts=12,summary=1,closed-line=1,payload-match=12/12,closed-match=12/12,selftest-match=12/12,control=1
```

## Evidence — accept on a real tee, reject on each forgery class

All of the following was run in `/fast/scratch/hyaku/kasegi-r42/ExecJ8Receipt/` (removed before
filing). The harness is a **stand-in host** that implements exactly the documented host contract
(`EXPORT`, `REF_RESOLVED`, `LANE`, `WORK`, `PAYFILE`, `payload_get`, `payload_closed`,
`selftest_line`); the real `corpus/instruments/r42-closure.sh` does not exist yet (ExecSuiteCore
builds it in this same wave), so the limb was exercised against a host that follows the contract
it documents. The fixture lane is a throwaway repo created with
`D=$(mktemp -d -p "$S" lane.XXXXXXXX) && git -C "$D" init -q`, `git -C "$D" rev-parse
--show-toplevel` verified equal to `$D` before the first commit, and a per-command identity
(`-c user.email=fixture@local -c user.name=fixture`); no throwaway identity was used anywhere
else.

### 1. The J / Y green window, byte identity and the real tee

```
fixture lane: /fast/scratch/.../lane.CcaBWBR9 (toplevel verified)
J=4a0bf4c190c200c4c7d8677b28bea2cb903ddcbd
Y=d61e187c9666307d2531623b5e2253ca012bbedc
diff J..Y: .ufo/waves/round-42/final-gates/all-gates.txt

run at J (seed): verify_rc=0
receipt=1,sentinel=1,ref=1,digest=1,time-basis=1,run-utc=1,not-future=1,ancestor=1,diff-clean=1,diff-read=ok,tree-bind=1,header-lines=5,run-lines=13,selftest-lines=12,selftest-verdicts=12,summary=1,closed-line=1,payload-match=12/12,closed-match=12/12,selftest-match=12/12,control=1
run at Y (committed receipt): verify_rc=0
receipt=1,sentinel=1,ref=1,digest=1,time-basis=1,run-utc=1,not-future=1,ancestor=1,diff-clean=1,diff-read=ok,tree-bind=1,header-lines=5,run-lines=13,selftest-lines=12,selftest-verdicts=12,summary=1,closed-line=1,payload-match=12/12,closed-match=12/12,selftest-match=12/12,control=1
byte identity: receipt teed at J == receipt reproduced at Y
receipt bytes=2193 sha256=7f25f627a00ac971a40742c9d45d521938ff1e8d28952604496ca9653c109a47
```

The receipt teed at J and the receipt reproduced by the run at Y are the same 2193 bytes. The
committed head of the transcript:

```
all-gates v1
export-ref=4a0bf4c190c200c4c7d8677b28bea2cb903ddcbd
suite-sha256=20e6ebdfb02f8b7adbf7b1a935cb3c091ec2f183ad5956b484299be2e3bd7cbd
time-basis=ref-commit
run-utc=2026-10-28T12:14:00Z
J1 payload=records=3,lines=14,graded=3,evidence=3/3,missing=0 closed=1
...
selftest case=J13 mutants=1/1 positive=pass payload-match=1 verdict=pass
selftest cases=13 failures=0
closed=13/13 exit=0
```

The **real tee** probe pipes the producer's stdout through `tee(1)` and grades the teed file:

```
tee rc=0
teed bytes=2193 sha256=7f25f627a00ac971a40742c9d45d521938ff1e8d28952604496ca9653c109a47
grade teed receipt: rc=0
tee identity: teed stdout == --out file
grade post-tee-forged: rc=1 classes=...,tampered-payload-line=rejected
```

### 2. The seven forgery classes — each rejected, each from its own locus

```
PROBE                      VERDICT CLASSES_REJECTED
control                    GREEN  (none)
honest                     GREEN  (none)
missed-control             RED    missed-control
payload-contradicting      RED    payload-contradicting
future-dated               RED    future-dated
foreign-ref                RED    foreign-ref
nonexistent-ref            RED    nonexistent-ref
summary-only               RED    summary-only
tampered-payload-line      RED    tampered-payload-line
```

The honest control raises **no** class; each forged receipt raises **exactly one**, i.e. the seven
predicates are disjoint on these bytes:

```
control:              missed-control=missed,payload-contradicting=missed,future-dated=missed,foreign-ref=missed,nonexistent-ref=missed,summary-only=missed,tampered-payload-line=missed
missed-control:       missed-control=rejected,payload-contradicting=missed,future-dated=missed,foreign-ref=missed,nonexistent-ref=missed,summary-only=missed,tampered-payload-line=missed
payload-contradicting: missed-control=missed,payload-contradicting=rejected,future-dated=missed,foreign-ref=missed,nonexistent-ref=missed,summary-only=missed,tampered-payload-line=missed
future-dated:         missed-control=missed,payload-contradicting=missed,future-dated=rejected,foreign-ref=missed,nonexistent-ref=missed,summary-only=missed,tampered-payload-line=missed
foreign-ref:          missed-control=missed,payload-contradicting=missed,future-dated=missed,foreign-ref=rejected,nonexistent-ref=missed,summary-only=missed,tampered-payload-line=missed
nonexistent-ref:      missed-control=missed,payload-contradicting=missed,future-dated=missed,foreign-ref=missed,nonexistent-ref=rejected,summary-only=missed,tampered-payload-line=missed
summary-only:         missed-control=missed,payload-contradicting=missed,future-dated=missed,foreign-ref=missed,nonexistent-ref=missed,summary-only=rejected,tampered-payload-line=missed
tampered-payload-line: missed-control=missed,payload-contradicting=missed,future-dated=missed,foreign-ref=missed,nonexistent-ref=missed,summary-only=missed,tampered-payload-line=rejected
```

### 3. Extra structural probes (outside the seven names, still rejected)

```
extra-run-line        RED    payload-contradicting        (a run line for an id the suite never printed)
self-case-missing     RED    missed-control               (the J8 graded case line removed)
substring-payload     RED    payload-contradicting        (lines=140 vs lines=14 — token, not substring)
flipped-closed-bit    RED    payload-contradicting        (closed bit contradicts the re-derived one)
summary-failures      RED    missed-control               (selftest cases=13 failures=1)
absent-receipt        RED    all seven classes            (fail closed, no vacuous tally)
body-dropped          RED    summary-only + tampered      (tally kept, body gone, self line gone)
```

### 4. `check_j8 TREE REF` entry point (tree/ref as arguments, not env)

With `EXPORT` and `REF_RESOLVED` deliberately unset, so the check must take the tree and ref from
its arguments:

```
env EXPORT=<unset> REF_RESOLVED=<unset> (both unset on purpose)
check_j8 export-Y d61e187c9666 -> rc=0   ...tree-bind=1...
check_j8 export-J 4a0bf4c190c2 -> rc=0   ...tree-bind=1...
check_j8 export-Y with ref=J   -> rc=1   ...tree-bind=0,control=0
```

The third line is the binding probe: exporting Y's tree while naming J is rejected — the export
is not the verified ref's tree with respect to the receipt (`tree-bind=0`), and the `foreign-ref`
class fires.

### 5. Lint / syntax

```
$ bash -n ExecJ8Receipt.sh && echo "syntax OK"
syntax OK
$ shellcheck -s bash -S warning ExecJ8Receipt.sh
(no output; rc=0)
```

## Defects this seat found in its own limb and fixed

1. `diff-clean` was initialised to `0` instead of `1`, so the honest bundle carried
   `diff-clean=0` at both J and Y — a self-consistent but wrong fact. Found by the first fixture
   run; fixed and re-verified.
2. `local tree=${1:-} exp="$tree/..."` read `$tree` before the same `local` had taken effect
   (`SC2318`); split into two `local`s.
3. A local variable named `export` shadowed the builtin (`SC2316`); renamed to `exp_root`.
4. The re-derivation loop initially compared the **self** id's payload against a suite value that
   does not exist (the self line carries the canonical bundle); the honest control then reds
   `payload-contradicting`. Fixed by skipping the self id in that loop.
5. A flipped `closed` bit was red only through the fact bundle, with no class naming it; folded
   into `payload-contradicting` (same locus: what the suite printed for that check).
6. The mismatch probe (section 4) showed a receipt accepted when the host names a different
   verification ref than the exported tree; added the `tree-bind` fact and gave the binding its
   home in the `foreign-ref` class.

## Integration contract (for the L1 / ExecSuiteCore)

1. Source the limb into `corpus/instruments/r42-closure.sh` (or copy its functions).
2. Set `EXPORT`, `REF_RESOLVED`, `LANE`, `WORK`, `PAYFILE`; either use `PAYFILE`
   (`ID<TAB>payload<TAB>closed`) with `WORK/sel-<ID>.line` per graded case, or define the hooks
   `payload_get`, `payload_closed`, `selftest_line`.
3. **Ordering**: J1..J7 and J9..J13 must have produced their payload values, and the graded
   selftest must have produced its thirteen case lines, before J8 runs. J8 must be last in the
   payload order.
4. **Invariance (the top risk)**: the other twelve payload values and the other twelve graded
   case lines must be byte-identical between the run at J and the run at Y. The receipt file does
   not exist in the tree at J and does exist at Y, so the receipt path must be excluded from every
   tree-dependent check and from every selftest fixture. If a check counts files or digests a tree,
   J8 will correctly red at Y — and the receipt could never be reproduced.
5. Produce the receipt with `make_receipt --out <path>` (or an identical producer) and tee the
   run's stdout; commit exactly those bytes at `Y = J + .ufo/waves/round-42/final-gates/all-gates.txt`.
6. Run `check_j8 "$EXPORT" "$REF_RESOLVED"`; it prints the J8 payload and returns 0/1. The suite
   composes the transcript line `J8 payload=<payload> closed=<0|1>`.

## Risks and limits (state them, do not hide them)

* **Not yet integrated with the real suite.** `corpus/instruments/r42-closure.sh` did not exist at
  filing time (ExecSuiteCore builds it in this wave), so the limb was verified against a stand-in
  host that implements the documented contract. The contract is written down in the limb header
  and in `ExecJ8Receipt.spec.txt`; if the built suite deviates from it the limb must be adapted,
  not trusted.
* **The nine-plus probes are limb-level, not lane-level.** They prove the J8 code accepts an
  honest transcript and rejects each forgery class; they do not prove that the r42 suite is green.
* **`tree-bind` costs four git reads per fact computation.** Measured cost of one full
  `j8_verify` in this harness is ~6 s (nine fixtures in ~100 s); the real suite calls it once.
* **The control flag is a detector-health fact, not a receipt fact.** A broken detector makes
  `control=0` and every receipt red — fail closed by construction.
* **`selftest-lines`/`selftest-verdicts` count the twelve other case lines only.** The J8 case
  line is the self-reference; its presence and shape are graded, its content is not compared
  (the suite's own graded-selftest judge owns that). This is stated in the spec.
* `J8_FORGE_DISABLE=<class>` is a documented defeat knob (used by a selftest to prove the detector
  is live); it is inert unless set.

## Housekeeping

* Scratch `/fast/scratch/hyaku/kasegi-r42/ExecJ8Receipt/` was created with `mkdir -p`, held all
  work copies, and was removed before filing (`rm -rf`, verified absent).
* `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` reported
  `/fast/scratch/hyaku` at 27% use / 592.6G free before the work; no heavy pass ran against a
  non-green guard.
* Tools installed or upgraded: none. Network fetches: none.
* Files written: the two deliverables above and this receipt (plus scratch, removed).
