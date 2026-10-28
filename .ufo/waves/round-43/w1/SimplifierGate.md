# SimplifierGate — YAGNI review of the claim-package gate (kasegi round 43, wave 1)

Seat: simplifier, leaf (no subagent dispatch, no swarm, no second judge). Item:
`/skill:godspeed` YAGNI review of the eight C2 gate rules and the ten selftest cases —
duplicate rules, cosmetically-different fixtures, contract keys no consumer reads,
rules that cannot fail — plus the minimal set that keeps every defect class caught.

Claims read first and never edited: `.ufo/waves/round-43/claims.json`
(lane kasegi, round 43, base `ab98fac9dce87130bc4f66de89e30650d63943dc`,
freeze commit `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`). C2 predicate read in
full (`:50:raw`), C1 kill rule read for the receipt discipline. Controls not
needed: this item measures the gate's rule surface, not C1's counters.

Axes named before work:

- **depth:verifiability** — every deletion candidate must be shown to cost zero
  verdicts on the frozen ten cases; every retained limb must be shown to have a
  delta that can make it fail.
- **coverage** — the eight rules and nine defect classes as frozen; a rule with
  no graded delta is the failure mode this seat exists to find.
- **depth:density (non-target guard)** — this item writes one receipt and no
  instrument bytes, so the tracked-footprint delta is one file.

No mutating git/jj command was run anywhere. No tool installed, no pacman, no
network fetch, no PATH write, no `~/.local/bin` write, no host-service restart.
No lane file was edited except this receipt.

## What was reviewed (bytes, hashes, live-edit note)

The gate itself (`claim-package-check.py`) and the fixtures are not in the tree at
review time — they are in-flight seat deliverables. The executable rule surface
that exists is the three sibling rule modules in this wave dir:

| Module | Rules | Bytes | sha256 at probe time | mtime |
|---|---|---:|---|---|
| `ExecGateManifest.rules.py` | R-FILES, R-MANIFEST, R-REDACT | 14379 | `e8131998f246684a9876d4a18769e544379a70146bf72f817bf929811b18a81b` | 13:41:57 |
| `ExecGateChain.rules.py` | R-CUSTODIAN, R-STATUS | 13115 | `6f0f1c42082652cdfd8ea6172ee96ab2e8450aca2fc20397e051adffa102c542` | 13:41:41 |
| `ExecGateProvReport.rules.py` | R-PROVENANCE, R-REPORT, R-NOSECRET | 15871 | `ddb2f2e3153fc8d907b5f0c06f9d991d136b0d4fd471c98871e663a50e91b3d9` | 13:46:51 |

`ExecGateProvReport.rules.py` was edited by its seat while this review ran; the
second hash it carried during the window was
`97003db342b713d20a159690e289c1b3aaeb7091a9a07531a44a6d1d80dc3aa5` (13:47:39).
`diff -u` between the two shows one line: `session_cookie` added to the
`session-cookie` alternation. Both batteries were re-run against the newer bytes
and the outputs are byte-identical (`probe2 identical on new bytes`,
`probe3 identical on new bytes`), so no finding below depends on the race.

Key inputs read (read-only): `corpus/knowledge/claim-package-contract.md`
(68 lines, the authoritative contract), `ScoutClaimContract.md` (the
contract-vs-lost-checker key map), `ScoutSiblingOverlap.md`, `.ufo/waves/round-43/
INTEGRATION-PLAN.md`, and `w1-spec.json` items `ExecGateCore`, `ExecGateManifest`,
`ExecGateChain`, `ExecGateProvReport`, `ExecGateFixtures`, `ExecGateSelftest`,
`MutGateRules`, `RevGateRules`, `RevGateFixtures`.

There is no `lsp` device mounted in this seat and the callers are Python functions
in a not-yet-landed script, so semantic-caller proof by LSP is unavailable. The
substitute used is stronger than grep for this object: each rule was **executed**
against a constructed package, and each deletion candidate was applied to a scratch
copy and the verdict vector re-measured (below). That is the contract the deletion
must not break.

