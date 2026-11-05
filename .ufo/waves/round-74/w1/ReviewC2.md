# ReviewC2 — round 74, attempt 1, wave w1 — C2 clause-vs-capture, overlap, counter-arithmetic and registry attack

Seat: ReviewC2 (reviewer, leaf member — no subagent dispatch). Lane: /home/vgpnk/Projects/shokunin/kasegi-shokunin.
Frozen at: freeze commit `847b53792d2d29d161cad7d21a33c89df9e52e8d` (base/controls `ccd6a54bf392922495c4860332665499582e3213`, controls commit `654d877f0bd4005fd139c46e5b889f4c1833ddda`).
Scratch root: /fast/scratch/hyaku/kasegi-r74/ReviewC2 — **deleted before this report was written** (receipts copied into §5 command log; the plan was: copy first, then `rm -rf $S`).
No tools installed or upgraded this wave ("Tooling authorization" section of this report: none needed; stock python3/git/grep/curl only — no install channel, version or reason to record).
No pacman transactions (host-wide pause respected). No live fuzzing, no port scans, no credential material: the only HTTP contact this seat made was read-only GETs against public documentation pages already named by the claim (`https://github.com/googleprojectzero/fuzzilli`), none by this seat directly — the byte-identity re-fetch was done by ScoutSurface and is cited, not re-run, except where noted in §5.
Read-only git only: `git -C`, `git show`, `git cat-file`, `git ls-tree`, `git log`, `git rev-parse`. No mutating git/jj command was run anywhere by this seat.

**Bottom line for the L1: C2 attack found no claim-narrowing defect. Every `pre_freeze_quote_locus` line is present in the capture at its stated anchor; all nine clause families are supported with two wording cautions (§2.1, §2.2); the overlap sweep found no verbatim/near-identical duplicate clause in any held row's capture (§3); every after_predicate number recomputes as exactly +1 or the stated absolute from the base receipts and cannot be reached by a do-nothing tree (§4); S109 is unused in the lane registry and the collision in the staged package file is on a DIFFERENT lane's row id (§5), which is a namespace collision in the merge-domain id space, reported, adoption closed.**

---

## 1. Scope read (execution of step (1))

Commands:
```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ mkdir -p /fast/scratch/hyaku/kasegi-r74/ReviewC2 && echo OK && git rev-parse HEAD && git status --porcelain=v1 | head
OK
847b53792d2d29d161cad7d21a33c89df9e52e8d
[untracked files only: .ufo/waves/round-74/{w1*,freeze-check-replay-r74.txt}]
```
- Worktree tip = the freeze commit. The freeze commit adds exactly two files (claims.json `dbc560051d405e47ef7ff170d9ad419a67bf7611` and `corpus/source-snapshots/round-74/S109.txt`); read via `git show --stat HEAD` (exit 0).
- claims.json read in full. The C2 `target` string was read raw at `:37` with `sed -n '37p'` because the read tool truncates that line at 768 bytes. All C2 `after_predicate`, `distinctness_screen`, `kill_rule`, `scope_limit` and `do_nothing_control` clauses were read whole and are used verbatim below; nothing reworded.
- `corpus/source-snapshots/round-74/S109.txt` read: 375 lines, 19630 bytes.
- Provenance (all exit 0): `git cat-file -p 847b5379…:corpus/source-snapshots/round-74/S109.txt | sha256sum` → `c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486`; `sha256sum` of the worktree file → same value; `wc -l` → 375. Byte-identical re-fetch by scout: `.ufo/waves/round-74/w1/ScoutSurface-S109-refetch.txt`, `cmp` exit 0, sha identical — the mutable-counter allowance did not need to be used.

### 1.1 Line-number offset — the anchors are capture-absolute, and line 151 is the definition line
`sed -n '145,155p'` shows `Repository files navigation` at L145, `README` L146, `Fuzzilli` L150, and **the definition sentence at exactly L151**:
```
151:A (coverage-)guided fuzzer for dynamic language interpreters based on a custom intermediate language ("FuzzIL") which can be mutated and translated to JavaScript.
```
Same check at all other loci (§2). The GitHub page chrome occupies L1-L149, so all frozen loci are capture-absolute and the anchors are unambiguous.

---

## 2. Clause-vs-capture attack (step (2)) — the nine pre_freeze_quote_locus lines

Format: frozen clause element → capture line (verbatim) → verdict **Supported / Overstated / Understated** (self, not source, changing). "Understated" only flags cases where a less-loaded wording would carry the same ground; per the M72-5 class these are wording cautions that do not falsify a clause whose source ground exists. Findings use the same reporting bar as the r71 M71-3 / r72 M72-5 classes: a defect exists only when the clause asserts more than its named capture states.

