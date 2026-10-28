# R46ScoutCensus4 — C1 re-groundability census: mission-ledger, operator-queue, ops-invariants

VERDICT: INFO

Scope: per-seat census only. Read-only; no lane byte touched; no scratch dir created (nothing to remove). No draft produced (scout seat returns findings; L1 integrates).

Headline: all three entries are richly corroborated by committed lane prose (12 / 11 / 15 support rows over 4 / 3 / 4 files), but **zero claims in any of the three have a content-bearing anchor under `corpus/instruments/` or `corpus/source-snapshots/`** — the only anchor roots `r46-c1-gate.py --entry` accepts (`ANCHOR_DIRS = ("corpus/instruments/", "corpus/source-snapshots/")`, gate :53). Under the gate bar all three classify `none`; under corpus-wide committed bytes all three classify `full`. Consequence for C1: these three entries cannot join the re-grounded set R without newly committed instruments/snapshots; the intended pair (claim-package-contract.md, claim-gates.md — fixture-anchorable) is the right pair, and this census supplies the negative controls.

## 0. Bar and method

Bar (from `corpus/instruments/r46-c1-gate.py:53` and the `--entry` mode doc, :7-20, check_row :104-131):
- PASS needs section `## Re-ground (round 46)` present once, >= 6 rows, unique ids, every anchor `` `path:N[-M]` `` a regular non-symlink file under `corpus/instruments/` or `corpus/source-snapshots/` inside TREE, never the entry itself, range <= 40 lines, token >= 6 chars whitespace-normalized found in those lines, >= 2 distinct anchor files.

