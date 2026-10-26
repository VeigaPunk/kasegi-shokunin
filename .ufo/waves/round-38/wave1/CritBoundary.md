# CritBoundary — boundary-condition probe of the planned round-38 checks

seat: CritBoundary (critic) · item: probe boundary conditions against `claims.json` and test the
fence / declared-block limbs on scratch files · receipt only, no deliverable bytes.
lane `kasegi-shokunin`, base `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, at HEAD `7001535`.
Scratch `S=/fast/scratch/hyaku/kasegi-r38/CritBoundary` (removed at exit; see §7).

Method: `r38-closure.sh` does not exist yet, so each limb was exercised against (a) the wave1
reference implementation the L1 will embed — `wave1/ExecFenceWalk.sh`
(sha256 `f5018c464afffe747785d8c8c9c89c1c83fc400749ecb0b5e997fbd9785c322d`) and
`wave1/ExecDeclaredBlocks.gen.sh` (`49925cd44d496074090432319c36d1cecc6e0f2020e53f4ef4b4ebb4977fa77d`),
both copied to `$S` and run there — and (b) spec-literal evaluators written in `$S` for G3, G4, G7 and
the G8 carry-over helpers extracted verbatim from `corpus/instruments/r37-closure.sh`.
No lane file was written; every fixture is under `$S`.

## 1. Prediction matrix (frozen predicate → observed behaviour)

| Check | Face value at honest J | Boundary case probed | Predicted & observed | Class |
|---|---|---|---|---|
| G1 fence state | green | base README is `open`, PROVINCE `closed`; delivered blocks appended | `province.j.md -> closed`, `readme.j.md -> closed` | correct |
| G1 fence state | — | closer `"```  "` (2 trailing spaces) | CommonMark walk `closed`; strict `^```$` parity `open=1 (base=1 append=0)` | **false red** if reimplemented by exact grep |
| G1 fence state | — | `~~~` opener left unbalanced in PROVINCE | tilde-aware walk `open`; backtick-only walk `closed` | **two conforming readings disagree** (predicate says "CommonMark" *and* "opening fence = ```") |
| G1 fence state | — | README block landed without its first line | `readme.noline1.md -> open` | correct red |
| G1 declared blocks | green | LF declaration | `declared=1 ok=1 fail=0 base=0 exit=0` | correct |
| G1 declared blocks | — | **CRLF** declaration | reference `ok=1 fail=0 exit=0`; naive `read` loop `ok=0 fail=1` (`want=…$'\r'`) | false red for a naive rewrite |
| G1 declared blocks | — | **trailing blank line** | reference `declared=1 ok=1`; naive loop `ok=1 fail=1` (spurious `path=''`, `tail -n ''` → sha of empty) | false red for a naive rewrite |
| G1 declared blocks | — | **empty** declaration file / comments-only | reference `declared=0 fail=1 exit=1`; naive loop `ok=0 fail=0` | **false green** for a naive rewrite |
| G1 declared blocks | — | 74 lines of r37 scaffolding re-inserted *before* the declared block | declared-block limb `ok=1 fail=0 exit=0`, fence `closed`, correction line present — **all three limbs green** | **false green in the frozen limb** (§2 C-B1) |
| G2 | green | not probed (receipt not yet committed; `.ufo/waves/round-38/final-gates/all-gates.txt` absent, `ls` exit 2 in `c1-controls/before.txt`) | export-ref==REF ⇒ empty diff ⊂ {receipt}=green; run over base ⇒ receipt absent ⇒ red | correct by construction |
| G3 | green only while no added lane line spells a token | `TODO` in an inline code span / fenced block / prose; whole vocabulary quoted | raw scan: all 7 tokens hit on one documentation line; `TODO` hits in code span, fence and prose | **gate cannot distinguish documentation from a placeholder** (§2 C-B2) |
| G3 | — | code-span-aware scan instead of raw | 6 of the 7 r37 `⟨pending` markers live inside inline code spans (L90, 95, 216, 265, 300, 320; only L10 plain) | **exemption would reopen D-C** |
| G4 | red today, green only once results land | `results.json` = `[]`, dispatch 73 tasks | `FAIL count` (0 vs 73) | correct red |
| G4 | — | dispatch `taskCall.tasks` = `[]` | `PASS` (0 == 0) | **false green** (vacuous) |
| G4 | — | results is an object with 73 keys, or a 73-char string | `PASS` (`len(dict)`/`len(str)`) | **false green** (not a seat list) |
| G4 | — | dispatch with no `taskCall` key | `KeyError` — uncaught exception, not a graded FAIL | crash, not graded |
| G5 | green (correction outside the round-38 section) | section-scoped vs file-wide `Final lane commit:` count | delivered correction line itself contains the literal once | file-wide count would **red its own mandated fix** |
| G6 | red until quiescence | live state now | `kasegi-r36 absent`, `kasegi-r37 absent`, `kasegi-r38 present entries=216118` | correct red mid-wave |
| G7 | green with delivered block | heading anchor | exact line `## Round-37 dispositions` → 0 at base (real heading is `## Round-37 dispositions (appended 2026-10-26, R31 home)`); prefix → 1 at base, **3** at J; new heading sits at L44, not adjacent to L37 | anchor must be the exact new heading (§2 C-B3) |
| G7 | — | rows numbered `1)` instead of `1.` | period-only regex 0; `[.)]` regex 7 | **false red** for a period-only regex |
| G7 | — | 7 rows with duplicated numbers (1,1,2,2,3,3,4) | count 7 (passes); number set `{1,2,3,4}` | **false green** for a count-only limb |
| G7 | — | file-wide row count at base (D-F open) | 12 numbering-shaped rows already in the file | **false green** for any file-wide count ≥ 7 |
| G8 | green at REF=J | r37 E1 re-run over the round-38 SCORECARD append | 3/3 captured hashes are ancestor commits (`2387dcf6…`, `83975acc…`, `f3246559…`) ⇒ E1 green; one 40-hex non-commit token on that line ⇒ `2 of 3` ⇒ E1 red | thin margin (§2 C-B4) |