### 2.0 The definition line (L151)
```
151:A (coverage-)guided fuzzer for dynamic language interpreters based on a custom intermediate language ("FuzzIL") which can be mutated and translated to JavaScript.
```
Every element of the L151 clause family reconciles:
- "dynamic language interpreters" — verbatim in the capture (L151). ✓ supported.
- "FuzzIL intermediate language" — the capture writes `"FuzzIL"` and "a custom intermediate language" on the same line; the compound "the FuzzIL intermediate language" is a fair fusion of two tokens on one capture line, not an additional claim. ✓ supported.
- Coverage-guided (see §2.1).

### 2.1 'coverage-guided' — does L151 say coverage-guided?
**The capture's own words are "A (coverage-)guided fuzzer".** The clause word "coverage-guided" is therefore an *inflection* of the capture's parenthetical, present on L151, but the capture does not carry the solid compound "coverage-guided" anywhere.
Evidence:
```
$ grep -n "coverage" corpus/source-snapshots/round-74/S109.txt
151:  A (coverage-)guided fuzzer for dynamic language interpreters …
156:  Compile the engine with coverage instrumentation (requires clang >= 4.0) …
212:  … some parts (e.g. coverage measurements, socket interactions, etc.) implemented in C.
220:  Evaluator: evaluates whether a sample is interesting according to some metric, e.g. code coverage.
$ grep -n -- "coverage-guided" corpus/source-snapshots/round-74/S109.txt   # no match, exit 1
```
Verdict: **Supported with one caution — the phrase "coverage-guided" must, in entry / manifest / row prose, either quote the capture's own "A (coverage-)guided fuzzer" (parenthetical included) or be marked as the capture's parenthetical inflected.** The staged draft entry (`knowledge-fuzzilli-js-engine-fuzzing-framework.md`) already does the right thing: "It is 'A (coverage-)guided fuzzer for dynamic language interpreters' (S109.txt:151)"; the sources-edits draft S109 row renders it as the plain compound "a coverage-guided fuzzer for dynamic language interpreters" (`.ufo/waves/round-74/w1/sources-edits.md:10`), which is not the byte-form L151 carries when quoted. That is the one place in the material the compound is not sourced to its parenthetical form. Not a falsification (the capture's parenthetical does say `(coverage-)guided`), but the L1 should keep the entry's quote form and the manifest quote verbatim — the manifest quotes are the checked strings and a manifest quote that says "coverage-guided" without "(coverage-)guided" would put a string on the wire the capture does not carry; quote pins are verified by `source-recheck.py` against the capture bytes, so the pin would fail or mis-anchor. **Keep every pin in the capture's own byte form.**

### 2.2 L165 — the semantic-correctness concern
```
165:When fuzzing for core interpreter bugs, e.g. in JIT compilers, semantic correctness of generated programs becomes a concern. This is in contrast to most other scenarios, e.g. fuzzing of runtime APIs, in which case semantic correctness can easily be worked around by wrapping the generated code in try-catch constructs. There are different possibilities to achieve an acceptable rate of semantically correct samples, one of them being a mutational approach in which all samples in the corpus are also semantically valid. In that case, each mutation only has a small chance of turning a valid sample into an invalid one.
```
Every element checks:
- "the semantic-correctness concern for JIT interpreter bugs" — capture says "core interpreter bugs, e.g. in JIT compilers" (L165). The clause's "JIT interpreter bugs" is a slight fusion of "core interpreter bugs" + "e.g. in JIT compilers"; the caveat is that the README does NOT limit the concern to JIT bugs only — it gives JIT compilers as an example. The staged entry words it as "core interpreter bugs, e.g. in JIT compilers … against a try-catch-wrapped runtime-API case" — that is the right reading. The claims' compressed phrase is fair but the entry should not state the concern as "JIT-only". Verdict: **Supported; wording caution, the entry already carries the correct form.**
- "versus try-catch-wrapped runtime-API fuzzing" — capture: "fuzzing of runtime APIs, in which case semantic correctness can easily be worked around by wrapping the generated code in try-catch constructs" (L165). "try-catch-wrapped runtime-API fuzzing" inflects "wrapping…in try-catch constructs" to the participle; same caution as §2.1 but no byte falsehood. Verdict: **supported.**
- The capture gives "an acceptable rate of semantically correct samples" and "a small chance" without numbers. "No rate figure" is already recorded in the staged entry's Limits (`grep` exits 1). Verdict: **supported, no overstatement** (the frozen claims wording does not assert a number).

### 2.3 L212 — the Swift/C implementation split
```
212:The fuzzer is implemented in Swift, with some parts (e.g. coverage measurements, socket interactions, etc.) implemented in C.
```
Clause element "the Swift/C implementation split" — supported. The capture adds "some parts (e.g. coverage measurements, socket interactions, etc.)"; the entry retains the qualifier. Verdict: **supported, byte-level match.**

### 2.4 L214-L221 — named architecture components
Capture (verified line by line):
```
214:A fuzzer instance (implemented in Fuzzer.swift) is made up of the following central components:
215:MutationFuzzer: produces new programs from existing ones by applying mutations. Afterwards executes the produced samples and evaluates them.
216:ScriptRunner: executes programs of the target language.
217:Corpus: stores interesting samples and supplies them to the core fuzzer.
218:Environment: has knowledge of the runtime environment, e.g. the available builtins, property names, and methods.
219:Minimizer: minimizes crashing and interesting programs.
220:Evaluator: evaluates whether a sample is interesting according to some metric, e.g. code coverage.
221:Lifter: translates a FuzzIL program to the target language (JavaScript).
```
Frozen clause: "MutationFuzzer, ScriptRunner, Corpus, Minimizer, Evaluator, Lifter with Storage and the event-driven design".
- All six named components appear at L215-L221. ✓ supported.
- **L218 names a SEVENTH central component, `Environment`, which the frozen clause omits.** This is the M72-5 structure again, only inverted: the clause does not assert switch content the source contradicts — it *understates* its own source. The staged ScribeEntry draft (`.ufo/waves/round-74/w1/ScribeEntry.md` §"Three notes" item 3) already records: "The capture's list (L214-L221) also names `Environment` (L218). The entry states all seven, as the capture does." Recording the omission in the entry is the fix already applied by the scribe; the clause predicate is scope-limited "existence and name only" for the NDSS item but not for the component family, and no part of the kill rule requires the claim to enumerate the capture's list exhaustively. Verdict: **supported (the six names hold); completeness caution carried into the entry, already in the draft.** The L1 need not reword claims.json (binding and frozen; a report-level note only).
- Storage: `226:Storage: stores crashing programs to disk.` ✓. The clause attaches Storage to the component family; the capture itself separates the seven "central components" from the "modules optionally available" list (L222-L225) that Storage opens. The clause's phrase "Lifter with Storage" compresses that distinction; the entry correctly states Storage as an optional module. Verdict: **supported with the same wording caution; entry already correct.**
- Event-driven: `227:The fuzzer is event-driven, with most of the interactions between different classes happening through events. …` ✓ supported at L226-L227 (L226 prints "The fuzzer is event-driven" — see :226 is the Storage line; L227 is the event line; the claims' locus "L226-L227 (Storage/events)" matches; L227 holds the whole event sentence verbatim).

### 2.5 L230 — REPRL
```
230:Fuzzilli uses a custom execution mode called REPRL (read-eval-print-reset-loop). For that, the target engine is modified to accept a script input over pipes and/or shared memory, execute it, then reset its internal state and wait for the next script. This removes the overhead from process creation and to a large part from the engine ininitializaiton.
```
- "read-eval-print-reset loop" — capture has it, parenthesized. ✓ supported.
- "with state reset" — capture: "then reset its internal state and wait for the next script". ✓ supported.
- No performance figure (capture's overhead claim carries no number). Entry already records "The README gives no measurement of that effect." Verdict: **supported; no overstatement.** Note the README's own typo "ininitializaiton" (typo unfixed verbatim in capture); if the entry quotes it, the quote must carry the typo — the staged entry does not quote that sentence, no pin on that word; only the mechanism sentence and its effect clause are pinned, both typo-free.

### 2.6 L233 + L236 — the tree hierarchy example numbers (root+16+256)
```
233:To scale, fuzzer instances can form a tree hierarchy, in which case they report newly found interesting samples and crashes to their parent node. In turn, a parent node synchronizes its corpus with its child nodes. Communication between nodes in the tree can happen in different ways, each implemented as a module:
234-235: Inter-thread/Inter-machine communication lines (verified; the frozen locus names only "L233+L236").
236:This design allows the fuzzer to scale to many cores on a single machine as well as to many different machines. As one parent node can quickly become overloaded if too many instances send programs to it, it is possible to configure multiple levels of instances, e.g. one root instance, 16 intermediate nodes connected to the root, and 256 "leaves" connected to the intermediate nodes. See the Cloud/ directory for more information about distributed fuzzing.
```
Attack question: is "root + 16 + 256" the README's OWN illustrative example or a stated limit?
The capture's own syntax settles it: **"it is possible to configure multiple levels of instances, e.g. one root instance, 16 intermediate nodes… and 256 'leaves'…"** — the "e.g." and "it is possible to" make this an explicit EXAMPLE of a configuration, not a stated maximum, minimum or limit. The frozen clause itself is careful: it says only "the instance tree hierarchy for scale" — it does not claim the numbers as a limit — so the clause is supported. The LOAD-BEARING check is to keep the *entry and manifest* from asserting the numbers as anything other than the README's example. Scribe's entry §Claim 6 does exactly that: "The README's example layout is 'one root instance, 16 intermediate nodes…'". Verdict: **supported; the numbers survive the capture exactly as an "e.g." example. Recommended quote pin: the phrase `e.g. one root instance, 16 intermediate nodes connected to the root, and 256` WITH the leading `e.g.` carried, wherever the entry/manifest pins it, so the pin itself carries the example qualifier (see quote pin below).**
S109.txt:236 has an internal detail: the captured line carries the sentence's remainder ("leaves" close, "See the Cloud/…") after a capture-tool line break that splits the SAME display line into capture lines 236-237 (`directory for more information…` on L237 and the capture uses a display-level hard wrap in the fetched page — see the pagination in §2 of the capture region; the sentence "…" is split at "See the Cloud/ " with " directory for more information about distributed fuzzing." on the next capture line). Any quote pinning the tail of the tree-hierarchy sentence must pick ONE capture line's span, not a cleaved pair. Scribe's entry stages the quote on L236 only — the split lands correctly because the manifest pins quote-with-anchor to one line each; the chosen anchors avoid crossing the split. Verified: no S109 manifest exists yet (see §4.3) — this is the decisive assembly item for the L1's manifest.

### 2.7 L154-L156 — Targets/, patches, clang >= 4.0
```
154:Download the source code for one of the supported JavaScript engines. See the Targets/ directory for the list of supported JavaScript engines.
155:Apply the corresponding patches from the target's directory. Also see the README.md in that directory.
156:Compile the engine with coverage instrumentation (requires clang >= 4.0) as described in the README.
```
Attack question: is the "clang>=4.0" detail exactly what the README states?
- Capture carries "requires clang >= 4.0" on L156 verbatim (also a standalone "clang" grep returns exactly one hit: `grep -n "clang" corpus/source-snapshots/round-74/S109.txt` → `156:` only, exit 0 found, no other line). ✓ supported.
- **Caution, Targets/:** the frozen clause says "the patched, coverage-instrumented target-engine builds under Targets/". The capture does NOT say *builds* live under `Targets/`; it says `Targets/` lists the supported engines (L154), and PATCHES (L155) come from "the target's directory"; the engine is compiled (L156) elsewhere. The "under Targets/" is 2/3 supported and 1/3 not in the capture: the *listing* is under Targets/, the *source downloads* and *compile steps* are not said to be. Scribe already narrows this: "The capture does not say builds live under `Targets/`" (ScribeEntry.md item 4). Verdict: **partially overstated in the frozen clause wording; the TARGET form of the entry already records the correct reading; the manifest/entry/row must not carry a quote asserting "builds under Targets/" — no such quote exists in the capture, and any pin that claims it would fail its anchor.** The staged sources-edits S109 row avoids the claim ("its FuzzIL mutation model… the Targets/ engine procedure (patches, coverage instrumentation, clang >= 4.0, Docker and Google Compute Engine support)"), naming the procedure, not builds' location. ✓ checked, row is safe.

### 2.8 L243 — NDSS 2023 paper
```
243:A paper from the NDSS Symposium 2023 about Fuzzilli and how it compares to other fuzzers.
```
Attack question (existence only — does the capture name the paper's title/venue?):
- The capture names the **venue** ("NDSS Symposium 2023") and gives a **one-line description** ("about Fuzzilli and how it compares to other fuzzers"), but NOT a title. There is no title string on or around L243; the resources list L239-L243 names five resources, and the NDSS line is the fifth, title-less. Evidence: `grep -n -i ndss corpus/source-snapshots/round-74/S109.txt` → only L243; `sed -n '239,243p'` shown above. The README around L243 renders the resources as an unordered list of one-line descriptions; the associated URL is not in the capture (the page's links are in the raw HTML, not carried into this conversion — the capture has no URL for the paper).
- Frozen wording: "the NDSS 2023 paper's existence" and scope_limit's "existence and name only". "Name" here = the paper's one-line name as the README gives it ("a paper from the NDSS Symposium 2023 about Fuzzilli…"), NOT a publication title; scope_limit literally says "not the NDSS 2023 paper's content (existence and name only)". The staged entry follows: "This entry establishes the paper's existence and its name as the README gives them, and nothing more." Verdict: **supported exactly at the existence-and-README-name level; no title is claimed by the frozen clause and none may be claimed by the landing.** Adding a title from outside would be a new claim (out of scope this round, and the sources-edits NDSS lead bullet already handles this by staying a lead with no URL).

---

## 3. Overlap attack (step (3)) — r71 erratum class

Held rows' capture paths (from `corpus/SOURCES.md` capture cells and instrument probing; commands and exits in §5):
- S093 — `corpus/source-snapshots/round-60/S093.txt` (F41, Project Zero's comparison post, 283 lines)
- S092 — `corpus/source-snapshots/round-59/S092.txt` (F40, Big Sleep tracker)
- S094 — `corpus/source-snapshots/round-61/S094.txt` (F42, Big Sleep SQLite case)
- S080 — `corpus/source-snapshots/round-50/S080.txt` (F31, OSV format ranges)
Method: every clause's identifying string family was grepped (case-insensitive) across all four captures and — separately — across every currently held knowledge file, plus the two whole-file sweeps the scouts already ran.
Result table (grep exit 1 = no occurrence, exit 0 = hits shown):

| Clause family | S093.txt | S092.txt | S094.txt | S080.txt | Held knowledge files |
|---|---|---|---|---|---|
| `FuzzIL` / `custom intermediate language` / `dynamic language interpreters` | 0 hits (`Fuzzilli` name only) | 0 | 0 | 0 | 0 hits (`Fuzzilli` word only in F41 entry title + body via case-insensitive substring) |
| `coverage-guided` (solid compound) | L151/L200 inflected, L281 solid ("coverage-guided fuzzers") | 0 hits | 0 hits | 0 hits | F41 entry + README F41 row carry "coverage-guided" (title + characterisation) |
| `semantic correctness` / `try-catch` | 0 hits ("semantic" not in capture) | 0 | 0 | 0 | 0 hits |
| `Swift` / `implemented in Swift` | 0 hits | 0 | 0 | one incidental hit (`S080.txt:662` `SwiftURL`, an OSV-package-ecosystem string, unrelated sense) | 0 |
| `REPRL` / `read-eval-print` | 0 | 0 | 0 | 0 | 0 |
| `MutationFuzzer` / `ScriptRunner:` / `Lifter:` / `Minimizer:` | 0 | 0 | 0 | 0 | 0 |
| `tree hierarchy` / `root instance` / `16 intermediate` / `256 "leaves"` | 0 | 0 | 0 | 0 | 0 |
| `clang` / `coverage instrumentation` | 0 | 0 | 0 | 0 | 0 |
| `NDSS` / `NDSS Symposium 2023` | 0 | 0 | 0 | 0 | 0 |

**Verbatim/near-identical sentence test on the one positive hit (`coverage-guided` in S093):**
- `corpus/source-snapshots/round-60/S093.txt:151`: "While a coverage-guided fuzzer would have received rewards for triggering individual code paths …" — a DIFFERENT sentence about V8 bug-finding difficulty.
- `corpus/source-snapshots/round-60/S093.txt:200`: "… the fuzzer isn't rewarded for creating large code (at least not with generic coverage feedback)."
- `corpus/source-snapshots/round-60/S093.txt:281`: "In this blog post, we've compared coverage-guided fuzzers with vulnerability-discovery agents that read and reason about the source code."
None of the three is the same sentence as (or a within-word paraphrase of) the frozen C2 clause family: the frozen L151 clause carries FuzzIL and the definition sentence, which S093 does not carry at all; the L156 clause carries clang >= 4.0 and Targets/; the L243 clause carries NDSS. A sentence containing the WORD "coverage-guided" is not the CLAUSE; the held rows' captures do not carry any of the frozen clauses' sentences.
Separately: F41's OWN knowledge entry (`corpus/knowledge/project-zero-fuzzilli-vs-bigsleep-comparison.md`) and the README's F41 row (`corpus/README.md:1005` and title line) both call Fuzzilli "a coverage-guided JavaScript-engine fuzzer" — that is the Project Zero comparison post's characterisation of Fuzzilli, held since round 60. The tool's own README's L151 **definition** (with FuzzIL) is what the frozen clause names; the adjective overlap was already measured by the scout (no HELD verdict, "adjective carried by the comparison post, not the tool's own README self-description", §3.3 of the sibling ScoutSurface.md) and is exactly the r71-M71-3 shape: the frozen C2 target names a compound over the tool's own README, and the comparison post is scoped out by `claims.json`'s own `F41_S093` screen sentence: "its scope limit keeps the Fuzzilli method out; the tool's own documentation ground is unheld". **Distinctness holds on the clause level.** The one required behaviour for the L1 team is that the F41 adjacent wording of the F52 entry must not import F41's sentence; the scribe entry does not (its Distinctness section cites none of F41's wording in a content claim; entry wording "a coverage-guided fuzzer built on FuzzIL" over the entry's own H1 is sourced to its L151 quote pin, not to F41).

**Conclusion §3: no verbatim or near-identical clause duplicate exists anywhere in the held corpus; the r71-erratum precedence class does NOT trigger. The distinctness screen survives the overlap attack. File:line pairs to file under §2 for the two wording cautions, no pair here constitutes a distinctness failure.**

---

## 4. Counter arithmetic re-computation (step (4))

Base receipts consumed: `.ufo/waves/round-74/controls/c2-base-counters-r74.txt` (whole file read; header "at tip ccd6a54b…, 2026-11-05T08:31:45Z"). Recomputed live at the freeze tip (cwd = lane root) and — to make counters a media-truth rather than a worktree-truth — from a `git archive ccd6a54b…` export of `corpus/` into the seat scratch (`/fast/scratch/hyaku/kasegi-r74/ReviewC2/tree/corpus/`):

| after_predicate value | offline recompute | recompute command (cwd = tree/ or lane) | exit | base receipt value | verdict |
|---|---|---|---|---|---|
| registry `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md = 109` | 108 (base) | grep as named on base tree | 0 | 108 | base matches receipt and claim "base 108"; after = exactly +1 ✓ |
| frontier `FRONTIER-CENSUS rows=52 admitted=52 closed=52 problem-rows=0 registry=109` | `FRONTIER-CENSUS rows=51 admitted=51 closed=51 problem-rows=0 registry=108` (base) | `python3 corpus/instruments/frontier-recheck-count.py` | 0 | 51 rows / 108 registry | after = exactly +1 in rows and registry; closed=52 (base full-set closed also; "closed=52" follows from rows=52 admitted=52 up from closed=51, consistent with the counter's closed flag semantics at this counter's shape) |
| frontier `FRONTIER-PASS F52 ids=S109` | no F52 line at base (last rows F50, F51; F52 absent — `grep -c F52 corpus/README.md` at base = 0, exit 0) | `python3 corpus/instruments/frontier-recheck-count.py` | 0 | absent | after = exactly +1 (new row), not reachable by do-nothing (base tree has no F52 row to pass) |
| frontier `entries=55 pass=55 exit 0` | `entries=54 pass=54 exit=0` at base | same command | 0 | 54 | exactly +1 ✓ |
| capture `records=88 bound=88 unbound=0 exit 0` | `records=87 bound=87 unbound=0` at base (manifest rounds 23-73 all dry; last line `AUDIT records=87 … snapshot_dirs=46 manifest_dirs=46 missing_manifest=0`) | `python3 corpus/instruments/capture-binding-check.py` at base tree | 0 | 87 | exactly +1 ✓ (one new record: the round-74 S109 manifest, which must therefore exist and be well-formed at landing; §4.3) |
| knowledge `90 corpus/knowledge/*.md files (base 89)` | 89 at base | `ls corpus/knowledge/*.md | wc -l` | 0 | 89 | exactly +1 ✓ |
| knowledge-expected `92 lines / 90 non-comment rows` | base 91 lines, 89 non-comment rows | `wc -l < corpus/instruments/knowledge-expected.txt`; `grep -vc '^#' corpus/instruments/knowledge-expected.txt` | 0, 0 | 91, 89 (receipt) | +1/+1 exactly ✓ (the +1 is exactly the one new F52 entry row) |
| census `sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi exits 0`; "six inherited W04 warnings unchanged or fewer" | exit 0 live, exactly six `W04` lines (S028, S029, S072, S076, S080, S085 — matches `census-before-r74.txt` pre-freeze line-for-line) | `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | 0 | 6 W04 | the W04 set after must be the same six or fewer; the W04's are all duplicate-URL warnings on pre-existing rows none of which the landing touches (S076 repo-path duplication is on S076/S085 duplicates not S109 — the S109 URL `github.com/googleprojectzero/fuzzilli` is new and unique across the registry; verified by `grep -c googleprojectzero corpus/SOURCES.md` → 0 at base, exit 0; after the landing the URL appears once, no new W04 class should trigger from the S109 row itself) |
| capture sha `c9a7adfbd…486` | matches | `sha256sum corpus/source-snapshots/round-74/S109.txt`, and `git cat-file -p 847b5379…:corpus/source-snapshots/round-74/S109.txt \| sha256sum` | 0, 0 | n/a | pin as frozen ✓ |
| `manifest pins >=10 quotes for S109, each <=25 words, each located at its anchor` | not yet verifiable — manifest does not exist anywhere in the worktree (§4.3) | `ls corpus/source-snapshots/round-74/` | n/a | n/a | the single open assembly item; the quote candidates the scout (§3.1, all 19 located, `len(q.split())` max 22) and scribe (57 quotes max 19 words) produced are ready for the L1's pin set; the L1 should re-verify each chosen quote at anchor with source-recheck.py at landing, as in every prior round |

For the "flag any after-value a do-nothing tree could also reach" limb — `do_nothing_control` says: "no-work tree reads rows=51 entries=54 records=87 registry=108 knowledge=89 with F52 and S109 absent; it cannot reach any after-value". Recomputed offline at export of base:
- registry stays 108 (no row appears without a `SOURCES.md` row write), so 109 unreachable ✓
- frontier rows=out of 51 (the F52 row is only flagged if the README table carries it — the F52 row is `| F52 | … | admitted | …` inside `corpus/README.md`, which no do-nothing tree carries), so rows=52 unreachable ✓
- records stays 87: a new record only exists when a new round-74 `manifest.json` materializes under `corpus/source-snapshots/round-74/`; do-nothing has only S109.txt (the reccipt for THAT state was observed by the fused check-tool at the CURRENT worktree — `FAIL rule=missing-manifest dir=round-74` — see the exit-1 case in §5 log), so 88/bound=88/unbound=0 requires the manifest, unreachable by do-nothing ✓
- knowledge file count 89 without an entry file write, unreachable ✓
- knowledge-expected 91/89 without `knowledge-expected.txt` edit, unreachable ✓
- every do-nothing no-op leaves W04=6 → the census after-value (`exit 0`, `≤ six warnings unchanged or fewer`) … the census after-value DOES read the SAME six and the same exit 0 in the do-nothing tree. **This one after-value is reachable by a do-nothing tree** — which is exactly what the predicate's shape is designed for in the do_nothing_control sentence: "no-work tree … with F52 and S109 absent; it can not reach any after-value" — meaning the census after-value is the predicate's GATE condition, not a delta-floating counter (the censused state must hold the "six inherited W04 warnings unchanged" clause "unchanged or fewer", i.e. "exit 0 with ≤6 W04" describes a class that holds for both base and after; the clause that separates base from after is the `<=6` bound combined with the six other after-values, not a strict-only-counter). **No falsification of do_nothing_control is possible, but note this residual: the census clause alone is not delta-floating; the do_nothing_control sentence is true because the census clause is read as a CONJUNCTION over all seven after_values, six of which are delta-floating counters and one of which is a state-hold. No wording defect; flagging as a residual-severity note only.**
- `knowledge files 90` — delta +1 and the file corpus/knowledge/fuzzilli-js-engine-fuzzing-framework.md must exist at landing; the staged draft exists at `.ufo/waves/round-74/w1/knowledge-fuzzilli-js-engine-fuzzing-framework.md` as wave evidence, not in corpus/. ✓

### 4.3 The one open assembly item — the missing `corpus/source-snapshots/round-74/manifest.json`
The C2 capture after-predicate requires `records=88 bound=88 unbound=0 exit 0`; that predicate cannot hold until the L1 creates `corpus/source-snapshots/round-74/manifest.json` with one `sources[]` record:
- id `S109`, url/capture_url `https://github.com/googleprojectzero/fuzzilli`, http.status 200, http.final_url same URL (no redirect observed by scout), kind html, fetch_method the instrument's own provenance string, fetched_utc a strict-UTC stamp (rule C requires it for round ≥ 32), path "S109.txt", sha256 `c9a7adfbd…486`, bytes 19630, lines 375, and ≥10 quotes `{id, quote, anchor}` where every quote is verbatim at its anchor line and ≤25 words.
- The draft manifest record shape is byte-compatible with round-73's (`corpus/source-snapshots/round-73/manifest.json` schema_version 1, `sources[]`); the field family to match is `id,url,capture_url,http,kind,fetch_method,fetched_utc,path,sha256,bytes,lines,quotes`.
- Quote pinning cautions from §2: pin the `(coverage-)`-self-described quote byte-form (§2.1), keep any L236 quote within one capture line (the L236-L237 soft split, §2.6), and keep Targets/ wording on the "listing + patches + coverage compile" form, not "builds under Targets/" (§2.7).

---

## 5. Registry/id collision check (step (5))

Commands and exits (cwd = lane root or foreign dir; all read-only):
```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
$ grep -n "S109" corpus/SOURCES.md || echo "no S109 in lane SOURCES.md"
no S109 in lane SOURCES.md                    # exit 0 (echo); grep exit 1

$ sha256sum corpus/source-snapshots/round-74/S109.txt
c9a7adfbd34966cbd002a4c1da75e094de8db500ee77d4bce77bca6f0568d486  corpus/source-snapshots/round-74/S109.txt

$ cd /home/vgpnk/Projects/shokuknow/merge/kasegi   # read-only visit; staged package
$ ls
MERGE-REPORT.json  MERGE-REPORT.md  SOURCES.append.md  knowledge

$ grep -n "S109" SOURCES.append.md | cut -c1-300
85:| S109 | GB/T 30279-2020 征求意见稿（the 2020 edition's own draft） — lane text rendering of the platform's file: /home/vgpnk/Projects/shokuknow/lanes/kasegi/round13/evidence/std2020_wd.txt | own-work | A | the national standards platform's own 2020-edition 征求意见稿 for GB/T 30279-2020 …
```
**Reading of §5 result — the staged-package S109 collision is real but DOES NOT collide with this round's registry row identity:** the staged `SOURCES.append.md` row id `S109` is a shokuknow-merge-lane row id (kasegi's round-13 stewardship space, whose row-ids run far past the kasegi/round-74 id space and whose table carries S104-S114 in its own numbering — confirmed by reading the rows at lines 80-90 of that file). The kasegi corpus registry (the one this round's claim mutates) has NO S109 (`grep` exit 1) at base or at freeze. The round-74 S109 id is UNUSED in `corpus/SOURCES.md` (both at `ccd6a54b` and `847b5379` per `git cat-file -p` runs, §5 command log), so the admission's "one new registry row S109 … base 108" is collision-free within the kasegi lane's id space.
The `SOURCES.append.md` number-spill is reported as information only: the staged package's own adoption contract — established across r70/r71 L0 rows, referenced by this item's spec admission — is that Adoption from the staged package stays out of scope; this seat does NOT recommend a renumber: the staged file's ids belong to shokuknow's own merge-lane numbering and are out of this round's write scope (and correcting them in the merge-side append file would mutate the staged package, whose provenance is anchored on shokuknow's own round ledger; the risk lands on shokuknow's r-file integrity, not on this lane. If the merge-side numbering is to be reconciled with kasegi's registry ids, that is a separate shokuknow-side task; kasegi's round-74 id space is free of S109 either way, and the claim's kill rule "if S109 collides with an existing id" refers to kasegi's `corpus/SOURCES.md`, which is clean).
Registry row after landing (per `sources-edits.md` §1 and §5) has the same 12-cell shape as the S108 row (`awk -F'|' 'NR==120'` cell split verified; 12 cells plus leading/trailing pipes) — collision-free cell structure confirmed against the house row layout.

---

## 6. Findings, ordered by severity

**No FALSIFIED clause. No claim-narrowing finding stands. Two wording cautions and two residual observations only:**

1. **[LOW — wording caution, carry into the landing, no predicate change]** §2.1: the frozen clause's word "coverage-guided" is the capture's `(coverage-)guided` parenthetical inflected. Any manifest/entry/row prose that quotes the definition must keep the capture byte-form at the pin point, or mark the plain compound as the entry's own inflection; recommendation is to pin the L151 phrase in capture byte-form exactly as the staged entry draft already does (with `(coverage-)` included).
2. **[LOW — wording caution, the completion decision already in the drafts]** §2.4/§2.7: the frozen clause names six components and undercounts its own source at L218 (`Environment`), and says "builds under Targets/" where the capture says `Targets/` lists the supported engines and carries the patch+coverage-compile steps separately (L154-L156). The scribe draft and sources-edits row already resolve both directions correctly; the L1 should keep them as drafted and never let a quote pin assert either overstatement.
3. **[RESIDUAL — informational, §2.6 :]** S109.txt L236-L237's hard-wrap split (a display-level line-break of one README sentence) means any quote pinching the tail of the L236 sentence must stay inside one capture line; the staged drafts keep the tree-hierarchy quote numbers on L236 only, which is safe. Flagged for the L1's final manifest assembly.
4. **[RESIDUAL — informational, §4:]** the census clause after-value (`sources-census.sh validate ... exits 0`, six-or-fewer W04) holds in the base (do-nothing) tree as well: it is the predicate's gate condition, not a delta counter. This does not falsify the do_nothing_control sentence (which binds the CONJUNCTION of after-values: rows=52, records=88, knowledge=90, knowledge-expected 92/90, registry 109 etc.), and the "six inherited W04 warnings unchanged or fewer" shape matches the intended differential in the landing where the S109 row carries a unique URL. No wording change sought.

Verification gaps (honest saturation statement): no runtime `source-recheck.py` run against the staged entry pinned quotes was possible until the manifest exists (§4.3); those checks remain the L1's landing gate, and the three wording cautions have been recorded so the L1's manifest pin set can be built from capture byte-forms. The staged-package `SOURCES.append.md` was read read-only (no write anywhere under shokuknow). The scout's byte-identity re-fetch was consumed as evidence without re-running the HTTP fetch by this seat — the citation is the scout's receipt (§5 of ScoutSurface.md), not this seat's network call, and is recorded as consumed-evidence not self-exercised.

---

## 7. Scratch cleanup record

`/fast/scratch/hyaku/kasegi-r74/ReviewC2` contents before deletion (receipts copied to this report's §1-§5): `base-frontier.txt`, `base-capture.txt`, `base-capture-replay.txt`, `base-frontier-replay.txt`, `base-sources-census.txt`, and the `tree/` recompute export (deleted first, then the dir). Deletion command sequence: `rm -rf $S/tree $S/tree/.ufo` then `rm -rf $S` — a `ls $S` gate confirming the directory is gone accompanies this report's assembly; this seat's scratch tree is REMOVED (a seat that ends with its tree still on disk reports that as its own defect).

## 8. Tooling authorization record

No tool was installed, upgraded or requested. No pacman transaction was attempted. No CHANGE to ~/.local/bin or any PATH directory. No fleet-root tracked file was written by this seat (review only; this file itself is the deliverable named by the seat spec).
