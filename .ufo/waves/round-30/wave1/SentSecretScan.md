# Round 30 wave 1 — trust-boundary scan

**Axes:** depth:verifiability; coverage. **Severity:** medium for verification/provenance; no credential exposure observed. Scope: changed/new production paths, round-30 lesson/ledger/instruments/manifests, and seat Markdown reports under `.ufo/waves/round-30/wave1/`. No remediation scope; read-only scan.

## Production scan

Patterns checked: common credential/token/private-key forms, assignment-style secret values, literal `op://`, URLs containing session/private/token/auth path terms, and live-target-action language. Per-file results:

| File | Result | Evidence |
|---|---|---|
| `SKILL.md` | PASS | no pattern hits |
| `corpus/README.md` | PASS | no pattern hits |
| `corpus/SOURCES.md` | PASS | no pattern hits |
| `corpus/QUALITY.md` | PASS | no pattern hits |
| `corpus/instruments/frontier-recheck-count.py` | PASS | no pattern hits |
| `corpus/instruments/source-recheck.py` | PASS | no pattern hits |
| `corpus/instruments/knowledge-expected.txt` | PASS | no pattern hits |
| `corpus/source-snapshots/round-30/manifest.json` | PASS | no pattern hits |
| `corpus/source-snapshots/round-30/S041.txt` | PASS | no pattern hits |
| `corpus/source-snapshots/round-30/S046.txt` | PASS | no pattern hits |
| `corpus/source-snapshots/round-30/S047.txt` | PASS | no pattern hits |
| `corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md` | PASS (Q6) | line 38 is a documentation-only *negative* statement, expressly saying it instructs no probing/scanning/login/submission; no credential/private material |
| `corpus/knowledge/considerthese-proposals-ledger.md` | PASS (Q6) | line 20 is the same explicit negative documentation-only statement; no credential/private material |
| `corpus/lessons/round-30.md` | NOT PRESENT | `read` returned not found; no lesson bytes scanned, no claim of pass |

The action-language regex also flagged both new knowledge-entry disclaimer lines because they name prohibited acts while explicitly disclaiming instructions. Manual context inspection confirmed no actionable target instructions. Q6 judgment here is based on that context, not raw regex status.

## Seat reports: banned `pacman` claims

Searched `.ufo/waves/round-30/wave1/*.md`; positives are documentation/claims, not command execution evidence. No assertion below is a claim that an actual invocation occurred:

- `ExecBeforeVerify.md:62` says no install/action occurred.
- `ExecImplFrontierHarness.md:10-11,205` says no transaction attempted.
- `RevEngIntent.md:11` says no attempt.
- `ScribeCloseOut.md:125` says no transaction.
- `ScribeSkillGate.md:4` says no package action.
- `SentScope.md:5,9` records no action and expressly says it could not certify complete process history.

These are unverified negative self-reports; this scan is not process auditing. Remaining reports had no `pacman` hit. In particular, presence of the word in a denial is not evidence of usage. Historical lesson mentions and Q6 fixture/corpus-copy matches are outside the new seat-report set and are not treated as round-30 actions.

## Limits / finding

No credential, vault URI, or session/private URL pattern was found in the scanned production files or top-level seat reports. The narrow pattern scan is not a secret detector with exhaustive coverage. **Severity: low/informational** for exposed-secret risk; **medium evidence limitation** for claims that no package-manager command ran, because self-reports and text search cannot establish process history. Exploit path: none evidenced. Smallest remediation: retain the report-level denials as claims only and use operator process/audit evidence if a positive assurance about command execution is required. No tool was installed or updated.