## Method (one passing baseline, then one delta at a time)

A synthetic six-file package was built that passes all eight rules under the three
modules (`probe.py`, 401 lines, sha256 `eda734fd…a6452`). Every delta is applied to
a fresh copy of those bytes and the full eight-rule verdict vector is printed. Two
further batteries run the ungraded-rule test (`probe2.py`, 338 lines,
`d257a190…ce70d`), the deletion-candidate proofs and the exemplar constraint
(`probe3.py`, 225 lines, `762e2e5a…09965`), and the per-file removal matrix
(`probe4.py`, 16 lines, `76669705…3d05`). All scratch lived under
`/fast/scratch/hyaku/kasegi-r43/SimplifierGate/` with `TMPDIR` set to it explicitly.

Baseline output (real, one run):

```
R-FILES        pass  files=6/6 missing=0 notregular=0
R-MANIFEST     pass  artifacts=2 positive=1 negative=1 digest-bad=0 escape=0 missing=0 shape=0
R-REDACT       pass  redactions=2 artifacts=2 covered=2 unbound=0 identity-bad=0 digest-bad=0
R-CUSTODIAN    pass  actions=1 grant-bad=0 scope-bad=0 fields-bad=0 head=ok expected-head=ok
R-STATUS       pass  manifest-bind=ok gates=4 gates-fail=0 subchecks=2 subchecks-fail=0 finding_count=0 reviewer-fields=ok reviewer-collide=0 claimable=false blocker=yes
R-PROVENANCE   pass  agents=1 transitions=1 commands=1
R-REPORT       pass  cited=2 manifest=3 absent=0
R-NOSECRET     pass  files=8 hits=0 symlinks=0 oversize=0 classes=none
```

The nine frozen defect classes, each applied to that baseline, one delta per copy:

| C2 class | delta built | failing rules (measured) |
|---|---|---|
| 1 missing sixth file | `claim_checklist.md` removed | R-FILES |
| 1 variant | `status.json` removed | R-FILES, R-STATUS |
| 2 artifact digest wrong | artifact **bytes** mutated | R-MANIFEST |
| 2 variant | recorded **digest** rewritten | R-MANIFEST, R-REDACT |
| 3 negative-only polarity | both artifacts `negative` | R-MANIFEST |
| 4 artifact path escape | `../../outside.txt` | R-MANIFEST |
| 4 variant | artifact symlink inside package | R-MANIFEST, R-NOSECRET |
| 5 empty redactions | `redactions: []` | R-REDACT |
| 6 custodian head mismatch | `head_sha256` changed | R-CUSTODIAN |
| 7 reviewer == producer (manifest key) | `manifest.producer_identity` = reviewer | R-STATUS |
| 7 reviewer == producer (status key) | `claim_review.producer_identity` = reviewer | **NONE — accepted** |
| 8 report without marker | marker line deleted | R-REPORT |
| 9 secret-shaped token | natural JSON `"api_key": "<32 hex>"` in provenance | R-NOSECRET |

## Q1 — Duplicate rules: does R-REDACT subsume part of R-MANIFEST?

**No, and the reverse is also false.** The two are disjoint on bytes:

- Mutate the artifact bytes (class 2, correct construction) → `R-MANIFEST
  fail digest-mismatch`, R-REDACT `pass`. R-REDACT binds the receipt to the
  *declared* digest, not to the bytes, so it cannot see a byte-level mismatch.
- `redactions: []` (class 5) → `R-REDACT fail empty-redactions`, R-MANIFEST `pass`.
  R-MANIFEST never reads `redactions`.

So neither rule subsumes the other and both must stay. What *is* duplicated is a
failure **surface**, not a rule:

1. **`manifest.expected_head_sha256` absent** fails two rules for one delta:
   `R-MANIFEST fail=head-missing` and `R-CUSTODIAN expected-head=absent`
   (`P1 expected_head_sha256 absent → failing=R-MANIFEST,R-CUSTODIAN`). C2 assigns
   the binding — "head_sha256 equal to … manifest.expected_head_sha256" — to
   R-CUSTODIAN only. `head-missing` is at `ExecGateManifest.rules.py:230-232`.