## 2. Counterexamples (strongest first)

### C-B1 — G1's declared-block limb cannot see D-A reappearing *before* the block (false green)

The frozen limb is suffix-anchored ("the file's last `<lines>` lines hash to `<sha256>`"), and the
frozen text does **not** require the `# base <path> <pre_lines>` guard the reference generator emits.

```
$ wc -l province.base.md scaffold74.md province.junk.md
  152 province.base.md
   74 scaffold74.md            # sed -n '79,152p' province.base.md — the r37 scaffolding itself
  230 province.junk.md         # base + 74 pasted lines + the 4-line r38 block
$ bash ExecDeclaredBlocks.gen.sh check decl.junk.txt --root root2 | tail -1
declared=1 ok=1 fail=0 base=0 exit=0
$ bash ExecFenceWalk.sh province.junk.md
closed
$ grep -c '^Correction (round 38)' province.junk.md
1
$ { printf '# base PROVINCE.md 152\n'; cat decl.junk.txt; } > decl.junk.base.txt
$ bash ExecDeclaredBlocks.gen.sh check decl.junk.base.txt --root root2 | tail -1
declared=1 ok=1 fail=1 base=1 exit=1     # file_lines=230 != pre_lines=152 + declared_lines=4
```

All three G1 limbs are green with 74 duplicated scaffolding lines re-landed above the block; only the
optional base guard catches it. (Control on the honest J bytes: `OK base PROVINCE.md file_lines=156
pre_lines=152 declared_lines=4` → `declared=1 ok=1 fail=0 base=1 exit=0`.)

Live confirmation against the landing in progress at HEAD `7001535` (read-only):

```
$ cat .ufo/waves/round-38/declared-blocks.txt
corpus/README.md 32 f0318ac8306f52c8085c192ee0c32f8f72dd2f4f5675164294433c9210fbbdff
PROVINCE.md 4 797666b943244f9174b627918f84b9027858a6d4ffe0213c026c568ff1ed3acf
$ bash .ufo/waves/round-38/wave1/ExecDeclaredBlocks.gen.sh check .ufo/waves/round-38/declared-blocks.txt --root .
OK   corpus/README.md lines=32 file_lines=486 sha256=f0318ac8…
OK   PROVINCE.md lines=4 file_lines=156 sha256=797666b9…
declared=2 ok=2 fail=0 base=0 exit=0
$ ExecFenceWalk.sh PROVINCE.md -> closed ; ExecFenceWalk.sh corpus/README.md -> closed
$ grep -c '^Correction (round 38)' PROVINCE.md -> 1 ; corpus/README.md -> 1
```

