VERDICT: DRAFT-READY

C1 re-groundability census for the three assigned gated entries (`retirement-autopsies.md`, `source-tree-loss-2026-09-28.md`, `submitted-registry.md`). Result: `source-tree-loss-2026-09-28.md` is a genuine `full` re-ground candidate (8 gate-eligible rows over 3 committed instrument files); `submitted-registry.md` is `partial` (4 rows / 3 files — cannot reach the gate's MIN_ROWS=6); `retirement-autopsies.md` is `none` (0 gate-eligible anchors; its content survives only in SKILL.md/policy-access-playbook.md, both outside the gate's ANCHOR_DIRS). No lane bytes were modified; only this Report file was written.

## Bar (from the counter docstring, read not assumed)

`corpus/instruments/r46-c1-gate.py:3-27` — per-entry PASS needs: section `## Re-ground (round 46)` present once, `>= 6 rows with unique ids, every anchor a regular non-symlink file under corpus/instruments/ or corpus/source-snapshots/ inside TREE (never the entry itself), a <= 40-line range inside the file, and the token (>= 6 chars, whitespace-normalised) inside those lines; >= 2 distinct anchor files.` Constants at `r46-c1-gate.py:37-41`: `MIN_ROWS = 6`, `ANCHOR_DIRS = ("corpus/instruments/", "corpus/source-snapshots/")`. Classification below counts only ANCHOR_DIRS-resolvable rows (the gate bar); non-eligible committed support is recorded separately.

## Pre-state control (gate run before any re-ground exists)

Command: `python3 /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/r46-c1-gate.py --entry corpus/knowledge/<e>.md --root /home/vgpnk/Projects/shokunin/kasegi-shokunin` for all three entries. Output, identical shape each time:

```
reground entry=retirement-autopsies.md rows=0 ok=0 exit=1 read=section-count=0
reground entry=source-tree-loss-2026-09-28.md rows=0 ok=0 exit=1 read=section-count=0
reground entry=submitted-registry.md rows=0 ok=0 exit=1 read=section-count=0
```

All `exit=1` — none of the three carries a `## Re-ground (round 46)` section today; every row set below is additive, and the entries' existing `recheck:` lines are untouched by this census.

Vacuity control: `grep ZZZNOANCHORZZZqxv` over `corpus/instruments` + `corpus/source-snapshots` → `No matches found`; and the token `autopsy` inside ANCHOR_DIRS hits only `corpus/instruments/citation-survival.tsv` GONE-census rows (`[lost-base] ops/park-disposition.mjs:… GONE`) and an unrelated forensics-syllabus line `corpus/source-snapshots/round-24/S032.txt:2694` ("Autopsy, Foremost, RootkitHunter…") — i.e. no instrument or snapshot states the classifier claims, so entry A's `none` is not a search failure.

Tracking control: `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-files -- <all anchor files>` printed all 17 paths (PROVINCE.md, SKILL.md, the 3 entries, root-loss-2026-10-12.md, claim-gates.md, claim-package-contract.md, ev-model.md, triage-thresholds.md, policy-access-playbook.md, instruments README.md/resolve.py/density.py/claim-package-check.py, fixtures exemplar status.json + defect-2-digest claim_checklist.md) — every anchor is committed bytes.

## Entry 1 — corpus/knowledge/retirement-autopsies.md

Classification: **none** (0 gate-eligible rows; 9 committed-supported rows exist but all anchors live in SKILL.md / policy-access-playbook.md, outside ANCHOR_DIRS). Historical-only claims (already stamped, excluded): the 31-autopsy sub-cause partition 27/1/1/2 and 26/5 platform split (entry :84-97), the 85-mission REVIEW drift census 529/85/30/1/1 (entry :89-101; SKILL.md:518-521 stamps it `[corpus-attested as-of 2026-09-28T23:32Z; source tree absent]`).

