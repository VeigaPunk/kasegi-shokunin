# ExecGateChain — round-43 C2 rule module (R-CUSTODIAN + R-STATUS)

Seat `ExecGateChain` (executor, leaf). Lane `kasegi-shokunin`, round 43, base
`ab98fac9dce87130bc4f66de89e30650d63943dc`. Frozen claims read first at
`.ufo/waves/round-43/claims.json` and not edited. Owned item: C2 rule module
`rule_custodian` + `rule_status` for the eight-rule claim-package gate.

## Deliverables (beside this receipt; not landed by me)

| file | bytes | lines | sha256 |
|---|---|---|---|
| `ExecGateChain.rules.py` | 13115 | 350 | `6f0f1c42082652cdfd8ea6172ee96ab2e8450aca2fc20397e051adffa102c542` |
| `ExecGateChain.transcript.txt` | 19553 | 322 | `1f0259c7cfcb00f7873fcf416da6bb75fccc6484001f12bb3f2cacc3251c4fe8` |

`python3 -m py_compile ExecGateChain.rules.py` → ok (no output, exit 0).

## Interface `ExecGateCore` must use

The delivery name contains a dot, so it is loaded by path, not imported by
module name. Verified in transcript section 1 with
`importlib.util.spec_from_file_location('chain_rules', <path>)`:

```
RULE_IDS = ["R-CUSTODIAN", "R-STATUS"]
rule_custodian(pkg) -> (verdict: bool, detail: str)
rule_status(pkg)    -> (verdict: bool, detail: str)
run(pkg)            -> [("R-CUSTODIAN", verdict, detail), ("R-STATUS", verdict, detail)]
```

`detail` is the text after `detail=` (no spaces in any field name; fields are
`k=v` pairs). The module also runs standalone as
`python3 ExecGateChain.rules.py <package-dir>`: it prints the two
`RULE <id> verdict=pass|fail detail=<detail>` lines plus
`package=<path> rules=2 pass=<k> fail=<m>` and exits 0/1. Neither rule raises
for bad input: missing / unreadable / truncated JSON, a wrong container type
and a refused path all return `(False, "error=<short>")`.

## Predicates as implemented

R-CUSTODIAN — reads `custodian-receipts.json` and `evidence/manifest.json`:
- chain is `chain` (also accepted: `decisions`, `custodian_chain`), non-empty;
- every action is an object carrying all five of `action`, `input_sha256`,
  `decision_sha256`, `matched_grant_id`, `scope_signal`, each a non-empty
  string (`fields-bad` counts actions missing any);
- every action's `matched_grant_id` non-empty (`grant-bad`), `scope_signal`
  exactly `NO_SCOPE_OBJECTION` (`scope-bad`);
- three-way head binding, reported as two legs: `head` = `head_sha256` equals
  the final action's `decision_sha256`; `expected-head` = `head_sha256` equals
  `manifest.expected_head_sha256`; both legs must be `ok`.

R-STATUS — reads `status.json` and the manifest bytes:
- `manifest-bind`: `status.manifest_sha256` equals the sha256 recomputed over
  the manifest file bytes (never trusted from the file);
- `claim_review` object with non-empty `hard_gates` and `subchecks`, every
  entry PASS; mapping `{name: verdict}` and list-of-objects
  `{"name": ..., "verdict"|"status"|"result"|"pass": ...}` both accepted;
- `reviewer`: non-empty `identity`, `requested_model`, `resolved_model`, and
  `fallback` a JSON boolean; folded reviewer identity must not equal any
  producer/verifier identity recorded in the manifest (top-level
  producer/verifier keys and every `redactions[]` producer/verifier;
  `reviewer-collide` counts the collision);
- `claimable` must be a JSON boolean. `true`: bind ok, every hard gate and
  subcheck PASS, `finding_count` an int >= 1. `false`: a named blocker —
  non-empty `blockers` / `residual_gates` / `remaining_gates` /
  `blocker_codes` (status or claim_review) or a non-empty `verdict` string.
  Absent/non-boolean `claimable` fails closed (`claimable=absent`).

Path discipline: only `<pkg>/evidence/manifest.json`, `<pkg>/status.json` and
`<pkg>/custodian-receipts.json` are read; an absolute path, `..`, a symlink at
the leaf or a realpath escaping the resolved package root is refused.

## Evidence

Command that produced the transcript (scratch dir since removed):

