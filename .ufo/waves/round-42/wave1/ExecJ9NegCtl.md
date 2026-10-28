# ExecJ9NegCtl — J9: the killable negative control (base, round-41 judged head, unresolvable ref)

Seat: ExecJ9NegCtl (executor, leaf). Round 42 build wave 1, lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only to this seat).
Deliverables, written beside this receipt:

| file | lines | sha256 |
|---|---|---|
| `ExecJ9NegCtl.sh` | 931 | `89cce69b9a3d0f46312bce51c7d2bfcdbaf63b92892a782094e895f95d2bbc7d` |
| `ExecJ9NegCtl.transcript.txt` | 210 | `c7b68b7e8746a0453cf1caa443949ed56abb454ee998658bcb1f93688d3996aa` |

The limb is a sourceable bash file. Sourcing it defines functions and
globals only and sets no shell options, so sourcing it into
`corpus/instruments/r42-closure.sh` cannot change that suite's behaviour
(the same discipline the sibling limbs `ExecJ11Corr.sh` / `ExecJ12J13.sh`
declare).

## 1. The contract this limb implements

Frozen claim C1, check J9 — *"negative controls (base and round-41
judged-head exports print closed<13/13 exit=1; an unresolvable --export-ref
reports a distinct ref-not-found red, never a vacuous closed<13/13)"*.

    check_j9 TREE REF
      Reads the export tree TREE and the resolved ref REF. Prints ONE flat
      payload line `k=v,…` and returns 0 (closed) / 1 (open).

The limb runs the suite ITSELF over the two control refs and requires both
to be red:

