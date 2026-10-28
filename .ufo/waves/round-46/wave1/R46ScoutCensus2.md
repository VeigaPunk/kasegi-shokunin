VERDICT: DRAFT-READY

# R46ScoutCensus2 — C1 re-groundability census (claim-package-contract, ev-model, evidence-dir)

Lane: kasegi round 46, C1 = depth:verifiability. Read-only census. The only file written is this Report. Scratch under /fast/scratch/hyaku/kasegi-r46/R46ScoutCensus2/ (removed on exit).

## Bar applied
The frozen counter `corpus/instruments/r46-c1-gate.py` (per-entry mode) passes an entry only when: one `## Re-ground (round 46)` section; >= 6 rows with unique ids; each anchor is a regular file under `corpus/instruments/` or `corpus/source-snapshots/` (never SKILL.md, never a knowledge entry); range <= 40 lines; token >= 6 chars found in those lines; >= 2 distinct anchor files.
Lane-support (SKILL.md, knowledge entries) is recorded below but NOT counted toward the class, because the gate rejects it (control D).

## Frozen bytes
- freeze 9f23aab, base 914ca0b.
- `sha256sum` (first 16 hex) identical at live / freeze blob / base for: `corpus/instruments/claim-package-check.py` = 8b6f849349157a91; `corpus/knowledge/claim-package-contract.md` = 2233cd0637a69c11; `corpus/knowledge/ev-model.md` = 000fe7fbb93dada0; `corpus/knowledge/evidence-dir.md` = 2d924d029be7dceb; `corpus/instruments/fixtures/claim-package/defect-2-digest/status.json` = 60f06dfebc04e419; `SKILL.md` = a7c4d818300df64e.
- `corpus/instruments/r46-c1-gate.py`: live = freeze blob = b0c730c834b4d7c6. Absent at base: `git -C <lane> cat-file -e 914ca0b:corpus/instruments/r46-c1-gate.py` -> "fatal: path 'corpus/instruments/r46-c1-gate.py' exists on disk, but not in '914ca0b'". The counter lands at freeze, not at base.

## Classification
| entry | gate-anchored claims | anchor files | class |
|---|---|---|---|
| claim-package-contract.md | 21 (20 gate-encoding + 1 exemplar) | 2 | **full** |
| evidence-dir.md | 3 supported (+1 contradicting) | 1 | **partial** (fails >= 2-file bar even at 6 rows) |
| ev-model.md | 0 | 0 | **none** (lane support only in SKILL.md) |

## Findings: claim-package-contract.md (full; draft passes the frozen gate)
Built as a scratch-only draft: 21 rows appended to a scratch copy, recheck line rewritten home-free (`recheck: python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md`). Run with the freeze copy of the counter:

    $ python3 -I .../r46-c1-gate.py --entry corpus/knowledge/claim-package-contract.md --root .../draft
    row G21 ok=1 read=token-located
    reground entry=claim-package-contract.md rows=21 ok=21 files=2 exit=0
    exit=0

Caveat: the anchors show what the committed gate ENCODES (claim-package-check.py R-* rules), not what the lost source `fleets/mission-template.md` says. Rows are worded as "gate encodes X" accordingly.