2. **A symlink** fails up to three rules for one delta. Symlinked artifact:
   `R-MANIFEST fail=path-escape` + `R-NOSECRET fail=symlink-entry`. Symlinked
   `report.md`: `R-FILES fail=not-regular-file` + `R-REPORT fail=report-missing`
   + `R-NOSECRET fail=symlink-entry` (`G6`, three rules, one delta).
3. **A rewritten recorded digest** (class-2 built the wrong way) fails
   R-MANIFEST + R-REDACT (`unbound-receipt,uncovered-artifact`), because the receipt
   still points at the old digest. That is correct behaviour, but it is exactly the
   contamination `RevGateFixtures` will call "fails for the wrong reason" if the
   fixture is built that way (see the construction constraints below).

Also non-subsuming but redundant: `R-REDACT`'s coverage set re-derives artifact
digests with `_is_sha256(entry["sha256"])` instead of consuming R-MANIFEST's
verified set, so there are two authorities for "what is a declared artifact digest".
The CLI can pass the parsed manifest (`manifest=` parameter already exists in all
three modules); it should also pass the verified digest set, or R-REDACT should
accept a `declared` argument. No verdict changes on any of the ten cases —
interface only.

## Q2 — Fixtures that differ only cosmetically / fail for the wrong reason

**None of the nine frozen classes is a cosmetic duplicate.** The per-file removal
matrix (measured, `probe4.py`) shows why class 1 is not interchangeable with any
other class, and why classes 2/3/4 are three distinct predicates of one rule:

```
report.md                    -> ['R-FILES', 'R-REPORT']
claim_checklist.md           -> ['R-FILES']
evidence/manifest.json       -> ['R-FILES', 'R-MANIFEST', 'R-REDACT', 'R-CUSTODIAN', 'R-STATUS', 'R-REPORT']
custodian-receipts.json      -> ['R-FILES', 'R-CUSTODIAN']
provenance.json              -> ['R-FILES', 'R-PROVENANCE']
status.json                  -> ['R-FILES', 'R-STATUS']
```

`claim_checklist.md` is the **only** file whose removal is single-rule. The
selftest's class 1 ("missing sixth file") therefore has exactly one valid
construction; any other file produces a wrong-reason fixture. The four
wrong-reason traps measured:

1. class 1 with `status.json`/`report.md`/… removed → two or six rules fail.
   `RevGateFixtures` will reject it; `ExecGateSelftest` requires
   `observed==expected` and will mark the case `verdict=fail`.
2. class 2 built by rewriting the recorded digest → R-MANIFEST **and** R-REDACT.
   Mutate the artifact file bytes instead.
3. class 7 built by writing `claim_review.producer_identity` (the field the lost
   `claim-check.mjs` actually compared) → **the gate accepts the package**
   (`D7b … failing=NONE`). `_manifest_identities` (`ExecGateChain.rules.py:143-163`)
   only folds manifest-level keys and redaction producer/verifier keys; the status
   object's `claim_review.producer_identity` is never in the compare set. This is
   both a fixture trap and a real acceptance hole: C2 says the reviewer identity
   must be "distinct from every producer", and the producer field the contract's
   own history uses is that one.
4. class 9 built by escaping the token inside a JSON string
   (`"note": "api_key = \"<hex>\""`) → **no rule fails** (`G1 … failing=NONE`);
   the backslash before the quote defeats the optional-quote in the
   `labelled-hex` pattern. The natural JSON form `"api_key": "<32 hex>"` is caught
   (`D9 → R-NOSECRET`). A fixture written the escaped way is a silent pass, not a
   cosmetic variant.

A fifth, exemplar-facing trap, measured (`G7`): a report that carries the
contract-mandated scope-excerpt `content sha256` **fails R-REPORT** unless that
digest is also registered as an artifact in `evidence/manifest.json`:

