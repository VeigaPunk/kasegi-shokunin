# ConnectorOverlap — kasegi round 79, wave w1 (13 seats), attempt 1

Read-only cross-lane overlap scan. No lane file, no frozen byte, no sibling tree was modified.
Lane root `/home/vgpnk/Projects/shokunin/kasegi-shokunin`; freeze `9d0b1eb0709e47c3c6decc09138b5012a8968924`,
base `d16d2124fd5262f5a8088aa598f1e628f897d3ab`.
Axes named: **depth:verifiability** (C1) and **coverage** (C2).

Commands run (all read-only, cwd `/home/vgpnk/Projects/shokunin`):

```
for d in */; do grep -rn -i -E 'determineversion|indexer-api-caller|osv-indexer' "$d/corpus"; done   # item 1, exact spec scan
for d in */; do grep -rnai --include=*.md --include=*.json --include=*.txt --include=*.py --include=*.sh \
  -E 'determine[_ -]?version|v1experimental|indexer-api-caller|osv-indexer' "$d"; done              # item 1, widened
for d in */; do grep -n -i -E 'equivalent mutant|equivalent-mutant|mutant equivalence' "$d/corpus/QUALITY.md"; \
  grep -rn -i ... "$d/corpus/lessons"; done                                                          # item 2
grep -n -i 'non-equivalent' */corpus/QUALITY.md                                                     # item 2, rule form
awk '/^kasegi \|/{printf "%d\t%s\n", NR, substr($0,1,110)}' .ufo/l0-questions.md                    # item 4
```

---

## 1. Cross-lane term scan (`determineversion | indexer-api-caller | osv-indexer`)

**Result: zero hits in every sibling lane's `corpus/`.** 20 sibling lanes were scanned (all `*-shokunin`
except kasegi). No lane, no file, no line. The widened scan over whole sibling trees (including
`.ufo/`) returned only the rows below.

