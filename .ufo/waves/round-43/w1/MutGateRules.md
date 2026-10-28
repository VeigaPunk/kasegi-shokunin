# MutGateRules — round 43 seat receipt

Item (leaf, receipt-only): mutate `corpus/instruments/claim-package-check.py` one rule at a
time, seven assigned weakenings, and record for each the fixture that should catch it and
whether it does. No lane file was written except this receipt; no mutating git command was run.

Round 43, lane kasegi-shokunin, base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Frozen claims read first: `.ufo/waves/round-43/claims.json` (not edited).

## Substrate

The instrument is not committed at base; the gate exists this round as the Executor deliverable.
I probed the exact bytes the L1 lands:

```
$ sha256sum .ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py
bdb50a82623d93f10fe2cc0616d1d180c2a14f6e11fe8ff9004c84c35ba9ce8e  .ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py
$ wc -l .ufo/waves/round-43/w1/ExecGateCore.claim-package-check.py
802
```

Two earlier Executor drafts were probed with the same driver before that file appeared and
returned the same verdict per mutation: `bec72198e768e1b42342a4ebbcb385c0da307429060d76c0967d76cd4539aa20`
(800 lines) and `ed281697cfc3bd0ef645a565100e66a75583a4656964b6e51d862fe1f0aa134d` (802 lines).
The run recorded below is the one against `bdb50a82…`, i.e. the landed bytes.

The gate carries no selftest implementation yet — `grep -n 'run_selftest'` over the landed file
returns only the dispatch hook, never a `def`:

```
767:    Preferred: a module-level `run_selftest(gate_path)` pasted into this file
772:    hook = globals().get('run_selftest')
800:# <!-- selftest-body-paste-anchor: paste run_selftest(...) ABOVE this guard -->
```

so the suite-level detector (`--selftest` expected-rule grading) could not be exercised; the
detector used is the gate's own per-rule output, the same surface the selftest grades.

Base package for every fixture: the Executor's passing package
`pkg-pass` (manifest sha256 `e00fc9dce2f6f4e6e8c3f3423cc36332682b8eb41ec6da10f1e4815f1d8eb479`),
8/8 exit 0 at baseline. Every fixture is one defect on top of it.

```
$ python3 <S>/gate.pristine.py <S>/base
RULE R-FILES verdict=pass detail=files=6,missing=0,bad=0
RULE R-MANIFEST verdict=pass detail=artifacts=2,positive=1,digest-bad=0,escape=0
RULE R-REDACT verdict=pass detail=artifacts=2,receipts=2,missing=0,digest-mismatch=0
RULE R-CUSTODIAN verdict=pass detail=chain=2,grant-miss=0,signal-bad=0,head=bound
RULE R-PROVENANCE verdict=pass detail=agents=2,commands=2,pin=ok,effects=none,secrets=ok
RULE R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named
RULE R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=1,unbound=0
RULE R-NOSECRET verdict=pass detail=files-scanned=ok,symlinks=0,oversize=0,hits=0
package=<S>/base rules=8 pass=8 fail=0 verdict=WELL-FORMED
```

`<S>` = `/fast/scratch/hyaku/kasegi-r43/MutGateRules` (removed before yield). The path in the
quoted gate output is abbreviated here; the full paths are in the driver transcript.

## Method

Detector = the gate. For each mutant:

1. **fixture**: a fresh copy of the passing package with exactly one defect that exercises the
   weakened check;
2. **pristine gate on the fixture** must reject it (exit 1) and must name the mutated rule —
   otherwise the fixture is not a real instance of that defect and the case is *inconclusive*,
   not a kill;
3. **mutated gate on the fixture**: rejected → *killed*; accepted → *survived*;
4. **mutated gate on the untouched base package** must still accept (exit 0), so the mutation
   is a weakening and not merely a broken build;
5. **boundary fixture**: an out-of-package artifact path/symlink must stay rejected under the
   path/symlink mutants, so a survivor is read as contract-strictness lost, not an escape hole;
