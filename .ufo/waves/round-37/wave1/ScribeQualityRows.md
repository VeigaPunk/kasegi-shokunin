# ScribeQualityRows — QUALITY.md R30/R31 append block (round 37)

Status: **block drafted and structurally verified; NOT landed** — `corpus/QUALITY.md` is outside this seat's
write scope (receipt + scratch only). The block below is the deliverable, with the three landing-time
measurements left as placeholders per R19.

Draft head: `b362068195d5489aa94b31e6ec8f880c367e0ba0` (lane `kasegi-shokunin`). Judged axis:
depth:verifiability. Item: R30 grounded in M37-2 (round-36 verifier D6), R31 grounded in
`considerthese/2026-10-26.md` proposal 7, plus the R6-form append preamble.

## 1. Deliverable — the append block (verbatim, placeholders intact)

Block sha256 `d2c59ad556145d7b0e948638dd8fe8e35ba86c1cd07b4d77e565bf7c0f39c282`, 4961 bytes, 14 lines.
Appending it to `corpus/QUALITY.md` (38265 bytes, 264 lines at draft head) yields 43226 bytes, 278 lines
(measured: `cat corpus/QUALITY.md block.md | wc -c -l` → `278 43226`).

````markdown

## Round-37 additions — fail-closed failure paths and proposal-status disposition (append-only)

R6 form: every line above keeps its number — this block is appended after line <LINES_BEFORE> (the file is
<BYTES_BEFORE> bytes before it, `head -c <BYTES_BEFORE> corpus/QUALITY.md | sha256sum` →
`<SHA256_BEFORE>`; `wc -l` → <LINES_BEFORE>), and R22 (line 226), R23 (line 227), R26 (line 249), R27 (line
250), R28 (line 263) and R29 (line 264) are not edited. The landing commit re-runs both commands
immediately before writing: a byte figure measured at draft time is a stale premise under R19 if an earlier
append in the same round moved it.

| id | criterion | grounded in |
|---|---|---|
| R30 | A gate's failure path is fail-closed: a read that fails turns its check red, never green. No default-to-clean swallow sits in a committed instrument — `2>/dev/null` on a status read whose empty output is then counted as clean, or `${x:-0}` applied to a read that may have failed where `0` is the passing value. A zero default is admissible only where the passing value is non-zero, because the failed read then lands on `0` and fails red; where `0` itself passes, the failing read carries an own error branch and no longer shares the passing value. | M37-2 (`corpus/lessons/round-37.md` § Mistakes, minted this round) — class fail-open failure path, captured by R15's runnable closure check and R17's load-bearing-limb rule, not by a pass count. Mints round-36 verifier defect D6 (`corpus/lessons/round-36-verifier-spotcheck.md:160-162`: "`r36-closure.sh:465-466` maps a failing `git status` read to `0` dirty lines (`2>/dev/null`, `${porcelain:-0}`); make the limb fail closed"), and the shape is wider than that row: `corpus/instruments/r36-closure.sh:465` reads status with `2>/dev/null`, `corpus/instruments/r36-closure.sh:466` defaults the empty result, and `corpus/instruments/r36-closure.sh:480-481` passes on `[ "$porcelain" -eq 0 ]`; the same direction is at `corpus/instruments/r36-closure.sh:309` with `corpus/instruments/r36-closure.sh:322` (`ph=${ph:-0}` … `[ "$ph" -eq 0 ]`), and earlier at `corpus/instruments/r35-defect-closure.sh:164-168`. The admissible direction is in the same file at `corpus/instruments/r36-closure.sh:766-768` (`cases=${cases:-0}` compared with `-eq 9`). Round-37 claim E14 is the executable form: `grep -cF 'porcelain:-0' corpus/instruments/r37-closure.sh` prints `0` with no `status --porcelain 2>/dev/null` in it — a landing requirement, not a draft measurement, since at draft head `b3620681` the round-37 instrument is untracked (`git ls-files corpus/instruments/r37-closure.sh` → empty). The round-36 instrument keeps the defect as the negative control: `grep -cF 'porcelain:-0' corpus/instruments/r36-closure.sh` prints `1` (measured at draft head `b3620681`). |
| R31 | A considerthese proposal that a round touches carries a disposition recorded old→new, in the round lesson and in `corpus/knowledge/considerthese-proposals-ledger.md`: the status before the round and the status after it, with the landing cited (`mined` → the landed QUALITY row or lesson section by path and line), the reason given when `declined`, and the reason given when `open`. A `partially landed` row keeps its remainder named open rather than letting one plank close the proposal, and a proposal the round did not touch is restated `unchanged` with the evidence consulted, never omitted. | `considerthese/2026-10-26.md:35` proposal 7 (2026-10-26): "Keep a proposal-status ledger. Two of my proposals were mined in r24 (Q9, the render/raw-sha debt), and per-platform severity is now F13/F17. Tracking proposed → adopted → declined would let me calibrate which suggestions are useful, and stop repeating closed ones like the anchorcheck regression test (now superseded by `anchorcheck.py` fail-closed in r28)." The old→new shape is the tracked ledger's own round-31 append (`corpus/knowledge/considerthese-proposals-ledger.md:22-33`: columns `status before (row above)` → `status after round 31`, five `unchanged` rows each naming the evidence consulted), with the partial-close caveat at `corpus/knowledge/considerthese-proposals-ledger.md:13` ("do not treat the whole proposal as closed") and the reflection-scoping header at `corpus/knowledge/considerthese-proposals-ledger.md:3` (`source:` names the reflection file and its proposal range). At draft head `b3620681` the ledger is tracked (35 lines, 6185 bytes, sha256 `c354ca0242bf7da44589e45c464deba0714dc083e2bf480a6c855ec30a1629c2`) and covers the 2026-10-25 proposals 1–6 only — `grep -cF '2026-10-26' corpus/knowledge/considerthese-proposals-ledger.md` prints `0` — so the 2026-10-26 section R31 requires is the first of its kind to be appended. Path note: the round-37 shorthand `corpus/considerthese-ledger.md` names no tracked path (`git ls-files corpus/considerthese-ledger.md` → empty at `b3620681`); this row cites the tracked ledger. |
````

