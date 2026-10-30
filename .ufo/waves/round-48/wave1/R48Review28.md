# R48Review28 — Score-attribution review: lowest depth 4 targeted, no 4→5 limbs, frontier 29 unchanged

- **Seat:** R48Review28 (UFO-FSD critic, leaf member; no subagent dispatch, no production edits, no git/jj mutation)
- **Round:** 48, wave 1 · **Lane:** kasegi-shokunin · **Axis judged:** depth:verifiability
- **Assignment:** review the round-48 score attribution — "lowest depth 4 targeted, no 4→5 promotion limbs achieved, coverage frontier 29 unchanged."
- **Frozen claim under review:** C1 (`claims.json` sha256 `b8022cdf…f31c69f2a345`, pin matches `freeze.txt`; base `903d47e13058982460f0d90c1c2b9c7c02680646`; freeze commit `3546f7089c224ac6c8adc68208b1e648bbf3e6a5`).
- **Rules read first:** `/home/vgpnk/.omp/agent/RULES.md` (tooling directive noted; **no installs** — git/coreutils/python3 only; host-wide pacman pause honored). Author-side form only; not promotion or semantic truth.
- **Round-47 routes:** R1 (SHONEN.md canonical-form drift, `corpus/lessons/round-47-verifier-spotcheck.md:85`) is the routed defect C1 closes; R2 (frozen plain-target phrasing, `:86`) read for context.
- Scratch `/fast/scratch/hyaku/kasegi-r48/R48Review28/` created; receipts saved there and embedded below; removed at exit.

## Verdict (up front)

All three score-attribution statements **verify** against independent read-only probes. No counterexample defeats them. The strongest available attack — that C1 "targets" the lowest depth axis only nominally — is a **disclosed tradeoff consistent with lane precedent**, not a rejectable defect. **No correction is required to the attribution.** One optional disclosure recommendation is named at the end.

## Bounded probes: exact command → expected → observed

| # | Probe | Expected (attribution) | Observed | Match |
|---|---|---|---|---|
| P1 | `python3 corpus/instruments/shonen-form.py --root .` | `canonical=1 finding=SF-CLEAN exit=0` (C1 after-state, landed tree) | `shonen-form canonical=1 finding=SF-CLEAN exit=0` | YES |
| P2 | `grep -cE '^\| F[0-9]+ \|' corpus/README.md` | 29 (frontier unchanged) | `29` | YES |
| P3 | `python3 corpus/instruments/r44-frontier-count.py --root . --expect 29` | `rows=29 admitted=29 exit=0` | `frontier rows=29 admitted=29` exit 0 | YES |
| P4 | `python3 corpus/instruments/recheck-audit.py --root . --quiet` | `gated=22` (limb "gated=0" not met; same as r46/r47) | `executes=45 gated=22 broken=0` | YES |
| P5 | `sha256sum .ufo/waves/round-48/controls/shonen-before.txt` | `596122c0…017e9c05` (kill_rule archive pin) | `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` | YES |
| P6 | `git diff --numstat 903d47e…..HEAD` | only SHONEN.md + controls/registry rows; SKILL/README/density untouched | SHONEN.md (5/349), LOG.md(+6), SOURCES.md(+2=S077), QUALITY.md(+6=R55), shonen-form.py(new), round-48.md(+24), `.ufo/waves/round-48/*`; SKILL.md/README/density.py absent | YES |
| P7 | `git diff 903d47e..HEAD -- corpus/README.md SKILL.md corpus/instruments/density.py` | empty (non-target guard) | empty diff | YES |
| P8 | `grep -c 'SHONEN' corpus/instruments/citation-survival.md` + `resolve.py` docstring | SHONEN.md not a depth:verifiability measured input | `0`; docstring L7 "`<root>/SKILL.md plus <root>/corpus/**/*.md`" | YES |

## Attribution check, statement by statement

**1. "Lowest depth 4 targeted" — CONFIRMED (nominal, not substantive; see counterexample).**
Current SCORECARD (pre-r48-integration tail = round 47): `depth:density = 9`, `depth:verifiability = 4`, `coverage = 7`. The lowest depth axis is `depth:verifiability = 4`. Round 48 declares exactly one claim, C1, and its `axis` field is `depth:verifiability`, satisfying the MISSION/AXES rule "at least one claim on the lane's lowest non-retired axis." The score is **held at 4 (delta 0)**, matching the lane's established rounds 39–47 "4 held" pattern.

