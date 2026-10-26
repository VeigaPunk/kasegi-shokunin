# ExecQualityAppends — round 34, wave 1 (R3 note, R22, R23, R24)

Seat: `ExecQualityAppends` (leaf). Scope: routed defect **R3** from
`corpus/lessons/round-33-verifier-spotcheck.md:171-173`, plus the two new record criteria from the wave
spec, plus **R24** added by the L1's in-flight instruction so the R4 clause of
`corpus/instruments/r-defect-closure.sh` goes green. Assigned path: `corpus/QUALITY.md` only (append).
No other file written by this seat.
No git/jj mutation (no `add`/`commit`/`push`/`jj`), no subagent, no `agent://all`.
No tool installed or upgraded (no pacman, no `uv tool`, no binary fetched).
Scratch: `/fast/scratch/hyaku/kasegi-r34/ExecQualityAppends/`, removed before yield — §7.

## Report

### 1. Before measurement (worktree at seat start)

```
$ wc -l corpus/QUALITY.md
213 corpus/QUALITY.md
$ sha256sum corpus/QUALITY.md
00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087  corpus/QUALITY.md
$ tail -c 300 corpus/QUALITY.md
provenance clause. At round-33 composition the checker was absent from the base
(`git cat-file -e 690b69da:corpus/instruments/capture-binding-check.py` → exit 128), so no landed
verdict is claimed by these rows; a later reader runs the command and reads its own output.
exit=0
$ git status --short
?? .ufo/waves/round-34/wave1.ready
?? .ufo/waves/round-34/wave1/
```

Citations of `QUALITY.md` by line number, inventoried before the edit (whole lane, excluding
`.ufo/waves/round-2x/3x`):

```
$ grep -rno "QUALITY\.md:[0-9]\+" --include=*.md --include=*.py --include=*.sh . | … | sort -n | uniq -c
      2 77       1 83       1 89       2 95       1 169
```

Cited by `corpus/knowledge/considerthese-proposals-ledger.md:29,32`, `corpus/lessons/round-31.md:108,119,147`
and `corpus/lessons/round-33-verifier-spotcheck.md:171`. R6 binds: none of those lines may move.

### 2. Appended block (15 lines, `214-228`; `R6` form, assigned wording)

```
$ sed -n '214,228p' corpus/QUALITY.md | nl -ba -v214

   214
   215	## Round-34 additions — pre-freeze satisfiability and reflection cadence (append-only)
   216
   217	R6 form: R20's row (line 169) and every earlier line stay byte-identical; the R20 note and the two
   218	rows below are appended at the end of the file.
   219
   220	Note (round 34): R20's 'exactly one registry-row URL' reading is superseded by the C1 erratum-2 per-id
   221	reading — a URL shared by two different registry rows is informational `multi_row_url=N`, not a
   222	failure (SCORECARD round-33 section, erratum 2).
   223
   224	| id | criterion | grounded in |
   225	|---|---|---|
   226	| R22 | A frozen claim predicate is checked for satisfiability against base bytes before freeze: every literal constant and regex in the predicate and kill rule is run against the base tree; an unsatisfiable literal is fixed before data, never waived by a post-freeze erratum. Grounded in: round-33 verifier R2; M34-2. | `corpus/lessons/round-33-verifier-spotcheck.md:167-169` (R2 — the frozen parenthetical that literally read `bound=38`); M34-2 at `.ufo/waves/round-34/claims.json` → `non_claim_frontier_items.mistake` |
   227	| R23 | A lane records an event-driven reflection cadence: burst activity and idle stretches are reviewed within the next round's lesson, citing the considerthese file and date. Grounded in: considerthese/2026-10-25.md proposal 6. | `considerthese/2026-10-25.md:76` proposal 6 (2026-10-25) |
   228	| R24 | A counter's mutant kill rule is recorded and tightened: the selftest clause requires one `selftest case=<name>` verdict line per case with cases>=11, so a summary-only forgery (cases=0 failures=0) cannot satisfy it. | `corpus/lessons/round-33-verifier-spotcheck.md:174-176` (R4) and the round-34 erratum at `corpus/lessons/round-33.md:215-226` — the frozen rule **caught 3 of 4**, skip-selftest (M4) survived (`.ufo/waves/round-33/wave1/RevClaimsFreeze.md:75,172`, finding F-5); M34-1 at `.ufo/waves/round-34/claims.json` → `non_claim_frontier_items.mistake` (the 'all mutants killed' overstatement) |
```

Grounding resolved in-repo, not copied from prose:

