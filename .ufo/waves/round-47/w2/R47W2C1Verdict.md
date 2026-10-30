# R47W2C1Verdict — adversarial grade of C1 against the unchanged frozen after sentence

Seat: critic, wave 2. Axes: depth:verifiability, coverage. Integrated revision graded: 65e19bdb142c90a08103eb4b2af60c71218a920e (corpus byte-identical at HEAD f074bff; `git diff 65e19bd HEAD -- corpus` = 0). Receipts: `.ufo/waves/round-47/w2/R47W2C1Verdict.receipts.txt`. No production edits, no git/jj mutation, no installs (none needed), no delegation, no agent broadcast.

## Verdict

**Full verification of the unchanged frozen C1 after sentence is NOT supportable — on two independent grounds.** The strongest supportable grade is: **C1 mechanically FAILED at the integrated revision, and substantively unmet in exactly one clause (the S074 `mined→rejected` transition, refused by design)**. This matches — and sharpens — the tree's own disclosure at `corpus/lessons/round-47.md:59` ("C1 is not fully verified … The harmful transition is not performed and the frozen target is not rewritten").

### Ground 1 (executed): the frozen counter is RED at the integrated revision — the kill rule fires now

The frozen after sentence (`claims.json:13`, sha `dc9d95cf…` byte-identical at freeze 308a2cb and 65e19bd) asserts the counter prints `routed-defects total=11 fixed=11 unresolved=0 exit=0`. Executed against a `git archive 65e19bd` corpus export with the freeze-pinned counter (sha `e6ede7b6…` = `freeze.txt:3`), it prints **`total=11 fixed=10 unresolved=1 exit=1`** — limb L3 red (`corrections-section-present content=0`). No wave receipt had ever run the counter on the landed tree (R47ExecGateReplay and R47ExecFreezeGates ran base 0/11 and the pre-landing working tree 2/11; selftest greens are synthetic fixtures), so this is the first integrated-tree measurement and it contradicts the sentence's own measurement clause.

L3 root cause (static + token scan): `corpus/lessons/round-46.md:153` carries `## Corrections (round 47)`, but its D5 bullet (`:155`) names the sections only hyphenated — "one **Search-log** and two **Registry-changes** bullets" — while the frozen predicate (`r47-routed-defects.py:139-143`) requires unhyphenated `Search log` or `Registry changes` in the section tail (both other conjuncts, `SOURCES.md` and `fence`, hold). The committed selftest fixture text carries exactly the missing tokens (`r47-counters-selftest.py:167-168`, "(`## Search log`, `## Registry changes`)"), so `c1-green` passes while the landed bytes fail: fixture and landed text diverge at precisely this predicate.

The frozen kill rule (`claims.json:14`) says "C1 fails if the counter prints fixed<11/11 at the final lane revision". That clause fires at 65e19bd regardless of the S074 question. No goalpost movement is involved: claims bytes and counter bytes are provably unchanged; the landed corrections text simply does not satisfy the frozen predicate it was landed to satisfy.

### Ground 2 (executed counterexample): even at 11/11 the counter cannot verify the refused transition — false-green by absent predicate

Flip-arm probe (executed in scratch): flipping ONLY the S074 row's status cell `mined → rejected` (`corpus/SOURCES.md:80`) in the integrated tree leaves the counter output byte-identical (same ten greens, same L3 red, same exit). No limb reads S074's status or used-by cells — the only status assertions in the counter concern S076 (`:250-254`, required `mined`) and the entry's citations (`:274-276`). Consequences:

- The counter greens BOTH the landed (mined) world and the frozen-sentence (rejected) world. Once L3 is repaired, a green counter certifies nothing about the one clause in dispute; the mechanical gate is structurally non-probative there.
- Performing the transition breaks capture-binding B3 on the actual tree: executed `capture-binding-check.py` gives `records=63 bound=63 unbound=0 EXIT=0` integrated vs `FAIL rule=rejected-row-anchor record=S074 row=S074 dir=round-46-a2`, `records=63 bound=62 unbound=1 EXIT=1` flipped — upgrading R47RevD7's 3-record fixture probe (`w1/R47RevD7.md:17-20`) to the full 63-record audit. A rejected S074 would also leave positive `teaches` prose on a rejected row, violating the rejection-semantics contract (`CORPUS.md:101-104` per R47RevD7's medium finding).
- The refusal is therefore the correct disposition under QUALITY R54 (`corpus/QUALITY.md:401`): "If a frozen claim demanded the harmful transition, report that claim unmet; do not weaken B3 or rewrite the frozen predicate to manufacture success." This is a tradeoff the judge must uphold, not a defect to fix: satisfying the sentence's letter would trade a real gate (B3 binding of the retained round-46-a2 manifest) for prose.

### False-green controls exist (three independent surfaces)

