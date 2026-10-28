VERDICT: DRAFT-READY

# R46ScoutCensus1 — C1 re-groundability census (read-only; lane untouched)

Scope: C1 (depth:verifiability). Three gated entries: `citation-bases`, `claim-anatomy-sample`, `claim-gates` (corpus/knowledge/). Base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba, read from the pure export copied into my scratch. Anchor files are the committed lane bytes under corpus/instruments/ (all `sed -n` / `_grep` runs on the pure export). No lane file was written; no git mutation; scratch removed on exit. Drafts were tested only in scratch copies; none is landed.

Host state (read-only test, run from the scratch copy):
```
ABSENT ~/Projects/bounties
ABSENT ~/Projects/the-bounty-hunter
ABSENT ~/Projects/origin-work/open-bug-bounties
```

## F1. Frozen base reading is confirmed
Command: gated-set classification of the 64 recheck lines on a copy of the base (r46-c1-gate.py `classify`, scratch copy).
Output (quoted):
```
base recheck lines=64 gated=24 broken=0 executes=40
gated with test -d ~/Projects: 23
gated without test -d: ['citation-bases.md']
```
Aggregate counter on base vs base:
```
gate L1 pass=0 read=gated=24 broken=0 lines=64/base=64
gate L2 pass=0 read=base-gated=24 regrounded=0
...
c1-gate fixed=1/7 exit=1
```
Matches claims.json `expect_before`. Note: `citation-bases` is one of the 24 gated, but it is gated by an anchor, not by `test -d`. Its recheck (no `test -d` guard) ran:
```
BASE-ABSENT md:31 ~/Projects/the-bounty-hunter/ops/rank.mjs:55-58 (base tree absent: ...)
LOST-RECORDED md:52 [lost-tree] ops/claim-check.mjs:174-199 (not checked)
== corpus/knowledge/citation-bases.md: 10 in-range cite instances, 0 bad; 8 distinct anchors; LOST-RECORDED=1 PIN-BROKEN=0 ORIGIN=0 OUTSIDE-BASE=0 BASE-ABSENT=1
```
Defect (lane, reported not fixed): entry line 31 says the cite is "now `[lost-base]` and BASE-ABSENT", but the backticked token is unprefixed, so anchorcheck exits 1. Prefixing it `[lost-base] ` inside the backticks would make it LOST-RECORDED.

## F2. Census — one TSV block per entry

Columns: entry, claim, anchor (path:N-M, corpus/instruments/ unless noted), token (verbatim, normalised as the counter normalises), verified (the command run and its outcome). NONE = no committed anchor. Classification after each block.

### TSV — citation-bases

