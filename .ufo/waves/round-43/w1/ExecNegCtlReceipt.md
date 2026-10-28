# ExecNegCtlReceipt — round 43 (K8 receipt integrity, K9 negative controls)

Axes: depth:verifiability (primary), coverage. Leaf seat; no spawn; no mutating git outside a
throwaway fixture under `$S`; no lane file touched except this report and the three deliverables.

## Deliverables (byte-exact, staged in `.ufo/waves/round-43/w1/`)

| file | lines | sha256 |
|---|---|---|
| `ExecNegCtlReceipt.sh` | 1124 | `ba1099a7b3905496717cd012db069172cc40e784da7f6d6eb827952180a414d2` |
| `ExecNegCtlReceipt.spec.txt` | 241 | `d7668f61d7b5f57b13015ade2fac28c77dde8fe89418495e326bcc7e9fd28cbe` |
| `ExecNegCtlReceipt.transcript.txt` | 303 | `1458cd023f631adf46c9097e80769abdb88ec18f41274ef2e7dc3046e111bdc6` |

Sourceable limbs: `check_k_receipt TREE [REF]` prints `K8 payload=... closed=0|1`; `check_k_negctl
TREE [REF]` prints `K9 payload=depth=...,base=...,r41=...,accept=tree-red,cap=nested closed=0|1`;
`make_receipt [--out PATH]` writes the canonical 45-line transcript. Helpers: `knegctl_verify`,
`knegctl_flags`, `knegctl_forge_fixtures`, `knegctl_battery`, `knegctl_neg_accept`. CLI equivalents
exist for every entry point. No dependency outside bash/git/coreutils/python3.

## Job 1 — negative controls, measured

- Plain run, live suite: `r43-closure: a plain run is refused (export mode only)...` `rc=2`. ✓
- Unresolvable ref, live suite: `ERROR ref-not-found ref=0000... closed=0 exit=1`, `rc=1`, and no
  `closed=<n>/<m>` tally line on stdout — the refusal cannot be mistaken for a vacuous `closed=0/19`. ✓
- Recursive re-invocation (suite snapshot sha `b3cb1c2a5a11e5507dd2553267b54099b20415f33d805e5d0501ee62d47834a4`,
  `--leaf`, own scratch outside the lane):
  - base `ab98fac9`: the suite prints **`closed=19/19 exit=0`** while only **12** of its 19 payload
    lines carry `closed=1` (K8 and K14-K19 are `closed=0`). This is the exact opposite of the frozen
    "base prints `closed<19/19 exit=1`": a vacuous green.
  - r41 head `1f7464612ac4`: prints `closed=7/19 exit=1` while **0** payload lines carry `closed=1`.
  - `K9 payload=depth=1,base=0,r41=0,accept=tree-red,cap=nested closed=0` — the limb refuses both
    legs, because it requires the declared tally to equal the number of `closed=1` payload lines the
    same transcript carries (a red that is not internally consistent is not evidence).
- The same limb against a *consistent* instrument (the r42 suite, whose counters are correct):
  `K9 payload=depth=1,base=1,r41=1,... closed=1` at r42's own baseline `5053a7f4` (nested base
  `closed=3/13` with 3 closed lines, six dependent reds) and `base=0` at `ab98fac9` (only J8 is a
  dependent red there under `--leaf`). The predicate discriminates; it is not a rubber stamp.
  `neg_accept` matrix (transcript §11): 12 cases, green only for a consistent tree-red control.

### Defect found — the suite's closed tally is inverted for the seven non-carried checks

`corpus/instruments/r43-closure.sh:323-324` counts the third `emit` argument as a **closed bit**
(`[ "$3" -eq 1 ] || OPEN++`). The carried loop passes the closed bit, but K8 and K14-K19 pass a
**return status** (0 = closed):

- `:341` `k8="$(check_k8 "$PAYLOAD_FILE")"; k8rc=$?` then `emit K8 "$k8" "$k8rc"`
- `:346-347` `ln="$(limb_line ...)"; rc=$?` then `emit "$id" "$ln" "$rc"`

So `CLOSED = carried_closed + (number of open non-carried checks)`. Measured on a copy with the
carried invocation stubbed and all 19 payload lines `closed=0`: `PROBE TOTAL=19 OPEN=12` →
`closed=7/19` (transcript §10). Consequence at the Y topology, derived from that same inversion:
12 carried closed + 7 rc=0 checks counted open → `closed=12/19 exit=1`, so **Y can never print
19/19** [INFERENCE: arithmetic from the measured inversion, not a run]. Smallest correction, at
the two call sites: `emit K8 "$k8" "$([ "$k8rc" -eq 0 ] && echo 1 || echo 0)"` and the same for
`rc`. Do not change `emit` itself: the carried callers already pass the bit.

### The suite's K8 cannot close at Y under the frozen J/Y topology

- `:160` `[ "$ref_line" = "$FULL" ] && ok_ref=1` requires the receipt's `export-ref` to equal the
  ref under verification. The receipt names J, the run is at Y, and a commit cannot contain its own
  hash (claims.json, `judged_head_rule`). Measured on the real r42 J/Y pair: `ref_line=4c40ef2...`
  `FULL=b2c49ea...` → `ok_ref=0` (transcript §12). K8 is therefore unachievable at Y.
