# ExecGateCore — C2 executable gate core (round 43, wave 1)

Seat: ExecGateCore (executor, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Freeze commit (lane HEAD while this seat ran): `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`.
Measured base named by the claims: `ab98fac9dce87130bc4f66de89e30650d63943dc` (parent of the
freeze commit; `git merge-base --is-ancestor ab98fac9 HEAD` = yes).

Read first, not edited: `.ufo/waves/round-43/claims.json` (frozen), then the specification:
`corpus/knowledge/claim-package-contract.md` (six-file table, status semantics, provenance
correction) and `corpus/knowledge/claim-gates.md` (per-gate derivations of the lost
`ops/claim-check.mjs`, incl. the blanket symlink ban and the 5 MiB cap). Control read:
`.ufo/waves/round-43/c2-controls/before.txt`.

## Deliverables

| path (lane-relative) | lands at | bytes | lines | sha256 |
|---|---|---|---|---|
| `.ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py` | `corpus/instruments/claim-package-check.py` | 32520 | 802 | `8b6f849349157a91dd7a2a3998c1f3956e8fed2dbd565c40815660cbd71cc8e6` |
| `.ufo/waves/round-43/w1/ExecGateCore.rules.txt` | reference table (receipt-side) | 10382 | 160 | `59875e76d88eb63b379bd18e4508fc2e70ea38bda4cdc0ade9b4bf1a63073da1` |

Byte identity: the scratch source and the delivered file hash to the same digest and
`cmp` reports no difference (`byte-identical`). No other lane file was written by this seat.

## What the gate decides

Eight rules, fixed order, one line each, then the verdict line. Exit 0 only at 8/8; 1 on any
fail; 2 on usage, a missing/non-directory package, or `--selftest` with no implementation.
The exact predicate and the contract sentence behind each rule are in
`ExecGateCore.rules.txt`; the module docstring repeats the table.

    R-FILES      six contract files, regular, non-symlink, non-empty, four JSON objects parse
    R-MANIFEST   schema string, numeric sequence, 64-hex head, per-artifact recomputed digest,
                 polarity enum with >=1 positive, relative confined paths
    R-REDACT     redactions[] non-empty, exactly one bound receipt per artifact,
                 artifact==scanned==manifest digest, non-empty distinct producer/verifier
    R-CUSTODIAN  non-empty chain, per-decision grant id + exact NO_SCOPE_OBJECTION, head ==
                 final decision digest == manifest.expected_head_sha256
    R-PROVENANCE agents with requested/resolved models, commands with exit codes, pin, policy
                 digest, external_effects_performed == [], secrets attestation
    R-STATUS     recomputed manifest_sha256, hard gates + subchecks + reviewer fields, reviewer
                 distinct from every manifest producer/verifier, claimable coherence
    R-REPORT     `Scope excerpt`, literal `No submission performed`, https URL, every cited
                 64-hex digest present in the manifest
    R-NOSECRET   symlink ban, 5 MiB cap, secret-shape scan; the value is never printed

What it does NOT decide (stated here so the capability row cannot over-claim): the lost
`claim-check.mjs` parity (its state/severity/reward, prior-submission global scan, nested
readiness contexts and reviewer role string are not modelled), and operator gates —
submission, prior-submission, reviewer appointment. Those stay in `claim_checklist.md`.

Read confinement (P0: `inspect_path`, lines 155-196; the `Package` reader at 197-244): every opened path is built from the package root,
must be relative with no `..`, has no symlink at any component, and must realpath beneath the
root. Fail-closed (P1): a read/parse/type failure or an unexpected exception is a FAIL of the
rule that needed the input, never a pass.

## Transcript — the two required runs, plus the error path

```
$ python3 claim-package-check.py pkg-two-file
RULE R-FILES verdict=fail detail=missing=4,bad=0
RULE R-MANIFEST verdict=fail detail=missing
RULE R-REDACT verdict=fail detail=missing
RULE R-CUSTODIAN verdict=fail detail=missing
RULE R-PROVENANCE verdict=fail detail=missing
RULE R-STATUS verdict=fail detail=missing
RULE R-REPORT verdict=fail detail=missing
RULE R-NOSECRET verdict=fail detail=hits=1,first=report.md,shape=credential
package=pkg-two-file rules=8 pass=0 fail=8 verdict=DEFECT exit=1
exit=1

$ python3 claim-package-check.py pkg-pass
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=2,positive=1,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=2,receipts=2,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=2,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=2,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=1,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=pkg-pass rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0

$ python3 claim-package-check.py /nonexistent/pkg
package=/nonexistent/pkg verdict=ERROR exit=2
exit=2
```

## Single-delta battery — nine defect classes and the junk twin

Built from the passing package by one delta each (`deltas.py` in scratch, transcript verbatim):

```
1 missing sixth file           exit=1 failing=R-FILES,R-PROVENANCE
2 artifact digest wrong        exit=1 failing=R-MANIFEST
3 negative-only polarity       exit=1 failing=R-MANIFEST
4 path escaping package        exit=1 failing=R-MANIFEST
5 empty redactions             exit=1 failing=R-REDACT
6 custodian head mismatch      exit=1 failing=R-CUSTODIAN
7 reviewer == producer         exit=1 failing=R-STATUS
8 report without marker        exit=1 failing=R-REPORT
9 secret in provenance         exit=1 failing=R-NOSECRET
10 junk twin (exemplar copy)   exit=0 failing=(none)
```

Class 1 (missing sixth file) also reds the rule that owns the deleted file: fail-closed by
design, so the fixture index should name `R-FILES` (first failing in canonical order). Classes
2-9 each red exactly their own rule. Class 2 is built by mutating the ARTIFACT BYTES; editing
the manifest digest instead reds R-MANIFEST **and** R-REDACT (receipt no longer matches the
manifest) **and** R-REPORT (report cites the true digest) — measured, and sent to
ExecGateFixtures.

## Fail-closed battery (R30)

```
corrupt evidence/manifest.json   exit=1 failing=R-FILES,R-MANIFEST,R-REDACT,R-CUSTODIAN,R-STATUS,R-REPORT
corrupt custodian-receipts.json  exit=1 failing=R-FILES,R-CUSTODIAN
corrupt provenance.json          exit=1 failing=R-FILES,R-PROVENANCE
corrupt status.json              exit=1 failing=R-FILES,R-STATUS
truncated custodian-receipts.json exit=1 failing=R-FILES,R-CUSTODIAN
absolute artifact path           exit=1 failing=R-MANIFEST
dotdot artifact path             exit=1 failing=R-MANIFEST
stray symlink in tree            exit=1 failing=R-NOSECRET
file over 5 MiB                  exit=1 failing=R-NOSECRET
unreadable provenance.json       exit=1 failing=R-FILES,R-PROVENANCE,R-NOSECRET
unreadable evidence file         exit=1 failing=R-NOSECRET
manifest is a JSON array         exit=1 failing=R-FILES,R-MANIFEST,R-REDACT,R-CUSTODIAN,R-STATUS,R-REPORT
package argument is a file       exit=2 failing=(none)
--selftest without implementation exit=2 failing=(none)
```

### Confinement (read only under the package root)

The three escaping-artifact shapes, each graded by the delivered bytes (the absolute and `..` cases
change one manifest path; the symlink case replaces `evidence/adv.txt` with a link to a sibling
artifact, leaving the manifest and the report untouched):

```
### confinement: escaping artifact paths must fail R-MANIFEST
absolute artifact path         exit=1 failing=R-MANIFEST
dotdot artifact path           exit=1 failing=R-MANIFEST
symlink artifact               exit=1 failing=R-MANIFEST,R-NOSECRET
  detail: RULE R-MANIFEST verdict=fail detail=artifacts=2,escape=1
```

The symlink also reds R-NOSECRET, because claim-gates records a blanket symlink ban beside the
manifest-artifact confinement check; those are two independent gates and both fire. No rule reads a
byte outside the package root: `inspect_path` rejects absolute, `~`, backslash, NUL and `..` before
any open, lstats every component and rejects a symlink at any of them, then requires the real path to
be the root or beneath it.

Two findings from this battery were fixed in the delivered bytes before the transcript above:
(1) a JSON-quoted credential (`"api_key": "…"`) was missed because the separator follows a
closing quote — and a JSON-escaped quoted value (`\"`) needs the optional backslash too; the
scan now handles both, and `Authorization: Bearer <token>` got its own shape. (2) an
unreadable file inside R-NOSECRET's walk returned without failing; it now raises FAIL.
A 15-character value is still not a hit (`near-short`/`short-neg` cases), so the rule does not
red ordinary prose.

## JSON mode

```
$ python3 claim-package-check.py pkg-pass --json | python3 -c "import json,sys; d=json.load(sys.stdin); print('verdict=%s pass=%d fail=%d exit=%d ids=%s' % (d['verdict'], d['pass'], d['fail'], d['exit'], ','.join(r['id'] for r in d['rules'])))"
verdict=WELL-FORMED pass=8 fail=0 exit=0 ids=R-FILES,R-MANIFEST,R-REDACT,R-CUSTODIAN,R-PROVENANCE,R-STATUS,R-REPORT,R-NOSECRET
```

## Predicate decisions: contract-stated vs lane convention

Stated and enforced as written: the six file names; `evidence-manifest/v1`; per-artifact
sha256 over the bytes; polarity enum and >=1 positive; relative confined artifact paths;
one same-digest receipt per artifact with non-empty distinct producer/verifier; non-empty
chain with exact `NO_SCOPE_OBJECTION` and non-empty grant id; three-way head binding; agents +
requested/resolved models; commands + exit codes; pin; `policy_sha256`; empty
`external_effects_performed`; secrets attestation; `manifest_sha256` over manifest bytes;
hard gates + subchecks + reviewer distinctness/fields; claimable coherence; `Scope excerpt`;
literal `No submission performed`; cited digests in the manifest; the secret regex, symlink
ban and 5 MiB cap (claim-gates).

Lane conventions, enforced and labelled `[convention]` in `rules.txt`:
- redaction receipts bind by `artifact` = manifest path (or `evidence/<path>`); when the field
  is absent, a digest matching exactly one artifact binds it;
- `secrets_attestation` may be a non-empty string, or an object with `"no_secrets": true`;
- the report URL must be `https://` (the contract states "program + official URL", not a scheme);
- reviewer identity comparison is case-insensitive.

Not invented: no rule reads `status.state`, `status.severity`, `status.reward`, the reviewer
`role` string, or the report's impact prose — claim-gates records that the lost tool never read
those either, so gating them would claim more than the contract supports. Consequence worth
knowing: R-REPORT binds **every** 64-hex token the report prints, so a scope-excerpt content
sha256 must be registered as a manifest artifact (e.g. `evidence/scope-excerpt.txt`) and cited
from there.

## Exemplar integration — the delivered exemplar, assembled and graded

The exemplar's files landed in the wave dir as `ExecExemplarPackage.*` while this seat ran. The seat
assembled them into the landing layout in scratch (report.md, claim_checklist.md, the four JSON
files, and the four evidence files under `evidence/` with their bare names) and ran the gate. No
lane write was made for this check.

```
$ python3 claim-package-check.py exemplar
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=4,positive=3,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=4,receipts=4,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=3,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=9,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=4,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=exemplar rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

All four implementations accept those bytes: ExecGateManifest's three rules print pass, ExecGateChain's
two print pass, ExecGateProvReport's three print pass (verbatim tails in "Cross-implementation
reconciliation"). The exemplar's honest state survives: `claimable:false` with
`no_duplicate_or_prior_submission: PENDING` is accepted by the core and by ExecGateChain (neither
requires PASS when not claimable; a blocker must be named), so the pending gate is disclosed rather
than masked.

Fail-closed proof from the same package: the first assembly attempt kept the wave-dir prefixes on
the evidence files, so every artifact path missed. The gate did not shrug:

```
RULE R-MANIFEST verdict=fail detail=artifacts=4,escape=4
package=exemplar rules=8 pass=7 fail=1 verdict=DEFECT exit=1
```

## Nine defect fixtures, graded by the delivered gate

ExecGateFixtures' nine fixture dirs landed in the wave dir while this seat ran. Each was copied to
scratch WITHOUT its `expected-rule` file (so the package is the six files plus evidence, exactly what
lands) and graded by the delivered bytes; the expected rule is read from the fixture's own file.

```
$ python3 claim-package-check.py <each delivered defect fixture, copied without its expected-rule file>
defect-1-missing-file expected=R-FILES      exit=1 failing=R-FILES                                  own-rule=PASS
defect-2-digest      expected=R-MANIFEST   exit=1 failing=R-MANIFEST                               own-rule=PASS
defect-3-negative    expected=R-MANIFEST   exit=1 failing=R-MANIFEST                               own-rule=PASS
defect-4-escape      expected=R-MANIFEST   exit=1 failing=R-MANIFEST                               own-rule=PASS
defect-5-redaction   expected=R-REDACT     exit=1 failing=R-REDACT                                 own-rule=PASS
defect-6-custodian   expected=R-CUSTODIAN  exit=1 failing=R-CUSTODIAN                              own-rule=PASS
defect-7-reviewer    expected=R-STATUS     exit=1 failing=R-STATUS                                 own-rule=PASS
defect-8-marker      expected=R-REPORT     exit=1 failing=R-REPORT                                 own-rule=PASS
defect-9-secret      expected=R-NOSECRET   exit=1 failing=R-NOSECRET                               own-rule=PASS
junk-twin            exit=0 | package=<scratch>/fixture-run/junk-twin rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
```

Result: nine of nine print `verdict=DEFECT exit=1` with exactly their own rule failing and no other
rule red, and the byte-identical exemplar twin prints 8/8. This is the C2 acceptance property
("its named rule not the failing one") demonstrated against the delivered bytes, on the fixtures as
delivered — no lane file was modified for the run.

## Cross-implementation reconciliation (for the L1)

Three sibling modules landed beside my deliverable. They were read and then run against the same
assembled exemplar (output in the section above): every rule passes under every implementation, so
the differences below are width, not verdict, on this package. Read for the divergences; not
spliced, not modified:

| module | difference from the core | direction |
|---|---|---|
| `ExecGateManifest.rules.py:327-332` | `scanned_artifact_sha256` optional; "at least one" receipt per artifact | core is stricter (requires both digests equal, exactly one bound receipt) |
| `ExecGateManifest.rules.py:184-214` | R-FILES checks presence | core also requires non-empty files and JSON-object parse |
| `ExecGateChain.rules.py:166-186` | blockers may sit in `claim_review`; keys `remaining_gates`/`blocker_codes` accepted | core reads `status` and `blockers`/`residual_gates` + verdict strings; `status.blockers` satisfies both |
| `ExecGateProvReport.rules.py:196-220` | requires a non-empty `transitions` list | core treats it as optional; the delivered exemplar carries `transitions` (2), so both pass (addendum sent to ExecExemplarPackage) |

Recommendation: land the core unchanged as `corpus/instruments/claim-package-check.py`. Pasting
the three modules into it would duplicate `rule_*`/`run` symbols and widen the two rules above
(R-REDACT, R-FILES), relaxing the frozen C2 predicate. If a module is preferred for one rule,
replace the core function wholesale and re-run the exemplar and the nine fixtures.

## Splice immunity — the selftest paste cannot shadow the gate

The L1 routed a splice defect: a pasted selftest body that defines `RULES` (its tuple of case ids)
shadowed the gate's rule dict, so `run_rules` raised TypeError for every package. Fixed at the source:
the delivered module no longer binds any of the names a selftest plausibly reuses at module scope.
Its internals are now `_GATE_RULE_IMPL` (rule functions), `_GATE_RULE_ORDER` (canonical order),
`_GateFail` (the failure exception) and `_gate_token` (detail sanitiser); `run_rules` indexes the
private dict and catches the private exception, so a later `RULES = (...)` cannot reach it. No rename
is required of the selftest: it may keep `RULES` as its own constant.

Reproduction and fix, same pasted body in both files (the paste defines `RULES` as a tuple,
`RULE_ORDER`, a `Fail` function and `run_selftest`):

```
$ python3 oldcopy.py pkg-pass    # pre-fix shape: module-level RULES/RULE_ORDER/Fail
  (full traceback omitted; the two decisive lines)
TypeError: tuple indices must be integers or slices, not str
TypeError: catching classes that do not inherit from BaseException is not allowed
exit=1

$ python3 composite.py pkg-pass   # fixed shape: same pasted selftest body
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=2,positive=1,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=2,receipts=2,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=2,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=2,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=1,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=pkg-pass rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=0
exit=0

$ python3 composite.py --selftest  # the pasted hook is reached
selftest cases=10 failures=0
exit=0
```

The pre-fix shape was worse than a red gate: the shadowed `Fail` also invalidated `except Fail`, so the
traceback escaped the per-rule handler and the process died (exit 1) instead of reporting. The fixed
shape keeps 8/8 on the same package and reaches the pasted `run_selftest` hook.

## `--selftest` seam (landing dependency, not implemented here)

My item delegates the selftest to ExecGateSelftest. The core already carries the hook:
`main()` → `selftest_dispatch(rest)`, which calls a module-level `run_selftest(os.path.abspath(__file__))`
when defined. The paste anchor is the last comment line before the `__main__` guard:

    # <!-- selftest-body-paste-anchor: paste run_selftest(...) ABOVE this guard -->

Fallback: a sibling script `<gate dir>/claim-package-selftest.py` (or `$CLAIM_PACKAGE_SELFTEST`)
is executed as a subprocess. With neither present the measured behaviour is:

```
$ python3 claim-package-check.py --selftest
selftest module=/fast/scratch/hyaku/kasegi-r43/ExecGateCore/claim-package-selftest.py verdict=missing exit=2
```

i.e. exit 2, never a vacuous green. ExecGateSelftest was told the seam and the paste anchor.

## Coordination sent

- `agent://ExecGateFixtures`: single-delta construction constraints (digest class = mutate
  artifact bytes; missing file reds R-FILES + owner; `..` path is the single-rule escape
  delta; JSON-quoted `api_key` is caught; receipt binding by path).
