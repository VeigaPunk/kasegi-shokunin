# R48Review29 — no-domain-task / no-promotion claims vs restored checklist evidence lines

Seat: R48Review29 (reviewer, leaf — no subagent dispatch). Lane root: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`. Claim under review: C1 (`claims.json` sha256 `b8022cdf…`, frozen 2026-10-30T14:30:48Z, base `903d47e1`). Scope: judge the author-side *no-domain-task* and *no-promotion* assertions behind the restored `SHONEN.md` evidence lines; flag misleading author assertions. Form semantics of the checker and historical-byte retention are covered by sibling probes; this seat grades the truthfulness of what the restored lines assert. No production edits, no target testing, no tool installs (none needed).

## Restored checklist evidence lines under review

`SHONEN.md` at HEAD `3d7e042` (working tree byte-identical to HEAD; sha256 `b1352168…`):

| Box | Mark | Pointer | Assertion text |
|---|---|---|---|
| 1 SKILL.md content | `[~]` | `SKILL.md` | "Author assertion; outside promotion verification remains required." |
| 2 end-to-end domain task | `[ ]` | `LOG.md` | "No new end-to-end domain task claimed; source and diagnostic work only." |
| 3 executable instructions | `[~]` | `corpus/lessons/round-47-verifier-spotcheck.md` | "Declared-root recheck observations; not promotion." |
| 4 no cross-domain bleed | `[~]` | `PROVINCE.md` | "Scope unchanged; live-target testing remains refused." |

## Commands and observed results (expected vs observed)

| Check | Command | Expected | Observed |
|---|---|---|---|
| After-state, frozen counter | `python3 corpus/instruments/shonen-form.py --root .` (lane root, HEAD `3d7e042`) | `canonical=1 finding=SF-CLEAN exit=0` (claims.json `expect_after`) | `shonen-form canonical=1 finding=SF-CLEAN exit=0`, process exit 0 — MATCH |
| Before-state, frozen archive | `python3 corpus/instruments/shonen-form.py --root . --file .ufo/waves/round-48/controls/shonen-before.txt` | `canonical=0 finding=SF-PREAMBLE exit=1` (`do-nothing.txt`) | exactly that, exit 1 — MATCH |
| Candidate control | same with `--file .ufo/waves/round-48/controls/canonical-candidate.txt` | clean (control) | `canonical=1 SF-CLEAN exit=0` — MATCH |
| "52 author marks" before-claim | `grep -c '^- \[~\]' .ufo/waves/round-48/controls/shonen-before.txt` | 52 (claim `before`; round-47 verifier route R1) | 52 — MATCH |
| Historical bytes retained | `sha256sum .ufo/waves/round-48/controls/shonen-before.txt`; `git show 903d47e:SHONEN.md \| sha256sum` | `596122c0f6b598d49eeb384898dc124d41ddb4ea867a569d77402d83017e9c05` (kill rule) | both print exactly `596122c0…` — MATCH (kill-rule limb 3 holds) |
| Checker not amended post-freeze | `git diff 3546f70 HEAD -- corpus/instruments/shonen-form.py`; `sha256sum corpus/instruments/shonen-form.py` | empty diff; `0ab32a2c…` (frozen receipt quoted by R48Probe16) | diff empty; sha256 `0ab32a2c6155a7d0055196df806898cb7e78880a072bf2504143b99377b313dd` — MATCH (kill rule "checker amendment cannot validate" not triggered) |
| Scores held / scope unchanged | `git diff 903d47e HEAD --stat -- SCORECARD.md PROVINCE.md` | empty (mechanical_limits "Scores held") | 0 lines — MATCH; PROVINCE.md:52 still carries "Live-target testing is refused; this corpus is documentation only." |
| No domain-task seat | roles in `.ufo/waves/round-48/wave1-spec.json` | none | executor 20, mutation-tester 20, reviewer 11, critic 4, scribe 4, connector 2, scout 2, sentinel 1 = 64, all probe/review classes — no hunt/submission seat |
| LOG round-48 entry | `git diff 903d47e -- LOG.md` (+6 lines) | no-domain-task statement | "no coverage claim or domain-task claim"; Bugcrowd/RaR lead "not a frozen claim, row or frontier admission … returned 404"; "Seventeen tree probes and six source mutants precede freeze" — both counts match `controls/pre-freeze-fixtures.txt` (17 cases) and `pre-freeze-mutants.txt` (6 mutants, all caught) |
| SOURCES round-48 row | `git diff 903d47e HEAD -- corpus/SOURCES.md` | S077 = own-work protocol row | S077 tier `own-work`: "Normative form of this lane's promotion checklist, not bounty policy or promotion evidence"; search-log: "No new domain source or frontier ground claimed" — MATCH |

## Findings

**No misleading author assertions found in the no-domain-task / no-promotion claims. The restored checklist's evidence lines are accurate and, on box 2, more conservative than required.** Details below; items 1–4 are the per-line verdicts, 5–8 are observations with severity.

1. **Box 2 (no-domain-task) — VERIFIED, honest.** Mark is `[ ]` (unchecked), not `[~]`: the lane declines to assert the box while claiming none of it. The assertion "No new end-to-end domain task claimed; source and diagnostic work only" matches `LOG.md` round-48 ("no coverage claim or domain-task claim"), the wave spec (64 probe/review seats, no domain seat), and `corpus/SOURCES.md` (only S077, an own-work protocol row; the Bugcrowd/RaR lead rejected, 404, not admitted). The only committed round-48 work is the form restoration, the new checker, QUALITY R55, the S077 row, and the lesson — source-registry/diagnostic work, no domain surface executed.

2. **Box 4 (no-bleed) — VERIFIED.** `PROVINCE.md` is byte-unchanged base→HEAD (`git diff 903d47e HEAD -- PROVINCE.md` empty); "Scope unchanged" is exact, and "live-target testing remains refused" is verbatim-grounded at `PROVINCE.md:52`.

3. **Box 3 — VERIFIED as a description, not a verification.** The pointer file exists (96 lines) and is the round-47 *non-author* spot-check; it does record declared-root recheck observations (recheck audit 67/67 with gated=22, and §6: "Box 2 … the lane claims none, honestly. Promotion remains operator-owned."). The line's own claim is confined to "Declared-root recheck observations; not promotion" — it does not present the file as a non-author check of box 3, and the mark stays `[~]`. Accurate.

4. **Box 1 — VERIFIED, weakest pointer (observation, low).** `SKILL.md` resolves and the round-47 spot-check §6 says box 1 "looks fully checkable by a non-author on the current evidence", but the pointer is a whole-file reference with no locator, thinner than the protocol's located-pointer norm for claims. The line self-labels "Author assertion; outside promotion verification remains required", so it is not misleading — flagged only as the thinnest of the four lines.

5. **No-promotion claim — VERIFIED.** No `[x]` mark exists (marks: `~, space, ~, ~`); the checker rejects `x` as `SF-VERIFIER` anyway, a limit the claim's mechanical_limits disclose. `SCORECARD.md` is byte-unchanged base→HEAD (scores held: depth:verifiability 4, coverage 8, depth:density 9 per round-47 closure). A `grep -n "promot"` sweep of all landed wave-1 reports shows every mention scoping itself ("author-side form only; no promotion or semantic-truth judgment"); R48Probe31's promotion-gate language only explains why a three-box file is noncanonical — no report asserts box verification, promotion readiness, or score movement.

6. **Landed file deviates from the frozen candidate control — in the safer direction (observation, informational, not a defect).** `controls/canonical-candidate.txt` (sha256 `b476c7aa…`) carries box 2 as `[~]` with blanket `LOG.md` pointers on all four boxes; the landed file drops box 2 to `[ ]` and uses per-box pointers (`SKILL.md`, the round-47 spotcheck lesson, `PROVINCE.md`). The candidate is a control snapshot, not the frozen predicate; the frozen after-line holds on the landed bytes (`canonical=1 SF-CLEAN exit=0`, confirmed above). No kill-rule limb is implicated. Documented so the candidate is not later mistaken for the binding target.

7. **A historical duplicate checklist passes the frozen checker — correct grading, not a kill-rule escape (observation, informational).** `python3 corpus/instruments/shonen-form.py --root . --file .ufo/waves/round-25/wave1/mut-audit/base/SHONEN.md` prints `canonical=1 SF-CLEAN exit=0` because that audit artifact is the untouched canonical seed (all `[ ]`, no evidence lines). The kill rule's "tested hidden/commented/duplicate checklist" limb targets evasions of the *drifted* content: the tested fixtures (`fixtures.json`: fenced, commented, duplicate, extra-prose, CRLF, no-newline, wrong-label, missing-evidence — 17/17 at `pre-freeze-fixtures.txt`) and six source mutants (`pre-freeze-mutants.txt`, all caught) all exit 1, and the actual pre-repair bytes fail `SF-PREAMBLE`. A genuinely canonical historical file grading clean is the checker working, not a loophole. Disclosed for completeness since a literal reading of the kill rule could be spooked by it.

8. **In-flight integration context (not scored, informational).** Working tree carries an uncommitted `SKILL.md` addition — a Gates & probes registry row for `shonen-form.py` whose own text makes the same disclaimers this seat verified ("repairs the lane's own promotion checklist, not a bounty gate … does not certify a domain task, evidence truth, source recovery or promotion") — plus an untracked `corpus/instruments/shonen-form-selftest.py` runner. These bytes are not needed for the frozen predicate (committed HEAD already grades `canonical=1`); noted so the record shows the registry/selftest delivery was observed mid-assembly and its wording is consistent with the no-domain-task/no-promotion frame.

## Residual risk and verification gaps

- **Semantic truth of the boxes remains unjudged here, by design.** This seat verified that the evidence lines' assertions are accurate as statements of record (no domain task executed, scope unchanged, no promotion claimed), not that the underlying box conditions hold — that stays with non-author promotion verification, as the checklist itself repeats ("outside promotion verification remains required").
- **R2 route (plain-target phrasing) not re-exercised:** per the claim and R48Probe12, R2 motivates the freeze but is not changed by this claim; my spot-check of the claim's before/after text counts (52 marks, 17 fixtures, 6 mutants) does not extend the R2 frozen-target counter, which remains an open integrator item from round 47.
- **Per-line locators:** if a future round wants stronger box-1/box-3 pointers, anchoring to a section or line would exceed the frozen grammar's requirements but improve the protocol-grade evidence standard; not required for C1 and not a conformance defect.
- Saturation: every no-domain-task/no-promotion assertion reachable from the claim, the restored checklist, `LOG.md`, `SOURCES.md`, `PROVINCE.md`, `SCORECARD.md`, and the 17 landed wave-1 reports was checked against a resolvable surface; nothing contradicted.

**Seat verdict:** C1's author-side disclaimers hold — the restoration is form validation only, no domain task is executed or claimed, no promotion is asserted or implied, scores are held, and each restored evidence line says only what the record supports. No misleading author assertion flagged. Expected vs observed matched on every command above.