```tsv
entry	claim	anchor	token	verified
corpus/knowledge/retirement-autopsies.md	`node ops/park-disposition.mjs [--apply]` is dry-run by default	`SKILL.md:477-478`	dry-run	sed -n '477,478p' SKILL.md → "`ops/park-disposition.mjs` (mirror: 80 lines, sha256 `868057c96cc8`; dry-run / by default, `--apply` acts" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	five classes, first match wins: HONEST→LEARNED, H1SPA→RETRY_METHOD, AUTH→RETIRE_AUTH, TRANSIENT→RETRY_TRANSIENT, else REVIEW (no action)	`SKILL.md:481-496`	REVIEW = no action	sed -n '481,496p' SKILL.md → "…→ RETRY_TRANSIENT; else **REVIEW = no action** … The dry-run prints the five class counts" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	RETRY_* is a real requeue: attempt_reset + mission_unparked telemetry, then rmSync of the status file	`SKILL.md:497-500`	rmSync	sed -n '497,500p' SKILL.md → "`rmSync` of the status file so the dispatcher re-picks it" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	RETIRE_AUTH writes docs/autopsies/<id>.md, rewrites state RETIRED, emits mission_retired telemetry	`SKILL.md:502-516`	mission_retired	sed -n '502,516p' SKILL.md → "emits `mission_retired` telemetry carrying the autopsy path" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	autopsy schema = seven fixed parts (4 bold metadata lines + 3 ## sections); "five" was the r15-falsified wording	`SKILL.md:502-516`	seven-part	sed -n '502,516p' SKILL.md → "**seven-part** body — round-15 correction, this section previously said / \"five-part\" while listing seven" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	requeue = delete BOTH the autopsy and the status file; instruction printed into the artifact	`SKILL.md:502-516`	delete BOTH	sed -n '502,516p' SKILL.md → "then delete BOTH the autopsy and the status file" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	parking rule: embed a literal classifier keyword in detail or the disposition pass no-ops	`SKILL.md:518-527`	classifier keyword	sed -n '518,527p' SKILL.md → "**When parking a / mission, embed a literal classifier keyword in `detail`**" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	H1 failure signature: 403 JS shell → try public GraphQL team(handle) once, no auth	`corpus/knowledge/policy-access-playbook.md:9-13`	team(handle)	sed -n '9,13p' → "Public GraphQL `team(handle)` for policy/scope/structured_scopes — no auth" [outside ANCHOR_DIRS]
corpus/knowledge/retirement-autopsies.md	generated "Why" paragraph is boilerplate; trust Reason (verbatim)	`SKILL.md:529-535`	boilerplate	sed -n '529,535p' SKILL.md → "\"Why\" paragraph is boilerplate — it always says \"account login\"" [outside ANCHOR_DIRS]
```

Autopsy note (what is really only a historical record): every claim whose only source was `docs/autopsies/*.md`, `fleets/run/*.status.json` or the mirror bytes (the partition table, the drift census numbers, all `[lost-base] ops/park-disposition.mjs:N` line anchors) is a historical record now — the SKILL.md restatement is itself corpus-quotation, and the gate bar cannot be met because no instrument or snapshot restates the classifier.

## Entry 2 — corpus/knowledge/source-tree-loss-2026-09-28.md

Classification: **full** (8 gate-eligible rows over 3 distinct ANCHOR_DIRS files: instruments/README.md, instruments/resolve.py, instruments/density.py — clears MIN_ROWS=6 and ≥2 files). These rows re-ground the entry's CURRENT §5/§6/§10 instrument claims; the entry's §1-§4 inventories, §7 DATA-half facts, §6/§10 measured rates and §9 forensic conclusions remain historical records (lost-tree/lost-base attested or one-time measurements).

