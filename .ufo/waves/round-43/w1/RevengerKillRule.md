# RevengerKillRule — round 43: why the last three claims died, and where K14–K19 will die next

Seat `RevengerKillRule` (revenger, leaf). Lane `kasegi-shokunin`, base `ab98fac9dce87130bc4f66de89e30650d63943dc`,
frozen claims `.ufo/waves/round-43/claims.json` (sha256 `a4c03e1e8224549dd864eb7c6befa025cbb0e9b639c0233eeff2287dd15a6630`,
`frozen_at_utc=2026-10-28T16:37:07Z`). Receipt-only item; this file is my only lane write. I ran no lane gate as a
gate: I read committed bytes, and I executed the **uncommitted wave-1 limb deliverables** (`w1/ExecK*.sh`) in
`--export` mode over `git archive` extractions in my own scratch to observe behaviour. No lane byte was written by
any of those runs (`git -C … status --porcelain` shows only the round-43 untracked wave dir). I ran no mutating git.

What I read: `.ufo/waves/round-{40,41,42,43}/claims.json`; the three closures
`corpus/lessons/round-{40,41,42}-verifier-spotcheck.md`; the round-43 controls; the committed r40/r41/r42 receipts and
controls; the r42 suite's `check_j11` engine; the landed K14–K19 limbs and the graded-selftest case inventory.

---

## 1. Why each claim died

Verbatim clauses are from the frozen `kill_rule` of the round named; “bytes” are the committed bytes the clause fired
on; “believed” is what the author of those bytes asserted at the time, reconstructed from the same commit set.