- `:146` the no-receipt branch returns `closed=0`; at base there is no r43 receipt, so K8 is open at
  base. With the six new checks also open, the base figure is `12/19`, not the frozen
  "exactly K14-K19 open". My limb's canonical-seed fallback makes the J run grade its own transcript
  (K8 closed when the bundle is clean) and yields exactly `13/19` at base.
- `:95` `run_utc() { date -u ...; }` stamps a wall clock, not the named ref's committer instant, so
  `time-basis=ref-commit` is not what the bytes say.
- `:181` and `:257` skip the K8 line (`[ "$id" = "K8" ] && continue`): the self claim is unbound.
  Measured: a plausible never-printed value inside K8 (`forged=6/6`→`7/7`) is ACCEPTED by the carried
  reader (CritReceiptForge D1).
- `_k8_grade` (`:236-267`) reads `digest` and the instant and compares neither (transcript §12), and
  the K8 selftest case (`:390-392`) checks only shape — a relabelled/padded selftest block survives
  (D2). My spec closes both: `selftest-match` binds every other case line byte-for-byte to the line
  the running selftest prints now; `tampered-payload-line` binds the self claim to the canonical
  bundle.
- Base limbs are `limb=absent` at `ab98fac9` (`corpus/instruments/r43-limbs/` does not exist there),
  so K14-K19 are red for absence, not for their narrative defect. The claim's "each new check must
  see its own committed defect at base" is not demonstrated by that run.

## Job 2 — receipt integrity, measured

The eight classes are disjoint on real bytes: each of the eight forgeries derived from the real run's
transcript is rejected with exactly its own token, and the honest control raises none
(`battery cases=9 rejected=8 missed=0`, transcript §5).

- **Real tee**: the r42 suite and its graded selftest were re-run over an export of J
  `4c40ef21` (650 s), and `make_receipt` over those values is byte-identical to the run's own
  transcript except the K8/J8 self line (33 = 33 lines, one hunk; §2). The minted receipt is
  accepted (`rc=0`); the same file names J and verifies at a Y-shaped export in the git fixture (§6).
- **Self claim bound (D1 closed)**: the committed r42 receipt raises only `tampered-payload-line`
  and verifies `rc=1`; every content class misses, i.e. the real content is accepted and only the
  self line (from another reader generation) is refused (§4).
- **Selftest block bound (D2 closed)**: `selftest-match=<m>/<n>` compares each recorded case line to
  the line the running selftest prints now; `verdicts` is also checked for internal consistency.
- **Ref-stable bundle**: the self payload carries `receipt=<rel>` (a constant) and **no** `source=`
  cell, because that label flips canonical→committed when the receipt lands — the r41 bootstrap
  defect. Proven in the fixture: minted at J (`closed=19/19 exit=0`, K8 closed), committed at Y,
  graded at Y `rc=0`, byte-identical, `J..Y` differs only by the receipt (§6).
- **Truthful tee, not green transcript**: the closed tally and the failure count must equal what the
  receipt's own lines carry; a red transcript can be faithful, a green claim the bytes do not
  support is `summary-only`. At the green Y these reduce to `closed=19/19 exit=0` and
  `selftest cases=19 failures=0`.

## Evidence

`ExecNegCtlReceipt.transcript.txt` carries every command with its verbatim output: instrument
(`bash -n`, `shellcheck` clean, `--help`), the real run + selftest, the producer diff, the accept and
reject paths, the eight-class battery, the bootstrap fixture, the driver refusals, the suite's two
control transcripts, the K9 output, the counter probe, the 12-case `neg_accept` matrix, the K8
ref-binding probe, and the suite identity at capture time.

## Verification actually run

`bash -n ExecNegCtlReceipt.sh`; `shellcheck -S warning` (clean); `--help`; `--make-receipt` (33/45
lines), `--verify` (accept rc=0, reject rc=1), `--flags` (8 vectors), `--battery` (9 cases),
`--receipt` (rc=0 and rc=1), `--negctl` (real suite), the 12-case matrix, the git-fixture bootstrap,
the counter probe, plus the two full r42 suite runs. Nothing in this receipt rests on an unrun check.

## Risks / blockers

1. **The suite's tally inversion** (§Job 1 defect) makes the base control a vacuous green and makes
   Y unreachable; it must be fixed before integration or C1's kill rule fires at Y.
2. **K8's ref binding** (`:160`) makes the receipt unachievable at its own Y; the correction is
   ancestor + diff + tree-bind, implemented in my limb and demonstrated on the real J/Y pair.
3. **Concurrent rewrite**: `corpus/instruments/r43-closure.sh` changed at 14:12 while a run was
   executing, and bash's incremental read produced a corrupted transcript (`closed=19/19` on a
   half-read script). Every measurement quoted here was re-taken from the snapshot
   `b3cb1c2a...`; do not run the suite from a file another seat is still writing.
4. My limb's K8 is not wired into the suite; `check_k8` there is a separate implementation with the
   gaps listed above. Adopting `check_k_receipt` + the spec, or porting the four corrections
   (canonical seed, ancestor/diff binding, self-claim binding, selftest content binding), is the
   L1's call.

Tooling: none installed or upgraded. Disk guard before the heavy pass: `/fast/scratch/hyaku` 25 %
used, 603.3 G free. Scratch `/fast/scratch/hyaku/kasegi-r43/ExecNegCtlReceipt` removed before filing.