entry	claim	anchor	token	verified
citation-bases	Relative cites try the lane repo first; INTERNAL when the path exists there	corpus/instruments/resolve.py:279-281	m, p = exists_any(os.path.join(lane_root, base))	sed -n '279,281p' -> match
citation-bases	INTERNAL precedence for lane-relative tokens is pinned by a test	corpus/instruments/test_resolve.py:233	self.assert_row(rows, tok_int, "INTERNAL", lane_file, "rel")	sed -n '233p' -> match
citation-bases	Mirror credit for a relative token is MIRROR-EQUIVALENT only when realpath-confined	corpus/instruments/resolve.py:284-285	return "MIRROR-EQUIVALENT", p, m, "rel"	sed -n '284,285p' -> match
citation-bases	A relative token absent from both roots is GONE	corpus/instruments/test_resolve.py:235	self.assert_row(rows, tok_gone, "GONE", domain="rel")	sed -n '235p' -> match
citation-bases	Other-root cite RESOLVES iff it exists, else GONE	corpus/instruments/resolve.py:277	return ("RESOLVES", p, m, "other") if m else ("GONE", "", "", "other")	sed -n '277p' -> match
citation-bases	MIRROR-EQUIVALENT is name survival, not content identity	corpus/instruments/README.md:35-38	counts name survival, not content survival.	sed -n '35,38p' -> match
citation-bases	MIRROR-EQUIVALENT does not establish byte-equivalence	corpus/instruments/resolve.py:538-540	does NOT establish byte-equivalence	sed -n '538,540p' -> match
citation-bases	Lost-marked tokens are never credited and stay GONE	corpus/instruments/test_resolve.py:237-247	def test_lostbase_markers_stay_gone_never_credited(self):	sed -n '237,247p' -> match
citation-bases	Lost-marked cites are LOST-RECORDED, never a fail class	corpus/instruments/anchorcheck.py:24-27	NEVER a fail class	sed -n '24,27p' -> match
citation-bases	Lost-marked prefix is matched by one regex	corpus/instruments/anchorcheck.py:160	LOST = re.compile(r"^\[lost-(?:tree|base)\]\s+(.*)$")	sed -n '160p' -> match
citation-bases	Blob pin form registers a pin verified by git show	corpus/instruments/anchorcheck.py:37-39	<!-- pin: <relpath.md|.mjs|.json|.sh> <7-40 hex> -->	sed -n '37,39p' -> match
citation-bases	Unprefixed mirror names classify BASE-ABSENT until marked lost-tree	corpus/instruments/anchorcheck.py:58-61	therefore classify BASE-ABSENT (mirror gone since 2026-10-14) until marked	sed -n '58,61p' -> match; DATE CONFLICT: entry says 2026-10-12
citation-bases	Bounty-root cite credited MIRROR-EQUIVALENT only where the mirror holds the suffix	corpus/instruments/test_resolve.py:249-253	self.assert_row(rows, tok, "MIRROR-EQUIVALENT", mirror_stats, "bounty")	sed -n '249,253p' -> match
citation-bases	Relative GONE carries sub-kind rel-unresolved	corpus/instruments/resolve.py:78 (prose only)	sub-kind `rel-unresolved`	_grep rel-unresolved -> only line 78; NO CODE emits it
citation-bases	Comma-anchor lists classify GONE (rule 5)	NONE	NONE	no committed match; entry cites resolve.py:74, which is glob text (drift); inference only
citation-bases	ufo-fsd-alpha is not lost and is re-anchored	NONE	NONE	no committed anchor
citation-bases	Line numbers on lane-edited files are unstable; use blob pin or re-verify	corpus/instruments/anchorcheck.py:36-39	(c) blob pin	sed -n '36,39p' -> pin form only; instability rule is prose
citation-bases	Blob refs must not appear bare in backticks (measured GONE)	NONE	NONE	grep -c -i blob resolve.py -> 0; inference only

Classification citation-bases: **full** (13 anchored claims, rows 1-13, over 4 files: resolve.py, test_resolve.py, README.md, anchorcheck.py; bar is >=6 over >=2). The anchored claims are the live resolver rules. Historical only: the MIRROR HEAD 1cfbd86 identity, the ORIGIN-WORK "RESOLVES while the root stood" history, the lost-tree ops/claim-check.mjs cite, and the ufo-fsd-alpha relocation (NONE). Four of the entry's own line anchors are wrong (see F3).

### TSV — claim-anatomy-sample

