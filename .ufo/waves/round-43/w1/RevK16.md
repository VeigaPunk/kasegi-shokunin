# RevK16 — round 43, adversarial review of the K16 placeholder limb (RD42-4 class)

Seat: `RevK16` (leaf reviewer, kasegi-shokunin round 43). Base `ab98fac9dce87130bc4f66de89e30650d63943dc`.
Item under attack: `.ufo/waves/round-43/w1/ExecK16Placeholder.sh` (213 lines, sha256
`d7c33c9efdcfb5ab0feeac494da6a12d83d95d9b0d2d20b2bd121ba7af5a74cb` — the same digest the executor's receipt
claims), snapshot-copied to `$S/k16.sh` before grading so the review is of one fixed artifact.
Scratch `S=/fast/scratch/hyaku/kasegi-r43/RevK16/` (removed before yield). Disk guard read before the pass:
`/fast/scratch/hyaku 26% 598.5G free`, `/tmp 17% 106.8G free`, `/var/tmp 38% 557.1G free`.
Environment: `Python 3.14.8`, `GNU bash, version 5.3.20(1)-release`. Review time `2026-10-28T16:45:35Z`.
No tool installs, no network fetch, no mutating git (`git archive` / `rev-parse` / `log` only); writes confined to
`$S` and this receipt.

## Method

Base export: `git -C <lane> archive ab98fac9dce87130bc4f66de89e30650d63943dc | tar -x -C $S/base` (8384 files).
Every case is graded by the limb's own entry point, exactly as the suite will call it:

```
$ . ./k16.sh ; K16_VERBOSE=1 check_k16 <tree>
```

`K16_VERBOSE=1` adds the `K16 unresolved file=… line=… heading=… clause=…` diagnostic on stderr (the limb's own
documented diagnostic switch), so each verdict is quoted with the section that produced it. Fixture trees are
minimal: `corpus/lessons/round-42.md` plus, where the case needs it, `LOG.md` / `SCORECARD.md` / `SHONEN.md`.
`aft` = base export + the three `ScribeCorrections.{lesson42,log,scorecard}.txt` blocks appended to their files.
`ysim2` = `aft` + `ScribeScorecardRound43.append.md` → `SCORECARD.md`, `ScribeLogEntry.log-entry.md` → `LOG.md`,
`ScribeShonenLines.append.md` → `SHONEN.md`.

Consolidated battery (`for f in …; do out=$(K16_VERBOSE=1 check_k16 "fx/$f" 2>&1); rc=$?; …`), verbatim newlines
rendered as `|`:

```
base rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=52 heading=Wave-2 falsification clause=schedule|payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0|
aft rc=0 :: payload=sections=491,promises=1,fenced=0,unresolved=0 closed=1|
ysim2 rc=0 :: payload=sections=494,promises=1,fenced=0,unresolved=0 closed=1|
empty rc=1 :: payload=sections=0,promises=0,fenced=0,unresolved=0 closed=0|
a1reword rc=1 :: payload=sections=2,promises=0,fenced=0,unresolved=0 closed=0|
a2tablecell rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=1 heading=ound 42 test clause=to-be-filled|payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0|
a3markerbefore rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=5 heading=Wave-2 falsification clause=schedule|payload=sections=3,promises=1,fenced=0,unresolved=1 closed=0|
a4twopromises rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Wave-2 falsification clause=schedule|payload=sections=3,promises=1,fenced=0,unresolved=1 closed=0|
a5fenced rc=1 :: payload=sections=3,promises=0,fenced=1,unresolved=0 closed=0|
a5fencedheading rc=1 :: payload=sections=2,promises=0,fenced=1,unresolved=0 closed=0|
a6mentions rc=1 :: payload=sections=9,promises=0,fenced=0,unresolved=0 closed=0|
a7blockquote rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Wave-2 falsification clause=to-be-filled|payload=sections=3,promises=1,fenced=0,unresolved=1 closed=0|
a8fencedmarker rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Wave-2 falsification clause=schedule|payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0|
a9substring rc=0 :: payload=sections=2,promises=1,fenced=0,unresolved=0 closed=1|
a10tbdcase rc=1 :: payload=sections=3,promises=0,fenced=0,unresolved=0 closed=0|
a11unclosedfence rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Wave-2 falsification clause=schedule|payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0|
a12openmarker rc=0 :: payload=sections=2,promises=1,fenced=0,unresolved=0 closed=1|
a13quotedmarker rc=0 :: payload=sections=2,promises=1,fenced=0,unresolved=0 closed=1|
a14dupheading rc=0 :: payload=sections=3,promises=1,fenced=0,unresolved=0 closed=1|
a15tableopen rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Mistakes clause=to-be-filled|payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0|
a16tablelater rc=1 :: payload=sections=2,promises=0,fenced=0,unresolved=0 closed=0|
a17crossfile rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Wave-2 falsification clause=schedule|payload=sections=3,promises=1,fenced=0,unresolved=1 closed=0|
a18unbalanced rc=1 :: K16 unresolved file=corpus/lessons/round-42.md line=3 heading=Wave-2 falsification clause=schedule|payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0|
a19rewordedstand rc=0 :: payload=sections=3,promises=1,fenced=0,unresolved=0 closed=1|
```