6. **mutant x fixture matrix**: every mutant against every fixture, to show whether any other
   defect fixture can still kill it (i.e. whether the gate has depth behind the mutated check).

Each mutation is one exact-string replacement with a mandatory single occurrence in the
substrate, applied to a throwaway copy under `<S>/mut/<id>.py`; the pristine file is never
edited and its sha256 is re-checked after every case.

Driver: `<S>/drive.py`, sha256 `be1e55b2476352471bfb4dbf7e6397fa542c5538f29363130a22ef12c8e7bcc9`
(scratch-local, removed; the mutation strings and fixture deltas are reproduced below so the
probe can be rebuilt).
Run: `cd <S> && python3 drive.py > transcript.txt 2>&1` → exit 0,
`transcript.txt` 532 lines, sha256 `9515cdfd925d649ee6b6ed1e5600ece4c039235738a43d77d12a64d883b19ca7`.

## Result table

| # | mutation | rule | fixture that should catch it | pristine gate on fixture | mutant gate on fixture | caught? |
|---|----------|------|------------------------------|--------------------------|------------------------|---------|
| M1 | R-MANIFEST trusts the recorded digest instead of recomputing it | R-MANIFEST | F1: `evidence/adv.txt` bytes altered after the digest was recorded | exit 1, `R-MANIFEST verdict=fail detail=artifacts=2,digest-bad=1` | exit 0, `verdict=WELL-FORMED`, `R-MANIFEST verdict=pass` | **no — survived** |
| M2 | R-MANIFEST accepts a `..` path that resolves back inside the package | R-MANIFEST | F2: artifact path `../evidence/adv.txt`, correct digest | exit 1, `R-MANIFEST verdict=fail detail=artifacts=2,escape=1` | exit 0, `verdict=WELL-FORMED`, `R-MANIFEST verdict=pass` | **no — survived** |
| M3 | R-MANIFEST accepts a symlink whose target stays inside the package | R-MANIFEST | F3: `evidence/link.txt -> adv.txt`, registered as an artifact | exit 1, `R-MANIFEST verdict=fail detail=artifacts=3,escape=1` (also `R-NOSECRET verdict=fail detail=symlinks=1`) | exit 1, `verdict=DEFECT`, `R-MANIFEST verdict=pass`, `R-NOSECRET verdict=fail detail=symlinks=1` | **yes — killed, by R-NOSECRET only** (named rule blind) |
| M4 | R-REDACT accepts `redactions: []` | R-REDACT | F4: manifest `redactions: []` with two artifacts | exit 1, `R-REDACT verdict=fail detail=redactions=empty` | exit 0, `verdict=WELL-FORMED`, `R-REDACT verdict=pass detail=artifacts=2,receipts=0,missing=0,digest-mismatch=0` | **no — survived** |
| M5 | R-STATUS accepts a reviewer whose identity equals a producer | R-STATUS | F5: `claim_review.reviewer.identity = agent-writer` (a redaction producer) | exit 1, `R-STATUS verdict=fail detail=reviewer=not-distinct` | exit 0, `verdict=WELL-FORMED`, `R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named` | **no — survived** |
| M6 | R-STATUS accepts `claimable:true` with a failing hard gate | R-STATUS | F6: `claimable:true`, `hard_gates.evidence_integrity=FAIL` | exit 1, `R-STATUS verdict=fail detail=claimable=true,gates-not-pass=1` | exit 0, `verdict=WELL-FORMED`, `R-STATUS verdict=pass detail=manifest=bound,reviewer=distinct,gates=6/6,claimable=true` | **no — survived** |
| M7 | R-REPORT accepts a report without the `No submission performed` marker | R-REPORT | F7: `report.md` with scope excerpt, URL and cited digest but no marker | exit 1, `R-REPORT verdict=fail detail=marker=absent` | exit 0, `verdict=WELL-FORMED`, `R-REPORT verdict=pass detail=scope-excerpt=ok,marker=ok,url=ok,cited=1,unbound=0` | **no — survived** |