entry	claim	anchor	token	verified
claim-anatomy-sample	D7 six-file anatomy (report.md, claim_checklist.md, evidence/manifest.json, custodian-receipts.json, provenance.json, status.json)	corpus/instruments/claim-package-check.py:101-108	SIX_FILES = (	sed -n '101,108p' -> match
claim-anatomy-sample	D2/D3 claim_review required, with hard_gates, subchecks and reviewer	corpus/instruments/claim-package-check.py:590-593	review = _require_dict(status, 'claim_review', 'status')	sed -n '590,593p' -> match
claim-anatomy-sample	D5 manifest_sha256 absent or null fails; binds status to manifest bytes	corpus/instruments/claim-package-check.py:584-589	recorded = status.get('manifest_sha256')	sed -n '584,589p' -> match
claim-anatomy-sample	D1 claimable is a required boolean	corpus/instruments/claim-package-check.py:609-611	claimable = status.get('claimable')	sed -n '609,611p' -> match
claim-anatomy-sample	D13 reviewer identity distinct from producer identity (part of the required-key test)	corpus/instruments/claim-package-check.py:607-608	if identity.strip().casefold() in _identities(manifest):	sed -n '607,608p' -> match
claim-anatomy-sample	D4 submit guards do_not_submit and no_submission_performed are required	corpus/instruments/fixtures/claim-package/exemplar/status.json:18-19	"do_not_submit": true,	sed -n '18,19p' -> exemplar shape only; committed gate checks neither (_grep do_not_submit in claim-package-check.py: no match)
claim-anatomy-sample	D10 verdict is free-form, not an enum	corpus/instruments/claim-package-check.py:570	for key in ('verdict', 'claimability_blocker', 'blocked_reason'):	sed -n '570p' -> verdict used only as a string; inference
claim-anatomy-sample	D11 state enum omitted PARKED (repaired in claim-package-contract.md:31)	NONE (knowledge only)	- `state`: `DONE` | `BLOCKED` | `SUBMITTED` | `PARKED`	sed -n '31p' corpus/knowledge/claim-package-contract.md -> knowledge file, not a gate anchor; checker does not check state
claim-anatomy-sample	D12 DONE is not filed	NONE	NONE	no committed anchor (no DONE/submitted_url check in claim-package-check.py)
claim-anatomy-sample	D6 deliverable escapes the package root	NONE	NONE	_grep deliverable over gate, selftest, exemplar -> no match
claim-anatomy-sample	D8 updated_at absent	NONE	NONE	_grep updated_at -> no match
claim-anatomy-sample	D9 non-canonical and extra keys	NONE	NONE	no key allowlist in claim-package-check.py
claim-anatomy-sample	Sample tallies: 280 universe, 20 sample, 241/280 claimable absent, 260/280 deviate, 12/280 claimable true, histograms	NONE	NONE	tree lost (provenance line 151 is [lost-tree]); _grep \b280\b in gate, selftest, fixtures -> no match
claim-anatomy-sample	SKILL.md echoes the sample counts (round-14)	SKILL.md:554 (knowledge, not a gate anchor)	claim-anatomy-sample.md	circular; not gate-admissible

Classification claim-anatomy-sample: **partial**. Five anchored definitional claims (D1, D2/D3, D5, D7, D13), all in ONE file (claim-package-check.py). The bar needs >=6 claims over >=2 files. The tallies and D4/D6/D8-D12 have no committed anchor and are historical. A draft of this entry passes the mechanical counter only with two fixture-shape rows (exemplar status.json:6 and :18), which describe the synthetic exemplar, not the sample. Not a re-ground of the entry's claims.

### TSV — claim-gates

entry	claim	anchor	token	verified
claim-gates	Required six files: report.md, claim_checklist.md, custodian-receipts.json, provenance.json, status.json, evidence/manifest.json	corpus/instruments/claim-package-check.py:101-108	SIX_FILES = (	sed -n '101,108p' -> match (entry's L22-24 line numbers are lost-source, drift)
claim-gates	report.md must match scope excerpt (case-insensitive)	corpus/instruments/claim-package-check.py:120	SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)	sed -n '120p' -> match
claim-gates	report.md must match no submission (performed|made)	corpus/instruments/claim-package-check.py:121,636	NO_SUBMISSION = 'No submission performed'	sed -n '121p;636p' -> PARTIAL: no "made"; case-sensitive `in`
claim-gates	claim_checklist.md must match OPERATOR-GATED	NONE	NONE	_grep OPERATOR-GATED over checker -> no match; phrase is only fixture text (fixtures/claim-package/exemplar/claim_checklist.md:3), not checked
claim-gates	sequence is numeric; expected_head_sha256 key present	corpus/instruments/claim-package-check.py:309-310	head = manifest.get('expected_head_sha256')	sed -n '309,310p' -> match
claim-gates	Artifact polarity in {positive,negative}; at least one positive	corpus/instruments/claim-package-check.py:352-355	if positive < 1:	sed -n '352,355p' -> match
claim-gates	Redaction receipt per artifact; redactions[] non-empty	corpus/instruments/claim-package-check.py:365-367	receipts = manifest.get('redactions')	sed -n '365,367p' -> match (exactly-one-receipt and distinct-identity checks are in the doc at 362 and 549-551)
claim-gates	custodian decisions: scope_signal exactly NO_SCOPE_OBJECTION	corpus/instruments/claim-package-check.py:460	if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':	sed -n '460p' -> match
claim-gates	three-way head binding: head_sha256 = final decision digest = manifest expected head	corpus/instruments/claim-package-check.py:471	if head.lower() != head_expected.lower():	sed -n '471,472p' -> match
claim-gates	manifest_sha256 = sha256 of current evidence/manifest.json bytes	corpus/instruments/claim-package-check.py:588	if recorded.lower() != actual:	sed -n '585,589p' -> match
claim-gates	secrets scan regex (api_key|secret|token|password|bearer), 16+ chars	corpus/instruments/claim-package-check.py:138-140	(?:api[_-]?key|secret|token|password)	sed -n '138,140p' -> PARTIAL: word-bounded; adds op-ref, authorization, session-cookie; not the entry's single regex
claim-gates	files over 5 MiB error; scan cap 5*1024*1024	corpus/instruments/claim-package-check.py:131	MAX_SCAN_BYTES = 5 * 1024 * 1024	sed -n '131p' -> match
claim-gates	blanket symlink ban on package tree	corpus/instruments/claim-package-check.py:659	if os.path.islink(os.path.join(dirpath, name)):	sed -n '659p' -> match
claim-gates	prior-submission guard: submission_performed, submitted_url, submission_state fail	NONE	NONE	_grep over checker -> no match
claim-gates	global duplicate scan of other claims/*/*/status.json	NONE	NONE	checker is single-package; its header (claim-package-check.py:4-8) says "the subset the contract states, and nothing more"
claim-gates	blocker fields: blocked_reason, submission_blocker, blocking_record, submit/BLOCKED.md	corpus/instruments/claim-package-check.py:570	for key in ('verdict', 'claimability_blocker', 'blocked_reason'):	sed -n '570p' -> PARTIAL: submission_blocker, blocking_record, BLOCKED.md absent
claim-gates	state === DONE	NONE	NONE	_grep \bDONE\b over checker -> no match
claim-gates	claimable === true	corpus/instruments/claim-package-check.py:609-612	claimable = status.get('claimable')	sed -n '609-612p' -> PARTIAL: only bool is required; true path checks gates
claim-gates	finding_count positive integer	corpus/instruments/claim-package-check.py:617-619	if isinstance(count, bool) or not isinstance(count, int) or count < 1:	sed -n '617,619p' -> PARTIAL: enforced only when claimable is true
claim-gates	claim_review.outcome === APPROVED	NONE	NONE	_grep outcome|APPROVED -> no match
claim-gates	reviewer role === kx-reviewer exactly	NONE	NONE	_grep kx-reviewer over checker -> no match; reviewer checks are at 600-606 (identity, models, fallback)
claim-gates	reviewer identity distinct from producer and verifier identities	corpus/instruments/claim-package-check.py:607-608 (and corpus/instruments/claim-package-selftest.py:83)	if identity.strip().casefold() in _identities(manifest):	sed -n '607,608p' -> match; selftest 83 -> (("reviewer", "producer"), "R-STATUS")
claim-gates	hard gates all PASS (written_scope, authorization, evidence_integrity, no_duplicate_or_prior_submission)	corpus/instruments/claim-package-check.py:123-128	'no_duplicate_or_prior_submission',	sed -n '123,128p' -> names match; PASS enforced only when claimable is true (line 613) => PARTIAL
claim-gates	subchecks PASS (no_secrets, operator_attribution)	corpus/instruments/claim-package-check.py:129	SUBCHECK_KEYS = ('no_secrets', 'operator_attribution')	sed -n '129p' -> names match; PASS enforced only when claimable is true (line 614) => PARTIAL
claim-gates	not-claimable heuristics error on claimable===false, not_claimable, do_not_submit, claimability_gap, finding_count===0, verdict regex	corpus/instruments/claim-package-check.py:621-623	if not _named_blocker(status):	sed -n '621,623p' -> CONTRADICTED: claimable false passes when a blocker is named; none of do_not_submit / claimability_gap / not_claimable / honest-zero regex in checker
claim-gates	nested readiness: claim_review/claim_wave/claim_attempt/submission outcome or state BLOCKED errors	NONE	NONE	no matching gate in checker
claim-gates	provenance steps/transitions/agents non-empty	corpus/instruments/claim-package-check.py:489-491	if not isinstance(agents, list) or not agents:	sed -n '489-491p' -> PARTIAL: agents only; steps and transitions absent
claim-gates	custodian chain/decisions non-empty; per-decision 64-hex digests	corpus/instruments/claim-package-check.py:440-456	if not isinstance(chain, list) or not chain:	sed -n '440,456p' -> match
claim-gates	prepare-claims: DONE-only, STAGED submit_state, route and attachments	NONE	NONE	no committed script; only knowledge/SKILL.md mention
claim-gates	claim-index operator queue and claim-ready/* tags	NONE	NONE	no committed script
claim-gates	Source: lost claim-check.mjs (233 lines, read in full 2026-09-28), unprefixed in backticks at claim-gates.md:3	NONE (historical)	~/Projects/bounties/ops/claim-check.mjs	historical record; no :line anchor, so anchorcheck counts 0 cite instances (rc 0); only the test -d guard gates the entry

Classification claim-gates: **partial**. Twelve rows are supported; all sit in corpus/instruments/claim-package-check.py except the reviewer row, which also cites claim-package-selftest.py:83 (the only second-file support). Eight are partial, nine have no committed anchor, and one is contradicted (not-claimable heuristics). The count bar is reached in the appendix only through two non-gate rows (selftest:84 and exemplar status.json:6), which do not evidence gate claims. The committed checker is explicitly the subset the contract states (claim-package-check.py:4-8), so re-grounding must narrow the entry to that subset; keeping the ten unsupported or contradicted claims under a green recheck would be a false ground.

## F3. Entry anchors that do not say what the entry claims (drift, verified with sed -n)
- citation-bases L16 `corpus/instruments/resolve.py:164-172` (lane-root rule). Committed 164-172 = end of strip_anchor and head of brace_expand. The relative rule is 278-286.
- citation-bases L18 `corpus/instruments/resolve.py:31-48` (INTERNAL). Committed 31-48 contains no INTERNAL. INTERNAL is at 60 (doc) and 281 (code).
- citation-bases L41 `corpus/instruments/resolve.py:161-163` (other-root rule). Committed 161-163 = strip_anchor. The other-root rule is at 277 (doc 42-44).
- citation-bases rule 5 `corpus/instruments/resolve.py:74` (line-anchor / comma). Committed 74 = "first match wins (a glob with zero matches does NOT resolve)". The line-anchor regex is at 105 (LINEANCHOR) with strip_anchor at 157-165.
- citation-bases vs anchorcheck.py:59-61: "gone since 2026-10-14" vs the entry's "2026-10-12" (entry L22, L36). The committed bytes disagree with themselves (anchorcheck.py:61-62 says 2026-10-12).
- claim-gates L3 cites the lost claim-check.mjs as a bare backticked path (historical, unprefixed). Its L22-24, L28-29 and similar line numbers refer to the lost script and do not match the committed checker.

## F4. Counter falsification (controls and drafts; scratch copies; quoted output)
Do-nothing control, entry mode, each of the three entries:
```
reground entry=citation-bases.md rows=0 ok=0 exit=1 read=section-count=0
reground entry=claim-gates.md rows=0 ok=0 exit=1 read=section-count=0
reground entry=claim-anatomy-sample.md rows=0 ok=0 exit=1 read=section-count=0
```
Fabricated-token control (six rows with non-existent tokens), entry mode:
```
row G1 ok=0 read=token-not-in-lines ... reground entry=citation-bases.md rows=6 ok=0 files=0 exit=1
row G1 ok=0 read=token-not-in-lines ... reground entry=claim-gates.md rows=6 ok=0 files=0 exit=1
row G1 ok=0 read=token-not-in-lines ... reground entry=claim-anatomy-sample.md rows=6 ok=0 files=0 exit=1
```
Drafts (rows listed in the appendix), entry mode:
```
reground entry=citation-bases.md rows=11 ok=11 files=4 exit=0
reground entry=claim-gates.md rows=16 ok=16 files=3 exit=0
reground entry=claim-anatomy-sample.md rows=7 ok=7 files=2 exit=0
```
Load-bearing (blank each row's token in a scratch corpus, entry mode must go red): citation-bases mutants=11 survivors=none; claim-gates mutants=16 survivors=none; claim-anatomy-sample mutants=7 survivors=none; every mutant exit=1.
Recheck self-run (each draft's recheck replaced by `cd <lane> && python3 corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md`, cwd = tree): `SELF-RECHECK citation-bases rc=0`, `SELF-RECHECK claim-gates rc=0`, `SELF-RECHECK claim-anatomy-sample rc=0`.

Aggregate counter, draft tree (three drafts, base as baseline):
```
gate L1 pass=1 read=gated=21 broken=0 lines=64/base=64
gate L2 pass=1 read=base-gated=24 regrounded=3 citation-bases.md,claim-anatomy-sample.md,claim-gates.md
gate L3 pass=1 read=recheck-lines-clean=3
gate L4 pass=1 read=entry-mode-green=3
gate L5 pass=1 read=append-only=3
gate L6 pass=1 read=mutants=34 survivors=none
gate L7 pass=1 read=still-gated=21 changed=none
c1-gate fixed=7/7 exit=0
```
Finding: the mechanical counter goes 7/7 on these drafts. Its seven limbs check token presence, not that rows support the entry's current claims. The C1 kill rule's non-author semantic check is therefore the only guard. Under that check, the claim-anatomy draft would turn its recheck green while its tallies remain unverified, and the claim-gates draft would turn it green while about 10 of its current claims stay unanchored or contradicted. This is a counter-gaming risk, not a pass.

## F5. Candidate pair (recommendation to the L1)
- citation-bases: full by bar, and a recheck candidate beyond the intended pair. Landing it needs the four drifted anchors corrected and the md:31 cite prefixed (or the recheck replaced). Its own recheck is gated for a non-`test -d` reason.
- claim-gates: partial. Narrow to the 12 supported rows (F2) and drop the 9 unanchored and 1 contradicted claim. The second-file requirement is met only by the selftest:83 row. Not a C1 pair on its own.
- claim-anatomy-sample: partial. Not a C1 pair candidate on current evidence.
- Frozen expectation: 23 gated `test -d` lines plus citation-bases (gated for another reason) match claims.json "before". The after count (gated<=22) needs two re-grounded entries. Only citation-bases is full on substance; claim-gates needs the narrowing above; claim-anatomy-sample is partial. No pair is substance-ready today; citation-bases is the only entry ready for L1 integration.

## F6. Appendix — draft rows (scratch, mechanically verified, not landed)
Each block is an appended `## Re-ground (round 46)` section; the recheck form is in F4. Rows are the four-cell form the counter parses.

citation-bases:
```
| G1 | Relative cites try the lane repo first; INTERNAL when the path exists there | `corpus/instruments/resolve.py:279-281` | `m, p = exists_any(os.path.join(lane_root, base))` |
| G2 | Lane-relative INTERNAL precedence is pinned by a test | `corpus/instruments/test_resolve.py:233` | `self.assert_row(rows, tok_int, "INTERNAL", lane_file, "rel")` |
| G3 | Mirror credit for a relative token is MIRROR-EQUIVALENT and only when realpath-confined | `corpus/instruments/resolve.py:284-285` | `return "MIRROR-EQUIVALENT", p, m, "rel"` |
| G4 | A relative token absent from both roots is GONE | `corpus/instruments/test_resolve.py:235` | `self.assert_row(rows, tok_gone, "GONE", domain="rel")` |
| G5 | Other-root cites RESOLVE when the path exists and are GONE otherwise | `corpus/instruments/resolve.py:277` | `return ("RESOLVES", p, m, "other") if m else ("GONE", "", "", "other")` |
| G6 | MIRROR-EQUIVALENT is name survival, not content identity | `corpus/instruments/README.md:35-38` | `counts name survival, not content survival.` |
| G7 | Lost-marked tokens are never credited and stay GONE | `corpus/instruments/test_resolve.py:237-247` | `def test_lostbase_markers_stay_gone_never_credited(self):` |
| G8 | Lost-marked cites are LOST-RECORDED and never a fail class | `corpus/instruments/anchorcheck.py:160` | `LOST = re.compile(r"^\[lost-` |
| G9 | Blob pin registration form is parsed by one regex | `corpus/instruments/anchorcheck.py:159` | `PIN = re.compile(r"<!--\s*pin:` |
| G10 | Unprefixed mirror names classify BASE-ABSENT until marked lost-tree | `corpus/instruments/anchorcheck.py:59` | `therefore classify BASE-ABSENT (mirror gone since 2026-10-14) until marked` |
| G11 | A bounty-root cite is credited MIRROR-EQUIVALENT only when the mirror holds the suffix | `corpus/instruments/test_resolve.py:253` | `self.assert_row(rows, tok, "MIRROR-EQUIVALENT", mirror_stats, "bounty")` |
```
claim-gates:
```
| G1 | Required six files: report.md, claim_checklist.md, custodian-receipts.json, provenance.json, status.json, evidence/manifest.json | `corpus/instruments/claim-package-check.py:101` | `SIX_FILES = (` |
| G2 | report.md must carry a scope excerpt heading | `corpus/instruments/claim-package-check.py:120` | `SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)` |
| G3 | manifest expected_head_sha256 key present and 64-hex | `corpus/instruments/claim-package-check.py:310` | `head = manifest.get('expected_head_sha256')` |
| G4 | custodian decisions: scope_signal exactly NO_SCOPE_OBJECTION | `corpus/instruments/claim-package-check.py:460` | `if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':` |
| G5 | three-way head binding: head_sha256 equals manifest expected head | `corpus/instruments/claim-package-check.py:471` | `if head.lower() != head_expected.lower():` |
| G6 | manifest_sha256 equals sha256 of current evidence/manifest.json bytes | `corpus/instruments/claim-package-check.py:588` | `if recorded.lower() != actual:` |
| G7 | 5 MiB cap on scanned package files | `corpus/instruments/claim-package-check.py:131` | `MAX_SCAN_BYTES = 5 * 1024 * 1024` |
| G8 | blanket symlink ban on the package tree | `corpus/instruments/claim-package-check.py:659` | `if os.path.islink(os.path.join(dirpath, name)):` |
| G9 | reviewer identity distinct from producer identities | `corpus/instruments/claim-package-check.py:607` | `if identity.strip().casefold() in _identities(manifest):` |
| G10 | hard-gate names: written_scope, authorization, evidence_integrity, no_duplicate_or_prior_submission | `corpus/instruments/claim-package-check.py:127` | `'no_duplicate_or_prior_submission',` |
| G11 | claimable true requires finding_count of at least 1 | `corpus/instruments/claim-package-check.py:618` | `if isinstance(count, bool) or not isinstance(count, int) or count < 1:` |
| G12 | secrets scan: credential-shaped api_key/secret/token/password values | `corpus/instruments/claim-package-check.py:140` | `(?:api[_-]?key` |
| G13 | blocker named by blocked_reason, verdict or claimability_blocker | `corpus/instruments/claim-package-check.py:570` | `for key in ('verdict', 'claimability_blocker', 'blocked_reason'):` |
| G14 | provenance agents non-empty with transition and models | `corpus/instruments/claim-package-check.py:490` | `if not isinstance(agents, list) or not agents:` |
| G15 | selftest: a missing no-submission marker fails R-REPORT | `corpus/instruments/claim-package-selftest.py:84` | `(("marker", "no-submission"), "R-REPORT"),` |
| G16 | exemplar status.json carries claimable as a field | `corpus/instruments/fixtures/claim-package/exemplar/status.json:6` | `"claimable": false,` |
```
claim-anatomy-sample (mechanically passes, substantively partial; see F2):
```
| G1 | Six-file contract: report.md, claim_checklist.md, evidence/manifest.json, custodian-receipts.json, provenance.json, status.json | `corpus/instruments/claim-package-check.py:101` | `SIX_FILES = (` |
| G2 | status.json must carry claim_review with hard_gates, subchecks and reviewer | `corpus/instruments/claim-package-check.py:590` | `review = _require_dict(status, 'claim_review', 'status')` |
| G3 | manifest_sha256 binds status to manifest bytes; absent or null fails | `corpus/instruments/claim-package-check.py:584` | `recorded = status.get('manifest_sha256')` |
| G4 | claimable is a required boolean | `corpus/instruments/claim-package-check.py:609` | `claimable = status.get('claimable')` |
| G5 | reviewer identity distinct from producer identity | `corpus/instruments/claim-package-check.py:607` | `if identity.strip().casefold() in _identities(manifest):` |
| G6 | exemplar status.json fixture carries claimable | `corpus/instruments/fixtures/claim-package/exemplar/status.json:6` | `"claimable": false,` |
| G7 | exemplar status.json fixture carries the do_not_submit guard | `corpus/instruments/fixtures/claim-package/exemplar/status.json:18` | `"do_not_submit": true,` |
```

## Limitations
- Only the three assigned entries were censused; the other 21 gated entries and claim-package-contract.md were not.
- The counter's L6 and L4 were run on scratch copies; the lane file r46-c1-gate.py was copied, not run in place. The pure base export does not contain it, so the self-run used my scratch copy. Freeze controls (marker-only, gutted-entry, fabricated-anchors, single-anchor-file) were not re-run.
- "Verified" is a token-level and line-level match, not semantic. Every "supported" call is my reading and needs a non-author check (the C1 kill rule). The counter cannot make that check (F4).
- Knowledge entries and SKILL.md were treated as non-gate-admissible (counter ANCHOR_DIRS = corpus/instruments/, corpus/source-snapshots/); they informed the classification but produced no gate rows.
- The host's lost roots were tested only for existence; no live target was touched (documentation corpus only).
- Installed tools: none (no pacman, uv, or binary installs were made).
