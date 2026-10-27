# CritI2Receipt — attack on the I2 receipt design (receipt-only seat)

Seat: CritI2Receipt (leaf, no subagents). Scope: attack the round-41 I2 design —
"the round-41 receipt at Y is the teed transcript of BOTH the suite run and the
graded selftest at Y, with `time-basis=ref-commit` and run-utc equal to the ref's
committer instant" (claims.json C1 predicate). ExecSuiteCore's suite bytes were NOT
yet landed when this seat ran (its dispatch shows early progress), so the attack
targets (a) the claims.json wording (live file at errata commit 96dbd5f, I2 sentence
unchanged by the errata) and (b) the ExecSuiteCore design spec in
`.ufo/waves/round-41/build-wave1-spec.py` (its I2/receipt-tee/selftest paragraphs),
grounded against the r40 machinery it claims to reuse (`corpus/instruments/r40-closure.sh`)
and the r40 wave-2 forgery ground truth (`.ufo/waves/round-40/wave2/CritReceiptForge.md`).
Axes: **depth:verifiability** (primary), **coverage** (a seventh forgery class is added
to the six exercised in round 40).

All transcripts are real command output captured 2026-10-27. Lane repo read-only; the
one git fixture and all models lived under scratch
`/fast/scratch/hyaku/kasegi-r41/CritI2Receipt` (removed before yield). No network
fetches; no tools installed/upgraded; no git/jj mutations anywhere.

---

## Attack 1 — can a receipt be forged by committing a file that merely LOOKS like a tee?

### The r40 baseline

The r40 wave-2 `CritReceiptForge` ground truth exercised six forgery classes against
the committed suite: (a) payload-contradicting, (b) future-dated `run-utc`,
(c1) coherent foreign-ref, (c2) nonexistent ref, (d) summary-only body, (h7line)
tampered self-check line. All six were rejected (`closed=8-9/10 exit=1`), the load-bearing
limbs being H7's `payload-match` (9 recomputed payloads compared byte-wise, excluding
H7's own line), `ancestor` + `diff-clean` (provenance binding to J..Y), and the clock-
anchored `not-future`. Round-41 I8 names exactly these six variants as independently
flagged, and I2 subsumes them at the whole-file level via re-derivation — **on the
run-section surface, nothing from round 40 is dropped, conditional on I8 keeping a
verification-clock anchor (see Correction 2).**

### What I2 newly exposes: the selftest section

The r41 receipt is the first to embed the graded selftest (`... the 12 run lines, the
12 graded selftest lines, and the closed line`, spec text). This transplants the r40
"summary-only" class into a new shape: **a receipt with honest run lines and a fabricated
selftest section**. The routed round-40 defect D2 was precisely "a Y-level selftest tally
without transcript" (spotcheck §2 C1: 'the Y-level `cases=10 failures=0` quoted in
SCORECARD/LOG/SHONEN/the report has no transcript'). If I2 verifies the run section by
re-derivation but the selftest section only by shape (12 `selftest case=... verdict=pass`
lines + summary present), D2 persists in r41: a forger fabricates 12 plausible case lines
and the committed receipt shows a green selftest that never ran.

Model demonstration (scratch, `fixedpoint.py`): a verifier that byte-compares the run
section and shape-checks the selftest section ACCEPTS a receipt whose selftest lines are
hand-written `selftest case=I<n> positive=pass verdict=pass` fabrications:

```
=== V_shape: run-section identity + selftest-section shape check (the D2 shortcut) ===
run-section byte-identical: True; selftest shape (12 verdict=pass lines): True
verdict: fabricated selftest section ACCEPTED - the r40 D2 class (tally without transcript) persists
```

