# kasegi round 47 — non-author verifier spot-check (hyaku closure)

author: hyaku closure (non-author integrator, @m_zfl)
Closed 2026-10-30 against lane tip `77551628781a10f03b98298f035a4565e9c0d975` (branch `master`), report `.ufo/reports/round-47/kasegi.md` (fleet commit `5968df7684d6c020ba401f090e6a2e2d6f5faed1`). This closure did not author the round; it verifies, spot-checks, and closes it.

## 1. Step-1 conformance

- Report committed in the fleet repo by the lane identity: `git log --format='%an %ae %H' -- .ufo/reports/round-47/kasegi.md` → `kasegi-shokunin kasegi@shokunin.local 5968df7684d6c020ba401f090e6a2e2d6f5faed1`.
- `## SHONEN` heading present in the report with one `[~]` line per box (4 of 4 SHONEN.md boxes).
- Every cited lane hash exists and is an ancestor of `refs/heads/master` (jj-colocated repo, git HEAD detached; ancestry tested against the branch ref, not `@{u}`): `308a2cb2`, `82a8bd70`, `65e19bdb`, `f074bffb`, `f0809bca`, `29c02f99`, `77551628`, base `fc8e0af2` — all `git merge-base --is-ancestor <h> refs/heads/master` = OK.
- Helper state: `scripts/hyaku/jj-lane.sh state` → `branch=master local=77551628781a10f03b98298f035a4565e9c0d975 remote=77551628781a10f03b98298f035a4565e9c0d975 ahead=0 behind=0`; `git status --porcelain` → 0 lines. Pushed, no uncommitted round work.
- Dispatched prompt `.ufo/prompts/kasegi-round-47.md` carries the full template contract: mission/axes binding (§1), 1–3 falsifiable claims with lowest-axis rule (§2), L2 ≥8 one-batched-swarm floor (§3), report contract with path, ordering, SHONEN heading and commit-hash citations (§4), commit-then-push and push scope (§4/§5), L0 side channel (§5), lane write scope (§6 item 3), plus the hyaku addendum §6 (run-11 routing, 64–128 band, WAVE-DONE rule, inline spawn handoff, assimilation contract, scratch discipline).
- All seven round commits carry the lane identity (`git log d8dfbcbf..77551628781a` — every author `kasegi-shokunin`).
- Report is a real report, not a marker: work performed with evidence pointers, landed changes tied to `LOG.md` Round 47 (LOG.md:2033) and per-commit hashes, per-claim before→after with counting commands, Sources & frontier with census before/after, trend verdicts, SHONEN assessment. Round shape reported: 64 + 32 = 96 seats; `wave1-results.json` holds 64 rows (the five empty-payload rows exactly as disclosed: R47ExecReanchor, R47CritClaims, R47CritAssim, R47RevengerD7, R47Simplifier — no terminal status invented), `wave2-results.json` holds 32 rows.
- Watchdog digest (copied from the closure dispatch; verified against `.ufo/watchdog.log` lines 1949–1990):
  - `2026-10-30T02:36:12-03:00 launch kasegi round=47 pgid=3506832 driver=hyaku-inline attempt=1`
  - `2026-10-30T02:48:43-03:00 lane-dead-no-report kasegi round=47; retry same round (hyaku-inline attempt=1: L1 KasegiR47 ended without a landed report: FAIL report_of (missing, unchanged, no SHONEN heading, or < 400B): .ufo/reports/round-47/kasegi.md)`
  - `2026-10-30T02:48:45-03:00 launch kasegi round=47 pgid=3172519 driver=hyaku-inline attempt=2`
  - `2026-10-30T04:09:08-03:00 lane-dead-no-report kasegi round=47; retry same round (hyaku-inline attempt=2: attempt-2 prompt rendered but L1 never spawned after orchestrator parse error; predecessor ended with provider permission_denied; campaign paused, round 47 remains uncompleted)`
  - `2026-10-30T07:19:37-03:00 launch kasegi round=47 pgid=1570756 driver=hyaku-inline attempt=3`
  - `2026-10-30T10:17:01-03:00 complete kasegi round=47; hyaku-inline attempt=3`