- `agent://ExecGateSelftest`: the `--selftest` seam, the paste anchor, the exact parse grammar
  (8 `RULE` lines + summary with `exit=`), and the measured failing rule per single delta.
- `agent://ExecExemplarPackage`: full acceptance schema, plus an addendum (add `transitions`,
  both receipt digests, one receipt per artifact, blockers in `status.json`) so the exemplar
  passes both my core and the sibling module.
- `agent://KasegiR43`: routed the splice defect back with the reproduction, the fixed-shape run
  (8/8 and `--selftest` reaching the pasted hook) and the three confinement runs; recorded here in
  "Splice immunity" and "Confinement".
- `agent://ScribeExemplarReport`: refused — agent not running. The report digest rule (every
  64-hex token must be a manifest artifact digest) is in "Predicate decisions" above for the L1
  to relay.

## Method and tooling

- Tools installed: none. No pacman transaction, no network fetch, no git/jj mutation.
  Read-only git used: `rev-parse`, `cat-file -t`, `merge-base --is-ancestor`, `log`, `status`.
- Disk guard before the heavy pass: `/fast/scratch` 25% used, 604G free.
- Scratch bound to `S=/fast/scratch/hyaku/kasegi-r43/ExecGateCore`, `TMPDIR=$S` on every
  builder run; `gate.py` in that directory hashed identically to the delivered file
  (`8b6f8493…c8e6`), so every transcript and battery above is a run of the delivered bytes.
  The splice reproduction used `oldcopy.py` (the pre-fix naming) and `composite.py`
  (the delivered naming plus the same pasted body); neither is part of the deliverable.