`base=0`: no guard is declared, so C-B1 is live in the current landing. The honest line counts are
`156 = 152 + 4` and `486 = 454 + 32`, so adding `# base PROVINCE.md 152` / `# base corpus/README.md 454`
costs nothing and keeps the file green today.

### C-B2 — G3's raw token scan cannot be satisfied by a lesson that documents the vocabulary, and a code-span exemption would reopen D-C (false red on one side, false red on the other)

```
case                       raw-hits                               code-span-aware-hits
quoted-vocabulary-line     {'⟨pending':1,'<fill>':1,'filled by the L1':1,'<LANE_HASH>':1,'<r38-':1,'TBD':1,'TODO':1}  {}
todo-in-inline-code        {'TODO': 1}                            {}
todo-in-fenced-block       {'TODO': 1}                            {}
prose-word-TODO            {'TODO': 1}                            {'TODO': 1}
tbd-in-table-cell          {'TBD': 1}                             {}
tilde-fenced-quote         {'TBD': 1}                             {}
clean-line                 {}                                    {}
```

Marker shapes at the base lesson (`git show <base>:corpus/lessons/round-37.md`):

```
10  plain-text  ... round-37 final lane commit `⟨pending: L1 closure commit — a commit cannot
90  code-span  `⟨pending: entry file at the integrated head⟩`.
95  code-span  `⟨pending: ExecC2Harness / final-gates transcript at the integrated head⟩`.
216 code-span  reds. `⟨pending: wave1/ExecGateReviewPrep.md; file at the integrated head⟩`.
265 code-span  `⟨pending: wave1/ScribeConsiderthese.md §3 delivers the byte-exact block, sha256 …`
300 code-span  `⟨pending: L1 integration census measurement⟩`.
320 code-span  `⟨pending: measurement at the integrated head⟩` — r36 discipline holds: …
```

So the 6/7 case: an inline-code exemption (the obvious fix for the false red) would have passed the
exact r37 defect the limb exists to close. The current delivered bytes are clean, so the limb is
green *today* — measured over every landable round-38 file:

```
$ for t in '⟨pending' '<fill>' 'filled by the L1' '<LANE_HASH>' '<r38-' TBD TODO;
    do printf '%-20s %s\n' "$t" "$(grep -cF -- "$t" ExecC2Capture.S055.txt)"; done
⟨pending 0 / <fill> 0 / filled by the L1 0 / <LANE_HASH> 0 / <r38- 0 / TBD 0 / TODO 0
# ScribeEntryF21.entry.md, ScribeRowS055.row.md, ScribeSourcesLog.blocks.md, ScribeScorecard.{section,correction}.md,
# ScribeFrontierBlocks.{province-eof,readme-eof,readme-row}.md, ScribePendingResolutions.block.md, ScribeLedgerFill.block.md,
# ScribeMistakes.block.md, ScribeQualityRows.block.md, ScribeLOG.block.md, ScribeConsiderthese.block.md,
# ScribeAssimilation.block.md, ExecC2Capture.manifest.json  -> 0 lines each
```

The live risk is the round-38 lesson, which must explain D-C (widening the vocabulary to `TODO`/`TBD`)
and will naturally spell the tokens; every spelling reds G3 and therefore C1.

### C-B3 — G7's anchor is ambiguous three ways, and two of the three wrong choices are false greens

```
$ grep -n '^## ' ledger.j.md
37:## Round-37 dispositions (appended 2026-10-26, R31 home)
41:## Re-pin note (appended 2026-10-26)
44:## Round-37 dispositions — filled (round 38)

variant          S1 `N.`  S2 `N.|N)`  S3 file-wide  S4 rows-2   S5 number set
base                None       None           12       None   None
filled-dot             7          7           19          7   [1..7]
filled-paren           0          7           12          7   [1..7]
filled-dup             7          7           19          7   [1,2,3,4]
filled-six             6          6           18          6   [1..6]
filled-noheader        7          7           19          5   [1..7]
```

- exact-line anchor `^## Round-37 dispositions$` → **0 at base and 0 at J** (the real heading carries
  `(appended 2026-10-26, R31 home)`), so an exact match on the claim's literal never fires;
