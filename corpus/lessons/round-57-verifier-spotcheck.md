# Round 57 verifier spot-check — kasegi (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-03 from fleet root /home/vgpnk/Projects/shokunin. Lane HEAD before the round
`eae1d614542e8d30d77e9f4e8b9dea6a11aad138`, after `e300ad5c5bfc30f1170044d5cfd992102da9b695`
(branch `master`). I did not author this round; I re-checked its committed bytes and re-opened
its sources. I did not execute the lane's gates beyond plain byte counts; their verdicts are
evidence-verified from the committed receipts.

## Step-1 conformance

- Report committed in the fleet repo by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-57/kasegi.md`
  → `kasegi-shokunin <kasegi@shokunin.local> 072105c1cce817cf12fb92bb065cb7a7639f58e3` (subject `round-57: kasegi report`). PASS.
- `## SHONEN` heading present, exactly one (`grep -c '^## SHONEN'` → 1), one line per canonical box
  (`[~]`, `[ ]`, `[~]`, `[~]`, each with a pointer); no `[x]` written. PASS. `SHONEN.md` itself is
  byte-unchanged base→tip (`git diff eae1d614… e300ad5c… -- SHONEN.md` → 0 lines). PASS.
- Cited lane commits exist and are ancestors of the branch ref: `git merge-base --is-ancestor <h> master`
  → OK for `6343e2c3882a96b1af86e1ecf4c9deba33361719` (freeze), `cd3029876eac7189aaff0d32b26031c0defa35aa`
  (implementation), `e300ad5c5bfc30f1170044d5cfd992102da9b695` (results), and the base `eae1d614…`. All
  carry the lane identity. PASS.
- Lane repo pushed and clean: `scripts/hyaku/jj-lane.sh state …` → `branch=master local=e300ad5c… remote=e300ad5c… ahead=0 behind=0`;
  `git status --porcelain` → only `?? .ufo/waves/round-57/w1.ready.dispatched` (the orchestrator dispatcher's
  rename of the `.ready` handoff marker, driver-side, not lane round work). PASS.
- Dispatch evidence: watchdog.log lines `2026-11-03T14:54:06-03:00 launch kasegi round=57 pgid=1998487 driver=hyaku-inline attempt=1`
  and `2026-11-03T17:23:39-03:00 complete kasegi round=57; hyaku-inline attempt=1` (lines 2064, 2086). Digest copied to the MANIFEST notes.
- Prompt fidelity: `templates/round-prompt.md` rendered with lane/round/fleet-root/axes substitutions diffs
  against `.ufo/prompts/kasegi-round-57.md` lines 1–140 only at line 1 (`<kasegi-repo>` placeholder written
  as the concrete repo path — a rendering improvement) and the trailing newline; §6 is the hyaku addendum.
  Round-level items (mission/axes binding, ≥8 L2 in one batched call, commit-then-push, push scope, L0)
  and the five child-lane items (report path, commit-before-report ordering, SHONEN heading, commit-hash
  citation, write scope) all carried. The quoted L2 floor (≥8) matches `MISSION.md` §L2 concurrency. PASS.
- Marker rule: the report names real committed work (three hashes, receipts, wave evidence) — a report,
  not a marker. Status `ok`.

## Claim re-checks

Commands run by this verifier over committed bytes; lane-gate verdict lines read from the committed
receipts only (never re-executed).

### C1 — depth:verifiability (figure-audit ledger 27 → 35 + host-portable `fail-entry-records` derive) — VERIFIED

- `git show eae1d614…:corpus/instruments/figure-audit-ledger.json | grep -c '"id"'` → **27**; same at tip → **35**. Matches.
- Before (evidence-verified, `controls/do-nothing-c1-r57.txt`): `FIGURE-AUDIT figures=27 ok=26 stale=1 exit=1`, exit 1 — the red
  before-state the claim repairs, measured at base before any C1 byte.