Three further case-sensitivity/line-split probes (`a20lowerheading`, `a21lowermarker`, `a22wrappedheading`) all
printed `rc=1 :: …heading=Wave-2 falsification clause=schedule|payload=sections=2,promises=1,fenced=0,unresolved=1 closed=0|`.

Doubles: two consecutive runs over `base` printed byte-identical payloads, rc=1 both; one run costs
`real 0m0.058s`. `check_k16 empty` / `check_k16 nope` / bare `check_k16` all print `closed=0` rc=1 (fail-closed,
with `K16 root-not-found root=nope` on stderr for the missing root).

## Findings, by severity

### F1 — false close: a correction naming a *different, longer* heading closes the promise (major)

Fixture `a9substring`: section `## Wave-2 falsification` promises `when the round-42 falsify wave reports`; the only
correction line names `## Wave-2 falsification notes`, a section that does not exist in the file. Observed
`rc=0 :: payload=sections=2,promises=1,fenced=0,unresolved=0 closed=1`. The limb matches the heading with a raw
substring test (`heading in line`) over `[3:]` of the heading, so any longer heading that has the graded heading as
a prefix satisfies it. This contradicts the receipt's own rule (`names the heading`) and is the M42-2
token-boundary class on the resolution side: the value is matched as a substring, not a whole token.
Suggested one-limb fix: require the heading as a delimited token — the `## <heading>` form, or the heading text
whose following character is not a word character and whose preceding character is not a word character.

### F2 — false close: identical heading text on two sections resolves both (major, live in the graded file)

Fixture `a14dupheading`: two `## Gate` sections; the first promises, the second does not; the correction says `the
second `## Gate` section's admitted row is superseded`. Observed
`rc=0 :: payload=sections=3,promises=1,fenced=0,unresolved=0 closed=1` — the first `## Gate`'s promise is closed by
a correction aimed at the other instance. This is not hypothetical: `corpus/lessons/round-42.md` carries duplicate
`## Gate` headings at lines 45 and 58 (`grep -n '^## Gate'` → `45:## Gate`, `58:## Gate`), so any promise that ever
lands in either Gate section is closed by a correction naming "Gate".
Suggested fix: carry the heading's line number or its first body line in the correction, or grade sections by
`(heading, line)` identity rather than heading text.

### F3 — false close: a correction quoted as an unlanded draft resolves the promise (moderate)