- prefix anchor → `1` at base but **`3`** at J (empty heading + the correction line quoting it + the new
  heading), so a `grep -c == 1` gate reds on a correct fill;
- the filled section lives at EOF (L44) with `## Re-pin note` between it and the empty heading, so any
  adjacency test reds;
- base already holds 12 numbering-shaped rows, so a file-wide `>= 7` count is green **before** D-F is
  touched; and a 7-row section whose numbers repeat passes a count-only limb while covering 4 proposals.

Delivered block is well-formed under the strict reading: `period-only rows: 7`, `period-or-paren: 7`,
new heading at L44 matching the claim's em-dash spelling.

### C-B4 — G8's inherited r37 E1 counts every 40-hex token near a `Final lane commit` literal, and G5 mandates exactly such a line

`e1_final_hashes()` in `r37-closure.sh` scans from the last `Round 37` heading **to EOF** and takes every
40-hex token on a `[Ff]inal lane commit` line or the 4 lines after it; E1 then requires each token to be a
commit ancestor of REF (`total >= 1`, `bound == total`).

```
$ e1_final_hashes scorecard.j.md          # base SCORECARD + delivered section + delivered correction
2387dcf6ccfefcfb703783387b9aade8fc82abfa
83975acc83df4bd8d5eaf463182ae615f2b64546
f3246559bed2fd085dde860e00247ce394f02bad
$ ... cat-file -e "${h}^{commit}" ; merge-base --is-ancestor "$h" <base>
2387dcf6… commit=yes ancestor=yes
83975acc… commit=yes ancestor=yes
f3246559… commit=yes ancestor=yes
$ # perturbation: one 40-hex non-commit token on that line
fatal: Not a valid object name deadbeefdeadbeefdeadbeefdeadbeefdeadbeef^{commit}
bound would be 2 of 3 -> E1 exit 1
```

The delivered `Correction (round 38)` SCORECARD line is E1-safe (3/3). Any blob hash, capture digest
truncated to 40 hex, or sibling-repo hash cited on or within 4 lines of a `Final lane commit` literal in
`SCORECARD.md` flips E1 → G8 → C1 red with no defect present.

### C-B5 — G4's sibling rule has no defensible stem, and the r37 lane proves it

```
$ git ls-tree -r --name-only 83975acc -- .ufo/waves/round-37/ | grep -E 'dispatch|results'
.ufo/waves/round-37/kasegi-r37-build-results.json
.ufo/waves/round-37/wave1-dispatch.json
```

The r37 dispatch stem is `wave1`, the results stem is `kasegi-r37-build`: a `<stem>-results.json` rule
finds nothing at the r37 tip. The round-38 dispatch carries `"wave": "kasegi-r38-build"` and
`counts={"spawn":73,"resume":0,"total":73}`; today
`ls .ufo/waves/round-38/*results*.json | wc -l` → `0` with 73 tasks, so G4 is correctly red at every head
until the WAVE-DONE file lands in J. The false-green faces of the same rule are in §1 (`[]` with a
0-task dispatch; `len()` of an object or string).

### C-B6 — G1's fence limb is only as good as its fence character set

