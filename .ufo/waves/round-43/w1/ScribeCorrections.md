# ScribeCorrections — round 43 receipt

Seat `ScribeCorrections` (scribe, leaf; no subagent dispatch). Task: draft the three append-only
correction blocks closing RD42-1, RD42-2, RD42-3 and RD42-4. Round 43, base
`ab98fac9dce87130bc4f66de89e30650d63943dc`, operating tip `4cb6d4a` (claims freeze; the three target
files are byte-identical to base in the regions I name — verified below). Axes: depth:verifiability,
coverage. Nothing here is committed; the L1 lands the block files.

## Deliverables (byte-exact append blocks)

| file (`.ufo/waves/round-43/w1/`) | target | anchor named | lines | bytes | sha256 | closes |
|---|---|---|---:|---:|---|---|
| `ScribeCorrections.scorecard.txt` | `SCORECARD.md` EOF | `SCORECARD.md:1634` | 1 | 945 | `27424eb13e025c8c5ad55d3ba5927d70a0286cb436efd22c9659bca10e035f07` | RD42-1 |
| `ScribeCorrections.log.txt` | `LOG.md` EOF | `LOG.md:1804` | 1 | 786 | `7e8f71992d374866f11ab2803bca7ea77a840e3017a039e1e012771b27332b41` | RD42-2 |
| `ScribeCorrections.lesson42.txt` | `corpus/lessons/round-42.md` EOF | `:11`, `:16`, `:52` | 2 | 786 | `37423d8b2943e116d1511d44ee8a0786b875032f684abcf085fc9543bb4922d6` | RD42-3, RD42-4 |

`lesson42.txt` is 2 lines because its first byte is the blank separator line the file needs (the file
ends with a single `\n`; the other two end with `\n\n`, so their blocks carry no leading blank). Its
single correction line is 782 bytes.

Each block is exactly one `Correction (round 43)` line at column 0 (J11/K14 `^Correction \(round 43\)`),
wrapped at the file's own width — the two records already carry single very long `Correction (round NN)`
paragraph lines (SCORECARD.md:1634 is one), and the lesson files' 3 existing corrections
(`round-38.md:311`, `round-39.md:98-99`) are single lines too. No heading is added to any file.

Quoted anchors (read at the tip):

```
SCORECARD.md:1634  Correction (round 42): D-r41-1's measurement is no longer pending: the r…
LOG.md:1804          (`.ufo/waves/round-42/wave1-dispatch.json`); wave 2 `kasegi-r42-falsify` 36 se…
round-42.md:11     never estimated: wave 2 dispatched 36 seats; the round total is 100. Every wave …
round-42.md:16     from the wave-2 dispatch when it lands: 36 seats, 32 attack roles.
round-42.md:52     ## Wave-2 falsification
```

## Re-derived values that the blocks state

1. Live correction ledger, using the r42 engine's own functions (`correction_lines`,
   `normalized_body`, `fence_scan`) extracted verbatim from
   `corpus/instruments/r42-closure.sh:107-2182` and executed as a module:

```
$ python3 -c '... ns=exec(r42engine.py); ns["check_j11"]("before") ...'
before  corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
   SCORECARD.md round43-lines=0   LOG.md round43-lines=0   SHONEN.md round43-lines=0
```
   Per file at the tip: `SCORECARD.md corrections=19 groups=4 dups=4`, `LOG.md corrections=7`,
   `SHONEN.md corrections=8`; duplicates are the four round-41 SCORECARD bodies at
   `[1602,1607] [1603,1608] [1604,1609] [1605,1610]` (the excused D-r41-1 state). Live = 34; the
   SCORECARD.md:1634 cell says `corrections=33`, stale by one — the RD42-1 defect, unchanged.
2. `LOG.md:1804` dead-seat pointer is unbacked:
```
$ ls .ufo/waves/round-42/wave2-results.json
ls: cannot access '.ufo/waves/round-42/wave2-results.json': No such file or directory   (exit 2)
$ ls .ufo/waves/round-42/  →  kasegi-r42-falsify.ready, wave2-dispatch.json, wave2-spec.json,
   wave2-run.err, wave2/   (no results aggregate; the .ready is a 175 B dispatch manifest)
```
3. The executed round-42 wave is wave 1: `.ufo/waves/round-42/kasegi-r42-build-results.json` →
   `seats: 64`, `results: 64`. So the round total is 64; `100` (round-42.md:11) and `32 attack roles`
   as a taken-wave tally (round-42.md:16) are not reachable.

