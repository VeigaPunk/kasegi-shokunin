# QUALITY.md — round-35 fixture payload (not the lane record)

Committed test fixture for the C1 closure check D7. The live record is `corpus/QUALITY.md`; this file
pins the R22/R23 rows and the appended supersession rows the check reads.

| id | criterion | grounded in |
|---|---|---|
| R22 | A frozen claim predicate is checked for satisfiability against base bytes before freeze: every literal constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze erratum. | `corpus/lessons/round-33-verifier-spotcheck.md:167-169` (R2 — the frozen parenthetical that literally read `bound=38`); M34-2 at `.ufo/waves/round-34/claims.json` |
| R23 | A lane records an event-driven reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing the considerthese file and date. | `considerthese/2026-10-25.md:76` proposal 6 (2026-10-25) |
<!-- limb D7 fixed: appended supersession rows for R22 and R23 exist -->
| R27 | (round 35) A record row's grounding cell is corrected by an appended supersession row that names the wrong grounding it replaces and the mistake it should have named. | supersedes R22 — the row named M34-2 as its grounding; the grounding is M34-3 (`corpus/lessons/round-34.md` open item 10, `.ufo/waves/round-34/mistakes-erratum-1.md`). |
| R28 | (round 35) A record row grounded in a proposal file is re-grounded on the round lesson that mined the proposal. | supersedes R23 — the grounded-in cell cited `considerthese/2026-10-25.md:76`; the grounding is the round-34 lesson §considerthese (`corpus/lessons/round-34.md`). |
