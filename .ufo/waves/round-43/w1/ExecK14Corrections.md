# ExecK14Corrections — K14 limb (RD42-1 correction-literal ledger)

Round 43, kasegi-shokunin. Leaf executor. Base `ab98fac9dce87130bc4f66de89e30650d63943dc`;
lane head at run time `4cb6d4ae768481e1a14afbedc2d865a060ebacfd`. Frozen claims read
first from `.ufo/waves/round-43/claims.json` (never edited). Axes: depth:verifiability
(4, held), coverage.

## Deliverables

| Path (relative to lane root) | Lines | sha256 |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecK14Corrections.sh` | 202 | `4a4945b085d7f2a6e81dedbd195fe62ace214d4b0d000e2049acd3864cc48d4c` |
| `.ufo/waves/round-43/w1/ExecK14Corrections.transcript.txt` | 208 | `26810447af5ef6b3c6953dbbb273a1fdf0fad3834d4e93887d3e598a896c2405` |

The limb is a sourceable bash file: `. ExecK14Corrections.sh; check_k14 <export>`. It
prints exactly one stdout line

```
K14 payload=literals=<n>,stale=<k>,superseded=<s>,live=corrections=<c>,groups=<g> closed=0|1
```

and returns 0 when `closed=1`, 1 when `closed=0`. Named diagnostics (each stale and each
superseded occurrence) go to **stderr only**; `bash ExecK14Corrections.sh <export>` is
the same function with `$1` for transcripts. The suite should call `check_k14` and keep
stdout: one line, nothing else.

Payload fields, for the r43 selftest grader: `literals` = counted occurrences (after the
evidence exclusions); `stale` = occurrences whose value differs from the re-derived value and
that no same-file later `Correction (round 43)` line names; `superseded` = occurrences whose
value differs but are named (or are the naming line's own quotation); `live=corrections=<c>`
and `groups=<g>` = check_j11's counts on that export. A mutant that re-introduces a stale
literal must make `stale>=1` and `closed=0`; the positive at Y must print `stale=0 closed=1`.

## How the live ledger is derived (reuse, not a fork)

The limb reads `<export>/corpus/instruments/r42-closure.sh`, extracts the engine between
`exec python3 - <<'R42_ENGINE_PY'` and the closing `R42_ENGINE_PY`, executes it with
`__name__ = "r42_k14_engine"` (so its `if __name__ == "__main__"` guard does not fire) and
calls **`check_j11`** on the same export. Its payload supplies `corrections` and `groups`;
its `RECORDS` (`SCORECARD.md`, `LOG.md`, `SHONEN.md` — the dispatch's "SHENON" is a typo),
`fence_scan`, `correction_lines`, `CORRECTION_RX` and `read_text` are used directly. No
counting rule is re-implemented. Engine absent/unreadable, any of the three records absent,
or `corrections=0` ⇒ `closed=0` (fails closed, never vacuously green).

Measured (`transcript.txt` §1), at both base and head:

```
engine=r42-closure.sh RECORDS=SCORECARD.md,LOG.md,SHONEN.md ROUND=42
check_j11=('corrections=34,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appended=1,eof-closed=3/3,fenced=0', True)
```

This is the same `corrections=34` the round-43 do-nothing control records for J11, so the
re-derivation is check_j11's own value.

## Grading rules (as implemented, byte-level)

1. **Literal read (R41).** `(?<![0-9A-Za-z_])(corrections|groups)=([0-9]+)(?![0-9A-Za-z_])`
   over every line of the three records. `corrections=330` is the value 330, `xcorrections=33`
   is nothing, two literals on one line are two occurrences.
2. **Equality.** Each occurrence must equal the value re-derived from the SAME export
   (corrections against `corrections`, groups against `groups`).
3. **Quoted defect evidence (R41).** Three line modes. A fenced line carrying `payload=` is
   a quoted run transcript: nothing on it is graded. A line carrying `mutant=` or
   `quarantined` is a quotation of defect evidence: its `live=` claims are still graded, its
   other literals are not. Every other line is a record line and every literal on it is
   graded. There is no word list: ordinary prose (`the 23/73 attack share`) can never license
   a stale literal. A bare stale literal inside a fence is still a carried literal and is
   graded.
4. **Supersession.** A stale occurrence at line *n* of file *F* is excused iff a line
   matching `^Correction \(round 43\)`, outside a fence, in **the same file**, at a line
   *> n*, names the literal verbatim as a whole token.
5. **Self-naming.** A `Correction (round 43)` line is itself a carrier of the literal it
   names; those occurrences are quotations and are exempt (a marker cannot be excused by a
   later copy of itself). The one exception is a literal inside a `live=...` token — the
   payload segment `live=corrections=<c>,groups=<g>`, both keys included — which is a live
   claim on any line and is always graded. Exactly the contiguous form `live=<key>=<n>` is a
   live claim; `live =<key>=<n>` with a space and narrative phrasing ("the live
   corrections=<n>") are not graded, so a correction line may state a stale value in prose
   without turning itself red. That boundary is deliberate: the naming remedy must never
   depend on prose, and RevK14's R1 records it as such.
6. `closed=1` iff the ledger was derived over all three records and `stale=0`.

Why rule 3 is not "any line with `payload=`": the frozen base expectation is
`SCORECARD.md:1634` carrying `corrections=33` against a live 34 with `stale=1`. That line
is a `Correction (round 42)` prose claim about what the r42 suite prints — a *result*, not
defect evidence — and it also carries `payload=`. Excluding every `payload=` line would
make K14 green at base and violate the C1 kill rule ("a check that cannot see its own
defect is not repaired"). Quotation is therefore scoped by position (a fenced transcript)
and by explicit mutant/quarantine marking, never by a vocabulary of ordinary words.

## Post-review revision (RevK14 §4, two escapes, both closed)

RevK14 filed two escapes against the first landed revision (`sha256 9fb97b4c…`). Both were
real; both are reproduced in `transcript.txt` §8 and §9 and are rejected by this revision.

- **F1 — word-list escape.** `DEFECT_TOKENS` contained `attack`, so an unfenced payload line
  that merely said "the 23/73 attack share" was dropped whole and its stale live value was
  never graded. Fix: the word list is gone; an unfenced payload line is a record line and is
  graded in full. Measured on RevK14's fixture (33 distinct correction lines, live 33):
  ```
  K14 stale=SCORECARD.md:34 corrections=31 live=33
  K14 payload=literals=2,stale=1,superseded=0,live=corrections=33,groups=0 closed=0
  exit=1
  ```
- **F2 — skip ran before the literal loop.** A `live=` claim on a `mutant=` (evidence) line
  was never graded, contradicting rule 5. Fix: an unfenced `mutant=`/`quarantined` line is
  mode `live` — only its `live=` occurrences are counted and graded. Measured on RevK14's
  fixture (3 correction lines, live 3):
  ```
  K14 stale=SCORECARD.md:4 corrections=99 live=3
  K14 payload=literals=1,stale=1,superseded=0,live=corrections=3,groups=0 closed=0
  exit=1
  ```

One behaviour deliberately changed with the fix: an **unfenced** prose line that quotes a
defect payload (`… payload=corrections=99 … closed=0 is the rejected mutant output`) is now
graded as a record claim, not exempted by the word "rejected". A committed quotation of a run
belongs in a fenced block, which stays exempt. Unchanged by the revision: base red
(`literals=2,stale=1,live=34`), head red, the green scratch tree, the 37-live landing shape,
the real scribe landing, all fenced/marker/near-token/two-literal/cross-file/engine-absent
controls (full output in the transcript).

## Evidence (full commands and output in `ExecK14Corrections.transcript.txt`)

Base — red, stale literal named on stderr, stdout one line:

```
$ bash ExecK14Corrections.sh .../base
K14 stale=SCORECARD.md:1634 corrections=33 live=34
K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0
exit=1
$ sed -n 1634p .../base/SCORECARD.md | cut -c1-200
Correction (round 42): D-r41-1's measurement is no longer pending: the r42 suite at Y prints `J11 payload=corrections=33,groups=4,dups=4,excused=4,unexcused=0,marker=1,marker-substantive=1,marker-appe
```

Head `4cb6d4ae` — red on the same literal (round 43 has not superseded it yet):
`K14 payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0`, exit 1.

Sourced from `/` — same red line, proving `check_k14` is a function and not a path-dependent script.

Green (scratch copy of head + one appended line naming the literal): `closed=1`, exit 0,
`literals=3,stale=0,superseded=2,live=corrections=35`. Green at the expected landing shape
(2 SCORECARD + 1 LOG round-43 correction lines): `closed=1`, exit 0,
`literals=3,stale=0,superseded=2,live=corrections=37,groups=4`.

Mutants, each rejected (`closed=0`, exit 1; full output in the transcript):

| mutant | line appended (or change) | result |
|---|---|---|
| bare stale | `The r42 suite printed corrections=99 at its first Y.` | `stale=2` (1634 + 99) |
| near-token | `corrections=330` | read as 330, `stale=2` |
| mutant-quoted | line carrying `mutant=` and `corrections=99` | only 1634 graded: `literals=2,stale=1` |
| two literals, one line | `corrections=33 groups=99` | both read: 33 stale, `groups=99` stale, `literals=4,stale=3` |
| cross-file marker | LOG.md carries the `Correction (round 43)` naming `corrections=33` | SCORECARD 1634 still `stale=1` |
| bare literal in fence | fenced `corrections=99` | graded, `stale=2` |
| `live=` under supersession | `Correction (round 43): ... live=corrections=99` | self-naming exempt, the `live=` claim still `stale=1` |
| wrong round marker | `Correction (round 42): the corrections=33 literal ...` | not a marker: `stale=2` |
| fenced payload transcript | fenced `K14 payload=...,live=corrections=99,...` | skipped whole, `literals=2,stale=1` |
| unfenced payload line | `J11 payload=corrections=99,groups=4,dups=0 closed=1` | graded as a record claim: `stale=2` |
| F1 attack-share line | `K14 payload=...,live=corrections=31,groups=0 ... 23/73 attack share` | `literals=2,stale=1` |
| F2 live claim on mutant line | `mutant=`corrections=1` …; live=corrections=99` | `literals=1,stale=1` |
| marker above the carrier | `Correction (round 43)` inserted at SCORECARD.md:4 | carrier at 1635 still `stale=1` |
| engine absent | `rm <export>/corpus/instruments/r42-closure.sh` | `error=engine-unreadable`, `closed=0` |

**Real landing text (`transcript.txt` §11).** The three correction blocks the scribe seat
already wrote into this wave dir were appended to a fresh head export exactly as they would
land (SCORECARD.md, LOG.md, and `corpus/lessons/round-42.md`, which is not one of the three
graded records):

```
K14 superseded=SCORECARD.md:1634 corrections=33 live=36
K14 superseded=SCORECARD.md:1661 corrections=33 live=36
K14 payload=literals=3,stale=0,superseded=2,live=corrections=36,groups=4 closed=1
exit=0
```

Digests of those blocks at capture: `ScribeCorrections.scorecard.txt`
`27424eb13e025c8c5ad55d3ba5927d70a0286cb436efd22c9659bca10e035f07`,
`ScribeCorrections.log.txt`
`7e8f71992d374866f11ab2803bca7ea77a840e3017a039e1e012771b27332b41`,
`ScribeCorrections.lesson42.txt`
`37423d8b2943e116d1511d44ee8a0786b875032f684abcf085fc9543bb4922d6`. Those blocks carry
exactly one `corrections=`/`groups=` token in total (`corrections=33`, on the SCORECARD
correction line) and it declares itself superseded, so K14 is green at the real landing shape
without any further edit. If the scribe revises the blocks, re-run §11 before landing.

Stdout contract: `bash ExecK14Corrections.sh .../fx-y37 2>/dev/null | wc -l` ⇒ `1`.

## Landing guidance for the round-43 close (measured, not assumed)

- The supersession line **must be in `SCORECARD.md`** (the file carrying line 1634) and at a
  **higher line number**; a LOG.md or SHONEN.md marker does not excuse it (rule 4).
- Live total = 34 + (number of `Correction (round <n>)` lines appended to the three records
  outside fences). Nothing may hardcode 34 or 37: the limb derives both sides from the export
  it is handed.
- K14 does **not** arbitrate how many correction lines the round lands; it requires every
  literal to agree with the count the export itself derives. Both sets were measured green:
  the two scribe blocks that touch graded records (SCORECARD + LOG) ⇒ `live=corrections=36,
  groups=4 closed=1` (`transcript.txt` §11), and the 2 SCORECARD + 1 LOG shape ⇒
  `live=corrections=37,groups=4 closed=1` (§6). The L1 must land one set and print that
  number in the round's prose; the same export minus `ScribeScorecardRound43.append.md`
  derives 36, with it 37, and either is internally consistent.
- Any `corrections=<n>` / `groups=<n>` literal written this round must equal the post-append
  value, or be named by a later round-43 correction in the same file. Prose ("the live ledger
  is 37 corrections over 4 distinct bodies") avoids the token entirely and is the safe form.
- Order: land all correction lines before the graded Y run if a record pastes the run
  transcript unfenced. A fenced transcript block is exempt (rule 3); an unfenced one is
  graded as a record claim.
- A `live=` claim is always graded; quote stale values bare or backticked, never as `live=`.

## Blockers, risks, deviations

- No blocker. Nothing outside the two deliverables and this receipt was written; the fleet
  root and `shokuknow` were not touched; no git mutation was run (only `rev-parse`,
  `cat-file -e`, `archive`).
- The limb fails closed if `r42-closure.sh`'s heredoc delimiter changes or the engine is
  otherwise unreadable (`closed=0`), so a future refactor of the r42 instrument cannot turn
  K14 green.
- Rule 5 deliberately exempts non-`live=` literals on a round-43 correction line: the round's
  correction record is the supersession instrument, and requiring a keyword would make the
  remedy depend on wording the L1 was not given. The cost is that a round-43 correction line
  could quote a stale value as narrative; K18/K19 grade that line's own narrative, and
  `live=` claims stay graded here.
- An unfenced quotation of a defect payload is graded as a record claim (post-review change);
  a seat quoting history must fence the transcript. A fenced bare token without `payload=`
  is still a carried literal and is graded.
- Tooling: nothing installed or upgraded; no pacman. `scripts/hyaku/disk-guard.sh status`
  was read before the pass (`/fast/scratch/hyaku` 25% used, 606.9G free).
- Scratch `/fast/scratch/hyaku/kasegi-r43/ExecK14Corrections` is removed after the copy of
  both deliverables into this wave dir; the exported trees, fixtures and driver do not
  survive.
