# MutC1 — round-78, wave w1: C1 gate-design mutation test vs the frozen r77 reference

Scope: mutation-test the C1 gate design against `.ufo/waves/round-77/c1-amended-reference.py`
(sha256 `18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33`, verified on copy),
independent of ExecC1Build's candidate. Mutants derived per
`.ufo/waves/round-78/c1-mutant-transforms.md` (K-X1/K-X2/K-M8 anchors at reference lines 318/323/305 — matched).
Detector (bounded, same for every run): `TMPDIR=$S/t python3 -B <variant> --selftest`.
Scratch: `/fast/scratch/hyaku/kasegi-r78/MutC1/` (deleted before yield; every run wrote only under `$S/t`).
No lane file outside `.ufo/waves/round-78/w1/` was written; no installs; no git/jj writes.

## Baseline (pristine reference)

`selftest cases=12 failures=0`, rc=0, no Traceback. Baseline passes → verdicts below are conclusive.
All runs: no Traceback in any variant (K-M3's NameError is caught by the gate's `except` and logged
as a FAIL detail — the exception kill class, as the table specifies).

## Kill table (single mutants on the reference)

| mutant | derivation (one anchored transform) | ref rc | reference FAIL lines | survived |
|---|---|---|---|---|
| K-M1 | delete `regs["restoration-only-result"] = lambda out, ret: (\n            ret == 1 and "RECHECK-CWD-RESULT nonconformant" in out)` (lines 264-265) | 1 | `gate-regs FAIL registered=[]`; `gate-consume FAIL no-registration`; `gate-negpolarity FAIL no-registration` | **no — killed** ✓ expected |
| K-M2 | closure body → `            True)` (line 265) | 1 | (`gate-consume ok clean_ok=True` — passes as predicted) `gate-negpolarity FAIL neg_ok=True` | **no — killed** ✓ expected (m2b class: caught by negpolarity) |
| K-M3 | delete `        out6, ret6 = capture(main, ["recheck-cwd-census.py", "--root", root6, "--lane", root6])` (line 253) | 1 | `gate-consume FAIL exception=NameError("name 'out6' is not defined")`; `gate-negpolarity FAIL not-evaluated-after-exception` | **no — killed** ✓ expected (exception class, logged detail) |
| K-M4 | `neg_ok is False` → `neg_ok is True` (line 329) | 1 | `gate-negpolarity FAIL neg_ok=False` | **no — killed** ✓ expected |
| K-M5 | delete the four-line `check("both-headers", …)` call (lines 281-284; fixture kept) | 1 (cases=11) | `gate-checkids FAIL missing=['both-headers'] extra=[]` | **no — killed** ✓ expected |
| K-X1 | `clean_ok = limb(out6, ret6)` → `clean_ok = True` (line 318) | 0 | — (`cases=12 failures=0`) | **yes — survived** ✓ matches known r77 finding |
| K-X2 | `check("gate-consume", clean_ok is True, …)` → `check("gate-consume", True, …)` (line 323) | 0 | — (`cases=12 failures=0`) | **yes — survived** ✓ matches known r77 finding |
| K-M8 | relabel-detection condition → `              True,` (lines 306-307; check id kept) | 0 | — (`cases=12 failures=0`) | **yes — survived** ✓ matches known r77 finding |

Expectation (3) confirmed 8/8: K-M1..K-M5 killed with exactly the FAIL lines the frozen table predicts;
K-X1, K-X2, K-M8 survive on the reference (the known r77 finding).

Each mutant's stdout is identical to pristine except the FAIL lines above — X1/X2/M8 outputs are
byte-identical to the baseline run (`cases=12 failures=0`).

## Composite probe (known limit — NOT counted as claim kills)

| composite | transforms | ref rc | result |
|---|---|---|---|
| COMP-A (tasking-named) | K-M8 + K-M4 | 1 | **killed**, `gate-negpolarity FAIL neg_ok=False` — killed entirely by its M4 half; the M8 half stays invisible |
| COMP-B | K-M8 + K-X1 | 0 | **survives** (`cases=12 failures=0`) — confirms the routed limit: composites of named transforms can evade the reference gate even when each half is individually required-kill |

## Survivor-kill proposals (patch: `MutC1-proposals.patch`, 3146 bytes, ref.py → prop.py)

