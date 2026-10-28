# CritReceiptUtc — attack on time-basis=ref-commit and receipt run-binding

Seat: CritReceiptUtc (critic, wave1). Scope: can a receipt be forged whose run-utc
matches the ref committer instant while the transcript is fabricated; what binds
payload lines to an actual run; comparison to r41 all-gates.txt. Read-only attack
against the frozen C1 design (corpus/instruments/r42-closure.sh does not yet exist;
J8 "inheriting the r40/r41 I2/I8 design" per claims.json).

## Verdict

A fully fabricated receipt can carry a run-utc that matches the ref committer
instant — trivially, because in the inherited design that match is *required and
computed*, not observed. Nothing in the receipt format binds any byte to an
execution event. This is not a correctable defect in the usual sense: no
nonce/signature/channel exists, and the suite's own honest fixture is itself a
synthesized transcript rated honest. The enforceable invariant is byte-level
re-derivability plus graph pinning — strong, but categorically different from
"teed transcript of one observed run". The kill-rule wording overclaims a clause
no evidence can ever fire.

## F1 — run-utc match is definitional, so forging it costs zero

`run-utc` under `time-basis=ref-commit` is the named ref's committer instant,
printed from commit metadata, never a wall clock:

- corpus/instruments/r41-closure.sh:464 `ref_utc()`: `git -C $LANE log -1 --format=%ct $1` → `date -u -d "@$e"`. Comment at 461-463: "Deterministic: it is a property of the commit, not of the clock."
- r41-closure.sh:725: the canonical header is built as `run-utc=$(ref_utc "$refhex")`; :719 marks `run-utc=1` only when the recorded stamp equals `ref_utc` of the receipt's own `export-ref`.
- r41 committed receipt .ufo/waves/round-41/final-gates/all-gates.txt:5 `run-utc=2026-10-27T12:16:34Z`; `git show -s --format=%cI` of the receipt's `export-ref=1f7464…` prints `2026-10-27T09:16:34-03:00` = 12:16:34Z. Byte-equal by construction.
- corpus/lessons/round-41-verifier-spotcheck.md:37 already records this as the conformant reading: "receipt `run-utc=2026-10-27T12:16:34Z` = J committer instant … receipt lands at Y (09:31:58-03:00) | conformant".

Counterexample answered directly: a forged receipt whose run-utc matches the ref
committer instant is not merely possible — every conforming receipt (forged or
honest) has exactly that property. run-utc carries zero evidence about when, or
whether, the suite ran. The field is honestly named (time-basis=ref-commit) but
the r42 kill-rule's "its run-utc is after its containing commit" reads it as if
it were an execution timestamp; it is not.

## F2 — no byte of the transcript binds to a run event

Every field of the canonical receipt is a deterministic function of (named ref,
export tree, suite bytes, verifier clock):

- `export-ref` — inherited verbatim from the receipt under test (`assemble_transcript` r41-closure.sh:2021 `href=$(receipt_ref "$(receipt_source)")`), falling back to the resolved ref. Not observed from the run.
- `suite-sha256` — `file_digest` of the exported suite file (r41 :843/:1980).
- `run-utc` — commit metadata (F1).
- every `I<n> payload=` value — re-derived by the grading run (`payload_match_count` :813 pure byte compare; `i2_canonical` :771 rebuilds I2's own line from shape facts "WITHOUT reading FILE's own I2 line"; I8's line rebuilt from the fresh payload :854).
- `selftest case=` lines — re-executed every run and byte-compared (the `selftest-lines-reordered` mutant at :1742-1747 requires `cmp=0`).
- tail lines — fixed strings.

So the complete canonical transcript is a fixed point anyone can compute:
`git archive J`, compute or predict each payload, emit bytes, commit as Y.
Decisive local evidence that synthesis is indistinguishable: `check_i8`
(r41-closure.sh:1276-1305) builds its *honest control* with `synthetic_receipt`
(:1224) — a file assembled by a shell function that never ran anything — and
requires `control=missed/missed` (every forgery flag must NOT fire on it). The
detector formally classifies a fabricated transcript as honest. The I8 variants
that must reject (payload-contradicting, future-dated, foreign-ref,
nonexistent-ref, summary-only, tampered-payload-line) are all *value* or *shape*
corruptions; "correct transcript, fabricated provenance" is untestable and
untested.

## F3 — what actually binds: re-derivation + graph pinning, not tee-ing

The receipt's real teeth are (a) every recorded value must equal a value
re-derived from the named ref's export — forging values costs work equivalent to
running, so nothing unearned can be smuggled, and (b) graph invariants observed
in r41 all-gates.txt:7 `ancestor=1,diff-clean=1`: the named ref must satisfy
`git merge-base --is-ancestor ref Y` (I verified `is-ancestor X X` is TRUE —
equality counts, so a receipt may name its own containing commit's parent or,
hypothetically, itself; self-naming is unreachable since a commit cannot contain
its own hash) and `git diff ref Y` must name exactly the receipt file (r41: the
J→Y diff is literally `.ufo/waves/round-41/final-gates/all-gates.txt` and nothing
else). Those pin the judged head to the commit graph and force Y = J + receipt.
That is the binding that exists; "one observed run" is not among the enforceable
facts.

Consequence for the kill rule: "is not the teed transcript of one observed
run+selftest at its named ref" can never be evidenced at Z — a synthesized
receipt is byte-identical to a teed one. The clause can only ever fire via the
other limbs (missing file, wrong values, bad ref, run-utc > containing commit).
Also note the "at Y"/"at its named ref" drift: the honest geometry is run at J,
receipt naming J=parent(Y), committed as Y's only diff; "run+selftest at Y"
(claims after-block) is impossible — Y does not exist when the run happens, and
export-ref=Y inside Y is unreachable.

## F4 — residual hazards for the r42 J8 implementation

- `run-utc ≤ containing-commit` (kill-rule limb) is vacuous given the enforced
  equality `run-utc = committer(named ref)` — and can false-kill an honest lane
  only if Y is committed with a committer date earlier than J's (backdating /
  stale env). Operational note for the L1: keep committer dates monotonic J→Y.
