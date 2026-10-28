# R44Critic6 — falsify the proposed SHONEN blank-line preservation

Seat: `R44Critic6` (critic, leaf). Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Round 44, frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; measured at HEAD
`6631401` (only `.ufo/waves/round-44/` controls added; `git diff --numstat 5ab3a60 HEAD -- SHONEN.md`
empty). Read-only: no production/shared file, no git/jj/index mutation, no commit. Scratch
`/fast/scratch/hyaku/kasegi-r44/R44Critic6/` (deleted on exit; see §8).

Assigned item: *try to falsify proposed SHONEN blank-line preservation; determine if this should be
handled or left historical.* The proposal is `corpus/lessons/round-43-verifier-spotcheck.md:106`
(item 6): "Restore the blank line when the file is next appended."

## 1. Verdict

**The observation is byte-exact; the prescription is falsified.** Item 6's *fact* reproduces to the
byte, but its *remedy* is ambiguous between an in-place junction insertion (forbidden by §6's own
landing rule, `:99`) and an EOF append (append-only but position-blind: it makes the numstat `8 0`
while the block still starts at 285, not the declared 286). Either branch restores a byte no lane
convention requires. Disposition: **handle it — as the protocol's appended named correction entry
(`PROTOCOL.md:366-367`), not as a byte restoration.** "Left historical" (silent drop) is not
available: the same protocol line keeps it on the routed-defect queue until it lands, and C1's kill
rule (`claims.json:15`) fails the claim on any unresolved frozen defect. A live, uncommitted EOF
append already sits in the worktree (§9) — the counter must not read that byte-count as a repair.

## 2. The claim reproduces (counterexample search failed on the facts)

```
$ git show ab98fac9:SHONEN.md | wc -c            → 30157
$ git show ab98fac9:SHONEN.md | tail -c 2 | xxd -p → 0a0a
$ git show dbd2e106:SHONEN.md | wc -c            → 34691
$ git show dbd2e106:SHONEN.md | tail -c 2 | xxd -p → 0a
$ git show dbd2e106:SHONEN.md | head -c 30158 | tail -c 4 | xxd -p → 2e0a2d20   # ".\n- "
$ git diff --numstat ab98fac9 dbd2e106 -- SHONEN.md → 8	1	SHONEN.md
$ git show ab98fac9:SHONEN.md | wc -l → 285 ;  git show dbd2e106:SHONEN.md | wc -l → 292
```

So base byte **30157** (the second `\n`) is absent at tip and the payload's first byte `-` sits in its
place: exactly one base byte, exactly the final empty line. Line arithmetic: 284 content lines + 1
empty = 285; 284 + 8 payload lines = 292 (the `8 1` diff). The landed block is 8 lines
(`git show dbd2e106:SHONEN.md | sed -n '285,292p' | wc -l` → 8).

**Verifiability nit (not a falsification):** the spot-check prints `9 +-` with no counting command.
The cited command alone prints a 17-line diff; 11 lines begin `+`/`-`; **9** is the count only after
excluding `---`/`+++` headers:

```
$ git diff ab98fac9 dbd2e106 -- SHONEN.md | wc -l → 17
$ git diff ab98fac9 dbd2e106 -- SHONEN.md | grep -cE '^[+-]' → 11
$ git diff ab98fac9 dbd2e106 -- SHONEN.md | grep -E '^[+-]' | grep -vcE '^(---|\+\+\+) ' → 9
```

`PROTOCOL.md:352` ("a numeric claim carries its counting command") binds this figure too; the
round-44 counter should carry the third command, not the bare number.

**Attribution:** the final shape is `0a24364d`'s (`git diff --numstat ab98fac9 0a24364d -- SHONEN.md`
→ `8 1`). The byte transition first appears at `9e6800e` (round-43 head J), whose SHONEN was a
`4 280` truncated landing that also ended single-`\n`; `0a24364d` reproduced it. The spot-check's
causal wording is imprecise but its hash pair and byte claim hold.

## 3. The base byte was a round-42 landing artifact, not a required byte

```
$ git diff --numstat 7ebe3cc 857cac4 -- SHONEN.md → 57	0	SHONEN.md   # round-42 landing, append-only
$ git show 7ebe3cc:SHONEN.md | tail -c 2 | xxd -p → 2e0a                # round-41 base ends single
$ git show 857cac4:SHONEN.md | tail -c 2 | xxd -p → 0a0a                # round-42 landing ends blank
```

- SHONEN.md history: **23 revisions, 2 end `0a0a`** (both round-42: `857cac4`, `49259a0`), 21 end
  `0a`.