## 2. Placeholder resolution and landing recipe

| placeholder | occurrences | value at draft head `b3620681` | command that produces it |
|---|---:|---|---|
| `<BYTES_BEFORE>` | 2 | `38265` | `wc -c < corpus/QUALITY.md` |
| `<LINES_BEFORE>` | 2 | `264` | `wc -l < corpus/QUALITY.md` |
| `<SHA256_BEFORE>` | 1 | `cfd0187ac6bcc39ccbaa33b5f40e82bf5de4dfa7197e169870163ebe78ca3728` | `head -c <BYTES_BEFORE> corpus/QUALITY.md \| sha256sum` |

Landing sequence (run from the lane root by the landing agent, not by this seat):

```
BYTES=$(wc -c < corpus/QUALITY.md); LINES=$(wc -l < corpus/QUALITY.md)
SHA=$(head -c "$BYTES" corpus/QUALITY.md | sha256sum | cut -d' ' -f1)
sed -e "s/<BYTES_BEFORE>/$BYTES/g" -e "s/<LINES_BEFORE>/$LINES/g" \
    -e "s/<SHA256_BEFORE>/$SHA/g" block.md > block.resolved.md
grep -c '<[A-Z0-9_]*>' block.resolved.md        # must print 0
cat block.resolved.md >> corpus/QUALITY.md
```

Post-append assertions, each fail-closed: `git diff --unified=0 corpus/QUALITY.md` shows only `+` lines and
no `-`/context replacement, i.e. only lines after the pre-append EOF; `head -c "$BYTES" corpus/QUALITY.md |
sha256sum` still prints `$SHA`; `wc -l corpus/QUALITY.md` = `$LINES + 14`; `grep -nE '^\| (R22|R23|R26|R27|R28|R29) ' corpus/QUALITY.md`
still prints the row lines `226 227 249 250 263 264` (measured at draft head by that exact command). If an
earlier round-37 append lands first, all three values and those six row lines must be re-measured before
substitution — the preamble states this and is why the values are placeholders, not literals.

## 3. Grounding evidence — every load-bearing clause, observed