**2. "No 4→5 promotion limbs achieved" — CONFIRMED.**
The two written limbs (Scorecard *Distance-to-next-score*, `### depth:verifiability, 4 → 5`) are (a) `gated=0` and (b) the score-5 audit bar (non-author audit passing 25/25 source chains). P4 reads `gated=22` — unchanged since r46/r47, so limb (a) is not met. Limb (b) was not performed this round. Moreover the frozen checker itself rejects `[x]` (`SF-VERIFIER`), so no self-promotion is even expressible. No 4→5 limb moved.

**3. "Coverage frontier 29 unchanged" — CONFIRMED.**
P2/P3: `rows=29 admitted=29`, dedicated counter exit 0. Round 48 added **S077** to `corpus/SOURCES.md` — a source-registry row, **not** a frontier (`F##`) row — so it does not move the coverage frontier. No frontier-ratio move is claimed or observed.

## Strongest counterexample (tested, not defeating)

**Claim:** C1 is attributed to `depth:verifiability` but is a *File-contract* form repair (`SHONEN.md` canonical-seed restoration, protocol "File contract per shokunin repo"), not a `depth:verifiability` axis-move — so "lowest depth 4 targeted" is nominal axis-labeling that consumes the lowest-axis claim slot without working the axis.

**Evidence:**
- P8: `depth:verifiability` is measured by `resolve.py` over `SKILL.md + corpus/**/*.md`; `SHONEN.md` is at repo root, is not in that set, and appears 0 times in the `citation-survival.md` census. Restoring `SHONEN.md` form therefore cannot move the axis metric.
- P4: C1 advances neither promotion limb (`gated` still 22; no audit).
- C1's own predicate discloses this: "this is form validation, not promotion or evidence truth"; `mechanical_limits`: "Scores held; no source restoration or end-to-end bounty task claimed."

**Why it is a tradeoff, not a rejectable defect:**
- The score is **held, not inflated** — the honest reading, and the lane states it explicitly.
- It is **consistent with the lane's own depth:verifiability precedent**: r45–r47 C1 claims are all mechanical/form counters (closure suites, c1/c2 gates, mutant batteries, scaffold repair). A form checker that verifies evidence-pointer *existence/resolution* is the same class and is genuinely verifiability-flavored (a reader can resolve what the checklist cites).
- It closes a **genuine routed defect** (round-47 R1: 13 accumulated assessment blocks / 52 author marks vs the canonical seed), and the historical bytes are retained (P5, archive pin matches).
- The framework requires a falsifiable before→after on the lowest axis, which C1 has (`SF-PREAMBLE → SF-CLEAN`); it does not require the claim to advance the score.

## Hidden-regression / provenance checks (all clean)

- **No density/frontier/verifiability regression:** P6/P7 — round 48 changed only `SHONEN.md` plus registry/lesson/controls; `SKILL.md` (density input), `corpus/README.md` (frontier table), and `density.py` are byte-unchanged. The repair did not touch any scored surface.
- **No lost historical bytes:** P5 — `shonen-before.txt` retains SHA256 `596122c0…`, satisfying the kill_rule archive limb.
- **No duplicate/hidden/commented checklist passes:** the frozen checker's committed fixtures (`controls/fixtures.json`: `fenced`, `commented`, `duplicate`, `missing-file`) each exit 1; only genuine single canonical seeds exit 0.
- **Landed-vs-candidate distinction (not a kill):** the landed `SHONEN.md` (`b1352168…`) differs from the frozen `canonical-candidate.txt` (`b476c7aa…`) at boxes 2/3/4 — landed box 2 is `[ ]` (unchecked, "no end-to-end domain task"), candidate box 2 is `[~]`. **Both pass `SF-CLEAN`**, so the claim after-state is satisfied by the landed bytes (P1); the landed form is the more conservative/honest one. Claim C1 requires `canonical=1`, not byte-identity to the candidate, so this is expected, not a defect.

## Impacted axes

- **depth:verifiability (4, held):** attribution confirmed; no promotion limb moved; metric not engaged by C1 (tradeoff noted).
- **depth:density (9, held):** non-target guard intact (SKILL.md/density.py unchanged).
- **coverage (7→frontier 29):** frontier unchanged; S077 is a registry row, not a frontier move. No coverage-ratio change.

## Smallest safe correction

**None required** — the attribution is accurate and honestly disclosed. Optional (not a gate): in future rounds the lane should keep stating explicitly that its lowest-axis claim is *form/holding* work rather than metric advancement, so "targeted" is never read as "advanced." This is a disclosure nicety only; requiring it retroactively would be scope the frozen claim does not own.

## Receipts

Probe commands and observed output are recorded verbatim above and in `/fast/scratch/hyaku/kasegi-r48/R48Review28/receipts.txt` (scratch removed at exit). No production files, fleet files, siblings, domain trees, or git/jj state were modified.