Applied only to the scratch copy `$S/prop.py`; never to any lane file. Pristine prop.py selftest:
**rc=0, `cases=14 failures=0`** — proposals add `gate-consume-calls` + `predicate-source` and break nothing.

**P1 — kills K-X1 (behavioral invocation spy).** X1's file computes `clean_ok = True` without calling
the limb; value-level assertions cannot see this (the value is the same True), so the proposal records
every gate consumption: a wrapper around the retrieved limb appends each result to `limb_calls`, and a
new check `gate-consume-calls` asserts `limb_calls == [True, False]` (positive on case-6, negative on
case-2), in all three gate paths (else/except/no-registration). Proof: `prop+K-X1` → **rc=1,
`selftest case=gate-consume-calls FAIL limb_calls=[False]`**.
Killable by one of my eight? **No** — verified: every prop+mutant run below still exits 1; none of the
eight transforms touches `gate-consume-calls`. Residual (routed class, not claim-scoped): a ninth,
unnamed transform neutering `gate-consume-calls` itself would evade.

**P2 — kills K-X2 and K-M8 (source-level meta-assertion).** Both mutants replace a condition that is
**constant-True on the pristine data** with the literal `True`; the mutated run is behaviorally
identical (same stdout, same rc), so *no* value-level assertion added anywhere can kill them — the
smallest demonstrable kill asserts the predicate text is still present in the source
(`predicate-source`), with the searched strings built by concatenation (`"all(got8u[k] == v" + " for k,
v in want8u.items())"`, `"clean_ok " + "is True"`) so the meta-check's own literals cannot satisfy it
(first draft had that self-reference bug; the split-literal form is what is proven here). Proofs:
`prop+K-X2` → **rc=1, `selftest case=predicate-source FAIL relabel_pred=True consume_pred=False`**;
`prop+K-M8` → **rc=1, `selftest case=predicate-source FAIL relabel_pred=False consume_pred=True`**.
Killable by one of my eight? **No** — verified below. Caveats: P2 is white-box and refactor-fragile
(renaming `got8u` or restructuring `gate-consume` false-fails it), and a meta-neutering ninth
transform evades it. The structural alternative — a dedicated negative-control case registering a
forged limb and asserting the gate catches it — kills the same class without source coupling but is a
larger diff; either is design feedback for the landing successor, not a lane edit.

**Proposal robustness across all eight mutants (prop.py + each transform):**
K-M1 → rc1 (`gate-regs`, `gate-consume`, `gate-negpolarity`, `gate-consume-calls limb_calls=[]`);
K-M2 → rc1 (`gate-negpolarity neg_ok=True`, `gate-consume-calls limb_calls=[True, True]`);
K-M3 → rc1 (`gate-consume exception=NameError…`, `gate-negpolarity not-evaluated…`, `gate-consume-calls limb_calls=[]`);
K-M4 → rc1 (`gate-negpolarity neg_ok=False`); K-M5 → rc1 (`gate-checkids missing=['both-headers']`);
K-X1 → rc1 (above); K-X2 → rc1 (above); K-M8 → rc1 (above). No proposal masks a named kill.
`prop+COMP-A` → rc1 (`predicate-source`, `gate-negpolarity`); `prop+COMP-B` → rc1
(`predicate-source`, `gate-consume-calls`) — the proposals compose and also kill the surviving
composite on the patched design.

## Restoration evidence

- `$S/ref.py` sha256 after all runs: `18bfc439238310af345189c0192c497b8451bea4a2bed1644a03866924588a33` — identical to the lane source `.ufo/waves/round-77/c1-amended-reference.py` (same hash, read-only, untouched).
- Mutant/prop variants were separate files under `$S`; scratch deleted at yield.
- Baseline ran first and passed, so no verdict above is inconclusive.

## Files written

- `.ufo/waves/round-78/w1/MutC1.md` (this report)
- `.ufo/waves/round-78/w1/MutC1-proposals.patch` (proposals P1+P2, unified diff against the r77 reference)

Verdict for the claim-design probe: on the r77 reference the C1 gate kills exactly K-M1..K-M5
(including the m2b-class K-M2 via negpolarity and the exception-class K-M3 via the logged NameError
detail) and survives K-X1, K-X2, K-M8 — the frozen expectation holds 8/8; the proposals above are the
smallest demonstrated assertions that close the three survivors.
