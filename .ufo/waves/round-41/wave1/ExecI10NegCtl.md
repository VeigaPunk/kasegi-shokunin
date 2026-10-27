# ExecI10NegCtl — I10: the killable negative-control acceptance (closes MutH6H10 D2)

Seat: ExecI10NegCtl (executor, leaf). Round 41 build wave 1, lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin` (read-only to this seat). Deliverable:
`.ufo/waves/round-41/wave1/ExecI10NegCtl.transcript.txt` (140 lines, 9,669 bytes,
sha256 `3608c8cad0b859ed7293e639e969758eebc16e5c9ebb395ceb427952ef5a1f32`), built by
`mktranscript.sh` from the verbatim run captures in scratch.

## 0. Freeze correction used

The dispatched prompt carried a 38-char base literal (`5b29ea1439450b712581edf5f0bf98dfb262ab`,
unresolvable). The authoritative base, per `claims.json` and the L1's
`.ufo/waves/round-41/wave1/CORRECTIONS-L1.md`, is the 40-char
`5b29ea1439450b712581edf5f0f0bf98dfb262ab`; every control run below uses that form. It resolves:
`git rev-parse 5b29ea1` → `5b29ea1439450b712581edf5f0f0bf98dfb262ab`.

## 1. The defect being closed (MutH6H10 D2, r40 H8)

r40's H8 acceptance was `[ "$b" -lt 10 ] && [ "$rc" -eq 1 ] && [ "$r" -lt 10 ] && [ "$rk" -eq 1 ]`
on nested leaf-mode tallies. Two independent faults made it unkillable and vacuous:

1. **Unreachable boundary.** Leaf mode reds the negative-control limb itself, and in the r40
   shape it also shifts the count-relative H5/H7, so a fully-green tree floors at 7/10. Every
   reachable `b` is ≤ 7, so `-lt 10` ≡ `-le 10` on all inputs: the M-H8a mutation
   (`-lt 10` → `-le 10`) is behaviourally equivalent and the selftest cannot see it.
2. **No fixture exercised the comparison.** The two H8 fixtures pointed the control refs at
   unresolvable strings and asserted `base-exit=2`; the numeric guard returned 1 before the
   comparison was reached, so no selftest limb ever reached the predicate.

Reproduced here (transcript §BEFORE, r40 pristine bytes, base control pointed at the r40 green
window `d0fe34d3…`):

```
H8 payload=base=7/10,base-exit=1,r39=2/10,r39-exit=1 closed=1     # accepts a leaf-capped green base
```

and the r40 M-H8a mutant (`-lt 10` → `-le 10`, sha256
`d17760b3d09dc0658d57c51a3c0ff217599b0438863a5ab246b311d435389c6f` — byte-for-byte the mutant
MutH6H10 recorded) prints the identical H8 line: equivalent, unkillable.

## 2. The I10 design

The export's **own suite copy** (`$tree/corpus/instruments/r41-closure.sh`) is run three times in
**leaf mode** (`R41_LEAF=1`, so the nested run's I10 returns red immediately — depth 2 at most, no
recursion):

| nested run | ref | meaning |
|---|---|---|
| `b`, `bc` | round-41 base `5b29ea1439450b712581edf5f0f0bf98dfb262ab` | negative control 1 |
| `r`, `rc` | round-40 judged head `c7aea5ef97902f38289cbdc1cf267068876a62dd` | negative control 2 |
| `g`, `gc` | **the receipt's declared `export-ref`** | the LEAF-CAPPED GREEN CEILING |

The ceiling run is the trick that makes the comparison meaningful and reachable: it is the tally a
*green* tree scores once the only red limb is the leaf cap itself. The acceptance then requires each
control to be **strictly redder** than that ceiling.

**The exact acceptance predicate (one line, as implemented):**

```sh
[ "$b" -lt "$g" ] && [ "$r" -lt "$g" ] && [ "$g" -lt "${#CHECK_IDS[@]}" ] && [ "$bc" -eq 1 ] && [ "$rc" -eq 1 ] && [ "$gc" -eq 1 ]
```

With 12 checks (the r41 suite) `g ≤ 11`, so each control must print `closed = K ≤ 10 < 12` with
exit 1 — the seat's "closed<=K<12 with exit 1" — and a tally that *reaches* `g` is a leaf-capped
green base and is REJECTED. `g < N` is part of the predicate so that a ceiling of N (leaf cap not
biting) cannot re-open the vacuity. Non-numeric tallies and non-red (≠1) exits fail closed.

**Why the ceiling ref is the receipt's ref, not the export ref.** The receipt is produced at J and
verified at Y = J + receipt. Measuring the ceiling over `$REF_RESOLVED` gives different tallies at J
(receipt absent → H5's source is synthesised) and Y (receipt present) → the I10 payload would differ
and H7's byte-identity would red at Y. Measuring over the receipt's declared ref gives the same
number at both stages. Verified: the plain transcript at Y is **byte-identical** to the committed
receipt in both fixtures (`cmp` clean), which also proves the payload is a function of stable facts
only.

**The graded selftest case** carries four fixtures (`R41_NEG_BASE`/`R41_NEG_R40` are selftest-only
overrides, unset with `env -u` for the nested runs so they never leak inward):

1. `leaf-capped-green-base`: base control pointed at the ceiling ref → its tally equals `g` by
   construction → must be REJECTED (pristine) / is ACCEPTED by the M-H8a mutant → **the kill**.
2. `leaf-capped-green-r40-head`: the same for the second control.
3. `base-ref-unresolvable`, 4. `r40-ref-unresolvable`: harness errors, not controls.

The payload prints the measured values only — `base=<b>/N,base-exit,b40-at-cap,cap,r40,r40-exit` —
and the `*-at-cap` markers are equalities of measurements (identical under the mutation), so the
mutant changes the verdict and nothing else.

## 3. Proof (transcript §PRISTINE / §MUTANT)

Prototype substrate: `corpus/instruments/r40-closure.sh` with its H8 limb replaced by I10
(10 check ids, 1,789 lines). Fixtures are scratch clones of the lane at the round-40 judged head
with the suite bytes committed, the suite's `declared-blocks` entry re-declared for the new tail,
and a receipt produced at J and committed at Y (`git diff --name-only J Y` = the receipt only).

| run | plain run at Y | selftest I10 case | summary | exit |
|---|---|---|---|---|
| pristine (`f268122b…`) | `closed=10/10 exit=0`, cmp clean | `positive=pass mutants=4/4 verdict=pass` | `cases=10 failures=0` | 0 |
| mutant (`8c08d118…`, `-lt "$g"`→`-le "$g"`) | `closed=10/10 exit=0`, cmp clean | `positive=pass mutants=3/4 verdict=fail` | `cases=10 failures=2` | 1 |

Flipped detail line (mutant):

```
selftest detail=I10 mutant=leaf-capped-green-base rejected=0 rc=0 payload=base=8/10,base-exit=1,base-at-cap=1,cap=8/10,cap-exit=1,r40=7/10,r40-exit=1,r40-at-cap=0
```

Measured payload at the green window (identical pristine/mutant):
`base=5/10,base-exit=1,base-at-cap=0,cap=8/10,cap-exit=1,r40=7/10,r40-exit=1,r40-at-cap=0`
— base over `5b29ea1…` = 5, r40 head over `c7aea5e…` = 7, ceiling = 8, all three nested exits 1.

`failures=2` for the mutant is the r40 machinery's accounting: the single failing case increments
`FAILS` twice (`st_neg` and `st_verdict`). Only one case line reads `verdict=fail`, and it is I10;
`selftest judge=own-report accepted=0` is the judge refusing the mutant report, as intended.

## 4. What the L1 must carry into `r41-closure.sh`

1. Replace the negative-control limb with the three-run design above: base `5b29ea14…`, round-40
   judged head `c7aea5ef…`, ceiling = **the receipt's declared export-ref**, all in leaf mode
   (`R41_LEAF=1`) executing the **export's own suite copy**.
2. Ship the predicate exactly as the one line in §2 with `N = 12`; keep the `g < N` clause.
3. Ship the four selftest fixtures, in particular `leaf-capped-green-base` (control override → the
   ceiling ref) as a graded negative fixture — that fixture is what kills the M-H8a class.
4. Keep the I10 payload free of stage-dependent fields (tallies, exits, at-cap markers only).

## 5. Risks the L1 should verify at Y

- **Margin.** In the prototype the r40 head scores 7 against a ceiling of 8 (margin 1) because the
  r40-shaped check set makes the round-40 head nearly as green as the export. Under the r41 check
  set the round-40 head lacks every round-41 artifact, so the margin should be larger — but it is
  *measured*, not assumed: if a control ever ties the ceiling the I10 limb reds and the suite
  refuses `closed=12/12` (fail-closed, never vacuous). The I10 positive limb is exactly that
  measurement gate.
- **Leaf-shape drift.** The r40 shape still reds the count-relative H5/H7 in leaf mode, so the
  ceiling is 8/10 rather than 9/10. The design measures the ceiling instead of hard-coding it, so
  the r41 I8/I9 per-variant redesigns may lift it to 11/12 without any change to the predicate;
  a hard-coded `≤ 10` would silently re-open D2 if the leaf shape were wider.
- **Payload stability.** If a future edit puts the ceiling in the payload measured over the export
  ref, the J→Y byte-identity breaks (H7 red). Keep the ceiling ref = the receipt's declared ref.

## 6. Conduct and hygiene

- Writes: only the two wave-dir deliverables (this receipt, the transcript) and scratch
  `$S=/fast/scratch/hyaku/kasegi-r41/ExecI10NegCtl/`. No lane/fleet/sibling/source-tree write; no
  PATH write; no `MANIFEST.json`/`templates/`/`scripts/`/`.ufo/state/` write.
- The lane repo was used read-only (`git archive`/`ls-tree`, `rev-parse`); no mutating git command
  ran in it. All fixture commits happened in the scratch clone `$S/fix`, whose toplevel was asserted
  (`/fast/scratch/hyaku/kasegi-r41/ExecI10NegCtl/fix`) before the first commit, with the
  fixture-only identity `r41-i10-fixture@local`: `b2a22c9`/`138591e` (pristine J/Y),
  `7474da9`/`3ef939d`/`2fe6aea` (mutant receipt-drop, J, Y).
- Tooling: nothing installed or upgraded (no pacman, no network fetch). Scratch `$S` removed before
  yield; the transcript and this receipt are the only surviving artifacts.
- Note: another seat (ExecI8Forge) deleted the shared `…/kasegi-r41` parent mid-flight; the
  scratch was rebuilt from the lane (all figures above come from the rebuilt run).