```
R-REPORT  fail  cited=2 manifest=2 absent=1 fail=cited-digest-absent
```

Since the contract's report row *requires* "Scope excerpt = verbatim policy text +
URL + observed_at + content sha256", R-REPORT's cited-digest limb is an implicit
requirement that the exemplar register the policy capture as a (negative-polarity)
artifact with its own redaction receipt. My passing baseline does exactly that
(`evidence/policy.txt`, `polarity: negative`, second receipt). If
`ExecExemplarPackage`/`ScribeExemplarReport` writes the report the way the contract
describes without that artifact, the exemplar prints `DEFECT` and C2's
`rules=8 pass=8` dies. This is the single highest-value finding for the L1.

## Q3 — Keys the contract states that no consumer reads

Measured by token search over the three modules:

- `status.state`, `status.severity`, `status.reward`, `status.do_not_submit`,
  `status.no_submission_performed`, `claim_review.claim_ready`,
  `claim_review.outcome`, `claim_checklist.md`'s `OPERATOR-GATED` — **no rule
  reads any of them**. For `severity`/`reward`/`do_not_submit`/
  `no_submission_performed` that is correct and required by the contract's
  round-13 boundary note (the lost checker never read them either); for
  `OPERATOR-GATED` ScoutClaimContract records C2's intent: exemplar content, not a
  rule verdict. Leave unread. Do not add.