| # | Claim, verdict | Clause that fired (verbatim) | Committed bytes it fired on | What the author believed | Closure lines |
|---|---|---|---|---|---|
| r40 C1 | depth:verifiability 4, **NOT VERIFIED** | “a committed fixture shows a check passing while its defect is present” | `.ufo/waves/round-40/wave2/RevC1Counters.defeats.txt` T2/T4/T7/T13/T14; `CritKillRule.h6-escapes.sh`; `MutH6H10.md` D2 | `corpus/lessons/round-40.md:216`: “**C1 — the suite holds at the verification ref; no live defect defeats a check.**” The lane treated its own surviving defeats as “routed to round 41”, i.e. as a queue item, not as evidence about C1 | `round-40-verifier-spotcheck.md:47` (NOT VERIFIED), `:51` (the clause), `:65–79` (the defeats), `:77–78` (“narrows the frozen clause after landing”), `:95` (“That is an overclaim”) |
| r40 C1 (second, independent) | same | R37: a Y-level selftest tally quoted with no transcript | `SCORECARD.md`/`LOG.md`/`SHONEN.md` r40 lines and the report quote `--selftest --export-ref Y → cases=10 failures=0`; the receipt holds no selftest line and the only committed tally is over scratch Y′ | believed a run performed in scratch is quotable as a Y-level result | `round-40-verifier-spotcheck.md:182` (D2) |
| r41 C1 | depth:verifiability 4, **NOT VERIFIED** | “the Y export prints closed!=12/12 or exit!=0”; and “a committed fixture shows a check passing while the defect it names is present” | `.ufo/waves/round-41/final-gates/all-gates.txt`: `selftest cases=12 failures=6`, `closed=10/12 exit=1` (re-read by me at `0f64b8c5`); I1/I3 defeats in `wave2/CritC1KillRule.md`, `wave2/RevC1Counters.md` | the lane already graded C1 “not verified” honestly — the claim still fails its own after-state, which is what “held” was supposed to be measured by | `round-41-verifier-spotcheck.md:50–51`, `:58`, `:64` |
| r41 C2 | coverage 8, **NOT VERIFIED** | *no frozen clause fired* — every counter in the predicate was reached | shared RFC 9116 ground with kake's `security-txt-publishing.md`, found by `CritProvinceBoundary` (committed in `kasegi-r41-falsify-results.json`); L0 question at `.ufo/l0-questions.md` | believed a predicate made of counters is a sufficient definition of “coverage improved”; the axis rule that killed it (non-duplication of sibling ground) is not expressible in the counters | `round-41-verifier-spotcheck.md:88–94` (“Every frozen counter is reached. The claim is nevertheless **NOT VERIFIED**”) |
| r42 C1, C2 | **met / met** | — | — | — | `round-42-verifier-spotcheck.md:191`, `:314` |
| r42 RD42-1 | record defect | stale literal vs live re-derivation | `SCORECARD.md:1634` says “the r42 suite at Y prints `J11 payload=corrections=33,…`”; the Y receipt's own line prints `corrections=34` (re-read by me: `git show b2c49ea5:…/all-gates.txt` line 16) | believed 33 was the current measurement. **The correction line itself raised the count**: the sentence that records the number is a `Correction (round <n>)` line, which `check_j11` counts | `round-42-verifier-spotcheck.md:173` |
| r42 RD42-2 | never-true narrative | — | `LOG.md:1804`: “wave 2 `kasegi-r42-falsify` 36 seats dispatched …; dead seats counted from `wave2-results.json`”; no `wave2-results.json`, no `.ready.dispatched`, zero seats | believed **handoff = dispatch**: `wave2-dispatch.json` with 36 `taskCall.tasks` plus a 175-byte `.ready` was written and committed, so “dispatched” was treated as true | `round-42-verifier-spotcheck.md:174`, `:191` (“wave 2 … **never taken**”) |
| r42 RD42-3 | never-true narrative | — | `corpus/lessons/round-42.md:11,16`: “wave 2 dispatched 36 seats; the round total is 100”; “36 seats, 32 attack roles” | same belief, carried into the lesson, where it was written as a present-tense round total | `round-42-verifier-spotcheck.md:175` |
| r42 RD42-4 | placeholder promise | — | `corpus/lessons/round-42.md:52` `## Wave-2 falsification`: “Appended when the round-42 falsify wave reports: …” | believed the wave would run later in the same round, so a forward-looking section was safe to commit | `round-42-verifier-spotcheck.md:176` |
| r42 RD42-5 | receipt granularity | — | quotes `closed=10/13`, `failures=3` at `de09313`; the only committed red transcript is `all-gates.pre-repair.txt` at `d238e36` = `9/13`, `failures=4` | believed a run performed in scratch counts as a record once it is quoted; it was never teed into the tree | `round-42-verifier-spotcheck.md:177` |
| r42 RD42-6 | timestamp hygiene | — | freeze label `2026-10-28T12:05:00Z`, 65 min after its containing commit (`11:00:01Z`), disclosed only by erratum 3 (real mtime `10:51:52Z`) | believed the label should record the intended/effective freeze instant, and that the erratum would carry the discrepancy | `round-42-verifier-spotcheck.md:178` |
| r42 RD42-8 | before-cell mismatch | — | `round-42/claims.json` C1 `before`: “the r41 suite at base prints `closed=10/12 exit=1`”; its cited control `.ufo/waves/round-42/c1-controls/do-nothing.txt` prints `closed=8/12 exit=1` (re-read by me) | believed the r41 suite's figure at **its own head** described the suite at **the r42 base**; the base carries commits after the r41 receipt, so the same suite prints 8/12 there | `round-42-verifier-spotcheck.md:297` |

### The three mechanisms behind all six deaths

**M1 — measured in one tree, asserted about another.** RD42-8 (r41-head figure used as a base figure), RD42-5 (scratch
run used as a committed record), RD42-6 (label from the intent, not the commit), and r40 D2 (scratch Y′ used as Y).
Every one is a number that was true *somewhere* and then became a property of a *different* export.

**M2 — the repair text re-enters the graded grammar (self-reference).** RD42-1 is the pure case: the `Correction
(round <n>)` line that reports the ledger is itself counted by the ledger, so the reported value is stale by exactly
the number of lines added after the measurement. The r42 author's 33 could not have been right at the tree that
contained it.