```
SUMMARY mutants=7 killed=1 survived=6 inconclusive=0
KILLED: M3-symlink-inside-package
SURVIVED: M1-manifest-trusts-recorded-digest,M2-path-dotdot-resolving-inside,M4-redactions-empty-accepted,M5-reviewer-equals-producer,M6-claimable-true-failing-gate,M7-report-without-marker
RESTORATION pristine gate sha256 before=bdb50a82… after=bdb50a82… equal=True
```

Every mutant also left the untouched base package at exit 0 (`mutant gate on untouched base
package: exit=0` in all seven case blocks), so none of the seven is detected because the gate
broke on a well-formed package.

## Mutation sites (exact replacement, one occurrence each)

Applied to `bdb50a82…`; the driver asserts `source.count(old) == 1`.

M1 — `rule_manifest` (line 346):
```
-        if actual != recorded.lower():
+        if False:
             digest_bad.append(rel)
```
(the recompute itself is left in place, its result ignored: the recorded digest is trusted)

M2 — `inspect_path`, `..` branch (line 172), the `..` ban becomes a normalisation:
```
-    if '..' in parts:
-        return None, 'dotdot'
+    if '..' in parts:
+        parts = [part for part in os.path.normpath('/'.join(parts)).split('/')
+                 if part not in ('', '.')]
```
(the `realpath` containment test below is untouched, so this only admits `..` that resolves inside)

M3 — `inspect_path`, symlink branch (line 181), ban narrowed to escapes:
```
-        if stat.S_ISLNK(st.st_mode):
+        if stat.S_ISLNK(st.st_mode) and not os.path.realpath(current).startswith(root + os.sep):
             return None, 'symlink'
```

M4 — `rule_redact` (line 366), empty list short-circuits to a pass:
```
-    if not isinstance(receipts, list) or not receipts:
+    if not isinstance(receipts, list):
         raise Fail('redactions=empty')
+    if not receipts:
+        return 'artifacts=%d,receipts=0,missing=0,digest-mismatch=0' % len(artifacts)
```

M5 — `rule_status` (line 607), distinctness check removed:
```
-    if identity.strip().casefold() in _identities(manifest):
-        raise Fail('reviewer=not-distinct')
+    pass
```

M6 — `rule_status`, claimable branch (line 615), the failing-gate list is emptied:
```
         failing = [key for key in HARD_GATE_KEYS if hard.get(key) != 'PASS']
         failing += [key for key in SUBCHECK_KEYS if subchecks.get(key) != 'PASS']
-        if failing:
-            raise Fail('claimable=true,gates-not-pass=%d' % len(failing))
+        failing = []
```
(`finding_count>=1` still guards the branch, so the mutant accepts the fixture with
`finding_count: 1` — the weaker of the two claimable preconditions)

M7 — `rule_report` (line 636):
```
-    if NO_SUBMISSION not in text:
-        raise Fail('marker=absent')
+    pass
```

## Fixture recipes

All are a copy of `pkg-pass` plus one delta; the manifest's `status.manifest_sha256` is
recomputed after any manifest edit so only the intended rule is in play.

- **F1-stale-digest** — append `b" tampered-after-record\n"` to `evidence/adv.txt`. Manifest
  untouched, so the recorded digest no longer matches the bytes.
- **F2-dotdot-inside** — `artifacts[0].path = "../evidence/adv.txt"` (resolves to
  `evidence/adv.txt` inside the package; digest correct); rebind `status.manifest_sha256`.
- **F3-symlink-inside** — `evidence/link.txt -> adv.txt`; append artifact
  `{path: "link.txt", polarity: "negative", sha256: sha(evidence/adv.txt)}` and a matching
  redaction receipt (`producer: agent-writer-2`, `verifier: agent-reader`, same digest in both
  `artifact_sha256`/`scanned_artifact_sha256`); rebind `status.manifest_sha256`.
