# ConnectorOverlap — round-81 sibling-overlap and cross-claim scan

Round 81, attempt 1, one v1 wave (13 seats). Read-only seat: no lane byte outside
`.ufo/waves/round-81/w1/` was written; no git/jj write; no tool install. Lane repo
`/home/vgpnk/Projects/shokunin/kasegi-shokunin`, fleet root `/home/vgpnk/Projects/shokunin`.
Freeze `7ad3118c86ee14fde433d73671cc407668533cec`, base `191e6ba8f872d08802d83b57cd7fcf4bfa122f0e`.

Receipt: `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ConnectorOverlap-receipts/fleet-ground-sweep.txt`
(every count below is that file's output).

## Findings table

| # | question | finding | evidence | consequence for r81 |
|---|---|---|---|---|
| 1 | Does any sibling lane hold F57's ground? | **No.** Across 20 sibling lanes with a `corpus/`, 242,993 sibling corpus files and 1,592 sibling `corpus/knowledge/*.md` (snapshot 2026-11-06T20:37:26Z; sibling lanes are concurrently active), the exact tokens `importfindings`, `source.yaml`, `home database` and `import findings` occur in **0 text files** outside kasegi (binary files excluded — a `.so` substring match on `osv` is noise, see homonym block). The only `osv` hit in a sibling knowledge entry is a homonym: object–subject–verb constituent order. Hit-bearing classes are all non-OSV senses. Kasegi's own lessons already name the endpoint as an open lead, so a sweep over lessons false-positives. | `ConnectorOverlap-receipts/fleet-ground-sweep.txt` §exact-token/§homonym/§lead-log; `/home/vgpnk/Projects/shokunin/kotodama-shokunin/corpus/knowledge/linguistics/syntax-typology.md:11,32`; `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-77.md:14`, `round-78.md:41`, `round-79.md:78` | B6's lane-literal 0/6 over 94 entries can be restated fleet-literal 0 over 1,592 sibling entries. No sibling arbitration owed. Residual: paraphrase, which no literal sweep closes (see Risks). |
| 2 | Does a sibling corpus hold a case-matched-kill / neutral-row counter rule? | **Yes — kaidoku holds the nearest rules, one matching and one stricter.** Row 138 matches r81's declared-case kill: “a kill is counted only when the *declared* case fails, never when any case does.” Row 133 adds the sole-detector requirement r81's counter does not meet: “The battery records `sole: failed == [expect_case]` per mutant and a claim that names a sole detector requires it.” Row 140: “the un-mutated instrument is its do-nothing control”. chousa 106/107 carry the alternating-tool and equivalent-mutant rules; kaidoku's round-85 spot-check drops verdict-neutral rows, where r81 *requires* them to pass. | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/QUALITY.md:218` (Row 138), `:210` (Row 133), `:222` (Row 140); `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/QUALITY.md:957` (106), `:958` (107); `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-85-verifier-spotcheck.md:94-95` | Cite Row 138 and Row 140 as prior art for the declared-case kill and the clean-baseline limb; **distinguish** Row 133 (`sole`, `:210`) and Row 147 (a kill names a detector, not its semantics, `:236`) as stronger bars r81 does not claim. r81's neutral-row requirement is stronger than the sibling practice of excluding neutral rows. |
| 3 | Does F57 (publisher-side import feedback) fit kasegi's province? | **By precedent, not by the governing line.** Governing line: “**Domain:** bounty & security research — scopes ~/Projects/bounties, program rules, claim packages” and “**Refuses:** anything outside this domain”. F57 is an OSV.dev API contract — not a scope, program rule or claim package. It fits because F31/F35/F51/F54/F55/F56 already admitted OSV surfaces. The F57 amendment exists **only in the working tree**: the freeze has 229 lines and `grep -c F57` = 0; the worktree has 231 lines, and **no B0–B8 predicate reads `PROVINCE.md`** (B3's census reads `corpus/README.md`). The entry's Claim 2 disclaims the province's practitioners (“a bounty hunter or a scanner author is not the audience”), so the only province tie is Claim 3: an OSV absence is not proof of non-publication. | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md:3,24,25`; F57 amendment `PROVINCE.md:231`; `git show 7ad3118c86ee14fde433d73671cc407668533cec:PROVINCE.md` (229 lines, F57 absent); `corpus/instruments/frontier-recheck-count.py:114-129` (README rows only) | The amendment is an unpredicated landing byte. Either label it integration bookkeeping (outside claim scope) in the C2 report, or route “PROVINCE amendment with no predicate” as a round-82 defect. The province tie to state is Claim 3's triage rule, not the audience. |
| 4 | Is there a still-unimplemented `considerthese/2026-10-26.md` proposal that fits either frozen claim? | **None fits.** Landed: #1 r39 (`SCORECARD.md:1534` names the 2026-10-26 proposal), #3 (`LOG.md:1700`), #5 (F18 in `PROVINCE.md`). A proposal ledger exists but is scoped to the previous reflection (`corpus/knowledge/considerthese-proposals-ledger.md` `source:` is `considerthese/2026-10-25.md`), so #7's own batch is untracked. Still open: #4 (wave-evidence cap), #6 (cadence), #7 (for the 10-26 batch) — none touching a frozen claim; #2 (line 30) is half-landed — `claim-package-check.py` r43 (`5b4a850`), documentation-only trial r74 (`LOG.md:2795`) — and its remaining end-to-end task is refused by province (`SHONEN.md:7-8`). | `/home/vgpnk/Projects/shokunin/kasegi-shokunin/considerthese/2026-10-26.md:29-35`; `corpus/knowledge/considerthese-proposals-ledger.md:3`; cites as listed | No proposal can be spliced into C1 or C2; #1/#3/#5 should not be re-proposed, and #7's ledger needs a 2026-10-26 batch only when a future round takes it. |

### Quotes the lane can cite verbatim (item 2)

- `kaidoku-shokunin/corpus/QUALITY.md:218` — “**Row 138 (a mutant is killed only by a detector present in the target's own output).** … and a kill is counted only when the *declared* case fails, never when any case does.”
- `kaidoku-shokunin/corpus/QUALITY.md:210` — “**Row 133 (a mutation case feeds the input the mutation changes, and a mutant has one declared detector).** … The battery records `sole: failed == [expect_case]` per mutant and a claim that names a sole detector requires it.”
- `kaidoku-shokunin/corpus/QUALITY.md:222` — “**Row 140 (… the un-mutated target is its do-nothing control).** … the un-mutated instrument's survivors are the do-nothing control, and an empty mutant set must fail a declared population floor rather than pass `survivors 0`.”
- `chousa-shokunin/corpus/QUALITY.md:957` — “**106. A counter's kill rule cannot be satisfied by a tool that alternates its behaviour or counts its calls.**”
- `chousa-shokunin/corpus/QUALITY.md:958` — “**107. A frozen mutant set holds no equivalent mutant; a survivor is classified before the target is fixed.**”
- `kaidoku-shokunin/corpus/lessons/round-85-verifier-spotcheck.md:94-95` — “`.mutants` has **21** rows; `.excluded` names the three verdict-neutral rows the report declares dropped.”

## Connector move (one bounded proposal)

### Evidence

1. **B8 pins location, not width.** The frozen gate accepts a span when its text is a *substring* of the declared snapshot line: `mislocated = sum(1 for t, n in spans if not (… and t in snapshot_lines[int(n) - 1]))` (`entry-gate.py:48-50`); the only width cap is 25 words (`overlong`, `:51`); the pin test is containment, `q in t` (`unpinned`, `:63`); `ok` at `:64-65`.
2. **A snapshot line is a paragraph.** `capture-source.py` collapses whitespace per line, so `S115.txt:32` carries the experimental-status sentence, the audience sentence and the feedback request; `:34` is the whole purpose paragraph; `:39` is three sentences.
3. **The C2 claim fences exactly the adjacent clauses.** C2's statement says “Not claimed: the experimental-status sentences of S115.txt:32 other than the audience sentence … the case-sensitivity note of S115.txt:39”. B8 cannot read that fence.
4. **A concrete accepted input exists.** The 19-word span `"This API endpoint is still considered experimental. It is targeted to operators of home databases that OSV.dev imports from." (S115.txt:32)` is a **measured** verbatim prefix of line 32 and is ≤ 25 words; it contains Q02, sits in a Claim section with the two required lines, and leaves header/claims counts unchanged → B8's four counters stay `mislocated=0 overlong=0 claimless=0 unpinned=0` and the gate prints pass [INFERENCE from `entry-gate.py:37-69`; the span string and word count are measured against the capture].
5. **The repair is already compatible with every OSV entry.** Across five entries (S108 23, S112 10, S113 10, S114 6, S115 6 = 55 spans), **every** span is textually *equal* to a manifest quote and carries that quote's anchor line: 55/55 equal, 0 fragments, 0 anchor mismatches (receipt §span/quote equality). This includes the S115 draft — whose six spans are all exact — so the move is preventive, not a fix to the landing entry.
6. **Cross-claim dual.** C1's forgery set covers *displacement* (F1 location, F5 all-case); B8's selftest covers `dump`, `moved` and `norule` (`entry-gate.py:93-99`). Neither covers *dilation* — a wider span inside one paragraph. C1's neutral-row limb tests that a semantics-preserving transform does not change the verdict; C2 has no limb testing that a semantics-*extending* transform inside a paragraph does change it.

### Affected axes

- **depth:verifiability (primary).** The C2 gate's enforcement boundary becomes explicit and falsifiable; the companion control can fail on a measured input. No score move is claimed (depth:verifiability stays 4; C1 remains the round's scored move).
- **coverage (not harmed).** No byte, count, predicate or verdict changes; F57's six clauses and the admission stand. The entry's `Not claimed` paragraph is load-bearing today and stays.

### Proposed move

Add a **companion** span-equality control beside B8 in the wave dir (not a predicate, not an edit to frozen bytes), with a supplementary receipt:

1. Parse every `"…" (<SID>.txt:<line>)` span of the landed entry and the four prior OSV entries; require `span_text` to **equal** a manifest quote of that source (equality, not containment) and `line` to equal that quote's anchor; count `spans / equal / not_equal / anchor_mismatch`.
2. Run the 19-word merged span above as the **negative** case (must be rejected); run S115 and F54–F56 as **positive** cases (must pass; measured 55/55 today).
3. State the limit in one sentence in the C2 report: *B8 pins location but not width, because the capture's line is a paragraph; the `Not claimed` fence is enforced by prose, not by the gate.*
4. Route a round-82 **B9** candidate: “a claim's located span equals a manifest quote of its source, at that quote's anchor” (safe rule: every span equals *some* quote — not a bijection; S112 has 10 spans over 7 quotes, S108 23 over 31, through nested/repeated quotes).

Do not edit `entry-gate.py` or the manifest this round (frozen bytes); the entry lands as drafted (6/6 exact).

### Risks

- **Rule compatibility beyond OSV entries is unmeasured.** The 55/55 equality was measured on the five OSV entries only; the 90 non-OSV knowledge entries may use fragment spans. B9 must be scanned over all 95 entries before adoption.
- **Post-freeze predicate risk.** The companion control is evidence, not a B-limb. Presenting its output as B8 or as a new predicate after any seat has scored would violate the kill rule; label it “supplementary; no verdict”.
- **Prospective, not present, harm.** The draft entry is clean (6/6 exact). The merged span is over-quotation unless a future entry leans on it to import an F51-held clause; the gate's silence is the structural issue, not this landing.
- **B6 residual.** A paraphrase of the six clauses in a sibling lane is invisible to every literal sweep run here; the homonym classes (`quality bar`, `import-time`, `R83OSV`, OSV=word order) show why broad sweeps mislead. Closing that residual is a reading task over the nearest topical neighbours, not a grep.
- **Item 3 seam.** If the F57 `PROVINCE.md` amendment lands unpredicated, the round carries a lane byte no predicate reads; that is a defect class, not a verdict change.

### Verification

1. `grep -n 'mislocated = \|overlong = \|unpinned = ' .ufo/waves/round-81/c2/entry-gate.py` → the containment/substring and 25-word conditions quoted above (`:48-51`, `:63`).
2. Equality/anchor scan (already run; receipt §span/quote equality): five files → `TOTAL spans=55 equal=55 not_equal=0 eq_anchor_mismatch=0`.
3. Negative case (needs an executor run; **not run by this seat**): copy the draft entry, replace Claim 2's span with the 19-word merged span, run `entry-gate.py` → expected `pass` (frozen B8) while the companion prints `not_equal=1`; the paired outputs are the receipt.
4. Fleet sweep re-run: the four exact-token classes → 0 files outside kasegi; the homonym classes → the cited non-OSV lines.

## Contradictions stated, not smoothed

- F57's audience is outside the province's practitioners while the amendment admits it as province ground; the only in-province sentence is the entry's triage rule (Claim 3), not the audience.
- The C2 statement's `Not claimed` fence lists clauses the B8 gate cannot distinguish from claimed ones, because the capture's line unit is a paragraph.
- B6's distinctness is lane-scoped; the fleet-scoped sweep I ran is stronger evidence but is not a predicate and must not be presented as one.

## Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ConnectorOverlap.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-81/w1/ConnectorOverlap-receipts/fleet-ground-sweep.txt`