- Every append-only record file ends single-`\n` at HEAD: `LOG.md` `342e0a`, `SCORECARD.md` `652e0a`,
  `corpus/QUALITY.md` `207c0a`, `corpus/README.md` `742e0a`, `corpus/SOURCES.md` `702e0a`,
  `SKILL.md` `73290a`, `PROVINCE.md` `34290a` (`git show HEAD:$f | tail -c 2 | xxd -p`).
- Of **4876** tracked `*.md` at HEAD, **13** end `0a0a` and **all 13 are `.ufo/waves/*` deliverable
  payload fragments**; zero record files. A census loop: `for f in $(git ls-files '*.md'); do … done`
  → `md_total=4876 double_newline=13`.
- **No instrument observes trailing newlines/EOF blanks:** `grep -rnE "tail -c|final newline|trailing
  (newline|blank)|last byte|0a0a" corpus/instruments/*.sh corpus/instruments/*.py` → 0 hits.
  `check_j11`'s EOF predicate is `fence_open_at_eof` (`r42-closure.sh:340`), not blank lines, and its
  correction reader is line-anchored (`CORRECTION_RX = ^Correction \(round (\d+)\)`,
  `r42-closure.sh:476,485`), not blank-line-delimited.

Counterexample to "restore it": restoring the byte at EOF would make `SHONEN.md` the **only record
file in 4876** ending with a blank line — i.e. it would *create* the convention divergence, not
repair one. The base's `\n\n` is the round-42 landing's 57th added line (`57 0`, EOF `0a0a`) and
nothing in the lane requires it.

## 4. The prescription is unsatisfiable append-only (the falsification)

- `round-43-verifier-spotcheck.md:99`: "Each lands as an appended correction or a new lesson row,
  never as an in-place rewrite". Item 6 (`:106`): "Restore the blank line when the file is next
  appended."
- The lost byte sits **between** the round-42 item and the round-43 block (tip lines 284/285). To put
  it back you must insert a line at tip **285**, shifting the round-43 block from 285-292 to 286-293 —
  a mid-file insertion, i.e. the in-place edit `:99` forbids. It also breaks committed line
  citations: `.ufo/waves/round-44/wave1/R44Review18.md:7` cites `SHONEN.md:286–292` and `:288`;
  `.ufo/waves/round-44/wave1/R44Scout6.md:53` cites `:287`.
- An **EOF append cannot restore it**: appending a blank line adds a new byte after the block; the
  numstat stays `8 1`, so the base byte is still absent. There is no append-only operation that puts
  a byte back *before* already-landed content.
- `PROTOCOL.md:366-367`: "A falsified claim in an append-only file gets a named correction entry in
  the lane's next round — appended, never rewritten; it stays on the routed-defect queue until it
  lands." That is the only append-only closure instrument the lane has for this file.

The round-43 scribe's own declared landing contract is the corroborating evidence that a deviation
really occurred: `.ufo/waves/round-43/w1/ScribeShonenLines.md:18` — "`SHONEN.md` (285 lines, ends
`\n\n`; the landable block begins on line 286 after the existing blank line)", rehearsal `293` lines.
The landed file has 292 lines and the block at 285.

## 5. Structural impact is nil — no second remedy is warranted

- `sed -n '270,292p' SHONEN.md > j.md; cmark j.md` renders tip line 285 as its own `<li>`; the
  round-42 item closes `</li>` first. The missing separator does not merge the block, and no gate
  reads it (§3).
- Bullet census (40 bullets): 22 are preceded directly by an evidence line — the file's dominant
  in-block style. At the *block* level, 9 of 10 round-block starts are blank-preceded; round 43's is
  the only evidence-preceded one. Real but cosmetic; cmark and K14 are blind to it.

## 6. Do-nothing discriminates the append-only remedy

```
$ git grep -c 'Correction (round 44)' HEAD -- corpus SCORECARD.md SHONEN.md LOG.md
(no stdout) ; exit=1
```

A counter that requires a `Correction (round 44)` entry naming the SHONEN final-byte loss is red at
the frozen base and can only go green after the appended entry lands. The frozen do-nothing control
(`controls/do-nothing.txt`) therefore cannot reach the item-6 after-state, as C1 requires.

## 7. Smallest safe correction

