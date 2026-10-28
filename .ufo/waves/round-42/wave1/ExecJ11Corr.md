# ExecJ11Corr — round 42, wave 1 (seat receipt)

- Seat: `ExecJ11Corr` (executor, leaf — no subagent dispatch; no labrat probe was needed).
- Lane repo: `/home/vgpnk/Projects/shokunin/kasegi-shokunin` (base `5053a7f46de35784cff4b56756906e9014a38276`).
- Item: family **F-CORR** — the J11 limb of the round-42 C1 closure suite (`corpus/instruments/r42-closure.sh`),
  closing **D-r41-1** (the verbatim-duplicated `Correction (round 41)` block in `SCORECARD.md`).
- Deliverables (written beside this receipt, in `.ufo/waves/round-42/wave1/`):
  - `ExecJ11Corr.sh` — the sourceable limb. **606 lines**, sha256 `5474fcc0254d5e7b8745d0db7a747102d84c153150340291aa522b225ff2ad9b`.
  - `ExecJ11Corr.transcript.txt` — the teed transcript. **79 lines**, sha256 `230e330a553b9ad1867d918bba26c2c4c864c42ed9b1fa7cbd0066119c062af2`.
  - this receipt.
- The lane's `corpus/instruments/r42-closure.sh` does **not** exist yet (the L1 lands it); this seat therefore
  delivers the limb as a **sourceable file**, not as an edit of a suite that does not yet exist.

## What the limb does (the contract the L1 lands)

`check_j11 TREE REF` reads only `SCORECARD.md`, `LOG.md`, `SHONEN.md` under `TREE`, prints one payload
line `k=v,...` and returns 0 (CLOSED) / 1 (RED). `REF` is accepted and ignored, so the suite's
`run_check` (`"check_${id,,}" "$@"`) calls it unchanged.

The limb is CLOSED only when all of these hold:

| Field | Requirement |
|---|---|
| `records=3` | all three records exist under the tree |
| `corrections>0` | the records still carry live corrections (an emptied record is not a pass) |
| `eof-closed=3/3` | every record's CommonMark fence is CLOSED at EOF (an open fence would hide corrections) |
| `marker=1` | `SCORECARD.md` carries an outside-fence, column-0 `Correction-dedup (round 42)` marker |
| `marker-substantive=1` | the marker carries ≥ 40 characters after its prefix |
| `marker-appended=1` | the marker's line number is greater than every live correction line of a round before 42 **in its own record** (a marker at the top of the file is not an appended erratum) |
| `unexcused=0` | every verbatim-duplicated correction body is named by the marker |

**The excuse rule (the heart of the check).** A duplicated group is `(record file, normalized body)`.
The marker excuses a group when it (a) lives in that record file or names that file, (b) names the
group's round, and (c) names **every** occurrence line of the group — the line range *exactly*, not an
approximation. Line numbers are read from the marker text as **standalone tokens of ≥ 3 digits** (a
number inside a longer token — a commit hash, a sha256 — is not a line reference), and an `A-B` pair
expands to every line between `A` and `B`. So the mandated marker
`... at SCORECARD.md lines 1602-1605 and 1607-1610 ...` names all eight lines of the duplicated block
and excuses all four groups; a marker naming only `1607-1610`, only `1602-1603`, or a line that is not
an occurrence line, excuses nothing.

**Why the duplication is excused rather than forbidden.** The round-41 verifier routed D-r41-1 as
"note the duplication in the next round's records (**no rewrite — append-only**)"
(`corpus/lessons/round-41-verifier-spotcheck.md` §5 item 1), and the L1's own claims erratum 1 (E2,
committed `27e18d2a`) confirms it: the committed r41 duplication is KEPT as history and J11's positive
limb reads "every verbatim-duplicated `Correction (round <n>)` line-block per file is either absent OR
is named line-range-exactly by an appended `Correction-dedup (round 42)` marker". A check that demanded
the duplication be deleted would be unsatisfiable under the append-only discipline and would fail the
round for a repair the lane is not permitted to make.

**A marker never makes the defect disappear.** The payload keeps reporting the defect itself
(`dups=`, `dup-distinct=`, `dup-lines=`, `dup-records=`) alongside the exception
(`recorded=`, `marker-covers=covered/total`). At the round-42 landing the payload is
`dups=4 dup-distinct=4 recorded=1 marker-covers=4/4 unexcused=0` — the duplication is **detected and
named**, not silently passed.

**Fence-aware, by the lane's own convention** (r41-closure.sh I4): a `Correction (round <n>)` line
inside a CommonMark fence is not a line-anchored correction. Fenced correction-shaped lines are counted
separately and reported in `fenced=`, so a fence-marked dedup is visible in the payload rather than
silent.

**Anchor discipline.** The correction anchor is `^Correction \(round [0-9]+\):` — a loose `^Correction`
anchor would also match the `Correction-dedup (round 42):` marker itself, and the marker must never be
counted as a correction line. Groups are counted **by content** (normalized body), never by position.