## 2. Claim re-checks

Gate/evidence split: both claims rest on lane-owned frozen instruments (`corpus/instruments/r47-routed-defects.py`, `corpus/instruments/r47-f30-gate.py`). Per PROTOCOL §Gate standard (Closure consequence) this closure verified their **committed evidence** (selftest/mutation tallies, frozen-run verdict, revision measured) and additionally **re-measured** both claims with plain grep/wc/jq counts over committed bytes at the tip. No sibling gate was executed by this closure.

### C1 — depth:verifiability (11 mechanical limbs of round-46 routed defects D5–D8) — evidence-verified, claim not fully verified (as the lane itself reports)

- Committed frozen-run receipt `.ufo/waves/round-47/controls/final-measure.txt` stamps `measured-at-rev: f0809bcaefe9f2b576d6e4d7a0d2ed43ebae214d` and prints `routed-defects total=11 fixed=11 unresolved=0 exit=0`, matching the report's after-line `total=11 fixed=11 unresolved=0 exit=0`. Base replay `controls/freeze-check.txt` and `w1/R47ExecGateReplay.md` reproduce the declared before-line `total=11 fixed=0 unresolved=11 exit=1` on the base export.
- Self-test evidence: pre-freeze 43-case tree-probe suite green (`controls/selftest-receipt.txt`); mutation battery 35+6 C1 mutants with 16+4 disclosed survivors (`controls/mutbat-receipt.txt`, `w1/R47MutC1b.md`) — disclosed as coverage gaps, never claimed as equivalence. B3 red-before witness `w1/R47RevD7.receipts.txt` (`records=3 bound=3` vs `bound=2 unbound=1`) grounds the refusal of the frozen `mined→rejected` limb and QUALITY R54.
- Revision nuance: `f0809bca→77551628781a` touches only `corpus/lessons/round-47.md` (+14 append-only lines). The only limb reading that file (L7, dropped-findings-named) still passes at the tip — my own greps below re-derive the limbs at `77551628781a`:
  - `grep -c 'to append' corpus/SOURCES.md` → 0 (base 2)
  - `grep -c '^```' corpus/SOURCES.md` → 0 (base 4)
  - `grep -c 'all 42 lines are body prose' corpus/knowledge/github-repository-security-advisories.md` → 0 (base 1)
  - `grep -c 'S074.txt:' corpus/knowledge/github-repository-security-advisories.md` → 0 matching lines (base 54 lines / 59 occurrences)
  - `wc -l corpus/knowledge/github-repository-security-advisories.md` → 145 (unchanged layout)
  - S076 row present at `corpus/SOURCES.md:82` opening `supersedes S074 —`; Search log round-47 bullet at `:117`; REST-API Leads bullet at `:124`; S074 used-by old→new logged at `:176`; landed bullets verified in `## Search log` / `## Registry changes`.
- Claim verdict: the frozen after-state is **not fully met** — the lane refused the harmful S074 `mined→rejected` limb (correctly; see B3 witness) and the plain expression `grep -c 'supersedes S074'` reads 2 against frozen target 1 (second match is prose in the Registry-changes bullet at `:175`), plus disclosed wave-1 false-green counterexamples (`w1/R47RevCounterC1.md`). No frozen byte was rewritten after scoring. The refusal is the honest, evidence-backed act; C1 is not admitted.

### C2 — coverage (F30 ZDI broker-policy frontier) — evidence-verified unmet, re-measured