- **F4-redactions-empty** — `manifest.redactions = []`; rebind `status.manifest_sha256`.
- **F5-reviewer-producer** — `status.claim_review.reviewer.identity = "agent-writer"`, the
  producer identity of the first redaction receipt.
- **F6-claimable-failing** — `status.claimable = True`, `hard_gates.evidence_integrity =
  "FAIL"`, `finding_count = 1`.
- **F7-report-marker** — delete the `No submission performed` line from `report.md`, keeping the
  scope excerpt, the https URL and the cited digest.

## Boundary confinement (the survivors are strictness losses, not escapes)

| boundary fixture | under mutant | pristine | mutant |
|---|---|---|---|
| B1: artifact path `../../outside.txt` (a file outside the package) | M2 | exit 1 `R-MANIFEST detail=artifacts=3,escape=1` | exit 1 `verdict=DEFECT`, `R-MANIFEST verdict=fail detail=artifacts=3,escape=1` |
| B2: `evidence/out.txt` symlink to a file outside the package | M3 | exit 1 `R-MANIFEST escape=1` + `R-NOSECRET symlinks=1` | exit 1 `verdict=DEFECT`, `R-MANIFEST verdict=fail detail=artifacts=3,escape=1` + `R-NOSECRET symlinks=1` |

Both stay rejected: M2 admits only `..` that resolves inside, M3 admits only symlinks whose
`realpath` stays inside. Neither mutant opens the package to bytes outside its own directory.

## Mutant x fixture matrix

`R(rule)` = rejected with the listed failing rules, `A` = accepted (gate exit 0):

```
mutant                            F1-stale-digest  F2-dotdot-inside F3-symlink-inside F4-redactions-empty F5-reviewer-producer F6-claimable-failing F7-report-marker  B1-escape-dotdot  B2-escape-symlink
M1-manifest-trusts-recorded-digest A                R(R-MANIFEST)    R(R-MANIFEST,R-NOSECRET) R(R-REDACT)   R(R-STATUS)   R(R-STATUS)   R(R-REPORT)    R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
M2-path-dotdot-resolving-inside    R(R-MANIFEST)    A                R(R-MANIFEST,R-NOSECRET) R(R-REDACT)   R(R-STATUS)   R(R-STATUS)   R(R-REPORT)    R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
M3-symlink-inside-package          R(R-MANIFEST)    R(R-MANIFEST)    R(R-NOSECRET)            R(R-REDACT)   R(R-STATUS)   R(R-STATUS)   R(R-REPORT)    R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
M4-redactions-empty-accepted       R(R-MANIFEST)    R(R-MANIFEST)    R(R-MANIFEST,R-NOSECRET) A             R(R-STATUS)   R(R-STATUS)   R(R-REPORT)    R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
M5-reviewer-equals-producer        R(R-MANIFEST)    R(R-MANIFEST)    R(R-MANIFEST,R-NOSECRET) R(R-REDACT)   A             R(R-STATUS)   R(R-REPORT)    R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
M6-claimable-true-failing-gate     R(R-MANIFEST)    R(R-MANIFEST)    R(R-MANIFEST,R-NOSECRET) R(R-REDACT)   R(R-STATUS)   A             R(R-REPORT)    R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
M7-report-without-marker           R(R-MANIFEST)    R(R-MANIFEST)    R(R-MANIFEST,R-NOSECRET) R(R-REDACT)   R(R-STATUS)   R(R-STATUS)   A              R(R-MANIFEST)  R(R-MANIFEST,R-NOSECRET)
```

Reading: each mutant accepts exactly its own fixture and rejects every other defect fixture —
the seven mutations are surgical, they blind one check and nothing else. The one exception is
M3, whose own fixture is still rejected, but only by `R-NOSECRET`, never by the mutated rule.