**M3 — the check's grammar is narrower than the defect's prose, so the repair can move the defect outside the check.**
RD42-3/4: the sentence was unbacked; the repair is another sentence. r41 C2: the counters were all met; the objection
was a rule the counters cannot express. The r42 “claim design lesson” states this for narrative; the closure for r41 C2
states it for axis scope.

Round 43's K14–K19 are M2/M3 instruments. The forecast below is where each one reproduces its parent defect.

---

## 2. K14–K19: the most likely repeat, the fixture that catches it

All “observed” lines below are real output from the landed `w1/ExecK*.sh` limbs run over an export I extracted with
`git archive` (base `ab98fac9` and lane HEAD `4cb6d4a`) into my scratch. Evidence log in §4. “Live” = what the limb
re-derived at that tree.

### K14 — `corrections=` literals (inherits RD42-1)

**Repeat.** The literal moves one file over, and the repair grammar doubles as the escape grammar.

- The frozen predicate scopes K14 to `SCORECARD.md/LOG.md/SHENON.md`. `SHENON.md` **does not exist**; the file is
  `SHONEN.md` (`ls SHENON.md` → `No such file or directory`; `SHONEN.md` carries 9 `Correction (round` lines). The limb
  correctly inherits `check_j11`'s `RECORDS` (`SHONEN.md`), so the limb and the frozen text disagree about their own
  scope, and no payload field says which list was used.