## Risks / blockers

1. `--selftest` is red (exit 2) until ExecGateSelftest's function is pasted above the anchor or
   its companion script lands (not delivered when this receipt was written). That is the only C2
   after-state my item cannot produce alone. The paste itself is now safe: the routed RULES-shadowing
   defect is reproduced and fixed in "Splice immunity" above, and the selftest may keep its own
   `RULES` constant.
2. The exemplar and the nine fixtures are not yet committed under
   `corpus/instruments/fixtures/claim-package/`; the runs above are scratch copies of the delivered
   bytes. The exemplar files must land with their bare names (the wave-dir `ExecExemplarPackage.`
   prefix is a handoff convention, not part of the package). Landing order matters: the six files
   plus `evidence/{source-capture,source-excerpt,solution-fixed-in,disclosure-timeline}.txt` must be
   in place (bare names) before C2's counting command can repeat it.
3. R-REPORT's cited-digest rule will red any future package whose report cites a digest that is
   not a manifest artifact. It is resolved for this exemplar: the package registers
   `evidence/source-excerpt.txt` and the report cites its digest (`cited=4 unbound=0`). The rule
   stays strict, because relaxing it would make "every artifact's sha256 it cites" unverifiable.
   The behaviour change is named here so a later package author knows the excerpt text must be an
   artifact.
4. Deleting a JSON contract file reds R-FILES and the rule that owns it (fail-closed). The
   delivered defect-1 removes `claim_checklist.md`, which has no owning rule, so it reds exactly
   R-FILES — the measured nine-for-nine above. A future missing-file fixture over
   `provenance.json`/`custodian-receipts.json`/`status.json`/`evidence/manifest.json` would red two
   rules, and the selftest must grade the fixture's named rule rather than cardinality one.