1. Executed by R47RevCounterC1 (`w1/R47RevCounterC1.md:7-9`): trees with all evidence hidden in multiline HTML comments / tilde fences still grade `total=11 fixed=11 exit=0` (attacks A and B, receipts retained).
2. Disclosed battery: 16 C1 survivors (`controls/mutbat-receipt.txt:36`, ids L2d…L11a). Structurally, none can cover the S074-status gap — the battery mutates predicates that exist and cannot disclose an absent one.
3. The selftest's positive fixture applies the refused transition itself (`r47-counters-selftest.py:218`, `edit_row_cells(txt, "S074", status="rejected", …)`): the 43/0 green suite validates the counter against a world that violates B3, never against the landed mined world for that clause (which nothing reads). Additionally the frozen kill rule contains no clause that fires for "after-sentence clause refused while counter green" — the contract's falsification machinery could only ever catch this round's failure in the L3 direction (false red), which it just did.

## Clause-by-clause against the unchanged after sentence (static, executed greps)

| After-sentence clause | State at 65e19bd |
|---|---|
| Counter 11/11 exit=0 | FALSE — 10/11 exit=1, L3 red (executed) |
| Three round-46 bullets landed, scaffold/fences gone | MET — L1/L2 green; fences 0, `to append` 0 (SOURCES.md:115, :172-173 vs base fence bytes at fc8e0af:114-123, 177-186) |
| F29 three sentences corrected in place, 145 lines, re-anchored to S076, 0 `S074.txt:` | MET — L4-L6/L9 green; 145 lines; spans 47/47 located in 558-600 |
| S076 registered, pinned manifest, recheck exit 0 | MET — L8 green (SOURCES.md:82) |
| **S074 status mined→rejected** | **REFUSED — row stays `mined` (SOURCES.md:80, :176); B3 break demonstrated** |
| S074 used-by → round-46.md logged old→new | MET — SOURCES.md:176 + row cell |
| REST-API lead under ## Leads | MET — SOURCES.md:124, L10 green |
| round-46 Corrections section | PRESENT but fails the frozen L3 token predicate (this round's landing defect) |
| round-47 lesson notes (dropped findings, ZDI reservation, S068) | MET — L7/L11 green |
| Plain `grep -c 'supersedes S074'` target 1 | Reads 2 (row :82 + Registry-changes bullet :175) — benign drift, not kill-rule-bound; log as observation |

## Impacted axes

- **depth:verifiability**: the after sentence's own measurement assertion is false at the tip (10/11); the gate is blind at the disputed clause (flip-arm proof); hidden-content false-greens are demonstrated. The honest state — "C1 is not fully verified" (`round-47.md:59`) — is accurate and, until this seat, incomplete: it did not mention the L3 mechanical red.
- **coverage**: no instrument row, battery survivor, selftest case, or kill-rule clause covers the refused transition in either direction; conversely L3 shows a false-red coverage mismatch on landed text. C2's disposition (no F30; ZDI as F02 enrichment) is out of my lane's scope and untouched here.

## Smallest safe correction (not mine to land — no shared production edits from this seat)

1. Integration owner only: amend the round-46 Corrections D5 bullet to name the sections unhyphenated (e.g. parenthetical "(`## Search log`, `## Registry changes`)" — the selftest fixture's own phrasing at `r47-counters-selftest.py:167-168`). Within-round correction of text landed this round; no historical bytes change; counter then reads 11/11 exit=0 at the final revision and the kill rule's mechanical clause is satisfied. If the round can no longer take production edits, C1 stands FAILED at 10/11 with this cause documented — do NOT edit the byte-frozen counter post-score (`round-47.md:61` bars presenting post-score hardening as validation).
2. Keep everything else as landed: S074 mined with used-by re-point and old→new log (SOURCES.md:176), S076 successor, B3/R54 intact, frozen sentence unrewritten. Final honest grade after fix 1: C1 unmet solely on the S074 status clause — reported unmet per R54, with the three false-green surfaces carried as disclosed gaps.
3. Record the counter's S074-status blindness and the fixture/landed-text divergence as disclosure items alongside the 16 mutbat survivors (documentation append, not counter edits).

## Executed vs static

- Executed (read-only): archive export; counter on integrated tree and flip arm; capture-binding-check on both arms; sha256 identity checks (claims.json ×3 readings, counter vs freeze pin); corpus diff 65e19bd↔HEAD; plain greps; L3 token scan. Full outputs in the receipts file.
- Static: counter source limb inventory; kill-rule text; lesson/QUALITY/R54 readings; R47RevD7, R47RevCounterC1, mutbat-receipt, selftest fixture readings. No network, no build/test/selftest/battery rerun, no pacman transactions (paused), no service restarts.

Report: .ufo/waves/round-47/w2/R47W2C1Verdict.md