Method: each claim was searched over the ticket-enumerated committed scope (SKILL.md, corpus/knowledge/*, corpus/instruments/* incl. fixtures/, corpus/source-snapshots/*). Every anchor below was verified by running the shown `sed -n` against the lane working tree; tree state checked first:
- `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin rev-parse HEAD` → `323d1f5d825a61cfd0dbf93f9580e092ee21c72a` (one commit past freeze 9f23aab4; that commit, `git show --stat 323d1f5`, touches only `.ufo/waves/round-46/{build-wave1-spec.py,wave-registry.txt,wave1-dispatch.json,wave1-dispatch.stderr.txt,wave1-spec.json,wave1/swarm-registry.json}` — no corpus/SKILL bytes, so working-tree sed == frozen bytes for every file cited).
- Working tree dirty paths are untracked `.ufo/waves/round-46/{final-measure.sh,wave1.ready,wave1.ready.dispatched,wave1/R46ExecPlain.draft/}` — none mine, none cited.
- Markdown census: no LSP server applies (prose claims, not symbols); grep + `sed -n` is the primary evidence method here, not a fallback.

Positive control that the gate bar is satisfiable in this lane (so `none` is a real finding, not a bar defect): `corpus/instruments/fixtures/claim-package/exemplar/status.json` (read in full) carries `"claimable": false`, `"do_not_submit": true`, `"no_submission_performed": true`, `"claim_review.hard_gates.no_duplicate_or_prior_submission"`, `"subchecks.no_secrets"` — i.e. claim-package-contract.md / claim-gates.md claims are anchorable to committed fixtures. None of MY three entries make claims those fixture bytes carry.

## 1. entry = corpus/knowledge/mission-ledger.md

```
entry	claim	anchor	token	verified
mission-ledger.md	missions.jsonl is the append-only hunter-contract state machine written by ops/shared.mjs::appendLedger (:15-16)	SKILL.md:224-226	`append-only hunter-contract state machine`	sed -n '224,226p' SKILL.md → OK
mission-ledger.md	appendLedger is the only writer; 3500-byte cap; truncated:true stub; PIPE_BUF atomicity (:15-20)	SKILL.md:331-334	`caps a line at **3500 bytes**`	sed -n '331,334p' SKILL.md → OK
mission-ledger.md	transition census 718 lines / 260 missions; SCOPED 232 → PLANNED 219 → LEARNED 244; dominant path 207 (:32-56)	SKILL.md:226-228	`Transition census (718 lines / 260 missions)`	sed -n '226,228p' SKILL.md → OK
mission-ledger.md	SUBMITTED/DISCLOSED_FREE are operator-attributed ledger facts, never fleet transitions (:48-56)	SKILL.md:229-231	`operator-attributed ledger facts`	sed -n '229,231p' SKILL.md → OK
mission-ledger.md	matches the 486-mission partition in corpus/knowledge/terminal-classes.md (:46)	corpus/knowledge/terminal-classes.md:3-7	`486-mission freeze`	sed -n '3,7p' terminal-classes.md → OK
mission-ledger.md	telemetry.jsonl is the dispatcher heartbeat (dispatcher_tick, mission_parked, claim_commit_failed, model_reroute, operator_decree…), counts as-of dated (:73-84)	SKILL.md:231-233	`is the dispatcher heartbeat`	sed -n '231,233p' SKILL.md → OK
mission-ledger.md	telemetry worktree carries 3 committed merge-conflict marker lines; JSON.parse fails on exactly those 3; sole consumer attempts() is regex-only (:20-28)	SKILL.md:999	`merge-conflict marker lines`	sed -n '998,1010p' SKILL.md + grep → OK (marker line numbers 4460/4462/4480 themselves are entry-local)
mission-ledger.md	234 rankings-<ts>.json artifacts over 229 distinct stamps (:7-9)	SKILL.md:999	`234 artifacts / 229 stamps`	grep print of SKILL.md:999 showed both substrings → OK
mission-ledger.md	rank.mjs DEFAULTS: p_in_scope .7, p_reproducible .7, p_unique .25, p_accepted .6, effort_hours 60, opportunity_rate 25, direct_cost 0, delay_cost 0, expected_risk_cost 250 (:67-71)	SKILL.md:872-875	`p_unique 0.25, p_accepted 0.6`	sed -n '868,877p' SKILL.md → OK
mission-ledger.md	same DEFAULTS set, second committed statement (:67-71)	corpus/knowledge/ev-model.md:44-48	`p_in_scope .7, p_reproducible .7`	sed -n '44,48p' ev-model.md → OK
mission-ledger.md	candidates.jsonl = the-bounty-hunter intake, run_id b1k-NNN; imports.jsonl binds board feed (:95-112)	SKILL.md:233-234	`intake (run_id \`b1k-NNN\`)`	sed -n '224,234p' SKILL.md → OK
mission-ledger.md	claim-check.mjs row points at corpus/knowledge/claim-gates.md (:129)	corpus/knowledge/claim-gates.md:1-5	`the complete gate list`	sed -n '1,5p' claim-gates.md → OK
mission-ledger.md	ops inventory roles: validate/registry-check/reroute-drill/check-freshness integrity gates (:120-124); claim-index among beyond-ledger writers (:130)	SKILL.md:1008-1009	`integrity gates`	sed -n '998,1010p' SKILL.md → OK
mission-ledger.md	UNSUPPORTED in committed scope: per-event distribution counts (dispatcher_tick 3680, mission_parked 1188, lease_claimed 107, attempt_reset 68, …) (:80-84)	none	—	grep '3680' over corpus+SKILL.md → hits only mission-ledger.md:80 itself (+ corpus/lessons/round-4-aggregator-audit.md:23, outside the enumerated scope); historical census of a lost file
```

Classification (r46-c1-gate.py bar): **none** — 0 gate-eligible anchor rows (no instruments/snapshots bytes carry these claims).
Classification (corpus-wide committed bytes): **full** — 12 anchored claims over 4 files (SKILL.md, terminal-classes.md, claim-gates.md, ev-model.md).
Historical-record statement: everything except the two cross-reference sentences (:46 terminal-classes, :129 claim-gates) and the ops-inventory role gloss is a historical record of the lost tree — writer contract, transition table, telemetry census, candidates/imports shapes, inventory roles all describe `~/Projects/bounties` + `~/Projects/the-bounty-hunter` bytes absent since 2026-09-28; counts carry as-of stamps by the entry's own words (:6-7).

## 2. entry = corpus/knowledge/operator-queue.md

```
entry	claim	anchor	token	verified
operator-queue.md	claim-hold/* tags inert; index only reads claim-ready/*; no hold filter; FOUR queued rows carry holds (2/4/7/10); 9 hold tags all creatordate 2026-09-05 (:12-23)	SKILL.md:777-782	`no hold filter exists`	sed -n '777,788p' SKILL.md → OK
operator-queue.md	nine claim-hold/* tags incl. anthropic; index still queues it as row 4 (:14-15, 87-88)	corpus/knowledge/submitted-registry.md:181-185	`9 \`claim-hold/*\``	sed -n '181,185p' submitted-registry.md → OK
operator-queue.md	anthropic row = byte-identical VDP twin (commit d7dbd9a…, sha ded642e8…, CWE-78), still returns claim-check: OK, do not file (:24-32)	SKILL.md:784-788	`Do not file row 4`	sed -n '777,788p' SKILL.md → OK (SKILL cites abbreviated d7dbd9a/ded642e8; the full-length hashes are entry-local, see F3)
operator-queue.md	the VDP twin is a real filed disclosure (SUBMITTED.md, 2026-09-06T01:19:04Z, operator-attributed) (:25-26)	corpus/knowledge/submitted-registry.md:89-92	`anthropic-plugin-dev-cmd-injection/SUBMITTED.md`	sed -n '89,92p' submitted-registry.md → OK
operator-queue.md	duplicate scan reads claims/ only; vdp-disclosures/ outside it (:24, 88-91)	corpus/knowledge/submitted-registry.md:113-117	`sibling-package scan enumerates only`	sed -n '113,117p' submitted-registry.md → OK
operator-queue.md	submitted_url = filed-report URL (/reports/<id>); submission_url = destination endpoint, not proof of filing (:33-41)	corpus/knowledge/submitted-registry.md:138-141	`destination endpoint, not`	sed -n '138,144p' submitted-registry.md → OK
operator-queue.md	submission_state STAGED variants are informational; a staged payload is not a filing (:41-44)	corpus/knowledge/submitted-registry.md:163-168	`A staged payload is not a filing`	sed -n '163,168p' submitted-registry.md → OK
operator-queue.md	field traps: submitted_url ≠ submission_url; submission_performed:false ≠ unsubmitted; do-not-refile triple (:36-44)	SKILL.md:749-753	`Field traps`	sed -n '749,753p' SKILL.md → OK
operator-queue.md	real /reports/<id> receipts exist only on the 2 SUBMITTED packages (airtable, spotify); queue membership = "never submitted" by field value (:39-41)	SKILL.md:793-795	`receipts exist only on the 2 SUBMITTED packages`	sed -n '793,801p' SKILL.md → OK — but DISCREPANT with submitted-registry.md, see Finding D1
operator-queue.md	dossier rows 10-11: intel BLOCKED-2026-09-11.md still on disk, no authenticated Intigriti session; personio OOS-required takeover gate (:59-60)	SKILL.md:797-799	`BLOCKED-2026-09-11`	sed -n '793,801p' SKILL.md → OK
operator-queue.md	intel hold corroborated as routing decree intel_hold_2026_09_06 (:59)	corpus/knowledge/intake-surface.md:142-143	`intel_hold_2026_09_06`	sed -n '142,146p' intake-surface.md → OK
operator-queue.md	operator-only steps (vault unlock, MFA/2FA, KYC, Submit click, payout rails) are runbook-distilled, source lost (:63-83)	SKILL.md:868-870	`operator-only contract (vault unlock`	sed -n '868,877p' SKILL.md → OK
operator-queue.md	UNSUPPORTED in committed scope: row 3 precondition_holds:true (13/13); row 7 submit/channel-block-20260911.md content; row 5 checklist :7,39 severity; per-row platform routes (:52-61)	none	—	grep 'precondition_holds|channel-block-20260911' over corpus+SKILL.md → hits only operator-queue.md:52,:56 (+ citation-survival.tsv:1253 token-classification row, meta only); the per-row dossier is a historical record of lost packages
```

Classification (r46-c1-gate.py bar): **none** — 0 gate-eligible anchor rows.
Classification (corpus-wide committed bytes): **full** — 11 anchored claims over 3 files (SKILL.md, submitted-registry.md, intake-surface.md).
Historical-record statement: the 12-row dossier, the three "systemic gaps" as statements about `ops/claim-index.mjs`/`ops/claim-check.mjs` source, and the runbook distill are historical records of lost bytes (live re-run + source read date-stamped 2026-09-28; the entry's own :87-91 mark the cross-domain bullets historical). What retains present-day decision value — do-not-file row 4, field-semantics traps, do-not-refile triple — is independently recorded in submitted-registry.md, which is where any future restatement should point.

## 3. entry = corpus/knowledge/ops-invariants.md

```
entry	claim	anchor	token	verified
ops-invariants.md	BANNED = ['cursor','opencode'], word-boundary scan (:18)	SKILL.md:321-324	`BANNED = ['cursor','opencode']`	sed -n '321,338p' SKILL.md → OK
ops-invariants.md	BANNED values, second committed statement (:18)	corpus/knowledge/triage-thresholds.md:390	`['cursor', 'opencode']`	sed -n '389,400p' triage-thresholds.md → OK
ops-invariants.md	PARKED = [] since chatgpt park lifted 2026-09-04; parked checks vacuous by construction (:19)	SKILL.md:324-327	`vacuous by construction`	sed -n '321,338p' SKILL.md → OK
ops-invariants.md	K3_SEATS ['judge','planner']; K3_TOKEN route regex (:20-21)	SKILL.md:327-329	`K3_SEATS = ['judge,`	sed -n '321,338p' SKILL.md → OK
ops-invariants.md	K3_SEATS values, second committed statement (:20)	corpus/knowledge/triage-thresholds.md:392	`['judge', 'planner']`	sed -n '389,400p' triage-thresholds.md → OK
ops-invariants.md	TELEMETRY_EVENTS = 8 registry kinds, runtime kinds emitted by fleet-dispatch (:22)	SKILL.md:340-343	`declares 8 event names`	sed -n '340,346p' SKILL.md → OK
ops-invariants.md	additive round-15 fact recorded in SKILL: TELEMETRY_EVENTS is a decorative whitelist — nothing imports it, appendLedger never checks the name (entry :22 context)	SKILL.md:340-346	`decorative whitelist`	sed -n '340,346p' SKILL.md → OK
ops-invariants.md	sha256File returns null on absent path (:23)	SKILL.md:330-331	`null\` when absent`	sed -n '321,338p' SKILL.md → OK
ops-invariants.md	sha256File null semantics, second committed statement (:23)	corpus/knowledge/triage-thresholds.md:395	`null\` when path absent/unreadable`	sed -n '389,400p' triage-thresholds.md → OK
ops-invariants.md	gitMutationBlocker fail-closed markers + HEAD on main; used by finalize-all/fleet-dispatch/--sync (:24)	corpus/knowledge/triage-thresholds.md:396	`ACTIVE_GIT_OPERATION`	sed -n '389,400p' triage-thresholds.md → OK
ops-invariants.md	gitMutationBlocker absent from the mirror; stalled-rebase consequence (:24)	SKILL.md:335-338	`absent from`	sed -n '321,338p' SKILL.md → OK
ops-invariants.md	appendLedger 3500-byte cap + truncated stub, PIPE_BUF (:25)	SKILL.md:331-334	`3500 bytes`	sed -n '321,338p' SKILL.md → OK
ops-invariants.md	appendLedger cross-ref target exists and carries the writer contract (:25)	corpus/knowledge/mission-ledger.md:15-16	`is the only writer`	sed -n '15,16p' mission-ledger.md → OK
ops-invariants.md	validate.mjs is a subset checker; --strict adds non-empty ev_inputs (:36-44)	corpus/knowledge/triage-thresholds.md:380-384	`hand-rolled`	sed -n '380,384p' triage-thresholds.md → OK
ops-invariants.md	--strict ev_inputs + k3_seats exactly [judge, planner] enforced (:42-44)	SKILL.md:360-362	`requires non-empty \`ev_inputs\``	sed -n '360,362p' SKILL.md → OK
ops-invariants.md	registry-check: empty bucket needs degrade note; banned absent; k3 confined; every grok route must end :low exactly (:66-77)	SKILL.md:375-380	`route must end \`:low\``	sed -n '375,393p' SKILL.md → OK
ops-invariants.md	reroute-drill simulation-only: parses park:<lane>, first non-banned/non-parked/non-k3, degrades to local, reroute_drill telemetry simulated:true, never mutates/spawns/networks (:79-86)	SKILL.md:381-387	`simulated: true`	sed -n '375,393p' SKILL.md → OK
ops-invariants.md	check-freshness THRESHOLD_H = 26 h; exits liveStale>0?1:0; one freshness_check line per run (:88-99)	SKILL.md:388-393	`THRESHOLD_H = 26`	sed -n '375,393p' SKILL.md → OK
ops-invariants.md	sighting scripts are observation windows, display only; authority stays with fleet-dispatch + L1 panes (:101-125)	SKILL.md:1010	`observation windows (display only)`	sed -n '998,1010p' SKILL.md → OK
ops-invariants.md	UNSUPPORTED in committed scope: registry-check live FAIL with seven @role errors + the two mechanics bugs (:57-76); sighting four-managed-windows/kill-scope mechanics (:103-125); kx-card census (:49-53)	none	—	grep over corpus+SKILL.md found no committed restatement of the FAIL run or window mechanics; historical observations of a lost base
```

Classification (r46-c1-gate.py bar): **none** — 0 gate-eligible anchor rows.
Classification (corpus-wide committed bytes): **full** — 15 anchored claims over 4 files (SKILL.md, triage-thresholds.md, mission-ledger.md, intake-surface.md — the last via `k3_seats` = judge+planner, sed -n '142,146p' intake-surface.md → OK).
Historical-record statement: the entire constants table, validator/drill/freshness descriptions, and the sighting how-to describe lost-base files (`~/Projects/the-bounty-hunter` absent since 2026-10-12); even the mirror-relative findings (TELEMETRY_EVENTS decorative, gitMutationBlocker absent) are as-of statements about a then-surviving mirror. The one still-machine-checkable strand is the cross-entry agreement itself: triage-thresholds.md's §9 table records `MATCHES: ops-invariants.md:18-25` per row (:390-397).

## Findings (each: thing attacked/built, command, output)

**F1 — built: per-entry census tables above.** Every row's `sed -n` was executed and its output captured in this session; representative verbatim output, `sed -n '777,788p' SKILL.md`:
```
- **`claim-hold/*` tags are inert** — `claim-index.mjs` only reads
  `claim-ready/*` tags; no hold filter exists. Queued rows 2 (8x8),
  4 (anthropic), 7 (wordpress), 10 (intel) — FOUR, round-13 correction; the
  8x8 hold tag has existed since 2026-09-05T19:28:41-03:00 — carry
  `claim-hold/*` tags the index ignores (9 hold tags total, all creatordate
  2026-09-05).
- **Duplicate scan reads `claims/` only** — row 4
  (`hackerone-anthropic/plugin-dev-test-hook-command-injection`) is
  byte-identical to the operator's own VDP disclosure
  (`vdp-disclosures/anthropic-plugin-dev-cmd-injection`: same commit
  `d7dbd9a`, file, sha256 `ded642e8`, CWE-78) and still returns
  `claim-check: OK`. **Do not file row 4.**
```

**F2 — attacked: "these three entries could join the re-grounded set with enough rows." Falsified for the gate bar.** Command: grep (tool) `telemetry|missions\.jsonl|claim-hold|appendLedger|registry-check|reroute|freshness|sighting|claim-index|K3_SEATS|BANNED` over `corpus/instruments` then `corpus/source-snapshots`. Output: only meta-bytes — `corpus/instruments/citation-survival.{md,tsv}` token-classification rows (e.g. tsv:14 `claim-hold/*	GONE … SKILL+CORPUS`), `r42-closure.sh:423` mutation-scenario name `MutFreshnessCensus`, resolver test fixtures (`resolve-dispatch-fixtures.json`, `test_resolve.py`), `source-recheck.py`; snapshots hit only sidebar words `Telemetry`/`OpenTelemetry` and `CVE-…-36802`. No content-bearing bytes. Corollary warning: do NOT write re-ground rows for these entries anchored to `citation-survival.tsv` — the gate's token-in-lines check would pass mechanically while the rows carry zero evidential weight; that is precisely the "rows are the semantic check the counter cannot make" hole named in the frozen kill_rule (claims.json:13).

**F3 — attacked: full-length fingerprint support for the operator-queue duplicate claim.** Command: grep `ded642e811b4731|d7dbd9a09f59775` over corpus and SKILL.md. Output: corpus hits only `operator-queue.md:27,:29` (the entry itself); SKILL.md hit `:787` with abbreviated `d7dbd9a`, `ded642e8`. The 64-hex commit and sha256 literals are entry-local; committed corroboration covers the identity claim, abbreviated prefixes, `claim-check: OK`, and do-not-file — not the full hash strings.

**F4 — attacked: "queue-membership facts agree across the corpus." They do not (D1).** `SKILL.md:794-795` (sed -n '793,801p' printed: `real \`/reports/<id>\` receipts exist only on the 2 SUBMITTED packages / (airtable, spotify). Queue membership means "never submitted" by field value,`) and `operator-queue.md:39-41` name airtable+spotify; `submitted-registry.md:17-19` shows the two `status.json`-SUBMITTED rows are mozilla (H1 4002776) and spotify (H1 4002810), with airtable (H1 4002789) `status.json` BLOCKED + `submission_state:"SUBMITTED"` + real `submitted_url`; and `sed -n '203,206p' submitted-registry.md` printed `Status histogram over the 280 real packages: PARKED 248, BLOCKED 15, DONE 15, SUBMITTED 2 (= 280; …)`. So "(airtable, spotify)" is an intra-corpus inconsistency (mozilla↔airtable under a status-state reading; airtable is receipt-bearing but not status-SUBMITTED). Any C1 row built on that phrase would re-ground a claim the corpus itself contradicts — reconcile or word the row around submitted-registry.md:17-19 before integrating.

**F5 — checked: frozen C1 framing.** `claims.json:12` ("after") requires >=2 re-grounded entries, >=6 rows over >=2 committed files via `r46-c1-gate.py --entry`; :18 control gives `grep -lE '^recheck:.*test -d ~/Projects/' … | wc -l` base 23, target <=21. Verified the intended pair is the viable one (positive control in §0: the exemplar fixture carries the field vocabulary those entries claim). My three entries supply 0 viable rows each — a third entry in R requires newly committed instruments/snapshots; these three cannot host gate-passing rows from existing committed bytes.

**F6 — negative controls (do-nothing discrimination).** Ran and printed: grep `merge-conflict|4460|4480` over corpus+SKILL.md → SKILL.md:999 carries the caveat in prose (marker line numbers 4460/4462/4480 entry-local only); grep `precondition_holds` → operator-queue.md:52 only; grep `channel-block-20260911` → operator-queue.md:56 + citation-survival.tsv:1253 (meta); grep `3680` → mission-ledger.md:80 + corpus/lessons/round-4-aggregator-audit.md:23 (lessons outside the enumerated scope, noted not counted); grep `p_in_scope` → SKILL.md:828,:873,:957, ev-model.md:14,:44-46, triage-thresholds.md:310,:367 — the DEFAULTS values are double-corroborated. Telemetry line counts 7225 (entry :4) / 7,224 (SKILL.md:231) / 7227 (SKILL.md:999) are as-of-stamped and consistent with the entry's own "counts carry as-of stamps" rule; rank DEFAULTS cited at rank.mjs:55-58 (entry :68) vs :55-59/:56-58 (SKILL.md:872-873) — lost-base line-span variance, values agree.

## Limitations

- Gate-eligible count is 0 for all three entries on today's committed bytes; if the L1 commits new instruments quoting this subject matter, rows must be re-derived from those new bytes.
- `corpus/README.md` (:17,:21,:25) and `corpus/lessons/round-4.md:13-16`, `round-7.md:9-13` also corroborate entry scope/content but sit outside the ticket-enumerated search scope; counted nowhere, noted for the L1.
- Anchors are working-tree bytes shown byte-identical to the freeze for cited files via `git show --stat 323d1f5` (that commit touches only `.ufo/waves/round-46/` dispatch artifacts); no `git archive` export was needed for a read-only census.
- Mutation discipline: no git/jj writes anywhere, no lane edits beyond this seat's own Report file, no scratch created (nothing to remove), no pacman, no installs.