## Findings

1. **Six of the seven assigned weakenings are invisible at package level.** With the gate
   weakened as described, a package carrying that defect prints
   `rules=8 pass=8 fail=0 verdict=WELL-FORMED` and exits 0 — the gate's own verdict, exit code
   and all eight rule verdicts agree that the package is well-formed. Only the symlink widening
   (M3) is still refused, and by a different rule.

2. **The gate is one-deep behind every rule except symlinks.** The matrix shows no second check
   recomputes an artifact digest, re-tests `..`, requires a nonempty `redactions[]`, compares
   reviewer against producer identity, cross-checks `claimable` against the gate values it
   carries, or re-reads the report marker. `R-NOSECRET` is the sole redundancy, and it covers
   only the symlink case (and only because it walks the tree independently of `inspect_path`).

3. **Consequence for the committed defect suite (C2 kill rule).** Since the gate itself offers
   no depth, each of M1, M2, M4, M5, M6, M7 is killed *only* by a committed defect fixture whose
   expected rule is the mutated rule and by a selftest that fails when that rule comes back
   `pass`. A selftest that grades only `verdict=DEFECT` on some other fixture, or that grades a
   summary line, kills none of them: under every one of the six surviving mutants the other
   defect fixtures still print `DEFECT`. The nine-defect fixture set is load-bearing, single-layer
   coverage — there is no second line of defence to fall back on.

4. **The symlink defect class cannot fail `R-MANIFEST` alone.** Both F3 (symlink inside,
   registered as an artifact) and B2 (symlink to outside) necessarily also fail
   `R-NOSECRET detail=symlinks=1`, because that rule bans symlinks anywhere in the package. If
   the planned selftest asserts "exactly the named rule fails", the symlink case is
   unsatisfiable and must be described as failing `R-MANIFEST` *and* `R-NOSECRET`; grade
   "named rule among the failing rules", not "the only failing rule". The same holds for a
   symlinked required file: `R-FILES` (missing) plus `R-NOSECRET` (symlinks).

5. **Three mutant verdicts carry a detail-token tell that a stricter selftest can grade without
   changing the contract.** Under M4 the gate passes `R-REDACT` while printing
   `receipts=0` against `artifacts=2` (a pass detail that contradicts the contract's one-receipt-
   per-artifact requirement). Under M5 it passes `R-STATUS` while printing `reviewer=distinct`
   for a reviewer identity that equals a producer in the manifest. Under M6 it passes with
   `gates=6/6` while the input status carries `evidence_integrity: FAIL`. M1, M2 and M7 pass with
   details identical to a clean package — no tell.

6. **Boundary check passed.** Neither path mutant lets bytes from outside the package directory
   be read: B1 and B2 stay rejected under M2 and M3 respectively. The six survivors are losses of
   contract strictness, not of containment.

## Not done / limits

- The suite-level detector (`--selftest`, expected-rule grading) does not exist in the landed
  gate yet (the paste anchor is empty), so no mutant was graded through the selftest. When the
  selftest lands, the six surviving mutants are the regression set to run: each must produce a
  failing selftest case, or that defect class is unguarded.
- Probe substrate is the gate deliverable in the wave dir, not a committed lane file; if the
  landed file changes, re-run the driver (mutation sites and fixtures are reproduced above).
- The probe was also run in full (all seven mutations) against two earlier Executor drafts with
  identical verdicts; those earlier transcripts were overwritten by the rebase run recorded here.

## Scratch

`/fast/scratch/hyaku/kasegi-r43/MutGateRules` (gate copies, base package, nine fixture packages,
seven mutant copies, driver, transcript) was removed after this receipt was written. No
mutating git command was run in the lane or anywhere else (only read-only `git log`/`git status`
to confirm the base commit); no PATH directory was touched. No package manager
was invoked (pacman is paused host-wide) and no tool installation was needed.