| clause in the rows | locator | command run (draft head `b3620681`) | observed output |
|---|---|---|---|
| R30 defect text is verbatim D6 | `corpus/lessons/round-36-verifier-spotcheck.md:160-162` | `sed -n '160,162p'` | `- **D6 — E9 limb (b) fail-open.** \`r36-closure.sh:465-466\` maps a failing \`git status\` read to \`0\` dirty lines` / `(\`2>/dev/null\`, \`${porcelain:-0}\`); make the limb fail closed.` |
| status read swallows its error | `corpus/instruments/r36-closure.sh:465` | `sed -n '465,466p'` | `porcelain=$(git --no-optional-locks -C "$srepo" status --porcelain 2>/dev/null \| count_lines)` |
| the empty result is defaulted to clean | `corpus/instruments/r36-closure.sh:466` | `sed -n '465,466p'` | `porcelain=${porcelain:-0}` |
| `0` is the passing value on that limb | `corpus/instruments/r36-closure.sh:480-481` | `sed -n '476,486p'` | `printf 'status-dirty=%s,scratch-seat-dirs=%s,...' "$porcelain" ...` / `[ "$porcelain" -eq 0 ] && [ "$left" -eq 0 ] && [ "$head_ok" -eq 1 ] \` |
| same fail-open direction on a presence check | `corpus/instruments/r36-closure.sh:309`, `:322` | `grep -n 'ph\b'`, `sed -n '322p'` | `ph=$(grep -cF -- "filled by the $(printf 'L1')" SCORECARD.md 2>/dev/null); ph=${ph:-0}` … `[ "$ph" -eq 0 ] && [ "$lh" -eq 0 ] && [ "$section" -eq 1 ] \` |
| the class predates round 36 | `corpus/instruments/r35-defect-closure.sh:164-168` | `sed -n '163,169p'` | `ph=${ph:-0}` / `lh=${lh:-0}` … `[ "$ph" -eq 0 ] && [ "$lh" -eq 0 ] && [ "$cor" -ge 1 ] && exit 0` |
| the admissible direction (zero default, non-zero pass value) | `corpus/instruments/r36-closure.sh:766-768` | `sed -n '765,770p'` | `cases=$(grep -c '^selftest case=' "$f" 2>/dev/null); cases=${cases:-0}` … `[ "$cases" -eq 9 ] && [ "$verdicts" -eq 9 ] && [ "$summary" -eq 1 ] \|\| return 1` |
| negative control count | `corpus/instruments/r36-closure.sh` | `grep -cF 'porcelain:-0' corpus/instruments/r36-closure.sh` | `1` (line 466) |
| proposed instrument absent at draft head | `corpus/instruments/r37-closure.sh` | `git ls-files corpus/instruments/r37-closure.sh` | empty |
| R30's capture rows exist and cover this shape | `corpus/QUALITY.md:89` (R15), `corpus/QUALITY.md:96` (R17) | `grep -n '^\| R1[57] '` | R15 "A named open defect stays open only while its runnable closure check exits non-zero…"; R17 "An instrument limb is claimed load-bearing only when a committed one-limb mutant makes that limb's kill command differ…" |
| R31's proposal text is verbatim | `considerthese/2026-10-26.md:35` | `cat -n considerthese/2026-10-26.md` | `7. **Keep a proposal-status ledger.** Two of my proposals were mined in r24 (Q9, the render/raw-sha debt), and per-platform severity is now F13/F17. Tracking proposed → adopted → declined would let me calibrate which suggestions are useful, and stop repeating closed ones like the anchorcheck regression test (now superseded by \`anchorcheck.py\` fail-closed in r28).` |
| old→new columns are the ledger's own shape | `corpus/knowledge/considerthese-proposals-ledger.md:22-33` | `awk 'NR>=22 && NR<=27'` + `awk 'NR>=28 && NR<=35'` + `grep -c '\| `unchanged` \|'` | `## Round-31 status flips (appended 2026-10-25)` at `:22`; header `\| proposal \| status before (row above) \| status after round 31 \| evidence / reason \|` at `:26`; the flip row at `:28`; five `unchanged` rows at `:29-33` (grep count `5`). The cite stops at `:33` — the closing audit sentence is `:35`, deliberately outside the quoted range. |
| partial-close caveat | `corpus/knowledge/considerthese-proposals-ledger.md:13` | `sed -n '13p'` | `| 3. Point a round at bounty craft and SHONEN box 2 | partially landed | 29 | … The lesson explicitly records the claims.json theme mismatch and SHONEN box 2 still open; do not treat the whole proposal as closed. |` |
| reflection scoping header | `corpus/knowledge/considerthese-proposals-ledger.md:3` | `sed -n '1,17p'` | `source: \`considerthese/2026-10-25.md\` — own-work path; proposals 1–6, numbered list under "Self-improvement suggestions"` |
| ledger tracked; 2026-10-26 absent | ledger path | `git ls-files --error-unmatch …`; `wc -c -l`; `sha256sum`; `grep -cF '2026-10-26' …` | tracked; `35 6185`; `c354ca02…a1629c2`; `0` |
| preamble row lines are the current ones | `corpus/QUALITY.md` | `grep -nE '^\| (R22\|R23\|R26\|R27\|R28\|R29) '` | `226 227 249 250 263 264` |

## 4. Structural verification of the block

- **Table shape.** `awk '{n=gsub(/\|/,"|")}'` over the block: the four table lines carry exactly 4 pipes each
  (header, separator, R30, R31), i.e. three cells; no cell contains an unescaped pipe, so the R6 table does not
  break column alignment.
- **Anchor gate.** `python3 corpus/instruments/anchorcheck.py corpus/QUALITY.md` → `20 in-range cite instances,
  1 bad; 20 distinct anchors; … BASE-ABSENT=0`, exit 1. Same tool on the appended copy
  (`KASEGI_LANE_ROOT=<lane>`): `32 in-range cite instances, 1 bad; 32 distinct anchors; … BASE-ABSENT=0`,
  exit 1. The 12 added anchors all resolve `IN-RANGE(LANE)`; the single bad class is the same pre-existing
  `PAST-EOF md:77 README.md:159 (file has 14 lines)` in both runs, so the append adds no failure and removes
  none. (The copy is outside the lane, so `KASEGI_LANE_ROOT` was set explicitly; without it every cite of the
  copy classifies `BASE-ABSENT` — a property of the checker's base resolution, not of the block.)
- **Delivered block is the verified block.** Extracting the fenced block from this receipt (the
  four-backtick `markdown` fence pair) gives 4961 bytes / 14 lines with sha256
  `d2c59ad556145d7b0e948638dd8fe8e35ba86c1cd07b4d77e565bf7c0f39c282` — the digest taken from the scratch
  `block.md` before it was removed. A transcription drift in this receipt would change that digest, so the
  block above is byte-for-byte the block that was anchor-checked.
- **Byte line.** 38265 + 4961 − 0 = 43226; 264 + 14 = 278 — matches the concatenated copy.
- **Duplication check.** `grep -c '^| R30 \|^| R31 '` over the existing file prints `0` and exits `1` (the
  no-match status is the expected state here — the count is the signal, not the exit code, which is exactly the
  direction R30 separates), so both ids are free at draft head; the last existing row is R29 at line 264.

## 5. Findings

**F1 — the frozen claims name a ledger path that does not exist.** `.ufo/waves/round-37/claims.json:78` reads
verbatim: `"considerthese": "2026-10-26.md: proposal 7 mined -> QUALITY R31 + corpus/considerthese-ledger.md; …"`.
`git ls-files corpus/considerthese-ledger.md` → empty, `ls corpus/considerthese-ledger.md` → `No such file or
directory`, and the string appears in the tree only inside `.ufo/waves/round-37/claims.json` and the dispatch
copies. The tracked durable ledger is `corpus/knowledge/considerthese-proposals-ledger.md` (round-31, tracked in
`eecad59`). R31 therefore cites the tracked path and records the shorthand as a path note; if the lane instead
intends a new consolidated file at the shorthand, the row's single path occurrence is the only token to change.
This is the same class as round-36 routed defect D2 (a false path in a record), caught here before landing.

**F2 — `anchorcheck.py`'s CITE alternation has no `considerthese/` prefix**, so any
`considerthese/YYYY-MM-DD.md:NN` cite is invisible to the gate (it matches no arm of `_CITE_PATH`,
`corpus/instruments/anchorcheck.py:165-172`). Measured: the appended copy resolves 12 of R30/R31's 13 backticked
anchors and silently skips `considerthese/2026-10-26.md:35`. Pre-existing: R23's
`considerthese/2026-10-25.md:76` is skipped the same way at `corpus/QUALITY.md:227`. R31 compensates by carrying
three ledger anchors that the gate does check; the proposal cite itself remains gate-invisible until a
`considerthese` arm is added — an instrument change, out of this seat's scope.

**F3 — `QUALITY.md` is already red at the anchor gate before this append.** `PAST-EOF md:77 README.md:159
(file has 14 lines)` — `corpus/QUALITY.md:77` cites a line the file no longer has. Reported, not repaired: the
row at line 77 is outside this item. The append neither adds nor removes a fail class (1 bad before, 1 bad
after).

**F4 — R30's `M37-2` anchor is not observable at draft head.** There is no `corpus/lessons/round-37.md` yet
(`find .ufo/waves/round-37 -name '*lesson*'` → empty; `corpus/lessons/` ends at `round-36.md`), and
`claims.json` records only `M37-1..M37-5 minted in round-37 lesson`. The row names M37-2 in R29's
"minted this round" style, so landing must confirm the round-37 lesson's § Mistakes actually numbers the
fail-closed defect as M37-2; if it numbers it differently the row's identifier is a one-token substitution. The
row does not depend on that identifier for its evidence — the D6 text, the three instrument locators and the
E14 command form are all observed at draft head.

**F5 — the ledger append R31 requires is owed by another seat.** A live peer `ScribeConsiderthese` is running
and `corpus/knowledge/considerthese-proposals-ledger.md` has no 2026-10-26 section (`grep -cF '2026-10-26'` →
`0`). R31 states the requirement; it does not claim the append landed. Flagged to that peer in the same run.

**F6 — `corpus/instruments/r37-closure.sh` is untracked at draft head**, so R30's `grep -cF 'porcelain:-0' … →
0` is written as a landing requirement with that fact stated in the row, not as a measurement.

**F7 — the ledger row R31 cites carries a stale instrument pin (verified here, surfaced by peer
`ScribeConsiderthese`).** `corpus/knowledge/considerthese-proposals-ledger.md:28` pins
`score-gap.py` at sha256 `855869bf97ae2081…` / 548 lines, while the file at draft head is
`57584fda83b813e44fb2e2cb6cb2b1e4af1dd20f07877a6b119db9ba9feb43cf` / 554 lines (`sha256sum`,
`wc -l corpus/instruments/score-gap.py`). The round-36 lesson already records "existing ledger re-pin owed".
R31 is a criterion row and does not restate the pin, so this item requires no re-pin; a round that edits
`:28` must re-pin rather than copy the literal (R19).

## 6. Scope honoured / not done

- Wrote only this receipt under `.ufo/waves/round-37/wave1/` and files under the seat scratch dir. No edit to
  `corpus/QUALITY.md`, no lane/fleet/`shokuknow` write, no `git` mutation, no subagent dispatch, no
  `agent://all` broadcast, no tool install.
- Did not run `r37-closure.sh` (absent), the wave-1 suite, or any gate: none is this item's, and this seat does
  not verify the round.

## 7. Tooling and environment

No installs or upgrades — nothing was needed. `git 2.56.0` at `/usr/bin/git`; one read-only call in a busy
temporary shell reported `command not found: git`, so every later git call used the absolute path. Scratch
`/fast/scratch/hyaku/kasegi-r37/ScribeQualityRows/` created with `mkdir -p` and removed with
`rm -rf -- <dir>` before this receipt was written: `test -d <dir>` → non-zero (`scratch-removed`), and
`ls /fast/scratch/hyaku/kasegi-r37/` lists only sibling seat dirs. Scratch artifact digests, recorded before
removal: `block.md` `d2c59ad5…f39c282`; appended copy `c6658e4c…2ba8a320`; `ac-base2.txt` `187628b7…93f0e1`;
`ac-app2.txt` `60fe19c5…a092ff`; `measurements.txt` `3a16225f…1fdd7b`.