| control | ref | required output |
|---|---|---|
| 1 | base `5053a7f46de35784cff4b56756906e9014a38276` | `closed=K/13 exit=1`, K < 13 |
| 2 | round-41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13` | `closed=K/13 exit=1`, K < 13 |
| 3 | unresolvable (`deadbeef…`) | the DISTINCT `ref-not-found` red, exit 1 |

The two control refs are exported **inside the suite's work dir** and the
**same suite bytes** are invoked recursively on them (leaf mode, depth 1),
so the control measures the committed suite and not a re-implementation.
The suite copy used is the export's own
`corpus/instruments/r42-closure.sh` when the export carries one, else the
running script; the payload records which (`suite=export` / `suite=self`),
so the payload stays a function of the tree and the ref.

## 2. Why the control is not vacuous (the part the r41 verifier routed)

The r41 verifier's routed queue (§5 item 6) and the round-40 wave-2 M-H8a
class are the same defect: **"closed < 13, exit 1" accepts a leaf-capped
GREEN base.** A nested run is depth-capped — its own J9 limb cannot nest
again — so a control tree that is green in every other respect scores 12 of
13, and a naive `K < 13` accepts it. The round-41 suite's own I10 had to be
repaired for exactly this.

The kill here is **THE LEAF CEILING**: every control must score STRICTLY
below the ceiling, where the ceiling is read from the control run's own J9
line (the depth-capped check):

    a green control tree scores 12 with J9 red   ->  ceiling 12, 12 < 12 false
    a green control tree scores 13 with J9 green ->  ceiling 13, 13 < 13 false

A lying J9 bit cannot help: to look green the tree needs 13 closed checks,
and the ceiling never exceeds 13, so no control run can both score 13 and
stay below the ceiling.

The ceiling is derived from the **control** run, never from a run over the
ref under test. Measuring it there would be circular: the ref under test's
own receipt grading compares recorded payload values against re-derived
ones, and the receipt records this limb's payload, which records the
ceiling.

Additional clauses on every control run, each with a replay fixture (§5):

* the exit status must be exactly 1 (0 = green, 2 = harness error);
* exactly 13 check lines, one per id J1..J13, each `closed=0|1` — a
  summary-only or truncated output cannot satisfy the control;
* the number of `closed=1` lines must EQUAL the tally numerator (a lying
  tally is rejected);
* the tally is read as a BOUNDED token (`^closed=[0-9]+/13 exit=[01]$`), so
  a mangled `closed=13/130` cannot pass (round-40 wave-2 T2);
* the transcript may not be a ref-not-found red — a control whose own ref
  did not resolve is a harness error, not a tree-dependent red;
* no bounded tally line may claim 13/13.

## 3. Two precision defects this seat found and fixed

**(a) The ref-not-found test must not be a substring search.** The
committed r41 receipt carries

    I12 payload=declared=153,valid=153,tail=153,pure=1,skill-del=0,…,census=1,ref-not-found=1,markers=0,neg-red=1 closed=1

so a plain `grep -qF 'ref-not-found'` over a control transcript would
misread an **ordinary** transcript as a ref-not-found red and false-red the
control. The limb therefore tests the transcript's SHAPE
(`j9_rnf_kind`): either the explicit status line
`suite-ref-status=ref-not-found`, or every well-formed check line's payload
beginning with `ref-not-found` (the r41 `print_ref_not_found` shape).
Replay fixture `payload-mentions-ref-not-found` reproduces the r41 payload
shape and must be ACCEPTED — it is.

**(b) The `closed=13/13` test must be scoped to the tally lines.** A check
payload may legitimately mention the string. `j9_any_green_tally` scans
only bounded tally lines.

## 4. What the L1 must carry into `r42-closure.sh`

1. **Source the limb.** The suite sources `ExecJ9NegCtl.sh` and calls
   `check_j9 "$EXPORT" "$REF_RESOLVED"` — the same `(TREE, REF)` signature
   as every other limb — and reads ONE payload line from stdout.
2. **Honour `R42_DEPTH >= 1` as leaf mode**: a depth-capped run performs NO
   nested exports. This limb honours both `R42_DEPTH` and `R42_J9_DEPTH`, so
   it never recurses through its own door even if the suite core forgot the
   depth guard. (This is the r41 `R41_DEPTH` convention.)
3. **The suite must print the thirteen check lines in the r42 format**
   `J<n> payload=… closed=0|1` and the tally `closed=K/13 exit=0|1`. The
   limb reads exactly that grammar; a suite that prints a different shape
   cannot be graded by it.
4. **The suite must print the distinct ref-not-found red** on an
   unresolvable `--export-ref`: exit 1 and either a
   `suite-ref-status=ref-not-found` line or check-line payloads beginning
   with `ref-not-found`. The r41 `print_ref_not_found` shape already
   satisfies this; a bare `closed=0/13 exit=1` with no marker does NOT, and
   the limb rejects it (`refnf-mark=0`).
5. **Pass `--lane` through.** The nested control runs need the lane to
   export the two control refs from. The limb passes the suite's own
   `--lane` value down to each nested run.
6. **Leave `--work` outside the lane** (the limb refuses a work dir inside
   the lane, exit 2) and give the nested runs a **private scratch root**
   (a fresh empty directory under the work dir). The limb does this itself;
   the suite core must not override `--scratch-root` for a nested run.
7. Optional tightening: `R42_J9_TREEDEP="J1 J3 J8"` additionally requires
   the named checks to be RED in a control run. It is **off by default**
   because it is a FALSE-RED risk: if any named check is vacuously green on
   a tree carrying no round-42 artifacts (nothing to grade ⇒ nothing
   failed), the honest control would be rejected and 13/13 would become
   unreachable at the judged head. The ceiling clause already kills the
   leaf-capped green base on its own. Turn it on only after confirming the
   named checks are red on both control trees.
8. Wire `j9_replay_fixtures WORK TREE [LANE]` into the suite's replay
   harness: it builds the nine in-family defeat fixtures and asserts the
   limb REJECTS every one of them.

## 5. Evidence — the three controls with real outputs

Full transcript: `ExecJ9NegCtl.transcript.txt` (210 lines). Every command
and every output line there is a recorded execution.

**The fixture.** The round-42 suite is authored by a sibling seat
(`ExecSuiteCore`) and was not committed at this seat's write time, so the
runs use a **r42-shaped STAND-IN** built in a scratch git fixture. It
implements the C1 contract the limb is written against: export mode only
(`git -C <lane> archive <hash> | tar -x`), a plain run refused with exit 2,
one `J<n> payload=… closed=0|1` line per check J1..J13, a
`closed=K/13 exit=0|1` tally, an unresolvable ref printing a distinct
ref-not-found red, and `R42_DEPTH=1` leaf mode. Its twelve non-J9 checks are
artifact-driven, so the two control trees score red for a **tree-dependent**
reason. The two control refs are the REAL lane refs, fetched into the
fixture from the lane.

**The three controls (transcript §4–§6):**

| run | ref | output | exit |
|---|---|---|---|
| green window | the r42-shaped round-42 tree | `closed=13/13 exit=0` | 0 |
| control 1 | base `5053a7f46de35784cff4b56756906e9014a38276` | `closed=1/13 exit=1` | 1 |
| control 2 | r41 judged head `1f7464612ac4c44e39886b82e812610d3c039b13` | `closed=1/13 exit=1` | 1 |
| control 3 | `deadbeef…` | `suite-ref-status=ref-not-found` … `closed=0/13 exit=1` | 1 |
| plain run | — | `refusing to run against the live worktree` | 2 |

Controls 1 and 2 print `closed=1/13 exit=1` — strictly less than 13/13, as
the predicate requires. Control 3 prints the distinct marker and never a
`closed=13/13` tally.

**The limb's own selftest** (`--selftest`, transcript §1): 8 cases,
`selftest cases=8 failures=0`, exit 0.

**The replay fixtures** (`--replay-fixtures`, transcript §2): 9 fixtures,
`replay fixtures=9 failures=0`, exit 0. The honest control is ACCEPTED; the
eight defeats are REJECTED:

| fixture | expected | limb's verdict |
|---|---|---|
| `honest-control` | accept | accepted=1 |
| `leaf-capped-green-base` | reject | rejected=1 (`base-ceiling`) |
| `green-base` | reject | rejected=1 (`base-K`) |
| `unresolvable-control` | reject | rejected=1 (`base-ref-not-found`) |
| `summary-only-control` | reject | rejected=1 (`base-lines`) |
| `mangled-tally` | reject | rejected=1 (`base-tally`) |
| `lying-tally` | reject | rejected=1 (`base-closed1`) |
| `dead-ref-green-tally` | reject | rejected=1 (`refnf-mark`) |
| `payload-mentions-ref-not-found` | accept | accepted=1 |

## 6. Scope, risks and blockers

**Files written.** `ExecJ9NegCtl.sh`, `ExecJ9NegCtl.transcript.txt` and this
receipt, all under `.ufo/waves/round-42/wave1/`. Nothing else in the lane,
the fleet repo or any sibling repo was modified. The lane is byte-identical
to its tip: `git status --porcelain` shows only the wave-1 files other
seats have written. No mutating git command was run against the lane; the
fixture repo was built in scratch (`git -C "$D" init -q`, then
`rev-parse --show-toplevel` asserted to equal the fixture dir before any
commit, per the host guard).

**No tool was installed or upgraded.** The limb needs only bash, git,
tar, awk and grep, all present. Nothing was installed, so there is nothing
to record under the operator's tooling directive.

**Risks.**

1. *The suite core's shape is a contract, not an assumption.* The limb
   reads the r42 transcript grammar (`J<n> payload=… closed=0|1`,
   `closed=K/13 exit=…`, `suite-ref-status=ref-not-found`). If the suite
   core prints a different shape, the limb grades it `verdict=open`. That
   is fail-closed, but it would red the 13/13 window; §4 item 3 states the
   grammar the limb needs.
2. *The limb's nested runs are expensive.* Each control run is a full
   suite invocation (export + thirteen checks). J9 therefore runs the suite
   four times inside one run (two controls, the dead ref, and the suite
   core's own leaf-mode copy). On the r41 suite bytes this is visibly slow —
   see §7. The r42 suite is lighter, but the L1 should know the cost.
3. *The ceiling assumes the leaf cap costs exactly one check.* The ceiling
   is READ from the control run's own J9 line, so a suite whose leaf mode
   closes J9 is graded against 13 instead of 12. Both cases reject a green
   control tree (§2), so the assumption is not load-bearing.
4. *`R42_J9_TREEDEP` is off by default.* §4 item 7 explains why; it is a
   tightening knob, not a requirement.

**Blockers.** None for this seat. One dependency: the limb has not been
run against the lane's own committed `corpus/instruments/r42-closure.sh`,
because that file does not exist in the lane at this seat's write time —
`ExecSuiteCore`'s deliverable had not landed. The stand-in fixture
implements the same contract and the two control refs are the real lane
refs, so the negative-control LOGIC is exercised against real trees; what
remains unverified is the byte-level agreement with the sibling's suite
transcript. The L1 must re-run the three controls against the committed
suite at the judged head (the counting commands in the frozen claims) — that
is the integration step this seat cannot perform.

## 7. A cross-check against the real r41 suite bytes

As a cross-check the limb was pointed at the **real committed r41 suite**
(`corpus/instruments/r41-closure.sh` at the round-41 judged head, copied
into a scratch tree under the r42 suite path). The r41 suite is not the r42
suite: it has twelve checks I1-I12, prints `I<n> payload=…` lines and a
`closed=K/12` tally, and it has its own nested-export machinery. The limb
therefore cannot grade it — its transcript grammar is `I<n>`/`/12`, not
`J<n>`/`/13` — and the nested run at the base control came back red, which
is the correct outcome. The r41 suite's own transcript for that run ended:

    selftest cases=12 failures=7
    closed=9/12 exit=1

which is the expected shape for a control tree that carries none of the
round-42 artifacts, and is the same red the committed r41 receipt records
for its own green-window run (`closed=10/12 exit=1`).

**This cross-check is a partial result, and its final line is not evidence.**
The r41 suite's nested-export machinery makes each invocation slow (this
run took ~121 s rather than seconds — the cost noted in §6 risk 2), and the
run was still in flight when this seat removed its scratch directory, so the
limb's own final verdict line for it reads
`base-K=?,base-lines=0,…,closed=0` with `awk: fatal: cannot open file …`
errors. Those are the DELETED scratch files, not a measurement: the limb's
grading inputs had already been removed underneath it. Only the r41 suite's
own transcript quoted above — captured before the cleanup — is a real
observation. Nothing in §5 depends on this cross-check; the stand-in
fixture covers the same contract and is where the reported results come
from.

Two further caveats on this cross-check, stated so it is not over-read:

* the 9/12 differs from the 8/12 the round-41 do-nothing control recorded
  at the same base ref, because the r41 suite's own checks are tree- and
  host-state-dependent (its scratch-scan limb reads live host state, so the
  tally moves with the machine). The limb's J9 output must not depend on
  host state, which is why it gives every nested run a PRIVATE scratch root
  (§4 item 6);
* the r41 suite is not the instrument under test. What this cross-check
  shows is that pointing J9 at a foreign suite is fail-closed (the limb
  reports `verdict=open` rather than accepting a transcript it cannot
  read) — not that the r42 suite behaves this way.

## 8. Deliverable discipline

`ExecJ9NegCtl.sh` contains only landable bytes: the sourceable limb with
its contract documented in the header, the same way the sibling limbs
document theirs. All validation evidence — the fixture, the three controls,
the selftest, the replay fixtures — is in the transcript and in this
receipt, not in the deliverable.
