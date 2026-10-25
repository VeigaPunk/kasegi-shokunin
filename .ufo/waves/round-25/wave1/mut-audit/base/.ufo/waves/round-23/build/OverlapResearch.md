# OverlapResearch — CVD coordination boundary (chousa method / kasegi application)

Seat: KasegiR23.OverlapResearch-5. Read-only. No production edit, no admission, no score.

Axes named: `depth:verifiability` (lane-qualified source identity; not the mirror detector) and `coverage` (F06 stays a kasegi frontier row; method text is not a second coverage unit).

## Pins

- kasegi HEAD `922a4dde90b60b465e2b8b241d1fe363f1f27e98` (matches `.ufo/waves/round-23/claims.json` `base`). Clean at observation: `PROVINCE.md`, `corpus/README.md`, `corpus/lessons/round-22.md`, `corpus/knowledge/coordinated-disclosure-timelines.md`. Dirty: `corpus/QUALITY.md` (append only, from the Round-23 criteria heading), `corpus/SOURCES.md`. Untracked: `corpus/knowledge/multiparty-vulnerability-coordination.md`.
- chousa HEAD `d730ae4c33989ad9c8535764d4cae77b4db869f6`. Cited chousa paths were porcelain-clean.
- No packages installed.

## Exact boundary

**Chousa owns the source method.** Domain line is deep-research method. Owned surfaces are question framing, the hierarchy primary / secondary / aggregator / unsourced, citation chaining and hop resolution, claim-vs-source verification, and search-strategy taxonomy (`/home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md` lines 3–8). The decision table is that order, and the hierarchy is stated as this lane’s own construction, not a rule inherited from another lane (`SKILL.md` lines 7–33). Chousa also keeps its own `corpus/SOURCES.md` A/B/C rows and search log (`SKILL.md` line 35). Those A/B/C labels are per-claim admission strength. They are not the four-rung hierarchy.

**Kasegi owns the domain application.** Domain line is bounty and security research: program rules, scopes, claim packages (`/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md` lines 3 and 29–30). It refuses anything outside that domain and reports it to the orchestrator rather than absorbing it (line 25). Adjacent, not absorbed: “chousa — research method and source hierarchy” (line 44). The admission bar already hands the method off: “Source tiers are defined in `corpus/SOURCES.md` (contract v1); the research method is chousa's — this file duplicates neither.” (`corpus/QUALITY.md` line 8; that sentence is inside the committed prefix; the worktree diff appends after line 38).

**CVD coordination roles are the application, not the method.** Frozen `corpus/README.md` line 200: F06 “Multi-party CVD — FIRST guidelines v1.1”, status `queued`, entry `—`, sources `S018`, next action “Open the public guideline and record its coordination roles.” Frozen `git show 922a4dde:corpus/SOURCES.md` S018 is that FIRST v1.1 URL, status `queued`, used-by `—`, teaches: “Coordinate upstream and downstream parties with clear contacts, negotiated timelines and shared disclosure expectations.” Round-22 lesson quote, still on the clean lesson file, line 94: “All parties should clearly and securely communicate and negotiate expectations and timelines.” Admitted precedent for this shape is F02 `corpus/knowledge/coordinated-disclosure-timelines.md`: attributed coordinator clocks, a “Kasegi use” binding to the report timeline, and a rejected universal deadline. It does not restate source hierarchy or search taxonomy.

**The two ladders stay distinct.** Equating kasegi tier A/B/C (QUALITY Q2: tier A or B required, tier C never sole support) with chousa’s primary > secondary > aggregator > unsourced ranking mixes admission strength with source rank. A FIRST guideline can be kasegi tier A for coordination-role claims and still be a primary specimen inside a chousa method exercise. The rank decision is chousa’s; the package-review rule is kasegi’s.

## What the worktree already did (not admission)

Observed after the frozen pin, not at HEAD:

- `corpus/SOURCES.md` line 24 now says S018 status `mined` and used-by `corpus/knowledge/multiparty-vulnerability-coordination.md`. Frozen row was `queued` / `—`.
- That knowledge file is untracked. It applies FIRST roles to a local disclosure-package review: finder, upstream vendor, downstream vendors, affected-product boundaries, optional coordinator, per-party contact and timeline (lines 7–16). It says “This is an application of FIRST's recommended practices” (lines 15–16). Quotes are coordination definitions and practices (lines 25–30). Rejected over-generalization is “upstream shipped, so every downstream user is patched” (lines 43–46). Limits refuse testing rights and bounty entitlement (lines 52–54).
- A search of that file for hierarchy or search-taxonomy wording hit only the `S018` citations and the recheck command (lines 2, 4, 21). No question-framing, primary/secondary ranking, citation-chain, or search-strategy lesson is in the draft as read.
- `corpus/README.md` line 200 is still `queued` / entry `—`. The dirty used-by cell and the frontier index disagree. Claims C2 counts admitted F06–F08 rows in `corpus/README.md`. This scan does not count F06.

## Cross-domain routing required