- `not-future` compares run-utc to the *verifier's* clock +120s skew
  (`iso_past` r41 :474-481) — correct, but it constrains the commit date, not an
  execution time.
- The inherited-export-ref quirk: because the transcript copies `export-ref`
  from the committed receipt under test, J8 must keep the guard that the named
  ref resolves, is a strict ancestor of the verification ref, and that its diff
  to the export ref is exactly the receipt — otherwise a stale/misnamed ref is
  ratified forward.
- Do NOT "fix" the gap by adding unverifiable provenance fields (hostname, pid,
  wall-clock, entropy): they would be self-asserted, forgeable for free, and
  would break the deterministic fixed point that makes the certificate
  well-defined. The only true execution evidence available is the verifier's
  own re-run of the counting commands — which the claim already requires.

## Impacted axes

- depth:verifiability — primary: C1 kill-rule/after wording asserts an
  unverifiable provenance property; J8 design must inherit r41 semantics
  (equality time-basis, byte-exact rebuild, strict-ancestor + receipt-only diff)
  and claims text should say what is actually enforced.
- coverage — no direct impact.

## Smallest safe correction

1. claims.json (L1 errata, "errata" field exists and is empty): reword the kill
   limb to the enforceable contract — "the final receipt is missing; is not the
   canonical transcript every recorded value of which re-derives at the named
   ref; names a ref that is not a strict ancestor with a receipt-only diff; has
   run-utc ≠ committer(named ref) or run-utc after the containing commit." Drop
   "teed transcript of one observed run" (unverifiable); keep the structural
   limbs. Fix the after-block "at Y" → "run at the named ref J=parent(Y),
   committed as Y".
2. r42-closure.sh J8 spec: inherit r41 exactly — run-utc equality (not ≤),
   byte-exact transcript rebuild modulo the self-referential lines, selftest
   lines byte-compared to this run's re-execution, strict-ancestor +
   receipt-only diff, not-future vs verifier clock +skew. No non-re-derivable
   provenance fields.
3. If an observed-run attestation is ever desired, it cannot live inside the
   commit (self-referential hash); the honest channel is the verifier's re-run
   plus the wave dispatch record outside the receipt. State that rather than
   implying the receipt carries it.

## Evidence commands (all read-only, run from the lane)

- `git show -s --format='%cI %ct' 1f7464… 0f64b8c…` →
  `2026-10-27T09:16:34-03:00 1793103394` / `2026-10-27T09:31:58-03:00 1793104318`
  (receipt run-utc = J committer instant; containing commit 15m24s later).
- `git merge-base --is-ancestor 1f7464… 1f7464…` → exit 0 (self counts as ancestor).
- `git diff --name-only 1f7464… 0f64b8c…` → `.ufo/waves/round-41/final-gates/all-gates.txt` only.
- Read corpus/instruments/r41-closure.sh:344-401, 461-482, 670-876, 1224-1330,
  1699-1760, 1958-2104 (seed, ref_utc, receipt_shape, i2_canonical/rebuild,
  synthetic_receipt, check_i8, assemble_transcript, run_suite_report write loop).
- Read .ufo/waves/round-41/final-gates/all-gates.txt (31 lines) and
  corpus/lessons/round-41-verifier-spotcheck.md:37.
- `ls corpus/instruments/r42*`, `find . -name 'r42-closure*'` → absent at
  2026-10-28 wave-1 time; this is a design-phase attack, matching the item.