```tsv
entry	claim	anchor	token	verified
corpus/knowledge/source-tree-loss-2026-09-28.md	§10: lane citation-resolvability is re-measurable with the committed `python3 corpus/instruments/resolve.py <lane-repo>`	`corpus/instruments/README.md:11`	citation-resolvability	sed -n '11p' README.md → "| `resolve.py` | **live citation-resolvability** … `python3 corpus/instruments/resolve.py <lane-repo-root>` → writes `citation-survival.md` + `citation-survival.tsv`"
corpus/knowledge/source-tree-loss-2026-09-28.md	§10: the density instrument is committed; ev = path-cites + concrete-table-rows + unique-numerics + unique-ALL-CAPS-signatures	`corpus/instruments/README.md:10`	path-cites	sed -n '10p' README.md → "`ev = path-cites + concrete-table-rows + unique-numerics + unique-ALL-CAPS-signatures`, `dens = ev*100/nb`"
corpus/knowledge/source-tree-loss-2026-09-28.md	§5/§6: line-anchored citations are machine range-checked by the committed anchorcheck.py	`corpus/instruments/README.md:12`	range-checked	sed -n '12p' README.md → "each supported `path:NN[-MM]` citation is range-checked against the lane, frozen mirror, pinned Git blob, or declared ORIGIN-WORK root"
corpus/knowledge/source-tree-loss-2026-09-28.md	§6: resolve.py's resolution policy is documented and deterministic	`corpus/instruments/resolve.py:16-27`	deterministic	sed -n '16,27p' resolve.py → "Resolution policy (documented, deterministic). For a token, strip the anchor"
corpus/knowledge/source-tree-loss-2026-09-28.md	§10: density.py is the runnable reimplementation of the r13 census; Deterministic, stdlib-only	`corpus/instruments/density.py:8-47`	Deterministic	sed -n '8,47p' density.py → line 47 "Deterministic: stdlib only, no randomness, no locale, fixed-format output." (count in range = 1)
corpus/knowledge/source-tree-loss-2026-09-28.md	§10: BAR_R15 = 142.5 is a frozen declared constant carried by instruments/README.md	`corpus/instruments/README.md:69-76`	frozen declared	sed -n '69,76p' README.md → "`BAR_R15 = 142.5` — **frozen declared constant**, equal to the pre-edit file / mean measured at the start of round 15"
corpus/knowledge/source-tree-loss-2026-09-28.md	§10: the density bar rule is amended conjunctive with a ≥60 % resolvability gate	`corpus/instruments/README.md:79-82`	resolvability gate	sed -n '79,82p' README.md → "From round 16 the density bar is **conjunctive** with a resolvability gate:"
corpus/knowledge/source-tree-loss-2026-09-28.md	§5: anchor-base naming is machine-enforced (explicit mirror/ORIGIN-WORK prefixes, realpath-confined, read-only)	`corpus/instruments/README.md:14`	realpath-confined	sed -n '14p' README.md → "Both roots are realpath-confined (`OUTSIDE-BASE`) and read-only."
```