1. **Land an appended `Correction (round 44)` entry** (in `SHONEN.md`, mirrored in the round-44
   lesson if that is the lane's record) that names the measurement, not just the marker:
   base `ab98fac9` byte `30157` = the final `\n`; `git diff --numstat ab98fac9 dbd2e106 --
   SHONEN.md` → `8 1`; landed 292 lines vs the declared 293 / block at 285 vs declared 286; provenance
   `857cac4` `57 0` + EOF `0a0a`; disposition: the base's terminal empty line was the round-42
   landing's added blank, not a lane convention (0 of 4876 record files end `0a0a` at HEAD), so no
   in-place insertion is made and the file keeps the single-final-newline convention.
2. **If round 44 appends any SHONEN block, begin it with a blank separator** (append `\n` then the
   block) so no new block boundary joins the one exception at 9/10.
3. **Counter predicate must be measurement-bearing and position-aware.** A bare
   `grep -c 'Correction (round 44)'` is satisfiable by a blanket assertion (the post-hoc-editability
   risk `R44Review9.md` raises), and a numstat-only predicate (`git diff --numstat ab98fac9 --
   SHONEN.md | awk '$2>0'`) is satisfied by an EOF blank line while the block still starts at 285
   (§9). Require the entry line to carry `30157` and `8 1`, and require the junction fact — block
   first line at 286 with a blank at 285, or an explicit statement that the position was not
   restored. The counter's docstring must state that item 6 is closed by supersession, not by
   byte restoration, so the narrowing is explicit rather than hidden.
4. **Do not insert a blank line at tip 285**: forbidden by `:99` and it shifts line numbers cited by
   committed round-44 reports (`R44Review18.md:7`, `R44Scout6.md:53`).

Impacted axes: **depth:verifiability** (item-6 predicate and the `9 +-` counting command);
**coverage** — no effect (no frontier, registry, or knowledge surface is touched by this item).

## 8. Limitations and disclosures

- Read-only seat: no lane file was modified; all commands were `git show`/`git diff`/`git grep`/
  `git log` and shell text processing. `cmark` (system binary) was used only to test render
  semantics.
- The landed 8 lines are **not byte-identical** to the committed payload: `diff -u
  .ufo/waves/round-43/w1/ScribeShonenLines.append.md <tip 285-292>` shows one edited evidence line,
  `+119` bytes — the CVE-2023-38545 → CVE-2025-9086 supersession that the landed line itself records.
  So payload-hash predicates over `base+payload` are invalid; line-count arithmetic (8 lines) holds.
- `corpus/instruments/r44-routed-defects.py` does not exist at the frozen base
  (`ls` → No such file), so the C1 counter's item-6 predicate could not be read; §7.3 is a
  requirement on the counter the round must still write, not a reading of it.
- Round-44's SHONEN landing plan is not in the dispatch (the five SHONEN-touching seats are
  read-only reviews); §7.2 is conditional on the L1 landing a block.
- No LSP/semantic device; greps are literal evidence. No scratch failure: scratch created under
  `/fast/scratch/hyaku/kasegi-r44/R44Critic6/` (`$HYAKU_SCRATCH` was unset in this shell) and
  removed on exit. No tool installed.

## 9. Live worktree state at measurement time (uncommitted — not evidence of a landing)

Observed 2026-10-28 16:12 local, after my read-only pass began; another seat is editing `SHONEN.md`
in the worktree (I did not write it):

```
$ git diff -- SHONEN.md | tail -3          → hunk @@ -290,3 +290,4 @@ … "+$"  (one added empty line at EOF)
$ git hash-object SHONEN.md                → 543fad700426c38ad99995cf24c40af36cb472b5
$ wc -l SHONEN.md                          → 293
$ tail -c 2 SHONEN.md | xxd -p             → 0a0a
$ git diff --numstat ab98fac9 -- SHONEN.md → 8	0	SHONEN.md
$ grep -n '^- \[~\] SKILL.md contains real decision' SHONEN.md → 9, 88, 162, 285  (block still at 285)
$ sed -n '284p' SHONEN.md                  → the round-42 evidence continuation line (junction still merged)
```

This is branch (ii) of the prescription: an EOF blank line. It makes the base-vs-worktree numstat
`8 0` (git matches the base's empty line at the new EOF position), so a "zero deletions" counter
passes — but the round-43 block still begins at **285**, not the scribe-declared **286**, the
junction is still the file's only unseparated block boundary (9/10), and the record file now ends
`0a0a`, which no other record file in 4876 tracked `*.md` does. It also does **not** put base byte
30157 back at its position: the file is 293 lines with an empty 293rd, not 285 lines with the base's
blank at 285 and the block at 286. If this lands, the correction entry (§7.1) must say so, and the
counter must not treat the byte count as the repair.