```
cd /fast/scratch/hyaku/kasegi-r43/ExecGateChain/final \
  && TMPDIR=/fast/scratch/hyaku/kasegi-r43/ExecGateChain/final \
     python3 drive.py 2>&1 | tee \
     /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-43/w1/ExecGateChain.transcript.txt
TRANSCRIPT_RC=0
```

The transcript header prints the module path and sha256
`6f0f1c42…2c542`, identical to the delivered file's sha256 (checked after the
run with `sha256sum`). It prints the exact fixture bytes that are digest
inputs (`evidence/manifest.json`, `custodian-receipts.json`, `status.json`),
then every command's argv and real stdout/stderr/exit.

Baseline (scratch package passing both), literal output:

```
RULE R-CUSTODIAN verdict=pass detail=actions=2 grant-bad=0 scope-bad=0 fields-bad=0 head=ok expected-head=ok
RULE R-STATUS verdict=pass detail=manifest-bind=ok gates=4 gates-fail=0 subchecks=2 subchecks-fail=0 finding_count=1 reviewer-fields=ok reviewer-collide=0 claimable=true blocker=n/a
package=/fast/scratch/hyaku/kasegi-r43/ExecGateChain/final/pkg rules=2 pass=2 fail=0
[exit 0]
```

Seven mutations — each transcript entry shows the mutation delta, the rule
lines and the graded line; literal graded lines:

```
mutation empty-chain expected=R-CUSTODIAN observed=R-CUSTODIAN count=actions=0 other-rule=pass:yes verdict=pass
mutation wrong-scope expected=R-CUSTODIAN observed=R-CUSTODIAN count=scope-bad=1 other-rule=pass:yes verdict=pass
mutation head-mismatch expected=R-CUSTODIAN observed=R-CUSTODIAN count=head=bad other-rule=pass:yes verdict=pass
mutation manifest-digest-mismatch expected=R-STATUS observed=R-STATUS count=manifest-bind=bad other-rule=pass:yes verdict=pass
mutation reviewer-producer expected=R-STATUS observed=R-STATUS count=reviewer-collide=1 other-rule=pass:yes verdict=pass
mutation claimable-true-failing-gate expected=R-STATUS observed=R-STATUS count=gates-fail=1 other-rule=pass:yes verdict=pass
mutation claimable-false-no-blocker expected=R-STATUS observed=R-STATUS count=blocker=no other-rule=pass:yes verdict=pass
```

Failing rule lines for the two rule families, verbatim (one per mutation):

```
RULE R-CUSTODIAN verdict=fail detail=actions=0 grant-bad=0 scope-bad=0 fields-bad=0 head=bad expected-head=ok
RULE R-CUSTODIAN verdict=fail detail=actions=2 grant-bad=0 scope-bad=1 fields-bad=0 head=ok expected-head=ok
RULE R-CUSTODIAN verdict=fail detail=actions=2 grant-bad=0 scope-bad=0 fields-bad=0 head=bad expected-head=bad
RULE R-STATUS verdict=fail detail=manifest-bind=bad gates=4 gates-fail=0 subchecks=2 subchecks-fail=0 finding_count=1 reviewer-fields=ok reviewer-collide=0 claimable=true blocker=n/a
RULE R-STATUS verdict=fail detail=manifest-bind=ok gates=4 gates-fail=0 subchecks=2 subchecks-fail=0 finding_count=1 reviewer-fields=ok reviewer-collide=1 claimable=true blocker=n/a
RULE R-STATUS verdict=fail detail=manifest-bind=ok gates=4 gates-fail=1 subchecks=2 subchecks-fail=0 finding_count=1 reviewer-fields=ok reviewer-collide=0 claimable=true blocker=n/a
RULE R-STATUS verdict=fail detail=manifest-bind=ok gates=4 gates-fail=1 subchecks=2 subchecks-fail=0 finding_count=1 reviewer-fields=ok reviewer-collide=0 claimable=false blocker=no
```

Extra probes (not part of the seven), literal graded lines:

```
probe expected-head-drift isolates the manifest leg ok=yes
probe symlinked status.json refused (error=symlink) ok=yes
probe string fallback rejected (reviewer-fields=bad) ok=yes
probe claimable=true finding_count=0 rejected ok=yes
probe claimable=false with named blocker accepted ok=yes
probe list-of-objects gates accepted ok=yes
probe decisions-key chain accepted ok=yes
mutations=7 caught=7 baseline=pass truncated-fail-closed=pass probes=7/7
```