TSV (entry, claim, anchor, token, verified):
entry	claim	anchor	token	verified
claim-package-contract.md	report.md literal marker "No submission performed" (gate constant)	corpus/instruments/claim-package-check.py:121	NO_SUBMISSION = 'No submission performed'	nl ok; G1 ok=1
claim-package-contract.md	report.md "Scope excerpt" heading (gate regex)	corpus/instruments/claim-package-check.py:120	re.compile(r'scope\s+excerpt'	sed ok; G2 ok=1
claim-package-contract.md	report.md carries an https program URL (R-REPORT)	corpus/instruments/claim-package-check.py:74-76	an https URL	sed ok; G3 ok=1
claim-package-contract.md	claim_checklist.md carries OPERATOR-GATED (exemplar only; no gate enforces it)	corpus/instruments/fixtures/claim-package/defect-2-digest/claim_checklist.md:3-4	OPERATOR-GATED: every step below	sed ok; G4 ok=1
claim-package-contract.md	manifest schema_version is evidence-manifest/v1	corpus/instruments/claim-package-check.py:305	manifest.get('schema_version') != 'evidence-manifest/v1'	sed ok; G5 ok=1
claim-package-contract.md	artifact polarity in {positive,negative}; >=1 positive (R-MANIFEST)	corpus/instruments/claim-package-check.py:55-56	polarity in {positive,negative}	sed ok; G6 ok=1
claim-package-contract.md	redactions[] empty is refused (R-REDACT)	corpus/instruments/claim-package-check.py:365-367	raise _GateFail('redactions=empty')	sed ok; G7 ok=1
claim-package-contract.md	artifact paths: symlink refused	corpus/instruments/claim-package-check.py:182	return None, 'symlink'	sed ok; G8 ok=1
claim-package-contract.md	custodian scope_signal must be NO_SCOPE_OBJECTION	corpus/instruments/claim-package-check.py:460	decision.get('scope_signal') != 'NO_SCOPE_OBJECTION'	sed ok; G9 ok=1
claim-package-contract.md	custodian head_sha256 read for final-digest binding	corpus/instruments/claim-package-check.py:464	head = document.get('head_sha256')	sed ok; G10 ok=1 (comparison 466-469 printed)
claim-package-contract.md	provenance external_effects_performed read, must be empty	corpus/instruments/claim-package-check.py:527	document.get('external_effects_performed')	sed ok; G11 ok=1
claim-package-contract.md	agents carry requested and resolved models per transition	corpus/instruments/claim-package-check.py:497	'requested_model', 'resolved_model'	sed ok; G12 ok=1
claim-package-contract.md	pin carries a remote	corpus/instruments/claim-package-check.py:518	remote = pin.get('remote')	sed ok; G13 ok=1
claim-package-contract.md	status manifest_sha256 binds manifest bytes (R-STATUS)	corpus/instruments/claim-package-check.py:584	recorded = status.get('manifest_sha256')	sed ok; G14 ok=1
claim-package-contract.md	claim_review hard gates include no_duplicate_or_prior_submission	corpus/instruments/claim-package-check.py:123-128	'no_duplicate_or_prior_submission',	sed ok; G15 ok=1
claim-package-contract.md	claim_review subchecks no_secrets and operator_attribution	corpus/instruments/claim-package-check.py:129	SUBCHECK_KEYS = ('no_secrets', 'operator_attribution')	sed ok; G16 ok=1
claim-package-contract.md	reviewer identity must differ from producer and verifier	corpus/instruments/claim-package-check.py:607-608	raise _GateFail('reviewer=not-distinct')	sed ok; G17 ok=1
claim-package-contract.md	reviewer fallback flag must be boolean	corpus/instruments/claim-package-check.py:605-606	raise _GateFail('reviewer:fallback')	sed ok; G18 ok=1
claim-package-contract.md	claimable true needs finding_count >= 1	corpus/instruments/claim-package-check.py:617-619	raise _GateFail('claimable=true,finding_count=bad')	sed ok; G19 ok=1
claim-package-contract.md	claimable false must name a blocker	corpus/instruments/claim-package-check.py:563-573	def _named_blocker(status):	sed ok; G20 ok=1
claim-package-contract.md	secrets attestation must be affirmative	corpus/instruments/claim-package-check.py:536	raise _GateFail('secrets_attestation=not-affirmative')	sed ok; G21 ok=1

Current claims NOT counted (no committed anchor, or anchor contradicts):
- "state" enum DONE|BLOCKED|SUBMITTED|PARKED (entry lines 29-34): no gate reads it; fixture holds only `"state": "BLOCKED"` (status.json:4). Not supported.
- `claimability_blocker` + `resume_condition` (entry lines 47-51): gate reads `claimability_blocker` (claim-package-check.py:570), `resume_condition` appears in no committed bytes (grep: no match). Partial, not counted.
- "Scope excerpt" definition tail (`observed_at` + content sha256, entry line 11): gate checks only the heading and https URL. Not counted.
- "repro steps without secrets" (line 11): gate R-NOSECRET scans the WHOLE package (claim-package-check.py:77-79), broader than the contract's wording. Not counted as stated.
- impact / affected asset / suggested fix / disclosure timeline (line 11): no gate. Not supported.
- Validation `node ops/claim-check.mjs` fail-closed (lines 56-62): the lane itself records that tool as documentation-only (claim-package-check.py:6-7). Contradicted as a current validator.

HISTORICAL-ONLY (lost-tree record, not re-groundable): lines 18-27 round-13 boundary note on the lost checker; lines 29-51 status census (280 packages, 249 verdicts, claimable 12/280, PARKED 248/280); lines 64-68 round-22 provenance.
Note: the boundary note says pin/policy_sha256/external_effects_performed/schema_version are "not machine gates". That is true of the lost checker only; the committed claim-package-check.py now enforces them (rows G5, G11, G13). Do not restate the note as a claim about the lane gate.

## Findings: evidence-dir.md (partial)
TSV:
entry	claim	anchor	token	verified
evidence-dir.md	manifest is strict evidence-manifest/v1 (R-MANIFEST)	corpus/instruments/claim-package-check.py:53	schema_version == "evidence-manifest/v1"	sed ok; control C row G1 ok=1
evidence-dir.md	manifest_sha256 binds status to manifest bytes ("frozen at wrap; manifest-bound")	corpus/instruments/claim-package-check.py:68	manifest_sha256 recomputed over the manifest bytes	sed ok; control C row G2 ok=1
evidence-dir.md	package manifest lives at evidence/manifest.json (one of six files)	corpus/instruments/claim-package-check.py:104	'evidence/manifest.json',	sed ok; control C row G3 ok=1
evidence-dir.md	CONTRADICTED: "Validated by ops/claim-check.mjs (fail-closed)"	corpus/instruments/claim-package-check.py:6-7	was documentation-only for this lane	sed ok: lane says the lost checker was doc-only

Control C (3 rows, evidence-dir scratch copy): `reground entry=evidence-dir.md rows=3 ok=3 files=1 exit=1`. Passing rows alone cannot make it full: all three are in one file. Adding the exemplar fixture (`fixtures/claim-package/exemplar/evidence/manifest.json:2` = `"schema_version": "evidence-manifest/v1",`) would give 2 files but still only 4 rows.

HISTORICAL-ONLY: "Scope" contrast table (lines 9-16); canonical-file counts over 592 dirs (lines 20-42); common subdirs (lines 44-60); honest-zero-record.json fields (lines 62-66, no committed fixture); evidence/<program>/status.json PARKED mirror (lines 73-75; committed fixture status.json says BLOCKED, not PARKED); `ops/fleet-dispatch.mjs` SYNC_PATHS (lines 17-18, lost tool); adjacent dirs (lines 77-85: vgn-bounty-lab, george 49G, pendle).
Not in any gate-anchor dir: "written by missions, dispatchers, custodian, hunts" (line 12).

## Findings: ev-model.md (none under the gate bar)
Lane-support only (SKILL.md, not a gate-anchor dir). Verified by sed -n:
entry	claim	anchor	token	verified
ev-model.md	p_success = p_in_scope x p_reproducible x p_unique x p_accepted (formula)	SKILL.md:828-832	p_success    = p_in_scope	sed 826,832p; not counted
ev-model.md	default p_success 0.0735 from listed defaults	SKILL.md:875-876	expected_risk_cost 250	sed 873,877p; not counted
ev-model.md	verdict strict: positive only when adjusted_ev > 0	SKILL.md:848-849	Verdict is strict	sed 840,852p; not counted
ev-model.md	missing inputs print UNKNOWN, fail-closed	SKILL.md:846	Missing inputs print	sed 840,852p; not counted
ev-model.md	ev-report does not persist adjusted_ev	SKILL.md:809	and persists nothing	sed 806,811p; not counted
ev-model.md	exit 2 for missing program-id; exit 0 on report	SKILL.md:850-852	for a missing program-id argument	sed 840,852p; not counted

Control D (ev-model scratch copy, rows anchored to SKILL.md and to the entry itself): `row G1 ok=0 read=anchor-dir-or-self` ... `reground entry=ev-model.md rows=6 ok=0 files=0 exit=1`. The gate rejects SKILL.md and self anchors as intended.

Zero gate-anchor rows: the EV formula, defaults and verdict rules appear in no file under corpus/instruments/ or corpus/source-snapshots/. Grep over those dirs for `p_in_scope|gross_value|adjusted_ev|expected_risk_cost|positive_adjusted_ev|ev-report|ev_inputs` returned only unrelated CVSS/glossary hits (S064 `"UNKNOWN"`).

HISTORICAL-ONLY: round-15 anchor base (lines 5-11: frozen 2026-09-05 mirror `1cfbd86`, sha256 ba5485ed6a5d; the mirror is not in committed bytes; only the recorded digest survives in source-tree-loss-2026-09-28.md:111); tool behaviour lines 22-29 (lost ops/ev-report.mjs); schema lines 36-43 (lost bounty-map/schema.json); rank defaults lines 44-48 (lost ops/rank.mjs; the same numbers appear as prose in SKILL.md:873-876, not counted); census counts 0/1088 (lines 33-35).

## Recheck lines (do-nothing control)
The three live recheck lines, run as the gate's classify() does (cd stripped, cwd = base export):
    claim-package-contract recheck_exit=1  cmd=[test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/claim-package-contract.md]
    ev-model recheck_exit=1  cmd=[test -d ~/Projects/bounties && test -d ~/Projects/the-bounty-hunter && python3 corpus/instruments/anchorcheck.py corpus/knowledge/ev-model.md]
    evidence-dir recheck_exit=1  cmd=[test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py corpus/knowledge/evidence-dir.md]
All three are gated today (exit 1), so each is a candidate for re-grounding.

## C1 counter run on the draft tree (falsification of the target)
Aggregate, scratch tree with only claim-package-contract re-grounded, baseline = base export:
    gate L1 pass=0 read=gated=23 broken=0 lines=64/base=64
    gate L2 pass=0 read=base-gated=24 regrounded=1 claim-package-contract.md
    gate L3 pass=1 read=recheck-lines-clean=1
    gate L4 pass=1 read=entry-mode-green=1
    gate L5 pass=1 read=append-only=1
    gate L6 pass=1 read=mutants=21 survivors=none
    gate L7 pass=1 read=still-gated=23 changed=none
    c1-gate fixed=5/7 exit=1
Reading: the base has 24 gated (matches the brief). One re-ground gives 23. L1 needs <= 22 and L2 needs |R| >= 2. So claim-package-contract alone does NOT meet C1. A second entry must be FULL; ev-model and evidence-dir do not qualify. The intended partner (claim-gates.md) was not censused here (outside my item).

Negative control A (tampered anchor token, NO_SUBMISSION changed to 'No submission made' in a scratch copy): `rows=21 ok=20 files=2 exit=1`, so exactly one row fails and the gate is sensitive to the anchor token.
Negative control B (do-nothing; base entry without section): `reground entry=claim-package-contract.md rows=0 ok=0 exit=1 read=section-count=0`.

## Adjacent lane observations (not fixed; out of item)
- `corpus/knowledge/triage-thresholds.md:310` cites `SKILL.md:498` for the EV formula, and line 313 cites `SKILL.md:502`. `sed -n '496,502p' SKILL.md` prints park-disposition prose (`RETRY_* is a real requeue ...`), not the formula. The formula is at SKILL.md:828-832.
- `claim-package-check.py:441` accepts a `decisions` key as a fallback for the custodian chain; the contract names only the chain (row G9 is anchored at 460, unaffected).

## Limitations
- Only the three assigned entries were censused. The other 21 gated entries, including claim-gates.md, were not checked, so the C1 target (<= 22) remains unmet by this census.
- "Re-grounded" here means the committed gate encodes the claim; the lost source (`fleets/mission-template.md`, `ops/*.mjs`) cannot be re-read and is not verified.
- Exemplar fixtures were authored by the lane (R43); anchoring to them is lane-internal evidence, and G4 is one such row.
- SKILL.md and knowledge-entry support is reported but not counted, per the gate bar.
- The counter exists only from freeze 9f23aab. All runs used the freeze blob copied into scratch, not the base export.
- The aggregate ran against a scratch tree; no lane file was modified. The per-entry runs used the same freeze counter bytes (sha b0c730c834b4d7c6).
- The "write Report" instruction conflicts with the read-only seat rule; I wrote only this Report file, per the seat spec.
- No tools were installed. No git mutation, no commit, no push. The host recheck lines were only executed for `test -d` (read-only), never against live targets.