- After (evidence-verified, `controls/gate-final-r57.txt`): `FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0`.
- Self-test tally (evidence-verified, both receipts): `selftest cases=5 failures=0`, exit 0.
- Red controls (evidence-verified, `controls/c1-red-r57.txt`): red 1 wrong-want and red 2 mutated r53 receipt
  (`FAIL_entry_records=34` vs want 33) each print `stale` and exit 1; R30 hardening receipt
  (`controls/r30-hardening-r57.txt`): missing-object red reads `derived=UNAVAILABLE reason=derive-exit-128 stale`, exit 1 —
  the repair is shown able to fail. Frozen predicate + kill rules committed at the freeze commit
  (`.ufo/waves/round-57/claims.json`, `frozen_at 2026-11-03T18:15:00Z`, before implementation). Score held 4 is the declared
  R58-nominal label, not a claim failure.

### C2 — coverage (frontier F38 on S089 + S090) — VERIFIED

- `git show eae1d614…:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → **88**; tip → **90**. Matches.
- Frontier delta re-measured independently: `grep -cE '^\| F[0-9]+' corpus/README.md` at base → 39, tip → 40 (+1, one new row);
  the lane's own counter reads rows 37 → 38 (its pattern excludes two non-frontier F-lines my grep sweeps); delta agrees.
- Knowledge: `git ls-tree -r --name-only <rev> corpus/knowledge/ | grep -c '\.md$'` 75 → **76**; expected list
  `grep -c '^corpus/knowledge/' corpus/instruments/knowledge-expected.txt` 75 → **76**; the new file
  `corpus/knowledge/iso-29147-30111-standard-records.md` opens with the provenance trio (`source:`, `recheck:` verified; 4 lines).
- Counter verdicts (evidence-verified, receipts): before `FRONTIER-CENSUS rows=37 admitted=37 closed=37 problem-rows=0 registry=88`,
  `entries=40 pass=40` (`do-nothing-c2-r57.txt`); after `rows=38 admitted=38 closed=38 problem-rows=0 registry=90`,
  `FRONTIER-PASS F38 ids=S089,S090`, `entries=41 pass=41 exit=0` (`gate-final-r57.txt`).
- Capture binding: `records=71 bound=71 unbound=0` (pure base, do-nothing receipt) → `records=73 bound=73 unbound=0` (gate-final). Matches.
- Capture digests re-measured: `sha256sum corpus/source-snapshots/round-57/S089.txt S090.txt` → `17ee9c4191ca…ebb0e1dd`,
  `2074d3a1b89f…4a6c2976a` — equal to the SOURCES rows, the Gate, and the manifest; sizes 6647 / 5598 bytes. Matches.
- Score held 8 (operator-owned denominator); the moved measure (frontier 37 → 38) verifies.

### Axis harm

`git diff eae1d614… e300ad5c… -- SCORECARD.md` is a pure EOF append (round-57 section + move log): depth:verifiability 4 → 4 held,
coverage 8 → 8 held, depth:density 9 → 9 held (SKILL.md untouched — verified: no SKILL.md path in the round's three commits'
name-only diffs), calibration improved verdict row. No owned axis harmed.

## Spot-check table (LEARNING.md — at least one admit and one reject)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S089 → F38 admit | admit (tier A, mined) | live `https://www.iso.org/standard/72311.html`, curl with the instrument's UA → HTTP 200, 88964 bytes (equal to the recorded fetch); quote lines re-read in the committed capture | **agree** | Both pinned quotes found in the live page: the abstract scope sentence (capture L84) and the applicability sentence (L92, 22 words); `AWI 29147` successor state present; `confirmed in&nbsp;2024` present in the raw HTML (the capture's L64 "confirmed in 2024" is the declared `&nbsp;`→space conversion). Byte-identical fetch size. The publisher-record scope (identity/stage/currency/abstract/applicability, normative text excluded) is exactly what the page holds. |
| S090 → F38 admit | admit (tier A, mined) | live `https://www.iso.org/standard/69725.html` → HTTP 200, 87845 bytes (equal to recorded); capture lines re-read | **agree** | Abstract scope sentence at L84 and applicability L85 present; `confirmed in&nbsp;2025` in raw HTML (capture L64); "A standard is reviewed every 5 years" at L109; `WD 30111.2` development state present. Row's scope note correctly excludes handler workflows (F12) and the 29147 record. |
| S089 row quote discipline | ≤25-word located quotes | capture L92 re-counted with `wc -w` | **agree** | Q4 re-measures at 22 words; the lesson's stated max (22) holds; anchors resolve at the cited lines. |
| Store prices (CHF 179 / 135) | rejected — "store state, not asserted" | live pages re-opened; `grep -n 'CHF\|179\|135'` over the captures finds the prices at L77–78 | **agree** | The prices are present in the served page but are dynamic store state; refusing to admit them as record facts is correct curation, and the rejection is kept with a reason in the Gate. |
| Successor drafts (AWI 29147, WD 30111.2), French/OBP pages | rejected / deferred — "named as development states, never opened", leads not rows | live pages re-opened (successor names found); CORPUS.md rule 1 | **agree** | A row is written only after opening the source; the lane named them without opening them and wrote no rows. Correct.