Weakest row: the last one (README enforces base-naming for mirror/ORIGIN-WORK roots, a subset of §5's (a)-(d) rule) — the L1 may drop it and still clear the bar with 7 rows.

Non-eligible committed support (census value, outside ANCHOR_DIRS): the loss event itself is restated in `PROVINCE.md:4-6` (sed → "`~/Projects/bounties` was removed from the filesystem at 2026-09-28T23:51:31Z / (actor UNDETERMINED, data PRESUMED-LOST locally)"); the round-19 errata point at committed `corpus/knowledge/root-loss-2026-10-12.md:5-12` (sed → "| `~/Projects/bounties` | ABSENT (lost 2026-09-28T23:51:31Z) | still ABSENT |"); §8's repairs are live in committed bytes: SKILL.md:502-516 "seven-part … round-15 correction", ev-model.md:36-39 "block `[lost-base] bounty-map/schema.json:32-52` — round-15 correction: the close is one / line later than the `:32-51`", triage-thresholds.md:7 "**Round-15 anchor-base pins (both bases moved under this file).**".

## Entry 3 — corpus/knowledge/submitted-registry.md

Classification: **partial** (4 gate-eligible rows over 3 distinct ANCHOR_DIRS files — cannot reach MIN_ROWS=6, so this entry cannot pass the gate alone; the L1 should not spend one of its two re-grounds here unless more eligible rows are added by another seat). The rows re-ground the entry's durable field-vocabulary/operator-gating claims; everything sourced from `~/Projects/bounties` bytes or origin-work receipts (the three verified submissions :13-19, archive-era receipts :21-47, elastic probable block, anthropic VDP row, the cross-tree double-filing gap mechanism :100-133, STAGED census :163-168, alias field census :169-176, tags, status-less dirs, zips) is a historical record — several of those lines already carry the entry's own `[r22 correction: … historical]` stamps and the `:105` cite is itself `[lost-tree]`-marked.

```tsv
entry	claim	anchor	token	verified
corpus/knowledge/submitted-registry.md	`no_duplicate_or_prior_submission` is a named hard gate the committed package checker requires	`corpus/instruments/claim-package-check.py:122-128`	no_duplicate_or_prior_submission	sed -n '122,128p' claim-package-check.py → "HARD_GATE_KEYS = ( / 'written_scope', / 'authorization', / 'evidence_integrity', / 'no_duplicate_or_prior_submission', / )"
corpus/knowledge/submitted-registry.md	`do_not_submit` / `no_submission_performed` are real status-vocabulary fields, instantiated in the committed fixture	`corpus/instruments/fixtures/claim-package/exemplar/status.json:18-19`	no_submission_performed	sed -n '18,19p' status.json → " \"do_not_submit\": true, / \"no_submission_performed\": true,"
corpus/knowledge/submitted-registry.md	prior-submission check is OPERATOR-GATED and the hard gate sits PENDING pre-review (staged ≠ filed)	`corpus/instruments/fixtures/claim-package/exemplar/status.json:9-25`	prior-submission check	sed -n '9,25p' status.json → "\"OPERATOR-GATED prior-submission check\" (:10) … \"no_duplicate_or_prior_submission\": \"PENDING\" (:25)"
corpus/knowledge/submitted-registry.md	portal no-duplicate confirmation is operator-only (no agent may submit or create portal records)	`corpus/instruments/fixtures/claim-package/defect-2-digest/claim_checklist.md:31-34`	no duplicate exists	sed -n '31,34p' claim_checklist.md → "only the operator can confirm on the portal that no duplicate exists."
```

Non-eligible committed support: the prior-submission guard predicate is restated verbatim in committed `corpus/knowledge/claim-gates.md:81-85` (sed → "Prior-submission guard: `submission_performed`, `submitted_url`, or / `submission_state:'SUBMITTED'` fails; PLUS a **global** scan … duplicate (L184–199).") and the not-claimable heuristics incl. `do_not_submit` at `claim-gates.md:78-80` — both are knowledge files, outside ANCHOR_DIRS, so they extend the census but not the gate count.

## Commands run (all read-only; quoted outputs above)

- `grep` (tool) over SKILL.md, policy-access-playbook.md, instruments/, source-snapshots/, fixtures/, the three entries, README.md, SCORECARD.md, claim-gates.md, claim-package-contract.md — line-numbered hits quoted in findings.
- `read` (tool) of r46-c1-gate.py:1-150 (docstring + check_row/entry_mode), the three entries, root-loss-2026-10-12.md:1-25, resolve.py:1-25, density.py:1-25.
- `sed -n '<r>p'` verification batches over SKILL.md (477-535), policy-access-playbook.md (9-13), instruments/README.md (10-14, 69-82), resolve.py (16-27), density.py (1-2, 8-47, 24-32), claim-package-check.py (120-129), fixtures exemplar status.json (4, 9-11, 18-19, 25), defect-2-digest/claim_checklist.md (31-34), PROVINCE.md (3-7), root-loss-2026-10-12.md (5-12), claim-gates.md (74-85), ev-model.md (36-39), triage-thresholds.md (1-8).
- `git -C <lane> ls-files -- <anchors>` → all 17 tracked.
- `python3 corpus/instruments/r46-c1-gate.py --entry <each> --root <lane>` → three `rows=0 ok=0 exit=1 read=section-count=0` lines.

## Limitations

- Tokens were located in the committed worktree (the gate's `--entry` mode measures TREE the same way). I did not diff anchor files against the frozen base `914ca0b6` — the gate imposes no base-stability constraint on anchor files (L5/L7 constrain only the re-grounded entry's own lines), and all anchors are pre-existing tracked files.
- Row sets are what the current committed bytes support; if another seat adds eligible instruments this round, submitted-registry may cross MIN_ROWS=6 — re-count before excluding it.
- I ran no fixture repos and made no exports; scratch root `/fast/scratch/hyaku/kasegi-r46/R46ScoutCensus6` held only TMPDIR and is removed at yield.
- The intended re-ground pair (claim-package-contract.md, claim-gates.md) is other seats' assignment; my claim-gates.md lines are cited only as non-eligible support for submitted-registry.
- No credential material, no live-target testing (corpus is documentation only); no git/jj mutation anywhere.