```
$ sed -n '167,169p' corpus/lessons/round-33-verifier-spotcheck.md | cut -c1-70
- **R2** Frozen C1 predicate/kill-rule text ("exactly one registry-row URL", "zero or two+")
  literally reads `bound=38`; erratum 1 supersedes it. Append erratum 2 restating the parenthetical
  per-id, and add a pre-freeze step that evaluates each literal predicate against base bytes for
$ sed -n '173,175p' corpus/lessons/round-33-verifier-spotcheck.md | cut -c1-70
- **R4** C1 counter mutants 3/4 under the frozen kill rule: skip-selftest survives (`RevClaimsFreeze.md`
  F-5), accept-record-without-url survives the plain run. Report lines 41/49 ("all killed") overstate.
  Tighten the kill rule to require `cases>=11` with one `selftest case=` verdict line per case; …
$ grep -n "Event-driven reflections" considerthese/2026-10-25.md
76:6. **Event-driven reflections.** The lane did three rounds in under three hours after 4.5 idle days; a push
```

`corpus/lessons/round-34.md` does **not** exist yet (`ls` → ENOENT), so the mistake grounding cites the
frozen `.ufo/waves/round-34/claims.json` byte instead of a lesson file that would resolve only after
another seat lands it — the `round-31` lesson §6 defect (rows citing a not-yet-existing lesson).

### 3. Append-only proof (R6)

```
$ git diff --numstat -- corpus/QUALITY.md
15	0	corpus/QUALITY.md
$ git diff --stat -- corpus/QUALITY.md
 corpus/QUALITY.md | 15 +++++++++++++++
 1 file changed, 15 insertions(+)
$ git diff -- corpus/QUALITY.md | grep '^@@'
@@ -211,3 +211,18 @@ whose rule A supplies the manifest clause, rule B the one-registry-row `url` cla
$ wc -l corpus/QUALITY.md ; stat -c%s corpus/QUALITY.md
228 corpus/QUALITY.md
30340
$ sha256sum corpus/QUALITY.md
77d99df9abf57a66065dbe927ce95f0ddf8acbfba237fefd163bdd3871751af8  corpus/QUALITY.md
```

