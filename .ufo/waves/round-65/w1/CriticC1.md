# CriticC1 — adversarial review of the intended C1 signal-fail-closed predicate

Seat: CriticC1 (leaf; no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Scratch: `/fast/scratch/hyaku/kasegi-r65/CriticC1` (one fixture git repo, `work/root`, toplevel asserted).
Receipts: `.ufo/waves/round-65/w1/CriticC1/receipts/` (harnesses under `receipts/tools/`).
No production file edited; no tool installed; no pacman transaction; no git mutation outside my own fixture.

## VERDICT

**SURVIVES** on every *literal* clause of the frozen predicate. I reproduced each clause with the real
instrument and could not make a signal-terminated direct child read green except through the two cases the
predicate itself declares benign/out of scope (SIGPIPE; grandchildren).

**DEFEATED** on two *surrounding* sentences, both by command:

* **H1 — "SIGPIPE (-13) on a non-final stage stays benign" silently converts the instrument's own pinned
  stale class (a missing input operand) into green.** Same missing file, two consumers: stale with `wc`,
  green with `head`.
* **D2 — the frozen driver's own trust root is the mutable working tree, not the measured revision, and it
  no longer checks its own bytes.** A mode-keyed counterfeit passes the collector surface; measurement 8
  (input-hashes) is the only remaining authenticity check and it compares working-tree files to a
  working-tree pin.

Both are ranked with one-line amendments at the end.

## Anchors used (all measured, not assumed)

```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b:corpus/instruments/figure-audit.py | sha256sum
8d92eaa0a1f248eb1fb8ae4d0d098c2a11d8d0674fa1eff6cefdb771e2e917e9  -
$ sha256sum corpus/instruments/figure-audit.py .ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py
86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef  corpus/instruments/figure-audit.py
86becbde1914941d9265634f38e644f3101ad5adc2d52d042ff68b4e83690bef  .ufo/waves/round-65/w1/ExecSignalGate/figure-audit.py
$ git log --oneline -4
a333d8e round-65: amend driver base reference before the final measured run
1c36d72 round-65: land signal-fail-closed derive gate and F44 PSIRT services catalogue
57cb8de round-65: freeze signal-fail-closed and F44 predicates before implementation
462ed24 round-65: commit exact predata controls and frozen gate inputs
```

The wave moved under me: the gate was landed (`1c36d72`) and the driver amended (`a333d8e`) while I was
attacking it. I therefore re-anchored **every base column** to the committed base blob
(`git show a283189:…` → `base-gate.py`, sha `8d92eaa0…`), never to the working tree. The landed gate, the
frozen candidate file and `claims.json`'s `input_sha256` all agree on `86becbde…`.

One self-caught error for the record: my first "collector base" run (receipt
`collector-modebase-against-landed-gate.txt`) hit the working tree *after* it had become the candidate
(header shows `instrument_sha256=86becbde…` in a run labelled base). It is kept, mislabel and all; the valid
base run is `collector-base-vs-baseblob.txt` (`instrument_sha256=8d92eaa0…`, `failures=1`).

Harnesses (copied): `probe.py` runs the real gate on one `(derive, want)` under a fixture root;
`native.py` replays the same pipeline with plain `Popen` and prints each stage rc; `battery.py` runs both.

---

## Q1 — Over-refusal: do legitimate derives die by signal benignly?

Six shapes, all executed. `B` = base blob `8d92eaa0`; `L` = landed `86becbde`. Full table:
`receipts/battery-baseblob-vs-landed.txt`; native statuses `receipts/q1-q2-native-remaining.txt`.

| derive | native | B | L |
|---|---|---|---|
| `git show HEAD:big.txt \| head -n 1` (4.4 MB object) | stage0 rc **-13**, stage1 0 | ok | ok |
| `cat big.txt \| head -n 1` | stage0 rc **-13**, stage1 0 | ok | ok |
| `sort big.txt \| head -n 1` | stage0 rc **-13**, stage1 0 | ok | ok |
| `python3 corpus/instruments/bigwriter.py \| head -n 1` | stage0 rc **1** (not -13) | stale `derive-upstream-exit-1` | stale `derive-upstream-exit-1` |
| `python3 corpus/instruments/printthenkill.py \| wc -l` (prints 35, then SIGTERM) | stage0 rc -15 | ok | **stale `derive-upstream-signal-15`** |
| `cat trunc.txt \| wc -l` (pre-truncated file) | all 0 | ok | ok |

Raw native statuses (`receipts/q1-native.txt`, `q1-sort-sigpipe.txt`, `q1-candidate-controls-native.txt`):

```
NATIVE stage=0 cmd='git show HEAD:big.txt' rc=-13      NATIVE stage=1 cmd='head -n 1' rc=0
NATIVE stage=0 cmd='cat big.txt'           rc=-13      NATIVE stage=1 cmd='head -n 1' rc=0
NATIVE stage=0 cmd='sort big.txt'          rc=-13      NATIVE stage=1 cmd='head -n 1' rc=0
NATIVE stage=0 cmd='python3 corpus/instruments/bigwriter.py' rc=1   NATIVE stage=1 cmd='head -n 1' rc=0
```

Findings:

1. **The -13 exemption is load-bearing and correctly preserved.** It is *not* load-bearing on today's
   ledger (no stage of the 35 committed figures receives any signal — `receipts/ledger-rc.txt`:
   `LEDGERRC figures=35 signal_stages=0`), so the exemption's only live evidence is the synthetic control.
2. **The one over-refusal the predicate does not fix is the interpreter, and the predicate's own wording
   makes it worse.** Python ignores `SIGPIPE` at startup; a `python3` producer piped into `head` writes into a
   closed pipe and exits **1** (`BrokenPipeError`), not -13. So `python3 … | head -n 1` is stale at base and
   *still stale after the fix*, while the identical shape with `cat`/`git`/`sort` is explicitly blessed as
   benign. The candidate's selftest positive control works only because its helper re-enables the default
   disposition (`signal.signal(signal.SIGPIPE, signal.SIG_DFL)`); drop that line and the control silently
   becomes `derive-upstream-exit-1`. This is a claims problem, not a code bug: "SIGPIPE is benign" is false
   for the only allow-listed interpreter head.
3. **Complete-output-then-signal is refused (by design).** `printthenkill.py | wc -l` emits the exact wanted
   value and is then killed by SIGTERM; the landed gate calls it stale. This is the sound trade — the audit
   has no completeness evidence beyond the wait status — but the predicate should say so rather than imply
   that only *partial* output is at risk.
4. **Truncated input does not exercise the predicate at all.** `trunc.txt` is a normal file; `cat` exits 0.
   The prompt's third example is a figure-class hazard (a figure derived from a truncated file reads green),
   not an over-refusal of the signal limb.

---

## Q2 — Under-refusal / false green: what still reads green?

Baseline (false greens now closed), `receipts/q2-base-holes.txt` + `q2-raw-labels.txt`:

| probe | B | L |
|---|---|---|
| `python3 kill.py \| wc -l` want 0 | **ok** | stale `derive-upstream-signal-15` |
| `python3 kill9.py \| wc -l` want 0 | **ok** | stale `derive-upstream-signal-9` |
| `cat g.txt \| python3 kill.py` want "" | stale `derive-exit--15` | stale `derive-signal-15` |
| `kill.py \| wc -l && cat g.txt` want `0\n35` | **ok** | stale `derive-upstream-signal-15` |
| `cat g.txt \| kill.py \| wc -l` want 0 (middle stage) | — | stale `derive-upstream-signal-15` |
| `python3 segv.py \| wc -l` want 0 | **ok** | stale `derive-upstream-signal-11` |

Raw lines (`receipts/q2-raw-labels.txt`):

```
CMD[p9-base]   ... exit=0 stdout='FIG p9-base recorded=0\n35 derived=0\n35 ok\n...'
CMD[p9-landed] ... exit=1 stdout='FIG p9-landed recorded=0\n35 derived=UNAVAILABLE reason=derive-upstream-signal-15 stale\n...'
```

So the limb is *complete for direct children*: -9, -11, -15 and the `&&`-masked case all go stale, and the
label form is right. **Surviving green cases:**

* **H1 (undisclosed, contradicts a pinned class): a SIGPIPE-truncated producer hides a later operand's
  error.**

```
$ cat big.txt 2>err-a.txt | head -n 1 >/dev/null; echo rc0=${PIPESTATUS[0]} stderr=$(wc -c <err-a.txt)
rc0=141 stderr=0
$ cat big.txt missing.txt 2>err-b.txt | head -n 1 >/dev/null; echo rc0=${PIPESTATUS[0]} stderr=$(wc -c <err-b.txt)
rc0=141 stderr=0
```

`missing.txt` does not exist, `cat` is killed by SIGPIPE **before** it reaches it — [INFERENCE from rc=-13 with
zero stderr: a `cat` that reached the name would have written a diagnostic] — so it never diagnoses it and
stderr is empty. Both the benign case and the masking case are therefore indistinguishable at the process
level. Through the gate (`receipts/q2-missing-input-contrast.txt`):

```
-- landed -- cat missing.txt | wc -l        -> exit=1 reason=derive-upstream-exit-1
-- landed -- cat big.txt missing.txt | head -n 1 -> exit=0 reason=-   (ok)
```

The instrument's own selftest pins the first line as stale (`upstream-cat-missing-exit1-stale`); the second is
green. That is the same input error with a bigger first operand. It is **not** one of the documented
residuals.

* **H2 (disclosed): exit-0 wrapper whose child is SIGKILLed** — `python3 childkill.py | wc -l` want 1 →
  `verdict=ok` at base and landed (`receipts/q2-middle-and-wrapper.txt`). Covered by residual
  "exit-0 wrappers that print partial output remain green".
* **H3 (disclosed): a stage that catches the signal and exits 0** — `python3 maskterm.py | wc -l` want 1 →
  ok both (`battery-baseblob-vs-landed.txt`, `P13-signal-caught-rc0`). Covered by the "direct child stages
  only" residual.
* **H4 (undisclosed, not a signal hole): want=0 with an empty exit-0 producer** —
  `python3 exit0empty.py | wc -l` want 0 → ok. The *false green the round set out to fix* is still reachable
  without any signal; C1 closes the signal route only.
* **H5: pre-truncated input** — `cat trunc.txt | wc -l` → ok (see Q1.4).

---

## Q3 — Counterfeit: can a forged receipt satisfy the intended driver/probe shape?

**Yes — for the collector, and for the driver's pins.** The gate itself cannot be substituted at `--final`
(measurement 8 would catch it), but the anti-forgery story as written does not hold.

### Q3.1 A mode-keyed counterfeit satisfies measurements 1, 2 and 7

The collector builds its fixture root under the caller's `--work` and hands that path to the instrument as
`--root`, so the instrument reads the expectation mode from its own argv. `receipts/tools/sniff-stub.py`
implements **no audit**: it prints base-shaped lines when `--root` contains `probes-base` (or the draft's
`collector-base`/`forgeries`), always-ok lines when it contains `selfcheck`, and candidate-shaped lines
otherwise. Run with the frozen driver's own work names (`receipts/q3-sniff-collector-frozenpaths.txt`):

```
work=probes-base      mode=base       collector_exit=1  PROBES probes=6 failures=1
work=probes-candidate mode=candidate  collector_exit=0  PROBES probes=6 failures=0
work=selfcheck        --selfcheck     collector_exit=0  SELFCHECK probes=6 runs=2 failures=6 want=6 verdict=pass
```

Every substring the frozen driver's `check_lines` requires for measurements 1 and 2 is present, e.g.:

```
FOUND: PROBE P1 mode=base audit_exit=0 verdict=ok
FOUND: PROBE P3 mode=base audit_exit=1 verdict=stale reason=derive-exit--15
FOUND: PROBE P1 mode=candidate audit_exit=1 verdict=stale reason=derive-upstream-signal-15
FOUND: PROBE P3 mode=candidate audit_exit=1 verdict=stale reason=derive-signal-15
FOUND: NATIVE P1 stage=0 rc=-15            FOUND: NATIVE P2 stage=0 rc=-9
```

An earlier variant that always exited 0 also passed the collector (`PROBE P1 mode=candidate audit_exit=0
verdict=stale reason=derive-upstream-signal-15`, `receipts/q3-sniff-collector.txt`): the collector never
cross-checks `audit_exit` or the summary against the FIG lines, so the instrument's exit code is decorative
there.

Measurements 3 and 6 check fixed summary strings (`selftest cases=63 failures=0`,
`FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`) that a non-auditing instrument can print. **4**
(source-anchored mutation battery) and **8** (gate sha256 == pin) are the only measurements with teeth
against a counterfeit. The frozen rewrite has no forgery measurement at all — the w1 draft's
`collector-forgeries` was dropped (`grep -c -i 'forg\|counterfeit\|stub' verify-r65.py` → `0`).

Scope: this is neutralised **only** by the gate hash pin at `--final` (measurement 8), not by the collector.
Used as standalone predata receipts (`probes-base.txt`, `probes-candidate.txt`), the collector's output carries
no authenticity.

### Q3.2 The frozen driver dropped the forgery measurement *and* its own self-check

```
$ grep -c -i 'forg\|counterfeit\|stub' .ufo/waves/round-65/verify-r65.py
0
$ grep -n -E 'CLAIMS|json.load\(open' .ufo/waves/round-65/verify-r65.py
44:CLAIMS = os.path.join(WAVE, "claims.json")
237:    if os.path.exists(CLAIMS):
239:            pins = json.load(open(CLAIMS, encoding="utf-8")).get("input_sha256", {})
$ grep -n 'driver-not-committed-bytes' .ufo/waves/round-65/w1/ExecDriver/verify-r65.py
145:                raise ValueError("driver-not-committed-bytes")
```

The w1 draft read the pins from the revision (`blob(revision, PINS_SOURCE)`) and refused when
`sha256(__file__)` differed from the committed driver — the frozen rewrite reads the pins (`CLAIMS`) and the
two programs it actually executes (`COLLECTOR`, `MUTBAT`) from the **working tree**, and never hashes itself.
Only the gate and the ledger come from the exported revision. `claims.json`'s `input_sha256` does not include
`claims.json` or the driver, so measurement 8 compares mutable files to a mutable pin. `--print-inputs` prints the claims hash but compares it to nothing
(`receipts/drv-print-inputs.txt`):

```
86becbde…  …/repo/corpus/instruments/figure-audit.py
28ad7fef…  …/repo/corpus/instruments/figure-audit-ledger.json
855af8df…  .ufo/waves/round-65/c1-signal-probes-r65.py
5050d853…  .ufo/waves/round-65/signal-mutbat-r65.py
86becbde…  .ufo/waves/round-65/figure-audit-candidate-r65.py
fe3fef49…  .ufo/waves/round-65/claims.json          <- pinned by nothing
```

The predicate also names `driver_sha256 533a6d4f…`; the file on disk and the erratum say `5aa842ab…`. The
erratum is explicit and was committed before the final run, but the *predicate sentence* is not literally
satisfiable by the driver in the tree.

---

## Q4 — Do the labels/claims match the mechanism?

Mechanism, from the landed bytes:

```
84:    """Stale upstream statuses: any >1, exit1 from a program other than grep, or a signal.
86:    Grep exit1 is an ordinary no-match. A negative status is a signal: stale unless it is
87:    SIGPIPE (-13). SIGPIPE on a non-final stage is benign by documented rule: a later stage
88:    closed the pipe early, so the truncated producer output is not the value.
91:        return status != -signal.SIGPIPE
127:                    return None, out, "derive-signal-%d" % -status
133:                        return None, out, "derive-upstream-signal-%d" % -p.returncode
```

* **Matches:** "any signal N is stale upstream, except -13" is exactly what the code does (verified with
  -9, -11, -15); "the final stage killed by signal N → `derive-signal-N`" is exact (verified); SIGPIPE can
  only arise on a non-final stage by construction (`communicate()` drains the final stage's stdout), so the
  "non-final" scoping is mechanically right, not arbitrary.
* **Promises more (1):** "a later stage closed the pipe early, so the truncated producer output is not the
  value" is a rationalisation the code cannot verify. It does not say that everything the producer *would*
  have reported after the truncation point is lost (H1).
* **Promises more (2):** "Exit codes: 0 every figure re-derives" over-claims in the presence of -13
  truncation and exit-0 wrappers. The sandbox/pipefail disclaimers are present and correct.
* **"Naming the signal" is a number**, not a name (`signal-15`, `signal-9`). If "name" is meant literally,
  the predicate over-specifies; if a number is acceptable, say "signal number".
* **The final-stage limb is label-only.** `python3 printthenkill.py` (want 35) is stale at base
  (`derive-exit--15`) and stale after (`derive-signal-15`) — same verdict, better label
  (`receipts/q2-raw-labels.txt`). Only the upstream limb changes a verdict.
* **Frozen collector docstring is false against its own receipt**:

```
20:  --mode base       the claim under test at base bytes: all six figures
21:                    read ok (P1/P2 are the upstream-signal false green; P3
22:                    is claimed to read ok as well).
```

  Actual base run (`receipts/collector-base-vs-baseblob.txt`): `PROBE P3 mode=base audit_exit=1 verdict=stale
  reason=derive-exit--15`, `failures=1`, exit 1. The frozen claim's residual already states the truth ("The
  base gate's P3 already read stale; the label … not the verdict"), so the instrument docstring contradicts
  the claim it serves — the same defect class the gate seat was told to avoid.
* Already-disclosed residuals that I verified rather than flagged: grandchildren/shell wrappers out of scope
  (H2/H3), exit-0 wrappers green, P3 label vs verdict, "not pipefail / not a sandbox".

---

## Ranked holes still open after the candidate

| # | hole | status | evidence |
|---|---|---|---|
| 1 | **H1** SIGPIPE-truncated producer hides a later operand's error (`cat big.txt missing.txt \| head -n 1` green; `cat missing.txt \| wc -l` stale) | undisclosed, contradicts a pinned selftest class | `q2-missing-input-contrast.txt`, `q2-sigpipe-masks-error-native.txt` |
| 2 | **D2** driver trust root is the working tree (pins + the collector/mutbat it runs), no self-hash, forgery measurement dropped | undisclosed; "committed-input" is inaccurate | `q3-driver-provenance.txt`, `drv-print-inputs.txt` |
| 3 | **Q3.1** collector expectations are keyed by a path the instrument can read; measurements 1/2/7 pass with a non-auditing instrument | bounded by the gate pin at `--final` | `q3-sniff-collector-frozenpaths.txt` |
| 4 | **P4b** `python3 … \| head` is stale while `cat … \| head` is benign — "SIGPIPE benign" is false for the interpreter head | undisclosed, claims-level | `battery-baseblob-vs-landed.txt` |
| 5 | **H4** want=0 with an empty exit-0 producer is green (the original false green, non-signal route) | undisclosed; figure-class, not signal limb | `battery-baseblob-vs-landed.txt` (`P11`) |
| 6 | **Frozen collector docstring** says base P3 reads ok; its own base run says stale | false statement in frozen bytes | `collector-base-vs-baseblob.txt` |
| 7 | predicate names driver `533a6d4f…`, erratum supersedes `5aa842ab…`, both unpinned by the driver | disclosed by erratum; provenance nit | `claims-erratum-1.md`, `drv-print-inputs.txt` |

### One-line amendments I would accept

1. **H1:** `SIGPIPE (-13) on a non-final stage is benign only when that stage has a single input operand; with
   two or more operands the truncation can hide a later operand's error, so the stage is stale
   (derive-upstream-signal-13-multi-input).`
   *(Cheaper alternative, disclosure only: add to residual 2 "…and any diagnostic the producer would have
   emitted after the truncation point is lost; a derive that must read several inputs MUST NOT pipe into
   head.")*
2. **D2:** `The driver MUST read input_sha256 and the four wave inputs from the measured revision
   (git show <rev>:…), and MUST refuse unless sha256(__file__) equals the predicate's driver_sha256.`
3. **Q3.1:** `The collector MUST pass the same --root basename in both modes (no mode token reachable by the
   instrument) and MUST require audit_exit and the audit summary to agree with the parsed FIG lines.`
4. **P4b:** `Replace "SIGPIPE (-13) on a non-final stage stays benign" with "only an actual signal death
   (-13) is benign; an interpreter that ignores SIGPIPE reports exit 1 and stays stale."`
5. **H4:** `A figure whose want is 0 and whose derive ends in wc -l MUST also pin a non-empty-producer
   positive control, because an empty exit-0 producer is green by construction.`
6. **Docstring:** `Delete "P3 is claimed to read ok as well" from c1-signal-probes-r65.py; P3 is stale at base
   with the malformed label.`

### Not defects (checked so the judge need not)

* SIGPIPE on a **final** stage is unreachable — the final stage's stdout is drained by `communicate()`; the
  "non-final" carve-out is therefore complete, not a scoping error.
* Pre-existing positives stay green under the landed gate: `cat g.txt | wc -l` want 1 and
  `grep absent g.txt | wc -l` want 0 (`battery-baseblob-vs-landed.txt`, P5/P6); the committed 35-figure
  ledger audits `figures=35 ok=35 stale=0 exit=0` (`ledger-real-candidate.txt`, run against the landed gate).
* The landed selftest is `cases=63 failures=0` with the SIGPIPE control reaching native -13
  (`selftest-real-candidate.txt`, `q1-candidate-controls-native.txt`).
* The landed diff contains only the limb, the docstring sentence, four selftest cases and the flipped
  lineage case; no unrelated behaviour changed (`diff -u base candidate`, 35 insertions / 10 deletions).

## Reproduction

```
cd /fast/scratch/hyaku/kasegi-r65/CriticC1
git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show a283189b…:corpus/instruments/figure-audit.py > base-gate.py
python3 -B battery.py --base $PWD/base-gate.py \
  --cand /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py
python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-65/c1-signal-probes-r65.py \
  --instrument $PWD/base-gate.py --work $PWD/cwork-base2 --mode base
python3 -B /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-65/c1-signal-probes-r65.py \
  --instrument $PWD/sniff-stub.py --work $PWD/attackwork3/probes-base --mode base
```

Fixture root (`work/root`, git repo with toplevel asserted): `g.txt`=`35\n`, `f1.txt`=`340\n`, `big.txt`
= 400 000 lines, helpers `kill.py` (SIGTERM), `kill9.py` (SIGKILL), `segv.py`, `printthenkill.py`,
`childkill.py`, `maskterm.py`, `bigwriter.py`, `pipe.py`, `exit0empty.py`.
