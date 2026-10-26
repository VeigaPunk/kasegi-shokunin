# ConnPatterns — F20 (SSVC) cross-reference proposal (round 37, coverage connector)

Seat: leaf connector (`ConnPatterns`), no subagent dispatch. Receipt only — no lane, fleet, sibling-lane or
source-tree file written except this receipt; no mutating git command. Lane HEAD observed `b362068195d5489aa94b31e6ec8f880c367e0ba0`
(read-only); frozen claims `224df74d`; erratum-1 (`b362068`) steers the S054 capture URL to the overview tutorial page.
Tooling installed: none (only `read`/`grep`/`bash` read-only inspection). Scratch dir
`/fast/scratch/hyaku/kasegi-r37/ConnPatterns/` created but unused; removed before yield.

## 1. What was read (evidence base)

- F13 `corpus/knowledge/program-severity-ladders-and-reward-scales.md` (S043/S044/S045; VRT "suggested baseline
  technical severity", S044.txt:33; P1–P5 ladder with override).
- F17 `corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md` (S051; five levels "finalizes them largely
  by the impact that they cause", S051.txt:52; `CVSS` occurs 0 times in that capture).
- F18 `corpus/knowledge/cisa-kev-catalog.md` (S052; no severity field, Claim 5; Claim 6 prices the F13/F17 boundary:
  "F13 holds platform reward ladders and F17 a Web3 impact ladder … this feed carries membership plus a deadline").
- F19 `corpus/knowledge/epss-exploit-prediction-scoring.md` (S053; 0–1 probability / 30-day horizon L216; "combine
  EPSS with CVSS and KEV" L224; rejected-overgeneralization 8 draws the F13/F17 payout boundary).
- F01 `corpus/knowledge/cvss-v4-severity-and-vector.md` (S001/S002; rule: "do not present that score alone as a
  complete risk assessment, program severity decision, or reward decision").
- F14/F15/F16 ground labels (`japanese-severity-vocabulary-and-impact-model.md`, `vendor-third-party-finding-coordination.md`,
  `chinese-crowdsourced-testing-scope-and-rewards.md`) for the optional tier.
- `SKILL.md` "Frontier decision table (round 22)" (lines 1024–1032, five rows F01/F03/F04/F05/F02 situations) and
  "## Finding-triage decision table" (line 134 — mission claim-state triage, not vulnerability prioritization; no
  SSVC hook belongs there).
- Sibling wave receipts: `ScoutF20Open.md` (overview capture sha256 `ff3f3b2c…`, 518 lines, quote candidates),
  `ExecC2QuoteOnce.md`/`ExecC2Capture.md` (four manifest pins Q1–Q4 at L247/L259/L277/L367),
  `ScribeEntryF20.md` (84-line entry draft incl. a "Sources overlap — SSVC against KEV catalog status (F18) and
  EPSS likelihood (F19)" section), `RevEntryF20.md` (Q1–Q6 plan review), `claims-erratum-1.md` (URL correction).
- Precedent check: `grep -n 'F18\|F19\|F20' SKILL.md` → **0 hits**; SKILL.md carries an F13 admission note only —
  admissions F14/F16/F18/F19 did not append SKILL.md rows.

## 2. Capture-grounded hooks the cross-references can hang on (overview pin, sha256 ff3f3b2c…)

All verified across three independent seat captures (ScoutF20Open, ScribeEntryF20, RevEntryF20 — identical digest):

- L247 contrast sentence: SSVC rates "risk to the concerned stakeholder", unlike systems rating "technical severity
  (how bad it could be …)" or "exploitability (how likely it is that there will be an exploit)".
- L93–L94 nav rows: "EPSS Probability as input to Exploitation", "EPSS Percentiles as an Amplifier".
- L153 nav row: "In KEV" under "CISA-based decision points" (L150–L152).
- L69–L70 nav rows: "CVSS v4 Analyst Models"; L156–L157: "CVSS-based decision points" — CVSS appears only as input
  branches; `score` occurs 0 times in the capture (FC-2 of the draft).
- L259+L261–L266: output is priority categories "in increasing order of priority", offered "as examples";
  categories "reflect the timeliness of action to be taken".
- L255/L257: Supplier/Deployer/Coordinator roles; decisions differ per stakeholder; roles not exhaustive.
- L463–L467: coordinator publication table reuses the Exploitation decision point; active exploitation → CERT/CC
  "more likely to publish".
- Gap (recorded by ScoutF20Open §5): BOD 26-04 response-model content (InKEV/Publicly Exposed/Automatable/Technical
  Impact → FSU/60D/14D/3D/3DF) lives on a *different* URL (`/howto/cisa_response/`), not on the pinned page — any
  cross-reference phrasing must not claim it from S054.

## 3. Proposed move (one bounded proposal)

### 3a. Cross-reference list the F20 entry should carry

The draft's "Sources overlap" section already covers F18 and F19. Keep those, and extend the same section with the
lane's severity-axis family and the coordinator role — every item hangs on a capture anchor already quoted in the
draft, so no new manifest pins are needed:

1. **F19 EPSS — keep (already drafted).** Exploitation decision point values None/Public PoC/Active (L289/L292/L295)
   consume exploitation evidence; the site routes EPSS as "input to Exploitation" (L93–L94). F19 holds the lane's
   likelihood definition (S053 L216).
2. **F18 KEV — keep (already drafted), plus one strengthening clause.** "In KEV" is a named CISA-based decision point
   (L153). Add: F18's README row records BOD 26-04 using KEV status as one of four risk-priority factors (public
   exposure, KEV status, automatability, technical impact) — the same four factors a CISA response model turns into
   decision points (content on a separate, uncaptured page per ScoutF20Open §5; phrase via F18's row only, never as
   an S054 claim).
3. **F01 CVSS — ADD.** The contrast sentence (L247) names the "technical severity" axis; the lane's F01 entry is that
   axis (`cvss-v4-severity-and-vector.md`, S001/S002), and its own rule already warns that CVSS-B alone is "not a
   complete risk assessment". Suggested one-sentence form: *"For the technical-severity axis SSVC explicitly does not
   rate, see F01 (`corpus/knowledge/cvss-v4-severity-and-vector.md`, S001/S002); the page's navigation lists CVSS
   only as input model branches (L69–L70, L156–L157), never as an SSVC output."*
4. **F13 program severity ladders — ADD.** The VRT is a platform's "suggested baseline technical severity"
   (S044.txt:33) — the program-side one-size-fits-all rating SSVC's stakeholder-specific model contrasts with; and
   SSVC's Defer→Immediate categories order timeliness of action (L259–L266), not payouts — the same not-a-payout-ladder
   boundary F18 and F19 already draw against F13/F17. Suggested form: *"F13's suggested-baseline ladders (S043–S045)
   price and band technical severity per program; SSVC orders a stakeholder's action instead — see F13 for the
   program-ladder side of that boundary."*
5. **F17 Immunefi VSCS — ADD.** The lane's other impact-fixed technical classifier ("finalizes them largely by the
   impact that they cause", S051.txt:52); like CVSS it sits on the "how bad it could be" axis. One clause: *"F17's
   per-asset-class impact ladder (S051) is the Web3 member of the same severity-axis family SSVC does not rate."*
6. **F15 coordinator intake route — OPTIONAL one clause.** SSVC's third role is the Coordinator, with triage and
   publication decision models (L269–L275) and CERT/CC's own publication rule (L467); F15
   (`vendor-third-party-finding-coordination.md`, S048) is the lane's coordinator-side entry. Include only if the
   line budget allows.
7. **F14 Japanese severity vocabulary — OPTIONAL, not proposed by default.** Its priority derivation is CVSS-vocabulary
   translation (P-guideline steps), a different severity→priority route; mentioning it adds a third severity-family
   pointer without a capture hook on S054. Leave to the L1.

### 3b. SKILL.md appended line (append-only, R6-compliant)

Precedent: F14/F16/F18/F19 admissions appended **no** SKILL.md rows, and the Frontier decision table (round 22) still
ends at its five original rows. But the table's F01 row already gestures at exactly this gap ("CVSS-B alone is
severity, not a complete risk assessment") and the SSVC entry is the lane's instrument for the missing side. One
appended row closes the loop without touching any existing line:

```
| A severity or likelihood number is asked to stand in for a prioritization decision | Rate risk to the concerned stakeholder instead: SSVC's output is a priority category (timeliness of action), with CVSS severity (F01) and EPSS likelihood (F19) as decision-point inputs, not the decision. | `corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md` | S054 |
```

Plus an optional one-line note under the table in the established style ("Round-37 note (appended 2026-10-26): …"),
mirroring the round-28 note shape. If the L1 holds the F14+ precedent (SKILL.md untouched at admission), the row can
be deferred to a later round without harming C2 — the entry's own cross-references carry the coverage gain.

### 3c. README frontier "next" cell suggestion (for `ScribeFrontierAmendments`)

*"(F20) SSVC rates risk to the concerned stakeholder, not technical severity (F01) or exploitability (F19); KEV
status (F18) and EPSS (F19) feed decision points such as Exploitation and In KEV; the output is a stakeholder-specific
priority category, not a score or a payout tier (F13/F17)."*

## 4. Affected axes and harm check

- **coverage (C2) — improved.** The F20 entry gains the full axis-family cross-links (F01/F13/F17 alongside the
  drafted F18/F19), matching the seat item's example shape ("F19 for EPSS likelihood; F18 for KEV status; F01 for
  CVSS severity") and the corpus's established cross-link conventions (F17's "What this adds beyond F13 and F15";
  F18 Claim 6; F19 rejected-overgeneralization 8).
- **depth:density — improved (small).** The SKILL.md appended row adds one cited-path instance to an existing block;
  the F20 entry's added sentences cite existing lane entries, raising cross-citation density without new files.
- **depth:verifiability (C1) — untouched.** No instrument change; the closure suite's E-checks do not read the
  F20 entry's prose, only structural/registry/manifest facts. Every proposed reference hangs on anchors already in
  the draft's FC list (L69–L70, L93–L94, L150–L153, L156–L157, L247, L259–L266) — no new manifest quotes required.

## 5. Risks

- **Line budget.** The draft is 84 lines (budget 60–100). Items 3–5 add ~4–6 lines inside the existing
  "Sources overlap" section; item 6 only if under budget. Risk: low; the section grows, not the skeleton.
- **Capture-safety.** Item 2's BOD 26-04 clause must stay phrased via F18's README row; claiming the how-to page's
  four-outcome content from S054 would overreach the single pinned URL (ScoutF20Open §5 gap). The suggested wording
  avoids it.
- **Precedent drift.** SKILL.md rows at admission stopped after F13; the proposed row is a deliberate, named
  exception (the F01 row's "not a complete risk assessment" clause is the hook). Flagged so the L1 can defer it
  without blocking the entry.

## 6. Verification performed

- All four neighbouring entries (F13/F17/F18/F19) and F01 re-read at HEAD; quotes above are their committed bytes.
- Overview-capture anchors (L69–L70, L93–L94, L150–L153, L156–L157, L247, L255, L257, L259–L266, L463–L467) match
  across `ScoutF20Open.md`, `ScribeEntryF20.md` §3 and `RevEntryF20.md` — three independent fetches, identical
  sha256 `ff3f3b2c…fdce21`.
- `grep -n 'F18\|F19\|F20' SKILL.md` → 0 (precedent); Frontier decision table located at `SKILL.md:1024–1032`;
  "Finding-triage decision table" at `SKILL.md:134` confirmed to be mission claim-state triage (no SSVC hook fits there).
- F01 rule sentence ("do not present that score alone as a complete risk assessment…") quoted from
  `corpus/knowledge/cvss-v4-severity-and-vector.md:7-8`.

Report: .ufo/waves/round-37/wave1/ConnPatterns.md