1. **Coordination-role question → kasegi, and the chousa gate will not do it automatically.** Live `SCOPE_BOUNTY` is `bug bounty|bounty program|bounty programs|bounty hunt|bounty hunting|bounty scope|claim package|claim packages|kasegi` (`/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` line 727). `scope_hit` matches a space-bounded phrase (`lines 742–748`). A Meta `domain`/`scope` value `coordinated vulnerability disclosure` or `multi-party vulnerability coordination` contains none of those phrases. `vulnerability disclosure`, `responsible disclosure`, and `security bounty` are recorded inflection debt, not installed triggers (chousa `SCORECARD.md` lines 1037–1040 and 1122–1124; round 23 selected the fenced-heading anchor instead). Routing is therefore orchestrator routing under kasegi `PROVINCE.md` line 25, not a gate hit. Declared `bounty program`, `claim package`, or `kasegi` still emits `SCOPE_BOUNTY_ABSORBED` with `route=bounty` (gate lines 768 and 772–773; contract in `corpus/knowledge/scope-refusal-r12.md` lines 19–22).

2. **Do not add `vulnerability disclosure` to `SCOPE_BOUNTY` in this round.** Same overbreadth class as `ai benchmark(s)`, which chousa left out because methodology research can name the topic without taking the refused province (`corpus/knowledge/scope-phrase-gap-r18.md` lines 19–22). A method record whose declared scope is citation method for disclosure policies would false-route into kasegi. Prose is already unscanned (gate lines 714–718; scope-refusal lines 49–52).

3. **Source-method question about the same documents → chousa.** Framing, ranking, hop resolution, and claim-vs-source checks stay chousa even when the specimen is the FIRST page. Kasegi `QUALITY.md` line 8 forbids duplicating that method. Domain quotes and package-review rules stay in the kasegi entry. Chousa may point at the kasegi artifact; it does not re-own the coordination rule.

4. **Bare `S018` is not a cross-lane pointer.** kasegi S018 is FIRST v1.1 (frozen row and worktree line 24; lesson line 94). chousa S018, `corpus/SOURCES.md` line 28, is Schreieder, Schopf, Farber, “Attribution, Citation, and Quotation”, ACL 2026, tier B, a lead index, status `queued`. The kasegi draft’s `source: S018` (line 2) and `source-recheck.py --source S018` (line 4) are in-lane registry ids. Any orchestrator or chousa handoff must write `kasegi S018` plus the FIRST URL. Opening chousa S018 for a FIRST quote is a false source.

5. **Not kagi and not kake.** Coordination roles are not vault custody. The draft’s recheck is a local kasegi manifest command, not web-property ownership. Secret values stay out (chousa `PROVINCE.md` lines 14–15; kasegi Q6).

## Contradiction, left unsmoothed

chousa `MINT.md` lines 14–17 says kasegi “explicitly refuses general source research.” No kasegi markdown sentence says that. The operative kasegi texts are the outside-domain refusal (`PROVINCE.md` line 25), the adjacent pointer (line 44), and the method handoff (`QUALITY.md` line 8). Chousa corpus markdown under `corpus/` has no match for `vulnerability|FIRST|CVD|multi-party|coordinated disclosure` at this read. That shows the coordination text is not filed in chousa’s corpus. It does not show the gate would route a CVD declaration.

The kasegi CVD search-log bullets (`corpus/SOURCES.md` lines 48 and 53) use the same identified/screened/included/excluded sweep shape as chousa’s search log. That is the sources-registry record of a domain sweep (scorecard capability `sources-registry`), not a second copy of the method. Teaching the taxonomy again inside an F06 entry would cross the line. The current draft does not.

## Falsifiers

1. Space-bounded containment of each `SCOPE_BOUNTY` alternative against normalized `coordinated vulnerability disclosure` is empty. A later constant that contains `vulnerability disclosure` supersedes the “gate will not route” claim. It still fails this round’s move unless a control Meta scope for disclosure-policy citation method stays CLEAN.
2. `rg` of `corpus/knowledge/multiparty-vulnerability-coordination.md` for `primary > secondary`, `search-strategy`, or `question framing` is empty on the bytes read. A later paragraph that states those as kasegi rules absorbs chousa.
3. Resolving bare `S018` in chousa `corpus/SOURCES.md` yields the Schreieder row (line 28), not the FIRST URL. A cross-lane FIRST citation that uses bare `S018` is false.
4. C2’s count surface is `corpus/README.md`. F06 there is `queued` / `—` (line 200). A dirty `SOURCES.md` used-by cell does not make the row admitted. This report does not authorize flipping that cell.

## Proposed move (one)

L1 keeps the multi-party entry in kasegi as domain application only. Cross-lane citations say `kasegi S018` and the FIRST URL. Do not widen chousa `SCOPE_BOUNTY` with disclosure phrases. Do not mark README F06 admitted from the untracked draft or the dirty used-by cell.

## Risks

- The untracked draft and dirty `SOURCES.md` are sibling work in progress. Line numbers there can move. Frozen README line 200 and the chousa gate constant are the stable pins.
- This seat did not re-open the FIRST page, did not run `source-recheck.py`, and did not run `research-gate.sh`. Quote truth and gate exit codes are unverified here. The lesson quote and the draft are corpus text, not a fresh official open.
- Declaration-only screening still misses undeclared bounty work (scope-refusal lines 49–52). That named limit is not a reason to keyword-scan prose.

## Verification

Not run, by the round’s mid-flight rule. L1 can falsify items 1–4 above with a phrase check, a content search of the draft, a read of both S018 rows, and `corpus/README.md` line 200. No mirror-detector case is implied; C1 containment is untouched.

## Scope limits

Kasegi overlap scan only. No edit to chousa, no edit to the F06 draft, no sibling vault/web/claims absorption, no live-target contact, no admission, no coverage increment.

Report: .ufo/waves/round-23/build/OverlapResearch.md