- The limb grades only those three files. The round-43 **lesson** — which will land as `corpus/lessons/round-43.md` —
  already states the live value three times in its draft (`ScribeLessonDraft.round-43-lesson.md:26,37`:
  “`corrections=33` against the suite's own live `corrections=34`”). At the tree where the round's own corrections are
  landed, the limb re-derives `live=corrections=35` (observed), so the lesson's “live” value is stale on arrival and
  nothing can see it:

  ```
  # tree = HEAD + ScribeCorrections.scorecard.txt appended; then a fabricated literal in the lesson
  K14 superseded=SCORECARD.md:1661 corrections=33 live=35
  K14 payload=literals=3,stale=0,superseded=2,live=corrections=35,groups=4 closed=1
  # corpus/lessons/round-43.md now contains "corrections=99": payload identical (literals=3)
  ```
- The second escape is in the limb itself: a stale literal carried on a `Correction (round 43)` line is auto-excused
  (`if not excused and is_marker and not line[:m.start()].endswith("live="): excused = True`), and a later marker that
  contains the literal verbatim also excuses earlier copies. A fabricated value is therefore laundered:

  ```
  K14 superseded=SCORECARD.md:1664 groups=9 live=4
  K14 payload=literals=5,stale=0,superseded=4,live=corrections=36,groups=4 closed=1   # corrections=99 accepted, silent
  ```
- The suite's **own K14 positive fixture** proves the laundering: it asserts “the value the suite re-derives at this
  export is `corrections=34`” while the limb at that same tree re-derives 35 — and grades it `closed=1`:

  ```
  K14 superseded=SCORECARD.md:1662 corrections=34 live=35
  K14 payload=literals=4,stale=0,superseded=3,live=corrections=35,groups=4 closed=1
  ```

**Fixture.** `k14-own-line`: a tree where `SCORECARD.md` carries `Correction (round 43): … corrections=99 …` **without**
the `live=` prefix, everything else identical to the positive fixture → the limb must print
`stale=SCORECARD.md:<l>:corrections=99 live=<n>` and `closed=0`. Companion `k14-lesson`: a tree whose
`corpus/lessons/round-43.md` carries `corrections=<wrong>` → must be red (add the lesson to the graded set, or freeze
the exclusion). Companion `k14-positive-rebuild`: regenerate the positive fixture by measure → append the marker →
quote nothing, and assert the fixture's own payload `live=` equals a fresh re-run.

### K15 — wave-dispatch narrative (inherits RD42-2/3)

**Repeat.** The sentence→evidence mapping is name-based, and the round's own results artifact may not be named what the
limb looks for. The wave registry is `wave=kasegi-r43-hyaku`, seats land in `.ufo/waves/round-43/w1/`, and the marker is
`w1.ready`; the limb resolves evidence as `wave<label>-results.json`, `<named-wave>-results.json`, or a seat-receipt
directory with the stated count. Nothing in the round-43 plan pins the results basename.

Observed: the limb is **sound on the historical defect and on the re-trigger** (the correction block is not re-collected):

```
# HEAD
K15 detail=LOG.md:1804 wave=kasegi-r42-falsify round=42 stated-seats=36 unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:11 … unbacked=no-evidence
K15 detail=corpus/lessons/round-42.md:16 … unbacked=no-evidence
K15 payload=sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0
# + ScribeCorrections.log.txt appended verbatim (which quotes the defect sentence): superseded=1, unbacked=2  ← no re-trigger
# + ScribeCorrections.lesson42.txt appended too:          unbacked=0, superseded=3, closed=1
```

The load-bearing naming, observed on a synthetic r43 sentence:

```
# sentence "one v2 wave `kasegi-r43-hyaku` 73 seats dispatched"; results at kasegi-r43-hyaku-results.json (73 results)
K15 payload=sentences=6,unbacked=0,superseded=3,mismatch=0 closed=1
# same tree, results renamed w1-results.json
K15 detail=LOG.md:1809 wave=kasegi-r43-hyaku round=43 stated-seats=73 unbacked=no-evidence
K15 payload=sentences=6,unbacked=1,superseded=3,mismatch=0 closed=0
```

**Fixture.** `k15-r43-name`: a LOG sentence naming `kasegi-r43-hyaku` with `73 seats`, and the results artifact under
the **other** candidate basename (`w1-results.json`) → must print `unbacked=1` (it does); then move the same bytes to
`kasegi-r43-hyaku-results.json` → must print `unbacked=0`. The fixture must also carry the `mismatch` arm: results
present with 72 results against a sentence stating 73 → red.

### K16 — placeholder promise (inherits RD42-4)

**Repeat.** The round writes a new lesson “in the shape of `corpus/lessons/round-42.md`” (scribe brief), and the promise
it writes is in a shape the clause grammar cannot parse — a comma or colon inside the subject, or the promise parked
after the section's opening blank line. The limb's payload has **no limit field**, so an unseen promise is a silent
pass, not a named limit; the round's own draft already carries `<pending: integration>` mid-section
(`ScribeLessonDraft.round-43-lesson.md:139,146`).

Observed:

```
# HEAD: the r42 promise is seen
payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0
# round-42.md corrected; then a NEW section in corpus/lessons/round-43.md:
#   ## Wave-3 falsification / "Appended when the round-43 falsify wave, produced by the harness, reports: …"
#   ## Gate / "…is `<pending: integration>` until the receipt prints."
payload=sections=494,promises=1,fenced=0,unresolved=0 closed=1    ← both promises invisible
```

Note also that this limb alone prints `payload=…` without the `K16 ` prefix (every other limb prints `K<n> payload=`);
the suite wrapper must add it or the `K<n> payload=` census breaks.

**Fixture.** `k16-comma-subject`: a new `## ` section in `corpus/lessons/round-43.md` whose opening stanza is
“Appended when the round-43 falsify wave, produced by the harness, reports: per-claim verdicts.” → must be
`unresolved=1 closed=0`, or the payload must carry `limit=comma-subject`. `k16-mid-section`: the same promise after
the first blank line → red, or `limit=mid-section`. A silent `closed=1` is the defect (observed).

### K17 — claims `before`/`after` literal (inherits RD42-8)

**Repeat.** Three concrete ways, all observed:

1. **The erratum lands in the wrong round's directory.** `superseded_by()` searches `os.path.dirname(claims.json)` —
   for the defective round-42 claim, `.ufo/waves/round-42/`. The round's erratum is authored as
   `.ufo/waves/round-43/claims-erratum-1.md` — the seat spec says so in as many words (“the L1 lands it at
   `.ufo/waves/round-43/claims-erratum-1.md`”, `w1-spec.json` item `ScribeClaimsErratum`), and the selftest's own
   positive builder writes the same path (`ExecSelftest19.sh:405`). Same bytes, two directories:

   ```
   # erratum in .ufo/waves/round-43/  (the authored path)
   K17 payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0
   # identical bytes as .ufo/waves/round-42/claims-erratum-5.md
   K17 payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1
   ```
   The suite's own K17 positive builder (`ExecSelftest19.sh:405`) writes the round-43 path, so **the K17 selftest
   positive cannot pass as authored** (observed `closed=0` with that exact fixture).

2. **`after` cells are not graded at all.** `ExecK17ClaimsBefore.sh:323`: `if field == "after": continue`. The frozen
   predicate says “every `closed=`/`failures=` literal in a claims.json `before`/`after` cell”. Observed: appending
   ``… The r43 control says `closed=99/99 exit=0`.`` to the round-43 **after** cell leaves `tokens=5` unchanged. So the
   round's own after-state (`closed=19/19`, `selftest cases=19 failures=0`) is ungraded — the r40 D2 class, inside the
   check meant to close RD42-8.

3. **Non-token numbers are invisible.** `TOKEN_RX = (closed|failures|cases)=(\d+)(?:/(\d+))?`. The round-43 frozen
   `before` cell says “the r43 suite is absent at base (exit 127)” while the control it cites prints `exit=2`
   (`c1-controls/do-nothing.txt:5`). That is RD42-8's shape — a number asserted beside a pointer that does not print it
   — already frozen into round 43, and K17 cannot see it (`tokens=5`, no `exit` row).

What K17 does grade, it grades correctly: a fabricated `closed=99/99` written into a **before** cell is
`result=unbacked` with both values printed.

**Fixture.** `k17-erratum-dir`: the positive erratum in `round-43/` naming a `round-42/claims.json` token → must be red
(it is); `k17-erratum-own-dir`: the same bytes in `round-42/` → green (it is) — and the selftest's positive case must
use the directory that makes its own claim green. `k17-after-cell`: a fabricated `closed=99/99` in an **after** cell →
must be unbacked (it is not). `k17-exit-token`: a before cell asserting `exit 127` against a control printing `exit=2`
→ must be red (it is not).

### K18 — quoted values vs committed transcripts (inherits RD42-5)

**Repeat.** Two ways, one already live:

1. **The append-only records are out of K18's quote scope.** Its declared scope is `corpus/lessons/round-42*`,
   `corpus/lessons/round-43*` and top-level `.ufo/waves/round-43/*.md`; `SCORECARD.md`, `LOG.md` and `SHONEN.md` are
   “supersede-marker sources, not quote sources”. But those are exactly where the round writes its headline numbers
   (`ScribeScorecardRound43.append.md`: `closed=19/19`, `selftest cases=19 failures=0`, `closed=13/19`; same in
   `ScribeShonenLines.append.md`). Observed: appending a false
   “the suite prints closed=1/19 exit=1 and selftest cases=19 failures=7” to `SCORECARD.md` leaves K18's counts
   **unchanged** (`quotes=24` before and after). That is the r40 D2 defect (Y-level tally in the append-only records
   with no transcript), unfixed.

2. **The RD42-5 repair does not bind the quoted tokens.** The delivered `w1/ExecTranscriptDe0931.txt` prints
   `closed=12/13 exit=1` and `selftest cases=13 failures=1`. The record quotes `closed=10/13` and
   `selftest cases=13 failures=3`. With that transcript landed:

   ```
   K18 payload=quotes=24,bound=20,report-only=0,superseded=3,unbound=1 closed=0
   K18 unbound token=selftest cases=13 failures=3 at corpus/lessons/round-42-verifier-spotcheck.md:65
   ```
   The supersede line names `failures=3`, but the token is the pair `selftest cases=13 failures=3`; only a token-exact
   naming (or a transcript printing the pair) closes it. A synthetic transcript printing both lines does close it
   (`bound=24, unbound=0, closed=1`), which is why the positive fixture passes while the real one does not.

3. **And the transcript is not reproducible from the bytes it names.** I ran the pinned suite bytes over the pinned
   export: suite sha256 `d92c0de1…` = `git show de09313:corpus/instruments/r42-closure.sh` and = the tee's own
   `suite-sha256`; export `de09313`. My run prints **`closed=10/13 exit=1`** (matching the r42 closure's §9.3/§7
   figures), the delivered tee prints `closed=12/13 exit=1`. The differing lines are J1
   (`replay=RevC1Counters.md=accepted closed=0` in my run vs `=rejected closed=1` in the tee) and J10
   (`graded-lines=10 closed=0` vs `graded-lines=13 closed=1`). Both are checks that read state outside the export, so
   at least one ambient input (lane/work/cwd) is load-bearing: the artifact the round intends to land as its RD42-5
   transcript is a transcript of *some* run, not of the inputs it records.

**Fixture.** `k18-scope`: a `SCORECARD.md` line quoting a false `closed=`/`selftest cases=` pair → must be red (it is
not). `k18-pair-token`: a record quoting `selftest cases=13 failures=3` with a correction naming only `failures=3` →
must stay red (it does); the positive must name the pair. `k18-repro`: a check that the landed transcript's summary
lines equal a re-run of the named suite bytes over the named export (J1/J10 differ here — the fixture fails today).

### K19 — freeze-record ordering (inherits RD42-6)

**Repeat.** A self-consistent freeze record whose label postdates the containing commit. The frozen predicate compares
`frozen_at_utc` to the two controls' `measured-at=` and to the freeze record's own `frozen-at=`, plus the claims digest.
It never compares the label to the containing commit — the relation RD42-6 violated. The limb can do it, but only when
the caller supplies `<commit-utc>`, and the frozen claim does not require that argument.

Observed, on a tree where I moved `frozen_at_utc` **and** `frozen-at` to 53 minutes after the export's committer time
and recomputed `claims-sha256` (a consistent lie):

```
K19 payload=freeze=present,order=ok,sha=match closed=1          # no commit argument — the frozen predicate
K19 payload=freeze=present,order=bad,sha=match closed=0         # with 2026-10-28T16:37:11Z (committer)
```

For the record, round 43's own freeze commit `4cb6d4a` has author `2026-10-28T13:27:52-03` / committer `13:37:11-03`
and the label `16:37:07Z`; the label sits 9m15s **after** the author instant and 4s before the committer instant — the
same jj author-date inheritance artifact the r42 closure recorded for `0566bd6` (`round-42-verifier-spotcheck.md:178`).

**Fixture.** `k19-commit-order`: a tree whose freeze label is later than its own commit's committer instant by one
minute → must be `order=bad` without any extra argument. `k19-controls-refresh`: a control receipt whose `measured-at=`
is later than `frozen-at=` → red (a late re-measure of a control is a plausible integration move; the freeze predates
it). `k19-digest`: claims.json bytes changed after the freeze → `sha=mismatch`.

---

## 3. Ranking — the single most likely repeat

1. **K17, erratum in the wrong round directory.** It is not a risk, it is already committed: the scribe's erratum
   deliverable and the selftest's own positive builder both point at `.ufo/waves/round-43/claims-erratum-1.md`, and the
   limb resolves only in the *defective claim's* round dir. Observed: those exact bytes → `closed=0`; moved to
   `round-42/` → `closed=1`. If the round lands the erratum where it is authored, K17 is red at Y and C1 cannot reach
   `closed=19/19`; if it lands in `round-42/` (a new file, `claims-erratum-5.md`: `round-42/claims-erratum-1.md` already
   exists), K17 closes — but then the selftest's K17 positive and the round's own erratum path disagree and must be
   reconciled in `claims.json`'s erratum note, which is exactly the RD42-8 class again.
2. **K14, the stale `corrections=` literal relocated to the lesson.** Already drafted three times at
   `ScribeLessonDraft.round-43-lesson.md:26,37`, at a tree where the limb re-derives 35, in a file K14 does not read.
   The RD42-1 defect survives the round verbatim, one file over.
3. **K18, the headline numbers in `SCORECARD.md`/`LOG.md`/`SHONEN.md` are ungraded**, and the RD42-5 repair transcript
   neither binds its tokens nor reproduces its own run.

---

## 4. Evidence log

All runs from my scratch `S=/fast/scratch/hyaku/kasegi-r43/RevengerKillRule` (removed at the end, §6). Exports:
`git -C <lane> archive ab98fac9… | tar -x -C $S/base` and `… archive HEAD | tar -x -C $S/head`. Limbs sourced from
`.ufo/waves/round-43/w1/`; `check_k<n> <tree>` invoked directly.

| # | Command | Observed |
|---|---|---|
| E1 | `check_k14 $S/base` | `K14 stale=SCORECARD.md:1634 corrections=33 live=34` / `payload=literals=2,stale=1,superseded=0,live=corrections=34,groups=4 closed=0`, rc=1 |
| E2 | `check_k14 $S/head` | identical to E1 |
| E3 | `check_k14 head + ScribeCorrections.scorecard.txt` | `superseded=SCORECARD.md:1661 corrections=33 live=35` / `payload=literals=3,stale=0,superseded=2,live=corrections=35,groups=4 closed=1` |
| E4 | `check_k14` with `Correction (round 43): … corrections=99,groups=9 closed=1` appended | `superseded=SCORECARD.md:1664 groups=9 live=4` / `payload=literals=5,stale=0,superseded=4,live=corrections=36,groups=4 closed=1` |
| E5 | `check_k14` with the suite's own positive fixture line | `superseded=SCORECARD.md:1662 corrections=34 live=35` / `payload=literals=4,stale=0,superseded=3,live=corrections=35,groups=4 closed=1` |
| E6 | `check_k14` with `corrections=99` in `corpus/lessons/round-43.md` | payload identical to E3 (`literals=3`) |
| E7 | `check_k17 e43` (erratum in `.ufo/waves/round-43/`) | `payload=claims=21,tokens=5,verified=4,superseded=0,unbacked=1,quoted=2 closed=0` |
| E8 | `check_k17 e42` (same bytes as `round-42/claims-erratum-5.md`) | `payload=claims=21,tokens=5,verified=4,superseded=1,unbacked=0,quoted=2 closed=1` |
| E9 | `check_k17` with the selftest builder's own erratum text in `round-43/` | `superseded=0,unbacked=1 closed=0` |
| E10 | `check_k17` with `The r42 control says closed=99/99` in a before cell | `tokens=6, unbacked=2 closed=0`; detail prints both values |
| E11 | `check_k17` with ``closed=99/99`` added to the **after** cell | `tokens=5` unchanged; `superseded=1,unbacked=0 closed=1` |
| E12 | `check_k15 $S/head` | `sentences=5,unbacked=3,superseded=0,mismatch=0 closed=0` (LOG:1804, lesson:11, lesson:16) |
| E13 | `check_k15` + `ScribeCorrections.log.txt` | `unbacked=2,superseded=1 closed=0` |
| E14 | `check_k15` + both drafted corrections | `unbacked=0,superseded=3 closed=1` |
| E15 | `check_k15` + r43 sentence + `kasegi-r43-hyaku-results.json` | `sentences=6,unbacked=0 closed=1`; renamed `w1-results.json` → `unbacked=1 closed=0` |
| E16 | `check_k16 $S/head` | `payload=sections=491,promises=1,fenced=0,unresolved=1 closed=0` (no `K16 ` prefix) |
| E17 | `check_k16` after resolving r42 + comma-subject promise + mid-section `<pending:>` | `payload=sections=494,promises=1,fenced=0,unresolved=0 closed=1` |
| E18 | `check_k18 $S/head` | `quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0`; unbound at `round-42-verifier-spotcheck.md:65,177` |
| E19 | `check_k18` + a false `closed=1/19` / `cases=19 failures=7` line in `SCORECARD.md` | `quotes=24` unchanged (both runs) |
| E20 | `check_k18` + correction naming `failures=3` only | `unbound=1` = `selftest cases=13 failures=3` |
| E21 | `check_k18` + synthetic transcript printing both tokens | `bound=24,unbound=0 closed=1` |
| E22 | `check_k18` + the delivered `ExecTranscriptDe0931.txt` at `.ufo/waves/round-43/final-gates/r42-at-de09313.txt` | `bound=20,unbound=1 closed=0` |
| E23 | `check_k19 $S/head` / `… 2026-10-28T16:37:11Z` / `… 2026-10-28T16:27:52Z` | `order=ok closed=1` / `order=ok closed=1` / `order=bad closed=0` |
| E24 | `check_k19` on a self-consistent record whose label is 53 min after the commit | `order=ok,sha=match closed=1` without the argument; `order=bad closed=0` with `16:37:11Z` |
| E25 | `git show de09313:…/r42-closure.sh \| sha256sum` / `git show HEAD:…` | `d92c0de1e3b4…` / `fca5ae6237…`; the tee's `suite-sha256` is `d92c0de1…` |
| E26 | `bash <de09313 suite bytes> --export-ref de09313 --lane <lane> --work $S/repro/w2 --scratch-root $S/repro` | `closed=10/13 exit=1`; diff vs the delivered tee: J1 `accepted closed=0` vs `rejected closed=1`, J10 `graded-lines=10 closed=0` vs `graded-lines=13 closed=1` |
| E27 | `git show b2c49ea5:….ufo/waves/round-42/final-gates/all-gates.txt` line 16 | `J11 payload=corrections=34,… closed=1` |
| E28 | `git show ab98fac:.ufo/waves/round-42/c1-controls/do-nothing.txt` tail | `selftest cases=12 failures=8` / `closed=8/12 exit=1` |
| E29 | `git log -1 --format='%ad %cd' 4cb6d4a` + `cat .ufo/waves/round-43/freeze.txt` | author `13:27:52-03`, committer `13:37:11-03`; `frozen-at=2026-10-28T16:37:07Z`, `measured-at-max=2026-10-28T16:34:15Z` |
| E30 | `TOKEN_RX` in `ExecK17ClaimsBefore.sh:105`; `c1-controls/do-nothing.txt:5`; r43 `before` cell | `(closed\|failures\|cases)=(\d+)…` — no `exit=`; control prints `exit=2`; cell says `exit 127` |

---

## 5. Limits

- The **suite skeleton** (`ExecSuiteSkeleton`) had not landed when I finished, so the integration-level facts — whether
  `check_k19` is called with the export's committer time, whether the `K16 ` prefix is added, whether the nineteen
  lines are ordered — are unobserved [INFERENCE].
- K15's draft-correction behaviour is observed; its r43-naming behaviour is observed on a synthetic sentence, not on
  the round's real results artifact (none exists yet).
- I did not run the round-43 suite (it does not exist) and verified no claim. The limbs I executed are uncommitted
  deliverables and may change after this pass; the observed outputs are pinned to the bytes present at 13:40–14:05.
- E26 is one invocation shape (`--lane <lane>`, cwd = scratch). The tee does not record its own argv, so I cannot name
  which ambient input its run differed on; I can only show the two pinned inputs produce a different result and name
  the two lines that differ.

## 6. Housekeeping

- Writes: this receipt only, plus scratch under `S=/fast/scratch/hyaku/kasegi-r43/RevengerKillRule`.
- Scratch removed: `du -sh` at 11G → `rm -rf -- "$S"` → `test ! -e "$S"` exit 0. The parent
  `/fast/scratch/hyaku/kasegi-r43/` remains because it holds sibling seats' dirs, not mine.
- No mutating git, no pacman, no tool installs, no network fetches, no writes to any PATH directory, no edits to
  `claims.json`, the controls, the lane source tree, the fleet root, or `shokuknow`.