- Committed receipt `controls/final-measure.txt` prints `f30-gate fixed=6/7 exit=1` with `H1 pass=0 read=rows=29` — matching the report's `1/7 → 6/7, exit 1` and the declared `expect_after fixed=7/7 exit=0`.
- Plain re-measurement at the tip (my own runs):
  - `grep -cE '^\| F[0-9]+ \|' corpus/README.md` → **29** (target 30 — unmet)
  - `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → **76** (74→76)
  - `find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l` → **67** (66→67)
  - `grep -rliE 'zero day initiative|zerodayinitiative' corpus/knowledge corpus/SOURCES.md corpus/README.md | wc -l` → **2** (entry + SOURCES row; no README admission block — consistent with the honest stop, target ≥3 not reached)
  - `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → EXIT=0, warnings W04 S028/S029/S072/S076 (S076's duplicate URL is the same-document supersede, warning-only like the S072/S070 precedent).
- Claim verdict: **unmet** — the frontier stays 29; the ZDI policy is admitted as sourced F02 enrichment (`corpus/knowledge/zdi-disclosure-policy.md`, provenance trio cites S075), not a new F30 row. The target was not narrowed after scoring; the miss is reported as a miss.

### No-harm

`git diff d8dfbcbf 77551628781a -- SCORECARD.md` is append-only (+23 lines: a Round 47 result section); scores held depth:verifiability 4, coverage 8, depth:density 9 — no score moved, no promotion claimed. `PROVINCE.md` unchanged in the round diff. The non-target density-proxy regression SKILL mean 275.1→273.6 (34→35 blocks; `controls/density-base.txt` before-receipt matches) is disclosed in the report and SCORECARD, not reformatted away or called a no-harm pass. Protected registry cells: wave-2 receipt `w2/R47W2RegistryCells.md` reports 813 original cells unchanged; my S074-row read shows only the permitted used-by cell changed, status/recheck untouched, old→new logged in the lesson.

## 3. Per-axis verdicts (closure)

| Axis | Grade | Basis |
|---|---|---|
| depth:verifiability | **improved** | All 11 mechanical D5–D8 limbs verified closed at the tip (receipt + this closure's plain re-derivations); three false F29 sentences gone; provenance made reproducible via committed-instrument re-capture (S076). The frozen claim C1 still does not verify (refused harmful limb; plain target 2≠1), so nothing is admitted on this axis; the score stays 4. |
| coverage | **unchanged** | C2 unmet: frontier 29→29, no F30; score stays 8. ZDI enrichment is real but sits on F02-held ground. |
| depth:density | **unchanged** | Score stays 9; proxy mean regressed 275.1→273.6 from the required registry block — disclosed, no claim, no harm grading beyond the disclosure. |

## 4. Discernment spot-check (LEARNING.md — Discernment is checked from outside)

Sampled the round's own `corpus/lessons/round-47.md` `## Gate`/`## Final Gate decisions`: two admits and one reject re-opened end to end.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S076 admit (reproducible re-capture superseding S074) | admit | Live URL https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories → HTTP 200; committed snapshot `corpus/source-snapshots/round-47/S076.txt` sha256 = `9bd8ab57…bbb38` (matches row/manifest/lesson); quotes at :582 ("GitHub is a CVE Numbering Authority (CNA)…") and :598 ("wait to disclose the issue when the fix is ready") verbatim at their anchors | **agree** | D7's provenance gap is real (no committed producer of the 42-line capture) and the supersede-without-rewrite form follows CORPUS rule 2; S074's historical capture is preserved, only permitted cells change. |
| S075 admit (ZDI policy as F02 enrichment) | admit | Live URL https://www.zerodayinitiative.com/advisories/disclosure_policy/ → HTTP 200; snapshot sha256 = `9dee8161…04e1` matches; L23–26 carry exactly the cited facts (15-business-day fallback, 120-day window with unnamed start event, sole-discretion rare extensions, 30/60/90 faulty-patch tiers, never-kept-quiet) | **agree** | Row teaches is grounded (19-word quote from L26); scope honestly limited to the policy text; tier-A docs on first-party policy text. |
| F30 reject (no independent frontier row) | reject | Same S075 source, plus `corpus/README.md` F02 row (`Coordinated-disclosure timelines`, S003–S005) and F12 (compares coordinator timelines against F02) | **agree** | The ZDI deadline rule instantiates the surface class F02 already holds (coordinator disclosure timelines); a new number would not add ground. Flip condition (independently scoped uncovered surface) is stated and sound. |

New-row quote check: every located Gate quote in the lesson is ≤25 words and found verbatim at its cited line in the committed snapshots; the two new SOURCES rows carry URL, tier, anchor-with-revision, ≤25-word grounded teaches, ISO opened/recheck, and used-by. Registry census (this closure's own run): EXIT=0 with the four disclosed W04 duplicate-URL warnings.

## 5. Trend verdicts (closure)

- **expansion: unchanged** — frontier 29→29, no new admitted surface; SOURCES 74→76 and knowledge 66→67 are enrichment/supersede on covered ground (F02 case, F29 successor). Matches the lane's verdict; evidence in §2.
- **quality: improved** — false sentences corrected in place at unchanged layout, drafting scaffold landed in real sections, provenance made reproducible, and every counter/selftest limitation, false green, dead seat and proxy regression disclosed rather than hidden. This closure found no remaining false phrase by its own greps. Matches the lane's verdict.
- **discernment: improved** — the outside check the lane flagged as outstanding is now on record: this non-author closure agrees with the gate on the sampled admits (S075, S076) and the sampled reject (F30); the round-46 disagreements were learned as M47-1…M47-4 and grounded QUALITY R54 (verified present at `corpus/QUALITY.md:401`). LEARNING.md's improved condition (spot-check agrees on admits and rejects; disagreements become lessons) is met for this round's sampled decisions. The lane's own `unchanged` was written before any outside check existed; this closure's grade supersedes it with evidence.

## 6. Routed defects and operator notes

Routed to the lane (fix next round; corrections append, never rewrite):

- **R1 — SHONEN.md canonical-form drift.** The file now carries 13 accumulated per-round assessment blocks (52 `- [~]` lines) against the canonical form (seed verbatim + marks confined to the box character plus one indented evidence line per box, no other prose). Predates this round — every historical block is earlier rounds' work — but this round appended one more (+7 lines). Route: keep per-round SHONEN assessments in the reports (they are already there), restore SHONEN.md toward the canonical seed shape, or record the fleet-sanctioned convention explicitly.
- **R2 — plain-target phrasing.** `supersedes S074` frozen target 1 matches 2 lines because the second match is prose in a Registry-changes bullet. Disclosed by the lane; frozen targets stay unrepaired. Future frozen plain expressions should anchor to row form (`^\| S[0-9]+ \|.*supersedes`) so prose cannot meet the target.

Operator notes (not lane debt):

- The five wave-1 dead seats carry empty final payload and no terminal status/last error in `wave1-results.json`; the report honestly declines to invent zero deaths. The seat-death reporting duty needs the handoff format to carry terminal status — orchestrator-side.
- `final-measure.txt` self-stamps `measured-at-rev: f0809bca` while the tip is `77551628781a`; the delta is +14 append-only lesson lines, and this closure re-derived the limbs at the tip. Keep the wording exact (same class as the round-46 observation).
- The pre-report landing-gate transcript ran at `29c02f99`, not at the later receipt-only tip; the report discloses exactly that, and push state is independently proven (`jj-lane.sh state` ahead=0; local=remote=`77551628781a`).
- L0 open question about the 22 gated historical rechecks remains unanswered and was routed around, not treated as answered.
- SHONEN boxes 1, 3 and 4 look fully checkable by a non-author on the current evidence (decision tables/error patterns/checklists with resolvable sources; rechecks execute at the declared root 67/67; PROVINCE unchanged, no absorption). Box 2 (end-to-end domain task) still has no executed end-to-end item — the lane claims none, honestly. Promotion remains operator-owned.

Closure verdict: **rejected-honest-stop** — C1 not fully verified (refused harmful limb, disclosed misses), C2 unmet (6/7, frontier 29), no axis harmed, honest stop confirmed.