## The replay limb (the C1 kill-rule requirement)

`j11_replay_fixtures WORK TREE` builds the in-family defeat artifacts **from the tree under test** (so
it works unchanged at any Y), asserts that the tree under test is ACCEPTED, and asserts that every
defeat artifact is REJECTED with the payload naming the reopened limb. It prints one
`replay fixture=<name> rejected=1|0 limb=<field> payload=<...>` line per fixture and the summary
`replay fixtures=N failures=K`; it returns non-zero when any fixture is accepted or the tree under test
is rejected.

The eleven defeat artifacts (all measured rejected — transcript §6):

| fixture | defect re-opened | rejected limb |
|---|---|---|
| `nomarker` | a duplicated correction line with the marker stripped | `unexcused` |
| `stub-marker` | the marker reduced to `Correction-dedup (round 42):` | `marker-substantive` |
| `marker-names-no-line` | the marker's line references rewritten to a non-occurrence line | `marker-covers` |
| `marker-names-no-round` | the marker names round 99 | `unexcused` |
| `marker-not-appended` | the marker moved above the history it marks | `marker-appended` |
| `marker-fenced` | the marker quoted inside a fenced block (a mention, not a marker) | `marker` |
| `marker-covers-no-group` | the marker names a line that belongs to no group | `marker-covers` |
| `marker-names-partial-range` | the marker names only one occurrence line of a group | `marker-covers` |
| `unexcused-duplicate-in-log` | a duplicate appended to `LOG.md` (the SCORECARD marker cannot excuse it) | `unexcused` |
| `whitespace-variant-duplicate` | a whitespace variant of a `SHONEN.md` correction (only normalization can catch it) | `unexcused` |
| `open-fence` | an unterminated fence at EOF (corrections hidden from the count) | `eof-closed` |