| lane | file:line | kind | verdict | recommendation |
|---|---|---|---|---|
| kaidoku | `.ufo/waves/round-65/w1/SentinelProvenance.md:100` (and `census-at-freeze.json:40`) | string `determine_versions.py` names a **cloned third-party repo's** network-fetching script in a provenance audit ("carries `build_versions_batch*.py` / `determine_versions.py` that would fetch from the network — they are present but nothing in the closure executes them") | **non-overlap** — same words, unrelated artifact; not OSV, not a corpus claim, outside `corpus/` | none |
| kaidoku | `corpus/SOURCES.md:21` (S015) — "OSV CVE-2025-55305 record — `https://api.osv.dev/v1/vulns/CVE-2025-55305`" | same vendor (OSV.dev), **different endpoint** (`/v1/vulns/<id>` dataset read vs F55's `POST /v1experimental/determineversion`), tier A **dataset** row, no endpoint-contract knowledge | **adjacent, not duplicate** — kaidoku owns "read one advisory record"; kasegi's S113 scopes itself to the determineversion endpoint only (`corpus/SOURCES.md:125`: "not the single-query or batch query contracts … not the OSV record format … not the API overview page") | keep F55 as written; do **not** widen the S113 scope sentence to "the OSV.dev API", which is the only way this could collide |
| kotodama | `corpus/knowledge/linguistics/syntax-typology.md:11,32` | `OSV` = object–subject–verb word order | **false positive** (substring) | none |
| kengaku | `corpus/SOURCES.md:293,358`; `corpus/lessons/round-100*.md` | `file_hashes` is a pytest variable in a Terminal-Bench grader | **false positive** | none |
| kasegi (in-lane, not cross-lane) | `corpus/knowledge/osv-post-v1-query-contract.md`, `osv-post-batch-query-contract.md`, `osv-affected-range-events.md` | the three admitted OSV.dev entries | the B6 distinctness surface is in-lane | covered by C2/B6; no action for this seat |

**Coverage verdict: F55 is unique across the fleet.** No sibling lane holds a claim on C/C++ source-hash →
library/version determination, and none holds the OSV.dev endpoint family at contract depth.

---

## 2. Does a sibling already hold "a required kill must be non-equivalent"?

**Yes — three siblings hold it, one in a stronger (ex-ante, set-level) form.**

| lane | file:line | quoted clause |
|---|---|---|
| mori | `corpus/QUALITY.md:2307` (criterion 205) | "A mutation battery's kill claim names its **non-equivalent mutant set** … **equivalent mutants are declared separately, not counted**." |
| chousa | `corpus/QUALITY.md:958` (criterion 107) | "**A frozen mutant set holds no equivalent mutant**; a survivor is classified before the target is fixed … a survivor the landed builder cannot kill is a **mutant-set defect, never a data result**." |
| souji | `corpus/QUALITY.md:122` (Q53) | "**Every listed non-equivalent mutant must be killed**; equivalents name their pinned-inventory assumptions. State adequacy 'of N listed mutants', never exhaustive." |
| mado | `corpus/QUALITY.md:391` (criterion 72) | "a one-site patch over a two-site property **is an equivalent mutant**, and it is either repaired to remove the surviving site or declared equivalent beside the declaration that names the surviving site …" |
| kengaku | `corpus/QUALITY.md:441` | "an equivalent mutant found later is reported as **a limit of the freeze, never removed**; a kill records a result difference, not a reason" |
| tabi | `corpus/QUALITY.md:875` (criterion 115) | "A counter that reads a producer's own verdict must carry **BOTH polarity negatives** … and the **exact source line** that combines them must be **mutated and run through the production CLI**. A selftest that never makes the two disagree cannot kill an `&&`→`||` weakening." |

Two separate facts, both relevant to this round:

1. **The equivalence rule is fleet-converged** (mori 205, chousa 107, souji Q53, mado 72). No sibling holds
   r79's exact ordering ("a *named required kill* must *first* be shown non-equivalent"), but chousa 107
   dominates it: it puts the burden on the **set** before the target is fixed, which is strictly stronger
   and is the same failure r79 names (a required row no harness can kill).
2. **tabi 115 is the closest prior art to r79's C1 *mechanism***, not to M79-1: both-polarity predicate
   tests plus the mutated exact line run through the production CLI is r79's "gate-predicates" limb.
   Kasegi's C1 pays for that mechanism locally; it is not a novel fleet concept.

**Verdict:** corroboration only. These are lane-local QUALITY tables grounded in each lane's own receipts;
kasegi's R-table is grounded in kasegi evidence. Sibling convergence may be cited as independent
corroboration in the lesson, never as the criterion's ground, and never as a reason to skip the lane's own
show-able-to-fail pair.

---

## 3. The lane's own prior equivalence concept — does M79-1 duplicate it?

**It duplicates it at two layers, and the duplicate is sharper than the mistake text says.**

Committed prior art in this lane:

| artifact | quoted content |
|---|---|
| `corpus/instruments/r46-mutant-equivalents.json` | 7 ids → proof paths: `M14-L6-exit-ignored`, `G6b-integrity-loose`, `G7a-verdict-or`, `G7c-okline-loose`, `H1b-raw-loose`, `H7a-verdict-or`, `H7c-okline-loose` |
| `corpus/instruments/r46-mutant-equivalents/README.md:1,3-6` | "Each proof argues that the named single-edit mutant of the round-46 counter **cannot change any verdict on any input tree**, so the committed selftest cannot catch it and the battery's `equivalent` classification is the honest reading. **Falsifying any proof** (constructing an input class where the mutated clause flips a verdict) **kills the equivalence and with it the claim.**" |
| `corpus/instruments/r46-mutbat.py:11,35,378,362-363` | verdict map "`equivalent`  the mutant id carries a committed proof in `--equivalent` (JSON: id -> path)"; `--equivalent MAP.json`; **default** `--equivalent corpus/instruments/r46-mutant-equivalents.json` |
| `corpus/instruments/README.md:378,961` | control `CONTROL CTL-equivalent verdict=survivor expected=survivor ok=y`; "`CTL-equivalent` (a comment-only patch no probe can see: `survivor` …)" |
| `corpus/QUALITY.md:96` (R17) | "An instrument limb is claimed load-bearing only when a committed one-limb mutant makes that limb's **kill command differ from the unmutated run** … rejects all three degenerate controls (no-op patch, non-compiling patch, **semantically equivalent patch**) … **a survivor is never relabelled killed**." |

**Verdict: M79-1 is a partial duplicate, and the non-duplicated part is the ordering, not the concept.**

- *Duplicated:* the observable-difference test (R17: "kill command differ from the unmutated run"), the
  classification object (a named mutant in a kill table), the evidence form (differential over input
  classes, `r46-mutant-equivalents/m14-equivalence-differential.py`), and the falsification condition
  (README:1-6). A new criterion phrased "a named required kill must first be shown non-equivalent" without
  naming these is a **second convention for one concept** — the defect this lane's R-table already
  penalises elsewhere.
- *Not duplicated:* the **precondition ordering** at the frozen-claim layer (test before the kill is
  counted) and the case r78 hit — a required row whose transform is structurally invisible to the harness,
  where the honest reading is "rebuild the mutant or the harness", not "declare equivalent and exempt".
  That part is held in siblings (chousa 107, souji Q53) but **not** in kasegi's QUALITY.
- *Wording risk in the mistake text:* `## Mistakes` M79-1's captured-by reads "QUALITY R127 asks for an
  assertion kill but **never asks whether the transform is observable**". That is true of R127
  (`corpus/QUALITY.md:579`: "Distinguish mutation assertion failures from runtime exceptions…") but false
  lane-wide — **R17 asks exactly that, at the limb layer**. The lesson must scope it: *R17 asks at the limb
  layer; no criterion asks at the frozen-kill-table layer; r46's `--equivalent` map holds the classification
  but no QUALITY criterion binds a claim's required rows to it.* Otherwise the mistake overstates the gap
  and the proposed criterion looks like a re-derivation.

**The sharpest measured fact (routed defect candidate, not a verdict change):** the counter that judges this
round cannot express the class M79-1 names.

```
$ grep -c equivalent .ufo/waves/round-79/c1/mutbat.py
0
$ grep -n 'KILLED\|SURVIVED\|DIRTY\|NOT-DERIVED' .ufo/waves/round-79/c1/mutbat.py | head -4
9:  KILLED          exit != 0, at least one 'selftest case=... FAIL' line, no 'Traceback'
12:  SURVIVED        exit 0
13:  DIRTY           exit != 0 without a FAIL line, or with a 'Traceback'
14:  NOT-DERIVED     the anchor does not occur exactly once in the target
```

`r46-mutbat.py` carries an `equivalent` verdict with a committed proof map and a default path;
`.ufo/waves/round-79/c1/mutbat.py` carries four verdicts and **no equivalence class at all**. Every one of
the 19 table rows (`K-M1, K-M2, K-M3, K-M4, K-M5, K-X1, K-X2a, K-X2b, K-M8, K-W1, K-W2, K-N1, K-P1, K-P2,
K-G1, K-C1, K-NP, K-CL, K-T1`) carries an `expect` field, so the class is **empty by construction, not
observed**. Two consequences worth the L1's attention:

1. A **composite or residual transform** proposed by an attack seat will read `SURVIVED`/`DIRTY`, never
   `equivalent` — the correct reading under C1's kill rule ("mutants outside the table … are routed
   findings, not verdict changes") but the *wrong* diagnostic label for an equivalent one.
2. A criterion that requires non-equivalence **cannot fail on this artifact**: 19/19 killed entails "none
   equivalent", so the criterion is vacuously green. It needs a positive control drawn from the lane's own
   committed equivalents (`M14-L6-exit-ignored` etc.), not the r78-K-X2 → r79-K-X2b pair — that pair shows
   the *successor kills*; it does not show the *criterion firing*.

---

## 4. Open kasegi L0 questions (`.ufo/l0-questions.md`, 378 lines)

The file is append-only with the header shape `<lane> | round-<N> | <question>` and **no status column**.
No kasegi line records a ruling (the only resolution marker in the file is `:77` — `tabi | round-19 |
RESOLVED-BY-RULING`). **All 25 lines naming kasegi are therefore open as written**, in five clusters:

| cluster | lines | note |
|---|---|---|
| Host / fleet / dispatch contract | **1, 10, 16, 39, 175, 217, 218, 246** | `1` bounties interactive-rebase stall; `10` bounties root vanished; `16` second in-round source loss; `39` round-namespace + craft-dispatch reconcile; `175` cap-deferred `wave1.ready`; `217` WAVE-DONE handoff; `218` two concurrent L1 attempts (authority); `246` prompt-fidelity D53-3 / L2 floor |
| Instruments / gates | **209, 269, 273, 279, 293, 315, 340, 354** | `269`+`273` are one question (`273`: "Re-asked (the round-57 row is unanswered)"); `279`+`293` are one question narrowing the figure-audit derive-gate boundary; `209` 22 gated recheck lines; `315` recheck value execution in a counter; `340` frozen S111 Q01 quote (9 chars) → `source-recheck.py` exit 2; `354` = **R-77-D** anchor-window semantics |
| Assimilation / id collision | **307, 308, 328, 341, 353** | one question, five filings (staged `shokuknow/merge/kasegi/SOURCES.append.md` id drift); `308` says it plainly: "round-70 row above still open, no answer"; `353` = **R-77-E** (staged S112 vs the lane's S112 OSV row) |
| Province / scope / ownership | **189, 222, 225** | `189` RFC 9116 overlap with kake; `222` citation-ground residue ownership (79 unopenable citations in sibling-owned lessons); `225` Windows-host recheck portability |
| C2 target amendment | **313** | r72 C2 target clause `api_key` falsified; `claims-amendment-c2.json` awaits accept/reject |

Consolidated distinct questions: **~19** from 25 filings. Nothing in this round's C1/C2 depends on any of
them; C2's S113 row is a new registry id (113) and does not touch the staged package, so the `353` collision
does not recur. **R-77-D / R-77-E remain open** and r79's `routed_not_claimed` records exactly that.

---

## 5. Contradictions stated, not smoothed

1. **M79-1's premise vs. its own captured-by.** The mistake's claim "no criterion asks whether the transform
   is observable" is true of R127 and **false** of R17 (`corpus/QUALITY.md:96`). Both cannot be stated as-is.
2. **One concept, three mechanisms.** The lane now has: R17's differ-test (limb layer), the r46 `--equivalent`
   proof map (battery layer), and the proposed M79-1 precondition (claim layer). Adding the third without
   binding it to the second manufactures a two-convention defect in the exact area the round is claiming.
3. **A criterion that cannot fail is not evidence.** On a 19/19-killed table with an empty equivalence class,
   "all required kills are non-equivalent" is entailed by the kill count. The criterion's red state must come
   from a committed equivalent row, not from the r78 survivor.
4. **tabi 115 vs. kasegi C1.** The both-polarity + mutated-exact-line mechanism is prior fleet art. Kasegi's
   gain is the local kill set (19 rows, K-X2a/K-X2b), not the mechanism; the lesson should not present the
   mechanism as new.

---

## Bounded proposal (one move; FSD connector)

**Move: make M79-1's criterion a *binding* to the lane's existing equivalence mechanism, and give it a red
state the lane already owns.**

Three edits, all in the L1's hands (this seat writes only this file):

1. **Criterion text** names the mechanism instead of restating the concept: non-equivalence for a named
   required kill is established by (a) the r46 differential form — same input classes, byte-identical
   readings ⇒ equivalent (`corpus/instruments/r46-mutant-equivalents/m14-equivalence-differential.py`,
   `.../README.md:3-6`) — or (b) a committed proof in `corpus/instruments/r46-mutant-equivalents.json` routed
   through `r46-mutbat.py --equivalent` (default at `:378`). No assertion, and no second map.
2. **Show-able-to-fail pair replaced/extended**: the red state is a counter that reports
   `M14-L6-exit-ignored` as killed when the proof says it cannot differ — i.e. run `r46-mutbat.py` with a
   table containing that id and a `--equivalent` map that omits it; the criterion must be able to see the
   misclassification. (The r78-K-X2 → r79-K-X2b pair stays as the *fix* evidence, not as the criterion's
   falsifier.)
3. **Declare the empty class** in the lesson rather than leaving it implicit: the 19-row table holds no
   equivalent row by construction (each row's transform changes printed output, which the `KILLED` verdict
   demonstrates), and `.ufo/waves/round-79/c1/mutbat.py` has no `equivalent` verdict — so a future composite
   or residual transform reads `SURVIVED`, and is a routed finding, never an exemption.

- **Affected axes:** `depth:verifiability` up — the criterion acquires a mechanism, a red state, and a stated
  limit inside the lane's own committed evidence; no new instrument, no new pin. `coverage` unchanged (no
  corpus byte, no registry row, S113 untouched).
- **Harm check:** no frozen byte edited; no row added to or removed from the 19-row table (C1's kill rule
  forbids it); no sibling tree touched; the C1 predicate P3 (`killed=19`) is not affected by the criterion
  text.
- **Risks:** (i) the criterion could be misread as re-scoring C1 — it must not change P1-P7; (ii) phrasing it
  without the `--equivalent` pointer invites a second equivalence mechanism (the very defect class); (iii)
  the `equivalent` label's absence from the r79 counter makes an equivalent composite read `SURVIVED`, so the
  lesson must state that "routed finding" ≠ "kill" ≠ "equivalent".
- **Verification (L1 runs, read-only):**
  `grep -c equivalent .ufo/waves/round-79/c1/mutbat.py` → `0`;
  `grep -n 'equivalent' corpus/instruments/r46-mutbat.py` → `:11,:35,:378` present;
  `python3 corpus/instruments/r46-mutbat.py --root <tree> --pure <pure> --work <scratch> --equivalent corpus/instruments/r46-mutant-equivalents.json`
  reports a non-zero `equivalent=` term on the counters whose ids are in the map (currently 7 ids), and never
  `uncaught` for them;
  `python3 colordiff`-free diff of the r46 README proof text against the criterion's mechanism clause returns
  no contradictory claim.

---

## Files written

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-79/w1/ConnectorOverlap.md` (this file)

No other file was created or modified. Scratch `/fast/scratch/hyaku/kasegi-r79/ConnectorOverlap` removed
before yield.