## Acceptance rules the blocks are written against (read from the seats, not assumed)

- **K14** (`ExecK14Corrections`, IRC answer, 2026-10-28): the marker must match `^Correction \(round 43\)`
  at line start, outside a fence, in the SAME file, at a line number strictly greater than the carrier;
  must contain the literal `corrections=33` byte-exact as a whole token; must carry a supersession word
  (`supersede|superseded|supersedes|replaces|stale|no longer`); a `live=`-prefixed claim must equal the
  live value and I therefore wrote none. The limb reuses r42's `RECORDS` = SCORECARD.md, LOG.md,
  SHONEN.md — the dispatch's `SHENON.md` is a typo; confirmed SHONEN.md. Live is derived, never frozen.
- **K15** (`ExecK15WaveNarrative`, IRC answer, 2026-10-28): lines whose stripped text starts with
  `Correction (round 43)` are never collected as assertions (no self-trigger); Markdown table rows and
  fenced blocks are skipped, so `round-42-verifier-spotcheck.md:174` needs no correction; the correction
  must contain `never-true` or `not taken` (exact) plus the wave token `kasegi-r42-falsify`, and sit at a
  later line in the same file. Its expected base set is exactly the three sentences I correct.
- **K16** (read from the landed limb `.ufo/waves/round-43/w1/ExecK16Placeholder.sh`): headings are
  `^#{1,2} `; a promise is graded only in the section's opening stanza with backticked/quoted spans
  stripped; `resolved()` scans from the heading line for a line containing both `Correction (round 43)`
  and the heading text after `## ` (`Wave-2 falsification`), outside a fence. My line contains both.

## Verification actually run (mine, not the round-43 suite — the suite is not landed)

Blocks were applied byte-exactly to scratch copies of the three files at the tip and graded with the
landed/real limbs where they exist.

Append-only proof (R9) — the original prefix of each file is byte-identical after the append:

```
$ head -c $(wc -c < $LANE/$f) $S/apply/$f | sha256sum   vs   sha256sum $LANE/$f
SCORECARD.md                       orig=d46a8c3645e5 prefix=d46a8c3645e5 PREFIX-IDENTICAL
LOG.md                             orig=b4a0ac0e3cad prefix=b4a0ac0e3cad PREFIX-IDENTICAL
corpus/lessons/round-42.md         orig=6ed6cefae3df prefix=6ed6cefae3df PREFIX-IDENTICAL
new line counts: SCORECARD.md 1661, LOG.md 1807, corpus/lessons/round-42.md 151
```