- `status.claimability_blocker` and `status.resume_condition` — contract keys,
  **unread**, while R-STATUS invents four substitutes (`blockers`,
  `residual_gates`, `remaining_gates`, `blocker_codes`,
  `ExecGateChain.rules.py:171-172`). Measured both ways: a package that names its
  blocker in the contract's own key **fails** (`G2 claimability_blocker only →
  R-STATUS blocker=no`) and a package that names it in a lane-invented key
  **passes** (`G3 residual_gates only → failing=NONE`). The key set is wider than
  the contract and narrower than the contract at the same time. This is the one
  contract-key gap that is a defect rather than a deliberate omission.
- `chain[].input_sha256` — contract brace names it, R-CUSTODIAN requires it
  non-empty, and **nothing binds its value to anything**. It is a presence-only
  key: one fixture can prove absence (`P5 → R-CUSTODIAN fields-bad=1`), none can
  prove a wrong value. Keep it (contract brace, one line in `_CHAIN_KEYS`) but the
  rule table must label it presence-only, not call it a digest check.
- `provenance`'s `secrets_attestation` **is** read; `R-NOSECRET` remains the actual
  scan. No conflict.

## Q4 — Rules that cannot fail in the graded surface

**R-PROVENANCE is the rule whose fixture always passes it, because it has no
fixture at all.** The nine classes cover seven rules — R-MANIFEST three times,
R-FILES/R-REDACT/R-CUSTODIAN/R-STATUS/R-REPORT/R-NOSECRET once each — and
R-PROVENANCE zero times. Arithmetic: 3 + 1 + 1 + 1 + 1 + 1 + 1 = 9 of 10 cases,
with the tenth spent on the degenerate control.

Measured consequence: a copy of the module with `rule_provenance` replaced by an
unconditional pass produces **identical eight-rule verdict vectors on every one of
the ten delta packages** (`identical_verdict_vectors=10/10`) and **8/8 pass on the
exemplar-shaped baseline** (`real=pppppppp gutted=pppppppp identical=True`). So the
ten-case selftest would print `selftest cases=10 failures=0` for a gate from which
R-PROVENANCE had been deleted, and from which all eleven of its reason codes
(`agents-empty`, `transitions-empty`, `commands-empty`, `pin-missing`,
`policy-sha256-invalid`, `external-effects-absent`, …) had vanished. That is the
frozen claim's largest ungraded surface: the rule with the most limbs
(~80 lines, 11 reasons, 7 key groups) is the one the cases never exercise.

A second, smaller cannot-fail limb: **R-REPORT's `no-cited-digest`** cannot fire on
a report that satisfies the contract's own report row, because that row mandates
the scope-excerpt `content sha256`, which is itself a 64-hex citation. Measured:
remove one of the two cited digests → `P7 failing=NONE`; remove both (already
contract-violating) → `G4 R-REPORT fail=no-cited-digest`. C2's clause is
"every artifact's sha256 it cites", which is vacuously true at zero citations.

The `claimable: true` half of R-STATUS (~20 lines: gates PASS, subchecks PASS,
`finding_count >= 1`) is likewise untested by the ten cases. It is retained
deliberately — see tradeoffs.

## Minimal set that keeps every defect class caught

Keep all eight rules and all nine classes: no rule is deletable and no class is
cosmetic (Q1, Q2). Cut weight **inside** the rules, where every cut was re-measured:

| # | Cut | Anchor | Measured effect |
|---|---|---|---|
| 1 | `head-missing` from R-MANIFEST | `ExecGateManifest.rules.py:230-232` | removes the duplicate surface; the key is still enforced by R-CUSTODIAN (`P1`), which C2 names as its owner |
| 2 | blanket `..` reject in `_artifact_target` | `:145-150` | outside `..` still `path-escape` (realpath prefix catches it); inside `sub/../trace.txt` stops being a false positive (`probe3`: original `path-escape` → patched `[]`) |
| 3 | `scanned_artifact_sha256` limb | `:328-331` | contract never names the key; absent is already accepted (`P2 → NONE`), so the limb grades nothing the contract states — `artifact_sha256` (equal to the artifact digest) is the "same-digest" check |
| 4 | `decisions` / `custodian_chain` aliases | `ExecGateChain.rules.py:200` | C2 says "chain"; `custodian_chain` is attested by no source. Measured: alias package passes (`P4 → NONE`), i.e. the alias adds acceptance, not coverage |
| 5 | four invented blocker keys | `ExecGateChain.rules.py:171-172` | replace with `verdict` (contract free-form, already the short-circuit) + `claimability_blocker`; measured: contract key currently fails (`G2`), invented key passes (`G3`) |
| 6 | `no-cited-digest` | `ExecGateProvReport.rules.py:351` | cannot fire on a contract-conformant report (`P7`/`G4`); C2's clause is vacuous at zero |
| 7 | head + redaction digests in `_manifest_digests` | `ExecGateProvReport.rules.py:302,308` | C2 says "artifact's sha256"; measured: a report citing only the head digest passes (`P6 → NONE`) though it cites no artifact. Redaction digests are ⊆ artifact digests for any package that passes R-REDACT, so the loop is dead weight |
| 8 | `symlink-entry` verdict from R-NOSECRET | `ExecGateProvReport.rules.py:411-412` | third authority for symlinks; keep the walk-level skip (`islink → continue`), drop the fail. Measured: symlinked artifact still `R-MANIFEST path-escape`; symlinked `report.md` still `R-FILES` + `R-REPORT` |
| 9 | unstated key aliases: `producer_identity`/`verifier_identity` as producer keys, `name`, `cmd`, `exit`, `url`, `sha`, `identity`-as-agent | `ExecGateManifest.rules.py:81-82`; `ExecGateProvReport.rules.py:87-92` | each doubles accepted key space; contract names `producer`, `verifier`, `command`, `exit_code`, `pin.remote`, `pin.commit`. `[INFERENCE]` no verdict changes on the exemplar; narrowing only rejects spelling drift the contract does not license |
| 10 | duplicate `session-cookie` label on two patterns | `ExecGateProvReport.rules.py:76,79` | cosmetic (two regexes, one class string); merge to one label or keep both patterns under `session-token` |

One **addition**, not a cut: R-STATUS must add `claim_review.producer_identity`
(and `producer_identity` at status level) to the compare set
(`ExecGateChain.rules.py:143-163`). Salary: one fixture delta; it closes the only
route by which a package can self-approve after passing the current rule (`D7b`).

One **re-target**, freezing ten cases: point the degenerate-control case's package
at a provenance-broken delta (e.g. `external_effects_performed: ["submission"]`,
measured `P11 → R-PROVENANCE fail=external-effects-not-empty-list`) instead of a
clean exemplar copy. The control's purpose — prove the selftest rejects an
always-pass stand-in — is unchanged, the case count stays ten, no new fixture dir
is needed, and R-PROVENANCE enters the graded surface, which the 10/10
identical-vector measurement shows it currently is not.

If the L1 will not re-target the control, then C2 must at minimum state in the
instrument/receipt that R-PROVENANCE is graded only by the exemplar positive and by
no defect fixture; an ungraded rule that is not declared is exactly the
"check that cannot see its own defect" the C1 kill rule treats as a defect.

## Tradeoffs, and what this seat did not cut

- **`claimable: true` branch kept.** No case exercises it and the exemplar is
  `claimable: false`, so YAGNI says delete; but it is the only code path that
  expresses the contract's `DONE` semantics and the gate's stated reason to exist
  outlives this round's exemplar. Deleting it would harm the capability axis, so it
  stays and is named ungraded here instead.
- **`oversize-file`, `program-url-absent`, `unreadable-file` reasons kept.** All
  three are falsifiable, none is in C2, none has a fixture. `oversize-file` is a
  genuine secrets-scan gap guard; `program-url-absent` is contract-row-backed
  (report row: program + official URL). They are extra surface, not duplicates.
- **`input_sha256` presence kept** (contract brace), labelled presence-only.
- **The `..` cut (#2) removes one `MutGateRules` mutation target** ("allow a path
  with `..` that resolves inside"). That mutant currently has no fixture among the
  nine either, so it survives the selftest today; cutting the block makes the
  mutant moot rather than newly survivable. Stated because it is the only cut whose
  loss is measurable anywhere.
- **The symlink cut (#8) means a stray symlink in `evidence/` that is neither a
  contract file nor a listed artifact no longer reddens the package.** C2 does not
  name that class; the reading rules still refuse to follow it, so the kill-rule
  clause ("the gate reading package bytes from outside the package directory")
  stays satisfied.
- Not my item, not run: the CLI's exit codes, the aggregate `rules=8` line, the
  selftest's own implementation, R30 corrupt-JSON behaviour (`RevGateRules` owns
  it). This seat measured rules only.

## Tooling / scratch

- No tool installed or upgraded; no pacman (host-wide pause honoured); no network
  fetch; no PATH write; no operator-owned config touched.
- Python 3.14.8 host interpreter, stdlib only. Scratch root
  `/fast/scratch/hyaku/kasegi-r43/SimplifierGate` (2.0M at removal) held the probe
  drivers, the frozen module copies and every built package; `TMPDIR` was set to it
  explicitly in every invocation.

Removal, real output:

```
$ S=/fast/scratch/hyaku/kasegi-r43/SimplifierGate; test -d "$S" && echo "before: present, $(du -sh "$S" | cut -f1)"
before: present, 2.0M
$ rm -rf -- "$S"; test ! -d "$S" && echo "scratch_removed=yes path=$S"
scratch_removed=yes path=/fast/scratch/hyaku/kasegi-r43/SimplifierGate
```

Probe drivers were removed with the scratch, so their hashes are recorded here:
`probe.py` 401 lines `eda734fd162a09d112433c421fa409f98a67c86fb1cccecbe4675671e11a6452`;
`probe2.py` 338 lines `d257a1900f26354b9282a766f2f61d83b2fe22234317c95502d6ce17d70ce70d`;
`probe3.py` 225 lines `762e2e5abf2f1b2fe08cba928562963b7417be629af95748f6c5041861709965`;
`probe4.py` 16 lines `766697053756bcb6051367ed8193de62fc725564d8461e49195eb134a5dd3d05`.

No separate deliverable: this item produces no landable text, only this receipt.
Any cut above is a recommendation with a line anchor and a measurement; the L1 (or
the owning executor) applies it, and `ExecGateFixtures`/`ExecGateSelftest` must
then be re-run in one pass.
