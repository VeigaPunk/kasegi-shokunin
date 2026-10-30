# R47W2FrozenLimits — frozen bytes vs freeze record, 34 disclosed survivors, wave1 false greens

Axes: depth:verifiability; coverage. Critic/reviewer seat; recommendation only — no admission, integration, judgment, or production edits. Reviewed integrated `65e19bdb142c90a08103eb4b2af60c71218a920e` against base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`, freeze `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`, dispatch HEAD `f074bff`. Every path below is relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.

Executed in this seat: sha256 verification of all freeze-pinned bytes at three revisions; one replay each of the two frozen counters on scratch `git archive` checkouts of the freeze and integrated commits; one exact-predicate test of limb L3; receipt↔harness ID set comparison. Static in this seat: survivor guard readings, wave1 false-green report reading, disclosure-trail reading. No mutant battery, no selftests, no git/jj mutations, no installs, no network, no domain targets. Receipts: `R47W2FrozenLimits.bytes.txt`, `R47W2FrozenLimits.replay.txt`, `R47W2FrozenLimits.l3.txt` beside this report.

## 1. Frozen bytes match the freeze record (executed) — and stayed frozen through integration

All ten `.ufo/waves/round-47/freeze.txt` pins verify OK at the working tree, at freeze `308a2cb`, and at integrated `65e19bd`: the two counters (`corpus/instruments/r47-routed-defects.py` e6ede7b6…, `r47-f30-gate.py` 563d52b8…), `r47-counters-selftest.py` 4c7c0aab…, `r47-mutbat.py` eda81d5d…, `entry29-fixed-bytes.md` 89fd18c4…, `corpus/source-snapshots/round-47/manifest.json` 6168521b…, `S075.txt` 9dee8161…, `S076.txt` 9bd8ab57…, and `claims.json` dc9d95cd…. HEAD `f074bff` adds only four wave2 dispatch artifacts (`.ufo/waves/round-47/wave2-*`, 730 insertions); no production or frozen byte changes after integration. Working-tree dirt is untracked w2 output plus the untracked `.ufo/waves/round-47/counter-errata.md` — the integration owner must commit that disclosure file; its content is consistent with frozen bytes.

**Consequence for the ticket sentence:** because claim and counter bytes are provably identical before any seat scored (freeze) and after all scoring (integrated, working tree), no post-score change exists that could be presented as frozen validation. Conversely the wave1-found weaknesses are still live in the byte-identical instruments: any current `11/11` or `7/7` from these counters does not exclude the documented false-green classes, and no repair of them may be retro-credited to the frozen instruments.

## 2. Counter replay: freeze readings match claims.json; integrated readings are BELOW the frozen after-states (executed)

- Freeze tree: C1 `routed-defects total=11 fixed=0 unresolved=11 exit=1` — matches claims.json C1 `freeze_tree_reading` verbatim. C2 `f30-gate fixed=2/7 exit=1` with exactly H4 and H7 passing — matches claims.json C2 `freeze_tree_reading`.
- Integrated tree: C1 `total=11 fixed=10 unresolved=1 exit=1` (L3 red); C2 `fixed=6/7 exit=1` (H1 red, `rows=29 admitted=29`). Neither reaches its frozen `expect_after`. Corroborated by sibling `w2/R47W2Gates.md` + `w2/R47W2Gates-c1.stdout`/`-c2.stdout` (independent working-tree runs, identical verdicts). My replay adds the byte-level root cause for L3, which no committed report names:
  - **New finding: the L3 red is a hyphenation mismatch, not missing substance.** The frozen predicate (`r47-routed-defects.py:175-183`) requires, after the `## Corrections (round 47)` heading in `corpus/lessons/round-46.md`, the strings `SOURCES.md`, `fence`, and (`Search log` OR `Registry changes`). The integrated lesson's D5 bullet (`corpus/lessons/round-46.md:155`) writes "one Search-log and two Registry-changes bullets" — hyphenated — so `content=0`. Executed predicate test: `SOURCES.md`=True, `fence`=True, `Search log`=False, `Registry changes`=False. The frozen scaffold phrases the limb protects (`r47-routed-defects.py:72-76`) use the backticked, space-separated heading forms.
  - **Smallest safe correction (integration owner's; not performed here):** at `corpus/lessons/round-46.md:155` write the names as the headings read: "one `## Search log` and two `## Registry changes` bullets". By the frozen counter alone this flips L3, giving integrated C1 `fixed=11/11 exit=0`. It is a one-line tree-prose edit; counter/claim bytes stay frozen. **This would still not make C1 fully verified:** the frozen S074 `mined→rejected` after-state remains unperformed (B3 no-harm; `w1/R47RevD7.md` + `w1/R47RevD7.receipts.txt`), per `counter-errata.md` "Claim outcomes are not narrowed". 11/11 is mechanical only.
  - **No committed document records this mechanical miss.** `counter-errata.md` says C1 is "not fully verified even if all eleven mechanical limbs become true" — the assumption is untested; one limb is false. The kill rule "C1 fails if the counter prints fixed<11/11 at the final lane revision" fires today at `65e19bd`, independent of the S074/B3 reason the wave was briefed with. The errata/lesson should record the pre-fix 10/11 reading (old→new) when the one-line fix lands.
- C2 at 6/7 is the documented intentional miss: H1 red because there is no F30 row; ZDI retained as F02 enrichment (`corpus/lessons/round-47.md` §Integration decisions; `counter-errata.md` §"Claim outcomes are not narrowed"). Consistent with the ticket: C2 frozen target not met, not rerolled.

## 3. The 34 disclosed survivors (static guard reading; count consistency executed)

`controls/mutbat-receipt.txt` lists 56 mutants: C1 35 = 19 caught + 16 uncaught; C2 21 = 3 caught + 18 uncaught; `equivalent=0`; `baseline_failures=0`; both battery summaries end `exit=1` (a battery exit 1 is not a pass — lesson M47-5). Executed cross-check: receipt mutant IDs and `corpus/instruments/r47-mutbat.py` triples form identical 56-ID sets (empty difference both directions); 16+18=34 survivors confirmed. The battery grades each mutant only against the 43-case selftest suite, so **uncaught means no committed fixture's verdict depends on that guard — a selftest-coverage gap, not an equivalence claim**. Each triple is asserted to edit the counter exactly once, so none silently mutated the wrong line. Guard readings below are static, from the harness triples (line numbers in `corpus/instruments/r47-mutbat.py`); survival = the 43-fixture suite contains no red tree shaped for that guard.

C1 survivors (16):

| ID | Guard weakened (r47-mutbat.py) | Fixture gap the survivor discloses |
|---|---|---|
| L2d-notebullet-loose (:58) | capture-directory-note bullet check disabled | no fixture drops the round-46-a2 note bullet alone |
| L3c-third-clip-dropped (:60) | Corrections tail need not name Search log/Registry changes | no fixture has SOURCES.md+fence but no section name — **the live integrated tree is exactly this shape (see §2)** |
| L4b-chrome-ignored (:63) | `chrome` marker check disabled | no fixture omits the chrome marker |
| L5a-order-ignored (:65) | order false-phrase rejection disabled | fixtures remove material; none restores FALSE_PHRASES[2] |
| L5b-corrected-loose (:66) | corrected-order sentence optional | no fixture drops just that sentence |
| L6b-twocase-loose (:69) | "two cases" requirement disabled | no fixture drops just the two-case phrase |
| L7a-one-name-only (:71) | one dropped-finding name suffices | no fixture names only one erratum |
| L7b-keyword-loose (:72) | erratum keyword regex matches anything | no fixture has the section with neither name |
| L8a-supersede-loose (:74) | supersedes-S074 row cell unchecked | no fixture alters that cell |
| L8c-recheck-ignored (:76) | S076 source-recheck subprocess result unchecked | no fixture breaks recheck output beside a valid row |
| L8d-cells-loose (:77) | 11 required row cells → ≥9 | no fixture ships a 9/10-cell S076 row |
| L9a-oldcite-ignored (:78) | S074.txt old-citation count disabled | no fixture keeps 59 old citations in a green tree |
| L9b-range-loose (:79) | quote span/range binding dropped | no fixture places a quote outside its claimed range |
| L10a-url-loose (:81) | REST-API page URL loosened to docs.github.com | no fixture carries a non-REST docs lead bullet |
| L10b-bullet-loose (:82) | `- ` lead-bullet shape unchecked | no fixture has a non-bullet lead line |
| L11a-zdi-only (:84) | reservation disposition word unchecked | no fixture has a ZDI note without reservation text |

C2 survivors (18):

| ID | Guard weakened | Fixture gap |
|---|---|---|
| H1a-counts-loose (:91) | 30 rows/admitted exact → ≥ | no 31+-row fixture |
| H1b-raw-loose (:92) | exactly-one raw block → >1 tolerated | no multi-raw fixture |
| H1c-src-boundary (:93) | `\bS075\b` → substring | no S075-prefix-token fixture |
| H2a-verified-loose (:94) | exact `verified-at: <ts>` → startswith | no extended-header fixture |
| H2b-wordfloor-low (:95) | section word floors 25/12 → 5/1 | no thin-section fixture |
| H2c-need-empty (:96) | required cross-reference name set emptied | no missing-xref fixture |
| H3a-cells-loose (:97) | S075 row 11 cells → ≥9 | no 9/10-cell row fixture |
| H3c-kind-dead (:99) | kind `docs` → also `Docs` | no wrong-case kind fixture |
| H4b-quotes-low (:101) | ≥8 located quotes → ≥1 | fixtures are all-10 or broken; no 1–7-quote fixture |
| H4c-distinct-dropped (:102) | pairwise-distinct quote texts unchecked | no duplicate-quote fixture |
| H5a-span-wide (:103) | anchor span ≤11 → ≤110 lines | no in-window/out-of-span anchor fixture |
| H5b-words-wide (:104) | 25-word quote cap → 250 | no long-quote fixture |
| H5c-pass-low (:105) | ≥4 passing sections → ≥1 | no 1–3-passing-section fixture |
| H6b-pin-dropped (:107) | base-knowledge content pin dropped | no altered-pinned-knowledge fixture |
| H6c-size-low (:108) | knowledge file ≥3000 bytes → ≥3 | no tiny-file fixture |
| H7a-verdict-or (:109) | census rc==0 AND ok-line → OR | no rc≠0-with-ok-line fixture |
| H7b-symlink-dead (:110) | census-input symlink rejection deleted | no symlink fixture |
| H7c-okline-loose (:111) | `\S+\tok\t` → `\S+\tok` | no tab-less ok-prefixed stdout fixture |

Disclosure honesty checks pass: no survivor is called equivalent (`equivalent=0` in both receipt summaries; claims.json `mechanical_limits` and `freeze.txt` line 1 say "disclosed … not called equivalent"); wave1's six fresh C1 and six fresh C2 mutants (`w1/R47MutC1b.md`, `w1/R47MutC2b.md`) add uncaught cases **without** erasing the pre-freeze 34 (lesson `corpus/lessons/round-47.md` §Wave-1; corroborated `w2/R47W2AdmissionLanguage.md:46`). Also verified static: the frozen H4 docstring/code mismatch ("≥7 distinct anchors" docstring at `r47-f30-gate.py:44-45` vs `>= 5` at :313) is disclosed, not amended (`counter-errata.md` §Pre-freeze implementation/documentation mismatch).

## 4. Wave1 false greens (static report reading; receipts verified present; counters verified unchanged)

- **C1 (`w1/R47RevCounterC1.md`)**: attack A wraps all rendered SOURCES.md content in one multiline HTML comment — frozen counter still prints 11/11 exit 0 (L2/L8/L10 consume commented bytes); root causes cited at `r47-routed-defects.py:96-110` (same-line comment strip only), `:122-138` (no comment state), `:300-309`. Attack B fences both lesson files and hides the corrected F29 entry in a comment while visibly asserting the false claims — again 11/11, `L9 spans=47 located=47` from hidden quotes (raw-token scans `:176-183`, `:190-223`, `:226-231`, `:270-297`, `:312-318`). Do-nothing base control 0/11, positive control 11/11, `identity.json` pins counter sha e6ede7b6… = freeze pin (verified against §1). Receipts exist: `w1/R47RevCounterC1.draft/attack-A{,.txt}`, `attack-B{,.txt}`, `do-nothing-base.txt`, `green-control.txt`, `identity.json`, `probe.py`.
- **C2 (`w1/R47RevCounterC2.md`)**: a U+2060 (word-joiner) dressed duplicate F30 row passes 7/7 — the normalizer at `r47-f30-gate.py:169-176` strips only U+200B/C/D/FEFF and the strict parser `:159-166` sees only ASCII digits next to `F`; and a hostile ` <!-- ; echo HOSTILE_TOKEN -->` appended to the canonical recheck line passes 7/7 because `:224` validates the comment-sanitized text (`live_lines` `:143`) rather than raw bytes (`:109-111` exact-form check bypassed). Its do-nothing control is honestly labeled a **synthetic positive fixture**, not the red base control. Receipts exist: `w1/R47RevCounterC2.draft/word-joiner-duplicate.txt`, `hostile-recheck-comment.txt`, `results.json`, `probe.py`, `control-entry.md`, `mutations.txt`.
- Both reviewers explicitly changed nothing ("Counter source was not changed"), matching §1's byte proof: **the false-green classes are disclosed, unresolved, and present in today's bytes.** The recommended rendered-content representation/normalization repairs exist only as prose in those reports; adopting them is the integration owner's authorized act, must preserve freeze identity, and must be logged as a re-derivation — it can never retroactively validate the original frozen predicates.

## 5. Strongest counterexample and what the canonical judge must reject

- **Counterexample to "C1 closed mechanically at integration":** executed replay, §2 — `git archive 65e19bd` + the frozen counter exits 1 at `fixed=10/11`, L3 `content=0`, cause hyphenation at `corpus/lessons/round-46.md:155`. The strongest *counterfactual* repair is the one-line un-hyphenation; it is safe, faithful to the headings, and changes no frozen bytes — but until an integration owner lands and logs it, C1 is below its own frozen mechanical bar, not merely semantically incomplete.
- **Counterexample to any frozen-validation claim from post-score evidence:** none can exist — bytes prove no post-score instrument change (§1), and the wave1 hostile trees would false-green the byte-identical counters today. Any statement like "the counter now validates rendered content" is false provenance: the counter never gained that power.
- The canonical judge should **reject**: (a) any claim that integrated `11/11` (after the one-line fix) equals C1 met — the frozen S074 disposition and the false-green classes remain; (b) any equivalence or saturation claim over the 34 survivors (or the 8 wave1 additions); (c) any counter "repair" presented without a counter-errata re-derivation that does not reuse the counter. **Accept**: C2's 6/7 as the honest, documented shape of an unmet target; the 10/11 reading as a finding, not a mandate to reroll either frozen target.

## 6. Verification boundaries

Executed: 30 sha256 computations (10 files × 3 revisions), 4 counter invocations on 2 scratch checkouts, 1 predicate test, 2 set comparisons, arithmetic checks. Not executed (per seat bounds): mutant battery, selftests, base-export replay (committed receipts relied on: `controls/freeze-check.txt`, `w1/R47RevCounterC1.draft/do-nothing-base.txt`), live recapture, any run of w1 hostile fixtures. Static: survivor guard semantics, w1 false-green mechanics (line cites from the committed counters, which are byte-verified). Scratch `/fast/scratch/hyaku/kasegi-r47/R47W2FrozenLimits/` deleted after receipts were saved. No tools installed or updated (none needed); pacman transactions untouched; no service restarts.

Report: `.ufo/waves/round-47/w2/R47W2FrozenLimits.md`; receipts `.ufo/waves/round-47/w2/R47W2FrozenLimits.bytes.txt`, `.replay.txt`, `.l3.txt` — all relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