## Per-axis verdicts (this verifier)

| axis | verdict | basis |
|---|---|---|
| depth:verifiability | **improved** | Ledger 27 → 35 re-counted at both revs; red→green derive repair with two red controls plus the R30 missing-object red; frozen predicate committed before data. Nominal score label (R58) does not unmake the verified move. |
| coverage | **improved** | Registry 88 → 90 and frontier +1 re-counted; F38 is new ground (standards-body publisher records), SiblingOverlap class (a) none (`w1/SiblingOverlap.md`); both captures re-opened live by this verifier. |
| depth:density | **unchanged** | SKILL.md untouched (no SKILL.md path in the three round commits). |
| calibration | **improved** | M57-1…M57-9 mined with class/captured-by/fix; the host-bound derive class was measured red at base before repair; the wave's one counter disagreement became M57-4 + criterion R67, named open — not unlearned. |

## Trend verdicts (this verifier)

- **expansion: improved.** F38 admitted on uncovered ground (no held row covered ISO's own publisher records of 29147/30111 —
  the neighbor screen `controls/neighbor-screen-r57.txt` and the class-(a) overlap-none result), each new knowledge entry citing
  its mined S089/S090 rows; frontier 37 → 38; registry 88 → 90 (tier A 2).
- **quality: improved.** The two round-54 fail-open derives repaired with a red control; entry anchors corrected after the
  non-author table found them wrong; both captures reproduce; no admitted entry failed its re-check. Caveat carried honestly:
  the frozen C2 counter admits a stub body (M57-4, R67 named open) — a named-open counter limb, not an entry failure.
- **discernment: improved.** This outside spot-check agrees with the gate on both sampled admits and on the sampled rejections
  (prices, successor drafts); the wave's single disagreement is a lesson with a grounded criterion (R67), not an unlearned
  disagreement. Wave seats were lane-dispatched, so the outside check is this closure — it agrees.

## Routed defects (lane must address next round; status-neutral here)

1. **Stale carry-in line.** The report's Limits bullet says "DF-56-2 is operator-side (no L2-minimum item in the dispatched
   prompt)". The round-57 dispatched prompt DOES embed the L2-minimum item (§3 "at least 8 L2 subagents in ONE batched
   AgentSwarm call"; the r56 prompt carried "Helpers (optional, honest)" instead). DF-56-2 is resolved for round 57; next
   round's report should record it resolved instead of standing.
2. **CENSUS-FRESH=stale (exit 1) in the gate-final receipt.** Disclosed in Limits; cause is the two live-log range bases in
   `corpus/instruments/citation-survival.md` (M57-9 / R69). The sources-census.sh gate itself exits 0. Routed: land the R69
   pinned-range census rule in round 58 (L0 question already filed: `kasegi | round-57 | the census freshness gate…`).
3. **Self-named open instrument limbs** (kept on the lane's queue, re-flagged here): M57-4/R67 (C2 counter admits a stub body —
   counter amendment is a next-round frozen claim; closure check probe a2 exits 1); M57-6 (mutation survivors m4, m6);
   M57-8 (r54 red fixture re-runs the live counter); LedgerReplay F2 (`check_read_only` `;`-chain bypass; no derive writes
   today) and F4 (edge-policy divergence, text only).
4. Note for the operator: SHONEN boxes 1 and 3 are author-asserted `[~]` but look fully checkable by a non-author from
   committed bytes (decision tables/error patterns/checklists with resolvable sources; ExportReplay/LedgerReplay seat
   re-runs). Promotion verification is operator-owned; this lane is a candidate when the operator chooses to run it.

## Verdict

All declared claims verify on re-measurement or committed gate evidence; no owned axis is harmed.
**kasegi round 57: ok, admitted.** Spot-check: 5/5 agree.