`nomarker` is exactly the defeat the erratum names ("a synthetic duplication carrying NO marker must
be rejected"), and it is the artifact that makes the committed r41 state non-silent.

## Measured behaviour (transcript `ExecJ11Corr.transcript.txt`, all output teed)

- **§1 RED over the claims-freeze export** `0566bd66e93d429b2df8b6751cf10cbdc391e79b`:
  `records=3,corrections=31,distinct=27,dups=4,dup-distinct=4,dup-lines=4,dup-records=1,unexcused=4,fenced=0,eof-closed=3/3,marker=0,...,marker-covers=0/4,recorded=0 closed=0`, exit 1.
- **§2 RED over both negative-control refs** named in the frozen claims — base
  `5053a7f46de35784cff4b56756906e9014a38276` and round-41 judged head
  `1f7464612ac4c44e39886b82e812610d3c039b13`: identical red payloads, exit 1 each.
- **§3 GREEN over a scratch copy with the mandated marker appended** (the marker line taken byte-exact
  from `.ufo/waves/round-42/wave1/ScribeScorecard.round42.txt`):
  `unexcused=0,marker=1,marker-line=1629,marker-substantive=1,marker-appended=1,marker-rounds=41,marker-lines=1,marker-covers=4/4,recorded=1 closed=1`, exit 0.
- **§4 GREEN over the full planned landing** — the three scribe appends applied verbatim
  (`ScribeScorecard.round42.txt` → `SCORECARD.md`, `ScribeShonenLog.log-round42.txt` → `LOG.md`,
  `ScribeShonenLog.shonen-append.txt` → `SHONEN.md`): `corrections=33,...,marker-covers=4/4,recorded=1 closed=1`, exit 0.
- **§5 GREEN over the `ScribeCorrections.blocks.txt` BLOCK 1 carrier** (the same mandated sentence plus
  the base commit hash and the block sha256): exit 0 — the hash-embedded digit runs are correctly not
  read as line references.
- **§6 REPLAY** — `replay fixtures=12 failures=0`, exit 0.

The committed duplication itself was re-measured read-only: `git show HEAD:SCORECARD.md | grep -n
'^Correction (round 41):'` → `1602 1603 1604 1605 1607 1608 1609 1610`, and
`diff <(sed -n '1602,1605p') <(sed -n '1607,1610p')` → `IDENTICAL`.

Degenerate trees were also checked (all RED with distinct payloads, all in the receipt's evidence run):
a tree missing `SHONEN.md` (`records=2`), an emptied `SCORECARD.md` (`marker=0`), and a nonexistent tree
(`records=0`).

## Integration instructions for the L1

1. Land `ExecJ11Corr.sh` (it is self-contained; it sets **no** shell options, so sourcing it into
   `corpus/instruments/r42-closure.sh` cannot change the suite's behaviour — verified by sourcing it
   under `set -uo pipefail` alongside the suite's own `RECORDS`/`FENCE_AWK` globals, which were left
   untouched). Either `. <path>/ExecJ11Corr.sh` before the suite's `main`, or paste the `check_j11` /
   `j11_*` functions into the suite.
2. Register `J11` in the suite's `CHECK_IDS` / `PAYLOAD_ORDER` and add `check_j11` to the run order; the
   limb returns 0/1 and prints one payload, which is the shape the suite's `run_check` expects.
3. Wire the replay limb into the graded selftest: `j11_replay_fixtures "$WORK/j11-replay" "$EXPORT"`
   and require `replay fixtures=12 failures=0` — the suite's selftest must then print
   `selftest case=J11 mutants=<n>/<n> positive=pass payload-match=1 verdict=pass`.
4. **The record must carry the marker.** The limb is RED over any tree whose `SCORECARD.md` does not
   carry the appended `Correction-dedup (round 42)` line naming the duplicated lines. The mandated
   wording (already produced byte-exact by two scribe seats) is:

   ```
   Correction-dedup (round 42): duplicated Correction (round 41) blocks at SCORECARD.md lines 1602-1605 and 1607-1610 — the second occurrence is the stray; both kept as history.
   ```

   It must be **column 0**, **outside any fence**, and **appended** (its line number greater than the
   last pre-round-42 correction line in `SCORECARD.md`). The equivalent `Dedup note (round 42, ...)`
   spelling is accepted as the same marker class. Neither spelling begins `Correction (round <n>):`, so
   neither is counted as a correction line.

5. **The L1 should still land exactly ONE carrier.** Two carrier files exist in wave 1
   (`ScribeScorecard.round42.txt` line 6 and `ScribeCorrections.blocks.txt` line 3) and the scribe
   states that only one may be landed, so that `SCORECARD.md` carries a single dedup erratum. Measured
   for this receipt: **J11 is indifferent to that choice** — a tree carrying BOTH carriers is GREEN
   (`recorded=2`, `marker-covers=4/4`, `unexcused=0`, exit 0), because every qualifying marker
   contributes to the coverage union and each one names the same exact ranges. So a double landing is
   not a J11 blocker, but it would leave two dedup errata in the record and the `recorded=2` field
   makes it visible rather than silent. Landing one carrier remains the right hygiene.

## Scope, limits and risks

1. **Line numbers are read as the marker states them.** The limb verifies that the marker names the
   duplicated lines *exactly*; it does not independently re-derive the block's coordinates. If the
   block's coordinates ever shift (a rewrite of the history, which the append-only rule forbids), the
   marker must be updated with them, or J11 goes RED with `marker-covers=0/4`. This is deliberate: the
   marker is the record of the exception, and a stale marker must not pass.
2. **Fence-awareness is inherited, not invented.** A duplicated correction inside a fenced block is not
   counted as a duplicate (the lane's I4 convention). This is visible in `fenced=` but is an accepted
   escape: a fence-marked dedup would pass. It is reported, never silent.
3. **The `Dedup note (round 42, ...)` alternate spelling** is accepted for robustness (one scribe seat
   proposed it before the spec mandate was confirmed). It is the only spelling tolerance in the marker
   class; every substantive requirement (substantive text, appended, names the round, names the exact
   line range) still applies to it.
4. **Two carriers in the record are not a J11 blocker** (measured: a tree with both wave-1 carriers is
   GREEN, `recorded=2`), but the L1 should land one so the record carries a single dedup erratum.
5. **No mutation of the lane, the fleet root, or any sibling lane.** All writes are the three files
   named above in `.ufo/waves/round-42/wave1/` plus this seat's scratch. No `git`/`jj` mutating command
   was run anywhere; the only git calls were read-only (`rev-parse`, `log`, `show`, `status`, `archive`).
6. **No tool install and no network fetch** were needed: the limb is pure bash + `awk`/`sed`/`grep`
   already present on the host, and it reads nothing outside the tree under test. Nothing was installed,
   so there is no tool/version/channel row to report. The host-wide pacman pause was respected (no
   pacman transaction was run).
7. **Disk guard was green before the work started** (`/tmp` 5%, `/var/tmp` 36%, `/fast/scratch/hyaku` 27%
   free-use) and no heavy pass ran against a non-green guard.
8. **Scratch** `/fast/scratch/hyaku/kasegi-r42/ExecJ11Corr/` held the exports, the fixture trees and the
   replay work dirs; it was removed after the deliverables were copied into the wave dir.
9. **Not in this seat's scope, untouched:** the r42 suite itself, the C1/C2 counters, the `SKILL.md`
   registry rows, the lesson Gate block, and any J/Y hash claims. F24 / RFC 9116 was not re-mined and
   is not referenced as a candidate.

## Evidence index

- Deliverable bytes and hashes: the two `sha256sum` lines above (the installed limb's sha256 equals the
  transcript's recorded `limb-sha256`, so the transcript describes exactly the installed bytes).
- Commands and their real output: `.ufo/waves/round-42/wave1/ExecJ11Corr.transcript.txt` (§0 the
  committed duplication, §1 the red over the freeze export, §2 the two negative-control reds, §3 the
  green over the marker-appended copy, §4 the green over the full planned landing, §5 the green over the
  second carrier, §6 the twelve replay fixtures).
