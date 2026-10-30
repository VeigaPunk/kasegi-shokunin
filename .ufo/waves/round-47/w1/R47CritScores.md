# R47CritScores — held-score attack

Axes: **depth:verifiability**, **coverage**. Read-only criticism; no scoring, admission, integration or canonical judgment performed.

## Findings

### 1. Defect closure is not promotion-limb closure

**Counterexample:** even a genuine C1 `fixed=11/11` leaves the first promotion limb unsatisfied if `gated=22`; even `gated=0` alone would leave the independent audit limb unsatisfied. `SCORECARD.md:1538-1541` explicitly requires **both** at the judged head: zero gated rechecks, and a non-author audit passing 25/25 source chains **and zero unsupported current claims**. The original threshold at `SCORECARD.md:331` agrees. A side-by-side audit of corrected F29 sentences is not automatically that 25-chain audit.

Observed prework receipt: `.ufo/waves/round-47/controls/recheck-audit-before.txt:1-5` prints `strict pass=66/66`, `executes=44 gated=22 broken=0`, and exit 0. Thus a green strict audit already coexists with 22 gated lines; exit 0 cannot substitute for the score-5 condition. The round-46 result explicitly distinguished measured improvement (24 → 22) from a completed promotion limb (`SCORECARD.md:1782,1788`). C1's frozen outcome instead repairs D5–D8 provenance (`claims.json:13`), not those 22 source chains.

**Smallest safe correction:** retain the distinction: “4 held; routed-defect closure measured [actual receipt]; score-5 gap: [actual judged-head gated count] to zero; independent 25/25-chain/zero-unsupported audit not established.” Do not say no *measurement* improved merely because no scalar promotion occurred. Conversely, avoid the ambiguous “both limbs move”: the criterion requires both **satisfied**, not just both improved.

### 2. Expansion and ratio improvement are different quantities

**Counterexample against demanding a coverage increase:** with no queued rows and every frontier row admitted, the do-nothing state has `(20+29)/(20+29)=49/49=1.000`; the intended F30 state has `50/50=1.000`. The extra row changes the enumerated breadth, not the ratio. These are arithmetic derivations from the recorded base and proposed target, **not newly executed measurements**.

Evidence: `SCORECARD.md:1551` includes queued registry rows in `F_total` and requires every admitted entry's frontier recheck to pass. `:1553` explicitly rejects the frontier-only tautology as discriminating 7 from 8. `:1789` records queued=0, no written 8 → 9 criterion, and the unchanged operator-owned 0/18 surfaces. Round 45, round 46 and round 46a2 consistently call +1 row an expansion count rather than a coverage-ratio move (`:1748,1783,1824`). Frozen C2 preserves that reading (`claims.json:37`).

**Smallest safe correction:** report 29 → 30 as an admission/expansion count only after substantive F02/F15 overlap review and the frozen kill rule; retain coverage 8 without inventing an 8 → 9 threshold. Recompute queued and non-admitted counts and all-entry rechecks at the judged head before asserting the ratio stays 1.000. A new number alone does not establish genuinely new research coverage.

### 3. Fixable draft omission: explicit distance evidence

The scoped scorecard draft correctly marks its after-values pending (`w1/R47SrScorecard.md:7,15,19-20`), but its insertion lacks an explicit current gap computation. `corpus/QUALITY.md:249` (R26) requires a read-only gap computation cited in the round lesson, not only “improved, held.”

**Smallest safe correction:** the L1's final filing should cite the judged-head `score-gap.py`/recheck receipt, state the separate audit status, and report coverage's held ratio plus absent 8 → 9 criterion. A closure may properly demand this evidence or reject unsupported frozen-claim success; it should not demand a scalar increase from these changes alone. Whether a held increment meets the canonical quality trend remains the canonical judge's decision, not this seat's.

## Do-nothing discrimination and limits

Named do-nothing controls are `controls/c1-base.txt:12-13` (`fixed=0/11`, exit 1) and `controls/c2-base.txt:1,8-9` (29 admitted, `fixed=1/7`, exit 1), replayed in `controls/freeze-check.txt:1-4` (`base_ok=2`). They distinguish the proposed artifact changes from doing nothing, while **the held scalar scores do not**. That is legitimate measurement granularity, not proof of promotion or admission.

Existing receipts were inspected; no counter, audit, full battery, browser or alternate runtime was invoked. No integrated round-47 result was verified. The 34 disclosed mutation survivors remain gaps (`controls/freeze-controls.txt:3`); “held — measured” must not conceal a failed kill rule or imply “held; verified” (QUALITY R38 at `corpus/QUALITY.md:337`). No scratch was created, so none remains. No tool installs, git/jj mutations or shared-production writes.

Self-evaluation: accuracy 4/5 (judged-head outcomes unobserved); completeness 4/5 (score semantics covered, canonical trend deliberately not judged); clarity 4/5 (measurement versus promotion separated); actionability 4/5 (specific filing correction and receipt named); conciseness 4/5 (evidence qualification adds necessary length). Overall 4.0/5. Priority: bind final gap evidence before filing. User-agreement check: this answers the assigned score challenge without manufacturing a score move.
