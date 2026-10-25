# Round 30 wave 1 — scope and boundary findings

## Scope and method

Axes observed: **depth:verifiability** (C1) and **coverage** (C2). I read the frozen claims and before receipts, lane corpus/quality/lesson materials, read-only merge package and absent-defect register, plus the operator rules. No remediation was assigned. No tools installed; no network/live-target action, git/jj command, or pacman command was run by this seat.

## Findings

**Severity: informational / no confirmed out-of-scope write in this inspection.** The observed round-30, post-freeze files under the fleet root are overwhelmingly beneath `kasegi-shokunin/.ufo/waves/round-30/` and are consistent with scoped seat artifacts. The only visible unrelated post-start changes in the sampled metadata listing were in sibling lanes (for example `kengaku-shokunin/.ufo/waves/round-34/` and `souji-shokunin/.ufo/waves/round-28/`); modification time alone cannot attribute them to this wave or any seat. The broad timestamp scan included git/jj internal metadata, so those metadata changes are not evidence of illicit git/jj commands. No `pacman` execution evidence was found or obtained. I did not establish a complete process-history/audit-log view and cannot certify that no seat ran a prohibited command.

**C1 / adversarial contract note (not a mutation audit).** Frozen C1 requires fail-closed A1/A2/B1/B2 probes. The committed before receipt documents the unsafe baseline: A1 traceback on missing entry, A2 duplicate target passes, B1 stem mismatch passes, B2 duplicate quote passes without verified anchor. The later executor report `ExecPostCommitRecheck.md` records a dry run with the intended corrected errors, but at its measurement the F14 entry and manifest were missing and C2 remained red (entry citation count 0, census exit 1, harness exit 1, source rechecks unavailable). This is evidence for those recorded bytes only, not a final integrated result.

This sentinel task did not execute `resume_continuity_v1` or reject a request through that path; therefore it has no observed rejection from which to assert zero mutation. Canonical before/after comparison for every rejection remains unverified here. Smallest remediation: require the canonical resume gate's rejection receipts to include a pre/post mutation inventory/hash for each mutable target, and fail the audit if any reject has a changed target.

**Scope sweep limits.** A recursive mtime scan across the broad fleet tree produced a very large output and cannot reliably identify causal authorship; it included metadata and unrelated concurrent waves. Findings above are limited to visible paths/receipts and are not a fleet-wide attestation. No later ~10-minute rescan was performed in this seat; no recurring watcher was started.

## Evidence pointers

- Frozen predicates and kill rules: `.ufo/waves/round-30/claims.json`.
- C1 baseline bytes/results: `.ufo/waves/round-30/c1-controls/before.txt`.
- C2 baseline: `.ufo/waves/round-30/c2-controls/before.txt`, `census-before.txt`.
- Recorded recheck dry run and blocker: `.ufo/waves/round-30/wave1/ExecPostCommitRecheck.md`.
- Source/admission constraints: `corpus/QUALITY.md` Q6; merge package and defect register read-only.

No confirmed exploit path or unauthorized mutation is evidenced by this inspection. F14's documented Japanese severity material is corpus documentation, not a live-target action.