Byte-level prefix identity — the pre-edit file is a literal prefix of the new file, which is what keeps
every cited line at its number. The before copy is taken from `HEAD` (the lane's only modification of
this file is this seat's append; the first scratch copy was removed after its digest was recorded):

```
$ git show HEAD:corpus/QUALITY.md > "$S/QUALITY.head.md"
$ sha256sum "$S/QUALITY.head.md"
00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087  /fast/scratch/hyaku/kasegi-r34/ExecQualityAppends/QUALITY.head.md
$ n=$(stat -c%s "$S/QUALITY.head.md"); echo "before_bytes=$n"
before_bytes=28370
$ head -c 28370 corpus/QUALITY.md | sha256sum
00781e095d808e18e733830931d7cb8b279b1d045848ed3901d33de403b0b087  -
$ diff <(head -n 213 corpus/QUALITY.md) "$S/QUALITY.head.md" && echo prefix_identical_lines_1_213=yes
prefix_identical_lines_1_213=yes
$ sed -n '169p' corpus/QUALITY.md | sha256sum
c27022fbca394e14d918484612c2c9e6697a0f0f675625c2cf77173148ddde88  -
```

Line-hash comparison for the cited anchors (measured against the pre-edit bytes; valid for the landed
file because the prefix is byte-identical and R24 only added a line at EOF):

```
line=77   before=02a14af744d1 after=02a14af744d1 same=y
line=83   before=e60443c926ee after=e60443c926ee same=y
line=89   before=e16d17c6262f after=e16d17c6262f same=y
line=95   before=769b49dabb1f after=769b49dabb1f same=y
line=169  before=c27022fbca39 after=c27022fbca39 same=y
```

Structural counts on the landed file:

```
$ grep -cE '^\| R[0-9]+ \|' corpus/QUALITY.md
24
$ grep -c "^Note (round 34):" corpus/QUALITY.md
1
```

21 pre-existing R rows + R22 + R23 + R24 = 24. Exact-wording check (whitespace-normalised containment
of the four assigned literals):

```
$ python3 -c '…norm(s)=re.sub(r"\s+"," ",s).strip(); norm(assigned) in norm(open("corpus/QUALITY.md").read())…'
R3 note: present=True
R22: present=True
R23: present=True
R24: present=True
```

### 4. What the R3 and R4 closure checks read (emulated from the instrument's current bytes)

`corpus/instruments/r-defect-closure.sh` is still an untracked worktree file owned by peer
`ExecRDefectClosureSuite` (`git status` → `??`, `sha256 7aca98b344d4ca8718344cc09c63b67b2382fd327d579e6b6a2c713b351e08ab`).
`check_r3` (`:163-179`) keys on the first `Note (round 34)` block via `block_from` (`:105-107`, print
from the match to the next blank line) and requires `R20`, `exactly one`, `supersed*`, `per-id|per id`.
`check_r4` (`:183-203`) binds the tightened kill rule to the `| R24 |` row when that row exists
(`:193-198`: row must carry `kill rule`, `selftest case=`, and `per case|>= ?11`), falling back to one
SCORECARD paragraph through `para_grep` (`:111-117`, `awk` paragraph mode, case-insensitive substring).
The helper bodies were copied verbatim into the checks below rather than running the suite (§6):

```
$ awk -v pat='[Nn]ote .round 34.' '$0 ~ pat { f=1 } f { print } f && /^[[:space:]]*$/ { exit }' corpus/QUALITY.md
Note (round 34): R20's 'exactly one registry-row URL' reading is superseded by the C1 erratum-2 per-
reading — a URL shared by two different registry rows is informational `multi_row_url=N`, not a
failure (SCORECARD round-33 section, erratum 2).
                                    # block_from(): note at :220 sits below R20 at :169
$ row=$(grep '^| R24 |' corpus/QUALITY.md)
$ { [ -n "$row" ] && printf '%s\n' "$row" | grep -qi 'kill rule' \
    && printf '%s\n' "$row" | grep -q 'selftest case=' \
    && printf '%s\n' "$row" | grep -Eqi 'per case|>= ?11'; }; echo "row_limb_exit=$?"
row_limb_exit=0                     # check_r4 limb 1 is satisfied by the R24 row alone
```

Isolation — the R24 row is the only carrier in the bar, and the SCORECARD fallback cannot mask its
absence:

```
$ awk -v a='kill rule' -v b='selftest case=' -v c='per case' … SCORECARD.md
scorecard_para_found=0
scorecard_para_exit=1               # no qualifying paragraph anywhere on the scorecard
$ grep -v '^| R24 |' corpus/QUALITY.md > "$S/no-r24.md" ; grep '^| R24 |' "$S/no-r24.md"
fixture_row_empty=y                 # row gone and fallback absent -> the R4 clause re-opens
```

Peer `ScribeQualityDraft` measured the before state independently: on digest `eb20eafc…` (this seat's
bytes before R24 landed) `r-defect-closure.sh --root` printed `R4 … open=1`, which its receipt
attributes to the missing R24 row — consistent with the isolation above. The instrument moved during
the wave (it was `para_grep`-only when first read and is row-bound at seat end); these checks quote the
`7aca98b3…` body.

### 5. Cross-references and peer state (disclosed, not written by this seat)

The R3 note's parenthetical resolves: peer `ExecErratum2` landed erratum 2 in the SCORECARD round-33
section —

```
$ grep -n "Erratum 2\|erratum 2" SCORECARD.md | head -2
1014:**Erratum 2, disclosed (round-34 append, round-25 form).** The frozen C1 kill-rule
1028:**Pre-freeze satisfiability step, recorded (QUALITY R22).** Before any claim is frozen, each
```

`SCORECARD.md:1028` names `QUALITY R22`, so that cross-reference is two-way and now resolves.
`git status` also shows peers' `SCORECARD.md`, `corpus/source-snapshots/round-32/manifest.json`,
`corpus/instruments/frontier-recheck-count.py` and the new `corpus/source-snapshots/round-34/` — none
touched here.

Judgment call recorded for the L1: the wave bullet says "below the R20 row", while the same handout
mandates append-only/R6. I appended at EOF (the only placement that keeps `:169` and the other four
cited lines at their numbers) and made the note name R20 explicitly; a literal insertion under `:169`
would have shifted `:170-213` by +3 and broken the five citations above.

### 6. Not run, and one draft not adopted

Per the wave rule ("skip build/lint/tests while the editing wave is in flight") the full
`r-defect-closure.sh` suite, `anchorcheck.py` and every formatter were **not** run. R6's anchor guarantee
is discharged by the byte-prefix identity plus the per-line hash comparison in §3; the R3/R4 clause
behaviour is discharged by copying the instrument's own helper bodies verbatim (§4), not by a suite run.

`ScribeQualityDraft` produced `.ufo/waves/round-34/wave1/ScribeQualityDraft-block.txt` (3971 B,
`sha256 41c51a86…afe2bb`) as a replacement for lines `215-227`, with three deltas: expanded note naming
S029/S006 and citing erratum 1 lines, R24 included, and **R22's grounding changed to drop M34-2**. I did
**not** adopt it: the L1's instruction fixes the R3-note, R22 and R23 wording and supplies R24's text
verbatim, and adopting the block would rewrite the assigned R22 criterion/grounding mid-wave. Its
substantive finding is passed to the L1 rather than silently applied: M34-2 as filed is the
`<LANE_HASH>` placeholder defect (R1), not the unsatisfiable-literal defect, so the mandated R22 sentence
"Grounded in: round-33 verifier R2; M34-2." cites a mistake of a different class — the same pairing
appears at `SCORECARD.md:1034-1035` and `ExecErratum2.md:124`. Either a new mistake id (M34-3) or an L1
wording change closes it; this seat keeps the mandated text and flags it here and in §Risks.

### 6.1 Post-landing review by ScribeQualityDraft — four findings, dispositions

Its addendum raised four defects in the appended R24. Two were mine to fix and are fixed in the row's
**grounding cell** (the criterion text is the L1's verbatim wording and stays byte-identical); two are
wording calls for the L1 and are not applied:

| # | finding | disposition | evidence |
|---|---|---|---|
| 1 | My grounding said "3 of 4 mutants **survived** the frozen rule" — direction inverted | **accepted, fixed**: cell now reads "the frozen rule **caught 3 of 4**, skip-selftest (M4) survived" | `.ufo/waves/round-33/wave1/RevClaimsFreeze.md:75` — M4 skip-selftest "**NOT caught — finding F-5**", M1/M2/M3 each "**caught**"; `:172` "M1/M2/M3 caught … M4 skip-selftest is NOT caught"; `corpus/lessons/round-33.md:215` erratum — "the frozen kill rule caught 3 of 4" |
| 2 | `cases>=11` is the round-33 floor, while this round's C1 floor is N>=19 | **referred to L1**: the criterion text is mandated verbatim; a floor change is a wording decision | `.ufo/waves/round-34/claims.json` C1 counting command "selftest cases=N … (N>=19)" vs `corpus/lessons/round-33-verifier-spotcheck.md:176` "`cases>=11`" |
| 3 | Cite `:173-175` includes R3's tail; R4 is `:174-176` | **accepted, fixed**: cell cites `:174-176` | `awk 'NR>=171 && NR<=177'` on the spotcheck file: `:174` is the `- **R4** …` heading, `:173` is R3's "bytes violate (S029, S006)" line |
| 4 | The criterion states a past act, and does not bind `cases=N` to the number of printed verdict lines | **referred to L1**: criterion text is mandated verbatim | this row carries the assigned literal unchanged (`Grounded in:` list omitted from the row on the L1's text) |

The grounding-cell fix moved the file from `2bb724fb…` (the digest in the first version of this
receipt) to `77d99df9…` (§3); criterion bytes for the R3 note, R22, R23, R24 are unchanged and the four
exact-wording checks still pass. `check_r4` still reads the row green (`row_limb_exit=0`, §4): the
criterion's `kill rule` / `selftest case=` / `per case` tokens are in the criterion cell, not the
grounding cell.

### 7. Scratch cleanup

```
$ ls -d /fast/scratch/hyaku/kasegi-r34/ExecQualityAppends
ls: cannot access '/fast/scratch/hyaku/kasegi-r34/ExecQualityAppends': No such file or directory
scratch_ls_exit=2        # expected: before copy + no-limb fixture removed after the digests above
```

## Risks

- The note corrects R20 by appended text, so a reader of the R20 row alone still sees "exactly one"; the
  note is at `corpus/QUALITY.md:220-222` and names R20 by number. A same-line suffix on `:169` (the other
  R6-allowed form) remains available to the L1 and would also keep anchors valid.
- R22's mandated "M34-2" grounding cites a mistake of a different class (§6); correction belongs to the
  L1 (mint M34-3 or reword), not to this append.
- `corpus/lessons/round-34.md` is not landed yet; the round-34 lesson's `## Mistakes` should restate
  M34-1/M34-2 so the R22/R24 grounding has a lesson-side address.
- R4's row limb is satisfied only by the R24 row in this file; removing it re-opens the clause (no
  SCORECARD fallback paragraph exists: `scorecard_para_exit=1` in §4).
- R24's mandated criterion carries `cases>=11`, the round-33 floor, while this round's C1 floor is N>=19
  (§6.1 finding 2); if the bar is meant to state the current floor the L1 must reword — the criterion is
  unchanged here because the text was supplied verbatim.
- R24's mandated criterion states the tightening as a past act and does not bind `cases=N` to the count
  of printed `selftest case=` lines (§6.1 finding 4); a forged `cases=19 failures=0` with zero case lines
  is excluded only by implication. Wording decision for the L1.
- No criterion ceiling is asserted outside the bar: the only range-form mention is
  `.ufo/waves/round-34/build-spec.py:45`, which already reads "record R1–R23"; it now understates R24,
  and updating it was out of this seat's write scope.
