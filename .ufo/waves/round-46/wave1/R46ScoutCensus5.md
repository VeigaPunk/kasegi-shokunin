VERDICT: BROKEN

Scope: C1 re-groundability census for policy-access-playbook, program-quirks, repo-git-state (read-only; no lane edits; this file is the only write). Verdict is BROKEN on two counts: (a) none of the three entries is re-groundable to the r46-c1-gate.py bar; (b) the frozen per-entry counter is polarity-blind and passes a fixture whose anchors record lost citations. Draft F28 and C1 re-ground builds are NOT done by this seat (scout seat is read-only, single census item); the census below is the input for the builder seats.

Bases read: committed base 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba (corpus, SKILL.md, PROVINCE.md, SCORECARD.md, SHONEN.md, LOG.md, exported by `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin archive 914ca0b6956f01d87b2e252ffad06fe74ec5d9ba corpus SKILL.md PROVINCE.md SCORECARD.md SHONEN.md LOG.md | tar -x -C <scratch>/base`); freeze 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5 additions (r46-c1-gate.py, r46-c2-gate.py, source-snapshots/round-46/S073.txt, manifest.json), exported the same way with `corpus` only.

## Findings

### F1 — Lane state and the three entries' recheck lines (fail closed, as claimed)
Command: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse --verify 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5^{commit}` and the same for 914ca0b.
Output: `9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5` / `914ca0b6956f01d87b2e252ffad06fe74ec5d9ba`.
Command: `git -C ... show --stat --format='%H %s' 9f23aab4636b620cdcf7ac3d3a29a5a06dd184b5`
Output (excerpt): `10 files changed, 1539 insertions(+)` covering `corpus/instruments/r46-c1-gate.py | 275`, `r46-c2-gate.py | 325`, `corpus/source-snapshots/round-46/S073.txt | 589`, `manifest.json | 63`, plus `.ufo/waves/round-46/*` controls. The freeze commit does NOT touch the three entries.
Command: `for e in ...; cmp -s base/corpus/knowledge/$e.md freeze/...` → `unchanged` for all three.
Command: run each entry's recheck with cd-prefix stripped, cwd = base export, read-only:
- policy-access-playbook: `rc=1 cmd=test -d ~/Projects/bounties && test -d ~/Projects/the-bounty-hunter && python3 corpus/instruments/anchorcheck.py ...`
- program-quirks: `rc=1 cmd=test -d ~/Projects/bounties && python3 corpus/instruments/anchorcheck.py ...`
- repo-git-state: `rc=1 cmd=test -d ~/Projects/bounties/.git && git -C ~/Projects/bounties rev-parse HEAD`
Host check: `test -d ~/Projects/bounties` → `bounties ABSENT`; `the-bounty-hunter ABSENT`. So all three are gated, as the entries' own notes say.

### F2 — Counter entry mode on the three entries (no Re-ground section exists)
Command: `python3 -I <freeze>/corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md --root <freeze>` for each entry.
Output (all three): `reground entry=<e>.md rows=0 ok=0 exit=1 read=section-count=0`, exit=1.
Positive control: `grep -cF "## Re-ground (round 46)" <freeze>/corpus/instruments/r46-c1-gate.py` → `3`. Do-nothing control on unmodified base program-quirks: `reground entry=program-quirks.md rows=0 ok=0 exit=1 read=section-count=0`.

### F3 — Counter falsification: a loss-record fixture PASSES the per-entry bar
Built in scratch only (copy of base corpus; a `## Re-ground (round 46)` section appended to program-quirks.md). Seven rows anchored to `corpus/instruments/citation-survival.tsv:877, :354, :1203, :1346, :231, :240` and `corpus/instruments/citation-survival.md:156`, tokens copied from those lines.
Command: `python3 -I <freeze>/corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/program-quirks.md --root <scratch>/fab`
Output: `row G1 ok=1 read=token-located` … `row G7 ok=1 read=token-located` … `reground entry=program-quirks.md rows=7 ok=7 files=2 exit=0`, exit=0.
The anchored lines it passed on, verified with `sed -n '877p' corpus/instruments/citation-survival.tsv` and `sed -n '354p' ...` and `sed -n '156p' corpus/instruments/citation-survival.md | cut -c1-200`:
- `deployments/<chain>-core.json	GONE		1		rel	1	+CORPUS`
- `/<program>/reports/new	GONE		1		other	1	+CORPUS`
- `| \`corpus/knowledge/mission-control.md:3\` | INTERNAL | ... | in range |`
The citation-survival.tsv header is `citation class resolved_path files_citing_count method domain occurrences scopes` and citation-survival.md:19 defines `GONE` as a terminal outcome class (`GONE(1346)`), i.e. the citation's target is unresolvable. The counter checks token presence only, not polarity, so a row recording a lost citation passes exactly like a row supporting a live claim. This is the counter-level gap the claims.json kill rule's "non-author reading" clause exists to catch. Not fixed here (lane read-only).

### F4 — Claim-level census against committed anchors (search: grep -F, base + freeze additions)
Command (per claim, wording-level): `grep -rnF --exclude=<self> -- "<token>" corpus/instruments corpus/source-snapshots corpus/knowledge SKILL.md PROVINCE.md SCORECARD.md SHONEN.md LOG.md`. 54 wording tokens (PAP 14, PQ 20, RGS 20). Freeze additions searched separately: 0 hits for all 54 tokens.
Command (implementation-level tokens, 26 tokens: in_scope_assets, impact_ceiling, credential_policy, invitation, external_effect, policy_sha256, is-ancestor, security.txt, ...): hits recorded in the table below; each implementation hit was read with sed -n.
Do-nothing control: `grep -rnF -- "zqxj-r46-nonexistent-control-7f3" corpus/instruments corpus/source-snapshots corpus/knowledge SKILL.md | wc -l` → `0`.
Topic sweep (anchor dirs): `Cantina 0`, `Intigriti 0`, `SIX Group 0`, `claim-ship 0`, `dydx 0`, `morpho 0`, `SEAL 0`, `kycRequired 0`, `plazir 0`, `Pendle 1` (only a citation row), `george/ 2` (knowledge-level citation rows), `security.txt 9`, `Safe Harbor 6`, `HackerOne 12`, `Immunefi 2`, `Bugcrowd 3`.

Mechanical hits in anchor dirs and what they actually say:
- `deployments/<chain>-core.json` → citation-survival.tsv:877 — GONE row (loss record), not support.
- `reports/new` → citation-survival.tsv:354, :1203, :1346 — GONE rows, not support.
- `mission-control` (generic token) → citation-survival.tsv:231,240,1070–1090,1379,1446; citation-survival.md:156; README.md:294; knowledge-expected.txt:38 — all about mission-control.md citations; not the SKILL.md section claim. Rejected as a match for RGS-20.
- Implementation hits that DO bear on a claim: `claim-package-check.py:524-526` (policy_sha256 must be 64-hex), `:527-529` (external_effects_performed must be empty), docstring `:63-66`; `r36-closure.sh:316`, `r37-closure.sh:432,649` (merge-base --is-ancestor).
- Topic-only (present but not the claim): `source-snapshots/round-24/S003.txt:173-176` (RFC 9116 purpose text, not "stub ≠ scope"); `source-snapshots/round-34/S051.txt` (Immunefi severity system; `grep -F -i scope` → no output; 0 `deployments`/`whitelist`).

### F5 — Knowledge-echo and root-doc restatements (not anchors; not counter-grade)
Each verified with sed -n: SKILL.md:94, :128, :129, :132, :314, :594, :654, :1020, :1021; LOG.md:36; corpus/knowledge/program-quirks.md:46; retirement-autopsies.md:85,128; claim-anatomy-sample.md:41,47; ufo-workspaces.md:369; source-tree-loss-2026-09-28.md:58,76; target-checkouts.md:12; submitted-registry.md:213.
Circularity found: SKILL.md:314 cites `corpus/knowledge/repo-git-state.md` as the source for the Sep 7–15 working-tree-only claim (RGS-08) — the echo is not independent. retirement-autopsies.md:85,128 cite policy-access-playbook.md for the GraphQL workaround (PAP-03) — the echo is circular too.
Token collision: claim-anatomy-sample.md:47 is a `hackerone-hyatt` row with `honest-zero-no-claimable-finding`; it does not support PQ-10 (cantina-morpho).

### F6 — Method-level support for one repo-git-state rule
`corpus/knowledge/repo-git-state.md:42` says single-witness git claims need `--is-ancestor`. Committed r36/r37 closure scripts use `merge-base --is-ancestor` at r36-closure.sh:316, r37-closure.sh:432, :649 (sed -n verified). This anchors the METHOD only; the lesson sentence exists in no committed instrument (`grep -rlF "single-witness" corpus/instruments corpus/source-snapshots` → 0).

## Classification (bar: r46-c1-gate.py: section with >=6 rows, each anchored under corpus/instruments/ or corpus/source-snapshots/, tokens located, >=2 files)

- policy-access-playbook — PARTIAL (2 of 14 current claims partly anchored, both in one file: claim-package-check.py; both are contract halves, not the observed platform reality). Counter bar: 2 rows / 1 file, FAIL.
- program-quirks — NONE (0 claims semantically anchored; PQ-07 and PQ-13 match only GONE loss rows). Counter bar: 0 rows, FAIL.
- repo-git-state — PARTIAL (1 of 21 current claims: the method row RGS-21, 2 files; all state claims are historical snapshot). Counter bar: 1 row / 2 files, FAIL.

What current claims are really only a historical record:
- policy-access-playbook: PAP-01, 02, 03, 04, 05, 07, 08, 11, 12, 13 (observed platform reality and autopsy-anchored examples, all tagged or sourced from lost bases); PAP-06 observed-reality half and PAP-14 (field absent from code) are historical/unanchored. Live: only the contract halves PAP-06 (policy_sha256 bind) and PAP-09 (external-effect principle).
- program-quirks: all PQ-01..PQ-20 are 2026-09-28 observations of ingestion packages in lost trees (header: "[lost-tree] claims/cantina-pendle/ingestion-20260915/"). PQ-07 and PQ-13 are contradicted by their own anchors (GONE).
- repo-git-state: all state claims RGS-01..RGS-20 are a dated (2026-09-28) snapshot of ~/Projects/bounties, which is absent on this host; the only live-tense material is the method row RGS-21.

## Limitations
- Searches are literal grep -F over committed bytes; a paraphrased implementation could be missed. Mitigated by 31 implementation-level tokens and topic sweeps (0 anchor files for Cantina, Intigriti, SIX Group, dydx, morpho, SEAL, kycRequired).
- Bases ~/Projects/bounties and ~/Projects/the-bounty-hunter are absent, so no state claim can be re-verified against its source; the census establishes anchor presence, not truth.
- I did not re-run the full seven-limb aggregate (classify runs 24+ recheck commands); I quoted the frozen controls only where I re-ran the entry mode and the do-nothing/positive controls myself.
- The F3 fixture is a falsification artifact in scratch, not a re-ground; it is not a draft and is not in the lane.
- Operator identity handles in the entries were not reproduced in this report.
- Scratch dir removed on exit.

## Census TSV (entry, claim, anchor, token, verified)

```
entry	claim	anchor	token	verified
policy-access-playbook	PAP-01 HackerOne HTML page is a JS shell	none	HTML page is a JS shell	grep -rnF over corpus+root docs: 0 hits
policy-access-playbook	PAP-02 HackerOne /policy 403 unauthenticated	none (echo SKILL.md:128)	can 403 unauthenticated	sed -n 128p SKILL.md (restatement, not anchor)
policy-access-playbook	PAP-03 HackerOne GraphQL team(handle) gives policy/scope without auth	none (echo program-quirks.md:46; retirement-autopsies.md:85,128 circular)	team(handle)	sed -n 46p corpus/knowledge/program-quirks.md; sed -n '85p;128p' corpus/knowledge/retirement-autopsies.md
policy-access-playbook	PAP-04 Bugcrowd auth-walled SPA shell for anonymous fetch	none	Auth-walled SPA shell for anonymous fetch	grep -rnF: 0 hits
policy-access-playbook	PAP-05 Bugcrowd: try public brief/changelog JSON once	none (echo SKILL.md:129)	Try public brief/changelog JSON once	sed -n 129p SKILL.md (restatement)
policy-access-playbook	PAP-06 Immunefi/Cantina/HackenProof public pages carry real scope; bind via policy_sha256	partial: corpus/instruments/claim-package-check.py:524-526 (bind half only)	policy_sha256	sed -n '524,526p' corpus/instruments/claim-package-check.py; observed half: grep -F -i scope source-snapshots/round-34/S051.txt → no output
policy-access-playbook	PAP-07 RFC 9116 security.txt stub is not scope; no assets+no grant means park	none (topic only: corpus/source-snapshots/round-24/S003.txt:173-176)	Stub ≠ scope	grep -rnF: 0 hits; sed -n '172,176p' S003.txt (RFC purpose text, not the claim)
policy-access-playbook	PAP-08 Terms-gated policy (SIX Group) requires terms acceptance	none	reading Program Rules requires terms acceptance	grep -rnF: 0 hits; 'SIX Group' 0 anchor files
policy-access-playbook	PAP-09 Terms acceptance is a forbidden external effect (autopsy + retire)	partial: corpus/instruments/claim-package-check.py:527-529 (general external-effect gate; no 'terms' term)	external_effects_performed	sed -n '527,529p' corpus/instruments/claim-package-check.py
policy-access-playbook	PAP-10 Generic invitation prose does NOT bind an asset	none	does NOT bind an asset	grep -rnF 'does NOT bind an asset' 0; 'invitation' 0 files
policy-access-playbook	PAP-11 SEEK stop_reason PUBLIC_BRIEF_INCOMPLETE_NO_EXACT_ASSETS	none (anchor is lost-tree)	PUBLIC_BRIEF_INCOMPLETE_NO_EXACT_ASSETS	grep -rnF: 0 hits
policy-access-playbook	PAP-12 in_scope_assets:[] records 'not observed in this response', never 'no scope'	none	not observed in this response	grep -rnF: 0; 'in_scope_assets' 0 files
policy-access-playbook	PAP-13 volatile-field redactions recorded; content_hash_basis	none (echo SKILL.md:94)	content_hash_basis	sed -n 94p SKILL.md (restatement); grep instruments: 0 files
policy-access-playbook	PAP-14 grant field external_effect_authorization null unless preauthorized	none (field absent; code has external_effects_performed, not the same field, not stretched)	external_effect_authorization	grep -rlF: 0 files
program-quirks	PQ-01 Cantina $100 submission deposit, read-only live-balance gate	none	$100 submission deposit	grep -rnF: 0 hits
program-quirks	PQ-02 Cantina findings valid only with executable impact on a live market	none	findings valid only with executable impact	grep -rnF: 0; 'executable impact' 0 files
program-quirks	PQ-03 Cantina malicious-trusted-role preconditions OOS	none	malicious-trusted-role preconditions OOS	grep -rnF: 0; 'trusted-role' 0 files
program-quirks	PQ-04 Cantina AI-assist disclosure required	none (r45-counters-selftest-c2.py:96 is a selftest prompt, not the rule)	AI-assist disclosure required	sed -n 96p corpus/instruments/r45-counters-selftest-c2.py
program-quirks	PQ-05 Cantina SEAL Whitehat Safe Harbor = active exploits only	none	SEAL Whitehat Safe Harbor = active exploits only	grep -rnF: 0; 'SEAL' 0 anchor files
program-quirks	PQ-06 Cantina kycRequired false at submission	none	kycRequired: false at submission	grep -rnF: 0; 'kycRequired' 0 anchor files
program-quirks	PQ-07 Cantina in-scope addresses enumerated in deployments/<chain>-core.json keys	GONE loss row only: corpus/instruments/citation-survival.tsv:877 (not support)	deployments/<chain>-core.json	sed -n 877p corpus/instruments/citation-survival.tsv → "deployments/<chain>-core.json	GONE..."
program-quirks	PQ-08 whitelist membership dynamic -> source-review-only under no-chain-contact boundary	none	source-review-only under no-chain-contact boundary	grep -rnF: 0 hits
program-quirks	PQ-09 cantina-dydx BLOCKED positive-blocked-live-precondition	none (echo SKILL.md:654 pendle context; LOG.md:36 restates)	positive-blocked-live-precondition	sed -n 654p SKILL.md; sed -n 36p LOG.md; anchor grep 0 files
program-quirks	PQ-10 cantina-morpho BLOCKED honest-zero-no-claimable-finding	none (knowledge hit claim-anatomy-sample.md:47 is a hackerone-hyatt row: token collision)	honest-zero-no-claimable-finding	sed -n 47p corpus/knowledge/claim-anatomy-sample.md
program-quirks	PQ-11 cantina-euler/uniswap/reserve-protocol PARKED honest-zero-local-source-review	none (knowledge echo claim-anatomy-sample.md:41, reserve-protocol row only)	honest-zero-local-source-review	sed -n 41p corpus/knowledge/claim-anatomy-sample.md
program-quirks	PQ-12 HackerOne portal fields React-controlled	none	React-controlled	grep -rnF: 0 hits
program-quirks	PQ-13 HackerOne submit route /<program>/reports/new	GONE loss rows only: corpus/instruments/citation-survival.tsv:354,1203,1346 (not support)	reports/new	sed -n '354p;1203p;1346p' corpus/instruments/citation-survival.tsv → GONE rows
program-quirks	PQ-14 HackerOne severity is portal language	none	portal language	grep -rnF: 0 hits
program-quirks	PQ-15 HackerOne payout needs payout method + tax form	none	payout needs payout method	grep -rnF: 0 hits
program-quirks	PQ-16 Intigriti KYC for payouts	none	KYC for payouts	grep -rnF: 0 hits
program-quirks	PQ-17 Intigriti Intel self-assigns severity (Unscored, Intel assigns CVSS v4.0)	none (echo SKILL.md:594)	Intel assigns CVSS	sed -n 594p SKILL.md (restatement)
program-quirks	PQ-18 Bugcrowd unprovisioned credential means no credentialed testing	none	unprovisioned credential	grep -rnF: 0 hits
program-quirks	PQ-19 Bugcrowd some programs forbid all automated tooling	none	forbid all automated tooling	grep -rnF: 0 hits
program-quirks	PQ-20 Bugcrowd AI-content rejection clause (low-effort or AI-generated content)	none	low-effort or	grep -rnF: 0 hits in anchors
repo-git-state	RGS-01 Repo state: interactive rebase in progress	none	interactive rebase in progress	grep -rnF: 0 hits (dated snapshot of absent ~/Projects/bounties)
repo-git-state	RGS-02 HEAD detached at 58acb6d8	none	HEAD detached at	grep -rnF: 0 hits
repo-git-state	RGS-03 Rebase stop: 1 command done (pick 3d28a716), 0 remaining	none	pick 3d28a716	grep -rnF: 0 hits
repo-git-state	RGS-04 autostash present	none (echo SKILL.md:1021)	autostash present	sed -n 1021p SKILL.md (restatement)
repo-git-state	RGS-05 local main 3d28a716 has 171 commits	none	171 commits	grep -rnF: 0 hits
repo-git-state	RGS-06 origin/main tip 7dce2872 has 180 commits	none (echo SKILL.md:1021)	7dce2872	sed -n 1021p SKILL.md (restatement)
repo-git-state	RGS-07 dirty tree 903 entries	none (echo SKILL.md:1021)	903 entries	sed -n 1021p SKILL.md (restatement)
repo-git-state	RGS-08 Sep 7-15 fleet work is working-tree-only	none (echo ufo-workspaces.md:369; SKILL.md:314 circular: cites repo-git-state.md)	is working-tree-only	sed -n 369p corpus/knowledge/ufo-workspaces.md; sed -n 314p SKILL.md
repo-git-state	RGS-09 all 12 claim-* tags are ancestors of origin/main	none	tags are ancestors of	grep -rnF: 0 hits
repo-git-state	RGS-10 claim-ship is a merged ancestor line	none	merged ancestor line	grep -rnF: 0 hits
repo-git-state	RGS-11 origin/main tip is a plazir lore commit	none	plazir lore:	grep -rnF: 0; 'plazir' 0 anchor files
repo-git-state	RGS-12 claims/ tracked 198 files / 19 program dirs	none	198 files / 19 program dirs	grep -rnF: 0 hits
repo-git-state	RGS-13 .ufo/ 1.5 G on disk, 0 tracked	none (echo source-tree-loss-2026-09-28.md:58)	1.5 G (bh* workspaces	sed -n 58p corpus/knowledge/source-tree-loss-2026-09-28.md (restatement)
repo-git-state	RGS-14 fleets/run ignored by design (.gitignore:8-9)	none (echo SKILL.md:1020)	ignored by design	sed -n 1020p SKILL.md (restatement)
repo-git-state	RGS-15 george/ 49 G untracked	none (echo target-checkouts.md:12; source-tree-loss-2026-09-28.md:76)	49 G	sed -n 12p corpus/knowledge/target-checkouts.md; sed -n 76p corpus/knowledge/source-tree-loss-2026-09-28.md
repo-git-state	RGS-16 root zip snapshots untracked	none (echo submitted-registry.md:213)	claim-ready-packages-2026-09-15.zip	sed -n 213p corpus/knowledge/submitted-registry.md (zip contents, not tracking status)
repo-git-state	RGS-17 .gitignore modified-uncommitted (HEAD has 9 lines)	none	modified-uncommitted (HEAD has 9)	grep -rnF: 0 hits
repo-git-state	RGS-18 656 claims/ files cite .ufo/ paths, 51 dangling	none	656 claims/ files cite	grep -rnF: 0 hits
repo-git-state	RGS-19 pre-09-06 commit citations remain valid; git log for Sep 7-15 finds nothing	none	pre-09-06 and remain valid	grep -rnF: 0 hits
repo-git-state	RGS-20 SKILL.md mission-control section describes design, not current state	none (mechanical 'mission-control' hits are mission-control.md citation rows: citation-survival.tsv:231,240,1070; rejected)	mission-control	sed -n '231p;1070p' corpus/instruments/citation-survival.tsv
repo-git-state	RGS-21 single-witness git claims need --is-ancestor, not log --oneline (method)	partial: corpus/instruments/r36-closure.sh:316; corpus/instruments/r37-closure.sh:432,649	merge-base --is-ancestor	sed -n '314,317p' corpus/instruments/r36-closure.sh; sed -n '430,433p;647,650p' corpus/instruments/r37-closure.sh
```

CLASSIFICATION policy-access-playbook: partial (2 of 14 claims partly anchored, 1 file)
CLASSIFICATION program-quirks: none (0 of 20; loss rows only)
CLASSIFICATION repo-git-state: partial (1 of 21: method row only, 2 files; state claims historical)