```
base:      bash ExecFenceWalk.sh province.base.md -> closed ; readme.base.md -> open   (matches before.txt)
appended:  province.j.md -> closed ; readme.j.md -> closed
tilde:     awk 'NR==81{print "~~~";next}1' province.base.md > province.tilde-open.md
           ExecFenceWalk.sh -> open      backtick-only walk -> closed (backtick fence lines=2)
closer+ws: readme.trail.j.md -> closed  (line 1 = "```  "); strict ^```$ parity -> open=1
info-tail: line 1 = "```close" -> open  (correct: not a closer)
```

The frozen sentence names "a CommonMark fence walk" and then defines "opening fence = ``` with
optional info string; closing fence = ``` with no info string". A `~~~`-only PROVINCE satisfies the
second definition (closed) and violates the first (open) — the same file gets opposite verdicts from two
faithful readings, and the backtick-only reading is the one that can be **evaded** by an unclosed `~~~`.

## 3. Impacted axes

- **depth:verifiability (C1, held 4)** — all eight limbs. C-B1 is the only *frozen-limb* false green
  (D-A can re-land above a declared block and still print `closed=8/8`); C-B3 and C-B5 are anchor/naming
  greens that a suite can acquire by rewriting the reference; C-B2 and C-B4 are false reds that fail the
  judged head with no defect present; C-B6 is a specification fork.
- **coverage (C2, held 7)** — not impacted by anything measured here: every C2 counter is untouched, and
  the C2 landable bytes (capture 272,441 B, manifest, entry, row) carry zero tokens of either vocabulary
  (§1 G3 row, §2 C-B2 measurement). The only coupling is that G3 scans added lane lines, so a C2 file
  that quoted a `TODO`/`TBD` from upstream would red C1 while C2 stayed green; measured 0 today.

## 4. Smallest safe corrections (one line each, no scope growth)

1. **G1**: require the `# base <path> <pre_lines>` guard for every declaration (the generator already
   emits it; honest J control passes: `file_lines=156 pre_lines=152 declared_lines=4`; the landed
   `declared-blocks.txt` has `base=0`, and `454 + 32 = 486` / `152 + 4 = 156` both hold, so adding the
   two guard lines keeps it green). Closes C-B1.
2. **G1**: embed `ExecFenceWalk.sh` as the fence walk rather than reimplementing it — CommonMark
   character set including `~`, closers may carry trailing spaces/tabs, 4-space indented lines are text.
   If the frozen text must stay backtick-only, add an explicit red for any `~~~` fence line in either
   front-door file so an unclosed tilde block cannot hide. Closes C-B6.
3. **G1**: the declaration reader must strip `\r`, skip blank/`#` lines, and grade `declared=0` (and an
   absent/garbled declaration file) as FAIL — not as a skipped limb. Closes the §1 naive-rewrite rows.
4. **G4**: require `isinstance(results, list)` and `len(taskCall.tasks) >= 1`; resolve the sibling as the
   unique `*-results.json` whose stem is either the dispatch stem or the dispatch's `"wave"` value
   (`wave1` ↔ `kasegi-r38-build`, the r37 precedent); grade a missing `taskCall` as FAIL. Closes C-B5.
5. **G7**: anchor on the exact new heading line (not a prefix, not adjacency), require the parsed number
   set to equal `{1..7}` (not a row count), accept `N.` and `N)`, and grade "anchor missing" as FAIL.
   Closes C-B3.
6. **G3**: keep the raw scan (a code-span exemption reopens 6 of the r37's 7 markers) and pin, in the
   round-38 lesson drafting guidance, that the lesson spells none of the seven literals — including in
   code spans and fenced blocks. Closes C-B2 without touching the gate.
7. **G5**: scope the `Final lane commit:` count to the round-38 section body only (the predicate's own
   wording), so the mandated correction line appended at EOF cannot red its own fix. For G8 safety, the
   SCORECARD correction must cite only ancestor-commit 40-hex tokens on a `Final lane commit` line
   (§2 C-B4). Closes the G5 self-red and the E1 margin.
8. **G6**: treat an absent `/fast/scratch/hyaku/kasegi-r3{6,7,8}` as quiescent and create the suite's own
   `--work` root before the check, under one fixed name, so a re-run does not red on its own leftover.
   (Today: `kasegi-r36 absent`, `kasegi-r37 absent`, `kasegi-r38 present entries=216118`.)

## 5. What this seat did not do

No verification of the suite itself (absent), no judgement of the claims, no lane edit, no mutation, no
network fetch, no subagent. Read-only git only (`show`, `rev-parse`, `ls-tree`, `cat-file`,
`merge-base`, `status`).

## 6. Tooling

None installed or upgraded; no package channel used; pacman not invoked.

## 7. Scratch

`S=/fast/scratch/hyaku/kasegi-r38/CritBoundary` held every copy, fixture and probe (`ExecFenceWalk.sh`,
`ExecDeclaredBlocks.gen.sh`, `province.*`, `readme.*`, `ledger.*`, `scorecard.*`, `root*/`, `fx*/`,
`g3.py`, `g4.py`, `e1fns.sh`) and is removed before yield; nothing was written outside `$S` and this
receipt.