Fixture `a13quotedmarker`: `The draft block reads "Correction (round 43): the `## Wave-2 falsification` section is
superseded" and is not yet landed.` Observed `rc=0 :: payload=sections=2,promises=1,fenced=0,unresolved=0 closed=1`.
The promise side strips backticked and double-quoted spans ("quoted text is evidence about a promise, never the
promise"); the resolution side does not, so a quoted draft closes the check. Suggested fix: run `strip_quoted` on
the candidate resolution line before the marker/heading test — a one-limb change that makes both sides use the same
quote rule.

### F4 — payload contradicts the documented section definition, and H1 headings get a mangled name (moderate)

The limb header and the executor receipt both define a section as a line matching `^## ` (body to the next `^# ` or
`^## `). The implementation's `HEADING_RX = re.compile(r"^#{1,2} ")` also opens a section on every `# ` line, and
slices its name with `[3:]`. Observed consequences:

- `check_k16 base` prints `sections=491`; a census of the same four scan targets in the base export under the
  documented definition returns `h1=68 h2=423 total=491`. The published payload counts 68 H1 sections that the
  documented shape excludes.
- `a2tablecell` diagnoses an H1-preamble promise as `heading=ound 42 test` (the `[3:]` slice eats `# R` of
  `# Round 42 test`), i.e. the name a correction would have to match is mangled in the diagnostic.

Suggested fix: either restrict section creation to `^## ` (and keep H1 preambles out of scope, as documented) or
amend the header/receipt and slice `# ` headings with `[2:]`.

### F5 — header claim "quoted or tabulated narrative cannot trip it" is false, and it is a false-positive surface at Y (minor)

`strip_quoted` removes only backticked and double-quoted spans. It does not skip markdown table rows or
blockquotes, so the `to-be-filled` clause fires on both:

- `a15tableopen` — a realistic `## Mistakes` section that opens with its table and one cell reading `to be filled`:
  `K16 unresolved … line=3 heading=Mistakes clause=to-be-filled … unresolved=1 closed=0`.
- `a7blockquote` — `> to be filled` as the opening stanza: `… clause=to-be-filled … unresolved=1 closed=0`.

Neither shape exists at base (`promises=1`, only the round-42 section), so the round is not reddened today; the risk
is that any graded table cell or blockquote written this round with `to be filled`/`TBD` in a section's opening
stanza turns K16 red at Y. Suggested fix: skip lines whose first non-space character is `|` or `>` in the clause
test, or drop the claim from the header. The natural companion limit is `a16tablelater`: the same table one blank
line lower is invisible (`promises=0`), so the clause is opening-stanza-only, as documented.

## Verified correct (each with the quoted stdout above)

- Base red names the exact routed defect: `file=corpus/lessons/round-42.md line=52 heading=Wave-2 falsification
  clause=schedule`, `promises=1,unresolved=1 closed=0` — exactly RD42-4, no other section in 491 is flagged.
- The intended after-state closes: `aft` (base + the three real `ScribeCorrections` blocks) → `closed=1` rc=0, and
  `ysim2` (also carrying the round-43 scorecard/log/shonen appends) → `sections=494,promises=1,fenced=0,unresolved=0
  closed=1` rc=0. The new round-43 prose does not introduce a false promise.
- A correction placed **before** the section does not close it (`a3markerbefore` → `line=5 … unresolved=1 closed=0`),
  matching the frozen "not followed by" wording; the executor's own `early` case says the same.
- Two promises in one section count once (`a4twopromises` → `promises=1`), which is the declared granularity
  ("sections whose opening stanza promises"); a single naming correction clears the section.
- Fenced promise vocabulary is ignored and reported (`a5fenced` → `promises=0,fenced=1`; `a5fencedheading` → the
  fenced `## ` heading creates no section, `fenced=1`), and a correction that sits inside a fence does not resolve
  (`a8fencedmarker` → `unresolved=1 closed=0`).
- Historical *mentions* are not promises (`a6mentions`, four files / 9 sections carrying the words in prose and
  quoted form → `promises=0`); this is what keeps the 30+ base-tree `placeholder` mentions from reddening the check.
- A correction in another file does not resolve a lesson promise (`a17crossfile` → `unresolved=1 closed=0`).
- An unbalanced backtick does not hide the clause (`a18unbalanced` → still `unresolved=1`).
- Degenerate roots fail closed (`empty`, missing root, no argument → `closed=0` rc=1).

## Named limits (shapes the limb cannot see; each is a limit, not a silent pass)

1. **Reworded promise without the clause vocabulary** — `a1reword` (`The per-claim verdicts are written here once the
   falsification wave has landed its tally.`) → `promises=0`, exit 1 only because of the `promises>0` guard. The guard
   is global, not per section: `a19rewordedstand` has a satisfied promise plus the reworded one and prints
   `rc=0 :: payload=sections=3,promises=1,fenced=0,unresolved=0 closed=1` — a standing promise, closed check.
2. **`Tbd` / lowercase `tbd`** — `a10tbdcase` → `promises=0`. The clause is `\bTBD\b`, case-sensitive; the receipt
   does not say so.
3. **Case-sensitive resolution** — a correction writing `## wave-2 falsification` (`a20lowerheading`) or a lowercase
   `correction (round 43)` marker (`a21lowermarker`) does not resolve; both print `unresolved=1 closed=0`.
4. **Heading split across two source lines** — `a22wrappedheading` does not resolve (`unresolved=1 closed=0`); the
   receipt declares "one literal line", so this is declared, but it is a landing hazard for any wrapped block.
5. **Unclosed fence earlier in a lesson file** — `a11unclosedfence`: a correction appended after an unclosed fence is
   treated as inside the fence and never resolves (`unresolved=1 closed=0`). The suite's J11 `eof-closed=3/3` guard
   covers the three records only; `corpus/lessons/*.md` is unguarded, so an unclosed fence there makes a promise
   unclosable without any diagnostic that says why.
6. **Semantic non-withdrawal** — `a12openmarker` (marker naming the heading while asserting `the … promise is still
   pending the falsify wave`) prints `closed=1`. This satisfies the frozen wording literally (a line carrying the
   marker that names the heading); it is a presence check, not a withdrawal check. Recorded so the suite's claim is
   read as "the statement exists", not "the promise was withdrawn".
7. **Symlink out of the export** — `check_k16 symtest` with `symtest/corpus/lessons/link.md → $S/outside.md` graded the
   outside file (`K16 unresolved file=corpus/lessons/link.md line=3 heading=S clause=schedule`). `git archive`
   preserves symlinks, so a committed symlink under `corpus/lessons/` would be read from outside the export. Low
   plausibility; no containment check exists.

## Residual risk

The limb is reachable to green at the intended Y: `ysim2` (base + the three real correction blocks + the round-43
scorecard/log/shonen appends) prints `closed=1` rc=0, so round closure does not depend on any of the findings above.
What remains is that `closed=1` proves less than the receipt says: a correction naming a longer sibling heading (F1),
a same-titled sibling section (F2), or a quoted draft (F3) all close it without withdrawing the promise, and the
`to-be-filled` clause can red a healthy file through a table cell or blockquote (F5). F4 makes the published
`sections=` number and the diagnostic heading name disagree with the documented shape. None of these changes the
base red or the intended after-state; they bound what the K16 line is evidence for.

## Verification gaps

- `corpus/instruments/r43-closure.sh` is not landed at review time, so the K16 line's integration (payload passthrough,
  numeric ordering, the suite's nineteen-line transcript) is unverified by this seat.
- The K16 selftest case and its mutants belong to `MutK16K17`; I did not run them and claim nothing about them.
- The true Y tree cannot be exported until the L1 lands it; `aft`/`ysim2` are byte composites of the base export plus
  the currently committed-nowhere scribe deliverables, so the exact Y heredoc copy of the limb is not graded here.
- Host observation, not this seat's scratch: `/tmp/verif-kasegi-r42` (25.4G, owner idle) is present outside my
  scratch root and was left untouched.

## Tooling and network

No installs, no upgrades, no network fetches; no pacman; nothing written to any PATH directory. Only read-only git
(`archive`, `rev-parse`, `log`) against the lane.

Scratch `$S` removed before yield; the only file written under the lane is this receipt.