`expected-head-drift` isolates the manifest leg: `head=ok expected-head=bad`
(after the manifest edit the status digest was recomputed, so R-STATUS passes
and only R-CUSTODIAN fails). Truncated `status.json` produced
`RULE R-STATUS verdict=fail detail=error=Unterminated string starting at`,
exit 1 — corrupt JSON fails closed, never passes.

Delivered bytes (not the scratch copy) run directly from the wave dir:

```
$ python3 .ufo/waves/round-43/w1/ExecGateChain.rules.py /nonexistent-package || echo "first_exit=$?"
RULE R-CUSTODIAN verdict=fail detail=error=no-package-dir
RULE R-STATUS verdict=fail detail=error=no-package-dir
package=/nonexistent-package rules=2 pass=0 fail=2
first_exit=1
$ python3 .ufo/waves/round-43/w1/ExecGateChain.rules.py 2>&1 || echo "second_exit=$?"
usage: ExecGateChain.rules.py <package-dir>
second_exit=2
```

## Integration requirements for the sibling seats

- `ExecGateCore` prints the module's `(rule_id, verdict, detail)` as
  `RULE <id> verdict=pass|fail detail=<detail>`; no other return shape is
  used.
- `ExecExemplarPackage` must satisfy: `manifest.expected_head_sha256` ==
  `custodian-receipts.head_sha256` == final `decision_sha256`;
  `status.manifest_sha256` over the exact `evidence/manifest.json` bytes;
  boolean `claimable`; if true, every `hard_gates`/`subchecks` entry PASS,
  at least one entry in each, `finding_count` int >= 1; if false, a named
  blocker as above; reviewer with `identity`, `requested_model`,
  `resolved_model`, boolean `fallback`, identity not equal to any manifest
  redaction producer/verifier. The transcript's scratch package is a worked
  instance of this shape (four hard gates, two subchecks, reviewer
  `reviewer-c` against producer `producer-a` / verifier `verifier-b`).
- `ExecGateFixtures`' defect classes (6) custodian head mismatch and (7)
  reviewer equals producer are the same two classes graded here as
  `head-mismatch` and `reviewer-producer`; on those deltas R-CUSTODIAN prints
  `head=bad` / `expected-head=bad` and R-STATUS prints `reviewer-collide=1`.

## Scope boundaries

This module does not implement: artifact digests/polarity/path confinement
(R-MANIFEST, R-REDACT), redaction receipt pairing (R-REDACT), provenance
fields (R-PROVENANCE), report markers/citations (R-REPORT), secret scanning
(R-NOSECRET) or file presence (R-FILES). It reads the manifest only for
`expected_head_sha256`, redaction identities and its raw bytes. `reviewer.role`
is not required by these rules (the contract text does not make it part of
R-STATUS); the scratch fixture carries `role: kx-reviewer` and the rule
ignores it — a core that wants the role gate must enforce it in R-STATUS or
elsewhere.

## Risks / open

- `claimable` as the string `"true"` fails closed (`claimable=absent`). Any
  donor package that stores it as a string is rejected by design.
- A `hard_gates` list of bare gate names (no verdicts) fails: a name is not a
  verdict. Names must be paired with `PASS` values (mapping or objects).
- No hex64 format constraint on `decision_sha256`/`head_sha256`; the frozen
  item spec requires the three-way equality, and equality is what is checked.
  A format gate, if wanted, belongs to R-CUSTODIAN's owner decision, not to
  this module silently.
- Scratch paths inside the transcript no longer exist by design (scratch
  removed). The transcript prints the full fixture JSON and each mutation
  delta, so the run is reconstructible with the delivered module; the driver
  itself was scratch-only and is not a deliverable.

## Tooling

None installed or upgraded.

## Scratch

Removed before yield:

```
$ rm -rf -- /fast/scratch/hyaku/kasegi-r43/ExecGateChain
$ test ! -e /fast/scratch/hyaku/kasegi-r43/ExecGateChain && echo "scratch absent: /fast/scratch/hyaku/kasegi-r43/ExecGateChain"
scratch absent: /fast/scratch/hyaku/kasegi-r43/ExecGateChain
```

Lane status after the work (`git status --short -- .`): only the untracked
`.ufo/waves/round-43/` wave files; no tracked lane file changed, no mutating
git command was run.