The only defense that closes D2 is re-EXECUTION: I2 must re-run the suite's own graded
selftest at Y and byte-compare every embedded selftest line. The spec says "I2 must
re-derive and compare"; for the selftest section, re-derivation is impossible without
execution (the per-case payloads report mutant verdicts that exist only by running the
mutants — e.g. I10's M-H8a kill). A payload-recompute shortcut is a compute-the-tally-
without-transcript defect of exactly the D2 class.

### Verdict — attack 1

**FIXABLE DEFECT (design wording, not yet in bytes).** The six r40 classes are covered
*if and only if* I2 re-executes both parts and I8 keeps a clock anchor. The new
selftest-section surface is covered *if and only if* the selftest lines are re-executed
and byte-compared (no shape shortcut). The spec's "I2 must re-derive and compare" must
say "re-execute the graded selftest and byte-compare" for the selftest limbs, or the
strongest available forgery — a fully fabricated selftest section riding honest run
lines — passes at Y.

---

## Attack 2 — is run-utc = committer-instant gameable?

### Does any lane path set GIT_COMMITTER_DATE?

```
grep -rln GIT_COMMITTER_DATE corpus/instruments/ corpus/*.sh   -> no matches (exit 2)
grep -rn  GIT_COMMITTER_DATE|GIT_AUTHOR_DATE scripts/ (fleet)  -> no matches
grep across lane (full tree): only fixture artifacts —
  .ufo/waves/round-36/wave1/ExecC1Fixtures.md      (fixture driver, pins FIXED_DATE for fixture repos)
  .ufo/waves/round-39/wave1/ExecWholeTailFixture.fixtures/g1-check.sh (fixture repo pinning)
```

No live lane instrument, no fleet harness script, and no lane commit path
(`scripts/hyaku/jj-lane.sh commit`, jj-based) pins or overrides committer dates.
The lane's own history is naturally dated:

```
git log --format='%h %cI %s' -4
96dbd5f 2026-10-27T05:26:15-03:00 round-41: freeze errata ...
b3b08b2 2026-10-27T05:17:06-03:00 round-41: wave-1 build spec ...
fbba3d9 2026-10-27T05:07:54-03:00 round-41: claims freeze ...
5b29ea1 2026-10-26T19:49:29-03:00 round-40 verifier spot-check ...
```

### The committer instant is self-asserted metadata (demonstrated)

Scratch fixture repo (`git init` under scratch, toplevel verified before committing,
deleted after):

```
default:  %ct=1793090088  %cI=2026-10-27T05:34:48-03:00
backdated: %ct=1577934245  %cI=2020-01-02T03:04:05Z      (GIT_COMMITTER_DATE='2020-01-02T03:04:05Z')
future:   %ct=1925089445  %cI=2031-01-02T03:04:05Z      (GIT_COMMITTER_DATE='2031-01-02T03:04:05Z')
suite ref_utc render of manipulated instant: 2031-01-02T03:04:05Z
```

`ref_utc` (r40-closure.sh lines 371-377, `%ct` epoch -> UTC render) renders whatever
instant the commit object asserts; git honors arbitrary past/future dates. So the
equality "run-utc == committer instant" is satisfiable by construction for any
fabricated receipt in an adversarial repo, and it proves nothing about wall time by
itself. This boundary was stated by sibling seat CritReceiptUtc and is affirmed here
with the manipulation demonstrated end-to-end.

### The gameable fork in the r41 wording: "the ref's committer instant" — WHICH ref?

r40 binds run-utc to the receipt's **named export-ref (J)**, not to the commit carrying
the receipt: `receipt_shape` compares the recorded stamp with `ref_utc "$refhex"` where
`refhex` is parsed from the receipt's own `export-ref=` line (r40-closure.sh ~line 470),
and `not-future` compares against the verification clock +120s (`iso_past`, lines
390-399). CritReceiptUtc verified the committed r40 receipt's stamp equals J7's committer
instant, not Y's, and ruled the wording consistent. The r41 spec repeats the r40 design
("run-utc read from the ref commit's committer instant via read-only git") — but the
r41 CLAIM says "run-utc equal to the ref's committer instant" in the sentence whose
subject is "the round-41 verification ref Y". Two readings, opposite consequences:

- **Bind to named J (r40 semantics):** production-satisfiable with zero date pinning
  (J exists before the receipt; its committer instant is read, not chosen), verification
  at Y reproducible. Sound.
- **Bind to Y's committer instant:** Y's committer date does not exist when the receipt
  bytes are produced (a commit cannot contain its own hash — the receipt is produced
  before Y). The L1 must then pin `GIT_COMMITTER_DATE` to the receipt's run-utc when
  committing Y. No lane path does this today (grep above), so honest integration FAILS
  I2; and if a path is created to make it pass, the commit object misrepresents its own
  time — the false-provenance class the receipt model exists to punish (r39 M39-1;
  r40 R37: "its run-utc is printed by the run, never restamped"). Worse, equality with
  Y's self-asserted date is vacuous as provenance: both sides attacker-chosen.

### Verdict — attack 2

**FIXABLE DEFECT (claim/spec wording).** On the lane as committed, run-utc is not
gameable in practice (no path pins dates; history is naturally dated). In principle the
committer instant is self-asserted — the equality check adds ordering value only, and
the anti-forgery weight must keep resting on payload binding + ancestor + diff-clean +
suite digest + a VERIFICATION-CLOCK anchor. The claims sentence must pin "the ref" to
"the receipt's named export-ref (the judged head J)", matching r40 `receipt_shape`;
and the r41 spec's "and is not wall-clock" must not be read as dropping `iso_past`
(r40 line 439 documents `not-future` vs the verification clock; the r41 spec text names
only "(a) the export tree facts, (b) the ref's committer instant, (c) a freshly teed
comparison run" for I8 — none of which is a wall clock, so the future-dated variant
would be caught only by accident). Keep an explicit clock-anchored limb.

---

## Attack 3 — does teeing the selftest at the same ref create a circularity?

### The dependence channels

The receipt R (30 lines: header, 12 run lines, 12 selftest lines, closed line) is
verified by I2 at Y. Three channels make printed bytes depend on R itself:

1. **Self-verifying run lines.** I2's own run line reports I2's verdict on R; I8's run
   line reports per-variant verdicts computed FROM the committed receipt (spec: I8
   "verifies a receipt file"). These lines are functions of R.
2. **The embedded selftest section.** The selftest re-runs checks against fixtures. r40's
   selftest already read the committed receipt when building fixtures (`h7_fixture` takes
   `href` from `receipt_ref "$EXPORT/$RECEIPT"`, r40-closure.sh ~line 1206; H5_SOURCE =
   the committed receipt, ~line 994) and its judge phase validated the receipt's own
   report shape. r40 was safe because its receipt did NOT embed the selftest output.
   r41 embeds it — any R-dependence in the selftest (a judge-on-R phase, fixture bytes
   derived from R beyond its header, or a payload field echoing a hash of R) feeds back.
3. **Production ordering.** The receipt must be produced before Y exists; verification
   re-derives it at Y. The producer and every verifier must converge to byte-identical
   bytes or I2 reds at honest Y.

### Demonstration: literal "byte-identical" is unpassable; the r40 carve-out converges

Scratch model (`fixedpoint2.py`) of a transcript whose self line reports the suite's
verdict, under the two contracts:

```
=== V_naive (literal 'byte-identical to a freshly teed run', self line included) ===
iter 0: R.self=seed  suite.self=ne  accept=False
iter 1: R.self=ne  suite.self=eq  accept=False
iter 2: R.self=eq  suite.self=ne  accept=False
iter 3: R.self=ne  suite.self=eq  accept=False
iter 4: R.self=eq  suite.self=ne  accept=False
iter 5: R.self=ne  suite.self=eq  accept=False
-> permanent 2-cycle: no fixed point exists; honest Y can NEVER satisfy I2

=== V_carveout (r40 pattern: cmp excludes the self line; self line = recomputed verdict) ===
iter 0: suite.self=eq  accept=False
iter 1: suite.self=eq  accept=True
-> converges to the unique green fixed point (selfcmp=eq)
```

This is the Liar structure: a self line that reports cmp(full R, output) can never equal
its own verdict (2-cycle). r40 solved it explicitly — "the H7 line itself is rebuilt
from the receipt minus its own H7 line, so the self-reference is closed rather than
trusted" (r40-closure.sh lines 127-130), with a seeded 4-iteration settle loop
(`run_suite_report`, lines 1006-1034). The r41 spec says "byte-identical to a freshly
teed run at the same ref" with NO carve-out stated. Consequences:

- implemented literally → no fixed point → I2 is unpassable at honest Y → C1 can never
  print `closed=12/12 exit=0` (claim broken in the unsatisfiable direction);
- implemented with an implicit carve-out → wave-2 falsifiers cannot test the real
  contract, and any payload field that echoes a hash of R makes the fixed point
  preimage-unsatisfiable (no R can contain sha256(R)).

On channel 2: if the selftest's R-dependence is confined to the receipt's HEADER
(fixture `href` from the `export-ref=` line, as r40's h7_fixture does) and the header is
fixed in the production seed before the settle loop, the selftest section is iteration-
invariant and byte-comparable at verification — no infinite regress, just a 2-pass
fixed-point construction (seed → run+selftest → rebuild → converge, exactly r40's
production flow). If the selftest reads R beyond the header (judge phase, R-derived
hashes), the fixed point may not exist at all.

### Verdict — attack 3

**FIXABLE DEFECT (design wording).** Not an infinite regress IF AND ONLY IF four
constraints are pinned in the suite/spec: (i) the byte-identity comparison excludes the
self-referential verdict lines (I2, and I8's line) — rebuilt from the receipt-minus-
those-lines, r40 `h7_inner` pattern; (ii) the graded selftest is receipt-independent
(scratch fixtures only; fixture hrefs from the receipt header; no judge-on-R; no
receipt-derived hashes in any payload); (iii) the receipt line grammar is fixed exactly
(header fields, 12 run lines, 12 selftest lines, closed line — including whether the
`selftest cases=12 failures=0` summary is one of the embedded lines), or "byte-identical"
is undefined; (iv) the 12 selftest lines are environment-invariant (no --work paths, no
dates, no knob values — the canonical judge re-runs with a different scratch layout than
the producer; r40 guaranteed this and the r41 spec must inherit it). Note the cost
consequence: I2's re-derivation makes the primary counting command
`bash corpus/instruments/r41-closure.sh --export-ref Y` execute the full graded selftest
(~40 nested suite runs) on every verification — acceptable (r40's selftest had the same
shape), but the suite must be deterministic under it or I2 flakes.

---

## Findings and smallest safe corrections

1. **I2 byte-identity carve-out (claims/spec).** State that the comparison runs over the
   receipt minus the self-referential verdict lines (I2; I8 if it reads the committed
   receipt), with those lines rebuilt from the remainder (r40 h7_inner pattern). Without
   this the literal contract is unpassable (demonstrated 2-cycle). One sentence in the
   ExecSuiteCore spec + the I2 claim limb.
2. **run-utc anchor (claims/spec).** Pin "the ref's committer instant" to "the receipt's
   named export-ref (the judged head J) committer instant" — r40 `receipt_shape`
   semantics, production-satisfiable without pinning, already validated by CritReceiptUtc
   against the committed r40 receipt. Keep an explicit verification-clock not-future limb
   (`iso_past`, +120s) in I2 or I8 so the future-dated variant (r40 var-b) stays red; the
   current r41 I8 variant list names "future-dated" but the spec defines no clock anchor
   for it.
3. **Selftest section must be re-executed (spec).** "I2 must re-derive and compare" must
   read: re-run the suite's graded selftest at the ref and byte-compare the 12 embedded
   case lines. A shape-only check on the selftest section reopens routed defect D2
   (demonstrated: fabricated selftest section accepted).
4. **Receipt line grammar + selftest purity (spec).** Pin the exact 29-vs-30-line
   grammar (is `selftest cases=12 failures=0` embedded?) and require the 12 selftest
   lines to carry no environment bytes (paths/dates/knobs) and no receipt-derived hashes.
5. **Coverage note for wave 2.** The r41 receipt adds a seventh forgery class beyond the
   r40 six: the fabricated-selftest-section forgery. Wave-2 receipt attacks should
   exercise it (honest run section + invented `selftest case=` lines) so Correction 3 is
   proven against bytes, not wording.

Impacted axes: **depth:verifiability** (I2 is the C1 receipt limb; wording defects 1-3
make it either unpassable at honest Y or passable under forgery), **coverage** (seventh
class added to the exercised forgery surface). No regression to C2. None of the findings
regresses any landed r40 capability; all five corrections are one-sentence wordings the
L1/ExecSuiteCore can land without touching the r40-proven machinery.

## Evidence integrity

Lane at freeze-errata commit 96dbd5f (read-only; claims.json errata section read — the
I2 sentence is byte-identical to the freeze wording; errata touched only the base-hash
length, I11 escape count, and dash encoding). r40 machinery read: r40-closure.sh
(receipt contract doc lines 94-138, iso_past 390-399, receipt_shape 440-480, production
settle loop 1006-1034, h5_fixture/h7_fixture 1186-1231, H5 check 710-760); r40 receipt
`.ufo/waves/round-40/final-gates/all-gates.txt`; r40 wave-2 CritReceiptForge.md (six
variants + transcripts); sibling CritReceiptUtc.md (three limbs affirmed, not
duplicated — its verdicts are cited as boundaries). Demonstrations: committer-date
manipulation and both fixed-point models, run under
/fast/scratch/hyaku/kasegi-r41/CritI2Receipt and removed before yield. No network
fetches; no tools installed/upgraded; pacman untouched; no git/jj mutations anywhere
(read-only lane git; the one fixture repo was scratch-local with toplevel asserted).
Writes: this receipt only.
