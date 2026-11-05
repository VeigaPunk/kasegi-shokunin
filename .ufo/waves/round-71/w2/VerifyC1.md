# VerifyC1 — kasegi round-71 attempt 2, C1 re-verification

Seat: VerifyC1 (leaf; no subagents). Scratch `/fast/scratch/hyaku/kasegi-r71/VerifyC1`
(created, used for clone/work dirs/receipts, deleted before yield; receipts copied below).
No tools installed or upgraded; host stack is exactly C1's enumerated scope —
`Python 3.14.8; GNU sort 9.12; git 2.56.0` (counter's own HOST line). PACMAN guard
respected (no pacman transactions).

## (1) Committed bytes at the lane tip

```
$ S=/fast/scratch/hyaku/kasegi-r71/VerifyC1; mkdir -p $S
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin clone --shared \
      /home/vgpnk/Projects/shokunin/kasegi-shokunin $S/clone      # done.
$ git -C $S/clone checkout 3cc8cd45cb6f8ca49a292f3b2647c5bddac71486
HEAD is now at 3cc8cd4 kasegi r71: late seat output (ScribeLesson round-71 lesson draft + report) after wrap-up; not a landed round
$ git -C $S/clone rev-parse --show-toplevel
/fast/scratch/hyaku/kasegi-r71/VerifyC1/clone
$ sha256sum $S/clone/corpus/instruments/figure-audit.py
182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603  .../figure-audit.py
$ sha256sum $S/clone/.ufo/waves/round-71/controls/c1-probe-run-r71.py
80020705e1ff8c3cd8b0d2d20485589d8f17b65e9d1aae9eb9af2f748dd61c0b  .../c1-probe-run-r71.py
```
Both equal `controls/pins-r71.txt` (`80020705…61c0b  controls/c1-probe-run-r71.py`).

Round-70 gate export and r69 base gate:
```
$ git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show 39cde8a:corpus/instruments/figure-audit.py > $S/r70-gate.py
$ sha256sum $S/r70-gate.py
7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5  $S/r70-gate.py
$ sha256sum $S/clone/.ufo/waves/round-70/controls/base-gate-r70.py   # exists at tip
c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde  .../base-gate-r70.py
```
No gate sha256 drift anywhere in this verification.

## (2) Three frozen counter runs (each run its own `--work` under $S)

a. Candidate, tip gate:
```
$ cd $S/clone && python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py \
      --gate corpus/instruments/figure-audit.py --work $S/FINAL --mode candidate
VERIFY measurements=25 failures=0 gate_sha256=182f4ef7d9c9e4d921482d1c2d0cde113c49fd40c76f8fdf0319ba86ba064603 mode=candidate
exit=0
```
All 25 MEASURE lines `ok`: N1–N12 all `rc=2 refused=1 marker_runs=0 wrote=0`;
R1–R8 all `admitted=1 value_ok=1`; `grep -c 'MEASURE .* FAIL' $S/FINAL.out` = 0.

b. Do-nothing, round-70 gate bytes:
```
$ python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py --gate $S/r70-gate.py --work $S/DONO --mode donothing
VERIFY measurements=25 failures=13 gate_sha256=7a8d52eb1d07924714c7f7c4aceca053dd78fddf63ca43b49ec2a2844cee59b5 mode=donothing
exit=1
MEASURE N8-python-no-option-head FAIL rc=1 refused=0 marker_runs=1 wrote=0
```
The 13 FAIL lines, measured exactly:
- N8 `rc=1 refused=0 marker_runs=1` (the frozen "N8 … marker_runs=1" detail ✓)
- N9 `rc=1 refused=0` (selftest ran), N12 `rc=1 refused=0` (unknown head ran)
- R1–R8, all eight: `direct_rc=0|1 gate_rc=2 admitted=0 value_ok=0` (all R refused)
- `MEASURE selftest FAIL selftest cases=96 failures=0 rc=0 min=104`
- `MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=1`
→ 3+8+2 = 13 ≥ 10 (kill-rule floor holds; matches frozen `failures=13`, exit 1).

c. Base, r69 base gate:
```
$ python3 -B .ufo/waves/round-71/controls/c1-probe-run-r71.py \
      --gate .ufo/waves/round-70/controls/base-gate-r70.py --work $S/BASE --mode base
VERIFY measurements=25 failures=14 gate_sha256=c09b0fb1a95b770e5a858ed88b005ec3530486d57dd721cbed2ec6386d882bde mode=base
exit=1
MEASURE no-write-side-effect FAIL fixture_changed=0 marker_runs=5
```
The 14 FAIL lines: all twelve N rows FAIL with `rc=1 refused=0` (i.e. every N derive
was *admitted* by the base gate — N4/N5/N6/N7 additionally `wrote=1`, the base gate ran
write-shaped heads), plus `MEASURE selftest FAIL selftest cases=86 failures=0 rc=0
min=104` and `no-write-side-effect FAIL marker_runs=5`. All eight R rows `ok
admitted=1 value_ok=1`. Matches frozen `failures=14`, exit 1, "every N row admitted".

## (3) Kill rule applied literally

| Frozen requirement | Measured | Fires? |
|---|---|---|
| Any FAIL MEASURE line at candidate | 0 FAIL lines | no |
| Nonzero exit at candidate gate | exit 0 | no |
| Candidate gate sha ≠ frozen `182f4ef…4503` | equal (file + counter-echoed) | no |
| Do-nothing < 10 failures | 13 ≥ 10 | no |
| Base run not failing every N row | all 12 N rows FAIL (admitted) | no |
| Gate sha drift (donothing `7a8d52…c5b5`, base `c09b0f…2bde`) | equal, all three | no |

No clause fires. **C1: VERIFIED** at lane tip `3cc8cd45cb6f8ca49a292f3b2647c5bddac71486`,
from committed bytes only, on the enumerated host stack.

## (4) R8 at the tip — one audit the attempt-1 wave did not run

Claim text freezes R8's grep as `records=84`, but C2's own after-value (and the tip
directly) is `records=85`:
```
$ cd $S/clone && python3 corpus/instruments/capture-binding-check.py --root .
direct_rc=0
  AUDIT records=85 with_url=85 ... orphan=S040-live.txt
  records=85 bound=85 unbound=0          # last stdout line
$ python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84
0
pipeline_rc=1    (grep -c found no match → exit 1, stdout "0")
```
Counter's R8 handling, quoted verbatim from `c1-probe-run-r71.py`:
```python
        ("R8-capture-binding-pipeline",
         "python3 corpus/instruments/capture-binding-check.py --root . | grep -c records=84"),
...
        direct_value = direct_out.strip()
        rc, out, err = probe(work, gate, lane, name.split("-")[0].lower(), derive,
                             direct_value, env)
        admitted = not refused(rc, err)
        if direct_rc == 0:
            value_ok = rc == 0 and ("FIG %s " % name.split("-")[0].lower()) in out and " ok" in out
        else:
            value_ok = rc == 1 and ("FIG %s " % name.split("-")[0].lower()) in out
        record(name, admitted and value_ok, ...)
```
Measured at the tip: candidate run row is
`MEASURE R8-capture-binding-pipeline ok direct_rc=1 gate_rc=1 admitted=1 value_ok=1`.
Because the pipeline's direct arm exits 1 (`direct_rc=1` — no `records=84` in stdout at
records=85), the counter takes the else-branch and `value_ok` degenerates to
`rc == 1 and "FIG r8 " in out`. I confirmed what the gate stamps for this exact fixture:
through `figure-audit.py --ledger` with R8's derive and `recorded="0"`:
```
FIG r8 recorded=0 derived=UNAVAILABLE reason=derive-exit-1 stale
FIGURE-AUDIT figures=1 ok=0 stale=1 exit=1     (gate_rc=1)
```
**R8 finding: R8 is a vacuous row at the tip, not a discriminating positive control.**
Its pattern `records=84` is stale at records=85; the direct arm always exits 1, so the
counter's stale-arm `value_ok = rc == 1 and "FIG r8 " in out` never compares `derived`
against `recorded` at all — it passes any gate that stamps a stale `FIG r8` line,
including an exit-1 `derived=UNAVAILABLE reason=derive-exit-1` stamp. It would keep
scoring `value_ok=1` even if the pipeline never produced a value again. It does not
defeat C1 (the kill rule does not require R8 to bind a value, and the other 24
measurements — 12 value-checked R/whole-gate probes' shape, 12 refused-N rows, 5 gate
limbs — retain their discriminating form; candidate still 25/25), but the C1 counter's
R8 limb is measurement debt against the claim: 24 of the 25 measurements re-derive a
value, R8 does not. Recommendation for the round: re-anchor the R8 pattern to the
direct arm's actual output (e.g. `grep -c '^records='`, which returns `1` non-vacuously
at any record count) or drop the stale count from the frozen command next time the
counter is re-cut.

## Verdict

`C1: VERIFIED` — three VERIFY lines and exits as above; no gate sha drift; do-nothing
still ≥ 10 failures (13). R8 bonus finding: vacuous at tip (direct pipeline
`records=84` → 0, exit 1 at records=85; counter stale-arm passes any stamp, e.g.
`derived=UNAVAILABLE reason=derive-exit-1 stale`).

Receipts: `FINAL.out` (verbatim above), `DONO.out`, `BASE.out`, `r8-led.json` probe
output — copied into this file; scratch tree `rm -rf`'d on exit.