J11 (the check K14's ledger semantics come from), real r42 engine, before vs after all three appends
(with every lesson file present):

```
before      corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
after_full  corrections=36,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0 closed=1
```
So the two record appends raise the ledger 34 → 36 and leave `unexcused=0`, the dedup marker intact and
all three records fence-closed at EOF. With the sibling `ScribeScorecardRound43` SCORECARD correction
line the Y value is 37, which is what my scorecard line states conditionally ("37 once this round's two
SCORECARD lines and one LOG line land"); it deliberately contains no `corrections=<n>` or `groups=<n>`
claim besides the superseded `corrections=33`.

Graded-token inventory of the three blocks — the ONLY graded literal present is the superseded one:

```
$ grep -o 'corrections=[0-9]*|groups=[0-9]*|payload=|live=|mutant=|quarantined' the three blocks
ScribeCorrections.scorecard.txt:corrections=33
```
(Same grep over all three: no `payload=`, no `live=`, no `groups=`, no `mutant=`, no `quarantined`; and
`grep -n 'closed=|selftest cases='` over the three → no match, so nothing a transcript check could bind.)

K14 rule simulation (implemented to the acceptance rule above), before vs after, full tree:

```
before      live=34 groups=4 stale=1 superseded=0 closed=0
   ('SCORECARD.md', 1634, 'corrections', 33, 'UNSUPERSEDED')
after_full  live=36 groups=4 stale=0 superseded=2 closed=1
   ('SCORECARD.md', 1634, 'corrections', 33, 'named-later')      # + the block's own line self-exempt
```

K15 targets — each of the three unbacked sentences now has a later `Correction (round 43)` line in the
same file carrying the wave token and the acceptance word:

```
LOG.md:1804                              superseding_correction_lines=[1807]  RESOLVED
corpus/lessons/round-42.md:11            superseding_correction_lines=[151]   RESOLVED
corpus/lessons/round-42.md:16            superseding_correction_lines=[151]   RESOLVED
```

`ExecK15WaveNarrative` then ran its landed limb over the base export with these two block files appended
and reported its own output to me (the sha256s it names — `7e8f7199…`, `37423d8b…` — are the two files
above, byte for byte):

```
K15 payload=sentences=5,unbacked=0,superseded=3,mismatch=0 closed=1
superseded-by=1808 (LOG) and =151 twice (round-42.md:11 and :16)     [K15_VERBOSE=1]
```
Its LOG marker lands at 1808 in its appended tree against 1807 in mine (one line of drift inside its
tree); the anchor itself is identical at base `ab98fac9` and tip `4cb6d4a`
(`git show <ref>:LOG.md | sed -n 1804p` both print the same bullet). Verdict: accepted as-is, no
follow-up corrections needed for the round-23/25 falsify sentences (backed by 36 and 32 seat receipts).

K16 — the real landed limb, before vs after, with the full lessons tree:

```
before      K16 unresolved file=corpus/lessons/round-42.md line=52 heading=Wave-2 falsification clause=schedule
            payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
after_full  payload=sections=491,promises=1,fenced=0,unresolved=0 closed=1
```
The lane carries exactly one promising `## ` section in the whole set K16 scans (491 sections,
promises=1), and the block resolves it. A section-set diff on `corpus/lessons/round-42.md` shows the
append introduces no new `## ` section and adds no promise clause to `## Gate`'s opening stanza:

```
round-42.md flagged sections BEFORE: 1   (52, 'Wave-2 falsification', 54, 'Appended when the round-42 falsify wave reports…')
round-42.md flagged sections AFTER : 1   (same)
new sections introduced by append: []    resolved: []
```

## Out-of-scope items received (recorded, not acted on)

- IRC from `W1ScribeLessonGate`: `corpus/SOURCES.md:189` (S242) has an unescaped `O_NONBLOCK | O_WRONLY`
  pipe (NF=14 under `awk -F'|'`, census E01 `fields=12`). I do not own `corpus/SOURCES.md`, it is not in
  my write scope, and it is a Souji/registry-seat item; forwarded only by recording it here.
- `corpus/lessons/round-42-verifier-spotcheck.md:174` quotes the LOG.md:1804 sentence inside a table
  row. `ExecK15WaveNarrative` confirmed table rows are skipped as quoted evidence, so no correction is
  needed in that file (and it is outside my three named deliverables).
- Dispatch typo `SHENON.md` for `SHONEN.md` (K14 prompt). My block uses the real file; K14 confirmed.
- `ExecK15WaveNarrative`'s integration note to the L1: the drafted round-43 LOG entry asserts
  `73 seats dispatched`, so Y must carry `.ufo/waves/round-43/kasegi-r43-hyaku-results.json` with
  seats=73 and 73 results, else K15 reds there by design.
- `ExecK14Corrections` ordering note: any record that pastes a run transcript unbounded is graded as a
  live claim, so the L1 should land these blocks before the graded Y run. My blocks contain no
  `closed=`/`selftest cases=` tokens, so this cannot bite them.

## Known limits

- I did not run `corpus/instruments/r43-closure.sh` — it is not landed; K1-K19 grade at Y, not here.
  The K14 limb was not on disk when I finished (`ls w1/ | grep -E 'K14'` → none), so the K14 result above
  is a rule simulation built to `ExecK14Corrections`' confirmed acceptance rule. The K15 and K16 results
  ARE the landed limbs' own output (K15 reported to me by its executor, K16 run by me).
- The live count 34 is a measurement at `ab98fac9` / tip `4cb6d4a`; at Y it is 36 (my two record appends)
  or 37 (+ the sibling SCORECARD line). The block states the derivation rather than a frozen number.
- `37` in the scorecard block assumes `ScribeScorecardRound43` lands its own SCORECARD correction line.
  If it does not, the ledger is 36 and the block's word "once … land" is already the hedge; the L1
  should prefer 36 in that case only by asking that seat, never by editing this line.

## Tooling

None installed or upgraded (no `uv tool install`, no npm, no binary fetch; `pacman` untouched per the
host-wide pause). Disk guard checked before the verification pass:
`/fast/scratch/hyaku` 26% used, 598.9G free, `/tmp` 17% — no heavy pass needed.
Scratch `S=/fast/scratch/hyaku/kasegi-r43/ScribeCorrections/` was created with `mkdir -p`, held every
copy and work tree (`before/`, `apply/`, `after_full/`, `r42engine.py`, `sim.py`), and is removed after
this receipt is in place; no scratch path survives me.
